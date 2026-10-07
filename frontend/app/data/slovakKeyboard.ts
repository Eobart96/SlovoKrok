const slovakAltVariants: Readonly<Record<string, readonly string[]>> = {
  KeyA: ["á", "ä"],
  KeyC: ["č"],
  KeyD: ["ď"],
  KeyE: ["é"],
  KeyI: ["í"],
  KeyL: ["ĺ", "ľ"],
  KeyN: ["ň"],
  KeyO: ["ó", "ô"],
  KeyR: ["ŕ"],
  KeyS: ["š"],
  KeyT: ["ť"],
  KeyU: ["ú"],
  KeyY: ["ý"],
  KeyZ: ["ž"],
};

export function applySlovakAltShortcut(
  value: string,
  code: string,
  shiftKey: boolean,
  start = value.length,
  end = start,
): { value: string; caret: number } | null {
  const lowerVariants = slovakAltVariants[code];
  if (!lowerVariants) return null;
  const variants = shiftKey ? lowerVariants.map((character) => character.toUpperCase()) : lowerVariants;
  const base = code.slice(-1);
  const expectedBase = shiftKey ? base.toUpperCase() : base.toLowerCase();
  const safeStart = Math.max(0, Math.min(start, value.length));
  const safeEnd = Math.max(safeStart, Math.min(end, value.length));

  if (safeStart === safeEnd && safeStart > 0) {
    const previous = value.slice(safeStart - 1, safeStart);
    const currentVariant = variants.indexOf(previous);
    if (previous === expectedBase || currentVariant >= 0) {
      const nextVariant = previous === expectedBase ? variants[0] : variants[(currentVariant + 1) % variants.length];
      return {
        value: `${value.slice(0, safeStart - 1)}${nextVariant}${value.slice(safeEnd)}`,
        caret: safeStart,
      };
    }
  }

  return {
    value: `${value.slice(0, safeStart)}${variants[0]}${value.slice(safeEnd)}`,
    caret: safeStart + 1,
  };
}
