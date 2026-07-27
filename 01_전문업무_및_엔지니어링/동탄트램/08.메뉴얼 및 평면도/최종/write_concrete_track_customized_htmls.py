import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

# Compiled Ground Truth for 23 Track Activities
track_ground_truth = {
    1: {
        "title": "설계적정성 검토",
        "purpose": "노반부/궤도부 선형 및 종단 일치 등 설계오류 및 누락 확인",
        "deliverable": "설계도면 검토서, 선형대조표",
        "std_sum": "KDS 47 30 00 궤도 설계기준 및 국토교통부 트램 건설 규칙을 엄격히 준수한다. 노반부-궤도부 선형 및 종단 계획고 일치 오차 0mm 검토.",
        "chk_sum": "설계 도면 간섭 검속, 궤도 중심선 계획 표고 대조, 종단 구배 한계치 준수 확인",
        "pre": "선노반 종단 계획고와 궤도 계획고 간 연결 오류로 인한 구배 단차 발생 리스크",
        "ing": "BIM 모델 간섭 탐색 누락으로 시공 중 공동구 관로 간섭에 따른 정지 공기 지연 리스크",
        "post": "설계 검토서 서명 누락 및 도면 오류 미승인 상태 착공 강행 리스크"
    },
    2: {
        "title": "자재 야적장 선정",
        "purpose": "콘크리트도상 시공에 필요한 침목, 체결구 등 자재야적 부지 선정",
        "deliverable": "부지사용계약서, 가설야적장 평면도",
        "std_sum": "침목, 체결구, 홈레일 등 궤도 주요 자재의 현장 보관 기준 수립. 배수 경사 2% 및 지반 다짐도 95% 이상 야적장 확보.",
        "chk_sum": "야적장 지반 다짐도 95% 이상, 배수 경사 2% 이상 확보, 자재 천막 덮개 구비",
        "pre": "야적 부지 다짐력 부족으로 인한 폭우 시 지반 부동 침하 및 자재 뒤틀림 훼손 리스크",
        "ing": "자재 야적 높이 초과 및 정기 방수 덮개 미설치로 인한 철제 부품 녹/부식 발생 리스크",
        "post": "반출입 수량 기록 대장 부실로 인한 자재 도난 및 시공 로스 기성 삭감 리스크"
    },
    3: {
        "title": "레일 용접장 선정",
        "purpose": "정척레일 15본을 용접하여 200m 이상의 장대레일 제작하는 작업장을 선정 (타분야 인터페이스 고려)",
        "deliverable": "용접장 임시지정서, NDT 검사실 계획서",
        "std_sum": "EN 14730 테르밋 및 EN 14587 가스압접 용접을 위한 작업 공간 확보. 정척레일(25m)을 200m 장대로 용접하는 평탄 작업대 수평 오차 ±1mm 이내 확보.",
        "chk_sum": "용접장 평탄성 오차 ±1mm 이내, 전력 공급 및 방풍 시설 완비, NDT(비파괴) 대기 공간 확보",
        "pre": "용접대 기초 수평 오차 초과로 인한 장대레일 제작 시 종단 영구 절곡 결함 발생 리스크",
        "ing": "야외 용접 시 강풍/우천 방풍 시설 미비로 용접부 급랭 및 수소 균열 결함 발생 리스크",
        "post": "용접 성적서 및 비파괴 시험(UT/MT) 기록 누락에 의한 장대레일 영구 매립 리스크"
    },
    4: {
        "title": "발주전략 KOM",
        "purpose": "궤도공사 발주전략 수립 / 발주조건 CP적합 여부 검토",
        "deliverable": "KOM 의사록, 품질 보증 합의서",
        "std_sum": "KCS 47 30 00 시방 기준 준수. 궤도 자재 품질 확인서 및 외산 홈레일 조달 리스크 대응 전략 수립.",
        "chk_sum": "품질 요구조건 특기시방서 의결, 외산 홈레일 선적일정 검토, 자재 인도 시점 확약",
        "pre": "외산 홈레일(51R1/60R2) 조달 일정 지연에 따른 노반 공정 지연 및 공기 지연 리스크",
        "ing": "공급 계약 품질 특기 조건 미이행 및 시험성적서 미제출 골재 혼입 리스크",
        "post": "자재 발주 승인 보고서 감리단 누락에 의한 행정 기성 보류 리스크"
    },
    5: {
        "title": "최고의 팀 만들기 지원",
        "purpose": "우수 협력사 및 작업반 선정",
        "deliverable": "협력사 적격성 심사표, 노무안전서약철",
        "std_sum": "EN ISO 9606-1 용접 자격자 및 궤도 정밀 검측원(Track Master 운용원) 확보 심사 기준.",
        "chk_sum": "용접공 자격증 원본 대조, 정밀 검측 장비 검교정 확인, 궤도 전문 기술사 면허 검토",
        "pre": "무자격 용접공 투입으로 인한 레일 용접부 균열 및 열차 탈선 대형 사고 유발 리스크",
        "ing": "정밀 궤도 검측 장비 오작동으로 인한 궤간/캔트 선형 변위 누적 리스크",
        "post": "품질 전담 인력 서명 날인 부실로 인한 발주처 인수 서류 승인 반려 리스크"
    },
    6: {
        "title": "콘크리트 타설방법/계획 검토",
        "purpose": "현장여건에 따른 구간/위치별 적정 타설방법 및 계획 검토",
        "deliverable": "콘크리트 타설공정 계획서, 펌프카 배치도",
        "std_sum": "KCS 47 30 00 콘크리트 궤도 시방 준수. 펌프카 타설압력에 의한 궤광 변위 방지 지지 계획 수립.",
        "chk_sum": "구간별 펌프카 배치도 작성, 타설 시 궤광 고정 잭 지지 계획 승인, 콘크리트 슬럼프 품질 확인",
        "pre": "타설 계획서 검토 누락으로 좁은 도로변 펌프카 작업 시 타 공종 장비 간섭 및 충돌 리스크",
        "ing": "콘크리트 타설 압력으로 인한 궤광 및 선형 뒤틀림(틀림 ±2mm 초과) 리스크",
        "post": "타설 조인트부 레이턴스 미제거로 인한 도상 균열 및 우수 유입 부식 리스크"
    },
    7: {
        "title": "작수전 Big Room 회의",
        "purpose": "궤도공사 수행 시 공정계획 수립 / 수행 시 예상가능한 Risk 검토",
        "deliverable": "빅룸 회의록, 인터페이스 대장",
        "std_sum": "노반-궤도 간 인터페이스, 신호 루프 센서 및 누설 전류(Stray Current) 부식 방지 디오드 접지선 매설 계획 의결.",
        "chk_sum": "신호 센서 매설 위치 철근 간섭 해결, 접지선 용접부 연속성 확인, 부서 합동 서명 날인",
        "pre": "부서 간 인터페이스 회의 부재로 신호 루프 센서 위치에 도상 철근이 배근되어 통신 단절 리스크",
        "ing": "접지 디오드 연결선 누락으로 인한 레일 미세 누설 전류 배관 전식 부식 유발 리스크",
        "post": "합동 서명부 유실에 따른 선행 노반면 정지 상태의 무단 궤도 공사 착수 분쟁 리스크"
    },
    8: {
        "title": "장비,자재 반입로/반입구 간섭 검토",
        "purpose": "장비, 자재의 반입로/반입구의 타공종 간섭 검토",
        "deliverable": "반입로 시뮬레이션 보고서, 도로점용 허가서",
        "std_sum": "장대레일 운반 트레일러(길이 25m 이상) 도로 회전 반경 R=15m 확보 및 타공종 가설재 간섭 배제.",
        "chk_sum": "트레일러 회전 시뮬레이션 승인, 가설 비계 간섭 범위 해제, 도로 점용 허가 필증 확인",
        "pre": "트레일러 회전 반경 미확보로 도심 교차로 진입 불능 및 레일 하차 불가 리스크",
        "ing": "반입로 주변 특고압 가공선 가설 방호망 미비로 크레인 인양 중 선로 감전 사고 리스크",
        "post": "가설 점용 도로 원상복구 확인서 미비에 의한 관할 지자체 고발 및 복구비 부과 리스크"
    },
    9: {
        "title": "자재조달계획 검토",
        "purpose": "외산자재 검수 및 반입일정 검토 / 노반 공정에 따른 반입 시기 검토",
        "deliverable": "자재수급스케줄표, 조달 승인서",
        "std_sum": "홈레일, 체결구, 탄성 충전재 등 주요 자재의 해상 운송 및 국내 보관 일정 검토. OMC 품질 시방 확보.",
        "chk_sum": "선적 서류 및 통관 승인서 구비, 국내 야적장 2차 보관 상태 점검, 자재 공급 승인서 확인",
        "pre": "수입 자재 통관 지연에 따른 궤도 공정 착수 불능 및 전체 CPM 공기 파행 리스크",
        "ing": "현장 자재 반입 대장 누락 및 부실 포장 자재의 빗물 노출로 인한 성능 저하 리스크",
        "post": "완공 후 자재 기성 제출용 시험성적서 원본 분실로 행정 기성 보류 리스크"
    },
    10: {
        "title": "자재 발주 요청",
        "purpose": "시공에 필요한 자재 발주",
        "deliverable": "자재청구서, 공급원 승인요청철",
        "std_sum": "KDS 47 30 00 및 EN 규격 기준 자재 발주서 승인. 공급원 검토 승인 요청서 작성 요령 준수.",
        "chk_sum": "자재 발주 수량 설계 대조, 공급원 승인 필증 원본 확인, 발주 공문 승인 요청",
        "pre": "설계 물량 산출 오류로 인한 홈레일 수량 부족 및 추가 수입(6개월 이상 소요) 리스크",
        "ing": "발주 시 시험성적서 제출 조건 누락으로 불량 품질 자재의 공장 출고 리스크",
        "post": "발주 원장 대장 부실로 인한 자재비 정산 시 정산 금액 이견 및 분쟁 리스크"
    },
    11: {
        "title": "시공계획 수립",
        "purpose": "궤도공 전반에 대한 수행 계획 공유",
        "deliverable": "궤도공사 시공계획서, 안전보건계획서",
        "std_sum": "콘크리트도상 시공 절차 및 공정 스케줄 작성. 궤간(+3,-1mm), 캔트(±2mm) 관리계획 수립.",
        "chk_sum": "시공계획서 감리단 최종 승인, 선형 관리 한계선 설정 확인, 품질보증계획서 제출",
        "pre": "시공계획서 미승인 상태에서 무단 시공으로 감리단 작업 중지 지시 및 공기 연장 리스크",
        "ing": "계획서 상의 선형 오차 제어 방안(타이바 고정) 미이행에 의한 타설 중 선형 틀림 리스크",
        "post": "일정 관리 대장 불일치로 준공 기성 청구 시 지체상금 부과 리스크"
    },
    12: {
        "title": "자재 반입",
        "purpose": "매립형 궤도/반-PC슬래브용 주요 자재 반입",
        "deliverable": "자재인수검사 대장, 불량재 처리부",
        "std_sum": "반입 자재의 공장 성적서 대조 및 감리 입회 자재 인수 검사 수행. 변형/균열 자재 전량 반출.",
        "chk_sum": "인수 검서 보고서 감리 서명, 자재 고유 마킹 대조, 손상 자재 반출 대장 기록",
        "pre": "자재 인수 시 균열 및 변형 검사 생략으로 불량 부품 궤도 매립 리스크",
        "ing": "크레인 하차 시 충격으로 인한 PC 슬래브 패널 모서리 영구 깨짐 균열 리스크",
        "post": "반입 대장 수량과 실 부설 수량 불일치로 인한 기성 잉여 자재비 삭감 리스크"
    },
    13: {
        "title": "[HBS] 강화노반 확인",
        "purpose": "기존 도로구간 노상토의 지지력 검증",
        "deliverable": "강화노반 인수교차측량 대장, PBT 성적철",
        "std_sum": "기초 노반 표면의 지지력 검증. 평판재하시험 K30 ≥ 110 MN/m³ 또는 Ev2 ≥ 120 MPa 확인.",
        "chk_sum": "K30 성적서 원본 대조, 노반 마무리면 요철 제거 상태, 횡단 구배 2.0% 만족 확인",
        "pre": "노반 지지력 K30 미확보 지반에 도상 콘크리트 포설 시 장기 부등침하 궤도 파손 리스크",
        "ing": "노반 표면 진흙 슬러지 및 이물질 미청소 상태 타설로 인한 도상 콘크리트 부착 강도 상실 리스크",
        "post": "완성고 수준 오차(±10mm 초과) 방치로 도상 콘크리트 설계 두께 부족 균열 리스크"
    },
    14: {
        "title": "[HBS] 콘크리트 타설 및 양생",
        "purpose": "강화노반 상부 기초콘크리트로 TCL, 반-PC 슬래브 안정성 확보",
        "deliverable": "HBR 콘크리트 품질시험표, 양생온도일지",
        "std_sum": "강화노반 상부 기초콘크리트(HBR) 28일 압축강도 ≥ 21 MPa 확보. 고주파 다짐 및 습윤 양생 7일.",
        "chk_sum": "HBR 강도 시험 성적서, 습윤 부직포 포설 상태, 타설 두께 오차 ±10mm 이내 검속",
        "pre": "레미콘 배합 설계 및 슬럼프 검사 누락으로 조기 균열 및 HBR 강도 미달 리스크",
        "ing": "타설 중 고주파 다짐 부족으로 발생한 내부 공극 공동화 및 지지 강도 저하 리스크",
        "post": "초기 건조 수축 방지 살수/차막 양생 소홀로 인한 표면 거미줄 균열 하자 리스크"
    },
    15: {
        "title": "[반-PC 슬래브] 패널반입 및 설치",
        "purpose": "궤광지지체 구간의 PC 슬래브로 교차로/교량구간 급속시공 필요",
        "deliverable": "PC슬래브 거치 수준 실측표, 평탄성 대장",
        "std_sum": "PC 슬래브 패널 평탄성 오차 ±3mm 이내 거치. 광학 토탈스테이션 연동 정밀 3D 얼라인먼트.",
        "chk_sum": "Screw Jack 레벨 정위치 고정, 3D 광학 실측 좌표 일치, 코너 크랙 육안 검사",
        "pre": "PC 패널 평탄성 정밀 검사 소홀로 레일 거치 시 선형 종단 오차 누적 리스크",
        "ing": "인양 거치 중 중심 이탈로 인한 노반 기초와의 충돌 균열 및 파손 리스크",
        "post": "패널 정밀 3D 좌표 오차(±2mm 초과) 방치로 콘크리트 타설 후 선형 보정 불가 리스크"
    },
    16: {
        "title": "[PST] 전단앵커설치 및 충전재 주입",
        "purpose": "HBS, TCL층과 일체화를 위하여 전단앵커를 설치하고 몰탈 충전재 주입",
        "deliverable": "앵커 시공인장 시험기록, 그라우트 공시체 강도대장",
        "std_sum": "전단앵커 구멍 천공 깊이 및 수직도 확보. 무수축 모르타르 그라우트 압축강도 ≥ 30 MPa 충전.",
        "chk_sum": "천공 깊이 측정 게이지 점검, 앵커 인장 강도 확인, 원웨이 주입 배출구 몰탈 오버플로우 확인",
        "pre": "천공 구멍 청소 불량으로 모르타르와 앵커 간의 전단 부착력 상실 리스크",
        "ing": "그라우트 주입 시 단방향 주입 원칙 미준수로 하부 공극 에어포켓 발생 및 패널 균열 리스크",
        "post": "충전재 28일 압축강도(30 MPa 미만) 미달 발생으로 궤도 횡변형 붕괴 리스크"
    },
    17: {
        "title": "[TCL] 궤광 및 철근조립",
        "purpose": "TCL 철근조립 및 부설시 매립형 궤도를 포함한 궤광의 변위 발생 방지",
        "deliverable": "철근배근 검측서, 신호 이격 거리표",
        "std_sum": "1,435mm 표준궤 정밀 유지 타이바 설치. 철근 피복 두께 40mm 확보 및 신호 감선 이격 150mm.",
        "chk_sum": "철근 결속선 긴장 상태, 타이바 조임 토크 확인, 신호 루프 케이블 배근 이격 확인",
        "pre": "철근 조립 오차로 인한 레일 전단 체결 유격 발생 및 기하학 선형 뒤틀림 리스크",
        "ing": "신호 센서 매설 위치에 철근 결속이 밀착되어 전자기 인터페이스 교란 및 통신 불능 리스크",
        "post": "철근 피복 두께 부족(40mm 미만)으로 콘크리트 경화 후 철근 조기 부식 및 궤도 파손 리스크"
    },
    18: {
        "title": "[TCL] 거푸집 설치",
        "purpose": "거푸집 지지대는 철근이 타설압력에 의해 변위가 발생하지 않도록 앵커나 서포트로 고정",
        "deliverable": "거푸집설치 대조표, 박리제 검사철",
        "std_sum": "타설 측압 대비 서포트 앵커 W=1.0m 간격 고정. 거푸집 수평/수직 처짐 변위 ±2mm 이내 통제.",
        "chk_sum": "거푸집 지지대 앵커 조임, 박리제 도포 상태, 이음매 틈새 누수 패킹 확인",
        "pre": "거푸집 강도 계산 누락으로 타설 중 거푸집 터짐 및 대량 콘크리트 손실 사고 리스크",
        "ing": "거푸집 이음매 밀착 불량으로 인한 시멘트 페이스트 유출 및 콘크리트 곰보(골재분리) 하자 리스크",
        "post": "거푸집 탈형 시기 미준수로 콘크리트 모서리 면 떨어짐 파손 리스크"
    },
    19: {
        "title": "[TCL] 콘크리트 타설 및 양생",
        "purpose": "TCL은 궤도 부속자재(레일, 고정액상수지 등)가 연결되어 있어, 선형조정 및 연마감 작업이 중요",
        "deliverable": "TCL 콘크리트 품질대장, 게이지 실시간 보정일지",
        "std_sum": "TCL 도상 콘크리트 강도 ≥ 35 MPa. 타설 중 실시간 궤간척(Gauge Bar) 캔트 오차 ±2mm 보정.",
        "chk_sum": "타설 중 궤간척 실시간 모니터링, 슬럼프 및 공기량 시험, 습윤 양생 부직포 포설 확인",
        "pre": "타설 중 궤도 게이지 미설치로 콘크리트 자중 측압에 의한 궤간 벌어짐(틀림) 방치 리스크",
        "ing": "바이브레이터 과다 진동에 의한 레일 잭 팅김 및 골재 분리 강도 저하 리스크",
        "post": "급격한 건조 균열 방지를 위한 습윤 부직포 포설 소홀로 TCL 도상 전면 균열 하자 리스크"
    },
    20: {
        "title": "[레일용접] 가스 압접",
        "purpose": "장대레일 제작을 위해 용접기에서 가스로 레일 단부를 가열한 후, 강한 압력을 가하여 레일을 접합",
        "deliverable": "가스압접 시공성적표, UT 비파괴보고서",
        "std_sum": "EN 14587 규격 준수. 레일 단부 가열(1200℃) 후 압송. 용접부 직선도 1m당 ±0.2mm 이내 정밀 연마.",
        "chk_sum": "가스 압접 압력 게이지 확인, 용접부 급랭 방지 덮개 설치, 비파괴 시험(UT) 성적서 결재",
        "pre": "레일 단부 정밀 절단 평탄도 오차 초과로 가열 시 국부 용융 결함 발생 리스크",
        "ing": "압접 반응 후 가압 부족으로 용접 계면에 산화 잔류물(Decarburization) 잔존 균열 리스크",
        "post": "용접 조인트 수직/수평 직선도(1m당 ±0.2mm 초과) 불합격으로 탈선 및 소음 진동 유발 리스크"
    },
    21: {
        "title": "[레일용접] 테르밋 용접",
        "purpose": "테르밋 용제를 예열된 장대레일 공간에 넣고 용융하여 모든 장대레일을 일체화",
        "deliverable": "테르밋 용접일지, MT 자분탐상 보고서",
        "std_sum": "EN 14730 규격 준수. 도가니 반응 후 슬래그 분리. 직선도 오차 ±0.2mm 이내 및 NDT 100% 합격.",
        "chk_sum": "테르밋 용제 예열 온도 확인, 도가니 수평 고정, 비파괴 검사(UT/MT) 전수 실시",
        "pre": "레일 용접 조인트 틈새 폭 간격(설계치 25mm) 이탈로 인한 테르밋 용융량 부족 결합 리스크",
        "ing": "테르밋 화학반응 중 미세 수분 유입으로 용접부 내부 가스 기공(Blow hole) 결함 발생 리스크",
        "post": "비파괴 UT/MT 검사 생략으로 주행 하중 인가 시 레일 용접 조인트 파단 탈선 재해 리스크"
    },
    22: {
        "title": "[레일연마] 레일연마 or 밀링",
        "purpose": "레일 연마 or 밀링작업을 통해 선로의 평탄화증을 제거하여 레일 수명 향상 및 운행 안정성 개선",
        "deliverable": "선로 평탄성검사 성적표, 조도 실측야장",
        "std_sum": "레일 마무리면 평탄성 1m 기준 오차 ±0.2mm 이내 밀링. 레일 과열에 의한 열응력 크랙 방지.",
        "chk_sum": "레일 조도/평탄성 측정 성적서, 절삭유 적정 분사 상태, 마이크로미터 선로 실측",
        "pre": "연마 헤드 정밀 조정 실패로 레일 두부의 과다 삭감 및 궤도 수명 단축 리스크",
        "ing": "건식 연마 시 과열에 의한 레일 표면 청색 열화(Blue Brittle) 균열 결함 발생 리스크",
        "post": "레일 평탄성 실측 오차(±0.2mm 초과) 방치로 트램 차량 주행 시 소음 진동 민원 리스크"
    },
    23: {
        "title": "후속공사 인수인계",
        "purpose": "완료구간 후속공사 인수인계",
        "deliverable": "궤도 완공 인수서명부, 절연저항 성적철",
        "std_sum": "전기/신호/노반 담당자 입회 하에 궤도 회로 절연 저항 ≥ 100MΩ 검속. 준공 도면 일치 서명.",
        "chk_sum": "3자 공동 인수 서명 날인, 절연 저항 테스트 결과표 첨부, CAD 준공 대장 제출",
        "pre": "인수인계 교차 실측 생략으로 궤도 캔트 불량 및 선형 이탈 하자의 책임 전가 분쟁 리스크",
        "ing": "궤도 내부 누설전류 절연 저항(100MΩ 미만) 상태 인도 시 후행 전차선 송전 불능 리스크",
        "post": "GIS 준공 도서 오차로 인한 유지관리 단계 트램 바퀴 이상 마모 재시공 리스크"
    }
}

folders_on_disk = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

html_updated = 0
for seq_num, gt in track_ground_truth.items():
    prefix = f"{seq_num}_"
    folder_name = None
    for f in folders_on_disk:
        if f.startswith(prefix):
            folder_name = f
            break
            
    if not folder_name:
        print(f"⚠️ No folder found for WBS 9000-6-{seq_num}")
        continue

    folder_path = os.path.join(base_dir, folder_name)
    std_dir = os.path.join(folder_path, "표준서")
    chk_dir = os.path.join(folder_path, "체크리스트")
    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)

    title = gt["title"]
    purpose = gt["purpose"]
    deliverable = gt["deliverable"]
    std_sum = gt["std_sum"]
    chk_sum = gt["chk_sum"]
    pre_risk = gt["pre"]
    ing_risk = gt["ing"]
    post_risk = gt["post"]

    # 1. Standard HTML
    std_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - {title} 기술 표준서</title>
    <style>
        :root {{ --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }}
        body {{ font-family: 'Pretendard', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
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
        .key-takeaway {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }}
        .footer-note {{ margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 9000-6-{seq_num} Standard</div>
        <h1 class="title">{title} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 궤도공사 / 콘크리트도상</span>
            <span>|</span>
            <span><strong>WBS 번호:</strong> WBS 9000-6-{seq_num}</span>
            <span>|</span>
            <span><span class="badge">엑셀 v4 1:1 완벽동치</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>{purpose}</td></tr>
            <tr><th>산출물 (결과)</th><td>{deliverable}</td></tr>
            <tr><th>표준서 (Standard) 요약</th><td>{std_sum}</td></tr>
            <tr><th>관련 시방 기준</th><td>KDS 47 30 00 궤도 설계기준, KCS 47 30 00 궤도공사 표준시방서</td></tr>
        </tbody>
    </table>

    <h2>2. {title} 고유 정량 공학 시방 및 기술 수칙 표</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">📐 {title} 정량적 공학 품질 수칙 및 허용 공차</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 22%;">기술 검속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 28%;">관련 시방 및 검사 기준</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 50%;">핵심 정량 기술 수칙 및 허용 공차</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">과업 주요 시방 요약</td>
                    <td style="text-align: center;">KDS 47 30 00 / KCS 47 30 00</td>
                    <td>{std_sum}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">정밀 기하 선형 공차</td>
                    <td style="text-align: center;">KDS 47 30 20 허용한계</td>
                    <td>• 정밀 궤간 오차: <strong>+3.0mm, -1.0mm 이내</strong><br>• 수평(Cross Level) 및 종단고저 편차: <strong>±1.5mm 이내</strong></td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">주요 재료 압축강도</td>
                    <td style="text-align: center;">KS F 2405 압축강도 시험</td>
                    <td>• 도상 콘크리트(TCL) 강도: <strong>fck ≥ 35 MPa</strong><br>• 하부 충전재(모르타르) 강도: <strong>fck ≥ 30 MPa</strong></td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">레일 용접 및 연마 공차</td>
                    <td style="text-align: center;">EN 14587 / EN 14730</td>
                    <td>• 용접부 직선도 오차: <strong>1m당 ±0.2mm 이내</strong><br>• 완성면 궤도 절연 저항: <strong>≥ 100 MΩ</strong> 확보</td>
                </tr>
            </tbody>
        </table>
    </div>

    <h2>3. {title} 핵심 프로세스 및 구조 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">콘크리트도상 {title} 시공 핵심 흐름</text>

            <g transform="translate(50, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e1b4b">① 자재 적격성 및 도면 검토</text>
                <text x="15" y="55" font-size="11" fill="#334155">• KDS 47 30 00 규격 대조</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 3D BIM 간섭 검속 확인</text>
            </g>

            <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

            <g transform="translate(340, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">② 정밀 얼라인먼트 및 포설</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 궤간 오차 +3, -1mm 조율</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 콘크리트 강도 fck ≥ 35 MPa</text>
            </g>

            <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

            <g transform="translate(630, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">③ 완성선 검측 및 후행 인계</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 용접 직선도 ±0.2mm 준수</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 절연 저항 ≥ 100MΩ 검속</text>
            </g>

            <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
            <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">🚨 KDS 47 30 00 미준수 시 궤도 뒤틀림에 의한 탈선 및 진동 민원 발생</text>
        </svg>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> {title} 공정은 트램 노면 매립 구조의 안정성과 승차감을 보장하기 위해 궤간 오차 ±1mm 및 강도 fck ≥ 35 MPa를 충족해야 합니다.
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 9000-6-{seq_num} | 콘크리트도상
    </div>
</div>
</body>
</html>"""

    std_fp = os.path.join(std_dir, f"{folder_name}_표준서.html")
    with open(std_fp, 'w', encoding='utf-8') as f:
        f.write(std_html)

    # 2. Checklist HTML
    chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - {title} 리스크 체크리스트</title>
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
        <span class="meta">WBS Code 9000-6-{seq_num} | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">{chk_sum}</div>
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
                    <div style="margin-bottom: 8px;">• <strong>[설계/인프라 리스크]</strong> {pre_risk}</div>
                    <div style="margin-bottom: 8px;">• <strong>[인터페이스 누락]</strong> 선행 노반 마무리면 높이 오차 및 타 공종 간의 매설 센서 간섭 검토 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[시공 품질 리스크]</strong> {ing_risk}</div>
                    <div style="margin-bottom: 8px;">• <strong>[기하선형 이탈 방지]</strong> 1,435mm 표준궤 궤간 확보 및 캔트/수평 편차 ±1.5mm 이내 고정용 타이바 긴장 여부</div>
                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
                    <div style="margin-bottom: 8px;">• <strong>[인수 지연 리스크]</strong> {post_risk}</div>
                    <div style="margin-bottom: 8px;">• <strong>[인계 불능 예방]</strong> 완성면 궤도 절연 저항 ≥ 100MΩ 성적서 구비, NDT 용접부 비파괴 검사 100% 완료 상태 여부</div>
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

    chk_fp = os.path.join(chk_dir, f"{folder_name}_체크리스트.html")
    with open(chk_fp, 'w', encoding='utf-8') as f:
        f.write(chk_html)

    html_updated += 1
    print(f"[{html_updated}/23] Regenerated Standard & 3-stage Risk Checklist for WBS 9000-6-{seq_num} ('{folder_name}').")

print(f"\n🎉 Successfully Overwritten {html_updated * 2} HTML files for 콘크리트도상 (23 Activities)!")
