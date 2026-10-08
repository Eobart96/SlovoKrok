import type { CourseModule, CourseTopicGroup } from "../../../courseTypes";
import { plannedA2Module3 } from "../../../a2CourseRoadmap";
import { a2AdjectiveCaseAgreementLesson } from "./lessons/adjective-case-agreement";
import { a2AdjectivesPluralLesson } from "./lessons/adjectives-plural";
import { a2AdjectiveComparisonLesson } from "./lessons/adjective-comparison";
import { a2AdverbComparisonLesson } from "./lessons/adverb-comparison";
import { a2PersonalPronounCasesLesson } from "./lessons/personal-pronoun-cases";
import { a2PossessivesSvojLesson } from "./lessons/possessives-svoj";
import { a2PossessiveAdjectivesLesson } from "./lessons/possessive-adjectives";
import { a2IndefiniteNegativePronounsLesson } from "./lessons/indefinite-negative-pronouns";
import { a2NumeralsDatesQuantityLesson } from "./lessons/numerals-dates-quantity";

const lessons = [a2AdjectiveCaseAgreementLesson, a2AdjectivesPluralLesson, a2AdjectiveComparisonLesson, a2AdverbComparisonLesson, a2PersonalPronounCasesLesson, a2PossessivesSvojLesson, a2PossessiveAdjectivesLesson, a2IndefiniteNegativePronounsLesson, a2NumeralsDatesQuantityLesson];
const topicGroups: CourseTopicGroup[] = [
  { id: "a2-m3-agreement-and-comparison", title: "Согласование и сравнение", slovakTitle: "Zhoda a stupňovanie", description: "Прилагательные в падежах и сравнение предметов и действий.", lessonSlugs: lessons.slice(0, 4).map(({ slug }) => slug) },
  { id: "a2-m3-pronouns-and-possession", title: "Местоимения и принадлежность", slovakTitle: "Zámená a privlastňovanie", description: "Личные формы, свой и принадлежность конкретному человеку.", lessonSlugs: lessons.slice(4, 7).map(({ slug }) => slug) },
  { id: "a2-m3-sets-and-quantity", title: "Обобщение, числа и даты", slovakTitle: "Zovšeobecnenie, čísla a dátumy", description: "Кто-то, никто, все; точное количество и дата.", lessonSlugs: lessons.slice(7, 9).map(({ slug }) => slug) },
];

export const a2Module3: CourseModule = {
  slug: plannedA2Module3.slug, order: 3, title: plannedA2Module3.title, level: "A2", description: plannedA2Module3.description,
  lessons, topicGroups,
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
