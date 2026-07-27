import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Find 2 Target Activity Folders (including twin folders)
target_folders = {}
for f in os.listdir(base_dir):
    f_path = os.path.join(base_dir, f)
    if os.path.isdir(f_path):
        if "무단수 연결" in f or "15_무단수" in f or "22_무단수" in f:
            target_folders.setdefault("hot_tapping", []).append(f_path)
        elif "연결관로 접속" in f or "16_신규관로" in f or "23_신규관로" in f:
            target_folders.setdefault("pipe_connection", []).append(f_path)

print(f"Target Folders Found: {target_folders}")

# 1. Hot Tapping HTML Templates
hot_tapping_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 무단수 연결을 위한 시설 설치 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-15 Standard</div>
        <h1 class="title">무단수 연결을 위한 시설 설치 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (무단수 천공)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 배관팀 / K-water / 맑은물</span>
            <span>|</span>
            <span><span class="badge">무단수 천공 시방 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 궤도 하부 상수도 및 광역상수도 이설 시 시민 수돗물 공급 중단 없이 무단수 천공(Hot-Tapping) 장비를 통해 이설 관로를 안전하게 연결</td></tr>
            <tr><th>수행 방법</th><td>무단수 천공 전용 새들 밸브 고정, 수압 15kg/cm² 이탈방지 세팅, 유압 천공기 가동 및 천공 칩(Chip) 100% 제거</td></tr>
            <tr><th>주요 산출물</th><td>무단수 천공 성과 보고서, 새들 밸브 기밀/수밀 시험성적서, 잔류염소 소독 필증</td></tr>
            <tr><th>관련 법령/기준</th><td>K-water 광역상수도 무단수 천공 지침, KCS 47 10 00 배관 수칙</td></tr>
        </tbody>
    </table>

    <h2>2. 무단수 천공(Hot-Tapping) 시설 설치 정량 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">💧 무단수 새들 밸브 체결 및 고압 천공 정량 수칙</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">무단수 공종 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">적용 시방 및 장비</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 수칙 및 안전 압력</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">새들 밸브 체결 수칙</td>
                    <td style="text-align: center;">D300~D800mm 무단수 새들</td>
                    <td>• 기설 관로 외면에 무단수 탭 분기 새들 밸브 볼팅 <strong>토크 100% 준수</strong><br>• 가스켓 밀착 시공 및 수압 15kg/cm² 이탈방지 압륜 조임</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">유압 천공기 가동</td>
                    <td style="text-align: center;">Under-Pressure Tapping기</td>
                    <td>• 무단수 천공기 정착 후 이송 수압 <strong>15kg/cm² 견딤 테스트</strong> 통과<br>• 천공 칩(Chip) 및 수태 이물질 100% 외부 자동 배출 세팅</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">수밀 및 염소 소독</td>
                    <td style="text-align: center;">수도법 / K-water 지침</td>
                    <td>• 천공 후 새들 밸브 수밀시험 <strong>15kg/cm² 1시간 유지 Zero 누수</strong><br>• 신설관 통수 전 24시간 잔류염소 소독 검사 필증 구비</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">궤도 이격 심도</td>
                    <td style="text-align: center;">동탄트램 궤도 시방서</td>
                    <td>• 무단수 분기 밸브 부위 트램 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 확보<br>• 밸브 하부 보호 콘크리트 패드(Saddle Pad) 부설</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 무단수 천공 절대 수칙:</strong> 본 과업은 수돗물 단수 민원을 차단하기 위해 <strong>새들 수압 15kg/cm², 천공 칩 100% 제거 및 염소 소독</strong>을 준수합니다.
        </div>
    </div>

    <h2>3. 무단수 연결 시설 설치 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">무단수 천공(Hot-Tapping) 새들 밸브 부설 및 통수 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 새들 밸브 부설</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">이탈방지 볼팅 100%</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 무단수 천공기 정착</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">수압 15kg 테스트 통과</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 수압 15kg 천공</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">천공 칩 100% 제거</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 차단 밸브 승인</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">잔류염소 소독 필증 결재</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 무단수 천공 조인트 이탈 시 상수도 고압 뿜음 및 대규모 단수 집단 민원 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 무단수 연결 시설 설치 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 수돗물 공급 중단 없이 무단수 새들 밸브를 설치하고 수압 15kg/cm² 조건에서 안전하게 천공 및 이설관을 분기 조율하는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 무단수 새들 밸브 체결, 수압 15kg/cm² 천공, 천공 칩 제거 및 염소 소독으로 단수 없는 연결을 완료하는 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-15 | 지장물이설
    </div>
</div>
</body>
</html>"""

# 2. Pipe Connection HTML Templates
pipe_conn_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 신규관로 및 연결관로 접속 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-16 Standard</div>
        <h1 class="title">신규관로 및 연결관로 접속 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (관로 접속)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 배관팀 / 5대 위탁기관</span>
            <span>|</span>
            <span><span class="badge">관로 접속 기술 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>기존 지하 지장관로와 신규 이설관로 간의 최종 컷오프(Cut-off) 및 찰부 접속(Tie-in)을 안전하게 연결하여 유체/전기 통수 개시</td></tr>
            <tr><th>수행 방법</th><td>심야 Cut-over 시간대(01:00~05:00) 준수, 수밀 플랜지 체결, 관종별 테스트(상수 10kg, 가스 RT 1급, 통신 OTDR ≤ 0.05dB) 통과</td></tr>
            <tr><th>주요 산출물</th><td>연결관로 접속 검속 보고서, 관종별 공인 성적서, 최종 통수/수전 확인증</td></tr>
            <tr><th>관련 법령/기준</th><td>KCS 47 10 00 배관공사 시방, 5대 위탁기관 기술 접속 규정</td></tr>
        </tbody>
    </table>

    <h2>2. 관로 최종 찰부 접속(Tie-in) 정량 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🔗 5대 관종별 접속 시방 및 심야 Cut-over 정량 수칙</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">관로 접속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">적용 시방 및 관종</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 수칙 및 시험 통과 기준</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">심야 Cut-over 준수</td>
                    <td style="text-align: center;">통신 / 가스 / 상수도</td>
                    <td>• 주민 이용 불편 최소화를 위해 <strong>심야 시간대(01:00~05:00)</strong> 접속 시행<br>• 사전 수용가 알림 공지 및 24시간 비상 대기조 운영</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">플랜지 수밀 접속</td>
                    <td style="text-align: center;">DCI 상수관 / 난방관</td>
                    <td>• 이중 수밀 가스켓 착용 및 토크 렌치 <strong>볼팅 토크 100% 균일 체결</strong><br>• 상수도 수압시험 <strong>10kg/cm² 1시간 Zero 누수</strong> 확인</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">용접 및 비파괴검사</td>
                    <td style="text-align: center;">도시가스 / 지역난방</td>
                    <td>• 가스관 용접부 <strong>RT(방사선) 100% 1급 판정</strong> 및 N₂ 질소 퍼지<br>• 난방 이중보온관 NDT 100% 및 감지선 도통 ≥ 100MΩ 검속</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">통신/전력 접속 시험</td>
                    <td style="text-align: center;">KT / 한전 경기본부</td>
                    <td>• 광케이블 접속 손실 <strong>OTDR ≤ 0.05dB 이내</strong> 100% 통과<br>• 특고압전력 22.9kV 절연저항 <strong>≥ 2,000MΩ</strong> 및 내전압 60kV 통과</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 관로 접속 절대 수칙:</strong> 본 과업은 접속부 누수 및 통신/전력 장애를 차단하기 위해 <strong>심야 Cut-over(01~05시) 및 관종별 공인 성적서</strong>를 획득합니다.
        </div>
    </div>

    <h2>3. 신규관로 및 연결관로 접속 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">신규관로 및 기존관 최종 Tie-in 접속 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 심야 Cut-over 준비</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">01:00~05:00 절체 사전 통지</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 기존관 절단 Tie-in</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">잔류 유체 드레인 후 절단</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 수밀 플랜지 체결</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">토크 렌치 균일 조임</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 성적서 검속 승인</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">수압/RT/OTDR/절연 결재</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 접속 부위 누수 및 광 통신 절체 장애 발생 시 즉시 복구 핫라인 가동으로 위험 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 신규관로 및 연결관로 접속 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 심야 시간대(01~05시) 기존 관로를 절단하고 수밀 플랜지 체결 및 관종별 시험(수압 10kg, RT 1급, OTDR ≤ 0.05dB)을 거쳐 최종 접속하는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 심야 Cut-over 준수, 수밀 플랜지 체결 및 관종별 검사 성적서(수압/RT/OTDR/절연) 통과로 최종 접속을 완료하는 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-16 | 지장물이설
    </div>
</div>
</body>
</html>"""

print("Executing Batch Overwrite for 2 Special Connection Target Activities...")

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

update_activity_files(target_folders.get("hot_tapping", []), hot_tapping_std)
update_activity_files(target_folders.get("pipe_connection", []), pipe_conn_std)

print("🎉 Complete Batch Overwrite for 2 Special Connection Target Activities Standard HTML files!")
