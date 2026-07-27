import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\14_[HBS] 콘크리트 타설 및 양생"

path_std = os.path.join(target_dir, "표준서", "[HBS] 콘크리트 타설 및 양생_표준서.html")
path_std_alt = os.path.join(target_dir, "표준서", "14_[HBS] 콘크리트 타설 및 양생_표준서.html")

path_gui = os.path.join(target_dir, "수행지침", "[HBS] 콘크리트 타설 및 양생_수행지침.html")
path_gui_alt = os.path.join(target_dir, "수행지침", "14_[HBS] 콘크리트 타설 및 양생_수행지침.html")

path_chk = os.path.join(target_dir, "체크리스트", "[HBS] 콘크리트 타설 및 양생_체크리스트.html")
path_chk_alt = os.path.join(target_dir, "체크리스트", "14_[HBS] 콘크리트 타설 및 양생_체크리스트.html")

def force_write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Successfully written WBS 14 file: {path}")

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
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 시방 기술 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
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
# 1. WBS 14 STANDARD HTML
# =========================================================================
standard_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 콘크리트 타설 및 양생 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-14 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">HBR 압축강도 &ge; 21 MPa 품질 규격</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">[HBS] 콘크리트 타설 및 양생 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"강화노반 상부 기초콘크리트(HBR): 이격거리 4.8km 이내, 슬럼프 10cm 이하, 28일 압축강도 &ge; 21 MPa 및 7일 습윤 양생"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 💡 핵심 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs sm:text-sm text-amber-900">
            <h4 class="font-bold text-amber-950 mb-1">💡 [HBS] 기초콘크리트 타설 및 양생 수칙 개요</h4>
            <p class="leading-relaxed">
                본 공종은 강화노반 상부에 <strong><span class="term-highlight" onclick="openGlossary('hbr')">HBR 기초콘크리트</span></strong>를 타설하여 TCL 도상 및 반-PC 슬래브의 구조적 안정성을 확보하는 핵심 공종입니다. 레미콘 공장과의 <strong><span class="term-highlight" onclick="openGlossary('plant_distance')">이격거리 4.8km 이내(60분 타설)</span></strong> 확보, <strong><span class="term-highlight" onclick="openGlossary('slump_strength')">슬럼프 10cm 이하 및 28일 강도 21 MPa 이상</span></strong>, 거푸집 테이핑 시멘트풀 유출 방지 및 <strong><span class="term-highlight" onclick="openGlossary('curing_7days')">7일 습윤 부직포 양생</span></strong>을 준수합니다.
            </p>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / [HBS] 콘크리트 타설 및 양생 (현장 공사팀)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">HBR 콘크리트 품질시험표 | 양생온도일지 | 28일 강도시험 성적서</p>
                </div>
            </div>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> HBR 기초콘크리트 타설 정량 기술 표준 (KCS 14 20 10 연동)
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">품질 관리 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 상세 기술 표준 (KCS 시방 연동)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">레미콘 공장 이격거리</td>
                            <td class="p-3 border text-center font-bold text-blue-700">이격거리 &le; 4.8km 이내<br>(운반 60분 이내)</td>
                            <td class="p-3 border text-slate-600">• 현장 인근 4.8km 이내 배치플랜트 지정.<br>• 출하 후 60분 이내 현장도착 타설 완료하여 슬럼프 로스 차단</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">슬럼프 및 공기량</td>
                            <td class="p-3 border text-center font-bold text-blue-700">슬럼프 &le; 10cm 이하<br>공기량 4.5 &plusmn; 1.5%</td>
                            <td class="p-3 border text-slate-600">• 반창/펌프카 타설 시 슬럼프 10cm 이하 유지.<br>• 현장 도착 즉시 시공 직전 슬럼프 및 공기량 시험 필치</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">28일 압축강도</td>
                            <td class="p-3 border text-center font-bold text-red-600">&ge; 21 MPa 확보<br>(최소 18 MPa 이상)</td>
                            <td class="p-3 border text-slate-600">• 현장 몰드 시편 28일 압축강도 21 MPa 이상 확인.<br>• 미달 시 감리단 현장 봉인 및 재시험 조치 수립</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">양생 조건 및 두께 오차</td>
                            <td class="p-3 border text-center font-bold text-blue-700">습윤 부직포 7일 양생<br>두께 오차 &plusmn;10mm 이내</td>
                            <td class="p-3 border text-slate-600">• 타설 직후 습윤 부직포 포설 및 7일 이상 지속 살수.<br>• 거푸집 테이핑 시멘트풀 유출 방지 및 타설 두께 &plusmn;10mm 유지</td>
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
# 2. WBS 14 GUIDELINE HTML (Flexible 4-Step & Light Theme Diagrams)
# =========================================================================
guideline_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 콘크리트 타설 및 양생 수행지침서</title>
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

        <!-- 1. [Flexible Step Policy 적용] HBR 콘크리트 4단계 시공 프로세스 마스터 체계도 -->
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

        <!-- 2. [Light Theme Only Policy 적용] HBR 콘크리트 타설 & 양생 기술 도식 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> HBR 콘크리트 타설 & 양생 정밀 공학 기술 도식 (Light Theme)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 도식 1: HBR 콘크리트 타설 & 거푸집 유출방지 테이핑 구조 단면도 (소프트 라이트 배경) -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-blue-600 rounded-full inline-block"></span>
                                [도식 1] HBR 타설 & 거푸집 테이핑 단면도
                            </h3>
                            <span class="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">슬럼프 &le; 10cm</span>
                        </div>
                        
                        <!-- SVG Diagram 1 (Light Theme: #f8fafc background) -->
                        <div class="bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200">
                            <svg viewBox="0 0 420 220" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- 강화노반 기초 지층 -->
                                <rect x="30" y="160" width="360" height="40" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
                                <text x="210" y="185" font-size="10" font-weight="bold" fill="#78350f" text-anchor="middle">HBS 강화노반 지층 (K30 ≥ 110 MN/m³)</text>

                                <!-- HBR 타설 콘크리트 층 -->
                                <rect x="50" y="100" width="320" height="60" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                                <text x="210" y="135" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">HBR 기초콘크리트 타설층 (두께 오차 ±10mm)</text>

                                <!-- 좌우 거푸집 & 밀봉 테이핑 -->
                                <rect x="40" y="80" width="10" height="80" fill="#b45309"/>
                                <rect x="370" y="80" width="10" height="80" fill="#b45309"/>
                                <circle cx="45" cy="160" r="5" fill="#ef4444"/>
                                <circle cx="375" cy="160" r="5" fill="#ef4444"/>
                                <text x="25" y="70" font-size="8" font-weight="bold" fill="#ef4444" text-anchor="start">시멘트풀 유출 방지 테이핑</text>

                                <!-- 펌프카 슈트 & 바이브레이터 -->
                                <line x1="210" y1="20" x2="210" y2="100" stroke="#0284c7" stroke-width="5"/>
                                <path d="M 200 20 L 220 20 L 210 50 Z" fill="#0284c7"/>
                                <text x="210" y="15" font-size="9" font-weight="bold" fill="#0284c7" text-anchor="middle">레미콘 펌프카 슈트 (이격거리 ≤ 4.8km)</text>

                                <line x1="290" y1="50" x2="290" y2="120" stroke="#10b981" stroke-width="3" stroke-dasharray="3,2"/>
                                <rect x="286" y="115" width="8" height="20" fill="#10b981" rx="2"/>
                                <text x="345" y="65" font-size="8" font-weight="bold" fill="#047857" text-anchor="middle">고주파 바이브레이터 다짐</text>
                            </svg>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-100 text-xs text-blue-900 leading-relaxed">
                        <strong>⚙️ 타설 핵심:</strong> 거푸집 접합면을 테이핑 처리하여 시멘트풀 유출을 차단하고, 펌프카로 <strong>슬럼프 10cm 이하 콘크리트를 연속 타설</strong>하며 바이브레이터 밀실 고주파 다짐을 실시합니다.
                    </div>
                </div>

                <!-- 도식 2: 7일 습윤 부직포 포설 양생 & 강도 측정 도면 (소프트 라이트 배경) -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-md flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                            <h3 class="font-bold text-base text-slate-900 flex items-center gap-2">
                                <span class="w-3 h-3 bg-emerald-600 rounded-full inline-block"></span>
                                [도식 2] 7일 습윤 부직포 양생 & 강도 측정
                            </h3>
                            <span class="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase">강도 &ge; 21 MPa</span>
                        </div>
                        
                        <!-- SVG Diagram 2 (Light Theme: #f8fafc background) -->
                        <div class="bg-slate-50 p-4 rounded-xl flex justify-center items-center shadow-inner border border-slate-200">
                            <svg viewBox="0 0 420 220" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0" y="0" width="420" height="220" fill="#f8fafc"/>
                                
                                <!-- HBR 콘크리트 층 -->
                                <rect x="40" y="120" width="340" height="60" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
                                <text x="210" y="155" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">HBR 기초콘크리트 경화층</text>

                                <!-- 습윤 부직포 덮개 -->
                                <rect x="40" y="112" width="340" height="8" fill="#059669" opacity="0.85" rx="1"/>
                                <text x="210" y="105" font-size="10" font-weight="bold" fill="#047857" text-anchor="middle">7일 연속 습윤 부직포 덮개 포설</text>

                                <!-- 살수 튜브 분무 물방울 -->
                                <line x1="50" y1="80" x2="370" y2="80" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,3"/>
                                <circle cx="100" cy="95" r="3" fill="#38bdf8"/>
                                <circle cx="180" cy="95" r="3" fill="#38bdf8"/>
                                <circle cx="260" cy="95" r="3" fill="#38bdf8"/>
                                <circle cx="340" cy="95" r="3" fill="#38bdf8"/>
                                <text x="210" y="70" font-size="9" font-weight="bold" fill="#0284c7" text-anchor="middle">자동 분무 살수 튜브 (지속 습윤 양생)</text>

                                <!-- 몰드 강도 시험 공시체 -->
                                <g transform="translate(330, 20)">
                                    <rect x="0" y="0" width="30" height="40" fill="#94a3b8" stroke="#334155" stroke-width="1.5"/>
                                    <text x="15" y="-5" font-size="8" font-weight="bold" fill="#0f172a" text-anchor="middle">28일 몰드</text>
                                    <text x="15" y="24" font-size="7" font-weight="black" fill="#1e293b" text-anchor="middle">≥21MPa</text>
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

# =========================================================================
# 3. WBS 14 CHECKLIST HTML
# =========================================================================
checklist_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - [HBS] 콘크리트 타설 및 양생 체크리스트</title>
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
        <h1 class="title">[HBS] 콘크리트 타설 및 양생 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-14 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 1.05rem; font-weight: 800;">📋 표준서 & 수행지침 연계 HBR 콘크리트 필수 검측 항목</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 레미콘 공장 이격거리(4.8km 이내/60분 이내 도착), 거푸집 시멘트풀 유출 방지 테이핑, 현장 슬럼프(10cm 이하), 연속 타설 고주파 다짐 및 7일 습윤 부직포 양생, 28일 압축강도(≥ 21 MPa)를 현장 감리 입회 검측하기 위해 수립되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">표준서 & 수행지침 연계 필수 검측 항목 (KCS 14 20 10 수립)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:var(--accent-orange);">⚠️ 사전 준비<br>(Step 1~2 운반/테이핑)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 이격거리 통제</span>
                        <strong>[레미콘 이격거리 & 시간]</strong> 인근 <span class="term-highlight" onclick="openGlossary('plant_distance')">4.8km 이내 배치플랜트</span> 배정 및 레미콘 출하 후 <b>60분 이내</b> 현장 도착 타설 완료 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 거푸집 & 슬럼프</span>
                        <strong>[거푸집 테이핑 & 슬럼프]</strong> 시멘트풀 유출 방지 거푸집 테이핑 마감 및 현장 <span class="term-highlight" onclick="openGlossary('slump_strength')">슬럼프 10cm 이하</span> 시험 통과 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-red);">⚡ 본 타설<br>(Step 3 연속타설/다짐)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 연속 타설</span>
                        <strong>[콜드조인트 예방]</strong> 펌프카 중단 없는 연속 타설 시행 및 콜드조인트 발생 차단 관리 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 3. 고주파 다짐</span>
                        <strong>[바이브레이터 밀실 다짐]</strong> 고주파 꽂힘 바이브레이터 투입을 통한 콘크리트 내부 공극 제거 및 밀실 다짐 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-green);">✅ 양생 마감<br>(Step 4 습윤양생/강도)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 4. 두께 & 습윤양생</span>
                        <strong>[타설 두께 & 7일 습윤양생]</strong> 타설 두께 오차(<b>&plusmn;10mm 이내</b>) 및 <span class="term-highlight" onclick="openGlossary('curing_7days')">7일 연속 습윤 부직포</span> 포설 살수 양생 상태 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 4. 강도 성적서</span>
                        <strong>[28일 압축강도 승인]</strong> HBR 콘크리트 현장 몰드 28일 압축강도 <b>&ge; 21 MPa</b> 확보 및 감리 승인 대장 마감 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-14 콘크리트도상 [HBS] 콘크리트 타설 및 양생 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

# Force write to all targets
force_write(path_std, standard_html)
force_write(path_std_alt, standard_html)

force_write(path_gui, guideline_html)
force_write(path_gui_alt, guideline_html)

force_write(path_chk, checklist_html)
force_write(path_chk_alt, checklist_html)

print("\n🎉 SUCCESSFULLY BUILT WBS 14 [HBS] CONCRETE POURING & CURING MASTER HTML FILES!")
