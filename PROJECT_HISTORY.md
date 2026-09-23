# История выполнения SlovoKrok

Этот файл хранит общую историю для владельца проекта. Новые записи располагаются
сверху. По правилам `AGENTS.md` агент добавляет их через служебный маркер, не
читая накопленное содержимое.

<!-- AGENT_APPEND_HERE -->

## 2026-09-23 — Подготовлен проверенный снимок проекта для GitHub

- Зафиксирован прогресс владельца: Modules 1–6 приняты вручную (67/83), Module 7 сейчас проверяется.
- Сведены в единый снимок накопленные изменения приложения, backend, frontend, тестов и актуальной документации.
- Подтверждены backend-тесты и компиляция, frontend unit/content/build/bundle, аудит репозитория и безопасность staged-состава.
- UI/Playwright-тесты не запускались по постоянному правилу проекта; финальную приёмку интерфейса выполняет владелец.

## 2026-09-23 — Документация и request policy

- Добавлен общий frontend request layer: 30 секунд для локальных запросов, 310 секунд для AI, caller cancellation и отдельные timeout/network/invalid-response ошибки.
- Blind transport retry отсутствует; безопасное повторение dirty course state остаётся под revision/`409`.
- README и документы API, архитектуры, базы, AI и тестирования сверены с routes, backup v1/v2, runtime storage и текущими командами.
- Подтверждены 10 frontend unit-тестов, validation/build/bundle budget, 93 backend tests и repository audit; UI/Playwright не запускались по правилу проекта.

## 2026-09-22 — Frontend bundle и быстрые тесты

- Начальный `/page` chunk уменьшен с 493700 до 388812 байт gzip (−21,2%) за счёт lazy-loading редких режимов и удаления дополнительного словаря из startup path.
- Добавлен автоматический bundle budget с проверкой, что каталог остаётся в отложенных chunks.
- Добавлены 4 unit-теста для progress merge, scoring, состояния переводчика и API error mapping; CI запускает unit и bundle checks.
- Подтверждены frontend validation/build, 93 backend tests и repository audit; UI/Playwright не запускались по постоянному правилу проекта.

## 2026-09-17 — воспроизводимые зависимости и CI

- Добавлен хешированный Python 3.12 lock; `install.cmd` и CI используют lock и `npm ci`.
- Pytest обновлён до 9.1.1, SQLite test connections закрываются явно, неожиданные warnings считаются ошибками.
- CI проверяет backend/frontend, Python/npm vulnerabilities и whitespace диапазона изменений.
- Подтверждено: 93 backend tests, compileall, validation/build, lock verification, repository audit; оба security-аудита чистые.
- UI/Playwright не запускались по постоянному правилу; GitHub workflow локально настроен, но удалённый CI не запускался.

## 2026-09-17 — Backend route and tutor separation

- Split course and tutor HTTP routes into focused domain modules while preserving every public URL and named response schema.
- Split tutor contracts, parsing, prompts, exercise logic, Codex CLI and OpenAI-compatible adapters behind the stable `app.tutor` facade.
- Added characterization tests for the exact course/tutor method and response surface.
- Verified: 93 backend tests, compileall, course validation, TypeScript/build, repository audit and diff check.
- Constraint: no schema or data migration, public API change, real provider call, UI test, commit, push or release.

## 2026-09-17 — SQLite integrity and versioned migrations

- Runtime SQLite now enables foreign keys, a five-second busy timeout and WAL at startup.
- Added validated pre-migration backups, strict version history and transactional additive migrations with rollback.
- Upgrade tests operate only on temporary legacy copies and prove the source remains byte-for-byte unchanged.
- Verified: 91 backend tests, compileall, course validation, TypeScript/build, repository audit and diff check.
- Constraint: real user data and legacy database files were not read or modified; UI tests were not run.

## 2026-09-17 — Защищён CourseState

- CourseState получил строгие вложенные схемы, bounds и запрет неизвестных полей; legacy schema v1 читается и при записи становится v2.
- Autosave и backup restore используют opaque revision и возвращают `409`, не перезаписывая новый прогресс устаревшим снимком.
- Browser cache хранит revision; при конфликте UI становится read-only, а отказ от локальных изменений требует явного подтверждения.
- Подтверждено: 86 backend-тестов, compileall, валидация курса и production build прошли.
- UI/Playwright не запускались по постоянному правилу проекта; физическая схема SQLite не изменялась.

## 2026-09-17 — Ужесточена AI boundary

- Ответы AI ограничены по размеру и проходят строгую Pydantic-валидацию полей, типов, массивов и `score`.
- Ошибки provider нормализованы в стабильные ответы API: `502`, `503` и `504` без утечки внутренних исключений.
- Codex CLI и OpenAI-compatible provider получили единый timeout; retry OpenAI SDK ограничен одной попыткой.
- Подтверждено: 76 backend-тестов, compileall, валидация курса и production build прошли.
- UI/Playwright не запускались по постоянному правилу проекта; реальный внешний provider отдельно не проверялся.

## 2026-09-17 — восстановлен Next.js runtime

- Ошибка отсутствующего `833.js` подтверждена как смешение dev/build-файлов в `.next`.
- Повреждённый сгенерированный кеш удалён, приложение пересобрано и перезапущено.
- Dev cache перенесён в `.next-dev`, production build продолжает использовать `.next`.
- Проверено: validation/build прошли при работающем dev-сервере; после build HTTP 200 без chunk error.
- Исходники и пользовательские данные не удалялись; UI/Playwright не запускались.

## 2026-09-17 — runtime data migration activated

- После явного разрешения владельца legacy SQLite скопирована в локальный data root.
- Целевая база прошла `PRAGMA quick_check`; подтверждено 348 страниц.
- Исходная база сохранена без изменений; автоматического удаления не выполнялось.
- Legacy AI-settings отсутствовали, поэтому копирование настроек не требовалось.
- Этап 2 закрыт; следующая точка — строгая проверка AI output и provider errors.

## 2026-09-17 — подготовлен перенос runtime data

- SQLite, AI settings, launcher state и логи перенаправлены в per-user data root с абсолютным env override.
- Legacy-файлы копируются без удаления и перезаписи; SQLite-копия проходит `quick_check` и сверку страниц.
- Добавлены rollback opt-in и изоляция тестов от реальных пользовательских данных.
- Подтверждено: 61 backend test, compileall, launcher self-test, frontend validation/build и repository audit.
- Реальная legacy SQLite не копировалась: для этого требуется отдельное явное разрешение владельца.

## 2026-09-17 — Изоляция Codex CLI и защита профиля

- Создан и проверен независимый SQLite snapshot вне синхронизируемого проекта.
- Все Codex CLI процессы запускаются в пустых временных директориях вне
  репозитория и очищают их после завершения, timeout или ошибки запуска.
- Персональный профиль больше не отправляется provider без явного локального
  opt-in; публичный tutor API сохранён.
- Подтверждены 6 целевых и 51 полный backend-тест, compileall, frontend
  validation/build, launcher/repository audit и diff check; UI не запускался.

## 2026-09-17 — Аудит и план укрепления проекта

- Выполнен общий аудит архитектуры, безопасности, хранения данных, AI boundary,
  frontend bundle, тестов и документации.
- Сформирован порядок исправлений: защита AI и приватных данных, перенос runtime
  data, строгие контракты, SQLite/migrations, рефакторинг, CI и оптимизация UI.
- Подтверждены backend tests, compileall, валидация 8 модулей и 83 уроков,
  TypeScript, production build, repository audit и diff check.
- UI/Playwright не запускались по постоянному правилу проекта; `npm audit` не
  выполнялся без разрешённого сетевого доступа.

## Сводное состояние к 2026-09-17

- Собран локальный single-user курс Slovak A1: 8 модулей, 83 урока; владельцем
  вручную приняты модули 1–4.
- Добавлены общий словарь на 2032 уникальные карточки, чтение, упражнения,
  домашние задания, повторение, статистика и offline exercise packs.
- Добавлены AI-настройки, переводчик RU↔SK, уточняющие вопросы, история
  переводов, SQLite persistence и backup format v2.
- Добавлены настройки внешнего вида, персональные шпаргалки, Windows launcher и
  проверки целостности репозитория.
- Накопленные изменения ещё не оформлены отдельным commit/release; ручная
  приёмка модулей 5–8 и интерфейса остаётся за владельцем.
