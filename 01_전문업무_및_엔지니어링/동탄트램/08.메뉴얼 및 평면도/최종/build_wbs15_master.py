import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\15_[반-PC 슬래브] 패널반입 및 설치"

path_std = os.path.join(target_dir, "표준서", "[반-PC 슬래브] 패널반입 및 설치_표준서.html")
path_std_alt = os.path.join(target_dir, "표준서", "15_[반-PC 슬래브] 패널반입 및 설치_표준서.html")

path_gui = os.path.join(target_dir, "수행지침", "[반-PC 슬래브] 패널반입 및 설치_수행지침.html")
path_gui_alt = os.path.join(target_dir, "수행지침", "15_[반-PC 슬래브] 패널반입 및 설치_수행지침.html")

path_chk = os.path.join(target_dir, "체크리스트", "[반-PC 슬래브] 패널반입 및 설치_체크리스트.html")
path_chk_alt = os.path.join(target_dir, "체크리스트", "15_[반-PC 슬래브] 패널반입 및 설치_체크리스트.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully written WBS 15 file: {path}")

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
    'half_pc': {
        title: '🧱 반-PC 슬래브 (Precast Slab Panel)',
        desc: '공장에서 사전 제작되어 현장 반입되는 궤도용 슬래브 구조체입니다. 교차로 및 교량 구간 궤공지지체 공사 시 현장 타설 거푸집 작업을 생략하고 급속 시공을 구현합니다.'
    },
    'support_timber': {
        title: '🪵 받침목 모서리 배치 (패널 1/4, 3/4 지점)',
        desc: 'PC 슬래브 적재 및 임시 거치 시 자중 휨 응력 집중으로 인한 균열을 예방하기 위해, 패널 전체 길이에 대해 모서리부 1/4 및 3/4 지점 좌우 4개소에 고무 받침목을 정밀 배치하는 수칙입니다.'
    },
    'screw_jack': {
        title: '⚙️ Screw Jack 레벨 고정',
        desc: '패널 거치 후 선로 계획고 및 캔트에 맞추어 높낮이를 0.5mm 단위로 조율하는 수직 조정 나사 장치입니다. 정위치 고정 후 콘크리트 2차 타설 전까지 변형을 방지합니다.'
    },
    'flatness_spec': {
        title: '📐 평탄성 오차 ±3mm 이내 & 3D 얼라인먼트',
        desc: '광파 토탈스테이션으로 3차원 노선 좌표를 정합하고, 패널 상면 평탄성을 3m 직선자로 실측하여 오차 ±3mm 이내 달성 시에만 하차 승인하는 표준 수칙입니다.'
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

# =========================================================================
# 1. WBS 15 STANDARD HTML
# =========================================================================
standard_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [반-PC 슬래브] 패널반입 및 설치 기술 표준서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-15 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">패널 평탄성 &plusmn;3mm & 3D 얼라인먼트 규격</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[반-PC 슬래브] 패널반입 및 설치 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"궤광지지체 구간 급속시공: PC 슬래브 균열/오염 검수, 받침목(1/4, 3/4 지점) 배치, Screw Jack 고정 및 평탄성 오차(&plusmn;3mm) 관리"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 💡 핵심 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs sm:text-sm text-amber-900">
            <h4 class="font-bold text-amber-950 mb-1">💡 [반-PC 슬래브] 패널반입 및 설치 과업 정의</h4>
            <p class="leading-relaxed">
                본 공종은 교차로 및 교량 구간의 급속 시공을 위해 <strong><span class="term-highlight" onclick="openGlossary('half_pc')">반-PC 슬래브 패널</span></strong>을 현장에 반입 및 거치하는 기술입니다. 반입 시 균열 및 캔트 제작 치수 검수, 적재 시 <strong><span class="term-highlight" onclick="openGlossary('support_timber')">패널 길이 1/4, 3/4 지점 받침목 4개소 배치</span></strong>, 광파 토탈스테이션 연동 3D 얼라인먼트, <strong><span class="term-highlight" onclick="openGlossary('screw_jack')">Screw Jack 레벨 고정</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('flatness_spec')">패널 평탄성 오차 &plusmn;3mm 이내</span></strong> 거치 표준을 준수합니다.
            </p>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / [반-PC 슬래브] 패널반입 및 설치 (현장 공사팀)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">PC슬래브 거치 수준 실측표 | 평탄성 대장 | 3D 얼라인먼트 측량표</p>
                </div>
            </div>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 반-PC 슬래브 패널 정량 기술 시방 절대 기준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">품질 관리 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 상세 기술 표준 (KCS 시방 연동)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">패널 상면 평탄성 오차</td>
                            <td class="p-3 border text-center font-bold text-red-600">&plusmn;3.0mm 이내</td>
                            <td class="p-3 border text-slate-600">• 3m 직선자를 이용한 상면 고저 凹凸 오차 &plusmn;3.0mm 제어.<br>• 규격 초과 패널 반출 및 재제작 조치 수립</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">받침목 배치 위치</td>
                            <td class="p-3 border text-center font-bold text-blue-700">길이 1/4, 3/4 지점<br>(좌우 4개소)</td>
                            <td class="p-3 border text-slate-600">• 적재 및 임시 거치 시 모서리부 휨 응력 파손 방지.<br>• 고무 침목 패드를 패널 길이에 맞춰 정밀 세팅 후 하차</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">3D 측량 얼라인먼트</td>
                            <td class="p-3 border text-center font-bold text-blue-700">광파 3D 좌표 100% 일치</td>
                            <td class="p-3 border text-slate-600">• 광파 토탈스테이션 연동 보조도상 표시 정위치 거치.<br>• 설계 캔트 및 곡선반경에 맞춰 정밀 위치 안착</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">Screw Jack 레벨 고정</td>
                            <td class="p-3 border text-center font-bold text-blue-700">수평 오차 &plusmn;0.5mm 이내</td>
                            <td class="p-3 border text-slate-600">• 거치 직후 Screw Jack 미세 수직 조정 나사 정위치 고정.<br>• 콘크리트 2차 타설 유동성에 따른 수평 침하 방지 조치</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# =========================================================================
# 2. WBS 15 GUIDELINE HTML (Flexible 4-Step & Light Theme Diagrams)
# =========================================================================
guideline_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [반-PC 슬래브] 패널반입 및 설치 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 to-slate-900 opacity-70"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-15 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">PC 슬래브 거치 & 평탄성 &plusmn;3mm 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[반-PC 슬래브] 패널반입 및 설치 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"받침목(1/4, 3/4 지점) 검수, 광파 3D 측량 셋팅, 정 인양 빔 거치, Screw Jack 고정 및 평탄성 오차(&plusmn;3mm) 가이드"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [반-PC 슬래브] 패널반입 및 설치 실무 핵심
            </h4>
            <p class="leading-relaxed">
                교차로 및 교량 구간 급속 시공을 위한 <strong><span class="term-highlight" onclick="openGlossary('half_pc')">반-PC 슬래브 패널</span></strong> 하차 및 안착 공종입니다. 적재 시 <strong><span class="term-highlight" onclick="openGlossary('support_timber')">패널 모서리 1/4, 3/4 지점 받침목 4개소 배치</span></strong>, 노반 청소 및 광파 토탈스테이션 3D 정밀 좌표 셋팅, 4점 정 인양 빔(Spreader Beam) 거치, <strong><span class="term-highlight" onclick="openGlossary('screw_jack')">Screw Jack 레벨 고정</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('flatness_spec')">평탄성 오차 &plusmn;3mm 이내</span></strong> 검측을 수행합니다.
            </p>
        </div>

        <!-- 1. [Flexible Step Policy 적용] 반-PC 슬래브 4단계 시공 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 반-PC 슬래브 반입·설치 4단계 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">반입 & 받침목 검수</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            패널 균열/오염 점검 & 모서리 <strong>1/4, 3/4 지점</strong> 받침목 4개소 배치 적재
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        🪵 핵심: 1/4, 3/4 받침목 배치
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">노반청소 & 3D 측량</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            보조도상 이물질 청소 & 광파 토탈스테이션 <strong>3D 정밀 좌표계</strong> 셋팅
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        📐 핵심: 광파 3D 좌표 셋팅
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">정인양빔 & 스크류잭</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            정 인양 빔(Spreader Beam) 거치 & <strong>Screw Jack 레벨</strong> 수평 정위치 고정
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        ⚙️ 핵심: Screw Jack 고정
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">평탄성 오차 &plusmn;3mm 검측</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            패널 상면 평탄성 오차 <strong>&plusmn;3.0mm 이내</strong> 3m 직선자 실측 서명
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        📏 핵심: 평탄성 오차 &plusmn;3mm
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. [Light Theme Only Policy 적용] 반-PC 슬래브 정밀 공학 기술 도식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 반-PC 슬래브 거치 & 평탄성 검측 정밀 공학 기술 도식 (🔍 클릭 시 대형 팝업 확대)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 도식 1: PC 슬래브 받침목 배치(1/4, 3/4 지점) & 정 인양 빔 구조 단면도 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 1] 받침목 배치(1/4, 3/4지점) & 정 인양 빔
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">4점 인양 빔</span>
                        </div>
                        
                        <!-- SVG Diagram 1 Container (Clickable Zoom) -->
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram15_1', '[도식 1] 받침목 배치(1/4, 3/4지점) & 정 인양 빔 단면도')">
                            <svg id="svgDiagram15_1" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- 노반 기초 -->
                                <rect x="30" y="170" width="360" height="35" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                                <text x="210" y="192" font-size="11" font-weight="bold" fill="#78350f" text-anchor="middle">보조도상 지층 (이물질 수쇄 청소 완료)</text>

                                <!-- 받침목 (1/4, 3/4 지점) -->
                                <rect x="110" y="150" width="20" height="20" fill="#b45309" stroke="#78350f" stroke-width="1.5"/>
                                <rect x="290" y="150" width="20" height="20" fill="#b45309" stroke="#78350f" stroke-width="1.5"/>
                                <text x="120" y="145" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1/4 지점 받침목</text>
                                <text x="300" y="145" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">3/4 지점 받침목</text>

                                <!-- PC 슬래브 패널 -->
                                <rect x="50" y="100" width="320" height="45" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <text x="210" y="127" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">반-PC 슬래브 패널 (균열/모서리 파손 없음)</text>

                                <!-- 4점 정 인양 빔 (Spreader Beam) -->
                                <line x1="210" y1="15" x2="210" y2="40" stroke="#0284c7" stroke-width="5"/>
                                <rect x="100" y="40" width="220" height="12" fill="#0284c7" rx="2"/>
                                <line x1="120" y1="52" x2="80" y2="100" stroke="#0369a1" stroke-width="2.5"/>
                                <line x1="160" y1="52" x2="150" y2="100" stroke="#0369a1" stroke-width="2.5"/>
                                <line x1="260" y1="52" x2="270" y2="100" stroke="#0369a1" stroke-width="2.5"/>
                                <line x1="300" y1="52" x2="340" y2="100" stroke="#0369a1" stroke-width="2.5"/>
                                <text x="210" y="32" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">크레인 4점 정 인양 빔 (Spreader Beam)</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>🪵 적재/인양 핵심:</strong> PC 슬래브 패널 적재 시 모서리 휨 파손 방지를 위해 <strong>길이 1/4, 3/4 지점 받침목 4개소</strong>를 배치하고, 크레인 <strong>4점 정 인양 빔(Spreader Beam)</strong>으로 수평 하차합니다.
                    </div>
                </div>

                <!-- 도식 2: Screw Jack 레벨 고정 & 3D 광파 얼라인먼트(±3mm) 측량 도면 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 2] Screw Jack 레벨 & 平炭性(&plusmn;3mm)
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">평탄성 &plusmn;3.0mm</span>
                        </div>
                        
                        <!-- SVG Diagram 2 Container (Clickable Zoom) -->
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram15_2', '[도식 2] Screw Jack 레벨 & 평탄성(±3mm) 정밀 측량 도면')">
                            <svg id="svgDiagram15_2" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- 보조도상 기초 -->
                                <rect x="30" y="170" width="360" height="35" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                                <text x="210" y="192" font-size="11" font-weight="bold" fill="#78350f" text-anchor="middle">기초 보조도상 지층</text>

                                <!-- Screw Jack 수직 조절 나사 (좌우) -->
                                <rect x="70" y="145" width="16" height="25" fill="#059669" rx="1"/>
                                <rect x="334" y="145" width="16" height="25" fill="#059669" rx="1"/>
                                <text x="78" y="138" font-size="9" font-weight="black" fill="#047857" text-anchor="middle">Screw Jack</text>
                                <text x="342" y="138" font-size="9" font-weight="black" fill="#047857" text-anchor="middle">Screw Jack</text>

                                <!-- PC 슬래브 패널 -->
                                <rect x="50" y="100" width="320" height="45" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>
                                <text x="210" y="127" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">PC 슬래브 패널 상면 평탄성 오차 ±3.0mm 이내</text>

                                <!-- 3m 직선 자 평탄성 검측 -->
                                <line x1="60" y1="92" x2="360" y2="92" stroke="#dc2626" stroke-width="3"/>
                                <text x="210" y="85" font-size="12" font-weight="black" fill="#dc2626" text-anchor="middle">3m 직선자 실측 (오차 ±3.0mm 이내 합격)</text>

                                <!-- 광파 3D 얼라인먼트 레이저 -->
                                <line x1="385" y1="35" x2="330" y2="100" stroke="#0284c7" stroke-width="2" stroke-dasharray="3,2"/>
                                <circle cx="385" cy="35" r="6" fill="#0284c7"/>
                                <text x="385" y="22" font-size="11" font-weight="black" fill="#0369a1" text-anchor="middle">3D 광파 토탈스테이션 연동</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-100 text-xs text-emerald-900 leading-relaxed">
                        <strong>📏 레벨/평탄성 핵심:</strong> 광파 토탈스테이션 3D 좌표에 맞춰 <strong>Screw Jack 수직 나사로 수평을 고정</strong>하고, 3m 직선자로 패널 상면 <strong>평탄성 오차 &plusmn;3.0mm 이내</strong>를 정밀 검측합니다.
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
                        <h4 class="font-bold text-slate-900 text-sm">PC 슬래브 반입 검수 & 받침목(1/4, 3/4 지점 4개소) 배치 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            패널 현장 반입 시 표면 균열 및 모서리 파손 유무를 전수 조사하고, 휨 응력 파손 방지를 위해 <span class="term-highlight" onclick="openGlossary('support_timber')">패널 길이 1/4, 3/4 지점 좌우 4개소에 받침목</span>을 정밀 배치하여 적재합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">노반 표면 고압 청소 & 3D 광파 토탈스테이션 측량 셋팅 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            보조도상 상부의 돌가루 및 이물질을 고압 수쇄 청소하고, 광파 토탈스테이션을 투입하여 <span class="term-highlight" onclick="openGlossary('flatness_spec')">3차원 노선 설계 좌표계 및 캔트 기준점</span>을 현장에 정밀 셋팅합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">4점 정 인양 빔(Spreader Beam) 거치 & Screw Jack 수평 고정 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            4점 정 인양 빔(Spreader Beam)을 결합하여 패널을 기울임 없이 수평 안착시키며, <span class="term-highlight" onclick="openGlossary('screw_jack')">Screw Jack 레벨 수직 조정 나사</span>를 회전시켜 계획고 레벨 정위치에 단단히 고정합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">패널 상면 평탄성 오차(±3.0mm) 실측 & 인수 서명 마감 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            3m 직선자를 패널 상면에 밀착하여 고저 凹凸 <span class="term-highlight" onclick="openGlossary('flatness_spec')">평탄성 오차가 ±3.0mm 이내</span>임을 감리 입회 하에 측량 확인하고, PC슬래브 거치 수준 실측표에 서명 등록 마감합니다.
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

# =========================================================================
# 3. WBS 15 CHECKLIST HTML
# =========================================================================
checklist_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [반-PC 슬래브] 패널반입 및 설치 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
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
            color: #1e3a8a;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }}
        .summary-box {{
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #065f46;
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
            color: #1e3a8a;
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
        <h1 class="title">[반-PC 슬래브] 패널반입 및 설치 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-15 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 1.05rem; font-weight: 800;">📋 표준서 & 수행지침 연계 반-PC 슬래브 필수 검측 항목</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 PC 슬래브 반입 검수, 모서리 받침목(1/4, 3/4 지점 4개소) 적재, 노반 청소 및 3D 광파 측량, 4점 정 인양 빔 안착, Screw Jack 레벨 고정 및 패널 상면 평탄성 오차(±3.0mm 이내)를 감리 입회 검측하기 위해 수립되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">표준서 & 수행지침 연계 필수 검측 항목 (KCS 47 30 00 수립)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:var(--accent-orange);">⚠️ 사전 준비<br>(Step 1~2 반입/측량)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 반입 & 받침목</span>
                        <strong>[패널 균열 & 받침목 배치]</strong> PC 슬래브 균열 유무 검수 및 패널 길이 <span class="term-highlight" onclick="openGlossary('support_timber')">1/4, 3/4 지점 받침목 4개소</span> 정밀 적재 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 노반청소 & 측량</span>
                        <strong>[노반 청소 & 3D 얼라인먼트]</strong> 보조도상 고압 수쇄 청소 및 광파 토탈스테이션 연동 <b>3D 좌표 100% 일치</b> 셋팅 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-red);">⚡ 본 거치<br>(Step 3 정인양/ScrewJack)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 정 인양 빔</span>
                        <strong>[4점 정 인양 빔 거치]</strong> 모서리 응력 집중에 따른 파손 방지용 <b>4점 Spreader Beam</b> 무균열 패널 안착 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 3. Screw Jack 고정</span>
                        <strong>[Screw Jack 레벨 정위치]</strong> <span class="term-highlight" onclick="openGlossary('screw_jack')">Screw Jack 나사 조율</span>을 통한 선로 수평 레벨 정위치 고정 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-green);">✅ 실측 마감<br>(Step 4 평탄성/대장)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 4. 평탄성 검측</span>
                        <strong>[상면 평탄성 오차 ±3mm]</strong> 3m 직선자 실측 패널 상면 <span class="term-highlight" onclick="openGlossary('flatness_spec')">평탄성 오차 &plusmn;3.0mm 이내</span> 통과 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 4. 실측대장 서명</span>
                        <strong>[PC슬래브 실측표 서명]</strong> 감리 입회 거치 수준 실측표 및 평탄성 대장 확인 서명 마감 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-15 콘크리트도상 [반-PC 슬래브] 패널반입 및 설치 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write files
force_write(path_std, standard_html)
force_write(path_std_alt, standard_html)

force_write(path_gui, guideline_html)
force_write(path_gui_alt, guideline_html)

force_write(path_chk, checklist_html)
force_write(path_chk_alt, checklist_html)

print("\n🎉 SUCCESSFULLY BUILT WBS 15 MASTER HTML FILES!")
