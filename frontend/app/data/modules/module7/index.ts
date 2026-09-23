import { getPlannedModule } from "../../a1CourseRoadmap";
import { defineLessonsFromPlannedContent, definePlannedModule } from "../moduleFactory";
import { definePlannedLesson } from "../plannedLessonFactory";
import { pastRegularContent } from "./lessons/past-regular";
import { pastFrequentContent } from "./lessons/past-frequent";
import { yesterdayContent } from "./lessons/yesterday";
import { futureBudemContent } from "./lessons/future-budem";
import { futureQuestionsNegationContent } from "./lessons/future-questions-negation";
import { yesterdayTodayTomorrowContent } from "./lessons/yesterday-today-tomorrow";
import { invitationArrangementContent } from "./lessons/invitation-arrangement";

const plannedModule = getPlannedModule(7);
if (!plannedModule) throw new Error("Module 7 roadmap is missing");

const registeredLessons = defineLessonsFromPlannedContent(
  plannedModule,
  [pastRegularContent, pastFrequentContent, yesterdayContent, futureBudemContent, futureQuestionsNegationContent, yesterdayTodayTomorrowContent, invitationArrangementContent],
  (planned, content, index) => definePlannedLesson(7, index + 1, planned, content),
);

const lessonBySlug = (slug: string) => {
  const lesson = registeredLessons.find((candidate) => candidate.slug === slug);
  if (!lesson) throw new Error(`Module 7 lesson is missing: ${slug}`);
  return lesson;
};

const lessonGroups = [
  {
    id: "past-tense",
    title: "Прошедшее время",
    slovakTitle: "Minulý čas",
    description: "Правильные и частотные глаголы, согласование по роду и завершённые действия.",
    lessons: [lessonBySlug("past-regular"), lessonBySlug("past-frequent")],
  },
  {
    id: "future-and-plans",
    title: "Будущее и планы",
    slovakTitle: "Budúcnosť a plány",
    description: "Budem + infinitív, вопросы о планах, краткие ответы и отрицание.",
    lessons: [lessonBySlug("future-budem"), lessonBySlug("future-questions-negation")],
  },
  {
    id: "three-times",
    title: "Вчера — сегодня — завтра",
    slovakTitle: "Včera — dnes — zajtra",
    description: "Рассказ о вчерашнем дне и переход между прошлым, настоящим и будущим.",
    lessons: [lessonBySlug("yesterday"), lessonBySlug("yesterday-today-tomorrow")],
  },
  {
    id: "invitation-and-arrangement",
    title: "Приглашение и договорённость",
    slovakTitle: "Pozvanie a dohoda",
    description: "Предложить встречу, принять или отклонить предложение и согласовать детали.",
    lessons: [lessonBySlug("invitation-arrangement")],
  },
];

export const module7 = definePlannedModule({ planned: plannedModule, lessonGroups });
export const module7Lessons = module7.lessons;
