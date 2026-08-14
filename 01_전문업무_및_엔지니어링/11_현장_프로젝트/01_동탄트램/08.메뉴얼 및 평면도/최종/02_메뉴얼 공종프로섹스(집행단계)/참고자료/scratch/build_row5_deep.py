import os, sys

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반\4_착수전 측량 Data 확인'
os.makedirs(os.path.join(base_dir, '표준서'), exist_ok=True)
os.makedirs(os.path.join(base_dir, '수행지침'), exist_ok=True)
os.makedirs(os.path.join(base_dir, '체크리스트'), exist_ok=True)

# 1. Row 5 표준서 HTML
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - 착수전 측량 Data 확인 표준서 (WBS 9000-7-4)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Noto Sans KR', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Survey Standard (WBS 9000-7-4)</span>
        <h1 class="text-3xl font-black mt-2">착수전 측량 Data 확인 표준서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: 9000-7-4 | 주관: 현장 공사팀 / 측량팀 | "GRS80 세계측지계 & CP/TBM 공학적 검측 표준"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-8">
        
        <!-- ⚖️ 근거 법령, 국가 설계기준 및 입찰안내서 검토 기준 -->
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 공간정보관리법 · 국가 측량기준 (Geospatial Survey Standard)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">GRS80 세계측지계</span>
            </div>
            
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 공간정보의 구축 및 관리 등에 관한 법률, <strong>공공측량 작업규정 및 KCS 47 10 25 (강화노반)</strong>에 의거하여, 상부강화노반 공사 착수 전 발주처 제공 CP(가구구조점) 및 TBM(수준점) 측량 성과표와 현장 토탈스테이션/GNSS 측량 데이터를 1:1 검증하는 표준 규정입니다.
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                
                <div class="bg-amber-50/70 p-4 rounded-xl border border-amber-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-amber-900 text-xs">📌 1. 발주처 CP/TBM 성과표 인수</span>
                        <span class="text-[10px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded border border-amber-300">단계 1</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"발주처 인계 기준점(CP, TBM) 성과표 인수 및 GRS80 좌표계(X, Y, Z) 도면 매핑 확인"</strong>
                    </p>
                </div>

                <div class="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-indigo-900 text-xs">📐 2. 현장 재측량 & 허용오차 검증</span>
                        <span class="text-[10px] bg-indigo-200 text-indigo-900 font-bold px-2 py-0.5 rounded border border-indigo-300">단계 2</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"광학 토탈스테이션 & RTK-GNSS 현장 대조 측량, 수준측량 오차 ≤ 5mm√K 수칙 검증"</strong>
                    </p>
                </div>

                <div class="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-emerald-900 text-xs">🛡️ 3. 인조점(TBM) 설치 & 보존</span>
                        <span class="text-[10px] bg-emerald-200 text-emerald-900 font-bold px-2 py-0.5 rounded border border-emerald-300">단계 3</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"공사 중 망실 방지를 위한 쇄석 노반 인근 인조점 3개소 추가 매설 및 콘크리트 보호주 설치"</strong>
                    </p>
                </div>

                <div class="bg-sky-50/70 p-4 rounded-xl border border-sky-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-sky-900 text-xs">📄 4. 측량 야장 결재 & 3D BIM 승인</span>
                        <span class="text-[10px] bg-sky-200 text-sky-900 font-bold px-2 py-0.5 rounded border border-sky-300">단계 4</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"착수전 측량 성과표, 야장 작성 후 책임감리단 공학적 입회 결재 및 3D BIM 좌표계 승인"</strong>
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
                동탄트램 상부강화노반 시공 착수 전, 발주처에서 인계받은 측량 기준점(CP, TBM)과 설계 도면의 좌표를 <strong>GRS80 세계측지계 기준으로 정밀 대조 검증하고, 현장 광학 재측량을 통해 공사 중 표고 오차(±10mm 이내) 및 중심선 이탈을 사전에 100% 소멸함</strong>에 있다.
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
                        <h4 class="font-bold text-slate-900 text-sm">측량 허용오차 준수 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        기준점 간 수준 왕복 측량 오차는 5mm√K (K: 측량거리 km) 이내이어야 하며, 공학 기준 초과 시 재측량을 실시함.
                    </p>
                </div>

                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 2</span>
                        <h4 class="font-bold text-slate-900 text-sm">인조점(TBM) 보존 및 관리 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        성토 및 쇄석 포설 시 망실되지 않는 안전 구역에 TBM 3개소를 인조 설치하고 주간 단위로 표고 변위를 점검함.
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
                <p class="text-slate-700 text-xs font-medium">착수전 측량 성과표, CP/TBM 인조점 위치도, 측량 야장 및 감리 승인서</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">
                측량 승인 완료
            </span>
        </div>

    </div>
</div>
</body>
</html>
"""

# 2. Row 5 수행지침 HTML
gui_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - 착수전 측량 Data 확인 상세 수행지침서 (WBS 9000-7-4)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        .clickable-diagram {
            cursor: zoom-in !important;
            transition: all 0.25s ease !important;
            position: relative !important;
        }
        .clickable-diagram:hover {
            transform: scale(1.01) !important;
            box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important;
        }
        .clickable-diagram::after {
            content: "🔍 클릭하여 대형 확대보기";
            position: absolute; bottom: 12px; right: 16px;
            background: rgba(15, 23, 42, 0.8); color: #ffffff;
            font-size: 11px; font-weight: 700; padding: 4px 12px;
            border-radius: 20px; backdrop-filter: blur(4px);
            pointer-events: none; opacity: 0.9;
        }
        .zoom-modal {
            display: none; position: fixed; z-index: 9999;
            left: 0; top: 0; width: 100%; height: 100%;
            overflow: auto; background-color: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(6px); align-items: center; justify-content: center;
        }
        .zoom-modal.active { display: flex; }
        .zoom-modal-content {
            background-color: #ffffff; margin: auto; padding: 28px;
            border: 1px solid #cbd5e1; width: 95%; max-width: 1100px; max-height: 90vh;
            border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative; overflow-y: auto; text-align: center;
        }
        .zoom-close {
            color: #64748b; position: absolute; right: 20px; top: 16px;
            font-size: 32px; font-weight: bold; cursor: pointer;
        }
        .zoom-close:hover { color: #ef4444; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Survey Guideline (WBS 9000-7-4)</span>
        <h1 class="text-3xl font-black mt-2">착수전 측량 Data 확인 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: 9000-7-4 | 주관: 현장 공사팀 / 측량팀 | "GRS80 좌표 대조 & 측량 실무 가이드라인"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        
        <!-- 💡 검토 개요 및 목표 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 착수전 측량 Data 확인 실무 수행 개요</h4>
            <p class="bg-white p-4 rounded-xl border border-amber-300 font-medium text-slate-900 leading-relaxed text-xs sm:text-sm">
                본 지침서는 동탄트램 상부강화노반 공사 착수 전 <strong>1) 발주처 기준점(CP, TBM) 인수, 2) 현장 광학 토탈스테이션/GNSS 재측량을 통한 오차(≤5mm√K) 검증, 3) 인조점(TBM) 보존 설치, 4) 3D BIM CAD 좌표 매핑 및 감리 승인</strong>을 통해 노반 표고 및 종횡단 구배 정밀도를 확보하기 위한 실무 절차서입니다.
            </p>
        </div>

        <!-- 🚀 4단계 상세 검토 방법 및 수행 절차 -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🛠️</span> 착수전 측량 4단계 상세 수행 절차
            </h2>

            <div class="grid grid-cols-1 gap-6">
                
                <!-- STEP 1 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 01</span>
                            <h3 class="font-bold text-base text-slate-900">기준점(CP/TBM) 인수 및 도서 1:1 대조</h3>
                        </div>
                        <span class="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">단계 1</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 발주처 인계 CP(가구점) 및 TBM(수준점) 성과표 데이터를 수령하고 GRS80 세계측지계 좌표계와 도면을 대조함.<br>
                        • <strong>세부 지침:</strong> 현장 인접 국가 기준점 및 궤도 중심선 평면 좌표(X, Y) 및 계획 표고(Z)를 100% 매핑함.
                    </p>
                </div>

                <!-- STEP 2 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-indigo-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 02</span>
                            <h3 class="font-bold text-base text-slate-900">현장 광학 재측량 및 공학 오차 검증</h3>
                        </div>
                        <span class="text-xs font-semibold text-indigo-700 bg-indigo-100 px-2.5 py-0.5 rounded-full">단계 2</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 정밀 오차 1초급 광학 토탈스테이션과 RTK-GNSS 장비를 활용하여 현장 왕복 수준 측량을 시행함.<br>
                        • <strong>세부 지침:</strong> 왕복 폐합 오차가 5mm√K 이내임을 확인하고, 규격 초과 시 즉시 재측량을 정밀 수행함.
                    </p>
                </div>

                <!-- STEP 3 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 03</span>
                            <h3 class="font-bold text-base text-slate-900">인조점(TBM) 설치 및 보호주 보존</h3>
                        </div>
                        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">단계 3</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 성토 및 토공 작업으로 기준점이 망실되지 않도록 공사 영향권 밖 안전 구역에 인조점 3개소를 매설함.<br>
                        • <strong>세부 지침:</strong> 콘크리트 타설 보호주와 황색 깃발을 설치하고 주간 단위 레벨 오차를 추적 대장에 기록함.
                    </p>
                </div>

                <!-- STEP 4 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-teal-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 04</span>
                            <h3 class="font-bold text-base text-slate-900">측량 성과표 결재 & 3D BIM 승인</h3>
                        </div>
                        <span class="text-xs font-semibold text-teal-700 bg-teal-100 px-2.5 py-0.5 rounded-full">단계 4</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 착수전 측량 성과표, 야장 및 CP/TBM 인조점 종합 위치도를 결재 서식으로 정리함.<br>
                        • <strong>세부 지침:</strong> 책임감리원 입회하에 측량 결과를 검측 수검하고 3D BIM CAD 데이터 최종 승인을 완성함.
                    </p>
                </div>

            </div>
        </div>

        <!-- 🖼️ 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🖼️</span> 착수전 측량 Data 확인 상세 수행 절차도
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_9000_7_4', '[WBS 9000-7-4] 착수전 측량 Data 확인 상세 수행 절차도')">
                <svg id="svg_9000_7_4" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="200" fill="#f8fafc" rx="8"/>
                    <rect x="15" y="15" width="520" height="170" fill="#ffffff" stroke="#d97706" stroke-width="2" rx="6"/>
                    <text x="275" y="38" font-size="13" font-weight="black" fill="#b45309" text-anchor="middle">📐 동탄트램 착수전 측량 Data 검증 절차도</text>
                    <line x1="25" y1="46" x2="525" y2="46" stroke="#e2e8f0" stroke-width="1.5"/>
                    
                    <g transform="translate(25, 55)">
                        <rect x="0" y="0" width="145" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="6"/>
                        <text x="72.5" y="22" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1. CP/TBM 성과 인수</text>
                        <text x="12" y="45" font-size="8" font-weight="bold" fill="#0f172a">• GRS80 세계측지계</text>
                        <text x="12" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 도면 좌표 1:1 대조</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="22" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">2. 현장 광학 재측량</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 토탈스테이션 / RTK</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 오차 ≤ 5mm√K 검증</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="22" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">3. 3D BIM 감리승인</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#15803d">• 측량 성과표 작성</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#15803d">• 감리단 입회 결재</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS 9000-7-4 착수전 측량 성과표 및 3D BIM 좌표 감리 승인 완수</text>
                </svg>
            </div>
        </div>

    </div>
</div>

<!-- 🟣 시공 도식 확대 팝업 모달 -->
<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 착수전 측량 Data 확인 2D Visual 도식 확대 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
    </div>
</div>

<script>
    function openDiagramZoom(elementId, titleText) {
        const srcEl = document.getElementById(elementId);
        if (!srcEl) return;
        
        const zoomBody = document.getElementById('zoomBody');
        document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "착수전 측량 Data 확인 도식 대형 확대 보기");
        zoomBody.innerHTML = srcEl.outerHTML;
        
        const innerSvg = zoomBody.querySelector('svg');
        if (innerSvg) {
            innerSvg.setAttribute('width', '100%');
            innerSvg.setAttribute('height', '520px');
            innerSvg.style.maxWidth = '1050px';
        }
        document.getElementById('zoomModal').classList.add('active');
    }

    function closeZoomModal() {
        document.getElementById('zoomModal').classList.remove('active');
    }

    function closeZoomModalOutside(event) {
        if (event.target.id === 'zoomModal') closeZoomModal();
    }

    window.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeZoomModal();
    });
</script>
</body>
</html>
"""

# 3. Row 5 체크리스트 HTML
chk_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - 착수전 측량 Data 확인 체크리스트 (WBS 9000-7-4)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Noto Sans KR', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Survey Checklist (WBS 9000-7-4)</span>
        <h1 class="text-3xl font-black mt-2">착수전 측량 Data 확인 체크리스트</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: 9000-7-4 | 주관: 현장 공사팀 / 측량팀 | "16개 정밀 검측 문항 1:1 수평대응 서식 (~하였는가? 어미 100% 통일)"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-6">
        
        <!-- 💡 체크리스트 점검의 핵심 의미 -->
        <div class="bg-amber-50 border-2 border-amber-300 p-5 sm:p-6 rounded-2xl text-xs text-amber-950 space-y-3 shadow-sm">
            <div class="flex items-center justify-between border-b border-amber-200 pb-2.5">
                <h4 class="font-black text-sm text-amber-900 flex items-center gap-2">
                    <span class="text-base">⚠️</span> 착수전 측량 Data 확인 체크리스트 점검의 핵심 의미
                </h4>
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">공간 정보 검측</span>
            </div>
            
            <p class="text-slate-800 leading-relaxed font-semibold">
                본 체크리스트는 상부강화노반 시공 착수 전 <strong>발주처 인계 CP/TBM 성과표 대조, 광학 토탈스테이션 현장 재측량 오차(≤5mm√K) 검증, 인조점 3개소 매설 및 3D BIM CAD 좌표계 일치성 관련 16개 핵심 항목을 100% 사전 검측하여 측량 오차로 인한 시공 재작업을 사전에 소멸하기 위한 필수 서식</strong>입니다.
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
                            <span class="font-bold text-slate-900 text-xs">성과표 인수 & 대조</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[CP/TBM 성과 인수]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">1. 발주처에서 인계한 가구점(CP) 및 수준점(TBM) 측량 성과표 데이터를 인수하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[GRS80 좌표계 확인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">2. 설계 도면의 좌표계가 GRS80 세계측지계에 정확히 매핑되었음을 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[측량 장비 교정]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">3. 현장 사용 토탈스테이션 및 RTK-GNSS 장비의 공인 교정성적서를 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[선로 중심선 확인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">4. 트램 선로 중심선 및 종단 구배 레벨 계산 데이터를 도면과 검증하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">현장 재측량 & 오차</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[수준 측량 오차 검증]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">5. 기준점 왕복 수준 측량 오차가 5mm√K (K: km) 이내임을 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[평면 좌표(X, Y) 재측]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">6. 토탈스테이션 삼각 다각형 측량을 통해 평면 위치 오차 허용치를 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[용지 경계선 검측]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">7. 용지 경계 말뚝 위치가 지적도 및 현장 굴착 경계와 일치함을 검측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[기준점 망실 점검]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">8. 발주처 CP점 현장 훼손 및 침하 여부를 전수 점검하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">인조점 매설 & 보존</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[TBM 3개소 추가 설치]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">9. 공사 영향권 바깥 안정된 위치에 인조점(TBM) 3개소를 매설하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[콘크리트 보호주]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">10. 인조점 주위에 콘크리트 타설 보호주 및 위험 표지판을 설치하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[인조점 위치도 작성]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">11. 추가 매설된 TBM 인조점 범주 위치도를 CAD로 작성하여 보관하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[주간 점검 대장]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">12. 토공 다짐 중 TBM 변위 발생 여부를 주간 단위 대장으로 관리하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">성과표 작성 & 승인</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[측량 야장 정리]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">13. 현측 정밀 야장 및 수준 왕복 계산서를 공식 서식으로 정리하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[3D BIM CAD 승인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">14. 측량 데이터를 3D BIM 모델 좌표계와 정밀 동기화하여 승인받았는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[책임감리 입회 결재]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">15. 착수전 측량 성과표에 대해 책임감리원 공학적 입회 결재를 수검하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[공무 대장 등록]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">16. 승인된 측량 성과표를 현장 공무 대장에 철하고 시공팀에 인계하였는가?</p>
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

# 파일 작성 실행
with open(os.path.join(base_dir, '표준서', '착수전 측량 Data 확인_표준서.html'), 'w', encoding='utf-8') as f:
    f.write(std_html)

with open(os.path.join(base_dir, '수행지침', '착수전 측량 Data 확인_수행지침.html'), 'w', encoding='utf-8') as f:
    f.write(gui_html)

with open(os.path.join(base_dir, '체크리스트', '착수전 측량 Data 확인_체크리스트.html'), 'w', encoding='utf-8') as f:
    f.write(chk_html)

print("Row 5 [9000-7-4 착수전 측량 Data 확인] 3개 HTML 딥빌드 완수!")
