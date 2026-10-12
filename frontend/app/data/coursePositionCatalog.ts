import { a1CourseModules } from "./a1Course";

// Only ready topic identifiers, never lesson text. Keep in sync with the A2 catalog.
export const a2Module1ReadyLessonSlugs = [
  "a2-readiness-for-a2",
  "a2-verb-aspect",
  "a2-clitics-word-order",
  "a2-word-families",
  "a2-case-map-government",
  "a2-coherence-focus",
  "a2-connected-pronunciation",
];

export const a2Module2ReadyLessonSlugs = [
  "a2-nominative-plural-things",
  "a2-nominative-plural-people",
  "a2-accusative-singular-agreement",
  "a2-accusative-plural",
  "a2-genitive-singular",
  "a2-genitive-quantity",
  "a2-genitive-plural",
  "a2-dative-recipient-benefit-cause",
  "a2-locative-place-topic",
  "a2-instrumental-means-company-role",
  "a2-case-triads",
  "a2-case-system-government-address",
];

export const a2Module3ReadyLessonSlugs = [
  "a2-adjective-case-agreement",
  "a2-adjectives-plural",
  "a2-adjective-comparison",
  "a2-adverb-comparison",
  "a2-personal-pronoun-cases",
  "a2-possessives-svoj",
  "a2-possessive-adjectives",
  "a2-indefinite-negative-pronouns",
  "a2-numerals-dates-quantity",
];

export const a2Module4ReadyLessonSlugs = ["a2-aspect-in-narrative", "a2-aspect-prefix-pairs", "a2-aspect-stem-pairs", "a2-aspect-present-past", "a2-imperfective-future", "a2-perfective-future", "a2-motion-verbs", "a2-reflexive-sa-si", "a2-imperative-requests", "a2-conditional-by", "a2-conditional-modals", "a2-verbal-nouns-participles"];

export const a2Module5ReadyLessonSlugs = ["a2-conjunctions-a-ale-alebo", "a2-paired-conjunctions", "a2-reported-statements-ze", "a2-relative-clauses-ktory", "a2-embedded-questions", "a2-cause-and-consequence", "a2-time-and-real-condition", "a2-connected-story-focus"];

export const a2Module6ReadyLessonSlugs = ["a2-housing-and-neighbourhood", "a2-rental-ad-and-search", "a2-household-problem-and-agreement", "a2-devices-files-and-apps", "a2-calls-messages-and-email", "a2-social-networks-and-digital-safety", "a2-quantity-packaging-and-product-info", "a2-clothes-fitting-payment-and-exchange", "a2-online-order-delivery-and-return"];

export const a2Module7ReadyLessonSlugs = ["a2-profession-duties-and-experience", "a2-vacancy-form-and-working-conditions", "a2-task-meeting-and-plan-change", "a2-ticket-route-and-transfer", "a2-booking-and-travel-plan", "a2-travel-story", "a2-geography-regions-and-weather", "a2-country-information-for-guest"];

export const a2Module8ReadyLessonSlugs = ["a2-family-friends-appearance-and-character", "a2-emotions-misunderstanding-and-support", "a2-wellbeing-and-doctor-conversation", "a2-pharmacy-injury-and-first-aid", "a2-lifestyle-and-sport", "a2-integrated-problem-solving", "a2-experience-plans-and-independence"];

export const a2ReadyLessonSlugs = [...a2Module1ReadyLessonSlugs, ...a2Module2ReadyLessonSlugs, ...a2Module3ReadyLessonSlugs, ...a2Module4ReadyLessonSlugs, ...a2Module5ReadyLessonSlugs, ...a2Module6ReadyLessonSlugs, ...a2Module7ReadyLessonSlugs, ...a2Module8ReadyLessonSlugs];

export const coursePositionCatalog = {
  A1: a1CourseModules,
  A2: [
    { order: 1, lessons: a2Module1ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 2, lessons: a2Module2ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 3, lessons: a2Module3ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 4, lessons: a2Module4ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 5, lessons: a2Module5ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 6, lessons: a2Module6ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 7, lessons: a2Module7ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 8, lessons: a2Module8ReadyLessonSlugs.map((slug) => ({ slug })) },
  ],
};
