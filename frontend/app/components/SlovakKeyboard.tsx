import { type KeyboardEvent, useRef, useState } from "react";

import { applySlovakAltShortcut } from "../data/slovakKeyboard";

const slovakKeys = ["á", "ä", "č", "ď", "é", "í", "ĺ", "ľ", "ň", "ó", "ô", "ŕ", "š", "ť", "ú", "ý", "ž", "ch", "dz", "dž"];

type SlovakKeyboardProps = { onInsert: (key: string) => void; disabled?: boolean };

type SlovakTextInputProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  disabled?: boolean;
};

export function SlovakKeyboard({ onInsert, disabled = false }: SlovakKeyboardProps) {
  const [capsLock, setCapsLock] = useState(false);
  return <div className="native-keyboard" aria-label="Словацкие буквы">
    <button className={`native-keyboard-caps ${capsLock ? "active" : ""}`} type="button" aria-pressed={capsLock} onClick={() => setCapsLock((value) => !value)} disabled={disabled}>Caps Lock</button>
    {slovakKeys.map((key) => <button key={key} type="button" onClick={(event) => onInsert(event.shiftKey || capsLock ? key.toUpperCase() : key)} disabled={disabled}>{capsLock ? key.toUpperCase() : key}</button>)}
  </div>;
}

export function SlovakTextInput({ value, onChange, placeholder, disabled = false }: SlovakTextInputProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const insertKey = (key: string) => {
    const input = inputRef.current;
    const start = input?.selectionStart ?? value.length;
    const end = input?.selectionEnd ?? start;
    onChange(`${value.slice(0, start)}${key}${value.slice(end)}`);
    requestAnimationFrame(() => {
      input?.focus();
      input?.setSelectionRange(start + key.length, start + key.length);
    });
  };

  const handleAltShortcut = (event: KeyboardEvent<HTMLInputElement>) => {
    if (!event.altKey || event.ctrlKey || event.metaKey) return;
    const input = inputRef.current;
    const inserted = applySlovakAltShortcut(value, event.code, event.shiftKey, input?.selectionStart ?? value.length, input?.selectionEnd ?? value.length);
    if (!inserted) return;
    event.preventDefault();
    onChange(inserted.value);
    requestAnimationFrame(() => {
      input?.focus();
      input?.setSelectionRange(inserted.caret, inserted.caret);
    });
  };

  return <>
    <input ref={inputRef} value={value} onChange={(event) => onChange(event.target.value)} onKeyDown={handleAltShortcut} placeholder={placeholder} autoComplete="off" disabled={disabled} />
    <SlovakKeyboard onInsert={insertKey} disabled={disabled} />
  </>;
}
