"use client";

import { FormEvent, type ReactNode, useEffect, useState } from "react";

import { type LearningMode } from "../data/learningMode";
import {
  getTutorSettings,
  startCodexLogin,
  TutorProviderName,
  TutorSettings,
  updateTutorSettings,
} from "../lib/api";

type Props = {
  open: boolean;
  onClose: () => void;
  developmentMode: boolean;
  onDevelopmentModeChange: (enabled: boolean) => void;
  learningMode: LearningMode;
  onLearningModeChange: (mode: LearningMode) => void;
  appearance: ReactNode;
  profile: ReactNode;
  tasks: ReactNode;
  mistakes: ReactNode;
  backup: ReactNode;
  developmentTools: ReactNode;
  settingsSections: { appearance: boolean; tasks: boolean; mistakes: boolean; ai: boolean };
  onSettingsSectionChange: (section: "appearance" | "tasks" | "mistakes" | "ai", open: boolean) => void;
};

const providerLabels: Record<TutorProviderName, { title: string; description: string }> = {
  codex: { title: "Codex CLI", description: "Использует локальный вход Codex без отдельного API-ключа." },
  openai: { title: "OpenAI API", description: "Прямое подключение по вашему OpenAI API-ключу." },
  polza: { title: "Polza API", description: "OpenAI-совместимый API через сервис Polza." },
};

export function AiSettingsPanel({ open, onClose, developmentMode, onDevelopmentModeChange, learningMode, onLearningModeChange, appearance, profile, tasks, mistakes, backup, developmentTools, settingsSections, onSettingsSectionChange }: Props) {
  const [settings, setSettings] = useState<TutorSettings | null>(null);
  const [provider, setProvider] = useState<TutorProviderName>("codex");
  const [openaiKey, setOpenaiKey] = useState("");
  const [openaiModel, setOpenaiModel] = useState("gpt-5");
  const [polzaKey, setPolzaKey] = useState("");
  const [polzaModel, setPolzaModel] = useState("google/gemini-2.5-flash-lite");
  const [clearOpenai, setClearOpenai] = useState(false);
  const [clearPolza, setClearPolza] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = async () => {
    setBusy(true);
    setError("");
    try {
      const next = await getTutorSettings();
      setSettings(next);
      setProvider(next.provider);
      setOpenaiModel(next.openai_model);
      setPolzaModel(next.polza_model);
      setOpenaiKey("");
      setPolzaKey("");
      setClearOpenai(false);
      setClearPolza(false);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Не удалось загрузить настройки");
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    if (open) void load();
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event: KeyboardEvent) => { if (event.key === "Escape") onClose(); };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open, onClose]);

  if (!open) return null;

  const save = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const next = await updateTutorSettings({
        provider,
        openai_api_key: openaiKey || undefined,
        openai_model: openaiModel,
        polza_api_key: polzaKey || undefined,
        polza_model: polzaModel,
        clear_openai_api_key: clearOpenai,
        clear_polza_api_key: clearPolza,
      });
      setSettings(next);
      setOpenaiKey("");
      setPolzaKey("");
      setClearOpenai(false);
      setClearPolza(false);
      setNotice("Настройки сохранены. Следующий запрос к преподавателю использует выбранный вариант.");
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Не удалось сохранить настройки");
    } finally {
      setBusy(false);
    }
  };

  const login = async () => {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const status = await startCodexLogin();
      setSettings((current) => current ? { ...current, codex_installed: status.installed, codex_authenticated: status.authenticated, codex_message: status.message } : current);
      setNotice(status.message);
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "Не удалось открыть вход Codex");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="ai-settings-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section className="ai-settings-panel" role="dialog" aria-modal="true" aria-labelledby="settings-title">
        <header>
          <div><span>SlovoKrok</span><h2 id="settings-title">Настройки</h2></div>
          <button type="button" className="ai-settings-close" onClick={onClose} aria-label="Закрыть настройки">×</button>
        </header>

        <section className="settings-section settings-development">
          <div>
            <strong>Режим разработки</strong>
            <p>Открывает ручные переходы по материалам и инструменты изменения прогресса для проверки курса.</p>
          </div>
          <button
            type="button"
            className="settings-switch"
            role="switch"
            aria-label="Режим разработки"
            aria-checked={developmentMode}
            onClick={() => onDevelopmentModeChange(!developmentMode)}
          >
            <span aria-hidden="true" />
            {developmentMode ? "Включён" : "Выключен"}
          </button>
        </section>

        <section className="settings-section settings-development settings-learning-mode">
          <div>
            <strong>Режим обучения</strong>
            <p>{learningMode === "online" ? "Онлайн: ИИ создаёт задания и помогает гибко проверять ответы." : "Офлайн: сохранённые упражнения, тексты для чтения и домашние задания проверяются по эталону без обращения к ИИ. Создание новых заданий временно недоступно."}</p>
          </div>
          <button
            type="button"
            className="settings-switch"
            role="switch"
            aria-label="Офлайн-режим"
            aria-checked={learningMode === "offline"}
            onClick={() => onLearningModeChange(learningMode === "online" ? "offline" : "online")}
          >
            <span aria-hidden="true" />
            {learningMode === "online" ? "Онлайн" : "Офлайн"}
          </button>
        </section>

        {developmentTools}
        {profile}

        <details className="settings-section settings-appearance" open={settingsSections.appearance} onToggle={(event) => onSettingsSectionChange("appearance", event.currentTarget.open)}>
          <summary>Оформление</summary>
          {appearance}
        </details>

        <details className="settings-section settings-tasks" open={settingsSections.tasks} onToggle={(event) => onSettingsSectionChange("tasks", event.currentTarget.open)}>
          <summary>Задания</summary>
          {tasks}
        </details>

        <section className="settings-section settings-backup">
          {backup}
        </section>
        <details className="settings-section" open={settingsSections.mistakes} onToggle={(event) => onSettingsSectionChange("mistakes", event.currentTarget.open)}>
          <summary>Ошибки и повторения</summary>
          {mistakes}
        </details>

        <details className="settings-section settings-ai" open={settingsSections.ai} onToggle={(event) => onSettingsSectionChange("ai", event.currentTarget.open)}>
          <summary>Подключение ИИ</summary>
          {learningMode === "offline" && <p className="ai-settings-mode-note">Подключение сохранено, но не используется для проверки заданий, пока включён офлайн-режим.</p>}
          <form onSubmit={save}>
          <fieldset className="ai-provider-picker" disabled={busy}>
            <legend>Выберите способ подключения</legend>
            <div className="ai-provider-switch">
              {(Object.keys(providerLabels) as TutorProviderName[]).map((name) => (
                <label key={name} className={provider === name ? "selected" : ""}>
                  <input type="radio" name="provider" value={name} checked={provider === name} onChange={() => { setProvider(name); setClearOpenai(false); setClearPolza(false); setError(""); }} />
                  <span>{providerLabels[name].title}</span>
                </label>
              ))}
            </div>
            <p className="ai-provider-description" aria-live="polite">{providerLabels[provider].description}</p>
          </fieldset>

          {provider === "codex" && <div className="ai-provider-details">
            <strong className={settings?.codex_authenticated ? "ai-status-ok" : "ai-status-warn"}>{settings?.codex_authenticated ? "Подключён" : "Требуется проверка или вход"}</strong>
            <p>{settings?.codex_message ?? (busy ? "Проверяем Codex CLI…" : "Статус пока неизвестен")}</p>
            <div className="ai-settings-actions"><button type="button" onClick={login} disabled={busy || !settings?.codex_installed || settings?.codex_authenticated}>Открыть вход Codex</button><button type="button" onClick={load} disabled={busy}>Обновить статус</button></div>
          </div>}

          {provider === "openai" && <div className="ai-provider-details">
            {settings?.openai_api_key_configured && <p className="ai-key-saved">Ключ OpenAI сохранён. Для смены модели вводить его повторно не нужно.</p>}
            <label>{settings?.openai_api_key_configured ? "Новый API-ключ OpenAI — необязательно" : "API-ключ OpenAI"}<input type="password" autoComplete="off" value={openaiKey} onChange={(event) => { setOpenaiKey(event.target.value); setClearOpenai(false); }} placeholder={settings?.openai_api_key_configured ? "Оставьте пустым, чтобы сохранить прежний ключ" : "Вставьте API-ключ"} /></label>
            <label>Модель<input value={openaiModel} onChange={(event) => { setOpenaiModel(event.target.value); setClearOpenai(false); setError(""); }} required /></label>
            {settings?.openai_api_key_configured && <details className="ai-key-management"><summary>Управление сохранённым ключом</summary><label className="ai-clear-key"><input type="checkbox" checked={clearOpenai} onChange={(event) => setClearOpenai(event.target.checked)} />Удалить ключ при сохранении настроек</label></details>}
          </div>}

          {provider === "polza" && <div className="ai-provider-details">
            {settings?.polza_api_key_configured && <p className="ai-key-saved">Ключ Polza сохранён. Меняйте только модель — ключ подставится автоматически.</p>}
            <label>{settings?.polza_api_key_configured ? "Новый API-ключ Polza — необязательно" : "API-ключ Polza"}<input type="password" autoComplete="off" value={polzaKey} onChange={(event) => { setPolzaKey(event.target.value); setClearPolza(false); }} placeholder={settings?.polza_api_key_configured ? "Оставьте пустым, чтобы сохранить прежний ключ" : "Вставьте API-ключ"} /></label>
            <label>Модель<input value={polzaModel} onChange={(event) => { setPolzaModel(event.target.value); setClearPolza(false); setError(""); }} required /></label>
            <small>Рекомендуемая для курса: <code>google/gemini-2.5-flash-lite</code> — быстрый и экономичный вариант для перевода, объяснений и генерации заданий.</small>
            <small>Endpoint: {settings?.polza_base_url ?? "https://polza.ai/api/v1"}</small>
            {settings?.polza_api_key_configured && <details className="ai-key-management"><summary>Управление сохранённым ключом</summary><label className="ai-clear-key"><input type="checkbox" checked={clearPolza} onChange={(event) => setClearPolza(event.target.checked)} />Удалить ключ при сохранении настроек</label></details>}
          </div>}

          <p className="ai-settings-security">Ключ хранится только локально на backend и никогда не возвращается в браузер. Персональный профиль ученика по умолчанию не отправляется выбранному ИИ; явное включение возможно только через локальную настройку <code>SHARE_PRIVATE_TUTOR_PROFILE=true</code>.</p>
          {error && <p className="ai-settings-error" role="alert">{error}</p>}
          {notice && <p className="ai-settings-notice" role="status">{notice}</p>}
            <footer><button type="submit" className="primary" disabled={busy}>{busy ? "Подождите…" : "Сохранить настройки ИИ"}</button></footer>
          </form>
        </details>
        <footer className="settings-footer"><button type="button" onClick={onClose}>Закрыть</button></footer>
      </section>
    </div>
  );
}
