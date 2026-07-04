/**
 * Shared response merge helpers (browser + Node smoke tests).
 * Used by dashboard.js to combine localStorage and imported Google Forms data.
 */

function normalizeText(value) {
  return String(value || '').trim().toLowerCase();
}

function responseDedupeKey(response) {
  if (!response || typeof response !== 'object') return '';
  if (response.id) return `id:${response.id}`;

  const res = response.responses || {};
  const email = normalizeText(res.q1_email);
  const problem = normalizeText(res.q2_problem);
  const ts = normalizeText(response.timestamp || response.imported_timestamp);
  if (email || problem || ts) {
    return `legacy:${email}|${problem}|${ts}`;
  }
  return `fallback:${JSON.stringify(response)}`;
}

function extractResponsesFromPayload(data) {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.responses)) return data.responses;
  return [];
}

function mergeResponses(primary, secondary) {
  const merged = [];
  const seen = new Set();

  (primary || []).concat(secondary || []).forEach((item) => {
    const key = responseDedupeKey(item);
    if (seen.has(key)) return;
    seen.add(key);
    merged.push(item);
  });

  return merged;
}

const api = {
  normalizeText,
  responseDedupeKey,
  extractResponsesFromPayload,
  mergeResponses,
};

if (typeof window !== 'undefined') {
  window.ResponseMerge = api;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = api;
}
