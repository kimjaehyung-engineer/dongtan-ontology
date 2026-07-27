import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

target_folder_name = "1_설계적정성 검토"
for ef in os.listdir(base_dir):
    if "설계적정성" in ef or ef.startswith("1_") or "9000-2-1" in ef:
        target_folder_name = ef
        break

target_folder_path = os.path.join(base_dir, target_folder_name)

std_dir = os.path.join(target_folder_path, "표준서")
gui_dir = os.path.join(target_folder_path, "수행지침")
chk_dir = os.path.join(target_folder_path, "체크리스트")

os.makedirs(std_dir, exist_ok=True)
os.makedirs(gui_dir, exist_ok=True)
os.makedirs(chk_dir, exist_ok=True)

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
    'lter_simulation': {
        title: '📡 LTE-R 무선망 음영 시뮬레이션',
        desc: '동탄트램 700MHz 전파 환경에서 지상/지하/터널 구간의 전파 전파(Propagation) 손실 및 음영지역을 시뮬레이션 프로그램으로 사전 예측하여 안테나 및 기지국 배치를 최적화하는 수칙입니다.'
    },
    'rail_standard_material': {
        title: '📜 철도표준자재 (KRSA / KS / KC)',
        desc: '국가철도공단 표준규격(KRSA) 및 KS/KC 인증을 통과한 광케이블, 통신기계실 랙, LTE-R 안테나 등 신뢰성이 입증된 트램 전용 자재입니다.'
    },
    'system_interface': {
        title: '🌐 타 시스템(토목/건축/전기/신호/PSD/차량) 인터페이스',
        desc: '통신망이 전차선 전기, 신호 궤도회로, PSD 비상통화, 건축 슬리브, 차량 차상 통신장치 및 통합관제센터(OCC)와 물리적·기능적으로 100% 무하자 연동되도록 검토하는 절차입니다.'
    },
    'construction_risk': {
        title: '⚠️ 시공성 및 환경 Risk 검토',
        desc: '옥외/옥내/특수 배선 포설 시 최소 곡률 반경 준수, 굴착 도로 민원, 습기/진동 방지 및 공종 간 간섭 요소를 사전에 분석·제어하는 리스크 평가입니다.'
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
# 1. STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Noto Sans KR', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-2-1 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">통신설계적정성 & 사양 검토 표준서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">설계적정성 검토 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"입찰 요구사항, 철도표준자재, LTE-R 음영 시뮬레이션 & 타 시스템 인터페이스 검증 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 통신공종의 시공 착수 전 설계 적정성 및 사양을 종합 검토하여 설계도서 오류, 재시공 리스크 및 시공 간섭을 사전에 차단하기 위한 공학 표준 수칙입니다. 입찰 요구사항, 철도표준자재, LTE-R 음영 시뮬레이션, 타 시스템 인터페이스, 배관/배선 적정성 및 시공성 Risk를 정밀 검증합니다. (주관: 현장 공무팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 정량적 공학 표준 수칙 (Engineering Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">📡 입찰 요구사항 & LTE-R 음영 시뮬레이션</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>입찰 요구사항 대조:</strong> 입찰안내서, 발주처 요구조건 및 철도표준자재(KRSA/KS) 반영 여부 검토</li>
                        <li><strong>음영지역 시뮬레이션:</strong> 설계단계 음영지역 시뮬레이션 수행 확인 (미반영 시 전파 손실 커버리지 시뮬레이션 필수 반영)</li>
                        <li><strong>용량 및 트래픽:</strong> 정거장 규모, 본선/종점 및 통신 트래픽(72-Core 광망) 고려 통신시스템 용량 산정</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="font-bold text-blue-700 block mb-1">🔗 타 시스템 인터페이스 & 배선/시공 Risk</span>
                    <ul class="list-disc pl-4 space-y-1 text-slate-700">
                        <li><strong>인터페이스 검증:</strong> 토목/건축(슬리브/기계실), 전기(급전), 신호(궤도회로), 차량, PSD 및 관제센터(OCC) 연동 검토</li>
                        <li><strong>배관/배선 적정성:</strong> 옥외/옥내/특수 배선 관로 포설 곡률 반경 및 트레이 점유율(≤40%) 검토</li>
                        <li><strong>환경 Risk & 공정계획:</strong> 현장 굴착/노반 환경 Risk 및 공정계획 적정성 검토 후 회의록 및 보고서 확정</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 필 수 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-2">
                <p>✔️ <strong>설계적정성 회의록:</strong> 공무팀, 시스템팀, 타 분야 협의 및 입찰 대조 회의록</p>
                <p>✔️ <strong>설계검토 보고서:</strong> LTE-R 음영 시뮬레이션, 인터페이스, 시공성 Risk 및 철도표준자재 검토 보고서</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. GUIDELINE HTML (3-Step Cards with 1:1 Matching Light-Theme SVGs)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 수행지침서</title>
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
        <div class="absolute inset-0 bg-gradient-to-r from-blue-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-2-1 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">설계적정성 3단계 visual 수행 지침서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">설계적정성 검토 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"입찰 요구사항, 철도표준자재, 음영 시뮬레이션 & 인터페이스 3단계 visual 검토 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (개념 해설) -->
        <div class="bg-blue-50 border border-blue-200 p-5 rounded-xl text-xs sm:text-sm text-blue-950 shadow-sm space-y-3">
            <h4 class="font-bold text-blue-950 text-base flex items-center gap-2">
                <span>💡</span> 설계적정성 검토(Design Adequacy Review) 친절한 개념 해설
            </h4>
            <div class="bg-white p-4 rounded-lg border border-blue-300 font-medium text-slate-900 leading-relaxed">
                📡 <strong>'설계적정성 검토'란?</strong><br>
                통신 공사 착수 전 입찰안내서 요구사항 및 <strong><span class="term-highlight" onclick="openGlossary('rail_standard_material')">철도표준자재(KRSA/KS)</span></strong> 반영 여부를 검토하고, <strong><span class="term-highlight" onclick="openGlossary('lter_simulation')">LTE-R 무선망 음영지역 시뮬레이션</span></strong> 수행 및 <strong><span class="term-highlight" onclick="openGlossary('system_interface')">타 시스템(토목/건축/전기/신호/차량) 인터페이스</span></strong>를 정밀 대조하여 설계 오류와 재시공 위험을 사전 차단하는 <strong><span class="term-highlight" onclick="openGlossary('construction_risk')">시공성 및 환경 Risk 검토</span></strong> 절차입니다.
            </div>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 4단계 검토 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">입찰/자재 대조 검토</h4>
                    </div>
                    <p class="text-[11px] text-blue-900 mt-2 font-medium">입찰안내서 & 철도표준자재</p>
                </div>

                <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-indigo-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">음영 시뮬레이션 & 인터페이스</h4>
                    </div>
                    <p class="text-[11px] text-indigo-900 mt-2 font-medium">LTE-R 커버리지 & 72-Core 광망</p>
                </div>

                <div class="bg-cyan-50 p-4 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-cyan-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">배선 & 시공 Risk 검토</h4>
                    </div>
                    <p class="text-[11px] text-cyan-900 mt-2 font-medium">옥내/옥외/특수 배선 & 환경 Risk</p>
                </div>

                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">회의록 & 보고서 결재</h4>
                    </div>
                    <p class="text-[11px] text-emerald-900 mt-2 font-medium">설계검토 보고서 최종 제출</p>
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
                    <div class="absolute -left-[37px] top-5 bg-blue-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 입찰 요구사항 및 자재 대조 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">입찰안내서 요구조건 & 철도표준자재(KRSA/KS) 정밀 대조</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        발주처 입찰안내서의 성능 요구조건과 <span class="term-highlight" onclick="openGlossary('rail_standard_material')">국가철도공단 표준규격(KRSA) 및 KS/KC 자재 반영 여부</span>를 1:1 대조·검토하여 미반영 항목을 선제 도출합니다.
                    </p>
                    
                    <!-- STEP 1 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 입찰 요구사항 & 철도표준자재(KRSA/KS) 정밀 대조 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                            
                            <!-- 서류 1: 입찰안내서 -->
                            <rect x="50" y="30" width="180" height="100" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="6"/>
                            <text x="140" y="55" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">입찰안내서 요구조건</text>
                            <line x1="70" y1="70" x2="210" y2="70" stroke="#cbd5e1" stroke-width="2"/>
                            <line x1="70" y1="90" x2="210" y2="90" stroke="#cbd5e1" stroke-width="2"/>
                            <text x="140" y="115" font-size="12" font-weight="bold" fill="#2563eb" text-anchor="middle">통신 트래픽/용량 산정</text>

                            <!-- 화살표 및 대조 -->
                            <path d="M 240 80 L 280 80" stroke="#4338ca" stroke-width="3" marker-end="url(#arrow)"/>

                            <!-- 서류 2: 철도표준자재 -->
                            <rect x="290" y="30" width="180" height="100" fill="#ffffff" stroke="#059669" stroke-width="2" rx="6"/>
                            <text x="380" y="55" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">철도표준자재(KRSA)</text>
                            <line x1="310" y1="70" x2="450" y2="70" stroke="#cbd5e1" stroke-width="2"/>
                            <text x="380" y="115" font-size="12" font-weight="bold" fill="#059669" text-anchor="middle">KS / KC 규격 1:1 검증</text>
                            <text x="260" y="160" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">입찰 요구사항 & 철도표준자재 1:1 대조 검토</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-indigo-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-indigo-100 text-indigo-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. LTE-R 음영 시뮬레이션 & 인터페이스 검토 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">LTE-R 무선망 음영 시뮬레이션 & 타 시스템 인터페이스 검증</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        <span class="term-highlight" onclick="openGlossary('lter_simulation')">설계 단계 LTE-R 음영지역 시뮬레이션을 수행</span>하여 커버리지를 확인하고, <span class="term-highlight" onclick="openGlossary('system_interface')">타 시스템(토목/건축/전기/신호/차량/PSD/관제) 간 인터페이스</span> 가능 여부를 정밀 대조합니다.
                    </p>

                    <!-- STEP 2 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgStep2_Card', '[본 검토] LTE-R 음영지역 시뮬레이션 & 타 시스템 인터페이스 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                            
                            <!-- 무선 망 기지국 & 전파 커버리지 -->
                            <rect x="40" y="30" width="210" height="110" fill="#ffffff" stroke="#0284c7" stroke-width="2" rx="6"/>
                            <text x="145" y="55" font-size="13" font-weight="black" fill="#0369a1" text-anchor="middle">LTE-R 무선망 커버리지</text>
                            <path d="M 70 100 Q 145 60 220 100" fill="none" stroke="#38bdf8" stroke-width="3" stroke-dasharray="4,2"/>
                            <text x="145" y="118" font-size="12" font-weight="bold" fill="#0284c7" text-anchor="middle">음영지역 시뮬레이션 검증</text>

                            <!-- 타 시스템 인터페이스 연동 -->
                            <rect x="270" y="30" width="210" height="110" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="6"/>
                            <text x="375" y="55" font-size="13" font-weight="black" fill="#3730a3" text-anchor="middle">타 시스템 인터페이스</text>
                            <text x="375" y="85" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">토목/건축 슬리브 · 전기 급전</text>
                            <text x="375" y="105" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">신호 궤도회로 · PSD · 관제</text>
                            <text x="260" y="160" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">LTE-R 전파 시뮬레이션 & 이종 시스템 연동 확정</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-5 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 시공성 Risk 검토 및 보고서 체결 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">배관/배선 적정성, 현장 시공성 Risk 검토 & 보고서 결재</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        옥외/옥내/특수 배선 관로 규격 및 현장 설치 시공성/환경 Risk를 종합 평가하고, <span class="term-highlight" onclick="openGlossary('construction_risk')">설계적정성 회의록 및 최종 설계검토 보고서</span>를 결재 제출합니다.
                    </p>

                    <!-- STEP 3 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[마감 승인] 배관/배선 시공성 Risk 검토 & 회의록/보고서 체결 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                            
                            <!-- 종합 보고서 양식 -->
                            <rect x="140" y="25" width="240" height="115" fill="#ffffff" stroke="#059669" stroke-width="2.5" rx="8"/>
                            <text x="260" y="52" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">설계적정성 검토 보고서</text>
                            <line x1="160" y1="65" x2="360" y2="65" stroke="#cbd5e1" stroke-width="2"/>
                            <text x="260" y="85" font-size="11" font-weight="bold" fill="#059669" text-anchor="middle">✔ 음영 시뮬레이션 완료</text>
                            <text x="260" y="105" font-size="11" font-weight="bold" fill="#059669" text-anchor="middle">✔ 시공성 & 환경 Risk 평가 합격</text>
                            <text x="260" y="160" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">설계적정성 회의록 & 설계검토 보고서 최종 체결</text>
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
# 3. CHECKLIST HTML (질문형 어미 "~하였는가?" 100% 적용, 엑셀 8대 방법 1:1)
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-blue: #1d4ed8;
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
            color: #1e40af;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: #2563eb;
        }}
        .summary-box {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #1e40af;
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
            color: #2563eb;
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
        <h1 class="title">설계적정성 검토 체크리스트</h1>
        <span class="meta">WBS Code 9000-2-1 | 통신 설계검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 1.05rem; font-weight: 800;">📋 설계적정성 검토 8대 필드 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 엑셀 시방에 명시된 8개 핵심 검토 방법(입찰 요구사항, 철도표준자재, 인터페이스, 음영 시뮬레이션, 배관/배선, 시공성 Risk 등)을 1:1 반영하여 작성되었으며, 모든 항목은 질문형 어미(~하였는가?)로 구성되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (엑셀 시방 8대 검토 수칙)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#1e40af;">⚠️ 사전 대조<br>(Step 1 요구조건)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 1. 입찰 반영</span>
                        <strong>[입찰 요구사항]</strong> 발주처 입찰안내서의 통신 요구조건이 설계도서에 충실히 반영되었는지 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 1. 표준 자재</span>
                        <strong>[철도표준자재]</strong> <span class="term-highlight" onclick="openGlossary('rail_standard_material')">국가철도공단 표준규격(KRSA) 및 KS/KC 인증 표준자재</span>가 적용되었는지 확인**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 1. 통신 용량</span>
                        <strong>[트래픽 용량]</strong> 종점, 정거장 규모 및 72-Core 광 백본 트래픽을 고려하여 통신시스템 용량을 산정**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#4338ca;">📡 무선 & 인터페이스<br>(Step 2 시뮬레이션)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">Step 2. 음영 지역</span>
                        <strong>[음영 시뮬레이션]</strong> 설계 단계에서 <span class="term-highlight" onclick="openGlossary('lter_simulation')">LTE-R 전파 음영지역 시뮬레이션</span>을 시행하였는지 체크**하였는가?** (미반영 시 반영 추진)
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">Step 2. 시스템 인터페이스</span>
                        <strong>[이종 연동]</strong> <span class="term-highlight" onclick="openGlossary('system_interface')">타 시스템(토목, 건축, 전기, 신호, 차량, PSD, 관제)</span> 간 인터페이스 연동 가능 여부를 확인**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">🤝 배관 & Risk 마감<br>(Step 3 최종결재)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 배관 배선</span>
                        <strong>[배관 적정성]</strong> 옥외/옥내/특수 배선 관로 포설 및 트레이 케이블 적정성을 사전 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 환경 Risk</span>
                        <strong>[시공성 Risk]</strong> <span class="term-highlight" onclick="openGlossary('construction_risk')">현장 설치 시공성, 굴착 환경 Risk 및 통신 공정계획</span>의 적정성을 체크**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 산출물 결재</span>
                        <strong>[보고서 체결]</strong> 설계적정성 회의록 및 최종 설계검토 보고서를 작성하여 결재 제출**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-2-1 설계적정성 검토 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Write all HTML files with both original and prefixed names
for fname in ["설계적정성 검토_표준서.html", "1_설계적정성 검토_표준서.html", "9000-2-1_설계적정성 검토_표준서.html"]:
    with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
        f.write(std_html)

for fname in ["설계적정성 검토_수행지침.html", "1_설계적정성 검토_수행지침.html", "9000-2-1_설계적정성 검토_수행지침.html"]:
    with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
        f.write(gui_html)

for fname in ["설계적정성 검토_체크리스트.html", "1_설계적정성 검토_체크리스트.html", "9000-2-1_설계적정성 검토_체크리스트.html"]:
    with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
        f.write(chk_html)

print("\n🎉 SUCCESSFULLY ENHANCED ALL 3 MASTER HTML FILES FOR WBS 9000-2-1 설계적정성 검토!")
