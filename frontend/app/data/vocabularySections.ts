export const vocabularySections = [
  { id: "basics-communication", title: "Общение и вежливость" },
  { id: "family-people", title: "Семья и люди" },
  { id: "appearance-character", title: "Внешность и характер" },
  { id: "home-household", title: "Дом и быт" },
  { id: "food-drink", title: "Еда и напитки" },
  { id: "shopping-money", title: "Покупки и деньги" },
  { id: "clothing-accessories", title: "Одежда и аксессуары" },
  { id: "body-health", title: "Тело и здоровье" },
  { id: "feelings-emotions", title: "Чувства и эмоции" },
  { id: "education-language", title: "Учёба и язык" },
  { id: "countries-nationalities", title: "Страны и национальности" },
  { id: "work-professions", title: "Работа и профессии" },
  { id: "time-calendar", title: "Время и календарь" },
  { id: "numbers-quantity", title: "Числа и количество" },
  { id: "colors-shapes-materials", title: "Цвета, формы и материалы" },
  { id: "nature-weather", title: "Природа и погода" },
  { id: "animals-plants", title: "Животные и растения" },
  { id: "city-services", title: "Город и услуги" },
  { id: "transport-travel", title: "Транспорт и путешествия" },
  { id: "location-directions", title: "Место и направление" },
  { id: "technology-media", title: "Техника и медиа" },
  { id: "leisure-sport-culture", title: "Досуг, спорт и культура" },
  { id: "actions-movement", title: "Действия и движение" },
  { id: "qualities-states", title: "Качества и состояния" },
  { id: "function-words", title: "Служебные слова" },
] as const;

export type VocabularySectionId = (typeof vocabularySections)[number]["id"];

const titleById = new Map<string, string>(vocabularySections.map((section) => [section.id, section.title]));

export function vocabularySectionTitle(sectionId: string): string {
  return titleById.get(sectionId) ?? "Без раздела";
}
