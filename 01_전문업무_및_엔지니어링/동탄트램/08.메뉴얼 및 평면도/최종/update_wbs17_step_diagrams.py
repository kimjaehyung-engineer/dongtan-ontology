import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\17_[TCL] 궤광 및 철근 조립"

path_gui = os.path.join(target_base, "수행지침", "[TCL] 궤광 및 철근 조립_수행지침.html")
path_gui_alt = os.path.join(target_base, "수행지침", "17_[TCL] 궤광 및 철근 조립_수행지침.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully updated WBS 17 Guideline with Step Diagrams: {path}")

zoom_modal_style = """
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
    .clickable-diagram {
        cursor: zoom-in !important;
        transition: all 0.25s ease !important;
        position: relative !important;
    }
    .clickable-diagram:hover {
        transform: scale(1.015) !important;
        box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important;
    }
    .clickable-diagram::after {
        content: "🔍 클릭하여 대형 확대보기";
        position: absolute;
        bottom: 8px;
        right: 12px;
        background: rgba(15, 23, 42, 0.75);
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
        pointer-events: none;
        opacity: 0.85;
        transition: opacity 0.2s;
    }
    .clickable-diagram:hover::after {
        opacity: 1;
        background: rgba(2, 132, 199, 0.9);
    }
    .glossary-modal, .zoom-modal {
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
    .glossary-modal.active, .zoom-modal.active {
        display: flex;
    }
    .glossary-modal-content {
        background-color: #ffffff;
        margin: auto;
        padding: 24px;
        border: 1px solid #e2e8f0;
        width: 90%;
        max-width: 550px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        position: relative;
        text-align: left;
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
    .glossary-close, .zoom-close {
        color: #64748b;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 32px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.2s;
    }
    .glossary-close:hover, .zoom-close:hover {
        color: #ef4444;
    }
"""

common_modal_html = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 공학 기술 해설</h3>
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
    'tie_bar': {
        title: '📏 1,435mm 타이바 (Tie Bar) 정원 고정',
        desc: '열차 주행 시 궤간의 확폭이나 변위를 방지하기 위해 1,435mm 표준궤 정원을 고정 유지해주는 레일 간 정밀 결속 조임 락 장치입니다.'
    },
    'rebar_cover': {
        title: '🛡️ 철근 피복 두께 (≥ 40mm) & 처짐 방지',
        desc: '콘크리트 도상(TCL) 내 철근의 부식 방지 및 내구성 확보를 위해 하부 콘크리트와의 최소 피복 두께 40mm 이상을 확보하고, 2m 간격 배근 시 처짐이 없도록 용접/결속하는 공학 규격입니다.'
    },
    'signal_clearance': {
        title: '📡 신호 감선 & 루프 케이블 이격 (≥ 150mm)',
        desc: '트램 신호 제어용 루프 케이블 배근 시 철근이나 금속 구조체와의 전자파 간섭 및 전자기 감쇄를 방지하기 위해 최소 150mm 이상의 안전 이격 거리를 유지하는 수칙입니다.'
    },
    'alignment_tolerance': {
        title: '📐 궤도 선형 오차 (궤간 +3/-1mm, 캔트 ±2mm)',
        desc: 'CP 광학 레벨기를 이용하여 궤도 중심선 및 기준 높이를 측량하고 궤간 +3, -1mm 이내, 캔트/수평 오차 ±2mm 이내, 중심간격 오차 3mm 이내로 조율하는 정밀 공차입니다.'
    }
};

function openGlossary(termKey) {
    const data = glossaryData[termKey];
    if (!data) return;
    document.getElementById('modalTitle').innerText = data.title;
    document.getElementById('modalDescription').innerText = data.desc;
    document.getElementById('glossaryModal').classList.add('active');
}
function closeGlossaryModal() {
    document.getElementById('glossaryModal').classList.remove('active');
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
        innerSvg.setAttribute('height', '520px');
        innerSvg.style.maxWidth = '1000px';
    }
    
    const innerImg = zoomBody.querySelector('img');
    if (innerImg) {
        innerImg.style.maxHeight = '70vh';
        innerImg.style.width = 'auto';
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
        closeGlossaryModal();
        closeZoomModal();
    }
});
</script>
"""

# Enhanced WBS 17 Guideline with Step Diagrams Embedded inside 3-Step Procedure Cards
gui_enhanced_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 궤광 및 철근 조립 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {zoom_modal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-sky-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-sky-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-17 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">4단계 매칭 2D 기술 도식 & 단계별 visual 가이드</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[TCL] 궤광 및 철근 조립 수행지침서</h1>
            <p class="text-sky-200 mt-2 text-sm sm:text-base">"CP 광파 측량, 1,435mm 타이바 정원 고정, 철근 40mm 피복 & 신호 150mm 이격 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-sky-50 border border-sky-200 p-5 rounded-xl text-xs sm:text-sm text-sky-900 shadow-sm">
            <h4 class="font-bold text-sky-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [TCL] 궤광 및 철근 조립 4단계 1:1 실무 핵심
            </h4>
            <p class="leading-relaxed">
                TCL 콘크리트도상 타설 전 궤광 변위 방지 및 <strong><span class="term-highlight" onclick="openGlossary('tie_bar')">1,435mm 표준궤 타이바</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('rebar_cover')">철근 피복 40mm</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('signal_clearance')">신호 케이블 150mm 이격</span></strong>을 검수하는 공종입니다. 각 단계별 <strong>정밀 2D 기술 도식</strong>을 제공하며, 모든 도식은 클릭 시 화면 전체에 <strong>초대형 고화질 뷰(`openDiagramZoom`)</strong>로 확대됩니다.
            </p>
        </div>

        <!-- 1. 4단계 시공 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-sky-600 pb-2">
                <span class="text-sky-600">1.</span> 궤광 및 철근 조립 4단계 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">CP 측량 & 노반 청소</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            CP 광학 레벨기로 <strong>궤도 중심선 & 레벨 측정</strong> 후 이물질 완전 청소
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        📐 [도식 1] 연동 참조
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">1,435mm 타이바 고정</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <strong>1,435mm 타이바 설치</strong> 및 궤간(<strong>+3, -1mm</strong>), 캔트(<strong>&plusmn;2mm</strong>) 고정
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        📏 [도식 2] 연동 참조
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">철근 2m배근 & 40mm피복</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            종/횡철근 <strong>2m 간격 배근</strong>, 하부 <strong>피복 40mm 스페이서</strong> 및 용접 고정
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        🏗️ [도식 3] 연동 참조
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">신호150mm이격 & 결속검측</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            신호 루프 <strong>&ge; 150mm 이격</strong>, 결속선 긴장 & 감리 검측서 마감
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        📡 [도식 4] 연동 참조
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 4단계 1:1 매칭 4대 정밀 공학 기술 도식 (Light Theme & Clickable Zoom) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-sky-600 pb-2">
                <span class="text-sky-600">2.</span> 4단계 1:1 매칭 정밀 공학 기술 도식 (🔍 도식 클릭 시 대형 팝업 확대)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- STEP 1 -> 도식 1 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-amber-500 rounded-full inline-block"></span>
                                [도식 1] (STEP 1) CP 측량 & 노반 레벨 측정
                            </h3>
                            <span class="bg-amber-100 text-amber-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">CP 광파 측량</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram17_STEP1', '[도식 1] CP 광학 레벨기 3D 측량 & 노반 레벨 측정 도면')">
                            <svg id="svgDiagram17_STEP1" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="40" y="160" width="340" height="40" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <text x="210" y="185" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">HBR 기초 콘크리트 바닥층</text>
                                <line x1="80" y1="50" x2="80" y2="160" stroke="#d97706" stroke-width="2.5"/>
                                <circle cx="80" cy="40" r="10" fill="#f59e0b"/>
                                <text x="80" y="22" font-size="11" font-weight="black" fill="#b45309" text-anchor="middle">CP 광학 레벨 삼각대</text>
                                <line x1="80" y1="50" x2="340" y2="110" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,2"/>
                                <text x="220" y="70" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">3D 중심선 & 기준높이 측정 빔</text>
                                <rect x="330" y="90" width="20" height="70" fill="#0284c7"/>
                                <text x="340" y="82" font-size="10" font-weight="black" fill="#0284c7" text-anchor="middle">측량 표척</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-amber-50 p-3.5 rounded-xl border border-amber-100 text-xs text-amber-900 leading-relaxed">
                        <strong>📐 STEP 1 핵심:</strong> CP 광학 레벨기를 정밀 세팅하여 <strong>궤도 중심선 및 기준 높이를 측량</strong>하고, 노반 면 이물질을 청소합니다.
                    </div>
                </div>

                <!-- STEP 2 -> 도식 2 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-sky-500 rounded-full inline-block"></span>
                                [도식 2] (STEP 2) 1,435mm 타이바 정원 고정
                            </h3>
                            <span class="bg-sky-100 text-sky-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">1,435mm 정원</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram17_STEP2', '[도식 2] 1,435mm 타이바 설치 & 궤간/캔트 정밀 조율 도면')">
                            <svg id="svgDiagram17_STEP2" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="80" y="90" width="30" height="70" fill="#475569"/>
                                <rect x="310" y="90" width="30" height="70" fill="#475569"/>
                                <line x1="110" y1="125" x2="310" y2="125" stroke="#0284c7" stroke-width="6"/>
                                <rect x="105" y="115" width="12" height="20" fill="#f59e0b"/>
                                <rect x="303" y="115" width="12" height="20" fill="#f59e0b"/>
                                <text x="210" y="110" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">1,435mm 타이바 (Tie Bar)</text>
                                <text x="210" y="150" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">궤간 오차 (+3, -1mm) | 캔트 (&plusmn;2.0mm)</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-sky-50 p-3.5 rounded-xl border border-sky-100 text-xs text-sky-900 leading-relaxed">
                        <strong>📏 STEP 2 핵심:</strong> 1,435mm 표준궤 정원을 유지하기 위해 <span class="term-highlight" onclick="openGlossary('tie_bar')">타이바를 결속</span>하고 락너트를 조여 오차를 정밀 조율합니다.
                    </div>
                </div>

                <!-- STEP 3 -> 도식 3 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 3] (STEP 3) 철근 2m배근 & 40mm 피복
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">피복 &ge; 40mm</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram17_STEP3', '[도식 3] 종/횡철근 2m 간격 배근 & 피복 블럭 40mm 확보 도면')">
                            <svg id="svgDiagram17_STEP3" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="40" y="170" width="340" height="30" fill="#cbd5e1"/>
                                <line x1="60" y1="130" x2="360" y2="130" stroke="#059669" stroke-width="4"/>
                                <line x1="120" y1="80" x2="120" y2="160" stroke="#059669" stroke-width="4"/>
                                <line x1="300" y1="80" x2="300" y2="160" stroke="#059669" stroke-width="4"/>
                                <rect x="110" y="160" width="20" height="10" fill="#1e293b"/>
                                <rect x="290" y="160" width="20" height="10" fill="#1e293b"/>
                                <text x="210" y="70" font-size="11" font-weight="black" fill="#059669" text-anchor="middle">종/횡방향 철근 2m 배근 간격</text>
                                <text x="210" y="155" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">하부 피복 스페이서 블럭 (&ge; 40mm)</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-100 text-xs text-emerald-900 leading-relaxed">
                        <strong>🏗️ STEP 3 핵심:</strong> 종/횡철근을 2m 간격으로 조립하고 하부 <span class="term-highlight" onclick="openGlossary('rebar_cover')">피복 블럭으로 40mm 이상 확보</span> 후 결속합니다.
                    </div>
                </div>

                <!-- STEP 4 -> 도식 4 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 4] (STEP 4) 신호루프 150mm이격 & 검측
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">이격 &ge; 150mm</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram17_STEP4', '[도식 4] 신호 감선 루프 케이블 150mm 이격 & 철근 결속 검측 도면')">
                            <svg id="svgDiagram17_STEP4" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <line x1="60" y1="150" x2="360" y2="150" stroke="#475569" stroke-width="4"/>
                                <line x1="60" y1="60" x2="360" y2="60" stroke="#dc2626" stroke-dasharray="5,3" stroke-width="3"/>
                                <text x="210" y="45" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">신호 감선 및 루프 케이블 (Loop Cable)</text>
                                <line x1="210" y1="65" x2="210" y2="145" stroke="#2563eb" stroke-width="2"/>
                                <text x="220" y="110" font-size="12" font-weight="black" fill="#2563eb" text-anchor="start">안전 이격 거리 &ge; 150mm</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>📡 STEP 4 핵심:</strong> <span class="term-highlight" onclick="openGlossary('signal_clearance')">신호 루프 케이블 배근 시 150mm 이상 이격</span>을 확보하고 철근 결속선 상태를 검측 마감합니다.
                    </div>
                </div>
            </div>
        </div>

        <!-- ★ [요청사항 구현] 3. 3단계 체계별 세부 작업 수행절차 (단계별 정밀 2D visual 도식 수록) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure & Visual Diagrams)
            </h2>
            
            <div class="space-y-8 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-500 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 사전 준비 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">스핀들 게이지 정밀 교정 및 광학 측량기 셋팅</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        CP 광학 레벨기를 이용하여 궤도 중심선 및 기준 높이를 정밀 측량하여 오차를 확인하고, 기초 노반 바닥 면의 잔여 이물질과 돌가루를 고압 에어 노즐로 100% 청소합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-amber-200" onclick="openDiagramZoom('svgStep1_Detail', '[사전 준비] CP 광학 레벨 3D 측량 & 노반 청소 실무 도면')">
                        <svg id="svgStep1_Detail" viewBox="0 0 500 160" width="100%" height="160" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="160" fill="#f8fafc"/>
                            <rect x="30" y="115" width="440" height="35" fill="#cbd5e1" stroke="#334155" stroke-width="1.5"/>
                            <text x="250" y="137" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">HBR 기초 콘크리트 버림 바닥층 (100% 청소 완료)</text>
                            <line x1="90" y1="35" x2="90" y2="115" stroke="#d97706" stroke-width="2.5"/>
                            <circle cx="90" cy="25" r="9" fill="#f59e0b"/>
                            <text x="90" y="12" font-size="11" font-weight="black" fill="#b45309" text-anchor="middle">CP 광학 레벨기 삼각대</text>
                            <line x1="90" y1="35" x2="410" y2="85" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,2"/>
                            <text x="260" y="52" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">3D CP 중심선 & 캔트/높이 측량 레이저 빔</text>
                            <rect x="400" y="65" width="20" height="50" fill="#0284c7"/>
                            <text x="410" y="58" font-size="10" font-weight="black" fill="#0284c7" text-anchor="middle">표척</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-sky-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-sky-100 text-sky-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 본 시공 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">궤광 조립, 스핀들 캔트 미세 조정 & 철근 절연 배근</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        <span class="term-highlight" onclick="openGlossary('tie_bar')">1,435mm 표준궤 타이바(Tie Bar)를 조임 고정</span>하여 궤간 오차(+3, -1mm) 및 캔트/수평 오차(&plusmn;2.0mm 이내)를 조율하고, <span class="term-highlight" onclick="openGlossary('rebar_cover')">절연 철근 받침대(피복 40mm)를 설치</span>하여 신호 궤도회로 단락 현상을 완벽히 차단합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-sky-200" onclick="openDiagramZoom('svgStep2_Detail', '[본 시공] 1,435mm 타이바 조임 & 철근 피복 40mm 절연 배근 도면')">
                        <svg id="svgStep2_Detail" viewBox="0 0 500 170" width="100%" height="170" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="170" fill="#f8fafc"/>
                            <rect x="30" y="135" width="440" height="25" fill="#cbd5e1"/>
                            <rect x="70" y="60" width="24" height="60" fill="#475569"/>
                            <rect x="406" y="60" width="24" height="60" fill="#475569"/>
                            <line x1="94" y1="90" x2="406" y2="90" stroke="#0284c7" stroke-width="5"/>
                            <rect x="90" y="82" width="10" height="16" fill="#f59e0b"/>
                            <rect x="400" y="82" width="10" height="16" fill="#f59e0b"/>
                            <text x="250" y="80" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">1,435mm 타이바 정원 고정 (+3,-1mm)</text>
                            
                            <line x1="50" y1="120" x2="450" y2="120" stroke="#059669" stroke-width="3"/>
                            <rect x="150" y="120" width="16" height="15" fill="#1e293b"/>
                            <rect x="330" y="120" width="16" height="15" fill="#1e293b"/>
                            <text x="250" y="115" font-size="10" font-weight="bold" fill="#059669" text-anchor="middle">철근 2m 배근 & 하부 피복 절연 스페이서 블럭 (&ge; 40mm)</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 검사 및 확정 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">궤도 틀림 측량표 작성, 신호150mm이격 & 검측 승인</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        실시간 정밀 궤간척(Track Gauge)으로 궤도 틀림을 측량하여 측정 성과표를 작성하고, <span class="term-highlight" onclick="openGlossary('signal_clearance')">신호 루프 센서 케이블 배근 이격(&ge; 150mm)</span>을 감리 입회 검측하여 최종 서명 승인합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Detail', '[검사 마감] 정밀 궤간척 측정 & 신호 루프 150mm 안전 이격 도면')">
                        <svg id="svgStep3_Detail" viewBox="0 0 500 170" width="100%" height="170" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="170" fill="#f8fafc"/>
                            <line x1="40" y1="120" x2="460" y2="120" stroke="#475569" stroke-width="4"/>
                            <line x1="40" y1="45" x2="460" y2="45" stroke="#dc2626" stroke-dasharray="5,3" stroke-width="3"/>
                            <text x="250" y="32" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">신호 루프 센서 케이블 배관 (AFTC / Loop)</text>
                            
                            <line x1="250" y1="50" x2="250" y2="115" stroke="#2563eb" stroke-width="2.5"/>
                            <text x="260" y="85" font-size="12" font-weight="black" fill="#2563eb" text-anchor="start">신호 이격 거리 &ge; 150mm (전자기 간섭 차단)</text>
                            
                            <rect x="360" y="105" width="80" height="30" fill="#15803d" rx="4"/>
                            <text x="400" y="124" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">궤간척 측정 합격</text>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write
force_write(path_gui, gui_enhanced_html)
force_write(path_gui_alt, gui_enhanced_html)

print("\n🎉 SUCCESSFULLY INTEGRATED VISUAL DIAGRAMS INTO WBS 17 3-STEP PROCEDURE!")
