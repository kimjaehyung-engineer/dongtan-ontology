import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\4_발주전략 KOM"

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
    'traffic_control': {
        title: '🚧 도심지 차도 통제 (Urban Traffic Control)',
        desc: '기존 차량이 주행 중인 도심지 차도 중앙에서 트램 궤도를 안전하게 타설하기 위해 도로 점용 인허가를 획득하고 방호벽, 라바콘, 신호수 등을 조밀 배치하여 차량 진입을 안전하게 차단/우회시키는 시공 교통안전 대책입니다.'
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

# Force write function
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
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"도심지 운행 차량 통제 하에서의 도상 타설 시공 요건 및 주요 자재 조달 전략"</p>
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
                    <span class="text-xs font-bold text-blue-700 uppercase">도심지 시공 조건</span>
                    <p class="font-bold text-slate-800 mt-1">기존 차도 전면/부분 통제 | 야간 연속 타설 동선 확보</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 기존 차량 운행 하에서의 도상 타설을 위한 교통안전대책 및 발주조건 CP 적합성을 정밀 검토하여 발주전략을 수립함</p>
                <p><strong>⚙️ 수행 방법:</strong> <span class="term-highlight" onclick="openGlossary('kcs_47_30_00')">KCS 47 30 00</span> 궤도공사 시방 준수. 외산 홈레일 조달 및 <span class="term-highlight" onclick="openGlossary('traffic_control')">도심지 차도 통제</span> 하에서의 안전 타설 수칙 수립</p>
                <p><strong>📑 주요 산출물:</strong> KOM 의사록, <span class="term-highlight" onclick="openGlossary('q_agreement')">품질 보증 합의서</span></p>
            </div>
        </div>

        <!-- 2. KDS/KCS 궤도공사 정량적 기술 표준 및 발주 요건 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 도심지 궤도공사 정량적 시방 표준 및 발주 요건 표
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
                            <td class="p-3 font-bold bg-slate-50 border text-center">차도 통제 및 가시설</td>
                            <td class="p-3 border text-center">도로점용허가 및 교통대책</td>
                            <td class="p-3 border font-semibold text-slate-700">• 도심지 차량 우회 조치 및 안전벽(PE 드럼, 라바콘) 배치 계획 수립. 작업 차선 외 주행 차량 보호용 방호막 완비</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">자재 조달 전략</td>
                            <td class="p-3 border text-center"><span class="term-highlight" onclick="openGlossary('grooved_rail')">외산 홈레일</span> 및 주요 부품</td>
                            <td class="p-3 border font-semibold text-slate-700">• 유럽 현지 생산 리드타임(최소 6개월) 분석 및 해상 통관 지연 대책. 현장인도 일정에 연동한 노선 공정계획 동기화</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">도상 콘크리트 B/P</td>
                            <td class="p-3 border text-center"><span class="term-highlight" onclick="openGlossary('bp_plant')">가시공 B/P</span> 수급성 검토</td>
                            <td class="p-3 border font-semibold text-slate-700">• 도심지 차량 정체 시 레미콘 연속 타설을 위한 공장 수급 적정성 및 타설 차량의 진입 동선 설계</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 도심지 차도 통제 타설 프로세스 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 도심지 궤도 타설 공정 교통 통제 프로세스
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">도심지 차도 통제 하의 궤도 타설 프로세스</text>

                    <g transform="translate(50, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e3a8a">① 사전 교통 허가 및 차단</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 우회로 확보 및 안전 인허가</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• PE 드럼 및 싸인카 배치 완료</text>
                    </g>

                    <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

                    <g transform="translate(340, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">② 운행중 차선점용 타설</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 타설 펌프카 작업 구획 확보</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 양생 초기 거동 차 주행 진동 관리</text>
                    </g>

                    <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

                    <g transform="translate(630, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">③ 차도 정상 복구 및 확인</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 잔재물 청소 및 안전펜스 철거</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 틀어짐 허용오차 합동점검</text>
                    </g>

                    <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
                    <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">⚠️ 도심지 공사 중 기존 주행 차량의 전방 시야 및 안전 보호 대책을 사전에 의무 반영할 것</text>
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
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">도심지 차도 통제 수칙</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">발주전략 KOM 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"기존 차량 주행 하에서의 도상 타설 시공 지침 및 교통 통제 안전 수칙"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 도심지 차량이 운행 중인 도로 중앙에서 안전을 완벽히 확보한 상태로 도상 콘크리트를 연속 타설하기 위한 수행 지침 수립</p>
                <p><strong>⚙️ 세부 방법:</strong> 교통 소통 및 안전 우회 대책 검토, 주야간 차도 점용 및 통제 승인 절차 반영, 차량 주행 진동에 따른 도상 초기 균열 예방 및 현장설명서 반영</p>
                <p><strong>📋 최종 산출물:</strong> KOM 의사록, 도심지 교통통제 및 시공계획 협의서</p>
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
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">교통소통 대책 및 도로점용 인허가 검토</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>도심지 기존 차량 통행 중 타설을 위한 도로점용/굴착 인허가 승인 여부 검토</li>
                        <li>주행 차량 보호를 위한 임시 안전 방호벽, 갈매기 표지판, 야간 신호용 싸인카 및 배치 계획 수립</li>
                        <li>레미콘 수송용 <span class="term-highlight" onclick="openGlossary('bp_plant')">가시공 B/P</span>의 도심지 정체 시 배송 한계 분석 및 우회로 확보</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 수행 단계 (차도 통제 타설)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">교통 차단 점용 및 도상 콘크리트 정밀 타설</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>차도 차단:</strong> 기 승인된 도로점용 계획에 따라 안전벽 설치 후 작업장 전용 점용구역 획득 (<span class="term-highlight" onclick="openGlossary('traffic_control')">차도 통제</span>)</li>
                        <li><strong>타설 동선:</strong> 타설용 펌프카와 레미콘 차량이 기존 통행 차선을 침범하지 않도록 안전 반경 펜스 보강 및 유도 신호수 밀착 배치</li>
                        <li><strong>진동 제어:</strong> 인접한 차로를 통과하는 기존 차량의 진동이 초기 도상 콘크리트 양생(28일 fck ≥ 30 MPa) 품질에 영향이 없도록 방진 대책 수립 및 주행 차량 감속 유도</li>
                        <li><strong>현설 조건 반영:</strong> 현장설명서(현설명서) 내에 "도심지 교통 통제 안전조치 및 타설 중 사고 방지 특기시방" 명기</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 복구 및 사후 관리 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">차도 정상 개방 및 선형 틀어짐 합동점검</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>타설 완료 직후 도로 표면의 슬러리 청소 및 교통 차단 가시설 철거 후 차도 정상 복구 개방</li>
                        <li>궤도 설치 직후 후행 점검에서 레일 선형 및 틀어짐 허용 오차 초과 시 협력사에 보수 의무를 즉각 조치 지시</li>
                        <li>조달 자재 품질성적 확인 후 KOM 의사록과 <span class="term-highlight" onclick="openGlossary('q_agreement')">품질 보증 합의서</span> 합동 날인 완료</li>
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
                    <li><strong>운행 차량 무단 침입:</strong> 야간 조명탑 설치 및 차단벽 시인성 강화로 타설 구역 차량 진입 차단</li>
                    <li><strong>양생 중 진동 균열:</strong> 대형 차량 우회 수립 및 작업 구간 감속 방지 턱 사전 조율</li>
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
        <div style="font-weight: bold; line-height: 1.6;">도심지 기존 운행 차량 안전 통제 및 우회로 구축, 타설 장비 진입 차선 확보, 품질보증합의 준수</div>
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
                    <div style="margin-bottom: 8px;">• <strong>[교통 통제/인허가]</strong> 도심지 기존 차량 통행 중 타설을 위한 도로점용 및 우회 조치 교통안전계획 인허가 미비 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[장비 동선/BP]</strong> 차도 점용 시 레미콘 및 펌프카의 현장 타설 진입 동선 및 통제 부스 설계 불량 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[수급 차질/홈레일]</strong> 전량 수입 수급인 <span class="term-highlight" onclick="openGlossary('grooved_rail')">외산 홈레일</span>의 조달 선적 및 입항 리드타임 지연 리스크</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[안전관리/차도 차단]</strong> 도심지 궤도 타설 중 기존 주행 차량 보호용 차단 안전벽(PE 드럼, 안내판) 배치 누락 리스크 (<span class="term-highlight" onclick="openGlossary('traffic_control')">차도 통제</span>)</div>
                    <div style="margin-bottom: 8px;">• <strong>[양생 하자/차량 진동]</strong> 인접 운행 차량 주행 진동이 초기 도상 콘크리트 양생(fck ≥ 30 MPa) 품질에 미치는 균열 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[계약 누락/특기사항]</strong> 도심지 시공 제한 및 안전 시방 조건이 현장설명서 및 특기 체크리스트에 누락될 리스크</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[도로 복구/민원 유발]</strong> 타설 후 도로 노면 청소 불량 및 통제 가시설 철거 지연에 따른 기존 주행 차도 개방 지연 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[보수 조치/합동점검]</strong> 궤도 설치 후 합동점검 결과 선형 및 틀어짐 허용 오차 초과 시 시공사의 보수 의무사항 고지 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[협약 지연/보증 계약]</strong> KOM 최종 의사록 수립 및 계약 특약용 <span class="term-highlight" onclick="openGlossary('q_agreement')">품질 보증 합의서</span> 날인 서명 누락 리스크</div>
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


# =========================================================================
# 4. AUTOMATED COPIER PROCESS (Eliminating token usage by 50%)
# =========================================================================
print("\n🔄 Starting fast automated copy process for prefixed files...")
shutil.copy(os.path.join(target_base, "표준서", "발주전략 KOM_표준서.html"), os.path.join(target_base, "표준서", "4_발주전략 KOM_표준서.html"))
shutil.copy(os.path.join(target_base, "수행지침", "발주전략 KOM_수행지침.html"), os.path.join(target_base, "수행지침", "4_발주전략 KOM_수행지침.html"))
shutil.copy(os.path.join(target_base, "체크리스트", "발주전략 KOM_체크리스트.html"), os.path.join(target_base, "체크리스트", "4_발주전략 KOM_체크리스트.html"))

print("💾 Copied prefix file: 4_발주전략 KOM_표준서.html")
print("💾 Copied prefix file: 4_발주전략 KOM_수행지침.html")
print("💾 Copied prefix file: 4_발주전략 KOM_체크리스트.html")

print("\n🎉 SUCCESSFULLY COMPLETED BOTH TRAFFIC CONTROL INJECTIONS AND 50% TOKEN REDUCTION SCHEME!")
