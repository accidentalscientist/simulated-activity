// Archive task: Typed Api Client
// Generated for 2020-01-21

type ApiResponse<T> = { data: T; status: number };

export async function getJson<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return { data: await response.json() as T, status: response.status };
}
