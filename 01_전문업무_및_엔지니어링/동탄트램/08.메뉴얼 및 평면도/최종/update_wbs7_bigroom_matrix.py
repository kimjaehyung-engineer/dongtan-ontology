import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 7 Path
wbs7_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\7_작수전 Big Room 회의"

# Ensure directories exist
os.makedirs(os.path.join(wbs7_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(wbs7_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(wbs7_base, "체크리스트"), exist_ok=True)

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
# CONSTANT: Glossary popup modal layer and data script for Big Room
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
    'handover': {
        title: '🤝 노선 Handover (노선 인수인계)',
        desc: '선행 노반 토목공사 완료 후, 후행 궤도공사를 시작할 수 있도록 토목 시공 구간의 기하학적 선형, 고저 레벨, 종횡단 측량 성과를 대조·검증하여 상호 정식으로 인수인계하는 공정 인터페이스 단계입니다.'
    },
    'bigroom': {
        title: '🏢 Big Room 회의 (합동 의사결정 회의)',
        desc: '본사 공정/견적/설계 담당팀, 현장 관리자, 궤도 협력업체 및 선후행 토목·설비 협력업체가 한자리에 모여 공정 간 간섭 사항을 실시간으로 도면 조율하고 리스크 헤지 방안을 의결하는 통합 협의체 회의체입니다.'
    },
    'stray_current': {
        title: '⚡ 누설전류 (Stray Current)',
        desc: '트램 주행로인 레일(귀선로)에서 누설되어 주변 지중 매설 금속관로나 토목 철근 구조체로 흘러들어가 전기 화학적 부식을 유발하는 유도 전류입니다. 이를 방지하기 위해 부식 방지 다이오드 및 접지 배선 매설 계획이 필수적입니다.'
    },
    'test_strip': {
        title: '🧱 시험성토 (Test Strip, 시범 타설)',
        desc: '본 타설에 들어가기 전, 궤도 지지 쟈키의 안정성 및 콘크리트 유동성/재료분리 여부, 바이브레이터 밀실도를 검증하기 위해 본선 외 구역에 동일 시방 사양으로 사전 진행하는 모의 시범 타설 공정입니다.'
    },
    'action_log': {
        title: '📋 Action Item Log (조치 대장)',
        desc: '빅룸 회의에서 도출된 각 분야 간 리스크에 대한 종결을 추적하기 위해 [리스크 내용 - 헤지 방안 - 담당 부서 - 조치 완료일]을 테이블화하여 실시간 기록·배포·관리하는 공정 관리 대장입니다.'
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
# 1. WRITE STANDARD HTML (WBS 7 - 작수전 Big Room 회의)
# =========================================================================
wbs7_standard = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 작수전 Big Room 회의 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-7 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">6대 분야 사전 리스크 & 헤지 전략</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">작수전 Big Room 회의 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"본사/현장/협력사 협의체 간의 공정·품질·안전 간섭 병목 극복 사전 의결 기준"</p>
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
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명 / 주관</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 착수전 Big Room 회의 (현장소장 주관)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">인터페이스 표준 의결</span>
                    <p class="font-bold text-slate-800 mt-1">노반 Handover | 누설전류(Stray Current) 디오드 접지 | 루프센서 매설</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 부서 간 공정·품질·안전 인터페이스에서 발생하는 병목과 리스크를 사전 도출하고 해결책을 약정하여 궤도공사 종합 계획을 의결함</p>
                <p><strong>⚙️ 수행 방법:</strong> 본사/현장/협력사 6대 분야 합동 <span class="term-highlight" onclick="openGlossary('bigroom')">빅룸 회의</span> 개최. BIM 시각화 공정 검토, <span class="term-highlight" onclick="openGlossary('action_log')">Action Item Log</span> 작성 및 <span class="term-highlight" onclick="openGlossary('test_strip')">시범 타설(Test Strip)</span> 일정 확약</p>
            </div>
        </div>

        <!-- 2. 분야별 사전 리스크 및 헤지(Hedge) 방안 매트릭스 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 본사-현장 분야별 사전 리스크 및 헤지(Hedge) 방안 매트릭스
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/6 text-center">담당 부서</th>
                            <th class="p-3 border border-slate-300 w-5/12 text-center">예상 리스크 (Risk)</th>
                            <th class="p-3 border border-slate-300 w-5/12 text-center">리스크 헤지 방안 (Hedge)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <!-- 1. 공사 -->
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center" rowspan="3">① 공사<br>(현장 시공팀)</td>
                            <td class="p-3 border text-slate-700 font-medium">• 터널/교량 협소 구간 내 레미콘 및 타설 장비 교행 불가에 의한 공기 지연</td>
                            <td class="p-3 border text-slate-600">• 타설 진입/회차로(Turn-around) 및 시공 순서(양방향 vs 단방향) 확정. 진출입 동선 선행 확보</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 궤도 선형 세팅 후 타설 시 동바리/거푸집 변형 또는 변위 발생</td>
                            <td class="p-3 border text-slate-600">• 궤도 고정 쟈키(Jacking) 수량 및 설치 간격 강화. 타설 전/중/후 3단계 정밀측량 체계 구축</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 후속 공종(전기·신호) 관로/접지 공사 지연으로 인한 도상 타설 중단</td>
                            <td class="p-3 border text-slate-600">• 타설 전 매설물(접지, 드레인 등) 체크리스트 작성 및 3계통 완공 확인 후 타설 승인(Sign-off) 절차 도입</td>
                        </tr>
                        <!-- 2. 공무 -->
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center" rowspan="2">② 공무<br>(현장 공무/계약)</td>
                            <td class="p-3 border text-slate-700 font-medium">• 선행 구조물(토목) 완료 지연에 따른 궤도 착수 공기 단축 압박</td>
                            <td class="p-3 border text-slate-600">• 선행 완공 구간부터 순차적으로 구간별 간이 개시(Phasing) 공정표 수립. 돌관 작업비용 사전 변경계획 검토</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 레미콘/특수재 단가 상승 및 야간 작업에 따른 실행 예산 초과</td>
                            <td class="p-3 border text-slate-600">• 야간 공사에 따른 노무비/장비비 사전 실행 반영. 물량 변동(Loss율) 분석 및 시공사-협력사 간 내역 명확화</td>
                        </tr>
                        <!-- 3. 품질 -->
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center" rowspan="3">③ 품질<br>(현장/본사 품질)</td>
                            <td class="p-3 border text-slate-700 font-medium">• 운반 시간 과다에 따른 콘크리트 슬러리 저하, 재료분리 및 콜드조인트 발생</td>
                            <td class="p-3 border text-slate-600">• 지연제/유동화제 투입 배합 사전 시험성토(Test Strip) 실시. 레미콘 배차 확보 및 운반 시간 상한선(90분) 통제</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 도상 콘크리트 수화열 및 건조수축에 의한 초기 균열 발생</td>
                            <td class="p-3 border text-slate-600">• 신축이음(Joint) 설치 간격 및 컷팅(Sawing) 타이밍 준수. 피막/수윤 양생 계획 수립</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 궤도 체결구 부근의 다짐 마감 불량으로 인한 정밀도 미달</td>
                            <td class="p-3 border text-slate-600">• 바이브레이터 진동 시인 시공 지침 수립. 본사 품질팀 연계 초기 타설 구간 합동 점검 실시</td>
                        </tr>
                        <!-- 4. 안전 -->
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center" rowspan="3">④ 안전<br>(현장/본사 안전)</td>
                            <td class="p-3 border text-slate-700 font-medium">• 터널 내부 장비 배기가스 축적 및 산소 결핍, 조도 부족 사고</td>
                            <td class="p-3 border text-slate-600">• 터널 송풍 환기팬 설치 및 가스농도 측정기 배치. 이동식 고조도 조명탑 및 안전 신호수 의무 배치</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 펌프카 아웃트리거 지지력 부족 전두 및 레미콘 후진 충돌</td>
                            <td class="p-3 border text-slate-600">• 타설 바닥 지지력 사전 검토 및 받침목 필수 적용. 후방감지기/어라운드뷰 및 전담 유도원 배치</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 야간 연속 작업 및 협소 구간 내 작업자 누적 피로 사고</td>
                            <td class="p-3 border text-slate-600">• 스마트 헬멧 및 접근 경보 장구 활용. 본사 안전팀 사전 위험성평가(JSA) 공동 검토 및 교대조 편성</td>
                        </tr>
                        <!-- 5. 외주/자재 -->
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center" rowspan="2">⑤ 외주/자재<br>(구매조달팀)</td>
                            <td class="p-3 border text-slate-700 font-medium">• 파업, 출하 제한 또는 운송 거리에 따른 연속 타설 공급 중단</td>
                            <td class="p-3 border text-slate-600">• 메인 공급망 외에 예비 서브 B/P 2~3곳 사전 계약 체결. 타설일 전용 배차 물량 최종 확약서 수령</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 궤도 도상 타설 숙련공 부족에 의한 시공 조립 마감 불량</td>
                            <td class="p-3 border text-slate-600">• 협력사 핵심 기능공 사전 등록제 및 시공 장비(슬립폼 페이버 등) 사전 예비 부품 확보</td>
                        </tr>
                        <!-- 6. 본사 설계 -->
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center" rowspan="2">⑥ 본사 설계<br>(설계 지원팀)</td>
                            <td class="p-3 border text-slate-700 font-medium">• 터널/교량 배수구 위치와 도상 구배 불일치로 인한 배수 물고임</td>
                            <td class="p-3 border text-slate-600">• 배수 구배 상세도 BIM/3D 사전 조밀 검토. 현장 실측치 연동 숍드로잉(Shop Drawing) 즉시 보정</td>
                        </tr>
                        <tr>
                            <td class="p-3 border text-slate-700 font-medium">• 토목 신축이음부와 궤도 신축이음부 위치 불일치로 인한 구조 파손</td>
                            <td class="p-3 border text-slate-600">• 토목-궤도 간 구조물 이음부 위치 1:1 대응 매칭 검증 및 시공 지침 전달</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 인터페이스 연동 기술 시방 의결 수칙 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 노반-궤도 간 인터페이스 & 전기신호 매설 표준 의결 사항
            </h2>
            <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 text-sm space-y-3">
                <ul class="space-y-2 text-slate-600 list-disc list-inside">
                    <li><strong>노반 선형 인수 (<span class="term-highlight" onclick="openGlossary('handover')">Handover</span>):</strong> 토목 인계면 오차 측정 성과표를 검증하여 레벨 편차 ±10mm 이하 합격 구간에 대해서만 인수 의결한다.</li>
                    <li><strong>누설전류(Stray Current) 방지 배선:</strong> 부식 방지 디오드 접지선 매설 계획의 궤도 단면 상세도를 확인하고 1:1 접지 단자함 포설을 의결한다.</li>
                    <li><strong>신호 루프센서 포설:</strong> 타설 시 감지선 파손을 대비하여 고정 지그 규격 및 타설 전 도통 테스트 절차를 확약한다.</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-7 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

wbs7_guideline = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 작수전 Big Room 회의 수행지침서</title>
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
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-7 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">의사결정 프로세스</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">작수전 Big Room 회의 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"6대 분야 사전 리스크 매트릭스 승인, BIM 시각화 및 Action Item Log 관리 지침"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 본사, 현장, 품질/안전 및 궤도·선후행 공종 협력사 간 빅룸 의사결정 체계를 통해 부서 간 병목을 예방함</p>
                <p><strong>⚙️ 세부 방법:</strong> 6대 분야 리스크 매트릭스 상정 및 헤지 방안 의결, BIM/3D 도면 기반 동선 간섭 분석, <span class="term-highlight" onclick="openGlossary('action_log')">Action Item Log</span> 수립 및 본 타설 전 <span class="term-highlight" onclick="openGlossary('test_strip')">시범 타설(Test Strip)</span> 승인</p>
            </div>
        </div>
        
        <!-- 2. 세부 절차 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 빅룸(Big Room) 회의 3단계 수행 프로세스
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 자료 준비 및 조율</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">분야별 사전 검토 및 참석 소집 계획 수립</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>6대 분야 자료 제출:</strong> 공사, 공무, 품질, 안전, 외주/자재, 본사 설계 분야별 예상 리스크와 헤지 방안 사전 취합</li>
                        <li><strong>기본 공정 분석:</strong> 자재/장비 반입로 및 반입구 확보 시기 분석, 토목 노반 <span class="term-highlight" onclick="openGlossary('handover')">노선 Handover</span> 일정 사전 대조</li>
                        <li>현장소장(주관) 및 분야별 담당자(현장 및 본사 견적/설계/공정팀), 선후행 공종 협력업체 소집</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 회의 진행 (Big Room 합동 의결)</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">BIM 시각화 분석, 리스크 헤지안 승인 및 시범 타설 확정</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>시각화 자료 활용:</strong> BIM 및 3D/Zone별 공정도면을 스크린에 투사하여 구간별 타설 동선 및 장비 교행/공정 간섭 실시간 도면 조율</li>
                        <li><strong>리스크 매트릭스 의결:</strong> 수화열 균열 제어(품질), 터널 환기/조도(안전), 외산 홈레일 조달 및 슬립폼/FB 용접사(외주), 토목-궤도 신축이음 위치 매칭(설계)에 대한 최종 헤지 방안 의결</li>
                        <li><strong>시범 타설 확정:</strong> 본 타설 시공 전에 품질/안전 요건을 사전 검증하기 위한 <strong>시범 타설(Test Strip)</strong> 일정을 빅룸 회의 현장에서 최종 확정</li>
                        <li><strong>Action Item Log 수립:</strong> [리스크 내용 - 헤지 방안 - 담당자 - 완료 예정일]을 정밀 수록한 추적 조치 대장 작성</li>
                    </ul>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 결과 환정 및 모니터링</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">빅룸 회의록 배포 및 조치사항 추적</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>의사결정 사항이 수록된 빅룸 회의록을 배포하여 본사 담당팀 및 감리단 공람</li>
                        <li>인터페이스 대장 합동 서명 완료 및 Action Item Log 기반 미결사항의 주기적 이행 여부 추적 관리</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- 3. 리스크 예방 관리 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 빅룸 회의 운영 및 Output 도출 핵심 가이드
            </h2>
            <div class="bg-rose-50 p-5 rounded-xl border border-rose-200 text-sm text-slate-700 space-y-2">
                <ul class="list-disc list-inside space-y-1 text-slate-600 text-xs sm:text-sm">
                    <li><strong>BIM 기반 공정도 검토:</strong> 정적 토의를 금지하고 구간별 3D 도면 위에서 장비 진입 및 회차 공간을 실시간 검토할 것</li>
                    <li><strong>Action Item 추적:</strong> 회의 후 모든 담당 부서는 지정된 기한 내에 리스크 헤지 방안의 물리적 조치 성과를 입증할 책임이 있음</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-7 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs7_base, "수행지침", "작수전 Big Room 회의_수행지침.html"), wbs7_guideline)


# =========================================================================
# 3. WRITE CHECKLIST HTML (WBS 7 - 작수전 Big Room 회의 - Master Table)
# =========================================================================
wbs7_checklist = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 작수전 Big Room 회의 리스크 체크리스트</title>
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
        <h1 class="title">작수전 Big Room 회의 리스크 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-7 | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">6대 분야(공사, 공무, 품질, 안전, 외주, 설계) 사전 리스크 검토서 수립, BIM 공정도 분석 및 시범타설 일정 확정</div>
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
                    <div style="margin-bottom: 8px;">• <strong>[리스크 취합/의결 누락]</strong> 6대 분야(공사/공무/품질/안전/외주/설계)의 사전 리스크 매트릭스 자료 검토 및 상정 누락 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[일정 조정/반입구]</strong> 자재 및 대형 장비 반입로/반입구 사용 시기 조정 실패로 인한 현장 대기 지연 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[인수인계/Handover]</strong> 선행 토목 공정의 <span class="term-highlight" onclick="openGlossary('handover')">노선 Handover</span> 일정 오차 편차 검증 및 합동 측량 계획 누락 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[간섭 분석/BIM]</strong> 시각화 자료(BIM 또는 3D 도면) 부재로 인한 공정 간섭 및 협소 구간 교행 오류 리스크 (<span class="term-highlight" onclick="openGlossary('bigroom')">빅룸 회의</span>)</div>
                    <div style="margin-bottom: 8px;">• <strong>[자재 장비/외주조달]</strong> 해외 홈레일 조달 일정 지연 및 플래시버트 용접 장비/용접사 확보 지연 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[인터페이스/누설전류]</strong> <span class="term-highlight" onclick="openGlossary('stray_current')">누설전류 부식 방지 디오드 접지선</span> 매설 및 신호 루프 센서 감지선의 궤도 철근 간섭 리스크</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[품질 검증/시범타설]</strong> 본 타설 전 궤도 쟈키 및 배합 유동성을 검증하기 위한 <span class="term-highlight" onclick="openGlossary('test_strip')">시범 타설(Test Strip)</span> 일정 미확정 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[추적 관리/Action Log]</strong> 조치 대장(<span class="term-highlight" onclick="openGlossary('action_log')">Action Item Log</span>) 미작성으로 인한 리스크 조치 기한별 추적 모니터링 누락 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[문서화/인터페이스]</strong> 빅룸 회의록 작성 및 타분야 인터페이스 인수인계 대장의 합의 서명 누락 리스크</div>
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

force_write(os.path.join(wbs7_base, "체크리스트", "작수전 Big Room 회의_체크리스트.html"), wbs7_checklist)


# =========================================================================
# 4. COPIER AUTOMATION FOR PREFIXED FILES (WBS 7 Only)
# =========================================================================
print("\n🔄 Running fast copier to sync prefixed files for WBS 7...")
shutil.copy(os.path.join(wbs7_base, "표준서", "작수전 Big Room 회의_표준서.html"), os.path.join(wbs7_base, "표준서", "7_작수전 Big Room 회의_표준서.html"))
shutil.copy(os.path.join(wbs7_base, "수행지침", "작수전 Big Room 회의_수행지침.html"), os.path.join(wbs7_base, "수행지침", "7_작수전 Big Room 회의_수행지침.html"))
shutil.copy(os.path.join(wbs7_base, "체크리스트", "작수전 Big Room 회의_체크리스트.html"), os.path.join(wbs7_base, "체크리스트", "7_작수전 Big Room 회의_체크리스트.html"))

print("💾 Synced WBS 7 Prefixed copies successfully.")
print("\n🎉 SUCCESSFULLY COMPLETED ALL WBS 7 FILE MIGRATIONS WITH 6-DEPARTMENT MATRICES AND TEST STRIP PLAN!")
