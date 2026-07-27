import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Target absolute paths
target_base = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\11_시공계획 수립"

path_guideline = os.path.join(target_base, "수행지침", "시공계획 수립_수행지침.html")
path_guideline_alt = os.path.join(target_base, "수행지침", "11_시공계획 수립_수행지침.html")

os.makedirs(os.path.dirname(path_guideline), exist_ok=True)

# Copy source images into guideline folder
user_uploaded_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.user_uploaded"
brain_root = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298"
wbs11_guideline_dir = os.path.dirname(path_guideline)

copy_mappings = {
    os.path.join(user_uploaded_dir, "media__1784946725204.png"): os.path.join(wbs11_guideline_dir, "thermit_field.png"),
    os.path.join(user_uploaded_dir, "media__1784946734213.png"): os.path.join(wbs11_guideline_dir, "thermit_crucible.png"),
    os.path.join(user_uploaded_dir, "media__1784946747955.png"): os.path.join(wbs11_guideline_dir, "thermit_diagram.png"),
    os.path.join(brain_root, "rail_welding_yard_view_real_1784940360828.jpg"): os.path.join(wbs11_guideline_dir, "rail_yard.jpg")
}

for src, dst in copy_mappings.items():
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"📦 Successfully Copied image: {os.path.basename(src)} ➔ {os.path.basename(dst)}")

def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Written Complete Master WBS 11 Guideline: {path}")

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
    .sim-step-btn {
        transition: all 0.25s ease;
    }
    .sim-step-btn.active {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.12);
    }
    .sim-btn {
        transition: all 0.2s ease;
    }
    .sim-btn:hover {
        transform: translateY(-1px);
    }
    .img-card {
        transition: all 0.3s ease;
    }
    .img-card:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.15);
    }
"""

common_modal_html = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 시공장면 해설</h3>
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

# Ultimate Master WBS 11 Guideline HTML (Layer Simulation Front + 5-Step Interactive Simulator + Manual Spindle Up/Down Control + Thermit Photo Gallery)
complete_wbs11_guideline_html = """<!DOCTYPE html>
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
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-11 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">인터랙티브 시뮬레이터 & 시각 실사 통합 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">시공계획 수립 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"4단계 수직 지층 시뮬레이션 + 5대 시공 마스터 플로우 & 스핀들 상승·하강 미세조정 조율 가이드"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> 동탄트램 콘크리트도상 시공계획 수립 실무 핵심
            </h4>
            <p class="leading-relaxed">
                본 수행지침서는 동탄트램 본선 콘크리트도상 전체 공정의 시작 단계로서, <strong><span class="term-highlight" onclick="openGlossary('hbs_layer')">1단계 강화노반(HBS)</span></strong> ➔ <strong><span class="term-highlight" onclick="openGlossary('hbr_layer')">2단계 기초콘크리트(HBR)</span></strong> ➔ <strong><span class="term-highlight" onclick="openGlossary('tcl_pst_layer')">3단계 궤도콘크리트/PST 패널</span></strong> ➔ <strong><span class="term-highlight" onclick="openGlossary('shear_anchor')">수직 전단앵커 일체화</span></strong>의 수직 지층 샌드위치 구조를 선제 파악하고, 5대 시공 마스터 플로우와 <strong>스핀들 수동 상승(▲)/하강(▼) 미세조정 인터랙티브 시뮬레이터</strong> 및 <strong>테르밋 용접 현장 실사 갤러리</strong>를 제공합니다.
            </p>
        </div>

        <!-- ★ 1. 동탄트램 궤도 4단계 수직 지층 샌드위치 구조도 & 전단앵커 결합 단면 시뮬레이션 (맨 앞단 마스터 가이드) -->
        <div class="border-b-2 border-slate-200 pb-8">
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">1.</span> [마스터 개념] 동탄트램 궤도 4단계 수직 지층 샌드위치 구조도 & 전단앵커 결합 단면 시뮬레이션
            </h2>

            <div class="bg-white p-6 rounded-2xl border border-indigo-100 shadow-lg space-y-6">
                <!-- SVG Simulation Diagram (Clickable Lightbox Zoom Modal) -->
                <div class="clickable-diagram bg-slate-50 p-6 rounded-xl flex justify-center items-center shadow-inner border border-indigo-200" onclick="openDiagramZoom('svgDiagramRef_Layers_WBS11_Complete', '[마스터 개념] 동탄트램 궤도 4단계 수직 지층 샌드위치 구조도')">
                    <svg id="svgDiagramRef_Layers_WBS11_Complete" viewBox="0 0 500 320" width="100%" height="320" xmlns="http://www.w3.org/2000/svg">
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

        <!-- ★ 2. [마스터 인터랙티브 시뮬레이터] 5대 시공 마스터 시퀀스 단계별 자동 시뮬레이터 -->
        <div class="bg-white text-slate-900 p-6 sm:p-8 rounded-2xl shadow-xl border border-slate-200">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-bold text-emerald-700 uppercase tracking-widest">Interactive Construction Master Flow</span>
                    <h2 class="text-2xl font-black tracking-tight text-slate-900 mt-0.5">★ 콘크리트도상 궤도공사 5대 시공 인터랙티브 시뮬레이터</h2>
                </div>
                <!-- 자동 재생 버튼 -->
                <button id="autoPlayBtn" onclick="toggleAutoPlay()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl flex items-center gap-2 border border-emerald-600 transition-all shadow-sm">
                    <span id="playIcon">▶</span> <span id="playText">자동 시뮬레이션 재생</span>
                </button>
            </div>

            <!-- 5단계 선택 탭 버튼 -->
            <div class="grid grid-cols-5 gap-2 mb-6">
                <button id="stepBtn1" onclick="setStep(1)" class="sim-step-btn active bg-amber-500 text-white p-3 rounded-xl border border-amber-600 text-left transition-all">
                    <div class="text-[10px] opacity-90 font-bold">1단계</div>
                    <div class="text-xs font-black truncate">지반 다짐·측량</div>
                </button>
                <button id="stepBtn2" onclick="setStep(2)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">2단계</div>
                    <div class="text-xs font-black truncate">궤광 가조립</div>
                </button>
                <button id="stepBtn3" onclick="setStep(3)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">3단계</div>
                    <div class="text-xs font-black truncate">스핀들 높이조정</div>
                </button>
                <button id="stepBtn4" onclick="setStep(4)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">4단계</div>
                    <div class="text-xs font-black truncate">테르밋 쇳물용접</div>
                </button>
                <button id="stepBtn5" onclick="setStep(5)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">5단계</div>
                    <div class="text-xs font-black truncate">도상 콘크리트</div>
                </button>
            </div>

            <!-- 시뮬레이션 캔버스 (밝은 라이트 배경: #f8fafc) -->
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-300 relative overflow-hidden shadow-inner">
                <div style="height: 280px;" class="w-full relative">
                    <svg id="masterSeqSvg" viewBox="0 0 700 280" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="700" height="280" fill="#f8fafc"/>
                        <rect id="subgradeBg" x="0" y="210" width="700" height="70" fill="#854d0e" stroke="#78350f" stroke-width="2"/>
                        <text x="20" y="245" font-size="11" font-weight="black" fill="#ffffff" opacity="0.95">강화 노반 (상부 지반 - K30 ≥ 110 MN/m³)</text>
                        
                        <!-- Step 1 -->
                        <g id="seqGroupStep1" opacity="1" class="transition-all duration-500">
                            <path d="M 80 210 L 65 140 M 80 210 L 95 140 M 80 140 L 80 210" stroke="#d97706" stroke-width="2"/>
                            <rect x="65" y="130" width="30" height="15" rx="3" fill="#d97706"/>
                            <line x1="95" y1="137" x2="650" y2="137" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
                            <circle cx="95" cy="137" r="4" fill="#dc2626"/>
                            <text x="110" y="128" font-size="10" font-weight="bold" fill="#dc2626">3D CP 정밀 선형 측량 레이저 빔</text>
                            
                            <circle cx="450" cy="180" r="30" fill="#64748b" stroke="#334155" stroke-width="3"/>
                            <rect x="420" y="140" width="100" height="40" fill="#ca8a04" rx="5"/>
                            <text x="470" y="165" text-anchor="middle" font-size="10" font-weight="black" fill="#ffffff">노반 다짐 롤러</text>
                        </g>

                        <!-- Step 2 -->
                        <g id="seqGroupStep2" opacity="0" class="transition-all duration-500" transform="translate(0, -30)">
                            <line x1="222" y1="0" x2="222" y2="140" stroke="#b45309" stroke-width="2" stroke-dasharray="4,2"/>
                            <line x1="482" y1="0" x2="482" y2="140" stroke="#b45309" stroke-width="2" stroke-dasharray="4,2"/>
                            <path d="M 222 140 L 250 160 M 482 140 L 450 160" stroke="#b45309" stroke-width="2"/>
                            <text x="350" y="80" text-anchor="middle" font-size="11" font-weight="black" fill="#b45309">크레인 인양 궤광 가조립 안착 중...</text>
                        </g>

                        <!-- Track Body (Step 2~5 공유) -->
                        <g id="seqGroupTrack" opacity="0" class="transition-all duration-500" transform="translate(0, 0)">
                            <rect x="180" y="140" width="16" height="70" fill="#64748b" stroke="#475569" stroke-width="1"/>
                            <rect x="504" y="140" width="16" height="70" fill="#64748b" stroke="#475569" stroke-width="1"/>
                            <rect x="170" y="205" width="36" height="6" fill="#334155"/>
                            <rect x="494" y="205" width="36" height="6" fill="#334155"/>
                            
                            <g id="seqTrackBody" transform="translate(0, 0)">
                                <rect x="120" y="160" width="460" height="35" rx="4" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                                <rect x="172" y="185" width="32" height="10" fill="#f59e0b"/>
                                <rect x="496" y="185" width="32" height="10" fill="#f59e0b"/>
                                
                                <path id="seqLeftRail" d="M 210 160 L 210 120 L 205 120 L 205 110 L 235 110 L 235 120 L 230 120 L 230 160 Z" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                                <path id="seqRightRail" d="M 470 160 L 470 120 L 465 120 L 465 110 L 495 110 L 495 120 L 490 120 L 490 160 Z" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                            </g>
                        </g>

                        <!-- Step 3 -->
                        <g id="seqGroupStep3" opacity="0" class="transition-all duration-500">
                            <path d="M 160 170 A 15 15 0 1 1 160 195" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="3,2"/>
                            <polygon points="160,195 166,190 166,200" fill="#0284c7"/>
                            <text x="105" y="185" font-size="10" font-weight="bold" fill="#0284c7">스핀들 볼트 미세 회전</text>
                            
                            <circle cx="560" cy="115" r="22" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
                            <line x1="560" y1="115" x2="560" y2="98" stroke="#dc2626" stroke-width="2" id="seqDialNeedle"/>
                            <circle cx="560" cy="115" r="3" fill="#dc2626"/>
                            <line x1="538" y1="115" x2="495" y2="115" stroke="#0284c7" stroke-width="2"/>
                            <text x="560" y="82" text-anchor="middle" font-size="10" font-weight="black" fill="#0284c7">다이얼 게이지 0점 (±0.5mm 정합)</text>
                        </g>

                        <!-- Step 4 (레일 X=222 위로 쇳물 주입) -->
                        <g id="seqGroupStep4" opacity="0" class="transition-all duration-500">
                            <path d="M 202 20 L 242 20 L 232 65 L 212 65 Z" fill="#c2410c" stroke="#ea580c" stroke-width="2"/>
                            <line x1="222" y1="65" x2="222" y2="110" stroke="#ea580c" stroke-width="6" stroke-linecap="round"/>
                            <line x1="222" y1="65" x2="222" y2="110" stroke="#fef08a" stroke-width="2.5" stroke-linecap="round"/>
                            <circle cx="222" cy="110" r="15" fill="#ef4444" opacity="0.65"/>
                            <circle cx="222" cy="110" r="8" fill="#facc15"/>
                            <text x="222" y="14" text-anchor="middle" font-size="11" font-weight="black" fill="#c2410c">2,500℃ 테르밋 쇳물 레일 조인트 주입 중!</text>
                        </g>

                        <!-- Step 5 -->
                        <g id="seqGroupStep5" opacity="0" class="transition-all duration-500">
                            <rect x="0" y="145" width="700" height="65" fill="#94a3b8" opacity="0.85" stroke="#475569" stroke-width="2"/>
                            <text x="350" y="182" text-anchor="middle" font-size="13" font-weight="black" fill="#0f172a">TCL 도상 콘크리트 타설 완료 (28일 압축강도 ≥ 30 MPa 완료)</text>
                        </g>
                    </svg>
                </div>
                
                <div class="mt-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div id="seqBadge" class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">
                        STEP 1
                    </div>
                    <div>
                        <h3 id="seqTitle" class="text-base font-bold text-slate-900 mb-1">1단계: 지반 다짐 & 3D CP 측량</h3>
                        <p id="seqDesc" class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            상부 강화 노반의 평판재하시험(K30 &ge; 110 MN/m³) 지지력을 다짐 롤러로 단단히 확보하고, 광파기를 이용해 노선 정밀 3차원 선형 좌표를 측정합니다.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. 시공계획 수립 5단계 세부 수행 프로세스 (스핀들 상승·하강 조율 버튼 컨트롤 포함!) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 시공계획 수립 5단계 세부 수행 프로세스
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-amber-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 지반 다짐 & 3D CP 측량 검증</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">하부 노반 지지력(K30) 검증 및 3D 정밀 기준점 측량 좌표 설정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm">
                        <span class="term-highlight" onclick="openGlossary('hbs_test')">HBS 노반 지지력(K30 &ge; 110 MN/m³)</span> 시험 성적서를 최종 검토하고 3차원 광파 측량 성과점을 노선 좌표계에 보정합니다.
                    </p>
                </div>
                
                <!-- STEP 2 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-sky-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-sky-100 text-sky-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 궤광 가조립 및 지반 안착</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">조립장 사전 궤광 형성 및 현장 크레인 임시 안착</h3>
                    <p class="text-slate-600 text-xs sm:text-sm">
                        25m 레일과 콘크리트 침목을 사다리 형태의 궤광 뼈대로 묶어 다져진 강화 노반 위에 정밀하게 임시 내려놓습니다.
                    </p>
                </div>

                <!-- STEP 3 (★ 스핀들 상승/하강 정밀 조율 인터랙티브 시뮬레이터전격 포함!) -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 스핀들 볼트 수동 높이 조율 (선형 정밀 조정)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">★ 스핀들 게이지 수동 상승(▲)/하강(▼) 조율 및 다이얼 인디케이터 0점 정합 시뮬레이터</h3>
                    <p class="text-slate-600 text-xs sm:text-sm mb-4">
                        하부 높이 조절 나사(스핀들 볼트)를 수동 회전시켜 레일의 높낮이와 캔트를 조율하며, 아래 조작 버튼을 눌러 스핀들을 <strong>상승(▲)</strong>시키거나 <strong>하강(▼)</strong>시켜 다이얼 게이지 바늘 오차가 ±0.5mm 이내가 되도록 조정한 후 락너트를 고정합니다.
                    </p>
                    
                    <!-- [핵심 스핀들 수동 상승/하강 컨트롤 시뮬레이터] -->
                    <div class="my-4 grid grid-cols-1 lg:grid-cols-12 gap-5 bg-slate-100 p-5 rounded-xl border border-slate-300">
                        <!-- 왼쪽: 수동 조절 시뮬레이터 SVG -->
                        <div class="lg:col-span-7 bg-white p-4 rounded-xl border border-slate-200 shadow-inner flex flex-col justify-between">
                            <div style="height: 250px;" class="relative">
                                <svg id="spindleSvg" viewBox="0 0 450 250" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                                    <!-- 흙지반 (고정) -->
                                    <rect x="0" y="200" width="450" height="50" fill="#854d0e"/>
                                    <line x1="0" y1="200" x2="450" y2="200" stroke="#78350f" stroke-width="3"/>
                                    
                                    <!-- 스핀들 나사 기둥 및 받침판 (고정) -->
                                    <rect x="205" y="193" width="40" height="7" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                                    <rect x="215" y="90" width="20" height="103" fill="url(#screwPattern)" stroke="#475569" stroke-width="1.5"/>

                                    <line x1="80" y1="220" x2="130" y2="220" stroke="#78350f" stroke-width="1" stroke-dasharray="2,2"/>
                                    <circle cx="80" cy="220" r="2.5" fill="#78350f"/>
                                    <text x="135" y="223" font-size="9" font-weight="bold" fill="#78350f">단단한 지반 (강화 노반)</text>

                                    <line x1="225" y1="160" x2="140" y2="160" stroke="#0284c7" stroke-width="1" stroke-dasharray="2,2"/>
                                    <circle cx="225" cy="160" r="2.5" fill="#0284c7"/>
                                    <text x="135" y="163" text-anchor="end" font-size="9" font-weight="bold" fill="#0284c7">스핀들 볼트 (높이 조절 나사)</text>

                                    <!-- 상하 이동 궤광 및 락너트 뭉치 -->
                                    <g id="spindleBoltGroup" transform="translate(0, 0)">
                                        <rect x="200" y="100" width="50" height="10" fill="#cbd5e1" stroke="#475569" stroke-width="1.5"/>
                                        <rect x="195" y="125" width="60" height="12" rx="2" fill="#f59e0b" stroke="#d97706" stroke-width="1"/>
                                        <line x1="205" y1="125" x2="205" y2="137" stroke="#d97706" stroke-width="1"/>
                                        <line x1="245" y1="125" x2="245" y2="137" stroke="#d97706" stroke-width="1"/>
                                        
                                        <line x1="195" y1="131" x2="140" y2="131" stroke="#b45309" stroke-width="1" stroke-dasharray="2,2"/>
                                        <circle cx="195" cy="131" r="2.5" fill="#b45309"/>
                                        <text x="135" y="134" text-anchor="end" font-size="9" font-weight="bold" fill="#b45309">락너트 (선형 최종 고정용)</text>

                                        <rect x="100" y="70" width="250" height="30" rx="3" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.5"/>
                                        <line x1="115" y1="85" x2="60" y2="85" stroke="#64748b" stroke-width="1" stroke-dasharray="2,2"/>
                                        <circle cx="115" cy="85" r="2.5" fill="#64748b"/>
                                        <text x="55" y="88" text-anchor="end" font-size="9" font-weight="bold" fill="#475569">침목 (콘크리트 블럭)</text>

                                        <rect x="130" y="60" width="30" height="10" fill="#1e293b"/>
                                        <rect x="290" y="60" width="30" height="10" fill="#1e293b"/>
                                        
                                        <path d="M 135 60 L 135 25 L 130 25 L 130 20 L 155 20 L 155 25 L 150 25 L 150 60 Z" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                                        <path d="M 295 60 L 295 25 L 290 25 L 290 20 L 315 20 L 315 25 L 310 25 L 310 60 Z" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
                                        
                                        <line x1="130" y1="28" x2="60" y2="28" stroke="#334155" stroke-width="1" stroke-dasharray="2,2"/>
                                        <circle cx="130" cy="28" r="2.5" fill="#334155"/>
                                        <text x="55" y="31" text-anchor="end" font-size="9" font-weight="bold" fill="#1e293b">레일 (51R1 홈레일)</text>

                                        <path d="M 90 15 L 85 15 L 85 95 L 90 95 M 85 55 L 75 55" stroke="#047857" stroke-width="1.5" fill="none"/>
                                        <text x="70" y="58" text-anchor="end" font-size="9" font-weight="black" fill="#047857">궤광 (레일+침목 조립체)</text>
                                    </g>

                                    <!-- 다이얼 인디케이터 게이지 -->
                                    <g transform="translate(390, 80)">
                                        <circle cx="0" cy="0" r="30" fill="#f8fafc" stroke="#334155" stroke-width="2.5"/>
                                        <circle cx="0" cy="0" r="26" fill="none" stroke="#e2e8f0" stroke-width="1"/>
                                        <line id="dialPin" x1="-30" y1="0" x2="-75" y2="0" stroke="#334155" stroke-width="3"/>
                                        <circle id="dialPinTip" cx="-75" cy="0" r="3.5" fill="#dc2626"/>
                                        <text x="0" y="-12" text-anchor="middle" font-size="7" font-weight="black" fill="#1e293b">DIAL GAUGE</text>
                                        <path d="M -7 -20 A 21 21 0 0 1 7 -20" stroke="#10b981" stroke-width="4" fill="none"/>
                                        <line id="dialNeedle" x1="0" y1="0" x2="0" y2="-22" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round" transform="rotate(-60)"/>
                                        <circle cx="0" cy="0" r="4" fill="#dc2626"/>
                                    </g>
                                    
                                    <line x1="390" y1="110" x2="350" y2="140" stroke="#475569" stroke-width="1" stroke-dasharray="2,2"/>
                                    <circle cx="390" cy="110" r="2.5" fill="#475569"/>
                                    <text x="345" y="148" font-size="9" font-weight="bold" fill="#334155" text-anchor="middle">다이얼 인디케이터</text>
                                    <text x="345" y="158" font-size="8" fill="#64748b" text-anchor="middle">(정밀 바늘 측정기)</text>
                                    
                                    <defs>
                                        <pattern id="screwPattern" width="10" height="6" patternUnits="userSpaceOnUse">
                                            <line x1="0" y1="1" x2="10" y2="1" stroke="#64748b" stroke-width="1.5"/>
                                            <line x1="0" y1="4" x2="10" y2="4" stroke="#e2e8f0" stroke-width="1.5"/>
                                        </pattern>
                                    </defs>
                                </svg>
                            </div>

                            <!-- 상승 / 하강 조작 버튼 및 오차 알림판 -->
                            <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-200">
                                <div class="flex items-center gap-2">
                                    <button onclick="adjustSpindle(1)" class="sim-btn bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3.5 py-2 rounded-lg border border-emerald-700 shadow-sm">▲ 상승 (나사 조임)</button>
                                    <button onclick="adjustSpindle(-1)" class="sim-btn bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold px-3.5 py-2 rounded-lg border border-rose-700 shadow-sm">▼ 하강 (나사 풀기)</button>
                                </div>
                                <div id="spindleAlert" class="text-xs font-bold px-3 py-1.5 rounded bg-rose-100 text-rose-800 border border-rose-200 transition-all duration-300">
                                    오차 초과 (-3.0mm)
                                </div>
                            </div>
                        </div>
                        
                        <!-- 오른쪽 순서 설명 -->
                        <div class="lg:col-span-5 flex flex-col justify-center space-y-3">
                            <h5 class="text-xs font-black text-slate-800 uppercase tracking-wider">📋 궤광 조립/조정 시공 순서</h5>
                            <ol class="list-decimal pl-4 text-xs text-slate-600 space-y-2">
                                <li><strong>1단계. 궤광 임시 안착:</strong> 조립된 궤광 뼈대를 지반 위에 가설치합니다.</li>
                                <li><strong>2단계. 다이얼 인디케이터 셋업:</strong> 레일 머리에 핀을 대어 편차를 잽니다.</li>
                                <li><strong>3단계. 스핀들 볼트 수동 조정:</strong> 버튼을 눌러 나사를 돌려 바늘을 ±0.5mm(0점)에 맞춥니다.</li>
                                <li><strong>4단계. 락너트 조임 고정:</strong> 락너트를 꽉 조여 궤도 선형을 영구 고정합니다.</li>
                            </ol>
                        </div>
                    </div>
                </div>

                <!-- STEP 4 (테르밋 용접 사진 3종 세트!) -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-orange-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">4</div>
                    <span class="bg-orange-100 text-orange-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 4. 레일 테르밋 쇳물 용접 (장대레일화)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">2,500℃ 화학반응 쇳물 주입 및 비파괴 UT 검사</h3>
                    <p class="text-slate-600 text-xs sm:text-sm mb-3">
                        콘크리트 타설 전, 도가니 화학반응 쇳물을 레일 틈새에 흘려보내 소음과 진동을 없애는 장대레일 용접을 실시합니다.
                    </p>
                    
                    <!-- 레퍼런스 사진 3종 세트 -->
                    <div class="bg-slate-100 p-4 rounded-xl border border-slate-200">
                        <h5 class="text-xs font-bold text-slate-700 mb-3 flex items-center gap-1.5">
                            <span class="inline-block w-1.5 h-3 bg-blue-600 rounded"></span>
                            테르밋 용접 공정 실무 레퍼런스 (현장 사진 & 모식도)
                        </h5>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="bg-white p-2 rounded-lg border border-slate-300 shadow-sm img-card clickable-diagram" onclick="openDiagramZoom('imgThermitField', '① 가설 궤도 테르밋 쇳물 주입 시공 사진')">
                                <img id="imgThermitField" src="./thermit_field.png" class="w-full h-40 object-cover rounded" alt="테르밋 현장 용접">
                                <p class="text-[10px] text-slate-500 mt-1.5 font-bold text-center">① 가설 궤도 테르밋 쇳물 주입</p>
                            </div>
                            <div class="bg-white p-2 rounded-lg border border-slate-300 shadow-sm img-card clickable-diagram" onclick="openDiagramZoom('imgThermitCrucible', '② 도가니 용탕 2,500도 화학 반응 사진')">
                                <img id="imgThermitCrucible" src="./thermit_crucible.png" class="w-full h-40 object-cover rounded" alt="도가니 화학 반응">
                                <p class="text-[10px] text-slate-500 mt-1.5 font-bold text-center">② 도가니 용탕 2,500도 반응</p>
                            </div>
                            <div class="bg-white p-2 rounded-lg border border-slate-300 shadow-sm img-card clickable-diagram" onclick="openDiagramZoom('imgThermitDiagram', '③ 테르밋 용접 단면 구조도')">
                                <img id="imgThermitDiagram" src="./thermit_diagram.png" class="w-full h-40 object-contain rounded" alt="테르밋 단면 모식도">
                                <p class="text-[10px] text-slate-500 mt-1.5 font-bold text-center">③ 테르밋 용접 단면 구조도</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- STEP 5 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">5</div>
                    <span class="bg-green-100 text-green-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 5. 도상 콘크리트(TCL) 타설 및 준공 제출</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">도상 콘크리트 슬래브 영구 고정 및 시공계획서 최종 마감</h3>
                    <p class="text-slate-600 text-xs sm:text-sm">
                        용접 UT 검사 합격 후, <span class="term-highlight" onclick="openGlossary('tcl_concrete')">TCL 도상 콘크리트(강도 &ge; 30 MPa)</span>를 연속 타설하여 궤도를 지반에 매설 완료하고 감리 승인서를 득합니다.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
""" + common_modal_html + """

<script>
// Master 5-Step Simulator Script
let currentStepIdx = 1;
let autoPlayTimer = null;

const stepData = {
    1: {
        badge: 'STEP 1',
        badgeBg: 'bg-amber-500 text-white',
        title: '1단계: 지반 다짐 & 3D CP 측량 (기초 단계)',
        desc: '상부 강화 노반의 평판재하시험(K30 ≥ 110 MN/m³) 지지력을 다짐 롤러로 단단히 확보하고, 광파기를 이용해 노선 정밀 3차원 선형 좌표를 측량합니다.',
        btnColor: 'bg-amber-500 text-white border-amber-600'
    },
    2: {
        badge: 'STEP 2',
        badgeBg: 'bg-sky-500 text-white',
        title: '2단계: 궤광 가조립 & 지반 안착 (레일 뼈대 안착)',
        desc: '조립장에서 25m 표준 레일과 콘크리트 침목을 사다리 뼈대 형태(궤광)로 사전 조립한 뒤, 크레인을 사용해 단단한 지반 위에 임시 안착시킵니다.',
        btnColor: 'bg-sky-500 text-white border-sky-600'
    },
    3: {
        badge: 'STEP 3',
        badgeBg: 'bg-emerald-500 text-white',
        title: '3단계: 스핀들 볼트 수동 높이 조율 (정밀 선형 조정)',
        desc: '하부 높이 조절 나사(스핀들 볼트)를 수동 회전시켜 궤도의 캔트와 수평 높이를 정밀 조정하며, 다이얼 인디케이터 바늘을 ±0.5mm(0점) 범위에 맞춥니다.',
        btnColor: 'bg-emerald-500 text-white border-emerald-600'
    },
    4: {
        badge: 'STEP 4',
        badgeBg: 'bg-orange-500 text-white',
        title: '4단계: 레일 테르밋 쇳물 용접 (이 단계! 장대레일화)',
        desc: '콘크리트를 붓기 직전, 레일 머리 위치(X=222) 상부 도가니 화학반응으로 생성된 2,500℃ 초고열 쇳물을 레일 틈새에 흘려부어 하나의 길다란 장대레일로 연동 연결합니다.',
        btnColor: 'bg-orange-500 text-white border-orange-600'
    },
    5: {
        badge: 'STEP 5',
        badgeBg: 'bg-green-500 text-white',
        title: '5단계: 도상 콘크리트(TCL) 타설 (영구 매설 고정)',
        desc: '테르밋 용접 비파괴 검사(UT) 합격 후, 레일과 침목 주변에 도상 콘크리트(압축강도 ≥ 30 MPa)를 가득 타설하여 궤도를 지반에 단단히 고정 완료합니다.',
        btnColor: 'bg-green-500 text-white border-green-600'
    }
};

function setStep(step) {
    currentStepIdx = step;
    const data = stepData[step];
    
    for (let i = 1; i <= 5; i++) {
        const btn = document.getElementById(`stepBtn${i}`);
        if (i === step) {
            btn.className = `sim-step-btn active ${data.btnColor} p-3 rounded-xl border font-bold text-left transition-all`;
        } else {
            btn.className = `sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200`;
        }
    }
    
    const badgeEl = document.getElementById('seqBadge');
    badgeEl.innerText = data.badge;
    badgeEl.className = `${data.badgeBg} font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5`;
    document.getElementById('seqTitle').innerText = data.title;
    document.getElementById('seqDesc').innerText = data.desc;
    
    const step1Group = document.getElementById('seqGroupStep1');
    const step2Group = document.getElementById('seqGroupStep2');
    const trackGroup = document.getElementById('seqGroupTrack');
    const step3Group = document.getElementById('seqGroupStep3');
    const step4Group = document.getElementById('seqGroupStep4');
    const step5Group = document.getElementById('seqGroupStep5');
    const leftRail = document.getElementById('seqLeftRail');
    
    step1Group.setAttribute('opacity', step === 1 ? '1' : '0');
    step2Group.setAttribute('opacity', step === 2 ? '1' : '0');
    trackGroup.setAttribute('opacity', step >= 2 ? '1' : '0');
    step3Group.setAttribute('opacity', step === 3 ? '1' : '0');
    step4Group.setAttribute('opacity', step === 4 ? '1' : '0');
    step5Group.setAttribute('opacity', step === 5 ? '1' : '0');
    
    if (step === 4) {
        if (leftRail) leftRail.setAttribute('fill', '#ea580c');
    } else {
        if (leftRail) leftRail.setAttribute('fill', '#475569');
    }
    
    if (step === 2) {
        trackGroup.setAttribute('transform', 'translate(0, 20)');
    } else if (step === 3) {
        trackGroup.setAttribute('transform', 'translate(0, 0)');
        const needle = document.getElementById('seqDialNeedle');
        if (needle) needle.setAttribute('transform', 'rotate(0 560 115)');
    } else {
        trackGroup.setAttribute('transform', 'translate(0, 0)');
    }
}

function toggleAutoPlay() {
    const playText = document.getElementById('playText');
    const playIcon = document.getElementById('playIcon');
    
    if (autoPlayTimer) {
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
        playText.innerText = "자동 시뮬레이션 재생";
        playIcon.innerText = "▶";
    } else {
        playText.innerText = "일시 정지";
        playIcon.innerText = "⏸";
        autoPlayTimer = setInterval(() => {
            currentStepIdx = (currentStepIdx % 5) + 1;
            setStep(currentStepIdx);
        }, 3000);
    }
}

// Manual Spindle Simulator Script
let currentSpindleStep = -30;

function adjustSpindle(direction) {
    currentSpindleStep += direction * 5;
    if (currentSpindleStep > 25) currentSpindleStep = 25;
    if (currentSpindleStep < -45) currentSpindleStep = -45;
    updateSpindleVisual();
}

function updateSpindleVisual() {
    const spindleBolt = document.getElementById('spindleBoltGroup');
    const dialNeedle = document.getElementById('dialNeedle');
    const dialPin = document.getElementById('dialPin');
    const dialPinTip = document.getElementById('dialPinTip');
    const alertEl = document.getElementById('spindleAlert');
    
    if (spindleBolt) {
        spindleBolt.setAttribute('transform', `translate(0, ${currentSpindleStep})`);
    }
    
    const needleAngle = currentSpindleStep * 3;
    if (dialNeedle) {
        dialNeedle.setAttribute('transform', `rotate(${needleAngle})`);
    }
    
    const pinOffset = currentSpindleStep * 0.4;
    if (dialPin) {
        dialPin.setAttribute('x1', -30 + pinOffset);
    }
    if (dialPinTip) {
        dialPinTip.setAttribute('cx', -75 + pinOffset);
    }
    
    const mmError = (currentSpindleStep * 0.1).toFixed(1);
    if (alertEl) {
        if (Math.abs(mmError) <= 0.5) {
            alertEl.innerText = `정밀 합격 (${mmError > 0 ? '+' : ''}${mmError}mm)`;
            alertEl.className = "text-xs font-bold px-3 py-1.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-300 transition-all duration-300";
        } else {
            alertEl.innerText = `오차 초과 (${mmError > 0 ? '+' : ''}${mmError}mm)`;
            alertEl.className = "text-xs font-bold px-3 py-1.5 rounded bg-rose-100 text-rose-800 border border-rose-200 transition-all duration-300";
        }
    }
}
</script>
</body>
</html>
"""

force_write(path_guideline, complete_wbs11_guideline_html)
force_write(path_guideline_alt, complete_wbs11_guideline_html)

print("\n🎉 SUCCESSFULLY RESTORED ULTIMATE COMPLETE WBS 11 GUIDELINE WITH ALL FEATURES & SPINDLE SIMULATOR!")
