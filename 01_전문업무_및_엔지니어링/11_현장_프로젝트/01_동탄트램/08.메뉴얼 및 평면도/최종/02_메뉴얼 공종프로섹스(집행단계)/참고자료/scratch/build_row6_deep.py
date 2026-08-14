import os, sys

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반\5_지장물이설 협의'
os.makedirs(os.path.join(base_dir, '표준서'), exist_ok=True)
os.makedirs(os.path.join(base_dir, '수행지침'), exist_ok=True)
os.makedirs(os.path.join(base_dir, '체크리스트'), exist_ok=True)

# 1. Row 6 표준서 HTML
std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - 지장물이설 협의 표준서 (WBS 9000-7-5)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Noto Sans KR', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Utility Relocation Standard (WBS 9000-7-5)</span>
        <h1 class="text-3xl font-black mt-2">지장물이설 협의 표준서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: 9000-7-5 | 주관: 현장 공사팀 / 공무팀 | "GPR 탐사 & 줄파기 지장물 이설 감리 승인 표준"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-8">
        
        <!-- ⚖️ 근거 법령, 국가 설계기준 및 입찰안내서 검토 기준 -->
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 지하안전관리에 관한 특별법 · 지장물 관리 표준 (Underground Safety Rules)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">지하안전법 제23조</span>
            </div>
            
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 <strong>지하안전관리에 관한 특별법 제23조, 도로법 제72조 및 KCS 47 10 25 (강화노반)</strong>에 의거하여, 상부강화노반 굴착 및 다짐 구역 내 위치한 지하 매설 지장물(상하수도, 가스, 전력, 통신) 및 지상 구조물을 정밀 탐사하고 관계 기관 협의를 통해 안전하게 이설·방호하는 표준 기준입니다.
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                
                <div class="bg-amber-50/70 p-4 rounded-xl border border-amber-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-amber-900 text-xs">📌 1. GPR 지중 탐사 & 줄파기(시탐)</span>
                        <span class="text-[10px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded border border-amber-300">단계 1</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"지중탐사레이더(GPR) 탐사 및 현장 인력 굴착 줄파기(깊이 1.5~2.0m)를 통한 위치 실측"</strong>
                    </p>
                </div>

                <div class="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-indigo-900 text-xs">📐 2. 점용기관 현장 입회 & 협의</span>
                        <span class="text-[10px] bg-indigo-200 text-indigo-900 font-bold px-2 py-0.5 rounded border border-indigo-300">단계 2</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"지자체, 한전, 가스공사, 통신사 관리주체 담당자 현장 입회 대조 및 이설 협의서 체결"</strong>
                    </p>
                </div>

                <div class="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-emerald-900 text-xs">🛡️ 3. 이설공법 승인 & 안전 방호</span>
                        <span class="text-[10px] bg-emerald-200 text-emerald-900 font-bold px-2 py-0.5 rounded border border-emerald-300">단계 3</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"가이설/방호매설 승인서 수령 및 중장비 굴착 시 관로 손상 방지 안전 매트 및 가림막 설치"</strong>
                    </p>
                </div>

                <div class="bg-sky-50/70 p-4 rounded-xl border border-sky-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-sky-900 text-xs">📄 4. 이설 보고서 & 3D BIM 반영</span>
                        <span class="text-[10px] bg-sky-200 text-sky-900 font-bold px-2 py-0.5 rounded border border-sky-300">단계 4</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"지장물 이설 완료보고서 작성, 3D BIM 좌표 매핑 후 책임감리단 공학적 입회 결재 완수"</strong>
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
                상부강화노반 시공 구간 내 지하 및 지상 지장물 이설 과업을 완수하기 위하여, <strong>GPR 탐사 및 인력 줄파기로 위치를 파악하고, 점용기관 1:1 현장 입회 협의 및 이설 방호 승인을 거쳐 노반 다짐 시 지장물 파손 사고 및 파쇄 재작업 손실을 사전에 100% 소멸함</strong>에 있다.
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
                        <h4 class="font-bold text-slate-900 text-sm">인력 줄파기(시탐) 필수 준수 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        도시가스, 고압전력 케이블 인접 2m 이내 구역은 중장비 굴착을 금지하고 인력 시탐 줄파기로 관로 노출을 검속함.
                    </p>
                </div>

                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 2</span>
                        <h4 class="font-bold text-slate-900 text-sm">관리기관 입회 서명 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        모든 지장물 이설 및 방호 작업은 관할 관리기관 담당자 입회하에 시행하고 서명된 완료 보고서를 대장 수록함.
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
                <p class="text-slate-700 text-xs font-medium">지장물 탐사 성과도, 시탐(줄파기) 야장, 이설 승인서 및 감리 입회 결재서</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">
                이설 승인 완료
            </span>
        </div>

    </div>
</div>
</body>
</html>
"""

# 2. Row 6 수행지침 HTML
gui_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - 지장물이설 협의 상세 수행지침서 (WBS 9000-7-5)</title>
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
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Utility Relocation Guideline (WBS 9000-7-5)</span>
        <h1 class="text-3xl font-black mt-2">지장물이설 협의 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: 9000-7-5 | 주관: 현장 공사팀 / 공무팀 | "지장물 탐사 & 관할기관 이설 실무 가이드라인"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        
        <!-- 💡 검토 개요 및 목표 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 지장물이설 협의 실무 수행 개요</h4>
            <p class="bg-white p-4 rounded-xl border border-amber-300 font-medium text-slate-900 leading-relaxed text-xs sm:text-sm">
                본 지침서는 동탄트램 상부강화노반 시공 구간 내 위치한 지하 매설물 및 지상 장애물에 대하여 <strong>1) GPR 탐사 및 인력 줄파기(시탐), 2) 점용기관 담당자 1:1 현장 입회, 3) 이설/방호 공법 확정 및 승인 수속, 4) 이설 완료 및 3D BIM 좌표 반영</strong>을 통해 노반 다짐 시 사고 예방 및 품질을 확보하는 실무 지침서입니다.
            </p>
        </div>

        <!-- 🚀 4단계 상세 검토 방법 및 수행 절차 -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🛠️</span> 지장물이설 4단계 상세 수행 절차
            </h2>

            <div class="grid grid-cols-1 gap-6">
                
                <!-- STEP 1 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 01</span>
                            <h3 class="font-bold text-base text-slate-900">GPR 지중 탐사 및 인력 줄파기(시탐)</h3>
                        </div>
                        <span class="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">단계 1</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> GPR(지중탐사레이더) 장비로 지하 관로 유무를 탐사한 후, 횡단 방향 1.5m 간격으로 인력 시탐 줄파기를 시행함.<br>
                        • <strong>세부 지침:</strong> 도시가스, 특고압 전력선 인근은 중장비 굴착을 일체 금지하고 인력 작업으로 깊이, 심도 및 매설 방향을 실측함.
                    </p>
                </div>

                <!-- STEP 2 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-indigo-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 02</span>
                            <h3 class="font-bold text-base text-slate-900">관리기관 현장 1:1 입회 및 이설 협의</h3>
                        </div>
                        <span class="text-xs font-semibold text-indigo-700 bg-indigo-100 px-2.5 py-0.5 rounded-full">단계 2</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 화성시, 수원시, 한전, 삼천리가스, 통신사 매설물 담당자를 현장으로 초빙하여 노출 관로를 1:1 실측 대조함.<br>
                        • <strong>세부 지침:</strong> 이설 시기, 우회 노선 및 가이설/방호 공법에 대한 기술 협의서를 작성하고 당사자 서명을 필함.
                    </p>
                </div>

                <!-- STEP 3 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 03</span>
                            <h3 class="font-bold text-base text-slate-900">이설 공사 시행 및 관로 안전 방호</h3>
                        </div>
                        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">단계 3</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 관리기관 승인 공법에 따라 지장물 이설을 시행하고, 존치 관로는 H-Beam 매달기 방호 및 보호관을 매설함.<br>
                        • <strong>세부 지침:</strong> 강동 롤러 다짐 시 진동으로 인한 관부속 파손을 예방하기 위하여 주변 1m 구간은 램머 소형 다짐을 실시함.
                    </p>
                </div>

                <!-- STEP 4 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-teal-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 04</span>
                            <h3 class="font-bold text-base text-slate-900">이설 보고서 승인 및 3D BIM 매핑</h3>
                        </div>
                        <span class="text-xs font-semibold text-teal-700 bg-teal-100 px-2.5 py-0.5 rounded-full">단계 4</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> 지장물 이설 전·후 사진, 준공 위치도 및 관리기관 서명이 수록된 완료보고서를 작성함.<br>
                        • <strong>세부 지침:</strong> 이설 후 지중 관로 좌표를 3D BIM 데이터에 최종 매핑하고 책임감리단 공학적 입회 승인을 결재함.
                    </p>
                </div>

            </div>
        </div>

        <!-- 🖼️ 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🖼️</span> 지장물이설 협의 상세 수행 절차도
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_9000_7_5', '[WBS 9000-7-5] 지장물이설 협의 상세 수행 절차도')">
                <svg id="svg_9000_7_5" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="200" fill="#f8fafc" rx="8"/>
                    <rect x="15" y="15" width="520" height="170" fill="#ffffff" stroke="#d97706" stroke-width="2" rx="6"/>
                    <text x="275" y="38" font-size="13" font-weight="black" fill="#b45309" text-anchor="middle">🚧 동탄트램 지장물 탐사 및 이설 절차도</text>
                    <line x1="25" y1="46" x2="525" y2="46" stroke="#e2e8f0" stroke-width="1.5"/>
                    
                    <g transform="translate(25, 55)">
                        <rect x="0" y="0" width="145" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="6"/>
                        <text x="72.5" y="22" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1. GPR & 인력줄파기</text>
                        <text x="12" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 지중 관로 탐사</text>
                        <text x="12" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 인력 시탐 깊이 실측</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="22" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">2. 기관 입회 & 이설</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 관리기관 1:1 입회</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 매달기 방호/이설</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="22" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">3. 3D BIM 매핑</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#15803d">• 완료보고서 작성</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#15803d">• 감리단 입회 승인</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS 9000-7-5 지장물이설 보고서 및 3D BIM 좌표 감리 승인 완수</text>
                </svg>
            </div>
        </div>

    </div>
</div>

<!-- 🟣 시공 도식 확대 팝업 모달 -->
<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 지장물이설 협의 2D Visual 도식 확대 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
    </div>
</div>

<script>
    function openDiagramZoom(elementId, titleText) {
        const srcEl = document.getElementById(elementId);
        if (!srcEl) return;
        
        const zoomBody = document.getElementById('zoomBody');
        document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "지장물이설 협의 도식 대형 확대 보기");
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

# 3. Row 6 체크리스트 HTML
chk_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - 지장물이설 협의 체크리스트 (WBS 9000-7-5)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Noto Sans KR', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Utility Relocation Checklist (WBS 9000-7-5)</span>
        <h1 class="text-3xl font-black mt-2">지장물이설 협의 체크리스트</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: 9000-7-5 | 주관: 현장 공사팀 / 공무팀 | "16개 정밀 검측 문항 1:1 수평대응 서식 (~하였는가? 어미 100% 통일)"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-6">
        
        <!-- 💡 체크리스트 점검의 핵심 의미 -->
        <div class="bg-amber-50 border-2 border-amber-300 p-5 sm:p-6 rounded-2xl text-xs text-amber-950 space-y-3 shadow-sm">
            <div class="flex items-center justify-between border-b border-amber-200 pb-2.5">
                <h4 class="font-black text-sm text-amber-900 flex items-center gap-2">
                    <span class="text-base">⚠️</span> 지장물이설 협의 체크리스트 점검의 핵심 의미
                </h4>
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">지하안전 검측</span>
            </div>
            
            <p class="text-slate-800 leading-relaxed font-semibold">
                본 체크리스트는 상부강화노반 시공 구역 내 지하/지상 지장물 이설에 대해 <strong>GPR 지중 탐사, 인력 줄파기(시탐), 관리기관 1:1 현장 입회, 이설 승인서 수령, 매달기 방호 및 3D BIM 좌표 반영 관련 16개 핵심 문항을 100% 사전 검측하여 다짐 시 파손 사고를 사전에 예방하기 위한 필수 서식</strong>입니다.
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
                            <span class="font-bold text-slate-900 text-xs">GPR & 시탐 검측</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[GPR 지중 탐사]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">1. GPR(지중탐사레이더) 장비를 활용하여 지하 매설 관로 유무 및 심도를 탐사하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[인력 줄파기(시탐)]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">2. 가스선, 전력선 인근 구역은 인력 줄파기(깊이 1.5m)로 위치를 현장 노출 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[지장물 성과도 작성]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">3. 탐사된 지장물의 규격, 재질, 심도 및 평면 위치도를 1:1 현장 야장으로 도출하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[중장비 작업 통제]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">4. 관로 노출 구역 주변 2m 이내 백호 굴착기 직접 작업 금지를 조치하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">관리기관 1:1 입회</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[점용기관 입회 수검]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">5. 화성시/수원시, 한전, 가스공사 담당자 1:1 현장 입회 대조를 완료하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[이설 협의서 체결]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">6. 이설 분담금, 이설 시기 및 임시 우회 노선에 대한 공식 협의서를 서명 체결하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[이설 승인서 수령]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">7. 관할 행정기관으로부터 도로점용 변경 및 지장물 이설 공가 승인서를 받았는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[안전관리계획서 검토]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">8. 이설 시 2차 사고 예방을 위한 방재 대책이 포함되었는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">관로 방호 & 램머 다짐</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[H-Beam 매달기 방호]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">9. 노출 존치 관로에 대해 H-Beam 및 앙카 체인 매달기 보강 방호를 시공하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[소형 램머 다짐 시공]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">10. 매설 관로 측면 1m 구간은 진동 롤러 대신 소형 램머 층다짐을 시행하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[안전 매트 & 표부]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">11. 관로 상부에 붉은색 라벨 안전 경고 매트를 부설하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[현장 가림막 설치]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">12. 작업 구획 안전 가림막 및 세륜 시설을 가동하였는가?</p>
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
                            <span class="font-bold text-slate-900 text-xs">완료보고 & 3D 매핑</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[이설 완료보고서]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">13. 이설 전·후 현장 사진 및 실측 준공도가 수록된 보고서를 작성하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[3D BIM 좌표 매핑]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">14. 최종 이설된 지중 관로 좌표를 3D BIM 모델에 정밀 업데이트하였는가?</p>
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
                            <p class="text-slate-800 font-medium leading-relaxed">15. 책임감리원 현장 검측 입회를 받고 이설 완료 결재를 마쳤는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[공무 대장 보관]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">16. 승인서 및 인수합의서 사본을 공무 관리대장에 등록 보관하였는가?</p>
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
with open(os.path.join(base_dir, '표준서', '지장물이설 협의_표준서.html'), 'w', encoding='utf-8') as f:
    f.write(std_html)

with open(os.path.join(base_dir, '수행지침', '지장물이설 협의_수행지침.html'), 'w', encoding='utf-8') as f:
    f.write(gui_html)

with open(os.path.join(base_dir, '체크리스트', '지장물이설 협의_체크리스트.html'), 'w', encoding='utf-8') as f:
    f.write(chk_html)

print("Row 6 [9000-7-5 지장물이설 협의] 3개 HTML 딥빌드 완수!")
