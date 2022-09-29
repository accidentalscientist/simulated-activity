// Archive task: Normalise Payload Helper
// Generated for 2022-09-29

type EventPayload = {
  id: string;
  createdAt: string;
  value: number;
};

export function normalisePayload(payload: EventPayload): EventPayload {
  return {
    id: payload.id.trim().toLowerCase(),
    createdAt: new Date(payload.createdAt).toISOString(),
    value: Number.isFinite(payload.value) ? payload.value : 0,
  };
}
