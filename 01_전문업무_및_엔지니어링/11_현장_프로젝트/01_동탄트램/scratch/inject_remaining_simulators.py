# -*- coding: utf-8 -*-
"""
전기분야 수행지침서 24번(가선 압상량) & 27번(고조파 THD) 추가 주입
"""

import os
import sys

BASE_DIR = r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\전기분야"

ADDITIONAL_SIMULATORS = {
    24: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 트램 주행속도별 팬터그래프 가선 압상량 계산기 -->
        <div class="bg-gradient-to-br from-amber-50 to-emerald-50 border-2 border-emerald-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-emerald-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-emerald-600 text-white text-xs font-bold px-2.5 py-1 rounded">시운전 집전 판정기</span>
                    <h3 class="font-bold text-base text-slate-900">🚋 트램 주행속도별 팬터그래프 가선 압상량 & 아크율 계산기</h3>
                </div>
                <span id="sim24_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">트램 주행 속도 (V, km/h)</label>
                    <input type="number" id="sim24_speed" value="45" step="5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSim24()">
                </div>
                <div>
                    <label class="block mb-1">팬터그래프 정적 접촉력 (F, N)</label>
                    <input type="number" id="sim24_force" value="70" step="5" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-emerald-900" oninput="calcSim24()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-emerald-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">동적 가선 압상량:</span>
                    <span id="sim24_uplift" class="font-black text-sm text-emerald-600 ml-1">28.5 mm</span>
                    <span class="text-slate-400 ml-1">(허용치: ≤ 50.0 mm)</span>
                </div>
                <div>
                    <span class="text-slate-500">예측 이선(Arc) 발생률:</span>
                    <span id="sim24_arc" class="font-black text-sm text-teal-600 ml-1">0.02 % (양호)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim24() {
            const v = parseFloat(document.getElementById('sim24_speed').value) || 0;
            const f = parseFloat(document.getElementById('sim24_force').value) || 0;
            const uplift = 15 + (v * 0.25) + (f * 0.05);
            const arc = Math.max(0.01, (v / 60) * 0.05 * (80 / Math.max(f, 10)));
            document.getElementById('sim24_uplift').innerText = uplift.toFixed(1) + " mm";
            document.getElementById('sim24_arc').innerText = arc.toFixed(3) + " % (" + (arc <= 0.1 ? "양호" : "주의") + ")";
            const isPass = uplift <= 50.0 && arc <= 0.1;
            const badge = document.getElementById('sim24_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "압상/아크 초과 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    ''',

    27: '''
        <!-- 💡 [인터랙티브 시뮬레이터] 다중 열차 최대 부하시 종합고조파 왜곡률 THD 계산기 -->
        <div class="bg-gradient-to-br from-indigo-50 to-blue-50 border-2 border-indigo-300 p-6 rounded-2xl shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-indigo-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="bg-indigo-600 text-white text-xs font-bold px-2.5 py-1 rounded">전력품질 분석기</span>
                    <h3 class="font-bold text-base text-slate-900">🌊 다중 열차 최대 부하시 종합고조파 왜곡률(THD) 계산기</h3>
                </div>
                <span id="sim27_badge" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full">적합 (PASS)</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs font-semibold text-slate-700">
                <div>
                    <label class="block mb-1">기본파 전압 (V1, V)</label>
                    <input type="number" id="sim27_v1" value="22900" step="100" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-indigo-900" oninput="calcSim27()">
                </div>
                <div>
                    <label class="block mb-1">5차 고조파 (V5, V)</label>
                    <input type="number" id="sim27_v5" value="380" step="10" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-indigo-900" oninput="calcSim27()">
                </div>
                <div>
                    <label class="block mb-1">7차 고조파 (V7, V)</label>
                    <input type="number" id="sim27_v7" value="240" step="10" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-indigo-900" oninput="calcSim27()">
                </div>
                <div>
                    <label class="block mb-1">11차 고조파 (V11, V)</label>
                    <input type="number" id="sim27_v11" value="120" step="10" class="w-full bg-white border border-slate-300 rounded-lg p-2 font-bold text-indigo-900" oninput="calcSim27()">
                </div>
            </div>
            <div class="bg-white p-4 rounded-xl border border-indigo-200 flex flex-wrap justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500">종합 고조파 왜곡률 (THD):</span>
                    <span id="sim27_thd" class="font-black text-sm text-indigo-600 ml-1">2.04 %</span>
                    <span class="text-slate-400 ml-1">(법정 기준치: ≤ 5.0%)</span>
                </div>
                <div>
                    <span class="text-slate-500">전력품질 상태:</span>
                    <span id="sim27_stat" class="font-bold text-emerald-600 ml-1">우수 (IEEE 519 기준 만족)</span>
                </div>
            </div>
        </div>
        <script>
        function calcSim27() {
            const v1 = parseFloat(document.getElementById('sim27_v1').value) || 1;
            const v5 = parseFloat(document.getElementById('sim27_v5').value) || 0;
            const v7 = parseFloat(document.getElementById('sim27_v7').value) || 0;
            const v11 = parseFloat(document.getElementById('sim27_v11').value) || 0;
            const thd = (Math.sqrt(v5*v5 + v7*v7 + v11*v11) / v1) * 100;
            document.getElementById('sim27_thd').innerText = thd.toFixed(2) + " %";
            const isPass = thd <= 5.0;
            document.getElementById('sim27_stat').innerText = isPass ? "우수 (IEEE 519 기준 만족)" : "고조파 필터 보완 필요";
            document.getElementById('sim27_stat').className = isPass ? "font-bold text-emerald-600 ml-1" : "font-bold text-rose-600 ml-1";
            const badge = document.getElementById('sim27_badge');
            badge.innerText = isPass ? "적합 (PASS)" : "고조파 초과 (FAIL)";
            badge.className = isPass ? "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full" : "bg-rose-600 text-white text-xs font-bold px-3 py-1 rounded-full";
        }
        </script>
    '''
}

for num, sim_code in ADDITIONAL_SIMULATORS.items():
    for fld in os.listdir(BASE_DIR):
        if fld.startswith(f"{num}_"):
            gd_dir = os.path.join(BASE_DIR, fld, '수행지침')
            for fn in os.listdir(gd_dir):
                if fn.endswith('.html'):
                    fp = os.path.join(gd_dir, fn)
                    with open(fp, 'r', encoding='utf-8') as f:
                        content = f.read()
                    target_str = '<div class="space-y-6">'
                    if target_str in content and 'sim' + str(num) not in content:
                        idx = content.find(target_str)
                        new_content = content[:idx] + sim_code + "\n\n        " + content[idx:]
                        with open(fp, 'w', encoding='utf-8') as f_out:
                            f_out.write(new_content)
                        print(f"Injected simulator into {fld}/{fn}")
