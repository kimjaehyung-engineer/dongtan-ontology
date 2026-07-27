import os
import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v4.xlsx"
backup_excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v4_updated.xlsx"
chk_file_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\1_설계적정성 검토\체크리스트\1_설계적정성 검토_체크리스트.html"

# 1. Update HTML file
new_chk_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - 설계적정성 검토 리스크 체크리스트</title>
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
            font-family: 'Pretendard', sans-serif;
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
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">설계적정성 검토 내부 리스크 체크리스트</h1>
        <span class="meta">WBS Code 9000-6-1 | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">궤도 중심 선형 좌표 대조, 3D BIM 지하 매설 지장물 간섭 체크, 최대 구배/최소 곡선 반경 한계치 및 누설 전류 방지 대책 검속</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 47 10 25 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[기하선형 정합성]</strong> 궤도 중심선 좌표(GRS80)와 선행 토목/노반 완성면 계획고(표고) 간 일치 오차(±0mm)를 설계 대조했는가?</div>
                    <div style="margin-bottom: 8px;">• <strong>[지하지장물 간섭]</strong> 공동구, 하수관로, 한전/통신 맨홀 등 매설 지장물과 도상 콘크리트 기초 타설 영역 간의 3D BIM 간섭 검속을 실시했는가?</div>
                    <div style="margin-bottom: 8px;">• <strong>[구배 구조 한계]</strong> 차량 주행 종단 한계인 최대 구배 60‰ 이하 및 정거장 내 수평 유지 조건 만족 여부를 도면상 검증했는가?</div>
                    <div style="margin-bottom: 8px;">• <strong>[레일 야적지 확보]</strong> 25m 정척레일을 200m 이상 장대레일로 가설 용접하기 위한 평탄 용접 작업대 및 예비 야적 용지가 사전에 설계 반영되었는가?</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[신호센서 전자기 간섭]</strong> 신호 루프 센서(Loop Detector) 매설 배관과 도상 보강 철근 간격(최소 150mm 이상 이격)에 따른 전기적 간섭 대책을 설계 검토했는가?</div>
                    <div style="margin-bottom: 8px;">• <strong>[도상 재료 강도]</strong> 도상 콘크리트(TCL) 28일 압축강도 fck ≥ 35 MPa 및 무수축 모르타르 그라우트 fck ≥ 30 MPa 강성 확보 조건 배합 설계가 규격화되었는가?</div>
                    <div style="margin-bottom: 8px;">• <strong>[누설전류 전식 방지]</strong> 주행 레일 누설 전류(Stray Current)에 의한 지하 상수관 전식 부식 방지용 다이오드 접지선 매설 설계의 적정성을 확인했는가?</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[도서 승인 누락]</strong> 설계 오류 및 간섭 확인 결과에 대해 궤도 기술 전문인의 교차 검증 서명 및 발주처 설계 변경 승인 필증이 완비되었는가?</div>
                    <div style="margin-bottom: 8px;">• <strong>[인계 한계 편차]</strong> 후행 전기/신호 분야 인계를 위해 궤도 기하구조 5대 공차(궤간, 캔트, 수평, 고저, 방향) 설계 허용 기준(±1.5mm) 확약 문서가 수립되었는가?</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | 콘크리트도상
    </div>
</div>
</body>
</html>"""

with open(chk_file_path, 'w', encoding='utf-8') as f:
    f.write(new_chk_html)
print(f"🎉 Regenerated '1_설계적정성 검토_체크리스트.html' with 9 detailed engineering items.")

# 2. Update Excel v4 file
wb = openpyxl.load_workbook(excel_path)
sheet = wb['콘크리트도상']

# Row 2 in 콘크리트도상 (WBS 9000-6-1)
# Column 15 (Col O) is Checklist Summary (체크리스트 요약)
new_chk_sum = "궤도 중심 선형 좌표 대조, 3D BIM 지하 매설 지장물 간섭 체크, 최대 구배/최소 곡선 반경 한계치 및 누설 전류 방지 대책 검속"
sheet.cell(row=2, column=15).value = new_chk_sum

try:
    wb.save(excel_path)
    print(f"🎉 Saved to Original Excel '{excel_path}' successfully.")
except PermissionError:
    wb.save(backup_excel_path)
    print(f"⚠️ Original Excel is locked. Saved to Backup: '{backup_excel_path}'")
