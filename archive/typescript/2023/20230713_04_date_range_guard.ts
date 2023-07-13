// Archive task: Date Range Guard
// Generated for 2023-07-13

export function isWithinRange(value: Date, start: Date, end: Date): boolean {
  return value.getTime() >= start.getTime() && value.getTime() <= end.getTime();
}
