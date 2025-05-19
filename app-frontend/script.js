const hostname = window.location.hostname;  
let API_BASE_URL;

if (hostname === 'localhost' || hostname === '127.0.0.1') {
  API_BASE_URL = 'http://localhost:8080';
} else {
  API_BASE_URL = `//${window.location.host}/api`;
}

console.log('Using API_BASE_URL:', API_BASE_URL);

async function loadVersions() {
    try {
      const res = await fetch(`${API_BASE_URL}/api/version`);
      console.log('Version API response status:', res.status);
      const data = await res.json();
      document.getElementById('app-version').textContent = data.app_version || 'N/A';
      document.getElementById('model-version').textContent = data.model_version || 'N/A';
    } catch (err) {
      console.error('Error fetching versions:', err);
      document.getElementById('app-version').textContent = 'error';
      document.getElementById('model-version').textContent = 'error';
    }
  }
  
  async function analyzeText() {
    const inputEl = document.getElementById('text-input');
    const text = inputEl.value.trim();
    if (!text) {
      alert('Please enter some text.');
      return;
    }
  
    const resultEl = document.getElementById('result');
    resultEl.textContent = '…';  
  
    try {
      const res = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      console.log('Analyze API response data:', data);
  
      if (res.ok && typeof data.sentiment === 'number') {
        // 1 is positive，0 is negative
        resultEl.textContent = data.sentiment === 1 ? '😊' : '☹️';
      } else {
        console.error('Analyze API error:', data);
        resultEl.textContent = 'Error';
      }
    } catch (err) {
      console.error('Error calling analyze API:', err);
      resultEl.textContent = 'Error';
    }
  }
  
  window.addEventListener('load', () => {
    document.getElementById('analyze-btn').addEventListener('click', analyzeText);
    document.getElementById('text-input').addEventListener('keyup', e => {
      if (e.key === 'Enter') analyzeText();
    });
    loadVersions();
  });  