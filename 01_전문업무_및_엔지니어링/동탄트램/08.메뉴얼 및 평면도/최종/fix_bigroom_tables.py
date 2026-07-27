import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Find Target Big Room Folders
target_folders = []
for f in os.listdir(base_dir):
    f_path = os.path.join(base_dir, f)
    if os.path.isdir(f_path):
        if "Big Room" in f or "빅룸" in f or "5_착수전" in f:
            target_folders.append(f_path)

print(f"Target Big Room Folders Found: {target_folders}")

bigroom_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 착수전 Big Room 회의 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-5 Standard</div>
        <h1 class="title">착수전 Big Room 회의 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (Big Room 협의)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공공협력팀 / 5대 위탁기관 / 발주처</span>
            <span>|</span>
            <span><span class="badge">Big Room 회의 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>지장물 이설 착수 전 발주처, 감리단, 시공사 및 5대 위탁기관이 3D BIM 기반으로 모여 지하 간섭(Clash Zero) 검증 및 공정 패스트트랙 협의를 의결</td></tr>
            <tr><th>수행 방법</th><td>3D BIM/BAM 모델링 간섭 검증, 5대 기관 소요 공기(255~62일) CPM 마스터 스케줄 상호 조율 및 인허가 사전 심의 서류 통합 작성</td></tr>
            <tr><th>주요 산출물</th><td>착수전 Big Room 회의록 및 의결서, 3D BIM 간섭 검증 보고서, 5대 기관 통합 마스터 공정표</td></tr>
            <tr><th>관련 법령/기준</th><td>지하안전관리에 관한 특별법, 동탄트램 사업관리 및 Big Room 운영 지침</td></tr>
        </tbody>
    </table>

    <h2>2. 착수전 Big Room 회의 고유 정량 행정/기술 수칙 및 정량 협의 표</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🏛️ 3D BIM 간섭 검증 및 5대 위탁기관 마스터 공정 협의 수칙</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">Big Room 협의 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 규정 및 시스템</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 협의 수칙 및 의결 기준</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">3D BIM 간섭 검증</td>
                    <td style="text-align: center;">BIM/BAM 3D 모델링 지침</td>
                    <td>• 5대 관종 및 궤도 구조물 간 <strong>3D 간섭(Clash) Zero Target</strong> 검증<br>• 관로 간 최소 수평/수직 이격거리 <strong>H ≥ 1.5m</strong> 사전 100% 확정</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">기관별 공정 조율</td>
                    <td style="text-align: center;">CPM 마스터 공정 지침</td>
                    <td>• 전력(255일), 광역(160일), 통신(150일), 난방(80일), 가스(62일) 동시 조율<br>• 크리티컬 패스(Critical Path) 공정 겹침 사전 재배치 확정</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">인허가 패스트트랙</td>
                    <td style="text-align: center;">화성시 인허가 통합 체계</td>
                    <td>• 도로점용/굴착 심의(분기 1회) 및 경찰서 교통 심의 사전 서류 작성<br>• 5대 기관 합동 인허가 서류 <strong>14일 전 사전 통합 제출</strong> 의결</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">리스크 핫라인 운영</td>
                    <td style="text-align: center;">Big Room 운영 수칙</td>
                    <td>• 발주처-위탁기관-시공사 주간 단위 실시간 핫라인 의결 체계<br>• 현장 현치 오차 발생 시 48시간 이내 긴급 Big Room 재개최</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 Big Room 회의 절대 수칙:</strong> 본 과업은 시공 중 재재시공을 예방하기 위해 <strong>3D BIM 간섭 Zero 및 5대 기관 마스터 공정</strong>을 착수 전 100% 확정합니다.
        </div>
    </div>

    <h2>3. 착수전 Big Room 회의 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">착수전 Big Room 3D BIM 간섭 검증 및 기관 공정 조율 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 3D BIM 간섭 검증</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">Clash Zero Target 달성</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 기관 공정 동시조율</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">소요공기 255~62일 조율</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 인허가 패스트트랙</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">도로/교통 심의 서류 상정</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ Big Room 서명 의결</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">합동 착수 의결서 체결</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 착수전 Big Room 회의 미개최 시 지하 3D 간섭 및 기관 간 공정 충돌 재난 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 착수전 Big Room 회의 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 5대 위탁기관 및 발주처가 착수 전 모여 3D BIM 간섭 검증(Clash Zero) 및 마스터 공정을 조율하여 서명 의결하는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 3D BIM 간섭 Zero 달성, 5대 기관 공정 조율 및 인허가 패스트트랙 의결로 착수전 준비를 완료하는 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

print("Executing Fix for Big Room Standard HTML files...")

for target in target_folders:
    sub_std = os.path.join(target, "표준서")
    if os.path.exists(sub_std):
        for f in os.listdir(sub_std):
            if f.endswith('.html'):
                fp = os.path.join(sub_std, f)
                with open(fp, 'w', encoding='utf-8') as out:
                    out.write(bigroom_std)
                print(f"  ✅ Fixed Big Room Standard: {fp}")

print("🎉 Complete Fix for Big Room Standard HTML files!")
