import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, readdirSync, renameSync, statSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const root = process.cwd();
const pdfRoot = join(root, "output", "pdf");
const a2Root = join(pdfRoot, "A2");

const hashFile = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
const flat = readdirSync(pdfRoot, { withFileTypes: true })
  .filter((entry) => entry.isFile() && /^Slovak_A2_Tema_\d+_\d+_.+\.pdf$/u.test(entry.name))
  .map((entry) => join(pdfRoot, entry.name));

const nested = [];
for (let module = 1; module <= 8; module += 1) {
  const dir = join(a2Root, `Module_${String(module).padStart(2, "0")}`);
  mkdirSync(dir, { recursive: true });
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isFile() && /^Slovak_A2_Tema_\d+_\d+_.+\.pdf$/u.test(entry.name)) nested.push(join(dir, entry.name));
  }
}

if (!((flat.length === 72 && nested.length === 0) || (flat.length === 0 && nested.length === 72))) {
  throw new Error(`Unexpected migration state: flat=${flat.length}, nested=${nested.length}`);
}

if (flat.length === 72) {
  for (const source of flat) {
    const name = basename(source);
    const match = name.match(/^Slovak_A2_Tema_(\d+)_(\d+)_/u);
    if (!match) throw new Error(`Cannot parse topic from ${name}`);
    const module = Number(match[1]);
    const targetDir = join(a2Root, `Module_${String(module).padStart(2, "0")}`);
    const target = join(targetDir, name);
    const before = hashFile(source);
    renameSync(source, target);
    const after = hashFile(target);
    if (before !== after || statSync(target).size < 40_000) throw new Error(`Move integrity failed: ${name}`);
  }
}

const scriptDir = join(root, "scripts");
const pythonFiles = readdirSync(scriptDir)
  .filter((name) => /^(?:build_a2_module_|verify-a2-pdf-).+\.py$/u.test(name))
  .map((name) => join(scriptDir, name));

for (const path of pythonFiles) {
  let text = readFileSync(path, "utf8");
  const filename = text.match(/Slovak_A2_Tema_(\d+)_(\d+)_[A-Za-z0-9_]+\.pdf/u);
  if (!filename) continue;
  const moduleDir = `Module_${String(Number(filename[1])).padStart(2, "0")}`;
  const replacements = [
    ["ROOT / \"output\" / \"pdf\" / \"Slovak_A2_Tema_", `ROOT / \"output\" / \"pdf\" / \"A2\" / \"${moduleDir}\" / \"Slovak_A2_Tema_`],
    ["ROOT / \"output/pdf/Slovak_A2_Tema_", `ROOT / \"output/pdf/A2/${moduleDir}/Slovak_A2_Tema_`],
    ["ROOT/\"output/pdf/Slovak_A2_Tema_", `ROOT/\"output/pdf/A2/${moduleDir}/Slovak_A2_Tema_`],
  ];
  for (const [from, to] of replacements) text = text.replaceAll(from, to);
  writeFileSync(path, text, "utf8");
}

const special = join(scriptDir, "windows", "check-a2-pdf-1-2-replacement.ps1");
let specialText = readFileSync(special, "utf8");
specialText = specialText.replaceAll("output\\pdf\\Slovak_A2_Tema_1_2_", "output\\pdf\\A2\\Module_01\\Slovak_A2_Tema_1_2_");
writeFileSync(special, specialText, "utf8");

console.log("A2 PDF migration completed");
