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

wbs12_guideline_dir = os.path.dirname(path_guideline)

# Copy user uploaded diagram image
brain_user_img = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.user_uploaded\media__1784952962498.png"
dst_img_path = os.path.join(wbs12_guideline_dir, "embedded_rail_system.png")

if os.path.exists(brain_user_img):
    shutil.copy(brain_user_img, dst_img_path)
    print(f"📦 Successfully copied user image to: {dst_img_path}")

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
    'polycork': {
        title: '① 레일고정수지 (Polycork)',
        desc: '매립형 궤도 홈레일 측면 틈새에 채워 넣어 레일을 탄성 감싸는 고탄성 폴리우레탄 수지입니다. 도심지 소음/진동을 차단하고 직류 누설전류(Stray Current) 부식을 방지합니다.'
    },
    'purailstrip': {
        title: '② 연속레일패드 (PURailstrip)',
        desc: '레일 하부 전 구간에 연속으로 깔리는 고탄성 탄성 패드입니다. 차량 하중 충격을 균일 분산하고 궤도의 수직 탄성을 지속 유지시켜 줍니다.'
    },
    'tfixb': {
        title: '③ 레일고정장치 (TFIXB)',
        desc: '매립형 홈레도의 좌우 게이지 수평 선형 및 측면 하중을 굳건히 고정해주는 전용 궤도 체결 장치입니다.'
    },
    'vert_pad': {
        title: '④ 레일수직조정패드',
        desc: '레일 바닥면에 설치되어 트램 선로의 미세 높낮이(고저) 및 캔트 미세 조정을 수행하는 정밀 패드입니다.'
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
# 1. WBS 12 STANDARD HTML (수지고정 매립형 레일체결시스템 반영)
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
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-12 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">수지고정 매립형 레일체결시스템 표준</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 반입 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"수지고정 매립형 레일체결 4대 자재(Polycork, PURailstrip, TFIXB, 수직조정패드) 및 PST 패널 허용공차(±2mm) 관리"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs sm:text-sm text-amber-900">
            <h4 class="font-bold text-amber-950 mb-1">💡 콘크리트도상 수지고정 매립형 레일체결 자재 정의</h4>
            <p class="leading-relaxed">
                본 공종은 단순 콘크리트를 반입하는 공종이 아닌, 트램 매설 선로의 핵심인 <strong><span class="term-highlight" onclick="openGlossary('polycork')">① 레일고정수지(Polycork)</span>, <span class="term-highlight" onclick="openGlossary('purailstrip')">② 연속레일패드(PURailstrip)</span>, <span class="term-highlight" onclick="openGlossary('tfixb')">③ 레일고정장치(TFIXB)</span>, <span class="term-highlight" onclick="openGlossary('vert_pad')">④ 레일수직조정패드</span></strong> 및 PST 패널 등 수지고정 매립형 궤도 시스템 구성품의 인수검사 및 품질 준수 기준입니다.
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
                <span class="text-blue-600">2.</span> 매립형 레일체결시스템 주요 구성자재 정량 기술 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">자재 구성품</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 관리 기술 표준 (KCS 시방 연동)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">① 레일고정수지<br>(Polycork)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">보관온도 15~25℃<br>절연저항 &ge; 10 M&Omega;</td>
                            <td class="p-3 border text-slate-600">• 주제/경화제 전용 교반 후 레일 측면 충전.<br>• 진동·소음 흡수 및 지중 누설전류(Stray Current) 부식 완벽 차단</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">② 연속레일패드<br>(PURailstrip)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">탄성복원율 &ge; 95%</td>
                            <td class="p-3 border text-slate-600">• 레일 바닥 전 구간 연속 인입 탄성 패드.<br>• 트램 차량 주행 수직 하원의 균일한 완충 분산 관리</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">③ 레일고정장치<br>(TFIXB)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">게이지 체결공차 &plusmn;0.5mm</td>
                            <td class="p-3 border text-slate-600">• 매립형 궤도 레일 좌우 게이지 수평 지지 클립.<br>• 볼트 체결 토크 시방치 100% 준수 하 하차 인수검사</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">④ 레일수직조정패드</td>
                            <td class="p-3 border text-center font-bold text-blue-700">높이 조정공차 &plusmn;0.5mm</td>
                            <td class="p-3 border text-slate-600">• 레일 바닥면 수직 고저 및 캔트 조율 패드.<br>• 균열 및 두께 변형 불량 자재 즉시 반출 처리</td>
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
# 2. WBS 12 GUIDELINE HTML (사용자 공유 그림1 반영 & 4대 자재 상세 카드)
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
        .flow-card {{
            transition: all 0.25s ease;
        }}
        .flow-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.08);
        }}
        .img-card {{
            transition: all 0.3s ease;
        }}
        .img-card:hover {{
            transform: scale(1.01);
            box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.12);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 to-slate-900 opacity-70"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-12 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">실무 정밀 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 반입 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"수지고정 매립형 레일체결시스템 구성(Polycork, PURailstrip, TFIXB, 수직조정패드) 정밀 수칙"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 오해 방지 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> "콘크리트도상 자재 반입" 개념 정립
            </h4>
            <p class="leading-relaxed">
                본 공종은 일반 콘크리트의 반입이 아닙니다! 트램 매설 선로를 구축하는 <strong><span class="term-highlight" onclick="openGlossary('polycork')">① 레일고정수지(Polycork)</span>, <span class="term-highlight" onclick="openGlossary('purailstrip')">② 연속레일패드(PURailstrip)</span>, <span class="term-highlight" onclick="openGlossary('tfixb')">③ 레일고정장치(TFIXB)</span>, <span class="term-highlight" onclick="openGlossary('vert_pad')">④ 레일수직조정패드</span></strong> 등 수지고정 매립형 궤도 체결시스템 핵심 자재의 인수검사 및 현장 반입 수칙을 정밀 서술한 지침서입니다.
            </p>
        </div>

        <!-- 1. ★ 사용자 제공 실무 그림1 반영: 수지고정 매립형 레일체결시스템의 구성 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 수지고정 매립형 레일체결시스템의 핵심 구성 ([그림 1] 실무 도식)
            </h2>
            
            <div class="bg-slate-100 p-5 rounded-2xl border border-slate-300 img-card">
                <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-inner flex justify-center mb-4 overflow-hidden">
                    <img src="./embedded_rail_system.png" alt="[그림 1] 수지고정 매립형 레일체결시스템의 구성" class="max-w-full h-auto object-contain rounded-lg">
                </div>
                <div class="text-center font-bold text-slate-800 text-sm mb-4">
                    [그림 1] 수지고정 매립형 레일체결시스템의 구성 및 주요 4대 자재
                </div>

                <!-- 4대 핵심 구성자재 2x2 그리드 카드 해설 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <span class="bg-blue-600 text-white font-bold text-[10px] px-2 py-0.5 rounded">구성 자재 1</span>
                            <h4 class="font-bold text-slate-900 text-sm mt-1.5 flex items-center gap-1.5">
                                ① 레일고정수지 (Polycork)
                            </h4>
                            <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                                매립형 궤도 홈레일 측면 틈새에 채워 넣어 레일을 유연하게 감싸는 탄성 고무 수지입니다. 트램 주행 <strong>진동·소음 차단 및 지중 누설전류(Stray Current) 부식 완벽 방지</strong> 역할을 수행합니다.
                            </p>
                        </div>
                        <div class="mt-3 text-[10px] font-bold text-blue-700 bg-blue-50 p-2 rounded border border-blue-100">
                            🧪 보관: 상온(15~25℃) 차광 보관 | 절연저항 &ge; 10 M&Omega;
                        </div>
                    </div>

                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <span class="bg-emerald-600 text-white font-bold text-[10px] px-2 py-0.5 rounded">구성 자재 2</span>
                            <h4 class="font-bold text-slate-900 text-sm mt-1.5 flex items-center gap-1.5">
                                ② 연속레일패드 (PURailstrip)
                            </h4>
                            <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                                레일 하부 전 구간에 연속으로 설치되는 고탄성 탄성 패드입니다. 트램 차량의 수직 충격 하중을 균일하게 분산시키고 궤도의 탄성력을 지속 유지해 줍니다.
                            </p>
                        </div>
                        <div class="mt-3 text-[10px] font-bold text-emerald-700 bg-emerald-50 p-2 rounded border border-emerald-100">
                            🧱 검수: 탄성복원율 &ge; 95% | 표면 흠집 전수 검측
                        </div>
                    </div>

                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <span class="bg-amber-600 text-white font-bold text-[10px] px-2 py-0.5 rounded">구성 자재 3</span>
                            <h4 class="font-bold text-slate-900 text-sm mt-1.5 flex items-center gap-1.5">
                                ③ 레일고정장치 (TFIXB)
                            </h4>
                            <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                                매립형 궤도의 좌우 게이지 수평 선형 및 레일 측면 하중을 굳건히 고정해주는 전용 궤도 고정 클립 장치입니다.
                            </p>
                        </div>
                        <div class="mt-3 text-[10px] font-bold text-amber-800 bg-amber-50 p-2 rounded border border-amber-100">
                            ⚙️ 검수: 게이지 공차 &plusmn;0.5mm | 볼트 토크 시방 대조
                        </div>
                    </div>

                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <span class="bg-purple-600 text-white font-bold text-[10px] px-2 py-0.5 rounded">구성 자재 4</span>
                            <h4 class="font-bold text-slate-900 text-sm mt-1.5 flex items-center gap-1.5">
                                ④ 레일수직조정패드
                            </h4>
                            <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                                레일 바닥면에 설치되어 트램 선로의 미세 높낮이(고저) 및 곡선부 캔트를 정밀 조정하는 수직 조정 패드입니다.
                            </p>
                        </div>
                        <div class="mt-3 text-[10px] font-bold text-purple-800 bg-purple-50 p-2 rounded border border-purple-100">
                            📏 검수: 높이 조정공차 &plusmn;0.5mm | 변형재 즉시 반출
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 자재 반입 5대 관리 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 자재 반입 5대 관리 프로세스 마스터 체계도 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">사전 공장검수</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            외산 자재(TFIXB, 수지 등) <strong>시공 60일 전</strong> 해외 공장성적서(Mill Sheet) 감리 승인
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        📋 핵심: 수입 성적서 대조
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">25Ton 장축 수송</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            경찰서/구청 도로점용 인허가 득함, 심야 <strong>사인카 & 신호수</strong> 교통 통제 반입
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        🚚 핵심: 도로점용 안전
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">현장 인수검사</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            감리 입회 패드/클립 점검, PST 패널 치수 <strong>&plusmn;2.0mm 이내</strong> 측량
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        📏 핵심: 공차 &plusmn;2.0mm
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">액상수지·야드적재</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            Polycork 액상수지 <strong>15~25℃ 상온</strong> 보관, 자재 Lot 마킹 대조 및 덮개 밀폐
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        🧪 핵심: 15~25℃ 보관
                    </div>
                </div>

                <div class="flow-card bg-rose-50 p-4 rounded-xl border border-rose-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-rose-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 5</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">불량재 반출·마감</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            규격 초과/변형 자재 <strong>즉시 현장 반출</strong>, 감리 인수검사 대장 서명
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-rose-100 text-[10px] text-rose-800 font-bold">
                        🚫 핵심: 불량재 100% 반출
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. 상세 세부 수행 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 단계별 실무 엔지니어링 수행 수칙
            </h2>
            
            <div class="space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 1</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">외산 수지고정 매립형 자재 사전 공장검수 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            <span class="term-highlight" onclick="openGlossary('polycork')">Polycork 액상수지</span>, <span class="term-highlight" onclick="openGlossary('tfixb')">TFIXB 레일고정장치</span> 등 해외 수입 자재는 공장 시험성적서(Mill Sheet) 원본을 입수하여 KCS 시방 규격 적합 여부를 검토하고 감리 승인을 의결합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">25Ton 장축 수송 & 도로점용 안전 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            장척 레일 및 대형 트레일러 투입에 따라 관할 경찰서 및 구청과 도로점용 인허가를 완료합니다. 심야 반입 시 사인카 투입, 신호수 배치 및 안전 펜스를 가설하여 도심지 교통 사고를 예방합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">감리 입회 인수검사 & PST 패널 치수 정밀 검측 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            자재 하차 직후 감리 입회 하에 <span class="term-highlight" onclick="openGlossary('purailstrip')">PURailstrip 연속패드</span> 및 TFIXB 장치 표면 흠집을 전수 조사합니다. PST 슬래브 패널은 버니어 캘리퍼스로 측정하여 허용 공차 <strong>&plusmn;2.0mm 이내</strong> 판정 시에만 하차 승인합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">Polycork 액상수지 상온 보관 & 현장 교반 주입 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            액상수지 드럼은 직사광선을 피하고 <strong>15~25℃ 상온 보관</strong>합니다. 현장 시공 시 레일 홈 청소 후 주제와 경화제를 규정 비율로 교반하여 액체 상태로 흘려넣고 2~4시간 후 완밀 경화시킵니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-rose-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 5</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">불량 자재 현장 전량 반출 & 자재대장 마감 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            치수 초과 및 균열 손상 자재는 현장 밖으로 회수 트럭을 투입해 전량 반출 조치합니다. 감리 입회 서명을 필한 자재인수검사 대장을 작성하고 품질 보존 대장에 영구 보존 등록합니다.
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

# =========================================================================
# 3. WBS 12 CHECKLIST HTML (Polycork, PURailstrip, TFIXB, 수직조정패드 반영)
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
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 1.05rem; font-weight: 800;">📋 수지고정 매립형 레일체결 4대 자재 인수 검측 항목</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 수지고정 매립형 레일체결 4대 부품(① Polycork, ② PURailstrip, ③ TFIXB, ④ 레일수직조정패드) 및 PST 패널 허용공차(±2.0mm 이내)를 현장 감리 입회 하에 실시간 검측하기 위해 제작되었습니다.
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
                        <strong>[외산 자재 60일 전 검수]</strong> <span class="term-highlight" onclick="openGlossary('polycork')">Polycork 액상수지</span>, <span class="term-highlight" onclick="openGlossary('tfixb')">TFIXB 레일고정장치</span> 공장 시험성적서(Mill Sheet) 원본 검토 및 감리 승인 여부
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
                        <strong>[4대 체결자재 & 패널 측량]</strong> <span class="term-highlight" onclick="openGlossary('purailstrip')">PURailstrip 패드</span> 흠집 점검 및 PST 패널 치수 공차(<b>&plusmn;2.0mm 이내</b>) 감리 입회 검측 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 액상수지 관리</span>
                        <strong>[Polycork 보관 & 현장 주입]</strong> Polycork 드럼 상온(<b>15~25℃</b>) 차광 보관, 2액형 정량 교반 및 레일 틈새 충전 수밀/절연 검측 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-green);">✅ 공사후 리스크<br>(Step 5 반출/마감)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 불량재 반출</span>
                        <strong>[불량 자재 현장 전량 반출]</strong> 규격 초과 및 변형/균열 불량 자재 즉시 현장 밖으로 반출 트럭 회수 조치 여부
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

print("\n🎉 SUCCESSFULLY INTEGRATED USER DIAGRAM & 4 EMBEDDED RAIL SYSTEM COMPONENTS INTO WBS 12!")
