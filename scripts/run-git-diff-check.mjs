import { spawnSync } from "node:child_process";

const safeDirectory = process.cwd().replaceAll("\\", "/");
const revisions = process.argv.slice(2);

if (revisions.length !== 0 && revisions.length !== 2) {
  console.error("Usage: node scripts/run-git-diff-check.mjs [base head]");
  process.exit(2);
}

function runGit(args, options = {}) {
  return spawnSync("git", ["-c", `safe.directory=${safeDirectory}`, ...args], {
    cwd: process.cwd(),
    encoding: "utf8",
    stdio: "pipe",
    ...options,
  });
}

function resolves(revision) {
  return runGit(["rev-parse", "--verify", `${revision}^{commit}`]).status === 0;
}

function emptyTree() {
  const result = runGit(["hash-object", "-t", "tree", "--stdin"], { input: "" });
  if (result.status !== 0 || !result.stdout.trim()) {
    process.stderr.write(result.stderr ?? "");
    console.error("Unable to create the empty Git tree used for an initial commit check.");
    process.exit(result.status ?? 1);
  }
  return result.stdout.trim();
}

let diffArgs = ["diff", "--check"];
if (revisions.length === 2) {
  let [base, head] = revisions;
  if (!resolves(head)) {
    console.error(`Head revision does not resolve: ${head}`);
    process.exit(2);
  }
  if (/^0+$/.test(base) || !resolves(base)) {
    base = resolves(`${head}^`) ? `${head}^` : emptyTree();
  }
  diffArgs.push(base, head);
}

const result = runGit(diffArgs);

process.stdout.write(result.stdout ?? "");
process.stderr.write(result.stderr ?? "");
if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}
if (result.status !== 0) process.exit(result.status ?? 1);
console.log("GIT_DIFF_CHECK_PASSED");
