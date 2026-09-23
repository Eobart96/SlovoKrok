const fs = require("node:fs");
const ts = require("typescript");

require.extensions[".ts"] = (module, filename) => {
  const source = fs.readFileSync(filename, "utf8");
  const output = ts.transpileModule(source, {
    compilerOptions: {
      esModuleInterop: true,
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
    },
    fileName: filename,
  }).outputText;
  module._compile(output, filename);
};

const { a1CourseModules, allA1Lessons } = require("../app/data/a1Course.ts");
const { buildModuleFinalQuestions, buildReinforcementPractices } = require("../app/data/coursePractice.ts");

const fail = (message) => { throw new Error(`Test option validation failed: ${message}`); };
const assertClosedOptions = (options, answer, context) => {
  if (!options.includes(answer)) fail(`${context}: answer is missing from options`);
  if (new Set(options).size !== options.length) fail(`${context}: duplicate options`);
};
const assertVaried = (positionsBySize, context) => {
  for (const [size, positions] of positionsBySize) {
    if (positions.length >= 2 && new Set(positions).size < 2) {
      fail(`${context}: ${positions.length} answers with ${size} options stay in one column`);
    }
  }
};
const addPosition = (positionsBySize, options, answer) => {
  const position = options.indexOf(answer);
  positionsBySize.set(options.length, [...(positionsBySize.get(options.length) ?? []), position]);
};

let topicClosedRows = 0;
let finalQuestions = 0;
for (const lesson of allA1Lessons) {
  const sourceBefore = JSON.stringify(lesson);
  const firstBuild = buildReinforcementPractices(lesson);
  const secondBuild = buildReinforcementPractices(lesson);
  if (JSON.stringify(firstBuild) !== JSON.stringify(secondBuild)) fail(`${lesson.slug}: topic option order is not stable`);
  if (JSON.stringify(lesson) !== sourceBefore) fail(`${lesson.slug}: topic builder mutates authored course data`);

  const choicePositionsBySize = new Map();
  for (const practice of firstBuild) {
    if (practice.type === "choice" && practice.options?.length) {
      assertClosedOptions(practice.options, practice.answer, `${lesson.slug}/${practice.id}`);
      addPosition(choicePositionsBySize, practice.options, practice.answer);
      topicClosedRows += 1;
    }
    const pairPositionsBySize = new Map();
    for (const [pairIndex, pair] of (practice.pairs ?? []).entries()) {
      if (!pair.options?.length) continue;
      assertClosedOptions(pair.options, pair.answer, `${lesson.slug}/${practice.id}/row-${pairIndex + 1}`);
      addPosition(pairPositionsBySize, pair.options, pair.answer);
      topicClosedRows += 1;
    }
    assertVaried(pairPositionsBySize, `${lesson.slug}/${practice.id}`);
  }
  assertVaried(choicePositionsBySize, lesson.slug);
}

for (const courseModule of a1CourseModules) {
  const firstBuild = buildModuleFinalQuestions(courseModule.lessons);
  const secondBuild = buildModuleFinalQuestions(courseModule.lessons);
  if (JSON.stringify(firstBuild) !== JSON.stringify(secondBuild)) fail(`${courseModule.slug}: final option order is not stable`);
  const positionsBySize = new Map();
  for (const question of firstBuild) {
    assertClosedOptions(question.options, question.answer, `${courseModule.slug}/${question.id}`);
    addPosition(positionsBySize, question.options, question.answer);
    finalQuestions += 1;
  }
  assertVaried(positionsBySize, `${courseModule.slug}/final`);
}

console.log(`TEST OPTION ORDER VALID: ${allA1Lessons.length} topic assessments, ${topicClosedRows} closed rows, ${finalQuestions} final questions`);
