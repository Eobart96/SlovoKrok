"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

import { CourseScreen } from "./components/CourseScreen";
import { IssueReports } from "./components/IssueReports";
import { CourseWelcome } from "./components/CourseWelcome";

const FloatingTranslator = dynamic(() => import("./components/FloatingTranslator").then((module) => module.FloatingTranslator));

type Theme = "light" | "dark";
type ModuleArea = "learning" | "cheats" | "exercises" | "reading" | "vocabulary" | "homework" | "review";

const themeStorageKey = "ai-learning-platform-theme";

export default function HomePage() {
  const [theme, setTheme] = useState<Theme>("light");
  const [themeReady, setThemeReady] = useState(false);
  const [activeArea, setActiveArea] = useState<ModuleArea>("learning");
  const [settingsOpen, setSettingsOpen] = useState(false);

  useEffect(() => {
    const storedTheme = window.localStorage.getItem(themeStorageKey);
    const preferredTheme: Theme = window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
    setTheme(storedTheme === "dark" || storedTheme === "light" ? storedTheme : preferredTheme);
    setThemeReady(true);
  }, []);

  useEffect(() => {
    if (!themeReady) return;
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem(themeStorageKey, theme);
  }, [theme, themeReady]);

  return (
    <main className="course-route-shell">
      <header className="course-route-header">
        <div>
          <span>Курс словацкого языка · Slovak A1</span>
          <strong>SlovoKrok</strong>
        </div>
        <nav aria-label="Навигация курса Slovak A1">
          <div className="course-primary-navigation" aria-label="Основные разделы">
            <button type="button" className={activeArea === "learning" ? "active" : ""} onClick={() => setActiveArea("learning")}>Обучение</button>
            <button type="button" className={activeArea === "cheats" ? "active" : ""} onClick={() => setActiveArea("cheats")}>Шпаргалки</button>
            <button type="button" className={activeArea === "exercises" ? "active" : ""} onClick={() => setActiveArea("exercises")}>Упражнения</button>
            <button type="button" className={activeArea === "homework" ? "active" : ""} onClick={() => setActiveArea("homework")}>Домашнее задание</button>
            <button type="button" className={activeArea === "reading" ? "active" : ""} onClick={() => setActiveArea("reading")}>Чтение</button>
            <button type="button" className={activeArea === "review" ? "active" : ""} onClick={() => setActiveArea("review")}>Ошибки</button>
            <button type="button" className={activeArea === "vocabulary" ? "active" : ""} onClick={() => setActiveArea("vocabulary")}>Слова</button>
          </div>
          <FloatingTranslator />
          <CourseWelcome onStart={() => { setSettingsOpen(false); setActiveArea("learning"); }} onProfile={() => setSettingsOpen(true)} />
          <button type="button" onClick={() => setSettingsOpen(true)} aria-label="Открыть настройки">
            <span aria-hidden="true">⚙</span>
            Настройки
          </button>
        </nav>
      </header>
      <CourseScreen requestedArea={activeArea} onAreaChange={setActiveArea} settingsOpen={settingsOpen} onSettingsClose={() => setSettingsOpen(false)} themeControl={<label>Тема интерфейса<select value={theme} disabled={!themeReady} onChange={(event) => setTheme(event.target.value as Theme)}><option value="light">Светлая</option><option value="dark">Тёмная</option></select></label>} />
      <div aria-label="Связь и проект">
        <div className="course-footer-links">
          <IssueReports section={activeArea} />
          <a href="https://github.com/Eobart96/SlovoKrok" target="_blank" rel="noopener noreferrer" aria-label="GitHub проекта — открыть в новой вкладке" title="GitHub проекта"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .75a11.25 11.25 0 0 0-3.558 21.922c.563.104.768-.244.768-.542 0-.267-.01-.974-.015-1.911-3.13.68-3.791-1.508-3.791-1.508-.512-1.3-1.25-1.646-1.25-1.646-1.022-.699.078-.685.078-.685 1.13.08 1.725 1.16 1.725 1.16 1.004 1.72 2.634 1.223 3.275.935.102-.727.393-1.223.715-1.504-2.498-.284-5.124-1.249-5.124-5.563 0-1.23.44-2.233 1.16-3.02-.116-.285-.503-1.43.11-2.98 0 0 .945-.303 3.094 1.153a10.8 10.8 0 0 1 5.626 0c2.149-1.456 3.092-1.153 3.092-1.153.615 1.55.228 2.695.112 2.98.722.787 1.158 1.79 1.158 3.02 0 4.325-2.63 5.276-5.136 5.554.404.348.765 1.034.765 2.084 0 1.504-.014 2.717-.014 3.086 0 .3.203.65.774.54A11.25 11.25 0 0 0 12 .75Z" /></svg></a>
        </div>
      </div>
    </main>
  );
}
