# -*- coding: utf-8 -*-
"""
동탄트램 중분대 연약지반 프리로딩 표준서 및 체크리스트 동기화 업데이트 스크립트
"""

import os

STANDARD_HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄도시철도 - 연약지반 처리공법 검토(필요시) 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 antialiased py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto space-y-8">
        
        <!-- Header Banner -->
        <div class="bg-slate-900 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
            <div class="absolute right-0 top-0 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="relative z-10 space-y-4">
                <div class="flex flex-wrap items-center gap-3">
                    <span class="bg-amber-400 text-slate-950 font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">WBS 9000-1-8</span>
                    <span class="bg-slate-800 text-slate-300 font-bold text-xs px-3 py-1 rounded-full">상부강화노반 기술 표준서</span>
                    <span class="bg-emerald-500/20 text-emerald-400 font-bold text-xs px-3 py-1 rounded-full">동탄도시철도 건설사업</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-black tracking-tight">연약지반 처리공법 검토(필요시) 기술 표준서</h1>
                <p class="text-slate-400 text-sm max-w-3xl leading-relaxed">
                    동탄트램 도로 중앙분리대(중분대) 구간 연약층 존재 시 압밀해석을 통한 <strong>잔류침하량 기준 10cm(≤100mm)</strong> 확보, <strong>가설 톤마대 옹벽 거치 후 프리로딩(여성토) 재하</strong> 기술 표준
                </p>
            </div>
        </div>

        <!-- 4대 관리 KPI Summary Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                <div class="text-xs font-bold text-amber-600 uppercase tracking-wider">품질 관리 (Q)</div>
                <div class="text-sm font-black text-slate-900">잔류침하량 &le; 10cm (100mm) 압밀도 &ge; 85% 확보</div>
            </div>
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                <div class="text-xs font-bold text-emerald-600 uppercase tracking-wider">안전 관리 (S)</div>
                <div class="text-sm font-black text-slate-900">가설 톤마대 옹벽 붕괴 및 차도 토사유출 100% 차단</div>
            </div>
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                <div class="text-xs font-bold text-blue-600 uppercase tracking-wider">공정 관리 (T)</div>
                <div class="text-sm font-black text-slate-900">프리로딩 방치기간(90~150일) CPM 마일스톤 준수</div>
            </div>
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                <div class="text-xs font-bold text-purple-600 uppercase tracking-wider">계측/원가 관리 (C)</div>
                <div class="text-sm font-black text-slate-900">쌍곡선법 실측 침하 판정 및 사토 유용 극대화</div>
            </div>
        </div>

        <!-- 기술사양 및 설계 기준 테이블 -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-4 p-6">
            <div class="flex items-center gap-2 border-b border-slate-100 pb-4">
                <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                <h2 class="font-bold text-lg text-slate-900">중분대 연약지반 프리로딩 공학 기술사양 및 설계 기준</h2>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <tbody>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800 bg-slate-50/50 w-1/4">적용 기준</td>
                            <td class="px-6 py-4 text-slate-600">KCS 11 30 00 연약지반개량공사, KDS 11 00 00 지반설계기준, 철도설계기준 노반편</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800 bg-slate-50/50 w-1/4">허용 잔류침하량</td>
                            <td class="px-6 py-4 text-slate-600 font-bold text-amber-700">트램 궤도 부설 후 공용 기간 잔류침하량 &le; 10cm (100mm) 엄수</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800 bg-slate-50/50 w-1/4">가설 옹벽 규격</td>
                            <td class="px-6 py-4 text-slate-600">1.0ton 규격 고강도 P.P 톤마대 계단식 3~4단 적치, 결속선 및 방진망 설치</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800 bg-slate-50/50 w-1/4">프리로딩 여성토</td>
                            <td class="px-6 py-4 text-slate-600">여성토 높이 H = 1.5~3.0m 양질토 성토 (일일 성토고 &le; 30cm, 층다짐 95% 이상)</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800 bg-slate-50/50 w-1/4">수평 배수층</td>
                            <td class="px-6 py-4 text-slate-600">Sand Mat (두께 50cm, k &ge; 1.0 &times; 10⁻² cm/s) + 지오텍스타일 부직포</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800 bg-slate-50/50 w-1/4">압밀 완료 기준</td>
                            <td class="px-6 py-4 text-slate-600">침하속도 &le; 1.0mm/8일 수렴, 쌍곡선법 예측 압밀도 85% 이상 달성</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3단계 표준 작업 프로세스 (Phases) -->
        <div class="space-y-4">
            <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-full bg-slate-900"></div>
                <h2 class="font-bold text-lg text-slate-900">3단계 표준 작업 프로세스 (Standard Procedure)</h2>
            </div>
            <div class="space-y-4">
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-slate-800 text-amber-400 font-bold text-xs px-2.5 py-1 rounded">PHASE 1</span>
                        <h3 class="font-bold text-base text-slate-900">지반조사 분석, 압밀해석 및 Sand Mat/계측기 설치</h3>
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">
                        시추주상도 및 실내 압밀시험 데이터 기반 Terzaghi 1차 압밀해석 수행, 잔류침하량 10cm 이하 설계를 위한 여성토 높이 결정, Sand Mat(두께 50cm) 포설 및 침하판/간극수압계 설치.
                    </p>
                </div>
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-slate-800 text-amber-400 font-bold text-xs px-2.5 py-1 rounded">PHASE 2</span>
                        <h3 class="font-bold text-base text-slate-900">가설 톤마대 옹벽 축조 및 내측 프리로딩(여성토) 재하</h3>
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">
                        중분대 외곽 1.0ton 마대 옹벽 3단 적치로 차도 토사유출 차단, 내측에 1.5~3.0m 높이로 양질토를 단계별 성토(30cm 층다짐)하여 조기 압밀 하중 재하.
                    </p>
                </div>
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-slate-800 text-amber-400 font-bold text-xs px-2.5 py-1 rounded">PHASE 3</span>
                        <h3 class="font-bold text-base text-slate-900">실시간 침하 계측, 압밀 완료(잔류침하 &le; 10cm) 판정 및 여성토 반출</h3>
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">
                        쌍곡선법 실측 침하량 회귀분석으로 잔류침하 10cm 이하 및 침하율 1mm/8일 수렴 확인, 감리원 승인 후 여성토 굴착 반출 및 K30&ge;110 지지력 검측 후 본선 인수인계.
                    </p>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-xs text-slate-400 py-4 border-t border-slate-200">
            동탄도시철도(트램) 건설사업 상부강화노반 공종 프로세스 관리 매뉴얼 | WBS 9000-1-8
        </div>
    </div>
</body>
</html>
'''

CHECKLIST_HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄도시철도 - 연약지반 처리공법 검토(필요시) 검측 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 antialiased py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto space-y-8">
        
        <!-- Header Banner -->
        <div class="bg-slate-900 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
            <div class="absolute right-0 top-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="relative z-10 space-y-4">
                <div class="flex flex-wrap items-center gap-3">
                    <span class="bg-emerald-500 text-slate-950 font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">WBS 9000-1-8</span>
                    <span class="bg-slate-800 text-slate-300 font-bold text-xs px-3 py-1 rounded-full">상부강화노반 검측 체크리스트</span>
                    <span class="bg-emerald-500/20 text-emerald-400 font-bold text-xs px-3 py-1 rounded-full">동탄도시철도 건설사업</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-black tracking-tight">연약지반 처리공법 검토(필요시) 검측 체크리스트</h1>
                <p class="text-slate-400 text-sm max-w-3xl leading-relaxed">
                    중분대 연약지반 프리로딩(마대옹벽+여성토) 시공, 계측 관리 및 <strong>잔류침하량 10cm 이하</strong> 판정 100% 질문형 마스터 검측 항목
                </p>
            </div>
        </div>

        <!-- Master Inspection Table -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-4 p-6">
            <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                <div class="flex items-center gap-2">
                    <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                    <h2 class="font-bold text-lg text-slate-900">현장 검측 및 감리원 확인 항목 (100% 질문형)</h2>
                </div>
                <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">합동 서명 전수 검측</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                        <tr>
                            <th class="px-6 py-3 w-5/12">검사항목 (질문형)</th>
                            <th class="px-6 py-3 w-3/12">검사기준 (시방/KCS)</th>
                            <th class="px-6 py-3 w-3/12">확인방법 및 판정</th>
                            <th class="px-6 py-3 w-1/12 text-center">판정</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800">중분대 연약층에 대한 압밀해석을 수행하여 공용 후 잔류침하량 허용기준(≤10cm)을 만족하도록 여성토 높이를 산정하였는가?</td>
                            <td class="px-6 py-4 text-slate-600 font-medium">KDS 11 00 00 & 철도설계기준</td>
                            <td class="px-6 py-4 text-slate-600">압밀해석 계산서 대조</td>
                            <td class="px-6 py-4 text-center"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">적합 (PASS)</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800">Sand Mat(두께 50cm, 투수계수 k≥1.0×10⁻²cm/s) 및 부직포를 연약지반 상부에 규정대로 포설하였는가?</td>
                            <td class="px-6 py-4 text-slate-600 font-medium">KCS 11 30 00</td>
                            <td class="px-6 py-4 text-slate-600">모래 품질시험 성적서 & 두께 실측</td>
                            <td class="px-6 py-4 text-center"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">적합 (PASS)</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800">인접 차도로의 토사 유출을 방지하기 위해 1.0ton 규격 톤마대 옹벽을 견고하게 3단 이상 계단식으로 축조하였는가?</td>
                            <td class="px-6 py-4 text-slate-600 font-medium">가설구조물 시방서</td>
                            <td class="px-6 py-4 text-slate-600">마대 결속 및 옹벽 단수 육안 점검</td>
                            <td class="px-6 py-4 text-center"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">적합 (PASS)</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800">마대 옹벽 내측에 설계된 여성토(1.5~3.0m)를 일일 30cm 이내 속도로 성토하고 층다짐도(≥95%)를 확보하였는가?</td>
                            <td class="px-6 py-4 text-slate-600 font-medium">KCS 11 20 00 토공사</td>
                            <td class="px-6 py-4 text-slate-600">들밀도시험 및 성토고 레벨 측량</td>
                            <td class="px-6 py-4 text-center"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">적합 (PASS)</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="px-6 py-4 font-bold text-slate-800">침하판 계측 데이터를 쌍곡선법으로 분석하여 잔류침하량 10cm 이하 및 침하율 수렴(≤1.0mm/8일)을 검증하였는가?</td>
                            <td class="px-6 py-4 text-slate-600 font-medium">계측관리지침서</td>
                            <td class="px-6 py-4 text-slate-600">쌍곡선법 침하분석 보고서 확인</td>
                            <td class="px-6 py-4 text-center"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">적합 (PASS)</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 합동 서명란 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm text-sm">
            <div class="space-y-2 border-r border-slate-100 pr-4">
                <div class="font-bold text-slate-900">시공자 토질/노반 담당자</div>
                <div class="text-slate-600 text-xs">직책/성명: 토목 공사 담당자 (서명)</div>
                <div class="text-slate-400 text-xs">점검일시: 2026년 ____월 ____일</div>
            </div>
            <div class="space-y-2 pl-4">
                <div class="font-bold text-slate-900">책임감리원 승인자</div>
                <div class="text-slate-600 text-xs">직책/성명: 토질 및 노반 책임감리원 (인)</div>
                <div class="text-slate-400 text-xs">승인일시: 2026년 ____월 ____일 (PMIS 등재완료)</div>
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-xs text-slate-400 py-4 border-t border-slate-200">
            동탄도시철도(트램) 건설사업 상부강화노반 공종 프로세스 관리 매뉴얼 | WBS 9000-1-8
        </div>
    </div>
</body>
</html>
'''

sync_targets = [
    (r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\8_시공계획서 수립 승인', '연약지반 처리공법 검토(필요시)'),
    (r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\8_연약지반 처리공법 검토(필요시)', '연약지반 처리공법 검토(필요시)'),
    (r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\8_작업조 편성', '연약지반 처리공법 검토(필요시)'),
    (r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\31_연약지반처리(필요시)', '연약지반처리(필요시)')
]

for base, name in sync_targets:
    std_dir = os.path.join(base, '표준서')
    chk_dir = os.path.join(base, '체크리스트')
    
    if os.path.exists(std_dir):
        with open(os.path.join(std_dir, f"{name}_표준서.html"), 'w', encoding='utf-8') as f:
            f.write(STANDARD_HTML)
        print(f"Updated standard: {std_dir}\\{name}_표준서.html")
        
    if os.path.exists(chk_dir):
        with open(os.path.join(chk_dir, f"{name}_체크리스트.html"), 'w', encoding='utf-8') as f:
            f.write(CHECKLIST_HTML)
        print(f"Updated checklist: {chk_dir}\\{name}_체크리스트.html")

print("=== All Standards and Checklists Synced! ===")
