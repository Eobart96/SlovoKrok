"use client";

import { useEffect, useMemo, useState } from "react";

import { a1CourseModules, allA1Lessons } from "../data/a1Course";
import { lessonVocabulary } from "../data/courseVocabulary";
import { filterKnownLessonSlugs } from "../data/courseEngine";
import { reviewCourseVocabulary, syncCourseVocabulary, type CourseVocabularyItem, type CourseVocabularySeed, type VocabularyRating } from "../lib/api";

export function contentVocabulary(completedLessonSlugs: string[]): CourseVocabularySeed[] {
  const completed = new Set(filterKnownLessonSlugs(a1CourseModules, completedLessonSlugs));
  const result: CourseVocabularySeed[] = [];
  for (const lesson of allA1Lessons) {
    if (!completed.has(lesson.slug)) continue;
    for (const item of lessonVocabulary(lesson)) result.push({ lesson_slug: lesson.slug, lesson_title: lesson.title, ...item, example: item.example ?? null });
  }
  return [...new Map(result.map((item) => [`${item.lesson_slug}:${item.word}`, item])).values()];
}

export function CourseVocabulary({ completedLessonSlugs }: { completedLessonSlugs: string[] }) {
  const [items, setItems] = useState<CourseVocabularyItem[]>([]);
  const [filter, setFilter] = useState("");
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
    setLoading(true); setError("");
    void syncCourseVocabulary(contentVocabulary(slugs))
      .then((stored) => { if (!cancelled) setItems(stored.filter((item) => slugs.includes(item.lesson_slug))); })
      .catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Не удалось загрузить слова."); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [completedKey]);
  const topics = useMemo(() => [...new Map(items.map((item) => [item.lesson_slug, item.lesson_title])).entries()], [items]);
  const visible = filter ? items.filter((item) => item.lesson_slug === filter) : items;
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
  const download = () => {
    const text = visible.map((item) => `${item.translation} — ${item.word}`).join("\r\n");
    const url = URL.createObjectURL(new Blob(["\ufeff" + text], { type: "text/plain;charset=utf-8" }));
    const link = document.createElement("a"); link.href = url; link.download = `${filter || "slovak-a1-words"}.txt`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  };
  return <section className="course-exercises course-vocabulary" aria-labelledby="course-vocabulary-title">
    <div className="course-section-heading"><div><span>Личный словарь</span><h3 id="course-vocabulary-title">Слова</h3></div><p>Слова открываются после завершения темы. Сначала вспомните перевод, затем проверьте себя.</p></div>
    <div className="course-vocabulary-actions"><button type="button" onClick={download} disabled={!visible.length}>Скачать .txt</button></div>
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {notice && <p role="status">{notice}</p>}
    {loading ? <p>Загружаю словарь…</p> : !completedLessonSlugs.length ? <p className="course-empty">Завершите первую тему — её слова появятся здесь.</p> : <>
      <div className="course-vocabulary-tags"><button type="button" className={!filter ? "active" : ""} onClick={() => { setFilter(""); setRevealedId(null); }}>Все</button>{topics.map(([slug, title]) => <button type="button" className={filter === slug ? "active" : ""} key={slug} onClick={() => { setFilter(slug); setRevealedId(null); }}>{title}</button>)}</div>
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
      <details className="course-vocabulary-all"><summary>Все слова и переводы ({visible.length})</summary>
        <div className="course-vocabulary-list">{visible.map((item) => <article key={item.id}><div><strong><span>{item.translation}</span> — <span lang="sk">{item.word}</span></strong>{item.example && item.example !== item.word && <small lang="sk">{item.example}</small>}</div><span>{item.review_count === 0 ? "Новое" : isDue(item) ? "К повторению" : item.next_review_at ? `Повторить ${new Date(item.next_review_at).toLocaleString("ru-RU", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })}` : "К повторению"}</span></article>)}</div>
      </details>
    </>}
  </section>;
}
