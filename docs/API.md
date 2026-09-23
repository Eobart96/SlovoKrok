# API

Base URL локально: `http://127.0.0.1:8000`. Интерактивная схема доступна в
`/docs` и `/openapi.json`.

## System

- `GET /health` — `{ "status": "ok" }`.

## Tutor

- `POST /api/v1/tutor/module1-chat` — один структурированный шаг чата.
- `POST /api/v1/tutor/translate` — перевод текста до 2 000 символов между
  русским и словацким через выбранный provider; направление `ru-sk|sk-ru`,
  ответ содержит основной перевод, до двух вариантов и необязательное краткое
  пояснение;
- `POST /api/v1/tutor/translate-question` — краткий ответ на вопрос о готовом
  переводе; принимает исходный текст, перевод, направление и вопрос до 1 000
  символов, возвращает валидированный ответ выбранного provider;
- `GET /api/v1/tutor/translation-history?limit=&before_id=` — сохранённые
  переводы с уточняющими вопросами, новые записи первыми;
- `DELETE /api/v1/tutor/translation-history/{id}` — удалить один перевод и
  связанные вопросы;
- `DELETE /api/v1/tutor/translation-history` — очистить всю историю; требует
  тело `{ "confirmation": "delete-translation-history" }`;
- `GET /api/v1/tutor/settings` — выбранный provider, модели, статус Codex и
  только признаки наличия API-ключей;
- `PUT /api/v1/tutor/settings` — выбрать `codex|openai|polza`, сохранить модель
  и при необходимости новый ключ;
- `POST /api/v1/tutor/codex-login` — открыть локальное окно авторизации Codex.

Сохранённые ключи никогда не входят в response schema. Пустое поле ключа при
обновлении сохраняет прежнее значение; удаление требует отдельного флага.

Все tutor, translator, exercise, reading и homework ответы provider проходят
единый строгий JSON boundary. Ошибки имеют стабильный `detail` без текста
внутреннего исключения:

- `502` + `ИИ вернул ответ в неверном формате` — malformed, oversized,
  лишние поля или значения вне допустимых границ;
- `503` + `AI provider временно недоступен` — соединение, rate limit или другая
  ошибка provider;
- `504` + `AI provider не ответил вовремя` — превышен настроенный timeout.

## Course state

- `GET /api/v1/course/state`
- `PUT /api/v1/course/state`

`GET` возвращает `exists`, `schema_version`, opaque `revision`, `state` и
`updated_at`. Каждый `PUT` обязан передать revision из последнего `GET` или
успешного `PUT` в заголовке `X-Course-State-Revision`. Для создания первой
записи используется значение `none`. Отсутствующий заголовок даёт `428`,
неверный формат — `400`, а устаревшая revision — `409`; при конфликте новое
состояние не записывается.

Верхний объект и вложенные mistake/chat/summary/cheat-sheet записи запрещают
неизвестные поля. Статусы прогресса, номера модулей, шаги, булевы значения,
длины строк и размеры коллекций ограничены схемой. Legacy state schema v1
читается с явными значениями по умолчанию и при следующей успешной записи
сохраняется как schema v2. Список `personalCheatSheets` остаётся необязательным:
его отсутствие означает пустой список.

`POST /api/v1/course/backup/restore` использует тот же заголовок revision и
конфликт `409`, поэтому устаревшее окно не может восстановлением затереть более
новый прогресс. Успешный ответ восстановления возвращает новую revision.

## Backup

- `GET /api/v1/course/backup` — экспорт текущего backup format v2;
- `POST /api/v1/course/backup/validate` — проверка backup без записи;
- `POST /api/v1/course/backup/restore` — атомарное восстановление с обязательной
  `X-Course-State-Revision`.

Format v2 включает course state, упражнения, чтение, словарь, домашние задания,
историю переводов и уточняющие вопросы. Format v1 по-прежнему принимается без
таблиц переводчика.

## Exercises

- `GET|POST /api/v1/course/exercises`
- `POST /api/v1/course/exercises/{id}/answer`
- `DELETE /api/v1/course/exercises/{id}`
- `DELETE /api/v1/course/exercises` — удалить все упражнения и их попытки;
  требует тело `{ "confirmation": "delete-all-exercises" }`.

Ответ упражнения дополнительно содержит `interaction_type` (`text`, `choice`,
`order`, `match`) и данные для соответствующего мини-задания: `options`,
`tokens`, `pair_prompts`, `pair_options`. Поля добавочные: старые записи без
интерактивных данных возвращаются как `text` с пустыми массивами. Для `match`
API не возвращает соответствие между левым и правым столбцами; правильные пары
остаются внутри серверного снимка задания и используются только при проверке.
Новые упражнения также сохраняют скрытые допустимые ответы одновременно с
текстом задания. Они не возвращаются браузеру отдельным полем.

Тело `POST /api/v1/course/exercises/{id}/answer` содержит `answer` и добавочный
`assessment_mode`: `online` (значение по умолчанию для старых клиентов) или
`offline`. В online-режиме provider сверяет ответ с сохранённым эталоном и может
принять равноценную формулировку. В offline-режиме backend выполняет
детерминированную проверку сохранённого эталона без вызова provider и сохраняет
обычную попытку. Старое задание без эталона остаётся доступным для online-
проверки, а на offline-проверку отвечает `409` с предложением сменить режим.

## Reading

- `GET|POST /api/v1/course/readings`
- `POST /api/v1/course/readings/{id}/check`
- `DELETE /api/v1/course/readings/{id}`

## Vocabulary

- `PUT /api/v1/course/vocabulary/sync`
- `GET /api/v1/course/vocabulary`
- `POST /api/v1/course/vocabulary/{id}/review`

## Homework

- `GET|POST /api/v1/course/homework`
- `POST /api/v1/course/homework/{id}/submit`
- `DELETE /api/v1/course/homework/{id}`

Точные поля и ограничения определены Pydantic-схемами в
`backend/app/schemas/` и типами `frontend/app/lib/api.ts`. Старые courses,
progress, diary, dialogue, module-test и vocabulary API не существуют и должны
возвращать `404`.

## Политика frontend-запросов

Typed client использует 30-секундный timeout для обычных локальных операций и
310-секундный для действий с AI provider. Длинный лимит намеренно превышает
максимальный backend `TUTOR_TIMEOUT_SECONDS=300`, чтобы backend успевал вернуть
стабильный `504`. Caller cancellation через `AbortSignal` отличается от
timeout и сетевой ошибки. Transport layer не повторяет один HTTP-запрос:
повтор записи после потерянного ответа мог бы продублировать изменение. Очередь
course autosave может позже снова синхронизировать dirty state, но всегда с
opaque revision; уже выполненная запись приводит к безопасному `409`. Backup
restore после потерянного ответа сначала перечитывает серверное состояние.
