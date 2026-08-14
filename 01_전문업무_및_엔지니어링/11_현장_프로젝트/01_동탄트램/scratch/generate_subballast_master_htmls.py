# -*- coding: utf-8 -*-
"""
상부강화노반 36개 액티비티 총 108개 파일 전수 생성 스크립트
(기존 폴더 완전 초기화 후 정규 108개 파일 단일 생성 보장)
"""

import os
import sys
import shutil

sys.path.append(os.path.abspath("scratch"))
from subballast_part1 import ALL_TASKS as PART1_TASKS
from subballast_part2 import PART2_TASKS

TOTAL_TASKS = PART1_TASKS + PART2_TASKS
print(f"총 {len(TOTAL_TASKS)}개 상부강화노반 태스크 로드 완료!")

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\4.상부강화노반")

def sanitize_filename(name):
    for ch in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        name = name.replace(ch, '_')
    return name

def generate_svg_diagram(task_num, title, wbs_code):
    """라이트 테마 전용 고해상도 2D 기술 다이어그램 SVG 생성"""
    return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad_sub_{task_num}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="grad_bar_{task_num}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <pattern id="hatch_{task_num}" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#cbd5e1" stroke-width="1.5" />
    </pattern>
  </defs>

  <!-- 배경 그리드 & 베이스 -->
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>

  <!-- 헤더 바 -->
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <circle cx="45" cy="43" r="6" fill="#10b981"/>
  <circle cx="65" cy="43" r="6" fill="#38bdf8"/>
  <circle cx="85" cy="43" r="6" fill="#f59e0b"/>
  <text x="110" y="48" fill="#ffffff" font-size="14" font-weight="bold">동탄도시철도 상부강화노반 엔지니어링 표준 단면도 - WBS {wbs_code}</text>
  <rect x="660" y="30" width="105" height="26" rx="6" fill="#047857"/>
  <text x="672" y="47" fill="#ffffff" font-size="11" font-weight="bold">KCS 47 10 25</text>

  <!-- 2D 구조 단면 렌더링 -->
  <!-- 1. 원지반층 (G.L) -->
  <rect x="60" y="310" width="680" height="65" fill="url(#hatch_{task_num})" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="75" y="348" fill="#475569" font-size="13" font-weight="bold">원지반 (Natural Ground) [ N ≥ 15, K30 ≥ 110 MN/m³ ]</text>
  <line x1="60" y1="310" x2="740" y2="310" stroke="#475569" stroke-width="2" stroke-dasharray="6,3"/>

  <!-- 2. 하부노반 (Subgrade Lower, 60cm) -->
  <rect x="60" y="235" width="680" height="75" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="75" y="278" fill="#334155" font-size="13" font-weight="bold">하부노반층 (Lower Subgrade) [ D_max ≤ 150mm, 다짐도 ≥ 90% ]</text>
  <rect x="580" y="250" width="140" height="45" rx="6" fill="#e2e8f0" stroke="#94a3b8"/>
  <text x="592" y="277" fill="#1e293b" font-size="12" font-weight="bold">K30 ≥ 110 MN/m³</text>

  <!-- 3. 상부노반 (Subgrade Upper, 60cm) -->
  <rect x="60" y="160" width="680" height="75" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
  <text x="75" y="203" fill="#0369a1" font-size="13" font-weight="bold">상부노반층 (Upper Subgrade) [ CBR ≥ 10%, 다짐도 ≥ 95%, Evd ≥ 45 MPa ]</text>
  <rect x="580" y="175" width="140" height="45" rx="6" fill="#bae6fd" stroke="#0284c7"/>
  <text x="592" y="202" fill="#0369a1" font-size="12" font-weight="bold">K30 ≥ 150 MN/m³</text>

  <!-- 4. 상부강화노반층 (Subballast, 30cm) -->
  <rect x="60" y="90" width="680" height="70" fill="url(#grad_sub_{task_num})" stroke="#059669" stroke-width="2.5"/>
  <text x="75" y="132" fill="#065f46" font-size="14" font-weight="900">★ 상부강화노반 (Subballast SB-1, 0~30mm) [ 두께 30cm, K30 ≥ 190 MN/m³, Evd ≥ 65 MPa ]</text>
  <rect x="580" y="102" width="140" height="46" rx="6" fill="url(#grad_bar_{task_num})"/>
  <text x="592" y="130" fill="#ffffff" font-size="12" font-weight="bold">K30 ≥ 190 MN/m³</text>

  <!-- 좌측 치수선 (두께 표시) -->
  <line x1="45" y1="90" x2="45" y2="160" stroke="#059669" stroke-width="2"/>
  <path d="M45,90 L42,98 L48,98 Z M45,160 L42,152 L48,152 Z" fill="#059669"/>
  <text x="25" y="130" fill="#065f46" font-size="12" font-weight="bold" transform="rotate(-90 25 130)">30cm</text>

  <!-- 우측 횡단 배수구배 2% 표시 -->
  <path d="M480,95 L560,99 L480,99 Z" fill="#047857" opacity="0.3"/>
  <text x="495" y="92" fill="#065f46" font-size="11" font-weight="bold">횡단구배 i=2.0% ➔</text>
</svg>'''

def build_standard_html(task_tuple):
    num, folder_name, wbs_code, act_name, quote, summary, kpis, specs, steps, diag_title, terms = task_tuple
    
    kpi_cards = "".join([f'''
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">
            <span class="text-xs font-bold text-slate-500 block mb-1">{k}</span>
            <span class="text-base sm:text-lg font-black text-emerald-700">{v}</span>
        </div>''' for k, v in kpis])

    spec_rows = "".join([f'''
        <tr class="border-b border-slate-100 hover:bg-slate-50/80 transition-colors">
            <td class="p-3.5 font-bold text-slate-900">{cat}</td>
            <td class="p-3.5 text-slate-700">{req}</td>
            <td class="p-3.5 text-center text-slate-600 text-sm">{freq}</td>
            <td class="p-3.5 text-center font-bold text-emerald-700">{crit}</td>
        </tr>''' for cat, req, freq, crit in specs])

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상부강화노반 - {act_name} 마스터 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 via-slate-900 to-teal-950 opacity-90"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS {wbs_code} Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">상부강화노반 엔지니어링 표준서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{act_name} 마스터 표준서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"{quote}"</p>
        </div>
    </div>

    <div class="p-8 space-y-10">
        <!-- 1. 표준 개요 및 적용 범위 -->
        <section>
            <div class="flex items-center gap-2 pb-3 mb-4 border-b-2 border-emerald-600">
                <div class="w-2.5 h-6 bg-emerald-600 rounded"></div>
                <h2 class="text-xl font-bold text-slate-900">1. 표준 목적 및 적용 범위 (Scope & Objectives)</h2>
            </div>
            <p class="text-slate-700 leading-relaxed text-base bg-emerald-50/50 p-5 rounded-xl border border-emerald-100">
                {summary}
            </p>
        </section>

        <!-- 2. 핵심 품질 및 관리 지표 (KPIs) -->
        <section>
            <div class="flex items-center gap-2 pb-3 mb-4 border-b-2 border-emerald-600">
                <div class="w-2.5 h-6 bg-emerald-600 rounded"></div>
                <h2 class="text-xl font-bold text-slate-900">2. 핵심 품질 및 관리 지표 (Quality KPIs)</h2>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {kpi_cards}
            </div>
        </section>

        <!-- 3. 엔지니어링 기술 기준 및 검측 규격 -->
        <section>
            <div class="flex items-center gap-2 pb-3 mb-4 border-b-2 border-emerald-600">
                <div class="w-2.5 h-6 bg-emerald-600 rounded"></div>
                <h2 class="text-xl font-bold text-slate-900">3. 기술 기준 및 검측 규격 (Engineering Specifications)</h2>
            </div>
            <div class="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
                <table class="w-full text-left text-sm">
                    <thead class="bg-slate-900 text-white font-bold">
                        <tr>
                            <th class="p-3.5 w-1/4">검사항목 / 규격</th>
                            <th class="p-3.5 w-2/5">기술 시방 기준 (KCS 47 10 25)</th>
                            <th class="p-3.5 text-center w-1/6">검사 빈도</th>
                            <th class="p-3.5 text-center w-1/6">합격 판정 기준</th>
                        </tr>
                    </thead>
                    <tbody>
                        {spec_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- 4. 안전·환경 및 인터페이스 관리 수칙 -->
        <section class="bg-slate-900 text-white p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-emerald-400 mb-3 flex items-center gap-2">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                현장 안전 및 품질 보증 준수 헌장
            </h3>
            <ul class="space-y-2 text-slate-300 text-sm list-disc list-inside">
                <li>노반 다짐 시 최적함수비(OMC ±2%)를 철저히 유지하여 과다짐으로 인한 골재 파쇄를 방지합니다.</li>
                <li>도로 중앙분리대 구간 중장비 선회 시 인접 차선 침범을 방지하고 신호수 2인 1조를 상시 배치합니다.</li>
                <li>강화노반 완성 후 후속 궤도(콘크리트도상) 공종 착수 전까지 중차량 통행을 엄격히 제한합니다.</li>
            </ul>
        </section>
    </div>

    <!-- Footer -->
    <div class="bg-slate-100 border-t border-slate-200 p-4 text-center text-xs text-slate-500 font-medium">
        동탄도시철도(트램) 건설공사 현장감리단 | 상부강화노반 기술표준 WBS {wbs_code}
    </div>
</div>
</body>
</html>'''

def build_guideline_html(task_tuple):
    num, folder_name, wbs_code, act_name, quote, summary, kpis, specs, steps, diag_title, terms = task_tuple
    svg_diag = generate_svg_diagram(num, act_name, wbs_code)

    step_cards = ""
    for s_idx, (s_title, s_head, s_items) in enumerate(steps, 1):
        items_html = "".join([f'''<li class="flex items-start gap-2"><span class="text-emerald-600 font-black mt-0.5">•</span><span class="text-slate-700 leading-relaxed text-sm sm:text-base">{item}</span></li>''' for item in s_items])
        step_cards += f'''
        <div class="bg-white border-2 border-slate-200 hover:border-emerald-500 rounded-2xl p-6 sm:p-8 shadow-sm transition-all duration-200">
            <div class="flex items-center gap-3 mb-4">
                <span class="bg-emerald-600 text-white text-xs font-black px-3.5 py-1.5 rounded-full uppercase tracking-wider">STEP {s_idx}</span>
                <h3 class="text-lg sm:text-xl font-black text-slate-900">{s_head}</h3>
            </div>
            <ul class="space-y-3 bg-slate-50 p-5 rounded-xl border border-slate-100">
                {items_html}
            </ul>
        </div>'''

    term_items = "".join([f'''
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 hover:border-emerald-400 transition-colors">
            <h4 class="font-bold text-slate-900 text-sm mb-1">{k}</h4>
            <p class="text-xs text-slate-600 leading-relaxed">{v}</p>
        </div>''' for k, v in terms])

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{act_name} 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        .term-highlight {{
            color: #059669 !important;
            font-weight: 700 !important;
            border-bottom: 2px dashed #059669 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            padding: 0 2px !important;
        }}
        .term-highlight:hover {{
            background: #ecfdf5 !important;
            color: #047857 !important;
            border-radius: 4px !important;
        }}
        .clickable-diagram {{
            cursor: zoom-in;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .clickable-diagram:hover {{
            transform: scale(1.005);
            box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.15);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto space-y-8">

    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 rounded-2xl shadow-xl relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-950 via-slate-900 to-teal-950 opacity-90"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">WBS {wbs_code} Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">현장 시공 기술지침</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{act_name} 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"{quote}"</p>
        </div>
    </div>

    <!-- 1:1 필수 2D 기술 도식 (Light Theme Zoomable) -->
    <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div class="flex justify-between items-center mb-4">
            <div class="flex items-center gap-2">
                <span class="w-2.5 h-6 bg-emerald-600 rounded"></span>
                <h2 class="text-lg font-bold text-slate-900">상부강화노반 표준 횡단 기술도식 ({diag_title})</h2>
            </div>
            <span class="text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full font-bold">🔍 클릭하여 고해상도 확대</span>
        </div>
        <div class="clickable-diagram" onclick="openDiagramZoom()">
            {svg_diag}
        </div>
    </div>

    <!-- 단계별 수행 절차 (Step Cards) -->
    <div class="space-y-6">
        <div class="flex items-center gap-2">
            <span class="w-2.5 h-6 bg-emerald-600 rounded"></span>
            <h2 class="text-xl font-black text-slate-900">단계별 정밀 시공 절차 (Step-by-Step Instructions)</h2>
        </div>
        {step_cards}
    </div>

    <!-- 인터랙티브 현장 엔지니어링 계산기 (다짐도 & 지지력 판정 시뮬레이터) -->
    <div class="bg-slate-900 text-white p-6 sm:p-8 rounded-2xl shadow-xl">
        <div class="flex items-center gap-3 mb-6">
            <div class="p-2.5 bg-emerald-600 rounded-xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            </div>
            <div>
                <h3 class="text-xl font-black text-white">현장 다짐도 & 지지력(K30/Evd) 적합성 시뮬레이터</h3>
                <p class="text-xs text-slate-400">현장 실측 건조밀도 및 평판재하 계수를 입력하여 시방 규격 적합 여부를 실시간 판정합니다.</p>
            </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <div>
                <label class="block text-xs font-bold text-slate-300 mb-1.5">현장 건조밀도 (t/m³)</label>
                <input type="number" id="calc_rhod" value="2.05" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-base font-bold focus:border-emerald-500 focus:outline-none" oninput="runSim()">
            </div>
            <div>
                <label class="block text-xs font-bold text-slate-300 mb-1.5">실내 최대건조밀도 (t/m³)</label>
                <input type="number" id="calc_rhomax" value="2.12" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-base font-bold focus:border-emerald-500 focus:outline-none" oninput="runSim()">
            </div>
            <div>
                <label class="block text-xs font-bold text-slate-300 mb-1.5">실측 K30 (MN/m³)</label>
                <input type="number" id="calc_k30" value="195" step="1" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white text-base font-bold focus:border-emerald-500 focus:outline-none" oninput="runSim()">
            </div>
        </div>

        <div class="mt-6 bg-slate-800/80 border border-slate-700 rounded-xl p-5 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
                <span class="text-xs text-slate-400 block font-medium">산출 다짐도(%) & 지지력 판정 결과:</span>
                <span id="sim_res_text" class="text-2xl font-black text-emerald-400">다짐도: 96.7% | K30: 195 MN/m³</span>
            </div>
            <span id="sim_badge" class="bg-emerald-500 text-slate-950 font-black text-sm px-4 py-2 rounded-xl">✓ 시방 합격 (PASS)</span>
        </div>
    </div>

    <!-- 기술 용어 사전 (Glossary) -->
    <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div class="flex items-center gap-2 mb-4">
            <span class="w-2.5 h-6 bg-emerald-600 rounded"></span>
            <h2 class="text-lg font-bold text-slate-900">핵심 엔지니어링 용어 해설 (Technical Glossary)</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {term_items}
        </div>
    </div>
</div>

<!-- 라이트박스 줌 모달 -->
<div id="zoomModal" class="fixed inset-0 bg-black/80 z-50 hidden items-center justify-center p-4" onclick="closeDiagramZoom()">
    <div class="bg-white rounded-2xl max-w-5xl w-full p-6 relative overflow-hidden shadow-2xl" onclick="event.stopPropagation()">
        <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold text-slate-900 text-lg">상부강화노반 고해상도 기술도식</h3>
            <button onclick="closeDiagramZoom()" class="p-2 hover:bg-slate-100 rounded-full font-bold text-slate-700">✕ 닫기</button>
        </div>
        <div class="max-h-[80vh] overflow-auto">
            {svg_diag}
        </div>
    </div>
</div>

<script>
function openDiagramZoom() {{
    document.getElementById('zoomModal').classList.remove('hidden');
    document.getElementById('zoomModal').classList.add('flex');
}}
function closeDiagramZoom() {{
    document.getElementById('zoomModal').classList.add('hidden');
    document.getElementById('zoomModal').classList.remove('flex');
}}
function runSim() {{
    const rhod = parseFloat(document.getElementById('calc_rhod').value) || 0;
    const rhomax = parseFloat(document.getElementById('calc_rhomax').value) || 1;
    const k30 = parseFloat(document.getElementById('calc_k30').value) || 0;
    
    const comp = ((rhod / rhomax) * 100).toFixed(1);
    const pass = (comp >= 95.0 && k30 >= 190);
    
    document.getElementById('sim_res_text').innerText = '다짐도: ' + comp + '% | K30: ' + k30 + ' MN/m³';
    const badge = document.getElementById('sim_badge');
    if (pass) {{
        badge.className = 'bg-emerald-500 text-slate-950 font-black text-sm px-4 py-2 rounded-xl';
        badge.innerText = '✓ 시방 합격 (PASS)';
    }} else {{
        badge.className = 'bg-rose-500 text-white font-black text-sm px-4 py-2 rounded-xl';
        badge.innerText = '✕ 시방 불합격 (재다짐 필요)';
    }}
}}
</script>
</body>
</html>'''

def build_checklist_html(task_tuple):
    num, folder_name, wbs_code, act_name, quote, summary, kpis, specs, steps, diag_title, terms = task_tuple

    check_items = [
        ("착수 전 사전점검", [
            ("설계도서 및 지반조사 주상도 대조 확인", "시추 N치 및 암반선 심도 일치 여부", "도면/성적서 검토"),
            ("토공량 및 운반 동선 검토", "사토장/토취장 인허가 및 운반거리 적정성", "현장 확인"),
            ("3D GPR 지하지장물 탐사 및 줄파기", "한전/통신/가스관로 이격거리 확보", "합동 입회")
        ]),
        ("시공 중 공정점검", [
            ("층별 포설 두께(30cm 이하) 준수", "규준틀 눈금 대조 및 그레이더 평탄성", "레벨 측량"),
            ("최적함수비(OMC ±2%) 관리", "살수차 가동 및 현장 함수비 측정", "Speedy Tester"),
            ("12ton 진동롤러 규정 횟수 다짐", "진동 4회 + 무진동 2회 전압 패턴", "롤러 주행 기록")
        ]),
        ("품질시험 및 검측", [
            ("들밀도시험(KS F 2311) 다짐도 검측", "다짐도 ≥ 95% (강화노반 98%) 만족", "1,000m²당 1회"),
            ("평판재하시험(K30) 지반지지력", "강화노반 K30 ≥ 190 MN/m³ 만족", "500m²당 1회"),
            ("동적변형계수(Evd) LFWD 시험", "강화노반 Evd ≥ 65 MPa 만족", "10m 간격 연속")
        ]),
        ("안전 및 환경관리", [
            ("중앙분리대 신호수 2인 1조 배치", "작업구간 PE드럼 및 LED 경광등", "상시 점검"),
            ("출차 덤프트럭 세륜 100% 이행", "자동세륜기 및 적재함 덮개 밀폐", "게이트 입회"),
            ("임시 배수로 및 3단 침사지 상태", "강우 시 토사 유출 차단 상태", "일일 점검")
        ])
    ]

    table_rows = ""
    item_count = 0
    for phase_name, sub_items in check_items:
        for idx, (iname, icrit, imeth) in enumerate(sub_items):
            item_count += 1
            phase_cell = f'<td rowspan="{len(sub_items)}" class="p-3.5 font-bold text-slate-900 bg-slate-50 border-r border-slate-200 text-center align-middle">{phase_name}</td>' if idx == 0 else ''
            table_rows += f'''
            <tr class="border-b border-slate-100 hover:bg-slate-50/80 transition-colors">
                {phase_cell}
                <td class="p-3.5 font-semibold text-slate-800">{iname}</td>
                <td class="p-3.5 text-slate-600 text-sm">{icrit}</td>
                <td class="p-3.5 text-center text-slate-500 text-sm">{imeth}</td>
                <td class="p-3.5 text-center">
                    <input type="checkbox" id="chk_{item_count}" class="w-5 h-5 accent-emerald-600 rounded cursor-pointer" onchange="calcScore()">
                </td>
            </tr>'''

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{act_name} 마스터 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto space-y-6">

    <!-- Header -->
    <div class="flex justify-between items-end border-b-2 border-slate-900 pb-4">
        <div>
            <div class="flex items-center gap-2 mb-1">
                <span class="bg-emerald-600 text-white text-xs font-black px-2.5 py-0.5 rounded">WBS {wbs_code}</span>
                <span class="text-xs font-bold text-slate-500">상부강화노반 검측대장</span>
            </div>
            <h1 class="text-3xl font-black text-slate-900 tracking-tight">{act_name} 마스터 체크리스트</h1>
        </div>
        <div class="text-right">
            <div id="score_box" class="text-2xl font-black text-emerald-600">0 / {item_count} 합격 (0%)</div>
            <span class="text-xs text-slate-500">KCS 47 10 25 기준 감리 검측</span>
        </div>
    </div>

    <!-- 검측 테이블 -->
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <table class="w-full text-left text-sm">
            <thead class="bg-slate-900 text-white font-bold">
                <tr>
                    <th class="p-3.5 w-1/5 text-center">검측 구분</th>
                    <th class="p-3.5 w-2/5">점검 항목</th>
                    <th class="p-3.5 w-1/4">판정 기준 (시방서 기준)</th>
                    <th class="p-3.5 text-center w-1/6">검사 방법</th>
                    <th class="p-3.5 text-center w-16">적합</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>

    <!-- 서명란 -->
    <div class="grid grid-cols-2 gap-4 bg-white p-5 rounded-2xl border border-slate-200">
        <div class="p-4 bg-slate-50 rounded-xl border border-slate-100 text-center">
            <span class="text-xs text-slate-500 block mb-2 font-bold">시공사 현장책임자</span>
            <div class="h-10 flex items-center justify-center font-bold text-slate-700">서명: __________________ (인)</div>
        </div>
        <div class="p-4 bg-slate-50 rounded-xl border border-slate-100 text-center">
            <span class="text-xs text-slate-500 block mb-2 font-bold">책임감리원 (검측확인)</span>
            <div class="h-10 flex items-center justify-center font-bold text-emerald-700">서명: __________________ (인)</div>
        </div>
    </div>
</div>

<script>
const TOTAL_ITEMS = {item_count};
function calcScore() {{
    let checked = 0;
    for (let i = 1; i <= TOTAL_ITEMS; i++) {{
        const el = document.getElementById('chk_' + i);
        if (el && el.checked) checked++;
    }}
    const pct = Math.round((checked / TOTAL_ITEMS) * 100);
    const box = document.getElementById('score_box');
    box.innerText = checked + ' / ' + TOTAL_ITEMS + ' 합격 (' + pct + '%)';
    if (pct === 100) {{
        box.className = 'text-2xl font-black text-emerald-600';
    }} else {{
        box.className = 'text-2xl font-black text-amber-600';
    }}
}}
</script>
</body>
</html>'''

# 기존 디렉토리 전면 정비 후 108개 파일 생성
success_count = 0

for t in TOTAL_TASKS:
    num, folder_name, wbs_code, act_name, quote, summary, kpis, specs, steps, diag_title, terms = t
    
    safe_folder = sanitize_filename(folder_name)
    safe_act = sanitize_filename(act_name)

    task_dir = os.path.join(BASE_DIR, safe_folder)
    
    # 태스크 디렉토리 초기화
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)

    std_dir = os.path.join(task_dir, "표준서")
    guide_dir = os.path.join(task_dir, "수행지침")
    chk_dir = os.path.join(task_dir, "체크리스트")

    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(guide_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)

    # 1. 표준서 파일
    std_path = os.path.join(std_dir, f"{safe_act}_표준서.html")
    with open(std_path, "w", encoding="utf-8") as f:
        f.write(build_standard_html(t))
    success_count += 1

    # 2. 수행지침 파일
    guide_path = os.path.join(guide_dir, f"{safe_act}_수행지침.html")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(build_guideline_html(t))
    success_count += 1

    # 3. 체크리스트 파일
    chk_path = os.path.join(chk_dir, f"{safe_act}_체크리스트.html")
    with open(chk_path, "w", encoding="utf-8") as f:
        f.write(build_checklist_html(t))
    success_count += 1

    print(f"[{num:02d}/36] {safe_act} -> 3종 HTML 깔끔 생성 완료!")

print(f"\n=======================================================")
print(f"상부강화노반 총 {success_count}개 고품질 HTML 파일 완벽 생성 완료!")
print(f"=======================================================")
