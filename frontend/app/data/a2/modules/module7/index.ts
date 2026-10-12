import type { CourseModule } from "../../../courseTypes";
import { plannedA2Module7 } from "../../../a2CourseRoadmap";
import { a2ProfessionExperienceLesson } from "./lessons/profession-duties-and-experience";
import { a2VacancyConditionsLesson } from "./lessons/vacancy-form-and-working-conditions";
import { a2WorkPlanLesson } from "./lessons/task-meeting-and-plan-change";
import { a2TicketRouteLesson } from "./lessons/ticket-route-and-transfer";
import { a2BookingPlanLesson } from "./lessons/booking-and-travel-plan";
import { a2TravelStoryLesson } from "./lessons/travel-story";
import { a2GeographyWeatherLesson } from "./lessons/geography-regions-and-weather";
import { a2GuestInformationLesson } from "./lessons/country-information-for-guest";

const workLessons = [a2ProfessionExperienceLesson, a2VacancyConditionsLesson, a2WorkPlanLesson];
const travelLessons = [a2TicketRouteLesson, a2BookingPlanLesson, a2TravelStoryLesson];
const countryLessons = [a2GeographyWeatherLesson, a2GuestInformationLesson];

export const a2Module7: CourseModule = {
  slug: plannedA2Module7.slug, order: 7, title: plannedA2Module7.title,
  level: "A2", description: plannedA2Module7.description, lessons: [...workLessons, ...travelLessons, ...countryLessons],
  topicGroups: [
    { id: "a2-m7-work-and-plans", title: "Работа, условия и договорённости", slovakTitle: "Práca, podmienky a dohody", description: "Профессия и опыт, чтение вакансии, формальный отклик и передача рабочего изменения.", lessonSlugs: workLessons.map(({ slug }) => slug) },
    { id: "a2-m7-travel-and-story", title: "Маршрут, поездка и история", slovakTitle: "Trasa, cesta a príbeh", description: "Билет и пересадка, условия бронирования, общий план и связный рассказ о поездке.", lessonSlugs: travelLessons.map(({ slug }) => slug) },
    { id: "a2-m7-country-and-guest", title: "Страна, погода и информация для гостя", slovakTitle: "Krajina, počasie a informácie pre hosťa", description: "География Словакии, сравнение регионов и передача главного из учебных источников без выдуманных деталей.", lessonSlugs: countryLessons.map(({ slug }) => slug) },
  ],
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
