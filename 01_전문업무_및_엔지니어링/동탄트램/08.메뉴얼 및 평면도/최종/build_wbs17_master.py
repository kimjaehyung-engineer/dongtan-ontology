import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\17_[TCL] 궤광 및 철근 조립"

path_std = os.path.join(target_base, "표준서", "[TCL] 궤광 및 철근 조립_표준서.html")
path_std_alt = os.path.join(target_base, "표준서", "17_[TCL] 궤광 및 철근 조립_표준서.html")

path_gui = os.path.join(target_base, "수행지침", "[TCL] 궤광 및 철근 조립_수행지침.html")
path_gui_alt = os.path.join(target_base, "수행지침", "17_[TCL] 궤광 및 철근 조립_수행지침.html")

path_chk = os.path.join(target_base, "체크리스트", "[TCL] 궤광 및 철근 조립_체크리스트.html")
path_chk_alt = os.path.join(target_base, "체크리스트", "17_[TCL] 궤광 및 철근 조립_체크리스트.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully written file: {path}")

# Common Zoom Modal Styles
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

# -------------------------------------------------------------------------
# 1. WBS 17 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 궤광 및 철근 조립 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-17 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 / KCS 47 30 00 규격</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[TCL] 궤광 및 철근 조립 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"TCL 철근조립 및 부연시 매립형 궤도 변위 방지 표준 엔지니어링 시방서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 본선 TCL(Track Concrete Layer) 콘크리트도상 공종 중 <strong>임시침목 및 궤광 조립, 1,435mm 표준궤 정원 타이바(Tie Bar) 설치, 종/횡방향 철근 조립 및 신호 감선 이격</strong> 작업을 안전하고 정밀하게 수행하기 위한 품질 및 공학 규격을 규정합니다. (주관: 현장 공사팀)
            </p>
        </div>

        <!-- 1. 엔지니어링 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 정량적 공학 표준 수칙 (Engineering Tolerances)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">📐 궤도 정원 & 타이바 설치 기준</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>표준 궤간:</strong> 1,435mm 정원 유지 타이바(Tie Bar) 전 구간 필수 설치</li>
                        <li><strong>궤간 공차:</strong> +3mm, -1mm 이내 고정</li>
                        <li><strong>캔트 및 수평:</strong> 오차 &plusmn;2.0mm 이내 관리</li>
                        <li><strong>중심간격 오차:</strong> 3mm 이내 정밀 수평 조율</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">🏗️ 철근 배근 & 피복·신호 이격 기준</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>철근 배근 간격:</strong> 종방향 및 횡방향 철근 2m 간격 설치</li>
                        <li><strong>피복 두께:</strong> 최소 피복 두께 <strong>&ge; 40mm</strong> 확보</li>
                        <li><strong>처짐 방지:</strong> 철근 처짐이 없도록 용접 또는 결속선 고정</li>
                        <li><strong>신호 루프 이격:</strong> 신호 감선 및 루프 케이블 <strong>&ge; 150mm</strong> 이격</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 서식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 필 수 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-2">
                <p>✔️ <strong>철근배근 검측서:</strong> 피복두께(40mm), 2m 배근 간격, 결속선 긴장 상태 검측 기록</p>
                <p>✔️ <strong>신호 이격 거리표:</strong> 신호 루프 케이블 배근 이격(150mm) 감리 입회 서명서</p>
                <p>✔️ <strong>궤도 중심선 레벨 측량표:</strong> CP 광파 측량 기반 궤간/캔트/수평 오차 데이터</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 17 GUIDELINE HTML (4-Step 1:1 Light-Theme SVG Diagrams & Zoom Modal)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">4단계 매칭 2D 기술 도식 매뉴얼</span>
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
                TCL 콘크리트도상 타설 전 궤광 변위 방지 및 <strong><span class="term-highlight" onclick="openGlossary('tie_bar')">1,435mm 표준궤 타이바</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('rebar_cover')">철근 피복 40mm</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('signal_clearance')">신호 케이블 150mm 이격</span></strong>을 검수하는 공종입니다. STEP 1부터 STEP 4까지 각 단계에 직관적으로 1:1 매칭되는 <strong>4개의 정밀 2D 기술 도식</strong>을 제공하며, 모든 도식은 클릭 시 화면 전체에 <strong>초대형 고화질 뷰(`openDiagramZoom`)</strong>로 확대됩니다.
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

        <!-- 3. 세부 수행 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-sky-600 pb-2">
                <span class="text-sky-600">3.</span> 4단계 실무 엔지니어링 수행 수칙
            </h2>
            
            <div class="space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 1</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">CP 광학 레벨 측량 & 노반 청소 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            CP 광학 레벨기로 궤도 중심선 및 기준 높이를 정밀 측량하여 오차를 파악하고, 기초 노반 상부의 흙가루 및 이물질을 완벽히 청소합니다. (상기 [도식 1] 참조)
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">1,435mm 타이바 정원 고정 & 오차 조율 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            <span class="term-highlight" onclick="openGlossary('tie_bar')">1,435mm 표준궤 타이바(Tie Bar)를 설치</span>하고, 궤간(+3,-1mm) 및 캔트/수평 오차(&plusmn;2.0mm 이내)를 고정 조율합니다. (상기 [도식 2] 참조)
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">철근 2m 간격 배근 & 피복 40mm 스페이서 고정 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            종/횡방향 철근을 2m 간격으로 배치하고 하부에 <span class="term-highlight" onclick="openGlossary('rebar_cover')">피복 블럭(40mm 이상)을 고정</span>하여 철근 처짐 및 부식을 예방합니다. (상기 [도식 3] 참조)
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">신호 케이블 150mm 이격 & 결속 검측 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            <span class="term-highlight" onclick="openGlossary('signal_clearance')">신호 감선 및 루프 케이블을 철근에서 150mm 이상 이격</span>하고, 결속선 긴장 상태 및 조임 토크를 확인하여 검측서를 승인받습니다. (상기 [도식 4] 참조)
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

# -------------------------------------------------------------------------
# 3. WBS 17 CHECKLIST HTML
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 궤광 및 철근 조립 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-blue: #0284c7;
            --border-color: #cbd5e1;
        }}
        body {{
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            padding: 30px 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        .container {{
            max-width: 950px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 35px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            border-bottom: 2px solid var(--text-primary);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .title {{
            font-size: 1.6rem;
            font-weight: 900;
            margin: 0;
            color: #0369a1;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: #0284c7;
        }}
        .summary-box {{
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #0369a1;
        }}
        table {{
            width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid var(--border-color);
            padding: 14px;
            font-size: 0.92rem;
            text-align: left;
        }}
        th {{
            background: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }}
        .category {{
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            width: 18%;
        }}
        .check-cell {{
            text-align: center;
            vertical-align: middle;
            width: 14%;
            font-weight: bold;
            color: #0369a1;
        }}
        .step-tag {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-right: 4px;
        }}
        {zoom_modal_style}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">[TCL] 궤광 및 철근 조립 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-17 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #0369a1; font-size: 1.05rem; font-weight: 800;">📋 4단계 실시간 O/X 검측 및 시방 기준</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 1,435mm 표준궤 타이바 정원 고정, 철근 피복 40mm 확보, 신호 루프 케이블 150mm 이격 검측 항목을 현장에서 실시간 검측하기 위해 작성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (KDS 47 30 00 공학 규격)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#b45309;">⚠️ 사전 준비<br>(Step 1 레벨측량)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 레벨 측정</span>
                        <strong>[CP 3D 측량]</strong> CP 광학 레벨기로 <span class="term-highlight" onclick="openGlossary('alignment_tolerance')">궤도 중심선 및 기준 높이 오차</span> 검측 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 노반 청소</span>
                        <strong>[기초면 청소]</strong> HBR 노반 상부 이물질 및 돌가루 100% 청소 상태 확인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#0369a1;">📏 타이바 고정<br>(Step 2 정원유지)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 타이바 설치</span>
                        <strong>[1,435mm 정원]</strong> <span class="term-highlight" onclick="openGlossary('tie_bar')">1,435mm 타이바(Tie Bar) 락너트</span> 조임 토크 확인 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 오차 조율</span>
                        <strong>[선형 공차]</strong> 궤간(+3, -1mm) 및 캔트/수평 오차(&plusmn;2.0mm 이내) 확인 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">🏗️ 철근 배근<br>(Step 3 피복확보)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 철근 배근</span>
                        <strong>[2m 배근 간격]</strong> 종/횡방향 철근 2m 간격 배치 및 처짐 방지 용접/결속 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 피복 두께</span>
                        <strong>[피복 블럭]</strong> <span class="term-highlight" onclick="openGlossary('rebar_cover')">하부 콘크리트 피복 두께 &ge; 40mm</span> 스페이서 배치 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#1e3a8a;">📡 신호 검측<br>(Step 4 케이블이격)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 신호 이격</span>
                        <strong>[루프 케이블]</strong> <span class="term-highlight" onclick="openGlossary('signal_clearance')">신호 루프 케이블 배근 이격 &ge; 150mm</span> 이상 확보 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 최종 마감</span>
                        <strong>[검측서 제출]</strong> 철근배근 검측서 및 신호 이격 거리표 감리단 최종 승인 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-17 [TCL] 궤광 및 철근 조립 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force Write Files
force_write(path_std, std_html)
force_write(path_std_alt, std_html)

force_write(path_gui, gui_html)
force_write(path_gui_alt, gui_html)

force_write(path_chk, chk_html)
force_write(path_chk_alt, chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 17 [TCL] 궤광 및 철근 조립!")
