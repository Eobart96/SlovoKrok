"use client";

import { useRef, useState } from "react";
import { getCourseBackup, restoreCourseBackup, validateCourseBackup, type CourseBackupSummary } from "../lib/api";
import { type CourseSession } from "../hooks/useCourseSession";

function download(data: unknown, prefix: string) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = `${prefix}-${new Date().toISOString().replace(/[:.]/g, "-")}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);
}

export function CourseBackupPanel({ session, onRestored }: { session: CourseSession; onRestored: () => void }) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [preview, setPreview] = useState<CourseBackupSummary | null>(null);
  const [backup, setBackup] = useState("");
  const selection = useRef(0);
  const run = async (operation: () => Promise<void>) => {
    setBusy(true); setError(""); setMessage("");
    try { await operation(); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось обработать копию."); }
    finally { setBusy(false); }
  };
  const choose = async (file?: File) => {
    const ticket = ++selection.current;
    setPreview(null); setBackup(""); setError(""); setMessage("");
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { setError("Выберите файл размером до 10 МБ."); return; }
    setBusy(true);
    try {
      const text = await file.text();
      const summary = await validateCourseBackup(text);
      if (ticket === selection.current) { setBackup(text); setPreview(summary); }
    } catch (cause) {
      if (ticket === selection.current) setError(cause instanceof Error ? cause.message : "Не удалось проверить копию.");
    } finally { if (ticket === selection.current) setBusy(false); }
  };
  return <details className="course-backup">
    <summary>Резервная копия</summary>
    <p>Сохраните прогресс, словарь, созданные материалы и ответы в один файл. Настройки ИИ и ключи в него не входят.</p>
    <div className="course-backup-actions">
      <button type="button" disabled={busy} onClick={() => void run(async () => {
        await session.maintenance(async () => { download(await getCourseBackup(), "slovokrok-backup"); });
        setMessage("Файл резервной копии передан браузеру для скачивания.");
      })}>Скачать резервную копию</button>
      <label>Открыть копию <input type="file" accept=".json,application/json" disabled={busy} onChange={(event) => void choose(event.target.files?.[0])} /></label>
    </div>
    {preview && <div className="course-backup-preview">
      <p>Копия от {new Date(preview.exported_at).toLocaleString("ru-RU")}. Завершено тем: {preview.completed_topics}. Слов и фраз: {preview.counts.vocabulary ?? 0}. Созданных материалов: {(preview.counts.exercises ?? 0) + (preview.counts.readings ?? 0) + (preview.counts.homework ?? 0)}.</p>
      <p>{preview.has_state ? "Прогресс будет заменён данными из файла. " : "В этой копии нет прогресса; текущий прогресс сохранится. "}Материалы добавятся к существующим. История уже имеющихся слов сохранится. Перед восстановлением будет скачана копия текущих данных.</p>
      <button type="button" disabled={busy} onClick={() => {
        if (!window.confirm("Восстановить выбранную копию? Если в ней есть прогресс, он заменит текущий.")) return;
        void run(async () => {
          await session.maintenance(async () => {
            download(await getCourseBackup(), "slovokrok-before-restore");
            return (await restoreCourseBackup(backup)).state ?? undefined;
          });
          setPreview(null); setBackup(""); onRestored(); setMessage("Копия восстановлена.");
        });
      }}>Восстановить выбранную копию</button>
    </div>}
    {busy && <p role="status">Обрабатываю резервную копию…</p>}
    {message && <p role="status">{message}</p>}
    {error && <p role="alert">{error}</p>}
  </details>;
}
