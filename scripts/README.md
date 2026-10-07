# Скрипты проекта

Запускайте команды из корня репозитория, если не указано другое.
Для обычного использования достаточно `install.cmd`, `start.cmd`,
`stop.cmd` и `doctor.cmd` в корне.

| Задача | Файлы |
|---|---|
| Запуск на Windows | `windows/platform.ps1`, корневые `.cmd` |
| Пересборка базового пакета A1 | `build-basic-task-pack.cjs` |
| Проверка пакета на отдельной БД | `validate-basic-task-pack.py` |
| Проверка публичного состава | `git-candidate.mjs`, `windows/check-repository.ps1` |
| Сборка исходников для передачи | `package-github.py`, `package-testers.py` |
| Изменённые строки Git | `run-git-diff-check.mjs` |
| Проверка Python lock-файла | `verify-python-lock.mjs` |

## Учебные PDF A2

Нумерация в имени скрипта соответствует теме курса, например
`build_a2_module_2_1.py` и `verify-a2-pdf-2-1.py` для темы 2.1.

- `build_a2_module_*.py` — сборка отдельных учебных PDF.
- `verify-a2-pdf*.py` — проверки отдельного PDF и всей коллекции.
- `verify-a2-roadmap.mjs` — проверка плана A2.
- `organize-a2-pdfs.mjs`, `verify-a2-pdf-organization.mjs` — организация коллекции.
- `build_a2_pdf_prompts.mjs`, `verify-a2-pdf-prompts.mjs` — промты для создания материалов.
- `windows/run-a2-pdf-verifiers.ps1` — запуск проверок PDF на Windows.

Учебные файлы находятся в [output/pdf/A2](../output/pdf/A2/).
Пути скриптов сохранены, чтобы существующие команды продолжали работать.

Обычные frontend-проверки находятся в `frontend/scripts/`; команды и
ограничения описаны в [docs/TESTING.md](../docs/TESTING.md).
