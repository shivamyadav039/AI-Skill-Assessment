// API service — all backend calls go here
// In production (Vercel), VITE_API_URL points to the Railway backend.
// In local dev, Vite proxy forwards /api and /health to localhost:8000.
const BACKEND = import.meta.env.VITE_API_URL || '';
const BASE = `${BACKEND}/api/v1`;

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  upload: (payload) =>
    request('/upload', { method: 'POST', body: JSON.stringify(payload) }),

  chat: (payload) =>
    request('/chat', { method: 'POST', body: JSON.stringify(payload) }),

  score: (payload) =>
    request('/score', { method: 'POST', body: JSON.stringify(payload) }),

  plan: (payload) =>
    request('/plan', { method: 'POST', body: JSON.stringify(payload) }),

  gaps: (sessionId) =>
    request(`/gaps/${sessionId}`),

  health: () =>
    fetch(`${BACKEND}/health`).then(r => r.json()),
};
