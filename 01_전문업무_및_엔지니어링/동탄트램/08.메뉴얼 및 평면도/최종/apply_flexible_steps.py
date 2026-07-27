import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

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

# Common Modals JS/HTML
common_modal_html = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 기술 해설</h3>
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
    'subcontractor_pool': {
        title: '👥 시공실적 적격 업체 Pool',
        desc: '유사 노면트램, 철도, 도시철도 정보통신 공사의 구축 및 영업운행 시공 실적이 입증된 적격 통신 전문 협력업체 선별 체계입니다.'
    },
    'eight_site_conditions': {
        title: '📋 8대 현장조건 정밀 항목',
        desc: '1) 자재 제작기간 2) 유경험 기술인력 3) 대관업무/소모품 4) 사용전검사 교육비 5) 내역서 누락 6) 창고 임대비 7) 공사용 용수/전력 8) 준공 후 상주 기술지원비 등 8개 항목을 예산에 사전 반영하는 절차입니다.'
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
# 1. WBS 9000-2-1 FLEXIBLE 5-STEP GUIDELINE HTML
# -------------------------------------------------------------------------
adequacy_5step_gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 설계적정성 검토 5단계 수행지침서</title>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">설계적정성 5단계(5-Step) 융통적 수행지침서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">설계적정성 검토 5단계 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"입찰 대조 ➔ 음영 시뮬레이션 ➔ 이종 연동 ➔ 시공 Risk ➔ 3자 체결 5단계 visual 실무 지침"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개념 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-xs sm:text-sm text-blue-950 shadow-sm space-y-3">
            <h4 class="font-bold text-blue-950 text-base flex items-center gap-2">
                <span>💡</span> 설계적정성 검토 유연 5단계(5-Step Master Architecture) 핵심 개념
            </h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                본 지침서는 공종의 기술적 복잡성을 직관적으로 반영하여 <strong>① 입찰/자재 대조 ➔ ② LTE-R 전파 시뮬레이션 ➔ ③ 8대 이종 연동 ➔ ④ 배관/배선 시공 Risk ➔ ⑤ 3자 보고서 체결</strong>의 <strong>유연 5단계(5-Step) 체계</strong>로 구성되어 현장 엔지니어가 명확히 업무를 이행하도록 가이드합니다.
            </p>
        </div>

        <!-- 5단계 마스터 프로세스 (Flexible 5-Step Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 5단계 검토 마스터 프로세스 (Flexible 5-Step Architecture)
            </h2>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 1</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">입찰/자재 대조</h4>
                    <p class="text-[11px] text-blue-900 mt-1 font-medium">• KRSA/KS 자재 반영<br>• 광망 용량 산정</p>
                </div>
                <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <span class="bg-indigo-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">LTE-R 전파 검증</h4>
                    <p class="text-[11px] text-indigo-900 mt-1 font-medium">• 음영 시뮬레이션<br>• 수신레벨 ≥ -95dBm</p>
                </div>
                <div class="bg-cyan-50 p-4 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <span class="bg-cyan-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">8대 이종 연동</h4>
                    <p class="text-[11px] text-cyan-900 mt-1 font-medium">• 토목/건축/전기/신호<br>• 차량/PSD/관제 연동</p>
                </div>
                <div class="bg-teal-50 p-4 rounded-xl border border-teal-200 flex flex-col justify-between">
                    <span class="bg-teal-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">시공 Risk 평가</h4>
                    <p class="text-[11px] text-teal-900 mt-1 font-medium">• 관로 R≥10D 준수<br>• 트레이 점유율≤40%</p>
                </div>
                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 5</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">3자 보고서 체결</h4>
                    <p class="text-[11px] text-emerald-900 mt-1 font-medium">• 공무/시스템/감리<br>• 종합 보고서 결재</p>
                </div>
            </div>
        </div>

        <!-- 2D Visual SVG Diagrams (Steps 1~3) -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 세부 수행절차 & 2D Visual 기술 도식 (Enriched 2D Diagrams)
            </h2>

            <!-- CARD 1 -->
            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full">STEP 1. 입찰안내서 & KRSA 철도표준자재 1:1 대조</span>
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgStep1_Card', '[1단계] 입찰안내서 & KRSA 표준자재 1:1 대조 도면')">
                    <svg id="svgStep1_Card" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                        <rect x="30" y="20" width="220" height="110" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="6"/>
                        <text x="140" y="42" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">📋 입찰안내서 요구조건</text>
                        <text x="50" y="70" font-size="11" font-weight="bold" fill="#334155">• 72-Core 광 백본망 이중화</text>
                        <text x="50" y="90" font-size="11" font-weight="bold" fill="#334155">• LTE-R SIL 4 무선망 커버리지</text>
                        <text x="50" y="110" font-size="11" font-weight="bold" fill="#334155">• 4K IP CCTV & PIS/PA 연동</text>

                        <path d="M 260 75 L 290 75" stroke="#4338ca" stroke-width="3"/>
                        <polygon points="290,70 300,75 290,80" fill="#4338ca"/>

                        <rect x="305" y="20" width="215" height="110" fill="#ffffff" stroke="#059669" stroke-width="2" rx="6"/>
                        <text x="412" y="42" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">📜 KRSA 철도표준자재</text>
                        <text x="325" y="70" font-size="11" font-weight="bold" fill="#334155">• KRSA 5007-R3 기지국 규격</text>
                        <text x="325" y="90" font-size="11" font-weight="bold" fill="#334155">• KRSA 5008-R2 광케이블 사양</text>
                        <text x="325" y="110" font-size="11" font-weight="bold" fill="#334155">• KS / KC 100% 공인자재 선별</text>
                        <text x="275" y="160" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">입찰 요구 사양 vs KRSA 철도표준자재 1:1 대조 완료</text>
                    </svg>
                </div>
            </div>

            <!-- CARD 2 -->
            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <span class="bg-indigo-100 text-indigo-900 text-xs font-bold px-3 py-1 rounded-full">STEP 2 & 3. LTE-R 음영 시뮬레이션 & 8대 이종 연동</span>
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgStep2_Card', '[2~3단계] LTE-R 전파 시뮬레이션 & 8대 이종 연동 도면')">
                    <svg id="svgStep2_Card" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                        <rect x="30" y="20" width="230" height="115" fill="#ffffff" stroke="#0284c7" stroke-width="2" rx="6"/>
                        <text x="145" y="42" font-size="13" font-weight="black" fill="#0369a1" text-anchor="middle">📡 LTE-R 전파 시뮬레이션</text>
                        <path d="M 50 95 Q 145 55 240 95" fill="none" stroke="#0284c7" stroke-width="3" stroke-dasharray="4,2"/>
                        <text x="145" y="75" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">전파 수신 레벨 ≥ -95dBm</text>
                        <text x="145" y="115" font-size="11" font-weight="bold" fill="#0284c7" text-anchor="middle">본선/터널 음영 Zero화 검증</text>

                        <rect x="280" y="20" width="240" height="115" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="6"/>
                        <text x="400" y="42" font-size="13" font-weight="black" fill="#3730a3" text-anchor="middle">🌐 8대 이종 연동 인터페이스</text>
                        <text x="400" y="68" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">1. 토목 슬리브  2. 건축 기계실</text>
                        <text x="400" y="88" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">3. 전기 DC750V  4. 신호 궤도회로</text>
                        <text x="400" y="108" font-size="11" font-weight="bold" fill="#4338ca" text-anchor="middle">5. 트램 차량   6. PSD 비상통화</text>
                        <text x="275" y="160" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">LTE-R 무선 커버리지 전파 검증 & 8대 이종 연동 확정</text>
                    </svg>
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
# 2. WBS 9000-2-2 FLEXIBLE 6-STEP GUIDELINE HTML
# -------------------------------------------------------------------------
kom_6step_gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 발주전략 KOM 6단계 수행지침서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-2-2 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">발주전략 KOM 6단계(6-Step) 융통적 수행지침서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 6단계 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"도면대조 ➔ 업체분석 ➔ 8대조건계상 ➔ 예산검증 ➔ 일정조율 ➔ 소장결재 6단계 visual 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개념 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-xs sm:text-sm text-blue-950 shadow-sm space-y-3">
            <h4 class="font-bold text-blue-950 text-base flex items-center gap-2">
                <span>💡</span> 발주전략 KOM 유연 6단계(6-Step Master Architecture) 핵심 개념
            </h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                본 지침서는 발주 업무의 특성에 맞추어 <strong>① 도면대조 ➔ ② 적격 업체Pool 분석 ➔ ③ 8대 현장조건 계상 ➔ ④ 내역 누락 예산검증 ➔ ⑤ 법정 인허가 일정 조율 ➔ ⑥ 현장소장 결재</strong>의 <strong>유연 6단계(6-Step) 체계</strong>로 구성되어 무결한 발주 실행을 가이드합니다.
            </p>
        </div>

        <!-- 6단계 마스터 프로세스 (Flexible 6-Step Architecture) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 6단계 발주 마스터 프로세스 (Flexible 6-Step Architecture)
            </h2>
            
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
                <div class="bg-blue-50 p-3 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <span class="bg-blue-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 1</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">도면 대조</h4>
                    <p class="text-[10px] text-blue-900 mt-1 font-medium">• 통신도면 분석<br>• 현장 여건 대조</p>
                </div>
                <div class="bg-indigo-50 p-3 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <span class="bg-indigo-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">업체 Pool</h4>
                    <p class="text-[10px] text-indigo-900 mt-1 font-medium">• 철도/트램 실적<br>• 유경험 인력</p>
                </div>
                <div class="bg-cyan-50 p-3 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <span class="bg-cyan-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">8대 조건</h4>
                    <p class="text-[10px] text-cyan-900 mt-1 font-medium">• 창고/전력/용수<br>• 교육비 계상</p>
                </div>
                <div class="bg-teal-50 p-3 rounded-xl border border-teal-200 flex flex-col justify-between">
                    <span class="bg-teal-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">예산 검증</h4>
                    <p class="text-[10px] text-teal-900 mt-1 font-medium">• 내역 누락 확인<br>• 상주인력비 계상</p>
                </div>
                <div class="bg-sky-50 p-3 rounded-xl border border-sky-200 flex flex-col justify-between">
                    <span class="bg-sky-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 5</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">일정 조율</h4>
                    <p class="text-[10px] text-sky-900 mt-1 font-medium">• 무선국 허가<br>• 사용전검사 준공</p>
                </div>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <span class="bg-emerald-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 6</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">소장 결재</h4>
                    <p class="text-[10px] text-emerald-900 mt-1 font-medium">• KOM 결과서 체결<br>• 현장설명서 확정</p>
                </div>
            </div>
        </div>

        <!-- 2D Visual SVG Diagrams -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 세부 수행절차 & 2D Visual 기술 도식 (Enriched 2D Diagrams)
            </h2>

            <!-- CARD 1 -->
            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <span class="bg-indigo-100 text-indigo-900 text-xs font-bold px-3 py-1 rounded-full">STEP 3 & 4. 8대 현장조건 정밀 계상 & 예산 무결성 검증</span>
                <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgStep2_Card', '[3~4단계] 8대 현장조건 계상 & 예산 무결성 도면')">
                    <svg id="svgStep2_Card" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                        <rect x="30" y="20" width="490" height="115" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="8"/>
                        <rect x="30" y="20" width="490" height="28" fill="#e0e7ff" rx="8"/>
                        <text x="275" y="39" font-size="12" font-weight="black" fill="#3730a3" text-anchor="middle">📋 8대 현장조건 계상 및 예산 내역 누락 재검증</text>

                        <text x="45" y="68" font-size="11" font-weight="bold" fill="#334155">1. 자재 제작/수급 기간 반영</text>
                        <text x="45" y="86" font-size="11" font-weight="bold" fill="#334155">2. 철도 유경험 기술자 투입</text>
                        <text x="45" y="104" font-size="11" font-weight="bold" fill="#334155">3. 대관업무 & 소모품 지원</text>
                        <text x="45" y="122" font-size="11" font-weight="bold" fill="#334155">4. 사용전검사 교육비 포함</text>

                        <text x="280" y="68" font-size="11" font-weight="bold" fill="#334155">5. 예산내역서 누락 항목 검토</text>
                        <text x="280" y="86" font-size="11" font-weight="bold" fill="#334155">6. 현장 자재창고 임대비 포함</text>
                        <text x="280" y="104" font-size="11" font-weight="bold" fill="#334155">7. 공사용 전기/용수/오수 시설</text>
                        <text x="280" y="122" font-size="11" font-weight="bold" fill="#334155">8. 가동 후 상주 인력비 계상</text>

                        <text x="275" y="158" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">8대 현장조건 100% 반영으로 예산 무결성 확보</text>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Overwrite for WBS 9000-2-1 (설계적정성 검토 - 5단계 체계 적용)
folder_1_path = os.path.join(base_dir, "1_설계적정성 검토")
if os.path.exists(folder_1_path):
    gui_p = os.path.join(folder_1_path, "수행지침")
    if os.path.exists(gui_p):
        for f in os.listdir(gui_p):
            if f.endswith('.html'):
                with open(os.path.join(gui_p, f), 'w', encoding='utf-8') as out:
                    out.write(adequacy_5step_gui_html)
                print("UPDATED 5-STEP GUIDELINE HTML FOR:", f)

# Overwrite for WBS 9000-2-2 (발주전략 KOM / 착수전략 KOM - 6단계 체계 적용)
for f_name in os.listdir(base_dir):
    full_f = os.path.join(base_dir, f_name)
    if os.path.isdir(full_f) and ('KOM' in f_name or '2_' in f_name or '9000-2-2' in f_name):
        gui_p = os.path.join(full_f, "수행지침")
        if os.path.exists(gui_p):
            for f in os.listdir(gui_p):
                if f.endswith('.html'):
                    with open(os.path.join(gui_p, f), 'w', encoding='utf-8') as out:
                        out.write(kom_6step_gui_html)
                    print("UPDATED 6-STEP GUIDELINE HTML FOR:", f)

print("\n🎉 SUCCESSFULLY APPLIED FLEXIBLE STEP COUNTS (5-STEP & 6-STEP) TO ALL TARGET GUIDELINE HTML FILES!")
