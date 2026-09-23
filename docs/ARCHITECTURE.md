# Архитектура

## Runtime

```text
Browser -> Next.js :3000 -> /api rewrite -> FastAPI :8000 -> SQLite
                                             |
                                             +-> Codex CLI / OpenAI-compatible API
```

Next.js хранит структуру курса в `frontend/app/data/`; FastAPI не загружает
старый YAML-каталог. Backend сохраняет интерактивное состояние всего курса,
созданные пользователем/AI материалы и историю переводчика.

## Frontend

- `app/page.tsx` — канонический экран;
- `app/new` и `app/module-1` — redirects;
- `app/components/Course*` — универсальный учебный UI;
- `app/components/AiSettingsPanel.tsx` — локальная настройка AI-provider;
- `app/components/FloatingTranslator.tsx` — перемещаемый не модальный переводчик
  поверх экранов курса через выбранный AI-provider;
- `app/data/courseTypes.ts`, `courseEngine.ts`, `courseValidation.ts` — модель,
  операции и инварианты;
- `app/data/coursePractice.ts` — чистая логика проверки ответов, парных
  заданий, закрепления и итоговых вопросов без зависимости от React;
- `app/data/modules/module1` … `module8` — каталог каждого модуля;
- `app/data/modules/moduleN/lessons/` — отдельный файл для каждой темы;
- `app/data/modules/moduleN/index.ts` — порядок тем и проверка полноты модуля;
- `app/data/a1Course.ts` — сборка всего Slovak A1;
- `app/lib/api.ts` — typed backend boundary; `app/lib/request.ts` задаёт единые
  timeout/cancellation и не повторяет один HTTP-запрос автоматически.

## Backend

- `main.py` подключает только system, course и tutor facades;
- `routers/course_routes/` разделяет state, exercises, readings, vocabulary и
  homework, сохраняя общий префикс `/api/v1/course`;
- `routers/tutor_routes/` разделяет settings/login, translation history и
  conversational practice, сохраняя прежние `/api/v1/tutor/*` URL;
- `models.py` содержит модели `Course*`, сопоставленные с прежними физическими
  именами таблиц SQLite для сохранения существующего прогресса;
- `services/startup.py` проверяет SQLite, создаёт pre-migration backup и
  атомарно применяет версионированные additive migrations;
- `services/runtime_data.py` готовит per-user data root и один раз копирует
  legacy SQLite/AI settings без удаления оригиналов;
- `tutor.py` остаётся стабильным import facade; строгие AI contracts, exercise
  logic, parsing и bounded prompts находятся в `tutor_core/`, а Codex CLI и
  OpenAI-compatible adapters — в `tutor_providers/`;
- `services/tutor_settings.py` атомарно сохраняет локальные provider-настройки
  без выдачи API-ключей через response schema.

## Состояние

Frontend course content versioned в Git. Пользовательское состояние, AI settings,
launcher state и логи находятся вне репозитория: на Windows по умолчанию в
`%LOCALAPPDATA%\SlovoKrok`, либо в абсолютном `SLOVOKROK_DATA_DIR`.
Legacy `backend/data/app.db` и `backend/data/ai_settings.json` копируются только
при отсутствии нового назначения и никогда автоматически не удаляются. Явный
SQLite `DATABASE_URL` внутри проекта также считается legacy-источником; внешний
URL сохраняет приоритет.
Три прежних browser-storage key читаются только как fallback импорта прогресса;
их переименование требует отдельного compatibility-перехода.
Локальный session cache хранит также dirty-флаг и последнюю серверную revision.
Все autosave и backup restore передают её backend; при несовпадении запись
останавливается с `409`, не пытаясь автоматически слить потенциально
противоречивые пользовательские данные. Интерфейс становится read-only; перейти
на серверный снимок можно только после явного подтверждения удаления
несохранённых изменений этой вкладки. Course state v1 мигрирует в памяти и
становится v2 только после успешной сравниваемой записи.
Старые classic-таблицы могут физически оставаться в
существующей базе, но compact runtime их не использует.
SQLite runtime включает foreign keys, пятисекундный busy timeout и WAL;
неизвестная migration history или failed quick check блокируют startup вместо
попытки продолжить с неподтверждённой схемой.

## Сетевые запросы браузера

Все обращения frontend к FastAPI проходят через единый request layer. Обычные
локальные операции ограничены 30 секундами, AI-операции — 310 секундами: этот
лимит больше максимальных 300 секунд backend, поэтому при штатном provider
timeout браузер получает контролируемый `504`. Переданный `AbortSignal`
отменяет ожидание отдельно от timeout. Transport layer не повторяет `PUT`,
`POST` и `DELETE`: после потери ответа неизвестно, успел ли сервер зафиксировать
изменение. Очередь autosave может позднее повторить синхронизацию dirty state,
но только с прежней revision; уже выполненная запись тогда даёт `409` и
останавливает очередь вместо двойной записи.

## Границы

Нет регистрации, multi-user, PostgreSQL, очередей, микросервисов и production
deployment. Их добавление требует отдельного ADR и миграционного плана.
