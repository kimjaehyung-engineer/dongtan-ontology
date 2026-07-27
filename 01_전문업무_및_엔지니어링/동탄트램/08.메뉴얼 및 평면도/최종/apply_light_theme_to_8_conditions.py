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

common_modal_html_kom = """
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

# LIGHT THEME 8 SITE CONDITIONS GUIDELINE HTML
light_theme_kom_gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>통신분야 - 발주전략 KOM 6단계 마스터 수행지침서</title>
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
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 마스터 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"발주조건, 적격 업체 Pool & 8대 현장조건 정밀 반영 6단계 visual 실무 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 (개념 해설) -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-xs sm:text-sm text-blue-950 shadow-sm space-y-4">
            <h4 class="font-bold text-blue-950 text-base flex items-center gap-2">
                <span>💡</span> 발주전략 Kick-off Meeting(KOM) 핵심 개념 및 기술 지침
            </h4>
            <div class="bg-white p-5 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed space-y-2">
                <p>🤝 <strong>'발주전략 KOM'이란 무엇인가?</strong><br>
                통신공사 발주 착수 전 현장소장 주관으로 발주조건, <strong><span class="term-highlight" onclick="openGlossary('subcontractor_pool')">유공 적격 시공업체 Pool 분석</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('eight_site_conditions')">8대 현장조건(창고 임대, 용수/전력, 상주 인력비, 사용전검사 교육비 등)</span></strong>을 종합 대조하여 예산 누락을 방지하고 <strong><span class="term-highlight" onclick="openGlossary('kom_meeting')">KOM 검토결과서 및 현장설명서</span></strong>의 무결성을 확립하는 6단계 실무 프로세스입니다.</p>
            </div>
        </div>

        <!-- ☀️ 8대 현장조건 상세 친절 해설 특화 섹션 (라이트 테마 / 밝은 계열 전면 개편) -->
        <div class="bg-blue-50/70 border border-blue-200 p-7 rounded-2xl shadow-md space-y-6">
            <div class="border-b border-blue-200 pb-4">
                <span class="bg-blue-600 text-white text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">SPECIAL FOCUS</span>
                <h3 class="text-xl font-black text-blue-950 mt-2 flex items-center gap-2">
                    <span>📋</span> 동탄트램 통신공사 필수 반영 『8대 현장조건』 정밀 해설
                </h3>
                <p class="text-slate-600 text-xs sm:text-sm mt-1">발주 착수 전 예산 누락 및 분쟁을 사전에 100% 방지하기 위해 정밀 계상해야 하는 8가지 실무 수칙</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
                <!-- 1. 자재 제작/수급 기간 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>📦</span> 1. 자재 제작 및 수급 기간 (Lead-Time)
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        주요 장비(LTE-R 기지국, 72-Core 광 전송장치, 4K IP CCTV, PIS/PA 방송 랙)의 공장 제작 및 해외/국내 조달 리드타임(최소 2~4개월)을 사전 반영하여 궤도/건축 공정 지연을 방지함.
                    </p>
                </div>

                <!-- 2. 유경험자 구축 실적 보유 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>👷</span> 2. 유경험자 구축 실적 보유 (철도/트램)
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        일반 건축 통신이 아닌 특수 철도/노면트램 환경(차상-지상 무선, SIL 4 안전망, 궤도 이중화 광망) 구축 및 영업운행 시공 실적이 검증된 숙련 기술자 및 적격 업체를 선별 투입함.
                    </p>
                </div>

                <!-- 3. 대관업무 및 소모품 지원 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>📜</span> 3. 대관업무 및 소모품 지원
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        관할 지자체(화성시/수원시), 경찰서(교통통제), 전파관리소 도로점용 굴착 허가 행정 비용 및 광 융착 접속 슬리브, 케이블 마킹 타이드 등 사소하지만 누락되기 쉬운 소모품 예산 포함.
                    </p>
                </div>

                <!-- 4. 사용전검사 교육 지원비 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>🎓</span> 4. 사용전검사 설비 운용 및 교육 지원비
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        정보통신공사업법 제36조 사용전검사 시험 측정(OTDR, 전파 분석기) 장비/엔지니어 운용비 및 완공 후 동탄트램 운영자 대상 시스템 조작/유지보수 실습 교육 비용 계상.
                    </p>
                </div>

                <!-- 5. 예산내역서 누락 사전 검토 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>🔍</span> 5. 예산내역서 누락 항목 사전 검토
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        설계도서 vs 물량내역서 1:1 대조를 통해 케이블 트레이 고정 금구, 방화 씰링(Fire-Stop), 랙 간 링커블 광점퍼코드 등 누락 내역을 발주 전 선제 발굴하여 계약 금액 반영.
                    </p>
                </div>

                <!-- 6. 현장 자재창고 임대비 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>🏠</span> 6. 현장 자재보관 창고 임대 비용
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        고가의 광케이블, LTE-R 안테나, 4K CCTV 및 관제 서버의 도난, 습기 파손 및 훼손을 방지하기 위한 온/습도 제어 및 보안 시설을 갖춘 전용 자재창고 임대 비용 계상.
                    </p>
                </div>

                <!-- 7. 공사용 유틸리티 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>⚡</span> 7. 공사용 전기, 용수, 오수 처리 시설
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        통신기계실 장비 설치 및 광융착 접속, 시험용 임시 가설 전력(220V/380V), 작업용 용수 공급 및 임시 오수/폐수 처리 가설 시설을 사전 확보하여 시공 환경 조성.
                    </p>
                </div>

                <!-- 8. 상주인력 기술지원비 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2 hover:border-blue-300 transition-all">
                    <span class="font-bold text-blue-700 text-sm flex items-center gap-2">
                        <span>👨‍💻</span> 8. 가동 후 현장 상주인력 기술지원비
                    </span>
                    <p class="text-slate-700 leading-relaxed text-xs sm:text-sm">
                        동탄트램 준공 및 영업시운전/초기 개통 후 시스템 안정을 위해 제작사 및 전문 기술자의 일정 기간(3~6개월) 현장 상주 비상 대응 인건비를 발주 내역에 정식 포함.
                    </p>
                </div>
            </div>
        </div>

        <!-- 1. 6단계 시공 마스터 흐름 요약 (Expanded Flow Architecture) -->
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
                    <svg id="svgStep2_Card" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="550" height="200" fill="#f8fafc"/>
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
{common_modal_html_kom}
</body>
</html>
"""

# Overwrite for WBS 9000-2-2 (발주전략 KOM / 착수전략 KOM)
for f_name in os.listdir(base_dir):
    full_f = os.path.join(base_dir, f_name)
    if os.path.isdir(full_f) and ('KOM' in f_name or '2_' in f_name or '9000-2-2' in f_name):
        gui_p = os.path.join(full_f, "수행지침")
        if os.path.exists(gui_p):
            for f in os.listdir(gui_p):
                if f.endswith('.html'):
                    with open(os.path.join(gui_p, f), 'w', encoding='utf-8') as out:
                        out.write(light_theme_kom_gui_html)
                    print("OVERWROTE LIGHT-THEME 8-CONDITIONS HTML FOR:", f)

print("\n🎉 SUCCESSFULLY CONVERTED ALL 8 SITE CONDITIONS CARDS TO LIGHT THEME (#f8fafc / #ffffff) FOR ALL TARGET GUIDELINE HTML FILES!")
