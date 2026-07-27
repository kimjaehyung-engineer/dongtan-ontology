import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야\9_착수 전 Big Room 회의"

std_dir = os.path.join(base_dir, "표준서")
gui_dir = os.path.join(base_dir, "수행지침")
chk_dir = os.path.join(base_dir, "체크리스트")

for d in [std_dir, gui_dir, chk_dir]:
    os.makedirs(d, exist_ok=True)

modal_style = """
    .clickable-diagram {
        cursor: zoom-in !important;
        transition: all 0.25s ease !important;
        position: relative !important;
    }
    .clickable-diagram:hover {
        transform: scale(1.015) !important;
        box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important;
    }
    .zoom-modal, .glossary-modal {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(6px);
        align-items: center;
        justify-content: center;
    }
    .zoom-modal.active, .glossary-modal.active {
        display: flex;
    }
    .zoom-modal-content {
        background-color: #ffffff;
        margin: auto;
        padding: 28px;
        border: 1px solid #cbd5e1;
        width: 95%;
        max-width: 1100px;
        max-height: 90vh;
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        position: relative;
        overflow-y: auto;
        text-align: center;
    }
    .glossary-modal-content {
        background-color: #ffffff;
        margin: auto;
        padding: 24px;
        border: 1px solid #e2e8f0;
        width: 90%;
        max-width: 580px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        position: relative;
        text-align: left;
    }
    .zoom-close, .glossary-close {
        color: #64748b;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 32px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.2s;
    }
    .zoom-close:hover, .glossary-close:hover {
        color: #ef4444;
    }
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
"""

common_js = """
<div class="glossary-modal" id="glossaryModal" onclick="closeGlossaryModalOutside(event)">
    <div class="glossary-modal-content" onclick="event.stopPropagation()">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 착수 회의 기술 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; color: #0f172a; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 도식 대형 고화질 정밀 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
        <div style="margin-top: 14px; text-align: right; font-size: 0.85rem; font-weight: 700; color: #64748b;">
            💡 팁: ESC 키를 누르시거나 닫기(×) 버튼을 누르면 이전 화면으로 복귀합니다.
        </div>
    </div>
</div>

<script>
const glossaryData = {
    "interface_check": "<b>5대 공종 간섭검토 (Interface Control)</b><br><br>• 노반(궤도), 전기, 신호, 기계, 차량 등 5대 이종 공종과 통신 설비 간 관통 관로, 층고, 양중 공간 및 전파 간섭 지점을 사전에 도출하고 조율하는 절차입니다.",
    "defect_prevention": "<b>타 프로젝트 하자 재발방지 (Defect Prevention)</b><br><br>• 과거 유사 철도/트램 프로젝트에서 발생했던 광케이블 접속 손실, 침수, 방화 충전 불량 등의 하자 사례를 분석하여 현장에 재발 방지 대책을 수립하는 수칙입니다.",
    "risk_hedge": "<b>공종별 Risk Hedge 방안</b><br><br>• 궤도 선로 작업 안전, 고소작업 낙하, 광 접속 품질 하자 및 도로 굴착 소음/진동 민원(2시간 이내 출동)에 대해 사전에 수립하는 종합 리스크 예방 대책입니다."
};

function openGlossary(term) {
    const modal = document.getElementById('glossaryModal');
    const titleEl = document.getElementById('modalTitle');
    const descEl = document.getElementById('modalDescription');
    
    if (glossaryData[term]) {
        titleEl.innerHTML = "📖 용어 해설: " + term;
        descEl.innerHTML = glossaryData[term];
        modal.classList.add('active');
    }
}

function closeGlossaryModal() {
    document.getElementById('glossaryModal').classList.remove('active');
}

function closeGlossaryModalOutside(event) {
    if (event.target.id === 'glossaryModal') {
        closeGlossaryModal();
    }
}

function openDiagramZoom(elementId, titleText) {
    const srcEl = document.getElementById(elementId);
    if (!srcEl) return;
    
    const zoomBody = document.getElementById('zoomBody');
    document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "도식 대형 정밀 보기");
    
    zoomBody.innerHTML = srcEl.outerHTML;
    
    const innerSvg = zoomBody.querySelector('svg');
    if (innerSvg) {
        innerSvg.setAttribute('width', '100%');
        innerSvg.setAttribute('height', '550px');
        innerSvg.style.maxWidth = '1050px';
    }
    
    document.getElementById('zoomModal').classList.add('active');
}

function closeZoomModal() {
    document.getElementById('zoomModal').classList.remove('active');
}

function closeZoomModalOutside(event) {
    if (event.target.id === 'zoomModal') {
        closeZoomModal();
    }
}

window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeZoomModal();
        closeGlossaryModal();
    }
});
</script>
"""

# 1. Standard HTML Template (Enriched with 8 Core Agendas)
std_html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 착수 전 Big Room 회의 표준서 (WBS 9000-2-9)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {modal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Standard (WBS 9000-2-9)</span>
        <h1 class="text-3xl font-black mt-2">착수 전 Big Room 회의 마스터 표준서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-9 | 주관: 현장소장 | "8대 착수 회의 의제 및 Risk Hedge 표준 규정"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 표준 개요 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-sm text-blue-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 본 표준서의 개요 및 8대 착수 회의 심사 표준</h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                본 표준서는 건설기술 진흥법, KCS 47 10 00, KDS 47 10 00 시방서에 의거하여, 통신공사 착수 전 본사·현장·협력사 3자 Big Room 협의체를 구축하고 <strong><span class="term-highlight" onclick="openGlossary('interface_check')">5대 공종 간섭(노반/전기/신호/기계/차량)</span></strong>, 자재 반입구 및 야적장 5대 환경, 성능보증, <span class="term-highlight" onclick="openGlossary('defect_prevention')">타 프로젝트 하자 재발방지</span>, 양중장비 안전검사 및 <span class="term-highlight" onclick="openGlossary('risk_hedge')">안전/품질/민원 Risk Hedge</span> 대책을 사전에 검증·확정하는 기술 표준입니다.
            </p>
        </div>

        <!-- 📜 8대 착수전 회의 심사 의제 규정 -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-blue-600 pb-2">1. 착수 전 Big Room 회의 8대 핵심 심사 규정</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">🤝 1. 본사/현장/협력사 협의체 구축</span>
                    <p class="text-slate-700 text-xs">현장소장 주관 3자 합동 Big Room 협의체를 구축하고 착수 세부 실행계획 1:1 대조 검토.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">📐 2. 5대 공종 간섭 사항 사전 검토</span>
                    <p class="text-slate-700 text-xs">노반(궤도)/전기/신호/기계/차량 인터페이스 및 관통 경로, 층고(≥3.0m) 간섭점 사전 검출.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">📦 3. 자재 반입동선 & 야적장/공장</span>
                    <p class="text-slate-700 text-xs">통신 랙(H=2200mm) 반입구, 야적장 5대 안전 환경 및 제작사 공장검사 계획 확인.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">💎 4. 자재 성능보증 & 유사실적 대조</span>
                    <p class="text-slate-700 text-xs">광케이블, CCTV, PIS 등 자재 성능보증 조건 및 타 철도/트램 적용 실적 사전 검증.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">🛡️ 5. 타 프로젝트 하자 재발방지</span>
                    <p class="text-slate-700 text-xs">과거 철도/트램 하자 사례(광손실, 침수, 방화충전) 분석 및 현장 재발 방지 대책 수립.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">🏗️ 6. 인원/자재/장비 & 양중 운영</span>
                    <p class="text-slate-700 text-xs">숙련 기술자 자격증, 계측기(KOLAS 1년 검교정), 크레인/양중장비 안전 운영 계획 검토.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">⚡ 7. 장비 안전검사 기준 공유</span>
                    <p class="text-slate-700 text-xs">당사 현장 장비 안전검사 기준 공유 및 양중/고소 작업 장비 검사 필증 사전 확인.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-800 flex items-center gap-2">🚧 8. 공종별 Risk Hedge 방안 검토</span>
                    <p class="text-slate-700 text-xs">안전/품질 Risk(궤도/고소작업/광접속) 및 도로 굴착 소음/진동 민원 2시간 출동 헷지 수칙 확정.</p>
                </div>
            </div>
        </div>
    </div>
</div>
{common_js}
</body>
</html>
"""

# 2. Guideline HTML Template (8 Core Agendas & 1:1 Step 1~5 SVG Diagrams)
gui_html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 착수 전 Big Room 회의 수행지침서 (WBS 9000-2-9)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {modal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Detailed Guideline (WBS 9000-2-9)</span>
        <h1 class="text-3xl font-black mt-2">착수 전 Big Room 회의 초정밀 실무 수행지침서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-9 | 주관: 현장소장 | "8대 실무 의제 & 1:1 STEP 2D 그림 수록 가이드"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 개념 해설 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-sm text-blue-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 8대 착수 회의 의제 및 Risk Hedge 현장 실무 개요</h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                본 지침서는 본사/현장/협력사 3자 Big Room 회의를 통해 <strong><span class="term-highlight" onclick="openGlossary('interface_check')">5대 공종 간섭(노반/전기/신호/기계/차량)</span></strong>, 자재 반입동선, <span class="term-highlight" onclick="openGlossary('defect_prevention')">하자 재발방지</span>, 양중장비 안전검사 및 <span class="term-highlight" onclick="openGlossary('risk_hedge')">안전/품질/민원 24H Risk Hedge</span> 대책을 5단계 마스터 절차로 완수할 수 있도록 **1:1 2D Visual SVG 도식 및 팝업 확대 기능**을 수록하였습니다.
            </p>
        </div>

        <!-- ☀️ 5단계 수행 마스터 프로세스 -->
        <div class="bg-blue-50/70 border border-blue-200 p-7 rounded-2xl shadow-md space-y-6">
            <div class="border-b border-blue-200 pb-4">
                <span class="bg-blue-600 text-white text-xs font-black px-3 py-1 rounded-full uppercase">FLEXIBLE 5-STEP ARCHITECTURE</span>
                <h3 class="text-xl font-black text-blue-950 mt-2">📋 8대 의제 반영 착수 회의 5단계 실무 프로세스</h3>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2 text-xs">
                <div class="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
                    <span class="bg-blue-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">STEP 1</span>
                    <h4 class="font-bold text-slate-900 text-xs">협의체 & 5대간섭</h4>
                    <p class="text-[10px] text-slate-600">• 3자 협의체 구축<br">• 5대 공종 간섭 검출</p>
                </div>
                <div class="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
                    <span class="bg-indigo-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-xs">반입동선 & 야적장</h4>
                    <p class="text-[10px] text-slate-600">• 반입구/층고 실측<br">• 야적장 5대 환경</p>
                </div>
                <div class="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
                    <span class="bg-cyan-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-xs">성능보증 & 하자예방</h4>
                    <p class="text-[10px] text-slate-600">• 유사 실적 대조<br">• 타 현장 하자 재발방지</p>
                </div>
                <div class="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
                    <span class="bg-teal-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-xs">자원 & 양중장비안전</h4>
                    <p class="text-[10px] text-slate-600">• 숙련 통신공/계측기<br">• 당사 장비안전검사</p>
                </div>
                <div class="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
                    <span class="bg-emerald-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">STEP 5</span>
                    <h4 class="font-bold text-slate-900 text-xs">Risk Hedge & 서명</h4>
                    <p class="text-[10px] text-slate-600">• 24H 민원/안전 헷지<br">• 회의록 확정 체결</p>
                </div>
            </div>
        </div>

        <!-- 🔥 8대 의제 상세 가이드 & 1:1 2D Visual SVG -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-indigo-600 pb-2">8대 회 의제 상세 실무 지침 & 1:1 직관적 2D 그림</h2>

            <!-- STEP 1 Card -->
            <div class="bg-white p-6 rounded-2xl border border-blue-200 shadow-sm space-y-4">
                <div class="flex items-center gap-3">
                    <span class="bg-blue-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 1</span>
                    <h3 class="font-bold text-base text-slate-900">본사/현장/협력사 협의체 구축 & <span class="term-highlight" onclick="openGlossary('interface_check')">5대 공종 간섭</span> 사전 검토</h3>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl text-xs text-slate-700 space-y-2 leading-relaxed">
                    <p>• <strong>3자 합동 협의체:</strong> 현장소장 주관으로 본사, 현장, 협력사 3자 Big Room 협의체를 결성하고 착수 세부 실행계획을 대조합니다.</p>
                    <p>• <strong>5대 공종 인터페이스:</strong> 노반(궤도), 전기, 신호, 기계, 차량 등 5대 이종 공종과 통신 관통 슬리브(ø100~ø150mm) 좌표 오차(±10mm 이내) 및 관로 경로 간섭점을 사전 검출합니다.</p>
                </div>

                <!-- 1:1 STEP 1 2D SVG -->
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3" onclick="openDiagramZoom('svg_step1_agenda', 'STEP 1 3자 협의체 구축 및 5대 공종 간섭 검토 2D 도식')">
                    <svg id="svg_step1_agenda" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                        <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                        <text x="130" y="50" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">🤝 3자 Big Room 협의체</text>
                        <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 본사/현장/협력사 3자 결성</text>
                        <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• 착수 세부 실행계획 대조</text>
                        <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 실행계획 대조 완료</text>

                        <path d="M 245 90 L 285 90" stroke="#2563eb" stroke-width="3"/>
                        <polygon points="285,85 295,90 285,95" fill="#2563eb"/>

                        <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                        <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">📐 5대 공종 간섭 검출</text>
                        <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 궤도/전기/신호/기계/차량</text>
                        <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• 관통 슬리브 좌표 오차 ±10mm</text>
                        <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 간섭점 사전 해결</text>
                    </svg>
                </div>
            </div>

            <!-- STEP 2 Card -->
            <div class="bg-white p-6 rounded-2xl border border-indigo-200 shadow-sm space-y-4">
                <div class="flex items-center gap-3">
                    <span class="bg-indigo-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 2</span>
                    <h3 class="font-bold text-base text-slate-900">자재 반입동선, 개구부 규격 및 자재 야적장/공장 검토</h3>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl text-xs text-slate-700 space-y-2 leading-relaxed">
                    <p>• <strong>기능실 층고 & 반입 동선:</strong> 통신기계실/관제실 마감 층고(≥3.0m) 및 통신 랙(H=2200mm) 반입 엘리베이터(유효폭 1.5m×2.1m) 통과 여부를 1:1 실측합니다.</p>
                    <p>• <strong>야적장 & 제작사 공장검사:</strong> 지면 이격 팔레트(10cm), 방수/방염 덮개, 잠금 펜스, CCTV 24시간 야적장 5대 환경 및 제작사 공장검사 일정 사전 승인.</p>
                </div>

                <!-- 1:1 STEP 2 2D SVG -->
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3" onclick="openDiagramZoom('svg_step2_agenda', 'STEP 2 반입동선 층고 실측 및 야적장 5대 환경 2D 도식')">
                    <svg id="svg_step2_agenda" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                        <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="8"/>
                        <text x="130" y="50" font-size="13" font-weight="black" fill="#3730a3" text-anchor="middle">📏 층고 실측 & EV 반입동선</text>
                        <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 기능실 마감 층고 ≥ 3.0m</text>
                        <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• 랙(H=2200mm) EV 1.5×2.1m 통과</text>
                        <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 반입동선 검측 합격</text>

                        <path d="M 245 90 L 285 90" stroke="#4f46e5" stroke-width="3"/>
                        <polygon points="285,85 295,90 285,95" fill="#4f46e5"/>

                        <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                        <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">⛺ 야적장 5대 환경 & 공장검사</text>
                        <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 지면이격 팔레트+방수/방염천막</text>
                        <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• 제작사 공장 사전검사 승인</text>
                        <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 야적장 환경 승인</text>
                    </svg>
                </div>
            </div>

            <!-- STEP 3 Card -->
            <div class="bg-white p-6 rounded-2xl border border-cyan-200 shadow-sm space-y-4">
                <div class="flex items-center gap-3">
                    <span class="bg-cyan-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 3</span>
                    <h3 class="font-bold text-base text-slate-900">통신자재 성능보증 조건 & <span class="term-highlight" onclick="openGlossary('defect_prevention')">타 프로젝트 하자 재발방지</span></h3>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl text-xs text-slate-700 space-y-2 leading-relaxed">
                    <p>• <strong>성능보증 & 실적 대조:</strong> 광케이블, CCTV, PIS전광판 자재 성능보증서 및 타 철도/트램 프로젝트 실제 적용 실적을 사전 대조합니다.</p>
                    <p>• <strong>하자 재발방지 수칙:</strong> 과거 타 현장 광 접속 손실 초과, 침수 및 내화 씰링 미비 하자 사례를 사전 분석하여 현장 예방 방안을 수립합니다.</p>
                </div>

                <!-- 1:1 STEP 3 2D SVG -->
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3" onclick="openDiagramZoom('svg_step3_agenda', 'STEP 3 성능보증 실적 대조 및 하자 재발방지 2D 도식')">
                    <svg id="svg_step3_agenda" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                        <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#0891b2" stroke-width="2" rx="8"/>
                        <text x="130" y="50" font-size="13" font-weight="black" fill="#0e7490" text-anchor="middle">💎 자재 성능보증 & 실적대조</text>
                        <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 광케이블/CCTV 성능보증확인</text>
                        <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• 타 트램 프로젝트 실적 대조</text>
                        <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 자재 품질 검증 통과</text>

                        <path d="M 245 90 L 285 90" stroke="#0891b2" stroke-width="3"/>
                        <polygon points="285,85 295,90 285,95" fill="#0891b2"/>

                        <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                        <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🛡️ 타 현장 하자 재발방지</text>
                        <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 과거 광손실/침수 하자 사례분석</text>
                        <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• 현장 맞춤 재발방지대책 수립</text>
                        <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 하자 Zero 대책 수립</text>
                    </svg>
                </div>
            </div>

            <!-- STEP 4 Card -->
            <div class="bg-white p-6 rounded-2xl border border-teal-200 shadow-sm space-y-4">
                <div class="flex items-center gap-3">
                    <span class="bg-teal-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 4</span>
                    <h3 class="font-bold text-base text-slate-900">자원 투입계획, 양중장비 운영 & 당사 장비 안전검사 공유</h3>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl text-xs text-slate-700 space-y-2 leading-relaxed">
                    <p>• <strong>자원 투입 & 계측기 검교정:</strong> 공정별 특급/고급 통신 기술자 투입, 광융착기 및 OTDR KOLAS 1년 유효 검교정 성적서 S/N 일치를 검증합니다.</p>
                    <p>• <strong>양중장비 안전검사 공유:</strong> 현장 크레인/고소작업차 안전검사 기준 공유, 장비 검사 필증 사전 확인 및 작업 안전수칙을 공유합니다.</p>
                </div>

                <!-- 1:1 STEP 4 2D SVG -->
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3" onclick="openDiagramZoom('svg_step4_agenda', 'STEP 4 자원 투입 및 양중장비 안전검사 기준 공유 2D 도식')">
                    <svg id="svg_step4_agenda" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                        <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#0d9488" stroke-width="2" rx="8"/>
                        <text x="130" y="50" font-size="13" font-weight="black" fill="#0f766e" text-anchor="middle">👤 자원 투입 & 계측기 검교정</text>
                        <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 고급/특급 통신 기술자 투입</text>
                        <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• OTDR/융착기 1년 검교정 S/N</text>
                        <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 자원 투입 준비 완료</text>

                        <path d="M 245 90 L 285 90" stroke="#0d9488" stroke-width="3"/>
                        <polygon points="285,85 295,90 285,95" fill="#0d9488"/>

                        <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                        <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🏗️ 양중장비 안전검사 공유</text>
                        <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 당사 장비 안전검사 기준 공유</text>
                        <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• 크레인/고소작업차 필증 확인</text>
                        <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 장비 안전검사 완료</text>
                    </svg>
                </div>
            </div>

            <!-- STEP 5 Card -->
            <div class="bg-white p-6 rounded-2xl border border-emerald-200 shadow-sm space-y-4">
                <div class="flex items-center gap-3">
                    <span class="bg-emerald-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 5</span>
                    <h3 class="font-bold text-base text-slate-900"><span class="term-highlight" onclick="openGlossary('risk_hedge')">공종별 Risk Hedge 방안</span> 수립 (안전/품질/민원대책)</h3>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl text-xs text-slate-700 space-y-2 leading-relaxed">
                    <p>• <strong>안전/품질 Risk 요소:</strong> 궤도 선로 투입 안전, 고소 작업 낙하 방지 및 Fire-Stop 내화 2시간 방화 구속 씰링 검측 대책을 확정합니다.</p>
                    <p>• <strong>민원 대응 24H 헷지:</strong> 도로 굴착 소음/진동 민원 접수 시 전담 신호수 2인 배치 및 2시간 이내 현장 출동 헷지 수칙을 Big Room 회의록에 수록·체결합니다.</p>
                </div>

                <!-- 1:1 STEP 5 2D SVG -->
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3" onclick="openDiagramZoom('svg_step5_agenda', 'STEP 5 공종별 Risk Hedge 방안 수립 및 회의록 체결 2D 도식')">
                    <svg id="svg_step5_agenda" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                        <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                        <text x="130" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🚧 안전 & 품질 Risk Hedge</text>
                        <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 궤도/고소작업 안전 대책</text>
                        <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• Fire-Stop 내화 2시간 씰링 확정</text>
                        <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 현장 리스크 사전 차단</text>

                        <path d="M 245 90 L 285 90" stroke="#059669" stroke-width="3"/>
                        <polygon points="285,85 295,90 285,95" fill="#059669"/>

                        <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                        <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🛡️ 24H 민원 헷지 & 서명 체결</text>
                        <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 민원 시 2시간 출동 헷지 수칙</text>
                        <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• Big Room 회의록 3자 서명 체결</text>
                        <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 착수 회의 최종 승인</text>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</div>
{common_js}
</body>
</html>
"""

# 3. Checklist HTML Template (3-Column Master & ~하였는가? 100% Phrasing for 8 Core Agendas)
chk_html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 착수 전 Big Room 회의 마스터 체크리스트 (WBS 9000-2-9)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {modal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- 🔵 헤더 영역 -->
    <div class="bg-white p-6 sm:p-8 border-b border-slate-200">
        <div class="flex justify-between items-start">
            <div>
                <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">착수 전 Big Room 회의 마스터 체크리스트</h1>
            </div>
            <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200">WBS Code 9000-2-9 | 통신 검측대장</span>
        </div>
        <div class="w-full h-1 bg-slate-900 mt-4"></div>
    </div>

    <div class="p-6 sm:p-8 space-y-8">
        <!-- 📋 안내 상자 -->
        <div class="bg-blue-50/70 border border-blue-200 p-6 rounded-2xl text-xs sm:text-sm text-blue-950 space-y-2">
            <h4 class="font-bold text-sm sm:text-base text-blue-900 flex items-center gap-2">📋 쉽게 풀어쓴 현장 점검 체크리스트 (8대 착수 회의 의제 반영)</h4>
            <p class="text-slate-700 leading-relaxed">
                본 체크리스트는 착수 전 Big Room 회의 8대 핵심 의제 및 Risk Hedge 점검 시 <strong>[🟣 시공 도식 열기]</strong>를 클릭하면 대형 고화질 팝업 모달이 열려 도식을 직접 보며 <strong>~하였는가? (100%)</strong> 점검을 진행할 수 있도록 연동되었습니다.
            </p>
        </div>

        <!-- 3-COLUMN MASTER TABLE -->
        <div class="overflow-x-auto rounded-2xl border border-slate-200 shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-100 text-slate-700 text-xs font-black uppercase tracking-wider border-b border-slate-200">
                        <th class="py-4 px-6 text-center w-1/4">시공 단계</th>
                        <th class="py-4 px-6 text-center w-7/12">필수 검측 항목 (쉬운 질문형 수칙)</th>
                        <th class="py-4 px-6 text-center w-1/6">점검 결과</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 text-xs sm:text-sm bg-white">
                    
                    <!-- STEP 1 Row Group -->
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-6 px-6 text-center align-middle bg-slate-50/50 border-r border-slate-200" rowspan="2">
                            <div class="flex flex-col items-center gap-2">
                                <span class="text-xl">🤝</span>
                                <span class="font-bold text-slate-900 text-sm">협의체 & 5대간섭</span>
                                <span class="text-xs text-slate-500 font-medium">(Step 1 인터페이스)</span>
                                <button onclick="openDiagramZoomByKey('step1', 'STEP 1 3자 협의체 구축 및 5대 공종 간섭검토 도식')" class="mt-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-full shadow-sm transition-all">
                                    🟣 시공 도식 열기
                                </button>
                            </div>
                        </td>
                        <td class="py-4 px-6">
                            <div class="flex items-start gap-2">
                                <span class="bg-blue-100 text-blue-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">1. 협의체 구축</span>
                                <p class="text-slate-800 font-medium"><strong>[Big Room 체계]</strong> 본사/현장/협력사 3자 Big Room 협의체를 구축하고 착수 세부 실행계획을 대조하였는가?</p>
                            </div>
                        </td>
                        <td class="py-4 px-6 text-center align-middle font-bold text-blue-600" rowspan="2">
                            ☐ 확인완료
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-4 px-6 border-t border-slate-100">
                            <div class="flex items-start gap-2">
                                <span class="bg-blue-100 text-blue-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">2. 5대 공종 간섭</span>
                                <p class="text-slate-800 font-medium"><strong>[인터페이스]</strong> 노반(궤도)/전기/신호/기계/차량 5대 공종 간 관통 경로 및 간섭점을 사전 도출 검출하였는가?</p>
                            </div>
                        </td>
                    </tr>

                    <!-- STEP 2 Row Group -->
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-6 px-6 text-center align-middle bg-slate-50/50 border-r border-slate-200" rowspan="2">
                            <div class="flex flex-col items-center gap-2">
                                <span class="text-xl">📦</span>
                                <span class="font-bold text-slate-900 text-sm">반입 & 성능보증</span>
                                <span class="text-xs text-slate-500 font-medium">(Step 2 야적/실적)</span>
                                <button onclick="openDiagramZoomByKey('step2', 'STEP 2 자재 반입동선 실측 및 성능보증 대조 도식')" class="mt-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-full shadow-sm transition-all">
                                    🟣 시공 도식 열기
                                </button>
                            </div>
                        </td>
                        <td class="py-4 px-6 border-t border-slate-200">
                            <div class="flex items-start gap-2">
                                <span class="bg-indigo-100 text-indigo-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">3. 반입동선 & 야적</span>
                                <p class="text-slate-800 font-medium"><strong>[자재 동선]</strong> 통신 자재 반입구, 야적장 5대 안전 환경 및 제작사 공장검사 계획을 사전 확인하였는가?</p>
                            </div>
                        </td>
                        <td class="py-4 px-6 text-center align-middle font-bold text-blue-600" rowspan="2">
                            ☐ 확인완료
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-4 px-6 border-t border-slate-100">
                            <div class="flex items-start gap-2">
                                <span class="bg-indigo-100 text-indigo-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">4. 성능보증 & 실적</span>
                                <p class="text-slate-800 font-medium"><strong>[품질 실적]</strong> 통신 자재 성능보증 조건 및 타 트램 프로젝트 유사 적용 실적을 사전 검증 대조하였는가?</p>
                            </div>
                        </td>
                    </tr>

                    <!-- STEP 3 Row Group -->
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-6 px-6 text-center align-middle bg-slate-50/50 border-r border-slate-200" rowspan="2">
                            <div class="flex flex-col items-center gap-2">
                                <span class="text-xl">🛡️</span>
                                <span class="font-bold text-slate-900 text-sm">하자예방 & 양중장비</span>
                                <span class="text-xs text-slate-500 font-medium">(Step 3 재발방지)</span>
                                <button onclick="openDiagramZoomByKey('step3', 'STEP 3 타 현장 하자 재발방지 및 양중장비 안전 도식')" class="mt-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-full shadow-sm transition-all">
                                    🟣 시공 도식 열기
                                </button>
                            </div>
                        </td>
                        <td class="py-4 px-6 border-t border-slate-200">
                            <div class="flex items-start gap-2">
                                <span class="bg-cyan-100 text-cyan-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">5. 하자예방 대책</span>
                                <p class="text-slate-800 font-medium"><strong>[재발 방지]</strong> 타 프로젝트 하자 사례(광손실, 침수)를 분석하여 현장 재발 방지 대책을 수립하였는가?</p>
                            </div>
                        </td>
                        <td class="py-4 px-6 text-center align-middle font-bold text-blue-600" rowspan="2">
                            ☐ 확인완료
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-4 px-6 border-t border-slate-100">
                            <div class="flex items-start gap-2">
                                <span class="bg-cyan-100 text-cyan-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">6. 양중장비 안전</span>
                                <p class="text-slate-800 font-medium"><strong>[장비 안전]</strong> 크레인/양중장비 투입 계획 및 당사 장비 안전검사 기준 공유를 확인하였는가?</p>
                            </div>
                        </td>
                    </tr>

                    <!-- STEP 4 Row Group -->
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-6 px-6 text-center align-middle bg-slate-50/50 border-r border-slate-200" rowspan="2">
                            <div class="flex flex-col items-center gap-2">
                                <span class="text-xl">🚧</span>
                                <span class="font-bold text-slate-900 text-sm">Risk Hedge & 체결</span>
                                <span class="text-xs text-slate-500 font-medium">(Step 4 회의록 서명)</span>
                                <button onclick="openDiagramZoomByKey('step3', 'STEP 4 24시간 Risk Hedge 및 Big Room 회의록 서명 체결 도식')" class="mt-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-full shadow-sm transition-all">
                                    🟣 시공 도식 열기
                                </button>
                            </div>
                        </td>
                        <td class="py-4 px-6 border-t border-slate-200">
                            <div class="flex items-start gap-2">
                                <span class="bg-emerald-100 text-emerald-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">7. 안전/품질 Risk</span>
                                <p class="text-slate-800 font-medium"><strong>[안전 품질]</strong> 궤도 선로 투입 및 고소작업 낙하 방지 안전/품질 Risk 예방 대책을 확정하였는가?</p>
                            </div>
                        </td>
                        <td class="py-4 px-6 text-center align-middle font-bold text-blue-600" rowspan="2">
                            ☐ 확인완료
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-4 px-6 border-t border-slate-100">
                            <div class="flex items-start gap-2">
                                <span class="bg-emerald-100 text-emerald-800 text-[11px] font-bold px-2 py-0.5 rounded shrink-0">8. 민원 대응 헷지</span>
                                <p class="text-slate-800 font-medium"><strong>[민원 헷지]</strong> 도로 굴착 소음/진동 민원 발생 시 2시간 이내 출동 헷지 대책을 수립하고 회의록에 확정 체결하였는가?</p>
                            </div>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>
    </div>
</div>

<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; color: #0f172a; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 도식 대형 고화질 정밀 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
        <div style="margin-top: 14px; text-align: right; font-size: 0.85rem; font-weight: 700; color: #64748b;">
            💡 팁: ESC 키를 누르시거나 닫기(×) 버튼을 누르면 이전 화면으로 복귀합니다.
        </div>
    </div>
</div>

<script>
const svgStore = {{
    'step1': `<svg viewBox="0 0 520 180" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                <text x="130" y="50" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">🤝 3자 Big Room 협의체</text>
                <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 본사/현장/협력사 3자 결성</text>
                <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• 착수 세부 실행계획 대조</text>
                <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 실행계획 대조 완료</text>
                <path d="M 245 90 L 285 90" stroke="#2563eb" stroke-width="3"/>
                <polygon points="285,85 295,90 285,95" fill="#2563eb"/>
                <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">📐 5대 공종 간섭 검출</text>
                <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 궤도/전기/신호/기계/차량</text>
                <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• 관통 슬리브 좌표 오차 ±10mm</text>
                <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 간섭점 사전 해결</text>
            </svg>`,
    'step2': `<svg viewBox="0 0 520 180" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="8"/>
                <text x="130" y="50" font-size="13" font-weight="black" fill="#3730a3" text-anchor="middle">📏 층고 실측 & EV 반입동선</text>
                <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 기능실 마감 층고 ≥ 3.0m</text>
                <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• 랙(H=2200mm) EV 1.5×2.1m 통과</text>
                <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 반입동선 검측 합격</text>
                <path d="M 245 90 L 285 90" stroke="#4f46e5" stroke-width="3"/>
                <polygon points="285,85 295,90 285,95" fill="#4f46e5"/>
                <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">⛺ 야적장 5대 환경 & 공장검사</text>
                <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 지면이격 팔레트+방수/방염천막</text>
                <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• 제작사 공장 사전검사 승인</text>
                <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 야적장 환경 승인</text>
            </svg>`,
    'step3': `<svg viewBox="0 0 520 180" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                <rect x="20" y="25" width="220" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                <text x="130" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🚧 안전 & 품질 Risk Hedge</text>
                <text x="35" y="78" font-size="11" font-weight="bold" fill="#334155">• 궤도/고소작업 안전 대책</text>
                <text x="35" y="100" font-size="11" font-weight="bold" fill="#334155">• Fire-Stop 내화 2시간 씰링 확정</text>
                <text x="130" y="132" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 현장 리스크 사전 차단</text>
                <path d="M 245 90 L 285 90" stroke="#059669" stroke-width="3"/>
                <polygon points="285,85 295,90 285,95" fill="#059669"/>
                <rect x="300" y="25" width="200" height="130" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                <text x="400" y="50" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🛡️ 24H 민원 헷지 & 서명 체결</text>
                <text x="315" y="78" font-size="11" font-weight="bold" fill="#334155">• 민원 시 2시간 출동 헷지 수칙</text>
                <text x="315" y="100" font-size="11" font-weight="bold" fill="#334155">• Big Room 회의록 3자 서명 체결</text>
                <text x="400" y="132" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">✔ 착수 회의 최종 승인</text>
            </svg>`
}};

function openDiagramZoomByKey(stepKey, titleText) {{
    const zoomBody = document.getElementById('zoomBody');
    document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "시공 도식 대형 정밀 보기");
    
    if (svgStore[stepKey]) {{
        zoomBody.innerHTML = svgStore[stepKey];
    }}
    
    document.getElementById('zoomModal').classList.add('active');
}}

function closeZoomModal() {{
    document.getElementById('zoomModal').classList.remove('active');
}}

function closeZoomModalOutside(event) {{
    if (event.target.id === 'zoomModal') {{
        closeZoomModal();
    }}
}}

window.addEventListener('keydown', function(event) {{
    if (event.key === 'Escape') {{
        closeZoomModal();
    }}
}});
</script>
</body>
</html>
"""

# Write HTML Files
files_to_write = [
    (os.path.join(std_dir, "9000-2-9_착수 전 Big Room 회의_표준서.html"), std_html_content),
    (os.path.join(std_dir, "착수 전 Big Room 회의_표준서.html"), std_html_content),
    (os.path.join(gui_dir, "9000-2-9_착수 전 Big Room 회의_수행지침.html"), gui_html_content),
    (os.path.join(gui_dir, "착수 전 Big Room 회의_수행지침.html"), gui_html_content),
    (os.path.join(chk_dir, "9000-2-9_착수 전 Big Room 회의_체크리스트.html"), chk_html_content),
    (os.path.join(chk_dir, "착수 전 Big Room 회의_체크리스트.html"), chk_html_content)
]

for path, content in files_to_write:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ [8-AGENDA MASTER HTML BUILT] -> {os.path.basename(path)}")

print("\n🎉 SUCCESSFULLY REBUILT ALL WBS 9000-2-9 HTMLs BASED ON REAL 8 CORE MEETING AGENDAS & RISK HEDGE FRAMEWORK!")
