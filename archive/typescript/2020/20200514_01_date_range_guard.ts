// Archive task: Date Range Guard
// Generated for 2020-05-14

export function isWithinRange(value: Date, start: Date, end: Date): boolean {
  return value.getTime() >= start.getTime() && value.getTime() <= end.getTime();
}
