import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 7 Path
wbs7_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\7_작수전 Big Room 회의"

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
    'traffic_control': {
        title: '🚧 도심지 교통 소통 통제 (Traffic Control)',
        desc: '기존 차량이 다니는 도로에서 트램 공사를 수행하기 위해 차도를 안전하게 우회 및 부분 차단하고 안전펜스와 표지판을 조밀 배치하여 차량 정체와 안전사고를 동시 예방하는 공사 관리 지침입니다.'
    },
    'test_strip': {
        title: '🧱 시험성토 (Test Strip, 시범 타설)',
        desc: '본 타설에 들어가기 전, 궤도 지지 쟈키의 안정성 및 콘크리트 유동성/재료분리 여부, 바이브레이터 밀실도를 검증하기 위해 본선 외 구역에 동일 시방 사양으로 사전 진행하는 모의 시범 타설 공정입니다.'
    },
    'action_log': {
        title: '📋 Action Item Log (조치 대장)',
        desc: '빅룸 회의에서 도출된 각 분야 간 리스크에 대한 조치 성과를 실시간 기록·배포·관리하는 공정 관리 대장입니다.'
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
# WBS 7 STANDARD HTML (Re-aligned to show Traffic Control & Quality priorities)
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
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">도심지 교통 및 품질 관리 우선 의결</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">작수전 Big Room 회의 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"부서 합동 빅룸 회의를 통한 도심지 교통 통제 및 콘크리트도상 초기 균열 방지 전략"</p>
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
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명 / WBS 코드</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 착수전 Big Room 회의 (9000-6-7)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최우선 조율 안건</span>
                    <p class="font-bold text-slate-800 mt-1">도심지 교통 정체 차단 | 양생 균열 & 슬럼프 저하 방지 | 시범 타설</p>
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
                            <td class="p-3 border text-slate-600">• 타설 전 매설물 체크리스트 작성 및 3계통 완공 확인 후 타설 승인(Sign-off) 절차 도입</td>
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
                            <td class="p-3 border text-slate-600">• 메인 공급망 외에 예비 레미콘 공장 2~3곳 사전 계약 체결. 타설일 전용 배차 물량 최종 확약서 수령</td>
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

        <!-- 3. 핵심 의결 사항 (교통 통제 및 도상 품질 확보) -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 도심지 교통 통제 및 도상 타설 품질 표준 의결 사항
            </h2>
            <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 text-sm space-y-3">
                <ul class="space-y-2 text-slate-600 list-disc list-inside">
                    <li><strong>도심지 <span class="term-highlight" onclick="openGlossary('traffic_control')">교통소통 통제</span> 계획:</strong> 주야간 차도 점용 시간 및 작업 구간 안전벽PE 드럼 배치, 신호수 운용 방안을 수립하고 기존 교통 흐름 방해 최소화 계획 의결.</li>
                    <li><strong>콘크리트 슬러리/재료분리 관리:</strong> 도심 주행 정체로 인한 레미콘 배송 리드타임 90분 초과 금지 수칙 수립.</li>
                    <li><strong>초기 균열 방지:</strong> 양생 초기 도상판 상부에 가해지는 주행 차량 진동 충격을 차단하기 위한 감속 턱 배치 및 차량 유도 방안 확정.</li>
                    <li><strong>인수인계 선형 오차:</strong> 토목 노반 완료 후 <span class="term-highlight" onclick="openGlossary('handover')">노선 Handover</span> 기하 오차 편차 ±10mm 이내 검증 후 인수 의결.</li>
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

force_write(os.path.join(wbs7_base, "표준서", "작수전 Big Room 회의_표준서.html"), wbs7_standard)


# =========================================================================
# WBS 7 CHECKLIST HTML (Re-aligned to show Traffic Control & Quality priorities)
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
                    <div style="margin-bottom: 8px;">• <strong>[일정 조정/반입구]</strong> 자재 및 대형 장비 반입로/반입구 사용가능 시기 조정 실패로 인한 현장 대기 지연 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[인수인계/Handover]</strong> 선행 토목 공정의 <span class="term-highlight" onclick="openGlossary('handover')">노선 Handover</span> 일정 오차 편차 검증 및 합동 측량 계획 누락 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[간섭 분석/BIM]</strong> 시각화 자료(BIM 또는 3D 도면) 부재로 인한 공정 간섭 및 협소 구간 교행 오류 리스크 (<span class="term-highlight" onclick="openGlossary('bigroom')">빅룸 회의</span>)</div>
                    <div style="margin-bottom: 8px;">• <strong>[교통 통제/민원 유발]</strong> 도심지 기존 도로 차도 점용에 따른 교통 정체 관리 소홀 및 극심한 민원 유발 리스크 (<span class="term-highlight" onclick="openGlossary('traffic_control')">교통소통 통제</span>)</div>
                    <div style="margin-bottom: 8px;">• <strong>[시공 품질/양생 균열]</strong> 인접 주행 차량 진동에 따른 도상 초기 균열 및 운송 시간 과다(90분 초과) 슬럼프 저하 리스크</div>
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
print("\n🎉 WBS 7 STANDARDS SUCCESSFULLY UPDATED WITH REALIGNED RISKS!")
