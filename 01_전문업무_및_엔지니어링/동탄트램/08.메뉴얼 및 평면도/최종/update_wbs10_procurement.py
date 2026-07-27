import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WBS 10 Path
wbs10_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\10_자재 발주 요청"

# Ensure directories exist
os.makedirs(os.path.join(wbs10_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(wbs10_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(wbs10_base, "체크리스트"), exist_ok=True)

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
# CONSTANT: Glossary popup modal layer and data script for WBS 10
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
    'fat_test': {
        title: '🏭 공장 수락 검사 (FAT, Factory Acceptance Test)',
        desc: '자재 선적 전 제조업체의 공장에서 발주처, 감리단, 시공사 검사원이 참석하여 정밀 품질/성능 시험을 수행하고 성적서를 확인하는 제도입니다. 홈레일의 경우 단면 치수, 인장 강도 등을 FAT 단계에서 검수합니다.'
    },
    'gp_srm': {
        title: '💻 GP/SRM 시스템 (Global Procurement & Supplier Relationship Management)',
        desc: '회사의 전사적 자원 조달 및 공급망 관리 시스템입니다. 공급원 검본 요청, 자재 청구, 구매 주문(PO) 승인 프로세스가 통합 관리되며, 발주 요청 시 필수 품질 요건(성적서/FAT 조건)을 시스템 상에 필수 입력해야 합니다.'
    },
    'loss_factor': {
        title: '📈 자재 로스율 (Material Loss Factor)',
        desc: '시공 중 절단, 연마, 용접 부위 가공 등으로 불가피하게 손실되는 자재 수량을 고려하여 설계량에 가산해주는 가산 분율입니다. 트램용 레일의 경우 통상 2~3%의 로스율을 가산합니다.'
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
# WBS 10 STANDARD HTML (자재 발주 요청)
# =========================================================================
wbs10_standard = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 발주 요청 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-10 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 & EN 규격</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 발주 요청 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"지급자재 청구서(M/R), 공급원 승인 요청 및 선적 전 FAT 품질 규정"</p>
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
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 자재 발주 요청 (현장 공무팀 주관)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">자재청구서(M/R) | 공급원 승인요청서</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> 설계도서 및 표준시방서(KDS 47 30 00)에 부합하는 자재 사양과 수량을 산정하여 지급자재 청약 및 공급원 검토 승인 절차를 적기에 이행함</p>
                <p><strong>⚙️ 발주 및 청구 채널:</strong> 본사 <span class="term-highlight" onclick="openGlossary('gp_srm')">GP/SRM 시스템</span> 연동을 통한 구매 주문서 발급</p>
            </div>
        </div>

        <!-- 2. 정량적 자재 발주 표준 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 자재 발주서 승인 및 공급원 검토 기준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">표준 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 규격</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">자재 발주 조건 및 품질보증 표준</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">수입 홈레일 규격</td>
                            <td class="p-3 border text-center font-bold text-blue-700">EN 14811 규격 준수</td>
                            <td class="p-3 border text-slate-600">• 매설 궤도에 최적화된 51R1/60R2 홈레일 단면 규격 준수.<br>• 성분 분석 및 경도 시험성적서 필수 요구</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">자재 발주 로스율</td>
                            <td class="p-3 border text-center font-bold text-blue-700">레일류 <span class="term-highlight" onclick="openGlossary('loss_factor')">2% ~ 3%</span> 가산</td>
                            <td class="p-3 border text-slate-600">• 시공 시 발생하는 절단 및 가공 마진을 상쇄하기 위해 순설계량 대비 2%~3%의 할증률 적용</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">선적전 공장 검수</td>
                            <td class="p-3 border text-center font-bold text-red-600">FAT 입회 검수 필수</td>
                            <td class="p-3 border text-slate-600">• 주요 자재 선적 전 제조공장에 시공사/감리단 파견.<br>• <span class="term-highlight" onclick="openGlossary('fat_test')">FAT(공장수락시험)</span> 성적서 실시간 교부 명시</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 공급원 승인 프로세스 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 공급원 검토 승인 및 자재 청약 업무 프로세스
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 130" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="130" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    
                    <!-- Nodes -->
                    <!-- 1. 자재 수량 산출 -->
                    <rect x="30" y="35" width="150" height="60" rx="6" fill="#1e3a8a" stroke="#1e3a8a" stroke-width="1"/>
                    <text x="105" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">1. 소요 자재 산출</text>
                    <text x="105" y="80" text-anchor="middle" font-size="9" fill="#93c5fd">설계량 + 로스율(2~3%)</text>
                    
                    <!-- Arrow 1 -->
                    <path d="M 190 65 L 220 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 2. 자재청구서(M/R) 제출 -->
                    <rect x="230" y="35" width="150" height="60" rx="6" fill="#0284c7" stroke="#0284c7" stroke-width="1"/>
                    <text x="305" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">2. 청구서 및 서류 구비</text>
                    <text x="305" y="80" text-anchor="middle" font-size="9" fill="#bae6fd">FAT 계약 조건 명시</text>
                    
                    <!-- Arrow 2 -->
                    <path d="M 390 65 L 420 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 3. 공급원 승인 요청 -->
                    <rect x="430" y="35" width="150" height="60" rx="6" fill="#ea580c" stroke="#ea580c" stroke-width="1"/>
                    <text x="505" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">3. 공급원 승인 요청</text>
                    <text x="505" y="80" text-anchor="middle" font-size="9" fill="#ffedd5">감리단 검토 공문 제출</text>
                    
                    <!-- Arrow 3 -->
                    <path d="M 590 65 L 620 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 4. GP/SRM 발주 실행 -->
                    <rect x="630" y="35" width="140" height="60" rx="6" fill="#16a34a" stroke="#16a34a" stroke-width="1"/>
                    <text x="700" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">4. GP/SRM 최종 발주</text>
                    <text x="700" y="80" text-anchor="middle" font-size="9" fill="#dcfce7">본사 PO 승인 완료</text>
                    
                    <!-- Arrow 4 -->
                    <path d="M 780 65 L 810 65" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

                    <!-- 5. 납품 확보 -->
                    <rect x="820" y="35" width="60" height="60" rx="6" fill="#475569" stroke="#475569" stroke-width="1"/>
                    <text x="850" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">5. 입고</text>
                    <text x="850" y="80" text-anchor="middle" font-size="9" fill="#cbd5e1">납품 개시</text>
                    
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
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-10 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs10_base, "표준서", "자재 발주 요청_표준서.html"), wbs10_standard)


# =========================================================================
# WBS 10 GUIDELINE HTML (자재 발주 요청)
# =========================================================================
wbs10_guideline = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 발주 요청 수행지침서</title>
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
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-10 Guideline</span>
                <span class="bg-white text-emerald-950 text-xs font-bold px-3 py-1 rounded-full">공무 발주 실무</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 발주 요청 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"지급자재 물량 산출, 선적 전 FAT 공장 시험 조건 약정 및 공급원 승인 프로세스"</p>
        </div>
    </div>
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 개요 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> 시공에 필요한 주요 자재(60kg/m 레일, 51R1 홈레일, PST 패널)의 수량을 대조 산출하여 공급원 승인 필증을 득한 후 발주 공문을 정상 송부함</p>
                <p><strong>⚙️ 수행 주체:</strong> 현장 공무팀 주관 하에 본사 구매조달팀(GP/SRM 운영) 및 감리단 협의 진행</p>
            </div>
        </div>
        
        <!-- 2. 세부 절차 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 자재 발주요청 3단계 세부 수행 프로세스
            </h2>
            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <!-- STEP 1 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 물량 검토 및 계획 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">설계 도서 파악 및 자재 로스율 할증 계산</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.1. 주요 궤도 자재 산출 물량 검토</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">설계 도면과 시방서를 바탕으로 60kg/m 레일 및 51R1 홈레일, PST 패널의 노선별 소요 길이를 교차 산출한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.2. 자재 로스율(할증) 가산 검토</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">레일 용접 및 현장 곡선 가공 절단에 따른 자재 손실률을 반영하여 레일류의 경우 설계량 대비 <span class="term-highlight" onclick="openGlossary('loss_factor')">2% ~ 3%의 할증률</span>을 가산한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">1.3. 공사 일정 연동 반입 리드타임 산정</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">선행 노반 구조물 인도 시점 대비 최소 45일 전 자재 야적장 입고가 보장되도록 발주 시기를 셋업한다.</p>
                        </div>
                    </div>
                </div>
                
                <!-- STEP 2 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 발주서 작성 및 승인 요청 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">자재청구서(M/R) 및 공장검사(FAT) 조건 명시</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.1. 지급자재 청구서(M/R) 작성</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">정밀 산출된 규격과 수량을 명시한 자재청구서(M/R)를 기재하여 현장 소장의 최종 승인 필증을 구비한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.2. 공장 검사(FAT) 조건 및 성적서 필수 명시</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">발주 사양서 상에 선적 전 해외 제조 공장에서 입회 수행하는 <span class="term-highlight" onclick="openGlossary('fat_test')">공장수락시험(FAT)</span> 수행 조건과 공인 품질성적서의 조기 발행 조건을 필수 조항으로 명시한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.3. 공급원 검토 승인 요청서 제출</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">제조사의 기술 규격서, 공인 성적서, 카탈로그를 취합하여 감리단에 공식 공급원 승인 요청 공문을 제출한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">2.4. 본사 GP/SRM 시스템 발주 승인 요청</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">감리단 공급원 승인이 의결되면 본사 <span class="term-highlight" onclick="openGlossary('gp_srm')">GP/SRM 구매시스템</span>에 자재 청구 자료를 업로드하고 구매 계약서(PO) 발송을 요청한다.</p>
                        </div>
                    </div>
                </div>
                
                <!-- STEP 3 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 발주 공문 승인 및 대장 등록 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-3">승인 필증 확보 및 현장 대장 대조 관리</h3>
                    
                    <div class="space-y-4 text-xs sm:text-sm text-slate-600">
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">3.1. 감리단 공급원 승인 필증 원본 대장화</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">감리단으로부터 회부된 정식 승인 통보서(필증 원본)를 현장 공무 캐비넷에 대장화하고 스캔본을 시스템에 저장한다.</p>
                        </div>
                        <div class="border-l-2 border-slate-300 pl-3">
                            <h4 class="font-bold text-slate-900 text-sm">3.2. 입고 스케줄 업데이트 및 하역 크레인 배정</h4>
                            <p class="text-slate-600 text-xs sm:text-sm mt-0.5">제조처 선편 일정(Shipping Schedule) 통보를 모니터링하여 국내 야적장 하역 장비(지게차/크레인) 대기 조율을 시작한다.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-emerald-900/10 text-slate-800 p-6 text-center text-xs border-t border-slate-200">
        동탄도시철도(트램) 수행지침서 | WBS 9000-6-10 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
""".replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

force_write(os.path.join(wbs10_base, "수행지침", "자재 발주 요청_수행지침.html"), wbs10_guideline)


# =========================================================================
# WBS 10 CHECKLIST HTML (자재 발주 요청)
# =========================================================================
wbs10_checklist = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 발주 요청 체크리스트</title>
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
        <h1 class="title">자재 발주 요청 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-10 | 현장 내부 품질대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">자재 발주 수량 설계 대조, 공급원 승인 필증 원본 확인, 발주 공문 승인 요청, FAT 성적서 조항 명시 (수행지침 1:1 매칭 완료)</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KDS 47 30 00 시방 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[설계대조/수량산출]</strong> 60kg/m 레일, 51R1 홈레일, PST 패널의 설계 도서 대비 발주 수량 산출 적합 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[할증률/로스계산]</strong> 레일 절단 및 가공 마진에 따른 적정 로스 할증률(<span class="term-highlight" onclick="openGlossary('loss_factor')">2% ~ 3%</span>) 적용 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[리드타임/일정]</strong> 시공 45일 전 적치를 목표로 한 발주 리드타임 사전 확보 계획 수립 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[청구서/소장필증]</strong> 자재청구서(M/R) 작성 시 규격 오기 방지 및 현장소장 내부 승인 필증 구비 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[FAT/공장시험]</strong> 자재 구매 사양서 내 선적 전 <span class="term-highlight" onclick="openGlossary('fat_test')">FAT(공장 수락 시험)</span> 수행 조건 및 품질성적서 제출 의무 조항 명시 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[공급원/승인요청]</strong> 감리단 제출용 제조사 기술서, 실적증명서, 성적서를 첨부한 공급원 승인 요청 공문 회신 상태 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[시스템/PO승인]</strong> 감리 승인 접수 후 본사 <span class="term-highlight" onclick="openGlossary('gp_srm')">GP/SRM 시스템</span> 최종 청구 및 PO 발송 의뢰 완료 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[승인필증/대장화]</strong> 감리단 최종 자재 공급원 승인 필증(공문) 원본 현장 공무 대장 등록 및 시스템 업로드 여부</div>
                    <div style="margin-bottom: 8px;">• <strong>[입고준비/크레인]</strong> 선적 통보 접수 및 국내 입고 시 하역용 대형 크레인/지게차 배정 계획 수립 여부</div>
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

force_write(os.path.join(wbs10_base, "체크리스트", "자재 발주 요청_체크리스트.html"), wbs10_checklist)


# =========================================================================
# COPIER AUTOMATION FOR PREFIXED FILES (WBS 10 Only)
# =========================================================================
print("\n🔄 Running fast copier to sync prefixed files for WBS 10...")
shutil.copy(os.path.join(wbs10_base, "표준서", "자재 발주 요청_표준서.html"), os.path.join(wbs10_base, "표준서", "10_자재 발주 요청_표준서.html"))
shutil.copy(os.path.join(wbs10_base, "수행지침", "자재 발주 요청_수행지침.html"), os.path.join(wbs10_base, "수행지침", "10_자재 발주 요청_수행지침.html"))
shutil.copy(os.path.join(wbs10_base, "체크리스트", "자재 발주 요청_체크리스트.html"), os.path.join(wbs10_base, "체크리스트", "10_자재 발주 요청_체크리스트.html"))

print("💾 Synced WBS 10 Prefixed copies successfully.")
print("\n🎉 SUCCESSFULLY COMPLETED ALL WBS 10 FILE MIGRATIONS AND FAT SPECIFICATIONS!")
