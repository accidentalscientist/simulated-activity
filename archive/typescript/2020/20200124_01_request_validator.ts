// Archive task: Request Validator
// Generated for 2020-01-24

type RequestBody = { email?: string; amount?: number };

export function validateRequest(body: RequestBody): string[] {
  const errors: string[] = [];
  if (!body.email?.includes("@")) errors.push("email is invalid");
  if (body.amount === undefined || body.amount <= 0) errors.push("amount must be positive");
  return errors;
}
