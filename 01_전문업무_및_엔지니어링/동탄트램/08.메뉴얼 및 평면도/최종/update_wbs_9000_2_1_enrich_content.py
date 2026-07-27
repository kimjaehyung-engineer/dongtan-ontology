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
        desc: '동탄트램 700MHz 전파 환경에서 지상/지하/터널 구간의 전파 전파(Propagation) 손실 및 음영지역을 시뮬레이션 프로그램으로 사전 예측하여 수신 레벨 ≥ -95dBm 및 안테나 배치를 최적화하는 수칙입니다.'
    },
    'rail_standard_material': {
        title: '📜 철도표준자재 (KRSA / KS / KC)',
        desc: '국가철도공단 표준규격(KRSA 5007-R3 / KRSA 5008-R2) 및 KS/KC 인증을 통과한 72-Core 광케이블, 통신기계실 랙, LTE-R 안테나 등 신뢰성이 입증된 트램 전용 자재입니다.'
    },
    'system_interface': {
        title: '🌐 타 시스템(토목/건축/전기/신호/PSD/차량) 8대 인터페이스',
        desc: '통신망이 전기 DC 750V, 신호 궤도회로, PSD 비상통화, 건축 통신기계실 슬리브, 차량 차상 통신장치 및 통합관제센터(OCC)와 물리적·기능적으로 100% 무하자 연동되도록 검토하는 절차입니다.'
    },
    'construction_risk': {
        title: '⚠️ 배관/배선 시공성 및 환경 Risk 검토',
        desc: '옥외/옥내/특수 배선 포설 시 최소 곡률 반경(R≥10D), 케이블 트레이 점유율(≤40%) 준수, 굴착 도로 민원, 습기/진동 방지 및 공종 간 간섭 요소를 사전에 분석·제어하는 리스크 평가입니다.'
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
    
    const innerImg = zoomBody.querySelector('img');
    if (innerImg) {
        innerImg.style.maxHeight = '75vh';
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
# 1. ENRICHED STANDARD HTML
# -------------------------------------------------------------------------
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 마스터 표준서</title>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">통신설계적정성 & 사양 검토 마스터 표준서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">설계적정성 검토 마스터 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"입찰 요구사항, 철도표준자재(KRSA), LTE-R 음영 시뮬레이션 & 8대 이종 시스템 인터페이스 무결성 수칙"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 통신공종의 시공 착수 전 설계 적정성 및 사양을 종합 검토하여 설계도서 오류, 재시공 리스크 및 시공 간섭을 사전에 차단하기 위한 공학 표준 수칙입니다. 입찰 요구사항, 국가철도공단 표준자재(KRSA), LTE-R 음영지역 시뮬레이션(커버리지 ≥-95dBm), 8대 이종 시스템 인터페이스, 배관/배선 규격(R≥10D, 점유율≤40%) 및 시공성 Risk를 정밀 검증합니다. (주관: 현장 공무팀)
            </p>
        </div>

        <!-- 1. 정량적 공학 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 정량적 공학 표준 및 법적 준수 수칙 (Engineering & Legal Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
                    <span class="font-bold text-blue-700 block text-base border-b pb-1">📡 입찰 요구사항 & LTE-R 전파 시뮬레이션</span>
                    <ul class="list-disc pl-4 space-y-1.5 text-slate-700">
                        <li><strong>입찰 요구조건 대조:</strong> 발주청 입찰안내서, 기술시방서 요구 사양(72-Core 광 백본망, LTE-R SIL 4, 4K CCTV, PIS/PA) 1:1 검토</li>
                        <li><strong>철도표준자재 반영:</strong> 국가철도공단 표준규격(KRSA 5007-R3 / KRSA 5008-R2) 및 KS/KC 공인 자재 선별 준수</li>
                        <li><strong>전파 음영지역 시뮬레이션:</strong> 설계단계 700MHz 전파 전파 시뮬레이션 필수 시행 (수신 레벨 ≥ -95dBm 확보, 미반영 시 시뮬레이션 수립 추진)</li>
                        <li><strong>통신 트래픽 용량 산정:</strong> 동탄트램 정거장 18개소, 본선 및 관제센터 트래픽 용량을 고려한 72-Core 광 백본 설계 검증</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
                    <span class="font-bold text-blue-700 block text-base border-b pb-1">🔗 8대 이종 시스템 연동 & 배선/시공 Risk</span>
                    <ul class="list-disc pl-4 space-y-1.5 text-slate-700">
                        <li><strong>8대 시스템 인터페이스:</strong> 토목(슬리브), 건축(기계실), 전기(DC 750V 급전), 신호(궤도회로), 차량, PSD, 도로교통, 관제센터(OCC) 연동 확정</li>
                        <li><strong>배관/배선 시공 규격:</strong> 옥외/옥내/특수 배선 최소 곡률 반경(R ≥ 10D), 케이블 트레이 점유율(≤ 40%) 및 광 접속 손실(≤ 0.05dB) 검토</li>
                        <li><strong>현장 환경 Risk 평가:</strong> 도로 굴착 민원, 진동/습기 방지, 선로변 설치 시공성 및 타 공종 간 간섭 요소를 선제 도출·제어</li>
                        <li><strong>법정 인허가 준비:</strong> 정보통신공사업법 제36조 사용전검사 및 전파법 제21조/제24조 무선국 허가/준공 검사 일정 사전 대조</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 증빙 산출물 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 필 수 증 빙 산 출 물 (Deliverables)
            </h2>
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm text-xs sm:text-sm space-y-3">
                <p class="flex items-center gap-2">✔️ <strong>설계적정성 회의록:</strong> 공무팀, 시스템팀, 감리단 및 타 공종(토목/건축/전기/신호) 3자 체결 회의록</p>
                <p class="flex items-center gap-2">✔️ <strong>설계검토 보고서:</strong> LTE-R 음영 시뮬레이션 결과서, 인터페이스 관리대장, 시공성 Risk 및 KRSA 표준자재 검토 종합 보고서</p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------------------
# 2. ENRICHED GUIDELINE HTML (Rich Content + Expanded Flow Architecture + 3 Detailed SVGs)
# -------------------------------------------------------------------------
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 마스터 수행지침서</title>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">설계적정성 3단계 visual 마스터 수행 지침서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">설계적정성 검토 마스터 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"입찰 요구사항, 철도표준자재(KRSA), LTE-R 음영 시뮬레이션 & 8대 이종 시스템 인터페이스 3단계 visual 검토 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (풍부한 개념 해설) -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-xs sm:text-sm text-blue-950 shadow-sm space-y-4">
            <h4 class="font-bold text-blue-950 text-base flex items-center gap-2">
                <span>💡</span> 설계적정성 검토(Design Adequacy Review) 핵심 개념 및 기술 지침
            </h4>
            <div class="bg-white p-5 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed space-y-2">
                <p>📡 <strong>'설계적정성 검토'란 무엇인가?</strong><br>
                동탄트램 통신 공사 착수 전 입찰안내서 요구조건 및 <strong><span class="term-highlight" onclick="openGlossary('rail_standard_material')">국가철도공단 표준규격(KRSA) 및 KS/KC 자재</span></strong> 반영 여부를 검토하고, <strong><span class="term-highlight" onclick="openGlossary('lter_simulation')">LTE-R 무선망 음영지역 시뮬레이션(커버리지 ≥ -95dBm)</span></strong> 수행 및 <strong><span class="term-highlight" onclick="openGlossary('system_interface')">8대 이종 시스템(토목/건축/전기/신호/차량/PSD/관제/도로교통) 인터페이스</span></strong>를 정밀 대조하여 설계 오류와 재시공 위험을 사전 차단하는 <strong><span class="term-highlight" onclick="openGlossary('construction_risk')">시공성 및 환경 Risk 검토</span></strong> 마스터 절차입니다.</p>
            </div>
        </div>

        <!-- 1. 4단계 시공 마스터 흐름 요약 (Expanded Flow Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 4단계 검토 마스터 프로세스 (Expanded Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <!-- STEP 1 BOX -->
                <div class="bg-blue-50 p-5 rounded-2xl border border-blue-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-blue-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 1</span>
                            <span class="text-[10px] font-bold text-blue-700 bg-blue-100 px-2 py-0.5 rounded">사전준비</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">입찰/자재 대조 검토</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>입찰안내서 요구조건 1:1 검토</li>
                            <li>KRSA/KS/KC 표준자재 반영</li>
                            <li>72-Core 광망 트래픽 용량 산정</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-blue-200 text-center">
                        <span class="text-[10px] font-bold text-blue-900">📌 KRSA 5007-R3 규격 검증</span>
                    </div>
                </div>

                <!-- STEP 2 BOX -->
                <div class="bg-indigo-50 p-5 rounded-2xl border border-indigo-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-indigo-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 2</span>
                            <span class="text-[10px] font-bold text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">본 검토</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">음영 시뮬레이션 & 연동</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>LTE-R 커버리지(≥-95dBm) 검증</li>
                            <li>미반영 시 전파 시뮬레이션 추진</li>
                            <li>8대 이종 시스템 인터페이스 대조</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-indigo-200 text-center">
                        <span class="text-[10px] font-bold text-indigo-900">📡 무선망 전파 시뮬레이션</span>
                    </div>
                </div>

                <!-- STEP 3 BOX -->
                <div class="bg-cyan-50 p-5 rounded-2xl border border-cyan-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-cyan-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 3</span>
                            <span class="text-[10px] font-bold text-cyan-700 bg-cyan-100 px-2 py-0.5 rounded">시공성 평가</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">배선 & 시공 Risk 검토</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>관로 곡률 반경(R≥10D) 검토</li>
                            <li>트레이 점유율(≤40%) 검증</li>
                            <li>굴착/노반 환경 Risk 평가</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-cyan-200 text-center">
                        <span class="text-[10px] font-bold text-cyan-900">⚠️ 현장 환경 Risk 제어</span>
                    </div>
                </div>

                <!-- STEP 4 BOX -->
                <div class="bg-emerald-50 p-5 rounded-2xl border border-emerald-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-emerald-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 4</span>
                            <span class="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">마감 승인</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">회의록 & 보고서 결재</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>공무/시스템/감리 3자 서명</li>
                            <li>설계적정성 회의록 작성</li>
                            <li>설계검토 보고서 사업관리 제출</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-emerald-200 text-center">
                        <span class="text-[10px] font-bold text-emerald-900">📄 최종 보고서 체결</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 3단계 체계별 세부 작업 수행절차 (알찬 2D visual 도식 수록) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure & Enriched Visual Diagrams)
            </h2>
            
            <div class="space-y-10 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 CARD -->
                <div class="bg-white p-7 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-6 bg-blue-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">1</div>
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 입찰 요구사항 및 철도표준자재 대조 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">입찰안내서 요구조건 & 철도표준자재(KRSA/KS) 1:1 대조 및 트래픽 산정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        발주처 입찰안내서의 통신 요구조건과 <span class="term-highlight" onclick="openGlossary('rail_standard_material')">국가철도공단 표준규격(KRSA 5007-R3 / 5008-R2) 및 KS/KC 인증 자재</span> 반영 여부를 1:1 정밀 대조합니다. 동탄트램 18개 정거장 및 본선 72-Core 광 백본 트래픽 용량을 검증하여 누락 사양을 선제 도출합니다.
                    </p>
                    
                    <!-- STEP 1 RICH 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 입찰 요구사항 & 철도표준자재(KRSA/KS) 1:1 대조 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
                            
                            <!-- 서류 1: 입찰안내서 -->
                            <rect x="30" y="25" width="220" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                            <rect x="30" y="25" width="220" height="30" fill="#eff6ff" rx="8"/>
                            <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">📋 입찰안내서 요구 사양</text>
                            <line x1="45" y1="65" x2="235" y2="65" stroke="#93c5fd" stroke-width="1.5"/>
                            <text x="50" y="85" font-size="11" font-weight="bold" fill="#334155">• 72-Core 광 백본 및 이중화 링</text>
                            <text x="50" y="105" font-size="11" font-weight="bold" fill="#334155">• LTE-R SIL 4 무선 통신 망</text>
                            <text x="50" y="125" font-size="11" font-weight="bold" fill="#334155">• 4K IP CCTV & PIS/PA 방송연동</text>

                            <!-- 화살표 및 1:1 검증 뱃지 -->
                            <path d="M 260 85 L 290 85" stroke="#4338ca" stroke-width="3"/>
                            <polygon points="290,80 300,85 290,90" fill="#4338ca"/>
                            <rect x="252" y="98" width="46" height="20" fill="#e0e7ff" rx="4"/>
                            <text x="275" y="112" font-size="10" font-weight="black" fill="#3730a3" text-anchor="middle">1:1 검증</text>

                            <!-- 서류 2: 철도표준자재 -->
                            <rect x="305" y="25" width="215" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                            <rect x="305" y="25" width="215" height="30" fill="#ecfdf5" rx="8"/>
                            <text x="412" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">📜 철도표준자재 (KRSA)</text>
                            <line x1="320" y1="65" x2="505" y2="65" stroke="#6ee7b7" stroke-width="1.5"/>
                            <text x="325" y="85" font-size="11" font-weight="bold" fill="#334155">• KRSA 5007-R3 기지국 규격</text>
                            <text x="325" y="105" font-size="11" font-weight="bold" fill="#334155">• KRSA 5008-R2 광케이블 사양</text>
                            <text x="325" y="125" font-size="11" font-weight="bold" fill="#334155">• KS/KC 인증 제품 100% 선별</text>

                            <!-- 하단 캡션 -->
                            <rect x="30" y="155" width="490" height="30" fill="#1e293b" rx="6"/>
                            <text x="275" y="175" font-size="13" font-weight="black" fill="#38bdf8" text-anchor="middle">입찰 요구 사양 vs KRSA 철도표준자재 1:1 대조 무하자 확인</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-7 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-6 bg-indigo-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-indigo-100 text-indigo-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. LTE-R 음영 시뮬레이션 & 8대 인터페이스 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">LTE-R 무선망 음영지역 시뮬레이션 & 8대 이종 시스템 인터페이스 연동 검증</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        <span class="term-highlight" onclick="openGlossary('lter_simulation')">설계 단계 700MHz 전파 전파 시뮬레이션을 수행</span>하여 전파 수신 레벨(≥ -95dBm)을 확인하고 미반영 시 시뮬레이션을 반영합니다. 또한 <span class="term-highlight" onclick="openGlossary('system_interface')">8대 이종 시스템(토목/건축/전기/신호/차량/PSD/관제/도로교통) 인터페이스</span> 연동 기준을 대조·확정합니다.
                    </p>

                    <!-- STEP 2 RICH 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgStep2_Card', '[본 검토] LTE-R 전파 음영 시뮬레이션 & 8대 이종 시스템 인터페이스 맵')">
                        <svg id="svgStep2_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
                            
                            <!-- 무선 망 전파 시뮬레이션 -->
                            <rect x="30" y="25" width="230" height="125" fill="#ffffff" stroke="#0284c7" stroke-width="2" rx="8"/>
                            <rect x="30" y="25" width="230" height="30" fill="#e0f2fe" rx="8"/>
                            <text x="145" y="45" font-size="13" font-weight="black" fill="#0369a1" text-anchor="middle">📡 LTE-R 700MHz 전파 시뮬레이션</text>
                            <path d="M 50 110 Q 145 65 240 110" fill="none" stroke="#0284c7" stroke-width="3" stroke-dasharray="4,2"/>
                            <text x="145" y="85" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">전파 수신 레벨 ≥ -95dBm 확보</text>
                            <text x="145" y="130" font-size="11" font-weight="bold" fill="#0284c7" text-anchor="middle">본선·터널 음영지역 Zero화 검증</text>

                            <!-- 8대 인터페이스 네트워크 -->
                            <rect x="280" y="25" width="240" height="125" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="8"/>
                            <rect x="280" y="25" width="240" height="30" fill="#e0e7ff" rx="8"/>
                            <text x="400" y="45" font-size="13" font-weight="black" fill="#3730a3" text-anchor="middle">🌐 8대 이종 시스템 인터페이스</text>
                            <text x="400" y="73" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">1. 토목 슬리브  2. 건축 기계실</text>
                            <text x="400" y="93" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">3. 전기 DC750V  4. 신호 궤도회로</text>
                            <text x="400" y="113" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">5. 트램 차량   6. PSD 비상통화</text>
                            <text x="400" y="133" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">7. 관제 센터   8. 도로교통 관제</text>

                            <!-- 하단 캡션 -->
                            <rect x="30" y="160" width="490" height="30" fill="#1e293b" rx="6"/>
                            <text x="275" y="180" font-size="13" font-weight="black" fill="#38bdf8" text-anchor="middle">LTE-R 무선 커버리지 전파 검증 & 8대 이종 시스템 연동 확정</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-7 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-6 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 시공성 Risk 평가 및 최종 보고서 결재 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">배관/배선 규격 검토, 현장 시공성 Risk 평가 & 최종 보고서 체결</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        옥외/옥내/특수 배선 관로 규격(최소 곡률 반경 R ≥ 10D, 케이블 트레이 점유율 ≤ 40%) 및 현장 굴착 환경 Risk를 종합 평가하고, <span class="term-highlight" onclick="openGlossary('construction_risk')">설계적정성 회의록 및 최종 설계검토 보고서</span>를 3자(공무/시스템/감리) 체결 후 제출합니다.
                    </p>

                    <!-- STEP 3 RICH 2D Visual Diagram (글씨 13px bold) -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[마감 승인] 배관/배선 시공성 Risk 평가 & 설계검토 보고서 체결 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
                            
                            <!-- 종합 결재 보고서 서식 -->
                            <rect x="110" y="20" width="330" height="135" fill="#ffffff" stroke="#059669" stroke-width="2.5" rx="8"/>
                            <rect x="110" y="20" width="330" height="30" fill="#ecfdf5" rx="8"/>
                            <text x="275" y="40" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">📄 동탄트램 통신 설계적정성 최종 검토 보고서</text>
                            <line x1="125" y1="58" x2="425" y2="58" stroke="#a7f3d0" stroke-width="1.5"/>
                            <text x="135" y="78" font-size="11" font-weight="bold" fill="#334155">✔ 관로 곡률 반경(R≥10D) & 트레이 점유율(≤40%) 검증</text>
                            <text x="135" y="98" font-size="11" font-weight="bold" fill="#334155">✔ 현장 굴착/노반 환경 Risk 평가서 합격</text>
                            
                            <!-- 3자 서명 란 -->
                            <rect x="135" y="108" width="85" height="35" fill="#f8fafc" stroke="#cbd5e1" rx="4"/>
                            <text x="177" y="123" font-size="10" font-weight="bold" fill="#64748b" text-anchor="middle">공무팀장 (인)</text>
                            <text x="177" y="137" font-size="10" font-weight="black" fill="#059669" text-anchor="middle">Sign [완료]</text>

                            <rect x="232" y="108" width="85" height="35" fill="#f8fafc" stroke="#cbd5e1" rx="4"/>
                            <text x="274" y="123" font-size="10" font-weight="bold" fill="#64748b" text-anchor="middle">시스템팀장 (인)</text>
                            <text x="274" y="137" font-size="10" font-weight="black" fill="#059669" text-anchor="middle">Sign [완료]</text>

                            <rect x="330" y="108" width="85" height="35" fill="#f8fafc" stroke="#cbd5e1" rx="4"/>
                            <text x="372" y="123" font-size="10" font-weight="bold" fill="#64748b" text-anchor="middle">책임감리원 (인)</text>
                            <text x="372" y="137" font-size="10" font-weight="black" fill="#059669" text-anchor="middle">Sign [승인]</text>

                            <!-- 하단 캡션 -->
                            <rect x="30" y="165" width="490" height="28" fill="#1e293b" rx="6"/>
                            <text x="275" y="184" font-size="13" font-weight="black" fill="#38bdf8" text-anchor="middle">배관/배선 시공 규격 검증 & 3자 서명 최종 체결 완료</text>
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
# 3. ENRICHED CHECKLIST HTML (12 Detailed Interrogative Items, "~하였는가?" 100%)
# -------------------------------------------------------------------------
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 마스터 체크리스트</title>
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
        <h1 class="title">설계적정성 검토 마스터 체크리스트</h1>
        <span class="meta">WBS Code 9000-2-1 | 통신 설계검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 1.05rem; font-weight: 800;">📋 설계적정성 검토 12대 정밀 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 엑셀 시방의 8개 검토 방법 및 시공성 Risk 평가 항목을 12개 정밀 점검 항목으로 확장 구성하였으며, 모든 항목의 문장 끝은 예외 없이 질문형 어미(~하였는가?)로 100% 정형화되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">필수 검측 항목 (12대 정밀 검토 수칙)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:#1e40af;">⚠️ 사전 대조<br>(Step 1 요구조건)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">1. 입찰 반영</span>
                        <strong>[입찰 요구사항]</strong> 발주처 입찰안내서의 통신 요구조건이 설계도서에 충실히 반영되었는지 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">2. 표준 자재</span>
                        <strong>[철도표준자재]</strong> <span class="term-highlight" onclick="openGlossary('rail_standard_material')">국가철도공단 표준규격(KRSA 5007-R3 / 5008-R2) 및 KS/KC 자재</span>가 적용되었는지 확인**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">3. 트래픽 용량</span>
                        <strong>[통신 용량]</strong> 정거장 18개소, 본선 및 관제센터 트래픽을 고려하여 72-Core 광 백본 용량을 산정**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">4. 도서 오류</span>
                        <strong>[설계도서 확인]</strong> 도면, 시방서, 물량내역서 간 수치 불일치 및 재시공 리스크 요소를 사전 도출**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#4338ca;">📡 무선 & 인터페이스<br>(Step 2 연동검증)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">5. 전파 음영</span>
                        <strong>[음영 시뮬레이션]</strong> 설계 단계에서 <span class="term-highlight" onclick="openGlossary('lter_simulation')">LTE-R 700MHz 전파 시뮬레이션(수신 레벨 ≥ -95dBm)</span>을 시행하였는지 체크**하였는가?** (미반영 시 추진)
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">6. 토목/건축</span>
                        <strong>[슬리브 및 기계실]</strong> 토목 구조물 슬리브 및 건축 통신기계실 랙 배치, 반입동선 인터페이스를 대조**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">7. 전기/신호</span>
                        <strong>[급전 및 궤도회로]</strong> 전기 DC 750V 급전 유도장해 방지 및 신호 궤도회로 연동 가능 여부를 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">8. 차량/PSD/관제</span>
                        <strong>[차상 및 관제]</strong> 차량 차상 통신, PSD 비상통화 및 통합관제센터(OCC) 영상 표출 인터페이스를 확인**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">🤝 배관 & Risk 마감<br>(Step 3 체결승인)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">9. 배관 곡률</span>
                        <strong>[관로 곡률반경]</strong> 옥외/옥내/특수 배선 포설 시 케이블 최소 곡률 반경(R ≥ 10D) 규격을 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">10. 트레이 점유율</span>
                        <strong>[트레이 용량]</strong> 케이블 트레이 내 케이블 단면적 점유율(≤ 40%) 및 열 방산 공간을 확인**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">11. 시공성 Risk</span>
                        <strong>[환경 Risk 평가]</strong> <span class="term-highlight" onclick="openGlossary('construction_risk')">도로 굴착 민원, 진동/습기 방지 및 공정계획</span>의 적정성을 체크**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">12. 보고서 체결</span>
                        <strong>[3자 최종 결재]</strong> 공무/시스템/감리 3자 서명이 포함된 설계적정성 회의록 및 설계검토 보고서를 제출**하였는가?**
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

print("\n🎉 SUCCESSFULLY ENRICHED CONTENTS AND SVGs FOR ALL 3 MASTER HTML FILES OF WBS 9000-2-1!")
