exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers: cors(), body: '' };
  }
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: cors(), body: 'Method Not Allowed' };
  }
  try {
    const payload = JSON.parse(event.body || '{}');
    const record = {
      id: `resp_${Date.now()}_${Math.random().toString(36).slice(2)}`,
      timestamp: new Date().toISOString(),
      ...payload
    };

    // Netlify Blobs (available on Netlify) – if not available, ignore
    try {
      const store = require('@netlify/blobs');
      const { set } = store;
      const key = `responses/${record.id}.json`;
      await set(key, JSON.stringify(record), { contentType: 'application/json' });
      return { statusCode: 200, headers: cors(), body: JSON.stringify({ ok: true }) };
    } catch (_) {}

    // Local fallback (dev): append to data/server_responses.json
    const fs = require('fs');
    const path = require('path');
    const dataDir = path.join(__dirname, '..', '..', 'data');
    const file = path.join(dataDir, 'server_responses.json');
    if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
    let arr = [];
    if (fs.existsSync(file)) {
      try { arr = JSON.parse(fs.readFileSync(file, 'utf-8')); } catch (_) { arr = []; }
    }
    arr.push(record);
    fs.writeFileSync(file, JSON.stringify(arr, null, 2));

    return { statusCode: 200, headers: cors(), body: JSON.stringify({ ok: true }) };
  } catch (e) {
    return { statusCode: 400, headers: cors(), body: JSON.stringify({ ok: false, error: String(e) }) };
  }
};

function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
}

