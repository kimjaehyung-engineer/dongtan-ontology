import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

target_folders = []
for f in os.listdir(base_dir):
    f_path = os.path.join(base_dir, f)
    if os.path.isdir(f_path):
        if "Big Room" in f or "빅룸" in f or "5_착수전" in f:
            target_folders.append(f_path)

print(f"Target Big Room Folders Found: {target_folders}")

# 1. Standard HTML Template (100% PDF content matched)
bigroom_pdf_std = """<!DOCTYPE html>
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
        .tip-box { background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 18px; margin-top: 20px; color: #92400e; font-size: 0.92rem; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-5 Standard</div>
        <h1 class="title">트램 지장물 이설공사 착수 전 빅룸(Big Room) 회의 핵심 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (Big Room 협의)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공공협력팀 / 5대 위탁기관 / 발주처</span>
            <span>|</span>
            <span><span class="badge">Big Room 회의 마스터 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 참석 기관 (Overview & Stakeholders)</h2>
    <p style="font-size: 0.95rem; color: #334155; margin-bottom: 15px;">
        트램 지장물 이설은 여러 기관의 이해관계와 개별 일정이 복잡하게 얽혀 있어, 착수 전 모든 관계자가 참여하는 <strong>빅룸(Big Room) 회의</strong>에서 목표를 맞추고 리스크를 사전에 제거하는 것이 필수적입니다.
    </p>
    <table>
        <tbody>
            <tr><th style="width: 20%;">주관 기관</th><td>트램 본공사 시공사 및 발주처 (화성시 / 경기교통공사)</td></tr>
            <tr><th>전력/통신 참석</th><td>한국전력공사 경기본부, KT, LG U+, SKT 등 통신 3사</td></tr>
            <tr><th>가스/열 참석</th><td>㈜삼천리 도시가스, 한국지역난방공사 동탄지사</td></tr>
            <tr><th>상하수도 참석</th><td>화성시 맑은물사업소 (수도행정과, 하수도과)</td></tr>
            <tr><th>행정/안전 참석</th><td>관할 화성동탄경찰서(교통계), 화성시 도로관리과</td></tr>
            <tr><th>설계/감리 참석</th><td>3D BIM 대표 설계사, 분야별 현장 감리단</td></tr>
        </tbody>
    </table>

    <h2>2. 5대 핵심 논의 아젠다 (Main Agenda)</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🎯 빅룸 회의 5대 핵심 논의 주제 및 정량 의결 시방</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 22%;">핵심 아젠다</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 28%;">핵심 검토 질문</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 50%;">주요 내용 및 정량 결정 사항</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">1. 3D BIM 기반 간섭 검토</td>
                    <td style="text-align: center;">"도면과 실제 위치가 다른 구간은 어디며 상호 간섭은 어떻게 조정할 것인가?"</td>
                    <td>• 시굴(줄파기) 및 GPR 탐사 결과 기반 통합 3D BIM 모델 공유<br>• 트램 궤도 슬래브, 정거장 기초, 신호/전력 구조물 간 공간 간섭 <strong>최소 이격(H ≥ 1.5m)</strong> 수치 검증<br>• 미확인 지장물 발견 시 즉각 대응 현장 확인 프로토콜 확립</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">2. 이설 순서 & 공정 동기화</td>
                    <td style="text-align: center;">"누가 먼저 이설해야 다음 기관이 들어오며, 최종 목표 일정은 언제인가?"</td>
                    <td>• 심도 및 위험도에 따른 이설 우회 순서 정의:<br>&nbsp;&nbsp;<strong>깊은 하수관/수도 ➔ 전력/통신 ➔ 도시가스</strong><br>• 기관별 예산 집행 시기, 단수/단전/정가스 승인 일정 반영<br>• 트램 궤도 구축 착수 일정과 직결되는 주공정(Critical Path) 관리</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">3. 통합 교통처리계획 (TMP)</td>
                    <td style="text-align: center;">"도심지 차선을 통제하면서 시민 불편과 민원을 어떻게 최소화할 것인가?"</td>
                    <td>• 차로 차단 최소화 전략(차선 폭 W ≥ 3.0m) 및 점용 허가 구간 조정 (경찰서 협의)<br>• 야간 공사 필수 구간(도로 횡단, 정전/단수 작업) 통보 및 사전 홍보 방안<br>• 공사 구간 우회 도로 확보 및 버스 정류장 임시 이전 대책</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">4. 다짐 & LCLM 품질 일원화</td>
                    <td style="text-align: center;">"이설 후 되메우기 침하로 인한 트램 탈선 리스크를 어떻게 차단할 것인가?"</td>
                    <td>• 각 기관별 시공법과 트램 궤도 하부 엄격 침하 기준 합의<br>• 좁은 굴착 및 협소 구간에 대한 <strong>유동성 채움재(LCLM)</strong> 적용 범위 규정<br>• 이설 완료 후 정밀 계측 및 다짐 밀도(95% 이상) 시험 결과 공유</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">5. 비상 대응 핫라인 구축</td>
                    <td style="text-align: center;">"현장에서 돌발 상황(관로 파손 등) 발생 시 즉시 판단할 시스템이 있는가?"</td>
                    <td>• 기관별 24시간 비상 연락망 및 현장 즉시 출동 담당자 지정<br>• 현장 변경 발생 시 <strong>선(先) 현장 협의 - 후(後) 문서화</strong> 프로세스 승인<br>• 정기 빅룸 회의 주기(주 1회 또는 월 2회) 및 종합 상황실 운영</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 Big Room 회의 절대 수칙:</strong> 본 과업은 시공 재재시공을 차단하기 위해 <strong>3D BIM 간섭 Zero, 심도순 이설(하수/수도➔전력/통신➔가스) 및 LCLM 채움재 품질</strong>을 착수 전 확정합니다.
        </div>
    </div>

    <h2>3. 빅룸 회의 진행 스케줄 표준 (2시간 120분 코스)</h2>
    <table>
        <thead>
            <tr style="background: #e2e8f0; color: #0f172a;">
                <th style="padding: 10px; text-align: center; width: 15%;">시간</th>
                <th style="padding: 10px; text-align: center; width: 25%;">프로그램</th>
                <th style="padding: 10px; text-align: center; width: 45%;">세부 운영 내용</th>
                <th style="padding: 10px; text-align: center; width: 15%;">주관/참석</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="font-weight: bold; text-align: center;">00~15분</td>
                <td style="text-align: center;">개회 및 트램 전체 일정 공유</td>
                <td>• 본공사 목표일 및 이설 목표 기간 브리핑, 기관별 협조 사항 안내</td>
                <td style="text-align: center;">시공사 / 발주처</td>
            </tr>
            <tr>
                <td style="font-weight: bold; text-align: center;">15~45분</td>
                <td style="text-align: center;">3D BIM 간섭 검토</td>
                <td>• 구간별 지장물 간섭 리스크 확인, 궤도 이격 1.5m 및 이설 선형 확정</td>
                <td style="text-align: center;">설계사 / 전 기관</td>
            </tr>
            <tr>
                <td style="font-weight: bold; text-align: center;">45~75분</td>
                <td style="text-align: center;">공정 순서(Sequence) 조정</td>
                <td>• 심도 순서(하수/수도➔전력/통신➔가스) 이설 목표일 작성 및 겹침 조정</td>
                <td style="text-align: center;">전 기관</td>
            </tr>
            <tr>
                <td style="font-weight: bold; text-align: center;">75~105분</td>
                <td style="text-align: center;">TMP 및 품질/안전 합의</td>
                <td>• 경찰서 교통 차선 통제, 유동성 채움재(LCLM) 적용 구간 및 야간 작업 승인</td>
                <td style="text-align: center;">경찰서 / 기관</td>
            </tr>
            <tr>
                <td style="font-weight: bold; text-align: center;">105~120분</td>
                <td style="text-align: center;">Action Item 확정 및 핫라인</td>
                <td>• 기관별 차기 회의 제출 서류 명시, 24시간 비상 핫라인 담당자 교환</td>
                <td style="text-align: center;">전체 참석자</td>
            </tr>
        </tbody>
    </table>

    <h2>4. 착수전 Big Room 회의 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 340" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="340" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="32" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">트램 지장물 이설공사 착수 전 빅룸(Big Room) 5대 아젠다 처리 절차</text>

            <!-- Box 1 -->
            <g transform="translate(30, 55)">
                <rect width="180" height="195" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="38" rx="8" fill="#dbeafe"/>
                <text x="90" y="24" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 3D BIM 간섭 검토</text>
                
                <text x="14" y="65" font-size="11" font-weight="bold" fill="#0f172a">• GPR/시굴 3D 모델 공유</text>
                <text x="14" y="88" font-size="11" fill="#334155">• 궤도 이격 H≥1.5m 검증</text>
                <text x="14" y="111" font-size="11" fill="#334155">• 미확인 지장물 프로토콜</text>
                <text x="14" y="134" font-size="11" fill="#2563eb" font-weight="bold">• 3D Clash Zero 달성</text>
            </g>

            <text x="225" y="155" font-size="22" fill="#2563eb">➔</text>

            <!-- Box 2 -->
            <g transform="translate(245, 55)">
                <rect width="190" height="195" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="38" rx="8" fill="#ffedd5"/>
                <text x="95" y="24" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 공정 동기화 (Sync)</text>

                <text x="14" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 하수/수도➔전력➔가스</text>
                <text x="14" y="88" font-size="11" fill="#334155">• 단수/단전/정가스 일괄</text>
                <text x="14" y="111" font-size="11" fill="#334155">• Critical Path 스케줄</text>
                <text x="14" y="134" font-size="11" fill="#ea580c" font-weight="bold">• 공정 순서(Sequence) 확정</text>
            </g>

            <text x="450" y="155" font-size="22" fill="#ea580c">➔</text>

            <!-- Box 3 -->
            <g transform="translate(470, 55)">
                <rect width="190" height="195" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="24" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ TMP & LCLM 합의</text>

                <text x="14" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 경찰서 교통통제 차선</text>
                <text x="14" y="88" font-size="11" fill="#334155">• LCLM 유동성채움재 범위</text>
                <text x="14" y="111" font-size="11" fill="#334155">• 야간 공사 및 우회 도로</text>
                <text x="14" y="134" font-size="11" fill="#059669" font-weight="bold">• 궤도 하부 침하 방지</text>
            </g>

            <text x="675" y="155" font-size="22" fill="#059669">➔</text>

            <!-- Box 4 -->
            <g transform="translate(695, 55)">
                <rect width="175" height="195" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="38" rx="8" fill="#e0e7ff"/>
                <text x="87" y="24" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 24h 핫라인 결재</text>

                <text x="14" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 기관별 24h 출동 담당</text>
                <text x="14" y="88" font-size="11" fill="#334155">• 先현장협의 - 後문서화</text>
                <text x="14" y="111" font-size="11" fill="#334155">• Action Item 서류 확정</text>
                <text x="14" y="134" font-size="11" fill="#1e3a8a" font-weight="bold">• 착수 준비 서명 완결</text>
            </g>

            <rect x="30" y="270" width="840" height="48" rx="8" fill="#1e3a8a"/>
            <text x="450" y="299" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 착수전 빅룸 회의 미개최 시 지하 3D 간섭 및 궤도 침하/탈선 재난 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 착수전 Big Room 회의 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 5대 위탁기관 및 발주처/경찰서가 모여 3D BIM 간섭 검토, 심도별 공정 순서(Sequence), TMP 및 LCLM 유동성채움재 합의를 이끌어내어 착수하는 절차입니다.</p>
    </div>

    <div class="tip-box">
        <h4 style="margin: 0 0 8px 0; color: #92400e;">💡 성공적인 빅룸(Big Room) 회의를 위한 3가지 핵심 팁</h4>
        <ol style="margin: 0; padding-left: 20px; line-height: 1.7;">
            <td><strong>1. 3D 모델 및 대형 지도 활용:</strong> 종이 도면 대신 대형 스크린에 3D BIM 모델을 띄우거나 대형 평면도를 바닥/벽면에 붙이고 포스트잇으로 기관별 일정을 직접 붙여가며 직관적 진행</td>
            <td><strong>2. Action Item의 명확화:</strong> "협의하기로 함"이 아닌 <em>"A기관 담당자가 X월 Y일까지 B문서를 제출함"</em>과 같이 주체, 기한, 결과물을 명확히 기재 결재</td>
            <td><strong>3. 상호 인센티브/협력 의지 확인:</strong> 지장물 이설 지연 시 전체 트램 공기에 미치는 영향 공유 및 인허가 패스트트랙 지원 등 발주처 차원의 협력 유인책 제시</td>
        </ol>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

# 2. Playbook (Guideline) HTML Template
bigroom_pdf_gui = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 착수전 Big Room 회의 수행지침서</title>
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
        .step-card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 24px; margin-bottom: 20px; border-left: 6px solid var(--accent-blue); }
        .step-title { font-size: 1.2rem; font-weight: 800; color: var(--accent-blue); margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
        .sub-bullet { margin-left: 20px; font-size: 0.93rem; color: #334155; margin-bottom: 6px; line-height: 1.7; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-5 Playbook</div>
        <h1 class="title">트램 지장물 이설공사 착수 전 빅룸(Big Room) 회의 수행지침서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (Big Room 수행)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공공협력팀 / 공무팀</span>
            <span>|</span>
            <span><span class="badge">빅룸 3단계 플레이북</span></span>
        </div>
    </div>

    <h2>📋 3단계 빅룸(Big Room) 회의 실행 플레이북 (Playbook)</h2>

    <!-- Step 1 -->
    <div class="step-card">
        <div class="step-title">1단계: 회의 사전 준비 단계 (Pre-Meeting Preparation)</div>
        <div class="sub-bullet">• <strong>3D BIM 모델 및 GPR 탐사 성과 통합:</strong> 시굴(줄파기) 및 GPR 탐사 성과를 반영한 통합 3D BIM 모델을 준비하고, 대형 스크린 렌더링 장비 구축</div>
        <div class="sub-bullet">• <strong>참석 대상 기관 사전 배포:</strong> 한전, KT/SKT/LGU+, 삼천리, 난방공사, 맑은물사업소, 경찰서 및 감리단에 2시간 진행 타임테이블 배포</div>
        <div class="sub-bullet">• <strong>5대 아젠다 양식 준비:</strong> 3D 간섭 리스트, 이설 순서(Sequence), TMP 및 LCLM 품질 일원화 안안 양식 준비</div>
        <div class="sub-bullet">• <strong>24시간 비상 연락망 사전 취합:</strong> 5대 기관별 24시간 비상 출동 담당자 직통 연락처 취합</div>
    </div>

    <!-- Step 2 -->
    <div class="step-card" style="border-left-color: #ea580c;">
        <div class="step-title" style="color: #9a3412;">2단계: 2시간 빅룸 회의 실행 및 5대 아젠다 의결 (Meeting Execution)</div>
        <div class="sub-bullet">• <strong>00~15분 (개회 & 전체 일정):</strong> 시공사/발주처 주관 트램 본공사 목표일 및 지장물 이설 목표 기간 브리핑</div>
        <div class="sub-bullet">• <strong>15~45분 (3D BIM 간섭 검토):</strong> 대형 스크린 3D BIM 렌더링을 통해 궤도 이격(H ≥ 1.5m) 및 정거장 기초 간섭 수치 확정</div>
        <div class="sub-bullet">• <strong>45~75분 (Sequence 공정 동기화):</strong> 심도 및 위험도에 따라 <strong>깊은 하수관/수도 ➔ 전력/통신 ➔ 도시가스</strong> 이설 순서 확정</div>
        <div class="sub-bullet">• <strong>75~105분 (TMP & LCLM 품질 합의):</strong> 경찰서 협의 차로 통제 최소화, 협소 부위 <strong>유동성 채움재(LCLM)</strong> 사용 및 야간 작업 승인</div>
        <div class="sub-bullet">• <strong>105~120분 (Action Item 명확화):</strong> "A기관 담당자가 X월 Y일까지 B문서를 제출함" 형태로 주체, 기한, 결과물 명시 서명</div>
    </div>

    <!-- Step 3 -->
    <div class="step-card" style="border-left-color: #059669;">
        <div class="step-title" style="color: #15803d;">3단계: 회의 결과 이행 및 핫라인 모니터링 (Post-Meeting Follow-up)</div>
        <div class="sub-bullet">• <strong>선(先) 현장 협의 - 후(後) 문서화 승인:</strong> 돌발 현치 오차 발생 시 24시간 핫라인으로 현장 먼저 처리 후 서류 후행 이관 승인</div>
        <div class="sub-bullet">• <strong>정기 빅룸 회의 운영:</strong> 주 1회(또는 월 2회) 현장 종합 상황실에서 Action Item 이행 여부 100% 모니터링</div>
        <div class="sub-bullet">• <strong>다짐 밀도 및 시험 결과 공유:</strong> 이설 완료 후 되메우기 층다짐 밀도(95% 이상) 시험 성적서를 빅룸 보관함에 상시 공유</div>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침서 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

# 3. Checklist HTML Template
bigroom_pdf_chk = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 착수전 Big Room 회의 체크리스트</title>
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
        .checkbox-cell { text-align: center; width: 80px; font-weight: bold; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-5 Checklist</div>
        <h1 class="title">트램 지장물 이설공사 착수 전 빅룸(Big Room) 회의 검측 체크리스트</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (Big Room 검측)</span>
            <span>|</span>
            <span><strong>검측일시:</strong> 착수 전 회의 시</span>
            <span>|</span>
            <span><span class="badge">빅룸 검측 체크리스트</span></span>
        </div>
    </div>

    <h2>☑️ 착수전 빅룸(Big Room) 회의 9대 핵심 실시간 O/X 검측 항목</h2>
    <table>
        <thead>
            <tr style="background: #e2e8f0; color: #0f172a;">
                <th style="padding: 10px; text-align: center; width: 8%;">번호</th>
                <th style="padding: 10px; text-align: center; width: 22%;">검측 항목</th>
                <th style="padding: 10px; text-align: center; width: 55%;">정량 검측 세부 수칙 및 의결 기준</th>
                <th style="padding: 10px; text-align: center; width: 15%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">1</td>
                <td style="font-weight: bold;">참석 기관 완비</td>
                <td>발주처, 시공사, 5대 위탁기관(전력/통신/가스/난방/상하수도), 경찰서, 3D BIM 설계사 100% 참석 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">2</td>
                <td style="font-weight: bold;">3D BIM 간섭 검증</td>
                <td>시굴/GPR 탐지 결과 기반 3D BIM 렌더링으로 궤도 이격(H ≥ 1.5m) 및 3D Clash Zero 달성 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">3</td>
                <td style="font-weight: bold;">이설 순서 (Sequence)</td>
                <td>심도/위험도 순서 (깊은 하수관/수도 ➔ 전력/통신 ➔ 도시가스) 이설 순서 확정 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="font-weight: bold; text-align: center;">4</td>
                <td style="font-weight: bold;">공정 동기화 (Sync)</td>
                <td>기관별 단수/단전/정가스 일시 확정 및 궤도 구축 착수 주공정(Critical Path) 부합 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">5</td>
                <td style="font-weight: bold;">TMP 교통 처리 승인</td>
                <td>통행 차선 폭(W ≥ 3.0m) 유지, 야간 공사 및 우회 도로 계획에 대해 경찰서 교통 승인 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">6</td>
                <td style="font-weight: bold;">LCLM 채움재 합의</td>
                <td>궤도 하부 침하 예방을 위한 유동성 채움재(LCLM) 적용 범위 및 되메우기 층다짐(95% 이상) 일원화 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">7</td>
                <td style="font-weight: bold;">24시간 비상 핫라인</td>
                <td>기관별 24시간 비상 연락망 및 현장 즉시 출동 담당자 지정 완료 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">8</td>
                <td style="font-weight: bold;">선(先)협의-후(後)문서화</td>
                <td>현장 돌발 오차 발생 시 24시간 핫라인 선 협의 및 후 문서화 프로세스 승인 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">9</td>
                <td style="font-weight: bold;">Action Item 명확화</td>
                <td>"A기관 담당자가 X월 Y일까지 B문서를 제출함"과 같이 주체, 기한, 결과물 명시 서명 여부</td>
                <td class="checkbox-cell">[ ☐ 승인 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

print("Executing Complete Overwrite for Big Room HTML files based on PDF content...")

for target in target_folders:
    # 1. Standard
    sub_std = os.path.join(target, "표준서")
    if os.path.exists(sub_std):
        for f in os.listdir(sub_std):
            if f.endswith('.html'):
                fp = os.path.join(sub_std, f)
                with open(fp, 'w', encoding='utf-8') as out:
                    out.write(bigroom_pdf_std)
                print(f"  ✅ PDF-Matched Standard Overwritten: {fp}")

    # 2. Guideline
    sub_gui = os.path.join(target, "수행지침")
    if os.path.exists(sub_gui):
        for f in os.listdir(sub_gui):
            if f.endswith('.html'):
                fp = os.path.join(sub_gui, f)
                with open(fp, 'w', encoding='utf-8') as out:
                    out.write(bigroom_pdf_gui)
                print(f"  ✅ PDF-Matched Guideline Overwritten: {fp}")

    # 3. Checklist
    sub_chk = os.path.join(target, "체크리스트")
    if os.path.exists(sub_chk):
        for f in os.listdir(sub_chk):
            if f.endswith('.html'):
                fp = os.path.join(sub_chk, f)
                with open(fp, 'w', encoding='utf-8') as out:
                    out.write(bigroom_pdf_chk)
                print(f"  ✅ PDF-Matched Checklist Overwritten: {fp}")

print("🎉 Complete PDF-Based Big Room HTML Regeneration Finished!")
