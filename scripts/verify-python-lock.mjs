import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = process.cwd();
const requirements = resolve(root, "backend/requirements.txt");
const lock = resolve(root, "backend/requirements.lock.txt");
const temporaryDirectory = mkdtempSync(join(tmpdir(), "slovokrok-python-lock-"));
const generatedLock = join(temporaryDirectory, "requirements.lock.txt");
const compileCommand =
  "uv pip compile backend/requirements.txt --output-file backend/requirements.lock.txt --generate-hashes --python-version 3.12";

try {
  const result = spawnSync(
    "uv",
    [
      "pip",
      "compile",
      requirements,
      "--output-file",
      generatedLock,
      "--generate-hashes",
      "--python-version",
      "3.12",
      "--custom-compile-command",
      compileCommand,
    ],
    { cwd: root, encoding: "utf8", stdio: "pipe" },
  );

  if (result.error) throw result.error;
  if (result.status !== 0) {
    process.stdout.write(result.stdout ?? "");
    process.stderr.write(result.stderr ?? "");
    process.exit(result.status ?? 1);
  }

  if (readFileSync(generatedLock, "utf8") !== readFileSync(lock, "utf8")) {
    console.error("backend/requirements.lock.txt is stale. Regenerate it with the command in its header.");
    process.exit(1);
  }

  console.log("PYTHON_LOCK_VERIFIED");
} finally {
  rmSync(temporaryDirectory, { recursive: true, force: true });
}
