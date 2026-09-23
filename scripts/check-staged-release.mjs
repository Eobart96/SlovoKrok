import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";

const safeDirectory = process.cwd().replaceAll("\\", "/");
const output = execFileSync("git", [
  "-c",
  `safe.directory=${safeDirectory}`,
  "diff",
  "--cached",
  "--name-only",
  "--diff-filter=ACMR",
  "-z",
]);
const paths = output.toString("utf8").split("\0").filter(Boolean).map((path) => path.replaceAll("\\", "/"));

assert.ok(paths.length > 0, "No staged publish candidate");
for (const required of ["README.md", "PROJECT_CHECKPOINT.md", "PROJECT_HISTORY.md", "course-content/slovak-a1/learning/learning_roadmap.md"]) {
  assert.ok(paths.includes(required), `Required publish document is not staged: ${required}`);
}

const forbidden = [
  /^\.unlazy\//,
  /^GATES\.md$/,
  /^\.claude\//,
  /^\.ai\/private\//,
  /^backend\/data\//,
  /(^|\/)\.env(?:\.|$)/,
  /(^|\/)(?:node_modules|\.next|\.next-dev|\.next-build|\.venv|__pycache__|\.pytest_cache)(?:\/|$)/,
  /(^|\/)(?:del|_git-package|_backups)(?:\/|$)/,
  /(?:\.db|\.sqlite3|\.bak|\.log)$/i,
  /sync-conflict|~syncthing~/i,
  /(?:playwright-report|test-results)\//,
];

const blocked = paths.filter((path) => path !== ".env.example" && forbidden.some((pattern) => pattern.test(path)));
assert.deepEqual(blocked, [], `Forbidden staged paths: ${blocked.join(", ")}`);

console.log(`STAGED_RELEASE_SAFE: ${paths.length} paths`);
