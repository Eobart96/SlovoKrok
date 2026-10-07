import { findCourseLesson, getCourseModule } from "../courseEngine";
import type { CourseLesson, CourseModule } from "../courseTypes";
import { a2Module2 } from "./modules/module2";

export const a2CourseModules: CourseModule[] = [a2Module2];
export const allA2Lessons = a2CourseModules.flatMap((module) => module.lessons);

export const getA2Module = (order: number): CourseModule => getCourseModule(a2CourseModules, order);
export const findA2Lesson = (slug: string): CourseLesson | undefined => findCourseLesson(a2CourseModules, slug);
