import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folder_with_space = os.path.join(base_dir, "19_[TCL] 콘크리트 타설 및 양생")
folder_no_space = os.path.join(base_dir, "19_[TCL] 콘크리트타설및양생")

os.makedirs(folder_with_space, exist_ok=True)
os.makedirs(folder_no_space, exist_ok=True)

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
    'tcl_strength': {
        title: '🏋️ TCL 콘크리트 강도 (fck ≥ 35 MPa)',
        desc: '트램 차륜 하중 및 열차 반복 주행 응력에 견디기 위해 콘크리트 28일 압축강도를 최소 35 MPa 이상 확보하는 공학 설계 기준입니다.'
    },
    'slump_control': {
        title: '🧪 슬럼프 시험 (≤ 10cm) & 공기량 (4.5 ± 1.5%)',
        desc: '타설 시 콘크리트 유동성 과다에 의한 재료분리를 방지하기 위해 슬럼프 값을 10cm 이하 저슬럼프로 엄격 통제하고 공기량을 시험하는 기준입니다.'
    },
    'gauge_bar_tuning': {
        title: '📏 실시간 궤간척 (Gauge Bar) 캔트 오차 (± 2.0mm)',
        desc: '콘크리트 타설 유체 측압에 의해 레일 궤간이나 캔트가 변형되지 않도록 타설 중 실시간 궤간척으로 측정하여 캔트 오차를 ±2.0mm 이내로 조율하는 수칙입니다.'
    },
    'wet_curing': {
        title: '💧 7일 이상 습윤 양생 & 부직포 포설',
        desc: '콘크리트 수화열 균열을 방지하고 소정의 강도를 발현하기 위해 타설 직후 부직포를 포설하고 최소 7일 이상 수분을 유지 살수하는 양생 수칙입니다.'
    },
    'groove_drain': {
        title: '🌧️ 그루브 드레인 (Groove Drain) 홈 세척 & 치수 검측',
        desc: '매설 궤도 표면 우수 배수를 위해 형성된 그루브 드레인 홈 부분의 콘크리트 잔여물을 세척하고 배수 홈 치수를 정밀 검측하는 과정입니다.'
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
# 1. WBS 19 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 콘크리트 타설 및 양생 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-19 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 / KCS 14 20 10 규격</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[TCL] 콘크리트 타설 및 양생 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"TCL 도상 강도 fck ≥ 35 MPa, 타설 중 실시간 궤간척 캔트 오차 ±2mm 보정 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 본선 TCL 콘크리트도상 타설 시 강도($f_{ck} \ge 35\text{ MPa}$), 슬럼프($\le 10\text{cm}$), 타설 중 실시간 궤간척(Gauge Bar) 캔트 오차($\pm 2.0\text{mm}$) 조율, 고주파 다짐 및 피니셔 멈춤 시 진동 중지, 7일 습윤 양생 및 그루브 드레인 홈 세척 규정을 준수하기 위해 작성되었습니다. (주관: 현장 공사팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">🏋️ 콘크리트 강도 & 품질 관리</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>설계 압축강도:</strong> 28일 압축강도 <strong>fck &ge; 35 MPa</strong> 확보</li>
                        <li><strong>슬럼프 규격:</strong> 타설 슬럼프 값 <strong>&le; 10cm 이하</strong> 저슬럼프 관리</li>
                        <li><strong>공기량 시험:</strong> 굳지 않은 콘크리트 공기량 <strong>4.5 &plusmn; 1.5%</strong> 확인</li>
                        <li><strong>실시간 궤간척:</strong> 타설 중 레일 캔트 오차 <strong>&plusmn;2.0mm 이내</strong> 보정</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">💧 다짐, 습윤 양생 & 배수 홈 세척</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>진동 다짐 제어:</strong> 피니셔 정지 시 고주파 진동 다짐 장비 즉시 중지</li>
                        <li><strong>습윤 양생:</strong> 타설 후 부직포 포설 및 최소 <strong>7일 이상 습윤양생</strong></li>
                        <li><strong>도상 및 홈 세척:</strong> 양생 후 이물질 세척 및 그루브 드레인 홈 치수 검측</li>
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
                <p>✔️ <strong>TCL 콘크리트 품질대장:</strong> 슬럼프(&le;10cm), 공기량(4.5%), 압축강도(35MPa) 현장 시험 성적서</p>
                <p>✔️ <strong>게이지 실시간 보정원지:</strong> 타설 중 궤간척(Gauge Bar) 캔트 오차(&plusmn;2.0mm) 모니터링 대장</p>
                <p>✔️ <strong>습윤 양생 일지:</strong> 7일 습윤양생 부직포 포설 및 살수 체크 기록지</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 19 GUIDELINE HTML (3-Step Procedure Cards with Embedded Visual Diagrams)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 콘크리트 타설 및 양생 수행지침서</title>
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
                <span class="bg-sky-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-19 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">3단계 visual 기술 도식 연동 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[TCL] 콘크리트 타설 및 양생 수행지침서</h1>
            <p class="text-sky-200 mt-2 text-sm sm:text-base">"fck ≥ 35 MPa, 타설 중 실시간 궤간척 캔트 오차 ±2mm 보정 & 7일 습윤양생 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-sky-50 border border-sky-200 p-5 rounded-xl text-xs sm:text-sm text-sky-900 shadow-sm">
            <h4 class="font-bold text-sky-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [TCL] 콘크리트 타설 및 양생 3단계 세부 수행절차 개요
            </h4>
            <p class="leading-relaxed">
                본 수행지침서는 TCL 콘크리트 타설 시 <strong><span class="term-highlight" onclick="openGlossary('tcl_strength')">강도 fck ≥ 35 MPa</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('slump_control')">슬럼프 ≤ 10cm 저슬럼프 타설</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('gauge_bar_tuning')">타설 중 실시간 궤간척 캔트 오차 ±2mm 보정</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('wet_curing')">7일 습윤양생</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('groove_drain')">그루브 드레인 홈 세척</span></strong>을 완수하기 위한 <strong>3단계 체계별 세부 작업 수행절차(사전준비, 본시공, 검사확정)</strong>로 구성됩니다. 각 단계별 카드 내부에 <strong>정밀 2D visual 기술 도식과 대형 확대 모달(`openDiagramZoom`)</strong>이 수록되어 있습니다.
            </p>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-sky-600 pb-2">
                <span class="text-sky-600">1.</span> 4단계 시공 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">직전 측량 & 슬럼프 시험</h4>
                    </div>
                    <p class="text-[11px] text-amber-900 mt-2 font-medium">슬럼프 &le; 10cm & 공기량 4.5%</p>
                </div>

                <div class="bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">실시간 궤간척 모니터링</h4>
                    </div>
                    <p class="text-[11px] text-sky-900 mt-2 font-medium">타설 중 캔트 오차 &plusmn;2.0mm 보정</p>
                </div>

                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">고주파 다짐 & 습윤양생</h4>
                    </div>
                    <p class="text-[11px] text-emerald-900 mt-2 font-medium">7일 이상 부직포 포설 습윤양생</p>
                </div>

                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">도상세척 & 드레인 검측</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">그루브 드레인 배수 홈 검측</p>
                </div>
            </div>
        </div>

        <!-- ★ 2. 3단계 체계별 세부 작업 수행절차 (단계별 정밀 2D visual 도식 수록) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure & Visual Diagrams)
            </h2>
            
            <div class="space-y-8 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-500 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 사전 준비 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">타설 직전 스핀들 측량 & 레미콘 슬럼프 현장 시험</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        콘크리트 타설 직전 스핀들 궤간 및 캔트 최종 상태를 측량하고, 현장 도착 레미콘의 <span class="term-highlight" onclick="openGlossary('slump_control')">슬럼프 값(≤ 10cm)과 공기량(4.5 ± 1.5%)을 시험</span>하여 품질 시방 적합 여부를 확인합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-amber-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 타설 직전 스핀들 측량 & 레미콘 슬럼프(≤ 10cm) 현장 시험 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 500 160" width="100%" height="160" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="160" fill="#f8fafc"/>
                            <rect x="50" y="40" width="160" height="90" fill="#ffffff" stroke="#d97706" stroke-width="1.5" rx="4"/>
                            <text x="130" y="65" font-size="11" font-weight="black" fill="#b45309" text-anchor="middle">레미콘 슬럼프 시험 콘</text>
                            <line x1="80" y1="110" x2="180" y2="110" stroke="#dc2626" stroke-width="3"/>
                            <text x="130" y="100" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">슬럼프 값 &le; 10cm 합격</text>
                            
                            <line x1="260" y1="85" x2="450" y2="85" stroke="#0284c7" stroke-width="4"/>
                            <text x="355" y="70" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">타설 직전 스핀들 궤광 레벨 정밀 측량</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-sky-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-sky-100 text-sky-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 본 시공 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">콘크리트 타설, 실시간 궤간척 모니터링 & 고주파 다짐</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        콘크리트 타설 시 측압에 따른 변위를 막기 위해 <span class="term-highlight" onclick="openGlossary('gauge_bar_tuning')">실시간 궤간척(Gauge Bar)으로 캔트 오차(±2.0mm 이내)를 조율</span>하고, 고주파 다짐을 실시하되 피니셔 정지 시 진동 다짐을 즉시 중지합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-sky-200" onclick="openDiagramZoom('svgStep2_Card', '[본 시공] 타설 중 실시간 궤간척(Gauge Bar) 캔트 오차(±2.0mm) 미세 조율 & 고주파 다짐 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 500 170" width="100%" height="170" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="170" fill="#f8fafc"/>
                            <rect x="40" y="110" width="420" height="45" fill="#cbd5e1"/>
                            <line x1="80" y1="80" x2="420" y2="80" stroke="#0284c7" stroke-width="6"/>
                            <rect x="230" y="70" width="40" height="20" fill="#f59e0b" rx="2"/>
                            <text x="250" y="60" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">실시간 궤간척 (Gauge Bar) 캔트 오차 &plusmn;2.0mm 모니터링</text>
                            
                            <path d="M 360 40 L 370 120 M 365 70 L 380 70 M 365 90 L 380 90" stroke="#dc2626" stroke-width="3"/>
                            <text x="415" y="45" font-size="10" font-weight="black" fill="#dc2626" text-anchor="middle">고주파 다짐 (피니셔 정지 시 진동 즉시 중지)</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 검사 및 확정 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">7일 습윤 양생, 도상 이물질 세척 & 그루브 드레인 검측</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        타설 직후 부직포를 포설하고 <span class="term-highlight" onclick="openGlossary('wet_curing')">최소 7일 이상 습윤 양생</span>을 실시한 후, 양생 완료 시 콘크리트 도상 내 이물질을 세척하고 <span class="term-highlight" onclick="openGlossary('groove_drain')">그루브 드레인(Groove Drain) 배수 홈 치수</span>를 최종 검측 승인합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[검사 마감] 7일 부직포 습윤양생 & 그루브 드레인 배수 홈 세척/치수 검측 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 500 170" width="100%" height="170" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="170" fill="#f8fafc"/>
                            <rect x="40" y="80" width="420" height="60" fill="#94a3b8"/>
                            <rect x="40" y="70" width="420" height="12" fill="#059669"/>
                            <text x="250" y="60" font-size="11" font-weight="black" fill="#059669" text-anchor="middle">부직포 포설 & 7일 이상 지속 습윤 양생 (살수)</text>
                            
                            <!-- 그루브 드레인 홈 -->
                            <rect x="180" y="80" width="25" height="40" fill="#334155"/>
                            <text x="192" y="140" font-size="10" font-weight="black" fill="#0369a1" text-anchor="middle">그루브 드레인 홈 세척 & 치수 검측 합격</text>
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

# -------------------------------------------------------------------------
# 3. WBS 19 CHECKLIST HTML
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 콘크리트 타설 및 양생 체크리스트</title>
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
        <h1 class="title">[TCL] 콘크리트 타설 및 양생 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-19 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #0369a1; font-size: 1.05rem; font-weight: 800;">📋 4단계 실시간 O/X 검측 및 시방 기준</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 TCL 강도(35MPa), 슬럼프(≤10cm), 타설 중 실시간 궤간척 캔트 오차(±2mm), 7일 습윤양생 및 그루브 드레인 홈 세척을 검측하기 위해 작성되었습니다.
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
                <td class="category" style="color:#b45309;">⚠️ 사전 준비<br>(Step 1 레미콘시험)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 스핀들 측량</span>
                        <strong>[직전 측량]</strong> 타설 직전 스핀들 궤간/캔트 레벨 정밀 상태 측량 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 레미콘 시험</span>
                        <strong>[슬럼프 시험]</strong> <span class="term-highlight" onclick="openGlossary('slump_control')">슬럼프 값 &le; 10cm</span> 및 공기량(4.5%) 시험 확인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#0369a1;">📏 타설 & 다짐<br>(Step 2 궤간모니터)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 궤간척 모니터ing</span>
                        <strong>[실시간 보정]</strong> <span class="term-highlight" onclick="openGlossary('gauge_bar_tuning')">타설 중 실시간 궤간척(Gauge Bar) 캔트 오차 &plusmn;2.0mm</span> 미세 조율 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 진동 다짐</span>
                        <strong>[다짐 제어]</strong> 고주파 다짐 실시 및 피니셔 진행 정지 시 진동 다짐 중지 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">💧 양생 & 세척<br>(Step 3 습윤양생)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 습윤 양생</span>
                        <strong>[7일 습윤양생]</strong> <span class="term-highlight" onclick="openGlossary('wet_curing')">부직포 포설 및 최소 7일 이상 습윤 양생</span> 실시 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 홈 세척</span>
                        <strong>[그루브 드레인]</strong> <span class="term-highlight" onclick="openGlossary('groove_drain')">양생 후 도상 세척 및 그루브 드레인 홈 배수 치수</span> 검측 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#1e3a8a;">📡 품질 & 승인<br>(Step 4 품질대장)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 강도 시험</span>
                        <strong>[28일 강도]</strong> TCL 도상 콘크리트 <span class="term-highlight" onclick="openGlossary('tcl_strength')">압축강도 fck &ge; 35 MPa</span> 시험 성적서 확인
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 서명 승인</span>
                        <strong>[품질 대장]</strong> TCL 콘크리트 품질대장 및 게이지 보정원지 감리원 최종 승인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-19 [TCL] 콘크리트 타설 및 양생 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write to both folder directories
for folder_path in [folder_with_space, folder_no_space]:
    std_dir = os.path.join(folder_path, "표준서")
    gui_dir = os.path.join(folder_path, "수행지침")
    chk_dir = os.path.join(folder_path, "체크리스트")
    
    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(gui_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)
    
    # Standard files
    for fname in ["[TCL] 콘크리트 타설 및 양생_표준서.html", "19_[TCL] 콘크리트 타설 및 양생_표준서.html", "[TCL] 콘크리트타설및양생_표준서.html", "19_[TCL] 콘크리트타설및양생_표준서.html"]:
        with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
            f.write(std_html)
            
    # Guideline files
    for fname in ["[TCL] 콘크리트 타설 및 양생_수행지침.html", "19_[TCL] 콘크리트 타설 및 양생_수행지침.html", "[TCL] 콘크리트타설및양생_수행지침.html", "19_[TCL] 콘크리트타설및양생_수행지침.html"]:
        with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
            f.write(gui_html)
            
    # Checklist files
    for fname in ["[TCL] 콘크리트 타설 및 양생_체크리스트.html", "19_[TCL] 콘크리트 타설 및 양생_체크리스트.html", "[TCL] 콘크리트타설및양생_체크리스트.html", "19_[TCL] 콘크리트타설및양생_체크리스트.html"]:
        with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
            f.write(chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 19 [TCL] 콘크리트 타설 및 양생!")
