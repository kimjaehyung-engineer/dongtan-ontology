import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Target paths for WBS 13 and WBS 14
wbs13_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\13_[HBS] 강화노반 확인\수행지침"
wbs14_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\14_[HBS] 콘크리트 타설 및 양생\수행지침"

path_gui13 = os.path.join(wbs13_dir, "[HBS] 강화노반 확인_수행지침.html")
path_gui13_alt = os.path.join(wbs13_dir, "13_[HBS] 강화노반 확인_수행지침.html")

path_gui14 = os.path.join(wbs14_dir, "[HBS] 콘크리트 타설 및 양생_수행지침.html")
path_gui14_alt = os.path.join(wbs14_dir, "14_[HBS] 콘크리트 타설 및 양생_수행지침.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Updated Zoom Modal for: {path}")

# Minimal Glossary Style & Enhanced Image/Diagram Zoom Modal Style
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
<!-- 용어 모달 -->
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 시방 기술 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<!-- ★ [신규 탑재] 대형 도식/그림 확대 라이트박스 팝업 모달 -->
<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; color: #0f172a; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 도식 대형 고화질 정밀 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
            <!-- Dynamic Enlarged SVG or Image content inserted here -->
        </div>
        <div style="margin-top: 14px; text-align: right; font-size: 0.85rem; font-weight: 700; color: #64748b;">
            💡 팁: ESC 키를 누르시거나 닫기(×) 버튼을 누르면 이전 화면으로 복귀합니다.
        </div>
    </div>
</div>

<script>
const glossaryData = {
    'hbr': {
        title: '🏗️ HBR 기초 콘크리트 (Hydraulic Base Concrete)',
        desc: '강화노반 상부에 타설되는 궤도 기초 콘크리트 레이어입니다. TCL도상 및 반-PC 슬래브 패널의 하중을 균일하게 받쳐주어 트램 궤도의 구조적 안정성을 확보합니다.'
    },
    'plant_distance': {
        title: '🚚 레미콘 이격거리 4.8km & 운반 60분 이내',
        desc: '콘크리트 슬럼프 로스 및 초기 경화 유출을 방지하기 위해 레미콘 배치 플랜트와 현장 이격거리를 4.8km 이내로 지정하고, 출하 후 60분 이내 현장 타설을 완료하는 표준 시방 수칙입니다.'
    },
    'slump_strength': {
        title: '📊 슬럼프 10cm 이하 & 28일 강도 ≥ 21 MPa',
        desc: 'HBR 콘크리트 워커빌리티와 밀실 다짐을 확보하기 위한 슬럼프 값 10cm 이하 시방 기준과 28일 경화 압축강도 21 MPa 이상(최소 18 MPa 이상) 확보 지수입니다.'
    },
    'curing_7days': {
        title: '💧 7일 습윤 부직포 양생',
        desc: '콘크리트 타설 직후 수분 급속 증발에 따른 건조수축 균열을 차단하기 위해 부직포를 덮고 7일 이상 지속적인 분무 살수 양생을 수행하는 수칙입니다.'
    },
    'hbs': {
        title: '🧱 HBS 강화노반 (Hydraulic Base Support Subgrade)',
        desc: '콘크리트 도상(TCL) 하부에 시공되는 고지지력 상부 노반층입니다. 트램 주행 하중을 노상 및 원지반으로 안전하게 분산시키는 핵심 기초 공종입니다.'
    },
    'pbt': {
        title: '⚙️ 평판재하시험 (Plate Bearing Test, PBT)',
        desc: '강화노반 표면에 Φ300mm 재하 평판을 놓고 유압 재크로 하중을 가하여 지반의 노반 반력계수(K30) 및 2차 변형계수(Ev2)를 정밀 측정하는 재하시험입니다.'
    },
    'k30_ev2': {
        title: '📊 K30 ≥ 110 MN/m³ & Ev2 ≥ 120 MPa',
        desc: '트램 콘크리트 도상 부등침하를 예방하기 위한 절대 지지력 지수입니다. K30 반력계수 110 MN/m³ 이상 및 Ev2 변형계수 120 MPa 이상(Ev2/Ev1 ≤ 2.2)이 필수 검증되어야 합니다.'
    },
    'cross_slope': {
        title: '📐 횡단 구배 2.0% & 높이 오차 ±10mm',
        desc: '강화노반 표면 배수 성능 확보를 위한 횡단 구배 2.0% 유지 수칙과 콘크리트 슬래브 두께 유지를 위한 마무리 높이 공차 ±10mm 이내 관리 기준입니다.'
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

// 대형 확대 팝업 모달 함수
function openDiagramZoom(elementId, titleText) {
    const srcEl = document.getElementById(elementId);
    if (!srcEl) return;
    
    const zoomBody = document.getElementById('zoomBody');
    document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "도식 대형 정밀 보기");
    
    zoomBody.innerHTML = srcEl.outerHTML;
    
    // SVG 확대 스타일 처리
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
# WBS 14 GUIDELINE HTML (ENLARGED SVG FONTS & CLICKABLE ZOOM MODAL)
# =========================================================================
guideline14_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 콘크리트 타설 및 양생 수행지침서</title>
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
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-14 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">HBR 타설 & 7일 습윤 양생 실무</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[HBS] 콘크리트 타설 및 양생 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"기초콘크리트(HBR): 4.8km 운반 통제, 슬럼프(10cm) 검사, 콜드조인트 방지 타설 및 7일 습윤 양생 매뉴얼"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [HBS] 기초콘크리트 타설 및 양생 실무 핵심
            </h4>
            <p class="leading-relaxed">
                강화노반 상부에 <strong><span class="term-highlight" onclick="openGlossary('hbr')">HBR 기초콘크리트</span></strong>를 타설하는 공종입니다. 레미콘 이격거리 <strong><span class="term-highlight" onclick="openGlossary('plant_distance')">4.8km 이내(60분 이내 도착)</span></strong> 확보, 거푸집 테이핑을 통한 시멘트풀 유출 차단, <strong><span class="term-highlight" onclick="openGlossary('slump_strength')">슬럼프 10cm 이하</span></strong> 시험, 연속 타설 및 바이브레이터 고주파 밀실 다짐, 그리고 <strong><span class="term-highlight" onclick="openGlossary('curing_7days')">습윤 부직포 7일 양생</span></strong>을 체계적으로 시행합니다.
            </p>
        </div>

        <!-- 1. HBR 콘크리트 4단계 시공 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> HBR 콘크리트 타설·양생 4단계 마스터 프로세스 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">배합 & 4.8km 운반</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            현장 이격거리 <strong>4.8km 이내</strong> 레미콘 공장 배정, 출하 60분 이내 현장 도착 관리
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        🚚 핵심: 이격거리 &le; 4.8km
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">거푸집 테이핑·슬럼프</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            시멘트풀 유출 차단 테이핑 및 현장 <strong>슬럼프 &le; 10cm</strong> 품질 검사
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        🧪 핵심: 슬럼프 &le; 10cm
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">연속타설·고주파다짐</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            콜드조인트 방지 펌프카 연속 타설 & 바이브레이터 <strong>밀실 고주파 다짐</strong>
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        ⚙️ 핵심: 바이브레이터 다짐
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">7일 습윤양생·강도승인</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            습윤 부직포 <strong>7일 양생</strong> 및 28일 압축강도 <strong>&ge; 21 MPa</strong> 최종 승인
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        💧 핵심: 7일 습윤 양생
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. HBR 콘크리트 타설 & 양생 기술 도식 (클릭 시 별도 팝업으로 초대형 확대) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> HBR 콘크리트 타설 & 양생 정밀 공학 기술 도식 (🔍 도식 클릭 시 대형 팝업 확대)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 도식 1: HBR 콘크리트 타설 & 거푸집 유출방지 테이핑 구조 단면도 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 1] HBR 타설 & 거푸집 테이핑 단면도
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">슬럼프 &le; 10cm</span>
                        </div>
                        
                        <!-- SVG Diagram 1 Container (Clickable for Zoom) -->
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram14_1', '[도식 1] HBR 타설 & 거푸집 테이핑 단면도')">
                            <svg id="svgDiagram14_1" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- 강화노반 기초 지층 -->
                                <rect x="30" y="155" width="360" height="45" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                                <text x="210" y="182" font-size="12" font-weight="bold" fill="#78350f" text-anchor="middle">HBS 강화노반 지층 (K30 ≥ 110 MN/m³)</text>

                                <!-- HBR 타설 콘크리트 층 -->
                                <rect x="50" y="95" width="320" height="60" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                                <text x="210" y="132" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">HBR 기초콘크리트 타설층 (두께 오차 ±10mm)</text>

                                <!-- 좌우 거푸집 & 밀봉 테이핑 -->
                                <rect x="40" y="75" width="10" height="85" fill="#b45309"/>
                                <rect x="370" y="75" width="10" height="85" fill="#b45309"/>
                                <circle cx="45" cy="160" r="6" fill="#ef4444"/>
                                <circle cx="375" cy="160" r="6" fill="#ef4444"/>
                                <text x="15" y="65" font-size="11" font-weight="black" fill="#ef4444" text-anchor="start">시멘트풀 유출 방지 테이핑</text>

                                <!-- 펌프카 슈트 & 바이브레이터 -->
                                <line x1="210" y1="15" x2="210" y2="95" stroke="#0284c7" stroke-width="6"/>
                                <path d="M 195 15 L 225 15 L 210 45 Z" fill="#0284c7"/>
                                <text x="210" y="12" font-size="12" font-weight="black" fill="#0284c7" text-anchor="middle">레미콘 펌프카 슈트 (이격거리 ≤ 4.8km)</text>

                                <line x1="295" y1="45" x2="295" y2="115" stroke="#059669" stroke-width="3.5" stroke-dasharray="3,2"/>
                                <rect x="290" y="110" width="10" height="22" fill="#059669" rx="2"/>
                                <text x="350" y="60" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">고주파 바이브레이터 다짐</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>⚙️ 타설 핵심:</strong> 거푸집 접합면을 테이핑 처리하여 시멘트풀 유출을 차단하고, 펌프카로 <strong>슬럼프 10cm 이하 콘크리트를 연속 타설</strong>하며 바이브레이터 밀실 고주파 다짐을 실시합니다.
                    </div>
                </div>

                <!-- 도식 2: 7일 습윤 부직포 포설 양생 & 강도 측정 도면 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 2] 7일 습윤 부직포 양생 & 강도 측정
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">강도 &ge; 21 MPa</span>
                        </div>
                        
                        <!-- SVG Diagram 2 Container (Clickable for Zoom) -->
                        <div class="clickable-diagram bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200" onclick="openDiagramZoom('svgDiagram14_2', '[도식 2] 7일 습윤 부직포 양생 & 강도 측정')">
                            <svg id="svgDiagram14_2" viewBox="0 0 420 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- HBR 콘크리트 층 -->
                                <rect x="40" y="115" width="340" height="65" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                                <text x="210" y="155" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">HBR 기초콘크리트 경화층</text>

                                <!-- 습윤 부직포 덮개 -->
                                <rect x="40" y="105" width="340" height="10" fill="#059669" opacity="0.9" rx="1"/>
                                <text x="210" y="98" font-size="12" font-weight="black" fill="#047857" text-anchor="middle">7일 연속 습윤 부직포 덮개 포설</text>

                                <!-- 살수 튜브 분무 물방울 -->
                                <line x1="50" y1="75" x2="370" y2="75" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="4,3"/>
                                <circle cx="90" cy="90" r="3.5" fill="#38bdf8"/>
                                <circle cx="170" cy="90" r="3.5" fill="#38bdf8"/>
                                <circle cx="250" cy="90" r="3.5" fill="#38bdf8"/>
                                <circle cx="330" cy="90" r="3.5" fill="#38bdf8"/>
                                <text x="210" y="65" font-size="11" font-weight="black" fill="#0284c7" text-anchor="middle">자동 분무 살수 튜브 (지속 습윤 양생)</text>

                                <!-- 몰드 강도 시험 공시체 -->
                                <g transform="translate(330, 15)">
                                    <rect x="0" y="0" width="35" height="42" fill="#94a3b8" stroke="#1e293b" stroke-width="1.5"/>
                                    <text x="17" y="-5" font-size="9" font-weight="bold" fill="#0f172a" text-anchor="middle">28일 몰드</text>
                                    <text x="17" y="25" font-size="8" font-weight="black" fill="#1e293b" text-anchor="middle">≥21MPa</text>
                                </g>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-100 text-xs text-emerald-900 leading-relaxed">
                        <strong>💧 양생 핵심:</strong> 콘크리트 타설 직후 <strong>습윤 부직포를 포설하고 7일간 살수 양생</strong>을 수행하며, 28일 현장 몰드 시편 압축강도가 <strong>21 MPa 이상(최소 18 MPa 이상)</strong> 달성 시 최종 통과 조치합니다.
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
                        <h4 class="font-bold text-slate-900 text-sm">레미콘 공장 배정 & 이격거리(4.8km 이내) 운반 통제 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            현장 인근 <span class="term-highlight" onclick="openGlossary('plant_distance')">4.8km 이내 배치플랜트 레미콘 공장</span>을 지정하고, 레미콘 출하 후 현장 도착 및 타설 완료까지 <strong>60분 이내</strong>로 정밀 스케줄링 관리합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">거푸집 테이핑 밀봉 & 현장 슬럼프(10cm 이하) 검사 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            시멘트풀 유출로 인한 공극을 예방하기 위해 거푸집 조인트면 테이핑을 가설하고, 현장 도착 레미콘 차량별로 <span class="term-highlight" onclick="openGlossary('slump_strength')">슬럼프(10cm 이하) 및 공기량(4.5%)</span> 시험을 즉시 수행합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">콜드조인트 방지 연속 타설 & 바이브레이터 고주파 다짐 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            펌프카를 투입하여 중단 없는 연속 타설을 시행함으로써 콜드조인트를 예방하고, 고주파 꽂힘 바이브레이터를 투입하여 기포 및 미타설 공극이 없도록 밀실 다짐 조치합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">7일 습윤 부직포 양생 & 28일 압축강도(≥ 21 MPa) 최종 승인 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            타설 두께 오차 <strong>&plusmn;10mm 이내</strong>를 측량 후, 타설 직후 습윤 부직포를 포설하여 <span class="term-highlight" onclick="openGlossary('curing_7days')">7일간 지속 살수 양생</span>을 시행하며, 현장 몰드 시편 28일 압축강도 <strong>&ge; 21 MPa(최소 18 MPa 이상)</strong> 확인 후 감리 승인 마감합니다.
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

force_write(path_gui14, guideline14_html)
force_write(path_gui14_alt, guideline14_html)

print("\n🎉 SUCCESSFULLY UPDATED ENLARGED SVG FONTS & CLICKABLE ZOOM MODAL IN WBS 14!")
