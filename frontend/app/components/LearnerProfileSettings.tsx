"use client";

import { useState } from "react";
import { saveLearnerProfile, translateWithTutor, type LearnerProfile } from "../lib/api";

export function LearnerProfileSettings({ profile, onSaved, loadError }: { profile: LearnerProfile; onSaved: (value: LearnerProfile) => void; loadError: string }) {
  const [draft, setDraft] = useState(profile);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const field = (key: keyof LearnerProfile, label: string, max: number, placeholder = "") => <label className="learner-profile-field"><span>{label}</span>{key === "interests" || key === "goal" ? <textarea rows={3} maxLength={max} value={String(draft[key])} disabled={busy} placeholder={placeholder} onChange={(event) => setDraft((current) => ({ ...current, [key]: event.target.value }))} /> : <input maxLength={max} value={String(draft[key])} disabled={busy} placeholder={placeholder} onChange={(event) => setDraft((current) => ({ ...current, [key]: event.target.value }))} />}</label>;
  return <details className="settings-section learner-profile"><summary>О себе</summary>
    <form className="learner-profile-form" onSubmit={async (event) => { event.preventDefault(); setBusy(true); setError(""); setNotice(""); try { const saved = await saveLearnerProfile(draft); onSaved(saved); setDraft(saved); setNotice("Профиль сохранён."); } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось сохранить профиль."); } finally { setBusy(false); } }}>
      <p className="learner-profile-intro">Расскажите немного о себе — примеры и новые задания станут ближе к вашей жизни. Все поля необязательные.</p>
      <fieldset><legend>Как к вам обращаться</legend><div className="learner-profile-grid">
      {field("name", "Ваше имя", 80, "Алексей")}
      {field("slovak_name", "Имя латиницей", 80, "Alexej")}
      </div><small>Заполните обе формы имени, чтобы словацкий пример и перевод совпадали.</small></fieldset>
      <fieldset><legend>Работа или учёба</legend><div className="learner-profile-grid">
      {field("occupation", "По-русски", 250, "Я работаю поваром")}
      {field("occupation_sentence_sk", "По-словацки", 250, "Pracujem ako kuchár.")}</div>
      <div className="learner-profile-translate"><button type="button" className="learner-profile-secondary" disabled={busy || !draft.occupation.trim() || !draft.share_with_ai} onClick={async () => { setBusy(true); setError(""); try { const result = await translateWithTutor(draft.occupation, "ru-sk"); setDraft((current) => ({ ...current, occupation_sentence_sk: result.translation.slice(0, 250) })); } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось перевести."); } finally { setBusy(false); } }}>Перевести с ИИ</button><small>{!draft.share_with_ai ? "Для перевода включите разрешение ниже." : "Перевод попадёт в поле справа и в историю переводчика."}</small></div>
      </fieldset>
      <fieldset><legend>Что вам интересно</legend>{field("city", "Ваш город", 100, "Братислава")}<div className="learner-profile-grid">{field("interests", "Интересы", 500, "Кулинария, путешествия")}{field("goal", "Цель обучения", 500, "Для жизни и работы в Словакии")}</div></fieldset>
      <div className="learner-profile-consent"><div><strong id="learner-profile-ai-label">Учитывать профиль в заданиях ИИ</strong><p>Разрешить передавать эти сведения выбранному ИИ для новых заданий и консультаций. Без разрешения примеры уроков адаптируются локально.</p></div><button type="button" role="switch" aria-labelledby="learner-profile-ai-label" aria-checked={draft.share_with_ai} className="settings-switch" disabled={busy} onClick={() => setDraft((current) => ({ ...current, share_with_ai: !current.share_with_ai }))}><span aria-hidden="true" />{draft.share_with_ai ? "Включено" : "Выключено"}</button></div>
      <div className="learner-profile-footer"><small>Сохранённые задания и фиксированные тесты сохраняют прежние условия.</small><button className="learner-profile-save" disabled={busy || Boolean(loadError)} type="submit">{busy ? "Сохраняю…" : "Сохранить профиль"}</button></div>
      {(loadError || error) && <p className="course-persistence-error" role="alert">{loadError || error}</p>}{notice && <p className="learner-profile-notice" role="status">{notice}</p>}
    </form></details>;
}
