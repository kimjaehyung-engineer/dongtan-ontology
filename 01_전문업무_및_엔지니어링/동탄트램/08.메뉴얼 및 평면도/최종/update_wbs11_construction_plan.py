import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 11 Path
wbs11_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\11_시공계획 수립"

# Ensure directories exist
os.makedirs(os.path.join(wbs11_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(wbs11_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(wbs11_base, "체크리스트"), exist_ok=True)

# -------------------------------------------------------------------------
# CONSTANT: Minimal Popups Styling
# -------------------------------------------------------------------------
minimal_glossary_style = """
    /* Glossary Modal Styles - Minimal Injection */
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
    .scene-link {
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        color: #059669 !important;
        font-weight: 700 !important;
        background: #ecfdf5 !important;
        border: 1px solid #10b981 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        font-size: 0.8rem !important;
        cursor: pointer !important;
        margin-left: 8px !important;
        transition: all 0.2s ease !important;
        text-decoration: none !important;
    }
    .scene-link:hover {
        background: #d1fae5 !important;
        color: #065f46 !important;
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
        max-width: 520px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        position: relative;
        animation: modalFadeIn 0.3s ease;
        text-align: left;
    }
    @keyframes modalFadeIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .glossary-close {
        color: #94a3b8;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.2s;
    }
    .glossary-close:hover {
        color: #334155;
    }
"""

# -------------------------------------------------------------------------
# CONSTANT: Glossary popup modal layer and data script for WBS 11
# -------------------------------------------------------------------------
common_modal_html = """
<!-- Glossary & Scene Popup Modal Layer -->
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

<script>
const glossaryData = {
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

function openScene(sceneKey) {
    openGlossary(sceneKey);
}

function closeGlossaryModal() {
    document.getElementById('glossaryModal').classList.remove('active');
}

// Esc close key handler
window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeGlossaryModal();
    }
});
</script>
"""

# Force write helper
def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Written Original: {path}")


# =========================================================================
# WBS 11 STANDARD HTML (시공계획 수립)
# =========================================================================
wbs11_standard = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 시공계획 수립 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        {minimal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-11 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">궤간 (+3, -1mm) & 캔트 관리</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">시공계획 수립 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"궤도공 전반의 시공계획서 의결, 노반 강도 검증 및 선형 오차 제어 한계선 수립"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 과업 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명 / 주관</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 시공계획 수립 (공사/공무/안전/품질 합동)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">궤도공사 시공계획서 | 품질보증계획서 | 안전보건계획서</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 트램 궤도 시공에 필요한 위치, 순서, 자재, 안전 통제 방법을 사전 수립하고 부서 간 인터페이스 병목을 방지함</p>
                <p><strong>⚙️ 검토 절차:</strong> 공사 합동 설명회 ➔ 주요 리스크 및 안전 유의사항 토의 ➔ 감리 승인 요청</p>
            </div>
        </div>

        <!-- 2. 정량적 시공 품질 기술 표준 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 콘크리트도상 선형 및 품질보증 정량 기술 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">선형 제어 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 상세 기술 표준 (KDS 47 30 00)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">궤간 (Track Gauge)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">+3mm, -1mm 이내</td>
                            <td class="p-3 border text-slate-600">• 1,435mm 표준궤 정밀 유지 관리.<br>• 궤광 인양 및 콘크리트 타설 전 스핀들 게이지 정밀 계측</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">캔트 (Track Cant)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">관리한계 ±2.0mm 이내</td>
                            <td class="p-3 border text-slate-600">• 설계 캔트(곡선 외선 레일 고저차 최대 160mm) 대비 오차는 ±2mm 이내로 엄격 제어 계획 수립</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">노반 지지력 검증</td>
                            <td class="p-3 border text-center font-bold text-red-600"><span class="term-highlight" onclick="openGlossary('hbs_test')">K30 &ge; 110 MN/m³</span></td>
                            <td class="p-3 border text-slate-600">• TCL 콘크리트 타설 전 하부 상부 강화 노반의 평판재하시험 성적서 승인 여부 사전 점검</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 시공 마스터 시퀀스 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 콘크리트도상 시공 마스터 시퀀스 흐름도
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 130" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="130" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    
                    <!-- Nodes -->
                    <!-- 1. HBS / 측량 -->
                    <rect x="20" y="35" width="140" height="60" rx="6" fill="#1e3a8a" stroke="#1e3a8a" stroke-width="1"/>
                    <text x="90" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">1. 노반 지지력 & 측량</text>
                    <text x="90" y="80" text-anchor="middle" font-size="9" fill="#93c5fd">K30 및 정밀 CP 측량</text>
                    
                    <!-- Arrow 1 -->
                    <path d="M 170 65 L 200 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 2. 궤광 조립 -->
                    <rect x="210" y="35" width="140" height="60" rx="6" fill="#0284c7" stroke="#0284c7" stroke-width="1"/>
                    <text x="280" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">2. 궤광 조립</text>
                    <text x="280" y="80" text-anchor="middle" font-size="9" fill="#bae6fd">스핀들 게이지 미세조정</text>
                    
                    <!-- Arrow 2 -->
                    <path d="M 360 65 L 390 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 3. 레일 테르밋 용접 -->
                    <rect x="400" y="35" width="140" height="60" rx="6" fill="#ea580c" stroke="#ea580c" stroke-width="1"/>
                    <text x="470" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">3. 레일 테르밋 용접</text>
                    <text x="470" y="80" text-anchor="middle" font-size="9" fill="#ffedd5"><span class="term-highlight" onclick="openGlossary('thermit_weld')">EN 14730 용접</span> & 비파괴</text>
                    
                    <!-- Arrow 3 -->
                    <path d="M 550 65 L 580 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 4. 도상 콘크리트 타설 -->
                    <rect x="590" y="35" width="140" height="60" rx="6" fill="#16a34a" stroke="#16a34a" stroke-width="1"/>
                    <text x="660" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">4. 도상 TCL 타설</text>
                    <text x="660" y="80" text-anchor="middle" font-size="9" fill="#dcfce7"><span class="term-highlight" onclick="openGlossary('tcl_concrete')">압축강도 &ge; 30 MPa</span></text>
                    
                    <!-- Arrow 4 -->
                    <path d="M 740 65 L 770 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 5. 최종 검측 마감 -->
                    <rect x="780" y="35" width="100" height="60" rx="6" fill="#475569" stroke="#475569" stroke-width="1"/>
                    <text x="830" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">5. 최종 선형 실사</text>
                    <text x="830" y="80" text-anchor="middle" font-size="9" fill="#cbd5e1">감리 승인 인수 인계</text>
                    
                    <!-- SVG marker defs -->
                    <defs>
                        <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
                        </marker>
                    </defs>
                </svg>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-11 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs11_base, "표준서", "시공계획 수립_표준서.html"), wbs11_standard)


# =========================================================================
# WBS 11 GUIDELINE HTML (시공계획 수립 - 시각적 현장 실사 사진 2대 내장 고도화)
# =========================================================================
wbs11_guideline = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 시공계획 수립 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        {minimal_style}
        .img-card {
            transition: all 0.3s ease;
        }
        .img-card:hover {
            transform: scale(1.01);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-11 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">실무 시각 가이드라인</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">시공계획 수립 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"초보자도 100% 한눈에 이해하는 실사 사진 기반 3단계 시공 수행 안내"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 처음 업무를 맡은 직원도 레일 뼈대(궤광) 배치 원리와 용접 쇳물 조인트를 사진으로 이해하여, 오류 없는 시공계획을 수립하고 감리 승인을 득함</p>
                <p><strong>⚙️ 협업 부서:</strong> 현장 공사팀, 공무팀, 안전팀 및 품질팀 전원 의무 참여</p>
            </div>
        </div>
        
        <!-- 2. 세부 절차 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 시공계획 수립 3단계 세부 수행 프로세스 (실물 사진 대조)
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 준비 및 지반/측량 검증 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">하부 노반 단단함 확인 및 3D 기준점 측량 좌표 설정</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.1. 하부 노반 지지력 (K30) 성적 검토</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5"><span class="term-highlight" onclick="openGlossary('hbs_test')">HBS 노반 지지력(K30 &ge; 110 MN/m³)</span> 시험 성적서 데이터를 검토하여 지반 안정을 정량적으로 검증한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.2. 궤도 선형 정밀 CP(기준점) 측량계 수립</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">광파기 및 정밀 GPS 기기를 사용한 궤도용 정밀 기준점(CP) 측량 성과물을 3차원 측지계 상에 셋업하고 보정한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.3. 통합 킥오프 설명회 개최</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">공무, 공사, 안전, 품질 및 협력사 책임자가 입회하여 공사 구획, 주간 단위 작업 스케줄, 안전 유의사항을 공유한다.</p>
                        </div>
                    </div>
                </div>
                
                <!-- STEP 2 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 시공 계획 수립 및 디테일 상세 검토 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">궤광 조립/조정 수칙 및 테르밋 용접(쇳물 접합) 계획 수립</h3>
                    
                    <div class="space-y-6 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.1. 궤광 조립(레일 뼈대 내려놓기) 및 스핀들 게이지(높낮이 조절 볼트) 미세조정 수칙</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">
                                침목과 레일을 사다리 모양으로 미리 조립해 둔 뼈대(궤광)를 크레인으로 지면에 임시로 내려놓은 뒤, 
                                <strong>나사식 높낮이 조절 볼트(스핀들 게이지)를 수동 렌치로 돌려가며 레일의 수평과 고저 높이를 미세하게 맞춘다.</strong> 
                                그 후 눈금바늘이 달린 기밀 측정기(다이얼 인디케이터 게이지)를 대고 바늘이 가리키는 눈금이 오차 한계(1mm 이내) 안으로 들어오는지 정밀 검측하도록 수칙을 기재한다.
                            </p>
                            <!-- 실사 야적 조립장 사진 탑재 -->
                            <div class="my-4 bg-slate-100 p-2.5 rounded-xl border border-slate-200 max-w-md img-card">
                                <img src="C:/Users/sskjh/.gemini/antigravity/brain/887aacfa-3165-4be1-8e89-29f90e47a298/rail_welding_yard_view_real_1784940360828.jpg" class="w-full h-auto rounded-lg shadow-sm" alt="궤도 야적 조립장 실사">
                                <p class="text-[11px] text-center text-slate-500 mt-1.5 font-bold">▲ 실제 궤광(침목과 레일 뼈대) 조립 및 보관이 이뤄지는 야적장 전경</p>
                            </div>
                        </div>
                        
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.2. 레일 테르밋 용접(화학반응 쇳물 주입 접합) 시방 설계</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">
                                가스나 전기 용접기를 쓰지 않고, <strong>도가니 그릇에 철가루와 알루미늄 가루를 혼합하여 넣은 후 불을 붙여 2,500도 이상의 화학반응 쇳물을 만들어낸 뒤, 이를 레일 연결 틈새에 흘려보내어 하나로 굳혀 붙이는 전통 용접 공법(<span class="term-highlight" onclick="openGlossary('thermit_weld')">테르밋 용접</span>)</strong>의 상세 시공 계획을 수립한다. 
                                용접 후에는 레일 표면을 평평하게 그라인더로 갈아내고 초음파 비파괴 검사(UT)를 거쳐 1m당 높낮이 굴곡 편차가 ±0.2mm 이내인지 확인하도록 규정한다.
                            </p>
                            <!-- 실사 테르밋 용접 사진 탑재 -->
                            <div class="my-4 bg-slate-100 p-2.5 rounded-xl border border-slate-200 max-w-md img-card">
                                <img src="C:/Users/sskjh/.gemini/antigravity/brain/887aacfa-3165-4be1-8e89-29f90e47a298/rail_welding_closeup_real_1784940372727.jpg" class="w-full h-auto rounded-lg shadow-sm" alt="테르밋 쇳물 용접 작업 실사">
                                <p class="text-[11px] text-center text-slate-500 mt-1.5 font-bold">▲ 실제 레일 연결부에 고온의 테르밋 쇳물을 주입하여 용접을 진행하는 현장 실사</p>
                            </div>
                        </div>
                        
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.3. TCL 도상 콘크리트 타설 동선 및 강도 계획</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5"><span class="term-highlight" onclick="openGlossary('tcl_concrete')">TCL 도상 콘크리트(압축강도 &ge; 30 MPa)</span>의 진동 크랙을 막기 위한 동선과 신구 콘크리트 콜드조인트 예방 타설 계획을 설계한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.4. 선형 오차(궤간, 캔트) 관리 한계선 설정</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">궤간 +3, -1mm 및 캔트 편차 ±2.0mm의 오차 한계를 현장 관리 상에 공학적으로 경고하는 오차 통제 모듈을 마스터 계획에 반영한다.</p>
                        </div>
                    </div>
                </div>
                
                <!-- STEP 3 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 인허가 승인 및 제출 마감 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">시공계획서 감리 승인 득 및 품질보증계획서 본사 제출</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">3.1. 감리단 궤도공사 시공계획서 및 안전보건계획서 최종 승인</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">공학적 검토 결과와 안전 지침을 바인딩한 시공계획서를 감리단에 공식 접수하고, 최종 적정 판정 승인서를 확보한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">3.2. 현장 품질보증계획서 본사 품질안전실 송부</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">감리 승인된 최종 마스터 계획서를 본사 시스템에 등록하고 영구 보존 대장화한다.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-11 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs11_base, "수행지침", "시공계획 수립_수행지침.html"), wbs11_guideline)

print("\n🎉 WBS 11 GUIDELINE VISUAL ENHANCEMENT COMPLETED SUCCESSFULLY!")
