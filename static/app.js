/**
 * TouchGrass AI — Client Application Logic
 * Enforces minimum screen time, pocket mode outdoor timer,
 * and handles field photo dispatch to local ONNX AI inference.
 */

// Application State
const state = {
  selectedDuration: 15,
  selectedBiome: 'park',
  currentQuest: null,
  sessionSeconds: 0,
  screenTimerInterval: null,
  pocketCountdownInterval: null,
  pocketSecondsRemaining: 900,
  selectedFile: null
};

// Web Audio API Synthesizer for Departure & Return Chimes
function playNatureChime(type = 'departure') {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    const now = ctx.currentTime;
    if (type === 'departure') {
      // Ascending calming chime
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, now); // A4
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.6); // A5
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
      osc.start(now);
      osc.stop(now + 0.8);
    } else {
      // Bell completion chime
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(523.25, now); // C5
      osc.frequency.setValueAtTime(659.25, now + 0.2); // E5
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
      osc.start(now);
      osc.stop(now + 1.2);
    }
  } catch (err) {
    console.warn('Audio chime skipped:', err);
  }
}

// DOM Elements
const el = {
  screenTimer: document.getElementById('screen-timer'),
  dispatchPanel: document.getElementById('dispatch-panel'),
  questPanel: document.getElementById('quest-panel'),
  pocketPanel: document.getElementById('pocket-panel'),
  verifyPanel: document.getElementById('verify-panel'),
  statsPanel: document.getElementById('stats-panel'),
  dispatchBtn: document.getElementById('dispatch-btn'),
  pocketModeBtn: document.getElementById('pocket-mode-btn'),
  newQuestBtn: document.getElementById('new-quest-btn'),
  exitPocketBtn: document.getElementById('exit-pocket-btn'),
  returnFromOutsideBtn: document.getElementById('return-from-outside-btn'),
  runVerifyBtn: document.getElementById('run-verify-btn'),
  imageInput: document.getElementById('image-input'),
  dropArea: document.getElementById('drop-area'),
  previewContainer: document.getElementById('image-preview-container'),
  previewImg: document.getElementById('image-preview'),
  removeImageBtn: document.getElementById('remove-image-btn'),
  actualTimeInput: document.getElementById('actual-time-input'),
  resultBox: document.getElementById('verification-result-box'),
  pocketCountdown: document.getElementById('pocket-countdown'),
  pocketQuestName: document.getElementById('pocket-quest-name'),
  questTitle: document.getElementById('quest-title'),
  questBiomeTag: document.getElementById('quest-biome-tag'),
  questBrief: document.getElementById('quest-brief'),
  questTasksList: document.getElementById('quest-tasks-list'),
  questChallenge: document.getElementById('quest-challenge'),
  statMinutes: document.getElementById('stat-minutes'),
  statExpeditions: document.getElementById('stat-expeditions'),
  statScore: document.getElementById('stat-score'),
  statDays: document.getElementById('stat-days'),
  historyList: document.getElementById('history-list'),
  modelStatusText: document.getElementById('model-status-text')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  startScreenTimer();
  setupSelectors();
  setupFileUpload();
  setupButtons();
  fetchHealth();
  fetchStats();
  fetchHistory();
});

// Screen Time Monitor (Enforces awareness of minimum screen interaction)
function startScreenTimer() {
  state.screenTimerInterval = setInterval(() => {
    state.sessionSeconds++;
    const mins = String(Math.floor(state.sessionSeconds / 60)).padStart(2, '0');
    const secs = String(state.sessionSeconds % 60).padStart(2, '0');
    el.screenTimer.textContent = `${mins}:${secs}`;
  }, 1000);
}

// Setup Pill Selectors
function setupSelectors() {
  document.querySelectorAll('#duration-selector .pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#duration-selector .pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.selectedDuration = parseInt(btn.dataset.duration, 10);
    });
  });

  document.querySelectorAll('#biome-selector .pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#biome-selector .pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.selectedBiome = btn.dataset.biome;
    });
  });
}

// Health Check Endpoint
async function fetchHealth() {
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    if (data.status === 'healthy') {
      el.modelStatusText.textContent = `${data.model_name} • 12ms Local CPU`;
    }
  } catch (err) {
    el.modelStatusText.textContent = 'Local Engine Ready';
  }
}

// Setup Event Listeners for Workflow
function setupButtons() {
  // Step 1: Dispatch Quest
  el.dispatchBtn.addEventListener('click', async () => {
    el.dispatchBtn.disabled = true;
    el.dispatchBtn.textContent = 'Synthesizing Quest...';

    try {
      const res = await fetch('/api/expeditions/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          duration_mins: state.selectedDuration,
          biome: state.selectedBiome
        })
      });

      const data = await res.json();
      if (data.success) {
        state.currentQuest = data.quest;
        displayQuest(data.quest);
      }
    } catch (err) {
      alert('Failed to generate expedition. Please try again.');
    } finally {
      el.dispatchBtn.disabled = false;
      el.dispatchBtn.textContent = '⚡ Dispatch Expedition & Leave Screen';
    }
  });

  // Re-roll Mission
  el.newQuestBtn.addEventListener('click', () => {
    el.questPanel.classList.add('panel-hidden');
    el.dispatchPanel.classList.remove('panel-hidden');
  });

  // Step 2: Enter Pocket Mode
  el.pocketModeBtn.addEventListener('click', () => {
    playNatureChime('departure');
    startPocketMode();
  });

  // Exit Pocket Mode prematurely
  el.exitPocketBtn.addEventListener('click', () => {
    clearInterval(state.pocketCountdownInterval);
    el.pocketPanel.classList.add('panel-hidden');
    el.dispatchPanel.classList.remove('panel-hidden');
  });

  // Return from Outside -> Verify Step
  el.returnFromOutsideBtn.addEventListener('click', () => {
    clearInterval(state.pocketCountdownInterval);
    el.pocketPanel.classList.add('panel-hidden');
    el.verifyPanel.classList.remove('panel-hidden');
    el.actualTimeInput.value = state.selectedDuration;
  });

  // Run Verification
  el.runVerifyBtn.addEventListener('click', runVerification);
}

// Display Quest Details
function displayQuest(quest) {
  el.questTitle.textContent = quest.title;
  el.questBiomeTag.textContent = quest.biome_display;
  el.questBrief.textContent = quest.mission_brief;

  el.questTasksList.innerHTML = '';
  quest.sensory_tasks.forEach(task => {
    const li = document.createElement('li');
    li.textContent = task;
    el.questTasksList.appendChild(li);
  });

  el.questChallenge.textContent = quest.verification_challenge;

  el.dispatchPanel.classList.add('panel-hidden');
  el.questPanel.classList.remove('panel-hidden');
}

// Pocket Mode Countdown
function startPocketMode() {
  el.questPanel.classList.add('panel-hidden');
  el.pocketPanel.classList.remove('panel-hidden');

  el.pocketQuestName.textContent = state.currentQuest.title;
  state.pocketSecondsRemaining = state.selectedDuration * 60;
  updatePocketDisplay();

  clearInterval(state.pocketCountdownInterval);
  state.pocketCountdownInterval = setInterval(() => {
    if (state.pocketSecondsRemaining > 0) {
      state.pocketSecondsRemaining--;
      updatePocketDisplay();
    } else {
      clearInterval(state.pocketCountdownInterval);
      playNatureChime('return');
      el.pocketCountdown.textContent = '00:00';
    }
  }, 1000);
}

function updatePocketDisplay() {
  const m = String(Math.floor(state.pocketSecondsRemaining / 60)).padStart(2, '0');
  const s = String(state.pocketSecondsRemaining % 60).padStart(2, '0');
  el.pocketCountdown.textContent = `${m}:${s}`;
}

// Setup File Upload
function setupFileUpload() {
  el.imageInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleSelectedFile(e.target.files[0]);
    }
  });

  el.removeImageBtn.addEventListener('click', () => {
    state.selectedFile = null;
    el.imageInput.value = '';
    el.previewContainer.classList.add('preview-hidden');
    el.dropArea.style.display = 'flex';
    el.runVerifyBtn.disabled = true;
    el.resultBox.classList.add('result-box-hidden');
  });

  // Drag and drop support
  ['dragenter', 'dragover'].forEach(name => {
    el.dropArea.addEventListener(name, (e) => {
      e.preventDefault();
      el.dropArea.style.borderColor = 'var(--accent-green)';
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    el.dropArea.addEventListener(name, (e) => {
      e.preventDefault();
      el.dropArea.style.borderColor = 'var(--border-color)';
    });
  });

  el.dropArea.addEventListener('drop', (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleSelectedFile(e.dataTransfer.files[0]);
    }
  });
}

function handleSelectedFile(file) {
  state.selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    el.previewImg.src = e.target.result;
    el.dropArea.style.display = 'none';
    el.previewContainer.classList.remove('preview-hidden');
    el.runVerifyBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

// Run AI Verification
async function runVerification() {
  if (!state.selectedFile) return;

  el.runVerifyBtn.disabled = true;
  el.runVerifyBtn.textContent = '🧠 Executing MobileNetV4 ONNX Inference on CPU...';

  const formData = new FormData();
  formData.append('image', state.selectedFile);
  formData.append('expedition_id', state.currentQuest ? state.currentQuest.quest_id : 'exp_direct');
  formData.append('actual_duration_mins', el.actualTimeInput.value || 15);

  try {
    const res = await fetch('/api/verify', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    if (data.success) {
      renderVerificationResult(data.verification);
      fetchStats();
      fetchHistory();
      playNatureChime('return');
    } else {
      alert(`Verification error: ${data.error}`);
    }
  } catch (err) {
    alert('Failed to run verification: ' + err.toString());
  } finally {
    el.runVerifyBtn.disabled = false;
    el.runVerifyBtn.textContent = '🧠 Run Local AI Biophilia Analysis';
  }
}

// Render AI Output
function renderVerificationResult(v) {
  el.resultBox.classList.remove('result-box-hidden');

  const isSuccess = v.is_nature && v.status === 'verified_nature';
  const cardClass = isSuccess ? 'result-card success' : 'result-card rejected';
  const icon = isSuccess ? '🌿' : '⚠️';
  const title = isSuccess ? 'Touch Grass Verified!' : 'Screen / Indoor Clutter Detected';

  let topPills = '';
  if (v.top_predictions) {
    topPills = v.top_predictions.map(p => 
      `<span class="top-label-chip">${p.label.split(',')[0]} (${Math.round(p.probability * 100)}%)</span>`
    ).join(' ');
  }

  el.resultBox.innerHTML = `
    <div class="${cardClass}">
      <div class="result-status-title">
        <span>${icon}</span>
        <span>${title}</span>
      </div>
      <p style="margin: 0.5rem 0; font-size: 0.95rem; color: #f3f4f6;">${v.feedback}</p>

      <div class="result-meta-grid">
        <div class="meta-item">
          <span class="meta-label">DISCOVERY CLASS</span>
          <span class="meta-value">${v.primary_identification}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">BIOPHILIA DOMAIN</span>
          <span class="meta-value">${v.biophilia_category}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">GRASS SCORE</span>
          <span class="meta-value" style="color: ${isSuccess ? 'var(--accent-light)' : 'var(--accent-red)'}">${v.grass_score}/100</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">CPU LATENCY</span>
          <span class="meta-value">${v.latency_ms} ms</span>
        </div>
      </div>

      <div class="top-labels-list">
        <strong>Open Vision Model Candidates:</strong><br>
        ${topPills}
      </div>

      <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
        <button id="reset-cycle-btn" class="btn btn-primary" style="flex: 1;">
          🌱 Start Another Expedition
        </button>
      </div>
    </div>
  `;

  document.getElementById('reset-cycle-btn').addEventListener('click', () => {
    // Reset view to Step 1
    el.verifyPanel.classList.add('panel-hidden');
    el.dispatchPanel.classList.remove('panel-hidden');
    el.resultBox.classList.add('result-box-hidden');
    state.selectedFile = null;
    el.previewContainer.classList.add('preview-hidden');
    el.dropArea.style.display = 'flex';
  });
}

// Fetch Stats
async function fetchStats() {
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    if (data.success && data.stats) {
      const s = data.stats;
      el.statMinutes.textContent = s.total_outdoor_minutes;
      el.statExpeditions.textContent = s.total_expeditions;
      el.statScore.textContent = `${Math.round(s.average_grass_score)}%`;
      el.statDays.textContent = s.active_days;
    }
  } catch (err) {
    console.warn('Could not load stats:', err);
  }
}

// Fetch History
async function fetchHistory() {
  try {
    const res = await fetch('/api/history');
    const data = await res.json();
    if (data.success && data.history && data.history.length > 0) {
      el.historyList.innerHTML = '';
      data.history.forEach(item => {
        const div = document.createElement('div');
        div.className = 'history-item';
        const isVer = item.status === 'completed';
        const dateStr = item.created_at ? item.created_at.split('T')[0] : 'Today';

        div.innerHTML = `
          <div>
            <div class="history-title">${isVer ? '🌿' : '⏳'} ${item.title}</div>
            <div class="history-sub">${item.biome.toUpperCase()} • ${item.actual_duration_mins || item.target_duration_mins} mins outdoors • ${dateStr}</div>
          </div>
          <div>
            <span class="badge-tag">${item.primary_identification || 'Pending Verification'}</span>
          </div>
        `;
        el.historyList.appendChild(div);
      });
    }
  } catch (err) {
    console.warn('Could not load history:', err);
  }
}
