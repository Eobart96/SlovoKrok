export function mergeProgress<Value>(
  defaults: Record<string, Value>,
  legacy: Record<string, Value>,
  cached: Record<string, Value> = {},
): Record<string, Value> {
  return { ...defaults, ...legacy, ...cached };
}
