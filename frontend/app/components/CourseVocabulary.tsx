"use client";

import { useEffect, useMemo, useState } from "react";

import { a1CourseModules, allA1Lessons } from "../data/a1Course";
import { ankiVocabularyText, learnedVocabularySeeds, vocabularyExportContent, type VocabularyExportDirection, type VocabularyExportFormat } from "../data/courseVocabulary";
import { filterKnownLessonSlugs } from "../data/courseEngine";
import { vocabularySections } from "../data/vocabularySections";
import { reviewCourseVocabulary, syncCourseVocabulary, type CourseVocabularyItem, type CourseVocabularySeed, type VocabularyRating } from "../lib/api";

export function contentVocabulary(completedLessonSlugs: string[]): CourseVocabularySeed[] {
  return learnedVocabularySeeds(allA1Lessons, filterKnownLessonSlugs(a1CourseModules, completedLessonSlugs));
}

function isSentenceItem(item: Pick<CourseVocabularyItem, "lesson_slug">): boolean {
  return item.lesson_slug.startsWith("additional-vocabulary:expanded-sentences-");
}

type ExportContent = "all" | "words" | "sentences";

function safeFilenamePart(value: string): string {
  return value.trim().toLocaleLowerCase("ru").replace(/[<>:"/\\|?*]+/g, "").replace(/\s+/g, "-") || "all";
}

export function CourseVocabulary({ completedLessonSlugs }: { completedLessonSlugs: string[] }) {
  const [items, setItems] = useState<CourseVocabularyItem[]>([]);
  const [filter, setFilter] = useState("");
  const [visibleLimit, setVisibleLimit] = useState(200);
  const [exportScope, setExportScope] = useState<"opened" | "section">("opened");
  const [exportContent, setExportContent] = useState<ExportContent>("all");
  const [exportFormat, setExportFormat] = useState<VocabularyExportFormat>("anki");
  const [exportDirection, setExportDirection] = useState<VocabularyExportDirection>("slovak-russian");
  const [loading, setLoading] = useState(true);
  const [reviewingId, setReviewingId] = useState<number | null>(null);
  const [revealedId, setRevealedId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [now, setNow] = useState(() => Date.now());
  const completedKey = JSON.stringify(completedLessonSlugs);
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 30_000);
    return () => window.clearInterval(timer);
  }, []);
  useEffect(() => {
    let cancelled = false;
    const slugs = JSON.parse(completedKey) as string[];
    const seeds = contentVocabulary(slugs);
    const order = new Map(seeds.map((item, index) => [`${item.lesson_slug}:${item.word}`, index]));
    const availableSources = new Set(seeds.map((item) => item.lesson_slug));
    setLoading(true); setError("");
    void syncCourseVocabulary(seeds)
      .then((stored) => { if (!cancelled) setItems(stored.filter((item) => availableSources.has(item.lesson_slug)).sort((left, right) => (order.get(`${left.lesson_slug}:${left.word}`) ?? Number.MAX_SAFE_INTEGER) - (order.get(`${right.lesson_slug}:${right.word}`) ?? Number.MAX_SAFE_INTEGER))); })
      .catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Не удалось загрузить слова."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [completedKey]);
  const sections = useMemo(() => {
    const available = new Set(items.map((item) => item.lesson_title));
    return vocabularySections.map((section) => section.title).filter((title) => available.has(title));
  }, [items]);
  const visible = filter ? items.filter((item) => item.lesson_title === filter) : items;
  const displayed = visible.slice(0, visibleLimit);
  const openedWords = items.filter((item) => !isSentenceItem(item));
  const openedSentences = items.filter(isSentenceItem);
  const exportScopeItems = exportScope === "section" && filter ? visible : items;
  const exportItems = exportContent === "words"
    ? exportScopeItems.filter((item) => !isSentenceItem(item))
    : exportContent === "sentences"
      ? exportScopeItems.filter(isSentenceItem)
      : exportScopeItems;
  const isDue = (item: CourseVocabularyItem) => !item.next_review_at || Date.parse(item.next_review_at) <= now;
  const due = visible.filter(isDue);
  const card = due[0];
  const revealed = card && revealedId === card.id;
  const review = async (item: CourseVocabularyItem, rating: VocabularyRating) => {
    setReviewingId(item.id); setError(""); setNotice("");
    try {
      const updated = await reviewCourseVocabulary(item.id, rating);
      setItems((current) => current.map((candidate) => candidate.id === item.id ? updated : candidate));
      setRevealedId(null); setNow(Date.now());
      setNotice(rating === "again" ? "Вернёмся к этой карточке через 10 минут." : "Повторение сохранено.");
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось сохранить повторение."); }
    finally { setReviewingId(null); }
  };
  const download = (downloadItems: CourseVocabularyItem[], filename: string) => {
    const text = ankiVocabularyText(downloadItems);
    const url = URL.createObjectURL(new Blob(["\ufeff" + text], { type: "text/plain;charset=utf-8" }));
    const link = document.createElement("a"); link.href = url; link.download = filename; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  };
  const downloadCustomExport = () => {
    const exported = vocabularyExportContent(exportItems, exportFormat, exportDirection);
    const scope = exportScope === "section" && filter ? `section-${safeFilenamePart(filter)}` : "opened";
    const filename = `slovak-a1-${exportContent}-${scope}-${exportDirection}.${exported.extension}`;
    const prefix = exported.extension === "json" ? "" : "\ufeff";
    const url = URL.createObjectURL(new Blob([prefix + exported.content], { type: exported.mimeType }));
    const link = document.createElement("a"); link.href = url; link.download = filename; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  };
  return <section className="course-exercises course-vocabulary" aria-labelledby="course-vocabulary-title">
    <div className="course-section-heading"><div><span>Личный словарь</span><h3 id="course-vocabulary-title">Слова</h3></div><p>Слова и фразы открываются по мере прохождения курса и собраны по смысловым разделам. Их можно повторять или выгрузить карточками в Anki.</p></div>
    <div className="course-vocabulary-actions">
      <span>{visible.length} карточек</span>
      <div className="course-vocabulary-downloads">
        <button type="button" onClick={() => download(visible, `${filter || "slovak-a1-all"}.txt`)} disabled={!visible.length}>{filter ? "Скачать раздел" : "Скачать всё"}</button>
        <button type="button" onClick={() => download(openedWords, "slovak-a1-words.txt")} disabled={!openedWords.length}>Скачать слова ({openedWords.length})</button>
        <button type="button" onClick={() => download(openedSentences, "slovak-a1-sentences.txt")} disabled={!openedSentences.length}>Скачать предложения ({openedSentences.length})</button>
      </div>
    </div>
    <details className="course-vocabulary-export">
      <summary>Другие варианты скачивания</summary>
      <div className="course-vocabulary-export-grid">
        <label>Что скачать<select value={exportContent} onChange={(event) => setExportContent(event.target.value as ExportContent)}><option value="all">Слова и предложения</option><option value="words">Только слова</option><option value="sentences">Только предложения</option></select></label>
        <label>Объём<select value={exportScope} onChange={(event) => setExportScope(event.target.value as "opened" | "section")}><option value="opened">Весь открытый словарь</option><option value="section" disabled={!filter}>Выбранный раздел{filter ? `: ${filter}` : ""}</option></select></label>
        <label>Направление<select value={exportDirection} onChange={(event) => setExportDirection(event.target.value as VocabularyExportDirection)}><option value="slovak-russian">Словацкий → русский</option><option value="russian-slovak">Русский → словацкий</option></select></label>
        <label>Формат<select value={exportFormat} onChange={(event) => setExportFormat(event.target.value as VocabularyExportFormat)}><option value="anki">Anki TXT — табуляция</option><option value="text">Обычный TXT — стрелка</option><option value="csv">CSV — таблица</option><option value="json">JSON — данные</option></select></label>
      </div>
      <div className="course-vocabulary-export-footer"><span>Будет скачано: {exportItems.length} карточек</span><button type="button" onClick={downloadCustomExport} disabled={!exportItems.length}>Скачать выбранный вариант</button></div>
    </details>
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {notice && <p role="status">{notice}</p>}
    {loading ? <p>Загружаю словарь…</p> : !completedLessonSlugs.length ? <p className="course-empty">Завершите первую тему — её слова появятся здесь.</p> : <>
      <div className="course-vocabulary-tags" aria-label="Разделы словаря"><button type="button" className={!filter ? "active" : ""} onClick={() => { setFilter(""); setVisibleLimit(200); setRevealedId(null); }}>Все разделы</button>{sections.map((title) => <button type="button" className={filter === title ? "active" : ""} key={title} onClick={() => { setFilter(title); setVisibleLimit(200); setRevealedId(null); }}>{title}</button>)}</div>
      <section className="course-vocabulary-learned" aria-labelledby="course-vocabulary-list-title">
        <div><h4 id="course-vocabulary-list-title">Изученные слова и фразы</h4><small>Файл для Anki: словацкий текст и русский перевод разделены табуляцией.</small></div>
        <div className="course-vocabulary-list">{displayed.map((item) => <article key={item.id}><div><strong lang="sk">{item.word}</strong><span>{item.translation}</span>{item.example && item.example !== item.word && <small lang="sk">{item.example}</small>}</div><span>{item.lesson_title}</span></article>)}</div>
        {displayed.length < visible.length && <button type="button" onClick={() => setVisibleLimit((current) => current + 200)}>Показать ещё ({visible.length - displayed.length})</button>}
      </section>
      {card ? <section className="course-vocabulary-due" aria-label="Повторение слов">
        <div><strong>Время повторить</strong><span>{due.length} элементов</span></div>
        <article key={card.id}>
          <strong lang="sk">{card.word}</strong>
          {revealed ? <>
            <span>{card.translation}</span>
            {card.example && card.example !== card.word && <small lang="sk">{card.example}</small>}
            <div className="course-review-ratings">
              <button type="button" disabled={reviewingId !== null} onClick={() => void review(card, "again")}>Не вспомнил</button>
              <button type="button" disabled={reviewingId !== null} onClick={() => void review(card, "hard")}>С трудом</button>
              <button type="button" disabled={reviewingId !== null} onClick={() => void review(card, "easy")}>Легко</button>
            </div>
          </> : <button type="button" onClick={() => setRevealedId(card.id)}>Показать перевод</button>}
        </article>
      </section> : <p role="status">На сейчас повторение завершено.</p>}
    </>}
  </section>;
}
