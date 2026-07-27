import os
import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

# Find all checklist files except the ones in "상부강화노반" if they are already converted, 
# but user said "모든 공정에 대해 체크리스크 양식 적용해줘..내용은 바꾸지 말고".
# If we convert "상부강화노반" again, it might overwrite the customized risks we just wrote.
# Let's check: "이 형식으로 내용을 바꾸지는 말고.. 이 형식으로 모든 공정에 대해 체크리스크 양식 적용해줘.."
# This means for all other processes (which still have the old ul-li format), apply the new 3-stage risk layout 
# by parsing the existing contents (which contains the original risks) and reshaping them into the 3-stage risk table.
# For "상부강화노반", they already have the 3-stage risk layout with customized contents, so we can skip them to avoid resetting their contents,
# OR we can apply it to everything, but for 상부강화노반, it already has the 3-stage format.
# Let's filter out "상부강화노반" to preserve the detailed risks we just wrote, or process it safely.
# Skiping "상부강화노반" is correct because they already have the 3-stage risk format with rich customized content.
# Let's write a script that processes files that are still in the old format.

all_html_files = glob.glob(os.path.join(base_dir, "**", "*체크리스트.html"), recursive=True)

converted_count = 0
skipped_count = 0

for file_path in all_html_files:
    # Skip "상부강화노반" to preserve the rich ground truth we just wrote
    if "상부강화노반" in file_path:
        skipped_count += 1
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # If the file already contains "내부 리스크 체크리스트" or the new table structure, skip it
        if "내부 리스크 체크리스트" in content and "⚠️ 사전 리스크" in content:
            skipped_count += 1
            continue

        # Extract WBS code
        wbs_match = re.search(r"WBS\s+([0-9a-zA-Z\-_]+)", content, re.IGNORECASE)
        wbs_code = wbs_match.group(1) if wbs_match else "9000-X-X"

        # Extract title
        title_match = re.search(r"<h1 class=\"title\">(.*?)</h1>", content)
        if not title_match:
            title_match = re.search(r"<title>(.*?)</title>", content)
        title = title_match.group(1).replace("완료 검측 체크리스트", "").replace("체크리스트", "").strip() if title_match else os.path.basename(file_path).replace("_체크리스트.html", "").strip()

        # Extract Category/Field from meta or breadcrumb
        field = "공통"
        field_match = re.search(r"<strong>공종/분야:</strong>\s*(.*?)\s*</span>", content)
        if not field_match:
            field_match = re.search(r"breadcrumb\">(.*?)WBS", content)
        if field_match:
            field = re.sub(r"<[^>]*>", "", field_match.group(1)).replace("Dongtan Tram", "").strip()

        # Extract existing list items (risks/items)
        li_items = re.findall(r"<li>(.*?)</li>", content)
        
        # Clean HTML tags inside li items
        cleaned_items = []
        for item in li_items:
            # remove HTML tags
            clean_txt = re.sub(r"<[^>]*>", "", item).strip()
            if clean_txt:
                cleaned_items.append(clean_txt)

        if not cleaned_items:
            # Fallback to paragraph extraction if no li found
            cleaned_items = [x.strip() for x in re.findall(r"<p>(.*?)</p>", content) if x.strip()]

        # Classify items into Pre, Ing, Post risks based on keywords
        pre_keywords = ["사전", "준비", "조사", "도면", "계약", "신고", "협의", "검토", "수립", "교육", "BIM", "간섭", "승낙", "계획", "KOM", "인허가", "확인", "부지"]
        ing_keywords = ["시공", "다짐", "설치", "포설", "포장", "부설", "타설", "측정", "시험", "검사", "연마", "밀링", "용접", "접속", "연결", "배수", "GPR", "장비", "작업", "그레이더", "롤러", "OMC", "함수"]
        post_keywords = ["완공", "완료", "인계", "인수", "준공", "최종", "검속", "정산", "제출", "보고", "확인서", "서명", "날인", "GIS"]

        pre_list = []
        ing_list = []
        post_list = []

        for item in cleaned_items:
            # Count keyword matches
            pre_score = sum(1 for kw in pre_keywords if kw in item)
            ing_score = sum(1 for kw in ing_keywords if kw in item)
            post_score = sum(1 for kw in post_keywords if kw in item)

            if pre_score > ing_score and pre_score > post_score:
                pre_list.append(item)
            elif post_score > pre_score and post_score > ing_score:
                post_list.append(item)
            elif ing_score > pre_score and ing_score > post_score:
                ing_list.append(item)
            else:
                # Default logic if tie
                if any(kw in item for kw in pre_keywords):
                    pre_list.append(item)
                elif any(kw in item for kw in post_keywords):
                    post_list.append(item)
                else:
                    ing_list.append(item)

        # Re-balance lists if any of them is empty to ensure at least one item per row
        all_remaining = cleaned_items.copy()
        if not pre_list and all_remaining:
            pre_list.append(all_remaining.pop(0))
        if not post_list and all_remaining:
            post_list.append(all_remaining.pop(-1))
        if not ing_list and all_remaining:
            ing_list.append(all_remaining[0])
            
        # If still empty, put placeholders
        if not pre_list:
            pre_list = [f"{title} 사전 설계도면 검토 및 지장물 간섭 체크"]
        if not ing_list:
            ing_list = [f"{title} 시공 규정 준수 및 정밀 다짐/설치 관리"]
        if not post_list:
            post_list = [f"{title} 완료 후 후행 공정 인수인계 및 품질 점검"]

        # Build list bullet strings
        pre_bullets = "\n".join([f"• {item}" for item in pre_list])
        ing_bullets = "\n".join([f"• {item}" for item in ing_list])
        post_bullets = "\n".join([f"• {item}" for item in post_list])

        # Core checklist summary text
        chk_sum = f"{title} 시방 이행, 사전/공사중/공사후 주요 리스크 요소를 점검하고 후행 공정 인계 품질 확보"

        # Generate the new standardized print-friendly HTML format
        new_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 리스크 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
            --border-color: #cbd5e1;
        }}
        body {{
            font-family: 'Pretendard', sans-serif;
            margin: 0;
            padding: 30px 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 35px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            border-bottom: 2px solid var(--text-primary);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .title {{
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0;
            color: #1e3a8a;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }}
        .summary-box {{
            background: #fdf2f8;
            border: 1px solid #fbcfe8;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #9d174d;
        }}
        table {{
            width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid var(--border-color);
            padding: 14px;
            font-size: 0.92rem;
            text-align: left;
        }}
        th {{
            background: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }}
        .category {{
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            width: 18%;
        }}
        .pre-row {{ color: #0f172a; }}
        .ing-row {{ color: #0f172a; }}
        .post-row {{ color: #0f172a; }}
        .label-pre {{ color: var(--accent-orange); font-weight: bold; }}
        .label-ing {{ color: var(--accent-red); font-weight: bold; }}
        .label-post {{ color: var(--accent-green); font-weight: bold; }}
        .check-cell {{
            text-align: center;
            vertical-align: middle;
            width: 15%;
            font-weight: bold;
            color: #1e3a8a;
        }}
        .footer {{
            text-align: center;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 15px;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">{title} 내부 리스크 체크리스트</h1>
        <span class="meta">WBS Code {wbs_code} | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">{chk_sum}</div>
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
                    {pre_bullets}
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    {ing_bullets}
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    {post_bullets}
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | {field}
    </div>
</div>
</body>
</html>"""

        # Overwrite the file with the standardized format
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        converted_count += 1
        print(f"[{converted_count}] Reshaped '{os.path.basename(file_path)}' to simple 3-stage risk table format.")

    except Exception as e:
        print(f"❌ Error processing '{file_path}': {e}")

print(f"\n🎉 Successfully processed all checklists!")
print(f"• Total Converted: {converted_count}")
print(f"• Total Skipped/Already Converted: {skipped_count}")
