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

export const a2Module4ReadyLessonSlugs = ["a2-aspect-in-narrative", "a2-aspect-prefix-pairs", "a2-aspect-stem-pairs"];

export const a2ReadyLessonSlugs = [...a2Module1ReadyLessonSlugs, ...a2Module2ReadyLessonSlugs, ...a2Module3ReadyLessonSlugs, ...a2Module4ReadyLessonSlugs];

export const coursePositionCatalog = {
  A1: a1CourseModules,
  A2: [
    { order: 1, lessons: a2Module1ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 2, lessons: a2Module2ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 3, lessons: a2Module3ReadyLessonSlugs.map((slug) => ({ slug })) },
    { order: 4, lessons: a2Module4ReadyLessonSlugs.map((slug) => ({ slug })) },
  ],
};
