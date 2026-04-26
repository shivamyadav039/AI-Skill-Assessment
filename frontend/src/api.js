// API service — all backend calls go here
const BASE = '/api/v1';

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
    fetch('/health').then(r => r.json()),
};
