export type TranslationVocabularySeed = {
  lesson_slug: string;
  lesson_title: string;
  word: string;
  translation: string;
  example: string | null;
};

export const translatorVocabularyWordSource = "translator:words";
export const translatorVocabularySentenceSource = "translator:sentences";
export const translatorVocabularyUpdatedEvent = "course-vocabulary-updated";

function oneLine(value: string): string {
  return value.replace(/[\t\r\n]+/g, " ").trim();
}

export function isTranslatorVocabularySource(source: string): boolean {
  return source === translatorVocabularyWordSource || source === translatorVocabularySentenceSource;
}

export function isSentenceVocabularyItem(item: Pick<TranslationVocabularySeed, "lesson_slug" | "word">): boolean {
  return item.lesson_slug.startsWith("additional-vocabulary:expanded-sentences-")
    || item.lesson_slug === translatorVocabularySentenceSource
    || /\s|[.!?…]/u.test(item.word.trim());
}

export function translationVocabularySeed(source: string, translation: string, direction: "ru-sk" | "sk-ru"): TranslationVocabularySeed | null {
  const slovak = oneLine(direction === "ru-sk" ? translation : source);
  const russian = oneLine(direction === "ru-sk" ? source : translation);
  if (!slovak || !russian || slovak.length > 255 || russian.length > 500) return null;
  const sentence = /\s|[.!?…]/u.test(slovak);
  return {
    lesson_slug: sentence ? translatorVocabularySentenceSource : translatorVocabularyWordSource,
    lesson_title: sentence ? "Из переводчика · предложения" : "Из переводчика · слова",
    word: slovak,
    translation: russian,
    example: slovak,
  };
}
