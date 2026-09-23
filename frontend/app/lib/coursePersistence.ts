import { ApiError, getCourseState, saveCourseState, type CourseState, type CourseStateSnapshot } from "./api";

class CourseStateSyncConflict extends Error {}

// One instance owns the browser's course lock. All writes, including retries,
// pass through the same queue; a response can only acknowledge its own snapshot.
export class CoursePersistence {
  private dirty: boolean;
  private connected = false;
  private stopped = false;
  private paused = false;
  private recoveryRequired = false;
  private timer: ReturnType<typeof setTimeout> | undefined;
  private flight: Promise<void> | undefined;

  constructor(
    private state: CourseState,
    dirty: boolean,
    private revision: string | null,
    private readonly cache: (state: CourseState, dirty: boolean, revision: string | null) => void,
    private readonly apply: (state: CourseState) => void,
    private readonly error: (message: string) => void,
    private readonly requireRecovery: () => void,
  ) { this.dirty = dirty; }

  start() { this.schedule(0); }

  update(state: CourseState) {
    if (this.stopped || this.paused || JSON.stringify(state) === JSON.stringify(this.state)) return;
    this.state = state;
    this.dirty = true;
    this.persist();
    this.schedule(350);
  }

  private persist() {
    try { this.cache(this.state, this.dirty, this.revision); }
    catch { this.error("Браузер не смог сохранить локальную копию. Не закрывайте страницу до синхронизации."); }
  }

  private schedule(delay: number) {
    if (this.stopped || this.paused) return;
    clearTimeout(this.timer);
    this.timer = setTimeout(() => { void this.flush().catch(() => undefined); }, delay);
  }

  async flush(): Promise<void> {
    if (this.flight) return this.flight;
    if (this.stopped || this.paused) return;
    this.flight = this.synchronize();
    try { await this.flight; } finally { this.flight = undefined; }
  }

  private async synchronize() {
    try {
      if (!this.connected) {
        const server = await getCourseState();
        if (this.stopped) return;
        if (this.dirty && server.revision !== this.revision) {
          throw new CourseStateSyncConflict("Локальные изменения основаны на устаревшей версии прогресса. Загрузите более новую сохранённую версию.");
        }
        if (server.exists && server.state && !this.dirty) {
          this.state = server.state;
          this.revision = server.revision;
          this.apply(server.state);
          this.persist();
        } else if (!server.exists) {
          this.revision = null;
          this.dirty = true;
        }
        this.connected = true;
      }
      while (this.dirty && !this.stopped) {
        const snapshot = JSON.stringify(this.state);
        const saved = await saveCourseState(JSON.parse(snapshot) as CourseState, this.revision);
        if (this.stopped) return;
        this.revision = saved.revision;
        if (snapshot === JSON.stringify(this.state)) {
          this.dirty = false;
        }
        this.persist();
      }
      if (!this.stopped) this.error("");
    } catch (cause) {
      if (!this.stopped) {
        if (cause instanceof CourseStateSyncConflict || (cause instanceof ApiError && cause.status === 409)) {
          this.recoveryRequired = true;
          this.paused = true;
          this.requireRecovery();
          this.error(cause instanceof Error ? cause.message : "Прогресс изменён в другом сеансе.");
          throw cause;
        }
        this.error(cause instanceof Error ? cause.message : "Не удалось сохранить прогресс.");
        this.schedule(1_500);
      }
      throw cause;
    }
  }

  // Backup operations run only after pending autosaves finish. Restore returns
  // the new state, so the old React snapshot cannot overwrite restored data.
  async maintenance(operation: (revision: string | null) => Promise<CourseStateSnapshot | void>) {
    if (this.recoveryRequired) throw new Error("Синхронизация прогресса приостановлена. Перезагрузите страницу.");
    await this.flush();
    this.paused = true;
    clearTimeout(this.timer);
    try {
      const snapshot = await operation(this.revision);
      if (snapshot) {
        this.state = snapshot.state;
        this.revision = snapshot.revision;
        this.dirty = false;
        this.apply(snapshot.state);
        this.persist();
      }
    } catch (cause) {
      // A lost restore response can mean the transaction already committed.
      // Re-read before permitting any subsequent autosave of the old state.
      try {
        const server = await getCourseState();
        if (server.state) {
          this.state = server.state;
          this.revision = server.revision;
          this.dirty = false;
          this.apply(server.state);
          this.persist();
        }
      } catch {
        this.recoveryRequired = true;
        this.requireRecovery();
        this.error("Не удалось уточнить результат восстановления. Перезагрузите страницу перед продолжением.");
      }
      throw cause;
    } finally { this.paused = this.recoveryRequired; }
  }

  needsRecovery() { return this.recoveryRequired; }

  stop() { this.stopped = true; clearTimeout(this.timer); }
}
