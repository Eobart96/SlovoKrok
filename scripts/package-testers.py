"""Build a source ZIP for Windows testers from a verified Git candidate."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {"README.md", "TESTING_START.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "UPDATES.md", ".env.example", "install.cmd", "start.cmd", "stop.cmd", "doctor.cmd"}


def selected(path):
    return path in ROOT_FILES or path.startswith(("backend/app/", "frontend/", "course-content/", "docs/")) or path in {"backend/requirements.txt", "backend/requirements.lock.txt", "scripts/windows/platform.ps1"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("destination")
    args = parser.parse_args()
    manifest = (ROOT / args.manifest).resolve()
    destination = (ROOT / args.destination).resolve()
    if not manifest.is_relative_to(ROOT / "tmp") or not destination.is_relative_to(ROOT / "tmp") or destination.suffix != ".zip":
        raise SystemExit("Manifest and ZIP must stay inside tmp/.")
    subprocess.run(["node", str(ROOT / "scripts/git-candidate.mjs"), "--verify", str(manifest)], cwd=ROOT, check=True)
    candidate = json.loads(manifest.read_text(encoding="utf-8"))
    files = [item for item in candidate["files"] if selected(item["path"])]
    required = {"TESTING_START.md", "install.cmd", "start.cmd", "stop.cmd", "doctor.cmd", "scripts/windows/platform.ps1", "backend/app/main.py", "backend/requirements.lock.txt", "frontend/package.json", "frontend/package-lock.json", "course-content/slovak-a1/learning/student_profile.md", "frontend/public/task-packs/slovokrok-a1-basic-v1.json"}
    if not required.issubset({item["path"] for item in files}):
        raise SystemExit("Missing required runtime or tester instructions.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in files:
            path = (ROOT / item["path"]).resolve()
            if not path.is_relative_to(ROOT) or path.is_symlink():
                raise SystemExit("Unsafe source path.")
            content = path.read_bytes()
            if hashlib.sha256(content).hexdigest() != item["sha256"]:
                raise SystemExit("Source changed during packaging.")
            archive.writestr("SlovoKrok/" + item["path"], content)
        archive.writestr("SlovoKrok/package-manifest.json", json.dumps({"version": 1, "files": files}, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(destination) as archive:
        expected = {"SlovoKrok/" + item["path"] for item in files} | {"SlovoKrok/package-manifest.json"}
        if set(archive.namelist()) != expected or len(archive.namelist()) != len(expected):
            raise SystemExit("Archive composition mismatch.")
        for item in files:
            if hashlib.sha256(archive.read("SlovoKrok/" + item["path"])).hexdigest() != item["sha256"]:
                raise SystemExit("Archive hash mismatch.")
    print(f"TESTER_PACKAGE_OK files={len(files)} bytes={destination.stat().st_size}")
    print(destination)


if __name__ == "__main__":
    main()
