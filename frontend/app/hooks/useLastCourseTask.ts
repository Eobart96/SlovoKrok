"use client";

import { useCallback, useEffect, useState } from "react";

export function useLastCourseTask(kind: "exercise" | "reading" | "homework", level: "a1" | "a2" = "a1") {
  const key = level === "a1" ? `slovokrok-last-task-${kind}-v1` : `slovokrok-last-task-a2-${kind}-v1`;
  const [lastId, setLastId] = useState<number | null>(null);
  useEffect(() => {
    try {
      const id = Number(window.localStorage.getItem(key));
      if (Number.isSafeInteger(id) && id > 0) setLastId(id);
    } catch { /* Navigation still works in the current session. */ }
  }, [key]);
  const remember = useCallback((id: number) => {
    setLastId(id);
    try { window.localStorage.setItem(key, String(id)); }
    catch { /* Keep the last task in memory if storage is unavailable. */ }
  }, [key]);
  return { lastId, remember };
}
