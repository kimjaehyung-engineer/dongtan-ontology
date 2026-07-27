import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\16_[PST] 전단앵커설치 및 충전재 주입"

path_gui = os.path.join(target_dir, "수행지침", "[PST] 전단앵커설치 및 충전재 주입_수행지침.html")
path_gui_alt = os.path.join(target_dir, "수행지침", "16_[PST] 전단앵커설치 및 충전재 주입_수행지침.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully updated WBS 16 with Reference Simulation Diagram: {path}")

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
    'shear_anchor': {
        title: '⚓ 전단앵커 (Shear Key Anchor)',
        desc: 'HBS 강화노반 및 TCL 기초 콘크리트 층과 상부 프리캐스트 패널(PST) 간의 층간 전단 미끄러짐을 완벽히 차단하여 일체화 구조를 형성하는 전단키 연결 장치입니다.'
    },
    'grout_strength': {
        title: '📊 무수축 모르타르 그라우트 압축강도 (≥ 30 / 45 MPa)',
        desc: '전단앵커 홀 및 충전층의 수축 균열을 방지하기 위한 무수축 그라우트의 시방 강도 기준입니다. 일반 그라우트 30 MPa 이상, PST 몰탈 충전재 공시체 45 MPa 이상을 충족해야 합니다.'
    },
    'eva_foam': {
        title: '🫧 EVA Foam 유출구 & 밀실 오버플로우',
        desc: '그라우트 주입 시 내부 공기 공동(Air Void)을 제거하고 충전재가 완전 밀실하게 찼는지 확인하기 위해 EVA Foam 구멍으로 몰탈이 넘쳐 나오도록 주입 상태를 점검하는 수칙입니다.'
    },
    'key_cap': {
        title: '🛡️ 전단키 덮개 봉인 & 미충전 재작업 수칙',
        desc: '그라우트 주입 직후 경화 전 전단키 덮개를 시공하여 수분 유출 및 이물질 침투를 차단합니다. 충전 이상 발생 시 경화 전에 기 주입재를 즉시 제거하고 물청소 후 재작업해야 합니다.'
    },
    'hbs_layer': {
        title: '🧱 HBS 강화노반 지반층 (Hydraulically Bound Base Support)',
        desc: '흙과 자갈에 시멘트를 섞어 롤러로 꽝꽝 다진 고지지력 노반 기초 지층입니다. 지지력 지수 K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa을 확보하여 부등침하를 방지합니다.'
    },
    'hbr_layer': {
        title: '🏗️ HBR 기초콘크리트 층 (Hydraulic Base Concrete)',
        desc: '강화노반(HBS) 상부에 매끄럽게 타설하여 궤도 콘크리트 슬래브가 올라설 평평한 수평 바닥을 만드는 기초 버림 콘크리트 레이어입니다.'
    },
    'tcl_pst_layer': {
        title: '🚆 TCL 궤도콘크리트 & PST 슬래브 패널 층',
        desc: '트램 레일을 직접 고정 지지하는 최종 본선 궤도 콘크리트 슬래브 구조체층입니다.'
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

guideline_wbs16_with_ref_diagram_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [PST] 전단앵커설치 및 충전재 주입 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        """ + zoom_modal_style + """
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 to-slate-900 opacity-70"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-16 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">4단계 매칭 + 수직지층 시뮬레이션 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[PST] 전단앵커설치 및 충전재 주입 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"4단계 시공 도식(1~4) 및 트램 궤도 수직 지층 샌드위치 구조 시뮬레이션 참고 도식 종합 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [PST] 전단앵커설치 및 충전재 주입 4단계 1:1 실무 핵심
            </h4>
            <p class="leading-relaxed">
                HBS 강화노반 및 TCL 기초층과 상부 PST 패널을 일체화하는 <strong><span class="term-highlight" onclick="openGlossary('shear_anchor')">전단앵커 공종</span></strong>입니다. STEP 1부터 STEP 4까지 각 단계에 직관적으로 1:1 매칭되는 <strong>4개의 정밀 2D 기술 도식</strong>과 문서 맨 아래 <strong>트램 궤도 수직 지층 구조 시뮬레이션 참고 도식</strong>을 제공하며, 모든 도식은 클릭 시 화면 전체에 <strong>초대형 고화질 뷰(`openDiagramZoom`)</strong>로 확대됩니다.
            </p>
        </div>

        <!-- 1. [Flexible Step Policy 적용] 전단앵커 4단계 시공 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 전단앵커 설치·그라우트 주입 4단계 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">천공·깊이수직도·청소</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            천공 깊이 게이지 측정 & 수직도 확보, 에어/수쇄 이물질 <strong>100% 청소</strong>
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        📐 [도식 1] 연동 참조
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">앵커삽입·인장시험</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            HBS/TCL 일체화 전단앵커 정위치 삽입 & 현장 <strong>앵커 인장강도</strong> 성적 확보
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        ⚓ [도식 2] 연동 참조
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">무수축그라우트·EVA폼</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            무수축 배합 준수 & <strong>EVA Foam 구멍 몰탈 오버플로우</strong> 밀실 주입
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        🫧 [도식 3] 연동 참조
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">전단키덮개·45MPa강도</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            경화 전 <strong>전단키 덮개 시공</strong> 봉인 & 28일 몰탈 강도 <strong>&ge; 45 MPa</strong> 최종 승인
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        🛡️ [도식 4] 연동 참조
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 4단계 1:1 매칭 4대 정밀 공학 기술 도식 (Light Theme & Clickable Zoom) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 4단계 1:1 매칭 정밀 공학 기술 도식 (🔍 도식 클릭 시 대형 팝업 확대)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- STEP 1 -> 도식 1 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-amber-500 rounded-full inline-block"></span>
                                [도식 1] (STEP 1) 천공 깊이수직도 & 청소
                            </h3>
                            <span class="bg-amber-100 text-amber-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">수직도 100%</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram16_STEP1', '[도식 1] 전단앵커 구멍 천공 깊이 게이지 측정 & 에어 청소 도면')">
                            <svg id="svgDiagram16_STEP1" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="40" y="100" width="340" height="100" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <text x="210" y="185" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">HBS / TCL 기초 콘크리트 지층</text>
                                <rect x="185" y="100" width="50" height="70" fill="#f8fafc" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,2"/>
                                <line x1="210" y1="30" x2="210" y2="165" stroke="#0284c7" stroke-width="3"/>
                                <text x="210" y="22" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">천공 깊이 측량 게이지</text>
                                <line x1="140" y1="60" x2="185" y2="120" stroke="#059669" stroke-width="2.5"/>
                                <text x="130" y="52" font-size="10" font-weight="black" fill="#059669" text-anchor="middle">고압 에어 분진 청소</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-amber-50 p-3.5 rounded-xl border border-amber-100 text-xs text-amber-900 leading-relaxed">
                        <strong>📐 STEP 1 핵심:</strong> 앵커 홀 천공 후 깊이 측정 게이지로 수직도를 검수하고, <strong>고압 에어/수쇄 노즐로 내부 돌가루를 100% 제거</strong>합니다.
                    </div>
                </div>

                <!-- STEP 2 -> 도식 2 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-sky-500 rounded-full inline-block"></span>
                                [도식 2] (STEP 2) 앵커 정위치 & 인장시험
                            </h3>
                            <span class="bg-sky-100 text-sky-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">층간 일체화</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram16_STEP2', '[도식 2] 전단앵커 정위치 삽입 & 인장강도 시험 도면')">
                            <svg id="svgDiagram16_STEP2" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="40" y="120" width="340" height="80" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <text x="210" y="185" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">HBS / TCL 층간 구조</text>
                                <rect x="50" y="70" width="320" height="50" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>
                                <text x="210" y="98" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">상부 PST 슬래브 패널</text>
                                <rect x="195" y="40" width="30" height="120" fill="#d97706" rx="2"/>
                                <text x="210" y="32" font-size="11" font-weight="black" fill="#b45309" text-anchor="middle">일체화 전단앵커 (인장시험 합격)</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-sky-50 p-3.5 rounded-xl border border-sky-100 text-xs text-sky-900 leading-relaxed">
                        <strong>⚓ STEP 2 핵심:</strong> HBS/TCL층과 상부 패널을 결합하는 <strong>전단앵커를 정위치에 세팅</strong>하고, 현장 앵커 인장시험 성적을 확보합니다.
                    </div>
                </div>

                <!-- STEP 3 -> 도식 3 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 3] (STEP 3) 그라우트 & EVA Foam 유출
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">오버플로우 점검</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram16_STEP3', '[도식 3] 무수축 모르타르 주입 & EVA Foam 유출 오버플로우 도면')">
                            <svg id="svgDiagram16_STEP3" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="40" y="100" width="340" height="90" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <rect x="150" y="100" width="120" height="70" fill="#0284c7" opacity="0.8"/>
                                <text x="210" y="140" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">무수축 그라우트 밀실 충전</text>
                                <line x1="170" y1="20" x2="170" y2="100" stroke="#0284c7" stroke-width="4"/>
                                <circle cx="250" cy="100" r="10" fill="#38bdf8"/>
                                <path d="M 250 90 Q 260 70 270 90 T 280 100" fill="none" stroke="#38bdf8" stroke-width="3"/>
                                <text x="290" y="80" font-size="11" font-weight="black" fill="#0369a1" text-anchor="start">EVA Foam 오버플로우 확인</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-100 text-xs text-emerald-900 leading-relaxed">
                        <strong>🫧 STEP 3 핵심:</strong> 무수축 모르타르 주입 시 <strong>EVA Foam 공기 배출 구멍으로 몰탈이 유출될 때까지 밀실 연속 주입</strong>합니다. (미충전 시 경화 전 즉시 세척 재작업)
                    </div>
                </div>

                <!-- STEP 4 -> 도식 4 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 4] (STEP 4) 전단키 덮개 & 45MPa 강도
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">강도 &ge; 45 MPa</span>
                        </div>
                        
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram16_STEP4', '[도식 4] 전단키 봉인 덮개 시공 & 45 MPa 몰탈 강도 승인 도면')">
                            <svg id="svgDiagram16_STEP4" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                <rect x="40" y="110" width="340" height="80" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <rect x="150" y="110" width="120" height="60" fill="#0284c7" opacity="0.8"/>
                                <rect x="130" y="98" width="160" height="14" fill="#1e293b" rx="2"/>
                                <text x="210" y="92" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">전단키 봉인 덮개 (경화 전 설치 완료)</text>
                                <g transform="translate(330, 20)">
                                    <rect x="0" y="0" width="35" height="42" fill="#94a3b8" stroke="#1e293b" stroke-width="1.5"/>
                                    <text x="17" y="25" font-size="8" font-weight="black" fill="#1e293b" text-anchor="middle">≥45MPa</text>
                                </g>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>🛡️ STEP 4 핵심:</strong> 충전층 경화 전 <strong>전단키 덮개를 즉시 설치하여 수분유출/이물질을 차단</strong>하고, 28일 몰탈 공시체 강도 <strong>&ge; 45 MPa(최소 30 MPa 이상)</strong>를 승인 마감합니다.
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. 상세 세부 수행 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 4단계 실무 엔지니어링 수행 수칙
            </h2>
            
            <div class="space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 1</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">전단앵커 천공 깊이·수직도 검수 & 에어 청소 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            천공 측정 게이지를 사용하여 전단앵커 홀 깊이 및 수직도를 100% 검수하고, 고압 에어 노즐 및 수쇄 청소를 수행하여 구멍 내부 돌가루와 이물질을 완벽히 제거합니다. (상기 [도식 1] 참조)
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">전단앵커 정위치 세팅 & 인장강도 성적 확보 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            HBS/TCL층과 상부 PST 패널을 일체화하는 <span class="term-highlight" onclick="openGlossary('shear_anchor')">전단앵커를 정위치에 삽입</span>하고, 인장시험기로 현장 앵커 인장강도를 검측하여 합격 성적서를 확보합니다. (상기 [도식 2] 참조)
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">무수축 그라우트 배합 & EVA Foam 오버플로우 주입 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            무수축 모르타르 배합비를 준수하고 주입 펌프를 투입하여, <span class="term-highlight" onclick="openGlossary('eva_foam')">EVA Foam 공기 배출구로 몰탈이 유출될 때까지 밀실 연속 주입</span>합니다. 장비 이상 등으로 미충전 시에는 경화 전에 기 주입재를 즉시 전량 제거 후 물청소를 실시하고 재작업합니다. (상기 [도식 3] 참조)
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">전단키 덮개 봉인 시공 & 45 MPa 몰탈 공시체 강도 승인 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            그라우트 주입 완료 직후 충전층이 경화되기 전에 <span class="term-highlight" onclick="openGlossary('key_cap')">전단키 덮개를 즉시 설치</span>하여 수분 급속 유출 및 이물질 침투를 봉인 차단하며, 28일 몰탈 공시체 압축강도 <strong>&ge; 45 MPa (최소 30 MPa 이상)</strong> 및 음향탐사를 확인하여 최종 마감합니다. (상기 [도식 4] 참조)
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ★ [신규 탑재] 4. 동탄트램 궤도 수직 지층 샌드위치 구조 & 전단앵커 결합 시뮬레이션 2D 기술 도식 -->
        <div class="border-t-2 border-slate-200 pt-8 mt-10">
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">4.</span> [참고 기술 시뮬레이션] 동탄트램 궤도 수직 지층 샌드위치 구조 & 전단앵커 결합 단면도
            </h2>

            <div class="bg-white p-6 rounded-2xl border border-indigo-100 shadow-lg space-y-6">
                <!-- SVG Simulation Diagram (Clickable Lightbox Zoom Modal) -->
                <div class="clickable-diagram bg-slate-50 p-6 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgDiagramRef_Layers', '[참고 시뮬레이션] 동탄트램 궤도 4단계 수직 지층 샌드위치 구조도')">
                    <svg id="svgDiagramRef_Layers" viewBox="0 0 500 320" width="100%" height="320" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="500" height="320" fill="#f8fafc"/>

                        <!-- [0단계] 원지반 / 다져진 토공 노반 -->
                        <rect x="30" y="255" width="440" height="50" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
                        <text x="250" y="285" font-size="12" font-weight="bold" fill="#334155" text-anchor="middle">0단계: 원지반 및 토공 노반 (Subgrade Ground)</text>

                        <!-- [1단계] HBS 강화노반 지반층 (K30 >= 110 MN/m3) -->
                        <rect x="30" y="195" width="440" height="60" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                        <text x="250" y="230" font-size="13" font-weight="black" fill="#78350f" text-anchor="middle">1단계: HBS 강화노반 지반층 (K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa)</text>

                        <!-- [2단계] HBR 기초 콘크리트 층 -->
                        <rect x="30" y="145" width="440" height="50" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                        <text x="250" y="175" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">2단계: HBR 기초 콘크리트 층 (수평 평탄 버림 바닥)</text>

                        <!-- [3단계] TCL 궤도콘크리트 & PST 슬래브 패널 -->
                        <rect x="30" y="85" width="440" height="60" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>
                        <text x="250" y="120" font-size="13" font-weight="black" fill="#1e3a8a" text-anchor="middle">3단계: TCL 궤도콘크리트 / PST 프리캐스트 슬래브 패널 (≥ 45 MPa)</text>

                        <!-- [4단계] 최상부 레일 (Rail 60kg / 51R1) -->
                        <rect x="100" y="55" width="40" height="30" fill="#334155" rx="3"/>
                        <rect x="360" y="55" width="40" height="30" fill="#334155" rx="3"/>
                        <text x="120" y="45" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">좌측 레일</text>
                        <text x="380" y="45" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">우측 레일</text>

                        <!-- [핵심 결합] 수직 전단앵커 (Shear Key Anchor) - 관통 결합 -->
                        <rect x="235" y="70" width="30" height="150" fill="#dc2626" rx="3" opacity="0.9"/>
                        <text x="250" y="150" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle" transform="rotate(-90 250 150)">수직 전단앵커 층간 결합 (Monolithic Bonding)</text>
                        
                        <!-- 화살표 콜아웃 -->
                        <line x1="280" y1="105" x2="330" y2="105" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,2"/>
                        <text x="335" y="109" font-size="11" font-weight="black" fill="#dc2626" text-anchor="start">무수축그라우트 밀실 충전</text>
                    </svg>
                </div>

                <!-- 상세 아파트 비유 해설 가이드 -->
                <div class="bg-indigo-50 p-5 rounded-xl border border-indigo-100 text-xs sm:text-sm text-indigo-950 space-y-3">
                    <h4 class="font-bold text-indigo-900 text-base flex items-center gap-2">
                        <span>🏗️</span> 트램 궤도 수직 지층 샌드위치 구조 & 전단앵커 역할 이해 가이드
                    </h4>
                    <p class="leading-relaxed">
                        아파트 건물 공사에 비유하면 동탄트램 궤도의 수직 지층 구조를 쉽게 이해할 수 있습니다:
                    </p>
                    <ul class="list-disc pl-5 space-y-1.5 text-indigo-900">
                        <li><strong>1단계 강화노반 (HBS) = 단단하게 다진 땅 지반:</strong> 흙과 자갈에 시멘트를 섞어 롤러로 꽝꽝 다진 고지지력 노반 기초층 (K30 &ge; 110 MN/m&sup3;)</li>
                        <li><strong>2단계 기초콘크리트 층 (HBR) = 평평한 버림 콘크리트 바닥:</strong> 다진 땅(HBS) 위에 수평을 매끄럽게 맞추기 위해 타설하는 수평 받침용 콘크리트</li>
                        <li><strong>3단계 궤도콘크리트/패널 (TCL / PST) = 본체 레일 슬래브 구조물:</strong> 트램 레일을 직접 고정 지지하는 최종 본선 궤도 콘크리트 슬래브 (&ge; 45 MPa)</li>
                        <li><strong>⚓ 수직 전단앵커 결합 = 층간 미끄러짐 방지 핀:</strong> HBS/HBR 기초층부터 상부 PST 패널까지 수직 전단앵커를 관통시키고 무수축 그라우트를 충전하여 열차 주행 시 층간 단층 미끄러짐 없이 **하나의 통 덩어리로 일체화(Monolithic Bonding)**시키는 핵심 장치입니다.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
""" + common_modal_html + """
</body>
</html>
"""

force_write(path_gui, guideline_wbs16_with_ref_diagram_html)
force_write(path_gui_alt, guideline_wbs16_with_ref_diagram_html)

print("\n🎉 SUCCESSFULLY ADDED REFERENCE LAYER SIMULATION DIAGRAM TO WBS 16 GUIDELINE!")
