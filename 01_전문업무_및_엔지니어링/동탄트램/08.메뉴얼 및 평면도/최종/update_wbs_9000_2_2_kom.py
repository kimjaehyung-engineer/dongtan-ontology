import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

target_folder_name = "2_발주전략 KOM"
for ef in os.listdir(base_dir):
    if "발주전략" in ef or ef.startswith("2_") or "9000-2-2" in ef:
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
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 발주 기술 해설</h3>
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
    'subcontractor_pool': {
        title: '👥 시공실적 적격 업체 Pool',
        desc: '유사 노면트램, 철도, 도시철도 정보통신 공사의 구축 및 영업운행 시공 실적이 입증된 적격 통신 전문 협력업체 선별 체계입니다.'
    },
    'eight_site_conditions': {
        title: '📋 8대 현장조건 정밀 항목',
        desc: '1) 자재 제작기간 2) 유경험 기술인력 3) 대관업무/소모품 4) 사용전검사 교육비 5) 내역서 누락 6) 창고 임대비 7) 공사용 용수/전력 8) 준공 후 상주 기술지원비 등 8개 항목을 예산에 사전 반영하는 절차입니다.'
    },
    'kom_meeting': {
        title: '🤝 발주전략 KICK-OFF MEETING (KOM)',
        desc: '현장소장 주관으로 하도급 조건, 자재 수급, 무선국 허가 및 사용전검사 일정을 최종 조율하여 KOM 검토결과서 및 현장설명서를 확정하는 킥오프 회의입니다.'
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
    <title>통신분야 - 발주전략 KOM 마스터 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-2-2 Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">발주전략 KOM 마스터 표준서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 마스터 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"발주조건, 적격 시공업체 Pool 분석 & 8대 현장조건을 반영한 최적 발주전략 수립 표준서"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                본 표준서는 동탄도시철도(트램) 통신공사 발주 착수 전 발주조건, 공사기간, 철도/지하철/노면트램 시공실적 업체 Pool 및 8대 현장조건(자재 제작기간, 유경험자, 대관/소모품, 사용전검사 교육비, 내역서 누락, 창고 임대비, 용수/전기, 상주 인력비)을 종합 분석하여 최적의 하도급 및 자재 수급 전략을 수립하는 공학 수칙입니다. (주관: 현장소장)
            </p>
        </div>

        <!-- 1. 정량적 공학 및 행정 표준 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 정량적 공학 및 행정 표준 수칙 (Engineering & Contract Standards)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
                    <span class="font-bold text-blue-700 block text-base border-b pb-1">👥 발주 조건 & 적격 시공업체 Pool 검토</span>
                    <ul class="list-disc pl-4 space-y-1.5 text-slate-700">
                        <li><strong>설계도서 & 현장 대조:</strong> 통신설계 도면과 현장 노반/정거장 제반 여건 대조 검토</li>
                        <li><strong>유경험 업체 Pool 선별:</strong> 유사 노면트램, 철도, 도시철도 구축 및 영업운행 실적이 입증된 적격 시공업체 Pool 구성</li>
                        <li><strong>공종 간 간섭 조율:</strong> 토목, 건축, 전기, 신호 공종과의 발주 시기 및 인터페이스 조율 수칙 준수</li>
                    </ul>
                </div>
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
                    <span class="font-bold text-blue-700 block text-base border-b pb-1">📋 8대 현장조건 반영 & 무결성 확보</span>
                    <ul class="list-disc pl-4 space-y-1.5 text-slate-700">
                        <li><strong>8대 현장조건 검토:</strong> 1) 자재 제작기간 2) 철도 유경험자 3) 대관/소모품 4) 사용전검사 설비 운용/교육비 5) 내역서 누락 6) 창고 임대비 7) 공사용 전기/용수/오수 8) 가동 후 상주 인력비 계상</li>
                        <li><strong>무선국 & 준공 일정:</strong> 전파법 무선국 허가 및 정보통신 사용전검사 법정 준공 일정 사전 반영</li>
                        <li><strong>결과서 작성:</strong> 현장소장 주관으로 최종 KOM 검토결과서 및 현장설명서 무결성 확립</li>
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
                <p class="flex items-center gap-2">✔️ <strong>KOM 검토결과서:</strong> 현장소장 결재, 하도급 전략 및 8대 현장조건 반영 검토 결과서</p>
                <p class="flex items-center gap-2">✔️ <strong>현장설명서:</strong> 입찰 참가 업체를 대상으로 발주조건, 현장 여건, 기술 지원비가 명시된 현장설명 도서</p>
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
    <title>통신분야 - 발주전략 KOM 마스터 수행지침서</title>
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
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">발주전략 KOM 3단계 visual 마스터 수행 지침서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 마스터 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"발주조건, 적격 업체 Pool & 8대 현장조건 반영 3단계 visual 실무 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (풍부한 개념 해설) -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-xs sm:text-sm text-blue-950 shadow-sm space-y-4">
            <h4 class="font-bold text-blue-950 text-base flex items-center gap-2">
                <span>💡</span> 발주전략 Kick-off Meeting(KOM) 핵심 개념 및 기술 지침
            </h4>
            <div class="bg-white p-5 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed space-y-2">
                <p>🤝 <strong>'발주전략 KOM'이란 무엇인가?</strong><br>
                통신공사 발주 착수 전 현장소장 주관으로 발주조건, <strong><span class="term-highlight" onclick="openGlossary('subcontractor_pool')">유공 적격 시공업체 Pool 분석</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('eight_site_conditions')">8대 현장조건(창고 임대, 용수/전력, 상주 인력비, 사용전검사 교육비 등)</span></strong>을 종합 대조하여 예산 누락을 방지하고 <strong><span class="term-highlight" onclick="openGlossary('kom_meeting')">KOM 검토결과서 및 현장설명서</span></strong>의 무결성을 확립하는 실무 프로세스입니다.</p>
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
                        <h4 class="font-black text-slate-900 text-sm">도면 & 업체 Pool 검토</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>통신도면 & 현장여건 대조</li>
                            <li>유경험 업체 Pool 검토</li>
                            <li>영업운행 실적 검증</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-blue-200 text-center">
                        <span class="text-[10px] font-bold text-blue-900">👥 적격 시공업체 Pool 분석</span>
                    </div>
                </div>

                <!-- STEP 2 BOX -->
                <div class="bg-indigo-50 p-5 rounded-2xl border border-indigo-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-indigo-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 2</span>
                            <span class="text-[10px] font-bold text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">본 검토</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">8대 현장조건 & 예산 검증</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>창고/임대/전력/용수 반영</li>
                            <li>상주인력비 & 교육비 검토</li>
                            <li>내역 누락 재검증</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-indigo-200 text-center">
                        <span class="text-[10px] font-bold text-indigo-900">📋 8대 현장조건 정밀 계상</span>
                    </div>
                </div>

                <!-- STEP 3 BOX -->
                <div class="bg-cyan-50 p-5 rounded-2xl border border-cyan-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-cyan-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 3</span>
                            <span class="text-[10px] font-bold text-cyan-700 bg-cyan-100 px-2 py-0.5 rounded">발주 계획</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">발주 실행계획 수립</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>하도급 & 자재 수급 일정</li>
                            <li>소모품 & 무선국 허가 반영</li>
                            <li>사용전검사 일정 조율</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-cyan-200 text-center">
                        <span class="text-[10px] font-bold text-cyan-900">📅 공정 및 법정 인허가 일정</span>
                    </div>
                </div>

                <!-- STEP 4 BOX -->
                <div class="bg-emerald-50 p-5 rounded-2xl border border-emerald-200 flex flex-col justify-between shadow-sm space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="bg-emerald-600 text-white text-[11px] font-black px-2.5 py-1 rounded-full">STEP 4</span>
                            <span class="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">마감 승인</span>
                        </div>
                        <h4 class="font-black text-slate-900 text-sm">결과서 & 현장설명서 결재</h4>
                        <ul class="text-[11px] text-slate-700 mt-2 space-y-1 font-medium list-disc pl-3.5">
                            <li>현장소장 최종 서명 체결</li>
                            <li>KOM 검토결과서 작성</li>
                            <li>현장설명서 확정 등록</li>
                        </ul>
                    </div>
                    <div class="bg-white p-2 rounded-lg border border-emerald-200 text-center">
                        <span class="text-[10px] font-bold text-emerald-900">📄 최종 발주서류 무결성</span>
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
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 1. 설계도서 대조 및 적격 업체 Pool 분석 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">통신설계 도면 대조 & 유사 철도/트램 영업운행 적격 시공업체 Pool 선별</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        통신설계 도면과 현장여건을 대조하고, <span class="term-highlight" onclick="openGlossary('subcontractor_pool')">철도, 도시철도 및 노면트램 정보통신 구축/영업운행 실적이 검증된 적격 시공업체 Pool</span>을 분석하여 최적의 입찰 대상 군을 구성합니다.
                    </p>
                    
                    <!-- STEP 1 RICH 2D Visual Diagram -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-blue-200" onclick="openDiagramZoom('svgStep1_Card', '[사전 준비] 설계도서 대조 & 적격 시공업체 Pool 분석 도면')">
                        <svg id="svgStep1_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
                            
                            <!-- 도면 및 실적 대조 -->
                            <rect x="30" y="25" width="220" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                            <rect x="30" y="25" width="220" height="30" fill="#eff6ff" rx="8"/>
                            <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">📐 통신 도면 & 현장 여건</text>
                            <line x1="45" y1="65" x2="235" y2="65" stroke="#93c5fd" stroke-width="1.5"/>
                            <text x="50" y="85" font-size="11" font-weight="bold" fill="#334155">• 트램 본선 & 정거장 18개소 도면</text>
                            <text x="50" y="105" font-size="11" font-weight="bold" fill="#334155">• 관로/기계실 현장 접근성 검토</text>
                            <text x="50" y="125" font-size="11" font-weight="bold" fill="#334155">• 타 공종 간섭 여부 사전 분석</text>

                            <!-- 화살표 -->
                            <path d="M 260 85 L 290 85" stroke="#4338ca" stroke-width="3"/>
                            <polygon points="290,80 300,85 290,90" fill="#4338ca"/>

                            <!-- 업체 Pool 선별 -->
                            <rect x="305" y="25" width="215" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                            <rect x="305" y="25" width="215" height="30" fill="#ecfdf5" rx="8"/>
                            <text x="412" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">👥 적격 시공업체 Pool</text>
                            <line x1="320" y1="65" x2="505" y2="65" stroke="#6ee7b7" stroke-width="1.5"/>
                            <text x="325" y="85" font-size="11" font-weight="bold" fill="#334155">• 트램/철도 실적 보유 업체</text>
                            <text x="325" y="105" font-size="11" font-weight="bold" fill="#334155">• 통신 전문 유경험 기술자 투입</text>
                            <text x="325" y="125" font-size="11" font-weight="bold" fill="#334155">• 신용도 및 시공 능력 평가 합격</text>

                            <!-- 하단 캡션 -->
                            <rect x="30" y="155" width="490" height="30" fill="#1e293b" rx="6"/>
                            <text x="275" y="175" font-size="13" font-weight="black" fill="#38bdf8" text-anchor="middle">설계 도면 대조 & 적격 시공업체 Pool 분석 완료</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 2 CARD -->
                <div class="bg-white p-7 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-6 bg-indigo-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">2</div>
                    <span class="bg-indigo-100 text-indigo-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 2. 8대 현장조건 정밀 반영 & 예산 검증 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">자재 제작기간, 창고 임대, 전력/용수, 상주인력비 등 8대 현장조건 계상</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        <span class="term-highlight" onclick="openGlossary('eight_site_conditions')">8대 현장조건(자재 제작기간, 유경험자, 대관/소모품, 사용전검사 교육비, 내역 누락, 창고 임대비, 용수/전기, 상주 인력비)</span>을 내역서에 정밀 계상하여 발주 후 발생할 수 있는 추가 예산 분쟁을 차단합니다.
                    </p>

                    <!-- STEP 2 RICH 2D Visual Diagram -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgStep2_Card', '[본 검토] 8대 현장조건 & 내역 누락 재검증 도면')">
                        <svg id="svgStep2_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
                            
                            <!-- 8대 현장조건 대시보드 -->
                            <rect x="30" y="25" width="490" height="125" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="8"/>
                            <rect x="30" y="25" width="490" height="30" fill="#e0e7ff" rx="8"/>
                            <text x="275" y="45" font-size="13" font-weight="black" fill="#3730a3" text-anchor="middle">📋 8대 현장조건 필수 내역 계상 체크리스트</text>

                            <text x="45" y="75" font-size="11" font-weight="bold" fill="#334155">1. 자재 제작/수급 기간 반영</text>
                            <text x="45" y="95" font-size="11" font-weight="bold" fill="#334155">2. 철도 유경험 기술자 투입</text>
                            <text x="45" y="115" font-size="11" font-weight="bold" fill="#334155">3. 대관업무 & 소모품 지원</text>
                            <text x="45" y="135" font-size="11" font-weight="bold" fill="#334155">4. 사용전검사 교육비 포함</text>

                            <text x="280" y="75" font-size="11" font-weight="bold" fill="#334155">5. 예산내역서 누락 항목 검토</text>
                            <text x="280" y="95" font-size="11" font-weight="bold" fill="#334155">6. 현장 자재창고 임대비 포함</text>
                            <text x="280" y="115" font-size="11" font-weight="bold" fill="#334155">7. 공사용 전기/용수/오수 시설</text>
                            <text x="280" y="135" font-size="11" font-weight="bold" fill="#334155">8. 가동 후 상주 인력비 계상</text>

                            <!-- 하단 캡션 -->
                            <rect x="30" y="160" width="490" height="30" fill="#1e293b" rx="6"/>
                            <text x="275" y="180" font-size="13" font-weight="black" fill="#38bdf8" text-anchor="middle">8대 현장조건 계상으로 예산 내역서 무결성 확보</text>
                        </svg>
                    </div>
                </div>

                <!-- STEP 3 CARD -->
                <div class="bg-white p-7 rounded-2xl border border-slate-200 shadow-md relative space-y-4">
                    <div class="absolute -left-[37px] top-6 bg-emerald-600 text-white rounded-full w-9 h-9 flex items-center justify-center font-black text-base shadow-md">3</div>
                    <span class="bg-emerald-100 text-emerald-900 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">STEP 3. 서류 작성 및 현장소장 최종 결재 단계</span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">KOM 검토결과서 및 현장설명서 서명 체결 후 발주 확정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">
                        하도급 및 자재 수급 전략, 8대 현장조건이 완벽히 반영된 <span class="term-highlight" onclick="openGlossary('kom_meeting')">KOM 검토결과서 및 현장설명서</span>를 작성하여 현장소장의 최종 서명을 체결하고 발주 서류의 무결성을 확립합니다.
                    </p>

                    <!-- STEP 3 RICH 2D Visual Diagram -->
                    <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-emerald-200" onclick="openDiagramZoom('svgStep3_Card', '[마감 승인] KOM 검토결과서 & 현장설명서 최종 체결 도면')">
                        <svg id="svgStep3_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
                            
                            <!-- 결과서 & 설명서 체결 서식 -->
                            <rect x="110" y="20" width="330" height="135" fill="#ffffff" stroke="#059669" stroke-width="2.5" rx="8"/>
                            <rect x="110" y="20" width="330" height="30" fill="#ecfdf5" rx="8"/>
                            <text x="275" y="40" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">📄 통신공사 KOM 검토결과서 & 현장설명서</text>
                            <line x1="125" y1="58" x2="425" y2="58" stroke="#a7f3d0" stroke-width="1.5"/>
                            <text x="135" y="78" font-size="11" font-weight="bold" fill="#334155">✔ 적격 시공업체 Pool 입찰 지침 수립</text>
                            <text x="135" y="98" font-size="11" font-weight="bold" fill="#334155">✔ 8대 현장조건 비용 100% 반영 완료</text>

                            <!-- 현장소장 결재란 -->
                            <rect x="210" y="108" width="130" height="35" fill="#f8fafc" stroke="#cbd5e1" rx="4"/>
                            <text x="275" y="123" font-size="11" font-weight="bold" fill="#64748b" text-anchor="middle">현장소장 (인)</text>
                            <text x="275" y="137" font-size="11" font-weight="black" fill="#059669" text-anchor="middle">Sign [최종 확정]</text>

                            <!-- 하단 캡션 -->
                            <rect x="30" y="165" width="490" height="28" fill="#1e293b" rx="6"/>
                            <text x="275" y="184" font-size="13" font-weight="black" fill="#38bdf8" text-anchor="middle">현장소장 서명 체결 및 발주 서류 무결성 확립 완료</text>
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
    <title>통신분야 - 발주전략 KOM 마스터 체크리스트</title>
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
        <h1 class="title">발주전략 KOM 마스터 체크리스트</h1>
        <span class="meta">WBS Code 9000-2-2 | 통신 발주검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 1.05rem; font-weight: 800;">📋 발주전략 KOM 12대 정밀 검측대장</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 엑셀 시방의 8대 현장조건 및 발주 검토 수칙을 12개 정밀 점검 항목으로 확장 구성하였으며, 모든 항목의 문장 끝은 예외 없이 질문형 어미(~하였는가?)로 100% 정형화되었습니다.
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
                <td class="category" style="color:#1e40af;">⚠️ 사전 준비<br>(Step 1 도면&Pool)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">1. 도면 대조</span>
                        <strong>[도면 및 여건]</strong> 통신설계 도면과 현장 설치 여건을 사전 대조 확인**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">2. 업체 Pool</span>
                        <strong>[적격 업체]</strong> <span class="term-highlight" onclick="openGlossary('subcontractor_pool')">철도/트램 시공 및 영업운행 실적이 입증된 적격 업체 Pool</span>을 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">3. 제작 기간</span>
                        <strong>[자재 수급]</strong> 통신 주요 자재(광케이블, 기지국)의 제작 및 현장 수급 기간을 계상**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">4. 유경험 인력</span>
                        <strong>[기술 인력]</strong> 철도/트램 유경험 전문 기술자 투입 계획을 확인**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#4338ca;">📋 8대 조건<br>(Step 2 예산검증)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">5. 대관 업무</span>
                        <strong>[대관 및 소모품]</strong> 관할 지자체 대관업무 및 현장 소모품 지원 계획을 검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">6. 사용전검사</span>
                        <strong>[교육 지원비]</strong> 사용전검사 통신설비 운용 및 교육 지원 비용이 예산에 반영되었는지 확인**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">7. 내역 누락</span>
                        <strong>[내역서 재검토]</strong> 공사 예산내역서 상 누락 항목이 없는지 정밀 재검토**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0e7ff; color:#3730a3;">8. 창고 임대</span>
                        <strong>[창고 비용]</strong> <span class="term-highlight" onclick="openGlossary('eight_site_conditions')">현장 자재 보관 창고 임대 비용</span>을 내역서에 포함**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:#15803d;">🤝 마감 승인<br>(Step 3 결과체결)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">9. 유틸리티</span>
                        <strong>[공사용 시설]</strong> 공사용 전기, 용수, 오수 처리 시설 확보 계획을 수립**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">10. 상주 인력</span>
                        <strong>[기술 지원비]</strong> 가동 후 현장 상주 기술지원 인력 기간 및 비용을 계상**하였는가?**
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">11. 법정 일정</span>
                        <strong>[인허가 일정]</strong> 무선국 허가 및 사용전검사 준공 일정을 종합 반영**하였는가?**
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">12. 결과서 체결</span>
                        <strong>[소장 서명]</strong> <span class="term-highlight" onclick="openGlossary('kom_meeting')">현장소장 결재가 포함된 KOM 검토결과서 및 현장설명서</span>를 확정**하였는가?**
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-2-2 발주전략 KOM 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Write all HTML files with both original and prefixed names
for fname in ["발주전략 KOM_표준서.html", "2_발주전략 KOM_표준서.html", "9000-2-2_발주전략 KOM_표준서.html"]:
    with open(os.path.join(std_dir, fname), 'w', encoding='utf-8') as f:
        f.write(std_html)

for fname in ["발주전략 KOM_수행지침.html", "2_발주전략 KOM_수행지침.html", "9000-2-2_발주전략 KOM_수행지침.html"]:
    with open(os.path.join(gui_dir, fname), 'w', encoding='utf-8') as f:
        f.write(gui_html)

for fname in ["발주전략 KOM_체크리스트.html", "2_발주전략 KOM_체크리스트.html", "9000-2-2_발주전략 KOM_체크리스트.html"]:
    with open(os.path.join(chk_dir, fname), 'w', encoding='utf-8') as f:
        f.write(chk_html)

print("\n🎉 SUCCESSFULLY ENRICHED ALL 3 MASTER HTML FILES FOR WBS 9000-2-2 발주전략 KOM!")
