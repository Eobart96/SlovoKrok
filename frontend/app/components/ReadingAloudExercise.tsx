"use client";

import { useRef, useState } from "react";
import { compareReadAloud } from "../data/readingAloud";
import { ReadingDictation } from "./ReadingDictation";

export function ReadingAloudExercise({ text, active, disabled, combined, onContinue }: { text: string; active: boolean; disabled: boolean; combined: boolean; onContinue: () => void }) {
  const [transcript, setTranscript] = useState("");
  const transcriptBuffer = useRef("");
  const [listening, setListening] = useState(false);
  const [comparison, setComparison] = useState<ReturnType<typeof compareReadAloud> | null>(null);
  const [take, setTake] = useState(0);
  const [limitReached, setLimitReached] = useState(false);
  const locked = disabled || !active || listening;

  return <section className="reading-practice-card reading-aloud-exercise" aria-label="Чтение вслух по-словацки">
    <h5>{combined ? "Шаг 1 из 2. Прочитайте вслух по-словацки" : "Прочитайте текст вслух по-словацки"}</h5>
    <p>Читайте весь текст выше в удобном темпе. Остановите запись, затем сравните распознанные слова с текстом.</p>
    <ReadingDictation key={take} active={active} disabled={disabled || limitReached} language="sk-SK" onListeningChange={setListening} onText={(phrase) => {
      setComparison(null);
      const next = transcriptBuffer.current + (transcriptBuffer.current ? " " : "") + phrase;
      transcriptBuffer.current = next.slice(0, 16000);
      setTranscript(transcriptBuffer.current);
      if (next.length >= 16000) setLimitReached(true);
    }} />
    <p className="reading-aloud-note">Это сравнение распознанных слов, без оценки произношения по звуку. Распознавание может ошибаться. Пунктуация, регистр и написание диакритики не влияют на совпадение.</p>
    {limitReached && <p role="status">Достигнут предел записи. Начните чтение заново.</p>}
    {transcript && <div className="reading-aloud-transcript"><strong>Распознанный текст</strong><p lang="sk">{transcript}</p></div>}
    <div className="reading-aloud-actions">
      <button type="button" disabled={locked || !transcript.trim()} onClick={() => setComparison(compareReadAloud(text, transcript))}>Сравнить с текстом</button>
      <button type="button" disabled={locked} onClick={() => { transcriptBuffer.current = ""; setTranscript(""); setComparison(null); setLimitReached(false); setTake((current) => current + 1); }}>Начать заново</button>
    </div>
    {comparison && <div className="reading-aloud-comparison" role="status">
      {comparison.tooLong ? <p>Текст слишком длинный для автоматического сравнения. Сравните запись с текстом самостоятельно.</p> : <>
        <strong>Совпало {comparison.matched} из {comparison.original.length} слов по порядку</strong>
        <p>Выделенные слова не совпали в распознавании. Проверьте их и при необходимости прочитайте текст ещё раз.</p>
        <div><b>В тексте</b><p lang="sk">{comparison.original.map((word, index) => <span key={index}>{index > 0 ? " " : ""}{word.changed ? <mark>{word.text}</mark> : word.text}</span>)}</p></div>
        <div><b>Распознано</b><p lang="sk">{comparison.recognized.map((word, index) => <span key={index}>{index > 0 ? " " : ""}{word.changed ? <mark>{word.text}</mark> : word.text}</span>)}</p></div>
      </>}
    </div>}
    {combined ? <>
      <button type="button" disabled={locked || !transcript.trim()} onClick={onContinue}>Чтение завершено — перейти к пересказу</button>
      <details><summary>Не получается включить микрофон?</summary><p>Прочитайте текст вслух самостоятельно, затем перейдите к пересказу. Автоматического подтверждения чтения в этом случае нет.</p><button type="button" disabled={locked} onClick={onContinue}>Я прочитал вслух самостоятельно — к пересказу</button></details>
    </> : <p>После чтения можно начать заново или выбрать другой текст. Запись и сравнение не сохраняются в результатах пересказа.</p>}
  </section>;
}
