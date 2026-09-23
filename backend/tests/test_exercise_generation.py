import pytest

from app.tutor import AIResponseError, decode_exercise_snapshot, encode_exercise_snapshot, parse_generated_exercise, parse_tutor_assessment, requested_exercise_interaction


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
