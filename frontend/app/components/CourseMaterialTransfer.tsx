"use client";

import { useState } from "react";

import { exportCourseMaterials, getBasicCourseMaterials, importCourseMaterials } from "../lib/api";


function downloadMaterials(data: unknown) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = `slovokrok-course-materials-${new Date().toISOString().replace(/[:.]/g, "-")}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);
}


export function CourseMaterialTransfer({ onImported }: { onImported: () => Promise<void> | void }) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const addBasicPack = async () => {
    setBusy(true); setMessage(""); setError("");
    try {
      const result = await importCourseMaterials(await getBasicCourseMaterials());
      await onImported();
      const imported = result.exercises.imported + result.readings.imported + result.homework.imported;
      const skipped = result.exercises.skipped + result.readings.skipped + result.homework.skipped;
      setMessage(`Базовый пакет: добавлено ${imported}, уже были в базе ${skipped}. Задания тем появятся после их завершения.`);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось добавить базовый пакет."); }
    finally { setBusy(false); }
  };

  const exportFile = async () => {
    setBusy(true); setMessage(""); setError("");
    try {
      const collection = await exportCourseMaterials();
      downloadMaterials(collection);
      const total = collection.exercises.length + collection.readings.length + collection.homework.length;
      setMessage(`Файл создан: ${total} заданий.`);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось создать файл заданий."); }
    finally { setBusy(false); }
  };

  const importFile = async (file?: File) => {
    if (!file) return;
    setMessage(""); setError("");
    if (file.size > 10 * 1024 * 1024) { setError("Выберите файл заданий размером до 10 МБ."); return; }
    setBusy(true);
    try {
      const result = await importCourseMaterials(JSON.parse(await file.text()) as unknown);
      await onImported();
      const imported = result.exercises.imported + result.readings.imported + result.homework.imported;
      const skipped = result.exercises.skipped + result.readings.skipped + result.homework.skipped;
      setMessage(`Добавлено: ${imported}. Уже были в базе: ${skipped}.`);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось открыть файл заданий."); }
    finally { setBusy(false); }
  };

  return <>
    <div className="course-reading-transfer"><div><strong>Общий базовый пакет A1</strong><small>83 темы: по 20 упражнений, 2 текста и 2 домашних задания. Без личного профиля и запросов к ИИ. Повторное добавление пропустит совпадающие задания.</small></div><div><button type="button" disabled={busy} onClick={() => void addBasicPack()}>{busy ? "Обрабатываю…" : "Добавить базовый пакет"}</button><a href="/task-packs/slovokrok-a1-basic-v1.json" download="slovokrok-a1-basic-v1.json">Скачать JSON</a></div></div>
    <div className="course-reading-transfer"><div><strong>Файл заданий</strong><small>Один файл переносит упражнения, тексты и домашние задания. Личные ответы и оценки в него не входят.</small></div><div><button type="button" disabled={busy} onClick={() => void exportFile()}>{busy ? "Обрабатываю…" : "Скачать задания"}</button><label>Загрузить задания<input type="file" accept=".json,application/json" disabled={busy} onChange={(event) => { const file = event.currentTarget.files?.[0]; event.currentTarget.value = ""; void importFile(file); }} /></label></div></div>
    {message && <p className="course-persistence-success" role="status">{message}</p>}
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
  </>;
}
