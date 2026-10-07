# Локальный запуск

Проект рассчитан на Windows и локальный loopback.

1. Установи Python 3.12+ и Node.js 22+; добавь Python в PATH.
2. Запусти `install.cmd`.
3. При необходимости создай ignored `.env` по `.env.example`.
4. Запусти `start.cmd`; диагностика — `doctor.cmd`, остановка — `stop.cmd`.

Backend слушает `127.0.0.1:8000`, frontend — `127.0.0.1:3000`. Launcher не
убивает чужие процессы на этих портах и сохраняет PID/start-time и логи в
`%LOCALAPPDATA%\SlovoKrok\launcher`. Старую ignored `.runtime/` launcher не
переносит и не удаляет. Общую папку можно переопределить только абсолютным
`SLOVOKROK_DATA_DIR` до запуска.

Публичный deployment не поддерживается. Нельзя открывать локальный Codex CLI
bridge в сеть. Production/auth/PostgreSQL требуют отдельного security design.

CI использует Python 3.12 и Node.js 22. Python-зависимости устанавливаются из
`backend/requirements.lock.txt` с обязательной проверкой хешей, Node — через
`npm ci`. Те же lock-файлы использует `install.cmd`; широкие диапазоны в
исходных manifest-файлах не участвуют в воспроизводимой установке.
