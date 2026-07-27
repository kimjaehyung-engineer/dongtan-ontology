import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 8 Path
wbs8_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\8_장비,자재 반입로_반입구 간섭 검토"

# -------------------------------------------------------------------------
# CONSTANT: Minimal Popups Styling
# -------------------------------------------------------------------------
minimal_glossary_style = """
    /* Glossary Modal Styles - Minimal Injection */
    .term-highlight {
        color: #0284c7 !important;
        font-weight: 700 !important;
        border-bottom: 2px dashed #0284c7 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        padding: 0 2px !important;
    }
    .term-highlight:hover {
        background: #e0f2fe !important;
        color: #0369a1 !important;
        border-radius: 4px !important;
    }
    .scene-link {
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        color: #059669 !important;
        font-weight: 700 !important;
        background: #ecfdf5 !important;
        border: 1px solid #10b981 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        font-size: 0.8rem !important;
        cursor: pointer !important;
        margin-left: 8px !important;
        transition: all 0.2s ease !important;
        text-decoration: none !important;
    }
    .scene-link:hover {
        background: #d1fae5 !important;
        color: #065f46 !important;
    }
    .glossary-modal {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(4px);
        align-items: center;
        justify-content: center;
    }
    .glossary-modal.active {
        display: flex;
    }
    .glossary-modal-content {
        background-color: #ffffff;
        margin: auto;
        padding: 24px;
        border: 1px solid #e2e8f0;
        width: 90%;
        max-width: 520px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        position: relative;
        animation: modalFadeIn 0.3s ease;
        text-align: left;
    }
    @keyframes modalFadeIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .glossary-close {
        color: #94a3b8;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.2s;
    }
    .glossary-close:hover {
        color: #334155;
    }
"""

# -------------------------------------------------------------------------
# CONSTANT: Glossary popup modal layer and data script for WBS 8
# -------------------------------------------------------------------------
common_modal_html = """
<!-- Glossary & Scene Popup Modal Layer -->
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 시공장면 해설</h3>
        <div class="modal-body">
            <img id="modalImage" src="" style="width:100%; border-radius:10px; display:none; margin-bottom:15px; border: 1px solid #cbd5e1;" />
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<script>
const glossaryData = {
    'long_rail': {
        title: '🛤️ 장대레일 (Long Welded Rail)',
        desc: '트램 시공을 위해 250m 이상의 길이로 연속 용접된 일체형 레일입니다. 현장 반입을 위해 최소 25m 이상의 특수 트레일러(트레일러+레일 거치대) 수송 차량이 도로 주행을 해야 하므로 고난도의 회전각 조율이 필요합니다.'
    },
    'rotation_radius': {
        title: '📐 최소 회전 반경 R=15m (Minimum Turning Radius)',
        desc: '길이 25m 이상의 장대레일 수송용 대형 트레일러가 도로 교차로 또는 진출입로를 회전할 때 앞바퀴와 뒷바퀴의 선회 궤적이 그리는 기하학적 최소 반경입니다. R=15m 이상을 충족해야 타이어 걸림 및 중앙선 침범 충돌을 피할 수 있습니다.'
    },
    'clearance': {
        title: '⚡ 상부 이격거리 5m (Vertical Clearance)',
        desc: '자재 수송 트레일러 상단 또는 운반물 상단 끝단과 주행 도로 상부에 매설/가설된 교통 신호등, 도로 안내 표지판, 한전 가공 고압 전선과의 수직 여유 거리입니다. 감전 및 물리적 파손을 예방하기 위해 최소 5m 이상 확보해야 합니다.'
    },
    'scaffolding': {
        title: '🧱 가공 비계 (Overhead Scaffolding)',
        desc: '철도 공사 중인 도로 중앙 궤도 부지 주변에 설치된 외부 작업용 비계 파이프 구조물입니다. 차량 주행 반경 내에 비계 끝단이 돌출되는 경우 선회하는 트레일러 적재함과의 충돌 리스크가 있어 사전 철거가 필요합니다.'
    },
    'traffic_control': {
        title: '🚧 도심지 교통 소통 통제 (Traffic Control)',
        desc: '기존 차량이 다니는 도로에서 트램 공사를 수행하기 위해 차도를 안전하게 우회 및 부분 차단하고 안전펜스와 표지판을 조밀 배치하여 차량 정체와 안전사고를 동시 예방하는 공사 관리 지침입니다.'
    }
};

function openGlossary(termKey) {
    const data = glossaryData[termKey];
    if (!data) return;
    
    document.getElementById('modalTitle').innerText = data.title;
    document.getElementById('modalDescription').innerText = data.desc;
    
    const imgEl = document.getElementById('modalImage');
    if (data.img) {
        imgEl.src = data.img;
        imgEl.style.display = 'block';
    } else {
        imgEl.src = '';
        imgEl.style.display = 'none';
    }
    
    document.getElementById('glossaryModal').classList.add('active');
}

function openScene(sceneKey) {
    openGlossary(sceneKey);
}

function closeGlossaryModal() {
    document.getElementById('glossaryModal').classList.remove('active');
}

// Esc close key handler
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeGlossaryModal();
    }
});
</script>
"""

# Force write helper
def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Written Original: {path}")


# =========================================================================
# WBS 8 STANDARD HTML (With High-visibility & Perfectly Aligned Text Boxes)
# =========================================================================
wbs8_standard = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 장비,자재 반입로/반입구 간섭 검토 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        {minimal_style}
        .sim-btn {
            transition: all 0.2s ease;
        }
        .sim-btn:hover {
            transform: translateY(-1px);
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-8 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">수평 R=15m & 수직 H=5m 이단 시뮬레이션</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">장비·자재 반입로/반입구 간섭 검토 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"대형 레일 수송 트레일러 선회 궤적 안전성 및 도로 점용 인허가 검증 기준"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 과업 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명 / 주관</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 장비,자재 반입로_반입구 간섭 검토 (현장공사팀 주관)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 공학 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">반입로 시뮬레이션 보고서 | 관할청 도로점용허가서</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 대형 궤도 건설 장비 및 장대레일 수송 차량이 안전하게 노선 부지에 도달하도록 반입로 기하구조 및 상하부 물리 간섭을 차단함</p>
                <p><strong>⚙️ 검토 방법:</strong> 자재 반입 시 노반 토목 시공 구간과의 선형 간섭 검토, 도로 점용 가능 시기 및 가설 지장물 이격거리 확보 계획 수립</p>
            </div>
        </div>

        <!-- 2. 정량적 공학 기술 표준 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 반입 트레일러 선회 및 지장물 정량적 공학 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">공학 검증 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 기술 규격</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 상세 기술 표준</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">트레일러 선회 반경</td>
                            <td class="p-3 border text-center font-bold text-blue-700"><span class="term-highlight" onclick="openGlossary('rotation_radius')">R &ge; 15m</span> 확보</td>
                            <td class="p-3 border text-slate-600">• 길이 25m 이상의 <span class="term-highlight" onclick="openGlossary('long_rail')">장대레일</span> 운반 트레일러 선회 시 도로 연석 및 중앙 분리대 간섭 차단을 위한 최소 곡선 궤적 확보</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">상부 지장물 이격</td>
                            <td class="p-3 border text-center font-bold text-blue-700"><span class="term-highlight" onclick="openGlossary('clearance')">5.0m 이상</span> 이격</td>
                            <td class="p-3 border text-slate-600">• 상부 교통 신호기, 도로 안내 표지판, 한전 가공 고압 전선과 자재 적재 차량의 최상단 사이의 수직 이격거리 실측 기준</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">가설 비계 간섭 해제</td>
                            <td class="p-3 border text-center font-bold text-red-600">물리적 충돌 0%</td>
                            <td class="p-3 border text-slate-600">• 선회 도로 주변 타공종 <span class="term-highlight" onclick="openGlossary('scaffolding')">가공 비계</span>, 가설 울타리 돌출부 사전 확인 및 한계 간섭 영역 내 구조물 일시 철거/후퇴 수립</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 대형 장대레일 트레일러(25m) 수평 선회 시뮬레이터 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 대형 장대레일 트레일러(25m) 기하학적 수평 선회 궤적 시뮬레이터
            </h2>
            <p class="text-xs text-slate-500 mb-4">※ [선회반경 선택] 버튼을 눌러 R=12m(중앙분리대/가설비계 충돌 리스크)와 R=15m(안전 우회 표준 규격)의 차이를 시뮬레이션으로 직접 조작해 보세요.</p>
            
            <div class="bg-slate-100 border border-slate-300 rounded-2xl p-6">
                <!-- 제어 판넬 -->
                <div class="flex flex-wrap gap-3 items-center justify-between mb-5 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex items-center gap-2">
                        <span class="text-sm font-bold text-slate-700">선회 반경 조건:</span>
                        <button id="btnRadius12" onclick="setRadius(12)" class="sim-btn bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300">R=12m (미달)</button>
                        <button id="btnRadius15" onclick="setRadius(15)" class="sim-btn bg-blue-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-blue-700">R=15m (표준)</button>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="startSimulation()" class="sim-btn bg-emerald-600 text-white text-xs font-bold px-4 py-1.5 rounded-lg flex items-center gap-1 shadow-sm">▶ 시작</button>
                        <button onclick="pauseSimulation()" class="sim-btn bg-amber-500 text-white text-xs font-bold px-4 py-1.5 rounded-lg flex items-center gap-1 shadow-sm">⏸ 정지</button>
                        <button onclick="resetSimulation()" class="sim-btn bg-slate-600 text-white text-xs font-bold px-4 py-1.5 rounded-lg flex items-center gap-1 shadow-sm">🔄 리셋</button>
                    </div>
                    <div id="statusAlert" class="text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800 border border-emerald-200 transition-all duration-300">
                        대기 중
                    </div>
                </div>

                <!-- 시뮬레이터 SVG 캔버스 -->
                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-inner relative" style="height: 300px;">
                    <svg id="simSvg" viewBox="0 0 900 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <rect width="900" height="300" fill="#f8fafc"/>
                        <!-- 도로 구조 -->
                        <path d="M 0 100 H 600 V 300 H 760 V 100 H 900 V 0 H 0 Z" fill="#cbd5e1" opacity="0.6"/>
                        <path d="M 0 100 H 600 V 300 H 760 V 100 H 900 V 0 H 0 Z" fill="none" stroke="#94a3b8" stroke-width="2"/>
                        <!-- 차선 -->
                        <path d="M 0 50 H 900" stroke="#fef08a" stroke-width="2" stroke-dasharray="8 8"/>
                        <path d="M 680 100 V 300" stroke="#fef08a" stroke-width="2" stroke-dasharray="8 8"/>
                        <!-- 가설비계 장애 구역 -->
                        <rect id="scaffoldZone" x="500" y="110" width="80" height="80" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4" rx="4"/>
                        <text x="540" y="145" text-anchor="middle" font-size="11" font-weight="black" fill="#ef4444">타공종 가설비계</text>
                        <text x="540" y="162" text-anchor="middle" font-size="10" fill="#ef4444">간섭 영역</text>
                        <!-- 선회 반경 R 가이드라인 -->
                        <path id="guideArc" d="M 450 100 A 150 150 0 0 0 600 250" stroke="#0284c7" stroke-width="2" stroke-dasharray="4 4" fill="none" opacity="0.7"/>
                        <!-- 주행 궤적 라인 -->
                        <path id="historyPath" d="" stroke="#10b981" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.5"/>
                        <!-- 차량 그룹 -->
                        <g id="trailerGroup" transform="translate(50, 25)">
                            <rect x="-140" y="-10" width="160" height="20" rx="3" fill="#475569" stroke="#1e293b" stroke-width="2"/>
                            <!-- 레일 적재물 -->
                            <line x1="-130" y1="-5" x2="10" y2="-5" stroke="#94a3b8" stroke-width="1.5"/>
                            <line x1="-130" y1="0" x2="10" y2="0" stroke="#94a3b8" stroke-width="1.5"/>
                            <line x1="-130" y1="5" x2="10" y2="5" stroke="#94a3b8" stroke-width="1.5"/>
                            <rect x="-120" y="-13" width="16" height="5" fill="#0f172a"/>
                            <rect x="-120" y="8" width="16" height="5" fill="#0f172a"/>
                            <rect x="-40" y="-13" width="16" height="5" fill="#0f172a"/>
                            <rect x="-40" y="8" width="16" height="5" fill="#0f172a"/>
                            <!-- 헤드차량 -->
                            <rect x="20" y="-12" width="40" height="24" rx="4" fill="#1e3a8a" stroke="#1e293b" stroke-width="2"/>
                            <rect x="42" y="-9" width="12" height="18" rx="1" fill="#bae6fd"/>
                            <circle cx="20" cy="0" r="4" fill="#f59e0b"/>
                            <rect x="25" y="-15" width="10" height="4" fill="#0f172a"/>
                            <rect x="25" y="11" width="10" height="4" fill="#0f172a"/>
                            <text x="-60" y="27" text-anchor="middle" font-size="9" font-weight="bold" fill="#334155">L=25m 레일 트레일러</text>
                        </g>
                    </svg>
                </div>
            </div>
        </div>

        <!-- 4. 상부 지장물 수직 이격거리(5.0m) 시뮬레이터 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">4.</span> 상부 지장물(신호등, 고압선) 수직 이격거리 시뮬레이터 (Side View)
            </h2>
            <p class="text-xs text-slate-500 mb-4">※ [수직 이격 높이 선택] 버튼을 조작하여 표준 규격(5.0m 이상)과 기준 미달 시 발생하는 간선 충돌/고압선 아크 스파크 현상을 확인해 보세요.</p>
            
            <div class="bg-slate-100 border border-slate-300 rounded-2xl p-6">
                <!-- 제어 판넬 -->
                <div class="flex flex-wrap gap-3 items-center justify-between mb-5 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex items-center gap-2">
                        <span class="text-sm font-bold text-slate-700">지장물 이격 조건:</span>
                        <button id="btnVert4" onclick="setVertClearance(4)" class="sim-btn bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300">4.0m 이격 (위험)</button>
                        <button id="btnVert5" onclick="setVertClearance(5)" class="sim-btn bg-blue-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-blue-700">5.0m 이격 (표준)</button>
                    </div>
                    <div id="vertStatusAlert" class="text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800 border border-emerald-200">
                        🟢 안전 이격 확보 (R=15m 표준)
                    </div>
                </div>

                <!-- 수직 시뮬레이터 SVG 캔버스 -->
                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-inner relative" style="height: 280px;">
                    <svg viewBox="0 0 900 280" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <!-- 배경 그라데이션 -->
                        <defs>
                            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" stop-color="#bae6fd" stop-opacity="0.3"/>
                                <stop offset="100%" stop-color="#f8fafc" stop-opacity="1"/>
                            </linearGradient>
                        </defs>
                        <rect width="900" height="280" fill="url(#skyGrad)"/>
                        
                        <!-- 도로 지면 -->
                        <rect x="0" y="230" width="900" height="50" fill="#475569"/>
                        <line x1="0" y1="230" x2="900" y2="230" stroke="#334155" stroke-width="3"/>
                        
                        <!-- 대형 자재 트레일러 (Side View) -->
                        <g transform="translate(150, 160)">
                            <!-- 트레일러 차체 바디 -->
                            <rect x="0" y="30" width="460" height="30" rx="3" fill="#334155" stroke="#1e293b" stroke-width="2"/>
                            <!-- 적재 레일 번들 -->
                            <rect x="20" y="10" width="420" height="20" fill="#94a3b8" stroke="#475569" stroke-width="1"/>
                            <line x1="20" y1="17" x2="440" y2="17" stroke="#64748b" stroke-width="1"/>
                            <!-- 바퀴들 -->
                            <circle cx="50" cy="65" r="10" fill="#0f172a"/>
                            <circle cx="75" cy="65" r="10" fill="#0f172a"/>
                            <circle cx="390" cy="65" r="10" fill="#0f172a"/>
                            <circle cx="415" cy="65" r="10" fill="#0f172a"/>
                            <!-- 동력 헤드트럭 -->
                            <path d="M 460 30 L 460 10 Q 470 0 490 0 L 515 0 Q 525 10 525 30 L 525 60 H 460 Z" fill="#1e3a8a" stroke="#1e293b" stroke-width="2"/>
                            <!-- 유리창 -->
                            <polygon points="495,10 515,10 515,25 495,25" fill="#e0f2fe"/>
                            <!-- 헤드 바퀴 -->
                            <circle cx="485" cy="65" r="10" fill="#0f172a"/>
                            
                            <!-- 라벨 -->
                            <text x="230" y="47" text-anchor="middle" font-size="12" font-weight="black" fill="#ffffff">장대레일 운반 트레일러 (적재단 H = 3.8m)</text>
                        </g>

                        <!-- 상부 지장물 그룹 (신호등 & 고압선) - JS에서 Y축 이동 -->
                        <g id="overheadObstacle" transform="translate(0, 0)">
                            <!-- 지장물 지지 지주 포스트 -->
                            <line x1="80" y1="0" x2="80" y2="230" stroke="#64748b" stroke-width="6"/>
                            <!-- 가로 신호등 Span arm -->
                            <line x1="80" y1="55" x2="520" y2="55" stroke="#64748b" stroke-width="4"/>
                            
                            <!-- 가로 신호등 기구 (H = 9.0m or H = 8.0m) -->
                            <rect x="360" y="43" width="64" height="24" rx="4" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
                            <circle cx="374" cy="55" r="6" fill="#ef4444"/>
                            <circle cx="392" cy="55" r="6" fill="#f59e0b"/>
                            <circle cx="410" cy="55" r="6" fill="#10b981"/>
                            
                            <!-- 신호등 라벨 텍스트 박스 추가로 가독성 강화 -->
                            <rect x="357" y="15" width="70" height="20" rx="3" fill="#1e293b"/>
                            <text x="392" y="29" text-anchor="middle" font-size="11" font-weight="black" fill="#ffffff">교통신호등</text>
                            
                            <!-- 가공 고압 전선 지장물 (3선) -->
                            <line x1="0" y1="30" x2="900" y2="30" stroke="#ef4444" stroke-width="2" stroke-dasharray="2 4"/>
                            <line x1="0" y1="36" x2="900" y2="36" stroke="#ef4444" stroke-width="2" stroke-dasharray="2 4"/>
                            
                            <rect x="680" y="12" width="160" height="20" rx="3" fill="#ea580c"/>
                            <text x="760" y="26" text-anchor="middle" font-size="11" font-weight="black" fill="#ffffff">한전 특고압 가공선로</text>
                        </g>

                        <!-- 이격거리 수직 치수선 (JS에서 좌표 갱신) -->
                        <g id="dimensionLine">
                            <!-- 수직선 화살표 -->
                            <line id="dimArrowLine" x1="392" y1="55" x2="392" y2="170" stroke="#0284c7" stroke-width="2.5"/>
                            <!-- 화살표 삼각 촉 -->
                            <polygon id="arrowTop" points="392,55 387,67 397,67" fill="#0284c7"/>
                            <polygon id="arrowBottom" points="392,170 387,158 397,158" fill="#0284c7"/>
                            
                            <!-- 수치 라벨 배경 상자 크기 증대 및 글자 안착 정밀 보정 -->
                            <rect id="labelBg" x="410" y="90" width="180" height="34" rx="6" fill="#0284c7"/>
                            <text id="vertLabelText" x="500" y="112" text-anchor="middle" font-size="14" font-weight="black" fill="#ffffff">이격거리 5.0m 확보</text>
                        </g>

                        <!-- 충돌 스파크/번개 이미지 효과 및 전용 붉은색 경고 상자 디자인 -->
                        <g id="sparkEffect" transform="translate(390, 120)" opacity="0">
                            <!-- 충돌 경고 백그라운드 붉은 상자 정식 렌더링 -->
                            <rect x="30" y="-12" width="280" height="38" rx="8" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>
                            <text x="170" y="12" text-anchor="middle" font-size="13" font-weight="black" fill="#ffffff">💥 아크 방전 및 접촉 충돌 발생!</text>
                            
                            <!-- 스파크 번개 모식도 -->
                            <polygon points="0,-25 15,-5 -8,5 20,30 -5,12 10,-5" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
                            <circle cx="5" cy="5" r="28" fill="#fbbf24" opacity="0.3" class="animate-ping"/>
                        </g>
                    </svg>
                </div>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-8 | 콘크리트도상
    </div>
</div>

{modal_html}

<script>
// Interactive Horizontal Simulation Logic
let simActive = false;
let simInterval = null;
let currentRadius = 15; // default R=15m
let currentT = 0; // time variable [0 to 100]
let pathCoordinates = [];

function getCoordinates(t, radius) {
    let x = 0; y = 0; angle = 0;
    if (radius === 15) {
        if (t <= 40) {
            x = 50 + (t / 40) * 400;
            y = 25;
            angle = 0;
        } else if (t <= 80) {
            let arcT = (t - 40) / 40;
            let theta = arcT * (Math.PI / 2);
            x = 450 + Math.sin(theta) * 190;
            y = 25 + (1 - Math.cos(theta)) * 190;
            angle = arcT * 90;
        } else {
            let straightT = (t - 80) / 20;
            x = 640;
            y = 215 + straightT * 100;
            angle = 90;
        }
    } else {
        if (t <= 40) {
            x = 50 + (t / 40) * 400;
            y = 25;
            angle = 0;
        } else if (t <= 80) {
            let arcT = (t - 40) / 40;
            let theta = arcT * (Math.PI / 2);
            x = 450 + Math.sin(theta) * 130;
            y = 25 + (1 - Math.cos(theta)) * 170;
            angle = arcT * 90;
        } else {
            x = 580;
            y = 195 + ((t - 80) / 20) * 110;
            angle = 90;
        }
    }
    return { x, y, angle };
}

function setRadius(r) {
    currentRadius = r;
    resetSimulation();
    const btn12 = document.getElementById('btnRadius12');
    const btn15 = document.getElementById('btnRadius15');
    const guideArc = document.getElementById('guideArc');
    
    if (r === 15) {
        btn15.className = "sim-btn bg-blue-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-blue-700";
        btn12.className = "sim-btn bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300";
        guideArc.setAttribute('d', 'M 450 25 A 190 190 0 0 1 640 215');
        guideArc.setAttribute('stroke', '#0284c7');
    } else {
        btn12.className = "sim-btn bg-red-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-red-700";
        btn15.className = "sim-btn bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300";
        guideArc.setAttribute('d', 'M 450 25 A 150 150 0 0 1 580 195');
        guideArc.setAttribute('stroke', '#ef4444');
    }
}

function startSimulation() {
    if (simActive) return;
    simActive = true;
    document.getElementById('statusAlert').innerText = "시뮬레이션 진행 중";
    document.getElementById('statusAlert').className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-blue-100 text-blue-800 border border-blue-200";
    
    simInterval = setInterval(() => {
        if (currentT >= 100) {
            clearInterval(simInterval);
            simActive = false;
            if (currentRadius === 15) {
                document.getElementById('statusAlert').innerText = "🟢 시공 표준 준수 (안전 통과)";
                document.getElementById('statusAlert').className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800 border border-emerald-200";
            } else {
                document.getElementById('statusAlert').innerText = "💥 가설비계/중앙선 충돌 발생 (불합격)";
                document.getElementById('statusAlert').className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-red-100 text-red-800 border border-red-200 animate-pulse";
            }
            return;
        }
        currentT += 1;
        updateVehiclePosition();
    }, 50);
}

function pauseSimulation() {
    clearInterval(simInterval);
    simActive = false;
    document.getElementById('statusAlert').innerText = "일시 정지";
    document.getElementById('statusAlert').className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-amber-100 text-amber-800 border border-amber-200";
}

function resetSimulation() {
    clearInterval(simInterval);
    simActive = false;
    currentT = 0;
    pathCoordinates = [];
    document.getElementById('historyPath').setAttribute('d', '');
    document.getElementById('statusAlert').innerText = "대기 중";
    document.getElementById('statusAlert').className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-slate-100 text-slate-800 border border-slate-200";
    updateVehiclePosition();
}

function updateVehiclePosition() {
    const pos = getCoordinates(currentT, currentRadius);
    const trailer = document.getElementById('trailerGroup');
    trailer.setAttribute('transform', `translate(${pos.x}, ${pos.y}) rotate(${pos.angle})`);
    pathCoordinates.push(`${pos.x},${pos.y}`);
    const dStr = "M " + pathCoordinates.join(" L ");
    document.getElementById('historyPath').setAttribute('d', dStr);
    
    const scaffoldZone = document.getElementById('scaffoldZone');
    if (currentRadius === 12 && currentT >= 48 && currentT <= 72) {
        scaffoldZone.setAttribute('fill', '#ef4444');
        scaffoldZone.setAttribute('opacity', '0.8');
        document.getElementById('statusAlert').innerText = "💥 충돌 위험! (비계 간섭 발생)";
        document.getElementById('statusAlert').className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-red-600 text-white border border-red-700 animate-bounce";
    } else {
        scaffoldZone.setAttribute('fill', '#fee2e2');
        scaffoldZone.setAttribute('opacity', '0.4');
    }
}

// -------------------------------------------------------------------------
// Vertical Clearance Simulation Logic
// -------------------------------------------------------------------------
function setVertClearance(h) {
    const btn4 = document.getElementById('btnVert4');
    const btn5 = document.getElementById('btnVert5');
    const obstacle = document.getElementById('overheadObstacle');
    
    const dimArrowLine = document.getElementById('dimArrowLine');
    const arrowTop = document.getElementById('arrowTop');
    const arrowBottom = document.getElementById('arrowBottom');
    const labelBg = document.getElementById('labelBg');
    const vertLabelText = document.getElementById('vertLabelText');
    const sparkEffect = document.getElementById('sparkEffect');
    const vertStatusAlert = document.getElementById('vertStatusAlert');

    if (h === 5) {
        // Standard 5m clearance
        btn5.className = "sim-btn bg-blue-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-blue-700";
        btn4.className = "sim-btn bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300";
        
        // Move obstacles up (Standard position)
        obstacle.setAttribute('transform', 'translate(0, 0)');
        
        // Adjust dimension line coords
        dimArrowLine.setAttribute('y1', '55');
        dimArrowLine.setAttribute('y2', '170');
        
        // Reposition arrows precisely
        arrowTop.setAttribute('points', '392,55 387,67 397,67');
        arrowBottom.setAttribute('points', '392,170 387,158 397,158');
        
        // Adjust measurement text box positioning (perfect alignment inside box)
        labelBg.setAttribute('y', '90');
        labelBg.setAttribute('fill', '#0284c7');
        vertLabelText.setAttribute('y', '112');
        vertLabelText.innerText = "이격거리 5.0m 확보";
        
        // Hide warning sparks
        sparkEffect.style.opacity = '0';
        vertStatusAlert.innerText = "🟢 안전 이격 확보 (R=15m 표준)";
        vertStatusAlert.className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800 border border-emerald-200";
    } else {
        // Restricted 4m clearance (Danger)
        btn4.className = "sim-btn bg-red-600 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-red-700";
        btn5.className = "sim-btn bg-slate-200 text-slate-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300";
        
        // Move obstacles down by 30px (Simulating lower wires/span arm)
        obstacle.setAttribute('transform', 'translate(0, 30)');
        
        // Adjust dimension line coords (shorter distance)
        dimArrowLine.setAttribute('y1', '85');
        dimArrowLine.setAttribute('y2', '170');
        
        // Reposition arrows precisely
        arrowTop.setAttribute('points', '392,85 387,97 397,97');
        arrowBottom.setAttribute('points', '392,170 387,158 397,158');
        
        // Adjust measurement text box positioning (perfect alignment inside box)
        labelBg.setAttribute('y', '110');
        labelBg.setAttribute('fill', '#dc2626');
        vertLabelText.setAttribute('y', '132');
        vertLabelText.innerText = "🚨 이격거리 4.0m 미달";
        
        // Show sparks & collision card
        sparkEffect.style.opacity = '1';
        vertStatusAlert.innerText = "💥 지장물 충돌 및 감전 리스크 경보!";
        vertStatusAlert.className = "text-xs font-bold px-3 py-1.5 rounded-lg bg-red-600 text-white border border-red-700 animate-pulse";
    }
}

// Initial positioning on load
window.onload = function() {
    setRadius(15);
    setVertClearance(5);
};
</script>

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs8_base, "표준서", "장비,자재 반입로_반입구 간섭 검토_표준서.html"), wbs8_standard)


# =========================================================================
# COPIER AUTOMATION FOR PREFIXED FILES (WBS 8 Only)
# =========================================================================
print("\n🔄 Running fast copier to sync prefixed files for WBS 8...")
shutil.copy(os.path.join(wbs8_base, "표준서", "장비,자재 반입로_반입구 간섭 검토_표준서.html"), os.path.join(wbs8_base, "표준서", "8_장비,자재 반입로_반입구 간섭 검토_표준서.html"))
shutil.copy(os.path.join(wbs8_base, "수행지침", "장비,자재 반입로_반입구 간섭 검토_수행지침.html"), os.path.join(wbs8_base, "수행지침", "8_장비,자재 반입로_반입구 간섭 검토_수행지침.html"))
shutil.copy(os.path.join(wbs8_base, "체크리스트", "장비,자재 반입로_반입구 간섭 검토_체크리스트.html"), os.path.join(wbs8_base, "체크리스트", "8_장비,자재 반입로_반입구 간섭 검토_체크리스트.html"))

print("💾 Synced WBS 8 Prefixed copies successfully.")
print("\n🎉 WBS 8 DUAL SIMULATOR VISIBILITY ERROR AND LABEL POSITIONING PERFECTLY RESOLVED!")
