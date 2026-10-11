import pytest
import json

from app.tutor import AIResponseError, decode_exercise_snapshot, encode_exercise_snapshot, parse_generated_exercise, parse_tutor_assessment, requested_exercise_interaction
from app.tutor_core.exercise import assess_exercise_offline


@pytest.mark.parametrize("tokens,reference,expected", [
    (["Kuriér", "Sergej", "je."], "Sergej je kuriér.", ["kuriér.", "Sergej", "je"]),
    (["máš", "ako?", "sa"], "Ako sa máš?", ["máš?", "Ako", "sa"]),
    (["a", "A", "b."], "A a b.", ["A", "a", "b."]),
    (["som.", "prišiel,", "Keď", "som", "oddychoval"], "Keď som prišiel, oddychoval som.", ["som", "prišiel,", "Keď", "som.", "oddychoval"]),
])
def test_order_tokens_use_reference_spelling_for_generation_and_legacy_reads(tokens, reference, expected):
    payload = {"question": "Соберите фразу", "instruction": "Расставьте слова", "interaction_type": "order", "tokens": tokens, "accepted_answers": [reference]}
    generated = parse_generated_exercise(json.dumps(payload))
    assert generated.tokens == expected
    snapshot = "slovokrok-exercise:v1:" + json.dumps({"theory": "Old theory", "interaction_type": "order", "tokens": tokens, "accepted_answers": [reference]})
    theory, restored = decode_exercise_snapshot(snapshot)
    assert theory == "Old theory"
    assert restored.tokens == expected
    assert assess_exercise_offline(interaction=restored, answer=reference).is_correct
    assert json.loads(snapshot.split(":v1:")[1])["tokens"] == tokens


def test_repaired_order_tokens_still_require_correct_word_order_and_diacritics():
    generated = parse_generated_exercise(json.dumps({"question": "Q", "instruction": "I", "interaction_type": "order", "tokens": ["Kuriér", "Sergej", "je."], "accepted_answers": ["Sergej je kuriér."]}))
    assert assess_exercise_offline(interaction=generated, answer="Sergej je kuriér.").is_correct
    assert not assess_exercise_offline(interaction=generated, answer="Sergej kuriér. je").is_correct
    assert not assess_exercise_offline(interaction=generated, answer="Sergej je kurier.").is_correct


def test_order_token_repair_preserves_token_length_limit():
    with pytest.raises(AIResponseError):
        parse_generated_exercise(json.dumps({"question": "Q", "instruction": "I", "interaction_type": "order", "tokens": ["Ahoj", "Peter"], "accepted_answers": ["Ahoj Peter" + "." * 100]}))


def test_correct_tutor_assessment_cannot_keep_a_contradictory_low_score():
    assessment = parse_tutor_assessment(
        '{"is_correct":true,"score":1,"corrected_answer":"Dnes musím pracovať.",'
        '"explanation":"Правильно.","next_exercise":"Продолжайте."}'
    )
    assert assessment.is_correct is True
    assert assessment.score == 100


def test_generated_exercise_interactions_validate_and_round_trip():
    generated = parse_generated_exercise(
        '{"question":"Соберите фразу.","instruction":"Нажмите на слова по порядку.",'
        '"interaction_type":"order","tokens":["sa","Ako","máš?"],"accepted_answers":["Ako sa máš?"]}'
    )
    snapshot = encode_exercise_snapshot("Только пройденная тема.", generated)
    theory, interaction = decode_exercise_snapshot(snapshot)
    assert theory == "Только пройденная тема."
    assert interaction.interaction_type == "order"
    assert interaction.tokens == ["sa", "Ako", "máš?"]
    assert interaction.accepted_answers == ["Ako sa máš?"]


@pytest.mark.parametrize(
    "payload",
    [
        '{"question":"Q","instruction":"I","interaction_type":"choice","options":["один"]}',
        '{"question":"Q","instruction":"I","interaction_type":"order","tokens":[]}',
        '{"question":"Q","instruction":"I","interaction_type":"match","pairs":[{"prompt":"A","answer":"B"}]}',
        '{"question":"Q","instruction":"I","interaction_type":"choice","options":["A","A"]}',
        '{"question":"Q","instruction":"I","interaction_type":"order","tokens":["Dobrý","deň"],"accepted_answers":["Dobrú noc"]}',
    ],
)
def test_generated_exercise_rejects_incomplete_game_payloads(payload):
    with pytest.raises(AIResponseError):
        parse_generated_exercise(payload)


def test_generated_exercise_requires_reference_answers():
    with pytest.raises(AIResponseError):
        parse_generated_exercise('{"question":"Переведите.","instruction":"Введите ответ."}')


def test_generated_exercise_choice_reference_must_be_an_option():
    with pytest.raises(AIResponseError):
        parse_generated_exercise(
            '{"question":"Выберите.","instruction":"Нажмите вариант.",'
            '"interaction_type":"choice","options":["Ahoj","Dobrý deň"],"accepted_answers":["Čau"]}'
        )


def test_requested_generated_exercise_interaction_is_read_from_progress_context():
    assert requested_exercise_interaction("Формат нового упражнения: Собери фразу.\nТип интерактива: order.") == "order"
    assert requested_exercise_interaction("Старый контекст без типа") is None
