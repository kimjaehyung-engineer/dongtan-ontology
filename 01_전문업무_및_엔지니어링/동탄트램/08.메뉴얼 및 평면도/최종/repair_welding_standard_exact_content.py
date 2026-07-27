import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

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
    'standard_rail': {
        title: '👷 정척레일 (Standard Rail)',
        desc: '제철소에서 압연 생산하여 반입되는 표준 길이의 단일 레일입니다. 한국도시철도 표준은 보통 25m 규격을 적용하며, 열차 주행 충격과 진동 소음의 원인이 되는 이음매를 줄이기 위해 용접장에서 여러 개를 이어 붙여 장대레일로 사전 가공합니다.'
    },
    'cwr': {
        title: '🛤️ 장대레일 (Continuous Welded Rail, CWR)',
        desc: '25m 정척레일의 끝단을 용접 접속하여 길이 200m 이상(트램의 경우 곡선 반경에 맞춰 수십 미터 단위도 포함)으로 연속시킨 궤도 레일입니다. 신축 이음매가 존재하지 않아 진동·소음이 획기적으로 차감되고 승차감이 우수하며, 레일 자체 신축 거동은 강력한 체결 장치와 도상 저항력으로 구속하여 흡수합니다.'
    },
    'thermit': {
        title: '🔥 테르밋 용접 (Thermit Welding)',
        desc: '알루미늄 분말과 산화철 분말의 발열 화학반응(2,000℃ 이상의 초고온)으로 생성되는 용융 철을 금형(몰드) 내부에 주입하여 레일 단면을 상호 융착 접합하는 현장 주조 용접 공법입니다. 전원 설비가 부족한 노선 현장에서 레일 조립 후 정밀 접속 시 주로 사용됩니다.',
        img: '../rail_welding_closeup.jpg'
    },
    'flash_butt': {
        title: '⚡ 플래시버트 용접 (Flash Butt Welding)',
        desc: '용접할 두 레일 단면 사이에 강한 전류를 흘려 불꽃(Flash) 아크 열로 강재 단면을 순간 융용시킨 후, 대용량 유압 잭으로 강한 압력을 주어 순간 접합하는 고성능 자동 기계식 용접법입니다. 인장 강도가 우수하고 품질 균질성이 매우 뛰어나 장대레일 기지 제작에 필수적으로 적용됩니다.',
        img: '../rail_welding_closeup.jpg'
    },
    'gas_pressure': {
        title: '💨 가스압접 (Gas Pressure Welding)',
        desc: '산소-아세틸렌 불꽃으로 레일 맞대기 단면을 고온(약 1,200℃, 용융점 이하)으로 균일 가열하여 연화시킨 후, 축방향 압축력을 주어 고체 상태에서 접촉면의 원자를 융합 접합하는 공법입니다. 용착 금속이나 전극 봉을 사용하지 않아 강재 조직 변형이 적은 특징이 있습니다.'
    },
    'ndt': {
        title: '🔍 비파괴검사 (Non-Destructive Testing, NDT)',
        desc: '용접부를 파괴하지 않고 내부 결함(미세 균열, 슬래그 혼입, 기포 등)을 검출하는 정밀 비파괴 검사입니다. 주로 초음파 탐상검사(UT) 및 자분 탐상검사(MT)를 적용하여 결함 지시가 없는 100% 합격 판정을 획득한 용접부만 현장 본선 부설로 공급할 수 있습니다.'
    },
    'yard': {
        title: '📐 레일 용접장 (Welding Yard)',
        desc: '반입된 25m 정척레일을 대용량 고정식 플래시버트/가스압접 장비 및 정밀 롤러대를 구축하여 장대레일(CWR)로 사전 대량 조립·제작하기 위해 궤도기지 내에 임시 마련하는 시공 전문 인프라 시설입니다.',
        img: '../rail_welding_yard_view.jpg'
    },
    'launching': {
        title: '🚚 장대레일 인양 및 인입 (Rail Launching)',
        desc: '사전 제작 완료된 200m 이상의 기다란 장대레일을 본선 궤도 현장 내부나 지하 터널 구간까지 롤러 베드 가이드를 따라 미끄러지듯 밀어 넣거나(Launching), 레일 전용 잭 크레인과 운반용 플랫카 열차 조합으로 수송 및 안치하는 정밀 기계화 시공 공정입니다.',
        img: '../rail_welding_yard_view.jpg'
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

standard_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 레일 용접장 선정 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        
        /* Glossary & Scene Popup CSS */
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
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-3 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 & KCS 47 30 00</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">레일 용접장 선정 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"동탄도시철도 콘크리트도상 레일 용접장 최적 입지 및 전용 설비 배치 절대 기준"</p>
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
                    <span class="text-xs font-bold text-blue-700 uppercase">공종 / 담당부서</span>
                    <p class="font-bold text-slate-800 mt-1">궤도 / 용접 | 현장 공무팀 / 궤도공사팀</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">핵심 정밀 공차</span>
                    <p class="font-bold text-slate-800 mt-1">수평 오차 ±1.0mm | 용접 직선도 ±0.2mm/1m | NDT 100%</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> <span class="term-highlight" onclick="openGlossary('standard_rail')">정척레일</span> 15본을 용접하여 200m 이상의 <span class="term-highlight" onclick="openGlossary('cwr')">장대레일</span>을 제작하는 작업장을 선정 (타분야 인터페이스 고려)</p>
                <p><strong>⚙️ 수행 방법:</strong> EN 14730 <span class="term-highlight" onclick="openGlossary('thermit')">테르밋</span> 및 EN 14587 <span class="term-highlight" onclick="openGlossary('flash_butt')">플래시버트 용접</span>을 위한 작업 공간 확보. 정척레일을 200m 장대로 용접하는 평탄 작업대 수평 오차 ±1mm 이내 확보.</p>
                <p><strong>📑 주요 산출물:</strong> 용접장 임시지정서, NDT 검사실 계획서</p>
            </div>
        </div>

        <!-- 2. 레일 용접장 선정 고유 정량 기술 표준 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 레일 용접장 선정 고유 정량적 기술 표준 및 허용 공차 <span class="scene-link" onclick="openScene('yard')">📸 용접장 전경 보기</span>
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">기술 검속 항목</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">관련 시방 및 검사 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">핵심 정량 기술 수칙 및 허용 공차</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">용접대 수평 평탄성</td>
                            <td class="p-3 border text-center">광학 레벨 검측</td>
                            <td class="p-3 border font-semibold text-slate-700">• 25m 레일 평탄 지지대 수평 오차 ±1.0mm 이내 정밀 통제</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">방풍 및 차광 설비</td>
                            <td class="p-3 border text-center">현장 환경 통제</td>
                            <td class="p-3 border font-semibold text-slate-700">• 용접 작업구간 풍속 2.0 m/s 이하 유도용 방풍 차단막 설치</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">비파괴검사 구역</td>
                            <td class="p-3 border text-center">NDT 작업 공간</td>
                            <td class="p-3 border font-semibold text-slate-700">• 감마선/초음파 검사를 위한 작업반 반경 방사선 안전거리 확보</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 레일 용접장 선정 핵심 프로세스 모식도 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 레일 용접장 선정 핵심 프로세스 및 구조 모식도
            </h2>
            <div class="svg-container bg-white border border-slate-200 rounded-xl p-4 text-center">
                <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                    <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
                    <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">레일 용접장 선정 및 설치 프로세스</text>

                    <g transform="translate(50, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e1b4b">① 작업대 기초 평탄 정밀 측정</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 광학 레벨 활용 정밀 측정</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 수평 오차 한계 ±1.0mm 관리</text>
                    </g>

                    <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

                    <g transform="translate(340, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">② 정척레일 종단 지지틀 조립</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 정척레일 고정 지지 롤러 베드</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• 종단 처짐 및 변형 방지 대책</text>
                    </g>

                    <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

                    <g transform="translate(630, 60)">
                        <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                        <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                        <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">③ 방풍 및 NDT 안전망 구축</text>
                        <text x="15" y="55" font-size="11" fill="#334155">• 풍속 2.0 m/s 이하 방풍 부스</text>
                        <text x="15" y="75" font-size="11" fill="#334155">• NDT 방사선 전용 검사실 이격</text>
                    </g>

                    <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
                    <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">⚠️ 용접 작업대 평탄성 오차 초과 시 장대레일 종단 영구 절곡 하자 발생</text>
                </svg>
            </div>
            <div class="mt-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs sm:text-sm text-slate-600">
                <strong>💡 핵심 요약:</strong> 용접 조인트의 기하학적 평탄성 확보 및 환경 변수 차단을 위해 전용 용접장의 환경 조건을 정밀 제어합니다.
            </div>
        </div>

        <!-- 4. 협력사 자문 및 공사관리 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">4.</span> 협력사 시공 / 공사관리 자문 (Subcontractor Advisory)
            </h2>
            <div class="bg-amber-50 p-5 rounded-xl border border-amber-200 text-sm text-slate-700 space-y-2">
                <p>📌 <strong>협력사 필수 이행 사항:</strong></p>
                <ul class="list-disc list-inside space-y-1 text-slate-600">
                    <li>테르밋/<span class="term-highlight" onclick="openGlossary('gas_pressure')">가스압접</span> 전문 자격증 보유자 현장 전담 배치 및 용접 설비 정밀도 교정필증 제출</li>
                    <li><span class="term-highlight" onclick="openGlossary('ndt')">비파괴검사(NDT)</span> 검사원의 전문 자격 확인 및 검사 성과표 감리원 정기 서명 획득</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-3 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
"""

standard_content_final = standard_content.replace("{modal_html}", common_modal_html)

# Overwrite Standard Files
fn1 = os.path.join(base_dir, "표준서", "레일 용접장 선정_표준서.html")
fn2 = os.path.join(base_dir, "표준서", "3_레일 용접장 선정_표준서.html")

with open(fn1, 'w', encoding='utf-8') as f:
    f.write(standard_content_final)
with open(fn2, 'w', encoding='utf-8') as f:
    f.write(standard_content_final)

print("🎉 Successfully compiled and overwrote standard files with perfect layout and content!")
