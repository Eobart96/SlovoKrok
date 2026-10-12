import type { CourseModule } from "../../../courseTypes";
import { plannedA2Module8 } from "../../../a2CourseRoadmap";
import { a2FamilyCharacterLesson } from "./lessons/family-friends-appearance-and-character";
import { a2EmotionsSupportLesson } from "./lessons/emotions-misunderstanding-and-support";
import { a2DoctorConversationLesson } from "./lessons/wellbeing-and-doctor-conversation";
import { a2PharmacyInjuryLesson } from "./lessons/pharmacy-injury-and-first-aid";
import { a2LifestyleSportLesson } from "./lessons/lifestyle-and-sport";
import { a2IntegratedProblemLesson } from "./lessons/integrated-problem-solving";
import { a2ExperienceIndependenceLesson } from "./lessons/a2-experience-plans-and-independence";

const relationshipLessons = [a2FamilyCharacterLesson, a2EmotionsSupportLesson, a2DoctorConversationLesson];
const healthLessons = [a2PharmacyInjuryLesson, a2LifestyleSportLesson];
const reviewLessons = [a2IntegratedProblemLesson, a2ExperienceIndependenceLesson];

export const a2Module8: CourseModule = {
  slug: plannedA2Module8.slug, order: 8, title: plannedA2Module8.title,
  level: "A2", description: plannedA2Module8.description, lessons: [...relationshipLessons, ...healthLessons, ...reviewLessons],
  topicGroups: [
    { id: "a2-m8-relationships-and-wellbeing", title: "Близкие, поддержка и самочувствие", slovakTitle: "Blízki, podpora a zdravotný stav", description: "Портрет близкого человека, обычное недоразумение и учебный разговор с врачом без диагностики или назначения лечения.", lessonSlugs: relationshipLessons.map(({ slug }) => slug) },
    { id: "a2-m8-pharmacy-and-lifestyle", title: "Аптека, травма и образ жизни", slovakTitle: "Lekáreň, úraz a životný štýl", description: "Перевод аптечной этикетки, сообщение о травме и учебный план занятий без назначения лекарств или нагрузок.", lessonSlugs: healthLessons.map(({ slug }) => slug) },
    { id: "a2-m8-integrated-review", title: "Решение проблемы и итог A2", slovakTitle: "Riešenie problému a záverečná práca A2", description: "Цепочка уточнения и договорённости, четыре части самостоятельной учебной работы без обещания официального уровня.", lessonSlugs: reviewLessons.map(({ slug }) => slug) },
  ],
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
