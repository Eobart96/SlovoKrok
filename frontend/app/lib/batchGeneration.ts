export type BatchGenerationProgress = {
  attempted: number;
  created: number;
  failed: number;
};

export type BatchGenerationResult<T> = BatchGenerationProgress & {
  items: T[];
  lastError: unknown;
  stoppedEarly: boolean;
};

export async function generateSequentialBatch<T>({
  count,
  create,
  onProgress,
  maxConsecutiveFailures = 3,
}: {
  count: number;
  create: (index: number, createdItems: readonly T[]) => Promise<T>;
  onProgress?: (progress: BatchGenerationProgress) => void;
  maxConsecutiveFailures?: number;
}): Promise<BatchGenerationResult<T>> {
  const requestedCount = Math.max(0, Math.trunc(count));
  const items: T[] = [];
  let attempted = 0;
  let failed = 0;
  let consecutiveFailures = 0;
  let lastError: unknown = null;

  for (let index = 0; index < requestedCount; index += 1) {
    attempted += 1;
    try {
      items.push(await create(index, items));
      consecutiveFailures = 0;
    } catch (error) {
      failed += 1;
      consecutiveFailures += 1;
      lastError = error;
    }
    onProgress?.({ attempted, created: items.length, failed });
    if (consecutiveFailures >= maxConsecutiveFailures) break;
  }

  return {
    items,
    attempted,
    created: items.length,
    failed,
    lastError,
    stoppedEarly: attempted < requestedCount,
  };
}
