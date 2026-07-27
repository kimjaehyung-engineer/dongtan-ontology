import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folder_with_space = os.path.join(base_dir, "21_[레일용접] 테르밋 용접")
folder_no_space = os.path.join(base_dir, "21_[레일용접] 테르밋용접")

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
    'sand_preheating': {
        title: '🔥 샌드 몰드 조립 & 900~1,000℃ 예열',
        desc: '레일 용접부 틈새에 흙 몰드(Sand Mold)를 밀봉 조립한 후 프로판-산소 버너 불꽃으로 900~1,000℃ 예열하여 쇳물 주입 시 온도 차이에 의한 균열을 방지합니다.'
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

# Restructured Complete 4-Step Guideline HTML with Enlarged Fonts
gui_4step_html = f"""<!DOCTYPE html>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">EN 14730 테르밋 용접 완전 4단계 visual 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일용접] 테르밋 용접 수행지침서</h1>
            <p class="text-amber-200 mt-2 text-sm sm:text-base">"유격 23~26mm, 2,500℃ 테르밋 쇳물 주입, 버 핫 쉐어링, 각인, 연마 & NDT 100% 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (테르밋 용접 친절한 개념 해설) -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-950 shadow-sm space-y-3">
            <h4 class="font-bold text-amber-950 text-base flex items-center gap-2">
                <span>💡</span> [레일용접] 테르밋 용접(Thermite Welding) 친절하고 쉬운 개념 해설
            </h4>
            <div class="bg-white p-4 rounded-lg border border-amber-300 font-medium text-slate-900 leading-relaxed">
                💥 <strong>'테르밋 용접'이란 무엇인가요?</strong><br>
                두 레일 사이 유격<strong><span class="term-highlight" onclick="openGlossary('rail_gap_control')">(23~26mm)</span></strong>에 흙 몰드(Sand Mold)를 밀봉 감싼 후, 도가니 솥에 산화철과 알루미늄 가루를 넣고 불붙여 <strong><span class="term-highlight" onclick="openGlossary('thermite_reaction')">2,500℃ 초고온 액체 쇳물을 틈새에 주입</span></strong>하여 하나로 붙이는 공법입니다.<br>
                주입 5분 후 튀어나온 쇳덩이(Riser)를 유압 컷터로 전단하고, 레일 복부에 <strong><span class="term-highlight" onclick="openGlossary('welder_stamp_marking')">용접년도 및 용접공 번호를 각인</span></strong>한 뒤 <strong><span class="term-highlight" onclick="openGlossary('mt_ut_testing')">MT/UT 비파괴검사 100%</span></strong>를 수행합니다.
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
                    <p class="text-[11px] text-amber-900 mt-2 font-medium">유격 23~26mm & 정밀 정렬</p>
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

        <!-- ★ 2. 완전 4단계(STEP 1 ~ STEP 4) 세부 작업 수행절차 & 4대 정밀 2D visual 도식 수록 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 완전 4단계 세부 작업 수행절차 (Structured 4-Step Procedure & 4 Visual Diagrams)
            </h2>
            
            <div class="space-y-8 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-500 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 사전 준비 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 끝단 23~26mm 유격 조정 & 정밀 정렬 클램프 고정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 용접부 단면 유격을 <span class="term-highlight" onclick="openGlossary('rail_gap_control')">측정 자로 23 ~ 26mm 범위 내로 정밀 세팅</span>하고, 레일 직선도 및 캔트 비틀림을 방지하기 위해 <span class="term-highlight" onclick="openGlossary('en14730_std')">EN 14730 정밀 정렬 클램프</span>로 완전 고정합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (글씨 크기 13px bold 확대) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-amber-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 레일 끝단 용접 유격(23~26mm) 세팅 & 3D 정렬 클램프 고정 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 좌측 레일 단부 -->
                            <rect x="40" y="75" width="200" height="40" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            
                            <!-- 용접 유격 23~26mm -->
                            <line x1="240" y1="40" x2="240" y2="135" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="4,3"/>
                            <line x1="268" y1="40" x2="268" y2="135" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="4,3"/>
                            <line x1="240" y1="52" x2="268" y2="52" stroke="#dc2626" stroke-width="3"/>
                            <text x="254" y="38" font-size="13" font-weight="black" fill="#dc2626" text-anchor="middle">용접 유격 23 ~ 26mm 정밀 세팅</text>
                            
                            <!-- 우측 레일 단부 -->
                            <rect x="268" y="75" width="200" height="40" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            
                            <!-- 정밀 정렬 클램프 -->
                            <rect x="20" y="130" width="480" height="32" rx="4" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                            <text x="260" y="151" font-size="13" font-weight="black" fill="#1e293b" text-anchor="middle">EN 14730 3D 정밀 레일 정렬 고정 클램프</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD (몰드 조립 & 예열) -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-orange-500 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-orange-100 text-orange-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 몰드 및 예열 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">샌드 몰드 밀봉 조립 & 900~1,000℃ 프로판-산소 버너 예열</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 용접부 틈새에 <span class="term-highlight" onclick="openGlossary('sand_preheating')">샌드 몰드(Sand Mold)를 밀봉 감싼 후</span> 찰흙으로 틈새를 마감하고, 프로판-산소 예열 버너 불꽃으로 레일 단부를 900~1,000℃ 적열 상태로 4~5분간 예열합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (글씨 크기 13px bold 확대) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-orange-200" onclick="openDiagramZoom('svgStep2_Card', '[몰드 예열] 샌드 몰드 조립 & 900~1,000℃ 프로판-산소 버너 예열 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 레일 단부 -->
                            <rect x="40" y="85" width="190" height="40" fill="#475569"/>
                            <rect x="290" y="85" width="190" height="40" fill="#475569"/>
                            
                            <!-- 샌드 몰드 밀봉 -->
                            <rect x="220" y="65" width="80" height="80" fill="#f59e0b" stroke="#b45309" stroke-width="2.5" rx="6"/>
                            <text x="260" y="110" font-size="13" font-weight="black" fill="#ffffff" text-anchor="middle">샌드 몰드 밀봉</text>

                            <!-- 예열 버너 불꽃 (900~1,000℃) -->
                            <path d="M 260 15 L 275 55 L 245 55 Z" fill="#ef4444"/>
                            <text x="260" y="30" font-size="13" font-weight="black" fill="#dc2626" text-anchor="middle">🔥 프로판 예열 버너 (900~1,000℃)</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD (본 시공: 쇳물 주입 & 핫 쉐어링) -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-red-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-red-100 text-red-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 본 시공 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">2,500℃ 테르밋 점화 반응 쇳물 주입 & 5분 후 핫 쉐어링 전단</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        일회용 도가니(Crucible) 솥에 불을 붙여 <span class="term-highlight" onclick="openGlossary('thermite_reaction')">2,500℃ 초고온 알루미노 쇳물을 몰드로 자동 주입</span>하며, 주입 약 5분 후 유압 핫 쉐어링 컷터로 튀어나온 쇳덩이(Riser)를 깔끔하게 전단 제거합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (글씨 크기 13px bold 확대) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-red-200" onclick="openDiagramZoom('svgStep3_Card', '[본 시공] 도가니 2,500℃ 테르밋 점화 반응 쇳물 주입 & 샌드 몰드 유압 전단 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 520 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="220" fill="#f8fafc"/>
                            
                            <rect x="40" y="115" width="190" height="40" fill="#475569"/>
                            <rect x="290" y="115" width="190" height="40" fill="#475569"/>
                            
                            <rect x="220" y="95" width="80" height="75" fill="#f59e0b" stroke="#b45309" stroke-width="2" rx="4"/>
                            <text x="260" y="140" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle">샌드 몰드</text>

                            <!-- 도가니 솥 -->
                            <path d="M 210 20 L 310 20 L 280 85 L 240 85 Z" fill="#b45309" stroke="#78350f" stroke-width="2"/>
                            <text x="260" y="45" font-size="13" font-weight="black" fill="#ffffff" text-anchor="middle">도가니 (Crucible)</text>
                            
                            <!-- 2,500℃ 쇳물 물줄기 -->
                            <line x1="260" y1="85" x2="260" y2="105" stroke="#ef4444" stroke-width="8"/>
                            <text x="260" y="70" font-size="13" font-weight="black" fill="#ef4444" text-anchor="middle">🔥 2,500℃ 용융 쇳물 주입</text>

                            <!-- 핫 쉐어링 컷터 -->
                            <path d="M 310 100 L 325 130 L 295 130 Z" fill="#dc2626"/>
                            <text x="375" y="115" font-size="12" font-weight="black" fill="#dc2626">약 5분 후 유압 전단</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 4 CARD (검사 및 확정 - ★ 신설 수록!) -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-blue-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">4</div>
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 4. 검사 및 마감 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">용접공 각인 마킹, 1m당 ±0.2mm 정밀 연마 & MT/UT 비파괴검사 100%</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 옆구리 복부에 <span class="term-highlight" onclick="openGlossary('welder_stamp_marking')">용접년도 및 용접공 고유번호를 스탬프 마킹 각인</span>하고, 레일 타슬면을 1m 당 오차 ±0.2mm 이내로 정밀 연마한 후 <span class="term-highlight" onclick="openGlossary('mt_ut_testing')">MT 자분탐상 및 UT 초음파 비파괴검사 100%</span>를 받아 감리원 최종 승인을 획득합니다.
                    </p>

                    <!-- STEP 4 2D Visual Diagram (글씨 크기 13px bold 확대 - ★ 신설) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgStep4_Card', '[검사 마감] 레일 복부 용접년도/용접공 번호 각인 스탬프, 1m당 ±0.2mm 연마 & MT/UT 비파괴 100% 도면')">
                        <svg id="svgStep4_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 완성된 용접 레일 -->
                            <rect x="40" y="80" width="440" height="40" fill="#475569"/>
                            <rect x="250" y="80" width="20" height="40" fill="#38bdf8"/>
                            
                            <!-- 용접년도 & 고유번호 각인 스탬프 -->
                            <rect x="230" y="90" width="60" height="22" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5" rx="3"/>
                            <text x="260" y="105" font-size="12" font-weight="black" fill="#854d0e" text-anchor="middle">2026-W09</text>
                            <text x="260" y="142" font-size="13" font-weight="black" fill="#854d0e" text-anchor="middle">용접년도 & 용접공 번호 각인</text>

                            <!-- MT / UT 탐상 센서 -->
                            <circle cx="100" cy="80" r="18" fill="#059669" stroke="#047857" stroke-width="2"/>
                            <text x="100" y="85" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">MT/UT</text>
                            <text x="100" y="52" font-size="13" font-weight="black" fill="#059669" text-anchor="middle">MT / UT 비파괴검사 100%</text>

                            <!-- 직선도 연마 1m ±0.2mm -->
                            <line x1="340" y1="60" x2="460" y2="60" stroke="#0284c7" stroke-width="3.5"/>
                            <text x="400" y="46" font-size="13" font-weight="black" fill="#0284c7" text-anchor="middle">직선도 1m당 &plusmn;0.2mm 연마</text>
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

# Force update all Guideline HTML files across both directories
for folder_path in [folder_with_space, folder_no_space]:
    gui_dir = os.path.join(folder_path, "수행지침")
    os.makedirs(gui_dir, exist_ok=True)
    
    for fname in ["[레일용접] 테르밋 용접_수행지침.html", "21_[레일용접] 테르밋 용접_수행지침.html", "[레일용접] 테르밋용접_수행지침.html", "21_[레일용접] 테르밋용접_수행지침.html"]:
        fpath = os.path.join(gui_dir, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(gui_4step_html)
        print(f"✏️ Updated WBS 21 Guideline with Complete 4-Step Cards & Enlarged Visuals: {fpath}")

print("\n🎉 SUCCESSFULLY UPDATED WBS 21 GUIDELINE WITH COMPLETE 4-STEP CARDS AND 4 ENLARGED VISUAL DIAGRAMS!")
