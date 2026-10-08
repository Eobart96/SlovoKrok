import { readFileSync, readdirSync, statSync } from "node:fs";
import { gzipSync } from "node:zlib";
import path from "node:path";

const baselineGzipBytes = 493700;
const budgetGzipBytes = Math.floor(baselineGzipBytes * 0.85);
const buildDirectory = path.join(process.cwd(), ".next");
const manifest = JSON.parse(readFileSync(path.join(buildDirectory, "app-build-manifest.json"), "utf8"));
const pageFiles = manifest.pages?.["/page"] ?? [];
const routeFiles = pageFiles.filter((file) => /static\/chunks\/app\/page-[^/]+\.js$/.test(file));

if (routeFiles.length !== 1) throw new Error(`Expected one /page application chunk, found ${routeFiles.length}`);

const routeSource = routeFiles.map((file) => readFileSync(path.join(buildDirectory, file), "utf8")).join("\n");
// Ready A2 lesson text must remain behind the level's dynamic import.
const a2LessonMarkers = ["Карта готовности: попробуйте, затем оцените", "Вид и время отвечают на разные вопросы", "Вторая позиция: считаем блоки, а не слова", "Самостоятельное чтение и письменная рефлексия", "Кого или что: четыре модели объекта", "Восемь предлогов: выбираем смысл", "Кому? Чему? Формы существительных", "Банк полных триад: учим место как маршрут", "Карта падежей: найдите управляющее слово", "Твёрдая модель: вся карта единственного числа", "Третье лицо и смысловой акцент", "Своя встреча: связываем число, дату и длительность", "Камера рассказа: фон, процесс, событие", "Приставка: граница или другое действие", "Возвращаться и возвращать: сохраняем нужную частицу"];
const initialSource = pageFiles.filter((file) => file.endsWith(".js"))
  .map((file) => readFileSync(path.join(buildDirectory, file), "utf8")).join("\n");
if (a2LessonMarkers.some((marker) => initialSource.includes(marker))) throw new Error("A2 lesson content leaked into initial /page chunks");
const routeGzipBytes = gzipSync(routeSource).byteLength;
if (routeGzipBytes > budgetGzipBytes) {
  throw new Error(`Initial /page chunk is ${routeGzipBytes} gzip bytes; budget is ${budgetGzipBytes}`);
}

function javascriptFiles(directory) {
  return readdirSync(directory).flatMap((name) => {
    const item = path.join(directory, name);
    return statSync(item).isDirectory() ? javascriptFiles(item) : item.endsWith(".js") ? [item] : [];
  });
}

const allChunkSource = javascriptFiles(path.join(buildDirectory, "static", "chunks"))
  .map((file) => readFileSync(file, "utf8"))
  .join("\n");
if (a2LessonMarkers.some((marker) => !allChunkSource.includes(marker))) throw new Error("Could not find ready A2 lesson content in lazy chunks");
const catalog = JSON.parse(readFileSync(path.join(process.cwd(), "app", "data", "additionalVocabularyCatalog.json"), "utf8"));
const candidateTerms = catalog.entries
  .flatMap((entry) => [entry.word, entry.translation, entry.storageSourceId])
  .filter((value) => typeof value === "string" && value.length >= 18);
const catalogTermsInBuild = [...new Set(candidateTerms.filter((term) => allChunkSource.includes(term)))].slice(0, 50);

if (catalogTermsInBuild.length < 20) throw new Error("Could not verify that the additional vocabulary catalog remains in lazy chunks");
const leakedTerms = catalogTermsInBuild.filter((term) => routeSource.includes(term));
if (leakedTerms.length) throw new Error(`Additional vocabulary leaked into the initial /page chunk: ${leakedTerms[0]}`);

const reduction = Math.round((1 - routeGzipBytes / baselineGzipBytes) * 1000) / 10;
console.log(`Initial /page chunk: ${routeGzipBytes} gzip bytes (${reduction}% below ${baselineGzipBytes})`);
console.log("BUNDLE_BUDGET_OK");
