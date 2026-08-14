import os, sys

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\전기분야'

# WBS 4, 5, 6 상세 데이터 정의
wbs_4 = {
    "wbs": "9000-3-4",
    "task": "신호 / 통신 / 기계 / PSD / 차량 인터페이스 협의",
    "folder": "4_신호 _ 통신 _ 기계 _ PSD _ 차량 인터페이스 협의",
    "prefix": "신호 _ 통신 _ 기계 _ PSD _ 차량 인터페이스 협의",
    "method": "전기분야와 타공종(신호, 통신, 기계, PSD, 트램 차량) 간 인터페이스 설계도서 상 누락 및 협의사항 도출, 관로/배선/트레이/인터록 신호선 사전 조율을 통해 재작업을 원천 예방함",
    "step1_title": "설계도서 누락 & 협의사항 도출",
    "step1_desc": "신호, 통신, 기계, PSD 및 트램 차량 전력 공급 관로, 배선 용량 및 트레이 타공 누락 사항 정밀 추출",
    "step2_title": "차량 충전 & PSD 인터록 조율",
    "step2_desc": "정거장 및 차량기지 급속 충전 스티치, 무선통신(LTE-R), 신호 연동 및 PSD 안전 개폐 인터록 사전 협의",
    "step3_title": "3D BIM 공종 간섭 & 재작업 예방",
    "step3_desc": "3D BIM 공간 클래시(Clash) 검토를 통해 타공종 관로/기계 덕트 간섭 해소 및 현장 재작업 100% 방지",
    "step4_title": "인터페이스 회의록 & 관리대장 승인",
    "step4_desc": "타공종 대표자 참석 인터페이스 회의록 및 관리대장 체결, 책임감리단 공학적 승인 최종 완수"
}

wbs_5 = {
    "wbs": "9000-3-5",
    "task": "전기설비 제작사 인터페이스 협의",
    "folder": "5_전기설비 제작사 인터페이스 협의",
    "prefix": "전기설비 제작사 인터페이스 협의",
    "method": "전기설비(변압기, 정류기, ESS, GIS, SCADA RTU) 제작사 사양 사전 반영, 이종 제작사 간 통신 프로토콜(IEC 61850, Modbus) 핀 맵/제어 랙 치수 조율 및 제작사양서 확정",
    "color": "indigo",
    "step1_title": "이종 제작사 프로토콜 & 핀 맵 대조",
    "step1_desc": "SCADA RTU, 변전소 GIS, 정류기, ESS 릴레이 간 IEC 61850 및 Modbus 통신 핀 맵/신호 주소 1:1 검증",
    "step2_title": "제어반 랙 치수 & 부스바 피치 조율",
    "step2_desc": "제어반 19인치 랙 배열, 대전류 동판 부스바 관통 피치 및 현장 케이블 인입 위치 제작사간 조율",
    "step3_title": "공인 성적서 & KESC 시험 항목 사전 검토",
    "step3_desc": "KTR/KTL 공인기관 시험성적서 및 KESC 사용전검사 필수 시험 항목 제작 사양서 100% 포함 확인",
    "step4_title": "제작사양서 & 관리대장 감리 승인",
    "step4_desc": "제작사 인터페이스 종합 회의록, 확정 제작사양서 작성 후 책임감리단 공학적 최종 승인 완수"
}

wbs_6 = {
    "wbs": "9000-3-6",
    "task": "관제 및 운영사 인터페이스 협의",
    "folder": "6_관제 및 운영사 인터페이스 협의",
    "prefix": "관제 및 운영사 인터페이스 협의",
    "method": "수원시/동탄 도로교통관제 트램 우선신호 연동, 트램관제실(OCC) SCADA MMI 심볼 표준화, 차단기/단로기/접지스위치 안전 인터록 Logic 및 유지보수자 편의 기능 사전 협의",
    "color": "emerald",
    "step1_title": "도로교통관제(수원·동탄) 우선신호 연동",
    "step1_desc": "지자체(수원시, 화성시) 도로교통관제 센터와 트램 우선신호 제어기 간 통신 인터페이스 및 연동 협의",
    "step2_title": "차단기-단로기-접지스위치 안전 인터록",
    "step2_desc": "변전소 고압 차단기(CB), 단로기(DS), 접지스위치(ES) 간 오조작 방지 시퀀스 및 LOCAL/REMOTE 락아웃",
    "step3_title": "OCC SCADA MMI 심볼 & 운영 편의기능",
    "step3_desc": "트램 관제실(OCC) SCADA 화면 MMI 표준 심볼 확정, 수전반 Layout 및 유지보수자 요청 기능 반영",
    "step4_title": "운영사 협의 회의록 & 관리대장 승인",
    "step4_desc": "관제 및 운영사 인터페이스 협의 회의록 작성, 책임감리단 서명 승인 및 공무 대장 공식 관리"
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
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 국가 기준 · 인터페이스 표준 (Legal & Bidding Verification)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">인터페이스 표준</span>
            </div>
            
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 전기공사업법, 건설기술 진흥법, KDS 47 00 00 철도설계기준 및 동탄트램 입찰안내서에 의거하여, <strong>{d['task']} 분야의 핵심 요구사항 및 감리단 공학적 승인 절차</strong>를 체계적으로 확정하는 표준입니다.
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
                        <h4 class="font-bold text-slate-900 text-sm">인터페이스 사전 검측 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        공종 간 누락 및 상충 요소를 3D BIM 기반으로 정밀 대조하고 시공 중 재작업 발생을 사전에 소멸함.
                    </p>
                </div>

                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 2</span>
                        <h4 class="font-bold text-slate-900 text-sm">회의록 & 관리대장 승인 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        모든 인터페이스 협의 사항은 서명된 회의록 및 관리대장으로 일원화하여 책임감리단 승인을 완수함.
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
                <p class="text-slate-700 text-xs font-medium">{d['task']} 관련 회의록, 인터페이스 관리대장 및 감리 승인 문서 사본</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">
                협의 승인 완료
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
                        • <strong>세부 지침:</strong> 관련 분야 도면 1:1 대조 검토를 수행하여 오차 및 상충 요소를 사전에 추출함.
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
                        • <strong>세부 지침:</strong> 신호, 인터록, 제어 랙 및 부스바 연결 부위의 기술적 부합성을 정밀 조율함.
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
                        • <strong>세부 지침:</strong> 3D BIM 기반 공간 검토를 통해 현장 재시공 충격을 사전에 100% 제거함.
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
                        • <strong>세부 지침:</strong> 인터페이스 종합 회의록 및 관리대장에 대해 책임감리단 공학적 결재를 완성함.
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
                        <text x="72.5" y="22" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1. 누락도출 & 검측</text>
                        <text x="12" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 사전 사양/도선 대조</text>
                        <text x="12" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 관로/배선 용량 대조</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="22" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">2. 인터록 & 3D BIM</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 3D 공간 간섭 해소</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 신호/인터록 조율</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="22" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">3. 관리대장 승인</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#15803d">• 종합 회의록 서명</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#15803d">• 감리단 결재 완수</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS {d['wbs']} {d['task']} 회의록 및 관리대장 감리 승인 완수</text>
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
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">시공 전 검측</span>
            </div>
            
            <p class="text-slate-800 leading-relaxed font-semibold">
                본 체크리스트는 동탄트램 전기분야 시공 착수 전 <strong>{d['method']} 관련 16개 핵심 실무 항목을 100% 사전 검측하여 공종 간 간섭 충격 및 재작업 손실을 사전에 소멸하기 위한 필수 서식</strong>입니다.
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
                            <p class="text-slate-800 font-medium leading-relaxed">1. {d['step1_desc']} 사항을 설계도서와 1:1 정밀 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[누락도서 추출 및 협의]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">2. 설계도서 상 누락되거나 모호한 인터페이스 항목을 도출하여 협의하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[기술 사양 부합성]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">3. 전기설비 특기시방서 및 관련 국가 표준 기준 부합성을 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[사전 검측 서표 작성]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">4. 공종 간 인터페이스 착수 전 필수 서표 및 검측 기록을 완료하였는가?</p>
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
                            <p class="text-slate-800 font-medium leading-relaxed">5. {d['step2_desc']} 수칙을 현장 실측 및 신호 시퀀스로 조율하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[배선 및 제어 랙 연동]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">6. 제어반 랙 치수, 배선 트레이 및 단자대 연결 상태를 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[인터록 & 프로토콜 검증]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">7. 차단기/단로기 인터록 시퀀스 및 통신 프로토콜 신호 맵을 검측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[유지보수 편의기능]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">8. 유지보수자 안전 및 관리 편의성이 확보되었는지 실무 검토하였는가?</p>
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
                            <p class="text-slate-800 font-medium leading-relaxed">9. {d['step3_desc']} 항목을 정밀 실측 및 3D BIM 검토하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[3D BIM 공간 간섭 소멸]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">10. 3D BIM 클래시(Clash) 분석을 통해 공간 간섭을 100% 사전에 소멸시켰는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[재작업 원인 차단]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">11. 현장 시공 중 굴착 및 파쇄 재시공 요소를 미연에 차단하였는가?</p>
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
                            <p class="text-slate-800 font-medium leading-relaxed">12. 사전 검측 중 지적된 부적합 사항에 대한 시정 조치를 완료하였는가?</p>
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
                            <p class="text-slate-800 font-medium leading-relaxed">13. {d['step4_desc']} 회의록을 작성하고 관련자 서명을 완수하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[인터페이스 관리대장 수록]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">14. 이행 마일스톤 및 공종별 확인 결과가 명시된 인터페이스 관리대장을 작성하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[책임감리단 결재 승인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">15. 책임감리원 입회 검측을 수검하고 인터페이스 최종 결재를 완료받았는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[공식 문서 배포 및 보관]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">16. 승인 완료된 문서를 관련 공종 및 운영사에 공식 전달하고 공무 대장에 보관하였는가?</p>
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

all_items = [wbs_4, wbs_5, wbs_6]

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

print("\nSUCCESSFULLY UPDATED ALL 9 HTML FILES FOR WBS 9000-3-4, 5, 6!")
