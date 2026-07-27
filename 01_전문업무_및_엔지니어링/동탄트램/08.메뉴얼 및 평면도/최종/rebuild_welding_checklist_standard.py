import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

from patch_welding_surgical import minimal_glossary_style
from implement_welding_glossary_interactive import common_modal_html

# Build the standardized Checklist HTML content matching the master layout perfectly
checklist_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 레일 용접장 선정 리스크 체크리스트</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
            --border-color: #cbd5e1;
        }
        body {
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            padding: 30px 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 35px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .header {
            border-bottom: 2px solid var(--text-primary);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .title {
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0;
            color: #1e3a8a;
        }
        .meta {
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }
        .summary-box {
            background: #fdf2f8;
            border: 1px solid #fbcfe8;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #9d174d;
        }
        table {
            width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid var(--border-color);
            padding: 14px;
            font-size: 0.92rem;
            text-align: left;
        }
        th {
            background: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }
        .category {
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            width: 18%;
        }
        .pre-row { color: #0f172a; }
        .ing-row { color: #0f172a; }
        .post-row { color: #0f172a; }
        .label-pre { color: var(--accent-orange); font-weight: bold; }
        .label-ing { color: var(--accent-red); font-weight: bold; }
        .label-post { color: var(--accent-green); font-weight: bold; }
        .check-cell {
            text-align: center;
            vertical-align: middle;
            width: 15%;
            font-weight: bold;
            color: #1e3a8a;
        }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 15px;
        }
    </style>
    {minimal_style}
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">레일 용접장 선정 리스크 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-3 | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">용접장 평탄성 오차 ±1mm 이내, 전력 공급 및 방풍 시설 완비, NDT(비파괴) 대기 공간 확보</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 47 30 00 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[설계/용접대 침하]</strong> 용접대 기초 수평 오차 초과로 인한 <span class="term-highlight" onclick="openGlossary('cwr')">장대레일</span> 제작 시 종단 영구 절곡 결함 발생 리스크 <span class="scene-link" onclick="openScene('yard')">📸 롤러 가이드 베드 보기</span></div>
                    <div style="margin-bottom: 8px;">• <strong>[인프라/전원 확보]</strong> <span class="term-highlight" onclick="openGlossary('gas_pressure')">가스압접</span> 및 <span class="term-highlight" onclick="openGlossary('flash_butt')">플래시버트 용접</span> 대용량 전력 공급 설비 부하 용량 검증 및 비상 전원 설비 확보 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[시공/환경 관리]</strong> 야외 용접 시 강풍/우천 방풍 시설 미비로 용접부 급랭 및 수소 균열 결함 발생 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[NDT 안전거리]</strong> 감마선/초음파 등 <span class="term-highlight" onclick="openGlossary('ndt')">비파괴 시험(NDT)</span> 구역 이격에 따른 작업원 방사선 노출 방지 대책 수립 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[품질 보증 누락]</strong> 용접 성적서 및 <span class="term-highlight" onclick="openGlossary('ndt')">NDT 용접부</span> 검사 기록 누락에 의한 장대레일 영구 매립 리스크</div>
                    <div style="margin-bottom: 8px;">• <strong>[용접부 추적]</strong> 용접년도 및 용접공 고유번호 레일 측면 타각 표식 기록 및 기하학 선형 공차(±0.2mm/1m) 만족 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | 콘크리트도상
    </div>
</div>

{modal_html}

</body>
</html>
"""

checklist_content_final = checklist_content.replace("{minimal_style}", minimal_glossary_style).replace("{modal_html}", common_modal_html)

# Write to Checklist HTML files cleanly
chk_fn1 = os.path.join(target_base, "체크리스트", "레일 용접장 선정_체크리스트.html")
chk_fn2 = os.path.join(target_base, "체크리스트", "3_레일 용접장 선정_체크리스트.html")

with open(chk_fn1, 'w', encoding='utf-8') as f:
    f.write(checklist_content_final)
with open(chk_fn2, 'w', encoding='utf-8') as f:
    f.write(checklist_content_final)

print("🎉 Successfully reformatted welding checklist files to the master table format!")
