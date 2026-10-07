import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, lstatSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const git = (...args) => execFileSync("git", ["-c", "core.quotepath=false", ...args], {
  cwd: root, encoding: "utf8", maxBuffer: 16 * 1024 * 1024,
});
const forbidden = /(^|\/)(?:\.git|\.env(?:\..*)?|node_modules|\.next(?:-[^/]*)?|\.venv|venv|__pycache__|\.pytest_cache|\.runtime|_backups|_git-package|del|tmp|Install|test-results|playwright-report)(?:\/|$)|(^|\/)(?:backend\/data|\.ai\/private)(?:\/|$)|(?:sync-conflict|~syncthing~)|\.(?:db|sqlite3?|log|bak|pyc|tsbuildinfo)$/i;
const localOnly = /^(?:\.(?:ai|codex|agents|claude|tmp|obsidian-note-staging)(?:\/|$)|AGENTS\.md$|PROJECT_(?:CHECKPOINT|HISTORY|REPORT)\.md$|scripts\/(?:check-course-progress\.mjs|check-staged-release\.mjs|verify-a2-study-skill\.mjs|windows\/check-a2-roadmap-and-skill\.ps1)$)/i;

export function isForbidden(path) {
  return path !== ".env.example" && (forbidden.test(path) || localOnly.test(path));
}

function collect() {
  const paths = [...new Set(git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
    .split("\0").filter(Boolean))].sort();
  const files = [];
  for (const path of paths) {
    const full = resolve(root, path);
    if (!existsSync(full)) continue;
    if (isForbidden(path)) throw new Error(`Forbidden candidate path: ${path}`);
    const realRelative = relative(realpathSync(root), realpathSync(full));
    if (realRelative.startsWith("..") || isAbsolute(realRelative)) throw new Error(`Candidate escapes repository: ${path}`);
    const stat = lstatSync(full);
    if (!stat.isFile()) throw new Error(`Candidate is not a regular file: ${path}`);
    files.push({ path, bytes: stat.size, sha256: createHash("sha256").update(readFileSync(full)).digest("hex") });
  }
  return {
    version: 1,
    head: git("rev-parse", "HEAD").trim(),
    branch: git("branch", "--show-current").trim(),
    staged: git("diff", "--cached", "--name-only", "-z").split("\0").filter(Boolean),
    files,
  };
}

function main() {
  const [mode, givenPath] = process.argv.slice(2);
  if (!["--write", "--verify", "--self-test"].includes(mode)) {
    throw new Error("Use --write [tmp/path.json], --verify tmp/path.json, or --self-test");
  }
  if (mode === "--self-test") {
    for (const path of [".env", ".env.local", "backend/data/a.txt", "backend/app.db", "del/a.ts", "tmp/a.ts", "frontend/node_modules/a.js", ".git/config", ".ai/private/a.md"]) {
      if (!isForbidden(path)) throw new Error(`Negative control missed: ${path}`);
    }
    for (const path of [".env.example", "frontend/app/page.tsx", "output/pdf/A2/Module_01/a.pdf"]) {
      if (isForbidden(path)) throw new Error(`Allowed control rejected: ${path}`);
    }
    console.log("GIT_CANDIDATE_SELF_TEST_OK");
    return;
  }
  if (mode === "--verify" && !givenPath) throw new Error("Specify a saved manifest to verify");
  const path = resolve(root, givenPath ?? `tmp/git-candidates/${Date.now()}.json`);
  const insideTmp = relative(resolve(root, "tmp"), path);
  if (!insideTmp || insideTmp.startsWith("..") || isAbsolute(insideTmp)) throw new Error("Manifest must stay inside tmp/");
  const current = collect();
  if (mode === "--write") {
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, JSON.stringify({ ...current, createdAt: new Date().toISOString() }, null, 2) + "\n", { flag: "wx" });
    console.log(`Manifest: ${path}`);
  } else {
    const saved = JSON.parse(readFileSync(path, "utf8"));
    if (saved.version !== 1 || !Array.isArray(saved.files)) throw new Error("Invalid manifest");
    const previous = new Map(saved.files.map(file => [file.path, file]));
    const present = new Map(current.files.map(file => [file.path, file]));
    const missing = saved.files.filter(file => !present.has(file.path));
    const extra = current.files.filter(file => !previous.has(file.path));
    const changed = current.files.filter(file => previous.has(file.path) && (previous.get(file.path).sha256 !== file.sha256 || previous.get(file.path).bytes !== file.bytes));
    console.log(`missing=${missing.length} extra=${extra.length} hash_mismatches=${changed.length}`);
    for (const file of [...missing, ...extra, ...changed]) console.error(file.path);
    if (missing.length || extra.length || changed.length || saved.head !== current.head || JSON.stringify(saved.staged) !== JSON.stringify(current.staged)) {
      throw new Error("Candidate changed since the saved manifest");
    }
  }
  const bytes = current.files.reduce((sum, file) => sum + file.bytes, 0);
  console.log(`files=${current.files.length} bytes=${bytes} staged=${current.staged.length}`);
  console.log("GIT_CANDIDATE_OK");
}

main();
