"use client";

import { useEffect, useMemo, useState } from "react";

import { type CourseLesson } from "../data/courseTypes";
import { homeworkReferenceSections } from "../data/homeworkPlanning";
import { type PersonalCheatSheet } from "../lib/api";

type ReferenceView = "cheats" | "topics" | null;

export function CourseHomeworkReference({ lessons, personalCheatSheets, preferredLessonSlug, recommendedLessonSlugs }: {
  lessons: CourseLesson[];
  personalCheatSheets: PersonalCheatSheet[];
  preferredLessonSlug?: string;
  recommendedLessonSlugs: string[];
}) {
  const [view, setView] = useState<ReferenceView>(null);
  const [lessonSlug, setLessonSlug] = useState(preferredLessonSlug ?? lessons[0]?.slug ?? "");
  const [sectionIndex, setSectionIndex] = useState(0);
  const lesson = useMemo(() => lessons.find((item) => item.slug === lessonSlug) ?? lessons[0], [lessonSlug, lessons]);
  const referenceSections = useMemo(() => homeworkReferenceSections(lesson?.sections ?? []), [lesson]);
  const section = referenceSections[sectionIndex - 1];

  useEffect(() => {
    const nextSlug = lessons.some((item) => item.slug === preferredLessonSlug) ? preferredLessonSlug! : lessons[0]?.slug ?? "";
    setLessonSlug(nextSlug);
    setSectionIndex(0);
  }, [lessons, preferredLessonSlug]);

  const toggleView = (nextView: Exclude<ReferenceView, null>) => setView((current) => current === nextView ? null : nextView);

  return <section className="course-homework-reference" aria-labelledby="course-homework-reference-title">
    <div className="course-homework-reference-heading">
      <div><span>Справка без выхода из задания</span><strong id="course-homework-reference-title">Нужно повторить материал?</strong></div>
      <div>
        <button type="button" className={view === "cheats" ? "active" : ""} aria-expanded={view === "cheats"} onClick={() => toggleView("cheats")}>Открыть шпаргалки</button>
        <button type="button" className={view === "topics" ? "active" : ""} aria-expanded={view === "topics"} onClick={() => toggleView("topics")}>Посмотреть темы</button>
      </div>
    </div>

    {view && (lesson ? <div className="course-homework-reference-panel">
      <label><span>Завершённая тема · подходящие к заданию стоят первыми</span><select value={lesson.slug} onChange={(event) => { setLessonSlug(event.target.value); setSectionIndex(0); }}>{lessons.map((item) => <option value={item.slug} key={item.slug}>{item.title} · {item.slovakTitle}{recommendedLessonSlugs.includes(item.slug) ? " · подходит к заданию" : ""}</option>)}</select></label>

      {view === "cheats" ? <div className="course-homework-reference-cheats">
        <article><span>Суть темы</span><h4>{lesson.title}</h4><p>{lesson.theory.summary}</p></article>
        <article><h4>Главные правила</h4><ul>{lesson.theory.rules.map((rule) => <li key={rule}>{rule}</li>)}</ul></article>
        <article><h4>Примеры</h4><div>{lesson.theory.examples.map((example) => <p key={example.slovak}><strong lang="sk">{example.slovak}</strong><span>{example.russian}</span><small>{example.explanation}</small></p>)}</div></article>
        {personalCheatSheets.length > 0 && <article className="personal"><h4>Мои шпаргалки</h4><div>{personalCheatSheets.map((sheet) => <details key={sheet.id}><summary>{sheet.title}</summary><p>{sheet.content}</p></details>)}</div></article>}
      </div> : <div className="course-homework-reference-topic">
        <header><div><span>Полная тема</span><h4>{lesson.title}</h4><p lang="sk">{lesson.slovakTitle}</p></div><small>{lesson.description}</small></header>
        <nav aria-label="Разделы выбранной темы"><button type="button" className={sectionIndex === 0 ? "active" : ""} onClick={() => setSectionIndex(0)}>Теория</button>{referenceSections.map((item, index) => <button type="button" className={sectionIndex === index + 1 ? "active" : ""} onClick={() => setSectionIndex(index + 1)} key={`${item.title}-${index}`}>{index + 1}. {item.title}</button>)}</nav>
        {sectionIndex === 0 ? <article className="course-homework-reference-theory"><p>{lesson.theory.summary}</p><ol>{lesson.theory.rules.map((rule) => <li key={rule}>{rule}</li>)}</ol><div>{lesson.theory.examples.map((example) => <p key={example.slovak}><strong lang="sk">{example.slovak}</strong><span>{example.russian}</span><small>{example.explanation}</small></p>)}</div></article> : section && <article className={`course-homework-reference-section ${section.importance === "extra" ? "extra" : ""}`}><h4>{section.title}</h4>{section.paragraphs?.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}{section.items && <ul>{section.items.map((item) => <li key={item}>{item}</li>)}</ul>}{section.table && <div className="course-table-wrap"><table><thead><tr>{section.table.headers.map((header) => <th key={header}>{header}</th>)}</tr></thead><tbody>{section.table.rows.map((row, rowIndex) => <tr key={rowIndex}>{row.map((cell, cellIndex) => <td key={`${cell}-${cellIndex}`}>{cell}</td>)}</tr>)}</tbody></table></div>}{section.note && <aside className="course-note"><b>Обратите внимание</b>{section.note}</aside>}</article>}
      </div>}
    </div> : <p className="course-empty">Завершите хотя бы одну тему — после этого её можно будет открыть здесь.</p>)}
  </section>;
}
