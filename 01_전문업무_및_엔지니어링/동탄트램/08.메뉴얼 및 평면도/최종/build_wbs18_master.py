import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folder_with_space = os.path.join(base_dir, "18_[TCL] 거푸집 설치")
folder_no_space = os.path.join(base_dir, "18_[TCL] 거푸집설치")

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
    'support_anchor': {
        title: '⚓ 서포트 앵커 고정 (W = 1.0m 간격)',
        desc: '콘크리트 타설 시 발생하는 유체 측압 및 전단 응력에 견디기 위해 강재 거푸집 지지대를 노반 바닥면에 1.0m 간격으로 앵커링 고정하는 수칙입니다.'
    },
    'form_tolerance': {
        title: '📐 거푸집 수평/수직 지점 변위 (± 2.0mm 이내)',
        desc: '거푸집의 면 비틀림이나 전도 변위를 방지하기 위해 정밀 턴버클 및 측량기로 수평도 및 수직도를 오차 ±2.0mm 이내로 엄격 통제하는 시방 규격입니다.'
    },
    'release_agent': {
        title: '🧪 친환경 박리제 균일 도포 & 청소',
        desc: '콘크리트 경화 후 거푸집 탈형 시 표면 뜯김을 방지하고 매끄러운 단면을 형성하기 위해 거푸집 면 이물질 청소 후 친환경 박리제를 미세막으로 균일 분사하는 수칙입니다.'
    },
    'joint_packing': {
        title: '🛡️ 거푸집 이음매 틈새 누수 패킹',
        desc: '콘크리트 타설 시 슬러리(시멘트 풀)가 틈새로 유출되는 곰보 현상을 방지하기 위해 거푸집 조인트 이음매에 고지수성 테이프나 지수 폼을 패킹하는 공법입니다.'
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
# 1. WBS 18 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 거푸집 설치 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-18 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 / KCS 14 20 12 규격</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[TCL] 거푸집 설치 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"타설 측압 대비 서포트 앵커 W=1.0m 고정 및 거푸집 변위 ±2mm 이내 통제 시방서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 본선 TCL(Track Concrete Layer) 콘크리트도상 타설 시 강재 거푸집 설치, 서포트 앵커($W = 1.0\text{m}$) 고정, 변위 통제($\pm 2\text{mm}$ 이내), 박리제 균일 도포, 누수 방지 패킹 및 안전 통로 확보 수칙을 규정합니다. (주관: 현장 공사팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">⚓ 서포트 앵커 & 지지대 고정</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>앵커 고정 간격:</strong> 타설 측압 대비 서포트 앵커 <strong>W = 1.0m 간격</strong> 고정</li>
                        <li><strong>강재 거푸집:</strong> 변위 방지형 고강도 강재 거푸집(Steel Form) 전면 반영</li>
                        <li><strong>안전 식별장치:</strong> 작업자 통로 지지대에 넘어짐 방지 식별 띠(Safety Strip) 설치</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">📐 허용 공차 & 누수 방지 규격</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>허용 공차:</strong> 거푸집 수평 및 수직 지점 변위 <strong>&plusmn;2.0mm 이내</strong> 통제</li>
                        <li><strong>친환경 박리제:</strong> 면 이물질 완전 청소 후 친환경 박리제 균일 미세막 도포</li>
                        <li><strong>이음매 패킹:</strong> 이음매 틈새 콘크리트 페이스트 누수 방지 지수 폼 패킹</li>
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
                <p>✔️ <strong>거푸집설치 대조표:</strong> 서포트 앵커 간격(1.0m) 및 수평/수직 변위(&plusmn;2.0mm) 실측서</p>
                <p>✔️ <strong>박리제 검사결과서:</strong> 환경 친화 박리제 도포 상태 및 도출 시험 성적서</p>
                <p>✔️ <strong>거푸집 선형 검측표:</strong> 감리원 입회 거푸집 수직도/수평도 최종 검측 승인서</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 18 GUIDELINE HTML (Single Clean 4-Step Architecture)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 거푸집 설치 수행지침서</title>
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
                <span class="bg-sky-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-18 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">중복 없는 4단계 단일 통일 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[TCL] 거푸집 설치 수행지침서</h1>
            <p class="text-sky-200 mt-2 text-sm sm:text-base">"4단계 시공 프로세스 (1:1 기술 도식 & 상세 엔지니어링 수행 가이드)"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-sky-50 border border-sky-200 p-5 rounded-xl text-xs sm:text-sm text-sky-900 shadow-sm">
            <h4 class="font-bold text-sky-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [TCL] 거푸집 설치 4단계 단일 체계 개요
            </h4>
            <p class="leading-relaxed">
                본 수행지침서는 TCL 콘크리트도상 타설 전 거푸집 변위 방지 및 <strong><span class="term-highlight" onclick="openGlossary('support_anchor')">서포트 앵커 W=1.0m 간격 고정</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('form_tolerance')">수평/수직 변위 오차 ±2mm 이내 통제</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('release_agent')">친환경 박리제 도포</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('joint_packing')">이음매 누수 패킹</span></strong>을 완수하기 위한 중복 없는 <strong>4단계(STEP 1 ~ STEP 4)</strong> 단일 수칙으로 구성됩니다. 각 단계별 <strong>1:1 매칭 2D 기술 도식과 상세 설명</strong>을 연동합니다.
            </p>
        </div>

        <!-- 1. 4단계 마스터 흐름 요약 (Flow Overview) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-sky-600 pb-2">
                <span class="text-sky-600">1.</span> 4단계 시공 마스터 흐름 (Single 4-Step Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">먹줄측량 & 앵커타공</h4>
                    </div>
                    <p class="text-[11px] text-amber-900 mt-2 font-medium">앵커 간격 W=1.0m 타공</p>
                </div>

                <div class="bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">강재거푸집 & 변위조율</h4>
                    </div>
                    <p class="text-[11px] text-sky-900 mt-2 font-medium">수평/수직 오차 &plusmn;2.0mm</p>
                </div>

                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">박리제도포 & 누수패킹</h4>
                    </div>
                    <p class="text-[11px] text-emerald-900 mt-2 font-medium">친환경 박리제 & 폼 코킹</p>
                </div>

                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">안전식별 & 선형검측</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">식별 띠 설치 & 최종 승인</p>
                </div>
            </div>
        </div>

        <!-- 2. 4단계별 1:1 매칭 2D 기술 도식 및 상세 엔지니어링 수행 가이드 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-sky-600 pb-2">
                <span class="text-sky-600">2.</span> 4단계별 정밀 2D 기술 도식 & 상세 엔지니어링 수행 가이드
            </h2>
            
            <div class="space-y-10">
                <!-- ==================== STEP 1 ==================== -->
                <div class="bg-white p-6 rounded-2xl border border-amber-200 shadow-md space-y-5">
                    <div class="flex items-center justify-between border-b border-amber-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-amber-500 text-white font-black text-sm px-3 py-1 rounded-lg">STEP 1</span>
                            <h3 class="text-lg font-bold text-slate-900">먹줄 선형 측량 & 서포트 앵커 타공 (W=1.0m 간격)</h3>
                        </div>
                        <span class="bg-amber-100 text-amber-900 text-xs font-bold px-2.5 py-1 rounded-full">사전 준비 단계</span>
                    </div>

                    <!-- 2D SVG 도식 (Light Theme & Click Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-amber-200" onclick="openDiagramZoom('svgDiagram18_STEP1', '[도식 1] CP 3D 선형 먹줄 배직 & 서포트 앵커 타공(1.0m 간격) 도면')">
                        <svg id="svgDiagram18_STEP1" viewBox="0 0 500 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="180" fill="#f8fafc"/>
                            <rect x="30" y="130" width="440" height="35" fill="#cbd5e1" stroke="#334155" stroke-width="1.5"/>
                            <text x="250" y="152" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">HBR 기초 콘크리트 버림 바닥층</text>
                            <line x1="40" y1="130" x2="460" y2="130" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,3"/>
                            <text x="250" y="122" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">3D 먹줄 거푸집 선형 기준선</text>
                            
                            <circle cx="100" cy="130" r="6" fill="#0284c7"/>
                            <circle cx="250" cy="130" r="6" fill="#0284c7"/>
                            <circle cx="400" cy="130" r="6" fill="#0284c7"/>
                            <line x1="100" y1="130" x2="250" y2="130" stroke="#0284c7" stroke-width="3"/>
                            <line x1="250" y1="130" x2="400" y2="130" stroke="#0284c7" stroke-width="3"/>
                            <text x="175" y="110" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">앵커 타공 간격 W = 1.0m</text>
                            <text x="325" y="110" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">W = 1.0m</text>
                        </svg>
                    </div>

                    <!-- 상세 엔지니어링 수행 설명 -->
                    <div class="bg-amber-50 p-4 rounded-xl border border-amber-100 text-xs sm:text-sm text-amber-950 space-y-1.5">
                        <h4 class="font-bold text-amber-900 text-sm">📋 STEP 1 엔지니어링 상세 수행 수칙</h4>
                        <ul class="list-disc pl-5 space-y-1 text-slate-700">
                            <li><strong>선형 먹줄 배직:</strong> CP 광파 측량 데이터를 기반으로 기초 콘크리트 노반 표면에 거푸집 설치 중심선 먹줄을 정밀 배직합니다.</li>
                            <li><strong>서포트 앵커 타공:</strong> 타설 측압에 대항하기 위해 <span class="term-highlight" onclick="openGlossary('support_anchor')">서포트 앵커를 1.0m 간격으로 뚫고</span> 노반 가루를 청소합니다.</li>
                        </ul>
                    </div>
                </div>

                <!-- ==================== STEP 2 ==================== -->
                <div class="bg-white p-6 rounded-2xl border border-sky-200 shadow-md space-y-5">
                    <div class="flex items-center justify-between border-b border-sky-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-sky-500 text-white font-black text-sm px-3 py-1 rounded-lg">STEP 2</span>
                            <h3 class="text-lg font-bold text-slate-900">강재 거푸집 거치 & 수평/수직 변위 조율 (오차 ±2.0mm)</h3>
                        </div>
                        <span class="bg-sky-100 text-sky-900 text-xs font-bold px-2.5 py-1 rounded-full">본 시공 단계</span>
                    </div>

                    <!-- 2D SVG 도식 (Light Theme & Click Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-sky-200" onclick="openDiagramZoom('svgDiagram18_STEP2', '[도식 2] 강재 거푸집 수평/수직 지점 변위(±2.0mm 이내) 턴버클 조율 도면')">
                        <svg id="svgDiagram18_STEP2" viewBox="0 0 500 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="180" fill="#f8fafc"/>
                            <rect x="40" y="145" width="420" height="25" fill="#cbd5e1"/>
                            <rect x="120" y="35" width="20" height="110" fill="#475569"/>
                            <line x1="140" y1="75" x2="320" y2="145" stroke="#0284c7" stroke-width="4"/>
                            <rect x="220" y="100" width="20" height="15" fill="#f59e0b"/>
                            <circle cx="320" cy="145" r="7" fill="#0369a1"/>
                            <text x="210" y="55" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">강재 거푸집 (Steel Form)</text>
                            <text x="320" y="95" font-size="11" font-weight="bold" fill="#d97706" text-anchor="middle">턴버클 수직/수평 조율기</text>
                            <text x="320" y="170" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">변위 통제 허용 오차 &plusmn;2.0mm 이내</text>
                        </svg>
                    </div>

                    <!-- 상세 엔지니어링 수행 설명 -->
                    <div class="bg-sky-50 p-4 rounded-xl border border-sky-100 text-xs sm:text-sm text-sky-950 space-y-1.5">
                        <h4 class="font-bold text-sky-900 text-sm">📋 STEP 2 엔지니어링 상세 수행 수칙</h4>
                        <ul class="list-disc pl-5 space-y-1 text-slate-700">
                            <li><strong>강재 거푸집 안착:</strong> 고강도 강재 거푸집(Steel Form)을 먹줄 선형에 맞춰 조립 안착합니다.</li>
                            <li><strong>변위 오차 조율:</strong> 턴버클 및 서포트로 <span class="term-highlight" onclick="openGlossary('form_tolerance')">거푸집 수평/수직 지점 변위를 &plusmn;2.0mm 이내</span>로 정밀 조율 고정합니다.</li>
                        </ul>
                    </div>
                </div>

                <!-- ==================== STEP 3 ==================== -->
                <div class="bg-white p-6 rounded-2xl border border-emerald-200 shadow-md space-y-5">
                    <div class="flex items-center justify-between border-b border-emerald-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-emerald-600 text-white font-black text-sm px-3 py-1 rounded-lg">STEP 3</span>
                            <h3 class="text-lg font-bold text-slate-900">친환경 박리제 균일 도포 & 이음매 틈새 누수 패킹</h3>
                        </div>
                        <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-2.5 py-1 rounded-full">본 시공 단계</span>
                    </div>

                    <!-- 2D SVG 도식 (Light Theme & Click Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgDiagram18_STEP3', '[도식 3] 친환경 박리제 미세 분사 & 거푸집 이음매 콘크리트 누수 방지 패킹 도면')">
                        <svg id="svgDiagram18_STEP3" viewBox="0 0 500 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="180" fill="#f8fafc"/>
                            <rect x="150" y="30" width="200" height="110" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                            <rect x="152" y="32" width="196" height="106" fill="#e0f2fe" opacity="0.6"/>
                            <line x1="250" y1="30" x2="250" y2="140" stroke="#dc2626" stroke-width="4"/>
                            <rect x="245" y="30" width="10" height="110" fill="#f59e0b"/>
                            <text x="250" y="20" font-size="11" font-weight="black" fill="#dc2626" text-anchor="middle">이음매 콘크리트 페이스트 누수 방지 지수 폼 패킹</text>
                            <text x="250" y="90" font-size="12" font-weight="black" fill="#0369a1" text-anchor="middle">친환경 박리제 균일 미세막 도포 완료</text>
                        </svg>
                    </div>

                    <!-- 상세 엔지니어링 수행 설명 -->
                    <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-100 text-xs sm:text-sm text-emerald-950 space-y-1.5">
                        <h4 class="font-bold text-emerald-900 text-sm">📋 STEP 3 엔지니어링 상세 수행 수칙</h4>
                        <ul class="list-disc pl-5 space-y-1 text-slate-700">
                            <li><strong>친환경 박리제 코팅:</strong> 거푸집 탈형 시 표면 뜯김을 방지하기 위해 <span class="term-highlight" onclick="openGlossary('release_agent')">친환경 박리제를 균일 분사</span>합니다.</li>
                            <li><strong>틈새 누수 패킹:</strong> 거푸집 이음매 틈새에 <span class="term-highlight" onclick="openGlossary('joint_packing')">고지수 폼 패킹을 밀실 시공</span>하여 페이스트 누출을 차단합니다.</li>
                        </ul>
                    </div>
                </div>

                <!-- ==================== STEP 4 ==================== -->
                <div class="bg-white p-6 rounded-2xl border border-blue-200 shadow-md space-y-5">
                    <div class="flex items-center justify-between border-b border-blue-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-blue-600 text-white font-black text-sm px-3 py-1 rounded-lg">STEP 4</span>
                            <h3 class="text-lg font-bold text-slate-900">작업자 통로 식별장치 안전확보 & 선형 검측 승인</h3>
                        </div>
                        <span class="bg-blue-100 text-blue-900 text-xs font-bold px-2.5 py-1 rounded-full">검사 및 확정 단계</span>
                    </div>

                    <!-- 2D SVG 도식 (Light Theme & Click Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgDiagram18_STEP4', '[도식 4] 거푸집 지지대 넘어짐 방지 식별 띠 & 거푸집 선형 최종 검측 승인 도면')">
                        <svg id="svgDiagram18_STEP4" viewBox="0 0 500 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="500" height="180" fill="#f8fafc"/>
                            <rect x="60" y="40" width="16" height="100" fill="#475569"/>
                            <line x1="76" y1="80" x2="220" y2="140" stroke="#f59e0b" stroke-width="6"/>
                            <line x1="76" y1="80" x2="220" y2="140" stroke="#000000" stroke-width="6" stroke-dasharray="10,10"/>
                            <text x="170" y="90" font-size="11" font-weight="black" fill="#b45309" text-anchor="middle">넘어짐 방지 야광 안전 식별 띠</text>
                            
                            <rect x="330" y="105" width="120" height="35" fill="#15803d" rx="6"/>
                            <text x="390" y="127" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">거푸집 선형 검측 승인</text>
                        </svg>
                    </div>

                    <!-- 상세 엔지니어링 수행 설명 -->
                    <div class="bg-blue-50 p-4 rounded-xl border border-blue-100 text-xs sm:text-sm text-blue-950 space-y-1.5">
                        <h4 class="font-bold text-blue-900 text-sm">📋 STEP 4 엔지니어링 상세 수행 수칙</h4>
                        <ul class="list-disc pl-5 space-y-1 text-slate-700">
                            <li><strong>작업자 안전 통로 확보:</strong> 서포트 지지대에 넘어짐 전도 방지 야광 식별 띠(Safety Strip)를 감아 보행 안전을 확보합니다.</li>
                            <li><strong>최종 검측 승인:</strong> 거푸집설치 대조표 및 거푸집 선형 검측표를 감리원에게 제출하고 승인 마감합니다.</li>
                        </ul>
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
# 3. WBS 18 CHECKLIST HTML
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [TCL] 거푸집 설치 체크리스트</title>
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
        <h1 class="title">[TCL] 거푸집 설치 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-18 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #0369a1; font-size: 1.05rem; font-weight: 800;">📋 4단계 실시간 O/X 검측 및 시방 기준</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 서포트 앵커 W=1.0m 간격 고정, 거푸집 변위 ±2mm 이내 통제, 박리제 균일 도포, 누수 방지 패킹, 안전 식별장치 설치 상태를 검측하기 위해 작성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (KCS 14 20 12 공학 규격)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#b45309;">⚠️ 사전 준비<br>(Step 1 앵커타공)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 먹줄 선형</span>
                        <strong>[선형 측량]</strong> CP 광파 측량 데이터 기준 먹줄 선형 배직 정합성 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 앵커 타공</span>
                        <strong>[앵커 간격]</strong> <span class="term-highlight" onclick="openGlossary('support_anchor')">서포트 앵커 W = 1.0m 간격</span> 타공 고정 상태 확인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#0369a1;">📐 거푸집 거치<br>(Step 2 변위통제)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 강재 거푸집</span>
                        <strong>[강재 패널]</strong> 변위 방지형 고강도 강재 거푸집(Steel Form) 조립 고정 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 허용 공차</span>
                        <strong>[변위 오차]</strong> <span class="term-highlight" onclick="openGlossary('form_tolerance')">거푸집 수평/수직 지점 변위 &plusmn;2.0mm 이내</span> 조율 확인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">🧪 표면 처리<br>(Step 3 박리누수)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 박리제 도포</span>
                        <strong>[친환경 박리제]</strong> 거푸집 면 이물질 청소 후 <span class="term-highlight" onclick="openGlossary('release_agent')">친환경 박리제 균일 도포</span> 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 틈새 누수</span>
                        <strong>[지수 폼 패킹]</strong> <span class="term-highlight" onclick="openGlossary('joint_packing')">거푸집 이음매 페이스트 누수 방지 폼 패킹</span> 설치 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#1e3a8a;">📡 안전 & 승인<br>(Step 4 선형검측)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 안전 식별</span>
                        <strong>[식별 띠 설치]</strong> 서포트 지지대 넘어짐 전도 방지 야광 식별 띠 감기 확인
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 최종 승인</span>
                        <strong>[선형 검측]</strong> 거푸집설치 대조표 및 감리원 거푸집 선형 검측서 최종 승인
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-18 [TCL] 거푸집 설치 마스터 체크리스트
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
    for fname in ["[TCL] 거푸집 설치_표준서.html", "18_[TCL] 거푸집 설치_표준서.html", "[TCL] 거푸집설치_표준서.html", "18_[TCL] 거푸집설치_표준서.html"]:
        with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
            f.write(std_html)
            
    # Guideline files
    for fname in ["[TCL] 거푸집 설치_수행지침.html", "18_[TCL] 거푸집 설치_수행지침.html", "[TCL] 거푸집설치_수행지침.html", "18_[TCL] 거푸집설치_수행지침.html"]:
        with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
            f.write(gui_html)
            
    # Checklist files
    for fname in ["[TCL] 거푸집 설치_체크리스트.html", "18_[TCL] 거푸집 설치_체크리스트.html", "[TCL] 거푸집설치_체크리스트.html", "18_[TCL] 거푸집설치_체크리스트.html"]:
        with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
            f.write(chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 18 [TCL] 거푸집 설치!")
