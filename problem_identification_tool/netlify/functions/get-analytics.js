exports.handler = async () => {
  try {
    let responses = [];

    // Try Netlify blobs listing (requires appropriate API; fallback used if not available)
    try {
      const store = require('@netlify/blobs');
      const { list, get } = store;
      const items = await list({ prefix: 'responses/' });
      for (const item of items.blobs || []) {
        const res = await get(item.key);
        if (res) responses.push(JSON.parse(await res.text()));
      }
    } catch (_) {
      // Local fallback
      const fs = require('fs');
      const path = require('path');
      const file = path.join(__dirname, '..', '..', 'data', 'server_responses.json');
      if (fs.existsSync(file)) {
        responses = JSON.parse(fs.readFileSync(file, 'utf-8'));
      }
    }

    const analytics = buildAnalytics(responses);
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ count: responses.length, analytics })
    };
  } catch (e) {
    return { statusCode: 500, headers: { 'Access-Control-Allow-Origin': '*' }, body: JSON.stringify({ error: String(e) }) };
  }
};

function buildAnalytics(responses) {
  const categories = {};
  const severities = {};
  for (const r of responses) {
    const cat = r.responses?.q1 || 'unknown';
    categories[cat] = (categories[cat] || 0) + 1;
    const sev = Number(r.responses?.q2 ? 11 - Number(r.responses.q2) : 5);
    severities[sev] = (severities[sev] || 0) + 1;
  }
  return { categories, severities };
}

