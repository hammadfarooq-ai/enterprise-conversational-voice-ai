const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8020";

export async function startCall(payload) {
  const res = await fetch(`${API_BASE}/calls/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Failed to start call");
  return res.json();
}

export async function endCall(payload) {
  const res = await fetch(`${API_BASE}/calls/end`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Failed to end call");
  return res.json();
}
