import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

dir_joint_survey = os.path.join(base_dir, "5_지장물 조사 (위탁기관 합동)")
dir_bigroom = os.path.join(base_dir, "5_착수전 Big Room 회의")
dir_malkeunmul = os.path.join(base_dir, "6_관리기관(맑은물사업소) 협의")

# 1. Joint Survey HTMLs
js_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>지장물이설 - 지장물 조사 (위탁기관 합동) 기술 표준서</title>
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
        <h1 class="title">지장물 조사 (위탁기관 합동) 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (합동조사)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공사팀 / 유관기관 합동조사단</span>
            <span>|</span>
            <span><span class="badge">현장 현치 조사 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 궤도 노선 내 매설된 6대 유틸리티(상하수도, 가스, 난방, 통신, 전력, 광역상수) 관리기관 담당자 현장 동행 입회 하에 지하 매설관 실치 위치 및 심도를 100% 현장 검증</td></tr>
            <tr><th>수행 방법</th><td>GPR 지하탐지, GRS80 세계측지계 측량 및 인력 줄따기 시굴(폭 1.0m, 깊이 1.2m~1.5m)을 실시하고 현장 실측 조사 보고서 작성</td></tr>
            <tr><th>주요 산출물</th><td>위탁기관 합동 현장 조사 보고서, GPR 탐사 성과표, 매설관 현치 측량 성과표, 현장 조사 사진대지</td></tr>
            <tr><th>관련 법령/기준</th><td>지하안전관리에 관한 특별법 제24조(지하안전평가), KCS 11 20 00 (토공사 탐정 수칙)</td></tr>
        </tbody>
    </table>

    <h2>2. 위탁기관 합동 지장물 현치 조사 4단계 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">위탁기관 합동 현장 실치 조사 및 정밀 측량 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 합동 조사단 구성</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 6대 위탁기관 동행</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 감리단/시공사 입회</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 사전 도면 대조</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② GPR & 정밀 측량</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• GPR 오차 ≤ ±10cm</text>
                <text x="15" y="85" font-size="11" fill="#475569">• GRS80 오차 ≤ ±5cm</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 관로 심도 정밀 측정</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 인력 시굴 현치</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 폭 1.0m 줄따기 굴착</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 매설관 노출 및 확인</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 궤도 이격 H≥1.5m 검증</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 조사서 서명 승인</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 기관 입회 날인</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 수량 오차 확정</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 최종 조사서 제출</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 기관 동행 입회 없이 줄따기 굴착 단독 진행 시 관로 불시 파손 및 법정 책임 발생 예방</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 위탁기관 합동 조사 업무 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 조사 업무는 동탄트램 궤도 노선 굴착 전 기존 GIS 지하매설물 도면과 실제 현장의 맨홀, 밸브, 관로 위치 오차를 6대 관리기관 담당자와 현장에서 직접 대조하여 불시 지하 관로 파손 사고를 근본 차단하는 공학적 검증 단계입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 6대 위탁기관 동행 입회, GPR 오차 10cm 이내, GRS80 측량 오차 5cm 이내 및 인력 줄따기 시굴을 통해 지하관로 위치를 100% 확정하는 단계입니다!
    </div>

    <h2>3. 정량적 행정/공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) 합동 입회 기준:</strong> 6대 위탁기관(맑은물사업소, 삼천리, 난방공사, KT, 한전, K-water) 전담 감독관 <strong>100% 현장 동행 입회</strong> 필수</li>
            <li><strong>2) 탐사 및 측량 허용 오차:</strong> GPR 지형 탐지 심도 오차 <strong>≤ ±10cm 이내</strong>, GRS80 세계측지계 수평/수직 측량 오차 <strong>≤ ±5cm 이내</strong> 준수</li>
            <li><strong>3) 인력 시굴 폭/깊이:</strong> 줄따기 시굴 시 백호 굴착 금지 및 인력 굴착(폭 1.0m, 깊이 1.2m~1.5m) 시행으로 관로 보호</li>
            <li><strong>4) 트램 궤도 최소 이격거리:</strong> 현치 실측관과 트램 궤도 구조물 및 강화노반 간 <strong>최소 이격거리 H ≥ 1.5m 이상</strong> 확보 검증</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

# Helper function to safely write files into subfolders
def overwrite_sub(target_folder, filename, content):
    if os.path.exists(target_folder):
        for sub in os.listdir(target_folder):
            sub_p = os.path.join(target_folder, sub)
            if os.path.isdir(sub_p):
                for f in os.listdir(sub_p):
                    if filename in f and f.endswith('.html'):
                        full_f = os.path.join(sub_p, f)
                        with open(full_f, 'w', encoding='utf-8') as out:
                            out.write(content)
                        print(f"  ✅ Overwritten: {full_f}")

print("Executing clean master overwrite for 3 activities...")
overwrite_sub(dir_joint_survey, "표준서", js_std)
print("🎉 Success!")
