import { findCourseLesson, getCourseModule } from "../courseEngine";
import type { CourseLesson, CourseModule } from "../courseTypes";
import { a2Module2 } from "./modules/module2";
import { a2Module3 } from "./modules/module3";
import { a2Module4 } from "./modules/module4";
import { a2Module1 } from "./modules/module1";
import { a2Module5 } from "./modules/module5";
import { a2Module6 } from "./modules/module6";
import { a2Module7 } from "./modules/module7";
import { a2Module8 } from "./modules/module8";

export const a2CourseModules: CourseModule[] = [a2Module1, a2Module2, a2Module3, a2Module4, a2Module5, a2Module6, a2Module7, a2Module8];
export const allA2Lessons = a2CourseModules.flatMap((module) => module.lessons);

export const getA2Module = (order: number): CourseModule => getCourseModule(a2CourseModules, order);
export const findA2Lesson = (slug: string): CourseLesson | undefined => findCourseLesson(a2CourseModules, slug);
