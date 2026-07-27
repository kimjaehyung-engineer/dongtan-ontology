import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\13_[HBS] 강화노반 확인"

path_std = os.path.join(target_dir, "표준서", "[HBS] 강화노반 확인_표준서.html")
path_std_alt = os.path.join(target_dir, "표준서", "13_[HBS] 강화노반 확인_표준서.html")

path_gui = os.path.join(target_dir, "수행지침", "[HBS] 강화노반 확인_수행지침.html")
path_gui_alt = os.path.join(target_dir, "수행지침", "13_[HBS] 강화노반 확인_수행지침.html")

path_chk = os.path.join(target_dir, "체크리스트", "[HBS] 강화노반 확인_체크리스트.html")
path_chk_alt = os.path.join(target_dir, "체크리스트", "13_[HBS] 강화노반 확인_체크리스트.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully written WBS 13 file: {path}")

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
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 공학 검측 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<script>
const glossaryData = {
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
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('glossaryModal');
        if(modal) modal.classList.remove('active');
    }
});
</script>
"""

# =========================================================================
# 1. WBS 13 STANDARD HTML
# =========================================================================
standard_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 강화노반 확인 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-13 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">노반 지지력 K30 &ge; 110 MN/m³ 품질 기준</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[HBS] 강화노반 확인 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"기존 도로구간 노상토 지지력 검증: 평판재하시험(K30 &ge; 110 MN/m³, Ev2 &ge; 120 MPa) 및 마무리 높이 오차(&plusmn;10mm) 관리"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 💡 핵심 오해 방지 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs sm:text-sm text-amber-900">
            <h4 class="font-bold text-amber-950 mb-1">💡 [HBS] 강화노반 확인 공종 개요</h4>
            <p class="leading-relaxed">
                본 공종은 콘크리트도상(TCL) 타설 전 토공사 분야로부터 전달받은 <strong><span class="term-highlight" onclick="openGlossary('hbs')">HBS 상부 강화노반</span></strong> 표면의 노반 반력계수(<span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³</span>), 변형계수(<span class="term-highlight" onclick="openGlossary('pbt')">Ev2 &ge; 120 MPa</span>), 마무리 높이 오차(&plusmn;10mm 이내) 및 횡단구배(2.0%) 배수 상태를 종합 인수·검증하는 필수 시방 공종입니다.
            </p>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / [HBS] 강화노반 확인 (현장 공사팀)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">강화노반 인수조치 측량 대장 | PBT 평판재하시험 성적서 | 배수점검표</p>
                </div>
            </div>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 강화노반 정량 기술 시방 절대 기준 (KCS 47 10 25 규정)
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">검측 품질 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 상세 기술 표준 (KCS 11 00 00 연동)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">노반 반력계수 (K30)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">K30 &ge; 110 MN/m³</td>
                            <td class="p-3 border text-slate-600">• 평판재하시험(PBT, Φ300mm) 성적서 원본 대조 승인.<br>• 토공사 인수 기준 K70 &ge; 150 MPa/m 성적서 수령 점검</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">2차 변형계수 (Ev2)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">Ev2 &ge; 120 MPa<br>(Ev2/Ev1 &le; 2.2)</td>
                            <td class="p-3 border text-slate-600">• 평판재하시험 2차 가하중 변형계수 120 MPa 이상 확보.<br>• 다짐도 연동 계수 Ev2/Ev1 비율 2.2 이하 달성 검증</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">마무리면 높이 오차</td>
                            <td class="p-3 border text-center font-bold text-red-600">&plusmn;10mm 이내</td>
                            <td class="p-3 border text-slate-600">• 광파 레벨기를 이용한 노반 표면 계획고 측정 오차 &plusmn;10mm 제어.<br>• 규격 초과 및 돌출 부위 돌가루 요철 전량 제거 처리</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">횡단 구배 및 배수</td>
                            <td class="p-3 border text-center font-bold text-blue-700">횡단 구배 2.0%</td>
                            <td class="p-3 border text-slate-600">• 빗물 정체 방지를 위한 노반 표면 2.0% 횡단 배수 경사 확보.<br>• 맹암거 및 측구 연결 부위 배수 정체 유무 현장 확인</td>
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
# 2. WBS 13 GUIDELINE HTML (Flow Architecture & 2D Engineering Diagrams)
# =========================================================================
guideline_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 강화노반 확인 수행지침서</title>
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
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-13 Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">노반 지지력 & 레벨 검측 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[HBS] 강화노반 확인 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"기존 도로구간 노상토 지지력(K30 &ge; 110 MN/m³), PBT 평판재하시험 및 노반 높이 오차(&plusmn;10mm) 정밀 가이드"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 작업 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl text-xs sm:text-sm text-amber-900 shadow-sm">
            <h4 class="font-bold text-amber-950 text-base mb-1.5 flex items-center gap-2">
                <span>💡</span> [HBS] 강화노반 확인 실무 수행 핵심
            </h4>
            <p class="leading-relaxed">
                콘크리트도상 시공 전, 토공사 공종으로부터 인수받는 <strong><span class="term-highlight" onclick="openGlossary('hbs')">상부 강화노반</span></strong>의 지지력 성적서(<span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³, Ev2 &ge; 120 MPa</span>)를 수령 대조하고, 현장 평판재하시험(<span class="term-highlight" onclick="openGlossary('pbt')">PBT</span>) 및 노반 마무리면 높이 오차(<span class="term-highlight" onclick="openGlossary('cross_slope')">&plusmn;10mm 이내</span>), 횡단 구배(2.0%)를 정밀 검측하는 절차입니다.
            </p>
        </div>

        <!-- 1. 강화노반 확인 5대 관리 프로세스 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 강화노반 확인 5대 관리 프로세스 마스터 체계도 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">인수 서류 확인</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            토공사 지지력 <strong><span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³</span></strong> 및 K70 &ge; 150 MPa/m 성적서 수령
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        📋 핵심: K30 성적서 수령
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">현장 시굴·밀도</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            터파기 시굴 후 들밀도 시험통 통과 상대다짐도 <strong>&ge; 95%</strong> 현장 검증
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        🧪 핵심: 다짐도 &ge; 95%
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">PBT 재하시험</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            현장 <strong><span class="term-highlight" onclick="openGlossary('pbt')">평판재하시험(PBT)</span></strong> 시행, 2차 변형계수 Ev2 &ge; 120 MPa 확인
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        ⚙️ 핵심: Ev2 &ge; 120 MPa
                    </div>
                </div>

                <div class="flow-card bg-blue-50 p-4 rounded-xl border border-blue-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">레벨·구배 측량</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            마무리면 높이 오차 <strong>&plusmn;10mm 이내</strong> 측량 및 횡단구배 2.0% 점검
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-blue-100 text-[10px] text-blue-800 font-bold">
                        📏 핵심: 오차 &plusmn;10mm
                    </div>
                </div>

                <div class="flow-card bg-rose-50 p-4 rounded-xl border border-rose-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-rose-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 5</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">인수 대장 서명</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            요철 부위 제거 및 감리 입회 <strong>강화노반 인수조치 대장</strong> 최종 서명
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-rose-100 text-[10px] text-rose-800 font-bold">
                        ✅ 핵심: 인수대장 서명
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 자재별 구조 정밀 공학 기술 도식 (Engineering Specification Diagram) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 강화노반 지지력 & 레벨 검측 정밀 공학 기술 도식
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 도식 1: HBS 강화노반 PBT 평판재하시험 메커니즘 도면 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 1] HBS 강화노반 PBT 평판재하시험 메커니즘
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">K30 &ge; 110 MN/m³</span>
                        </div>
                        
                        <!-- SVG Diagram 1 -->
                        <div class="bg-slate-900 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-800">
                            <svg viewBox="0 0 420 220" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#0f172a"/>
                                
                                <!-- 노반 지층 -->
                                <rect x="30" y="150" width="360" height="50" fill="#78350f" stroke="#b45309" stroke-width="2"/>
                                <text x="210" y="180" font-size="11" font-weight="bold" fill="#fef3c7" text-anchor="middle">HBS 강화노반 (K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa)</text>
                                
                                <!-- PBT 재하 평판 (300mm) -->
                                <rect x="150" y="142" width="120" height="8" fill="#cbd5e1" stroke="#334155" stroke-width="1.5"/>
                                <text x="210" y="137" font-size="9" font-weight="bold" fill="#e2e8f0" text-anchor="middle">Φ300mm PBT 재하 평판</text>
                                
                                <!-- 유압 재크 & 하중 반력 트럭 바닥 -->
                                <rect x="195" y="80" width="30" height="55" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
                                <text x="210" y="112" font-size="9" font-weight="bold" fill="#0f172a" text-anchor="middle">유압재크</text>
                                <line x1="210" y1="20" x2="210" y2="80" stroke="#f59e0b" stroke-width="4"/>
                                <rect x="110" y="15" width="200" height="12" fill="#ef4444" rx="2"/>
                                <text x="210" y="24" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">반력 트럭 덤프 하중 (25Ton)</text>

                                <!-- 변형 인디케이터 게이지 -->
                                <line x1="90" y1="146" x2="150" y2="146" stroke="#10b981" stroke-width="2"/>
                                <circle cx="90" cy="146" r="6" fill="#10b981"/>
                                <text x="85" y="132" font-size="9" font-weight="bold" fill="#34d399" text-anchor="end">침하량 다이얼 게이지</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>📊 공학 핵심:</strong> 덤프 트럭 반력 하중을 이용해 Φ300mm 평판에 유압을 가하여 <strong>K30 &ge; 110 MN/m³ 및 Ev2 &ge; 120 MPa(Ev2/Ev1 &le; 2.2)</strong> 지지력을 감리 입회 하에 정밀 산출합니다.
                    </div>
                </div>

                <!-- 도식 2: 강화노반 마무리면 레벨 & 횡단구배(2.0%) 점검 도면 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 2] 노반 레벨(&plusmn;10mm) & 횡단구배(2.0%)
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">배수 경사 2.0%</span>
                        </div>
                        
                        <!-- SVG Diagram 2 -->
                        <div class="bg-slate-900 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-800">
                            <svg viewBox="0 0 420 220" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#0f172a"/>
                                
                                <!-- 경사 노반 -->
                                <polygon points="30,120 390,145 390,195 30,195" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
                                <text x="210" y="175" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">강화노반 표면 (마무리면 오차 ±10mm 이내)</text>

                                <!-- 횡단 구배 2.0% 경사 표시선 -->
                                <line x1="50" y1="100" x2="370" y2="125" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,2"/>
                                <text x="210" y="105" font-size="10" font-weight="bold" fill="#fbbf24" text-anchor="middle">횡단 구배 2.0% 배수 경사</text>

                                <!-- 광파 측량 타겟 & 레벨 측량 -->
                                <line x1="120" y1="60" x2="120" y2="126" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2,2"/>
                                <circle cx="120" cy="60" r="5" fill="#38bdf8"/>
                                <text x="120" y="48" font-size="9" font-weight="bold" fill="#7dd3fc" text-anchor="middle">광파 타겟 (계획고 오차 점검)</text>

                                <!-- 배수 맹암거 측구 -->
                                <rect x="370" y="140" width="30" height="55" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
                                <circle cx="385" cy="170" r="8" fill="#0284c7"/>
                                <text x="385" y="132" font-size="8" font-weight="bold" fill="#38bdf8" text-anchor="middle">배수 맹암거</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-100 text-xs text-emerald-900 leading-relaxed">
                        <strong>📏 측량 핵심:</strong> 광파 레벨기로 노반 마무리면 계획고 오차를 <strong>&plusmn;10mm 이내</strong>로 정밀 관리하며, 표면 우수 배수를 위한 <strong>2.0% 횡단 구배</strong>를 형성하여 맹암거로 유도합니다.
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
                        <h4 class="font-bold text-slate-900 text-sm">토공사 지지력 성적서 사전 검토 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            토공 공종으로부터 상부 강화노반 지지력 성적서(<span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³</span> 또는 K70 &ge; 150 MPa/m) 원본을 대조 수령하고 시험 위치 및 시험 일자를 검토합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">터파기 시굴 & 들밀도 상대다짐도 검증 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            현장 터파기 구간 시굴 후 들밀도 시험통을 통과한 강화노반 흙의 상대다짐도 <strong>&ge; 95%</strong> 확보 여부를 현장에서 직접 측정 점검합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">현장 PBT 평판재하시험 & 2차 변형계수 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            감리 입회 하에 Φ300mm 재하 평판과 유압 재크를 세팅하여 현장 <span class="term-highlight" onclick="openGlossary('pbt')">평판재하시험(PBT)</span>을 수행하고 2차 변형계수 <strong>Ev2 &ge; 120 MPa(Ev2/Ev1 &le; 2.2)</strong>를 최종 승인합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">마무리면 오차(&plusmn;10mm) & 횡단 구배(2.0%) 측량 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            광파 레벨기를 투입하여 강화노반 마무리면 계획고 오차를 <strong>&plusmn;10mm 이내</strong>로 관리하며, 표면 우수가 맹암거로 유도되도록 <strong><span class="term-highlight" onclick="openGlossary('cross_slope')">2.0% 횡단 경사</span></strong>를 검측합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-rose-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">STEP 5</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">노반 마무리면 요철 제거 & 인수대장 서명 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            노반 표면의 요철, 돌가루 및 불량토를 깨끗이 제거 조치하고, 감리단 입회 하에 강화노반 인수조치 측량 대장에 최종 확인 서명하여 궤도공으로 명확히 인수합니다.
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
# 3. WBS 13 CHECKLIST HTML
# =========================================================================
checklist_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 강화노반 확인 체크리스트</title>
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
        <h1 class="title">[HBS] 강화노반 확인 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-13 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 1.05rem; font-weight: 800;">📋 표준서 & 수행지침 연계 HBS 강화노반 필수 검측 항목</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 노반 지지력(K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa) 성적서 수령, PBT 평판재하시험, 마무리면 높이 오차(±10mm 이내) 및 횡단구배(2.0%) 배수 상태를 현장 감리 입회 하에 검측하기 위해 제작되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">표준서 & 수행지침 연계 필수 검측 항목 (KCS 47 10 25 수립)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:var(--accent-orange);">⚠️ 사전 준비<br>(Step 1~2 인수/시굴)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 서류 확인</span>
                        <strong>[지지력 성적서 원본 대조]</strong> <span class="term-highlight" onclick="openGlossary('k30_ev2')">K30 &ge; 110 MN/m³</span> 및 K70 &ge; 150 MPa/m 토공사 성적서 수령 점검
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 다짐도 검증</span>
                        <strong>[들밀도 상대다짐도 측량]</strong> 터파기 시굴 후 상대다짐도 <b>&ge; 95%</b> 현장 통과 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-red);">⚡ 본 검측<br>(Step 3~4 PBT/측량)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. PBT 재하시험</span>
                        <strong>[2차 변형계수(Ev2) 측정]</strong> <span class="term-highlight" onclick="openGlossary('pbt')">평판재하시험(PBT)</span> 시행, <b>Ev2 &ge; 120 MPa</b> (Ev2/Ev1 &le; 2.2) 검측 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 오차/구배 측량</span>
                        <strong>[높이 오차 & 횡단 구배]</strong> 마무리면 높이 오차(<b>&plusmn;10mm 이내</b>) 광파 측량 및 <span class="term-highlight" onclick="openGlossary('cross_slope')">횡단구배 2.0%</span> 배수 점검
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-green);">✅ 인수 마감<br>(Step 5 인수/서명)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 요철 제거</span>
                        <strong>[마무리면 요철 정리]</strong> 돌가루 및 불량토 현장 제거 후 마무리면 평탄화 정리 상태 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 인수대장 서명</span>
                        <strong>[강화노반 인수조치 대장 서명]</strong> 감리 입회 인수조치 측량 대장 서명 및 품질 보존 보관 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-13 콘크리트도상 [HBS] 강화노반 확인 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write to target paths
force_write(path_std, standard_html)
force_write(path_std_alt, standard_html)

force_write(path_gui, guideline_html)
force_write(path_gui_alt, guideline_html)

force_write(path_chk, checklist_html)
force_write(path_chk_alt, checklist_html)

print("\n🎉 SUCCESSFULLY BUILT WBS 13 [HBS] STRENGTHENED SUBGRADE MASTER HTML FILES!")
