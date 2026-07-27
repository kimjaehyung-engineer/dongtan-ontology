import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Find 10 Target Activity Folders (including twin folders)
target_folders = {}
for f in os.listdir(base_dir):
    f_path = os.path.join(base_dir, f)
    if os.path.isdir(f_path):
        if "기존관로 철거" in f or "17_기존관로" in f or "24_기존관로" in f:
            target_folders.setdefault("removal", []).append(f_path)
        elif "광역상수관" in f or "18_광역상수관" in f or "25_광역상수관" in f:
            target_folders.setdefault("kwater", []).append(f_path)
        elif "상수도 관로" in f or "19_상수도" in f or "26_상수도 관로" in f:
            target_folders.setdefault("water", []).append(f_path)
        elif "하수도 관로" in f or "20_하수도" in f or "27_하수도 관로" in f:
            target_folders.setdefault("sewer", []).append(f_path)
        elif "도시가스관" in f or "21_도시가스관" in f or "28_도시가스관" in f:
            target_folders.setdefault("gas", []).append(f_path)
        elif "지역난방관" in f or "22_지역난방관" in f or "29_지역난방관" in f:
            target_folders.setdefault("heating", []).append(f_path)
        elif "통신관로" in f or "23_통신관로" in f or "30_통신관로" in f:
            target_folders.setdefault("telecom", []).append(f_path)
        elif "특고압 전력" in f or "24_특고압" in f or "31_특고압" in f:
            target_folders.setdefault("power", []).append(f_path)
        elif "송유관" in f or "25_송유관" in f or "32_송유관" in f:
            target_folders.setdefault("oil", []).append(f_path)
        elif "상하수도 이설 시공 최종 점검" in f or "26_상하수도" in f or "33_상하수도" in f:
            target_folders.setdefault("final_check", []).append(f_path)

print(f"Target Folders Found ({len(target_folders)} types): {list(target_folders.keys())}")

def get_std_template(wbs_code, title_name, dept_name, badge_name, purpose_text, method_text, deliverables, act_table_rows, svg_title, box1, box2, box3, box4, alert_msg, exp_text, summary_text):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - {title_name} 기술 표준서</title>
    <style>
        :root {{ --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }}
        body {{ font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }}
        .header {{ border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }}
        .breadcrumb {{ font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }}
        .title {{ font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }}
        .meta-info {{ display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }}
        .badge {{ background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }}
        h2 {{ font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }}
        table {{ width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }}
        th, td {{ border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }}
        th {{ background: #f1f5f9; color: #1e293b; font-weight: 700; }}
        .svg-container {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
        .diagram-explanation {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }}
        .key-takeaway {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }}
        .footer-note {{ margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS {wbs_code} Standard</div>
        <h1 class="title">{title_name} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 ({badge_name})</span>
            <span>|</span>
            <span><strong>주관부서:</strong> {dept_name}</span>
            <span>|</span>
            <span><span class="badge">{badge_name} 기술 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>{purpose_text}</td></tr>
            <tr><th>수행 방법</th><td>{method_text}</td></tr>
            <tr><th>주요 산출물</th><td>{deliverables}</td></tr>
            <tr><th>관련 법령/기준</th><td>관련 기술 시방서, 5대 위탁기관 표준 규정 및 동탄트램 궤도 시방서</td></tr>
        </tbody>
    </table>

    <h2>2. {title_name} 정량 공학/시방 기술 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">⚙️ {title_name} 핵심 정량 검속 시방 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">검속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">적용 기관 및 기준</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 수칙 및 안전 기준</th>
                </tr>
            </thead>
            <tbody>
                {act_table_rows}
            </tbody>
        </table>
    </div>

    <h2>3. {title_name} 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">{svg_title}</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① {box1[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box1[1]}</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② {box2[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box2[1]}</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ {box3[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box3[1]}</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ {box4[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box4[1]}</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 {alert_msg}</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 {title_name} 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">{exp_text}</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> {summary_text}
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS {wbs_code} | 지장물이설
    </div>
</div>
</body>
</html>"""

# Define specs for 10 target activities
activity_specs = {
    "removal": {
        "wbs": "2000-1-17", "title": "기존관로 철거 및 원상복구", "dept": "현장 공사팀 / 감리단", "badge": "폐관 철거 복구",
        "purpose": "구 관로 내 잔류 유체를 완전 드레인 및 퍼지 후 안전 철거하고, 되메우기 층다짐 95% 및 도로 복구를 이행",
        "method": "기존 관 잔류물 퍼지, 폐관 철거 및 폐기물 처리, KCS 11 20 00 되메우기 층다짐 95% 및 도로 아스콘 원상복구",
        "deliverables": "폐관 철거 사진대지, 폐기물 처리 증빙서, 도로 복구 다짐 성과표",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">잔류유체 완전 퍼지</td><td style="text-align:center;">환경법 / 안전 수칙</td><td>• 가스/기름/수돗물 잔류 유체 N₂ 퍼지 및 드레인 100% 이행<br>• 잔류 가스 0% 검증 후 인력 절단 철거 시행</td></tr>
<tr><td style="font-weight:bold;text-align:center;">폐관 철거 폐기물</td><td style="text-align:center;">폐기물관리법</td><td>• 철거 기존관 지정 폐기물/건설 폐기물 적법 이관 처리<br>• 노면 방치 금지 및 철거 당일 현장 즉시 적재 수송</td></tr>
<tr><td style="font-weight:bold;text-align:center;">되메우기 층다짐 95%</td><td style="text-align:center;">KCS 11 20 00 토공</td><td>• 되메우기 30cm 층다짐 밀도 <strong>95% 이상</strong> 확보<br>• 도로 기층 및 아스콘 원상복구 후 도로과 준공 확인</td></tr>""",
        "svg_title": "기존관로 안전 철거 및 도로 원상복구 절차",
        "box1": ("유체 N₂ 퍼지", "잔류가스/기름 100% 드레인"),
        "box2": ("기존관 절단 철거", "폐기물 적법 수송 처리"),
        "box3": ("되메우기 층다짐", "밀도 95% 이상 다짐"),
        "box4": ("도로 복구 GIS", "아스콘 복구 & 폐관 GIS"),
        "alert": "폐관 철거 미흡 시 잔류 유체 폭발 및 도로 침하 위험 전면 차단",
        "exp": "본 과업은 기존 관로 잔류 유체 퍼지 후 폐관을 철거하고 되메우기 층다짐(95% 이상)으로 도로를 복구하는 절차입니다.",
        "summary": "잔류 유체 퍼지, 폐관 적법 철거 및 층다짐 95% 준수로 도로 복구를 완료하는 단계입니다!"
    },
    "kwater": {
        "wbs": "2000-1-18", "title": "광역상수관 이설 공사", "dept": "현장 배관팀 / K-water", "badge": "광역상수관 이설",
        "purpose": "한국수자원공사 관리 D800mm 이상 광역상수관을 무단수 Tapping 분기 및 수압 15kg/cm² 조인트로 이설 완료",
        "method": "K-water 무단수 천공, 이탈방지 압륜 체결, 24시간 잔류염소 소독 및 궤도 이격 H ≥ 1.5m 준수",
        "deliverables": "광역상수관 이설 성과표, 수압시험(15kg) 성적서, K-water 통수 승인 공문",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">D800mm+ 무단수 탭</td><td style="text-align:center;">K-water 광역 시방</td><td>• 광역 대형 수관 D800mm 이상 무단수 천공 100% 이행<br>• 수압 15kg/cm² 이탈방지 압륜 조인트 체결</td></tr>
<tr><td style="font-weight:bold;text-align:center;">수압 15kg 시험</td><td style="text-align:center;">수도법 / K-water</td><td>• 시험 수압 <strong>15kg/cm² 1시간 유지 Zero 누수</strong> 확인<br>• 24시간 잔류염소 소독 및 수질 검증 필증 획득</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 H≥1.5m</td><td style="text-align:center;">동탄트램 궤도 시방</td><td>• 트램 궤도 구조물과 <strong>최소 이격거리 H ≥ 1.5m</strong> 준수<br>• 이설관 보호 콘크리트 패드(Saddle) 시공</td></tr>""",
        "svg_title": "광역상수도관(D800mm+) 정밀 이설 및 통수 절차",
        "box1": ("무단수 Tapping", "D800mm+ 무단수 천공"),
        "box2": ("광역관 부설", "이탈방지 압륜 체결"),
        "box3": ("수압 15kg 검속", "1시간 Zero 누수 확인"),
        "box4": ("소독 통수 승인", "K-water 잔류염소 승인"),
        "alert": "광역상수관 이설 누수 발생 시 수도권 대규모 단수 재난 전면 차단",
        "exp": "본 과업은 K-water D800mm 이상 광역수관을 무단수 천공 후 수압 15kg/cm² 시험 및 잔류염소 소독을 거쳐 이설하는 절차입니다.",
        "summary": "K-water 무단수 탭, 수압 15kg/cm² Zero 누수 및 궤도 이격 1.5m 준수로 광역관 이설을 완료하는 단계입니다!"
    },
    "water": {
        "wbs": "2000-1-19", "title": "상수도 관로 이설 공사", "dept": "현장 배관팀 / 맑은물사업소", "badge": "상수도 이설",
        "purpose": "화성시 맑은물사업소 D300~D600mm 상수도관을 Sand Bedding 150mm 및 수압 10kg/cm² 시방으로 이설 완료",
        "method": "Sand Bedding 150mm 부설, 덕타일 주철관(DCI) 체결, 수압 10kg 1시간 유지 및 궤도 이격 H ≥ 1.5m 준수",
        "deliverables": "상수도 이설 성과표, 수압시험(10kg) 성적서, 맑은물사업소 통수 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">Sand Bedding 150mm</td><td style="text-align:center;">KCS 47 10 00 배관</td><td>• 관 기초 모래 쿠션재(Sand Bedding) 두께 <strong>150mm 이상</strong> 부설<br>• 관 측면 다짐 95% 확보 및 부등 침하 방지</td></tr>
<tr><td style="font-weight:bold;text-align:center;">수압 10kg 시험</td><td style="text-align:center;">화성시 맑은물 시방</td><td>• 상수도 시험 수압 <strong>10kg/cm² 1시간 유지 Zero 누수</strong><br>• 잔류염소 소독 및 맑은물사업소 감독관 결재</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 H≥1.5m</td><td style="text-align:center;">동탄트램 궤도 시방</td><td>• 트램 궤도와 <strong>최소 이격거리 H ≥ 1.5m 이상</strong> 확보<br>• 관로 상단 매설 경고 테이프 2줄 부설</td></tr>""",
        "svg_title": "상수도관(DCI) 정밀 이설 및 수압 검속 절차",
        "box1": ("Sand Bedding", "모래 기초 두께 150mm"),
        "box2": ("DCI 관 부설", "이탈방지 조인트 체결"),
        "box3": ("수압 10kg 검속", "1시간 Zero 누수 확인"),
        "box4": ("맑은물 통수", "잔류염소 소독 통수"),
        "alert": "상수도관 누수 발생 시 도로 지하 토사 침식 및 궤도 침하 전면 차단",
        "exp": "본 과업은 Sand Bedding 150mm 기초 위에 DCI 상수관을 부설하고 수압 10kg/cm² 1시간 Zero 누수를 검증하는 절차입니다.",
        "summary": "Sand Bedding 150mm, 수압 10kg/cm² 통과 및 궤도 이격 1.5m 준수로 상수도 이설을 완료하는 단계입니다!"
    },
    "sewer": {
        "wbs": "2000-1-20", "title": "하수도 관로 이설 공사", "dept": "현장 토공팀 / 맑은물사업소", "badge": "하수도 이설",
        "purpose": "화성시 하수도관을 자연유하 구배 ≥1.0% 및 CCTV 내시경 100% 검사 시방으로 정밀 이설 완료",
        "method": "콘크리트 기초 부설, 유선형 인버트 시공, 자연유하 구배 ≥1.0% 측정 및 CCTV 내시경 100% 촬영",
        "deliverables": "하수도 이설 성과표, CCTV 내시경 100% 촬영 DVD/사진대지, 맑은물 준공 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">자연유하 구배 ≥1.0%</td><td style="text-align:center;">하수도법 시방서</td><td>• 오/하수관 <strong>자연유하 구배 ≥ 1.0% 이상</strong> 정밀 부설<br>• 관 역구배 및 관 처짐 Zero 검증 측량</td></tr>
<tr><td style="font-weight:bold;text-align:center;">CCTV 내시경 100%</td><td style="text-align:center;">화성시 맑은물 시방</td><td>• 신설 하수관전 구간 <strong>CCTV 내시경 100% 촬영</strong> 제출<br>• 접합부 이격, 관 균열 및 토사 유입 여부 전수 검속</td></tr>
<tr><td style="font-weight:bold;text-align:center;">유선형 인버트 시공</td><td style="text-align:center;">KCS 하수도 시방</td><td>• 맨홀 하부 유선형 콘크리트 인버트(Invert) 몰탈 시공<br>• 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 준수 시공</td></tr>""",
        "svg_title": "하수도관 정밀 이설 및 CCTV 100% 검속 절차",
        "box1": ("콘크리트 기초", "하수관 기초 부설"),
        "box2": ("구배 ≥1.0% 부설", "자연유하 구배 정밀 측정"),
        "box3": ("CCTV 100% 촬영", "관 처짐/이격 전수 검사"),
        "box4": ("맑은물 준공 승인", "하수관 이설 완료 통보"),
        "alert": "하수관 역구배 발생 시 오수 역류 및 악취 집단 민원 전면 차단",
        "exp": "본 과업은 하수관을 자연유하 구배(≥1.0%)로 부설하고 CCTV 내시경 100% 촬영으로 관 처짐 및 누수를 검증하는 절차입니다.",
        "summary": "자연유하 구배 1.0%, CCTV 100% 촬영 통과 및 궤도 이격 1.5m 준수로 하수도 이설을 완료하는 단계입니다!"
    },
    "gas": {
        "wbs": "2000-1-21", "title": "도시가스관 이설 공사", "dept": "현장 배관팀 / ㈜삼천리", "badge": "도시가스 이설",
        "purpose": "㈜삼천리 관리 도시가스관을 용접부 RT 100% 1급 및 N₂ 질소 퍼지 시방으로 안전하게 이설 완료 (62일)",
        "method": "PE피복 강관(SPPS) 부설, 용접부 RT 100% 1급 판정, N₂ 질소 퍼지(산소 ≤1.0%) 및 궤도 이격 H ≥ 1.5m",
        "deliverables": "도시가스관 이설 성과표, RT 비파괴 필름/성적서, 삼천리 가스 공급 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">RT 비파괴 100% 1급</td><td style="text-align:center;">도시가스사업법 / 삼천리</td><td>• 강관 배관 용접부 <strong>RT(방사선) 100% 전수 1급 판정</strong><br>• CP 피복 테이핑 및 절연 저항 시험 통과</td></tr>
<tr><td style="font-weight:bold;text-align:center;">N₂ 질소 퍼지 1.0%</td><td style="text-align:center;">가스 안전 시방</td><td>• 관내 residual oxygen <strong>N₂ 퍼지 산소 농도 ≤ 1.0%</strong><br>• 가스 수압/기밀시험 1.5배 정격 압력 통과</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 & 소요공기</td><td style="text-align:center;">동탄트램 / 삼천리</td><td>• 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 및 표준 공기 <strong>62일</strong> 준수<br>• 가스 밸브 박스 및 가스 탐지 센서 설치</td></tr>""",
        "svg_title": "도시가스관 정밀 이설 및 RT 100% 검속 절차",
        "box1": ("SPPS 강관 부설", "도시가스관 정밀 배관"),
        "box2": ("용접 RT 100%", "방사선 비파괴 1급 판정"),
        "box3": ("N₂ 질소 퍼지", "잔류산소 ≤ 1.0% 세팅"),
        "box4": ("삼천리 가스 승인", "가스 공급 개시 승인"),
        "alert": "도시가스 누출 시 대규모 가스 폭발 및 화재 사고 위험 전면 차단",
        "exp": "본 과업은 도시가스관 용접부 RT 100% 1급 검사 및 N₂ 질소 퍼지(산소 ≤1.0%)를 수행하여 가스관을 이설하는 절차입니다.",
        "summary": "용접 RT 100% 1급, N₂ 질소 퍼지 및 삼천리 승인(62일)으로 도시가스관 이설을 완료하는 단계입니다!"
    },
    "heating": {
        "wbs": "2000-1-22", "title": "지역난방관 이설 공사", "dept": "현장 배관팀 / 한국지역난방공사", "badge": "지역난방 이설",
        "purpose": "한국지역난방공사 관리 이중보온관을 NDT 100% 및 16bar 수압시험 시방으로 안전 이설 완료 (80일)",
        "method": "이중보온관 부설, 용접 NDT 100% 검사, 110℃ / 16bar 수압시험, 누수 감지선 도통 ≥ 100MΩ 및 궤도 이격 H ≥ 1.5m",
        "deliverables": "지역난방관 이설 성과표, NDT 검사 성적서, 난방공사 온수 공급 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">이중보온관 NDT 100%</td><td style="text-align:center;">한국지역난방공사</td><td>• 직매립 이중보온관 용접부 <strong>NDT 100% 비파괴 통과</strong><br>• 외관 외피관 시동 조인트(Pur기밀) 수밀 시공</td></tr>
<tr><td style="font-weight:bold;text-align:center;">16bar 수압시험</td><td style="text-align:center;">난방공사 시방</td><td>• <strong>110℃ / 16bar 시험 수압 1시간 유지 Zero 누수</strong><br>• 누수 감지선 도통 및 절연저항 <strong>≥ 100MΩ</strong> 측정</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 & 소요공기</td><td style="text-align:center;">동탄트램 / 난방공사</td><td>• 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 및 표준 공기 <strong>80일</strong> 준수<br>• 신음 신축 흡수관(Bellows) 부설</td></tr>""",
        "svg_title": "지역난방 이중보온관 이설 및 16bar 수압 절차",
        "box1": ("이중보온관 부설", "난방 배관 정밀 접합"),
        "box2": ("용접 NDT 100%", "비파괴검사 100% 통과"),
        "box3": ("16bar 수압 검속", "감지선 절연 ≥ 100MΩ"),
        "box4": ("난방공사 승인", "열수송관 온수 공급"),
        "alert": "고온 열수송관 누수 발생 시 도로 파손 및 고온 스팀 인명 사고 전면 차단",
        "exp": "본 과업은 이중보온관 용접 NDT 100% 및 16bar 수압시험을 통해 지역난방관을 안전하게 이설하는 절차입니다.",
        "summary": "NDT 100%, 16bar 수압 통과 및 난방공사 승인(80일)으로 지역난방관 이설을 완료하는 단계입니다!"
    },
    "telecom": {
        "wbs": "2000-1-23", "title": "통신관로 및 케이블 이설 공사", "dept": "현장 통신팀 / KT SKT LGU+", "badge": "통신관로 이설",
        "purpose": "KT/SKT/LGU+ 통신 관로 및 72-Core 광케이블을 OTDR ≤0.05dB 및 심야 Cut-over 시방으로 이설 완료 (150일)",
        "method": "72-Core 광케이블 핸드홀 부설, 광 접속 OTDR ≤ 0.05dB 이내, 심야 Cut-over(01~05시) 및 궤도 이격 H ≥ 1.5m",
        "deliverables": "통신관로 이설 성과표, OTDR 광 접속 시험성적서, 통신 3사 절체 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">OTDR ≤ 0.05dB</td><td style="text-align:center;">KT/SKT/LGU+ 시방</td><td>• 광케이블 접속 손실 <strong>OTDR ≤ 0.05dB 이내</strong> 100% 통과<br>• 72-Core 광케이블 방서/수밀 핸드홀 설치</td></tr>
<tr><td style="font-weight:bold;text-align:center;">심야 Cut-over 01~05시</td><td style="text-align:center;">정보통신공사업법</td><td>• 주민 통신 장애 방지를 위해 <strong>심야(01:00~05:00)</strong> Cut-over<br>• 사전 방송 통지 및 통신 절체 핫라인 가동</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 & 소요공기</td><td style="text-align:center;">동탄트램 / 통신 3사</td><td>• 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 및 표준 공기 <strong>150일</strong> 준수<br>• 케이블 보호 관로(CD관/유연관) 시공</td></tr>""",
        "svg_title": "통신관로 및 72-Core 광케이블 정밀 이설 절차",
        "box1": ("통신 관로 부설", "핸드홀 & CD관 시공"),
        "box2": ("광케이블 포설", "72-Core 광케이블 견인"),
        "box3": ("심야 OTDR 검속", "접속 손실 ≤ 0.05dB"),
        "box4": ("통신 3사 승인", "통신 망 절체 승인"),
        "alert": "광케이블 절단 발생 시 동탄 시내 통신 마비 및 국가 통신 재난 전면 차단",
        "exp": "본 과업은 72-Core 광케이블을 부설하고 OTDR(≤0.05dB) 시험 및 심야 Cut-over를 거쳐 통신망을 이설하는 절차입니다.",
        "summary": "OTDR ≤ 0.05dB, 심야 Cut-over 및 통신 3사 승인(150일)으로 통신관로 이설을 완료하는 단계입니다!"
    },
    "power": {
        "wbs": "2000-1-24", "title": "특고압 전력관로 이설 공사", "dept": "현장 전기팀 / 한전 경기본부", "badge": "전력관로 이설",
        "purpose": "한국전력공사 22.9kV 특고압 지중 전력관을 절연저항 ≥ 2000MΩ 및 내전압 60kV 시방으로 안전 이설 완료 (255일)",
        "method": "TR-CNCV 22.9kV 지중관 부설, 절연저항 ≥ 2000MΩ, 내전압 60kV 10분, 맨홀 접지저항 ≤ 10Ω 및 궤도 이격 H ≥ 1.5m",
        "deliverables": "특고압 전력관 이설 성과표, 한전 절연/내전압 시험성적서, 한전 송전 개시 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">절연저항 ≥ 2000MΩ</td><td style="text-align:center;">한전 경기본부 시방</td><td>• 22.9kV TR-CNCV 특고압 케이블 <strong>절연저항 ≥ 2,000MΩ</strong><br>• 상용주파 내전압 시험 <strong>60kV 10분간 견딤</strong> 통과</td></tr>
<tr><td style="font-weight:bold;text-align:center;">맨홀 접지저항 ≤ 10Ω</td><td style="text-align:center;">전기공사업법 / KEC</td><td>• 전력 맨홀 접지망 시공 <strong>접지저항 ≤ 10Ω 이하</strong><br>• 누설전류(Stray Current) 부식 방지 디오드 접지</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 & 소요공기</td><td style="text-align:center;">동탄트램 / 한전</td><td>• 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 및 표준 공기 <strong>255일</strong> 준수<br>• 한전 감독관 입회 정전 후 송전 개시</td></tr>""",
        "svg_title": "특고압 전력관(22.9kV) 정밀 이설 및 한전 송전 절차",
        "box1": ("전력 관로 부설", "한전 22.9kV 관로 부설"),
        "box2": ("특고압 케이블 포설", "TR-CNCV 케이블 견인"),
        "box3": ("절연 & 내전압 검속", "절연 ≥ 2000MΩ 통과"),
        "box4": ("한전 송전 승인", "한전 정전 후 송전 개시"),
        "alert": "특고압 전력 감전/지진 감전 사고 및 트램 변전소 정전 위험 전면 차단",
        "exp": "본 과업은 한전 22.9kV 특고압 케이블을 부설하고 절연저항(≥ 2000MΩ) 및 내전압(60kV) 검사를 거쳐 송전하는 절차입니다.",
        "summary": "절연저항 ≥ 2000MΩ, 내전압 60kV 및 한전 승인(255일)으로 특고압 전력관 이설을 완료하는 단계입니다!"
    },
    "oil": {
        "wbs": "2000-1-25", "title": "송유관 이설 공사", "dept": "현장 배관팀 / 대한송유관공사", "badge": "송유관 이설",
        "purpose": "대한송유관공사 관리 국가 송유관을 RT 100% 1급 및 N₂ 질소 완전 치환 시방으로 특별 안전 이설 완료",
        "method": "송유관 특수 강관 부설, 용접부 RT 100% 1급, N₂ 질소 완전 치환, 방식(CP) 전위 측정 및 궤도 이격 H ≥ 2.0m",
        "deliverables": "송유관 이설 성과표, RT 1급 비파괴 성적서, 대한송유관공사 송유 승인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">RT 비파괴 100% 1급</td><td style="text-align:center;">위험물안전관리법 / 송유관공사</td><td>• 국가 송유관 용접부 <strong>RT(방사선) 100% 전수 1급 판정</strong><br>• 음극 전기방식(CP) 전위 측정 및 테이핑 100%</td></tr>
<tr><td style="font-weight:bold;text-align:center;">N₂ 질소 완전 치환</td><td style="text-align:center;">송유관 안전 수칙</td><td>• 기존관 기름 완전 드레인 후 <strong>N₂ 질소 완전 치환</strong><br>• 1.5배 정격 수압시험 1시간 Zero 누수 확인</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 H≥2.0m</td><td style="text-align:center;">위험물 안전 시방</td><td>• 트램 궤도 구조물과 <strong>최소 이격거리 H ≥ 2.0m 특별 확보</strong><br>• 콘크리트 방호 피복 및 송유관 안전 표지판 부설</td></tr>""",
        "svg_title": "국가 송유관 정밀 이설 및 RT 1급 안전 통유 절차",
        "box1": ("송유관 부설", "위험물 특수 강관 부설"),
        "box2": ("용접 RT 100% 1급", "방사선 1급 비파괴 통과"),
        "box3": ("N₂ 질소 치환", "기름 드레인 & 질소 치환"),
        "box4": ("송유관공사 승인", "유류 송유 개시 승인"),
        "alert": "송유관 유류 누출 시 토양 대형 오염 및 화재/폭발 disaster 위험 전면 차단",
        "exp": "본 과업은 대한송유관공사 송유관을 RT 100% 1급 검사 및 N₂ 질소 치환을 수행하여 이격 2.0m로 안전하게 이설하는 절차입니다.",
        "summary": "RT 100% 1급, N₂ 질소 치환 및 궤도 이격 2.0m 준수로 송유관 이설을 완료하는 단계입니다!"
    },
    "final_check": {
        "wbs": "2000-1-26", "title": "상하수도 이설 시공 최종 점검", "dept": "현장 감리단 / 맑은물사업소", "badge": "상하수도 최종점검",
        "purpose": "이설 완료된 상하수도 시설에 대해 맑은물사업소 합동 준공 점검을 수행하고 GIS 위치 대장을 최종 등록 승인",
        "method": "합동 현장 점검, 수압 10kg/CCTV 100% 성적서 검속, GRS80 GIS 지도 반영 및 최종 준공 서명 획득",
        "deliverables": "상하수도 이설 최종 점검표, GIS 수치지형도 대장, 맑은물사업소 준공 검사 확인서",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">수압 / CCTV 성적서</td><td style="text-align:center;">화성시 맑은물사업소</td><td>• 상수도 수압 10kg/cm² 및 하수도 CCTV 100% 성적서 검속<br>• 잔류염소 소독 검사 필증 최종 서류 확인</td></tr>
<tr><td style="font-weight:bold;text-align:center;">GIS 수치지형도 이관</td><td style="text-align:center;">지적재조사법 / 화성시</td><td>• GRS80 세계측지계 이설관 위치 <strong>GIS 지형도 100% 반영</strong><br>• 화성시 지하시설물 통합 GIS 시스템 등록</td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 H≥1.5m</td><td style="text-align:center;">동탄트램 궤도 시방</td><td>• 이설 상하수도관과 트램 궤도 <strong>최소 이격거리 H ≥ 1.5m</strong> 재확인<br>• 맑은물사업소 감독관 준공 검사 서명 획득</td></tr>""",
        "svg_title": "상하수도 이설 시공 최종 준공 점검 절차",
        "box1": ("준공 서류 검속", "수압/CCTV 성적서 확인"),
        "box2": ("현장 합동 점검", "맑은물 입회 현치 검사"),
        "box3": ("GIS 대장 반영", "GRS80 GIS 지형도 등록"),
        "box4": ("맑은물 준공 승인", "최종 준공 확인서 서명"),
        "alert": "준공 미승인 시 상하수도 위수탁 정산 불가 및 트램 본공사 착공 지연 전면 차단",
        "exp": "본 과업은 수압/CCTV 성적서를 확인하고 화성시 GIS 대장 반영 및 맑은물사업소 최종 준공 서명을 받는 절차입니다.",
        "summary": "성적서 검속, GIS 지도 등록 및 맑은물사업소 준공 서명 획득으로 상하수도 이설 최종 점검을 완료하는 단계입니다!"
    }
}

print("Executing Batch Overwrite for 10 Target Activities Standard HTML files...")

for key, spec in activity_specs.items():
    folders = target_folders.get(key, [])
    std_content = get_std_template(
        spec["wbs"], spec["title"], spec["dept"], spec["badge"],
        spec["purpose"], spec["method"], spec["deliverables"],
        spec["rows"], spec["svg_title"], spec["box1"], spec["box2"],
        spec["box3"], spec["box4"], spec["alert"], spec["exp"], spec["summary"]
    )
    for folder in folders:
        sub_std = os.path.join(folder, "표준서")
        if os.path.exists(sub_std):
            for f in os.listdir(sub_std):
                if f.endswith(".html"):
                    fp = os.path.join(sub_std, f)
                    with open(fp, "w", encoding="utf-8") as out:
                        out.write(std_content)
                    print(f"  ✅ Overwritten [{spec['title']}]: {fp}")

print("🎉 Complete Batch Overwrite for 10 Target Activities Standard HTML files!")
