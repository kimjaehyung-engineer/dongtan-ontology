import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folder_with_space = os.path.join(base_dir, "20_[레일용접] 가스 압접")
folder_no_space = os.path.join(base_dir, "20_[레일용접] 가스압접")

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
    'en14587_std': {
        title: '📜 EN 14587 국제 레일 용접 규격',
        desc: '유럽 표준 레일 가스 압접(Gas Pressure Welding) 및 플래시 버트 용접 시방 규격으로, 자동 가열 및 가압 제어를 통해 높은 결합 강도를 보장합니다.'
    },
    'gas_heating_1200': {
        title: '🔥 레일 단부 1,200℃ 적열 가열 & 유압 압접',
        desc: '산소-아세틸렌 다공 링 토치를 이용하여 레일 접속 단면을 1,200℃ 이상 적열 상태로 급속 가열한 후, 강력한 유압 압축력을 가해 금속 원자를 소결 접합하는 기술입니다.'
    },
    'burr_hot_trimming': {
        title: '✂️ 버 (Burr/Flange Extrusion) 핫 쉐어링 전단',
        desc: '유압 압접 직후 쇳덩이가 붉게 달궈진 적열 상태일 때, 용접부 바깥으로 밀려 나온 불순물 지느러미(Burr)를 핫 쉐어링 컷터로 깔끔하게 절단 제거하는 과정입니다.'
    },
    'slow_cooling_cover': {
        title: '🛡️ 용접부 급랭 방지 보온 덮개 설치',
        desc: '가스 압접 직후 바람이나 외기에 의해 용접부가 갑자기 식으면 조직이 딱딱하고 부러지기 쉬운 마르텐사이트 변태가 일어납니다. 이를 막기 위해 보온 커버를 씌워 서서히 식히는 기술입니다.'
    },
    'ut_testing': {
        title: '📡 UT 초음파 비파괴검사 (Ultrasonic Testing)',
        desc: '레일 용접부 내부에 눈에 보이지 않는 미세 기포나 융합 불량 등 결함이 존재하는지 초음파 탐상 장치로 100% 검측하여 안전성을 입증하는 성적서입니다.'
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
# 1. WBS 20 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일용접] 가스 압접 표준서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-red-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-red-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-20 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">EN 14587 / KR C-14030 규격 준수</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일용접] 가스 압접 표준서</h1>
            <p class="text-red-200 mt-2 text-sm sm:text-base">"EN 14587 규격 준수, 레일 단부 1,200℃ 가열 유압 압접 & 1m당 ±0.2mm 정밀 연마 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-red-50 border border-red-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-red-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-red-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 본선 장대레일 제작을 위해 가스 압접 용접기에서 레일 단부를 1,200℃ 이상 가열한 후 강한 유압 압력을 가하여 레일을 접합하는 가스 압접 시방 수칙입니다. EN 14587 국제 규격 준수, 적열 상태 버(Burr) 핫 쉐어링, 급랭 방지 보온 덮개 설치, 1m 당 ±0.2mm 정밀 연마 및 UT 비파괴검사를 규정합니다. (주관: 현장 공사팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-red-600 pb-2">
                <span class="text-red-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-red-700 block mb-1">🔥 가열, 유압 압접 & 핫 쉐어링</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>국제 용접 규격:</strong> <strong>EN 14587</strong> 프로그램 자동 제어 준수</li>
                        <li><strong>단부 가열 온도:</strong> 산소-아세틸렌 링 토치 <strong>1,200℃ 이상</strong> 적열 가열</li>
                        <li><strong>유압 압축 가압:</strong> 유압 클램프 강력 압축 가압 수칙 적용</li>
                        <li><strong>버(Burr) 핫 쉐어링:</strong> 적열 상태일 때 버 핫 쉐어링 컷터로 즉시 전단</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-red-700 block mb-1">🛡️ 급랭 방지, 정밀 연마 & UT 검사</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>급랭 방지 덮개:</strong> 취성 마르텐사이트 변태 방지 보온 커버 포설</li>
                        <li><strong>용접부 직선도:</strong> 1m 당 직선도 <strong>&plusmn;0.2mm 이내</strong> 정밀 연마</li>
                        <li><strong>비파괴 탐상검사:</strong> <strong>UT 초음파 탐상검사 100%</strong> 실시 및 보고서 결재</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 서식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-red-600 pb-2">
                <span class="text-red-600">2.</span> 필 수 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-2">
                <p>✔️ <strong>가스압접 시공성적표:</strong> 가열 온도(1,200℃), 유압 압력, 버 전단 데이터 일지</p>
                <p>✔️ <strong>UT 비파괴보고서:</strong> 초음파 탐상 비파괴 시험 100% 합격 검사 보고서</p>
                <p>✔️ <strong>용접부 직선도 검측대장:</strong> 1m 당 오차 &plusmn;0.2mm 이내 정밀 연마 측량표</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 20 GUIDELINE HTML (3-Step Procedure Cards with Embedded Visual Diagrams)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일용접] 가스 압접 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-red-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-red-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-20 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">EN 14587 가스 압접 3단계 visual 기술 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일용접] 가스 압접 수행지침서</h1>
            <p class="text-red-200 mt-2 text-sm sm:text-base">"EN 14587 1,200℃ 가열 유압 압접, 버 핫 쉐어링, 1m당 ±0.2mm 연마 & UT 100% 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (가스 압접 개념 포함) -->
        <div class="bg-red-50 border border-red-200 p-5 rounded-xl text-xs sm:text-sm text-red-950 shadow-sm space-y-3">
            <h4 class="font-bold text-red-950 text-base flex items-center gap-2">
                <span>💡</span> [레일용접] 가스 압접(Gas Pressure Welding) 개념 해설
            </h4>
            <div class="bg-white p-3 rounded-lg border border-red-300 font-medium text-slate-900">
                🔥 <strong>'레일 가스 압접'이란?</strong><br>
                레일 양 끝 접속 단면을 산소-아세틸렌 링 토치로 <strong><span class="term-highlight" onclick="openGlossary('gas_heating_1200')">1,200℃ 이상 벌겋게 달군 뒤</span></strong> 유압 장치로 꽉 짓눌러 하나로 눌러붙이는 공법입니다. 눌려 튀어나온 불순물 쇳덩이(Burr)는 <strong><span class="term-highlight" onclick="openGlossary('burr_hot_trimming')">적열 상태일 때 핫 쉐어링 컷터로 싹 전단</span></strong>하고, <strong><span class="term-highlight" onclick="openGlossary('slow_cooling_cover')">보온 덮개</span></strong>를 씌워 식힌 후 <strong><span class="term-highlight" onclick="openGlossary('ut_testing')">UT 초음파 탐상검사를 100%</span></strong> 실시합니다.
            </div>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-red-600 pb-2">
                <span class="text-red-600">1.</span> 4단계 시공 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">단면 청소 & 클램프 고정</h4>
                    </div>
                    <p class="text-[11px] text-amber-900 mt-2 font-medium">단면 50mm 녹/기름 100% 제거</p>
                </div>

                <div class="bg-red-50 p-4 rounded-xl border border-red-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">1,200℃ 가열 & 유압 압접</h4>
                    </div>
                    <p class="text-[11px] text-red-900 mt-2 font-medium">유압 압축 & 버 핫 쉐어링 전단</p>
                </div>

                <div class="bg-orange-50 p-4 rounded-xl border border-orange-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-orange-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">급랭 방지 & 적열 교정</h4>
                    </div>
                    <p class="text-[11px] text-orange-900 mt-2 font-medium">보온 덮개 포설 서냉 유지</p>
                </div>

                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">정밀 연마 & UT 탐상검사</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">1m당 &plusmn;0.2mm 연마 & UT 100%</p>
                </div>
            </div>
        </div>

        <!-- 2. 3단계 체계별 세부 작업 수행절차 (단계별 정밀 2D visual 도식 수록) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure & Visual Diagrams)
            </h2>
            
            <div class="space-y-8 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-500 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 사전 준비 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 접속 단면 50mm Grinding 연마 청소 & 유압 클램프 고정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        용접 불량 및 스케일 혼입을 방지하기 위해 레일 접속 단부 50mm 영역의 녹, 스케일, 기름을 Grinder로 광택면이 나올 때까지 100% 제거하고, <span class="term-highlight" onclick="openGlossary('en14587_std')">EN 14587 규격 유압 클램프</span>에 레일을 고정합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-amber-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 레일 단면 50mm Grinding 연마 & 유압 클램프 고정 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 좌측 레일 단부 -->
                            <rect x="40" y="75" width="180" height="40" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            <rect x="170" y="75" width="50" height="40" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
                            <text x="130" y="60" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">50mm 광택 Grinding 연마</text>
                            
                            <!-- 우측 레일 단부 -->
                            <rect x="300" y="75" width="180" height="40" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            <rect x="300" y="75" width="50" height="40" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
                            
                            <!-- 유압 고정 클램프 -->
                            <rect x="20" y="125" width="480" height="35" rx="6" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                            <text x="260" y="147" font-size="12" font-weight="black" fill="#1e293b" text-anchor="middle">EN 14587 유압 고정 클램프 (유압 압력 센서 세팅)</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-red-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-red-100 text-red-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 본 시공 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">1,200℃ 산소-아세틸렌 토치 가열, 유압 압접 & 핫 쉐어링</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        다공 링 토치로 레일 단부를 <span class="term-highlight" onclick="openGlossary('gas_heating_1200')">1,200℃ 이상 적열 상태로 가열</span>한 후 강력한 유압 압축력을 가해 접합하며, 접합 직후 붉게 달궈진 적열 상태일 때 <span class="term-highlight" onclick="openGlossary('burr_hot_trimming')">버(Burr) 핫 쉐어링 컷터로 즉시 전단 제거</span>합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-red-200" onclick="openDiagramZoom('svgStep2_Card', '[본 시공] 1,200℃ 가속 산소-아세틸렌 링 토치 가열 & 적열 버(Burr) 핫 쉐어링 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 520 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="220" fill="#f8fafc"/>
                            
                            <!-- 가열 압접 레일 -->
                            <rect x="40" y="85" width="200" height="45" fill="#475569"/>
                            <rect x="280" y="85" width="200" height="45" fill="#475569"/>
                            
                            <!-- 1,200℃ 적열 용접부 -->
                            <rect x="235" y="75" width="50" height="65" fill="#ef4444" rx="4"/>
                            <text x="260" y="60" font-size="12" font-weight="black" fill="#dc2626" text-anchor="middle">🔥 1,200℃ 적열 가열 & 유압 압접</text>

                            <!-- 산소-아세틸렌 링 토치 불꽃 -->
                            <circle cx="260" cy="107" r="45" fill="none" stroke="#f59e0b" stroke-width="4" stroke-dasharray="8,4"/>
                            
                            <!-- 핫 쉐어링 컷터 -->
                            <path d="M 260 25 L 275 65 L 245 65 Z" fill="#b45309"/>
                            <text x="260" y="20" font-size="11" font-weight="black" fill="#b45309" text-anchor="middle">버(Burr) 핫 쉐어링 컷터 즉시 전단</text>

                            <!-- 유압 가압 화살표 -->
                            <polygon points="20,107 40,95 40,119" fill="#dc2626"/>
                            <polygon points="500,107 480,95 480,119" fill="#dc2626"/>
                            <text x="260" y="165" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">강력 유압 고압 압축 (P &ge; 35 MPa)</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 검사 및 확정 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">급랭 방지 보온 덮개 서냉, 1m당 ±0.2mm 연마 & UT 탐상검사</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        용접 직후 마르텐사이트 취성 조직 생성을 막기 위해 <span class="term-highlight" onclick="openGlossary('slow_cooling_cover')">보온 덮개를 씌워 서냉</span>시키고, 용접부 직선도를 1m 당 오차 ±0.2mm 이내로 정밀 연마한 후 <span class="term-highlight" onclick="openGlossary('ut_testing')">UT 초음파 탐상검사 100%</span>를 받아 최종 감리원 결재를 획득합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[검사 마감] 급랭 방지 보온 덮개 서냉, 1m당 ±0.2mm 정밀 연마 & UT 탐상검사 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="220" fill="#f8fafc"/>
                            
                            <!-- 서냉 및 연마 레일 -->
                            <rect x="40" y="80" width="440" height="40" fill="#475569"/>
                            
                            <!-- 급랭 방지 보온 덮개 커버 -->
                            <rect x="200" y="65" width="120" height="70" fill="#f59e0b" stroke="#b45309" stroke-width="2" rx="4"/>
                            <text x="260" y="105" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">보온 덮개 (서냉 유지)</text>

                            <!-- UT 초음파 탐상 센서 -->
                            <circle cx="100" cy="80" r="16" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
                            <text x="100" y="84" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">UT</text>
                            <text x="100" y="55" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">UT 초음파 비파괴검사 100%</text>

                            <!-- 직선도 1m ±0.2mm 자 -->
                            <line x1="340" y1="60" x2="460" y2="60" stroke="#059669" stroke-width="3"/>
                            <text x="400" y="48" font-size="11" font-weight="black" fill="#059669" text-anchor="middle">직선도 1m당 &plusmn;0.2mm 연마</text>
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
# 3. WBS 20 CHECKLIST HTML
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일용접] 가스 압접 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
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
            color: #991b1b;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: #dc2626;
        }}
        .summary-box {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #991b1b;
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
            color: #dc2626;
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
        <h1 class="title">[레일용접] 가스 압접 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-20 | 레일 용접 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #991b1b; font-size: 1.05rem; font-weight: 800;">📋 EN 14587 레일 가스 압접 O/X 필수 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 레일 단면 50mm 연마, 1,200℃ 적열 가열, 유압 압접, 버 핫 쉐어링, 급랭 방지 덮개, 1m 당 오차 ±0.2mm 연마 및 UT 100% 탐상을 검측하기 위해 작성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (EN 14587 / KR C-14030 규격)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#b45309;">⚠️ 사전 준비<br>(Step 1 단면연마)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 단면 청소</span>
                        <strong>[Grinding 연마]</strong> 레일 접속 단면 50mm 이내 녹, 스케일, 기름 100% 광택 연마 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 클램프 고정</span>
                        <strong>[유압 고정]</strong> <span class="term-highlight" onclick="openGlossary('en14587_std')">EN 14587 규격</span> 압접기 유압 클램프 축 선형 정밀 고정 확인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#991b1b;">🔥 가열 & 압접<br>(Step 2 유압가압)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef2f2; color:#991b1b;">Step 2. 1,200℃ 가열</span>
                        <strong>[적열 가열]</strong> <span class="term-highlight" onclick="openGlossary('gas_heating_1200')">산소-아세틸렌 링 토치 1,200℃ 적열 가열</span> & 유압 고압 압축 체결
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef2f2; color:#991b1b;">Step 2. 버 쉐어링</span>
                        <strong>[핫 쉐어링]</strong> <span class="term-highlight" onclick="openGlossary('burr_hot_trimming')">적열 상태일 때 버(Burr) 핫 쉐어링 컷터</span> 전단 제거 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#c2410c;">🛡️ 급랭방지<br>(Step 3 서냉보온)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#ffedd5; color:#9a3412;">Step 3. 보온 덮개</span>
                        <strong>[서냉 유지]</strong> <span class="term-highlight" onclick="openGlossary('slow_cooling_cover')">마르텐사이트 방지 급랭 방지 보온 덮개</span> 설치 서냉 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#ffedd5; color:#9a3412;">Step 3. 적열 교정</span>
                        <strong>[굴곡 교정]</strong> 용접부 적열 상태 중 레일 굴곡/비틀림 정밀 1차 교정 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#1e3a8a;">📡 연마 & UT<br>(Step 4 비파괴)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 정밀 연마</span>
                        <strong>[직선도 검측]</strong> 용접부 레일 직선도 1m 당 오차 <strong>&plusmn;0.2mm 이내</strong> 정밀 연마 확인
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. UT 탐상</span>
                        <strong>[비파괴 검사]</strong> <span class="term-highlight" onclick="openGlossary('ut_testing')">UT 초음파 탐상 비파괴검사 100%</span> 실시 및 시공성적표 결재
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-20 [레일용접] 가스 압접 마스터 체크리스트
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
    for fname in ["[레일용접] 가스 압접_표준서.html", "20_[레일용접] 가스 압접_표준서.html", "[레일용접] 가스압접_표준서.html", "20_[레일용접] 가스압접_표준서.html"]:
        with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
            f.write(std_html)
            
    # Guideline files
    for fname in ["[레일용접] 가스 압접_수행지침.html", "20_[레일용접] 가스 압접_수행지침.html", "[레일용접] 가스압접_수행지침.html", "20_[레일용접] 가스압접_수행지침.html"]:
        with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
            f.write(gui_html)
            
    # Checklist files
    for fname in ["[레일용접] 가스 압접_체크리스트.html", "20_[레일용접] 가스 압접_체크리스트.html", "[레일용접] 가스압접_체크리스트.html", "20_[레일용접] 가스압접_체크리스트.html"]:
        with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
            f.write(chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 20 [레일용접] 가스 압접!")
