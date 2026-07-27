import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Target absolute paths for WBS 12 (자재 반입)
target_base = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\12_자재 반입"

path_standard = os.path.join(target_base, "표준서", "자재 반입_표준서.html")
path_standard_alt = os.path.join(target_base, "표준서", "12_자재 반입_표준서.html")
path_checklist = os.path.join(target_base, "체크리스트", "자재 반입_체크리스트.html")
path_checklist_alt = os.path.join(target_base, "체크리스트", "12_자재 반입_체크리스트.html")

def force_write(path, text):
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✏️ Re-written WBS 12 Master: {path}")

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
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 자재검측 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<script>
const glossaryData = {
    'resin_fill': {
        title: '🧪 레일고정 액상수지 (Elastic Resin Fill)',
        desc: '일반 콘크리트가 아닙니다! 트램 홈레일(51R1) 측면 틈새에 액체 상태로 채워 넣어 탄성 고무로 경화시키는 2액형 유연 수지입니다.\\n1) 진동·소음 흡수: 도심지 트램 진동 차단\\n2) 누설전류(Stray Current) 절연: 지중 매설관 부식 방지\\n3) 수밀 고정: 빗물 침투 차단 및 레일 고정'
    },
    'special_turnout': {
        title: '🔀 외산 특수 분기기 (Special Foreign Turnout)',
        desc: '트램 차선 전환을 위한 전량 해외 수입 특수 분기기입니다. 콘크리트도상 반입 60일 전 해외 공장에서 3D 치수 및 작동 성능 검수를 마치고 국내 전용 컨테이너로 반입됩니다.'
    },
    'grooved_rail': {
        title: '🛤️ 그루브드레일 (Grooved Rail, 51R1/60R2)',
        desc: '도로 매설형 트램 선로에 사용되는 홈이 파인 특수 레일입니다. 전량 해외 수입 자재로, 콘크리트도상 시공 60일 전 공장 성적서(Mill Sheet) 검수 및 운반 조달 계획을 감리단과 의결해야 합니다.'
    },
    'pst_panel': {
        title: '🧱 PST 프리캐스트 슬래브 패널',
        desc: '공장에서 사전 제작되어 현장 반입되는 궤도용 콘크리트 슬래브 구조체입니다. 현장 반입 시 패널 치수 오차(±2.0mm 이내) 및 균열 흠집 여부를 정밀 계측하여 불량 시 즉시 반출합니다.'
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

standard_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 반입 기술 표준서</title>
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
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS 9000-6-12 Standard</span>
                <span class="bg-emerald-50 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">액상수지 & 외산 특수분기기 정밀 품질</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">자재 반입 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"콘크리트 자재 오해 방지: 레일고정 액상수지(탄성체), 외산 특수분기기 60일 전 공장검수 및 PST 패널 허용공차(±2mm) 관리"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-8">
        <!-- 💡 오해 방지 안내 박스 -->
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs sm:text-sm text-amber-900">
            <h4 class="font-bold text-amber-950 mb-1">💡 "콘크리트도상 자재 반입" 개념 정립</h4>
            <p class="leading-relaxed">
                본 공종의 자재는 일반 믹서트럭 콘크리트가 아닙니다! 트램 도로 매설 선로를 구성하는 <strong><span class="term-highlight" onclick="openGlossary('resin_fill')">레일고정 액상수지(탄성 절연재)</span>, <span class="term-highlight" onclick="openGlossary('special_turnout')">외산 특수 분기기</span>, <span class="term-highlight" onclick="openGlossary('grooved_rail')">그루브드레일(51R1/60R2)</span>, <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 프리캐스트 슬래브 패널</span>, 탄성 체결장치</strong> 등 핵심 매설 궤도 자재의 인수검사 및 현장 관리를 뜻합니다.
            </p>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">WBS 공정명</span>
                    <p class="font-bold text-slate-800 mt-1">콘크리트도상 / 자재 반입 (공사팀/자재팀/품질팀)</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">최종 품질 산출물</span>
                    <p class="font-bold text-slate-800 mt-1">자재인수검사 대장 | 공장시험성적서(Mill Sheet) | 불량재 반출서</p>
                </div>
            </div>
        </div>

        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 핵심 주요 자재별 정량 기술 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">자재 구획</th>
                            <th class="p-3 border border-slate-300 w-1/4 text-center">절대 공학 기준</th>
                            <th class="p-3 border border-slate-300 w-1/2 text-center">수행 조건 및 관리 기술 표준 (KCS 시방 연동)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">레일고정 액상수지<br>(Pourable Resin Fill)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">보관온도 15~25℃<br>절연저항 &ge; 10 M&Omega;</td>
                            <td class="p-3 border text-slate-600">• 주제:경화제 전용 비율 교반 후 2~4시간 내 고탄성 고무 경화.<br>• 트램 진동/소음 차단 및 누설전류(Stray Current) 지중 매설관 부식 방지 이중 절연성 확보</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">외산 특수 분기기<br>(Special Turnout)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">반입 60일 전 공장검수</td>
                            <td class="p-3 border text-slate-600">• 해외 전문 제조사(Vossloh 등) 조립 3D 치수 검수 완료 후 반입.<br>• 선로 전환기 인터페이스 및 부품 번호(Lot No.) 100% 대조</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">그루브드레일 (51R1/60R2)</td>
                            <td class="p-3 border text-center font-bold text-blue-700">직선도 1m당 &plusmn;0.2mm</td>
                            <td class="p-3 border text-slate-600">• 외산 매설 홈레일 현장 하차 시 레일 표면 흠집/균열 전수 점검.<br>• 공장 시험성적서(Mill Sheet) 원본 대조 및 감리 임회 검측</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border text-center">PST 슬래브 패널</td>
                            <td class="p-3 border text-center font-bold text-red-600">치수 공차 &plusmn;2.0mm 이내</td>
                            <td class="p-3 border text-slate-600">• 현장 반입 시 버니어 캘리퍼스로 패널 폭, 길이, 대각선 측정.<br>• 허용 공차 초과 및 모서리 휨/손상 자재는 현장 즉시 반출</td>
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

checklist_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 자재 반입 체크리스트</title>
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
        <h1 class="title">자재 반입 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-12 | 콘크리트도상 품질 검측대장</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; color: #065f46; font-size: 1.05rem; font-weight: 800;">📋 표준서 & 수행지침 연계 자재 인수 검측 항목</h4>
        <div style="font-weight: 600; line-height: 1.7; font-size: 0.9rem;">
            본 체크리스트는 외산 자재(그루브드레일/역상수지/외산 특수분기기) 60일 전 공장성적서 검수, 레일고정 액상수지 상온(15~25℃) 보관, 25Ton 장축 수송, PST 패널 허용공차(±2.0mm 이내) 및 불량재 현장 반출 처리를 검측하기 위해 제작되었습니다.
        </div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">시공 단계</th>
                <th style="width: 68%;">표준서 & 수행지침 연계 필수 검측 항목 (KCS 시방 수립)</th>
                <th style="width: 14%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="category" style="color:var(--accent-orange);">⚠️ 사전 리스크<br>(Step 1~2 반입 전)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#fef3c7; color:#92400e;">Step 1. 공장 검수</span>
                        <strong>[외산 자재 60일 전 검수]</strong> <span class="term-highlight" onclick="openGlossary('grooved_rail')">그루브드레일(51R1)</span>, <span class="term-highlight" onclick="openGlossary('resin_fill')">역상수지</span>, <span class="term-highlight" onclick="openGlossary('special_turnout')">외산 특수분기기</span> 공장 시험성적서(Mill Sheet) 원본 검토 및 감리 승인 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#e0f2fe; color:#0369a1;">Step 2. 운반 통제</span>
                        <strong>[25Ton 장축 수송 인허가]</strong> 경찰서/구청 도로점용 인허가, 심야 사인카 배치 및 신호수 조 수립 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-red);">⚡ 공사중 리스크<br>(Step 3~4 하차/적재)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#dcfce7; color:#166534;">Step 3. 인수 검측</span>
                        <strong>[PST 패널 치수 측량]</strong> 버니어 캘리퍼스 측정 <span class="term-highlight" onclick="openGlossary('pst_panel')">PST 슬래브 패널</span> 치수 허용공차(<b>&plusmn;2.0mm 이내</b>) 및 표면 흠집 감리 입회 검측 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#dbeafe; color:#1e40af;">Step 4. 액상수지 관리</span>
                        <strong>[액상수지 보관 & 현장 주입]</strong> 레일고정 액상수지 드럼 상온(<b>15~25℃</b>) 차광 보관, 2액형 정량 교반 및 레일 틈새 주입 수밀/절연 검측 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr>
                <td class="category" style="color:var(--accent-green);">✅ 공사후 리스크<br>(Step 5 반출/마감)</td>
                <td>
                    <div style="margin-bottom: 10px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 불량재 반출</span>
                        <strong>[불량 자재 현장 전량 반출]</strong> 규격 초과 및 변형 불량 자재 즉시 현장 밖으로 반출 트럭 회수 조치 여부
                    </div>
                    <div style="margin-bottom: 4px;">
                        <span class="step-tag" style="background:#f0fdf4; color:#15803d;">Step 5. 대장 서명</span>
                        <strong>[자재인수검사 대장 서명]</strong> 감리 입회 인수검사 대장 서명 완료 및 품질대장 영구 보존 등록 여부
                    </div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div style="text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        동탄도시철도(트램) 건설공사 | WBS 9000-6-12 콘크리트도상 자재 반입 마스터 체크리스트
    </div>
</div>
{common_modal_html}
</body>
</html>
"""

force_write(path_standard, standard_html)
force_write(path_standard_alt, standard_html)
force_write(path_checklist, checklist_html)
force_write(path_checklist_alt, checklist_html)

print("\n🎉 SUCCESSFULLY RESTORED WBS 12 MASTER STANDARD AND CHECKLIST FILES!")
