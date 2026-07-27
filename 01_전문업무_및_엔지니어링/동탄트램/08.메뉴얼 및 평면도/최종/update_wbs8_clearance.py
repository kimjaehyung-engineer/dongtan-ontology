import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 8 Path
wbs8_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\8_장비,자재 반입로_반입구 간섭 검토"

# Ensure directories exist
os.makedirs(os.path.join(wbs8_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(wbs8_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(wbs8_base, "체크리스트"), exist_ok=True)

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
        desc: '자재 수송 트레일러 상단 또는 운반물 상단 끝단과 주행 도로 상부에 매설/가설된 교통 신호등, 도로 안내 표지판, 한전 가공전선과의 수직 여유 거리입니다. 감전 및 물리적 파손을 예방하기 위해 최소 5m 이상 확보해야 합니다.'
    },
    'scaffolding': {
        title: '🧱 가공 비계 (Overhead Scaffolding)',
        desc: '철도 공사 중인 도로 중앙 궤도 부지 주변에 설치된 외부 작업용 비계 파이프 구조물입니다. 차량 주행 반경 내에 비계 끝단이 돌출되는 경우 선회하는 트레일러 적재함과의 충돌 리스크가 있어 사전 철거가 필요합니다.'
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
# WBS 8 STANDARD HTML (장비,자재 반입로_반입구 간섭 검토)
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
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-8 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">트레일러 회전반경 R=15m & 지장물 이격 5m</span>
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

        <!-- 3. 트레일러 회전 궤적 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 대형 장대레일 트레일러(25m) 선회 R=15m 기하학적 궤적도
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    
                    <!-- Roads layout -->
                    <path d="M 50 160 L 500 160 L 500 240 M 620 240 L 620 160 L 850 160 M 850 40 L 620 40 L 620 0 M 500 0 L 500 40 L 50 40" stroke="#94a3b8" stroke-width="2" fill="none" stroke-dasharray="6"/>
                    <rect x="500" y="40" width="120" height="120" fill="#e2e8f0" opacity="0.4"/>
                    
                    <!-- Center lines -->
                    <path d="M 50 100 L 440 100 L 560 220 M 560 220 L 560 240" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4"/>
                    
                    <!-- R=15m Arc -->
                    <path d="M 500 160 A 120 120 0 0 1 620 40" stroke="#ea580c" stroke-width="3" fill="none"/>
                    <text x="590" y="115" font-size="11" font-weight="bold" fill="#ea580c">R=15m 선회 반경 확보</text>
                    
                    <!-- Trailer Vehicle representation -->
                    <g transform="translate(180, 80)">
                        <rect x="0" y="5" width="220" height="30" rx="4" fill="#475569" stroke="#1e293b" stroke-width="2"/>
                        <!-- Wheels -->
                        <circle cx="20" cy="38" r="8" fill="#0f172a"/>
                        <circle cx="40" cy="38" r="8" fill="#0f172a"/>
                        <circle cx="180" cy="38" r="8" fill="#0f172a"/>
                        <circle cx="200" cy="38" r="8" fill="#0f172a"/>
                        <text x="110" y="24" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">레일 수송 트레일러 (L &ge; 25m)</text>
                    </g>
                    
                    <!-- Legend -->
                    <circle cx="700" cy="60" r="6" fill="#ea580c"/>
                    <text x="715" y="64" font-size="11" fill="#475569">최소 선회 곡선부 (R = 15m)</text>
                    
                    <circle cx="700" cy="85" r="6" fill="#475569"/>
                    <text x="715" y="89" font-size="11" fill="#475569">타공종 가설 비계 간섭 차단 구간</text>
                </svg>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-8 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs8_base, "표준서", "장비,자재 반입로_반입구 간섭 검토_표준서.html"), wbs8_standard)


# =========================================================================
# WBS 8 GUIDELINE HTML (장비,자재 반입로_반입구 간섭 검토)
# =========================================================================
wbs8_guideline = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 장비,자재 반입로/반입구 간섭 검토 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        {minimal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-8 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">반입로 유도 수칙</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">장비·자재 반입로/반입구 간섭 검토 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"상부 신호등 이격거리 5m 실측, 도로 점용 인허가 및 신호수 배치 절차"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 대형 장대레일(L&ge;25m) 트레일러의 선회 반경 R=15m를 확보하고 상부 전선 등 지장 시설물과의 물리 충돌을 방지함</p>
                <p><strong>⚙️ 수행 주체:</strong> 현장공사팀 주관 하에 전담 신호수 배치 및 도로 점용 구역 통제</p>
            </div>
        </div>
        
        <!-- 2. 세부 절차 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 반입 간섭 검토 3단계 세부 수행 프로세스
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 현장 조사 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">상부 신호등/가공전선 이격 실측 및 점용 구간 설정</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>수직 이격거리 실측:</strong> 도로 상부 신호등, 안내 표지판 및 가공 고압 전선과의 수직 <span class="term-highlight" onclick="openGlossary('clearance')">이격거리(5m 이상)</span> 실측 상태 검증</li>
                        <li><strong>허가 구역 사전 조사:</strong> 도로점용 허가 승인 구역 및 주변 차로 통제 폭 종합 실사 수행</li>
                        <li><strong>가설 간섭 제거:</strong> 주행 동선 주변 타공종 <span class="term-highlight" onclick="openGlossary('scaffolding')">가공 비계</span> 및 펜스 간섭 범위 해제 요청</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 반입 및 주행 제어 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">선회 반경 시뮬레이션 승인 및 전담 신호수 차선 통제 유도</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>선회 궤적 검토:</strong> 길이 25m 이상 트레일러의 회전 반경 <span class="term-highlight" onclick="openGlossary('rotation_radius')">R=15m</span> 확보 시뮬레이션 보고서 사전 승인 완료</li>
                        <li><strong>전담 신호수 배치:</strong> 교차로 및 궤도 부지 진입로(반입구) 병목 구간에 전담 신호수를 밀착 배치하여 대형 레일 운반 차량 유도</li>
                        <li><strong>교통 소통 유지:</strong> 도로점용 허가 조건(허가 필증 소지)에 맞추어 인접 일반 주행 차량 통제 조율 및 일시 차단 실시</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 복구 및 검증 마감 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">도로 점용 필증 회수 및 반입로 기록 보존</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>대형 운송 장비 퇴거 즉시 점용 도로 복구 상태 점검 및 도로 시설물 원상 복구</li>
                        <li>도로점용 허가 완료 보고서 및 반입로 시뮬레이션 결과 보고서 파일 최종 저장 및 대장 공유</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-8 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs8_base, "수행지침", "장비,자재 반입로_반입구 간섭 검토_수행지침.html"), wbs8_guideline)


# =========================================================================
# WBS 8 CHECKLIST HTML (장비,자재 반입로_반입구 간섭 검토)
# =========================================================================
wbs8_checklist = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 장비,자재 반입로/반입구 간섭 검토 체크리스트</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
            --border-color: #cbd5e1;
        }
        body {
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            padding: 30px 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 35px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .header {
            border-bottom: 2px solid var(--text-primary);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .title {
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0;
            color: #1e3a8a;
        }
        .meta {
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }
        .summary-box {
            background: #fdf2f8;
            border: 1px solid #fbcfe8;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #9d174d;
        }
        table {
            width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid var(--border-color);
            padding: 14px;
            font-size: 0.92rem;
            text-align: left;
        }
        th {
            background: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }
        .category {
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            width: 18%;
        }
        .pre-row { color: #0f172a; }
        .ing-row { color: #0f172a; }
        .post-row { color: #0f172a; }
        .label-pre { color: var(--accent-orange); font-weight: bold; }
        .label-ing { color: var(--accent-red); font-weight: bold; }
        .label-post { color: var(--accent-green); font-weight: bold; }
        .check-cell {
            text-align: center;
            vertical-align: middle;
            width: 15%;
            font-weight: bold;
            color: #1e3a8a;
        }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 15px;
        }
        {minimal_style}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">장비,자재 반입로/반입구 간섭 검토 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-8 | 현장 내부 품질대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">장대레일 운반 트레일러(L&ge;25m) 회전반경 R=15m 시뮬레이션 승인, 상부 신호등/가공전선 이격 5m 이상 확보 및 가공 비계 간섭 배제</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 47 30 00 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[선회 곡선/R=15m]</strong> 25m 트레일러 차량 회전 반경 R=15m 시뮬레이션 결과서 승인 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[이격거리/가공전선]</strong> 주행로 상부 신호등 및 가공 고압 전선과의 수직 <span class="term-highlight" onclick="openGlossary('clearance')">이격거리 5m 이상</span> 현장 실측 확인 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[비계 간섭/사전배제]</strong> 주행 도로 선회 반경 내 돌출된 타공종 <span class="term-highlight" onclick="openGlossary('scaffolding')">가공 비계</span> 및 가설재 간섭 영역 사전 해제 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[신호수/대열 유도]</strong> 주요 선회 병목 지역에 전담 신호수를 밀착 배치하여 대형 <span class="term-highlight" onclick="openGlossary('long_rail')">장대레일</span> 운반 차량의 실시간 유도 통제 수행 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[인허가/도로점용]</strong> 유효한 도로점용허가증(허가 기간 및 면적 구획선) 현장 소지 및 인근 차량 통제 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[도로 원상복구]</strong> 대형 자재 차량 철수 즉시 도로 파손 상태 확인 및 점용 허가조건 준수 도로 원상 복구 완료 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[산출물/문서화]</strong> 반입로 시뮬레이션 보고서 및 도로점용허가서 파일 보존 관리 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs8_base, "체크리스트", "장비,자재 반입로_반입구 간섭 검토_체크리스트.html"), wbs8_checklist)


# =========================================================================
# COPIER AUTOMATION FOR PREFIXED FILES (WBS 8 Only)
# =========================================================================
print("\n🔄 Running fast copier to sync prefixed files for WBS 8...")
shutil.copy(os.path.join(wbs8_base, "표준서", "장비,자재 반입로_반입구 간섭 검토_표준서.html"), os.path.join(wbs8_base, "표준서", "8_장비,자재 반입로_반입구 간섭 검토_표준서.html"))
shutil.copy(os.path.join(wbs8_base, "수행지침", "장비,자재 반입로_반입구 간섭 검토_수행지침.html"), os.path.join(wbs8_base, "수행지침", "8_장비,자재 반입로_반입구 간섭 검토_수행지침.html"))
shutil.copy(os.path.join(wbs8_base, "체크리스트", "장비,자재 반입로_반입구 간섭 검토_체크리스트.html"), os.path.join(wbs8_base, "체크리스트", "8_장비,자재 반입로_반입구 간섭 검토_체크리스트.html"))

print("💾 Synced WBS 8 Prefixed copies successfully.")
print("\n🎉 SUCCESSFULLY COMPLETED ALL WBS 8 FILE MIGRATIONS AND GEOMETRIC ROAD SIMULATIONS!")
