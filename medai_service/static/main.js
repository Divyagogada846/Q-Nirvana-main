// ─── MedAI — Unified JavaScript for all 4 modules ────────────────────────────
// This file is shared across all pages. Each module's JS is in its own section.

// ══════════════════════════════════════════════════════════════════════════════
// SHARED UTILITIES
// ══════════════════════════════════════════════════════════════════════════════

function showLoading(btnEl, text = "Processing...") {
  btnEl.disabled = true;
  btnEl.dataset.original = btnEl.textContent;
  btnEl.textContent = text;
  btnEl.style.opacity = "0.7";
}

function hideLoading(btnEl) {
  btnEl.disabled = false;
  btnEl.textContent = btnEl.dataset.original || "Submit";
  btnEl.style.opacity = "1";
}

function showError(containerId, message) {
  const el = document.getElementById(containerId);
  if (el) {
    el.innerHTML = `<div class="error-box">${message}</div>`;
    el.style.display = "block";
  }
}

function getSeverityColor(level) {
  const map = { low: "#3B6D11", medium: "#854F0B", high: "#A32D2D", critical: "#A32D2D" };
  return map[level] || "#185FA5";
}

function getSeverityBg(level) {
  const map = { low: "#EAF3DE", medium: "#FAEEDA", high: "#FCEBEB", critical: "#FCEBEB" };
  return map[level] || "#E6F1FB";
}

async function apiPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
}


// ══════════════════════════════════════════════════════════════════════════════
// MODULE 1 — SYMPTOM PREDICTOR
// ══════════════════════════════════════════════════════════════════════════════

let selectedSymptoms = [];

function toggleSymptom(btn, symptom) {
  const idx = selectedSymptoms.indexOf(symptom);
  if (idx === -1) {
    selectedSymptoms.push(symptom);
    btn.classList.add("selected");
  } else {
    selectedSymptoms.splice(idx, 1);
    btn.classList.remove("selected");
  }
  document.getElementById("selected-count").textContent = selectedSymptoms.length;
}

async function runPrediction() {
  if (selectedSymptoms.length === 0) {
    alert("Please select at least one symptom.");
    return;
  }
  const btn = document.getElementById("predict-btn");
  showLoading(btn, "Predicting...");

  try {
    const data = await apiPost("/api/predict", { symptoms: selectedSymptoms });
    renderPredictionResult(data);

    // ── Cross-module: Auto-load support info for predicted disease ──
    if (data.status === "success" && data.top_prediction) {
      loadSupportForDisease(data.top_prediction);
    }
  } catch (e) {
    showError("prediction-result", "Error connecting to server. Is Flask running?");
  } finally {
    hideLoading(btn);
  }
}

function renderPredictionResult(data) {
  const el = document.getElementById("prediction-result");
  el.style.display = "block";

  if (data.status !== "success") {
    el.innerHTML = `<div class="error-box">${data.message || "No match found."}</div>`;
    return;
  }

  const sevColor = getSeverityColor(data.severity);
  const sevBg    = getSeverityBg(data.severity);

  let predCards = "";
  (data.all_predictions || []).forEach((p, i) => {
    predCards += `
      <div class="pred-card ${i === 0 ? 'top' : ''}">
        <div class="pred-name">${i === 0 ? "★ " : ""}${p.disease}</div>
        <div class="conf-bar-wrap">
          <div class="conf-bar" style="width:${p.confidence}%;background:${i===0?'#185FA5':'#94a3b8'}"></div>
        </div>
        <div class="conf-label">${p.confidence}% match</div>
      </div>`;
  });

  el.innerHTML = `
    <div class="result-section">
      <div class="result-header">
        <div>
          <h3>${data.top_prediction}</h3>
          <div style="display:flex;gap:8px;margin-top:4px;">
            <span class="badge" style="background:${sevBg};color:${sevColor};">${data.severity} risk</span>
            <span class="badge" style="background:#E6F1FB;color:#0C447C;">${data.confidence}% confidence</span>
          </div>
        </div>
      </div>

      <div class="result-grid">
        <div>
          <p class="section-label">Matched symptoms (${data.matched_symptoms.length})</p>
          <div class="pill-row">${(data.matched_symptoms||[]).map(s=>`<span class="pill">${s.replace('_',' ')}</span>`).join("")}</div>
        </div>
        <div>
          <p class="section-label">Other possibilities</p>
          ${predCards}
        </div>
      </div>

      <p class="section-label" style="margin-top:14px;">Suggested medicines</p>
      <div class="pill-row">${(data.medicines||[]).map(m=>`<span class="pill blue">${m}</span>`).join("")}</div>

      <p class="section-label" style="margin-top:12px;">Precautions</p>
      <ul class="prec-list">${(data.precautions||[]).map(p=>`<li>${p}</li>`).join("")}</ul>

      <div class="cross-module-link">
        <span>Get full support guide for ${data.top_prediction}</span>
        <a href="/support" class="link-btn">Open patient support →</a>
      </div>
    </div>`;
}

function loadSupportForDisease(diseaseName) {
  // Store in sessionStorage so Module 4 page can read it
  sessionStorage.setItem("predicted_disease", diseaseName);
}


// ══════════════════════════════════════════════════════════════════════════════
// MODULE 2 — REPORT ANALYZER
// ══════════════════════════════════════════════════════════════════════════════

async function analyzeReport() {
  const text = document.getElementById("report-text")?.value?.trim();
  const gender = document.getElementById("gender-select")?.value || "male";

  if (!text) {
    alert("Please paste your report text first.");
    return;
  }

  const btn = document.getElementById("analyze-btn");
  showLoading(btn, "Analyzing...");

  try {
    const data = await apiPost("/api/analyze", { text, gender });
    renderReportResult(data);
  } catch (e) {
    showError("report-result", "Error. Is Flask running?");
  } finally {
    hideLoading(btn);
  }
}

function renderReportResult(data) {
  const el = document.getElementById("report-result");
  el.style.display = "block";

  if (data.status === "error") {
    el.innerHTML = `<div class="error-box">${data.message}</div>`;
    return;
  }

  // Summary row
  let html = `
    <div class="summary-row">
      <div class="metric-card"><div class="metric-num">${data.total_parameters}</div><div class="metric-label">Parameters</div></div>
      <div class="metric-card danger"><div class="metric-num">${data.abnormal_count}</div><div class="metric-label">Abnormal</div></div>
      <div class="metric-card ok"><div class="metric-num">${data.normal_count}</div><div class="metric-label">Normal</div></div>
    </div>`;

  // Values table
  html += `<div class="values-table">`;
  (data.results || []).forEach(r => {
    const color = r.status === "normal" ? "#3B6D11" : r.status === "high" ? "#A32D2D" : "#854F0B";
    const bg    = r.status === "normal" ? "#EAF3DE" : "#FCEBEB";
    const pct   = Math.min(Math.round(((r.value - r.normal_min*0.5) / (r.normal_max*1.5 - r.normal_min*0.5)) * 100), 98);
    html += `
      <div class="value-row">
        <div class="value-left">
          <div class="value-name">${r.label}</div>
          <div class="value-bar-wrap">
            <div class="value-bar" style="width:${pct}%;background:${color}"></div>
          </div>
          <div class="value-range">Normal: ${r.normal_min}–${r.normal_max} ${r.unit}</div>
          <div class="plain-eng">${r.plain_english}</div>
        </div>
        <div class="value-right">
          <div class="value-num" style="color:${color}">${r.value}</div>
          <span class="badge" style="background:${bg};color:${color}">${r.status}</span>
        </div>
      </div>`;
  });
  html += `</div>`;

  // Cross-module: if abnormal values found, suggest risk assessment
  if (data.abnormal_count > 0) {
    html += `<div class="cross-module-link">
      <span>${data.abnormal_count} abnormal value(s) detected — check your future disease risk</span>
      <a href="/risk" class="link-btn">Go to risk prediction →</a>
    </div>`;
  }

  el.innerHTML = html;
}


// ══════════════════════════════════════════════════════════════════════════════
// MODULE 3 — RISK PREDICTOR
// ══════════════════════════════════════════════════════════════════════════════

let riskChartInstance = null;

async function runRiskPrediction() {
  const params = {
    sugar:    parseFloat(document.getElementById("r-sugar")?.value    || 100),
    bp:       parseFloat(document.getElementById("r-bp")?.value       || 120),
    chol:     parseFloat(document.getElementById("r-chol")?.value     || 180),
    hgb:      parseFloat(document.getElementById("r-hgb")?.value      || 14),
    creat:    parseFloat(document.getElementById("r-creat")?.value    || 0.9),
    smoke:    parseFloat(document.getElementById("r-smoke")?.value    || 0),
    activity: parseFloat(document.getElementById("r-activity")?.value || 5),
    family:   parseFloat(document.getElementById("r-family")?.value   || 0),
    age:      parseFloat(document.getElementById("r-age")?.value      || 30),
    bmi:      parseFloat(document.getElementById("r-bmi")?.value      || 22),
  };

  const btn = document.getElementById("risk-btn");
  showLoading(btn, "Calculating...");

  try {
    const data = await apiPost("/api/risk", params);
    renderRiskResult(data);
  } catch (e) {
    showError("risk-result", "Error. Is Flask running?");
  } finally {
    hideLoading(btn);
  }
}

function renderRiskResult(data) {
  const el = document.getElementById("risk-result");
  el.style.display = "block";

  const oc = getSeverityColor(data.overall_level);
  const ob = getSeverityBg(data.overall_level);

  let html = `
    <div class="summary-row">
      <div class="metric-card" style="border-top:3px solid ${oc}">
        <div class="metric-num" style="color:${oc}">${data.overall_score}%</div>
        <div class="metric-label">Overall risk</div>
      </div>
      <div class="metric-card danger"><div class="metric-num">${data.high_risk_count}</div><div class="metric-label">High-risk</div></div>
    </div>`;

  Object.entries(data.diseases || {}).forEach(([key, d]) => {
    const dc = getSeverityColor(d.level);
    const db = getSeverityBg(d.level);
    html += `
      <div class="risk-card" style="border-left:4px solid ${dc};background:${db}">
        <div class="risk-card-header">
          <span class="risk-icon" style="background:${dc};color:#fff">${d.icon}</span>
          <div>
            <div class="risk-name">${d.label}</div>
            <div class="risk-pct" style="color:${dc}">${d.score}% — ${d.level}</div>
          </div>
        </div>
        <ul class="prec-list">${(d.tips||[]).map(t=>`<li>${t}</li>`).join("")}</ul>
      </div>`;
  });

  // 5-year chart
  html += `<canvas id="risk-chart" height="240"></canvas>`;

  el.innerHTML = html;

  // Draw Chart.js after DOM update
  setTimeout(() => drawRiskChart(data), 100);
}

function drawRiskChart(data) {
  const ctx = document.getElementById("risk-chart");
  if (!ctx) return;
  if (riskChartInstance) riskChartInstance.destroy();

  const colors = { heart:"#E24B4A", diabetes:"#BA7517", stroke:"#534AB7", kidney:"#1D9E75", anemia:"#7F77DD" };
  const datasets = Object.entries(data.diseases || {}).map(([key, d]) => ({
    label: d.label,
    data: d.projection,
    borderColor: colors[key] || "#888",
    backgroundColor: (colors[key] || "#888") + "15",
    tension: 0.4, fill: true, pointRadius: 3
  }));

  riskChartInstance = new Chart(ctx, {
    type: "line",
    data: { labels: data.timeline_labels || ["Now","1yr","2yr","3yr","4yr","5yr"], datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: "bottom", labels: { font: { size: 11 } } } },
      scales: {
        y: { min:0, max:100, ticks: { callback: v => v+"%" } },
        x: { grid: { display:false } }
      }
    }
  });
}


// ══════════════════════════════════════════════════════════════════════════════
// MODULE 4 — PATIENT SUPPORT CHAT
// ══════════════════════════════════════════════════════════════════════════════

async function sendChatMessage() {
  const input = document.getElementById("chat-input");
  const msg = input?.value?.trim();
  if (!msg) return;

  appendChatMsg("user", msg);
  input.value = "";
  showTypingIndicator();

  // Cross-module: check if Module 1 stored a disease prediction
  const predictedDisease = sessionStorage.getItem("predicted_disease") || "";

  try {
    const data = await apiPost("/api/chat", {
      message: msg,
      disease: predictedDisease
    });
    removeTypingIndicator();
    renderChatResponse(data);
  } catch (e) {
    removeTypingIndicator();
    appendChatMsg("bot", "Error connecting to server. Please ensure Flask is running.");
  }
}

function appendChatMsg(role, text) {
  const wrap = document.getElementById("chat-messages");
  if (!wrap) return;
  const div = document.createElement("div");
  div.className = `chat-msg ${role}`;
  div.innerHTML = `
    <div class="chat-av ${role}">${role === "bot" ? "M+" : "U"}</div>
    <div class="chat-bubble">${text}</div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

function showTypingIndicator() {
  const wrap = document.getElementById("chat-messages");
  if (!wrap) return;
  const div = document.createElement("div");
  div.id = "typing-indicator";
  div.className = "chat-msg bot";
  div.innerHTML = `<div class="chat-av bot">M+</div><div class="chat-bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

function removeTypingIndicator() {
  document.getElementById("typing-indicator")?.remove();
}

function renderChatResponse(data) {
  if (data.type === "general" || data.type === "fallback") {
    appendChatMsg("bot", data.message);
    return;
  }

  if (data.type === "medicines" || data.type === "full") {
    let html = `<strong>${data.message}</strong><br><br>`;

    if (data.medicines) {
      html += `<strong>Medicines:</strong><ul style="margin:6px 0 12px 16px;">`;
      data.medicines.forEach(m => {
        html += `<li><strong>${m.name}</strong> — ${m.dose} <em>(${m.note})</em></li>`;
      });
      html += `</ul>`;
    }

    if (data.precautions) {
      html += `<strong>Precautions:</strong><ul style="margin:6px 0 12px 16px;">`;
      data.precautions.forEach(p => { html += `<li>${p}</li>`; });
      html += `</ul>`;
    }

    if (data.diet) {
      html += `<strong>Diet:</strong><ul style="margin:6px 0 12px 16px;">`;
      data.diet.forEach(d => { html += `<li>${d}</li>`; });
      html += `</ul>`;
    }

    if (data.warning) {
      html += `<div style="background:#FCEBEB;color:#A32D2D;padding:8px 12px;border-radius:8px;margin-top:8px;font-size:13px;">⚠ ${data.warning}</div>`;
    }

    appendChatMsg("bot", html);
    return;
  }

  appendChatMsg("bot", data.message || "I couldn't find information for that query.");
}

function sendQuickQuestion(disease) {
  const input = document.getElementById("chat-input");
  if (input) {
    input.value = `Tell me about medicines and precautions for ${disease}`;
    sendChatMessage();
  }
}

// Auto-trigger if Module 1 passed a disease
document.addEventListener("DOMContentLoaded", () => {
  const predicted = sessionStorage.getItem("predicted_disease");
  if (predicted && document.getElementById("chat-messages")) {
    setTimeout(() => {
      appendChatMsg("bot", `I see you were diagnosed with <strong>${predicted}</strong> by the symptom checker. Would you like medicines and precautions for it?`);
      const chipWrap = document.createElement("div");
      chipWrap.style = "margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;";
      chipWrap.innerHTML = `
        <button onclick="sendQuickQuestion('${predicted}')" class="quick-chip">Yes, show me →</button>
        <button onclick="sessionStorage.removeItem('predicted_disease')" class="quick-chip">No thanks</button>`;
      document.getElementById("chat-messages")?.appendChild(chipWrap);
    }, 500);
  }
});

// Enter key support for chat
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("chat-input")?.addEventListener("keydown", e => {
    if (e.key === "Enter") sendChatMessage();
  });
});
