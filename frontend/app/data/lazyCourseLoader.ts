// Share in-flight/successful imports, but allow retry after a failed chunk download.
export function createLazyCourseLoader<T>(importCourse: () => Promise<T>): () => Promise<T> {
  let pending: Promise<T> | undefined;
  return () => {
    if (!pending) {
      pending = Promise.resolve().then(importCourse).catch((error: unknown) => {
        pending = undefined;
        throw error;
      });
    }
    return pending;
  };
}
