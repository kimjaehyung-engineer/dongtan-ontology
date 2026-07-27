import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\4_발주전략 KOM"

# Ensure target subdirectories exist
os.makedirs(os.path.join(target_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(target_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(target_base, "체크리스트"), exist_ok=True)

# -------------------------------------------------------------------------
# CONSTANT: Minimal Popups Styling (Design Lock Compliant)
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
# CONSTANT: Glossary popup modal layer and data script for KOM
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
    'kcs_47_30_00': {
        title: '📑 KCS 47 30 00 (궤도공사 표준시방)',
        desc: '국토교통부 제정 국가건설기준으로서 궤도재료(레일, 침목, 체결장치, 도상 콘크리트)의 규격, 시험법, 조립공차 및 품질 기준을 정밀 규정한 궤도공사 시공 마스터 시방서입니다.'
    },
    'grooved_rail': {
        title: '🛤️ 외산 홈레일 (Grooved Rail)',
        desc: '트램 매설궤도 구간에 주행로와 매설 도로 간 단차 극복을 위해 단면 내에 유도 홈(Groove)이 일체형으로 압연된 특수 레일입니다. 국내 제철소에서는 생산되지 않아 전량 오스트리아(Voestalpine) 등 유럽 현지에서 주문 제작 수입되므로 긴 리드타임(6개월 이상) 대응 전략이 필수적입니다.'
    },
    'bp_plant': {
        title: '🏭 가시공 B/P (Batching Plant)',
        desc: '현장 배합 설계에 따른 고품질 도상 콘크리트(TCL)를 안정적으로 연속 공급하기 위해 공사 현장 인근에 수배하는 전용 콘크리트 배치 플랜트(레미콘 공장) 설비 및 공급망 체계입니다.'
    },
    'q_agreement': {
        title: '🤝 품질 보증 합의서 (Quality Assurance Agreement)',
        desc: '하도급 협력사와 궤도 자재 조달 및 시공 시 준수해야 할 기하학 오차 편차와 품질 요구 사항을 확약하고, 하자 발생 시 책임 소소 및 무상 보수 의무를 정밀 명문화한 합동 보증 계약 문서입니다.'
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

# Force overwrite function
def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✅ Clean file written to: {path}")


# =========================================================================
# 1. WRITE STANDARD HTML (WBS 9000-6-4)
# =========================================================================
standard_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 발주전략 KOM 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        {minimal_style}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-4 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KCS 47 30 00 준수</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"동탄도시철도 콘크리트도상 궤도공사 발주조건 CP 적합성 및 주요 자재 조달 전략"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 과업 개요 및 목적 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">공종 / WBS 액티비티</span>
                    <p class="font-bold text-slate-800 mt-1">궤도 / 발주전략 KOM (Kick-Off Meeting)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">핵심 품질 보증</span>
                    <p class="font-bold text-slate-800 mt-1">품질확인서 획득 | 수입 홈레일 리드타임 대책 수립</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 궤도공사 발주전략 수립 및 발주조건 CP(Condition Precedent)적합 여부를 검토하여 하도급 협력사와의 품질 보증 체계를 사전에 구축함</p>
                <p><strong>⚙️ 수행 방법:</strong> <span class="term-highlight" onclick="openGlossary('kcs_47_30_00')">KCS 47 30 00</span> 시방 기준 준수. 궤도 자재 품질 확인서 확보 및 <span class="term-highlight" onclick="openGlossary('grooved_rail')">외산 홈레일 조달 리스크</span> 대응 전략 수립</p>
                <p><strong>📑 주요 산출물:</strong> KOM 의사록, <span class="term-highlight" onclick="openGlossary('q_agreement')">품질 보증 합의서</span></p>
            </div>
        </div>

        <!-- 2. KDS/KCS 궤도공사 정량적 기술 표준 및 발주 요건 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 궤도공사 정량적 시방 표준 및 발주 요건 표
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">기술 검속 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">관련 시방 및 검사 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">핵심 정량 기술 수칙 및 발주 요건</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">시방 기준 수립</td>
                            <td class="p-3 border text-center">KCS 47 30 00 궤도공사</td>
                            <td class="p-3 border font-semibold text-slate-700">• 궤도 주요 자재(60kg 레일, PST 패널, 체결장치 등)의 제작공장 품질확인서 및 공식 시험성적서 제출 의무화</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">자재 조달 전략</td>
                            <td class="p-3 border text-center">외산 홈레일(51R1/60R2) 조달</td>
                            <td class="p-3 border font-semibold text-slate-700">• 유럽 현지 제조사 주문 생산 리드타임(최소 6개월) 분석 및 해상 운송/통관 지연 리스크 방지 대응안 수립</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">가시설 검토</td>
                            <td class="p-3 border text-center"><span class="term-highlight" onclick="openGlossary('bp_plant')">가시공 B/P(Batching Plant)</span></td>
                            <td class="p-3 border font-semibold text-slate-700">• 현장 인근 레미콘 B/P 공급 적정성 평가 및 도상 콘크리트(fck ≥ 30 MPa) 조달 연속성 사전 적정성 검토</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 발주전략 KOM 핵심 프로세스 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 발주전략 KOM 검토 및 계약 진행 프로세스
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">발주전략 KOM 품질 검속 및 입찰 진행 프로세스</text>

                    <g transform="translate(50, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e3a8a">① 가시설 & 환경 분석</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 가시공 B/P 공급망 적정성 평가</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 발주시기/현설/여건 고려 분석</text>
                    </g>

                    <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

                    <g transform="translate(340, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">② 입찰 조건 및 공정 수립</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 사전 설계 공법 사양서 반영</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 현설명서 하자관리체크리스트</text>
                    </g>

                    <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

                    <g transform="translate(630, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">③ 계약 체결 & 품질 합의</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 구간별 노반 인도시기 고려 수립</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 오차 발생시 보수 의무사항 고지</text>
                    </g>

                    <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
                    <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">⚠️ 궤도 설치 후 합동점검 시 레일 선형 틀어짐 허용 오차 초과 시 보수 의무사항 안내</text>
                </svg>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-4 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(target_base, "표준서", "발주전략 KOM_표준서.html"), standard_html)
force_write(os.path.join(target_base, "표준서", "4_발주전략 KOM_표준서.html"), standard_html)


# =========================================================================
# 2. WRITE GUIDELINE HTML (WBS 9000-6-4)
# =========================================================================
guideline_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 발주전략 KOM 수행지침서</title>
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
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-4 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">3단계 정밀 수행 지침</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"가시공 B/P 적정성 및 외산 홈레일 조달 대응, 현설 하자관리방안 수립 가이드"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 하도급 협력사 선정 및 자재 발주 전략 분석을 통해 최적의 공사 착수 준비 상태 확보</p>
                <p><strong>⚙️ 세부 방법:</strong> 가시공 B/P 수급량 평가, 수입 홈레일 리드타임 관리, 특수 공법 반영 및 현장인도 일정에 연동한 노선 공정계획 수립</p>
                <p><strong>📋 최종 산출물:</strong> KOM 의사록, 품질 보증 합의서</p>
            </div>
        </div>
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure)
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 준비 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">공시설계 분석 및 B/P 적정성 검토</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>현장 인근 <span class="term-highlight" onclick="openGlossary('bp_plant')">가시공 B/P(Batching Plant)</span> 공급 능력, 품질 등 조달 적정성 전수 조사 및 검토</li>
                        <li>공사 발주시기, 발주내역, 입찰 현설조건, 노선 현장여건을 정밀 반영한 하도급 발주전략 분석 보고 수립</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 수행 단계 (입찰 및 현설)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">특화 공법 사양 반영 및 현설명서 작성</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>사전 검토 완료된 특수 궤도 설계 및 공법(<span class="term-highlight" onclick="openGlossary('grooved_rail')">외산 홈레일</span>, 프리캐스트 패널 등) 사양을 하도급 시방서에 반영</li>
                        <li>하자관리방안 및 품질 확보 특별 조항이 포함된 현장설명서(현설명서) 및 특기사항 체크리스트 작성</li>
                        <li>선행 토목 노반의 구간별 인도시기(인터페이스)를 반영한 궤도 노선 공정계획 수립</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 계약 및 관리 마감 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">합동점검 보수 의무사항 고지 및 협약 체결</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>궤도 설치 후 후행 인수를 위한 합동점검 시 레일 선형 및 틀어짐 허용오차 초과 발생 시 하도급사 보수 의무사항 고지</li>
                        <li>최종 Kick-Off Meeting 의사록을 수립하고, 계약서 하위 특약으로 <span class="term-highlight" onclick="openGlossary('q_agreement')">품질 보증 합의서</span> 날인 서명 체결</li>
                    </ul>
                </div>
            </div>
        </div>
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 하자 예방 및 위험관리 (Risk Management)
            </h2>
            <div class="bg-rose-50 p-5 rounded-xl border border-rose-200 text-sm text-slate-700 space-y-2">
                <p class="font-bold text-rose-900">⚠️ 주요 위험요인 및 방지대책:</p>
                <ul class="list-disc list-inside space-y-1 text-slate-600 text-xs sm:text-sm">
                    <li><strong>홈레일 수입 차질:</strong> 해외 제작사(유럽) 생산 지연 방지를 위해 정기 조달 트래킹 회의 진행</li>
                    <li><strong>합동점검 선형 불량:</strong> 궤도 완성면 오차 편차 사전 차단을 위한 다짐 및 체결력 확보 공사관리 실시</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-4 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(target_base, "수행지침", "발주전략 KOM_수행지침.html"), guideline_html)
force_write(os.path.join(target_base, "수행지침", "4_발주전략 KOM_수행지침.html"), guideline_html)


# =========================================================================
# 3. WRITE CHECKLIST HTML (WBS 9000-6-4 - Master Table Format)
# =========================================================================
checklist_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 발주전략 KOM 리스크 체크리스트</title>
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
        <h1 class="title">발주전략 KOM 리스크 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-4 | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">KCS 47 30 00 시방 기준 준수. 궤도 자재 품질 확인서 및 외산 홈레일 조달 리스크 대응 전략 수립.</div>
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
                    <div style="margin-bottom: 8px;">• <strong>[조달 지연/홈레일]</strong> 전량 수입되는 <span class="term-highlight" onclick="openGlossary('grooved_rail')">외산 홈레일</span>의 해상 물류 리드타임(최소 6개월) 분석 및 통관 차질 대책 수립 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[가시설/레미콘 BP]</strong> 도상 타설을 위한 인근 <span class="term-highlight" onclick="openGlossary('bp_plant')">가시공 B/P</span>의 공급 수급량 한계 및 기온 조건별 배합 설계 적정성 사전 검토 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[현장여건/발주분석]</strong> 발주시기, 발주내역, 입찰현설 조건 및 현장 노선 여건을 고려한 하도급 최적 발주전략 수립 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[시방 누락/특화공법]</strong> 사전 검토한 설계 사양 및 핵심 공법(PST 패널, 홈레일) 수칙이 하도급 계약서 및 시방서에 누락될 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[인도 지연/인터페이스]</strong> 토목 노반의 구간별 궤도 인도시기(인터페이스 일정) 불일치로 인한 궤도 공정계획 미동기화 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[현설 하자/체크리스트]</strong> 하자관리방안이 포함된 현장설명서(현설명서) 작성 및 특기사항 체크리스트 반영 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[의무 고지/합동점검]</strong> 궤도 설치 후 합동점검 시 레일 선형 및 틀어짐 허용오차 이상 발생 시 하도급 협력사 보수 의무사항 고지 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[보증 누락/계약 체결]</strong> Kick-Off Meeting 의사록 작성 및 하도급 특약 계약용 <span class="term-highlight" onclick="openGlossary('q_agreement')">품질 보증 합의서</span> 서명 날인 누락 리스크</div>
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

force_write(os.path.join(target_base, "체크리스트", "발주전략 KOM_체크리스트.html"), checklist_html)
force_write(os.path.join(target_base, "체크리스트", "4_발주전략 KOM_체크리스트.html"), checklist_html)

print("\n🎉 ALL WBS 9000-6-4 (발주전략 KOM) HTML FILES SUCCESSFULLY COMPILED AND WRITTEN CLEANLY!")
