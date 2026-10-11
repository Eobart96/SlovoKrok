import type { CourseModule } from "../../../courseTypes";
import { plannedA2Module4 } from "../../../a2CourseRoadmap";
import { a2AspectInNarrativeLesson } from "./lessons/aspect-in-narrative";
import { a2AspectPrefixPairsLesson } from "./lessons/aspect-prefix-pairs";
import { a2AspectStemPairsLesson } from "./lessons/aspect-stem-pairs";
import { a2AspectPresentPastLesson } from "./lessons/aspect-present-past";
import { a2ImperfectiveFutureLesson } from "./lessons/imperfective-future";
import { a2PerfectiveFutureLesson } from "./lessons/perfective-future";
import { a2MotionVerbsLesson } from "./lessons/motion-verbs";
import { a2ReflexiveSaSiLesson } from "./lessons/reflexive-sa-si";
import { a2ImperativeRequestsLesson } from "./lessons/imperative-requests";
import { a2ConditionalByLesson } from "./lessons/conditional-by";
import { a2ConditionalModalsLesson } from "./lessons/conditional-modals";
import { a2VerbalNounsParticiplesLesson } from "./lessons/verbal-nouns-participles";

const narrativeLessons = [a2AspectInNarrativeLesson, a2AspectPrefixPairsLesson, a2AspectStemPairsLesson];
const tenseLessons = [a2AspectPresentPastLesson, a2ImperfectiveFutureLesson, a2PerfectiveFutureLesson];
const actionLessons = [a2MotionVerbsLesson, a2ReflexiveSaSiLesson, a2ImperativeRequestsLesson];
const conditionalLessons = [a2ConditionalByLesson, a2ConditionalModalsLesson, a2VerbalNounsParticiplesLesson];
const lessons = [...narrativeLessons, ...tenseLessons, ...actionLessons, ...conditionalLessons];

export const a2Module4: CourseModule = {
  slug: plannedA2Module4.slug, order: 4, title: plannedA2Module4.title,
  level: "A2", description: plannedA2Module4.description, lessons,
  topicGroups: [
    { id: "a2-m4-narrative-and-pairs", title: "Рассказ и видовые пары", slovakTitle: "Rozprávanie a vidové dvojice", description: "Фон и событие, приставки, суффиксы и смена основы.", lessonSlugs: narrativeLessons.map(({ slug }) => slug) },
    { id: "a2-m4-aspect-and-tense", title: "Вид и время", slovakTitle: "Vid a čas", description: "Настоящее и прошедшее, будущее процесса и результата.", lessonSlugs: tenseLessons.map(({ slug }) => slug) },
    { id: "a2-m4-motion-reflexives-imperative", title: "Движение, sa/si и инструкции", slovakTitle: "Pohyb, zvratnosť a pokyny", description: "Маршруты, значения частиц и вежливые команды.", lessonSlugs: actionLessons.map(({ slug }) => slug) },
    { id: "a2-m4-conditional-and-result-forms", title: "Условные просьбы и формы результата", slovakTitle: "Podmieňovací spôsob a výsledné tvary", description: "Кондиционал, модальные просьбы и советы, названия действий и состояния.", lessonSlugs: conditionalLessons.map(({ slug }) => slug) },
  ],
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
