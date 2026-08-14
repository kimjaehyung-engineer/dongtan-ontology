import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Toolbar HTML inside modal-body if not already present
toolbar_html = """
      <!-- 실시간 교차로 차량 & 트램 흐름 시뮬레이션 제어 툴바 -->
      <div class="sim-toolbar" style="display: flex; align-items: center; justify-content: space-between; background: #f1f5f9; padding: 0.6rem 1rem; border-radius: 10px; border: 1px solid #cbd5e1; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.8rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
          <button id="btn-sim-toggle" onclick="toggleSimPlay()" style="background: #2563eb; color: #ffffff; border: none; padding: 0.45rem 0.9rem; border-radius: 6px; font-size: 0.82rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 0.35rem; box-shadow: 0 2px 4px rgba(37,99,235,0.25);">
            <span id="sim-play-icon">⏸️</span> <span id="sim-play-text">시뮬레이션 일시정지</span>
          </button>
          <button id="btn-sim-tram" onclick="triggerTramPriority()" style="background: #059669; color: #ffffff; border: none; padding: 0.45rem 0.9rem; border-radius: 6px; font-size: 0.82rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 0.35rem; box-shadow: 0 2px 4px rgba(5,150,105,0.25);">
            <span>🚊</span> 트램 우선신호 요청 (PPC)
          </button>
        </div>
        <div style="display: flex; align-items: center; gap: 0.8rem; font-size: 0.8rem; font-weight: 600; color: #334155;">
          <div style="display: flex; align-items: center; gap: 0.4rem;">
            <span>교통량:</span>
            <select id="sim-density-select" onchange="changeTrafficDensity(this.value)" style="padding: 0.25rem 0.5rem; border-radius: 6px; border: 1px solid #cbd5e1; font-weight: 700; background: #ffffff; color: #0f172a; cursor: pointer;">
              <option value="LOW">원활 (Low)</option>
              <option value="MEDIUM" selected>서행 (Medium)</option>
              <option value="HEAVY">혼잡 (Heavy)</option>
            </select>
          </div>
          <div id="sim-signal-status" style="background: #dcfce7; color: #15803d; padding: 0.25rem 0.75rem; border-radius: 50px; font-weight: 800; border: 1px solid #86efac; display: flex; align-items: center; gap: 0.4rem;">
            <span id="sim-signal-dot" style="width: 9px; height: 9px; border-radius: 50%; background: #22c55e; display: inline-block; box-shadow: 0 0 6px #22c55e;"></span>
            <span id="sim-signal-text">동서 직진 (녹색)</span>
          </div>
        </div>
      </div>
"""

if '<div class="sim-toolbar"' not in content:
    content = content.replace('<div class="diagram-wrapper">', toolbar_html + '\n      <div class="diagram-wrapper">')
    print("Added sim-toolbar HTML to modal-body!")

# 2. Comprehensive Traffic & Tram Simulation JS Logic
full_sim_js = """
// ============================================================================
// 🚦 실시간 교차로 차량 & 트램 흐름(Traffic Flow) 애니메이션 시뮬레이션 엔진
// ============================================================================
let simAnimFrameId = null;
let simRunning = false;
let simTime = 0;
let signalPhase = 'EW_GREEN'; // EW_GREEN, EW_YELLOW, NS_GREEN, NS_YELLOW, TRAM_PRIORITY
let signalTimer = 0;
let trafficDensity = 'MEDIUM'; // LOW, MEDIUM, HEAVY
let ppcRequested = false;

let simVehicles = [];
let simTram = null;

// Signal Timings (frames at ~60fps)
const SIGNAL_TIMINGS = {
  EW_GREEN: 300,   // ~5 sec
  EW_YELLOW: 90,   // ~1.5 sec
  NS_GREEN: 240,   // ~4 sec
  NS_YELLOW: 90,   // ~1.5 sec
  TRAM_PRIORITY: 360 // ~6 sec
};

function toggleSimPlay() {
  simRunning = !simRunning;
  const iconEl = document.getElementById("sim-play-icon");
  const textEl = document.getElementById("sim-play-text");
  const btnEl = document.getElementById("btn-sim-toggle");

  if (simRunning) {
    if (iconEl) iconEl.textContent = "⏸️";
    if (textEl) textEl.textContent = "시뮬레이션 일시정지";
    if (btnEl) btnEl.style.background = "#2563eb";
    runTrafficAnimLoop();
  } else {
    if (iconEl) iconEl.textContent = "▶️";
    if (textEl) textEl.textContent = "시뮬레이션 시작";
    if (btnEl) btnEl.style.background = "#059669";
    if (simAnimFrameId) cancelAnimationFrame(simAnimFrameId);
  }
}

function changeTrafficDensity(val) {
  trafficDensity = val;
}

function triggerTramPriority() {
  ppcRequested = true;
  if (!simTram || simTram.x > 750 || simTram.x < -100) {
    spawnTram();
  }
}

function spawnTram() {
  simTram = {
    id: 'tram_main',
    type: 'TRAM',
    dir: 'EB', // Eastbound along center track y=180
    x: -120,
    y: 180,
    speed: 2.2,
    targetSpeed: 2.2,
    length: 90,
    width: 22,
    state: 'APPROACHING'
  };
}

function spawnRandomVehicle() {
  const densityFreq = trafficDensity === 'LOW' ? 0.015 : (trafficDensity === 'MEDIUM' ? 0.035 : 0.065);
  if (Math.random() > densityFreq) return;

  const dirs = ['EB_L1', 'EB_L2', 'WB_L1', 'WB_L2', 'SB_L1', 'SB_L2', 'NB_L1', 'NB_L2'];
  const dir = dirs[Math.floor(Math.random() * dirs.length)];

  // Check lane crowding
  const tooClose = simVehicles.some(v => {
    if (v.dir !== dir) return false;
    if (dir.startswith('EB') && v.x < 80) return true;
    if (dir.startswith('WB') && v.x > 720) return true;
    if (dir.startswith('SB') && v.y < 60) return true;
    if (dir.startswith('NB') && v.y > 320) return true;
    return false;
  });
  if (tooClose) return;

  const types = ['CAR', 'CAR', 'CAR', 'BUS', 'TRUCK'];
  const type = types[Math.floor(Math.random() * types.length)];
  const colors = ['#dc2626', '#2563eb', '#059669', '#d97706', '#475569', '#0284c7', '#7c3aed', '#059669', '#4b5563'];

  let posX = 0, posY = 0, len = 24, w = 12, baseSpd = 1.6 + Math.random() * 0.8;
  if (type === 'BUS') { len = 42; w = 14; baseSpd = 1.3; }
  if (type === 'TRUCK') { len = 38; w = 14; baseSpd = 1.2; }

  if (dir === 'EB_L1') { posX = -40; posY = 122; }
  else if (dir === 'EB_L2') { posX = -40; posY = 144; }
  else if (dir === 'WB_L1') { posX = 840; posY = 216; }
  else if (dir === 'WB_L2') { posX = 840; posY = 238; }
  else if (dir === 'SB_L1') { posX = 345; posY = -40; }
  else if (dir === 'SB_L2') { posX = 368; posY = -40; }
  else if (dir === 'NB_L1') { posX = 432; posY = 420; }
  else if (dir === 'NB_L2') { posX = 455; posY = 420; }

  simVehicles.push({
    id: 'veh_' + Math.random().toString(36).substr(2, 6),
    type: type,
    dir: dir,
    x: posX,
    y: posY,
    speed: baseSpd,
    targetSpeed: baseSpd,
    length: len,
    width: w,
    color: colors[Math.floor(Math.random() * colors.length)]
  });
}

function updateSignalPhase() {
  signalTimer++;

  // Handle Tram Priority Override
  if (ppcRequested && signalPhase !== 'TRAM_PRIORITY') {
    if (signalPhase === 'EW_GREEN' || signalPhase === 'NS_GREEN') {
      signalPhase = 'TRAM_PRIORITY';
      signalTimer = 0;
    }
  }

  const maxTimer = SIGNAL_TIMINGS[signalPhase] || 300;
  if (signalTimer >= maxTimer) {
    signalTimer = 0;
    if (signalPhase === 'EW_GREEN') signalPhase = 'EW_YELLOW';
    else if (signalPhase === 'EW_YELLOW') signalPhase = 'NS_GREEN';
    else if (signalPhase === 'NS_GREEN') signalPhase = 'NS_YELLOW';
    else if (signalPhase === 'NS_YELLOW') signalPhase = 'EW_GREEN';
    else if (signalPhase === 'TRAM_PRIORITY') {
      signalPhase = 'EW_GREEN';
      ppcRequested = false;
    }
  }

  // Update UI Status Badge
  const statusDot = document.getElementById("sim-signal-dot");
  const statusText = document.getElementById("sim-signal-text");
  const statusBox = document.getElementById("sim-signal-status");

  if (statusText && statusDot && statusBox) {
    if (signalPhase === 'EW_GREEN') {
      statusText.textContent = "동서 직진 (녹색)";
      statusDot.style.background = "#22c55e";
      statusDot.style.boxShadow = "0 0 8px #22c55e";
      statusBox.style.background = "#dcfce7";
      statusBox.style.color = "#15803d";
      statusBox.style.borderColor = "#86efac";
    } else if (signalPhase === 'EW_YELLOW' || signalPhase === 'NS_YELLOW') {
      statusText.textContent = "신호 변경 주의 (황색)";
      statusDot.style.background = "#eab308";
      statusDot.style.boxShadow = "0 0 8px #eab308";
      statusBox.style.background = "#fef9c3";
      statusBox.style.color = "#a16207";
      statusBox.style.borderColor = "#fde047";
    } else if (signalPhase === 'NS_GREEN') {
      statusText.textContent = "남북 직진 (녹색)";
      statusDot.style.background = "#22c55e";
      statusDot.style.boxShadow = "0 0 8px #22c55e";
      statusBox.style.background = "#dcfce7";
      statusBox.style.color = "#15803d";
      statusBox.style.borderColor = "#86efac";
    } else if (signalPhase === 'TRAM_PRIORITY') {
      statusText.textContent = "🚦 트램 우선신호 획득 (PPC ACTIVE)";
      statusDot.style.background = "#0284c7";
      statusDot.style.boxShadow = "0 0 10px #0284c7";
      statusBox.style.background = "#e0f2fe";
      statusBox.style.color = "#0369a1";
      statusBox.style.borderColor = "#7dd3fc";
    }
  }
}

function updateVehicles() {
  const isEWRed = (signalPhase === 'NS_GREEN' || signalPhase === 'NS_YELLOW');
  const isNSRed = (signalPhase === 'EW_GREEN' || signalPhase === 'EW_YELLOW' || signalPhase === 'TRAM_PRIORITY');
  const isAllRed = (signalPhase === 'TRAM_PRIORITY');

  // Stop lines
  const STOP_EB = 250;
  const STOP_WB = 540;
  const STOP_SB = 80;
  const STOP_NB = 300;

  // Update Tram
  if (simTram) {
    simTram.x += simTram.speed;
    if (simTram.x > 200 && simTram.x < 600) {
      ppcRequested = true;
    }
    if (simTram.x > 880) {
      simTram = null;
    }
  }

  // Update Vehicles
  for (let i = simVehicles.length - 1; i >= 0; i--) {
    const v = simVehicles[i];
    let shouldStop = false;

    // Traffic light checks
    if (v.dir.startswith('EB')) {
      if ((isEWRed || isAllRed) && v.x < STOP_EB && (v.x + v.length >= STOP_EB - 35)) {
        shouldStop = true;
      }
    } else if (v.dir.startswith('WB')) {
      if ((isEWRed || isAllRed) && v.x > STOP_WB && (v.x - v.length <= STOP_WB + 35)) {
        shouldStop = true;
      }
    } else if (v.dir.startswith('SB')) {
      if ((isNSRed || isAllRed) && v.y < STOP_SB && (v.y + v.length >= STOP_SB - 35)) {
        shouldStop = true;
      }
    } else if (v.dir.startswith('NB')) {
      if ((isNSRed || isAllRed) && v.y > STOP_NB && (v.y - v.length <= STOP_NB + 35)) {
        shouldStop = true;
      }
    }

    // Vehicle ahead check in same lane
    for (let j = 0; j < simVehicles.length; j++) {
      if (i === j) continue;
      const other = simVehicles[j];
      if (other.dir !== v.dir) continue;

      if (v.dir.startswith('EB') && other.x > v.x && (other.x - v.x < v.length + 15)) shouldStop = true;
      if (v.dir.startswith('WB') && other.x < v.x && (v.x - other.x < v.length + 15)) shouldStop = true;
      if (v.dir.startswith('SB') && other.y > v.y && (other.y - v.y < v.length + 15)) shouldStop = true;
      if (v.dir.startswith('NB') && other.y < v.y && (v.y - other.y < v.length + 15)) shouldStop = true;
    }

    // Accelerate / Decelerate
    if (shouldStop) {
      v.speed = Math.max(0, v.speed - 0.12);
    } else {
      v.speed = Math.min(v.targetSpeed, v.speed + 0.08);
    }

    // Move
    if (v.dir.startswith('EB')) v.x += v.speed;
    else if (v.dir.startswith('WB')) v.x -= v.speed;
    else if (v.dir.startswith('SB')) v.y += v.speed;
    else if (v.dir.startswith('NB')) v.y -= v.speed;

    // Remove offscreen
    if (v.x > 880 || v.x < -80 || v.y > 440 || v.y < -80) {
      simVehicles.splice(i, 1);
    }
  }
}

function renderTrafficSvgOverlay() {
  const group = document.getElementById("svg-vehicles-group");
  if (!group) return;

  // Signal LED Colors
  const isEWGreen = (signalPhase === 'EW_GREEN');
  const isEWYellow = (signalPhase === 'EW_YELLOW');
  const isNSGreen = (signalPhase === 'NS_GREEN');
  const isNSYellow = (signalPhase === 'NS_YELLOW');
  const isTramPri = (signalPhase === 'TRAM_PRIORITY');

  const colorEB = (isEWGreen || isTramPri) ? '#22c55e' : (isEWYellow ? '#eab308' : '#ef4444');
  const colorWB = colorEB;
  const colorNS = isNSGreen ? '#22c55e' : (isNSYellow ? '#eab308' : '#ef4444');

  let html = `
    <!-- Traffic Signals 🚦 -->
    <g id="signals-layer">
      <!-- Eastbound Signal (x=245, y=70) -->
      <rect x="235" y="65" width="28" height="14" fill="#0f172a" rx="4" stroke="#475569" stroke-width="1"/>
      <circle cx="243" cy="72" r="4" fill="${colorEB}" filter="drop-shadow(0 0 4px ${colorEB})"/>
      <circle cx="255" cy="72" r="4" fill="${colorEB === '#ef4444' ? '#ef4444' : '#334155'}"/>

      <!-- Westbound Signal (x=535, y=275) -->
      <rect x="535" y="275" width="28" height="14" fill="#0f172a" rx="4" stroke="#475569" stroke-width="1"/>
      <circle cx="543" cy="282" r="4" fill="${colorWB === '#ef4444' ? '#ef4444' : '#334155'}"/>
      <circle cx="555" cy="282" r="4" fill="${colorWB}" filter="drop-shadow(0 0 4px ${colorWB})"/>

      <!-- Southbound Signal (x=285, y=40) -->
      <rect x="285" y="40" width="14" height="28" fill="#0f172a" rx="4" stroke="#475569" stroke-width="1"/>
      <circle cx="292" cy="48" r="4" fill="${colorNS === '#ef4444' ? '#ef4444' : '#334155'}"/>
      <circle cx="292" cy="60" r="4" fill="${colorNS}" filter="drop-shadow(0 0 4px ${colorNS})"/>

      <!-- Northbound Signal (x=500, y=310) -->
      <rect x="500" y="310" width="14" height="28" fill="#0f172a" rx="4" stroke="#475569" stroke-width="1"/>
      <circle cx="507" cy="318" r="4" fill="${colorNS}" filter="drop-shadow(0 0 4px ${colorNS})"/>
      <circle cx="507" cy="330" r="4" fill="${colorNS === '#ef4444' ? '#ef4444' : '#334155'}"/>
    </g>
  `;

  // Render Tram Priority Banner
  if (isTramPri) {
    html += `
      <g transform="translate(400, 35)">
        <rect x="-140" y="-14" width="280" height="28" fill="#0284c7" rx="14" filter="drop-shadow(0 2px 8px rgba(2,132,199,0.5))"/>
        <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="12px" font-weight="900" fill="#ffffff">
          🚦 트램 우선신호 (PPC ACTIVE) 통과 중
        </text>
      </g>
    `;
  }

  // Render Vehicles
  simVehicles.forEach(v => {
    if (v.dir.startswith('EB')) {
      html += `
        <g transform="translate(${v.x}, ${v.y})">
          <rect x="0" y="${-v.width/2}" width="${v.length}" height="${v.width}" fill="${v.color}" rx="4" filter="drop-shadow(0 2px 3px rgba(0,0,0,0.25))"/>
          <!-- Headlights -->
          <circle cx="${v.length-2}" cy="${-v.width/2 + 2}" r="2" fill="#fef08a"/>
          <circle cx="${v.length-2}" cy="${v.width/2 - 2}" r="2" fill="#fef08a"/>
          ${v.type === 'BUS' ? `<rect x="6" y="${-v.width/2 + 2}" width="${v.length-12}" height="${v.width-4}" fill="#e2e8f0" opacity="0.6" rx="2"/>` : ''}
        </g>
      `;
    } else if (v.dir.startswith('WB')) {
      html += `
        <g transform="translate(${v.x}, ${v.y})">
          <rect x="${-v.length}" y="${-v.width/2}" width="${v.length}" height="${v.width}" fill="${v.color}" rx="4" filter="drop-shadow(0 2px 3px rgba(0,0,0,0.25))"/>
          <!-- Headlights -->
          <circle cx="${-v.length+2}" cy="${-v.width/2 + 2}" r="2" fill="#fef08a"/>
          <circle cx="${-v.length+2}" cy="${v.width/2 - 2}" r="2" fill="#fef08a"/>
          ${v.type === 'BUS' ? `<rect x="${-v.length+6}" y="${-v.width/2 + 2}" width="${v.length-12}" height="${v.width-4}" fill="#e2e8f0" opacity="0.6" rx="2"/>` : ''}
        </g>
      `;
    } else if (v.dir.startswith('SB')) {
      html += `
        <g transform="translate(${v.x}, ${v.y})">
          <rect x="${-v.width/2}" y="0" width="${v.width}" height="${v.length}" fill="${v.color}" rx="4" filter="drop-shadow(0 2px 3px rgba(0,0,0,0.25))"/>
          <circle cx="${-v.width/2 + 2}" cy="${v.length-2}" r="2" fill="#fef08a"/>
          <circle cx="${v.width/2 - 2}" cy="${v.length-2}" r="2" fill="#fef08a"/>
        </g>
      `;
    } else if (v.dir.startswith('NB')) {
      html += `
        <g transform="translate(${v.x}, ${v.y})">
          <rect x="${-v.width/2}" y="${-v.length}" width="${v.width}" height="${v.length}" fill="${v.color}" rx="4" filter="drop-shadow(0 2px 3px rgba(0,0,0,0.25))"/>
          <circle cx="${-v.width/2 + 2}" cy="${-v.length+2}" r="2" fill="#fef08a"/>
          <circle cx="${v.width/2 - 2}" cy="${-v.length+2}" r="2" fill="#fef08a"/>
        </g>
      `;
    }
  });

  // Render Tram Unit (🚊 5-Module Train)
  if (simTram) {
    const tx = simTram.x;
    const ty = simTram.y;
    html += `
      <g transform="translate(${tx}, ${ty})">
        <!-- Main Tram Body -->
        <rect x="-90" y="-13" width="90" height="26" fill="#0284c7" rx="6" stroke="#0369a1" stroke-width="2" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.35))"/>
        <!-- Glass Windows -->
        <rect x="-82" y="-10" width="74" height="20" fill="#38bdf8" opacity="0.85" rx="3"/>
        <!-- Module Sections -->
        <line x1="-70" y1="-13" x2="-70" y2="13" stroke="#0f172a" stroke-width="1.5"/>
        <line x1="-50" y1="-13" x2="-50" y2="13" stroke="#0f172a" stroke-width="1.5"/>
        <line x1="-30" y1="-13" x2="-30" y2="13" stroke="#0f172a" stroke-width="1.5"/>
        <line x1="-10" y1="-13" x2="-10" y2="13" stroke="#0f172a" stroke-width="1.5"/>
        <!-- Front Glowing Headlights -->
        <circle cx="2" cy="-8" r="3.5" fill="#fef08a" filter="drop-shadow(0 0 6px #fef08a)"/>
        <circle cx="2" cy="8" r="3.5" fill="#fef08a" filter="drop-shadow(0 0 6px #fef08a)"/>
        <!-- Tram Roof Pantograph -->
        <rect x="-48" y="-4" width="8" height="8" fill="#e2e8f0" rx="1"/>
        <!-- Tram Front Label -->
        <text x="-45" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="900" fill="#ffffff">동탄트램 101호</text>
      </g>
    `;
  }

  group.innerHTML = html;
}

function runTrafficAnimLoop() {
  if (!simRunning) return;
  simTime++;
  spawnRandomVehicle();
  updateSignalPhase();
  updateVehicles();
  renderTrafficSvgOverlay();
  simAnimFrameId = requestAnimationFrame(runTrafficAnimLoop);
}

function startTrafficSimulation() {
  simRunning = true;
  simVehicles = [];
  spawnTram();
  runTrafficAnimLoop();
}

function stopTrafficSimulation() {
  simRunning = false;
  if (simAnimFrameId) {
    cancelAnimationFrame(simAnimFrameId);
    simAnimFrameId = null;
  }
}
"""

# Update renderModalSvgDiagram to include <g id="svg-vehicles-group"></g>
pattern_svg_end = r'(<!-- Stage & Method Overlay Badge -->[\s\S]*?</g>)'
replacement_svg_end = r'\1\n\n    <!-- Dynamic Animated Vehicles & Tram Overlay Layer -->\n    <g id="svg-vehicles-group"></g>'

if 'id="svg-vehicles-group"' not in content:
    content = re.sub(pattern_svg_end, replacement_svg_end, content, count=1)
    print("Added svg-vehicles-group container to SVG diagram template!")

# Inject JS loop logic into content
if 'function startTrafficSimulation()' not in content:
    pos_js_end = content.rfind("</script>")
    content = content[:pos_js_end] + full_sim_js + "\n" + content[pos_js_end:]
    print("Injected Traffic & Tram Simulation JS Engine!")

# Trigger startTrafficSimulation inside openIntersectionModal and stopTrafficSimulation inside closeIntersectionModal
if 'startTrafficSimulation();' not in content:
    content = content.replace('modal.classList.add("active");', 'modal.classList.add("active");\n  startTrafficSimulation();')
    print("Hooked startTrafficSimulation() into openIntersectionModal!")

if 'stopTrafficSimulation();' not in content:
    content = content.replace('modal.classList.remove("active");', 'modal.classList.remove("active");\n  stopTrafficSimulation();')
    print("Hooked stopTrafficSimulation() into closeIntersectionModal!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying Traffic & Tram Simulation to V1 HTML!")
