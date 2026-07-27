import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

target_folder = None
for f in os.listdir(base_dir):
    if f.startswith("3_") or "토목" in f:
        target_folder = os.path.join(base_dir, f)
        break

if not target_folder:
    print("❌ ERROR: Target folder for WBS 9000-2-3 not found!")
    sys.exit(1)

print(f"Target WBS 9000-2-3 Folder: {target_folder}")

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

common_js = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 토목/건축 인터페이스 기술 해설</h3>
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
    'sleeve_penetration': {
        title: '🧱 토목/건축 콘크리트 타설 전 통신 슬리브 관통구',
        desc: '동탄트램 1,2공구 교량, 지하차도 및 정거장 골조 타설 전 72-Core 광케이블 및 전원선 관입용 슬리브(ø100~ø150mm)를 매설 위치에 정확히 시공하여 타공 손상을 방지하는 수칙입니다.'
    },
    'equipment_room_height': {
        title: '🏢 건축 통신기계실·관제실·앰프실·TPS실 마감 층고',
        desc: '통신 기계실 랙(Height 2200mm) 및 케이블 트레이(300~500mm) 적재 공간을 고려하여 천장 마감 층고 최소 3.0m 이상 확보 및 바닥 이중바닥(Access Floor H=300mm) 규격을 검증하는 절차입니다.'
    },
    'fire_stop_seal': {
        title: '🔥 방화 구속(Fire-Stop) 밀폐 씰링',
        desc: '토목/건축 관통 구역 및 벽체 관로 입구에 내화 2시간 이상의 방화 재료로 밀폐 마감하여 화재 시 연기 및 화염 전파를 차단하는 필수 인허가 안전 수칙입니다.'
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
        innerSvg.setAttribute('height', '550px');
        innerSvg.style.maxWidth = '1050px';
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

# 1. STANDARD HTML
std_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 토목 / 건축 인터페이스 협의 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Standard</span>
        <h1 class="text-3xl font-black mt-2">토목 / 건축 인터페이스 협의 표준서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-3 | 주관: 현장 시스템팀 / 토목·건축 기술단</p>
    </div>
    
    <div class="p-8 space-y-8">
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-blue-950 mb-2">🎯 표준 목적 (Objective)</h3>
            <p class="text-slate-700 text-sm font-medium leading-relaxed">
                동탄트램 1,2공구 본선 궤도, 정거장 18개소, 지하차도 및 교량 구조물과 통신 설비(기계실, 관제실, 앰프실, TPS실) 설치 간의 공간적·구조적 인터페이스 요구사항을 사전에 정밀 검토하여 시공 마찰을 차단하고 회의록 및 종합 관리대장의 무결성을 확보함을 목적으로 함.
            </p>
        </div>

        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-blue-600 pb-2">📜 토목 / 건축 인터페이스 시방 수칙 (Methodology)</h3>
            <ul class="space-y-3">
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 1</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>슬리브 위치 및 관로 대조:</strong> 토목/건축 콘크리트 타설 전, 통신 광케이블 및 배선 관입용 슬리브(ø100~ø150mm) 위치와 케이블 인입구 배관관로 규격을 도면 1:1 대조하여 선제 매설함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 2</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>기능실 마감 층고 검증:</strong> 건축 통신기계실, 관제실, 앰프실 및 TPS실의 천장 마감 층고(최소 3.0m 이상) 및 이중바닥(Access Floor H=300mm) 규격을 대조하고 랙 반입 타공 위치를 확인함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 3</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>장비 반입 동선 및 창고 검토:</strong> 고가 통신 랙 및 케이블 드럼 반입을 위한 엘리베이터, 공용구, 반입구 크기와 현장 전용 보관 창고 위치를 토목/건축과 사전 확정함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 4</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>방화 구속 및 방수 씰링:</strong> 벽체 관과 구역에 내화 2시간 이상의 방화 재료(Fire-Stop) 씰링 조치를 확정하여 최종 인터페이스 회의록 및 1,2공구 종합 관리대장을 작성·서명 체결함.</span>
                </li>
            </ul>
        </div>

        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-emerald-950 mb-2">📦 증빙 산출물 (Deliverables)</h3>
            <p class="text-emerald-900 text-sm font-bold">인터페이스 회의록, 토목/건축 슬리브 대조서, 1,2공구 종합 관리대장, 3자 서명 체결 승인서</p>
        </div>
    </div>
</div>
</body>
</html>
"""

# 2. GUIDELINE HTML
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 토목 / 건축 인터페이스 협의 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {zoom_modal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Guideline</span>
        <h1 class="text-3xl font-black mt-2">토목 / 건축 인터페이스 협의 유연 5단계 수행지침서</h1>
        <p class="text-blue-200 text-sm mt-1">"슬리브 관통, 층고 규격 & 반입동선 검증 5단계 2D Visual 마스터 지침"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 친절한 개념 해설 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-sm text-blue-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 토목 / 건축 인터페이스 협의 실무 해설</h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                동탄트램 1,2공구 구조물과 통신 기능실 간의 통합 무결성을 확보하려면 콘크리트 타설 전 슬리브 위치 및 기계실 층고를 사전 조율해야 합니다. 본 지침서는 <strong><span class="term-highlight" onclick="openGlossary('sleeve_penetration')">통신 관통 슬리브</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('equipment_room_height')">기능실 마감 층고</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('fire_stop_seal')">방화 구속(Fire-Stop)</span></strong>을 수록한 <strong>유연 5단계(5-Step) 마스터 프로세스</strong>로 가이드합니다.
            </p>
        </div>

        <!-- ☀️ 라이트 테마 특화 카드 섹션 -->
        <div class="bg-blue-50/70 border border-blue-200 p-7 rounded-2xl shadow-md space-y-6">
            <div class="border-b border-blue-200 pb-4">
                <span class="bg-blue-600 text-white text-xs font-black px-3 py-1 rounded-full uppercase">SPECIAL FOCUS</span>
                <h3 class="text-xl font-black text-blue-950 mt-2">📋 토목/건축 인터페이스 4대 정밀 검토 가이드</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🧱</span> 1. 타설 전 통신 슬리브 매설</span>
                    <p class="text-slate-700 text-xs">콘크리트 타설 전 통신 관통 관로 및 방수 슬리브 위치 1:1 대조 확정.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🏢</span> 2. 통신기계실 마감 층고</span>
                    <p class="text-slate-700 text-xs">기계실, 관제실, 앰프실, TPS실 천장 층고(≥3.0m) 및 타공 규격 확인.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🚛</span> 3. 장비 반입 동선 & 공용구</span>
                    <p class="text-slate-700 text-xs">통신 랙, 관제 서버 반입 엘리베이터 및 반입구 마감 규격 조율.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🔥</span> 4. 방화 구속(Fire-Stop) 마감</span>
                    <p class="text-slate-700 text-xs">관통 부위 내화 2시간 이상 방화 재료 씰링 조치 및 3자 서명 체결.</p>
                </div>
            </div>
        </div>

        <!-- 1. FLEXIBLE 5-STEP ARCHITECTURE -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 5단계 수행 마스터 프로세스 (Flexible 5-Step Architecture)
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2">
                <div class="bg-blue-50 p-3 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <span class="bg-blue-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 1</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">도면 대조</h4>
                    <p class="text-[10px] text-blue-900 mt-1 font-medium">• 1,2공구 구조물<br">• 슬리브 위치 대조</p>
                </div>
                <div class="bg-indigo-50 p-3 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <span class="bg-indigo-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">현장 실측</h4>
                    <p class="text-[10px] text-indigo-900 mt-1 font-medium">• 기계실 층고 검증<br">• 반입 동선 측량</p>
                </div>
                <div class="bg-cyan-50 p-3 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <span class="bg-cyan-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">슬리브 설치</h4>
                    <p class="text-[10px] text-cyan-900 mt-1 font-medium">• 콘크리트 타설 전<br">• 통신관 매설 검측</p>
                </div>
                <div class="bg-teal-50 p-3 rounded-xl border border-teal-200 flex flex-col justify-between">
                    <span class="bg-teal-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">방화 구속</h4>
                    <p class="text-[10px] text-teal-900 mt-1 font-medium">• Fire-Stop 씰링<br">• 인입 관로 밀폐</p>
                </div>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <span class="bg-emerald-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 5</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">3자 체결</h4>
                    <p class="text-[10px] text-emerald-900 mt-1 font-medium">• 회의록 서명<br">• 종합 관리대장 연동</p>
                </div>
            </div>
        </div>

        <!-- 2. 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 2D Visual 기술 도식 (Enriched 2D SVG)
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_r3', '[WBS 9000-2-3] 토목/건축 인터페이스 슬리브 & 층고 2D visual 도식')">
                <svg id="svg_r3" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                    <rect x="30" y="20" width="220" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                    <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">🧱 토목 콘크리트 슬리브 매설</text>
                    <text x="50" y="75" font-size="11" font-weight="bold" fill="#334155">• 타설 전 통신관 매설 위치 1:1</text>
                    <text x="50" y="98" font-size="11" font-weight="bold" fill="#334155">• 방수/방화 씰링 조치 완료</text>

                    <path d="M 260 80 L 290 80" stroke="#2563eb" stroke-width="3"/>
                    <polygon points="290,75 300,80 290,85" fill="#2563eb"/>

                    <rect x="305" y="20" width="215" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                    <text x="412" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🏢 건축 기계실 층고 & 반입동선</text>
                    <text x="325" y="75" font-size="11" font-weight="bold" fill="#334155">• 기계실/관제실 층고 ≥ 3.0m</text>
                    <text x="325" y="98" font-size="11" font-weight="bold" fill="#334155">• 반입구/공용구 마감 검증</text>
                    <text x="275" y="162" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">토목/건축 인터페이스 회의록 및 1,2공구 종합 관리대장 작성 완료</text>
                </svg>
            </div>
        </div>
    </div>
</div>
{common_js}
</body>
</html>
"""

# 3. CHECKLIST HTML (~하였는가? 100%)
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 토목 / 건축 인터페이스 협의 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Checklist</span>
        <h1 class="text-3xl font-black mt-2">토목 / 건축 인터페이스 협의 체크리스트</h1>
        <p class="text-emerald-200 text-sm mt-1">L4 Code: 9000-2-3 | 주관: 현장 시스템팀 / 토목·건축 기술단</p>
    </div>
    
    <div class="p-8 space-y-6">
        <div class="bg-slate-100 p-4 rounded-xl border border-slate-300 flex justify-between items-center text-xs font-bold">
            <span>공종: 통신분야</span>
            <span>작업단위: 토목 / 건축 인터페이스 협의</span>
            <span>산출물: 인터페이스 회의록 및 관리대장</span>
        </div>

        <table class="w-full border-collapse border border-slate-300 text-sm text-left">
            <thead>
                <tr class="bg-slate-800 text-white text-xs">
                    <th class="border border-slate-300 p-3 text-center w-12">NO</th>
                    <th class="border border-slate-300 p-3 text-center">검측 및 점검 항목 statement (질문형 종결어미)</th>
                    <th class="border border-slate-300 p-3 text-center w-20">판정</th>
                </tr>
            </thead>
            <tbody>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">1</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 통신기계실 반입 동선, 공용구, 케이블 인입구 및 층고 등 마감 규격을 대조 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">2</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 토목/건축 콘크리트 타설 전 통신 슬리브 위치를 확인하고 인터페이스 회의록을 작성하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">3</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 건축 통신기계실, 관제실, 앰프실, TPS실 천장 마감 층고(≥3.0m) 유지를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">4</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 고가 장비 반입용 엘리베이터 및 개구부 타공 규격을 검측하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">5</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 관통 구역 내화 2시간 이상 방화 구속(Fire-Stop) 재료 반영 여부를 검토하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">6</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 본선 궤도 및 지하차도 구간 통신 배관 관로 매설 깊이(≥1.2m)를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">7</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 현장 전용 통신 자재 보관 창고 위치 및 보안 시설 확보 여부를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">8</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 정거장 18개소 통신 케이블 인입 관로와 토목 구조물 마찰 유무를 점검하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">9</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 토목/건축 감리원과의 1:1 대조 서명 및 의견 반영 여부를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">10</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 1,2공구 통합 인터페이스 관리대장 최신화 여부를 점검하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">11</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 입찰안내서 및 기본설계 도서 요구조건과의 1:1 부합 여부를 검측하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">12</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 최종 토목/건축 인터페이스 회의록에 현장소장 및 감리원 서명을 체결하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
"""

sub_dirs = {
    "표준서": std_html,
    "수행지침": gui_html,
    "체크리스트": chk_html
}

for s_n, content in sub_dirs.items():
    sp = os.path.join(target_folder, s_n)
    if os.path.exists(sp):
        for fn in os.listdir(sp):
            if fn.endswith('.html'):
                with open(os.path.join(sp, fn), 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                print(f"   ✓ [WBS 9000-2-3 OVERWRITE] {s_n} -> {fn}")

print("\n🎉 SUCCESSFULLY COMPLETED ULTRA-DETAILED ENHANCEMENT FOR WBS 9000-2-3!")
