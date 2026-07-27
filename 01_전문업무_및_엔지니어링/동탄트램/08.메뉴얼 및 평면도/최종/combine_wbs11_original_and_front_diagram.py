import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 11 Path
wbs11_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\11_시공계획 수립"
path_guideline = os.path.join(wbs11_base, "수행지침", "시공계획 수립_수행지침.html")
path_guideline_alt = os.path.join(wbs11_base, "수행지침", "11_시공계획 수립_수행지침.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully updated WBS 11 Guideline: {path}")

# Zoom Modal & Glossary Styles
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
            <img id="modalImage" src="" style="width:100%; border-radius:10px; display:none; margin-bottom:15px; border: 1px solid #cbd5e1;" />
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
    'hbs_layer': {
        title: '🧱 HBS 강화노반 지반층 (Hydraulically Bound Base Support)',
        desc: '흙과 자갈에 시멘트를 섞어 롤러로 꽝꽝 다진 고지지력 노반 기초 지층입니다. 지지력 지수 K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa을 확보하여 부등침하를 방지합니다.'
    },
    'hbr_layer': {
        title: '🏗️ HBR 기초콘크리트 층 (Hydraulic Base Concrete)',
        desc: '강화노반(HBS) 상부에 매끄럽게 타설하여 궤도 콘크리트 슬래브가 올라설 평평한 수평 바닥을 만드는 기초 버림 콘크리트 레이어입니다.'
    },
    'tcl_pst_layer': {
        title: '🚆 TCL 궤도콘크리트 & PST 슬래브 패널 층',
        desc: '트램 레일을 직접 고정 지지하는 최종 본선 궤도 콘크리트 슬래브 구조체층입니다.'
    },
    'shear_anchor': {
        title: '⚓ 전단앵커 (Shear Key Anchor)',
        desc: 'HBS 강화노반 및 TCL 기초 콘크리트 층과 상부 프리캐스트 패널(PST) 간의 층간 전단 미끄러짐을 완벽히 차단하여 일체화 구조를 형성하는 전단키 연결 장치입니다.'
    },
    'hbs_test': {
        title: '🧱 HBS 지지력 검증 (Hydraulic Base Support Test)',
        desc: '콘크리트 도상(TCL) 하부에 위치한 상부 강화 노반의 하중 지지력을 현장에서 시험하는 단계입니다. 평판재하시험(PBT)을 실시하여 노반 반력계수 K30 >= 110 MN/m3 이상을 달성했는지 시공 전 필수 검증해야 합니다.'
    },
    'thermit_weld': {
        title: '🔥 테르밋 용접 (Thermit Welding, EN 14730)',
        desc: '용접기나 전기 없이, 철가루와 알루미늄 가루를 혼합하여 화학반응 열(2,500도 이상)을 내서 벌건 쇳물을 만든 뒤, 이를 레일과 레일 사이의 틈새에 부어 굳혀서 붙이는 전통적이고 가장 강력한 철도 연결 공법입니다.',
        img: 'thermit_field.png'
    },
    'tcl_concrete': {
        title: '🛤️ TCL 도상 콘크리트 (Track Concrete Layer)',
        desc: '트램 레일 및 침목 궤도를 하부에서 고정해주는 핵심 무근/철근 콘크리트 슬래브 구조체입니다. 28일 기준 설계기준 압축강도가 최소 30 MPa 이상을 확보하고 연속 타설을 통해 콜드조인트를 예방해야 합니다.'
    }
};

function openGlossary(termKey) {
    const data = glossaryData[termKey];
    if (!data) return;
    document.getElementById('modalTitle').innerText = data.title;
    document.getElementById('modalDescription').innerText = data.desc;
    
    const imgEl = document.getElementById('modalImage');
    if (data.img) {
        imgEl.src = data.img;
        imgEl.style.display = 'block';
    } else {
        imgEl.src = '';
        imgEl.style.display = 'none';
    }
    
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

# Full Combined WBS 11 Guideline HTML (Original Content Preserved + Master Simulation Diagram Front)
full_wbs11_guideline_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 시공계획 수립 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        """ + zoom_modal_style + """
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 to-slate-900 opacity-70"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-11 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">동탄트램 콘크리트도상 시공계획 마스터 가이드</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">시공계획 수립 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"동탄트램 궤도 4단계 수직 지층 구조 메커니즘 & 콘크리트도상 마스터 실무 시퀀스 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> 동탄트램 콘크리트도상 시공계획 수립 실무 핵심
            </h4>
            <p class="leading-relaxed">
                본 수행지침서는 동탄트램 본선 콘크리트도상 전체 공정의 첫 번째 시작 단계로서, <strong><span class="term-highlight" onclick="openGlossary('hbs_layer')">1단계 강화노반(HBS)</span></strong> ➔ <strong><span class="term-highlight" onclick="openGlossary('hbr_layer')">2단계 기초콘크리트(HBR)</span></strong> ➔ <strong><span class="term-highlight" onclick="openGlossary('tcl_pst_layer')">3단계 궤도콘크리트/PST 패널</span></strong> ➔ <strong><span class="term-highlight" onclick="openGlossary('shear_anchor')">수직 전단앵커 일체화</span></strong>로 이어지는 4단계 수직 지층 샌드위치 구조 메커니즘을 선제 이해하고, 설계 도서 검토, 5대 시공 시퀀스 및 정밀 3D 얼라인먼트 시공계획서를 작성하는 마스터 통합 매뉴얼입니다.
            </p>
        </div>

        <!-- ★ [전격 삽입] 1. 동탄트램 궤도 수직 지층 샌드위치 구조 & 전단앵커 결합 시뮬레이션 2D 기술 도식 (맨 앞단 마스터 가이드) -->
        <div class="border-b-2 border-slate-200 pb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">1.</span> [마스터 개념] 동탄트램 궤도 4단계 수직 지층 샌드위치 구조도 & 전단앵커 결합 단면 시뮬레이션
            </h2>

            <div class="bg-white p-6 rounded-2xl border border-indigo-100 shadow-lg space-y-6">
                <!-- SVG Simulation Diagram (Clickable Lightbox Zoom Modal) -->
                <div class="clickable-diagram bg-slate-50 p-6 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgDiagramRef_Layers_WBS11_Combined', '[마스터 개념] 동탄트램 궤도 4단계 수직 지층 샌드위치 구조도')">
                    <svg id="svgDiagramRef_Layers_WBS11_Combined" viewBox="0 0 500 320" width="100%" height="320" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="500" height="320" fill="#f8fafc"/>

                        <!-- [0단계] 원지반 / 다져진 토공 노반 -->
                        <rect x="30" y="255" width="440" height="50" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
                        <text x="250" y="285" font-size="12" font-weight="bold" fill="#334155" text-anchor="middle">0단계: 원지반 및 토공 노반 (Subgrade Ground)</text>

                        <!-- [1단계] HBS 강화노반 지반층 (K30 >= 110 MN/m3) -->
                        <rect x="30" y="195" width="440" height="60" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                        <text x="250" y="230" font-size="13" font-weight="black" fill="#78350f" text-anchor="middle">1단계: HBS 강화노반 지반층 (K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa)</text>

                        <!-- [2단계] HBR 기초 콘크리트 층 -->
                        <rect x="30" y="145" width="440" height="50" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                        <text x="250" y="175" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">2단계: HBR 기초 콘크리트 층 (수평 평탄 버림 바닥)</text>

                        <!-- [3단계] TCL 궤도콘크리트 & PST 슬래브 패널 -->
                        <rect x="30" y="85" width="440" height="60" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>
                        <text x="250" y="120" font-size="13" font-weight="black" fill="#1e3a8a" text-anchor="middle">3단계: TCL 궤도콘크리트 / PST 프리캐스트 슬래브 패널 (≥ 45 MPa)</text>

                        <!-- [4단계] 최상부 레일 (Rail 60kg / 51R1) -->
                        <rect x="100" y="55" width="40" height="30" fill="#334155" rx="3"/>
                        <rect x="360" y="55" width="40" height="30" fill="#334155" rx="3"/>
                        <text x="120" y="45" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">좌측 레일</text>
                        <text x="380" y="45" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">우측 레일</text>

                        <!-- [핵심 결합] 수직 전단앵커 (Shear Key Anchor) - 관통 결합 -->
                        <rect x="235" y="70" width="30" height="150" fill="#dc2626" rx="3" opacity="0.9"/>
                        <text x="250" y="150" font-size="12" font-weight="black" fill="#ffffff" text-anchor="middle" transform="rotate(-90 250 150)">수직 전단앵커 층간 결합 (Monolithic Bonding)</text>
                        
                        <!-- 화살표 콜아웃 -->
                        <line x1="280" y1="105" x2="330" y2="105" stroke="#dc2626" stroke-width="2" stroke-dasharray="3,2"/>
                        <text x="335" y="109" font-size="11" font-weight="black" fill="#dc2626" text-anchor="start">무수축그라우트 밀실 충전</text>
                    </svg>
                </div>

                <!-- 상세 아파트 비유 해설 가이드 -->
                <div class="bg-indigo-50 p-5 rounded-xl border border-indigo-100 text-xs sm:text-sm text-indigo-950 space-y-3">
                    <h4 class="font-bold text-indigo-900 text-base flex items-center gap-2">
                        <span>🏗️</span> 시공계획 수립을 위한 수직 지층 샌드위치 구조 & 전단앵커 역할 가이드
                    </h4>
                    <p class="leading-relaxed">
                        아파트 건물 공사에 비유하면 동탄트램 궤도의 수직 지층 구조를 한눈에 쉽게 파악할 수 있습니다:
                    </p>
                    <ul class="list-disc pl-5 space-y-1.5 text-indigo-900">
                        <li><strong>1단계 강화노반 (HBS) = 단단하게 다진 땅 지반:</strong> 흙과 자갈에 시멘트를 섞어 롤러로 꽝꽝 다진 고지지력 노반 기초층 (K30 &ge; 110 MN/m&sup3;)</li>
                        <li><strong>2단계 기초콘크리트 층 (HBR) = 평평한 버림 콘크리트 바닥:</strong> 다진 땅(HBS) 위에 수평을 매끄럽게 맞추기 위해 타설하는 수평 받침용 콘크리트</li>
                        <li><strong>3단계 궤도콘크리트/패널 (TCL / PST) = 본체 레일 슬래브 구조물:</strong> 트램 레일을 직접 고정 지지하는 최종 본선 궤도 콘크리트 슬래브 (&ge; 45 MPa)</li>
                        <li><strong>⚓ 수직 전단앵커 결합 = 층간 미끄러짐 방지 핀:</strong> HBS/HBR 기초층부터 상부 PST 패널까지 수직 전단앵커를 관통시키고 무수축 그라우트를 충전하여 열차 주행 시 층간 단층 미끄러짐 없이 **하나의 통 덩어리로 일체화(Monolithic Bonding)**시키는 핵심 장치입니다.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. [보존된 이전 원본 콘텐츠] 5대 시공 마스터 시퀀스 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 콘크리트도상 시공계획 5대 시공 마스터 시퀀스 (Master Sequence)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                <div class="flow-card bg-amber-50 p-3.5 rounded-xl border border-amber-200 flex flex-col justify-between space-y-2">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">노반 지지력 검증</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <span class="term-highlight" onclick="openGlossary('hbs_test')">K30 &ge; 110 MN/m³</span> 노반 평판재하시험 & 3D 측량 정합
                        </p>
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-3.5 rounded-xl border border-sky-200 flex flex-col justify-between space-y-2">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">궤광 가조립 안착</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            25m 궤광 템플릿 크레인 인양 및 지지대 정위치 안착
                        </p>
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-3.5 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-2">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">스핀들 오차 조율</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            궤간(<b>+3, -1mm</b>) & 캔트(<b>&plusmn;2.0mm</b>) 정밀 게이지 고정
                        </p>
                    </div>
                </div>

                <div class="flow-card bg-orange-50 p-3.5 rounded-xl border border-orange-200 flex flex-col justify-between space-y-2">
                    <div>
                        <span class="bg-orange-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">테르밋 레일 용접</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <span class="term-highlight" onclick="openGlossary('thermit_weld')">2,500℃ 화학 쇳물</span> 용접 & 비파괴 UT 굴곡 검측
                        </p>
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-3.5 rounded-xl border border-blue-200 flex flex-col justify-between space-y-2">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 5</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">TCL 도상 타설</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <span class="term-highlight" onclick="openGlossary('tcl_concrete')">강도 &ge; 30 MPa</span> 연속 타설 및 감리 최종 승인
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. [보존된 이전 원본 콘텐츠] 테르밋 용접 & 실무 현장 멀티-미디어 시공 장비 갤러리 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 현장 핵심 시공 장비 & 테르밋 용접 실무 갤러리 (현장 수칙)
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 테르밋 용접 도식 및 몰드 설치 -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
                    <div>
                        <h3 class="font-bold text-base text-slate-900 mb-2 border-b border-slate-100 pb-2">
                            🔥 테르밋(Thermit) 반응 메커니즘 & 도가니 반응
                        </h3>
                        <div class="clickable-diagram bg-slate-50 p-3 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('imgThermitDiagram', '테르밋 반응 메커니즘 도식')">
                            <img id="imgThermitDiagram" src="thermit_diagram.png" alt="테르밋 반응 도식" class="max-h-52 w-auto object-contain rounded-lg" />
                        </div>
                    </div>
                    <p class="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                        알루미늄 분말과 산화철의 발열 화학반응(2,500℃)으로 고온 슬래그와 쇳물을 분리시켜 레일 틈새를 완전 일체형으로 접합하는 표준 프로세스입니다.
                    </p>
                </div>

                <!-- 현장 쇳물 주입 및 비파괴 수칙 -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
                    <div>
                        <h3 class="font-bold text-base text-slate-900 mb-2 border-b border-slate-100 pb-2">
                            ⚡ 현장 테르밋 쇳물 주입 & 궤광 정밀 조율 지지대
                        </h3>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="clickable-diagram bg-slate-50 p-2 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('imgThermitField', '현장 쇳물 주입 시공 장면')">
                                <img id="imgThermitField" src="thermit_field.png" alt="현장 쇳물 주입" class="max-h-40 w-auto object-contain rounded-lg" />
                            </div>
                            <div class="clickable-diagram bg-slate-50 p-2 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('imgJigSupport', '궤광 조율 지지대 장비')">
                                <img id="imgJigSupport" src="track_jig_support.png" alt="궤광 조율 지지대" class="max-h-40 w-auto object-contain rounded-lg" />
                            </div>
                        </div>
                    </div>
                    <p class="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                        현장 쇳물 주입 후 굴곡 수평 오차(&plusmn;0.2mm/m) 검측 및 궤도 템플릿 스핀들 락너트 고정 수칙을 철저히 이행합니다.
                    </p>
                </div>
            </div>
        </div>

        <!-- 4. [보존된 이전 원본 콘텐츠] 3단계 실무 엔지니어링 수행 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">4.</span> 3단계 실무 엔지니어링 수행 수칙 (사전준비 ➔ 본시공 ➔ 검사마감)
            </h2>
            
            <div class="space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">① 사전 준비</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">노반 지지력 K30 검수 & 광파 3D 측량 셋팅</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            토공 및 노반 공종 인도 레벨을 확인하고, <span class="term-highlight" onclick="openGlossary('hbs_test')">노반 지지력 K30 ≥ 110 MN/m³</span> 시험 성적서 확보 후 광파 토탈스테이션으로 CP점 오차를 정밀 셋팅합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">② 본 시공</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">궤광 조율, 테르밋 용접 & TCL 도상 타설</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            궤광 템플릿을 배치하고 궤간(+3,-1mm) 및 캔트(±2.0mm)를 조율한 뒤, <span class="term-highlight" onclick="openGlossary('thermit_weld')">테르밋 쇳물 주입(EN 14730)</span>과 <span class="term-highlight" onclick="openGlossary('tcl_concrete')">TCL 콘크리트(강도 ≥ 30 MPa)</span> 연속 타설을 시행합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">③ 검사 마감</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">비파괴 UT 검측 & 감리단 최종 착공 승인</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            테르밋 용접부 UT 초음파 비파괴 검사 성적서와 도상 경화 공시체 강도를 확인하고, 감리단 서명을 받아 최종 착공 시공계획 보고서를 대장 마감합니다.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""" + common_modal_html + """
</body>
</html>
"""

force_write(path_guideline, full_wbs11_guideline_html)
force_write(path_guideline_alt, full_wbs11_guideline_html)

print("\n🎉 SUCCESSFULLY COMBINED ORIGINAL WBS 11 CONTENT WITH FRONT MASTER SIMULATION DIAGRAM!")
