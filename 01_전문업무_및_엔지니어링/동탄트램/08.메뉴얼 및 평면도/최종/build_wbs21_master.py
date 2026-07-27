import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folder_with_space = os.path.join(base_dir, "21_[레일용접] 테르밋 용접")
folder_no_space = os.path.join(base_dir, "21_[레일용접] 테르밋용접")

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
    'en14730_std': {
        title: '📜 EN 14730 국제 테르밋 용접 규격',
        desc: '유럽 및 국제 표준 레일 알루미노테르밋 용접(Aluminothermic Welding) 시방 규격으로, 도가니 알루미늄 반응과 정밀 샌드 몰드 시공 수칙을 규정합니다.'
    },
    'rail_gap_control': {
        title: '📏 레일 끝단 용접 유격 (23 ~ 26mm)',
        desc: '테르밋 쇳물이 틈새로 충분히 침투하여 단면 전체를 수밀 소결시키기 위한 표준 용접 갭(Gap) 세팅 값입니다.'
    },
    'thermite_reaction': {
        title: '💥 2,500℃ 테르밋 점화 반응 & 쇳물 주입',
        desc: '도가니(Crucible) 내 산화철과 알루미늄 분말에 점화 성냥을 대어 2,500℃ 이상의 환원 발열 반응을 일으켜 순수 용융 강철을 생성하고 샌드 몰드로 자동 주입하는 공법입니다.'
    },
    'welder_stamp_marking': {
        title: '🏷️ 용접년도 & 용접공 고유번호 마킹 각인',
        desc: '용접이 완료된 레일 복부(Web) 개소 측면에 책임 시공 관리를 위해 용접년월일과 승인받은 용접공 고유 고유번호를 스탬프로 영구 마킹 각인하는 수칙입니다.'
    },
    'mt_ut_testing': {
        title: '📡 MT (자분) & UT (초음파) 비파괴검사 100%',
        desc: '용접부 표면 미세 균열(MT 자분탐상) 및 내부 불순물/기포 결함(UT 초음파 탐상) 유무를 100% 전수 검사하여 시공성적표에 결재하는 절차입니다.'
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
# 1. WBS 21 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일용접] 테르밋 용접 표준서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-amber-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-amber-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-21 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">EN 14730 / KR C-14030 규격 준수</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일용접] 테르밋 용접 표준서</h1>
            <p class="text-amber-200 mt-2 text-sm sm:text-base">"EN 14730 규격 준수, 유격 23~26mm, 2,500℃ 테르밋 반응 쇳물 주입 & 1m당 ±0.2mm 연마 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-amber-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-amber-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 본선 장대레일 상호 간을 일체화하기 위해 테르밋 용재를 예열된 장대레일 유격 공간(23~26mm)에 부어 2,500℃ 용융 접합하는 테르밋 용접 시방 규정입니다. EN 14730 규격 준수, 도가니 점화 반응, 약 5분 후 유압 핫 쉐어링, 용접년도/고유번호 각인, 1m 당 ±0.2mm 연마 및 MT/UT NDT 비파괴검사 100% 합격을 규정합니다. (주관: 현장 공사팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-amber-700 block mb-1">💥 유격 조정, 예열 & 테르밋 반응</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>국제 용접 규격:</strong> <strong>EN 14730-1 / EN 14730-2</strong> 시방 준수</li>
                        <li><strong>레일 유격 조정:</strong> 레일 단부 유격 <strong>23 ~ 26mm</strong> 정밀 세팅</li>
                        <li><strong>예열 온도:</strong> 프로판-산소 900~1,000℃ 약 4~5분 예열</li>
                        <li><strong>테르밋 용융 반응:</strong> 일회용 도가니 <strong>2,500℃</strong> 초고온 쇳물 주입</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-amber-700 block mb-1">🏷️ 핫 쉐어링, 각인, 연마 & NDT 검사</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>핫 쉐어링:</strong> 쇳물 주입 5분 후 적열 상태 Riser 유압 전단</li>
                        <li><strong>용접공 각인:</strong> 레일 복부에 <strong>용접년도 & 고유번호</strong> 스탬프 각인</li>
                        <li><strong>직선도 연마:</strong> 1m 당 직선도 <strong>&plusmn;0.2mm 이내</strong> 정밀 플러시 연마</li>
                        <li><strong>비파괴 탐상검사:</strong> <strong>MT(자분) & UT(초음파) 100%</strong> 전수 실시</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 서식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">2.</span> 필 수 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-2">
                <p>✔️ <strong>테르밋 용접일지:</strong> 예열 온도, 유격(23~26mm), 쇳물 주입 및 전단 시간 일지</p>
                <p>✔️ <strong>MT / UT 비파괴보고서:</strong> 자분탐상(MT) 및 초음파탐상(UT) 100% 합격 검사 성적서</p>
                <p>✔️ <strong>용접부 직선도 검측대장:</strong> 1m 당 오차 &plusmn;0.2mm 이내 정밀 연마 측량표 및 각인 기록지</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 21 GUIDELINE HTML (3-Step Procedure Cards with Embedded Visual Diagrams)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일용접] 테르밋 용접 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-amber-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-amber-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-21 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">EN 14730 테르밋 용접 3단계 visual 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일용접] 테르밋 용접 수행지침서</h1>
            <p class="text-amber-200 mt-2 text-sm sm:text-base">"유격 23~26mm, 2,500℃ 테르밋 쇳물 주입, 버 핫 쉐어링, 각인, 연마 & NDT 100% 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (테르밋 용접 개념 포함) -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-950 shadow-sm space-y-3">
            <h4 class="font-bold text-amber-950 text-base flex items-center gap-2">
                <span>💡</span> [레일용접] 테르밋 용접(Thermite Welding) 개념 해설
            </h4>
            <div class="bg-white p-3 rounded-lg border border-amber-300 font-medium text-slate-900">
                💥 <strong>'테르밋 용접'이란?</strong><br>
                두 레일 사이 유격<strong><span class="term-highlight" onclick="openGlossary('rail_gap_control')">(23~26mm)</span></strong>에 샌드 몰드를 감싼 후, 일회용 도가니 솥에 산화철과 알루미늄 가루를 넣고 불붙여 <strong><span class="term-highlight" onclick="openGlossary('thermite_reaction')">2,500℃ 초고온 액체 쇳물을 틈새에 주입</span></strong>하여 하나로 붙이는 공법입니다. 주입 5분 후 튀어나온 쇳덩이(Riser)를 유압 컷터로 전단하고, 레일 복부에 <strong><span class="term-highlight" onclick="openGlossary('welder_stamp_marking')">용접년도 및 용접공 번호를 각인</span></strong>한 뒤 <strong><span class="term-highlight" onclick="openGlossary('mt_ut_testing')">MT/UT 비파괴검사를 100%</span></strong> 수행합니다.
            </div>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">1.</span> 4단계 시공 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">유격 조정 & 클램프 고정</h4>
                    </div>
                    <p class="text-[11px] text-amber-900 mt-2 font-medium">유격 23~26mm & 직선 정렬</p>
                </div>

                <div class="bg-orange-50 p-4 rounded-xl border border-orange-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-orange-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">몰드 조립 & 1,000℃ 예열</h4>
                    </div>
                    <p class="text-[11px] text-orange-900 mt-2 font-medium">프로판-산소 900~1,000℃ 예열</p>
                </div>

                <div class="bg-red-50 p-4 rounded-xl border border-red-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">2,500℃ 반응 & 핫 쉐어링</h4>
                    </div>
                    <p class="text-[11px] text-red-900 mt-2 font-medium">쇳물 주입 & 5분 후 유압 전단</p>
                </div>

                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">각인, 연마 & NDT 검사</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">용접공 각인, 0.2mm 연마, NDT 100%</p>
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
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 끝단 23~26mm 유격 조정 & 정밀 정렬 클램프 고정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 용접부 단면 유격을 <span class="term-highlight" onclick="openGlossary('rail_gap_control')">측정 자로 23 ~ 26mm 범위 내로 세팅</span>하고, 레일 직선도 및 캔트 비틀림을 방지하기 위해 <span class="term-highlight" onclick="openGlossary('en14730_std')">EN 14730 정밀 정렬 클램프</span>로 완전 고정합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-amber-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 레일 끝단 용접 유격(23~26mm) 세팅 & 3D 정렬 클램프 고정 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 좌측 레일 단부 -->
                            <rect x="40" y="75" width="200" height="40" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            
                            <!-- 용접 유격 23~26mm -->
                            <line x1="240" y1="45" x2="240" y2="135" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,3"/>
                            <line x1="268" y1="45" x2="268" y2="135" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,3"/>
                            <line x1="240" y1="55" x2="268" y2="55" stroke="#dc2626" stroke-width="2.5"/>
                            <text x="254" y="45" font-size="12" font-weight="black" fill="#dc2626" text-anchor="middle">유격 23 ~ 26mm</text>
                            
                            <!-- 우측 레일 단부 -->
                            <rect x="268" y="75" width="200" height="40" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            
                            <!-- 정밀 정렬 클램프 -->
                            <rect x="20" y="130" width="480" height="30" rx="4" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                            <text x="260" y="150" font-size="11" font-weight="black" fill="#1e293b" text-anchor="middle">EN 14730 3D 정밀 레일 정렬 고정 클램프</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-red-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-red-100 text-red-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 본 시공 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">900~1,000℃ 예열, 2,500℃ 테르밋 반응 쇳물 주입 & 핫 쉐어링</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        샌드 몰드 조립 후 프로판 버너로 900~1,000℃ 예열을 실시하고, 일회용 도가니에서 <span class="term-highlight" onclick="openGlossary('thermite_reaction')">2,500℃ 테르밋 알루미노 점화 반응 쇳물을 주입</span>하며, 주입 약 5분 후 유압 핫 쉐어링 컷터로 Riser를 깔끔하게 전단 제거합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-red-200" onclick="openDiagramZoom('svgStep2_Card', '[본 시공] 도가니 2,500℃ 테르밋 점화 반응 쇳물 주입 & 샌드 몰드 유압 전단 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 520 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="230" fill="#f8fafc"/>
                            
                            <!-- 레일 단부 -->
                            <rect x="40" y="115" width="190" height="40" fill="#475569"/>
                            <rect x="290" y="115" width="190" height="40" fill="#475569"/>
                            
                            <!-- 샌드 몰드 (Sand Mold) -->
                            <rect x="220" y="95" width="80" height="75" fill="#f59e0b" stroke="#b45309" stroke-width="2" rx="4"/>
                            <text x="260" y="140" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">샌드 몰드</text>

                            <!-- 테르밋 도가니 (Thermite Crucible) -->
                            <path d="M 210 20 L 310 20 L 280 85 L 240 85 Z" fill="#b45309" stroke="#78350f" stroke-width="2"/>
                            <text x="260" y="45" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle">도가니 (Crucible)</text>
                            
                            <!-- 2,500℃ 용융 쇳물 물줄기 -->
                            <line x1="260" y1="85" x2="260" y2="105" stroke="#ef4444" stroke-width="8"/>
                            <text x="260" y="70" font-size="12" font-weight="black" fill="#ef4444" text-anchor="middle">🔥 2,500℃ 용융 쇳물 주입</text>

                            <!-- 핫 쉐어링 컷터 -->
                            <path d="M 310 100 L 325 130 L 295 130 Z" fill="#dc2626"/>
                            <text x="365" y="115" font-size="10" font-weight="black" fill="#dc2626">약 5분 후 유압 전단</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 검사 및 확정 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">용접공 각인 마킹, 1m당 ±0.2mm 정밀 연마 & MT/UT 비파괴검사</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 복부에 <span class="term-highlight" onclick="openGlossary('welder_stamp_marking')">용접년도 및 용접공 고유번호를 마킹 각인</span>하고, 레일 면을 1m 당 오차 ±0.2mm 이내로 정밀 연마한 후 <span class="term-highlight" onclick="openGlossary('mt_ut_testing')">MT 자분탐상 및 UT 초음파 탐상검사 100%</span>를 실시하여 검측 승인을 획득합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (Clickable Lightbox Zoom) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[검사 마감] 레일 복부 용접년도/고유번호 각인, 1m당 ±0.2mm 정밀 연마 & MT/UT 검사 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 완성된 용접 레일 -->
                            <rect x="40" y="80" width="440" height="40" fill="#475569"/>
                            <rect x="250" y="80" width="20" height="40" fill="#38bdf8"/>
                            
                            <!-- 용접년도 & 고유번호 각인 스탬프 -->
                            <rect x="235" y="90" width="50" height="20" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5" rx="2"/>
                            <text x="260" y="104" font-size="10" font-weight="black" fill="#854d0e" text-anchor="middle">2026-W09</text>
                            <text x="260" y="140" font-size="11" font-weight="black" fill="#854d0e" text-anchor="middle">용접년도 & 용접공 번호 각인</text>

                            <!-- MT / UT 탐상 센서 -->
                            <circle cx="100" cy="80" r="16" fill="#059669" stroke="#047857" stroke-width="2"/>
                            <text x="100" y="84" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">MT/UT</text>
                            <text x="100" y="55" font-size="11" font-weight="black" fill="#059669" text-anchor="middle">MT / UT 비파괴검사 100%</text>

                            <!-- 직선도 연마 1m ±0.2mm -->
                            <line x1="340" y1="60" x2="460" y2="60" stroke="#0284c7" stroke-width="3"/>
                            <text x="400" y="48" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">직선도 1m당 &plusmn;0.2mm 연마</text>
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
# 3. WBS 21 CHECKLIST HTML (질문형 어미 "~하였는가?" 100% 적용)
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [레일용접] 테르밋 용접 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-amber: #d97706;
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
            color: #b45309;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: #d97706;
        }}
        .summary-box {{
            background: #fffbeb;
            border: 1px solid #fef3c7;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #b45309;
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
            color: #d97706;
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
        <h1 class="title">[레일용접] 테르밋 용접 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-21 | 레일 테르밋 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #b45309; font-size: 1.05rem; font-weight: 800;">📋 EN 14730 테르밋 용접 O/X 필수 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 유격(23~26mm), 예열(900~1,000℃), 테르밋 점화 반응(2,500℃), 유압 핫 쉐어링, 용접년도 각인, 1m당 ±0.2mm 연마 및 MT/UT 탐상 100%를 검측하기 위해 작성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (EN 14730 / KR C-14030 규격)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#b45309;">⚠️ 사전 준비<br>(Step 1 유격조정)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 유격 세팅</span>
                        <strong>[용접 유격]</strong> 레일 끝단 용접 유격 <span class="term-highlight" onclick="openGlossary('rail_gap_control')">23 ~ 26mm 범위 내로 정확히 조정하였는가?</span>
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 클램프 고정</span>
                        <strong>[정밀 정렬]</strong> <span class="term-highlight" onclick="openGlossary('en14730_std')">EN 14730 정밀 클램프</span>로 레일 직선도 및 캔트를 고정하였는가?
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#991b1b;">💥 예열 & 쇳물주입<br>(Step 2 테르밋반응)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef2f2; color:#991b1b;">Step 2. 예열 온도</span>
                        <strong>[몰드 예열]</strong> 샌드 몰드 설치 후 프로판-산소 버너로 900~1,000℃ 온도 예열하였는가?
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#fef2f2; color:#991b1b;">Step 2. 쇳물 주입</span>
                        <strong>[테르밋 주입]</strong> <span class="term-highlight" onclick="openGlossary('thermite_reaction')">도가니 2,500℃ 테르밋 점화 반응 쇳물</span>을 샌드 몰드로 자동 주입하였는가?
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#c2410c;">✂️ 전단 & 각인<br>(Step 3 핫쉐어링)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#ffedd5; color:#9a3412;">Step 3. 핫 쉐어링</span>
                        <strong>[유압 전단]</strong> 쇳물 주입 약 5분 후 적열 상태일 때 유압 컷터로 Riser를 전단 제거하였는가?
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#ffedd5; color:#9a3412;">Step 3. 용접공 각인</span>
                        <strong>[마킹 각인]</strong> 레일 복부 측면에 <span class="term-highlight" onclick="openGlossary('welder_stamp_marking')">용접년도 및 용접공 고유번호를 스탬프 마킹 각인하였는가?</span>
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#1e3a8a;">📡 연마 & NDT<br>(Step 4 비파괴)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 정밀 연마</span>
                        <strong>[직선도 연마]</strong> 용접부 레일 직선도 오차 <strong>1m 당 &plusmn;0.2mm 이내</strong> 정밀 플러시 연마하였는가?
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. NDT 검사</span>
                        <strong>[비파괴 탐상]</strong> <span class="term-highlight" onclick="openGlossary('mt_ut_testing')">MT 자분탐상 및 UT 초음파 탐상검사 100%</span> 실시 후 성적서 결재하였는가?
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-21 [레일용접] 테르밋 용접 마스터 체크리스트
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
    for fname in ["[레일용접] 테르밋 용접_표준서.html", "21_[레일용접] 테르밋 용접_표준서.html", "[레일용접] 테르밋용접_표준서.html", "21_[레일용접] 테르밋용접_표준서.html"]:
        with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
            f.write(std_html)
            
    # Guideline files
    for fname in ["[레일용접] 테르밋 용접_수행지침.html", "21_[레일용접] 테르밋 용접_수행지침.html", "[레일용접] 테르밋용접_수행지침.html", "21_[레일용접] 테르밋용접_수행지침.html"]:
        with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
            f.write(gui_html)
            
    # Checklist files
    for fname in ["[레일용접] 테르밋 용접_체크리스트.html", "21_[레일용접] 테르밋 용접_체크리스트.html", "[레일용접] 테르밋용접_체크리스트.html", "21_[레일용접] 테르밋용접_체크리스트.html"]:
        with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
            f.write(chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 21 [레일용접] 테르밋 용접!")
