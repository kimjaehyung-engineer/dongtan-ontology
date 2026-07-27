import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

# Target paths for WBS 11 (시공계획 수립)
target_base = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\11_시공계획 수립"

path_standard = os.path.join(target_base, "표준서", "시공계획 수립_표준서.html")
path_guideline = os.path.join(target_base, "수행지침", "시공계획 수립_수행지침.html")
path_checklist = os.path.join(target_base, "체크리스트", "시공계획 수립_체크리스트.html")

wbs11_guideline_dir = os.path.dirname(path_guideline)

# Copy user uploaded Jig Support image
brain_user_img = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.user_uploaded\media__1784954504670.png"
dst_img_path = os.path.join(wbs11_guideline_dir, "track_jig_support.png")

if os.path.exists(brain_user_img):
    shutil.copy(brain_user_img, dst_img_path)
    print(f"📦 Successfully copied Jig Support image to: {dst_img_path}")

def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Written Master WBS 11: {path}")

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
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 공법 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<script>
const glossaryData = {
    'jig_support': {
        title: '📐 궤광 지그 지지대 (Track Gauge & Leveling Jig Frame)',
        desc: '콘크리트 도상 시공 시 레일의 궤간(1,435mm) 및 수평 캔트를 정확히 유지해주는 트러스 구조의 특수 가설 지지 프레임입니다.\\n1) 궤간 고정: 타설 시 궤도 비틀림 방지\\n2) 부력 억제: 콘크리트 타설 유동성에 따른 궤광 들뜸 방지\\n3) 선로 중심선 정합: 스핀들 볼트 조율 시 다이얼 게이지 0점 정합'
    },
    'hbs_test': {
        title: '🧱 HBS 지지력 검증 (Hydraulic Base Support Test)',
        desc: '콘크리트 도상(TCL) 하부에 위치한 상부 강화 노반의 하중 지지력을 현장에서 시험하는 단계입니다. 평판재하시험(PBT)을 실시하여 노반 반력계수 K30 >= 110 MN/m3 이상을 달성했는지 시공 전 필수 검증해야 합니다.'
    },
    'thermit_weld': {
        title: '🔥 테르밋 용접 (Thermit Welding, EN 14730)',
        desc: '용접기나 전기 없이, 철가루와 알루미늄 가루를 혼합하여 화학반응 열(2,500도 이상)을 내서 벌건 쇳물을 만든 뒤, 이를 레일과 레일 사이의 틈새에 부어 굳혀서 붙이는 전통적이고 가장 강력한 철도 연결 공법입니다.'
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
# WBS 11 GUIDELINE HTML (궤광 지그 지지대 실무 도식 & 단면도 수록)
# =========================================================================
guideline_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 시공계획 수립 수행지침서</title>
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
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-11 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">현장 정밀 기술 매뉴얼</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">시공계획 수립 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"궤광 지그 지지대(Jig Support) 가설 및 5대 시공 마스터 프로세스 정밀 가이드"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 1. 작업 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 처음 업무를 맡은 직원도 5단계 시공 마스터 시퀀스, <strong><span class="term-highlight" onclick="openGlossary('jig_support')">궤광 지그 지지대(Jig Support)</span></strong> 가설 구조, 테르밋 용접 쇳물 조인트를 직관적으로 이해하여 감리 승인 득함</p>
                <p><strong>⚙️ 협업 부서:</strong> 현장 공사팀, 공무팀, 안전팀 및 품질팀 전원 의무 참여</p>
            </div>
        </div>

        <!-- 2. ★ 사용자 제공 실무 그림: 궤광 지그 지지대 (Jig Support) 도식 & 구조 해석 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 궤광 지그 지지대 (Track Jig Frame Support) 구조 및 역할
            </h2>
            
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-white shadow-xl img-card">
                <!-- 이미지 파트 -->
                <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 shadow-inner flex justify-center mb-4 overflow-hidden">
                    <img src="./track_jig_support.png" alt="궤광 지그 지지대 CAD 단면도" class="max-w-full h-auto object-contain rounded-lg border border-slate-800">
                </div>
                <div class="text-center font-bold text-amber-400 text-sm mb-5">
                    [도면 1] 궤광 지그 지지대(Jig Support) 트러스 체결 단면 구조도
                </div>

                <!-- 3대 공학 메커니즘 카드 -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">기능 1</span>
                        <h4 class="font-bold text-amber-300 text-sm mt-2">궤간(1,435mm) 정밀 고정</h4>
                        <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">
                            양쪽 레일 상단을 주황색 삼각 트러스 구조로 강체 연결하여 타설 전후 궤간 확폭 및 비틀림 오차(+3, -1mm 이내)를 완벽 통제합니다.
                        </p>
                    </div>

                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">기능 2</span>
                        <h4 class="font-bold text-sky-300 text-sm mt-2">중심선(Centerline) 캔트 정합</h4>
                        <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">
                            선로 중앙 수직 축(V-점)을 기준으로 좌우 궤도의 높낮이와 캔트 오차(&plusmn;2.0mm 이내)를 균형 있게 스핀들 조율에 연동해 줍니다.
                        </p>
                    </div>

                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="bg-emerald-500 text-white text-[10px] font-black px-2 py-0.5 rounded">기능 3</span>
                        <h4 class="font-bold text-emerald-300 text-sm mt-2">타설 시 부력/들뜸 억제</h4>
                        <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">
                            TCL 도상 콘크리트 타설 시 유동성 콘크리트 하중으로 인해 궤광이 위로 들뜨는 현상을 하부 강화노반 지지면에서 상쇄 지지해 줍니다.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. 시공계획 수립 5단계 마스터 체계도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 콘크리트도상 5대 시공 마스터 체계도 (Flow Architecture)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                <div class="flow-card bg-amber-50 p-4 rounded-xl border border-amber-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-amber-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 1</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">지반다짐·측량</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <span class="term-highlight" onclick="openGlossary('hbs_test')">K30 &ge; 110 MN/m³</span> 노반 시험 검증 및 3D CP 측량
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-amber-100 text-[10px] text-amber-800 font-bold">
                        🧱 노반 지지력 검증
                    </div>
                </div>

                <div class="flow-card bg-sky-50 p-4 rounded-xl border border-sky-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-sky-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 2</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">궤광 가조립·지그</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            25m 홈레일+침목 가조립, <strong><span class="term-highlight" onclick="openGlossary('jig_support')">궤광 지그 지지대</span></strong> 거치
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-sky-100 text-[10px] text-sky-800 font-bold">
                        📐 지그 프라이머 결합
                    </div>
                </div>

                <div class="flow-card bg-emerald-50 p-4 rounded-xl border border-emerald-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-emerald-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 3</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">스핀들 높이조율</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            스핀들 나사 수동 조정, 다이얼 게이지 <strong>&plusmn;0.5mm 0점</strong> 체결
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-emerald-100 text-[10px] text-emerald-800 font-bold">
                        ⚙️ 선형 정밀 조정
                    </div>
                </div>

                <div class="flow-card bg-orange-50 p-4 rounded-xl border border-orange-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-orange-500 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 4</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">테르밋 쇳물용접</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <span class="term-highlight" onclick="openGlossary('thermit_weld')">2,500℃ 테르밋 용접</span>, 비파괴 UT 굴곡 오차 &plusmn;0.2mm 검사
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-orange-100 text-[10px] text-orange-800 font-bold">
                        🔥 레일 장대화
                    </div>
                </div>

                <div class="flow-card bg-green-50 p-4 rounded-xl border border-green-200 flex flex-col justify-between space-y-3">
                    <div>
                        <span class="bg-green-600 text-white text-[10px] font-black px-2 py-0.5 rounded">STEP 5</span>
                        <h4 class="font-bold text-slate-900 text-xs mt-2">도상 콘크리트</h4>
                        <p class="text-[11px] text-slate-600 mt-1 leading-snug">
                            <span class="term-highlight" onclick="openGlossary('tcl_concrete')">TCL 콘크리트(&ge;30MPa)</span> 타설 및 감리 승인서 마감
                        </p>
                    </div>
                    <div class="bg-white p-2 rounded border border-green-100 text-[10px] text-green-800 font-bold">
                        ✅ 영구 매설 완공
                    </div>
                </div>
            </div>
        </div>

        <!-- 4. 세부 수행 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">4.</span> 5단계 세부 수행 프로세스 수칙
            </h2>
            <div class="space-y-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-amber-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">Step 1</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">지반 다짐 검증 & 3D CP 측량 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            상부 강화 노반의 평판재하시험(K30 &ge; 110 MN/m³) 성적서를 최종 검토하고 광파측량기로 3차원 노선 설계 좌표를 정밀 세팅합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-sky-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">Step 2</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">궤광 가조립 & 궤광 지그 지지대(Jig Support) 결합 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            25m 홈레일과 콘크리트 침목을 묶은 궤광 위에 <strong><span class="term-highlight" onclick="openGlossary('jig_support')">궤광 지그 지지대</span></strong>를 결합하여 트러스 구조로 단단히 고정 후 노반 상부에 안착시킵니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-emerald-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">Step 3</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">스핀들 높이 조율 & 다이얼 인디케이터 0점 정합 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            하부 스핀들 나사를 회전시켜 레일 캔트와 높이를 조율하며 다이얼 게이지 오차가 &plusmn;0.5mm 이내가 되도록 정합 후 락너트를 체결합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-orange-500 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">Step 4</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">레일 테르밋 쇳물 용접 & 비파괴 UT 검사 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            콘크리트 타설 전, 도가니 화학반응 2,500℃ 초고열 쇳물을 주입하여 장대레일 용접을 완료하고 초음파 비파괴 검사(UT)를 시행합니다.
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
                    <div class="bg-green-600 text-white font-black text-xs px-3 py-1.5 rounded-lg shrink-0 mt-0.5">Step 5</div>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">도상 콘크리트(TCL) 타설 & 준공 서명 수칙</h4>
                        <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                            TCL 도상 콘크리트(설계강도 &ge; 30 MPa)를 연속 타설하여 궤도를 매설 완료하고 감리 승인서를 득해 종합 마감합니다.
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

# Write WBS 11 master HTML files
force_write(path_guideline, guideline_html)

print("\n🎉 SUCCESSFULLY INTEGRATED TRACK JIG FRAME SUPPORT DIAGRAM INTO WBS 11 GUIDELINE!")
