import os, sys

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\전기분야'

# WBS 7, 8, 9 상세 데이터 정의
wbs_7 = {
    "wbs": "9000-3-7",
    "task": "발주처 품질 요구사항 검토",
    "folder": "7_발주처 품질 요구사항 검토",
    "prefix": "발주처 품질 요구사항 검토",
    "method": "감리/감독원 품질검사(ITP/ITC) 항목 검토, Hold Point/Witness Point 입회점 구분 수립, 현장 계측기 교정성적서 관리 및 불합격 자재 48시간 내 반출 통제 수칙",
    "step1_title": "ITP / ITC 품질검측 절차서 수립",
    "step1_desc": "감리/감독원 입회 품질검측계획서(ITP: Inspection & Test Plan) 작성 및 Hold Point(필수정지점) / Witness Point(입회점) 구분 명시",
    "step2_title": "현장 계측기 공인 교정성적서 대장 관리",
    "step2_desc": "Megger(절연저항계), OTDR(광시험기), 접지저항계 등 현장 사용 측정 장비 국가 공인기관 교정성적서 유효기간 1:1 검증 및 대장 관리",
    "step3_title": "불합격 자재 48시간 내 반출 & NCR 통제",
    "step3_desc": "자재 검수 시 부적합 자재 발생 즉시 현장 격리 후 48시간 이내 현장 반출 처리, NCR 부적합 시정조치 요구서 발행 및 품질 보완",
    "step4_title": "품질시험계획서 감리 승인 & 보고",
    "step4_desc": "발주처 품질 요구사항이 100% 반영된 종합 품질시험계획서 작성, 책임감리단 공학적 최종 승인 결재 및 현장 품질 관리대장 적용"
}

wbs_8 = {
    "wbs": "9000-3-8",
    "task": "자재 / 인원 / 장비 등 투입 사전 검토",
    "folder": "8_자재 _ 인원 _ 장비 등 투입 사전 검토",
    "prefix": "자재 _ 인원 _ 장비 등 투입 사전 검토",
    "method": "현장 여건 및 공정을 기준으로 주요 자재 Lead Time(30~60일) 사전 발주 검증, 한국전기공사협회 기술자 자격 실물 대조, 고소작업차 안전검사합격증 확인 및 투입계획서 승인",
    "step1_title": "주요 자재 조달 Lead Time 사전 검증",
    "step1_desc": "변압기, GIS, 정류기, ESS, 전차선 등 주요 전기자재 공장 제작 및 수급 소요 기간(Lead Time 30~60일)을 공정표와 사전 연동 통제",
    "step2_title": "전철전력 기술자 자격 수첩 실물 1:1 대조",
    "step2_desc": "한국전기공사협회 발행 전철전력 시공 기술 자격 수첩 실물 대조, 현장대리인 및 특고압/고소 작업자 경력사항 100% 검증",
    "step3_title": "고소작업차 & 안전검사합격증 점검",
    "step3_desc": "산업안전보건공단 고소작업차 안전검사합격증 유효기간, 장비 Spec, 조종원 면허증 및 일일 점검표 부합성 확인",
    "step4_title": "자재/인력/장비 동원계획서 감리 승인",
    "step4_desc": "현장 투입 자재, 인원, 장비 세부 동원계획서 작성, 책임감리단 결재 승인 수검 및 현장 공공 안전 확보 완수"
}

wbs_9 = {
    "wbs": "9000-3-9",
    "task": "인허가 준비",
    "folder": "9_인허가 준비",
    "prefix": "인허가 준비",
    "method": "한전 22.9kV 수전 전기사용신청, 지자체 전기 공사계획신고, 도로점용허가(도로법 56조), 도로공사신고(도로교통법 69조) 및 KESC 사용전검사 인허가 To-Do List 추적 관리",
    "step1_title": "한전 22.9kV 수전 전기사용신청",
    "step1_desc": "관할 한전에 수전 용량 계산서, 건축허가서, 22.9kV 수전 단선도 첨부 전기사용신청서 제출(처리기간 1개월) 및 인수점 지중 맨홀 협의",
    "step2_title": "지자체 공사계획신고 & 도로점용허가",
    "step2_desc": "화성시/수원시 지자체 전기 공사계획신고서 제출 및 도로법 제56조에 따른 도로점용허가(도로점용 2주 전 신청, 7~10일 소요) 교부 완료",
    "step3_title": "경찰서 도로공사신고 & 사용전검사 접수",
    "step3_desc": "관할 경찰서 도로교통법 제69조 도로공사신고(공사 3일 전 제출) 승인 필증 수령 및 KESC 사용전검사(설치 완료 7일 전) 신청 접수",
    "step4_title": "인허가 종합 To-Do List 추적 관리",
    "step4_desc": "인허가 항목별 신청시기, 처리기간, 발급 기관 및 수속 현황을 To-Do List 대장으로 작성하여 공정 지연 원천 차단"
}

# Standard HTML Generator
def gen_standard(d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 전기분야 - {d['task']} 표준서 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Electrical Standard (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 표준서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: 현장 전철전력팀 (책임감리단 공조) | "{d['step1_title']} & 표준 수칙"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-8">
        
        <!-- ⚖️ 근거 법령, 국가 설계기준 및 입찰안내서 검토 기준 -->
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 국가 기준 · 업무 표준 규정 (Legal & Bidding Verification)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">업무이행 표준</span>
            </div>
            
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 전기사업법, 도로법, 도로교통법, 건설기술 진흥법, KDS 47 00 00 철도설계기준 및 동탄트램 입찰안내서에 의거하여, <strong>{d['task']}에 대한 상세 기준 및 감리단 공학적 승인 수칙</strong>을 체계적으로 확정하는 표준입니다.
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                
                <div class="bg-amber-50/70 p-4 rounded-xl border border-amber-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-amber-900 text-xs">📌 {d['step1_title']}</span>
                        <span class="text-[10px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded border border-amber-300">단계 1</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step1_desc']}"</strong>
                    </p>
                </div>

                <div class="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-indigo-900 text-xs">📐 {d['step2_title']}</span>
                        <span class="text-[10px] bg-indigo-200 text-indigo-900 font-bold px-2 py-0.5 rounded border border-indigo-300">단계 2</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step2_desc']}"</strong>
                    </p>
                </div>

                <div class="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-emerald-900 text-xs">🛡️ {d['step3_title']}</span>
                        <span class="text-[10px] bg-emerald-200 text-emerald-900 font-bold px-2 py-0.5 rounded border border-emerald-300">단계 3</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step3_desc']}"</strong>
                    </p>
                </div>

                <div class="bg-sky-50/70 p-4 rounded-xl border border-sky-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-sky-900 text-xs">📄 {d['step4_title']}</span>
                        <span class="text-[10px] bg-sky-200 text-sky-900 font-bold px-2 py-0.5 rounded border border-sky-300">단계 4</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step4_desc']}"</strong>
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
                {d['method']}
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
                        <h4 class="font-bold text-slate-900 text-sm">시방 및 규정 100% 준수 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        철도설계기준, 발주처 특기시방서 및 인허가 법정 처리기간을 사전 검측하여 적기 시공을 확보함.
                    </p>
                </div>

                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 2</span>
                        <h4 class="font-bold text-slate-900 text-sm">서류 대장 관리 & 감리 승인 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        모든 검측 서표, 교정성적서, 자격증, 필증 및 승인 문서는 관리대장에 수록하여 책임감리단 결재를 완수함.
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
                <p class="text-slate-700 text-xs font-medium">{d['task']} 관련 승인서, 검측 성과표, 허가/신고 필증 사본 및 관리대장</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">
                최종 승인 완료
            </span>
        </div>

    </div>
</div>
</body>
</html>
"""

# Guideline HTML Generator
def gen_guideline(d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 전기분야 - {d['task']} 상세 수행지침서 (WBS {d['wbs']})</title>
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
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Electrical Guideline (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: 현장 전철전력팀 (책임감리단 공조) | "{d['step1_title']} & 실무 절차 방법론"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        
        <!-- 💡 검토 개요 및 목표 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 {d['task']} 업무수행 방법 및 절차</h4>
            <p class="bg-white p-4 rounded-xl border border-amber-300 font-medium text-slate-900 leading-relaxed text-xs sm:text-sm">
                {d['method']}
            </p>
        </div>

        <!-- 🚀 4단계 상세 검토 방법 및 수행 절차 -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🛠️</span> {d['task']} 상세 수행 절차
            </h2>

            <div class="grid grid-cols-1 gap-6">
                
                <!-- STEP 1 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 01</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step1_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">단계 1</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step1_desc']}<br>
                        • <strong>세부 지침:</strong> 관련 시방서 및 법정 기준을 1:1 사전 대조하여 이행 계획을 확정함.
                    </p>
                </div>

                <!-- STEP 2 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-indigo-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 02</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step2_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-indigo-700 bg-indigo-100 px-2.5 py-0.5 rounded-full">단계 2</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step2_desc']}<br>
                        • <strong>세부 지침:</strong> 계측기 성적서, 자격증, 합격증 및 허가 서류 유효기간을 100% 검증함.
                    </p>
                </div>

                <!-- STEP 3 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 03</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step3_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">단계 3</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step3_desc']}<br>
                        • <strong>세부 지침:</strong> 부적합/불합격 자재 즉시 반출 통제 및 관할 기관 신고 접수를 수속함.
                    </p>
                </div>

                <!-- STEP 4 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-teal-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 04</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step4_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-teal-700 bg-teal-100 px-2.5 py-0.5 rounded-full">단계 4</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step4_desc']}<br>
                        • <strong>세부 지침:</strong> 종합 계획서 작성 및 To-Do List 관리를 통해 책임감리단 공학적 결재를 완성함.
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
                    <text x="275" y="38" font-size="13" font-weight="black" fill="#b45309" text-anchor="middle">⚡ 동탄트램 {d['task']} 수행 절차도</text>
                    <line x1="25" y1="46" x2="525" y2="46" stroke="#e2e8f0" stroke-width="1.5"/>
                    
                    <g transform="translate(25, 55)">
                        <rect x="0" y="0" width="145" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="6"/>
                        <text x="72.5" y="22" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1. 수속/계획 수립</text>
                        <text x="12" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 시방/법률 항목 검토</text>
                        <text x="12" y="65" font-size="8" font-weight="bold" fill="#0f172a">• Lead Time/신청서 대조</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="22" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">2. 서류/자격 검증</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 성적서/자격증 실측</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 허가/신고 필증 수령</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="22" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">3. 최종 결재 승인</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#15803d">• To-Do List 대장관리</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#15803d">• 감리단 결재 완수</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS {d['wbs']} {d['task']} 관련 계획서 및 승인문서 결재 완수</text>
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

# Checklist HTML Generator
def gen_checklist(d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 전기분야 - {d['task']} 체크리스트 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
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
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Electrical Checklist (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 체크리스트</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: 현장 전철전력팀 (책임감리단 공조) | "16개 정밀 검측 문항 1:1 수평대응 서식 (~하였는가? 어미 100% 통일)"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-6">
        
        <!-- 💡 체크리스트 점검의 핵심 의미 -->
        <div class="bg-amber-50 border-2 border-amber-300 p-5 sm:p-6 rounded-2xl text-xs text-amber-950 space-y-3 shadow-sm">
            <div class="flex items-center justify-between border-b border-amber-200 pb-2.5">
                <h4 class="font-black text-sm text-amber-900 flex items-center gap-2">
                    <span class="text-base">⚠️</span> {d['task']} 체크리스트 점검의 핵심 의미
                </h4>
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">사전/시공 검측</span>
            </div>
            
            <p class="text-slate-800 leading-relaxed font-semibold">
                본 체크리스트는 동탄트램 전기분야 업무 이행에 대해 <strong>{d['method']} 관련 실무 요소를 100% 사전 검측하여 품질 부적합 및 공정 지연 리스크를 예방하기 위한 필수 서식</strong>입니다.
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
                            <span class="font-bold text-slate-900 text-xs">{d['step1_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[{d['step1_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">1. {d['step1_desc']} 규정 준수 여부를 사전 검측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[시방 및 기술기준 대조]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">2. 발주처 특기시방서 및 KDS 47 00 00 철도설계기준 허용 범위를 1:1 검토하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[사전 서류 준비]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">3. 착수 전 필요한 신청서, 제출서류 및 계산서 구비 여부를 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[예정공정표 연동]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">4. 해당 작업 마일스톤이 전체 예정공정표와 부합하도록 조정하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">{d['step2_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[{d['step2_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">5. {d['step2_desc']} 실무 수칙을 검증 및 이행하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[자격 및 성적서 유효성]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">6. 기술자 자격증, 계측기 교정성적서 및 합격증의 유효기간을 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[법정 인허가 수속]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">7. 관계 기관(한전, 지자체, 경찰서, 전기안전공사) 서류 접수를 이행하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[현장 안전 및 품질 검측]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">8. 안전 수칙 준수 및 자재/장비 수급 상태를 점검하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">{d['step3_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[{d['step3_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">9. {d['step3_desc']} 사항을 검사 및 시정 조치하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[부적합 및 격리 통제]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">10. 부적합 자재 현장 격리 및 48시간 내 반출 수칙을 이행하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[허가 필증 수령]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">11. 도로점용허가서, 도로공사신고 필증 등 정식 필증을 발급받았는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[시정조치 결과 보고]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">12. 지적 사항 시정 조치 확인서를 작성하여 감리단에 보고하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">{d['step4_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[{d['step4_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">13. {d['step4_desc']} 계획서 및 대장 작성을 완료하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[To-Do List 및 대장 수록]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">14. 종합 이행 대장 및 To-Do List 추적 현황을 업데이트하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[책임감리단 승인 결재]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">15. 책임감리원 입회 및 공학적 최종 승인 결재를 완수하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[공무 대장 등록 및 관리]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">16. 승인된 서표 및 필증 사본을 현장 공무 대장에 보관 완료하였는가?</p>
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

all_items = [wbs_7, wbs_8, wbs_9]

for d in all_items:
    fpath = os.path.join(base_dir, d['folder'])
    
    # 1. Standard
    std_p = os.path.join(fpath, '표준서', f"{d['prefix']}_표준서.html")
    with open(std_p, 'w', encoding='utf-8') as f:
        f.write(gen_standard(d))
    print(f"Updated: {std_p}")
    
    # 2. Guideline
    gui_p = os.path.join(fpath, '수행지침', f"{d['prefix']}_수행지침.html")
    with open(gui_p, 'w', encoding='utf-8') as f:
        f.write(gen_guideline(d))
    print(f"Updated: {gui_p}")
    
    # 3. Checklist
    chk_p = os.path.join(fpath, '체크리스트', f"{d['prefix']}_체크리스트.html")
    with open(chk_p, 'w', encoding='utf-8') as f:
        f.write(gen_checklist(d))
    print(f"Updated: {chk_p}")

print("\nSUCCESSFULLY UPDATED ALL 9 HTML FILES FOR WBS 9000-3-7, 8, 9!")
