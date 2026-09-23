"use client";

import { type Dispatch, type FormEvent, type SetStateAction, useMemo, useState } from "react";

import { a1CourseModules } from "../data/a1Course";
import { type CourseLesson } from "../data/courseTypes";
import { type PersonalCheatSheet } from "../lib/api";

type CheatSheetLesson = { lesson: CourseLesson; moduleOrder: number; moduleTitle: string };

export function CourseCheatSheets({ completedLessonSlugs, personalCheatSheets, setPersonalCheatSheets, openLesson }: {
  completedLessonSlugs: string[];
  personalCheatSheets: PersonalCheatSheet[];
  setPersonalCheatSheets: Dispatch<SetStateAction<PersonalCheatSheet[]>>;
  openLesson: (moduleOrder: number, lesson: CourseLesson) => void;
}) {
  const [collection, setCollection] = useState<"course" | "personal">("course");
  const [moduleFilter, setModuleFilter] = useState("all");
  const [query, setQuery] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [personalTitle, setPersonalTitle] = useState("");
  const [personalContent, setPersonalContent] = useState("");
  const completed = useMemo(() => new Set(completedLessonSlugs), [completedLessonSlugs]);
  const sheets = useMemo<CheatSheetLesson[]>(() => a1CourseModules.flatMap((module) =>
    module.lessons
      .filter((lesson) => completed.has(lesson.slug))
      .map((lesson) => ({ lesson, moduleOrder: module.order, moduleTitle: module.title })),
  ), [completed]);
  const normalizedQuery = query.trim().toLocaleLowerCase("ru-RU");
  const visible = sheets.filter(({ lesson, moduleOrder }) =>
    (moduleFilter === "all" || moduleOrder === Number(moduleFilter))
    && (!normalizedQuery || `${lesson.title} ${lesson.slovakTitle} ${lesson.theory.summary}`.toLocaleLowerCase("ru-RU").includes(normalizedQuery)),
  );
  const availableModules = a1CourseModules.filter((module) => module.lessons.some((lesson) => completed.has(lesson.slug)));
  const clearPersonalForm = () => { setEditingId(null); setPersonalTitle(""); setPersonalContent(""); };
  const savePersonalSheet = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const title = personalTitle.trim();
    const content = personalContent.trim();
    if (!title || !content) return;
    const now = new Date().toISOString();
    setPersonalCheatSheets((current) => editingId
      ? current.map((sheet) => sheet.id === editingId ? { ...sheet, title, content, updatedAt: now } : sheet)
      : [{ id: crypto.randomUUID(), title, content, createdAt: now, updatedAt: now }, ...current]);
    clearPersonalForm();
  };
  const editPersonalSheet = (sheet: PersonalCheatSheet) => {
    setEditingId(sheet.id);
    setPersonalTitle(sheet.title);
    setPersonalContent(sheet.content);
  };
  const deletePersonalSheet = (sheet: PersonalCheatSheet) => {
    if (!window.confirm(`Удалить шпаргалку «${sheet.title}»?`)) return;
    setPersonalCheatSheets((current) => current.filter((item) => item.id !== sheet.id));
    if (editingId === sheet.id) clearPersonalForm();
  };

  return <section className="course-cheats" aria-labelledby="course-cheats-title">
    <header className="course-section-heading">
      <div><span>Быстрое повторение</span><h3 id="course-cheats-title">Шпаргалки</h3></div>
      <p>Короткие правила, примеры и план повторения по завершённым темам.</p>
    </header>

    <nav className="course-cheats-tabs" aria-label="Разделы шпаргалок">
      <button type="button" className={collection === "course" ? "active" : ""} aria-pressed={collection === "course"} onClick={() => setCollection("course")}>По курсу</button>
      <button type="button" className={collection === "personal" ? "active" : ""} aria-pressed={collection === "personal"} onClick={() => setCollection("personal")}>Мои шпаргалки <span>{personalCheatSheets.length}</span></button>
    </nav>

    {collection === "personal" ? <div className="personal-cheats">
      <form className="personal-cheat-form" onSubmit={savePersonalSheet}>
        <div><span>{editingId ? "Редактирование" : "Новая личная шпаргалка"}</span><h4>{editingId ? "Измените свою заметку" : "Запишите то, что хотите быстро вспомнить"}</h4></div>
        <label><span>Название</span><input value={personalTitle} onChange={(event) => setPersonalTitle(event.target.value)} maxLength={120} placeholder="Например: окончания Akuzatív" required /></label>
        <label><span>Правило или памятка</span><textarea value={personalContent} onChange={(event) => setPersonalContent(event.target.value)} maxLength={4000} rows={5} placeholder="Коротко запишите правило, пример или свой план действий…" required /></label>
        <div className="personal-cheat-form-actions">
          <button type="submit">{editingId ? "Сохранить изменения" : "Добавить шпаргалку"}</button>
          {editingId && <button type="button" onClick={clearPersonalForm}>Отмена</button>}
        </div>
      </form>
      {personalCheatSheets.length === 0 ? <div className="course-empty"><strong>Личных шпаргалок пока нет</strong><p>Добавьте первое правило, пример или короткую памятку.</p></div> : <div className="personal-cheats-list">
        {personalCheatSheets.map((sheet) => <article className="personal-cheat-card" key={sheet.id}>
          <h4>{sheet.title}</h4><p>{sheet.content}</p>
          <footer><button type="button" onClick={() => editPersonalSheet(sheet)}>Изменить</button><button type="button" className="danger" onClick={() => deletePersonalSheet(sheet)}>Удалить</button></footer>
        </article>)}
      </div>}
    </div> : sheets.length === 0 ? <div className="course-empty"><strong>Шпаргалок пока нет</strong><p>Завершите первую тему — её краткая памятка появится здесь автоматически.</p></div> : <>
      <div className="course-cheats-toolbar">
        <label><span>Модуль</span><select aria-label="Модуль шпаргалок" value={moduleFilter} onChange={(event) => setModuleFilter(event.target.value)}>
          <option value="all">Все пройденные модули</option>
          {availableModules.map((module) => <option value={module.order} key={module.slug}>{module.title}</option>)}
        </select></label>
        <label><span>Найти тему</span><input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Например: падежи" /></label>
        <strong>{visible.length} из {sheets.length}</strong>
      </div>

      {visible.length === 0 ? <div className="course-empty"><strong>Ничего не найдено</strong><p>Измените запрос или выберите другой модуль.</p></div> : <div className="course-cheats-list">
        {visible.map(({ lesson, moduleOrder, moduleTitle }) => <details className="course-cheat-card" key={lesson.slug}>
          <summary><span>Модуль {moduleOrder}</span><div><strong>{lesson.title}</strong><small lang="sk">{lesson.slovakTitle}</small></div></summary>
          <div className="course-cheat-content">
            <section className="course-cheat-summary"><span>Суть темы</span><p>{lesson.theory.summary}</p></section>
            <section><h4>Главные правила</h4><ul>{lesson.theory.rules.map((rule) => <li key={rule}>{rule}</li>)}</ul></section>
            <section><h4>Примеры</h4><div className="course-cheat-examples">{lesson.theory.examples.map((example) => <article key={example.slovak}><strong lang="sk">{example.slovak}</strong><span>{example.russian}</span><small>{example.explanation}</small></article>)}</div></section>
            <section className="course-cheat-plan"><h4>План действий</h4><ol><li>Прочитайте правила и назовите главное своими словами.</li><li>Закройте перевод и повторите словацкие примеры вслух.</li><li>Проверьте себя: {lesson.goals.join("; ").toLocaleLowerCase("ru-RU")}.</li></ol></section>
            <footer><span>{moduleTitle}</span><button type="button" onClick={() => openLesson(moduleOrder, lesson)}>Открыть полную тему →</button></footer>
          </div>
        </details>)}
      </div>}
    </>}
  </section>;
}
