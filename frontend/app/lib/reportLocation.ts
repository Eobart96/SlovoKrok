import type { IssueReportSection } from "./api";

export type ReportLocation = { view?: string; module?: string; lesson?: string; step?: number; task_type?: string; task_id?: string; task_title?: string; scope?: string; training_stage?: string };
export function captureReportLocation(section: IssueReportSection): ReportLocation {
  const course = document.querySelector<HTMLElement>(".course[data-report-view]");
  const location: ReportLocation = { view: course?.dataset.reportView ?? section };
  if (section === "learning") {
    location.module = course?.dataset.reportModule;
    location.lesson = course?.dataset.reportLesson;
    const step = Number(course?.dataset.reportStep);
    if (Number.isInteger(step) && step > 0) location.step = step;
  }
  const task = Array.from(document.querySelectorAll<HTMLElement>("[data-report-task-type]")).find((item) => !item.closest("[hidden]") && item.dataset.reportTaskId);
  if (task) {
    location.task_type = task.dataset.reportTaskType;
    location.task_id = task.dataset.reportTaskId;
    location.task_title = task.dataset.reportTaskTitle?.slice(0, 500);
    location.scope = task.dataset.reportScope?.slice(0, 255);
    location.training_stage = task.dataset.reportStage;
  }
  return location;
}
export function describeReportLocation(location?: ReportLocation | null): string {
  if (!location) return "";
  return [location.view && `Экран: ${location.view}`, location.module && `Модуль: ${location.module}`, location.lesson && `Тема: ${location.lesson}`, location.step && `Шаг: ${location.step}`, location.task_type && `Тип: ${location.task_type}`, location.task_id && `ID: ${location.task_id}`, location.task_title && `Задание: ${location.task_title}`, location.scope && `Область: ${location.scope}`, location.training_stage && `Этап тренировки: ${location.training_stage}`].filter(Boolean).join("\n");
}
