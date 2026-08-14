import os, sys, openpyxl, re

excel_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v4.xlsx'
base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

wb = openpyxl.load_workbook(excel_path)
ws = wb['상부강화노반']

# 엑셀 데이터 추출 (Row 4 ~ Row 37)
rows_data = []
for r in range(4, 38):
    wbs = ws.cell(row=r, column=4).value
    task = ws.cell(row=r, column=6).value
    dept = ws.cell(row=r, column=7).value or '현장 공사팀'
    purpose = ws.cell(row=r, column=8).value or f'{task} 과업 목적 달성 및 KCS 47 10 25 공학 품질 확보'
    method = ws.cell(row=r, column=9).value or ''
    deliverable = ws.cell(row=r, column=10).value or '검측보고서, 시험성적서 및 인계인수서'
    rule = ws.cell(row=r, column=11).value or ''
    
    # Clean string
    method_clean = re.sub(r'\s+', ' ', str(method)).strip()
    purpose_clean = re.sub(r'\s+', ' ', str(purpose)).strip()
    
    wbs_num = wbs.split('-')[-1] if wbs else str(r-2)
    
    # find target directory
    target_folder = None
    for d in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, d)) and (d.startswith(f'{wbs_num}_') or d == wbs_num):
            target_folder = os.path.join(base_dir, d)
            break
            
    if not target_folder:
        # create fallback directory if not found
        target_folder = os.path.join(base_dir, f"{wbs_num}_{task.replace('/', '_')}")
        os.makedirs(target_folder, exist_ok=True)
        
    rows_data.append({
        'row': r,
        'wbs': wbs,
        'task': task,
        'dept': dept,
        'purpose': purpose_clean,
        'method': method_clean,
        'deliverable': deliverable,
        'rule': rule,
        'folder': target_folder,
        'prefix': task.replace('/', ' _ ')
    })

print(f"Extracted {len(rows_data)} rows of data (Row 4 ~ Row 37).")

def generate_standard_html(d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {d['task']} 표준서 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Roadbed Standard (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 표준서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: {d['dept']} | "KCS 47 10 25 강화노반 & 공학적 품질 표준"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-8">
        
        <!-- ⚖️ 근거 법령, 국가 설계기준 및 입찰안내서 검토 기준 -->
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 국가 건설기준 · 시방 표준 규정 (Legal & Technical Specification)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">KCS 47 10 25 강화노반</span>
            </div>
            
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 건설기술 진흥법, 철도건설법, <strong>KCS 47 10 25 (강화노반) 국가건설기준</strong> 및 동탄트램 입찰안내서에 의거하여, <strong>{d['task']} 과업의 기술적 요구사항 및 감리단 공학적 승인 절차</strong>를 체계적으로 확정하는 표준 규정입니다.
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                
                <div class="bg-amber-50/70 p-4 rounded-xl border border-amber-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-amber-900 text-xs">📌 1. 사전 기준 & 대조 검증</span>
                        <span class="text-[10px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded border border-amber-300">단계 1</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"관련 도면, 측량 데이터, 설계 지침서 및 국가 건설기준(KCS 47 10 25) 1:1 사전 대조 검증"</strong>
                    </p>
                </div>

                <div class="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-indigo-900 text-xs">📐 2. 공학적 품질 & 정량 기준</span>
                        <span class="text-[10px] bg-indigo-200 text-indigo-900 font-bold px-2 py-0.5 rounded border border-indigo-300">단계 2</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"강화노반 다짐도 ≥95%, K30≥110 MN/m³(Ev2≥60MPa), 표고 허용 오차 ±10mm 수칙 준수"</strong>
                    </p>
                </div>

                <div class="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-emerald-900 text-xs">🛡️ 3. 안전 & 환경 Risk 차단</span>
                        <span class="text-[10px] bg-emerald-200 text-emerald-900 font-bold px-2 py-0.5 rounded border border-emerald-300">단계 3</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"3D BIM 공간 간섭 소멸, 살수차 가동 비산먼지 통제, 세륜 및 인프라 안전 확보"</strong>
                    </p>
                </div>

                <div class="bg-sky-50/70 p-4 rounded-xl border border-sky-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-sky-900 text-xs">📄 4. 서표 대장 & 감리 승인</span>
                        <span class="text-[10px] bg-sky-200 text-sky-900 font-bold px-2 py-0.5 rounded border border-sky-300">단계 4</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"실측 성적서, 시험 야장 및 성과표 작성 후 책임감리단 공학적 최종 결재 완수"</strong>
                    </p>
                </div>

            </div>
        </div>

        <!-- 🎯 표준 목적 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl">
            <h3 class="text-base font-bold text-amber-950 mb-2 flex items-center gap-2">
                <span>🎯</span> 표준 목적 (Objective)
            </h3>
            <p class="text-slate-800 text-sm font-medium leading-relaxed">
                {d['purpose']} 이에 따라 <strong>"{d['method']}"</strong> 실무 수칙을 정밀 이행하여 노반 품질 부적합 및 공정 지연을 미연에 방지함.
            </p>
        </div>

        <!-- 📜 업무수행 수칙 -->
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span>📜</span> 업무수행 핵심 수칙 (Execution Rules)
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-red-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 1</span>
                        <h4 class="font-bold text-slate-900 text-sm">정량적 공학 품질 준수 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        KCS 47 10 25 강화노반 국가건설기준에 명시된 다짐도(95% 이상) 및 표고 허용 오차(±10mm) 기준을 100% 준수함.
                    </p>
                </div>

                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 2</span>
                        <h4 class="font-bold text-slate-900 text-sm">검측 대장 관리 & 감리 승인 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        모든 측량 야장, 재하시험 성적서 및 검측 대장은 관리 서식으로 작성하여 책임감리단 승인을 필함.
                    </p>
                </div>
            </div>
        </div>

        <!-- 📦 증빙 산출물 -->
        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <h3 class="text-base font-bold text-emerald-950 mb-1 flex items-center gap-2">
                    <span>📦</span> 증빙 산출물 (Deliverables)
                </h3>
                <p class="text-slate-700 text-xs font-medium">{d['deliverable']}</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">
                검측 승인 완료
            </span>
        </div>

    </div>
</div>
</body>
</html>
"""

def generate_guideline_html(d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {d['task']} 상세 수행지침서 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        .clickable-diagram {{
            cursor: zoom-in !important;
            transition: all 0.25s ease !important;
            position: relative !important;
        }}
        .clickable-diagram:hover {{
            transform: scale(1.01) !important;
            box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important;
        }}
        .clickable-diagram::after {{
            content: "🔍 클릭하여 대형 확대보기";
            position: absolute; bottom: 12px; right: 16px;
            background: rgba(15, 23, 42, 0.8); color: #ffffff;
            font-size: 11px; font-weight: 700; padding: 4px 12px;
            border-radius: 20px; backdrop-filter: blur(4px);
            pointer-events: none; opacity: 0.9;
        }}
        .zoom-modal {{
            display: none; position: fixed; z-index: 9999;
            left: 0; top: 0; width: 100%; height: 100%;
            overflow: auto; background-color: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(6px); align-items: center; justify-content: center;
        }}
        .zoom-modal.active {{ display: flex; }}
        .zoom-modal-content {{
            background-color: #ffffff; margin: auto; padding: 28px;
            border: 1px solid #cbd5e1; width: 95%; max-width: 1100px; max-height: 90vh;
            border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative; overflow-y: auto; text-align: center;
        }}
        .zoom-close {{
            color: #64748b; position: absolute; right: 20px; top: 16px;
            font-size: 32px; font-weight: bold; cursor: pointer;
        }}
        .zoom-close:hover {{ color: #ef4444; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Roadbed Guideline (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: {d['dept']} | "KCS 47 10 25 강화노반 & 실무 절차 가이드라인"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        
        <!-- 💡 검토 개요 및 목표 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 {d['task']} 업무수행 방법 및 실무 절차 개요</h4>
            <p class="bg-white p-4 rounded-xl border border-amber-300 font-medium text-slate-900 leading-relaxed text-xs sm:text-sm">
                {d['method']}
            </p>
        </div>

        <!-- 🚀 4단계 상세 검토 방법 및 수행 절차 -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🛠️</span> {d['task']} 4단계 상세 수행 절차
            </h2>

            <div class="grid grid-cols-1 gap-6">
                
                <!-- STEP 1 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 01</span>
                            <h3 class="font-bold text-base text-slate-900">사전 대조 & 도서/측량 검토</h3>
                        </div>
                        <span class="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">단계 1</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 관련 설계도서, 현장 측량 야장, 국가건설기준(KCS 47 10 25) 및 공정 마일스톤을 1:1 대조함.<br>
                        • <strong>세부 지침:</strong> 현장 여건과 설계 규격의 일치성을 확인하고 사전 오차 요소를 추출함.
                    </p>
                </div>

                <!-- STEP 2 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-indigo-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 02</span>
                            <h3 class="font-bold text-base text-slate-900">현장 실측 & 정량 품질 검측</h3>
                        </div>
                        <span class="text-xs font-semibold text-indigo-700 bg-indigo-100 px-2.5 py-0.5 rounded-full">단계 2</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 쇄석 다짐(95% 이상), 평판재하시험(K30≥110 MN/m³), 종횡단 표고(±10mm 이내) 현장 정밀 실측 수행.<br>
                        • <strong>세부 지침:</strong> 시험성적서 및 레벨 측량 데이터를 공학적 대장에 100% 기록관리함.
                    </p>
                </div>

                <!-- STEP 3 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 03</span>
                            <h3 class="font-bold text-base text-slate-900">안전 · 환경 관리 & 3D BIM 간섭 소멸</h3>
                        </div>
                        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">단계 3</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 덤프트럭 비산 먼지 통제(살수차 가동), 올바로시스템 대조 및 3D BIM 횡단관로 공간 클래시 소멸.<br>
                        • <strong>세부 지침:</strong> 시공 중 안전 사고 요소를 차단하고 부적합 발생 시 즉시 시정 조치함.
                    </p>
                </div>

                <!-- STEP 4 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-teal-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 04</span>
                            <h3 class="font-bold text-base text-slate-900">검측 대장 작성 & 감리 승인</h3>
                        </div>
                        <span class="text-xs font-semibold text-teal-700 bg-teal-100 px-2.5 py-0.5 rounded-full">단계 4</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 종합 검측 보고서, 시험성적서 및 준공도서를 결재 서식으로 작성하여 최종 보고함.<br>
                        • <strong>세부 지침:</strong> 책임감리원 공학적 서명 결재를 수검하고 후행 공종에 정상 인계함.
                    </p>
                </div>

            </div>
        </div>

        <!-- 🖼️ 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🖼️</span> {d['task']} 상세 수행 절차도
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_{d['wbs'].replace("-", "_")}', '[WBS {d['wbs']}] {d['task']} 상세 수행 절차도')">
                <svg id="svg_{d['wbs'].replace("-", "_")}" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="200" fill="#f8fafc" rx="8"/>
                    <rect x="15" y="15" width="520" height="170" fill="#ffffff" stroke="#d97706" stroke-width="2" rx="6"/>
                    <text x="275" y="38" font-size="13" font-weight="black" fill="#b45309" text-anchor="middle">🚜 동탄트램 {d['task']} 수행 절차도</text>
                    <line x1="25" y1="46" x2="525" y2="46" stroke="#e2e8f0" stroke-width="1.5"/>
                    
                    <g transform="translate(25, 55)">
                        <rect x="0" y="0" width="145" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="6"/>
                        <text x="72.5" y="22" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1. 사전 대조/측량</text>
                        <text x="12" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 도면/KCS 47 10 25 대조</text>
                        <text x="12" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 오차 요소 사전 추출</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="22" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">2. 정량 품질검측</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 다짐 95%/K30≥110</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 표고 오차 ±10mm</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="22" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">3. 감리 결재 완수</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#15803d">• 성적서/야장 작성</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#15803d">• 감리단 승인 수검</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS {d['wbs']} {d['task']} 검측 대장 및 성적서 감리 승인 완수</text>
                </svg>
            </div>
        </div>

    </div>
</div>

<!-- 🟣 시공 도식 확대 팝업 모달 -->
<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 {d['task']} 2D Visual 도식 확대 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
    </div>
</div>

<script>
    function openDiagramZoom(elementId, titleText) {{
        const srcEl = document.getElementById(elementId);
        if (!srcEl) return;
        
        const zoomBody = document.getElementById('zoomBody');
        document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "{d['task']} 도식 대형 확대 보기");
        zoomBody.innerHTML = srcEl.outerHTML;
        
        const innerSvg = zoomBody.querySelector('svg');
        if (innerSvg) {{
            innerSvg.setAttribute('width', '100%');
            innerSvg.setAttribute('height', '520px');
            innerSvg.style.maxWidth = '1050px';
        }}
        document.getElementById('zoomModal').classList.add('active');
    }}

    function closeZoomModal() {{
        document.getElementById('zoomModal').classList.remove('active');
    }}

    function closeZoomModalOutside(event) {{
        if (event.target.id === 'zoomModal') closeZoomModal();
    }}

    window.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') closeZoomModal();
    }});
</script>
</body>
</html>
"""

def generate_checklist_html(d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {d['task']} 체크리스트 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Roadbed Checklist (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 체크리스트</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: {d['dept']} | "16개 정밀 검측 문항 1:1 수평대응 서식 (~하였는가? 어미 100% 통일)"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-6">
        
        <!-- 💡 체크리스트 점검의 핵심 의미 -->
        <div class="bg-amber-50 border-2 border-amber-300 p-5 sm:p-6 rounded-2xl text-xs text-amber-950 space-y-3 shadow-sm">
            <div class="flex items-center justify-between border-b border-amber-200 pb-2.5">
                <h4 class="font-black text-sm text-amber-900 flex items-center gap-2">
                    <span class="text-base">⚠️</span> {d['task']} 체크리스트 점검의 핵심 의미
                </h4>
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">정밀 시공 검측</span>
            </div>
            
            <p class="text-slate-800 leading-relaxed font-semibold">
                본 체크리스트는 동탄트램 상부강화노반 시공 및 검측에 대해 <strong>{d['method']} 관련 16개 핵심 실무 문항 및 KCS 47 10 25 강화노반 공학 수칙(다짐도 ≥95%, K30≥110, 표고오차 ±10mm)을 100% 사전 검측하여 노반 품질 확보 및 시공 하자를 사전에 예방하기 위한 필수 서식</strong>입니다.
            </p>
        </div>

        <!-- 📊 1:1 정밀 수평대응 3컬럼 체크리스트 테이블 (16개 핵심 문항) -->
        <div class="overflow-x-auto border border-slate-200 rounded-xl shadow-sm">
            <table class="w-full text-left border-collapse text-xs">
                <thead>
                    <tr class="bg-slate-100 border-b border-slate-200 text-slate-700">
                        <th class="p-4 font-bold w-44 text-center border-r border-slate-200">검토 단계 (Procedure)</th>
                        <th class="p-4 font-bold border-r border-slate-200">필수 검측 및 확인 항목 (Inspection Criteria)</th>
                        <th class="p-4 font-bold w-32 text-center">점검 결과</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 bg-white">
                    
                    <!-- STEP 1 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-amber-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 1</span>
                            <span class="font-bold text-slate-900 text-xs">사전 검토 & 대조</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[설계도서 및 기준 준수]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">1. 관련 설계도서, KCS 47 10 25 시방 규정 및 공정 마일스톤 부합성을 사전 검토하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[실무 방법론 대조]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">2. "{d['method'][:50]}..." 지침 수칙을 정밀 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[측량 좌표 & 레벨]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">3. GRS80 측지계 좌표 및 중심선 표고 레벨 측량 데이터를 사전 검증하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[사전 서류 준비]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">4. 시공 및 검측에 필요한 제반 서류 및 검측서표를 선제적으로 구비하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                    <!-- STEP 2 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-indigo-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 2</span>
                            <span class="font-bold text-slate-900 text-xs">정량 품질 검측</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[강화노반 다짐도]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">5. 강화노반 및 노반 다짐도 95% 이상(KS F 2312) 시험 성적을 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[평판재하시험 K30]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">6. 완성면 평판재하시험 지반반발계수 K30 ≥ 110 MN/m³ (Ev2≥60MPa) 부합성을 검측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[표고 및 구배 오차]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">7. 마무리면 종횡단 표고 계획 오차 ±10mm 이내 및 구배(2.0% 이상) 정밀도를 측정하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[자재 품질 성적서]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">8. 반입 쇄석 골재, 유공관 및 부직포 시험성적서 일치성을 검수하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                    <!-- STEP 3 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-emerald-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 3</span>
                            <span class="font-bold text-slate-900 text-xs">안전 · 환경 통제</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[비산먼지 & 살수차]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">9. 덤프트럭 덮개 자동 개폐 및 반출 경로 15톤 살수차 상시 가동 상태를 점검하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[올바로시스템 대조]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">10. 토사/폐기물 올바로시스템 반입 확인서와 운반 일지를 전수 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[3D BIM 간섭 소멸]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">11. 3D BIM 클래시 분석을 통해 지하 매설관 및 횡단 관로 간섭을 100% 사전에 제거하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[부적합 시정 확인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">12. 검측 과정 중 지적된 지점의 재다짐 및 보완 조치 완수를 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                    <!-- STEP 4 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-teal-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 4</span>
                            <span class="font-bold text-slate-900 text-xs">서표 작성 & 감리승인</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[종횡단 검측 야장]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">13. 종횡단 표고 측량 성과표 및 3D 검측대장 작성을 완수하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[책임감리 입회 검측]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">14. 책임감리원 입회하에 노반 완성면 현장 수검을 수행하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[공학적 최종 승인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">15. 검측 결과 보고서에 감리단 최종 결재 서명을 완료받았는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[후행 궤도 인계인수]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">16. 승인 성적서를 첨부하여 후행 궤도 공종 시공팀에 공식 인계인수를 완료하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>

    </div>
</div>
</body>
</html>
"""

# 전체 일괄 생성 반복문
count = 0
for d in rows_data:
    folder = d['folder']
    os.makedirs(os.path.join(folder, '표준서'), exist_ok=True)
    os.makedirs(os.path.join(folder, '수행지침'), exist_ok=True)
    os.makedirs(os.path.join(folder, '체크리스트'), exist_ok=True)
    
    # Write Standard
    std_p = os.path.join(folder, '표준서', f"{d['prefix']}_표준서.html")
    with open(std_p, 'w', encoding='utf-8') as f:
        f.write(generate_standard_html(d))
        
    # Write Guideline
    gui_p = os.path.join(folder, '수행지침', f"{d['prefix']}_수행지침.html")
    with open(gui_p, 'w', encoding='utf-8') as f:
        f.write(generate_guideline_html(d))
        
    # Write Checklist
    chk_p = os.path.join(folder, '체크리스트', f"{d['prefix']}_체크리스트.html")
    with open(chk_p, 'w', encoding='utf-8') as f:
        f.write(generate_checklist_html(d))
        
    count += 3
    print(f"Row {d['row']:2d} [{d['wbs']} - {d['task']}]: Generated 3 HTML files -> {folder}")

print(f"\nSUCCESSFULLY GENERATED ALL {count} HTML FILES FOR ROWS 4 ~ 37!")
