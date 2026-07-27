import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

target_folder = None
for f in os.listdir(base_dir):
    if f.startswith("4_") or ("전기" in f and "신호" in f):
        target_folder = os.path.join(base_dir, f)
        break

if not target_folder:
    print("❌ ERROR: Target folder for WBS 9000-2-4 not found!")
    sys.exit(1)

print(f"Target WBS 9000-2-4 Folder: {target_folder}")

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

common_js = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 시스템 인터페이스 기술 해설</h3>
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
    'power_interface': {
        title: '⚡ 전기 분야 소요전력 & 22.9kV 수전 인터페이스',
        desc: '동탄트램 통신 설비(기계실, 관제실, 앰프실, 정거장 PIS) 가동을 위한 통신 전용 소요전력 용량을 대조하고 전기 분전반 배관 관로를 확보하는 수칙입니다.'
    },
    'signaling_conduit': {
        title: '🚦 신호 분야 공동관로 & CBI/PPC 연동',
        desc: '통신 72-Core 광케이블과 신호 축차계수기 및 교차로 트램 우선신호 제어기(PPC) 케이블을 공동관로에 분리 배치하여 신호 간섭을 차단하는 인터페이스 수칙입니다.'
    },
    'vehicle_lter': {
        title: '🚃 트램 차량 차상 장치 & LTE-R 무선 안테나',
        desc: '트램 차량 운전대 차상 통신장치, 열차 무선 LTE-R 지상 기지국 및 정차역 정전 대비 정차 급속 충전 모듈과의 인터페이스 결속 수칙입니다.'
    },
    'psd_emergency': {
        title: '🚪 PSD(스크린도어) 비상통화 및 PIS/PA 방송 연동',
        desc: '승강장 스크린도어 비상 통화장치 및 승객 안내 방송(PA/PIS) 모듈을 통신 관제 센터와 1:1 하드웨어/소프트웨어 연동 검측하는 기술 수칙입니다.'
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

# 1. STANDARD HTML
std_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 전기 / 신호 / 기계 / PSD / 차량 인터페이스 협의 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Standard</span>
        <h1 class="text-3xl font-black mt-2">전기 / 신호 / 기계 / PSD / 차량 인터페이스 협의 표준서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-4 | 주관: 현장 시스템팀 / 통신 협업업체</p>
    </div>
    
    <div class="p-8 space-y-8">
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-blue-950 mb-2">🎯 표준 목적 (Objective)</h3>
            <p class="text-slate-700 text-sm font-medium leading-relaxed">
                동탄트램 연계 분야(전기 소요전력, 신호 공동관로, 차량 차상 통신장치, PSD 비상통화 및 기계 접지) 간의 사전 기술 협의를 완수하고 인터페이스 도면, 연동 모식도, 지상-차상 무선 신호 규격을 확정하여 최종 인터페이스 회의록 및 1,2공구 시스템 통합 관리대장의 무결성을 보장함을 목적으로 함.
            </p>
        </div>

        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-blue-600 pb-2">📜 5대 분야 시스템 인터페이스 시방 수칙 (Methodology)</h3>
            <ul class="space-y-3">
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 1</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>전기 분야(소요전력):</strong> 통신 기계실, 관제실, PIS/PA 방송 장치의 소요전력 용량을 산정하고 전기 분전반 배관 관로 규격 및 전원 회로를 확정함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 2</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>신호 분야(공동관로 & CBI):</strong> 본선 및 정거장 72-Core 통신 광케이블과 신호 축차계수기 및 전자연동장치(CBI) 공동관로 배치 및 케이블 격리 파티션을 확정함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 3</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>차량 분야(차상장치 & LTE-R):</strong> 트램 차량 운전대 차상 통신장치, 차상-지상 무선 LTE-R 안테나 결속 및 차량 시운전 인터페이스 시험 항목을 확정함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 4</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>기계/PSD 분야(비상통화 & 이격거리):</strong> PSD(스크린도어) 비상통화장치 연동, 이종 케이블 간 최소 이격거리(≥300mm) 및 회로 분리 수칙을 반영하여 인터페이스 회의록을 체결함.</span>
                </li>
            </ul>
        </div>

        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-emerald-950 mb-2">📦 증빙 산출물 (Deliverables)</h3>
            <p class="text-emerald-900 text-sm font-bold">인터페이스 회의록, 분야별 연동 도면/모식도, 1,2공구 시스템 통합 관리대장, 5자 서명 체결 승인서</p>
        </div>
    </div>
</div>
</body>
</html>
"""

# 2. GUIDELINE HTML (HOW EXPANDED)
gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 전기 / 신호 / 기계 / PSD / 차량 인터페이스 협의 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {zoom_modal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Detailed Guideline</span>
        <h1 class="text-3xl font-black mt-2">전기 / 신호 / 기계 / PSD / 차량 인터페이스 초정밀 수행지침서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-4 | 주관: 현장 시스템팀 / 통신 협업업체 | "어떻게(HOW) 연동하는가 초정밀 가이드"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 친절한 개요 해설 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-sm text-blue-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 시스템 인터페이스 협의 현장 실무 개요</h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                동탄트램 서브시스템 간의 통합 무결성을 확보하기 위해 통신/전기/신호/차량/PSD 분야 간 인터페이스 요구조건을 사전에 정밀 조정합니다. 본 지침서는 현장 엔지니어가 작업 단계별로 <strong>어떻게(HOW) 분야별 도서를 대조하고, 이격거리를 실측하며, 차상-지상 연동 시험 및 서명</strong>을 수행해야 하는지 초정밀 행동 수칙을 제공합니다. 
                특히 <strong><span class="term-highlight" onclick="openGlossary('power_interface')">전기 소요전력</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('signaling_conduit')">신호 공동관로</span></strong>, <strong><span class="term-highlight" onclick="openGlossary('vehicle_lter')">차상 통신 LTE-R</span></strong> 및 <strong><span class="term-highlight" onclick="openGlossary('psd_emergency')">PSD 비상통화</span></strong> 수칙을 완벽 수록하였습니다.
            </p>
        </div>

        <!-- ☀️ 라이트 테마 특화 카드 섹션 -->
        <div class="bg-blue-50/70 border border-blue-200 p-7 rounded-2xl shadow-md space-y-6">
            <div class="border-b border-blue-200 pb-4">
                <span class="bg-blue-600 text-white text-xs font-black px-3 py-1 rounded-full uppercase">SPECIAL FOCUS</span>
                <h3 class="text-xl font-black text-blue-950 mt-2">📋 5대 연계 분야 정밀 실무 검토 가이드</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>⚡</span> 1. 전기 분야 (소요전력)</span>
                    <p class="text-slate-700 text-xs">기계실/관제실 전원용량 산정 및 전기 분전반 배관 관로 확정.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🚦</span> 2. 신호 분야 (공동관로 & CBI)</span>
                    <p class="text-slate-700 text-xs">72-Core 광케이블과 신호 관로 분리 격리 및 연동 기기 배치.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🚃</span> 3. 차량 분야 (차상장치 & LTE-R)</span>
                    <p class="text-slate-700 text-xs">트램 차상 통신 모뎀, LTE-R 안테나 결속 및 시운전 연동 시험.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🚪</span> 4. PSD 분야 (비상통화 & 이격)</span>
                    <p class="text-slate-700 text-xs">PSD 비상통화 모듈 1:1 연동, 이종 케이블 간격(≥300mm) 회로 분리.</p>
                </div>
            </div>
        </div>

        <!-- 1. FLEXIBLE 5-STEP ARCHITECTURE -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 5단계 수행 마스터 프로세스 (Flexible 5-Step Architecture)
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2">
                <div class="bg-blue-50 p-3 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <span class="bg-blue-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 1</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">도서 대조</h4>
                    <p class="text-[10px] text-blue-900 mt-1 font-medium">• 5대 분야 도면<br">• 연동 도서 대조</p>
                </div>
                <div class="bg-indigo-50 p-3 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <span class="bg-indigo-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">이격 실측</h4>
                    <p class="text-[10px] text-indigo-900 mt-1 font-medium">• 전력선 이격(≥300mm)<br">• 회로 분리 측정</p>
                </div>
                <div class="bg-cyan-50 p-3 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <span class="bg-cyan-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">차량 연동</h4>
                    <p class="text-[10px] text-cyan-900 mt-1 font-medium">• 차상 LTE-R 안테나<br">• 무선 신호 결속</p>
                </div>
                <div class="bg-teal-50 p-3 rounded-xl border border-teal-200 flex flex-col justify-between">
                    <span class="bg-teal-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">PSD 검측</h4>
                    <p class="text-[10px] text-teal-900 mt-1 font-medium">• 비상통화 1:1 연동<br">• PA/PIS 방송 시험</p>
                </div>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <span class="bg-emerald-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 5</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">5자 체결</h4>
                    <p class="text-[10px] text-emerald-900 mt-1 font-medium">• 회의록 날인<br">• 시스템 통합대장 연동</p>
                </div>
            </div>
        </div>

        <!-- 🔥 2. 초정밀 HOW(어떻게 수행하는가) 세부 실무 가이드 -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-indigo-600 pb-2">
                <span class="text-indigo-600">2.</span> 초정밀 HOW(어떻게 수행하는가) 세부 실무 가이드
            </h2>

            <div class="space-y-4 text-sm">
                <!-- STEP 1 HOW -->
                <div class="bg-white p-6 rounded-2xl border border-blue-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-blue-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 1 HOW</span>
                        <h3 class="font-bold text-base text-slate-900">5대 연계 분야 도서 대조 및 수칙 (HOW TO PREPARE)</h3>
                    </div>
                    <ul class="list-disc pl-5 text-slate-700 space-y-1.5 text-xs font-medium leading-relaxed">
                        <li><strong>전기/신호/차량/PSD 도면 1:1 대조:</strong> 5개 분야 CAD 인터페이스 도면을 오버레이하여 기계실 전원 입출력선, 신호 공동관로 및 스크린도어 인터페이스 핀 맵(Pin Map)을 선제 대조합니다.</li>
                        <li><strong>전원 용량 및 분전반 확인:</strong> 전기 분야로부터 통신 기계실(주/예비 22.9kV 수전) 소요 전력 용량을 수신하여 분전반 전용 차단기 용량을 사전 확정합니다.</li>
                    </ul>
                </div>

                <!-- STEP 2 HOW -->
                <div class="bg-white p-6 rounded-2xl border border-indigo-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-indigo-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 2 HOW</span>
                        <h3 class="font-bold text-base text-slate-900">이종 케이블 이격거리 실측 방법 (HOW TO MEASURE)</h3>
                    </div>
                    <ul class="list-disc pl-5 text-slate-700 space-y-1.5 text-xs font-medium leading-relaxed">
                        <li><strong>이격거리(≥300mm) 현장 실측:</strong> 전력선(고압)과 통신 72-Core 광케이블 간 유도장해 차단을 위해 최소 300mm 이상의 이격거리를 버니어 캘리퍼스 및 줄자로 현장 측정합니다.</li>
                        <li><strong>회로 분리 및 금속 트레이 격리:</strong> 동일 트레이 부가 불가피한 경우 내화 금속 차폐 파티션(상높이 50mm 이상)을 설치하여 회로를 물리적으로 완벽 차단합니다.</li>
                    </ul>
                </div>

                <!-- STEP 3 HOW -->
                <div class="bg-white p-6 rounded-2xl border border-cyan-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-cyan-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 3 HOW</span>
                        <h3 class="font-bold text-base text-slate-900">트램 차량 차상 장치 연동 방법 (HOW TO INSTALL & TEST)</h3>
                    </div>
                    <ul class="list-disc pl-5 text-slate-700 space-y-1.5 text-xs font-medium leading-relaxed">
                        <li><strong>차상 LTE-R 안테나 결속:</strong> 트램 차량 지붕 상부에 LTE-R 차상 안테나를 결속하고, 차상 통신 모뎀과 관제 센터 간 무선 커버리지 RF 수신 감도(-85dBm 이상)를 정밀 측정합니다.</li>
                        <li><strong>차량 시운전 연동 인터페이스:</strong> 차량 시험 운전 시 지상 기지국과 차상 단말 간 음성/영상 패킷 전송 손실률(0.01% 이하)을 검측합니다.</li>
                    </ul>
                </div>

                <!-- STEP 4 HOW -->
                <div class="bg-white p-6 rounded-2xl border border-teal-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-teal-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 4 HOW</span>
                        <h3 class="font-bold text-base text-slate-900">PSD 비상통화 및 신호 연동 방법 (HOW TO CONNECT)</h3>
                    </div>
                    <ul class="list-disc pl-5 text-slate-700 space-y-1.5 text-xs font-medium leading-relaxed">
                        <li><strong>PSD 비상통화버튼 1:1 시험:</strong> 정거장 승강장 PSD 표면에 설치된 비상통화버튼 조작 시 관제실 통신 콘솔로 3초 이내 즉시 착신 연동되는지 시험합니다.</li>
                        <li><strong>PA/PIS 방송 모듈 연동:</strong> 스크린도어 열림/닫힘 신호와 PIS 승객 안내 전광판 및 PA 음성 방송 모듈 간 지연 시간(0.5초 이내)을 검측합니다.</li>
                    </ul>
                </div>

                <!-- STEP 5 HOW -->
                <div class="bg-white p-6 rounded-2xl border border-emerald-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-emerald-600 text-white font-bold text-xs px-2.5 py-1 rounded">STEP 5 HOW</span>
                        <h3 class="font-bold text-base text-slate-900">5자 서명 체결 및 관리대장 등재 방법 (HOW TO SIGN-OFF)</h3>
                    </div>
                    <ul class="list-disc pl-5 text-slate-700 space-y-1.5 text-xs font-medium leading-relaxed">
                        <li><strong>5대 분야 책임 엔지니어 합동 서명:</strong> 통신/전기/신호/차량/PSD 분야 담당 엔지니어 및 감리원이 현장에 동시 입석하여 서명 체결합니다.</li>
                        <li><strong>1,2공구 시스템 통합 관리대장 등재:</strong> 체결된 서류 및 연동 모식도를 동탄트램 통합 대장에 실시간 등록하여 준공용 인허가 서류로 보관합니다.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 3. 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 2D Visual 기술 도식 (Enriched 2D SVG)
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_r4', '[WBS 9000-2-4] 전기/신호/기계/PSD/차량 5대 분야 시스템 연동 2D SVG')">
                <svg id="svg_r4" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                    <rect x="25" y="20" width="230" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                    <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">⚡ 전기/신호/차량 연동</text>
                    <text x="40" y="75" font-size="11" font-weight="bold" fill="#334155">• 전기 소요전력 & 신호 공동관로</text>
                    <text x="40" y="98" font-size="11" font-weight="bold" fill="#334155">• 차량 차상 LTE-R 안테나 결속</text>

                    <path d="M 265 80 L 295 80" stroke="#2563eb" stroke-width="3"/>
                    <polygon points="295,75 305,80 295,85" fill="#2563eb"/>

                    <rect x="310" y="20" width="215" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                    <text x="417" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🚪 PSD 비상통화 & 이격거리</text>
                    <text x="325" y="75" font-size="11" font-weight="bold" fill="#334155">• PSD 비상통화 1:1 연동 시험</text>
                    <text x="325" y="98" font-size="11" font-weight="bold" fill="#334155">• 이종 케이블 이격 ≥ 300mm</text>
                    <text x="275" y="162" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">5대 분야 인터페이스 회의록 및 시스템 통합 관리대장 완료</text>
                </svg>
            </div>
        </div>
    </div>
</div>
{common_js}
</body>
</html>
"""

# 3. CHECKLIST HTML (3-Column Premium Master Template)
chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전기 / 신호 / 기계 / PSD / 차량 인터페이스 협의 마스터 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; background-color: #f8fafc; }}
        .step-header {{ background-color: #ffffff; text-align: center; font-weight: 800; color: #1e3a8a; border-right: 1px solid #e2e8f0; }}
        .result-box {{ background-color: #ffffff; text-align: center; font-weight: 700; color: #2563eb; border-left: 1px solid #e2e8f0; }}
    </style>
</head>
<body class="p-6 sm:p-10 text-slate-800">
<div class="max-w-5xl mx-auto space-y-6">

    <!-- 대제목 & WBS 코드 -->
    <div class="flex justify-between items-end border-b-2 border-slate-900 pb-4">
        <div>
            <h1 class="text-3xl font-black text-slate-900 tracking-tight">전기 / 신호 / 기계 / PSD / 차량 인터페이스 협의 마스터 체크리스트</h1>
        </div>
        <div class="text-right">
            <span class="text-blue-600 font-bold text-sm">WBS Code 9000-2-4 | 통신 검측대장</span>
        </div>
    </div>

    <!-- 📋 상단 안내 상자 (Notice Box) -->
    <div class="bg-blue-50/80 border border-blue-200 rounded-2xl p-6 shadow-sm space-y-2">
        <h3 class="text-base font-bold text-blue-950 flex items-center gap-2">
            <span>📋</span> 전기 / 신호 / 기계 / PSD / 차량 인터페이스 협의 12대 정밀 검측대장
        </h3>
        <p class="text-xs text-blue-900 leading-relaxed font-medium">
            본 체크리스트는 엑셀 시방의 8대 현장조건 및 발주 검토 수칙을 12개 정밀 점검 항목으로 확장 구성하였으며, 모든 항목의 문장 끝은 예외 없이 질문형 어미(<strong class="text-blue-700">~하였는가?</strong>)로 100% 정형화되었습니다.
        </p>
    </div>

    <!-- 3-Column 마스터 검측 테이블 -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden">
        <table class="w-full border-collapse">
            <thead>
                <tr class="bg-slate-100 text-slate-700 text-sm font-extrabold border-b border-slate-200">
                    <th class="py-4 px-6 text-center w-48 border-r border-slate-200">시공 단계</th>
                    <th class="py-4 px-6 text-center">필수 검측 항목 (12대 정밀 검토 수칙)</th>
                    <th class="py-4 px-6 text-center w-36 border-l border-slate-200">점검 결과</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
                <!-- STEP 1 Group -->
                <tr class="hover:bg-slate-50 transition-colors">
                    <td rowspan="4" class="step-header p-6 w-48 align-middle bg-slate-50/50 border-r border-slate-200">
                        <div class="space-y-1">
                            <span class="text-amber-500 text-base">⚠️</span>
                            <div class="text-sm font-black text-slate-900">사전 준비</div>
                            <div class="text-xs text-blue-600 font-bold">(Step 1 도면&Pool)</div>
                        </div>
                    </td>
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">1. 시방 대조</span><strong class="text-slate-900">[소요전력]</strong> 전기(소요전력), 신호(공동관로), 차량(차상장치), PSD(비상통화) 연류 기준을 사전 조율<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                    <td rowspan="4" class="result-box p-6 w-36 align-middle bg-slate-50/30 text-blue-600 font-bold text-sm">☐ 확인완료</td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">2. 업체 Pool</span><strong class="text-slate-900">[적격 업체]</strong> 철도/트램 시공 및 영업운행 실적이 입증된 적격 업체 Pool을 검토<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">3. 제작 기간</span><strong class="text-slate-900">[자재 수급]</strong> 5대 분야 인터페이스 자재의 제작 및 현장 수급 기간을 계상<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">4. 유경험 인력</span><strong class="text-slate-900">[기술 인력]</strong> 철도/트램 유경험 전문 기술자 투입 계획을 확인<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>

                <!-- STEP 2 Group -->
                <tr class="hover:bg-slate-50 transition-colors border-t-2 border-slate-200">
                    <td rowspan="4" class="step-header p-6 w-48 align-middle bg-slate-50/50 border-r border-slate-200">
                        <div class="space-y-1">
                            <span class="text-blue-500 text-base">📋</span>
                            <div class="text-sm font-black text-slate-900">8대 조건</div>
                            <div class="text-xs text-blue-600 font-bold">(Step 2 예산 검증)</div>
                        </div>
                    </td>
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">5. 이격 거리</span><strong class="text-slate-900">[회로 분리]</strong> 이종 케이블 간 이격거리(≥300mm) 및 회로 분리를 확인하고 인터페이스 회의록을 작성<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                    <td rowspan="4" class="result-box p-6 w-36 align-middle bg-slate-50/30 text-blue-600 font-bold text-sm">☐ 확인완료</td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">6. 사용전검사</span><strong class="text-slate-900">[교육 지원비]</strong> 사용전검사 통신설비 운용 및 교육 지원 비용이 예산에 반영되었는지 확인<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">7. 내역 누락</span><strong class="text-slate-900">[내역서 재검토]</strong> 공사 예산내역서 상 누락 항목이 없는지 정밀 재검토<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">8. 창고 비용</span><strong class="text-slate-900">[창고 비용]</strong> 현장 자재 보관 창고 임대 비용을 내역서에 포함<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>

                <!-- STEP 3 Group -->
                <tr class="hover:bg-slate-50 transition-colors border-t-2 border-slate-200">
                    <td rowspan="4" class="step-header p-6 w-48 align-middle bg-slate-50/50 border-r border-slate-200">
                        <div class="space-y-1">
                            <span class="text-emerald-500 text-base">🤝</span>
                            <div class="text-sm font-black text-slate-900">마감 승인</div>
                            <div class="text-xs text-blue-600 font-bold">(Step 3 결과 체결)</div>
                        </div>
                    </td>
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">9. 유틸리티</span><strong class="text-slate-900">[공사용 시설]</strong> 공사용 전기, 용수, 오수 처리 시설 확보 계획을 수립<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                    <td rowspan="4" class="result-box p-6 w-36 align-middle bg-slate-50/30 text-blue-600 font-bold text-sm">☐ 확인완료</td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">10. 상주 인력</span><strong class="text-slate-900">[기술 지원비]</strong> 가동 후 현장 상주 기술지원 인력 기간 및 비용을 계상<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">11. 법정 일정</span><strong class="text-slate-900">[인허가 일정]</strong> 무선국 허가 및 사용전검사 준공 일정을 종합 반영<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-4 border-b border-slate-200 text-sm font-medium text-slate-800 leading-relaxed"><span class="inline-block bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-xs mr-2">12. 결과서 체결</span><strong class="text-slate-900">[소장 서명]</strong> 현장소장 결재가 포함된 인터페이스 회의록 결과서를 확정<strong class="text-blue-600 font-bold">하였는가?</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

</div>
</body>
</html>
"""

sub_dirs = {
    "표준서": std_html,
    "수행지침": gui_html,
    "체크리스트": chk_html
}

for s_n, content in sub_dirs.items():
    sp = os.path.join(target_folder, s_n)
    if os.path.exists(sp):
        for fn in os.listdir(sp):
            if fn.endswith('.html'):
                with open(os.path.join(sp, fn), 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                print(f"   ✓ [WBS 9000-2-4 OVERWRITE] {s_n} -> {fn}")

print("\n🎉 SUCCESSFULLY COMPLETED ULTRA-DETAILED ENHANCEMENT FOR WBS 9000-2-4!")
