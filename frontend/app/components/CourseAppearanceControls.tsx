"use client";

import { useEffect, useState, type ReactNode } from "react";
import { type CourseSession, type FontSize } from "../hooks/useCourseSession";

// Browser-only preferences; existing CourseState and legacy keys stay compatible.
const storageKey = "slovokrok-appearance-v1";
const choices = {
  font: { default: "Системный", sans: "Arial", serif: "Georgia · с засечками", mono: "Consolas · моноширинный" },
  spacing: { default: "Исходный", compact: "Компактный", relaxed: "Свободный" },
  shadows: { default: "Исходные", none: "Без теней", soft: "Мягкие", strong: "Выраженные" },
  corners: { default: "Исходные", square: "Прямые", soft: "Мягкие", round: "Округлые" },
};
type Appearance = { [K in keyof typeof choices]: keyof typeof choices[K] };
const defaults: Appearance = { font: "default", spacing: "default", shadows: "default", corners: "default" };
const labels = { font: "Шрифт", spacing: "Межстрочный интервал", shadows: "Тени", corners: "Скругление карточек" };
const keys = Object.keys(defaults) as (keyof Appearance)[];

export function CourseAppearanceControls({ session, showTitle = true, themeControl }: { session: CourseSession; showTitle?: boolean; themeControl?: ReactNode }) {
  const [appearance, setAppearance] = useState<Appearance>(defaults);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    try {
      const parsed: unknown = JSON.parse(localStorage.getItem(storageKey) ?? "{}");
      if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
        const valid = Object.fromEntries(keys.map((key) => {
          const value = (parsed as Record<string, unknown>)[key];
          return [key, typeof value === "string" && Object.hasOwn(choices[key], value) ? value : "default"];
        })) as Appearance;
        setAppearance(valid);
      }
    } catch { setError("Не удалось прочитать оформление. Использован исходный вид."); }
    setReady(true);
  }, []);
  useEffect(() => {
    if (!ready) return;
    for (const key of keys) document.documentElement.setAttribute(`data-appearance-${key}`, appearance[key]);
    try { localStorage.setItem(storageKey, JSON.stringify(appearance)); }
    catch { setError("Оформление применено, но браузер не разрешил его сохранить."); }
    return () => { for (const key of keys) document.documentElement.removeAttribute(`data-appearance-${key}`); };
  }, [appearance, ready]);
  return <fieldset aria-label={showTitle ? undefined : "Оформление"}>
    {showTitle && <legend>Оформление</legend>}
    <p>Изменения видны сразу. Настройки оформления сохраняются.</p>
    {themeControl}
    <label>Размер текста курса<select value={session.fontSize} onChange={(event) => session.setFontSize(event.target.value as FontSize)}>
      <option value="normal">Обычный</option><option value="large">Крупный</option><option value="extra-large">Очень крупный</option>
    </select></label>
    {keys.map((key) => <label key={key}>{labels[key]}<select aria-label={labels[key]} disabled={!ready} value={appearance[key]} onChange={(event) => setAppearance((current) => ({ ...current, [key]: event.target.value }))}>
      {Object.entries(choices[key]).map(([value, title]) => <option key={value} value={value}>{title}</option>)}
    </select></label>)}
    <button className="course-appearance-reset" type="button" onClick={() => { setAppearance(defaults); session.setFontSize("large"); setError(""); }}>Вернуть исходное оформление</button>
    {error && <p role="alert">{error}</p>}
  </fieldset>;
}
