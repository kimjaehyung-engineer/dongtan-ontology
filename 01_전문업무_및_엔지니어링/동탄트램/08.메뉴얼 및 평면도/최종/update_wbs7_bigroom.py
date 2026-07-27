import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 7 Path
wbs7_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\7_작수전 Big Room 회의"

# Ensure directories exist
os.makedirs(os.path.join(wbs7_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(wbs7_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(wbs7_base, "체크리스트"), exist_ok=True)

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
# CONSTANT: Glossary popup modal layer and data script for Big Room
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
    'handover': {
        title: '🤝 노선 Handover (노선 인수인계)',
        desc: '선행 노반 토목공사 완료 후, 후행 궤도공사를 시작할 수 있도록 토목 시공 구간의 기하학적 선형, 고저 레벨, 종횡단 측량 성과를 대조·검증하여 상호 정식으로 인수인계하는 공정 인터페이스 단계입니다.'
    },
    'bigroom': {
        title: '🏢 Big Room 회의 (합동 의사결정 회의)',
        desc: '본사 공정/견적/설계 담당팀, 현장 관리자, 궤도 협력업체 및 선후행 토목·설비 협력업체가 한자리에 모여 공정 간 간섭 사항을 실시간으로 도면 조율하고 리스크 헤지 방안을 의결하는 통합 협의체 회의체입니다.'
    },
    'stray_current': {
        title: '⚡ 누설전류 (Stray Current)',
        desc: '트램 주행로인 레일(귀선로)에서 누설되어 주변 지중 매설 금속관로나 토목 철근 구조체로 흘러들어가 전기 화학적 부식을 유발하는 유도 전류입니다. 이를 방지하기 위해 부식 방지 다이오드 및 접지 배선 매설 계획이 필수적입니다.'
    },
    'loop_sensor': {
        title: '📡 신호 루프 센서 (Inductive Loop Sensor)',
        desc: '도상 콘크리트 내부에 루프 코일 선로를 포설하여 트램 차량의 위치와 대기 상태를 전자유도로 감지하고 교차로 신호 우선권을 제어하는 핵심 신호 설비입니다. 타설 전 정밀 위치 고정이 요구됩니다.'
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
# 1. WRITE STANDARD HTML (WBS 7 - 작수전 Big Room 회의)
# =========================================================================
wbs7_standard = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 작수전 Big Room 회의 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-7 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">노선 Handover & 누설전류 방지</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">작수전 Big Room 회의 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"노반-궤도 간 인터페이스 및 신호 루프 센서, 누설전류 부식 방지 디오드 접지선 의결 기준"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 과업 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명 / 주관</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 착수전 Big Room 회의 (현장소장 주관)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">핵심 의결 대상</span>
                    <p class="font-bold text-slate-800 mt-1">인터페이스 조정 | 누설전류 접지 | 루프센서 포설</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 궤도공사 수행 시 공정계획 수립 및 선후행 공종 간 간섭을 배제하고, 시공 시 예상가능한 리스크를 조밀 검토 및 의결함</p>
                <p><strong>⚙️ 수행 방법:</strong> 본사/현장/협력사 합동 협의체 구축. <span class="term-highlight" onclick="openGlossary('handover')">노반-궤도 간 인터페이스</span>, 신호 루프 센서 및 <span class="term-highlight" onclick="openGlossary('stray_current')">누설전류(Stray Current) 부식 방지 디오드 접지선</span> 매설 계획 의결</p>
                <p><strong>📑 주요 산출물:</strong> <span class="term-highlight" onclick="openGlossary('bigroom')">빅룸 회의록</span>, 인터페이스 대장</p>
            </div>
        </div>

        <!-- 2. 정량적 인터페이스 기술 규격 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 궤도-타분야 정량적 인터페이스 의결 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">기술 검속 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">의결 및 검사 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">핵심 정량 기술 수칙 및 허용 공차</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">노반 Handover 허용공차</td>
                            <td class="p-3 border text-center">기하 선형 광학 검측</td>
                            <td class="p-3 border font-semibold text-slate-700">• 노반 인도 구간 종단 및 횡단 레벨 오차 편차 ±10mm 이하 검증 완료 후 인수 의결</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">누설전류 부식방지 접지</td>
                            <td class="p-3 border text-center">접지 동선 저항 측정</td>
                            <td class="p-3 border font-semibold text-slate-700">• 매설용 접지 동선 단면적 및 저항 사양 준수. 귀선전류 바이패스용 다이오드(Diode) 매설 피치 계획 승인</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">신호 루프센서 포설</td>
                            <td class="p-3 border text-center"><span class="term-highlight" onclick="openGlossary('loop_sensor')">신호 루프 센서</span> 도통 시험</td>
                            <td class="p-3 border font-semibold text-slate-700">• 도상 콘크리트 타설 전 매설되는 감지선로 도통 저항 수치 사전 확약 및 매설 깊이 공차 규격 검증</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 빅룸회의 참석 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 본사-현장-협력사 빅룸(Big Room) 협의체 구성도
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 220" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="220" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    
                    <!-- Main Owner Box -->
                    <rect x="360" y="20" width="180" height="40" rx="8" fill="#1e3a8a" stroke="#1e3a8a" stroke-width="1"/>
                    <text x="450" y="45" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">회의 주관: 현장소장</text>
                    
                    <!-- Connector lines -->
                    <path d="M 450 60 L 450 110" stroke="#475569" stroke-width="1.5" stroke-dasharray="4"/>
                    <path d="M 170 110 L 730 110" stroke="#475569" stroke-width="1.5"/>
                    <path d="M 170 110 L 170 130" stroke="#475569" stroke-width="1.5"/>
                    <path d="M 450 110 L 450 130" stroke="#475569" stroke-width="1.5"/>
                    <path d="M 730 110 L 730 130" stroke="#475569" stroke-width="1.5"/>

                    <!-- Left: Head Office Support -->
                    <rect x="70" y="130" width="200" height="60" rx="8" fill="#ffffff" stroke="#475569" stroke-width="2"/>
                    <rect x="70" y="130" width="200" height="22" rx="8" fill="#f1f5f9"/>
                    <text x="170" y="146" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">본사 지원 담당팀</text>
                    <text x="80" y="168" font-size="10" fill="#475569">• 견적 / 설계 / 품질 / 안전 Part</text>
                    <text x="80" y="182" font-size="10" fill="#475569">• 수행(공정) 관리 의사결정 지원</text>

                    <!-- Middle: Field Control -->
                    <rect x="350" y="130" width="200" height="60" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                    <rect x="350" y="130" width="200" height="22" rx="8" fill="#ffedd5"/>
                    <text x="450" y="146" text-anchor="middle" font-size="11" font-weight="bold" fill="#9a3412">현장 관리 조직</text>
                    <text x="360" y="168" font-size="10" fill="#475569">• 공무 / 공사 / 품질 / 안전 담당</text>
                    <text x="360" y="182" font-size="10" fill="#475569">• 노선 Handover 시기 종합 조정</text>

                    <!-- Right: Partners -->
                    <rect x="630" y="130" width="200" height="60" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                    <rect x="630" y="130" width="200" height="22" rx="8" fill="#dcfce7"/>
                    <text x="730" y="146" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">협력사 파트너</text>
                    <text x="640" y="168" font-size="10" fill="#475569">• 궤도 전문공사 협력업체</text>
                    <text x="640" y="182" font-size="10" fill="#475569">• 선후행 토목 및 설비 협력업체</text>
                </svg>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-7 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs7_base, "표준서", "작수전 Big Room 회의_표준서.html"), wbs7_standard)


# =========================================================================
# 2. WRITE GUIDELINE HTML (WBS 7 - 작수전 Big Room 회의)
# =========================================================================
wbs7_guideline = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 작수전 Big Room 회의 수행지침서</title>
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
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-7 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">의사결정 프로세스</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">작수전 Big Room 회의 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"본사/현장/협력사 협의체 기반의 공정 간섭 극복 및 조달 리스크 대응 의결 가이드"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 궤도 시공 착수 전 본사, 현장, 협력사가 빅룸 협의체를 구성하여 궤도공사 종합 공정계획을 수립하고, 공종별 리스크를 해지함</p>
                <p><strong>⚙️ 세부 방법:</strong> 자재 반입로/반입구 일정 확보, 노선 인도시기별 시공계획 수립, 외산 홈레일 조달 및 용접 장비/용접사 확보 의결</p>
                <p><strong>📋 최종 산출물:</strong> 빅룸 회의록, 인터페이스 대장</p>
            </div>
        </div>
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure)
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 준비 단계 (정보 분석)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">반입로 계획 수립 및 노선 Handover 시기 정밀 분석</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>궤도 자재 및 대형 장비 반입로/반입구 사용가능 시기를 분석하여 최적 반입 일정 설계</li>
                        <li>선행 토목 공정의 <span class="term-highlight" onclick="openGlossary('handover')">노선 Handover(인수인계)</span> 시점을 정밀 수집하여 궤도 착수 일정과 동기화</li>
                        <li>참석 대상 통보: 현장소장, 공무/공사/품질/안전 담당, 협력업체 및 본사 견적/설계/공정팀 합동 소집</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 수행 단계 (Big Room 합동 의결)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">타설공법 선정 및 공종별 리스크 헤지(Risk Hedge) 안 승인</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>타설방법 선정:</strong> 현장 도심지 도로 통제 등 제반 여건을 고려하여 최적의 도상 콘크리트 타설 방안 선정 의결</li>
                        <li><strong>수급 리스크 헤지:</strong> <span class="term-highlight" onclick="openGlossary('grooved_rail')">외산 홈레일</span>의 해상 물류 조달 입항 일정을 최종 확정하고, 기지 플래시버트 용접기 임대 및 전문 용접사 수급 계획 의결</li>
                        <li><strong>인터페이스 조율:</strong> 노반-궤도 간 간섭 해소, 전기 누설전류(Stray Current) 부식 방지 디오드 접지선 매설 및 신호 루프센서 포설 계획 의결</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 결과 확정 및 계약 마감 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">빅룸 회의록 공람 및 인터페이스 대장 최종 서명</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>빅룸 회의 의사록(의사결정 사항 수록)을 수립하여 본사 담당팀 및 감리단에 공식 보고</li>
                        <li>공정 간 간섭 극복 및 물리적 인계 오차 허용치를 약정한 인터페이스 대장에 상호 서명 날인하여 계약 도서 편입</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-7 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs7_base, "수행지침", "작수전 Big Room 회의_수행지침.html"), wbs7_guideline)


# =========================================================================
# 3. WRITE CHECKLIST HTML (WBS 7 - 작수전 Big Room 회의 - Master Table)
# =========================================================================
wbs7_checklist = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 작수전 Big Room 회의 리스크 체크리스트</title>
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
        <h1 class="title">작수전 Big Room 회의 리스크 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-7 | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">본사/현장/협력사 협의체 기반 공정계획 수립, 노선 Handover 및 타설계획 의결, 누설전류/신호루프 계획 수립</div>
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
                    <div style="margin-bottom: 8px;">• <strong>[반입로/계획수립]</strong> 자재 및 장비 반입로/반입구의 사용가능 시기 확인 누락으로 인한 궤도 자재 수급 지연 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[일정 조정/Handover]</strong> 선행 토목 공정의 <span class="term-highlight" onclick="openGlossary('handover')">노선 Handover</span> 일정 수립 오류에 따른 궤도 착수 지연 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[빅룸 소집/참석 누락]</strong> 본사 담당팀(설계/견적/공정/안전) 및 선후행 공종 협력사의 핵심 의사결정자 참석 누락 리스크 (<span class="term-highlight" onclick="openGlossary('bigroom')">빅룸 회의</span>)</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[타설계획/현장여건]</strong> 도심지 시공 제한 요소를 고려하지 않은 도상 타설방법 부적정 선정 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[수급 차질/용접사 확보]</strong> 해외 특수 홈레일 반입 지연 및 기지 플래시버트 장비 임대/용접사 확보 차질 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[인터페이스/누설전류]</strong> 궤도 내 <span class="term-highlight" onclick="openGlossary('stray_current')">누설전류 부식 방지 디오드 접지선</span> 매설 및 루프 코일 설치 설계 간섭 리스크</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[회의록/문서화 누락]</strong> 빅룸 합동 회의록 합의 서명 부재 및 타분야 인터페이스 대장 누락에 따른 책임 분쟁 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[신호 검증/루프 센서]</strong> 도상 타설 후 <span class="term-highlight" onclick="openGlossary('loop_sensor')">신호 루프 센서</span> 단선 발생 및 기능 결함 검증 누락 리스크</div>
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

force_write(os.path.join(wbs7_base, "체크리스트", "작수전 Big Room 회의_체크리스트.html"), wbs7_checklist)


# =========================================================================
# 4. COPIER AUTOMATION FOR PREFIXED FILES (WBS 7 Only)
# =========================================================================
print("\n🔄 Running fast copier to sync prefixed files for WBS 7...")
shutil.copy(os.path.join(wbs7_base, "표준서", "작수전 Big Room 회의_표준서.html"), os.path.join(wbs7_base, "표준서", "7_작수전 Big Room 회의_표준서.html"))
shutil.copy(os.path.join(wbs7_base, "수행지침", "작수전 Big Room 회의_수행지침.html"), os.path.join(wbs7_base, "수행지침", "7_작수전 Big Room 회의_수행지침.html"))
shutil.copy(os.path.join(wbs7_base, "체크리스트", "작수전 Big Room 회의_체크리스트.html"), os.path.join(wbs7_base, "체크리스트", "7_작수전 Big Room 회의_체크리스트.html"))

print("💾 Synced WBS 7 Prefixed copies successfully.")
print("\n🎉 SUCCESSFULLY COMPLETED ALL WBS 7 FILE MIGRATIONS AND KICK-OFF DISK HEDGE REFLECTIONS!")
