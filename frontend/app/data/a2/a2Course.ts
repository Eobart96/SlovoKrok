import { findCourseLesson, getCourseModule } from "../courseEngine";
import type { CourseLesson, CourseModule } from "../courseTypes";
import { a2Module2 } from "./modules/module2";
import { a2Module3 } from "./modules/module3";
import { a2Module4 } from "./modules/module4";
import { a2Module1 } from "./modules/module1";

export const a2CourseModules: CourseModule[] = [a2Module1, a2Module2, a2Module3, a2Module4];
export const allA2Lessons = a2CourseModules.flatMap((module) => module.lessons);

export const getA2Module = (order: number): CourseModule => getCourseModule(a2CourseModules, order);
export const findA2Lesson = (slug: string): CourseLesson | undefined => findCourseLesson(a2CourseModules, slug);
