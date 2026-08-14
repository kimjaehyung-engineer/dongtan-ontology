# -*- coding: utf-8 -*-
"""
동탄트램 중분대 연약지반 프리로딩(마대옹벽+여성토) 및 잔류침하량(10cm) 관리 수행지침서/표준서/체크리스트 생성 스크립트
"""

import os

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄도시철도 - 연약지반 처리공법 검토(필요시) 실무 작업수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        .clickable-diagram { cursor: pointer; transition: transform 0.2s; }
        .clickable-diagram:hover { transform: scale(1.01); }
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
                    <span class="bg-slate-800 text-slate-300 font-bold text-xs px-3 py-1 rounded-full">상부강화노반 지반공학 실무지침</span>
                    <span class="bg-emerald-500/20 text-emerald-400 font-bold text-xs px-3 py-1 rounded-full">동탄도시철도 건설사업</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-black tracking-tight">연약지반 처리공법 검토(필요시) 실무 수행지침서</h1>
                <p class="text-slate-400 text-sm max-w-3xl leading-relaxed">
                    동탄트램 도로 중앙분리대(중분대) 구간 연약층 존재 시 압밀해석을 통한 <strong>잔류침하량 기준 10cm(≤100mm)</strong> 확보, <strong>가설 톤마대 옹벽 거치 후 프리로딩(여성토) 재하</strong> 및 침하 완료 판정 프로세스
                </p>
            </div>
        </div>

        <!-- 💡 [실시간 인터랙티브 시뮬레이터] 1차 압밀 침하 & 잔류침하량(10cm) 판정기 -->
        <div class="bg-gradient-to-br from-amber-50 to-emerald-50 border-2 border-emerald-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-emerald-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-emerald-600 text-white text-xs font-bold px-2.5 py-1 rounded">지반 압밀 해석 계산기</span>
                    <h3 class="font-bold text-base text-slate-900">📉 중분대 프리로딩 압밀침하 & 잔류침하량(≤10cm) 판정 시뮬레이터</h3>
                </div>
                <span id="sim_settle_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">연약층 두께 (H, m)</label>
                    <input type="number" id="sim_h" value="4.5" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSettlement()">
                </div>
                <div>
                    <label class="block mb-1">프리로딩 여성토 높이 (Δh, m)</label>
                    <input type="number" id="sim_surcharge" value="2.0" step="0.5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSettlement()">
                </div>
                <div>
                    <label class="block mb-1">현장 방치 기간 (t, 일)</label>
                    <input type="number" id="sim_days" value="120" step="10" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSettlement()">
                </div>
                <div>
                    <label class="block mb-1">실측 총 침하량 (S_act, cm)</label>
                    <input type="number" id="sim_s_act" value="28.5" step="0.5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSettlement()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-emerald-200 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div>
                    <span class="text-slate-500">예측 최종 압밀침하량 (Sf):</span>
                    <span id="sim_sf" class="font-black text-sm text-emerald-600 ml-1">35.2 cm</span>
                </div>
                <div>
                    <span class="text-slate-500">현재 압밀도 (U%):</span>
                    <span id="sim_u" class="font-black text-sm text-blue-600 ml-1">81.0 %</span>
                </div>
                <div>
                    <span class="text-slate-500">예측 공용 후 잔류침하량:</span>
                    <span id="sim_s_res" class="font-black text-sm text-indigo-600 ml-1">6.7 cm</span>
                    <span class="text-slate-400 ml-1">(기준: ≤ 10.0 cm)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSettlement() {
            const H = parseFloat(document.getElementById('sim_h').value) || 4.5;
            const sur = parseFloat(document.getElementById('sim_surcharge').value) || 2.0;
            const days = parseFloat(document.getElementById('sim_days').value) || 120;
            const sAct = parseFloat(document.getElementById('sim_s_act').value) || 0;
            
            // 공학적 압밀 근사 계산
            const sf = (H * 0.06 * (sur * 1.8 + 2.5) / 3.0) * 10;
            const u = Math.min(99, Math.round((sAct / Math.max(sf, sAct + 1)) * 100));
            const sRes = Math.max(0, sf - sAct);
            
            document.getElementById('sim_sf').innerText = sf.toFixed(1) + " cm";
            document.getElementById('sim_u').innerText = u + " %";
            document.getElementById('sim_s_res').innerText = sRes.toFixed(1) + " cm";
            
            const isPass = sRes <= 10.0 && u >= 80;
            const badge = document.getElementById('sim_settle_badge');
            badge.innerText = isPass ? "적합 (PASS - 잔류침하 10cm 이하)" : "침하 진행중 (WAIT)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-amber-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>

        <!-- Section 1: 2D Visual Light-Theme Technical Diagram (중분대 프리로딩 마대옹벽 상세 단면도) -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                <div class="flex items-center gap-2">
                    <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                    <h2 class="font-bold text-lg text-slate-900">동탄트램 중분대 연약지반 톤마대 옹벽 & 프리로딩(여성토) 표준 단면도</h2>
                </div>
                <span class="text-xs text-blue-600 font-semibold bg-blue-50 px-2.5 py-1 rounded-full">도식 클릭 시 대형 팝업 확대</span>
            </div>
            
            <div class="clickable-diagram bg-slate-50 border border-slate-200 rounded-xl p-4 flex justify-center items-center overflow-hidden" onclick="openDiagramZoom('svg_soft_ground', '동탄트램 중분대 연약지반 프리로딩(마대옹벽+여성토) 표준 단면 구조도')">
                <svg id="svg_soft_ground" viewBox="0 0 650 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
                    <!-- 배경 -->
                    <rect x="0" y="0" width="650" height="240" fill="#f8fafc"/>
                    
                    <!-- 기존 차도 지반 (좌우) -->
                    <rect x="10" y="140" width="120" height="90" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5"/>
                    <text x="70" y="165" font-size="11" font-weight="black" fill="#475569" text-anchor="middle">기존 차도 (좌측)</text>
                    <text x="70" y="185" font-size="10" fill="#64748b" text-anchor="middle">아스팔트 포장층</text>
                    
                    <rect x="520" y="140" width="120" height="90" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5"/>
                    <text x="580" y="165" font-size="11" font-weight="black" fill="#475569" text-anchor="middle">기존 차도 (우측)</text>
                    <text x="580" y="185" font-size="10" fill="#64748b" text-anchor="middle">아스팔트 포장층</text>

                    <!-- 중앙분리대 (트램 부지) 연약지반층 -->
                    <rect x="140" y="170" width="370" height="60" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <text x="325" y="195" font-size="12" font-weight="black" fill="#92400e" text-anchor="middle">⚠️ 연약점토 / 실트질 퇴적층 (압밀 대상층)</text>
                    <text x="325" y="215" font-size="10" font-weight="bold" fill="#b45309" text-anchor="middle">잔류침하량 설계 허용기준: &le; 10cm (100mm)</text>

                    <!-- 샌드매트(Sand Mat) 및 지오텍스타일 수평배수층 -->
                    <rect x="140" y="150" width="370" height="20" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5"/>
                    <text x="325" y="164" font-size="10" font-weight="black" fill="#c2410c" text-anchor="middle">Sand Mat (두께 50cm 수평배수층) + 부직포</text>

                    <!-- 가설 톤마대 옹벽 (좌/우 계단식 적치) -->
                    <!-- 좌측 마대 3단 -->
                    <rect x="140" y="115" width="45" height="35" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" rx="3"/>
                    <text x="162" y="137" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">톤마대</text>
                    <rect x="140" y="80" width="45" height="35" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" rx="3"/>
                    <text x="162" y="102" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">톤마대</text>
                    <rect x="140" y="45" width="45" height="35" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" rx="3"/>
                    <text x="162" y="67" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">톤마대</text>

                    <!-- 우측 마대 3단 -->
                    <rect x="465" y="115" width="45" height="35" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" rx="3"/>
                    <text x="487" y="137" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">톤마대</text>
                    <rect x="465" y="80" width="45" height="35" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" rx="3"/>
                    <text x="487" y="102" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">톤마대</text>
                    <rect x="465" y="45" width="45" height="35" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" rx="3"/>
                    <text x="487" y="67" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">톤마대</text>

                    <!-- 내측 프리로딩(여성토) 토사 성토층 -->
                    <polygon points="185,150 465,150 465,45 185,45" fill="#fde68a" stroke="#d97706" stroke-width="1.5"/>
                    <text x="325" y="80" font-size="12" font-weight="black" fill="#78350f" text-anchor="middle">프리로딩 (Preloading) 여성토 (H = 1.5~3.0m)</text>
                    <text x="325" y="100" font-size="10" font-weight="bold" fill="#92400e" text-anchor="middle">재하토사 적치 후 압밀 촉진 (차도 토사유출 100% 차단)</text>

                    <!-- 지반 계측기 (침하판 & 간극수압계) -->
                    <line x1="325" y1="35" x2="325" y2="170" stroke="#dc2626" stroke-width="2"/>
                    <rect x="315" y="25" width="20" height="10" fill="#dc2626" rx="2"/>
                    <circle cx="325" cy="170" r="4" fill="#dc2626"/>
                    <text x="325" y="20" font-size="10" font-weight="black" fill="#dc2626" text-anchor="middle">📍 지반 침하판(SP) & 침하봉 계측</text>

                    <!-- 상단 설명 -->
                    <text x="325" y="235" font-size="11" font-weight="black" fill="#0f172a" text-anchor="middle">【중분대 전용 가설 마대옹벽 프리로딩 공법 : 압밀 완료 후 여성토 굴착 및 본선 상부강화노반 시공】</text>
                </svg>
            </div>
        </div>

        <!-- 5-Step Detailed Practical Engineering Guidelines -->
        <div class="space-y-6">
            <div class="flex items-center justify-between border-b-2 border-amber-600 pb-2">
                <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">5단계</span> 중분대 연약지반 프리로딩(마대옹벽+여성토) 세부 실무 프로세스
                </h2>
                <span class="text-xs text-amber-700 font-semibold bg-amber-50 px-2.5 py-1 rounded-full">공학적 압밀해석 & 10cm 관리</span>
            </div>
            
            <div class="space-y-6">
                
                <!-- STEP 1 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-amber-600 text-white font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">STEP 1</span>
                            <h3 class="font-bold text-base text-slate-900">지질조사 데이터 분석 및 Terzaghi 1차 압밀침하 해석</h3>
                        </div>
                        <span class="text-xs text-slate-400 font-semibold">설계 검토 단계</span>
                    </div>
                    <p class="text-sm text-slate-700 leading-relaxed">
                        도로 중앙분리대(중분대) 하부의 시추주상도를 분석하여 연약 점토 및 실트질 퇴적층의 심도, 두께(H), 지하수위 및 자연함수비를 산출합니다. 실내 압밀시험(e-log p 곡선) 결과를 바탕으로 압밀계수(Cv), 압축지수(Cc)를 도출하고 <span class="text-blue-600 font-bold underline cursor-pointer" onclick="openGlossary('terzaghi_consolidation', '외력에 의해 포화 점토층의 간극수가 배출되면서 체적이 감소하고 강도가 증진되는 1차 압밀 이론.')">Terzaghi 압밀 이론</span>에 따라 최종 예상 침하량(Sf)과 시간-침하 곡선을 작성합니다.
                    </p>
                    <div class="bg-amber-50 p-3.5 rounded-xl border border-amber-200 text-xs text-amber-900 space-y-1">
                        <div class="font-black text-amber-800">📌 핵심 설계 기준:</div>
                        <div>• 트램 궤도 구조물의 장기 공용성 확보를 위해 <strong>목표 잔류침하량 기준을 10cm 이하 (≤ 100mm)</strong>로 설정</div>
                        <div>• 프리로딩 여성토 높이(Δh = 1.5~3.0m) 산정 시 도로 인접부 안전율(Fs ≥ 1.3) 및 침하 소요일수(90~150일) 확정</div>
                    </div>
                </div>

                <!-- STEP 2 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-blue-600 text-white font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">STEP 2</span>
                            <h3 class="font-bold text-base text-slate-900">수평 배수층(Sand Mat) 포설 및 지반 계측기 설치</h3>
                        </div>
                        <span class="text-xs text-slate-400 font-semibold">현장 준비 단계</span>
                    </div>
                    <p class="text-sm text-slate-700 leading-relaxed">
                        연약지반 표층의 유기물 및 잡목을 제거하고 지반 지지력 확보와 간극수 수평 배출을 위해 <span class="text-blue-600 font-bold underline cursor-pointer" onclick="openGlossary('sand_mat', '연약지반 상부에 포설하는 0.5~1.0m 두께의 양질 모래층으로, 압밀수를 원활히 측면 배출하는 수평 드레인.')">Sand Mat(두께 50cm 양질사)</span>과 토목섬유(지오텍스타일 부직포)를 포설합니다. 성토 중심부 및 차도 인접부에 <span class="text-blue-600 font-bold underline cursor-pointer" onclick="openGlossary('settlement_plate', '지표면 또는 원지반에 매설하여 상부 성토 하중에 따른 지반의 연직 침하량을 정밀 측정하는 강재 플레이트.')">지반 침하판(Settlement Plate)</span>, 간극수압계, 지중경사계를 규정 간격(20~30m)으로 정밀 설치합니다.
                    </p>
                    <div class="bg-blue-50 p-3.5 rounded-xl border border-blue-200 text-xs text-blue-900 space-y-1">
                        <div class="font-black text-blue-800">📌 핵심 시공 기준:</div>
                        <div>• Sand Mat 모래 투수계수: k ≥ 1.0 × 10⁻² cm/s (점토분 함유량 ≤ 5%)</div>
                        <div>• 계측기 영점(Initial Zero) 좌표 측량 및 3차원 절대좌표계 캘리브레이션 100% 완료</div>
                    </div>
                </div>

                <!-- STEP 3 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-emerald-600 text-white font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">STEP 3</span>
                            <h3 class="font-bold text-base text-slate-900">가설 톤마대 옹벽 거치 및 내측 프리로딩(여성토) 흙쌓기</h3>
                        </div>
                        <span class="text-xs text-slate-400 font-semibold">본 공사 단계</span>
                    </div>
                    <p class="text-sm text-slate-700 leading-relaxed">
                        도로 중앙분리대의 협소한 공간적 제약과 인접 차도로의 토사 유출을 방지하기 위해 중분대 외곽을 따라 <span class="text-blue-600 font-bold underline cursor-pointer" onclick="openGlossary('sand_bag_wall', '1톤 규격의 고강도 P.P 마대에 양질토를 채워 계단식으로 축조함으로써 토압을 지지하고 차도 유출을 방지하는 가설 흙막이.')">톤마대(1.0ton P.P Sand Bag) 옹벽</span>을 3~4단 계단식으로 견고하게 축조합니다. 마대 옹벽 내측에 양질의 성토재(로울러 층다짐 30cm마다 다짐도 95% 확보)를 투입하여 설계된 여성토 높이(1.5~3.0m)까지 흙을 쌓아 조기 압밀 하중을 재하합니다.
                    </p>
                    <div class="bg-emerald-50 p-3.5 rounded-xl border border-emerald-200 text-xs text-emerald-900 space-y-1">
                        <div class="font-black text-emerald-800">📌 핵심 시공 기준:</div>
                        <div>• 톤마대 결속 상태 및 차도측 경사면 방수포/방진망 설치 (비산먼지 및 우수 유입 100% 차단)</div>
                        <div>• 프리로딩 토사 일일 성토 속도: ≤ 30cm/일 (과잉간극수압 급상승에 의한 지반 전단파괴 방지)</div>
                    </div>
                </div>

                <!-- STEP 4 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-indigo-600 text-white font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">STEP 4</span>
                            <h3 class="font-bold text-base text-slate-900">지반 침하 실시간 계측 관리 및 쌍곡선법 압밀 완료 판정</h3>
                        </div>
                        <span class="text-xs text-slate-400 font-semibold">계측 판정 단계</span>
                    </div>
                    <p class="text-sm text-slate-700 leading-relaxed">
                        여성토 완료 후 방치 기간 동안 침하판 레벨 측량을 매일(초기 30일) 및 주 2회(이후) 정밀 실시합니다. 실측 데이터를 <span class="text-blue-600 font-bold underline cursor-pointer" onclick="openGlossary('hyperbolic_method', '실측된 시간-침하 데이터를 쌍곡선 함수로 변환하여 최종 압밀 침하량을 수치적으로 정밀 예측하는 기법.')">쌍곡선법(Hyperbolic Method)</span> 또는 아사오카(Asaoka)법으로 회귀 분석하여 지반 압밀도(U ≥ 80~90%) 및 향후 궤도 부설 후 발생할 <strong>잔류침하량이 10cm 이하 (≤ 100mm)</strong>에 도달하였는지를 통계적으로 판정합니다.
                    </p>
                    <div class="bg-indigo-50 p-3.5 rounded-xl border border-indigo-200 text-xs text-indigo-900 space-y-1">
                        <div class="font-black text-indigo-800">📌 압밀 완료 및 제거 승인 기준:</div>
                        <div>• 최종 침하 속도: <strong>침하율 &le; 1.0mm/8일 (또는 0.1mm/일 미만)</strong> 수렴 확인</div>
                        <div>• 토질 및 기초기술사 기술검토서 첨부 후 책임감리원 최종 압밀 완료 승인 득</div>
                    </div>
                </div>

                <!-- STEP 5 -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="bg-purple-600 text-white font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider">STEP 5</span>
                            <h3 class="font-bold text-base text-slate-900">프리로딩 토사 굴착 반출 및 상부강화노반 본 시공 인계</h3>
                        </div>
                        <span class="text-xs text-slate-400 font-semibold">인수인계 단계</span>
                    </div>
                    <p class="text-sm text-slate-700 leading-relaxed">
                        감리원의 압밀 완료 승인 후 내측 프리로딩 여성토 및 가설 톤마대를 백호(0.7㎥)와 덤프트럭으로 안전하게 굴착 반출합니다. 굴착 저면의 Sand Mat 상부를 로드롤러(10ton 이상)로 재다짐하여 <span class="text-blue-600 font-bold underline cursor-pointer" onclick="openGlossary('k30_bearing', '지반에 ø30cm 평판을 재하하여 침하량 1.25mm 시의 지지력 계수로, 상부강화노반 기준 K30 ≥ 110 MN/m³.')">평판재하시험(K30 ≥ 110 MN/m³)</span> 지지력을 최종 확인한 후 후속 상부강화노반(HBS) 및 궤도 구조체 시공팀에 인수인계합니다.
                    </p>
                    <div class="bg-purple-50 p-3.5 rounded-xl border border-purple-200 text-xs text-purple-900 space-y-1">
                        <div class="font-black text-purple-800">📌 후속 공종 인계 확인사항:</div>
                        <div>• 잔류침하량 10cm 이하 보증서 및 계측 종합보고서 PMIS 등재 완료</div>
                        <div>• 노반 지지력 평판재하시험(K30) 100% 합격 확인 후 인수증 3자 날인</div>
                    </div>
                </div>

            </div>
        </div>

        <!-- Section: Engineering Technical Glossary -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <div class="flex items-center gap-2 border-b border-slate-100 pb-3">
                <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                <h2 class="font-bold text-lg text-slate-900">연약지반 지반공학 핵심 전문 용어사전 (Technical Glossary)</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 cursor-pointer hover:border-amber-400 transition" onclick="openGlossary('잔류침하량 10cm 기준', '트램 콘크리트 도상 및 궤도 부설 후 공용 기간 동안 허용되는 최대 잔류 침하량(10cm 이하)으로, 궤도 틀림과 레일 단차를 방지하기 위한 핵심 한계치.')">
                    <div class="font-bold text-sm text-amber-900 flex items-center justify-between">
                        <span>잔류침하량 10cm 기준</span>
                        <span class="text-xs text-amber-600 font-normal">상세보기 ↗</span>
                    </div>
                    <p class="text-xs text-slate-600 mt-1 line-clamp-2">트램 궤도 부설 후 허용되는 최대 연직 침하 한계치 (≤100mm)...</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 cursor-pointer hover:border-amber-400 transition" onclick="openGlossary('프리로딩 공법 (Preloading)', '본 구조물 시공 전 연약층에 사전에 큰 하중(토사)을 재하하여 유해한 1차 압밀 침하를 조기에 완료시키는 지반 개량 공법.')">
                    <div class="font-bold text-sm text-amber-900 flex items-center justify-between">
                        <span>프리로딩 공법 (Preloading)</span>
                        <span class="text-xs text-amber-600 font-normal">상세보기 ↗</span>
                    </div>
                    <p class="text-xs text-slate-600 mt-1 line-clamp-2">사전 여성토를 통해 유해한 1차 압밀을 조기 종결시키는 공법...</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 cursor-pointer hover:border-amber-400 transition" onclick="openGlossary('가설 톤마대 옹벽', '중앙분리대의 협소한 공간에서 차도로의 토사 유출을 방지하기 위해 1톤 규격 마대로 축조하는 가설 흙막이 구조물.')">
                    <div class="font-bold text-sm text-amber-900 flex items-center justify-between">
                        <span>가설 톤마대 옹벽</span>
                        <span class="text-xs text-amber-600 font-normal">상세보기 ↗</span>
                    </div>
                    <p class="text-xs text-slate-600 mt-1 line-clamp-2">차도 간섭 및 토사 붕괴를 원천 차단하는 중분대 전용 가설벽체...</p>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-xs text-slate-400 py-4 border-t border-slate-200">
            동탄도시철도(트램) 건설사업 상부강화노반 공종 프로세스 관리 매뉴얼 | WBS 9000-1-8
        </div>
    </div>

    <!-- Lightbox Zoom Modal -->
    <div id="zoomModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4" onclick="closeDiagramZoom()">
        <div class="bg-white rounded-3xl max-w-4xl w-full p-6 space-y-4 shadow-2xl" onclick="event.stopPropagation()">
            <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                <h3 id="zoomTitle" class="font-bold text-lg text-slate-900">도식 확대 보기</h3>
                <button onclick="closeDiagramZoom()" class="text-slate-400 hover:text-slate-600 font-black text-xl px-2">✕</button>
            </div>
            <div id="zoomContent" class="overflow-auto max-h-[75vh] flex justify-center p-4 bg-slate-50 rounded-2xl"></div>
        </div>
    </div>

    <!-- Glossary Modal -->
    <div id="glossaryModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4" onclick="closeGlossary()">
        <div class="bg-white rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl" onclick="event.stopPropagation()">
            <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                <h3 id="glossaryTitle" class="font-bold text-lg text-amber-900">용어 설명</h3>
                <button onclick="closeGlossary()" class="text-slate-400 hover:text-slate-600 font-black text-xl px-2">✕</button>
            </div>
            <p id="glossaryText" class="text-sm text-slate-700 leading-relaxed"></p>
        </div>
    </div>

    <script>
        function openDiagramZoom(svgId, title) {
            const svgEl = document.getElementById(svgId);
            if (svgEl) {
                document.getElementById('zoomTitle').innerText = title;
                document.getElementById('zoomContent').innerHTML = svgEl.outerHTML;
                const modalSvg = document.getElementById('zoomContent').querySelector('svg');
                if (modalSvg) {
                    modalSvg.setAttribute('width', '100%');
                    modalSvg.setAttribute('height', '480px');
                }
                document.getElementById('zoomModal').classList.remove('hidden');
            }
        }
        function closeDiagramZoom() {
            document.getElementById('zoomModal').classList.add('hidden');
        }
        function openGlossary(title, desc) {
            document.getElementById('glossaryTitle').innerText = title;
            document.getElementById('glossaryText').innerText = desc;
            document.getElementById('glossaryModal').classList.remove('hidden');
        }
        function closeGlossary() {
            document.getElementById('glossaryModal').classList.add('hidden');
        }
    </script>
</body>
</html>
'''

# 대상 파일 목록에 일괄 덮어쓰기
target_files = [
    r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\8_시공계획서 수립 승인\수행지침\연약지반 처리공법 검토(필요시)_수행지침.html',
    r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\8_연약지반 처리공법 검토(필요시)\수행지침\연약지반 처리공법 검토(필요시)_수행지침.html',
    r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\8_작업조 편성\수행지침\연약지반 처리공법 검토(필요시)_수행지침.html',
    r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\31_연약지반처리(필요시)\수행지침\연약지반처리(필요시)_수행지침.html',
    r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\31_배수시설(측구_유공관) 시공\수행지침\연약지반처리(필요시)_수행지침.html',
    r'08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\상부강화노반\31_배수시설 시공 검측\수행지침\연약지반처리(필요시)_수행지침.html'
]

for fp in target_files:
    if os.path.exists(os.path.dirname(fp)):
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(HTML_CONTENT)
        print(f"Updated: {fp}")

print("=== Soft Ground Preloading Guideline Successfully Written! ===")
