import { a1CourseModules } from "./a1Course";
import { a2CourseModules } from "./a2/a2Course";
import type { CourseLevel } from "./courseLevelState";

export const courseCatalog = { A1: a1CourseModules, A2: a2CourseModules };
export const allCourseModules = [...a1CourseModules, ...a2CourseModules];
