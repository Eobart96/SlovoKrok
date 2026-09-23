import { getPlannedModule } from "../../a1CourseRoadmap";
import { defineLessonsFromPlannedContent, definePlannedModule } from "../moduleFactory";
import { definePlannedLesson } from "../plannedLessonFactory";
import { socialEtiquetteContent } from "./lessons/social-etiquette";
import { supportedDialogueContent } from "./lessons/supported-dialogue";
import { everydayTaskContent } from "./lessons/everyday-task";
import { understandMessageContent } from "./lessons/understand-message";
import { voiceDescriptionContent } from "./lessons/voice-description";
import { writtenProfileContent } from "./lessons/written-profile";
import { simpleMediationContent } from "./lessons/simple-mediation";
import { repairStrategiesContent } from "./lessons/repair-strategies";
import { a1ScenariosContent } from "./lessons/a1-scenarios";

const plannedModule = getPlannedModule(8);
if (!plannedModule) throw new Error("Module 8 roadmap is missing");

const registeredLessons = defineLessonsFromPlannedContent(
  plannedModule,
  [socialEtiquetteContent, supportedDialogueContent, everydayTaskContent, understandMessageContent, voiceDescriptionContent, writtenProfileContent, simpleMediationContent, repairStrategiesContent, a1ScenariosContent],
  (planned, content, index) => definePlannedLesson(8, index + 1, planned, content),
);

const lessonBySlug = (slug: string) => {
  const lesson = registeredLessons.find((candidate) => candidate.slug === slug);
  if (!lesson) throw new Error(`Module 8 lesson is missing: ${slug}`);
  return lesson;
};

const lessonGroups = [
  {
    id: "communication-and-understanding",
    title: "Общение и взаимопонимание",
    slovakTitle: "Komunikácia a porozumenie",
    description: "Этикет ty/vy, поддерживаемый диалог и стратегии при непонимании.",
    lessons: [lessonBySlug("social-etiquette"), lessonBySlug("supported-dialogue"), lessonBySlug("repair-strategies")],
  },
  {
    id: "messages-and-self-presentation",
    title: "Сообщения и самопрезентация",
    slovakTitle: "Správy a predstavenie sa",
    description: "Понимание личного сообщения, устное описание и письменный профиль.",
    lessons: [lessonBySlug("understand-message"), lessonBySlug("voice-description"), lessonBySlug("written-profile")],
  },
  {
    id: "practical-interaction",
    title: "Практическое взаимодействие",
    slovakTitle: "Praktická komunikácia",
    description: "Решение бытовой задачи и точная передача простой информации.",
    lessons: [lessonBySlug("everyday-task"), lessonBySlug("simple-mediation")],
  },
  {
    id: "final-a1-scenarios",
    title: "Итоговые сценарии A1",
    slovakTitle: "Záverečné scenáre A1",
    description: "Комплексная практика основных речевых задач уровня A1.",
    lessons: [lessonBySlug("a1-scenarios")],
  },
];

export const module8 = definePlannedModule({ planned: plannedModule, lessonGroups });
export const module8Lessons = module8.lessons;
