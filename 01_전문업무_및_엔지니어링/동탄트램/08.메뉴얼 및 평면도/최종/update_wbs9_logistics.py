import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 9 Path
wbs9_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\9_자재조달계획 검토"

# Ensure directories exist
os.makedirs(os.path.join(wbs9_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(wbs9_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(wbs9_base, "체크리스트"), exist_ok=True)

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
# CONSTANT: Glossary popup modal layer and data script for WBS 9
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
    'grooved_rail': {
        title: '🛤️ 홈레일 (Grooved Rail, 51R1/60R2)',
        desc: '도심지 매설 궤도에 사용되는 요(凹)자형 홈이 파여진 특수 철도 레일입니다. 트램 차량의 차륜 플랜지가 궤도를 주행할 수 있도록 유도해주는 단면 형상을 지니고 있으며, 전량 유럽 국외 수입에 의존하므로 조달 계획 관리가 생명입니다.'
    },
    'pst_panel': {
        title: '🧱 PST 슬래브 패널 (Precast Slab Track Panel)',
        desc: '공장에서 사전 일체식으로 제작하여 현장 반입하는 콘크리트 궤도 슬래브 패널입니다. 현장 조립 속도가 매우 빠르나, 28일 기준 설계기준 압축강도가 최소 45 MPa 이상을 달성해야 열차 하중을 안전하게 분산시킬 수 있습니다.'
    },
    'omc': {
        title: '🤝 OMC 품질 시방 (Operation and Maintenance Agreement)',
        desc: '국산화가 불가능한 해외 수입 특수 궤도 자재에 대해, 제작사가 품질 등급, 화학 성분, 내마모성 시험 결과 등을 보증하고 유지 보수용 특기 사양을 약정한 정식 품질보증합의서입니다.'
    },
    'bl_document': {
        title: '🚢 선하증권 (B/L, Bill of Lading)',
        desc: '해상 운송 시 선박 회사에서 화주에게 발행하는 물품 수령증이자 소유권 문서입니다. 특수 홈레일 통관 승인을 위해 B/L 원본, 상업송장(Invoice), 제작사 시험성적서 등 선적 서류 구비가 필수적입니다.'
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
# WBS 9 STANDARD HTML (자재조달계획 검토)
# =========================================================================
wbs9_standard = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재조달계획 검토 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-9 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">OMC 품질보증 & 해상 물류 조달</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재조달계획 검토 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"특수 홈레일 및 PST 패널 해상운송, 공장 강도 검수 및 야적 승인 기준"</p>
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
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 자재조달계획 검토 (현장관리팀, 현장공사팀 주관)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">자재수급스케줄표 | 자재 공급 승인서(OMC 서약서)</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 외산 특수 자재의 수입 통관 일정 지연 리스크를 사전에 헤지하고, 노반 인도(Handover) 공정에 맞추어 적정 물량을 야적 보관함</p>
                <p><strong>⚙️ 조달 및 검수 대상:</strong> 유럽산 <span class="term-highlight" onclick="openGlossary('grooved_rail')">홈레일(51R1/60R2)</span>, 레일 체결구, 탄성 충전재 및 국내 제작 <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 슬래브 패널</span></p>
            </div>
        </div>

        <!-- 2. 정량적 자재 조달 기술 표준 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 주요 자재 공학 규격 및 통관 품질보증 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">자재 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">공학 품질 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">해상 운송 및 공장 검수 표준</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">유럽산 홈레일 (51R1/60R2)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">단면 오차 ±0.5mm 이하</td>
                            <td class="p-3 border text-slate-600">• 수입 레일의 단면 선형 정밀 측정.<br>• 화학 성분 분석 성적서 및 <span class="term-highlight" onclick="openGlossary('omc')">OMC 품질 시방</span> 확보 서명 확인</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">PST 슬래브 패널</td>
                            <td class="p-3 border text-center font-bold text-blue-700">fck &ge; 45 MPa 이상</td>
                            <td class="p-3 border text-slate-600">• 패널 공장 제작 시 28일 압축강도 정밀 비파괴/공시체 파괴 시험 검수.<br>• 철근 배근 간격 및 매설 앵커 볼트 정렬 상태 확인</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">체결장치 및 탄성충전재</td>
                            <td class="p-3 border text-center font-bold text-blue-700">국제 SIL 인증 규격 만족</td>
                            <td class="p-3 border text-slate-600">• 열차 하중 흡수용 탄성 충전재의 동탄성 계수 및 흡음 복원률 검증. 제작사 선적전 시험성적서 대조</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 해상 조달 물류 프로세스 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 유럽산 홈레일 해상 운송 및 조달 통관 흐름도
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="140" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    
                    <!-- Nodes -->
                    <!-- 1. 제작 공장 출하 -->
                    <rect x="30" y="40" width="140" height="60" rx="6" fill="#1e3a8a" stroke="#1e3a8a" stroke-width="1"/>
                    <text x="100" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">1. 유럽 제작처 출하</text>
                    <text x="100" y="85" text-anchor="middle" font-size="9" fill="#93c5fd">OMC 품질 검증</text>
                    
                    <!-- Arrow 1 -->
                    <path d="M 180 70 L 210 70" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 2. 선적 및 해상운송 -->
                    <rect x="220" y="40" width="140" height="60" rx="6" fill="#0284c7" stroke="#0284c7" stroke-width="1"/>
                    <text x="290" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">2. 선적 및 해상수송</text>
                    <text x="290" y="85" text-anchor="middle" font-size="9" fill="#bae6fd"><span class="term-highlight" onclick="openGlossary('bl_document')">B/L 선적 서류</span> 발행</text>
                    
                    <!-- Arrow 2 -->
                    <path d="M 370 70 L 400 70" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 3. 국내 세관 통관 -->
                    <rect x="410" y="40" width="140" height="60" rx="6" fill="#ea580c" stroke="#ea580c" stroke-width="1"/>
                    <text x="480" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">3. 세관 통관 검수</text>
                    <text x="480" y="85" text-anchor="middle" font-size="9" fill="#ffedd5">관세율 및 수량 실사</text>
                    
                    <!-- Arrow 3 -->
                    <path d="M 560 70 L 590 70" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 4. 현장 2차 야적장 -->
                    <rect x="600" y="40" width="140" height="60" rx="6" fill="#16a34a" stroke="#16a34a" stroke-width="1"/>
                    <text x="670" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">4. 국내 야적장 보관</text>
                    <text x="670" y="85" text-anchor="middle" font-size="9" fill="#dcfce7">부식/우천 방수 보호</text>
                    
                    <!-- Arrow 4 -->
                    <path d="M 750 70 L 780 70" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 5. 궤도 현장 가설 -->
                    <rect x="790" y="40" width="80" height="60" rx="6" fill="#475569" stroke="#475569" stroke-width="1"/>
                    <text x="830" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">5. 시공 투입</text>
                    <text x="830" y="85" text-anchor="middle" font-size="9" fill="#cbd5e1">적기 공급 실현</text>
                    
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
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-9 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs9_base, "표준서", "자재조달계획 검토_표준서.html"), wbs9_standard)


# =========================================================================
# WBS 9 GUIDELINE HTML (자재조달계획 검토)
# =========================================================================
wbs9_guideline = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재조달계획 검토 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        {minimal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-9 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">공정 연동 조달 계획</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재조달계획 검토 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"해상 운송 선적서류 및 통관 승인, PST 공장 생산 강도 및 야적장 보관 관리 수칙"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 외산 특수 자재(홈레일, 체결구 등)의 수입 해상 물류 조달 지연을 방지하고 국내 PST 생산 품질 및 야적장 2차 보관 수명 주기를 제어함</p>
                <p><strong>⚙️ 수행 주체:</strong> 현장관리팀 및 현장공사팀 주관 하에 본사 구매조달팀 지원 협력</p>
            </div>
        </div>
        
        <!-- 2. 세부 절차 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 자재조달 및 검수 3단계 세부 수행 프로세스
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 계획 수립 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">조달 마스터 스케줄 수립 및 야적 공간 대조 분석</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.1. 자재 수급 마스터 스케줄 검토</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">외산 <span class="term-highlight" onclick="openGlossary('grooved_rail')">홈레일</span>의 해상 선적 리드타임과 국내 <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 패널</span> 공장 생산 완료일을 산정하여 통합 조달 스케줄표를 수립한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.2. 노반 인도(Handover) 구역별 소요량 매핑</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">선행 구조물 토목 완료 구간의 면적 대비 소요 궤도 자재 수량을 동기화하여, 과잉 반입으로 인한 가설 적체 또는 조달 부족을 방지한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.3. 2차 야적장 규모 및 운송 인프라 평가</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">현장 야적이 불가할 때를 대비하여 차량기지 용접장 내 2차 보관 전용 야적 공간의 수용 능력과 인양 크레인 가동성을 검토한다.</p>
                        </div>
                    </div>
                </div>
                
                <!-- STEP 2 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 수행 단계 (서류 검토 및 품질 검수)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">선적서류·통관승인 확보, 공장 강도 검수 및 공급원 서명</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.1. 해상 선적서류 및 통관 승인서 구비 검토</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">세관 통관 병목을 해소하기 위해 <span class="term-highlight" onclick="openGlossary('bl_document')">선하증권(B/L)</span>, 인보이스, 패킹리스트 및 제작처 자체 검사성적서를 보세 운송 착수 전 사전 검증한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.2. PST 슬래브 패널 공장 생산 강도 및 배근 검수</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">PST 콘크리트 패널 제작 공장을 품질담당자가 방문하여 28일 압축강도(fck &ge; 45 MPa) 실측값 검증 및 앵커 플레이트 밀착 공차를 실사한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.3. 입항 수입 홈레일 단면 치수 정밀 오차 검수</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">부산/인천항 현장 입고 시 레일 단면 형상 치수(높이, 플랜지 폭)가 허용 한계 오차 편차 ±0.5mm 이내인지 버니어 캘리퍼스로 실측 대조한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.4. 자재 공급 승인서 및 OMC 약정서 발급</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">공학 시험 규격을 만족한 자재에 한해 최종 자재공급 승인서(Sign-off)를 발급하고, 수입 자재의 경우 <span class="term-highlight" onclick="openGlossary('omc')">OMC 품질 시방서</span>를 첨부하여 최종 문서화한다.</p>
                        </div>
                    </div>
                </div>
                
                <!-- STEP 3 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 국내 야적 보관 및 관리 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">야적장 방수/방습 보호 및 수급 대장 실시간 업데이트</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">3.1. 국내 2차 야적장 보관 관리 실태 합동 실사</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">야적장에 적치된 홈레일의 산화(녹 발생) 방지를 위해 하부 침목 받침대 설치 및 우천 보호 방수 천막 차광막 고정 상태를 주기적으로 합동 점검한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">3.2. 자재 수급 대장 및 공정율 연동 기록 등록</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">최종 인수 완료된 자재 명세를 본사 ERP 자재 관리 시스템에 등록하여, 노반 시공 진척율과 자재 조달 밸런스를 동기화한다.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-9 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs9_base, "수행지침", "자재조달계획 검토_수행지침.html"), wbs9_guideline)


# =========================================================================
# WBS 9 CHECKLIST HTML (자재조달계획 검토)
# =========================================================================
wbs9_checklist = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재조달계획 검토 체크리스트</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
            --border-color: #cbd5e1;
        }
        body {
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            padding: 30px 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 35px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .header {
            border-bottom: 2px solid var(--text-primary);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .title {
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0;
            color: #1e3a8a;
        }
        .meta {
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }
        .summary-box {
            background: #fdf2f8;
            border: 1px solid #fbcfe8;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #9d174d;
        }
        table {
            width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid var(--border-color);
            padding: 14px;
            font-size: 0.92rem;
            text-align: left;
        }
        th {
            background: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }
        .category {
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            width: 18%;
        }
        .pre-row { color: #0f172a; }
        .ing-row { color: #0f172a; }
        .post-row { color: #0f172a; }
        .label-pre { color: var(--accent-orange); font-weight: bold; }
        .label-ing { color: var(--accent-red); font-weight: bold; }
        .label-post { color: var(--accent-green); font-weight: bold; }
        .check-cell {
            text-align: center;
            vertical-align: middle;
            width: 15%;
            font-weight: bold;
            color: #1e3a8a;
        }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 15px;
        }
        {minimal_style}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">자재조달계획 검토 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-9 | 현장 내부 품질대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">특수 홈레일/PST 패널 조달 마스터 일정표 수립, 해상운송 선적서류/통관승인서 확보, PST 생산 강도(45MPa 이상) 및 홈레일 단면 검수, 야적장 2차 보관 점검</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 47 30 00 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[마스터 일정/수립]</strong> 특수 홈레일 수입 일정 및 PST 패널 조달 마스터 일정표 검토 수립 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[소요량 매핑/노반]</strong> 선행 노반 구조물 인도(Handover) 구역 면적과 현장 소요 자재 물량의 1:1 매칭 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[야적 인프라/크레인]</strong> 용접장 내 2차 보관 야적장 면적 및 중량물 인양용 크레인 규격 사전 확보 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[선적서류/통관승인]</strong> <span class="term-highlight" onclick="openGlossary('bl_document')">선하증권(B/L)</span>, 인보이스 등 해상 선적 서류 구비 및 관세청 통관 승인 확인 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[패널 강도/공장검수]</strong> <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 슬래브 패널</span> 공장 생산 28일 압축강도(fck &ge; 45 MPa) 달성 및 검수 성적서 적격 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[홈레일 치수/오차]</strong> 입항 수입 <span class="term-highlight" onclick="openGlossary('grooved_rail')">홈레일</span>의 단면 형상 치수 허용 오차 공차(±0.5mm 이하) 충족 여부 실측 검사</div>
                    <div style="margin-bottom: 8px;">• <strong>[자재 승인/OMC]</strong> 품질 보증을 위한 해외 제조사 공급 적격 검증 및 <span class="term-highlight" onclick="openGlossary('omc')">OMC 품질 시방서</span> 자재 공급 승인서 확인 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[야적 관리/우천 보호]</strong> 국내 2차 야적장 보관 시 레일 받침대 및 방수 덮개(차광막) 포설 상태 합동 점검 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[대장 갱신/ERP]</strong> 최종 합격 인수 물량의 본사 자재수급 관리 대장 시스템 실시간 기록 등록 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs9_base, "체크리스트", "자재조달계획 검토_체크리스트.html"), wbs9_checklist)


# =========================================================================
# COPIER AUTOMATION FOR PREFIXED FILES (WBS 9 Only)
# =========================================================================
print("\n🔄 Running fast copier to sync prefixed files for WBS 9...")
shutil.copy(os.path.join(wbs9_base, "표준서", "자재조달계획 검토_표준서.html"), os.path.join(wbs9_base, "표준서", "9_자재조달계획 검토_표준서.html"))
shutil.copy(os.path.join(wbs9_base, "수행지침", "자재조달계획 검토_수행지침.html"), os.path.join(wbs9_base, "수행지침", "9_자재조달계획 검토_수행지침.html"))
shutil.copy(os.path.join(wbs9_base, "체크리스트", "자재조달계획 검토_체크리스트.html"), os.path.join(wbs9_base, "체크리스트", "9_자재조달계획 검토_체크리스트.html"))

print("💾 Synced WBS 9 Prefixed copies successfully.")
print("\n🎉 SUCCESSFULLY COMPLETED ALL WBS 9 FILE MIGRATIONS AND SHIPMENT LOGISTICS!")
