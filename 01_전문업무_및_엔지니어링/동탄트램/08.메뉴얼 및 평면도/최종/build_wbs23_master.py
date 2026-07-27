import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

# Find all WBS 23 matching folders
wbs23_folders = []
for item in os.listdir(base_dir):
    if item.startswith("23_") or "후속공사" in item or "인수인계" in item:
        wbs23_folders.append(os.path.join(base_dir, item))

if not wbs23_folders:
    wbs23_folders = [
        os.path.join(base_dir, "23_후속공사 인수인계"),
        os.path.join(base_dir, "23_후속공사인수인계")
    ]

for f in wbs23_folders:
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
    'handover_protocol': {
        title: '📋 후속공사 인수인계 (Handover to Subsequent Works)',
        desc: '완공된 콘크리트도상 궤도 구간을 후속 공종인 전기(전차선/급전), 신호(신호기/궤도회로), 통신 부서가 안심하고 시공할 수 있도록 3자 입회 하에 관리권을 공식 이관하는 시방 절차입니다.'
    },
    'insulation_resistance': {
        title: '⚡ 궤도 회로 절연저항 (≥ 100MΩ)',
        desc: '신호 제어 전류 유출 및 누설전류(Stray Current) 부식을 방지하기 위해 궤도 절연 블록 및 정크션 본드 구간의 절연저항을 100MΩ 이상으로 정밀 검측하는 품질 기준입니다.'
    },
    'alignment_sheet': {
        title: '📐 준공 CAD 궤도 정완표 (Alignment Sheet)',
        desc: '궤도 완공 후 레일 중심선, 궤간(+3mm,-1mm), 캔트, 수평, 평탄도 실측치를 CAD 준공 도면과 1:1 대조·검증하는 대장입니다.'
    },
    'joint_inspection': {
        title: '🤝 궤도/전기/신호 3자 합동 입회 검측',
        desc: '궤도공사 담당자, 전기 담당자, 신호 담당자가 현장에 함께 입회하여 궤간, 절연, 신호 연동 부위를 현장 검증하고 3자 공동 서명을 체결하는 합동 절차입니다.'
    },
    'ndt_strength_reports': {
        title: '📑 NDT 용접 성과표 & 콘크리트 강도 성적서',
        desc: '레일 가스압접/테르밋 용접부 100% NDT(MT/UT) 비파괴검사 보고서와 TCL 콘크리트 28일 압축강도(≥30MPa/35MPa) 합격 성적서를 최종 첨부하여 제출하는 서류입니다.'
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
# 1. WBS 23 STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 후속공사 인수인계 표준서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-23 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">궤도 완공 3자 인수인계 표준서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">후속공사 인수인계 표준서</h1>
            <p class="text-indigo-200 mt-2 text-sm sm:text-base">"궤도/전기/신호 3자 입회, 절연저항 ≥ 100MΩ, NDT/강도 성적서 & 3자 서명 체결 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-indigo-50 border border-indigo-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-indigo-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-indigo-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 콘크리트도상 궤도공사 완공 후, 후속 공종인 전기, 신호, 통신 분야가 무하자 시공을 진행할 수 있도록 궤도/전기/신호/노반 담당자 입회 하에 궤도 회로 절연저항(≥100MΩ), 궤간 오차, 용접 NDT 성과표 및 콘크리트 강도 성적서를 대조 검증하고 3자 공동 서명 날인으로 관리권을 공식 이관하는 최종 준공 인수인계 규정입니다. (주관: 현장 공사팀 / 품질팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-indigo-700 block mb-1">⚡ 절연저항 & 3자 합동 검측</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>절연저항 기준:</strong> 전기/신호/노반 입회 하 궤도 회로 절연저항 <strong>&ge; 100M&Omega; 이상</strong> 검측</li>
                        <li><strong>3자 현장 입회:</strong> 궤도/전기/신호 담당자 현장 합동 입회 및 궤각 오차 확인</li>
                        <li><strong>궤도 제형 대조:</strong> 궤간(+3mm, -1mm), 캔트, 수평 실측치 CAD 정완표 대조</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-indigo-700 block mb-1">📑 준공 성적서 & 3자 서명 날인</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>NDT 용접 성과표:</strong> 레일 용접부 100% NDT(MT/UT) 비파괴 합격 보고서 첨부</li>
                        <li><strong>강도 성적서:</strong> 궤도 콘크리트 28일 압축강도(&ge;30MPa/35MPa) 합격 성적서 확인</li>
                        <li><strong>3자 공동 체결:</strong> 궤도 완공 인수인계서 3자 공동 서명 날인 및 준공 CAD 대장 제출</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 서식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">2.</span> 필 수 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-2">
                <p>✔️ <strong>궤도 완공 인수서류:</strong> 궤도/전기/신호 3자 공동 서명 날인 완공 인수인계서</p>
                <p>✔️ <strong>절연저항 성적서:</strong> 궤도 회로 절연저항 &ge; 100M&Omega; 측정 결과표 및 검측 기록지</p>
                <p>✔️ <strong>준공 CAD 대장:</strong> CAD 준공 도면, NDT 용접 성과표, 콘크리트 강도 성적서 최종 대장</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. WBS 23 GUIDELINE HTML (3-Step Procedure Cards with Embedded Visual Diagrams)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 후속공사 인수인계 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-23 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">후속공사 인수인계 3단계 visual 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">후속공사 인수인계 수행지침서</h1>
            <p class="text-indigo-200 mt-2 text-sm sm:text-base">"3자 합동 입회, 절연저항 ≥ 100MΩ, NDT/강도 성적서 대조 & 3자 인수 서명 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (개념 해설) -->
        <div class="bg-indigo-50 border border-indigo-200 p-5 rounded-xl text-xs sm:text-sm text-indigo-950 shadow-sm space-y-3">
            <h4 class="font-bold text-indigo-950 text-base flex items-center gap-2">
                <span>💡</span> 후속공사 인수인계(Handover to Subsequent Works) 친절한 개념 해설
            </h4>
            <div class="bg-white p-4 rounded-lg border border-indigo-300 font-medium text-slate-900 leading-relaxed">
                📋 <strong>'후속공사 인수인계'란?</strong><br>
                완공된 콘크리트도상 궤도 구조물을 후속 분야(전차선 전기, 신호 제어, 통신 등)가 안심하고 시공할 수 있도록, <strong><span class="term-highlight" onclick="openGlossary('joint_inspection')">궤도/전기/신호 3자 입회 하에 현장 검측</span></strong>을 실시하고, <strong><span class="term-highlight" onclick="openGlossary('insulation_resistance')">궤도 회로 절연저항 ≥ 100MΩ</span></strong>, NDT 성과표 및 콘크리트 강도 성적서를 대조하여 <strong><span class="term-highlight" onclick="openGlossary('handover_protocol')">3자 공동 서명으로 인수인계를 최종 체결</span></strong>하는 최종 마감 공정입니다.
            </div>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">1.</span> 4단계 인수인계 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-indigo-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">서류 & 준공 CAD 대조</h4>
                    </div>
                    <p class="text-[11px] text-indigo-900 mt-2 font-medium">NDT 성과표 & 강도 성적서 확인</p>
                </div>

                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">3자 현장 합동 입회</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">궤도/전기/신호 오차 검측</p>
                </div>

                <div class="bg-cyan-50 p-4 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-cyan-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">절연저항 ≥ 100MΩ 검측</h4>
                    </div>
                    <p class="text-[11px] text-cyan-900 mt-2 font-medium">궤도 회로 절연 테스트 완료</p>
                </div>

                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">3자 인수 서명 체결</h4>
                    </div>
                    <p class="text-[11px] text-emerald-900 mt-2 font-medium">인수서류 공동 서명 & 이관</p>
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
                    <div class="absolute -left-[37px] top-5 bg-indigo-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-indigo-100 text-indigo-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 사전 서류 검증 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">준공 CAD 도면 대조 & 레일 NDT 용접/콘크리트 강도 성적서 확인</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        완공 구간에 대한 준공 CAD 궤도 정완표와 실제 선로 위치를 1:1 대조하고, 레일 용접부 100% NDT(MT/UT) 성과표 및 <span class="term-highlight" onclick="openGlossary('ndt_strength_reports')">콘크리트 28일 강도 성적서(&ge;30MPa/35MPa)</span>를 사전 서류 검증합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 검증] 준공 CAD 도면 & 레일 NDT/콘크리트 강도 성적서 대조 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- CAD 준공 도면 및 성적서 서류 -->
                            <rect x="60" y="35" width="180" height="110" fill="#ffffff" stroke="#6366f1" stroke-width="2" rx="6"/>
                            <text x="150" y="60" font-size="13" font-weight="black" fill="#4338ca" text-anchor="middle">준공 CAD 궤도 정완표</text>
                            <line x1="80" y1="75" x2="220" y2="75" stroke="#cbd5e1" stroke-width="2"/>
                            <line x1="80" y1="95" x2="220" y2="95" stroke="#cbd5e1" stroke-width="2"/>
                            <text x="150" y="125" font-size="12" font-weight="bold" fill="#6366f1" text-anchor="middle">NDT/강도 합격 대조</text>

                            <!-- 궤도 선로 -->
                            <rect x="280" y="85" width="180" height="30" fill="#475569"/>
                            <line x1="240" y1="90" x2="280" y2="90" stroke="#4338ca" stroke-width="3" stroke-dasharray="3,2"/>
                            <text x="370" y="65" font-size="13" font-weight="black" fill="#1e293b" text-anchor="middle">실제 완공 선로 1:1 검증</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-blue-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 현장 합동 입회 및 절연 검측 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">궤도/전기/신호 3자 합동 입회 & 절연저항 ≥ 100MΩ 정밀 실측</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        궤도, 전기, 신호 담당자가 현장에 동시 입회하여 <span class="term-highlight" onclick="openGlossary('joint_inspection')">궤간 오차 및 수평 상태를 합동 확인</span>하고, 절연계(Megger)로 <span class="term-highlight" onclick="openGlossary('insulation_resistance')">궤도 회로 절연저항 &ge; 100M&Omega; 이상</span>을 정밀 실측합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgStep2_Card', '[본 시공] 궤도/전기/신호 3자 합동 현장 입회 & 절연저항 ≥ 100MΩ 실측 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 궤도 선로 -->
                            <rect x="40" y="90" width="440" height="35" fill="#475569"/>
                            
                            <!-- 3자 입회 아이콘 (궤도/전기/신호) -->
                            <circle cx="120" cy="50" r="18" fill="#4f46e5"/>
                            <text x="120" y="55" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">궤도</text>
                            
                            <circle cx="260" cy="50" r="18" fill="#0284c7"/>
                            <text x="260" y="55" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">전기</text>
                            
                            <circle cx="400" cy="50" r="18" fill="#059669"/>
                            <text x="400" y="55" font-size="11" font-weight="black" fill="#ffffff" text-anchor="middle">신호</text>
                            
                            <!-- 절연 테스터 (≥ 100MΩ) -->
                            <rect x="200" y="115" width="120" height="30" fill="#0284c7" rx="4"/>
                            <text x="260" y="135" font-size="13" font-weight="black" fill="#ffffff" text-anchor="middle">절연저항 &ge; 100M&Omega;</text>
                            <text x="260" y="165" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">3자 합동 현장 절연저항 실측</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 서명 및 관리권 이관 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">3자 공동 완공 인수인계서 서명 날인 & 준공 CAD 대장 최종 제출</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        모든 검측 항목 합격 시 <span class="term-highlight" onclick="openGlossary('handover_protocol')">궤도/전기/신호 3자 공동 서명 날인</span>을 인수인계 서류에 체결하고, 절연저항 결과표 및 준공 CAD 대장을 최종 제출하여 완공 구간 관리권을 공식 이관합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[인수 체결] 3자 공동 완공 인수인계서 서명 날인 & 준공 CAD 대장 제출 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 520 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="200" fill="#f8fafc"/>
                            
                            <!-- 인수인계 체결 서류 -->
                            <rect x="140" y="30" width="240" height="120" fill="#ffffff" stroke="#059669" stroke-width="2.5" rx="8"/>
                            <text x="260" y="55" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">궤도 완공 인수인계 체결서</text>
                            
                            <!-- 3자 서명 인장 -->
                            <circle cx="180" cy="100" r="16" fill="#ec4899"/>
                            <text x="180" y="104" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">궤도</text>

                            <circle cx="260" cy="100" r="16" fill="#3b82f6"/>
                            <text x="260" y="104" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">전기</text>

                            <circle cx="340" cy="100" r="16" fill="#10b981"/>
                            <text x="340" y="104" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">신호</text>

                            <text x="260" y="170" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">3자 공동 서명 날인 & CAD 준공 대장 인수인계 완료</text>
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
# 3. WBS 23 CHECKLIST HTML (질문형 어미 "~하였는가?" 100% 적용)
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 후속공사 인수인계 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-indigo: #4338ca;
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
            color: #3730a3;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: #4338ca;
        }}
        .summary-box {{
            background: #eef2ff;
            border: 1px solid #c7d2fe;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #3730a3;
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
            color: #4338ca;
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
        <h1 class="title">후속공사 인수인계 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-23 | 궤도 완공 인수인계 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #312e81; font-size: 1.05rem; font-weight: 800;">📋 후속공사 3자 인수인계 O/X 필수 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 궤도/전기/신호 3자 입회 하 절연저항 ≥ 100MΩ 검측, 준공 CAD 궤도 정완표 대조, NDT 용접 성과표 및 콘크리트 강도 성적서 확인, 3자 공동 서명 인수를 체결하기 위해 작성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (궤도 완공 3자 인수인계 규격)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#3730a3;">⚠️ 사전 준비<br>(Step 1 서류검증)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">Step 1. 도면 대조</span>
                        <strong>[CAD 정완표]</strong> 준공 CAD 궤도 정완표와 실제 선로의 위치 및 오차를 대조 확인**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">Step 1. 품질 성적서</span>
                        <strong>[통합 성과표]</strong> <span class="term-highlight" onclick="openGlossary('ndt_strength_reports')">레일 NDT 용접 성과표 및 콘크리트 28일 강도 성적서</span>를 첨부 확인**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#0284c7;">⚡ 현장 입회<br>(Step 2 절연저항)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 3자 입회</span>
                        <strong>[합동 입회]</strong> <span class="term-highlight" onclick="openGlossary('joint_inspection')">궤도, 전기, 신호 담당자 3자 합동 입회</span> 하에 현장 인수인계를 진행**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 절연 검측</span>
                        <strong>[절연저항]</strong> <span class="term-highlight" onclick="openGlossary('insulation_resistance')">궤도 회로 절연저항 &ge; 100M&Omega; 이상</span>으로 정상 검측**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">🤝 인수 체결<br>(Step 3 3자 서명)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 3자 서명</span>
                        <strong>[공동 서명]</strong> <span class="term-highlight" onclick="openGlossary('handover_protocol')">궤도 완공 인수인계서에 3자 공동 서명 날인</span>**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. CAD 제출</span>
                        <strong>[대장 제출]</strong> 절연저항 결과표 및 준공 CAD 대장을 최종 제출**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-23 후속공사 인수인계 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write to all WBS 23 folder variants
for folder_path in wbs23_folders:
    std_dir = os.path.join(folder_path, "표준서")
    gui_dir = os.path.join(folder_path, "수행지침")
    chk_dir = os.path.join(folder_path, "체크리스트")
    
    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(gui_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)
    
    # Standard files
    for fname in ["후속공사 인수인계_표준서.html", "23_후속공사 인수인계_표준서.html", "후속공사인수인계_표준서.html", "23_후속공사인수인계_표준서.html"]:
        with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
            f.write(std_html)
            
    # Guideline files
    for fname in ["후속공사 인수인계_수행지침.html", "23_후속공사 인수인계_수행지침.html", "후속공사인수인계_수행지침.html", "23_후속공사인수인계_수행지침.html"]:
        with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
            f.write(gui_html)
            
    # Checklist files
    for fname in ["후속공사 인수인계_체크리스트.html", "23_후속공사 인수인계_체크리스트.html", "후속공사인수인계_체크리스트.html", "23_후속공사인수인계_체크리스트.html"]:
        with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
            f.write(chk_html)

print("\n🎉 SUCCESSFULLY BUILT ALL MASTER FILES FOR WBS 23 후속공사 인수인계!")
