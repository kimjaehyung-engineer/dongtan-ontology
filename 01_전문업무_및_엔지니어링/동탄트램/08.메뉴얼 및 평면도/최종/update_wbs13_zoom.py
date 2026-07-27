import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

wbs13_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\13_[HBS] 강화노반 확인\수행지침"

path_gui13 = os.path.join(wbs13_dir, "[HBS] 강화노반 확인_수행지침.html")
path_gui13_alt = os.path.join(wbs13_dir, "13_[HBS] 강화노반 확인_수행지침.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Updated Zoom Modal for: {path}")

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
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 공학 검측 해설</h3>
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
    'hbs': {
        title: '🧱 HBS 강화노반 (Hydraulic Base Support Subgrade)',
        desc: '콘크리트 도상(TCL) 하부에 시공되는 고지지력 상부 노반층입니다. 트램 주행 하중을 노상 및 원지반으로 안전하게 분산시키는 핵심 기초 공종입니다.'
    },
    'pbt': {
        title: '⚙️ 평판재하시험 (Plate Bearing Test, PBT)',
        desc: '강화노반 표면에 Φ300mm 재하 평판을 놓고 유압 재크로 하중을 가하여 지반의 노반 반력계수(K30) 및 2차 변형계수(Ev2)를 정밀 측정하는 재하시험입니다.'
    },
    'k30_ev2': {
        title: '📊 K30 ≥ 110 MN/m³ & Ev2 ≥ 120 MPa',
        desc: '트램 콘크리트 도상 부등침하를 예방하기 위한 절대 지지력 지수입니다. K30 반력계수 110 MN/m³ 이상 및 Ev2 변형계수 120 MPa 이상(Ev2/Ev1 ≤ 2.2)이 필수 검증되어야 합니다.'
    },
    'cross_slope': {
        title: '📐 횡단 구배 2.0% & 높이 오차 ±10mm',
        desc: '강화노반 표면 배수 성능 확보를 위한 횡단 구배 2.0% 유지 수칙과 콘크리트 슬래브 두께 유지를 위한 마무리 높이 공차 ±10mm 이내 관리 기준입니다.'
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

guideline13_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 강화노반 확인 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 to-slate-900 opacity-70"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-13 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">노반 지지력 & 레벨 검측 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[HBS] 강화노반 확인 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"기존 도로구간 노상토 지지력(K30 &ge; 110 MN/m³), PBT 평판재하시험 및 노반 높이 오차(&plusmn;10mm) 정밀 가이드"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [HBS] 강화노반 확인 실무 수행 핵심
            </h4>
            <p class="leading-relaxed">
                콘크리트도상 시공 전, 토공사 공종으로부터 인수받는 <strong><span class="term-highlight" onclick="openGlossary('hbs')">상부 강화노반</span></strong>의 지지력 성적서(<span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³, Ev2 &ge; 120 MPa</span>)를 수령 대조하고, 현장 평판재하시험(<span class="term-highlight" onclick="openGlossary('pbt')">PBT</span>) 및 노반 마무리면 높이 오차(<span class="term-highlight" onclick="openGlossary('cross_slope')">&plusmn;10mm 이내</span>), 횡단 구배(2.0%)를 정밀 검측하는 절차입니다.
            </p>
        </div>

        <!-- 1. 강화노반 확인 5대 관리 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 강화노반 확인 5대 관리 프로세스 마스터 체계도 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">인수 서류 확인</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            토공사 지지력 <strong><span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³</span></strong> 및 K70 &ge; 150 MPa/m 성적서 수령
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        📋 핵심: K30 성적서 수령
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">현장 시굴·밀도</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            터파기 시굴 후 들밀도 시험통 통과 상대다짐도 <strong>&ge; 95%</strong> 현장 검증
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        🧪 핵심: 다짐도 &ge; 95%
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">PBT 재하시험</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            현장 <strong><span class="term-highlight" onclick="openGlossary('pbt')">평판재하시험(PBT)</span></strong> 시행, 2차 변형계수 Ev2 &ge; 120 MPa 확인
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        ⚙️ 핵심: Ev2 &ge; 120 MPa
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">레벨·구배 측량</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            마무리면 높이 오차 <strong>&plusmn;10mm 이내</strong> 측량 및 횡단구배 2.0% 점검
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        📏 핵심: 오차 &plusmn;10mm
                    </div>
                </div>

                <div class="flow-card bg-rose-50 p-4 rounded-xl border border-rose-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-rose-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 5</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">인수 대장 서명</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            요철 부위 제거 및 감리 입회 <strong>강화노반 인수조치 대장</strong> 최종 서명
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-rose-100 text-[10px] text-rose-800 font-bold">
                        ✅ 핵심: 인수대장 서명
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 자재별 구조 정밀 공학 기술 도식 (클릭 시 별도 팝업으로 대형 확대) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 강화노반 지지력 & 레벨 검측 정밀 공학 기술 도식 (🔍 클릭 시 대형 팝업 확대)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 도식 1: HBS 강화노반 PBT 평판재하시험 메커니즘 도면 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 1] HBS 강화노반 PBT 평판재하시험 메커니즘
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">K30 &ge; 110 MN/m³</span>
                        </div>
                        
                        <!-- SVG Diagram 1 Container (Clickable Zoom) -->
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram13_1', '[도식 1] HBS 강화노반 PBT 평판재하시험 메커니즘')">
                            <svg id="svgDiagram13_1" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- 노반 지층 -->
                                <rect x="30" y="150" width="360" height="50" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                                <text x="210" y="182" font-size="12" font-weight="black" fill="#78350f" text-anchor="middle">HBS 강화노반 (K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa)</text>
                                
                                <!-- PBT 재하 평판 (300mm) -->
                                <rect x="150" y="140" width="120" height="10" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                                <text x="210" y="133" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">Φ300mm PBT 재하 평판</text>
                                
                                <!-- 유압 재크 & 하중 반력 트럭 바닥 -->
                                <rect x="195" y="75" width="30" height="60" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
                                <text x="210" y="110" font-size="11" font-weight="black" fill="#0369a1" text-anchor="middle">유압재크</text>
                                <line x1="210" y1="18" x2="210" y2="75" stroke="#d97706" stroke-width="4"/>
                                <rect x="100" y="12" width="220" height="16" fill="#ef4444" rx="2"/>
                                <text x="210" y="24" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">반력 트럭 덤프 하중 (25Ton)</text>

                                <!-- 변형 인디케이터 게이지 -->
                                <line x1="85" y1="145" x2="150" y2="145" stroke="#059669" stroke-width="2.5"/>
                                <circle cx="85" cy="145" r="6.5" fill="#059669"/>
                                <text x="80" y="130" font-size="11" font-weight="black" fill="#047857" text-anchor="end">침하량 다이얼 게이지</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>📊 공학 핵심:</strong> 덤프 트럭 반력 하중을 이용해 Φ300mm 평판에 유압을 가하여 <strong>K30 &ge; 110 MN/m³ 및 Ev2 &ge; 120 MPa(Ev2/Ev1 &le; 2.2)</strong> 지지력을 감리 입회 하에 정밀 산출합니다.
                    </div>
                </div>

                <!-- 도식 2: 강화노반 마무리면 레벨 & 횡단구배(2.0%) 점검 도면 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 2] 노반 레벨(&plusmn;10mm) & 횡단구배(2.0%)
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">배수 경사 2.0%</span>
                        </div>
                        
                        <!-- SVG Diagram 2 Container (Clickable Zoom) -->
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram13_2', '[도식 2] 노반 레벨(&plusmn;10mm) & 횡단구배(2.0%) 점검 도면')">
                            <svg id="svgDiagram13_2" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- 경사 노반 -->
                                <polygon points="30,120 390,145 390,195 30,195" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
                                <text x="210" y="175" font-size="12" font-weight="black" fill="#1e293b" text-anchor="middle">강화노반 표면 (마무리면 오차 ±10mm 이내)</text>

                                <!-- 횡단 구배 2.0% 경사 표시선 -->
                                <line x1="50" y1="98" x2="370" y2="123" stroke="#d97706" stroke-width="2.5" stroke-dasharray="4,2"/>
                                <text x="210" y="103" font-size="12" font-weight="black" fill="#b45309" text-anchor="middle">횡단 구배 2.0% 배수 경사</text>

                                <!-- 광파 측량 타겟 & 레벨 측량 -->
                                <line x1="120" y1="55" x2="120" y2="126" stroke="#0284c7" stroke-width="2" stroke-dasharray="2,2"/>
                                <circle cx="120" cy="55" r="5.5" fill="#0284c7"/>
                                <text x="120" y="42" font-size="11" font-weight="black" fill="#0369a1" text-anchor="middle">광파 타겟 (계획고 오차 점검)</text>

                                <!-- 배수 맹암거 측구 -->
                                <rect x="370" y="140" width="30" height="55" fill="#f1f5f9" stroke="#0284c7" stroke-width="1.5"/>
                                <circle cx="385" cy="170" r="8" fill="#0284c7"/>
                                <text x="385" y="132" font-size="10" font-weight="black" fill="#0369a1" text-anchor="middle">배수 맹암거</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-100 text-xs text-emerald-900 leading-relaxed">
                        <strong>📏 측량 핵심:</strong> 광파 레벨기로 노반 마무리면 계획고 오차를 <strong>&plusmn;10mm 이내</strong>로 정밀 관리하며, 표면 우수 배수를 위한 <strong>2.0% 횡단 구배</strong>를 형성하여 맹암거로 유도합니다.
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. 상세 세부 수행 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 단계별 실무 엔지니어링 수행 수칙
            </h2>
            
            <div class="space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 1</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">토공사 지지력 성적서 사전 검토 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            토공 공종으로부터 상부 강화노반 지지력 성적서(<span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³</span> 또는 K70 &ge; 150 MPa/m) 원본을 대조 수령하고 시험 위치 및 시험 일자를 검토합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">터파기 시굴 & 들밀도 상대다짐도 검증 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            현장 터파기 구간 시굴 후 들밀도 시험통을 통과한 강화노반 흙의 상대다짐도 <strong>&ge; 95%</strong> 확보 여부를 현장에서 직접 측정 점검합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">현장 PBT 평판재하시험 & 2차 변형계수 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            감리 입회 하에 Φ300mm 재하 평판과 유압 재크를 세팅하여 현장 <span class="term-highlight" onclick="openGlossary('pbt')">평판재하시험(PBT)</span>을 수행하고 2차 변형계수 <strong>Ev2 &ge; 120 MPa(Ev2/Ev1 &le; 2.2)</strong>를 최종 승인합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">마무리면 오차(&plusmn;10mm) & 횡단 구배(2.0%) 측량 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            광파 레벨기를 투입하여 강화노반 마무리면 계획고 오차를 <strong>&plusmn;10mm 이내</strong>로 관리하며, 표면 우수가 맹암거로 유도되도록 <strong><span class="term-highlight" onclick="openGlossary('cross_slope')">2.0% 횡단 경사</span></strong>를 검측합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-rose-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 5</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">노반 마무리면 요철 제거 & 인수대장 서명 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            노반 표면의 요철, 돌가루 및 불량토를 깨끗이 제거 조치하고, 감리단 입회 하에 강화노반 인수조치 측량 대장에 최종 확인 서명하여 궤도공으로 명확히 인수합니다.
                        </p>
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

force_write(path_gui13, guideline13_html)
force_write(path_gui13_alt, guideline13_html)

print("\n🎉 SUCCESSFULLY UPDATED WBS 13 & 14 WITH CLICKABLE DIAGRAM ZOOM MODALS!")
