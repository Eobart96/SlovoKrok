from dataclasses import dataclass
import re


WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
STOP_WORDS = {
    "ale", "ako", "bol", "bola", "bolo", "by", "do", "i", "je", "na", "o", "od", "po", "pre", "sa", "si", "sú", "to", "v", "vo", "z", "za",
    "а", "был", "была", "было", "в", "во", "для", "и", "из", "к", "как", "на", "о", "об", "он", "она", "они", "по", "с", "со", "у", "это",
}


@dataclass(frozen=True)
class OfflineOpenAnswerAssessment:
    score: int
    is_correct: bool


def _tokens(text: str) -> set[str]:
    normalized = text.casefold().replace("ё", "е")
    return {
        token
        for token in WORD_RE.findall(normalized)
        if len(token) >= 3 and token not in STOP_WORDS
    }


def assess_open_answer_offline(answer: str, reference_answer: str) -> OfflineOpenAnswerAssessment:
    """Estimate an open answer from saved meaning words without calling an AI provider."""
    answer_tokens = _tokens(answer)
    reference_tokens = _tokens(reference_answer)
    if not reference_tokens:
        matches = answer.strip().casefold() == reference_answer.strip().casefold()
        return OfflineOpenAnswerAssessment(score=100 if matches else 0, is_correct=matches)
    common = answer_tokens & reference_tokens
    coverage = len(common) / len(reference_tokens)
    precision = len(common) / max(1, len(answer_tokens))
    score = round((coverage * 0.8 + precision * 0.2) * 100)
    return OfflineOpenAnswerAssessment(score=score, is_correct=score >= 65)
