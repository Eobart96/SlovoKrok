export type TranslationDraft<Result> = {
  direction: "ru-sk" | "sk-ru";
  text: string;
  result: Result | null;
};

export type TranslationDraftReset<Result> = TranslationDraft<Result> & {
  error: "";
  questionOpen: false;
  question: "";
  questionAnswer: "";
  questionError: "";
};

function resetFollowUp<Result>(direction: TranslationDraft<Result>["direction"], text: string): TranslationDraftReset<Result> {
  return { direction, text, result: null, error: "", questionOpen: false, question: "", questionAnswer: "", questionError: "" };
}

export function editTranslationDraft<Result>(draft: TranslationDraft<Result>, text: string): TranslationDraftReset<Result> {
  return resetFollowUp(draft.direction, text);
}

export function swapTranslationDraft<Result extends { translation: string }>(draft: TranslationDraft<Result>): TranslationDraftReset<Result> {
  return resetFollowUp(draft.direction === "ru-sk" ? "sk-ru" : "ru-sk", draft.result?.translation ?? draft.text);
}
