// const hostname = window.location.hostname;  
// let API_BASE_URL;

// if (hostname === 'localhost' || hostname === '127.0.0.1') {
//   API_BASE_URL = 'http://localhost:8080';
// } else {
//   API_BASE_URL = `//${window.location.host}/api`;
// }

const API_BASE_URL = "";
const APP_VERSION = 'v1';
console.log('Using API_BASE_URL:', API_BASE_URL);
console.log('Using APP_VERSION:', APP_VERSION);

async function loadVersions() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/version`, { headers: { version: APP_VERSION } });
    console.log('Version API response status:', res.status);
    const data = await res.json();
    document.getElementById('app-version').textContent = data.app_version || 'N/A';
    // document.getElementById('model-version').textContent = data.model_version || 'N/A';
  } catch (err) {
    console.error('Error fetching versions:', err);
    document.getElementById('app-version').textContent = 'error';
    // document.getElementById('model-version').textContent = 'error';
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
  const feedbackEl = document.getElementById('feedback');
  const resultLabel = document.getElementById('result-label');
  const feedbacklabel = document.getElementById('feedback-label');
  resultEl.textContent = '…';  
  feedbackEl.style.display = 'none';
  resultLabel.style.display = 'none';
  feedbacklabel.style.display = 'none';

  try {
    const res = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', version: APP_VERSION },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    console.log('Analyze API response data:', data);

    if (res.ok && typeof data.sentiment === 'number') {
      // 1 is positive，0 is negative
      resultEl.textContent = data.sentiment === 1 ? '😊' : '☹️';
      resultLabel.style.display = '';
      feedbackEl.style.display = '';
      feedbacklabel.style.display = '';
      document.getElementById('thumbs-up').onclick = () => sendFeedback(text, data.sentiment, 1);
      document.getElementById('thumbs-down').onclick = () => sendFeedback(text, data.sentiment, 0);
    } else {
      console.error('Analyze API error:', data);
      resultEl.textContent = 'Error';
      feedbackEl.style.display = 'none';
    }
  } catch (err) {
    console.error('Error calling analyze API:', err);
    resultEl.textContent = 'Error';
    feedbackEl.style.display = 'none';
  }
}

async function sendFeedback(text, predicted_sentiment, actual_sentiment) {
  try {
    await fetch(`${API_BASE_URL}/api/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', version: APP_VERSION },
      body: JSON.stringify({
        text,
        predicted_sentiment,
        actual_sentiment
      })
    });
    alert('Thank you for your feedback!');
    document.getElementById('feedback').style.display = 'none';
  } catch (err) {
    alert('Error sending feedback. Please try again later.');
  }
}

async function loadAppServiceVersion() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/app-service-version`, { headers: { version: APP_VERSION } });
    const data = await res.json();
    document.getElementById('app-service-version').textContent =
      data['app-service-version'] || 'N/A';
  } catch (err) {
    console.error('Error fetching app-service version:', err);
    document.getElementById('app-service-version').textContent = 'error';
  }
}
  
window.addEventListener('load', () => {
  document.getElementById('analyze-btn').addEventListener('click', analyzeText);
  document.getElementById('text-input').addEventListener('keyup', e => {
    if (e.key === 'Enter') analyzeText();
  });
  loadVersions();
  loadAppServiceVersion();
});  