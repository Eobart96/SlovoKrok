import type { CourseModule, CourseTopicGroup } from "../../../courseTypes";
import { plannedA2Module2 } from "../../../a2CourseRoadmap";
import { a2NominativePluralThingsLesson } from "./lessons/nominative-plural-things";
import { a2NominativePluralPeopleLesson } from "./lessons/nominative-plural-people";
import { a2AccusativeSingularAgreementLesson } from "./lessons/accusative-singular-agreement";
import { a2AccusativePluralLesson } from "./lessons/accusative-plural";
import { a2GenitiveSingularLesson } from "./lessons/genitive-singular";
import { a2GenitiveQuantityLesson } from "./lessons/genitive-quantity";
import { a2GenitivePluralLesson } from "./lessons/genitive-plural";
import { a2DativeRecipientBenefitCauseLesson } from "./lessons/dative-recipient-benefit-cause";
import { a2LocativePlaceTopicLesson } from "./lessons/locative-place-topic";
import { a2InstrumentalMeansCompanyRoleLesson } from "./lessons/instrumental-means-company-role";
import { a2CaseTriadsLesson } from "./lessons/case-triads";
import { a2CaseSystemGovernmentAddressLesson } from "./lessons/case-system-government-address";

const lessons = [a2NominativePluralThingsLesson, a2NominativePluralPeopleLesson, a2AccusativeSingularAgreementLesson, a2AccusativePluralLesson, a2GenitiveSingularLesson, a2GenitiveQuantityLesson, a2GenitivePluralLesson, a2DativeRecipientBenefitCauseLesson, a2LocativePlaceTopicLesson, a2InstrumentalMeansCompanyRoleLesson, a2CaseTriadsLesson, a2CaseSystemGovernmentAddressLesson];

const topicGroups: CourseTopicGroup[] = [
  {
    id: "a2-m2-plural-and-accusative",
    title: "Множественное число и Akuzatív",
    slovakTitle: "Množné číslo a akuzatív",
    description: "Полное согласование групп предметов и дальнейшая работа с прямым объектом.",
    lessonSlugs: lessons.slice(0, 4).map((lesson) => lesson.slug),
  },
  {
    id: "a2-m2-genitive",
    title: "Genitív: отсутствие и количество",
    slovakTitle: "Genitív: neprítomnosť a množstvo",
    description: "Происхождение, границы, количество, мера и формы множественного числа.",
    lessonSlugs: lessons.slice(4, 7).map((lesson) => lesson.slug),
  },
  {
    id: "a2-m2-dative-locative-instrumental",
    title: "Datív, Lokál и Inštrumentál",
    slovakTitle: "Datív, lokál a inštrumentál",
    description: "Адресат и причина, место и тема, средство и совместность.",
    lessonSlugs: lessons.slice(7, 10).map((lesson) => lesson.slug),
  },
  {
    id: "a2-m2-case-system-and-movement",
    title: "Система падежей и движение",
    slovakTitle: "Systém pádov a pohyb",
    description: "Маршруты, управление, полное согласование и вежливое обращение.",
    lessonSlugs: lessons.slice(10, 12).map((lesson) => lesson.slug),
  },
];

export const a2Module2: CourseModule = {
  slug: plannedA2Module2.slug,
  order: plannedA2Module2.order,
  title: plannedA2Module2.title,
  level: "A2",
  description: plannedA2Module2.description,
  lessons,
  topicGroups,
  contentRequirements: {
    minSections: 5,
    minCoreSections: 5,
    minStepPractices: 5,
    minTheoryRules: 5,
    minTheoryExamples: 5,
    minKnowledgeChecks: 3,
    minFinalChecks: 2,
    requirePracticeForEverySection: true,
  },
};

export const a2Module2Lessons = a2Module2.lessons;
