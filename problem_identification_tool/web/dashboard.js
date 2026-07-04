// Dashboard logic: load responses, aggregate, and render charts
(function(){
  const $ = (id) => document.getElementById(id);
  const mergeApi = window.ResponseMerge || {};
  const extractResponsesFromPayload = mergeApi.extractResponsesFromPayload || function(data) {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.responses)) return data.responses;
    return [];
  };
  const mergeResponses = mergeApi.mergeResponses || function(primary, secondary) {
    return (primary || []).concat(secondary || []);
  };

  const IMPORTED_JSON_URL = './data/imports/google_forms_ill_pay_to.json';
  const state = {
    responses: [],
    problems: [],
    categories: {},
    severities: {},
    importedCount: 0,
    localCount: 0,
  };

  function setStatusMessage(message) {
    const el = $('loadStatus');
    if (el) el.textContent = message;
  }

  async function fetchImportedResponses() {
    try {
      const res = await fetch(IMPORTED_JSON_URL, { cache: 'no-store' });
      if (!res.ok) return [];
      const data = await res.json();
      return extractResponsesFromPayload(data);
    } catch (e) {
      console.warn('Imported responses not available:', e);
      return [];
    }
  }

  async function loadMergedFromBrowser() {
    try {
      const raw = localStorage.getItem('questionnaire_responses') || '[]';
      const local = JSON.parse(raw);
      const imported = await fetchImportedResponses();
      state.localCount = local.length;
      state.importedCount = imported.length;
      state.responses = mergeResponses(local, imported);
      deriveProblemsFromResponses(state.responses);
      render();

      if (imported.length) {
        setStatusMessage(
          `Loaded ${state.responses.length} total (${local.length} browser, ${imported.length} imported).`
        );
      } else {
        setStatusMessage(`Loaded ${state.responses.length} from this browser.`);
      }
    } catch (e) {
      alert('Failed to load responses');
      console.error(e);
    }
  }

  function deriveProblemsFromResponses(responses) {
    state.problems = [];
    state.categories = {};
    state.severities = {};

    const categorize = (catRaw, text) => {
      const map = {
        'Work/Career':'workplace','Health & Fitness':'health','Personal Relationships':'relationships',
        'Financial Situation':'finance','Learning & Education':'education','Technology & Digital Life':'technology',
        'Home & Environment':'environment','Personal Development':'personal_development','Business/Entrepreneurship':'business'
      };
      if (map[catRaw]) return map[catRaw];
      const t = (text||'').toLowerCase();
      if (/work|job|career|boss/.test(t)) return 'workplace';
      if (/health|fitness|exercise|medical/.test(t)) return 'health';
      if (/money|financial|budget|debt|income/.test(t)) return 'finance';
      if (/relationship|family|friend|partner/.test(t)) return 'relationships';
      return 'lifestyle';
    };

    const severityFromRating = (ratingStr) => {
      const n = parseInt(ratingStr,10);
      if (!isNaN(n)) return Math.max(1, Math.min(10, 11-n));
      return 5;
    };

    responses.forEach(r => {
      const res = r.responses || {};
      const isIllPayTo = r.questionnaire_id === 'ill_pay_to_v1' || res.q2_problem;

      if (isIllPayTo) {
        const txt = (res.q2_problem || '').trim();
        if (txt.length > 5) {
          const urgency = res.q8_urgency || '';
          let sev = 5;
          if (/extremely urgent/i.test(urgency)) sev = 10;
          else if (/very urgent/i.test(urgency)) sev = 8;
          else if (/moderately urgent/i.test(urgency)) sev = 6;
          else if (/slightly urgent/i.test(urgency)) sev = 4;
          else if (/not urgent/i.test(urgency)) sev = 2;
          state.problems.push({ category: 'business', severity: sev, text: txt });
          state.categories.business = (state.categories.business || 0) + 1;
          state.severities[sev] = (state.severities[sev] || 0) + 1;
        }
        return;
      }

      const cat = categorize(res.q1, res.q3);
      const sev = severityFromRating(res.q2);

      ['q3','q5'].forEach(q => {
        const txt = (res[q]||'').trim();
        if (txt.length > 5){
          state.problems.push({ category: cat, severity: sev, text: txt });
        }
      });

      state.categories[cat] = (state.categories[cat]||0)+1;
      state.severities[sev] = (state.severities[sev]||0)+1;
    });
  }

  function applyPayloadToState(data) {
    if (Array.isArray(data)) {
      state.responses = data;
      deriveProblemsFromResponses(state.responses);
      return;
    }

    const imported = extractResponsesFromPayload(data);
    if (imported.length) {
      state.responses = imported;
      deriveProblemsFromResponses(state.responses);
      return;
    }

    if (data && data.problems) {
      state.problems = data.problems || [];
      state.categories = {};
      state.severities = {};
      state.problems.forEach(p => {
        state.categories[p.category] = (state.categories[p.category]||0)+1;
        const sev = parseInt(p.severity,10) || 5;
        state.severities[sev] = (state.severities[sev]||0)+1;
      });
      return;
    }

    throw new Error('Unrecognized JSON structure');
  }

  function loadFromFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        applyPayloadToState(JSON.parse(reader.result));
        setStatusMessage(`Loaded ${state.responses.length} response(s) from file.`);
        render();
      } catch (e) {
        alert('Invalid JSON file');
        console.error(e);
      }
    };
    reader.readAsText(file);
  }

  let catChart, sevChart;
  function render() {
    $('metricTotal').textContent = String(state.responses.length || 0);
    $('metricProblems').textContent = String(state.problems.length || 0);
    const topCats = Object.entries(state.categories).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([k,v])=>`${k} (${v})`);
    $('metricCategories').textContent = topCats.length ? topCats.join(', ') : '—';

    const catLabels = Object.keys(state.categories);
    const catValues = Object.values(state.categories);
    const sevLabels = Array.from({length:10}, (_,i)=>String(i+1));
    const sevValues = sevLabels.map(l=> state.severities[parseInt(l,10)]||0);

    const catCtx = document.getElementById('catChart').getContext('2d');
    const sevCtx = document.getElementById('sevChart').getContext('2d');

    if (catChart) catChart.destroy();
    if (sevChart) sevChart.destroy();

    catChart = new Chart(catCtx, {
      type: 'bar',
      data: {
        labels: catLabels,
        datasets: [{
          label: 'Problems by Category',
          data: catValues,
          backgroundColor: 'rgba(13, 110, 253, 0.5)',
          borderColor: 'rgba(13, 110, 253, 1)',
          borderWidth: 1
        }]
      },
      options: { scales: { y: { beginAtZero: true } } }
    });

    sevChart = new Chart(sevCtx, {
      type: 'line',
      data: {
        labels: sevLabels,
        datasets: [{
          label: 'Severity Distribution',
          data: sevValues,
          borderColor: 'rgba(13, 110, 253, 1)',
          backgroundColor: 'rgba(13, 110, 253, 0.2)',
          tension: 0.3,
          fill: true
        }]
      },
      options: { scales: { y: { beginAtZero: true } } }
    });
  }

  function bind() {
    $('loadLocal').addEventListener('click', loadMergedFromBrowser);
    $('loadServer').addEventListener('click', async ()=>{
      try {
        const res = await fetch('/.netlify/functions/get-analytics');
        if (!res.ok) throw new Error('Server analytics not available');
        const data = await res.json();
        state.categories = data.analytics?.categories || {};
        state.severities = data.analytics?.severities || {};
        state.responses = [];
        state.problems = [];
        state.importedCount = 0;
        state.localCount = 0;
        setStatusMessage('Loaded aggregate analytics from server.');
        render();
      } catch (e) {
        alert('Could not load from server. Ensure functions are deployed.');
        console.error(e);
      }
    });
    $('fileInput').addEventListener('change', (e)=>{
      if (e.target.files && e.target.files[0]) loadFromFile(e.target.files[0]);
    });
    $('clearLocal').addEventListener('click', ()=>{
      localStorage.removeItem('questionnaire_responses');
      state.responses = [];
      state.problems = [];
      state.categories = {};
      state.severities = {};
      state.importedCount = 0;
      state.localCount = 0;
      render();
      setStatusMessage('Local responses cleared. Imported data still loads on next merge reload.');
      alert('Local responses cleared');
    });
  }

  document.addEventListener('DOMContentLoaded', ()=>{ bind(); render(); });
})();
