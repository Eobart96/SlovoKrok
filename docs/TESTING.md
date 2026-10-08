# Тестирование

## Backend

Из `backend/`:

```powershell
.venv\Scripts\python.exe -m pip install --require-hashes -r requirements.lock.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall -q app tests
```

`requirements.lock.txt` фиксирует транзитивное дерево и хеши для Python 3.12.
После изменения `requirements.txt` lock обновляется и проверяется так:

```powershell
uv pip compile backend/requirements.txt --output-file backend/requirements.lock.txt --generate-hashes --python-version 3.12
node scripts/verify-python-lock.mjs
```

Pytest считает неожиданные warnings ошибками. Единственное точное исключение —
известное upstream-предупреждение Starlette/AnyIO `BlockingPortal`; его нельзя
расширять до подавления всех `DeprecationWarning`.

Активный набор проверяет route boundary, строгий state round-trip, чтение
legacy schema v1, revision/conflict для autosave и backup restore, сохранность
прогресса после startup, tutor contract и lifecycle упражнений, чтения,
словаря и домашних заданий. `test_database_migrations.py` дополнительно
проверяет SQLite PRAGMA/FK, WAL, upgrade только временной копии, pre-migration
backup, идемпотентность, отказ на неизвестной истории и полный rollback сбоя.
`test_route_contracts.py` фиксирует точный набор course/tutor методов и URL, а
также именованные success response schemas, чтобы внутреннее разбиение router
и tutor-модулей не меняло публичный API.

`test_interactive_api.py` также прогоняет все шесть AI-write путей заданий
(создание и проверка упражнения, чтения и домашней работы) с недоступным
provider и неверным JSON, а также все task write/delete пути с ошибкой SQLite.
Ожидаются стабильные `502/503`, rollback и отсутствие необработанной `500`.

## Frontend

Из `frontend/`:

```powershell
npm.cmd run validate:a1
npm.cmd run test:unit
npm.cmd run build
npm.cmd run check:bundle
```

`test:unit` быстро проверяет чистую логику сохранения прогресса, подсчёта,
состояния переводчика, отображения API-ошибок, timeout, caller cancellation и
отсутствие blind retry в transport layer. Для упражнений, чтения и домашней
работы он отдельно проверяет read-only восстановление после потерянного ответа:
POST/DELETE не повторяется, а уже сохранённый объект или попытка находятся
последующим GET. Там же проверяются прямой browser URL в обход Next proxy и
пакет, который сохраняет успешные элементы при единичном сбое и прекращает
работу после трёх последовательных ошибок. Backend route-тест фиксирует CORS
только для двух локальных frontend origins. `check:bundle` после production
build контролирует размер начального `/page` chunk и не допускает возврата
дополнительного словаря в стартовую загрузку. Также подтверждает наличие
материала A2 в отдельных файлах и его отсутствие во всех стартовых файлах
страницы. `validate:a2` сверяет лёгкий каталог позиций с готовыми уроками;
unit-тесты проверяют общий импорт, кеш и повтор после ошибки загрузки.
`validate:a1` проверяет content
invariants и TypeScript. UI-тесты запускаются
только по прямому запросу владельца командой `npm.cmd run test:ui`; они
подменяют backend/provider и не меняют реальную SQLite.
Development server использует `.next-dev`, а production build — `.next`,
поэтому `npm.cmd run build` не должен повреждать кеш запущенного приложения.

## Repository

Из корня:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/windows/platform.ps1 -Mode SelfTest
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/windows/check-repository.ps1
git diff --check
git status --short
```

CI устанавливает Python только из хешированного lock-файла, запускает backend
tests/compileall, frontend validation/build, production `npm audit`, Python
`pip-audit` и `git diff --check` только для диапазона изменений.

Read-only dependency checks:

```powershell
backend\.venv\Scripts\python.exe -m pip check
uvx --from pip-audit==2.10.1 pip-audit --require-hashes -r backend/requirements.lock.txt
Set-Location frontend
npm.cmd audit --omit=dev --audit-level=high
```
