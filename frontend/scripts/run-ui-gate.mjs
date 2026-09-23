import { spawnSync } from "node:child_process";

const [pattern, marker] = process.argv.slice(2);
if (!pattern || !marker) {
  console.error("Usage: node scripts/run-ui-gate.mjs <pattern> <success-marker>");
  process.exit(2);
}

const result = spawnSync(process.execPath, ["scripts/run-ui-tests.mjs", "-g", pattern], {
  cwd: process.cwd(),
  encoding: "utf8",
  stdio: "pipe",
});

process.stdout.write(result.stdout ?? "");
process.stderr.write(result.stderr ?? "");
if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}
if (result.status !== 0) process.exit(result.status ?? 1);
console.log(marker);
