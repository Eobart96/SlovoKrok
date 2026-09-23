"use client";

import { type SyntheticEvent, useState } from "react";

import {
  clearTutorTranslationHistory,
  deleteTutorTranslationHistoryEntry,
  getTutorTranslationHistory,
  type TutorTranslationHistoryEntry,
} from "../lib/api";

const pageSize = 50;

export function CourseTranslationHistory() {
  const [entries, setEntries] = useState<TutorTranslationHistoryEntry[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(false);
  const [message, setMessage] = useState("");

  const loadHistory = async (beforeId?: number) => {
    setLoading(true);
    setMessage("");
    try {
      const page = await getTutorTranslationHistory(pageSize, beforeId);
      setEntries((current) => beforeId ? [...current, ...page] : page);
      setHasMore(page.length === pageSize);
      setLoaded(true);
    } catch (cause) {
      setMessage(cause instanceof Error ? cause.message : "Не удалось загрузить историю переводчика.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = (event: SyntheticEvent<HTMLDetailsElement>) => {
    if (event.currentTarget.open && !loaded && !loading) void loadHistory();
  };

  const deleteEntry = async (historyId: number) => {
    setMessage("");
    try {
      await deleteTutorTranslationHistoryEntry(historyId);
      setEntries((current) => current.filter((entry) => entry.id !== historyId));
      setMessage("Запись перевода и связанные вопросы удалены.");
    } catch (cause) {
      setMessage(cause instanceof Error ? cause.message : "Не удалось удалить запись.");
    }
  };

  const clearHistory = async () => {
    if (!window.confirm("Удалить всю историю переводов, вопросов и ответов? Это действие нельзя отменить.")) return;
    setLoading(true);
    setMessage("");
    try {
      const result = await clearTutorTranslationHistory();
      setEntries([]);
      setHasMore(false);
      setMessage(`Удалено переводов: ${result.translations_deleted}; вопросов: ${result.questions_deleted}.`);
    } catch (cause) {
      setMessage(cause instanceof Error ? cause.message : "Не удалось очистить историю.");
    } finally {
      setLoading(false);
    }
  };

  return <details className="course-translation-history" onToggle={handleToggle}>
    <summary>История переводчика</summary>
    <div className="course-translation-history-body">
      <p>Здесь видны данные, которые переводчик автоматически сохраняет локально: исходный текст, перевод, пояснения, провайдер, вопросы и ответы.</p>
      <div className="course-test-actions">
        <button type="button" onClick={() => void loadHistory()} disabled={loading}>{loading ? "Загружаю…" : "Обновить историю"}</button>
        <button className="course-test-reset" type="button" onClick={() => void clearHistory()} disabled={loading || entries.length === 0}>Очистить всю историю</button>
      </div>
      {message && <p role="status">{message}</p>}
      {!loading && entries.length === 0 && !message && <p>История пока пуста.</p>}
      <div className="course-translation-history-list">
        {entries.map((entry) => <article key={entry.id}>
          <header>
            <strong>#{entry.id} · {entry.direction === "ru-sk" ? "RU → SK" : "SK → RU"}</strong>
            <small>{new Date(entry.created_at).toLocaleString("ru-RU")} · ИИ {entry.provider}</small>
          </header>
          <dl>
            <div><dt>Исходный текст</dt><dd>{entry.source_text}</dd></div>
            <div><dt>Перевод</dt><dd>{entry.translation}</dd></div>
            {entry.alternatives.length > 0 && <div><dt>Варианты</dt><dd>{entry.alternatives.join(" · ")}</dd></div>}
            {entry.note && <div><dt>Пояснение</dt><dd>{entry.note}</dd></div>}
          </dl>
          {entry.questions.length > 0 && <section>
            <strong>Вопросы и ответы</strong>
            {entry.questions.map((item) => <div key={item.id}>
              <p><b>Вопрос:</b> {item.question}</p>
              <p><b>Ответ:</b> {item.answer}</p>
              <small>ИИ {item.provider} · {new Date(item.created_at).toLocaleString("ru-RU")}</small>
            </div>)}
          </section>}
          <button className="course-test-reset" type="button" onClick={() => void deleteEntry(entry.id)}>Удалить запись</button>
        </article>)}
      </div>
      {hasMore && <button type="button" onClick={() => void loadHistory(entries.at(-1)?.id)} disabled={loading}>{loading ? "Загружаю…" : "Показать ещё"}</button>}
    </div>
  </details>;
}
