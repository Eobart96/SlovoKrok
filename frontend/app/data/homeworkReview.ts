export const homeworkPassingScore = 80;

export function homeworkPassed(score: number): boolean {
  return Number.isFinite(score) && score >= homeworkPassingScore;
}

export type ReviewToken = { text: string; changed: boolean };

/** Exact tokens preserve punctuation, accents and line breaks in both answers. */
export function compareHomeworkAnswers(original: string, corrected: string): { original: ReviewToken[]; corrected: ReviewToken[] } {
  const tokenize = (text: string) => text.match(/\s+|[\p{L}\p{M}\p{N}]+|[^\s\p{L}\p{M}\p{N}]/gu) ?? [];
  const left = tokenize(original);
  const right = tokenize(corrected);
  const originalTokens = left.map((text) => ({ text, changed: true }));
  const correctedTokens = right.map((text) => ({ text, changed: true }));
  let start = 0;
  while (start < left.length && start < right.length && left[start] === right[start]) {
    originalTokens[start].changed = correctedTokens[start].changed = false;
    start++;
  }
  let leftEnd = left.length;
  let rightEnd = right.length;
  while (leftEnd > start && rightEnd > start && left[leftEnd - 1] === right[rightEnd - 1]) {
    originalTokens[--leftEnd].changed = correctedTokens[--rightEnd].changed = false;
  }
  // Bound work for oversized legacy answers; the middle remains visibly changed.
  if ((leftEnd - start) * (rightEnd - start) <= 1_000_000) {
    const rows = Array.from({ length: leftEnd - start + 1 }, () => new Uint32Array(rightEnd - start + 1));
    for (let i = leftEnd - start - 1; i >= 0; i--) {
      for (let j = rightEnd - start - 1; j >= 0; j--) {
        rows[i][j] = left[start + i] === right[start + j]
          ? rows[i + 1][j + 1] + 1
          : Math.max(rows[i + 1][j], rows[i][j + 1]);
      }
    }
    let i = 0;
    let j = 0;
    while (i < leftEnd - start && j < rightEnd - start) {
      if (left[start + i] === right[start + j]) {
        originalTokens[start + i++].changed = false;
        correctedTokens[start + j++].changed = false;
      } else if (rows[i + 1][j] >= rows[i][j + 1]) i++;
      else j++;
    }
  }
  return { original: originalTokens, corrected: correctedTokens };
}
