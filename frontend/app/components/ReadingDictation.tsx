"use client";

import { useEffect, useRef, useState } from "react";

type RecognitionResult = { isFinal: boolean; 0: { transcript: string } };
type Recognition = {
  lang: string; continuous: boolean; interimResults: boolean;
  onresult: ((event: { resultIndex: number; results: { length: number; [index: number]: RecognitionResult } }) => void) | null;
  onerror: ((event: { error: string }) => void) | null;
  onend: (() => void) | null;
  start: () => void; stop: () => void; abort: () => void;
};
type RecognitionConstructor = new () => Recognition;

export function ReadingDictation({ active, disabled, onText }: { active: boolean; disabled: boolean; onText: (text: string) => void }) {
  const [supported, setSupported] = useState<boolean | null>(null);
  const [listening, setListening] = useState(false);
  const [message, setMessage] = useState("");
  const recognition = useRef<Recognition | null>(null);
  const appendText = useRef(onText);
  appendText.current = onText;
  const cancel = () => {
    const instance = recognition.current;
    recognition.current = null;
    if (instance) { instance.onresult = null; instance.onerror = null; instance.onend = null; instance.abort(); }
  };
  useEffect(() => {
    const browser = window as Window & { SpeechRecognition?: RecognitionConstructor; webkitSpeechRecognition?: RecognitionConstructor };
    setSupported(Boolean(browser.SpeechRecognition ?? browser.webkitSpeechRecognition));
    return cancel;
  }, []);
  useEffect(() => {
    if (!active || disabled) { cancel(); setListening(false); }
  }, [active, disabled]);
  const toggle = () => {
    if (recognition.current) { recognition.current.stop(); return; }
    const browser = window as Window & { SpeechRecognition?: RecognitionConstructor; webkitSpeechRecognition?: RecognitionConstructor };
    const Constructor = browser.SpeechRecognition ?? browser.webkitSpeechRecognition;
    if (!Constructor || disabled || !active) return;
    const instance = new Constructor();
    const processed = new Set<number>();
    instance.lang = "ru-RU"; instance.continuous = true; instance.interimResults = false;
    recognition.current = instance;
    instance.onresult = (event) => {
      if (recognition.current !== instance) return;
      const phrases: string[] = [];
      for (let index = event.resultIndex; index < event.results.length; index++) {
        if (!event.results[index].isFinal || processed.has(index)) continue;
        processed.add(index);
        const phrase = event.results[index][0].transcript.trim();
        if (phrase) phrases.push(phrase);
      }
      if (phrases.length) appendText.current(phrases.join(" "));
    };
    instance.onerror = (event) => {
      const errors: Record<string, string> = { "not-allowed": "Разрешите браузеру доступ к микрофону для голосового ввода.", "service-not-allowed": "Браузер не разрешает распознавание речи.", "audio-capture": "Микрофон не найден или занят другим приложением.", "no-speech": "Речь не распознана. Попробуйте ещё раз.", network: "Не удалось подключиться к распознаванию речи. Проверьте интернет." };
      setMessage(errors[event.error] ?? "Голосовой ввод прервался. Можно продолжить вводить текст вручную.");
    };
    instance.onend = () => { if (recognition.current === instance) { recognition.current = null; setListening(false); } };
    setMessage("");
    try { instance.start(); setListening(true); }
    catch { cancel(); setListening(false); setMessage("Не удалось включить микрофон. Попробуйте ещё раз."); }
  };
  return <div className="course-reading-dictation">
    <button type="button" onClick={toggle} disabled={disabled || !active || !supported} aria-pressed={listening}><span aria-hidden="true">{listening ? "■" : "🎙"}</span> {listening ? "Остановить диктовку" : "Надиктовать пересказ"}</button>
    <small role="status" aria-live="polite">{message || (supported === false ? "Этот браузер не поддерживает голосовой ввод. Пересказ можно написать вручную." : listening ? "Слушаю по-русски… Текст добавляется в поле ответа." : "Голосовой ввод на русском. Браузер запросит микрофон; для распознавания может требоваться интернет.")}</small>
  </div>;
}
