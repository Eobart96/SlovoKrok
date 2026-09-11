import { getCourseState, saveCourseState, type CourseState } from "./api";

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
    private readonly cache: (state: CourseState, dirty: boolean) => void,
    private readonly apply: (state: CourseState) => void,
    private readonly error: (message: string) => void,
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
    try { this.cache(this.state, this.dirty); }
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
        if (server.exists && server.state && !this.dirty) {
          this.state = server.state;
          this.apply(server.state);
          this.persist();
        } else if (!server.exists) this.dirty = true;
        this.connected = true;
      }
      while (this.dirty && !this.stopped) {
        const snapshot = JSON.stringify(this.state);
        await saveCourseState(JSON.parse(snapshot) as CourseState);
        if (this.stopped) return;
        if (snapshot === JSON.stringify(this.state)) {
          this.dirty = false;
          this.persist();
        }
      }
      if (!this.stopped) this.error("");
    } catch (cause) {
      if (!this.stopped) {
        this.error(cause instanceof Error ? cause.message : "Не удалось сохранить прогресс.");
        this.schedule(1_500);
      }
      throw cause;
    }
  }

  // Backup operations run only after pending autosaves finish. Restore returns
  // the new state, so the old React snapshot cannot overwrite restored data.
  async maintenance(operation: () => Promise<CourseState | void>) {
    await this.flush();
    this.paused = true;
    clearTimeout(this.timer);
    try {
      const state = await operation();
      if (state) {
        this.state = state;
        this.dirty = false;
        this.apply(state);
        this.persist();
      }
    } catch (cause) {
      // A lost restore response can mean the transaction already committed.
      // Re-read before permitting any subsequent autosave of the old state.
      try {
        const server = await getCourseState();
        if (server.state) {
          this.state = server.state;
          this.dirty = false;
          this.apply(server.state);
          this.persist();
        }
      } catch {
        this.recoveryRequired = true;
        this.error("Не удалось уточнить результат восстановления. Перезагрузите страницу перед продолжением.");
      }
      throw cause;
    } finally { this.paused = this.recoveryRequired; }
  }

  needsRecovery() { return this.recoveryRequired; }

  stop() { this.stopped = true; clearTimeout(this.timer); }
}
