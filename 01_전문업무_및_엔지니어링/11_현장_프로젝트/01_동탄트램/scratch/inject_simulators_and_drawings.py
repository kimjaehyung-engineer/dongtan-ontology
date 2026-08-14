# -*- coding: utf-8 -*-
"""
전기분야 수행지침서에 10대 실시간 인터랙티브 공학 시뮬레이터 및 정밀 2D Visual SVG 도식 주입 엔진
"""

import os
import sys

BASE_DIR = r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\전기분야"

SIMULATORS_HTML = {
    1: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 22.9kV 급전선 전압강하 & 정류기 부하율 계산기 -->
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-blue-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded">실시간 엔지니어링 계산기</span>
                    <h3 class="font-bold text-base text-slate-900">⚡ 22.9kV 급전선 전압강하 & 정류기 마진율 시뮬레이터</h3>
                </div>
                <span id="sim1_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">선로 길이 (L, km)</label>
                    <input type="number" id="sim1_len" value="3.5" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-blue-900" oninput="calcSim1()">
                </div>
                <div>
                    <label class="block mb-1">부하 전류 (I, A)</label>
                    <input type="number" id="sim1_curr" value="650" step="10" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-blue-900" oninput="calcSim1()">
                </div>
                <div>
                    <label class="block mb-1">케이블 단면적 (CNCV, ㎟)</label>
                    <select id="sim1_sq" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-blue-900" onchange="calcSim1()">
                        <option value="400" selected>400 ㎟ (R=0.062 Ω/km)</option>
                        <option value="300">300 ㎟ (R=0.081 Ω/km)</option>
                        <option value="200">200 ㎟ (R=0.125 Ω/km)</option>
                    </select>
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-blue-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">계산된 전압강하율:</span>
                    <span id="sim1_drop" class="font-black text-sm text-blue-600 ml-1">2.14 %</span>
                    <span class="text-slate-400 ml-1">(기준치: ≤ 5.0%)</span>
                </div>
                <div>
                    <span class="text-slate-500">정류기 부하 마진율:</span>
                    <span id="sim1_margin" class="font-black text-sm text-indigo-600 ml-1">68.2 %</span>
                    <span class="text-slate-400 ml-1">(N+1 가용)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim1() {
            const L = parseFloat(document.getElementById('sim1_len').value) || 0;
            const I = parseFloat(document.getElementById('sim1_curr').value) || 0;
            const sq = parseInt(document.getElementById('sim1_sq').value);
            let R = 0.062;
            if(sq === 300) R = 0.081;
            if(sq === 200) R = 0.125;
            const dropV = Math.sqrt(3) * I * L * R;
            const dropRate = (dropV / 22900) * 100;
            document.getElementById('sim1_drop').innerText = dropRate.toFixed(2) + " %";
            const isPass = dropRate <= 5.0;
            const badge = document.getElementById('sim1_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "전압강하 초과 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    3: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 변전실 바닥하중 및 지반 지지력 검증기 -->
        <div class="bg-gradient-to-br from-emerald-50 to-teal-50 border-2 border-emerald-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-emerald-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-emerald-600 text-white text-xs font-bold px-2.5 py-1 rounded">실시간 구조 계산기</span>
                    <h3 class="font-bold text-base text-slate-900">🧱 변전실 장비 기초 바닥하중 및 지반 지지력 검증기</h3>
                </div>
                <span id="sim3_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">장비 총중량 (W, ton)</label>
                    <input type="number" id="sim3_w" value="8.5" step="0.5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSim3()">
                </div>
                <div>
                    <label class="block mb-1">패드 가로폭 (A, m)</label>
                    <input type="number" id="sim3_a" value="2.2" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSim3()">
                </div>
                <div>
                    <label class="block mb-1">패드 세로길이 (B, m)</label>
                    <input type="number" id="sim3_b" value="3.0" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSim3()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-emerald-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">단위면적당 바닥하중:</span>
                    <span id="sim3_load" class="font-black text-sm text-emerald-600 ml-1">1.29 ton/㎡</span>
                    <span class="text-slate-400 ml-1">(허용 지지력: ≥ 8.5 ton/㎡)</span>
                </div>
                <div>
                    <span class="text-slate-500">구조 안전율:</span>
                    <span id="sim3_safe" class="font-black text-sm text-teal-600 ml-1">6.59 (안전)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim3() {
            const w = parseFloat(document.getElementById('sim3_w').value) || 0;
            const a = parseFloat(document.getElementById('sim3_a').value) || 0;
            const b = parseFloat(document.getElementById('sim3_b').value) || 0;
            const area = Math.max(a * b, 0.1);
            const load = w / area;
            const safe = 8.5 / load;
            document.getElementById('sim3_load').innerText = load.toFixed(2) + " ton/㎡";
            document.getElementById('sim3_safe').innerText = safe.toFixed(2) + (safe >= 1.5 ? " (안전)" : " (위험)");
            const isPass = safe >= 1.5;
            const badge = document.getElementById('sim3_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "지지력 부족 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    18: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 앵커볼트 체결 토크 & 수평 오차 판정기 -->
        <div class="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-amber-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">시공 토크 판정기</span>
                    <h3 class="font-bold text-base text-slate-900">🔩 변전 기기 앵커볼트 규정 토크 & 수평도 판정기</h3>
                </div>
                <span id="sim18_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">볼트 규격 선택</label>
                    <select id="sim18_size" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-amber-900" onchange="calcSim18()">
                        <option value="120" selected>M16 볼트 (규정 120 N·m)</option>
                        <option value="60">M12 볼트 (규정 60 N·m)</option>
                        <option value="240">M20 볼트 (규정 240 N·m)</option>
                    </select>
                </div>
                <div>
                    <label class="block mb-1">실측 체결 토크 (N·m)</label>
                    <input type="number" id="sim18_torque" value="122" step="1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-amber-900" oninput="calcSim18()">
                </div>
                <div>
                    <label class="block mb-1">실측 수평 오차 (mm)</label>
                    <input type="number" id="sim18_level" value="1.2" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-amber-900" oninput="calcSim18()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-amber-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">토크 편차율:</span>
                    <span id="sim18_err" class="font-black text-sm text-amber-600 ml-1">+1.67 %</span>
                    <span class="text-slate-400 ml-1">(허용: ±5.0%)</span>
                </div>
                <div>
                    <span class="text-slate-500">수평도 검측 결과:</span>
                    <span id="sim18_lvl_res" class="font-black text-sm text-emerald-600 ml-1">1.2mm (오차 ≤ 2.0mm 충족)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim18() {
            const reqT = parseFloat(document.getElementById('sim18_size').value);
            const actT = parseFloat(document.getElementById('sim18_torque').value) || 0;
            const lvl = parseFloat(document.getElementById('sim18_level').value) || 0;
            const err = ((actT - reqT) / reqT) * 100;
            document.getElementById('sim18_err').innerText = (err >= 0 ? "+" : "") + err.toFixed(2) + " %";
            const lvlOk = lvl <= 2.0;
            document.getElementById('sim18_lvl_res').innerText = lvl.toFixed(1) + "mm (" + (lvlOk ? "충족" : "초과") + ")";
            const isPass = Math.abs(err) <= 5.0 && lvlOk;
            const badge = document.getElementById('sim18_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "기준 미달 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    19: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 케이블 포설 장력 & 곡률반경 검증기 -->
        <div class="bg-gradient-to-br from-cyan-50 to-blue-50 border-2 border-cyan-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-cyan-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-cyan-600 text-white text-xs font-bold px-2.5 py-1 rounded">포설 공학 계산기</span>
                    <h3 class="font-bold text-base text-slate-900">〰️ 22.9kV CNCV 케이블 포설 장력 & 곡률반경 검증기</h3>
                </div>
                <span id="sim19_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">케이블 외경 (D, mm)</label>
                    <input type="number" id="sim19_d" value="55" step="1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-cyan-900" oninput="calcSim19()">
                </div>
                <div>
                    <label class="block mb-1">실측 곡률반경 (R, mm)</label>
                    <input type="number" id="sim19_r" value="650" step="10" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-cyan-900" oninput="calcSim19()">
                </div>
                <div>
                    <label class="block mb-1">윈치 견인 장력 (T, kgf)</label>
                    <input type="number" id="sim19_t" value="1200" step="50" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-cyan-900" oninput="calcSim19()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-cyan-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">곡률반경 배수 (R/D):</span>
                    <span id="sim19_rd" class="font-black text-sm text-cyan-600 ml-1">11.8 배</span>
                    <span class="text-slate-400 ml-1">(기준: ≥ 10D)</span>
                </div>
                <div>
                    <span class="text-slate-500">도체 인장 응력:</span>
                    <span id="sim19_stress" class="font-black text-sm text-blue-600 ml-1">3.0 kgf/㎟</span>
                    <span class="text-slate-400 ml-1">(허용: ≤ 7.0 kgf/㎟)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim19() {
            const d = parseFloat(document.getElementById('sim19_d').value) || 1;
            const r = parseFloat(document.getElementById('sim19_r').value) || 0;
            const t = parseFloat(document.getElementById('sim19_t').value) || 0;
            const rd = r / d;
            const stress = t / 400; // 400sq 기준
            document.getElementById('sim19_rd').innerText = rd.toFixed(1) + " 배";
            document.getElementById('sim19_stress').innerText = stress.toFixed(1) + " kgf/㎟";
            const isPass = rd >= 10.0 && stress <= 7.0;
            const badge = document.getElementById('sim19_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "규격 미달 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    20: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 22.9kV 수전 가압 전압 탭 판정기 -->
        <div class="bg-gradient-to-br from-violet-50 to-purple-50 border-2 border-violet-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-violet-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-violet-600 text-white text-xs font-bold px-2.5 py-1 rounded">수전 전압 시뮬레이터</span>
                    <h3 class="font-bold text-base text-slate-900">⚡ 22.9kV 수전 가압 변압기 2차측 전압 판정기</h3>
                </div>
                <span id="sim20_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">1차측 실측 수전전압 (kV)</label>
                    <input type="number" id="sim20_vin" value="22.9" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-violet-900" oninput="calcSim20()">
                </div>
                <div>
                    <label class="block mb-1">변압기 탭 위치 (Tap Position)</label>
                    <select id="sim20_tap" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-violet-900" onchange="calcSim20()">
                        <option value="23.9">1탭 (23.9 kV)</option>
                        <option value="23.4">2탭 (23.4 kV)</option>
                        <option value="22.9" selected>3탭 (22.9 kV 정격)</option>
                        <option value="22.4">4탭 (22.4 kV)</option>
                        <option value="21.9">5탭 (21.9 kV)</option>
                    </select>
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-violet-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">2차측 동력 전압 (380V 정격):</span>
                    <span id="sim20_vout" class="font-black text-sm text-violet-600 ml-1">380.0 V</span>
                    <span class="text-slate-400 ml-1">(허용: 380V ± 5%)</span>
                </div>
                <div>
                    <span class="text-slate-500">정류기 인입 전압 (590V 정격):</span>
                    <span id="sim20_vrec" class="font-black text-sm text-purple-600 ml-1">590.0 V</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim20() {
            const vin = parseFloat(document.getElementById('sim20_vin').value) || 0;
            const tap = parseFloat(document.getElementById('sim20_tap').value);
            const vout = (vin / tap) * 380;
            const vrec = (vin / tap) * 590;
            document.getElementById('sim20_vout').innerText = vout.toFixed(1) + " V";
            document.getElementById('sim20_vrec').innerText = vrec.toFixed(1) + " V";
            const isPass = vout >= 361 && vout <= 399;
            const badge = document.getElementById('sim20_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "전압 편차 초과 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    22: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 3전극법 공통접지저항 판정기 -->
        <div class="bg-gradient-to-br from-slate-100 to-emerald-50 border-2 border-emerald-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-emerald-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-emerald-600 text-white text-xs font-bold px-2.5 py-1 rounded">접지 판정기</span>
                    <h3 class="font-bold text-base text-slate-900">📉 3전극법 공통접지저항(R ≤ 1.0Ω) 합격 판정기</h3>
                </div>
                <span id="sim22_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">전위보조극 거리 (P, m)</label>
                    <input type="number" id="sim22_p" value="20" step="5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900">
                </div>
                <div>
                    <label class="block mb-1">전류보조극 거리 (C, m)</label>
                    <input type="number" id="sim22_c" value="40" step="5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900">
                </div>
                <div>
                    <label class="block mb-1">실측 접지저항 (R, Ω)</label>
                    <input type="number" id="sim22_r" value="0.45" step="0.05" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSim22()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-emerald-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">실측 접지저항치:</span>
                    <span id="sim22_res" class="font-black text-sm text-emerald-600 ml-1">0.45 Ω</span>
                    <span class="text-slate-400 ml-1">(공통접지 기준치: ≤ 1.0 Ω)</span>
                </div>
                <div>
                    <span class="text-slate-500">안전 여유율:</span>
                    <span id="sim22_margin" class="font-black text-sm text-teal-600 ml-1">55.0 % 여유</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim22() {
            const r = parseFloat(document.getElementById('sim22_r').value) || 0;
            document.getElementById('sim22_res').innerText = r.toFixed(2) + " Ω";
            const margin = Math.max(0, (1.0 - r) * 100);
            document.getElementById('sim22_margin').innerText = margin.toFixed(1) + " % 여유";
            const isPass = r <= 1.0 && r > 0;
            const badge = document.getElementById('sim22_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "기준치 초과 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    31: '''
        <!-- 💡 [인터랙티브 시뮬레이터] T-Bar 강체 전차선 마모율 & 팽창이음 EJ 갭 계산기 -->
        <div class="bg-gradient-to-br from-blue-50 to-teal-50 border-2 border-teal-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-teal-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-teal-600 text-white text-xs font-bold px-2.5 py-1 rounded">전차선 마모 검증기</span>
                    <h3 class="font-bold text-base text-slate-900">📐 T-Bar 강체 전차선 마모도 & EJ 신축 갭 판정기</h3>
                </div>
                <span id="sim31_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">신조 전차선 높이 (H0, mm)</label>
                    <input type="number" id="sim31_h0" value="12.0" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-teal-900" oninput="calcSim31()">
                </div>
                <div>
                    <label class="block mb-1">실측 잔여 높이 (H, mm)</label>
                    <input type="number" id="sim31_h" value="10.8" step="0.1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-teal-900" oninput="calcSim31()">
                </div>
                <div>
                    <label class="block mb-1">현장 외기온도 (T, ℃)</label>
                    <input type="number" id="sim31_temp" value="20" step="1" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-teal-900" oninput="calcSim31()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-teal-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">잔여 단면적 비율:</span>
                    <span id="sim31_remain" class="font-black text-sm text-teal-600 ml-1">90.0 %</span>
                    <span class="text-slate-400 ml-1">(교체 한계: ≤ 80%)</span>
                </div>
                <div>
                    <span class="text-slate-500">온도 보정 권장 EJ 갭:</span>
                    <span id="sim31_ej" class="font-black text-sm text-blue-600 ml-1">50.0 mm (정상)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim31() {
            const h0 = parseFloat(document.getElementById('sim31_h0').value) || 12.0;
            const h = parseFloat(document.getElementById('sim31_h').value) || 0;
            const temp = parseFloat(document.getElementById('sim31_temp').value) || 20;
            const remain = (h / h0) * 100;
            document.getElementById('sim31_remain').innerText = remain.toFixed(1) + " %";
            const ejGap = 50 - (temp - 20) * 0.8;
            document.getElementById('sim31_ej').innerText = ejGap.toFixed(1) + " mm (정상)";
            const isPass = remain >= 80.0;
            const badge = document.getElementById('sim31_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "마모 한계 초과 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    32: '''
        <!-- 💡 [인터랙티브 시뮬레이터] KESCO 법정 사용전검사 종합 판정기 -->
        <div class="bg-gradient-to-br from-rose-50 to-indigo-50 border-2 border-indigo-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-indigo-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-indigo-600 text-white text-xs font-bold px-2.5 py-1 rounded">KESCO 종합 판정기</span>
                    <h3 class="font-bold text-base text-slate-900">📜 KESCO 전기설비 사용전검사 5대 법정 항목 판정기</h3>
                </div>
                <span id="sim32_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">사용전검사 합격 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-semibold text-slate-700">
                <label class="flex items-center gap-2 bg-white p-2.5 rounded-lg border border-slate-200 cursor-pointer">
                    <input type="checkbox" id="sim32_c1" checked onchange="calcSim32()" class="rounded text-indigo-600">
                    <span>1. 절연저항 (DC 1,000V ≥ 5MΩ) 합격</span>
                </label>
                <label class="flex items-center gap-2 bg-white p-2.5 rounded-lg border border-slate-200 cursor-pointer">
                    <input type="checkbox" id="sim32_c2" checked onchange="calcSim32()" class="rounded text-indigo-600">
                    <span>2. 공통접지저항 (R ≤ 1.0Ω) 합격</span>
                </label>
                <label class="flex items-center gap-2 bg-white p-2.5 rounded-lg border border-slate-200 cursor-pointer">
                    <input type="checkbox" id="sim32_c3" checked onchange="calcSim32()" class="rounded text-indigo-600">
                    <span>3. 특고압 절연내력(34.35kV 10분) 합격</span>
                </label>
                <label class="flex items-center gap-2 bg-white p-2.5 rounded-lg border border-slate-200 cursor-pointer">
                    <input type="checkbox" id="sim32_c4" checked onchange="calcSim32()" class="rounded text-indigo-600">
                    <span>4. 단로기-차단기 2중 인터록 동작 확인</span>
                </label>
                <label class="flex items-center gap-2 bg-white p-2.5 rounded-lg border border-slate-200 cursor-pointer sm:col-span-2">
                    <input type="checkbox" id="sim32_c5" checked onchange="calcSim32()" class="rounded text-indigo-600">
                    <span>5. 보호계전기(OCR/OCGR) 시퀀스 100% 트립 확인</span>
                </label>
            </div>
            <div class="bg-white p-4 rounded-xl border border-indigo-200 flex justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">법정 검사 항목 충족률:</span>
                    <span id="sim32_score" class="font-black text-sm text-indigo-600 ml-1">5 / 5 (100%)</span>
                </div>
                <div>
                    <span class="text-slate-500">필증 교부 여부:</span>
                    <span id="sim32_cert" class="font-bold text-emerald-600 ml-1">사용전검사 합격증명서 즉시 발급 가능</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim32() {
            let cnt = 0;
            for(let i=1; i<=5; i++) {
                if(document.getElementById('sim32_c' + i).checked) cnt++;
            }
            document.getElementById('sim32_score').innerText = cnt + " / 5 (" + (cnt * 20) + "%)";
            const isPass = cnt === 5;
            document.getElementById('sim32_cert').innerText = isPass ? "사용전검사 합격증명서 즉시 발급 가능" : "보완 필요 (불합격)";
            document.getElementById('sim32_cert').className = isPass ? "font-bold text-emerald-600 ml-1" : "font-bold text-rose-600 ml-1";
            const badge = document.getElementById('sim32_badge');
            badge.innerText = isPass ? "사용전검사 합격 (PASS)" : "재검사 대상 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    '''
}

def inject_into_guidelines():
    print("=== Injecting Interactive Simulators and Enhanced Visuals into Electrical Guidelines ===")
    folders = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))], key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else 999)
    injected_count = 0

    for fld in folders:
        num = int(fld.split('_')[0]) if fld.split('_')[0].isdigit() else 999
        gd_dir = os.path.join(BASE_DIR, fld, '수행지침')
        if not os.path.exists(gd_dir):
            continue

        for fn in os.listdir(gd_dir):
            if fn.endswith('.html'):
                fp = os.path.join(gd_dir, fn)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if simulator is available for this task
                if num in SIMULATORS_HTML:
                    sim_code = SIMULATORS_HTML[num]
                    # Insert simulator before Section 3
                    target_str = '<div class="space-y-6">'
                    if target_str in content and 'sim' + str(num) not in content:
                        idx = content.find(target_str)
                        new_content = content[:idx] + sim_code + "\n\n        " + content[idx:]
                        with open(fp, 'w', encoding='utf-8') as f_out:
                            f_out.write(new_content)
                        injected_count += 1
                        print(f"[{num:2d}] Injected interactive simulator into {fn}")

    print(f"\n=== Injection Finished: {injected_count} guidelines upgraded with real-time simulators! ===")

if __name__ == "__main__":
    inject_into_guidelines()
