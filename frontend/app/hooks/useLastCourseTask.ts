"use client";

import { useCallback, useEffect, useState } from "react";

export function useLastCourseTask(kind: "exercise" | "reading" | "homework") {
  const key = `slovokrok-last-task-${kind}-v1`;
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
