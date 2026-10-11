export type ReadingPracticeMode = "retelling" | "aloud" | "aloud-retelling";
export type ReadingWord = { text: string; changed: boolean };

/** Compare word order, ignoring recognizer casing, punctuation and accent spelling. */
export function compareReadAloud(expected: string, spoken: string) {
  const words = (text: string): ReadingWord[] => (text.match(/[\p{L}\p{M}\p{N}]+/gu) ?? []).map((text) => ({ text, changed: true }));
  const key = (word: ReadingWord) => word.text.normalize("NFD").replace(/\p{M}/gu, "").toLocaleLowerCase("sk");
  const original = words(expected);
  const recognized = words(spoken);
  const left = original.map(key);
  const right = recognized.map(key);
  // Legacy/imported texts can be large. Do not block the interface on them.
  if (left.length * right.length > 1_000_000) return { original, recognized, matched: 0, tooLong: true };
  const table = Array.from({ length: left.length + 1 }, () => new Uint32Array(right.length + 1));
  for (let i = left.length - 1; i >= 0; i--) {
    for (let j = right.length - 1; j >= 0; j--) {
      table[i][j] = left[i] === right[j] ? table[i + 1][j + 1] + 1 : Math.max(table[i + 1][j], table[i][j + 1]);
    }
  }
  let i = 0;
  let j = 0;
  let matched = 0;
  while (i < left.length && j < right.length) {
    if (left[i] === right[j]) {
      original[i++].changed = recognized[j++].changed = false;
      matched++;
    } else if (table[i + 1][j] >= table[i][j + 1]) i++;
    else j++;
  }
  return { original, recognized, matched, tooLong: false };
}
