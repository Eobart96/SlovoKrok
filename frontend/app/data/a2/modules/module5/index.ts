import type { CourseModule } from "../../../courseTypes";
import { plannedA2Module5 } from "../../../a2CourseRoadmap";
import { a2ConjunctionsLesson } from "./lessons/conjunctions-a-ale-alebo";
import { a2PairedConjunctionsLesson } from "./lessons/paired-conjunctions";
import { a2ReportedStatementsLesson } from "./lessons/reported-statements-ze";
import { a2RelativeClausesLesson } from "./lessons/relative-clauses-ktory";
import { a2EmbeddedQuestionsLesson } from "./lessons/embedded-questions";
import { a2CauseConsequenceLesson } from "./lessons/cause-and-consequence";
import { a2TimeConditionLesson } from "./lessons/time-and-real-condition";
import { a2ConnectedStoryLesson } from "./lessons/connected-story-focus";

const messageLessons = [a2ConjunctionsLesson, a2PairedConjunctionsLesson, a2ReportedStatementsLesson];
const clauseLessons = [a2RelativeClausesLesson, a2EmbeddedQuestionsLesson, a2CauseConsequenceLesson];
const storyLessons = [a2TimeConditionLesson, a2ConnectedStoryLesson];
const lessons = [...messageLessons, ...clauseLessons, ...storyLessons];

export const a2Module5: CourseModule = {
  slug: plannedA2Module5.slug, order: 5, title: plannedA2Module5.title,
  level: "A2", description: plannedA2Module5.description, lessons,
  topicGroups: [
    { id: "a2-m5-conjunctions-and-messages", title: "Союзы и передача сообщения", slovakTitle: "Spojky a sprostredkovanie správy", description: "Добавление, контраст, выбор, парные союзы и содержание сообщения с že.", lessonSlugs: messageLessons.map(({ slug }) => slug) },
    { id: "a2-m5-relative-questions-and-cause", title: "Уточнение, неизвестное и причина", slovakTitle: "Spresnenie, neznáma informácia a príčina", description: "Ktorý, косвенные вопросы kto/čo/kde и связь причины с результатом.", lessonSlugs: clauseLessons.map(({ slug }) => slug) },
    { id: "a2-m5-time-condition-and-story", title: "Время, условие и связный рассказ", slovakTitle: "Čas, podmienka a súvislé rozprávanie", description: "Kedy/keď/ak, последовательность событий, известное и новое, смысловой акцент.", lessonSlugs: storyLessons.map(({ slug }) => slug) },
  ],
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
