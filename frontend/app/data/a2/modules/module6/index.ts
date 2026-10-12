import type { CourseModule } from "../../../courseTypes";
import { plannedA2Module6 } from "../../../a2CourseRoadmap";
import { a2HousingNeighbourhoodLesson } from "./lessons/housing-and-neighbourhood";
import { a2RentalSearchLesson } from "./lessons/rental-ad-and-search";
import { a2HouseholdProblemLesson } from "./lessons/household-problem-and-agreement";
import { a2DevicesFilesLesson } from "./lessons/devices-files-and-apps";
import { a2CallsMessagesLesson } from "./lessons/calls-messages-and-email";
import { a2SocialDigitalSafetyLesson } from "./lessons/social-networks-and-digital-safety";
import { a2QuantityPackagingLesson } from "./lessons/quantity-packaging-and-product-info";
import { a2ClothesFittingLesson } from "./lessons/clothes-fitting-payment-and-exchange";
import { a2OnlineOrderLesson } from "./lessons/online-order-delivery-and-return";

const housingLessons = [a2HousingNeighbourhoodLesson, a2RentalSearchLesson, a2HouseholdProblemLesson];
const onlineLessons = [a2DevicesFilesLesson, a2CallsMessagesLesson, a2SocialDigitalSafetyLesson];
const shoppingLessons = [a2QuantityPackagingLesson, a2ClothesFittingLesson, a2OnlineOrderLesson];
const lessons = [...housingLessons, ...onlineLessons, ...shoppingLessons];

export const a2Module6: CourseModule = {
  slug: plannedA2Module6.slug, order: 6, title: plannedA2Module6.title,
  level: "A2", description: plannedA2Module6.description, lessons,
  topicGroups: [
    { id: "a2-m6-housing-and-agreements", title: "Жильё, район и договорённости", slovakTitle: "Bývanie, okolie a dohody", description: "Описание жилья, чтение объявления, сообщение владельцу и согласование решения.", lessonSlugs: housingLessons.map(({ slug }) => slug) },
    { id: "a2-m6-online-life", title: "Устройства, общение и безопасность", slovakTitle: "Zariadenia, komunikácia a bezpečnosť", description: "Цифровая инструкция, адресат сообщения, письмо и безопасная помощь со входом.", lessonSlugs: onlineLessons.map(({ slug }) => slug) },
    { id: "a2-m6-shopping-and-delivery", title: "Товары, покупки и доставка", slovakTitle: "Výrobky, nákupy a doručenie", description: "Количество и этикетка, примерка и обмен, статус заказа и точная передача условий.", lessonSlugs: shoppingLessons.map(({ slug }) => slug) },
  ],
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
