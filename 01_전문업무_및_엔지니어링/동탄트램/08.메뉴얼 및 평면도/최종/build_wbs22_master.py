import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

# Find all WBS 22 matching folders
wbs22_folders = []
for item in os.listdir(base_dir):
    if item.startswith("22_") or "레일연마" in item or "밀링" in item:
        wbs22_folders.append(os.path.join(base_dir, item))

if not wbs22_folders:
    wbs22_folders = [
        os.path.join(base_dir, "22_[레일연마] 레일연마 or 밀링"),
        os.path.join(base_dir, "22_[레일연마] 레일연마or밀링")
    ]

for f in wbs22_folders:
    os.makedirs(f, exist_ok=True)

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
    'rail_grinding_milling': {
        title: '⚙️ 레일 연마 or 밀링 (Rail Grinding & Milling)',
        desc: '레일 용접 후 발생하는 표면 단차나 잔물결, 녹을 회전 연마석 또는 밀링 컷터로 정밀 절삭하여 선로 평탄성을 확보하고 차륜 승차감 및 레일 수명을 대폭 향상시키는 시방 공법입니다.'
    },
    'flatness_control': {
        title: '📐 레일 마무리면 평탄성 (1m당 ±0.2mm 이내)',
        desc: '레일 주행면 마무리면 1m 기준 직선도 오차를 ±0.2mm 이내로 정밀 연마하여 차량 주행 시 소음 및 궤도 진동을 최소화하는 정량 수칙입니다.'
    },
    'roughness_test': {
        title: '📊 표면 조도 기준 (Ra ≤ 10㎛ 이하)',
        desc: '디지털 표면 조도계로 연마면 미세 거칠기를 실측하여 Ra 10㎛ 이하의 매끈한 거칠기 정밀도를 획정하는 평가 시험입니다.'
    },
    'thermal_stress_cooling': {
        title: '❄️ 절삭유 적절 분사 & 과열 열응력 크랙 방지',
        desc: '연마/밀링 시 고속 마찰열로 인해 레일 금속 표면이 과열 및 경화되는 열응력(Thermal Stress) 및 미세 균열(Micro-crack)을 방지하기 위해 절삭유/냉각수를 최적 분사하는 방지 수칙입니다.'
    },
    'depth_measurement': {
        title: '📏 연마 깊이(절삭량) 압축기 및 선로 실측',
        desc: '연마 완료 후 연마차 센서 및 마이크로미터/디지털 레일 측정 압축기를 설치하여 레일두부 절삭 깊이를 정밀 실측하는 검측 절차입니다.'
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
# 1. WBS 22 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일연마] 레일연마 or 밀링 표준서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-teal-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-teal-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-22 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 / KR C-14030 규격 준수</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일연마] 레일연마 or 밀링 표준서</h1>
            <p class="text-teal-200 mt-2 text-sm sm:text-base">"평탄성 1m당 ±0.2mm, 표면 조도 Ra ≤ 10㎛, 과열 열응력 방지 & 절삭량 정밀 실측 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-teal-50 border border-teal-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-teal-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-teal-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 콘크리트도상 장대레일 시공 완료 후 발생되는 표면 단차 및 요철을 연마차(Grinding Train) 또는 밀링 장비로 정밀 절삭하여 선로 평탄화, 차륜 승차감 개선, 소음 저감 및 레일 수명을 향상시키는 공학 시방 수칙입니다. 1m당 오차 ±0.2mm 이내 밀착, 표면 조도 Ra ≤ 10㎛ 판정, 절삭유 적절 분사를 통한 과열 열응력 크랙 방지를 규정합니다. (주관: 현장 공사팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-teal-600 pb-2">
                <span class="text-teal-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-teal-700 block mb-1">⚙️ 마무리면 평탄성 & 표면 조도 기준</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>평탄성 오차:</strong> 레일 마무리면 1m 기준 직선도 오차 <strong>&plusmn;0.2mm 이내</strong> 밀착</li>
                        <li><strong>표면 조도 (Roughness):</strong> 디지털 조도계 실측 <strong>Ra &le; 10&mu;m 이하</strong> 판정</li>
                        <li><strong>단차 제거:</strong> 레일 용접부 및 이음매 표면 단차 사전 조사 후 100% 연마</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-teal-700 block mb-1">❄️ 과열 열응력 방지 & 연마깊이 실측</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>열응력 방지:</strong> 연마 시 과열에 의한 금속 열응력 크랙 방지용 <strong>절삭유/냉각수 적절 분사</strong></li>
                        <li><strong>연마깊이 실측:</strong> 연마차 센서 및 압축기/마이크로미터 설치로 <strong>절삭량 정밀 실측</strong></li>
                        <li><strong>환경 Risk 관리:</strong> 연마 스파크, 분진, 냉각수 유출 집진 차단막 설치</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 서식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-teal-600 pb-2">
                <span class="text-teal-600">2.</span> 필 수 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-2">
                <p>✔️ <strong>선로 평탄성검사 성적표:</strong> 1m 당 오차 &plusmn;0.2mm 이내 실측 측량 기록지</p>
                <p>✔️ <strong>표면 조도(Ra) 실측 대장:</strong> 조도계 측정 Ra &le; 10&mu;m 합격 검측 성적표</p>
                <p>✔️ <strong>장대레일 연마 장비 점검표:</strong> 연마차/밀링 장비 점검 및 연마깊이(절삭량) 실측 성적서</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 22 GUIDELINE HTML (3-Step Procedure Cards with Embedded Visual Diagrams)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일연마] 레일연마 or 밀링 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-teal-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-teal-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-22 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">레일 연마/밀링 3단계 visual 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일연마] 레일연마 or 밀링 수행지침서</h1>
            <p class="text-teal-200 mt-2 text-sm sm:text-base">"장비 점검, 절삭유 분사, 1m당 ±0.2mm 평탄성, Ra ≤ 10㎛ 조도 실측 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (개념 해설) -->
        <div class="bg-teal-50 border border-teal-200 p-5 rounded-xl text-xs sm:text-sm text-teal-950 shadow-sm space-y-3">
            <h4 class="font-bold text-teal-950 text-base flex items-center gap-2">
                <span>💡</span> [레일연마] 레일 연마 or 밀링(Rail Grinding/Milling) 친절한 개념 해설
            </h4>
            <div class="bg-white p-4 rounded-lg border border-teal-300 font-medium text-slate-900 leading-relaxed">
                ⚙️ <strong>'레일 연마/밀링'이란?</strong><br>
                레일 용접 후 상부에 튀어나온 단차나 표면의 미세 잔물결, 녹을 <strong><span class="term-highlight" onclick="openGlossary('rail_grinding_milling')">연마차 회전 연마석이나 밀링 컷터로 매끈하게 깎아내는 공법</span></strong>입니다. 연마 마찰열로 인한 열응력 크랙을 막기 위해 <strong><span class="term-highlight" onclick="openGlossary('thermal_stress_cooling')">절삭유/냉각수를 적절히 분사</span></strong>하며, 연마 후 <strong><span class="term-highlight" onclick="openGlossary('roughness_test')">표면 조도 Ra ≤ 10㎛</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('flatness_control')">1m 당 평탄도 ±0.2mm 이내</span></strong>를 정밀 측정합니다.
            </div>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-teal-600 pb-2">
                <span class="text-teal-600">1.</span> 4단계 시공 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-teal-50 p-4 rounded-xl border border-teal-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-teal-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">단차 조사 & 장비 점검</h4>
                    </div>
                    <p class="text-[11px] text-teal-900 mt-2 font-medium">용접부 표면 단차 사전 측량</p>
                </div>

                <div class="bg-cyan-50 p-4 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-cyan-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">절삭유 분사 & 연마 주행</h4>
                    </div>
                    <p class="text-[11px] text-cyan-900 mt-2 font-medium">과열 열응력 크랙 100% 방지</p>
                </div>

                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">연마깊이(절삭량) 실측</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">센서 및 마이크로미터 실측</p>
                </div>

                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">조도 & 평탄도 검측 승인</h4>
                    </div>
                    <p class="text-[11px] text-emerald-900 mt-2 font-medium">Ra ≤ 10㎛ & 1m당 ±0.2mm</p>
                </div>
            </div>
        </div>

        <!-- 2. 3단계 체계별 세부 작업 수행절차 (단계별 2D visual 도식 수록) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure & Visual Diagrams)
            </h2>
            
            <div class="space-y-8 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-teal-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-teal-100 text-teal-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 사전 준비 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">장대레일 연마/밀링 장비 점검 & 표면 단차 사전 조사</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        장대레일 구간 연마/밀링 장비의 구동 유압 및 회전 속도를 사전 점검하고, 레일 용접부 및 연결부의 <span class="term-highlight" onclick="openGlossary('rail_grinding_milling')">표면 단차와 미세 요철을 사전 실측 측량</span>합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-teal-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 연마/밀링 장비 점검 & 레일 표면 단차 사전 조사 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 미세 단차 레일 -->
                            <rect x="40" y="85" width="210" height="40" fill="#475569"/>
                            <rect x="250" y="80" width="230" height="45" fill="#475569"/>
                            <line x1="250" y1="50" x2="250" y2="135" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="3,3"/>
                            
                            <text x="250" y="40" font-size="13" font-weight="black" fill="#dc2626" text-anchor="middle">용접부 표면 단차 사전 측량</text>
                            
                            <!-- 측정 자 / 센서 -->
                            <rect x="180" y="70" width="140" height="12" fill="#cbd5e1" stroke="#334155" stroke-width="1.5" rx="2"/>
                            <text x="250" y="155" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">연마/밀링 장비 투입 전 정밀 단차 조사</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-cyan-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-cyan-100 text-cyan-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 본 시공 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">절삭유 적절 분사(열응력 방지) & 연마차 회전 연마 시공</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        연마차(Grinding Train)를 최적 주행속도로 운행하며, 마찰 과열에 의한 열응력 크랙을 방지하기 위해 <span class="term-highlight" onclick="openGlossary('thermal_stress_cooling')">절삭유/냉각수를 적절히 분사</span>하면서 레일두부 상면 및 궤간 측면을 정밀 절삭합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-cyan-200" onclick="openDiagramZoom('svgStep2_Card', '[본 시공] 연마차 회전 연마석 절삭 & 절삭유 적절 분사 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 레일 -->
                            <rect x="40" y="90" width="440" height="40" fill="#475569"/>
                            
                            <!-- 회전 연마석 (Grinding Wheel) -->
                            <circle cx="260" cy="65" r="28" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
                            <text x="260" y="70" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle">연마석</text>
                            
                            <!-- 절삭유 분사 노즐 & 분사선 -->
                            <path d="M 210 40 L 235 65" stroke="#38bdf8" stroke-width="3" stroke-dasharray="2,2"/>
                            <path d="M 310 40 L 285 65" stroke="#38bdf8" stroke-width="3" stroke-dasharray="2,2"/>
                            <text x="260" y="28" font-size="13" font-weight="black" fill="#0284c7" text-anchor="middle">❄️ 절삭유/냉각수 분사 (열응력 크랙 방지)</text>
                            <text x="260" y="155" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">연마차 고속 회전 절삭 시공</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 검사 및 확정 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">표면 조도 Ra ≤ 10㎛ 판정 & 1m당 ±0.2mm 평탄성 검측 승인</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        연마 완료 후 연마 깊이(절삭량)를 실측하고, 디지털 조도계로 <span class="term-highlight" onclick="openGlossary('roughness_test')">표면 조도 Ra ≤ 10㎛ 이하</span> 판정 및 <span class="term-highlight" onclick="openGlossary('flatness_control')">1m 당 오차 ±0.2mm 이내 평탄성</span>을 마이크로미터/선로 검측기로 정밀 측정하여 검측 승인을 받습니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[검사 마감] 디지털 조도계 Ra ≤ 10㎛ 측정 & 1m당 ±0.2mm 마이크로미터 평탄성 검측 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 정밀 연마된 매끈한 레일 -->
                            <rect x="40" y="80" width="440" height="40" fill="#475569"/>
                            <line x1="40" y1="80" x2="480" y2="80" stroke="#38bdf8" stroke-width="3.5"/>
                            
                            <!-- 조도계 센서 (Roughness Tester) -->
                            <rect x="110" y="45" width="90" height="35" fill="#059669" rx="4"/>
                            <text x="155" y="67" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle">Ra ≤ 10㎛</text>
                            <text x="155" y="32" font-size="13" font-weight="black" fill="#059669" text-anchor="middle">표면 조도 측정</text>

                            <!-- 1m 평탄도 측정 바 (±0.2mm) -->
                            <line x1="280" y1="50" x2="440" y2="50" stroke="#0284c7" stroke-width="3"/>
                            <text x="360" y="38" font-size="13" font-weight="black" fill="#0284c7" text-anchor="middle">1m당 &plusmn;0.2mm 평탄도</text>
                            <text x="260" y="155" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">마이크로미터 및 선로 평탄도 검측 승인</text>
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
# 3. WBS 22 CHECKLIST HTML (질문형 어미 "~하였는가?" 100% 적용)
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일연마] 레일연마 or 밀링 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-teal: #0d9488;
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
            color: #0f766e;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: #0d9488;
        }}
        .summary-box {{
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #166534;
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
            color: #0d9488;
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
        <h1 class="title">[레일연마] 레일연마 or 밀링 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-22 | 레일 연마/밀링 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #15803d; font-size: 1.05rem; font-weight: 800;">📋 레일 연마/밀링 O/X 필수 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 장비 점검, 절삭유 분사(열응력 방지), 연마깊이(절삭량) 측정, 표면 조도 Ra ≤ 10㎛ 및 마무리면 1m당 ±0.2mm 평탄성 검측을 위해 작성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (KDS 47 30 00 / KR C-14030 규격)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#0f766e;">⚠️ 사전 준비<br>(Step 1 단차조사)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#ccfbf1; color:#0f766e;">Step 1. 단차 조사</span>
                        <strong>[표면 조사]</strong> 장대레일 구간 용접부 및 이음매 표면 단차를 사전 실측 조사**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#ccfbf1; color:#0f766e;">Step 1. 장비 점검</span>
                        <strong>[장비 점검]</strong> <span class="term-highlight" onclick="openGlossary('rail_grinding_milling')">연마차/밀링 장비 구동 상태</span> 및 투입 스케줄을 확인**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#0284c7;">⚙️ 본 시공<br>(Step 2 절삭유분사)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 절삭유 분사</span>
                        <strong>[열응력 방지]</strong> 과열에 의한 레일 열응력 크랙 방지용 <span class="term-highlight" onclick="openGlossary('thermal_stress_cooling')">절삭유/냉각수를 적절히 분사</span>**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 환경 관리</span>
                        <strong>[분진 집진]</strong> 연마 작업 시 발생 스파크, 분진, 냉각수 유출 방지 조치**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">📡 검사 마감<br>(Step 3 조도 & 평탄도)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 표면 조도</span>
                        <strong>[조도 판정]</strong> 디지털 조도계 측정 결과 <span class="term-highlight" onclick="openGlossary('roughness_test')">표면 조도 Ra &le; 10&mu;m 이하</span>로 판정**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 평탄성 검측</span>
                        <strong>[직선도 검측]</strong> 마무리면 1m 기준 직선도 오차 <strong>&plusmn;0.2mm 이내</strong>로 정밀 밀착 연마**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 절삭량 실측</span>
                        <strong>[깊이 실측]</strong> <span class="term-highlight" onclick="openGlossary('depth_measurement')">연마차 압축기 및 마이크로미터</span>로 연마깊이(절삭량)를 실측**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-22 [레일연마] 레일연마 or 밀링 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write to all WBS 22 folder variants
for folder_path in wbs22_folders:
    std_dir = os.path.join(folder_path, "표준서")
    gui_dir = os.path.join(folder_path, "수행지침")
    chk_dir = os.path.join(folder_path, "체크리스트")
    
    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(gui_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)
    
    # Standard files
    for fname in ["[레일연마] 레일연마 or 밀링_표준서.html", "22_[레일연마] 레일연마 or 밀링_표준서.html", "[레일연마] 레일연마or밀링_표준서.html", "22_[레일연마] 레일연마or밀링_표준서.html"]:
        with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
            f.write(std_html)
            
    # Guideline files
    for fname in ["[레일연마] 레일연마 or 밀링_수행지침.html", "22_[레일연마] 레일연마 or 밀링_수행지침.html", "[레일연마] 레일연마or밀링_수행지침.html", "22_[레일연마] 레일연마or밀링_수행지침.html"]:
        with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
            f.write(gui_html)
            
    # Checklist files
    for fname in ["[레일연마] 레일연마 or 밀링_체크리스트.html", "22_[레일연마] 레일연마 or 밀링_체크리스트.html", "[레일연마] 레일연마or밀링_체크리스트.html", "22_[레일연마] 레일연마or밀링_체크리스트.html"]:
        with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
            f.write(chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 22 [레일연마] 레일연마 or 밀링!")
