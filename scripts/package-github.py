"""Copy an exact public source snapshot; never stage, commit or publish it."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"AGENTS.md", "PROJECT_CHECKPOINT.md", "PROJECT_HISTORY.md", "PROJECT_REPORT.md"}
PREFIXES = (".ai/", ".codex/")
PUBLIC_PREPARATION = """# Публичный снимок исходников

Включены приложение, тесты, CI, публичная документация, учебные PDF A2
и базовые задания A1 (83 темы, 1660 упражнений, 166 текстов, 166 ДЗ).
Личные данные, зависимости, сборки и локальные записи агента исключены.

Состав фиксируется внешним manifest: пути, размеры и SHA-256 каждого файла.
Проверка требует отсутствия пропусков, лишних файлов и несовпадений хешей.
Копия создана без `.git`, поэтому не содержит историю исходного репозитория.
Сборка и UI этой копии отдельно не запускались; CI выполняется после публикации.

Публикация и добавление файлов в Git не выполняются сборщиком.
Если обновляется существующий репозиторий, его прежняя история сохраняется.
След ранее обнаруженного credential в старой истории требует отзыва ключа;
чистый текущий снимок сам по себе не очищает историю GitHub.
"""


def digest(content):
    return hashlib.sha256(content).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("destination")
    parser.add_argument("archive")
    args = parser.parse_args()
    manifest = (ROOT / args.manifest).resolve()
    destination = (ROOT / args.destination).resolve()
    archive_path = (ROOT / args.archive).resolve()
    if not manifest.is_relative_to(ROOT / "tmp") or not destination.is_relative_to(ROOT / "_git-package") or destination == ROOT / "_git-package" or not archive_path.is_relative_to(ROOT / "tmp") or archive_path.suffix != ".zip":
        raise SystemExit("Unsafe output path")
    if destination.exists() or archive_path.exists():
        raise SystemExit("Output already exists; use a new name")
    subprocess.run(["node", str(ROOT / "scripts/git-candidate.mjs"), "--verify", str(manifest)], cwd=ROOT, check=True)
    source = json.loads(manifest.read_text(encoding="utf-8"))
    files = [item for item in source["files"] if item["path"] not in EXCLUDED and not item["path"].startswith(PREFIXES)]
    required = {"README.md", "README.en.md", "README.sk.md", ".github/workflows/ci.yml", ".gitignore", "LICENSE", "install.cmd", "start.cmd", "frontend/public/task-packs/slovokrok-a1-basic-v1.json", "scripts/build-basic-task-pack.cjs", "scripts/validate-basic-task-pack.py"}
    if not required.issubset({item["path"] for item in files}):
        raise SystemExit("Missing source requirements")
    overrides = {"docs/GIT_PREPARATION.md": PUBLIC_PREPARATION.encode()}
    result = []
    for item in files:
        src = (ROOT / item["path"]).resolve()
        if not src.is_relative_to(ROOT) or src.is_symlink():
            raise SystemExit("Unsafe source path")
        content = src.read_bytes()
        if digest(content) != item["sha256"]:
            raise SystemExit("Source changed during copy")
        content = overrides.get(item["path"], content)
        if item["path"] == "TESTING_START.md":
            content = content.decode("utf-8").replace("Учебные PDF A2 в этот\nархив не включены; они распространяются отдельно.", "Учебные PDF A2 включены в `output/pdf/A2/`.").replace("Учебные PDF A2 в этот\r\nархив не включены; они распространяются отдельно.", "Учебные PDF A2 включены в `output/pdf/A2/`.").encode()
        target = destination / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        result.append({"path": item["path"], "bytes": len(content), "sha256": digest(content)})
    expected = {item["path"] for item in result}
    actual = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
    if expected != actual or any(digest((destination / item["path"]).read_bytes()) != item["sha256"] for item in result):
        raise SystemExit("Copy composition or hash mismatch")
    # Every relative Markdown link in the public copy must resolve.
    for path in destination.rglob("*.md"):
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            target = link.split("#")[0].split(" ")[0].strip("<>")
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            if not (path.parent / target).exists():
                raise SystemExit(f"Broken link: {path.relative_to(destination)} -> {target}")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in result:
            archive.writestr("SlovoKrok/" + item["path"], (destination / item["path"]).read_bytes())
    with zipfile.ZipFile(archive_path) as archive:
        if set(archive.namelist()) != {"SlovoKrok/" + item["path"] for item in result} or len(archive.namelist()) != len(result):
            raise SystemExit("ZIP composition mismatch")
        if any(digest(archive.read("SlovoKrok/" + item["path"])) != item["sha256"] for item in result):
            raise SystemExit("ZIP hash mismatch")
    report_path = manifest.with_name(manifest.stem + "-public.json")
    with report_path.open("x", encoding="utf-8") as report:
        json.dump({"version": 1, "source_manifest": manifest.name, "destination": str(destination), "archive": str(archive_path), "files": result}, report, ensure_ascii=False, indent=2)
    print(f"GITHUB_PACKAGE_OK files={len(result)} bytes={sum(item['bytes'] for item in result)} missing=0 extra=0 hash_mismatches=0")
    print(destination)
    print(f"ZIP_OK bytes={archive_path.stat().st_size} {archive_path}")


if __name__ == "__main__":
    main()
