import os
import sys
import base64

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"
img_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298"

folder_with_space = os.path.join(base_dir, "21_[레일용접] 테르밋 용접")
folder_no_space = os.path.join(base_dir, "21_[레일용접] 테르밋용접")

# Load base64 encoded images for reliable HTML embedding
def get_b64_img(filename):
    path = os.path.join(img_dir, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode('utf-8')}"
    return ""

img_b64_dict = {
    'cleaning': get_b64_img('01_cleaning.jpg'),
    'alignment': get_b64_img('02_rail_to_rail_alignment.jpg'),
    'sealing': get_b64_img('03_sealing_mold.jpg'),
    'preheating': get_b64_img('04_preheating.jpg'),
    'pouring': get_b64_img('05_thermite_welding_pouring.jpg'),
    'shearing': get_b64_img('06_pushing_tumor_shearing.jpg'),
    'grinding': get_b64_img('07_finish_grinding.jpg'),
    'finished': get_b64_img('08_finished_joint.jpg'),
}

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
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; color: #0f172a; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 사진 및 도식 대형 고화질 정밀 보기</h3>
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
    document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "사진 및 도식 대형 정밀 보기");
    
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
        innerImg.style.borderRadius = '12px';
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

# Restructured 8-Step Sinchold Process Guideline HTML
gui_sinchold_8step_html = f"""<!DOCTYPE html>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">Sinchold 표준 8단계 실사 공정 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[레일용접] 테르밋 용접 수행지침서</h1>
            <p class="text-amber-200 mt-2 text-sm sm:text-base">"Sinchold 8대 현장 공정 순서(청소→정렬→몰드→예열→쇳물주입→전단→연마→검사) 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (Sinchold 표준 8단계 친절 해설) -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-950 shadow-sm space-y-3">
            <h4 class="font-bold text-amber-950 text-base flex items-center gap-2">
                <span>💡</span> [레일용접] Sinchold 트램 레일 테르밋 용접 8대 표준 시공 순서
            </h4>
            <div class="bg-white p-4 rounded-lg border border-amber-300 font-medium text-slate-900 leading-relaxed">
                💥 <strong>Sinchold 알루미노테르밋 용접이란?</strong><br>
                도시철도 트램 궤도 시공 시 두 레일 접속부를 <strong><span class="term-highlight" onclick="openGlossary('thermite_reaction')">8단계 연속 현장 공정(청소 → 정렬 → 샌드몰드 → 1,000℃ 예열 → 2,500℃ 쇳물 주입 → 유압 버 전단 → 정밀 연마 → 비파괴검사)</span></strong>으로 일체화시켜 용접 흔적 없이 매끈한 장대레일을 형성하는 시방 공법입니다.
            </div>
        </div>

        <!-- 1. 8단계 시공 마스터 프로세스 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">1.</span> Sinchold 8단계 시공 마스터 프로세스 (8-Step Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                <div class="bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                    <h4 class="font-bold text-slate-900 mt-1">용접 전 청소</h4>
                    <p class="text-[10px] text-amber-900 mt-1">단면 50mm Grinding</p>
                </div>
                <div class="bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                    <h4 class="font-bold text-slate-900 mt-1">Rail-to-Rail 정렬</h4>
                    <p class="text-[10px] text-amber-900 mt-1">유격 23~26mm 정렬</p>
                </div>
                <div class="bg-amber-50 p-3 rounded-xl border border-amber-200">
                    <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                    <h4 class="font-bold text-slate-900 mt-1">몰드 설치 & 씰링</h4>
                    <p class="text-[10px] text-amber-900 mt-1">샌드 몰드 완전 밀봉</p>
                </div>
                <div class="bg-orange-50 p-3 rounded-xl border border-orange-200">
                    <span class="bg-orange-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                    <h4 class="font-bold text-slate-900 mt-1">용접부 예열</h4>
                    <p class="text-[10px] text-orange-900 mt-1">900~1,000℃ 예열</p>
                </div>
                <div class="bg-red-50 p-3 rounded-xl border border-red-200">
                    <span class="bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 5</span>
                    <h4 class="font-bold text-slate-900 mt-1">테르밋 쇳물 주입</h4>
                    <p class="text-[10px] text-red-900 mt-1">2,500℃ 초고온 주입</p>
                </div>
                <div class="bg-red-50 p-3 rounded-xl border border-red-200">
                    <span class="bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 6</span>
                    <h4 class="font-bold text-slate-900 mt-1">버 전단 (핫 쉐어링)</h4>
                    <p class="text-[10px] text-red-900 mt-1">주입 5분 후 유압 전단</p>
                </div>
                <div class="bg-blue-50 p-3 rounded-xl border border-blue-200">
                    <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 7</span>
                    <h4 class="font-bold text-slate-900 mt-1">마무리 정밀 연마</h4>
                    <p class="text-[10px] text-blue-900 mt-1">1m당 &plusmn;0.2mm 연마</p>
                </div>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200">
                    <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 8</span>
                    <h4 class="font-bold text-slate-900 mt-1">각인 & NDT 검사</h4>
                    <p class="text-[10px] text-emerald-900 mt-1">용접공 각인 & MT/UT 100%</p>
                </div>
            </div>
        </div>

        <!-- 2. Sinchold 8단계 세부 작업 수행절차 (현장 실사 사진 + 1:1 2D visual 도식 수록) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> Sinchold 8단계 세부 작업 수행절차 (Structured 8-Step Detailed Procedure & Photos)
            </h2>
            
            <div class="space-y-8 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-500 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 용접 전 청소 (Cleaning before welding)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 접속 단면 50mm Grinding 광택 청소</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        용접 불량 및 스케일 혼입을 방지하기 위해 레일 접속 단부 50mm 영역의 녹, 스케일, 기름을 Grinder로 광택면이 나올 때까지 100% 제거합니다.
                    </p>
                    
                    <!-- STEP 1 현장 사진 및 도식 (클릭 시 줌 확대) -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-amber-200 text-center" onclick="openDiagramZoom('imgStep1', '[Sinchold 현장 사진] STEP 1. 용접 전 레일 단면 50mm Grinding 청소')">
                            <img id="imgStep1" src="{img_b64_dict['cleaning']}" alt="Cleaning before welding" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-amber-900 mt-2 block">📷 현장 사진: 레일 단면 Grinding 광택 청소</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-amber-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep1', '[2D 기술 도식] STEP 1. 레일 단면 50mm Grinding 연마 도면')">
                            <svg id="svgStep1" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="20" y="50" width="80" height="35" fill="#475569"/>
                                <rect x="80" y="50" width="20" height="35" fill="#38bdf8"/>
                                <rect x="150" y="50" width="80" height="35" fill="#475569"/>
                                <rect x="150" y="50" width="20" height="35" fill="#38bdf8"/>
                                <text x="125" y="35" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">50mm 광택 연마</text>
                                <text x="125" y="110" font-size="12" font-weight="black" fill="#1e293b" text-anchor="middle">녹/기름 100% 제거</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. Rail-to-Rail 레일 정렬 (Rail-to-Rail Alignment)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 유격 23~26mm 세팅 & EN 14730 3D 정밀 정렬 클램프 체결</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 용접부 단면 유격을 <span class="term-highlight" onclick="openGlossary('rail_gap_control')">측정 자로 23 ~ 26mm 범위 내로 세팅</span>하고, 레일 직선도 및 캔트 비틀림을 방지하기 위해 정밀 정렬 클램프로 고정합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-amber-200 text-center" onclick="openDiagramZoom('imgStep2', '[Sinchold 현장 사진] STEP 2. Rail-to-Rail 유격 세팅 & 3D 정렬 클램프 체결')">
                            <img id="imgStep2" src="{img_b64_dict['alignment']}" alt="Rail-to-Rail Alignment" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-amber-900 mt-2 block">📷 현장 사진: Rail-to-Rail 정렬 & 유격 세팅</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-amber-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep2', '[2D 기술 도식] STEP 2. 레일 유격 23~26mm 세팅 도면')">
                            <svg id="svgStep2" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="20" y="50" width="95" height="35" fill="#475569"/>
                                <rect x="135" y="50" width="95" height="35" fill="#475569"/>
                                <line x1="115" y1="30" x2="115" y2="95" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,2"/>
                                <line x1="135" y1="30" x2="135" y2="95" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,2"/>
                                <text x="125" y="25" font-size="12" font-weight="black" fill="#dc2626" text-anchor="middle">유격 23~26mm</text>
                                <text x="125" y="115" font-size="12" font-weight="black" fill="#1e293b" text-anchor="middle">EN 14730 3D 정렬 클램프</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-amber-700 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 샌드 몰드 설치 및 씰링 (Sealing Mold)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">샌드 몰드(Sand Mold) 장착 및 찰흙/지수 패킹 완전 밀봉</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 용접부 틈새에 <span class="term-highlight" onclick="openGlossary('sand_preheating')">샌드 몰드(Sand Mold)를 밀봉 조립</span>한 후, 쇳물 누출을 막기 위해 찰흙과 지수 폼으로 틈새를 100% 밀봉 처리합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-amber-200 text-center" onclick="openDiagramZoom('imgStep3', '[Sinchold 현장 사진] STEP 3. 샌드 몰드 장착 및 찰흙/지수 패킹 100% 씰링')">
                            <img id="imgStep3" src="{img_b64_dict['sealing']}" alt="Sealing Mold" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-amber-900 mt-2 block">📷 현장 사진: 샌드 몰드 조립 & 찰흙 밀봉</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-amber-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep3', '[2D 기술 도식] STEP 3. 샌드 몰드 밀봉 도면')">
                            <svg id="svgStep3" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="20" y="55" width="90" height="35" fill="#475569"/>
                                <rect x="140" y="55" width="90" height="35" fill="#475569"/>
                                <rect x="105" y="40" width="40" height="65" fill="#f59e0b" stroke="#b45309" stroke-width="2" rx="4"/>
                                <text x="125" y="80" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle">몰드 씰링</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 4 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-orange-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">4</div>
                    <span class="bg-orange-100 text-orange-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 4. 용접부 예열 (Preheating)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">프로판-산소 버너 불꽃으로 900~1,000℃ 4~5분 예열</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        샌드 몰드 상부에 프로판-산소 가열 버너를 장착하고 레일 단부를 <span class="term-highlight" onclick="openGlossary('sand_preheating')">900~1,000℃ 적열 상태로 약 4~5분간 예열</span>하여 열충격 균열을 방지합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-orange-200 text-center" onclick="openDiagramZoom('imgStep4', '[Sinchold 현장 사진] STEP 4. 프로판-산소 버너 900~1,000℃ 용접부 예열')">
                            <img id="imgStep4" src="{img_b64_dict['preheating']}" alt="Preheating" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-orange-900 mt-2 block">📷 현장 사진: 900~1,000℃ 가열 버너 예열</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-orange-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep4', '[2D 기술 도식] STEP 4. 프로판 예열 버너 도면')">
                            <svg id="svgStep4" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="105" y="50" width="40" height="60" fill="#f59e0b"/>
                                <path d="M 125 10 L 138 45 L 112 45 Z" fill="#ef4444"/>
                                <text x="125" y="25" font-size="12" font-weight="black" fill="#dc2626" text-anchor="middle">🔥 1,000℃ 예열</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 5 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-red-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">5</div>
                    <span class="bg-red-100 text-red-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 5. 테르밋 쇳물 주입 (Thermite Welding Pouring)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">도가니(Crucible) 솥 2,500℃ 초고온 알루미노 쇳물 자동 주입</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        일회용 도가니 솥에 테르밋 소모품을 점화하여 <span class="term-highlight" onclick="openGlossary('thermite_reaction')">2,500℃ 초고온 용융 쇳물을 반응</span>시키고, 자동 주입 탭을 열어 샌드 몰드 내부로 쇳물을 가득 채웁니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-red-200 text-center" onclick="openDiagramZoom('imgStep5', '[Sinchold 현장 사진] STEP 5. 도가니 2,500℃ 초고온 테르밋 쇳물 주입')">
                            <img id="imgStep5" src="{img_b64_dict['pouring']}" alt="Thermite Welding Pouring" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-red-900 mt-2 block">📷 현장 사진: 2,500℃ 초고온 용융 쇳물 주입</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-red-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep5', '[2D 기술 도식] STEP 5. 2,500℃ 테르밋 쇳물 주입 도면')">
                            <svg id="svgStep5" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <path d="M 100 15 L 150 15 L 135 60 L 115 60 Z" fill="#b45309"/>
                                <line x1="125" y1="60" x2="125" y2="85" stroke="#ef4444" stroke-width="6"/>
                                <rect x="105" y="80" width="40" height="40" fill="#f59e0b"/>
                                <text x="125" y="40" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle">도가니 2,500℃</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 6 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-red-700 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">6</div>
                    <span class="bg-red-100 text-red-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 6. 버 전단 / 핫 쉐어링 (Pushing the Tumor / Hot Shearing)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">쇳물 주입 5분 후 유압 핫 쉐어링 컷터로 Riser 돌출 쇳덩이 전단</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        쇳물 주입 완료 약 4.5~5분 후 적열 상태일 때, 유압 버 전단기(Hot Shear)를 장착하여 레일 상부의 돌출 쇳덩이(Riser/Tumor)를 깔끔하게 전단 제거합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-red-200 text-center" onclick="openDiagramZoom('imgStep6', '[Sinchold 현장 사진] STEP 6. 약 5분 후 유압 버 전단기(Hot Shear) Riser 전단')">
                            <img id="imgStep6" src="{img_b64_dict['shearing']}" alt="Pushing the Tumor Hot Shearing" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-red-900 mt-2 block">📷 현장 사진: 유압 컷터 버(Riser) 전단 제거</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-red-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep6', '[2D 기술 도식] STEP 6. 유압 핫 쉐어링 컷터 전단 도면')">
                            <svg id="svgStep6" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="20" y="70" width="210" height="35" fill="#475569"/>
                                <path d="M 125 40 L 140 70 L 110 70 Z" fill="#dc2626"/>
                                <text x="125" y="30" font-size="12" font-weight="black" fill="#dc2626" text-anchor="middle">유압 버 전단</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 7 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-blue-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">7</div>
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 7. 마무리 정밀 연마 (Finish Grinding)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 주행면 & 측면 1m당 오차 ±0.2mm 이내 정밀 플러시 연마</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        용접부가 식은 후 레일 유압 그라인더를 사용하여 레일 주행면과 궤간 측면을 1m 당 오차 ±0.2mm 이내로 매끈하게 플러시 정밀 연마합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-blue-200 text-center" onclick="openDiagramZoom('imgStep7', '[Sinchold 현장 사진] STEP 7. 레일 유압 그라인더 1m당 ±0.2mm 정밀 연마')">
                            <img id="imgStep7" src="{img_b64_dict['grinding']}" alt="Finish Grinding" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-blue-900 mt-2 block">📷 현장 사진: 1m당 ±0.2mm 정밀 매끈 연마</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-blue-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep7', '[2D 기술 도식] STEP 7. 1m당 ±0.2mm 정밀 연마 도면')">
                            <svg id="svgStep7" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="20" y="60" width="210" height="35" fill="#475569"/>
                                <line x1="20" y1="45" x2="230" y2="45" stroke="#0284c7" stroke-width="3"/>
                                <text x="125" y="35" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">직선도 1m당 &plusmn;0.2mm 연마</text>
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- STEP 8 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">8</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 8. 완성 조인트 & NDT 검사 (Finished Joint & Inspection)</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">레일 복부 용접년도/고유번호 각인 & MT/UT 비파괴검사 100% 승인</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        레일 복부 측면에 <span class="term-highlight" onclick="openGlossary('welder_stamp_marking')">용접년도 및 용접공 고유번호를 스탬프 마킹 각인</span>하고, <span class="term-highlight" onclick="openGlossary('mt_ut_testing')">MT 자분탐상 및 UT 초음파 비파괴검사 100%</span>를 실시하여 최종 감리원 결재를 획득합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-emerald-200 text-center" onclick="openDiagramZoom('imgStep8', '[Sinchold 현장 사진] STEP 8. 완성된 용접 조인트 매끈한 주행면 & NDT 탐상 완료')">
                            <img id="imgStep8" src="{img_b64_dict['finished']}" alt="The Finished Joint" class="w-full h-44 object-cover rounded-lg shadow-sm">
                            <span class="text-[11px] font-bold text-emerald-900 mt-2 block">📷 현장 사진: 완성 조인트 & NDT 100% 합격</span>
                        </div>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl border border-emerald-200 flex justify-center items-center" onclick="openDiagramZoom('svgStep8', '[2D 기술 도식] STEP 8. 용접공 각인 & MT/UT 탐상검사 도면')">
                            <svg id="svgStep8" viewBox="0 0 250 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="250" height="140" fill="#f8fafc"/>
                                <rect x="20" y="60" width="210" height="35" fill="#475569"/>
                                <rect x="110" y="68" width="30" height="18" fill="#fef08a" rx="2"/>
                                <text x="125" y="81" font-size="10" font-weight="black" fill="#854d0e" text-anchor="middle">2026-W09</text>
                                <circle cx="50" cy="60" r="14" fill="#059669"/>
                                <text x="50" y="64" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">NDT</text>
                                <text x="125" y="35" font-size="12" font-weight="black" fill="#059669" text-anchor="middle">MT/UT 탐상 100% & 각인</text>
                            </svg>
                        </div>
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
            f.write(gui_sinchold_8step_html)
        print(f"✏️ Updated WBS 21 Guideline with Sinchold 8-Step Process & Photos: {fpath}")

print("\n🎉 SUCCESSFULLY UPDATED WBS 21 GUIDELINE WITH SINCHOLD 8-STEP PROCESS & PHOTOS!")
