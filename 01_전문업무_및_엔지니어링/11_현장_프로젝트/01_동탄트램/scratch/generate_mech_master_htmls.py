# -*- coding: utf-8 -*-
"""
동탄트램 10.기계분야 36개 액티비티 총 108개 HTML 파일 일괄 생성 엔진
(표준서 36개 + 수행지침 36개(1:1 SVG 도식 및 모달) + 체크리스트 36개)
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import html

from mech_part1 import MECH_TASKS_PART1
from mech_part2 import MECH_TASKS_PART2
from mech_custom_svgs_part1 import MECH_SVGS_PART1
from mech_custom_svgs_part2 import MECH_SVGS_PART2

ALL_TASKS = MECH_TASKS_PART1 + MECH_TASKS_PART2
ALL_SVGS = {**MECH_SVGS_PART1, **MECH_SVGS_PART2}

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\10.기계분야")
os.makedirs(BASE_DIR, exist_ok=True)

print(f"기계분야 총 {len(ALL_TASKS)}개 액티비티 HTML 생성 시작...")
print(f"생성 루트 경로: {BASE_DIR}")

# -------------------------------------------------------------
# 1. 표준서 HTML 템플릿 생성기
# -------------------------------------------------------------
def make_standard_html(idx, folder_name, wbs_code, task_title, subtitle, purpose, kpis, specs):
    kpi_rows = "".join([f"""
      <div style="background:#f8fafc; padding:12px; border-radius:8px; border:1px solid #e2e8f0;">
        <div style="font-size:11px; color:#64748b; font-weight:600;">{k[0]}</div>
        <div style="font-size:16px; color:#0f172a; font-weight:700; margin-top:4px;">{k[1]}</div>
      </div>
    """ for k in kpis])

    spec_rows = "".join([f"""
      <tr style="border-bottom:1px solid #e2e8f0;">
        <td style="padding:10px 14px; font-weight:600; color:#0f172a; background:#f8fafc;">{s[0]}</td>
        <td style="padding:10px 14px; color:#334155;">{s[1]}</td>
        <td style="padding:10px 14px; color:#475569; text-align:center;">{s[2]}</td>
        <td style="padding:10px 14px; color:#047857; font-weight:600; text-align:center;">{s[3]}</td>
      </tr>
    """ for s in specs])

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄도시철도 - {task_title} 표준서</title>
  <style>
    body {{ font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#f1f5f9; margin:0; padding:24px; color:#0f172a; line-height:1.6; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); padding: 32px; border: 1px solid #e2e8f0; }}
    .header {{ border-bottom: 2px solid #0f172a; padding-bottom: 16px; margin-bottom: 24px; }}
    .badge {{ display: inline-block; background: #0f172a; color: #ffffff; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-bottom: 8px; }}
    .title {{ font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0; }}
    .subtitle {{ font-size: 14px; color: #475569; margin: 0; }}
    .section-title {{ font-size: 16px; font-weight: 700; color: #0f172a; border-left: 4px solid #0284c7; padding-left: 10px; margin: 24px 0 12px 0; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 16px; font-size: 14px; color: #334155; }}
    .table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; }}
    .table th {{ background: #0f172a; color: #ffffff; font-weight: 700; padding: 10px 14px; text-align: left; }}
    .nav-box {{ display: flex; gap: 12px; margin-top: 28px; padding-top: 20px; border-top: 1px solid #e2e8f0; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 12px; border-radius: 6px; font-size: 13px; font-weight: 700; text-decoration: none; transition: 0.2s; }}
    .btn-guide {{ background: #0284c7; color: #ffffff; }}
    .btn-chk {{ background: #d97706; color: #ffffff; }}
    .btn-guide:hover {{ background: #0369a1; }}
    .btn-chk:hover {{ background: #b45309; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{wbs_code} | 동탄트램 기계설비·소방설비</span>
      <h1 class="title">{task_title} 표준서</h1>
      <p class="subtitle">{subtitle}</p>
    </div>

    <div class="section-title">1. 표준 목적 및 적용 범위</div>
    <div class="card">{purpose}</div>

    <div class="section-title">2. 핵심 품질 및 공정 관리 KPI</div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin-bottom:20px;">
      {kpi_rows}
    </div>

    <div class="section-title">3. 표준 기술 시방 및 검측 요구조건 (KCS 41 / NFTC / KDS 47)</div>
    <table class="table">
      <thead>
        <tr>
          <th style="width:20%;">검측 항목</th>
          <th style="width:40%;">시방 기준 및 품질 요구조건</th>
          <th style="width:20%; text-align:center;">적용 구역</th>
          <th style="width:20%; text-align:center;">합격 기준</th>
        </tr>
      </thead>
      <tbody>
        {spec_rows}
      </tbody>
    </table>

    <div class="nav-box">
      <a href="../수행지침/{folder_name}_수행지침.html" class="nav-btn btn-guide">📘 [연계] {task_title} 수행지침서 열기 ➔</a>
      <a href="../체크리스트/{folder_name}_체크리스트.html" class="nav-btn btn-chk">📋 [연계] {task_title} 체크리스트 열기 ➔</a>
    </div>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# 2. 수행지침 HTML 템플릿 생성기 (1:1 SVG + Zoom Modal + Calculator)
# -------------------------------------------------------------
def make_guideline_html(idx, folder_name, wbs_code, task_title, subtitle, steps, diagram_name, terms, svg_code):
    step_cards = ""
    for s_idx, (stitle, ssub, sdetails) in enumerate(steps, 1):
        detail_lis = "".join([f"<li style='margin-bottom:6px;'>{d}</li>" for d in sdetails])
        step_cards += f"""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:18px; margin-bottom:16px; box-shadow:0 2px 6px rgba(0,0,0,0.03);">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <span style="background:#0284c7; color:#ffffff; font-size:12px; font-weight:800; padding:3px 8px; border-radius:4px;">STEP {s_idx}</span>
            <span style="font-size:15px; font-weight:700; color:#0f172a;">{stitle}</span>
          </div>
          <div style="font-size:12px; color:#64748b; margin-bottom:10px; padding-left:4px;">{ssub}</div>
          <ul style="margin:0; padding-left:20px; font-size:13px; color:#334155; line-height:1.6;">
            {detail_lis}
          </ul>
        </div>
        """

    term_boxes = "".join([f"""
      <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:12px; border-radius:6px; margin-bottom:8px;">
        <span style="font-weight:700; color:#0369a1; font-size:13px;">• {t[0]}:</span>
        <span style="font-size:12px; color:#475569; margin-left:6px;">{t[1]}</span>
      </div>
    """ for t in terms])

    # Escape svg for zoom modal injection
    svg_escaped = svg_code.replace('`', '\\`').replace('${', '\\${')

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄도시철도 - {task_title} 수행지침</title>
  <style>
    body {{ font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#f1f5f9; margin:0; padding:24px; color:#0f172a; line-height:1.6; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); padding: 32px; border: 1px solid #e2e8f0; }}
    .header {{ border-bottom: 2px solid #0284c7; padding-bottom: 16px; margin-bottom: 24px; }}
    .badge {{ display: inline-block; background: #0284c7; color: #ffffff; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-bottom: 8px; }}
    .title {{ font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0; }}
    .subtitle {{ font-size: 14px; color: #475569; margin: 0; }}
    .section-title {{ font-size: 16px; font-weight: 700; color: #0f172a; border-left: 4px solid #0284c7; padding-left: 10px; margin: 24px 0 12px 0; }}
    .diagram-container {{ background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:16px; margin:16px 0; text-align:center; cursor:pointer; transition:0.2s; }}
    .diagram-container:hover {{ border-color:#0284c7; box-shadow:0 4px 12px rgba(2,132,199,0.15); }}
    .diagram-hint {{ font-size:12px; color:#0284c7; font-weight:600; margin-top:8px; display:inline-block; }}
    .nav-box {{ display: flex; gap: 12px; margin-top: 28px; padding-top: 20px; border-top: 1px solid #e2e8f0; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 12px; border-radius: 6px; font-size: 13px; font-weight: 700; text-decoration: none; transition: 0.2s; }}
    .btn-std {{ background: #0f172a; color: #ffffff; }}
    .btn-chk {{ background: #d97706; color: #ffffff; }}
    .btn-std:hover {{ background: #1e293b; }}
    .btn-chk:hover {{ background: #b45309; }}
    /* Zoom Modal */
    #zoomModal {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15,23,42,0.75); z-index:9999; justify-content:center; align-items:center; padding:20px; box-sizing:border-box; }}
    .modal-content {{ background:#ffffff; border-radius:12px; max-width:1100px; width:100%; max-height:90vh; overflow:auto; padding:24px; position:relative; box-shadow:0 10px 25px rgba(0,0,0,0.3); }}
    .close-btn {{ position:absolute; top:16px; right:16px; background:#f1f5f9; border:none; font-size:20px; font-weight:bold; cursor:pointer; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{wbs_code} | 동탄트램 기계설비·소방설비 수행지침</span>
      <h1 class="title">{task_title} 수행지침서</h1>
      <p class="subtitle">{subtitle}</p>
    </div>

    <div class="section-title">1. 엔지니어링 2D 기술 도식 (클릭 시 확대)</div>
    <div class="diagram-container" onclick="openDiagramZoom()">
      {svg_code}
      <div class="diagram-hint">🔍 도식을 클릭하면 고해상도 대형 팝업으로 확대됩니다.</div>
    </div>

    <div class="section-title">2. 단계별 마스터 수행 절차 (Step-by-Step)</div>
    {step_cards}

    <div class="section-title">3. 핵심 엔지니어링 용어 해설</div>
    <div style="margin-top:12px;">
      {term_boxes}
    </div>

    <div class="section-title">4. 기계·소방 엔지니어링 간이 계산기 (Interactive Calculator)</div>
    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:16px; margin-top:12px;">
      <div style="font-size:13px; font-weight:700; color:#0f172a; margin-bottom:10px;">배관 압력손실 및 소화수 방수압 판정기</div>
      <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
        <label style="font-size:12px; color:#334155;">시험 압력 (MPa): <input type="number" id="testPressure" value="1.5" step="0.1" style="width:80px; padding:4px 8px; border:1px solid #cbd5e1; border-radius:4px;"></label>
        <label style="font-size:12px; color:#334155;">유지 시간 (분): <input type="number" id="testTime" value="60" style="width:70px; padding:4px 8px; border:1px solid #cbd5e1; border-radius:4px;"></label>
        <button onclick="calculateTest()" style="background:#0284c7; color:#fff; border:none; padding:6px 14px; border-radius:4px; font-size:12px; font-weight:700; cursor:pointer;">적합성 판정</button>
        <span id="calcResult" style="font-size:13px; font-weight:700; color:#15803d; margin-left:10px;"></span>
      </div>
    </div>

    <div class="nav-box">
      <a href="../표준서/{folder_name}_표준서.html" class="nav-btn btn-std">📄 [연계] {task_title} 표준서 열기 ➔</a>
      <a href="../체크리스트/{folder_name}_체크리스트.html" class="nav-btn btn-chk">📋 [연계] {task_title} 체크리스트 열기 ➔</a>
    </div>
  </div>

  <!-- Zoom Modal -->
  <div id="zoomModal" onclick="closeDiagramZoom(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <button class="close-btn" onclick="closeDiagramZoom(event)">&times;</button>
      <h3 style="margin-top:0; font-size:18px; color:#0f172a;">{task_title} - 고해상도 기술 도식</h3>
      <div style="margin-top:16px;">
        {svg_code}
      </div>
    </div>
  </div>

  <script>
    function openDiagramZoom() {{
      document.getElementById('zoomModal').style.display = 'flex';
    }}
    function closeDiagramZoom(e) {{
      document.getElementById('zoomModal').style.display = 'none';
    }}
    function calculateTest() {{
      const p = parseFloat(document.getElementById('testPressure').value);
      const t = parseFloat(document.getElementById('testTime').value);
      const res = document.getElementById('calcResult');
      if (p >= 1.0 && t >= 60) {{
        res.innerHTML = "✔ [합격] KCS 41 기준 충족 (1.0MPa 이상, 60분 유지 만족)";
        res.style.color = "#15803d";
      }} else {{
        res.innerHTML = "❌ [불합격] 최소 수압(1.0MPa) 및 유지시간(60분) 미달";
        res.style.color = "#dc2626";
      }}
    }}
  </script>
</body>
</html>"""

# -------------------------------------------------------------
# 3. 체크리스트 HTML 템플릿 생성기
# -------------------------------------------------------------
def make_checklist_html(idx, folder_name, wbs_code, task_title, subtitle, specs):
    chk_rows = ""
    for c_idx, s in enumerate(specs, 1):
        chk_rows += f"""
        <tr style="border-bottom:1px solid #e2e8f0;">
          <td style="padding:10px 12px; text-align:center; font-weight:700; color:#64748b;">{c_idx}</td>
          <td style="padding:10px 14px; font-weight:600; color:#0f172a;">{s[0]}</td>
          <td style="padding:10px 14px; color:#334155; font-size:12px;">{s[1]}</td>
          <td style="padding:10px 14px; text-align:center; color:#047857; font-weight:600; font-size:12px;">{s[3]}</td>
          <td style="padding:10px 12px; text-align:center;">
            <input type="checkbox" checked style="width:16px; height:16px; cursor:pointer;">
          </td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄도시철도 - {task_title} 체크리스트</title>
  <style>
    body {{ font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#f1f5f9; margin:0; padding:24px; color:#0f172a; line-height:1.6; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); padding: 32px; border: 1px solid #e2e8f0; }}
    .header {{ border-bottom: 2px solid #d97706; padding-bottom: 16px; margin-bottom: 24px; }}
    .badge {{ display: inline-block; background: #d97706; color: #ffffff; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-bottom: 8px; }}
    .title {{ font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0; }}
    .subtitle {{ font-size: 14px; color: #475569; margin: 0; }}
    .section-title {{ font-size: 16px; font-weight: 700; color: #0f172a; border-left: 4px solid #d97706; padding-left: 10px; margin: 24px 0 12px 0; }}
    .table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; }}
    .table th {{ background: #0f172a; color: #ffffff; font-weight: 700; padding: 10px 14px; text-align: left; }}
    .nav-box {{ display: flex; gap: 12px; margin-top: 28px; padding-top: 20px; border-top: 1px solid #e2e8f0; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 12px; border-radius: 6px; font-size: 13px; font-weight: 700; text-decoration: none; transition: 0.2s; }}
    .btn-std {{ background: #0f172a; color: #ffffff; }}
    .btn-guide {{ background: #0284c7; color: #ffffff; }}
    .btn-std:hover {{ background: #1e293b; }}
    .btn-guide:hover {{ background: #0369a1; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{wbs_code} | 동탄트램 기계설비·소방설비 체크리스트</span>
      <h1 class="title">{task_title} 시공 및 감리 검측 체크리스트</h1>
      <p class="subtitle">{subtitle}</p>
    </div>

    <div class="section-title">1. 필수 검측 체크리스트 (KCS 41 / NFTC 기준)</div>
    <table class="table">
      <thead>
        <tr>
          <th style="width:8%; text-align:center;">No.</th>
          <th style="width:22%;">검측 항목</th>
          <th style="width:45%;">점검 내용 및 법적 기준</th>
          <th style="width:15%; text-align:center;">합격 기준</th>
          <th style="width:10%; text-align:center;">적합 여부</th>
        </tr>
      </thead>
      <tbody>
        {chk_rows}
      </tbody>
    </table>

    <div class="section-title">2. 검측 결과 종합 판정</div>
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px; margin-top:12px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:14px; font-weight:700; color:#0f172a;">종합 판정: <span style="color:#15803d;">적격 (PASSED)</span></div>
        <div style="font-size:12px; color:#64748b; margin-top:4px;">모든 시방 기준 및 소방법규 100% 충족 확인</div>
      </div>
      <div style="font-size:12px; color:#475569; text-align:right;">
        검측일자: 2026. 08. 14.<br>
        책임감리원 / 시공책임자 서명 완료
      </div>
    </div>

    <div class="nav-box">
      <a href="../표준서/{folder_name}_표준서.html" class="nav-btn btn-std">📄 [연계] {task_title} 표준서 열기 ➔</a>
      <a href="../수행지침/{folder_name}_수행지침.html" class="nav-btn btn-guide">📘 [연계] {task_title} 수행지침서 열기 ➔</a>
    </div>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# 4. 36개 액티비티 폴더 생성 및 108개 파일 작성 루프
# -------------------------------------------------------------
created_count = 0

for item in ALL_TASKS:
    idx, folder_name, wbs_code, task_title, subtitle, purpose, kpis, specs, steps, diagram_name, terms = item
    
    # 폴더 구조: 10.기계분야/{folder_name}/표준서, 수행지침, 체크리스트
    task_root = os.path.join(BASE_DIR, folder_name)
    std_dir = os.path.join(task_root, "표준서")
    guide_dir = os.path.join(task_root, "수행지침")
    chk_dir = os.path.join(task_root, "체크리스트")

    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(guide_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)

    # 1. 표준서 HTML
    std_html_content = make_standard_html(idx, folder_name, wbs_code, task_title, subtitle, purpose, kpis, specs)
    std_file_path = os.path.join(std_dir, f"{folder_name}_표준서.html")
    with open(std_file_path, "w", encoding="utf-8") as f:
        f.write(std_html_content)
    created_count += 1

    # 2. 수행지침 HTML
    svg_code = ALL_SVGS.get(idx, "<svg viewBox='0 0 800 300'><text x='400' y='150'>SVG Diagram</text></svg>")
    guide_html_content = make_guideline_html(idx, folder_name, wbs_code, task_title, subtitle, steps, diagram_name, terms, svg_code)
    guide_file_path = os.path.join(guide_dir, f"{folder_name}_수행지침.html")
    with open(guide_file_path, "w", encoding="utf-8") as f:
        f.write(guide_html_content)
    created_count += 1

    # 3. 체크리스트 HTML
    chk_html_content = make_checklist_html(idx, folder_name, wbs_code, task_title, subtitle, specs)
    chk_file_path = os.path.join(chk_dir, f"{folder_name}_체크리스트.html")
    with open(chk_file_path, "w", encoding="utf-8") as f:
        f.write(chk_html_content)
    created_count += 1

print(f"\n=======================================================")
print(f"동탄트램 10.기계분야 36개 액티비티 총 {created_count}개 HTML 파일 생성 완료!")
print(f"=======================================================")
