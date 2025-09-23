// Dashboard logic: load responses, aggregate, and render charts
(function(){
  const $ = (id) => document.getElementById(id);
  const state = { responses: [], problems: [], categories: {}, severities: {} };

  function loadFromLocalStorage(){
    try {
      const raw = localStorage.getItem('questionnaire_responses') || '[]';
      const arr = JSON.parse(raw);
      state.responses = arr;
      deriveProblemsFromResponses(arr);
      render();
    } catch(e){
      alert('Failed to load from localStorage');
      console.error(e);
    }
  }

  function deriveProblemsFromResponses(responses){
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
      const cat = categorize(res.q1, res.q3);
      const sev = severityFromRating(res.q2);

      // build problems from free text fields
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

  function loadFromFile(file){
    const reader = new FileReader();
    reader.onload = () => {
      try{
        const data = JSON.parse(reader.result);
        if (Array.isArray(data)){
          // assume array of responses
          state.responses = data;
          deriveProblemsFromResponses(state.responses);
        } else if (data && data.problems){
          // export format from engine
          state.problems = data.problems || [];
          // rebuild aggregates
          state.categories = {};
          state.severities = {};
          state.problems.forEach(p => {
            state.categories[p.category] = (state.categories[p.category]||0)+1;
            const sev = parseInt(p.severity,10) || 5;
            state.severities[sev] = (state.severities[sev]||0)+1;
          });
        } else {
          throw new Error('Unrecognized JSON structure');
        }
        render();
      } catch(e){
        alert('Invalid JSON file');
        console.error(e);
      }
    };
    reader.readAsText(file);
  }

  let catChart, sevChart;
  function render(){
    // metrics
    $('metricTotal').textContent = String(state.responses.length || 0);
    $('metricProblems').textContent = String(state.problems.length || 0);
    const topCats = Object.entries(state.categories).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([k,v])=>`${k} (${v})`);
    $('metricCategories').textContent = topCats.length ? topCats.join(', ') : '—';

    // charts
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

  function bind(){
    $('loadLocal').addEventListener('click', loadFromLocalStorage);
    $('fileInput').addEventListener('change', (e)=>{
      if (e.target.files && e.target.files[0]) loadFromFile(e.target.files[0]);
    });
    $('clearLocal').addEventListener('click', ()=>{
      localStorage.removeItem('questionnaire_responses');
      state.responses = []; state.problems = []; state.categories = {}; state.severities = {};
      render();
      alert('Local responses cleared');
    });
  }

  document.addEventListener('DOMContentLoaded', ()=>{ bind(); render(); });
})();
