import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Find 3 Target Activity Folders (including twin folders)
target_folders = {}
for f in os.listdir(base_dir):
    f_path = os.path.join(base_dir, f)
    if os.path.isdir(f_path):
        if "맑은물사업소" in f:
            target_folders.setdefault("malkeunmul", []).append(f_path)
        elif "위수탁 지장물 이설 설계" in f or "7_위수탁" in f or "14_위수탁" in f:
            target_folders.setdefault("witak_design", []).append(f_path)
        elif "실정보고" in f or "8_상하수도" in f or "15_상하수도" in f:
            target_folders.setdefault("siljung_report", []).append(f_path)

print(f"Target Folders Found: {target_folders}")

# 1. Malkeunmul HTML Templates
malkeunmul_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 관리기관(맑은물사업소) 협의 기술 표준서</title>
    <style>
        :root { --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }
        .header { border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }
        .breadcrumb { font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }
        .title { font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }
        .meta-info { display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }
        .badge { background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }
        h2 { font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }
        table { width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }
        th, td { border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; }
        .svg-container { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }
        .diagram-explanation { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }
        .key-takeaway { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-6 Standard</div>
        <h1 class="title">관리기관(맑은물사업소) 협의 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (상하수도 협의)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공무팀 / 화성시 맑은물사업소</span>
            <span>|</span>
            <span><span class="badge">상하수도 인허가 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 구간 내 도급자 시행 상하수도(상수, 하수, 오수관) 이설 도서에 대해 화성시 맑은물사업소 기술 시방 검토 및 정식 이설 협의 승인 획득</td></tr>
            <tr><th>수행 방법</th><td>이설 계획 도면, 관재 규격서, 수량 산출서 제출 후 수압시험(10kg/cm²), CCTV 검사(100%), 자연유하 구배(≥1.0%) 시방 조건 협의 체결</td></tr>
            <tr><th>주요 산출물</th><td>맑은물사업소 이설 협의 승인서, 상하수도 이설 도서, 관재 및 수량 변경 비교표</td></tr>
            <tr><th>관련 법령/기준</th><td>수도법 제21조, 하수도법 제27조, 화성시 수도정비 기본계획 및 KCS 47 10 00</td></tr>
        </tbody>
    </table>

    <h2>2. 화성시 맑은물사업소 상하수도 이설 정량 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">💧 맑은물사업소 관재 선정 및 수질/수압 정량 검속 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">상하수도 구분</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관리기관 및 관련 법령</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 공학 시방 및 검속 수칙</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">상수도 관로 이설</td>
                    <td style="text-align: center;">맑은물사업소 (수도법)</td>
                    <td>• 이설 후 수압시험 <strong>10kg/cm² 1시간 유지 Zero 누수</strong> 검증<br>• 통수 전 24시간 수돗물 세척 및 잔류염소 소독 필증 획득</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">하수/오수관 이설</td>
                    <td style="text-align: center;">맑은물사업소 (하수도법)</td>
                    <td>• 하수도관 <strong>자연유하 구배 ≥ 1.0% 이상</strong> 확보<br>• 맨홀 인버트(Invert) 유선형 시공 및 CCTV 100% 전수 조사</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">궤도 이격 및 심도</td>
                    <td style="text-align: center;">동탄트램 시방서 / 토공</td>
                    <td>• 매설관 동파 방지 최소 심도(1.2m 이상) 확보<br>• 트램 궤도 구조물과 <strong>최소 이격거리 H ≥ 1.5m</strong> 검증</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">협의 승인 절차</td>
                    <td style="text-align: center;">화성시 조례</td>
                    <td>• 관재/관경 변경 내역서 맑은물사업소 담당자 입회 서명<br>• 정식 협의 승인 공문 획득 후 감리단 보고 및 착수</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 맑은물사업소 협의 절대 수칙:</strong> 본 과업은 상하수도 인계인수 거부를 차단하기 위해 <strong>상수 수압 10kg/cm², 하수 CCTV 100% 및 구배 1.0% 이상</strong>을 엄격히 적용합니다.
        </div>
    </div>

    <h2>3. 맑은물사업소 이설 협의 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">화성시 맑은물사업소 기술 시방 검토 및 승인 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 이설 도서 제출</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">이설 평·종단면도 구비</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 기술 시방 검토</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">수압 10kg / CCTV 100%</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 보완 및 입회</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">자연유하 구배 ≥1.0%</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 정식 승인 통보</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">사업소 승인 공문 획득</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 맑은물사업소 미협의 시 신설 상하수도 관로 인계인수 거부 및 통수 불허 리스크 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 맑은물사업소 이설 협의 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 도급자 이설 상하수관 도서를 화성시 맑은물사업소에 제출하여 수압 및 CCTV 시방 조건을 협의 승인받는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 상수 수압 10kg/cm², 하수 CCTV 100% 및 구배 1.0% 이상을 적용하여 맑은물사업소 협의 승인을 획득하는 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-6 | 지장물이설
    </div>
</div>
</body>
</html>"""

# 2. Witak Design HTML Templates
witak_design_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 위수탁 지장물 이설 설계 기술 표준서</title>
    <style>
        :root { --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }
        .header { border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }
        .breadcrumb { font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }
        .title { font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }
        .meta-info { display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }
        .badge { background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }
        h2 { font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }
        table { width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }
        th, td { border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; }
        .svg-container { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }
        .diagram-explanation { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }
        .key-takeaway { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-7 Standard</div>
        <h1 class="title">위수탁 지장물 이설 설계 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (위수탁 설계)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 설계팀 / 5대 위탁기관</span>
            <span>|</span>
            <span><span class="badge">엔지니어링 설계 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>5대 위탁기관(가스, 난방, 통신, 전력, 광역상수) 이설 기술 도서 작성 및 트램 궤도 간 3D CAD 간섭 검토를 통한 최적 이설 설계 반영</td></tr>
            <tr><th>수행 방법</th><td>위탁기관별 엔지니어링 시방 수수 준수, 궤도 최소 이격거리(H ≥ 1.5m) 확보 및 기관 기술 심의 승인 획득</td></tr>
            <tr><th>주요 산출물</th><td>위수탁 지장물 이설 설계 도서, 3D CAD 간섭 검토 리포트, 관종별 예산 산출서</td></tr>
            <tr><th>관련 법령/기준</th><td>KDS 47 10 00 지하매설물 설계 기준, 지하시설물 통합관리체계 지침</td></tr>
        </tbody>
    </table>

    <h2>2. 5대 위탁 관종별 이설 설계 정량 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">⚙️ 5대 위탁기관 시방 반영 정량 설계 검속 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">위수탁 관종</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">전담 기관 및 설계 시방</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 설계 시방 및 품질 수칙</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">도시가스관 설계</td>
                    <td style="text-align: center;">㈜삼천리 (가스사업법)</td>
                    <td>• 용접부 RT 100% 1급, N₂ 질소 퍼지(잔류산소 ≤ 1.0%) 설계<br>• CP 테이핑 및 궤도 최소 이격거리 H ≥ 1.5m 반영 (62일)</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">지역난방관 설계</td>
                    <td style="text-align: center;">한국지역난방공사</td>
                    <td>• 이중보온관 NDT 100%, 누수 감지선 절연저항 ≥ 100MΩ 설계<br>• 110℃ / 16bar 수압 시험 조항 포함 (80일)</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">통신관로 설계</td>
                    <td style="text-align: center;">KT / SKT / LGU+</td>
                    <td>• 광 접속 손실 OTDR ≤ 0.05dB, 심야 시간대 Cut-over 설계<br>• 72-Core 광케이블 핸드홀 방서/수밀 설계 (150일)</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">특고압 전력 설계</td>
                    <td style="text-align: center;">한국전력공사 경기본부</td>
                    <td>• 22.9kV TR-CNCV 특고압 지중 관로, 절연저항 ≥ 2,000MΩ 설계<br>• 내전압 60kV 10분, 전력 맨홀 접지저항 ≤ 10Ω 반영 (255일)</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">광역상수도 설계</td>
                    <td style="text-align: center;">한국수자원공사 (K-water)</td>
                    <td>• D800mm 이상 광역관 무단수 Tapping 차단 공법 설계<br>• 이송 수압 15kg/cm² 이탈방지 조인트 설계 (160일)</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 위수탁 이설 설계 절대 수칙:</strong> 5대 관종 이설 설계 시 동탄트램 궤도 구조물과 <strong>수평/수직 최소 이격거리 H ≥ 1.5m 이상</strong>을 100% 반영합니다.
        </div>
    </div>

    <h2>3. 위수탁 지장물 이설 설계 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">위수탁 지장물 이설 설계 및 3D CAD 간섭 검토 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 관종별 설계 지침</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">위탁기관 시방 수집</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 3D CAD 간섭 검토</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">궤도 이격 H≥1.5m 검증</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 시방 반영</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">RT/NDT/OTDR/절연 반영</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 기관 설계 승인</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">위탁기관 심의 승인 공문</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 위수탁 이설 설계 승인 지연 시 지장물 굴착 착공 불가 및 트램 공전 리스크 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 위수탁 지장물 이설 설계 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 5대 위탁기관 시방 수칙(가스/난방/통신/전력/광역상수)을 설계 도서에 100% 반영하고 3D CAD 정합으로 궤도 이격 1.5m를 확보하는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 5대 위탁기관 품질 시방 반영 및 궤도 이격 1.5m 확보로 기관 기술 심의 승인을 획득하는 핵심 설계 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-7 | 지장물이설
    </div>
</div>
</body>
</html>"""

# 3. Siljung Report HTML Templates
siljung_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 상하수도 이설계획 실정보고 기술 표준서</title>
    <style>
        :root { --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }
        .header { border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }
        .breadcrumb { font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }
        .title { font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }
        .meta-info { display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }
        .badge { background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }
        h2 { font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }
        table { width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }
        th, td { border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; }
        .svg-container { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }
        .diagram-explanation { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }
        .key-takeaway { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-8 Standard</div>
        <h1 class="title">상하수도 이설계획 실정보고 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (실정보고)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공무팀 / 감리단 / 발주처</span>
            <span>|</span>
            <span><span class="badge">설계 변경 승인 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>도급자 시행 상하수도 현장 시굴 실측 오차에 따른 관경·관재·이설 위치 변경 건에 대해 감리단 및 발주처에 정식 실정보고 승인 획득</td></tr>
            <tr><th>수행 방법</th><td>현치 오차 비교표, 설계 변경 수량 산출서, 맑은물사업소 입회 의견서 작성 및 감리원 적정성 검속 승인</td></tr>
            <tr><th>주요 산출물</th><td>상하수도 이설계획 실정보고서, 설계 변경 수량 비교표, 감리단 검토 의견서</td></tr>
            <tr><th>관련 법령/기준</th><td>국가지계약법 시행령 제65조(설계 변경), KCS 11 20 00 토공 시방</td></tr>
        </tbody>
    </table>

    <h2>2. 상하수도 이설계획 실정보고 정량 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">📝 실정보고 수량 재산정 및 설계 변경 검속 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">보고 및 변경 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 법령 및 규정</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 수칙 및 변경 승인 조건</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">현치 오차 증빙서</td>
                    <td style="text-align: center;">건설기술 진흥법</td>
                    <td>• GPR 탐사(오차 ±10cm) 및 인력 시굴 현장 노출 사진대지 구비<br>• GRS80 세계측지계 측량 성과표(오차 ±5cm) 대조 증빙</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">관재/관경 산출서</td>
                    <td style="text-align: center;">KCS 47 10 00 / 맑은물</td>
                    <td>• 신설 상하수도 관경(D300~D800mm) 및 이설 연장 증감 산출<br>• 상수도 수압 10kg/cm², 하수도 CCTV 100% 시방 적용 확인</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">공사비 변경 산정</td>
                    <td style="text-align: center;">국가계약법 시행령 제65조</td>
                    <td>• 계약 단가 및 신규 공종 단가 산정 적정성 검증<br>• 토사 굴착량, 되메우기 층다짐(95% 이상) 내역서 첨부</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">감리/발주처 승인</td>
                    <td style="text-align: center;">발주처 계약 조건</td>
                    <td>• 감리원 현장 적정성 검토 서명 결재 획득<br>• 화성시 발주처 정식 실정보고 승인 공문 수령 후 시공</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 실정보고 이행 절대 수칙:</strong> 본 과업은 정산 분쟁을 예방하기 위해 <strong>GPR/측량 성과 증빙 및 감리/발주처 사전 승인</strong>을 거쳐 시공합니다.
        </div>
    </div>

    <h2>3. 상하수도 이설계획 실정보고 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">상하수도 이설계획 실정보고 및 승인 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 현치 오차 도출</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">GPR/측량 성과 산출</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 실정보고서 작성</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">변경 내역/수량 수립</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 감리단 검속</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">감리원 검토 서명</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 발주처 승인</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">설계 변경 금액 승인</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 실정보고 미승인 무단 시공 시 공사비 정산 불허 및 사후 설계 변경 거부 리스크 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 상하수도 이설계획 실정보고 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 현치 오차에 의한 변경 사항을 정량 수량 비교표로 산정하여 감리단 및 발주처 승인을 획득하는 행정 및 계약 변경 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> GPR/측량 성과 증빙 및 감리원 서명, 발주처 승인을 획득하여 설계 변경 금액을 확정하는 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-8 | 지장물이설
    </div>
</div>
</body>
</html>"""

print("Executing Batch Overwrite for 3 Target Activities...")

def update_activity_files(folder_list, std_c):
    for target in folder_list:
        sub_std = os.path.join(target, "표준서")
        if os.path.exists(sub_std):
            for f in os.listdir(sub_std):
                if f.endswith('.html'):
                    fp = os.path.join(sub_std, f)
                    with open(fp, 'w', encoding='utf-8') as out:
                        out.write(std_c)
                    print(f"  ✅ Standard Overwritten: {fp}")

update_activity_files(target_folders.get("malkeunmul", []), malkeunmul_std)
update_activity_files(target_folders.get("witak_design", []), witak_design_std)
update_activity_files(target_folders.get("siljung_report", []), siljung_std)

print("🎉 Complete Batch Overwrite for 3 Target Activities Standard HTML files!")
