import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

# Source definitions for the 3 target KOM activities
kom_custom_data = {
    "사전토공사": {
        "wbs": "9000-5-2",
        "folder": "2_발주전략 KOM",
        "title": "발주전략 KOM",
        "dept": "사전토공사 / 공무행정",
        "purpose": "사전 토공사(도로 굴착, 임시 포장 등)의 외주 협력사 선정 및 발주 시방 검토",
        "deliverable": "토공사 발주 심의서, 적격성 검토 보고서",
        "std_sum": "KCS 11 20 00 토공사 시방 및 되메우기 다짐도 95% 이상 명시. 도로 굴착 깊이 1.5m 이상 시 흙막이 지보공 설치 안전 특기 기준 적용.",
        "chk_sum": "토공사 전문면허 보유 검증, 흙막이 지보공 안전 조건 시방 반영, 하도급 적격 및 저가 심의 이행 여부",
        "specs": [
            ("하도급 입찰 자격", "건설산업기본법", "토공사업 전문건설면허 및 신용등급 BB- 이상 업체 제한"),
            ("되메우기 다짐도", "KCS 11 20 00", "최대건조밀도의 95% 이상 다짐 관리 규정 의무화"),
            ("안전 지보공 설치", "산업안전보건기준", "굴착 깊이 1.5m 이상 구간 가설 흙막이 지보공 설계 반영 검토")
        ],
        "planning": [
            "<strong>토공 설계 도면 및 수량 검토:</strong> 토공(절·성토, 사면 보호) 설계 수량을 실측하고 굴착 토사 처리용 사토장 확보 계획을 검토합니다.",
            "<strong>하도급 입찰 공고안 작성:</strong> 시방서, 특별 시방 조건, 설계 물량 내역서 및 안전 관리 특기 조항을 포함한 토공 하도급 입찰 안내서를 작성합니다."
        ],
        "execution": [
            "<strong>하도급 입찰 설명회 개최:</strong> 우수 토공 전문업체 대상 설명회를 개최하고, 도심지 도로 굴착 및 복구 시방 기준과 지장물 파손 방지 인력 굴착 조건을 안내합니다.",
            "<strong>하도급 적격 심사(85점 이상) 평가:</strong> 기술인력(토목 분야 초급 이상 2인), 굴착 장비 동원 능력, 시공 실적 및 신용 상태를 종합 심사하여 85점 이상 득점 업체를 선정합니다.",
            "<strong>하도급율(82% 이상) 저가 방지 검증:</strong> 실행예산 대비 하도급 낙찰 금액 비율이 82% 이상인지 검증하여 부실 굴착 및 사면 붕괴 예방 조치를 실현합니다.",
            "<strong>외주 심의위원회 개최 및 결재:</strong> 최저가 대조표, 지반 굴착 안전 검토서 및 하도급 심의 의결서를 첨부하여 본사 조달팀 심의 승인을 완료합니다."
        ],
        "handover": [
            "<strong>토공 하도급 계약 체결:</strong> 시방 기준, 흙막이 안전 보증서, 하자 보증 5% 및 이행 보증 증권이 첨부된 정식 하도급 표준 계약서를 체결합니다.",
            "<strong>발주처 하도급 통지 완료:</strong> 계약 체결일로부터 30일 이내에 건설산업기본법 제29조에 의거, 발주처 및 감리단에 하도급 계약 통지서를 제출합니다.",
            "<strong>현장 대리인 및 기술자 투입 승인:</strong> 계약 상대자의 현장 대리인 재직 증명, 토목 자격증 및 안전 관리자 배치서를 확인하고 현장 투입을 최종 승인합니다."
        ],
        "pre_risk": "토공사 협력업체의 도심지 도로 굴착 경험 및 장비 동원 능력 검토 누락으로 인한 시공 초기 공기 지연 리스크",
        "ing_risk": "굴착 시 주변 지하 매설 지장물 파손 방지를 위한 특기시방서 상 인력 굴착(폭 1.0m 이내) 범위 명시 누락 리스크",
        "post_risk": "계약 상대자의 하도급 통지서 제출 지연 및 안전관리 계획서 발주처 미승인 상태에서의 불법 착공 리스크"
    },
    "상부강화노반": {
        "wbs": "9000-7-2",
        "folder": "2_발주전략 KOM",
        "title": "발주전략 KOM",
        "dept": "상부강화노반 / 공무행정",
        "purpose": "상부강화노반 포설 및 다짐공사의 외주 협력사 선정 및 발주 조건 CP 적합 검토",
        "deliverable": "강화노반 하도급 심의서, 특기시방서",
        "std_sum": "롤러 조합(진동롤러, 탬핑롤러) 사양 시방 명시. K30 ≥ 110 MN/m³ 또는 Ev2 ≥ 120 MPa 정량적 품질 요건 및 시험 포설 500㎡ 시방 강제 적용.",
        "chk_sum": "강화노반 정량 품질 기준(K30, Ev2) 특기 시방 의결, 시험 포설 500㎡ 기준 수립, 하도급 적격 및 공정 조율 적정성",
        "specs": [
            ("다짐 장비 조합 요건", "KCS 47 10 25 시방", "강화노반 다짐용 진동 롤러 및 탬핑 롤러 조합 장비 사양 규정"),
            ("정량적 지지력 조건", "KDS 47 10 00 기준", "PBT 반력계수 K30 ≥ 110 MN/m³ 및 Ev2 ≥ 120 MPa, Ev2/Ev1 ≤ 2.2 강제"),
            ("시험 포설 시방 강제", "KCS 11 30 00", "본 시공 전 다짐 횟수 및 두께 결정을 위한 시험 포설 면적 500㎡ 규정")
        ],
        "planning": [
            "<strong>강화노반 설계 사양 검토:</strong> 설계 도면의 노반 두께(30cm 이하 분할), 다짐도 및 지반 지지력 설계 스펙을 분석하고 특기시방서 초안을 작성합니다.",
            "<strong>하도급 공구 분할 계획 검토:</strong> 동탄트램 전체 연장 구간의 강화노반 시공 순서에 연계하여 자재 운반 및 다짐 구역별 최적 공구 분할 계획을 수립합니다."
        ],
        "execution": [
            "<strong>하도급 입찰 설명회 개최:</strong> 지반·노반 시공 면허 보유 우수 협력사 대상 입찰 설명회를 열어 횡단 구배 2.0% 및 정밀 롤러 다짐 시방 수칙을 교육합니다.",
            "<strong>하도급 적격 심사(85점 이상) 평가:</strong> 특급/고급 토질 기술자 보유 여부, 평판재하시험(PBT) 및 PFWD 장비 보유 상태, 시공 실적을 평가하여 85점 이상 업체를 선정합니다.",
            "<strong>하도급율(82% 이상) 저가 방지 검증:</strong> 실행예산 대비 입찰 금액 비율이 82% 이상인지 검증하여 부등 침하 예방용 고품질 포설 골재 품질을 보증합니다.",
            "<strong>외주 심의위원회 개최 및 결재:</strong> 하도급 적격 심사 보고서, 시험 포설 계획서 및 외주 심의서를 첨부하여 본사 조달본부의 최종 승인을 완료합니다."
        ],
        "handover": [
            "<strong>강화노반 하도급 계약 체결:</strong> 정량 품질 요건, 양생 및 보호 조치 특기 조건, 공정표가 첨부된 정식 표준 하도급 계약서를 체결합니다.",
            "<strong>발주처 하도급 통지 완료:</strong> 계약 체결일로부터 30일 이내에 건설산업기본법에 따라 발주처 및 감리단에 하도급 통지서 및 적격 서류를 제출합니다.",
            "<strong>현장 대리인 및 기술자 투입 승인:</strong> 계약 상대자의 현장 대리인 재직 증명서 및 기술 자격자 배치서를 확인하고 현장 투입을 최종 승인합니다."
        ],
        "pre_risk": "강화노반 고유 다짐 스펙(Ev2/Ev1 ≤ 2.2) 누락 시방 배포로 인한 부실 시공 및 지반 침하 하자 리스크",
        "ing_risk": "다짐도 95% 미확보 상태의 급속 포설로 인해 노반 인계 후 후행 궤도 시공 중 노반 처짐 균열 하자 리스크",
        "post_risk": "지반 지지력(K30) 시험 성적서 발주처 제출 지연 및 감리단 노반 인수 거부에 따른 공기 지연 리스크"
    },
    "콘크리트도상": {
        "wbs": "9000-6-4",
        "folder": "4_발주전략 KOM",
        "title": "발주전략 KOM",
        "dept": "콘크리트도상 / 궤도공무",
        "purpose": "콘크리트도상 궤광 조립, 거푸집 및 타설 공사의 하도급 발주 조건 및 품질 보증 방안 수립",
        "deliverable": "궤도 하도급 심의서, 궤도 품질 특기시방서",
        "std_sum": "Track Master 등 정밀 선형 검측 장비(검교정 필증) 확보 필수 명시. 궤간 오차 +3, -1mm, 캔트/수평 오차 ±1.5mm 정밀 기하 공차 및 TCL fck ≥ 35 MPa 강제 시방 기준 의결.",
        "chk_sum": "궤도 정밀 검측 장비(Track Master) 확보 명시, 궤도 기하구조 5대 공차 기준 시방 수록, 하도급 적격 및 저가 심의 이행",
        "specs": [
            ("정밀 검측 장비 요건", "KCS 47 30 00 시방", "Track Master 등 정밀 선형 검측 장비(검교정 필증 유효) 확보 명시"),
            ("기하학 선형 공차", "KDS 47 30 20 기준", "궤간 오차 +3.0, -1.0mm 이내, 캔트/수평 오차 ±1.5mm 이내 시공 규정"),
            ("콘크리트 강도 조건", "KS F 2405 규격", "도상 콘크리트 fck ≥ 35 MPa 및 무수축 모르타르 그라우트 fck ≥ 30 MPa 강제")
        ],
        "planning": [
            "<strong>궤도 설계 도면 및 궤광 구조 검토:</strong> 1,435mm 표준궤 정밀 얼라인먼트 및 도상 콘크리트 타설 범위, 타이바 배치 사양을 검토하고 특기시방서를 작성합니다.",
            "<strong>궤도 발주 전략 수립:</strong> 외산 홈레일 조달 및 매립형 궤도 전문 기술 하도급 업체의 시공 실적 및 자격 조건을 정의하여 하도급 입찰 공고를 기획합니다."
        ],
        "execution": [
            "<strong>하도급 입찰 설명회 개최:</strong> 궤도 전문건설업 면허 보유 우수 업체 대상 설명회를 개최하여, 타설 중 게이지 모니터링 수칙 및 테르밋 용접(EN 14730) 기술 자격 요건을 안내합니다.",
            "<strong>하도급 적격 심사(85점 이상) 평가:</strong> 철도 궤도 전문 기술자 보유, 테르밋/가스 용접 자격 소지자 투입 능력, 궤도 시공 실적을 종합 심사하여 85점 이상 업체를 선정합니다.",
            "<strong>하도급율(82% 이상) 저가 방지 검증:</strong> 실행예산 대비 낙찰 가격 비율이 82% 이상인지 검증하여 정밀 궤도 선형 조정을 위한 노무비 삭감 및 부실 시공을 차단합니다.",
            "<strong>외주 심의위원회 개최 및 결재:</strong> 적격 심사 평가서, 궤도 품질 보증 계획서 및 하도급 의결서를 첨부하여 본사 공무팀 및 외주 부서 승인을 완료합니다."
        ],
        "handover": [
            "<strong>궤도 하도급 계약 체결:</strong> 정밀 기하 공차 준수 보증서, 용접 비파괴 검사(NDT 100%) 의무, 절연 저항 성적서 제출 조건이 첨부된 하도급 표준 계약서를 체결합니다.",
            "<strong>발주처 하도급 통지 완료:</strong> 계약 체결일로부터 30일 이내에 감리단 및 발주처에 하도급 통지서 및 궤도 품질 보증 계획서를 제출합니다.",
            "<strong>현장 대리인 및 기술자 투입 승인:</strong> 계약 상대자의 현장 대리인 재직 증명서 및 궤도 자격증을 확인하고 현장 투입을 최종 승인합니다."
        ],
        "pre_risk": "정밀 궤도 선형 검측 장비 검교정 요건 누락으로 시공 중 누적 궤도 틀림(오차 한계선 초과) 하자 리스크",
        "ing_risk": "도상 콘크리트 타설 시 측압에 따른 궤광 변위 방지용 고정 지지 잭(Jack) 자재 조달 미비로 궤도 뒤틀림 리스크",
        "post_risk": "완성선 궤도 절연 저항(R ≥ 100 MΩ) 성적서 누락에 의한 후행 전기/신호 연계 시험 인수인계 차단 리스크"
    }
}

for parent_folder, data in kom_custom_data.items():
    wbs = data["wbs"]
    folder = data["folder"]
    title = data["title"]
    dept = data["dept"]
    purpose = data["purpose"]
    deliverable = data["deliverable"]
    std_sum = data["std_sum"]
    chk_sum = data["chk_sum"]
    
    parent_path = os.path.join(base_dir, parent_folder, folder)
    std_dir = os.path.join(parent_path, "표준서")
    chk_dir = os.path.join(parent_path, "체크리스트")
    guide_dir = os.path.join(parent_path, "수행지침")
    
    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)
    os.makedirs(guide_dir, exist_ok=True)

    # Re-render specs table rows for standard
    specs_rows = ""
    for name, standard, spec in data["specs"]:
        specs_rows += f"""                <tr>
                    <td style="font-weight: bold; text-align: center;">{name}</td>
                    <td style="text-align: center;">{standard}</td>
                    <td>• {spec}</td>
                </tr>\n"""

    # 1. Standard HTML Rebuild
    std_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{parent_folder} - {title} 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS {wbs} Standard</div>
        <h1 class="title">{title} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> {dept}</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공무팀 / 외주팀</span>
            <span>|</span>
            <span><span class="badge">현장 맞춤 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>{purpose}</td></tr>
            <tr><th>산출물 (결과)</th><td>{deliverable}</td></tr>
            <tr><th>표준서 (Standard) 요약</th><td>{std_sum}</td></tr>
            <tr><th>관련 시방 기준</th><td>건설산업기본법, 하도급 거래 공정화에 관한 법률, 동탄트램 특별시방서</td></tr>
        </tbody>
    </table>

    <h2>2. {title} 고유 정량 공학 시방 및 기술 수칙 표</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">📐 {title} 정량적 하도급 심사 및 발주 품질 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">기술 검속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 법규 및 기준</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 50%;">핵심 정량 기술 수칙 및 발주 요건</th>
                </tr>
            </thead>
            <tbody>
{specs_rows}            </tbody>
        </table>
    </div>

    <h2>3. {title} 핵심 프로세스 및 구조 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">{parent_folder} {title} 발주 행정 프로세스</text>

            <g transform="translate(50, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e1b4b">① 사전 준비 및 입찰 기획</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 하도급 입찰 시방 특별조건 수립</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 공구 분할 및 실행 내역 검토</text>
            </g>

            <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

            <g transform="translate(340, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">{title}설명회 및 적격심사</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 적격 심사 종합 평가 85점 이상</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 저가 심의(하도급율 82% 이상)</text>
            </g>

            <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

            <g transform="translate(630, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">③ 계약 체결 및 발주처 통지</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 표준 계약 체결 및 보증 증권 징구</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 30일 이내 감리단/발주처 통지</text>
            </g>

            <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
            <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">🚨 하도급 통지 기한(30일) 미준수 및 부적합 업체 계약 강행 시 행정 제재 조치</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <strong>💡 프로세스 주요 설명:</strong><br>
        1. <strong>입찰 시방 특별조항 수립:</strong> 계약 전 관련 핵심 시방 규격(KCS/KDS)에 명시된 정량 기준과 안전 수칙을 하도급 특기 조항으로 명문화합니다.<br>
        2. <strong>적격 심사 및 하도급율 검증:</strong> 전문 기술인 확보, 시공 실적 및 신용 한도를 심사하고 부실 시공 방지를 위해 하도급율 82% 이상 기준을 엄격히 적용합니다.<br>
        3. <strong>행정 신고 완료:</strong> 하도급 계약 후 30일 이내에 법정 통지 서류를 지체 없이 발주처 및 감리단에 보고 완료합니다.
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> {parent_folder} 공사의 발주 전략 수립은 적격 하도급사를 선정하고 품질/안전 위해 리스크를 계약 단계에서 선제 차단하기 위한 필수 행정 절차입니다.
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS {wbs} | {parent_folder}
    </div>
</div>
</body>
</html>"""

    std_fp = os.path.join(std_dir, f"{folder}_표준서.html")
    with open(std_fp, 'w', encoding='utf-8') as f:
        f.write(std_html)

    # 2. Guideline HTML Rebuild
    planning_list = "".join([f"            <li>{item}</li>" for item in data["planning"]])
    execution_list = "".join([f"            <li>{item}</li>" for item in data["execution"]])
    handover_list = "".join([f"            <li>{item}</li>" for item in data["handover"]])

    guide_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{parent_folder} - {title} 수행지침서</title>
    <style>
        :root {{ --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #cbd5e1; }}
        body {{ font-family: 'Pretendard', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; background: var(--bg-card); padding: 35px; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .header {{ border-bottom: 2px solid var(--text-primary); padding-bottom: 15px; margin-bottom: 25px; }}
        .title {{ font-size: 1.8rem; font-weight: 800; margin: 0; color: var(--accent-blue); }}
        .meta {{ font-size: 0.9rem; color: var(--text-secondary); margin-top: 8px; }}
        .card {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
        .card-header {{ font-size: 1.15rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
        .bullet-list {{ list-style-type: none; padding-left: 0; margin: 0; }}
        .bullet-list li {{ position: relative; padding-left: 20px; margin-bottom: 12px; font-size: 0.92rem; color: #334155; }}
        .bullet-list li::before {{ content: "•"; position: absolute; left: 0; top: 0; color: var(--accent-cyan); font-weight: bold; font-size: 1.2rem; }}
        .footer-note {{ text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">{parent_folder} - {title} 현장 수행지침서</h1>
        <div class="meta">WBS Code {wbs} | 공무행정 및 조달 관리 프로세스</div>
    </div>

    <div class="card" style="border-left: 6px solid #1e3a8a;">
        <div class="card-header" style="color: #1e3a8a;">① 사전 준비 및 계획 검토 단계 (Planning & Preparation)</div>
        <ul class="bullet-list">
{planning_list}        </ul>
    </div>

    <div class="card" style="border-left: 6px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 본 시공 및 정밀 실행 단계 (Execution & Quality Assurance)</div>
        <ul class="bullet-list">
{execution_list}        </ul>
    </div>

    <div class="card" style="border-left: 6px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 검사, 준공 승인 및 이관 단계 (Sign-off & Handover)</div>
        <ul class="bullet-list">
{handover_list}        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS {wbs} | {parent_folder}
    </div>
</div>
</body>
</html>"""

    guide_fp = os.path.join(guide_dir, f"{folder}_수행지침.html")
    with open(guide_fp, 'w', encoding='utf-8') as f:
        f.write(guide_html)

    # 3. Checklist HTML Rebuild
    pre_r = data["pre_risk"]
    ing_r = data["ing_risk"]
    post_r = data["post_risk"]

    chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{parent_folder} - {title} 리스크 체크리스트</title>
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
        <span class="meta">WBS Code {wbs} | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">{chk_sum}</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[조달/기획 리스크]</strong> {pre_r}</div>
                    <div style="margin-bottom: 8px;">• <strong>[입찰 시방 검토]</strong> 하도급 계약 설계 도면 및 공구 분할 내역 정확성 대조 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[부실 시공 예방]</strong> {ing_r}</div>
                    <div style="margin-bottom: 8px;">• <strong>[단가 덤핑 차단]</strong> 하도급율 82% 저가 방지 검증 이행 및 적격 평가 85점 이상 충족 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[행정 위반 리스크]</strong> {post_r}</div>
                    <div style="margin-bottom: 8px;">• <strong>[기술진 배치 검속]</strong> 하도급 계약일로부터 30일 이내 발주처 보고 및 현장대리인 투입 승인 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | {parent_folder}
    </div>
</div>
</body>
</html>"""

    chk_fp = os.path.join(chk_dir, f"{folder}_체크리스트.html")
    with open(chk_fp, 'w', encoding='utf-8') as f:
        f.write(chk_html)

    print(f"🎉 Fully Rebuilt and Customized KOM Files for '{parent_folder}' (WBS {wbs}).")

print("\n🎉 Rebuilding all specified KOM HTML files completed successfully!")
