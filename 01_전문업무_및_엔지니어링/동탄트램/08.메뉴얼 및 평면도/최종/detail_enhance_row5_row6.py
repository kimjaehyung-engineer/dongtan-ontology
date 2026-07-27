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

common_js = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 사업관리 기술 해설</h3>
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
    'team_building': {
        title: '👥 최고의 팀 만들기 (Best Team Building)',
        desc: '동탄트램 통신공사의 고품질 완공을 위해 정보통신기술사 및 숙련 기술자로 사업단을 구성하고, 협력사와 시공성 검토 및 수평적 자율 협업 체계를 구축하는 사업관리 절차입니다.'
    },
    'big_room': {
        title: '🏛️ Big Room 워크숍 (Integrated Big Room)',
        desc: '발주처, 감리단, 시공사 및 이종 공종(토목/건축/전기/신호/차량) 담당자가 한 공간에 모여 8대 인터페이스 및 Risk 레지스터를 실시간 상호 검증하는 통합 의사결정 워크숍입니다.'
    },
    'interface_matrix': {
        title: '🌐 8대 이종 공종 인터페이스 매트릭스',
        desc: '통신 기계실 슬리브, 트레이 간섭, 전차선 DC750V 유도장애, 궤도회로 신호 간섭, PSD 비상통화 및 차량 무선 장치 연동 항목을 상호 검증하는 표입니다.'
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

# -------------------------------------------------------------------------
# ROW 5 (Index 4): 4_최고의 팀 만들기 지원 (DETAILED ULTRA ENHANCEMENT)
# -------------------------------------------------------------------------
folder_row5 = None
for f in os.listdir(base_dir):
    if f.startswith("4_") or "최고의 팀" in f:
        folder_row5 = os.path.join(base_dir, f)
        break

if folder_row5:
    print(f"Enhancing Row 5 Folder: {folder_row5}")
    
    # 1. Standard HTML
    r5_std = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 최고의 팀 만들기 지원 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Standard</span>
        <h1 class="text-3xl font-black mt-2">최고의 팀 만들기 지원 표준서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-4 | 주관: 공무팀 / 통신기술단</p>
    </div>
    
    <div class="p-8 space-y-8">
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-blue-950 mb-2">🎯 표준 목적 (Objective)</h3>
            <p class="text-slate-700 text-sm font-medium leading-relaxed">
                동탄트램 사업의 원활한 수행을 위해 현장소장, 통신기술사, 감리단 및 전문 협력업체 간의 원팀(One-Team) 체계를 구축하고, 각 인원의 기술 자격 및 전문 역량을 검증하여 시공 무결성을 보장하는 것을 목적으로 함.
            </p>
        </div>

        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-blue-600 pb-2">📜 사업관리 및 팀 구성 디테일 시방 수칙 (Methodology)</h3>
            <ul class="space-y-3">
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 1</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>자격 요건 검증:</strong> 정보통신공사업법에 의거, 정보통신기술사 또는 고급 엔지니어 자격을 보유한 현장대리인을 지정하고, 철도/도시철도 통신망 시공 경력 5년 이상 숙련 기술자를 배치함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 2</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>R&R 매트릭스 확립:</strong> 발주처, 시공사, 협력사 간 업무 역할 및 책임(R&R) 매트릭스를 수립하여 인터페이스 업무 공백 및 중복 제출을 100% 사전 차단함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 3</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>실시간 소통 채널 구축:</strong> Big Room 협업 공간 및 디지털 커뮤니케이션 채널을 개설하여 시공 중 현장 이슈 및 변경사항을 실시간 공유하고 당일 의결 체계를 확립함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 4</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>협력사 상생 교육 지원:</strong> LTE-R 기술 규격 및 사용전검사 수칙에 대한 기술 공유 워크숍을 정기 개최하여 협력사의 품질 관리 역량을 평준화함.</span>
                </li>
            </ul>
        </div>

        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-emerald-950 mb-2">📦 증빙 산출물 (Deliverables)</h3>
            <p class="text-emerald-900 text-sm font-bold">최고의 팀 구성 명단, R&R 매트릭스 의결서, 기술역량 검증 보고서, 팀 빌딩 워크숍 결과록</p>
        </div>
    </div>
</div>
</body>
</html>
"""

    # 2. Guideline HTML
    r5_gui = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 최고의 팀 만들기 지원 수행지침서</title>
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
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Guideline</span>
        <h1 class="text-3xl font-black mt-2">최고의 팀 만들기 지원 유연 4단계 수행지침서</h1>
        <p class="text-blue-200 text-sm mt-1">"원팀(One-Team) 체계 구축 & 자격 검증 4단계 2D Visual 마스터 지침"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 친절한 개념 해설 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-sm text-blue-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 최고의 팀 만들기 지원 실무 해설</h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                동탄트램 사업의 성공은 기술 인력의 직무 신뢰성에서 시작됩니다. 본 수행지침서는 <strong><span class="term-highlight" onclick="openGlossary('team_building')">최고의 팀 만들기(Best Team Building)</span></strong> 원칙에 입각하여 기술인력 자격 검증부터 R&R 확립, 협력사 교육 지원까지 <strong>유연 4단계(4-Step) 마스터 프로세스</strong>로 가이드합니다.
            </p>
        </div>

        <!-- ☀️ 라이트 테마 특화 카드 섹션 -->
        <div class="bg-blue-50/70 border border-blue-200 p-7 rounded-2xl shadow-md space-y-6">
            <div class="border-b border-blue-200 pb-4">
                <span class="bg-blue-600 text-white text-xs font-black px-3 py-1 rounded-full uppercase">SPECIAL FOCUS</span>
                <h3 class="text-xl font-black text-blue-950 mt-2">📋 최고의 팀 수립 4대 핵심 가이드</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>👨‍💻</span> 1. 전문 기술자격 인력 배치</span>
                    <p class="text-slate-700 text-xs">정보통신기술사 및 철도 통신 5년 이상 경력자를 선별 배치하여 기술 품질 확보.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>📊</span> 2. R&R 업무 분장 명확화</span>
                    <p class="text-slate-700 text-xs">발주처-감리단-시공사-협력사 간 R&R 매트릭스를 의결하여 책임 소재 명확화.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🗣️</span> 3. Big Room 실시간 협업</span>
                    <p class="text-slate-700 text-xs">현장 Big Room 전용 공간에서 당일 미결사항 해결 및 소통 활성화.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🎓</span> 4. 상생 기술 워크숍 개최</span>
                    <p class="text-slate-700 text-xs">협력사 기술 역량 강화를 위한 정기 기술 세미나 및 안전 워크숍 진행.</p>
                </div>
            </div>
        </div>

        <!-- 1. FLEXIBLE 4-STEP ARCHITECTURE -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 4단계 수행 마스터 프로세스 (Flexible 4-Step Architecture)
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between">
                    <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 1</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">자격 검증 & 인력 선별</h4>
                    <p class="text-[11px] text-blue-900 mt-1 font-medium">• 통신기술사/고급엔지니어<br">• 철도 경력 5년 이상 확인</p>
                </div>
                <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <span class="bg-indigo-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">R&R 매트릭스 확립</h4>
                    <p class="text-[11px] text-indigo-900 mt-1 font-medium">• 4자 간 역할 분장<br">• 책임 소재 일치</p>
                </div>
                <div class="bg-cyan-50 p-4 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <span class="bg-cyan-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">Big Room 협업 개설</h4>
                    <p class="text-[11px] text-cyan-900 mt-1 font-medium">• 온/오프라인 소통 채널<br">• 당일 미결사항 해결</p>
                </div>
                <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded w-fit">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-xs mt-2">기술 워크숍 & 평가</h4>
                    <p class="text-[11px] text-emerald-900 mt-1 font-medium">• 협력사 상생 교육<br">• 최종 역량 보고서 체결</p>
                </div>
            </div>
        </div>

        <!-- 2. 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 2D Visual 기술 도식 (Enriched 2D SVG)
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_r5', '[Row 5] 최고의 팀 만들기 조직 체계 2D visual 도식')">
                <svg id="svg_r5" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                    <rect x="30" y="20" width="220" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
                    <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">👨‍💻 통신기술단 & 현장대리인</text>
                    <text x="50" y="75" font-size="11" font-weight="bold" fill="#334155">• 정보통신기술사/고급 자격</text>
                    <text x="50" y="98" font-size="11" font-weight="bold" fill="#334155">• 철도 통신 경력 5년 이상</text>

                    <path d="M 260 80 L 290 80" stroke="#2563eb" stroke-width="3"/>
                    <polygon points="290,75 300,80 290,85" fill="#2563eb"/>

                    <rect x="305" y="20" width="215" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
                    <text x="412" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🤝 원팀(One-Team) R&R 체결</text>
                    <text x="325" y="75" font-size="11" font-weight="bold" fill="#334155">• 발주/감리/시공/협력사 통합</text>
                    <text x="325" y="98" font-size="11" font-weight="bold" fill="#334155">• Big Room 실시간 의결 완성</text>
                    <text x="275" y="162" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">최고의 팀 수립을 통한 동탄트램 완벽 시공 품질 달성</text>
                </svg>
            </div>
        </div>
    </div>
</div>
{common_js}
</body>
</html>
"""

    # 3. Checklist HTML
    r5_chk = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 최고의 팀 만들기 지원 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Checklist</span>
        <h1 class="text-3xl font-black mt-2">최고의 팀 만들기 지원 체크리스트</h1>
        <p class="text-emerald-200 text-sm mt-1">L4 Code: 9000-2-4 | 주관: 공무팀 / 통신기술단</p>
    </div>
    
    <div class="p-8 space-y-6">
        <div class="bg-slate-100 p-4 rounded-xl border border-slate-300 flex justify-between items-center text-xs font-bold">
            <span>공종: 통신분야</span>
            <span>작업단위: 최고의 팀 만들기 지원</span>
            <span>산출물: R&R 매트릭스 의결서 및 기술인력 보고서</span>
        </div>

        <table class="w-full border-collapse border border-slate-300 text-sm text-left">
            <thead>
                <tr class="bg-slate-800 text-white text-xs">
                    <th class="border border-slate-300 p-3 text-center w-12">NO</th>
                    <th class="border border-slate-300 p-3 text-center">검측 및 점검 항목 statement (질문형 종결어미)</th>
                    <th class="border border-slate-300 p-3 text-center w-20">판정</th>
                </tr>
            </thead>
            <tbody>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">1</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 정보통신공사업법에 따른 기술자 자격증 및 경력증명서를 검증하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">2</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 철도/도시철도 통신망 시공 경력 5년 이상 엔지니어 현장 배치를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">3</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 발주처-감리단-시공사-협력사 4자 간 R&R 매트릭스를 서명 작성하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">4</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• Big Room 협업 공간 내 통신 전용 의결 좌석 및 장비를 확보하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">5</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 디지털 협업 소통 채널 구축 및 담당자 등록을 완료하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">6</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 협력사 대상 기술 공유 상생 워크숍 계획을 수립하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">7</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 이종 공종 간 인터페이스 담당자 1:1 매칭 조율을 완료하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">8</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 팀 성과 평가지표(KPI) 수립 및 주간 점검 체계를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">9</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 현장 안전 관리 요원과 통신 기술 요원 간 합동 안전 점검을 시행하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">10</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 비상 상황 발생 시 실시간 연락망 최신화 여부를 점검하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">11</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 입찰안내서 요구조건과의 팀 역량 일치 여부를 재검토하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">12</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 최종 최고의 팀 구성 결과서에 현장소장 및 감리원 서명을 체결하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
"""

    sub_dirs = {
        "표준서": r5_std,
        "수행지침": r5_gui,
        "체크리스트": r5_chk
    }
    for s_n, content in sub_dirs.items():
        sp = os.path.join(folder_row5, s_n)
        if os.path.exists(sp):
            for fn in os.listdir(sp):
                if fn.endswith('.html'):
                    with open(os.path.join(sp, fn), 'w', encoding='utf-8') as f_out:
                        f_out.write(content)
                    print(f"   ✓ [ROW 5 OVERWRITE] {s_n} -> {fn}")


# -------------------------------------------------------------------------
# ROW 6 (Index 5): 5_착수전 Big Room 회의 (DETAILED ULTRA ENHANCEMENT)
# -------------------------------------------------------------------------
folder_row6 = None
for f in os.listdir(base_dir):
    if f.startswith("5_") or "Big Room" in f:
        folder_row6 = os.path.join(base_dir, f)
        break

if folder_row6:
    print(f"Enhancing Row 6 Folder: {folder_row6}")

    # 1. Standard HTML
    r6_std = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 착수전 Big Room 회의 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Standard</span>
        <h1 class="text-3xl font-black mt-2">착수전 Big Room 회의 표준서</h1>
        <p class="text-blue-200 text-sm mt-1">L4 Code: 9000-2-5 | 주관: 공무팀 / 사업관리단</p>
    </div>
    
    <div class="p-8 space-y-8">
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-blue-950 mb-2">🎯 표준 목적 (Objective)</h3>
            <p class="text-slate-700 text-sm font-medium leading-relaxed">
                통신공사 본격 착수 전, 발주처, 감리단, 통신시공사 및 이종 타 공종(토목/건축/전기/신호/차량) 책임자가 한 공간에 모여 8대 인터페이스 간섭, CPM 전체 공정표 및 Risk 레지스터를 통합 대조 의결하는 것을 목적으로 함.
            </p>
        </div>

        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-blue-600 pb-2">📜 Big Room 회의 디테일 시방 수칙 (Methodology)</h3>
            <ul class="space-y-3">
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 1</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>통합 의사결정 참석자 구성:</strong> 사업총괄, 통신/신호/전기/건축/토목 분야 책임자 및 감리원이 100% 필수 참석하는 통합 워크숍으로 개최함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 2</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>8대 인터페이스 정밀 대조:</strong> 건축 슬리브/관로 위치, 전기 DC750V 특고압 접지 유도장애, 궤도 신호회로 간섭 및 PSD 비상통화 연동 8대 항목을 도면 1:1 대조함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 3</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>Risk Register 매핑:</strong> 공정 지연 및 기술 마찰 위험 항목을 Risk 매트릭스에 등록하고 당일 의결 해결책 및 전담 조치자를 지정함.</span>
                </li>
                <li class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-start gap-3">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded mt-0.5">수칙 4</span>
                    <span class="text-slate-800 text-sm font-medium leading-relaxed"><strong>Big Room 회의록 서명 체결:</strong> 회의 결과 도출된 종합 공정표 및 인터페이스 조율안에 현장소장 및 각 분야 책임자 3자 서명을 완료함.</span>
                </li>
            </ul>
        </div>

        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-xl">
            <h3 class="text-base font-bold text-emerald-950 mb-2">📦 증빙 산출물 (Deliverables)</h3>
            <p class="text-emerald-900 text-sm font-bold">Big Room 회의록, Risk Register 매트릭스, 8대 인터페이스 조율서, 서명 체결 승인서</p>
        </div>
    </div>
</div>
</body>
</html>
"""

    # 2. Guideline HTML
    r6_gui = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 착수전 Big Room 회의 수행지침서</title>
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
        <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Guideline</span>
        <h1 class="text-3xl font-black mt-2">착수전 Big Room 회의 유연 5단계 수행지침서</h1>
        <p class="text-blue-200 text-sm mt-1">"8대 인터페이스 & Risk Register 실시간 의결 5단계 2D Visual 마스터 지침"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 친절한 개념 해설 박스 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl text-sm text-blue-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 착수전 Big Room 회의 실무 해설</h4>
            <p class="bg-white p-4 rounded-xl border border-blue-300 font-medium text-slate-900 leading-relaxed">
                시공 장애를 사전에 막는 가장 강력한 도구는 현장 상호 대면 검증입니다. 본 수행지침서는 <strong><span class="term-highlight" onclick="openGlossary('big_room')">Big Room 워크숍(Integrated Big Room)</span></strong>을 통해 <strong><span class="term-highlight" onclick="openGlossary('interface_matrix')">8대 이종 공종 인터페이스</span></strong>와 Risk를 조율하는 <strong>유연 5단계(5-Step) 마스터 프로세스</strong>로 가이드합니다.
            </p>
        </div>

        <!-- ☀️ 라이트 테마 특화 카드 섹션 -->
        <div class="bg-blue-50/70 border border-blue-200 p-7 rounded-2xl shadow-md space-y-6">
            <div class="border-b border-blue-200 pb-4">
                <span class="bg-blue-600 text-white text-xs font-black px-3 py-1 rounded-full uppercase">SPECIAL FOCUS</span>
                <h3 class="text-xl font-black text-blue-950 mt-2">📋 Big Room 워크숍 5대 실행 포인트</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>🏛️</span> 1. 전 분야 책임자 참석</span>
                    <p class="text-slate-700 text-xs">통신, 신호, 전기, 건축, 토목 및 감리단 전원 대면 참석.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>📐</span> 2. 도면 1:1 인터페이스 검증</span>
                    <p class="text-slate-700 text-xs">건축 슬리브, 트레이 관로, DC750V 접지 유도장애 물리적 검증.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>⚠️</span> 3. Risk Register 실시간 등록</span>
                    <p class="text-slate-700 text-xs">공정 지연 및 시공 간섭 Risk 등록 후 당일 조치자 지정.</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <span class="font-bold text-blue-700 flex items-center gap-2"><span>📝</span> 4. 3자 서명 의결록 확정</span>
                    <p class="text-slate-700 text-xs">발주처-감리단-시공사 3자 서명 완료로 법적 무결성 확보.</p>
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
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">참석자 소집</h4>
                    <p class="text-[10px] text-blue-900 mt-1 font-medium">• 5대 분야 전원<br">• 도서 준비</p>
                </div>
                <div class="bg-indigo-50 p-3 rounded-xl border border-indigo-200 flex flex-col justify-between">
                    <span class="bg-indigo-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 2</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">인터페이스 토론</h4>
                    <p class="text-[10px] text-indigo-900 mt-1 font-medium">• 8대 항목 대조<br">• 간섭 선제 발굴</p>
                </div>
                <div class="bg-cyan-50 p-3 rounded-xl border border-cyan-200 flex flex-col justify-between">
                    <span class="bg-cyan-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 3</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">Risk 등록</h4>
                    <p class="text-[10px] text-cyan-900 mt-1 font-medium">• Risk Register<br">• 조치자 당일 지정</p>
                </div>
                <div class="bg-teal-50 p-3 rounded-xl border border-teal-200 flex flex-col justify-between">
                    <span class="bg-teal-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 4</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">공정표 통합</h4>
                    <p class="text-[10px] text-teal-900 mt-1 font-medium">• CPM 공정 일치<br">• 수급 일정 확정</p>
                </div>
                <div class="bg-emerald-50 p-3 rounded-xl border border-emerald-200 flex flex-col justify-between">
                    <span class="bg-emerald-600 text-white text-[9px] font-black px-1.5 py-0.5 rounded w-fit">STEP 5</span>
                    <h4 class="font-bold text-slate-900 text-[11px] mt-1">3자 체결</h4>
                    <p class="text-[10px] text-emerald-900 mt-1 font-medium">• 회의록 최종 체결<br">• 사업관리 시스템 보고</p>
                </div>
            </div>
        </div>

        <!-- 2. 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 2D Visual 기술 도식 (Enriched 2D SVG)
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_r6', '[Row 6] Big Room 워크숍 레이아웃 2D visual 도식')">
                <svg id="svg_r6" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
                    <rect x="30" y="20" width="490" height="120" fill="#ffffff" stroke="#4f46e5" stroke-width="2" rx="8"/>
                    <rect x="30" y="20" width="490" height="28" fill="#e0e7ff" rx="8"/>
                    <text x="275" y="39" font-size="12" font-weight="black" fill="#3730a3" text-anchor="middle">🏛️ 동탄트램 착수전 Big Room 통합 의사결정 회의실</text>

                    <rect x="50" y="60" width="130" height="65" fill="#f1f5f9" stroke="#6366f1" stroke-width="1.5" rx="6"/>
                    <text x="115" y="85" font-size="11" font-weight="black" fill="#4338ca" text-anchor="middle">📡 통신 / 신호 분야</text>
                    <text x="115" y="105" font-size="10" font-weight="bold" fill="#334155">LTE-R / 이중화 광망</text>

                    <rect x="210" y="60" width="130" height="65" fill="#f1f5f9" stroke="#0284c7" stroke-width="1.5" rx="6"/>
                    <text x="275" y="85" font-size="11" font-weight="black" fill="#0369a1" text-anchor="middle">🏗️ 토목 / 건축 / 전기</text>
                    <text x="275" y="105" font-size="10" font-weight="bold" fill="#334155">슬리브 / DC750V 접지</text>

                    <rect x="370" y="60" width="130" height="65" fill="#f1f5f9" stroke="#059669" stroke-width="1.5" rx="6"/>
                    <text x="435" y="85" font-size="11" font-weight="black" fill="#047857" text-anchor="middle">🤝 감리단 / 발주처</text>
                    <text x="435" y="105" font-size="10" font-weight="bold" fill="#334155">3자 서명 승인 체결</text>

                    <text x="275" y="162" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">Big Room 대면 검증을 통한 시공 Risk 및 8대 인터페이스 당일 해결</text>
                </svg>
            </div>
        </div>
    </div>
</div>
{common_js}
</body>
</html>
"""

    # 3. Checklist HTML
    r6_chk = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 통신분야 - 착수전 Big Room 회의 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8">
        <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Dongtan Tram Checklist</span>
        <h1 class="text-3xl font-black mt-2">착수전 Big Room 회의 체크리스트</h1>
        <p class="text-emerald-200 text-sm mt-1">L4 Code: 9000-2-5 | 주관: 공무팀 / 사업관리단</p>
    </div>
    
    <div class="p-8 space-y-6">
        <div class="bg-slate-100 p-4 rounded-xl border border-slate-300 flex justify-between items-center text-xs font-bold">
            <span>공종: 통신분야</span>
            <span>작업단위: 착수전 Big Room 회의</span>
            <span>산출물: Big Room 회의록 및 8대 인터페이스 조율서</span>
        </div>

        <table class="w-full border-collapse border border-slate-300 text-sm text-left">
            <thead>
                <tr class="bg-slate-800 text-white text-xs">
                    <th class="border border-slate-300 p-3 text-center w-12">NO</th>
                    <th class="border border-slate-300 p-3 text-center">검측 및 점검 항목 statement (질문형 종결어미)</th>
                    <th class="border border-slate-300 p-3 text-center w-20">판정</th>
                </tr>
            </thead>
            <tbody>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">1</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 발주처-감리단-시공사-타 공종 책임자의 100% 대면 참석 여부를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">2</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 건축 통신기계실 슬리브 및 케이블 관로 유무를 도면 1:1 대조하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">3</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 전기 DC750V 특고압 급전선의 통신 케이블 간섭 여부를 점검하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">4</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 신호 궤도회로 무선 간섭 및 축차계수기 연동 위치를 검측하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">5</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• PSD 승강장 스크린도어 비상통화 및 PIS 안내방송 인터페이스를 조율하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">6</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• Risk Register 매트릭스에 시공 간섭 항목을 등록하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">7</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• Risk 조치 담당자를 당일 회의에서 즉시 지정하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">8</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• CPM 마스터 공정표상 통신 자재 반입 및 포설 일정을 검증하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">9</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 현장 자재창고 및 공사용 전기/용수 유틸리티 지원 여부를 확인하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">10</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• LTE-R 무선국 허가 및 정보통신사용전검사 준공 일정을 조율하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">11</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• 입찰안내서 요구조건과의 Big Room 회의 결과 일치 여부를 재검토하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
                <tr class="hover:bg-slate-50">
                    <td class="border border-slate-300 p-3 text-center font-bold">12</td>
                    <td class="border border-slate-300 p-3 font-medium text-slate-900">• Big Room 최종 의결록에 현장소장, 감리원 및 타 공종 책임자 서명을 체결하였는가?</td>
                    <td class="border border-slate-300 p-3 text-center font-bold text-emerald-600">☐ 적합</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
"""

    sub_dirs = {
        "표준서": r6_std,
        "수행지침": r6_gui,
        "체크리스트": r6_chk
    }
    for s_n, content in sub_dirs.items():
        sp = os.path.join(folder_row6, s_n)
        if os.path.exists(sp):
            for fn in os.listdir(sp):
                if fn.endswith('.html'):
                    with open(os.path.join(sp, fn), 'w', encoding='utf-8') as f_out:
                        f_out.write(content)
                    print(f"   ✓ [ROW 6 OVERWRITE] {s_n} -> {fn}")

print("\n🎉 SUCCESSFULLY COMPLETED ULTRA-DETAILED ENHANCEMENT FOR ROW 5 AND ROW 6!")
