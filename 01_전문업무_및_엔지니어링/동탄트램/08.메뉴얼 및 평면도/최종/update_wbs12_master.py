import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Target absolute paths for WBS 12 (자재 반입)
target_base = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\12_자재 반입"

path_standard = os.path.join(target_base, "표준서", "자재 반입_표준서.html")
path_standard_alt = os.path.join(target_base, "표준서", "12_자재 반입_표준서.html")
path_guideline = os.path.join(target_base, "수행지침", "자재 반입_수행지침.html")
path_checklist = os.path.join(target_base, "체크리스트", "자재 반입_체크리스트.html")
path_checklist_alt = os.path.join(target_base, "체크리스트", "12_자재 반입_체크리스트.html")

os.makedirs(os.path.dirname(path_standard), exist_ok=True)
os.makedirs(os.path.dirname(path_guideline), exist_ok=True)
os.makedirs(os.path.dirname(path_checklist), exist_ok=True)

def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Written Master WBS 12: {path}")

# Minimal Glossary Style & Enhanced Popup HTML
minimal_glossary_style = """
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
    .glossary-modal {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(4px);
        align-items: center;
        justify-content: center;
    }
    .glossary-modal.active {
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
    .glossary-close {
        color: #94a3b8;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }
"""

common_modal_html = """
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 자재검측 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<script>
const glossaryData = {
    'resin_fill': {
        title: '🧪 레일고정 액상수지 (Elastic Resin Fill)',
        desc: '일반 콘크리트가 아닙니다! 트램 홈레일(51R1) 측면 틈새에 액체 상태로 채워 넣어 탄성 고무로 경화시키는 2액형 유연 수지입니다.\\n1) 진동·소음 흡수: 도심지 트램 진동 차단\\n2) 누설전류(Stray Current) 절연: 지중 매설관 부식 방지\\n3) 수밀 고정: 빗물 침투 차단 및 레일 고정'
    },
    'special_turnout': {
        title: '🔀 외산 특수 분기기 (Special Foreign Turnout)',
        desc: '트램 차선 전환을 위한 전량 해외 수입 특수 분기기입니다. 콘크리트도상 반입 60일 전 해외 공장에서 3D 치수 및 작동 성능 검수를 마치고 국내 전용 컨테이너로 반입됩니다.'
    },
    'grooved_rail': {
        title: '🛤️ 그루브드레일 (Grooved Rail, 51R1/60R2)',
        desc: '도로 매설형 트램 선로에 사용되는 홈이 파인 특수 레일입니다. 전량 해외 수입 자재로, 콘크리트도상 시공 60일 전 공장 성적서(Mill Sheet) 검수 및 운반 조달 계획을 감리단과 의결해야 합니다.'
    },
    'pst_panel': {
        title: '🧱 PST 프리캐스트 슬래브 패널',
        desc: '공장에서 사전 제작되어 현장 반입되는 궤도용 콘크리트 슬래브 구조체입니다. 현장 반입 시 패널 치수 오차(±2.0mm 이내) 및 균열 흠집 여부를 정밀 계측하여 불량 시 즉시 반출합니다.'
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
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('glossaryModal');
        if(modal) modal.classList.remove('active');
    }
});
</script>
"""

# =========================================================================
# 1. WBS 12 STANDARD HTML (자재 반입 기술 표준서 - 액상수지 & 특수분기기 정밀 반영)
# =========================================================================
standard_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 반입 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {minimal_glossary_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-12 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">액상수지 & 외산 특수분기기 정밀 품질</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 반입 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"콘크리트 자재 오해 방지: 레일고정 액상수지(탄성체), 외산 특수분기기 60일 전 공장검수 및 PST 패널 허용공차(±2mm) 관리"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 💡 오해 방지 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs sm:text-sm text-amber-900">
            <h4 class="font-bold text-amber-950 mb-1">💡 "콘크리트도상 자재 반입" 개념 정립</h4>
            <p class="leading-relaxed">
                본 공종의 자재는 일반 믹서트럭 콘크리트가 아닙니다! 트램 도로 매설 선로를 구성하는 <strong><span class="term-highlight" onclick="openGlossary('resin_fill')">레일고정 액상수지(탄성 절연재)</span>, <span class="term-highlight" onclick="openGlossary('special_turnout')">외산 특수 분기기</span>, <span class="term-highlight" onclick="openGlossary('grooved_rail')">그루브드레일(51R1/60R2)</span>, <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 프리캐스트 슬래브 패널</span>, 탄성 체결장치</strong> 등 핵심 매설 궤도 자재의 인수검사 및 현장 관리를 뜻합니다.
            </p>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 자재 반입 (공사팀/자재팀/품질팀)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">자재인수검사 대장 | 공장시험성적서(Mill Sheet) | 불량재 반출서</p>
                </div>
            </div>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 핵심 주요 자재별 정량 기술 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">자재 구획</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 관리 기술 표준 (KCS 시방 연동)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">레일고정 액상수지<br>(Pourable Resin Fill)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">보관온도 15~25℃<br>절연저항 &ge; 10 M&Omega;</td>
                            <td class="p-3 border text-slate-600">• 주제:경화제 전용 비율 교반 후 2~4시간 내 고탄성 고무 경화.<br>• 트램 진동/소음 차단 및 누설전류(Stray Current) 지중 매설관 부식 방지 이중 절연성 확보</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">외산 특수 분기기<br>(Special Turnout)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">반입 60일 전 공장검수</td>
                            <td class="p-3 border text-slate-600">• 해외 전문 제조사(Vossloh 등) 조립 3D 치수 검수 완료 후 반입.<br>• 선로 전환기 인터페이스 및 부품 번호(Lot No.) 100% 대조</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">그루브드레일 (51R1/60R2)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">직선도 1m당 &plusmn;0.2mm</td>
                            <td class="p-3 border text-slate-600">• 외산 매설 홈레일 현장 하차 시 레일 표면 흠집/균열 전수 점검.<br>• 공장 시험성적서(Mill Sheet) 원본 대조 및 감리 임회 검측</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">PST 슬래브 패널</td>
                            <td class="p-3 border text-center font-bold text-red-600">치수 공차 &plusmn;2.0mm 이내</td>
                            <td class="p-3 border text-slate-600">• 현장 반입 시 버니어 캘리퍼스로 패널 폭, 길이, 대각선 측정.<br>• 허용 공차 초과 및 모서리 휨/손상 자재는 현장 즉시 반출</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# =========================================================================
# 2. WBS 12 GUIDELINE HTML (자재 반입 수행지침서 - 액상수지 주입/경화 시뮬레이터 수록)
# =========================================================================
guideline_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 반입 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        {minimal_glossary_style}
        .sim-step-btn {{
            transition: all 0.25s ease;
        }}
        .sim-step-btn.active {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.12);
        }}
        .sim-btn {{
            transition: all 0.2s ease;
        }}
        .sim-btn:hover {{
            transform: translateY(-1px);
        }}
        .img-card {{
            transition: all 0.3s ease;
        }}
        .img-card:hover {{
            transform: scale(1.02);
            box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.15);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-12 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">현장 시각 자료 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 반입 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"레일고정 액상수지 시공/관리 & 외산 특수분기기 인수검사 실사 가이드"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 1. 작업 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 처음 업무를 맡은 직원도 레일고정 액상수지의 진동흡수/절연 역할, 반입 보관(15~25℃), 현장 액상 주입 수행 단계 및 PST 패널 치수 측량을 완벽하게 이해함</p>
                <p><strong>⚙️ 협업 부서:</strong> 현장 공사팀, 자재팀, 품질팀 및 감리단 입회 검측</p>
            </div>
        </div>

        <!-- [마스터 시뮬레이터] 5대 자재 반입 마스터 시퀀스 단계별 시뮬레이터 -->
        <div class="bg-white text-slate-900 p-6 sm:p-8 rounded-2xl shadow-xl border border-slate-200">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-bold text-emerald-700 uppercase tracking-widest">Interactive Material Receiving Flow</span>
                    <h2 class="text-2xl font-black tracking-tight text-slate-900 mt-0.5">★ 콘크리트도상 자재 반입 5대 마스터 인터랙티브 시뮬레이터</h2>
                </div>
                <button id="autoPlayBtn" onclick="toggleAutoPlay()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl flex items-center gap-2 border border-emerald-600 transition-all shadow-sm">
                    <span id="playIcon">▶</span> <span id="playText">자동 시뮬레이션 재생</span>
                </button>
            </div>

            <!-- 5단계 탭 버튼 -->
            <div class="grid grid-cols-5 gap-2 mb-6">
                <button id="stepBtn1" onclick="setStep(1)" class="sim-step-btn active bg-amber-500 text-white p-3 rounded-xl border border-amber-600 text-left transition-all">
                    <div class="text-[10px] opacity-90 font-bold">1단계</div>
                    <div class="text-xs font-black truncate">사전 공장검수</div>
                </button>
                <button id="stepBtn2" onclick="setStep(2)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">2단계</div>
                    <div class="text-xs font-black truncate">25Ton 장축수송</div>
                </button>
                <button id="stepBtn3" onclick="setStep(3)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">3단계</div>
                    <div class="text-xs font-black truncate">인수검사·치수</div>
                </button>
                <button id="stepBtn4" onclick="setStep(4)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">4단계</div>
                    <div class="text-xs font-black truncate">액상수지·마킹</div>
                </button>
                <button id="stepBtn5" onclick="setStep(5)" class="sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200">
                    <div class="text-[10px] opacity-70 font-bold">5단계</div>
                    <div class="text-xs font-black truncate">불량재 반출</div>
                </button>
            </div>

            <!-- 시뮬레이션 SVG 캔버스 -->
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-300 relative overflow-hidden shadow-inner">
                <div style="height: 280px;" class="w-full relative">
                    <svg id="masterSeqSvg" viewBox="0 0 700 280" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0" y="0" width="700" height="280" fill="#f8fafc"/>
                        <rect x="0" y="210" width="700" height="70" fill="#475569"/>
                        <line x1="0" y1="210" x2="700" y2="210" stroke="#334155" stroke-width="3"/>
                        <text x="20" y="245" font-size="11" font-weight="black" fill="#ffffff" opacity="0.9">현장 자재 하차 야드 & 도로 수송구역</text>
                        
                        <!-- 1단계: 해외 공장검수 서류 & 60일전 승인 (Step 1) -->
                        <g id="seqGroupStep1" opacity="1" class="transition-all duration-500">
                            <rect x="250" y="40" width="200" height="130" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="2.5"/>
                            <path d="M 280 70 L 420 70 M 280 95 L 390 95 M 280 120 L 410 120" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
                            <circle cx="410" cy="130" r="18" fill="#d97706"/>
                            <text x="410" y="135" text-anchor="middle" font-size="11" font-weight="black" fill="#ffffff">PASS</text>
                            <text x="350" y="190" text-anchor="middle" font-size="11" font-weight="black" fill="#b45309">외산 특수분기기/홈레일 60일 전 공장검수 승인</text>
                        </g>

                        <!-- 2단계: 25Ton 장축 트레일러 수송 (Step 2) -->
                        <g id="seqGroupStep2" opacity="0" class="transition-all duration-500">
                            <rect x="150" y="150" width="220" height="40" fill="#0284c7" rx="3"/>
                            <rect x="370" y="130" width="70" height="60" fill="#0369a1" rx="5"/>
                            <circle cx="190" cy="195" r="12" fill="#1e293b"/>
                            <circle cx="320" cy="195" r="12" fill="#1e293b"/>
                            <circle cx="410" cy="195" r="12" fill="#1e293b"/>
                            <rect x="160" y="142" width="200" height="8" fill="#94a3b8" stroke="#334155"/>
                            <circle cx="420" cy="115" r="8" fill="#ef4444"/>
                            <text x="300" y="100" text-anchor="middle" font-size="11" font-weight="black" fill="#0284c7">25Ton 장축 트레일러 야간 도로점용 통제 수송 중</text>
                        </g>

                        <!-- 3단계: 버니어 캘리퍼스 PST 패널 치수 오차(±2mm) 정밀 검측 (Step 3) -->
                        <g id="seqGroupStep3" opacity="0" class="transition-all duration-500">
                            <rect x="200" y="130" width="300" height="65" fill="#cbd5e1" stroke="#475569" stroke-width="2" rx="3"/>
                            <text x="350" y="168" text-anchor="middle" font-size="12" font-weight="black" fill="#1e293b">PST 슬래브 패널 (치수 허용공차 ±2.0mm 이내)</text>
                            <line x1="200" y1="110" x2="500" y2="110" stroke="#059669" stroke-width="2.5" stroke-dasharray="4,2"/>
                            <polygon points="200,110 208,105 208,115" fill="#059669"/>
                            <polygon points="500,110 492,105 492,115" fill="#059669"/>
                            <text x="350" y="98" text-anchor="middle" font-size="11" font-weight="black" fill="#059669">감리 입회 버니어 캘리퍼스 정밀 측정: 0.0mm 오차 합격</text>
                        </g>

                        <!-- 4단계: 레일고정 액상수지 드럼 보관 & Lot 마킹 (Step 4) -->
                        <g id="seqGroupStep4" opacity="0" class="transition-all duration-500">
                            <rect x="180" y="120" width="50" height="80" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
                            <rect x="240" y="120" width="50" height="80" rx="6" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
                            <rect x="300" y="120" width="50" height="80" rx="6" fill="#0369a1" stroke="#1e3a8a" stroke-width="2"/>
                            <text x="205" y="165" font-size="9" font-weight="black" fill="#ffffff">주제 A</text>
                            <text x="265" y="165" font-size="9" font-weight="black" fill="#ffffff">주제 A</text>
                            <text x="325" y="165" font-size="9" font-weight="black" fill="#ffffff">경화 B</text>
                            <rect x="370" y="150" width="180" height="50" fill="#64748b" rx="3"/>
                            <text x="460" y="180" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">외산 특수분기기 정렬 적재</text>
                            <text x="350" y="90" text-anchor="middle" font-size="11" font-weight="black" fill="#d97706">액상수지 상온(15~25℃) 전용 차광 야드 보관 & Lot 번호 관리</text>
                        </g>

                        <!-- 5단계: 불량 자재 현장 전량 반출 (Step 5) -->
                        <g id="seqGroupStep5" opacity="0" class="transition-all duration-500">
                            <rect x="350" y="150" width="180" height="40" fill="#dc2626" rx="3"/>
                            <rect x="290" y="130" width="60" height="60" fill="#b91c1c" rx="5"/>
                            <circle cx="320" cy="195" r="12" fill="#1e293b"/>
                            <circle cx="480" cy="195" r="12" fill="#1e293b"/>
                            <path d="M 400 135 L 440 175 M 440 135 L 400 175" stroke="#ffffff" stroke-width="4"/>
                            <text x="350" y="85" text-anchor="middle" font-size="12" font-weight="black" fill="#dc2626">🚫 변형/손상 불량 자재 현장 즉시 전량 반출 조치 완료!</text>
                        </g>
                    </svg>
                </div>
                
                <div class="mt-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div id="seqBadge" class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">
                        STEP 1
                    </div>
                    <div>
                        <h3 id="seqTitle" class="text-base font-bold text-slate-900 mb-1">1단계: 사전 공장검수 & 60일 전 승인</h3>
                        <p id="seqDesc" class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            해외 수입 자재인 그루브드레일(51R1/60R2), 역상수지, 특수 분기기는 시공 60일 전 공장성적서(Mill Sheet) 검수 및 자재 조달 계획을 감리단과 최종 의결합니다.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 세부 절차 (5단계 세부 수행 프로세스) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 자재 반입 5단계 세부 수행 프로세스
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-amber-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-amber-100 text-amber-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 외산 자재 사전 공장검수</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">시공 60일 전 공장성적서(Mill Sheet) 검토 및 자재조달 승인</h3>
                    <p class="text-slate-600 text-xs sm:text-sm">
                        <span class="term-highlight" onclick="openGlossary('grooved_rail')">그루브드레일(51R1/60R2)</span>, <span class="term-highlight" onclick="openGlossary('resin_fill')">역상수지</span>, <span class="term-highlight" onclick="openGlossary('special_turnout')">외산 특수분기기</span>의 공장 시험성적서를 대조하고 감리단 승인을 득합니다.
                    </p>
                </div>
                
                <!-- STEP 2 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-sky-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-sky-100 text-sky-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 25Ton 장축 수송 & 도로점용 협업</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">관할 경찰서/구청 도로점용 인허가 및 심야 교통통제 수송</h3>
                    <p class="text-slate-600 text-xs sm:text-sm">
                        25Ton 장축 트레일러 투입에 따라 도로 점용 계획을 수립하고, 사인카배치 및 신호수 조를 동원하여 도로 안전을 확보한 후 자재를 반입합니다.
                    </p>
                </div>

                <!-- STEP 3 (PST 패널 치수측정 시뮬레이터) -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 현장 인수검사 & PST 패널 치수 측량</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">감리 입회 레일 표면 흠집 검사 및 PST 패널 치수(±2mm) 정밀 측정</h3>
                    <p class="text-slate-600 text-xs sm:text-sm mb-4">
                        반입 자재 하차 후 감리 입회 하에 레일 표면 균열 흠집을 전수 조사하고, 버니어 캘리퍼스로 <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 프리캐스트 패널</span> 치수가 <strong>±2.0mm 이내</strong>인지 측정합니다.
                    </p>
                    
                    <!-- PST 패널 치수 측량 시뮬레이터 -->
                    <div class="my-4 grid grid-cols-1 lg:grid-cols-12 gap-5 bg-slate-100 p-5 rounded-xl border border-slate-300">
                        <div class="lg:col-span-7 bg-white p-4 rounded-xl border border-slate-200 shadow-inner flex flex-col justify-between">
                            <div style="height: 220px;" class="relative">
                                <svg id="panelMeasSvg" viewBox="0 0 450 220" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                                    <rect x="0" y="0" width="450" height="220" fill="#f8fafc"/>
                                    <rect id="panelObj" x="70" y="60" width="310" height="110" fill="#cbd5e1" stroke="#475569" stroke-width="3" rx="4"/>
                                    <text x="225" y="120" text-anchor="middle" font-size="12" font-weight="black" fill="#1e293b">PST 패널 모재 (설계 폭 3,000mm)</text>
                                    
                                    <line id="measBeamLeft" x1="70" y1="30" x2="70" y2="185" stroke="#059669" stroke-width="2" stroke-dasharray="3,2"/>
                                    <line id="measBeamRight" x1="380" y1="30" x2="380" y2="185" stroke="#059669" stroke-width="2" stroke-dasharray="3,2"/>
                                    <line id="measBeamCenter" x1="70" y1="40" x2="380" y2="40" stroke="#059669" stroke-width="2"/>
                                    <circle cx="70" cy="40" r="4" fill="#059669"/>
                                    <circle cx="380" cy="40" r="4" fill="#059669"/>
                                    <text id="measValTxt" x="225" y="32" text-anchor="middle" font-size="11" font-weight="black" fill="#059669">측정값: 3,000.0mm (오차 0.0mm - 합격)</text>
                                </svg>
                            </div>
                            <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-200">
                                <div class="flex items-center gap-1.5">
                                    <button onclick="testPanelWidth(0)" class="sim-btn bg-emerald-600 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg border border-emerald-700">🟢 정상 (오차 0.0mm)</button>
                                    <button onclick="testPanelWidth(1.5)" class="sim-btn bg-blue-600 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg border border-blue-700">🟡 미세편차 (+1.5mm)</button>
                                    <button onclick="testPanelWidth(3.5)" class="sim-btn bg-rose-600 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg border border-rose-700">🔴 불량 (+3.5mm 반출)</button>
                                </div>
                                <div id="panelAlert" class="text-[11px] font-bold px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 border border-emerald-200">
                                    🟢 합격 (공차 ±2.0mm 이내)
                                </div>
                            </div>
                        </div>
                        
                        <div class="lg:col-span-5 flex flex-col justify-center space-y-3">
                            <h5 class="text-xs font-black text-slate-800 uppercase tracking-wider">📋 PST 패널 인수검사 수칙</h5>
                            <ol class="list-decimal pl-4 text-[11px] text-slate-600 space-y-2">
                                <li><strong>1단계. 버니어 캘리퍼스 측량:</strong> 패널 폭, 길이, 대각선을 잽니다.</li>
                                <li><strong>2단계. 공차 허용범위 확인:</strong> 오차가 <strong>±2.0mm 이내</strong>일 때만 합격입니다.</li>
                                <li><strong>3단계. 흠집 조사:</strong> 표면 크랙 발생 시 즉시 반출 조치합니다.</li>
                            </ol>
                        </div>
                    </div>
                </div>

                <!-- STEP 4 (★ 요청사항 특별 보강: 레일고정 액상수지 현장 시공/관리 & 주입 시뮬레이터!) -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">4</div>
                    <span class="bg-blue-100 text-blue-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 4. 레일고정 액상수지 보관·관리 및 현장 주입 수행</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">상온(15~25℃) 드럼 보관 및 2액형 현장 교반 액상 주입(Pouring)</h3>
                    <p class="text-slate-600 text-xs sm:text-sm mb-4">
                        <span class="term-highlight" onclick="openGlossary('resin_fill')">레일고정 액상수지</span>는 주제와 경화제로 구성된 2액형 고탄성 수지입니다. 보관 시 직사광선을 피해 <strong>15~25℃ 상온</strong> 보관하며, 현장에서 레일 측면 틈새에 액체 상태로 채워 넣어 탄성 고무로 경화시킵니다.
                    </p>
                    
                    <!-- 🧪 액상수지 현장 시공 4단계 가이드 & 주입/경화 시뮬레이터 -->
                    <div class="my-4 grid grid-cols-1 lg:grid-cols-12 gap-5 bg-blue-50/60 p-5 rounded-xl border border-blue-200">
                        <div class="lg:col-span-7 bg-white p-4 rounded-xl border border-slate-200 shadow-inner flex flex-col justify-between">
                            <div style="height: 230px;" class="relative">
                                <svg id="resinSimSvg" viewBox="0 0 450 230" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                                    <rect x="0" y="0" width="450" height="230" fill="#f8fafc"/>
                                    <rect x="40" y="140" width="370" height="70" fill="#94a3b8"/>
                                    <rect x="150" y="70" width="150" height="140" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                                    
                                    <path d="M 200 190 L 200 90 L 195 90 L 195 75 L 255 75 L 255 90 L 250 90 L 250 190 Z" fill="#475569" stroke="#1e293b" stroke-width="2"/>
                                    <text x="225" y="130" text-anchor="middle" font-size="10" font-weight="black" fill="#ffffff">홈레일 51R1</text>

                                    <rect id="resinLeft" x="155" y="190" width="40" height="0" fill="#0284c7" opacity="0.85"/>
                                    <rect id="resinRight" x="255" y="190" width="40" height="0" fill="#0284c7" opacity="0.85"/>

                                    <text id="resinStatusTxt" x="225" y="35" text-anchor="middle" font-size="11" font-weight="black" fill="#0284c7">수지 상태: 미주입 (레일 틈새 빈 상태)</text>
                                </svg>
                            </div>
                            
                            <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-200">
                                <div class="flex items-center gap-1.5">
                                    <button onclick="pourResin()" class="sim-btn bg-blue-600 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg border border-blue-700">🧪 1. 액상 주입 (Pouring)</button>
                                    <button onclick="cureResin()" class="sim-btn bg-emerald-600 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg border border-emerald-700">🟢 2. 탄성 경화 (Curing)</button>
                                    <button onclick="resetResin()" class="sim-btn bg-slate-500 text-white text-[11px] font-bold px-2.5 py-1.5 rounded-lg">↺ 초기화</button>
                                </div>
                                <div id="resinAlert" class="text-[11px] font-bold px-2.5 py-1 rounded bg-slate-100 text-slate-700 border border-slate-200">
                                    대기 중
                                </div>
                            </div>
                        </div>

                        <div class="lg:col-span-5 flex flex-col justify-center space-y-2.5 text-xs text-slate-700">
                            <h5 class="text-xs font-black text-blue-900 uppercase tracking-wider">🧪 액상수지 현장 수행 4단계</h5>
                            <div class="bg-white p-2.5 rounded-lg border border-blue-100">
                                <strong>1. 홈 청소 & 프라이머 도포:</strong> 레일 측면 먼지 습기를 제거하고 도포제 처리.
                            </div>
                            <div class="bg-white p-2.5 rounded-lg border border-blue-100">
                                <strong>2. 2액형 비율 교반:</strong> 주제와 경화제를 전용 혼합기로 3분간 균일 혼합.
                            </div>
                            <div class="bg-white p-2.5 rounded-lg border border-blue-100">
                                <strong>3. 액체 상태 주입 (Pouring):</strong> 틈새에 흘려넣어 기포 없이 공극 완밀 충전.
                            </div>
                            <div class="bg-white p-2.5 rounded-lg border border-blue-100">
                                <strong>4. 탄성 고무 경화 (Curing):</strong> 2~4시간 후 굳어져 진동·소음·누설전류 차단.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- STEP 5 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">5</div>
                    <span class="bg-green-100 text-green-900 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 5. 불량 자재 현장 전량 반출 & 대장 기인</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">불량 자재 현장 전량 반출 조치 및 자재인수검사 대장 서명</h3>
                    <p class="text-slate-600 text-xs sm:text-sm">
                        규격 초과 및 변형 자재는 즉시 현장 밖으로 반출 트럭을 이용하여 회수 조치하고, 자재인수검사 대장에 감리 서명을 득해 마감합니다.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{common_modal_html}

<script>
// Master 5-Step receiving simulator script
let currentStepIdx = 1;
let autoPlayTimer = null;

const stepData = {{
    1: {{
        badge: 'STEP 1',
        badgeBg: 'bg-amber-500 text-white',
        title: '1단계: 사전 공장검수 & 60일 전 승인 (서류 검증)',
        desc: '해외 수입 자재인 그루브드레일(51R1/60R2), 역상수지, 특수 분기기는 시공 60일 전 공장성적서(Mill Sheet) 검수 및 자재 조달 계획을 감리단과 최종 의결합니다.',
        btnColor: 'bg-amber-500 text-white border-amber-600'
    }},
    2: {{
        badge: 'STEP 2',
        badgeBg: 'bg-sky-500 text-white',
        title: '2단계: 25Ton 장축 수송 & 도로점용 협업 (운반 수송)',
        desc: '25Ton 장축 트레일러 투입에 따라 관할 경찰서 및 구청과 도로점용 인허가를 득하고, 심야 수송 시 사인카 배치 및 신호수 조를 동원하여 도로 안전을 확보합니다.',
        btnColor: 'bg-sky-500 text-white border-sky-600'
    }},
    3: {{
        badge: 'STEP 3',
        badgeBg: 'bg-emerald-500 text-white',
        title: '3단계: 현장 인수검사 & PST 패널 치수 측량 (정밀 검측)',
        desc: '반입 자재 하차 후 감리 입회 하에 레일 표면 흠집을 전수 조사하고, 버니어 캘리퍼스로 PST 프리캐스트 패널 치수가 ±2.0mm 이내인지 측정합니다.',
        btnColor: 'bg-emerald-500 text-white border-emerald-600'
    }},
    4: {{
        badge: 'STEP 4',
        badgeBg: 'bg-blue-600 text-white',
        title: '4단계: 레일고정 액상수지 보관 & 현장 주입 수행 (탄성 고무 경화)',
        desc: '주제/경화제 2액형 액상수지를 상온(15~25℃) 보관하며, 레일 측면 틈새에 액체로 주입(Pouring)하여 2~4시간 후 진동·누설전류 차단 탄성체로 경화시킵니다.',
        btnColor: 'bg-blue-600 text-white border-blue-700'
    }},
    5: {{
        badge: 'STEP 5',
        badgeBg: 'bg-green-500 text-white',
        title: '5단계: 불량 자재 현장 전량 반출 & 대장 기인 (최종 마감)',
        desc: '규격 초과 및 균열 손상 자재는 현장 밖으로 즉시 반출 트럭 회수 조치하고, 자재인수검사 대장에 감리 서명을 기록하여 마감합니다.',
        btnColor: 'bg-green-500 text-white border-green-600'
    }}
}};

function setStep(step) {{
    currentStepIdx = step;
    const data = stepData[step];
    
    for (let i = 1; i <= 5; i++) {{
        const btn = document.getElementById(`stepBtn${{i}}`);
        if (i === step) {{
            btn.className = `sim-step-btn active ${{data.btnColor}} p-3 rounded-xl border font-bold text-left transition-all`;
        }} else {{
            btn.className = `sim-step-btn bg-slate-100 text-slate-700 p-3 rounded-xl border border-slate-300 text-left transition-all hover:bg-slate-200`;
        }}
    }}
    
    const badgeEl = document.getElementById('seqBadge');
    badgeEl.innerText = data.badge;
    badgeEl.className = `${{data.badgeBg}} font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5`;
    document.getElementById('seqTitle').innerText = data.title;
    document.getElementById('seqDesc').innerText = data.desc;
    
    for (let i = 1; i <= 5; i++) {{
        const group = document.getElementById(`seqGroupStep${{i}}`);
        if (group) group.setAttribute('opacity', i === step ? '1' : '0');
    }}
}}

function toggleAutoPlay() {{
    const playText = document.getElementById('playText');
    const playIcon = document.getElementById('playIcon');
    
    if (autoPlayTimer) {{
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
        playText.innerText = "자동 시뮬레이션 재생";
        playIcon.innerText = "▶";
    }} else {{
        playText.innerText = "일시 정지";
        playIcon.innerText = "⏸";
        autoPlayTimer = setInterval(() => {{
            currentStepIdx = (currentStepIdx % 5) + 1;
            setStep(currentStepIdx);
        }}, 3000);
    }}
}}

// PST Panel Width measurement simulator logic
function testPanelWidth(errorMm) {{
    const rightLine = document.getElementById('measBeamRight');
    const valTxt = document.getElementById('measValTxt');
    const alertBox = document.getElementById('panelAlert');
    const panelObj = document.getElementById('panelObj');
    
    let xOffset = 380 + (errorMm * 10);
    if (rightLine) rightLine.setAttribute('x1', xOffset);
    if (rightLine) rightLine.setAttribute('x2', xOffset);
    
    let totalVal = (3000 + errorMm).toFixed(1);
    if (errorMm > 0) {{
        valTxt.innerText = `측정값: ${{totalVal}}mm (오차 +${{errorMm.toFixed(1)}}mm)`;
    }} else {{
        valTxt.innerText = `측정값: ${{totalVal}}mm (오차 0.0mm - 합격)`;
    }}
    
    if (Math.abs(errorMm) <= 2.0) {{
        valTxt.setAttribute('fill', '#059669');
        if (panelObj) panelObj.setAttribute('stroke', '#475569');
        alertBox.innerText = `🟢 합격 (공차 ±2.0mm 이내)`;
        alertBox.className = "text-[11px] font-bold px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 border border-emerald-200";
    }} else {{
        valTxt.setAttribute('fill', '#dc2626');
        if (panelObj) panelObj.setAttribute('stroke', '#dc2626');
        alertBox.innerText = `🔴 규격 초과 (+${{errorMm.toFixed(1)}}mm 즉시 반출!)`;
        alertBox.className = "text-[11px] font-bold px-2.5 py-1 rounded bg-rose-100 text-rose-800 border border-rose-200 animate-pulse";
    }}
}}

// Resin Pouring & Curing Simulator logic
function pourResin() {{
    const left = document.getElementById('resinLeft');
    const right = document.getElementById('resinRight');
    const txt = document.getElementById('resinStatusTxt');
    const alertBox = document.getElementById('resinAlert');
    
    if (left) {{
        left.setAttribute('y', '75');
        left.setAttribute('height', '115');
        left.setAttribute('fill', '#0284c7');
    }}
    if (right) {{
        right.setAttribute('y', '75');
        right.setAttribute('height', '115');
        right.setAttribute('fill', '#0284c7');
    }}
    if (txt) {{
        txt.innerText = "수지 상태: 액체 주입 완료 (Pouring 완료 - 경화 대기)";
        txt.setAttribute('fill', '#0284c7');
    }}
    if (alertBox) {{
        alertBox.innerText = "🧪 1단계: 주입 완료";
        alertBox.className = "text-[11px] font-bold px-2.5 py-1 rounded bg-blue-100 text-blue-800 border border-blue-200";
    }}
}}

function cureResin() {{
    const left = document.getElementById('resinLeft');
    const right = document.getElementById('resinRight');
    const txt = document.getElementById('resinStatusTxt');
    const alertBox = document.getElementById('resinAlert');
    
    if (left) {{
        left.setAttribute('y', '75');
        left.setAttribute('height', '115');
        left.setAttribute('fill', '#10b981');
    }}
    if (right) {{
        right.setAttribute('y', '75');
        right.setAttribute('height', '115');
        right.setAttribute('fill', '#10b981');
    }}
    if (txt) {{
        txt.innerText = "수지 상태: 🟢 탄성 고무 경화 완료 (진동·소음·누설전류 완벽 차단!)";
        txt.setAttribute('fill', '#059669');
    }}
    if (alertBox) {{
        alertBox.innerText = "🟢 2단계: 경화완료";
        alertBox.className = "text-[11px] font-bold px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 border border-emerald-200";
    }}
}}

function resetResin() {{
    const left = document.getElementById('resinLeft');
    const right = document.getElementById('resinRight');
    const txt = document.getElementById('resinStatusTxt');
    const alertBox = document.getElementById('resinAlert');
    
    if (left) {{
        left.setAttribute('y', '190');
        left.setAttribute('height', '0');
    }}
    if (right) {{
        right.setAttribute('y', '190');
        right.setAttribute('height', '0');
    }}
    if (txt) {{
        txt.innerText = "수지 상태: 미주입 (레일 틈새 빈 상태)";
        txt.setAttribute('fill', '#0284c7');
    }}
    if (alertBox) {{
        alertBox.innerText = "대기 중";
        alertBox.className = "text-[11px] font-bold px-2.5 py-1 rounded bg-slate-100 text-slate-700 border border-slate-200";
    }}
}}

window.addEventListener('load', () => {{
    setStep(1);
}});
</script>
</body>
</html>
"""

# =========================================================================
# 3. WBS 12 CHECKLIST HTML (자재 반입 마스터 체크리스트)
# =========================================================================
checklist_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 반입 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
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
            color: #1e3a8a;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }}
        .summary-box {{
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #065f46;
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
            color: #1e3a8a;
        }}
        .step-tag {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-right: 4px;
        }}
        {minimal_glossary_style}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">자재 반입 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-12 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 1.05rem; font-weight: 800;">📋 표준서 & 수행지침 연계 자재 인수 검측 항목</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 외산 자재(그루브드레일/역상수지/외산 특수분기기) 60일 전 공장성적서 검수, 레일고정 액상수지 상온(15~25℃) 보관, 25Ton 장축 수송, PST 패널 허용공차(±2.0mm 이내) 및 불량재 현장 반출 처리를 검측하기 위해 제작되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">표준서 & 수행지침 연계 필수 검측 항목 (KCS 시방 수립)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:var(--accent-orange);">⚠️ 사전 리스크<br>(Step 1~2 반입 전)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 공장 검수</span>
                        <strong>[외산 자재 60일 전 검수]</strong> <span class="term-highlight" onclick="openGlossary('grooved_rail')">그루브드레일(51R1)</span>, <span class="term-highlight" onclick="openGlossary('resin_fill')">역상수지</span>, <span class="term-highlight" onclick="openGlossary('special_turnout')">외산 특수분기기</span> 공장 시험성적서(Mill Sheet) 원본 검토 및 감리 승인 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 운반 통제</span>
                        <strong>[25Ton 장축 수송 인허가]</strong> 경찰서/구청 도로점용 인허가, 심야 사인카 배치 및 신호수 조 수립 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-red);">⚡ 공사중 리스크<br>(Step 3~4 하차/적재)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 인수 검측</span>
                        <strong>[PST 패널 치수 측량]</strong> 버니어 캘리퍼스 측정 <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 슬래브 패널</span> 치수 허용공차(<b>&plusmn;2.0mm 이내</b>) 및 표면 흠집 감리 입회 검측 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 액상수지 관리</span>
                        <strong>[액상수지 보관 & 현장 주입]</strong> 레일고정 액상수지 드럼 상온(<b>15~25℃</b>) 차광 보관, 2액형 정량 교반 및 레일 틈새 주입 수밀/절연 검측 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-green);">✅ 공사후 리스크<br>(Step 5 반출/마감)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 불량재 반출</span>
                        <strong>[불량 자재 현장 전량 반출]</strong> 규격 초과 및 변형 불량 자재 즉시 현장 밖으로 반출 트럭 회수 조치 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 대장 서명</span>
                        <strong>[자재인수검사 대장 서명]</strong> 감리 입회 인수검사 대장 서명 완료 및 품질대장 영구 보존 등록 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-12 콘크리트도상 자재 반입 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Write all WBS 12 master HTML files
force_write(path_standard, standard_html)
force_write(path_standard_alt, standard_html)

force_write(path_guideline, guideline_html)

force_write(path_checklist, checklist_html)
force_write(path_checklist_alt, checklist_html)

print("\n🎉 SUCCESSFULLY RE-UPDATED WBS 12 (자재 반입) WITH ELASTIC RESIN & FOREIGN TURNOUT GUIDANCE!")
