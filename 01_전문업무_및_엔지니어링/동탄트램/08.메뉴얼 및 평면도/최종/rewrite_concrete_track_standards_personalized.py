import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

# Detailed personalized specs for 23 Track Standard HTMLs
track_standards_custom_data = {
    1: {
        "title": "설계적정성 검토",
        "purpose": "노반부/궤도부 선형 및 종단 일치 등 설계오류 및 누락 확인",
        "deliverable": "설계도면 검토서, 선형대조표",
        "std_sum": "KDS 47 30 00 궤도 설계기준 및 국토교통부 트램 건설 규칙을 엄격히 준수한다. 노반부-궤도부 선형 및 종단 계획고 일치 오차 0mm 검토.",
        "specs": [
            ("노반-궤도 계획고 대조", "설계 도면 분석", "노반 상단 계획 표고와 궤도 하단 계획고 일치 오차 0mm 만족 검토"),
            ("구배 및 곡선 반경", "트램 건설 규칙", "최대 구배 60‰ 이하, 최소 곡선 반경 25m 기하구조 한계치 검속"),
            ("지하지장물 간섭", "BIM 간섭 체크", "공동구, 배수관로 등 매설물과 궤도 기초 간 간섭 범위 전수 조사")
        ],
        "step1": "① 설계 도면 접수/분석",
        "step2": "② 선형 및 종단계획고 대조",
        "step3": "③ 최종 설계검토서 서명",
        "caution": "⚠️ 노반과 궤도 선형 불일치 시 궤도 단차로 인한 열차 주행 불가 초래",
        "summary": "노반-궤도 간의 기하학적 선형 정합성을 100% 일치시켜 현장 재시공 리스크를 원천 차단합니다."
    },
    2: {
        "title": "자재 야적장 선정",
        "purpose": "콘크리트도상 시공에 필요한 침목, 체결구 등 자재야적 부지 선정",
        "deliverable": "부지사용계약서, 가설야적장 평면도",
        "std_sum": "침목, 체결구, 홈레일 등 궤도 주요 자재의 현장 보관 기준 수립. 배수 경사 2% 및 지반 다짐도 95% 이상 야적장 확보.",
        "specs": [
            ("야적장 지반 지지력", "평판재하시험(PBT)", "PBT 지반 반력계수 K30 ≥ 80 MN/m³ 이상 견고성 확보"),
            ("배수 계획 수립", "횡단 경사도 실측", "우수 체류 방지를 위한 야적 바닥면 배수 구배 2% 이상 시공"),
            ("자재 적치 안전성", "적치 높이 제한", "침목 8단 이하, 철제 체결 자재 1.5m 이하 적치 및 방수포 덮개")
        ],
        "step1": "① 야적 부지 다짐/정지",
        "step2": "② 배수 및 차수 시설 설치",
        "step3": "③ 자재 인수/정돈 야적",
        "caution": "⚠️ 배수 불량 및 부지 침하 시 자재 뒤틀림 및 녹/부식 훼손 발생",
        "summary": "주요 자재(침목, 레일)의 변형을 방지하기 위해 다짐 및 배수 기준을 충족하는 전용 야적장을 조성합니다."
    },
    3: {
        "title": "레일 용접장 선정",
        "purpose": "정척레일 15본을 용접하여 200m 이상의 장대레일 제작하는 작업장을 선정 (타분야 인터페이스 고려)",
        "deliverable": "용접장 임시지정서, NDT 검사실 계획서",
        "std_sum": "EN 14730 테르밋 및 EN 14587 가스압접 용접을 위한 작업 공간 확보. 정척레일(25m)을 200m 장대로 용접하는 평탄 작업대 수평 오차 ±1mm 이내 확보.",
        "specs": [
            ("용접대 수평 평탄성", "광학 레벨 검측", "25m 레일 평탄 지지대 수평 오차 ±1.0mm 이내 정밀 통제"),
            ("방풍 및 차광 설비", "현장 환경 통제", "용접 작업구간 풍속 2.0 m/s 이하 유도용 방풍 차단막 설치"),
            ("비파괴검사 구역", "NDT 작업 공간", "감마선/초음파 검사를 위한 작업반 반경 방사선 안전거리 확보")
        ],
        "step1": "① 작업대 기초 평탄 정밀 측정",
        "step2": "② 정척레일 종단 지지틀 조립",
        "step3": "③ 방풍 및 NDT 안전망 구축",
        "caution": "⚠️ 용접 작업대 평탄성 오차 초과 시 장대레일 종단 영구 절곡 하자 발생",
        "summary": "용접 조인트의 기하학적 평탄성 확보 및 환경 변수 차단을 위해 전용 용접장의 환경 조건을 정밀 제어합니다."
    },
    4: {
        "title": "발주전략 KOM",
        "purpose": "궤도공사 발주전략 수립 / 발주조건 CP적합 여부 검토",
        "deliverable": "KOM 의사록, 품질 보증 합의서",
        "std_sum": "KCS 47 30 00 시방 기준 준수. 궤도 자재 품질 확인서 및 외산 홈레일 조달 리스크 대응 전략 수립.",
        "specs": [
            ("품질 요구조건 의결", "KCS 47 30 00 시방 준수", "계약 시 외산 홈레일(51R1/60R2) 공장 시험성적서 첨부 강제"),
            ("조달 일정 리스크", "조달 관리 기법", "해외 수입 자재 조달 리드타임(최소 6개월) 및 선적 준수율 100%"),
            ("협력사 자문 연동", "CP 준수 협약", "안전/품질 준수 공동 협약서 및 특기 조건 서명 날인")
        ],
        "step1": "① 계약 품질 특기 시방 검토",
        "step2": "② 조달 리드타임 확정",
        "step3": "③ 파트너십 상생 KOM 서명",
        "caution": "⚠️ 해외 조달 홈레일 통관 지연 시 전체 공정의 심각한 CPM 공기 지연 리스크",
        "summary": "자재 조달 지연 예방 및 요구 품질 보증을 위한 시방 특기 사항과 조달 프로세스를 KOM에서 최종 승인합니다."
    },
    5: {
        "title": "최고의 팀 만들기 지원",
        "purpose": "우수 협력사 및 작업반 선정",
        "deliverable": "협력사 적격성 심사표, 노무안전서약철",
        "std_sum": "EN ISO 9606-1 용접 자격자 및 궤도 정밀 검측원(Track Master 운용원) 확보 심사 기준.",
        "specs": [
            ("용접공 적격성 평가", "자격증 원본 대조", "EN ISO 9606-1 또는 KS 궤도 용접 자격 소지 여부 필터링 검토"),
            ("장비 검교정 여부", "장비 검교정 필증", "궤도 정밀 검측 장비의 검교정 유효기간 1년 확인서 제출"),
            ("현장 대리인 경력", "건설기술인협회 경력", "철도 궤도 분야 현장 대리인 시공 경력 5년 이상 배치")
        ],
        "step1": "① 기술진 자격/경력 심사",
        "step2": "② 검측 장비 검교정 필증 확인",
        "step3": "③ 현장 안전 서약서 작성",
        "caution": "⚠️ 무자격 용접자 시공 시 레일 파단 및 열차 탈선 등 초대형 중대 재해 직결",
        "summary": "철저한 자격 심사 및 검교정 장비 투입을 통해 고정밀 궤도 시공을 위한 최정예 기술 팀을 구축합니다."
    },
    6: {
        "title": "콘크리트 타설방법/계획 검토",
        "purpose": "현장여건에 따른 구간/위치별 적정 타설방법 및 계획 검토",
        "deliverable": "콘크리트 타설공정 계획서, 펌프카 배치도",
        "std_sum": "KCS 47 30 00 콘크리트 궤도 시방 준수. 펌프카 타설압력에 의한 궤광 변위 방지 지지 계획 수립.",
        "specs": [
            ("타설 압력 분산", "펌프카 시공 계획", "레일 타이바 및 게이지 잭에 직접적인 압력이 가해지지 않도록 유도"),
            ("타설 두께 통제", "완성고 레벨 실측", "TCL 및 HBR 거푸집 깊이 및 타설 높이 오차 ±5mm 이내 통제"),
            ("슬럼프 및 온도 관리", "레미콘 품질 검사", "콘크리트 슬럼프 120±20mm, 타설 온도 30℃ 이하 확보")
        ],
        "step1": "① 구간별 펌프카 작업 반경 검토",
        "step2": "② 궤광 변위 방지 지지 계획 수립",
        "step3": "③ 콘크리트 배합 품질 검인",
        "caution": "⚠️ 콘크리트 타설 압력 분산 실패 시 궤도 선형 틀림 발생",
        "summary": "콘크리트 타설 시 발생하는 측압과 거동에 대비하여 궤광 변형 방지 고정 장치 및 타설 경로 계획을 정밀 검토합니다."
    },
    7: {
        "title": "작수전 Big Room 회의",
        "purpose": "궤도공사 수행 시 공정계획 수립 / 수행 시 예상가능한 Risk 검토",
        "deliverable": "빅룸 회의록, 인터페이스 대장",
        "std_sum": "노반-궤도 간 인터페이스, 신호 루프 센서 및 누설 전류(Stray Current) 부식 방지 디오드 접지선 매설 계획 의결.",
        "specs": [
            ("공종 간 간섭 검토", "전기/신호/노반 합동", "궤도 배근 철근과 신호 루프 센서 차수 구멍 위치 간섭 전수 점검"),
            ("누설 전류 방지", "접지 설계 검토", "Stray Current 부식 방지용 디오드 접지선 매설 및 용접 계획 확인"),
            ("협력사 리스크 협의", "WBS 위험성 평가", "작업 개시 전 안전 위해요소 분석 대장 서명")
        ],
        "step1": "① 공종 간 인터페이스 도면 공유",
        "step2": "② 신호/접지 간섭 및 누설전류 대책 검토",
        "step3": "③ 합동 리스크 관리대장 확정",
        "caution": "⚠️ 궤도 철근과 신호 루프 센서 간섭 시 전자기 장애로 인한 트램 통신 단절 리스크",
        "summary": "타 공종(노반, 전기, 신호)과의 물리적·전자기적 간섭을 착공 전 완벽히 제거하기 위한 협력 대책을 의결합니다."
    },
    8: {
        "title": "장비,자재 반입로/반입구 간섭 검토",
        "purpose": "장비, 자재의 반입로/반입구의 타공종 간섭 검토",
        "deliverable": "반입로 시뮬레이션 보고서, 도로점용 허가서",
        "std_sum": "장대레일 운반 트레일러(길이 25m 이상) 도로 회전 반경 R=15m 확보 및 타공종 가설재 간섭 배제.",
        "specs": [
            ("운반 트레일러 반경", "현장 실측 좌표", "25m 장대레일 운반을 위한 도심 교차로 최소 회전 반경 R=15m 확보"),
            ("공중 가설물 간섭", "시설물 높이 검측", "크레인 인양 범위 내 특고압 가공 전선 이격 거리 3.0m 이상 확보"),
            ("도로 점용 및 안전", "지자체 허가 필증", "관할 경찰서/구청 도로점용 및 굴착허가증 확보 및 신호수 배치")
        ],
        "step1": "① 운반 트랙 진입 동선 시뮬레이션",
        "step2": "② 공중 전선 방호벽 설비 검토",
        "step3": "③ 도로점용 허가 및 통제원 배치",
        "caution": "⚠️ 장대레일 운송 차량 회전 반경 부족 시 교차로 진입 불가 및 교통 마비 야기",
        "summary": "초장대 궤도 자재의 도심지 반입 시 도로 회전 반경 및 특고압 가공선 가설 방호 조치 계획을 정밀 검토합니다."
    },
    9: {
        "title": "자재조달계획 검토",
        "purpose": "외산자재 검수 및 반입일정 검토 / 노반 공정에 따른 반입 시기 검토",
        "deliverable": "자재수급스케줄표, 조달 승인서",
        "std_sum": "홈레일, 체결구, 탄성 충전재 등 주요 자재의 해상 운송 및 국내 보관 일정 검토. OMC 품질 시방 확보.",
        "specs": [
            ("통관 리스크 제어", "공급 체인 분석", "수입 홈레일 및 특수 체결장치 승인서 및 항만 통관 기한 확보 검토"),
            ("적정 입고 시기", "CPM 공정표 연동", "선행 노반(HBS) 완료예정일과 현장 야적 자재 반입 일정 일치"),
            ("품질 시험 검증", "시험 성적서 대조", "입고 예정 자재의 공장 성적서 품질 기준(KS/EN) 적격성 100%")
        ],
        "step1": "① 수입 통관 문서 및 승인서 대조",
        "step2": "② 노반 공정율 연계 자재 수요 매칭",
        "step3": "③ 예비 자재 비축 수량 확정",
        "caution": "⚠️ 자재 수입 및 입고 지연 시 궤도 시공 중단으로 인한 전체 공기 지연 리스크",
        "summary": "홈레일 및 체결장치 등 외산 핵심 자재의 원활한 조달을 위해 선행 공정의 완료 스케줄에 연계한 입고 계획을 수립합니다."
    },
    10: {
        "title": "자재 발주 요청",
        "purpose": "시공에 필요한 자재 발주",
        "deliverable": "자재청구서, 공급원 승인요청철",
        "std_sum": "KDS 47 30 00 및 EN 규격 기준 자재 발주서 승인. 공급원 검토 승인 요청서 작성 요령 준수.",
        "specs": [
            ("설계 물량 대조", "설계 도서 실측", "도면 연장 실측 물량 대비 레일/체결구 발주 수량 대조 정합성 100%"),
            ("공급원 검토 신청", "감리단 승인서", "계약서 규정 품질 기준에 부합하는 공인 제조업체 승인서 구비"),
            ("발주서 제작 납기", "조달 부서 연동", "공식 발주 요청 공문 발송 및 제조 공장 납기 확약서 확보")
        ],
        "step1": "① 설계 도면 대비 소요 물량 산출",
        "step2": "② 공급원 검토 요청서 승인",
        "step3": "③ 공식 발주서 작성 및 납기 확정",
        "caution": "⚠️ 발주 물량 오산으로 인한 자재 부족 시 해외 자재 재수입에 따른 장기 공사 중단",
        "summary": "정확한 설계 물량 산출 및 승인된 자재 제조업체 발주를 통해 자재 부족이나 품질 미달 리스크를 제거합니다."
    },
    11: {
        "title": "시공계획 수립",
        "purpose": "궤도공 전반에 대한 수행 계획 공유",
        "deliverable": "궤도공사 시공계획서, 안전보건계획서",
        "std_sum": "콘크리트도상 시공 절차 및 공정 스케줄 작성. 궤간(+3,-1mm), 캔트(±2mm) 관리계획 수립.",
        "specs": [
            ("선형 정밀 제어", "관리 한계 설정", "궤간(+3.0, -1.0mm) 및 캔트/수평(±1.5mm) 시방 기준 관리 계획 수립"),
            ("콘크리트 양생 계획", "양생 기간 및 방식", "기초 HBR 7일, 도상 TCL 14일 이상 습윤 살수 양생 계획 성문화"),
            ("안전 보건 계획", "유해위험 방지 계획", "도심지 도로 굴착 및 대형 장비 가동 시 통제 펜스 및 안전원 배치")
        ],
        "step1": "① 시공 상세 도면 및 공정표 작성",
        "step2": "② 품질·안전 관리 계획 승인",
        "step3": "③ 시공계획서 감리단 최종 의결",
        "caution": "⚠️ 시공계획서 미승인 착공 시 부적합 시공 발생 및 감리단 공사 중지 처분 리스크",
        "summary": "완성선 정밀도 확보와 현장 안전 확보를 위한 시공 순서, 품질 계획 및 안전 수칙을 체계적으로 수립합니다."
    },
    12: {
        "title": "자재 반입",
        "purpose": "매립형 궤도/반-PC슬래브용 주요 자재 반입",
        "deliverable": "자재인수검사 대장, 불량재 처리부",
        "std_sum": "반입 자재의 공장 성적서 대조 및 감리 입회 자재 인수 검사 수행. 변형/균열 자재 전량 반출.",
        "specs": [
            ("감리단 자재 검수", "현장 입회 검사", "반입 자재의 시험성적서 원본 대조 및 인수 검수서 감리 서명 100%"),
            ("자재 식별 관리", "품질 추적성 확보", "레일 및 주요 자재의 제품 고유HEAT No. 마킹 기록 관리"),
            ("부적합 자재 통제", "불량 자재 반출", "변형, 균열 및 품질 기준 미달 자재는 적색 적치 태그 부착 후 즉시 반출")
        ],
        "step1": "① 자재 운반 차량 하차 대기",
        "step2": "② 시험성적서 대조 및 외관 인수 검사",
        "step3": "③ 합격 자재 현장 적치 및 마킹",
        "caution": "⚠️ 인수 검사 소홀로 균열 및 불량 체결 자재 매립 시 궤도 하중에 따른 파단 유발",
        "summary": "현장에 입고되는 모든 자재의 품질 추적성을 확보하고 감리 입회 하에 결함 자재를 엄격히 걸러내어 반출합니다."
    },
    13: {
        "title": "[HBS] 강화노반 확인",
        "purpose": "기존 도로구간 노상토의 지지력 검증",
        "deliverable": "강화노반 인수교차측량 대장, PBT 성적철",
        "std_sum": "기초 노반 표면의 지지력 검증. 평판재하시험 K30 ≥ 110 MN/m³ 또는 Ev2 ≥ 120 MPa 확인.",
        "specs": [
            ("노반 지지력 검증", "평판재하시험(PBT)", "PBT 결과 지반 반력계수 K30 ≥ 110 MN/m³ 또는 Ev2 ≥ 120 MPa 확인"),
            ("높이 및 횡단구배", "광학 토탈스테이션", "노반 마무리면 높이 오차 ±10mm 이내, 횡단 배수 경사 구배 2.0% 준수"),
            ("노반면 표면 청소", "고압 살수 세척", "타설 전 점토 슬러지, 부스러기 및 이물질 전수 제거 및 배수 건조")
        ],
        "step1": "① 노반 지지력(K30) 시험 및 통과",
        "step2": "② 표면 종횡단 레벨 오차 측정",
        "step3": "③ 고압수 살수 청소 및 노반 인수",
        "caution": "⚠️ 노반 지지력 부족 및 부적합 침하 방치 시 도상 콘크리트 영구 파손 균열 하자",
        "summary": "궤도의 기초 역할을 하는 하부 강화노반의 지지력과 높이 정밀도를 검증하여 궤도의 영구 침하를 방지합니다."
    },
    14: {
        "title": "[HBS] 콘크리트 타설 및 양생",
        "purpose": "강화노반 상부 기초콘크리트로 TCL, 반-PC 슬래브 안정성 확보",
        "deliverable": "HBR 콘크리트 품질시험표, 양생온도일지",
        "std_sum": "강화노반 상부 기초콘크리트(HBR) 28일 압축강도 ≥ 21 MPa 확보. 고주파 다짐 및 습윤 양생 7일.",
        "specs": [
            ("설계 압축 강도", "압축강도 시험(28일)", "기초콘크리트(HBR) 설계 강도 fck ≥ 21 MPa 충족 성적서 확보"),
            ("타설면 수평도 관리", "광학 레벨 확인", "HBR 표면 마무리면 오차 ±10mm 이내 정밀 스크리딩 다짐"),
            ("양생 및 청소 수칙", "살수 습윤 양생", "타설 직후 7일간 살수 습윤 부직포 포설 양생 및 표면 레이턴스 파쇄")
        ],
        "step1": "① HBR 레미콘 슬럼프 품질 검사",
        "step2": "② 다짐기 조작 타설 및 높이 실측",
        "step3": "③ 7일간 습윤 살수 양생 및 청소",
        "caution": "⚠️ 타설 후 수축 수열 관리 소홀 시 표면 건조 크랙 및 구조적 피로 손실 유발",
        "summary": "강화노반 상부 기초콘크리트의 설계 강도를 보장하고 고밀도 시공을 유도하여 궤도의 기초 거치 성능을 확보합니다."
    },
    15: {
        "title": "[반-PC 슬래브] 패널반입 및 설치",
        "purpose": "궤광지지체 구간의 PC 슬래브로 교차로/교량구간 급속시공 필요",
        "deliverable": "PC슬래브 거치 수준 실측표, 평탄성 대장",
        "std_sum": "PC 슬래브 패널 평탄성 오차 ±3mm 이내 거치. 광학 토탈스테이션 연동 정밀 3D 얼라인먼트.",
        "specs": [
            ("패널 평탄성 확보", "정밀 수준 측량", "PC 슬래브 패널 상부면 평탄성 오차 ±3.0mm 이내 조립 거치"),
            ("패널 3D 좌표 실측", "광학 토탈스테이션", "3차원 절대 좌표 오차(평면/종단) ±2.0mm 이내 정위치 앵커 고정"),
            ("외관 크랙 전수검사", "균열 측정 게이지", "하차 및 크레인 양중 시 발생한 코너 크랙 폭 0.2mm 초과 여부 검사")
        ],
        "step1": "① 크레인 이용 PC 패널 안전 양중",
        "step2": "② 스크류 잭 활용 3D 레벨 얼라인먼트",
        "step3": "③ 조인트 폼 설치 및 코너 크랙 검사",
        "caution": "⚠️ PC 패널 레벨 조정 실패 시 레일 거치 후 궤간 및 캔트 허용 한계 오차 초과",
        "summary": "반-PC 슬래브 패널을 정밀 거치하고 광학 장비로 3차원 얼라인먼트를 실측하여 교차로부 급속 시공의 품질을 보장합니다."
    },
    16: {
        "title": "[PST] 전단앵커설치 및 충전재 주입",
        "purpose": "HBS, TCL층과 일체화를 위하여 전단앵커를 설치하고 몰탈 충전재 주입",
        "deliverable": "앵커 시공인장 시험기록, 그라우트 공시체 강도대장",
        "std_sum": "전단앵커 구멍 천공 깊이 및 수직도 확보. 무수축 모르타르 그라우트 압축강도 ≥ 30 MPa 충전.",
        "specs": [
            ("전단 앵커 천공", "깊이 게이지 측정", "설계 천공 깊이 준수 및 수직도 오차 5° 이내 천공 및 진공 흡입 청소"),
            ("무수축 그라우트 강도", "공시체 압축시험", "무수축 모르타르 그라우트 28일 압축강도 fck ≥ 30 MPa 검증"),
            ("주입 연속성 확보", "원웨이 압송 공법", "하부 배출구로 슬러리가 오버플로우 될 때까지 공기 배출구 확인 압송")
        ],
        "step1": "① 전단 앵커 구멍 천공 및 이물질 청소",
        "step2": "② 무수축 몰탈 배합 및 유동 시험",
        "step3": "③ 앵커 고정 및 원웨이 그라우트 연속 주입",
        "caution": "⚠️ 그라우트 압송 중단 시 내부 에어포켓 발생으로 전단 앵커 지지 강도 파괴",
        "summary": "앵커 고정 및 무수축 충전재를 원웨이로 빈틈없이 그라우팅하여 PC 슬래브 패널과 기초를 완전 일체화합니다."
    },
    17: {
        "title": "[TCL] 궤광 및 철근조립",
        "purpose": "TCL 철근조립 및 부설시 매립형 궤도를 포함한 궤광의 변위 발생 방지",
        "deliverable": "철근배근 검측서, 신호 이격 거리표",
        "std_sum": "1,435mm 표준궤 정밀 유지 타이바 설치. 철근 피복 두께 40mm 확보 및 신호 감선 이격 150mm.",
        "specs": [
            ("철근 피복 두께", "두께 측정 게이지", "TCL 콘크리트 도상 철근 피복 두께 설계치 최소 40mm 이상 확보"),
            ("철근-신호 이격거리", "절연 스페이서 실측", "신호 루프 센서 케이블 배관과 철근 배근 간격 최소 150mm 이상 이격"),
            ("타이바 조임 토크", "토크 렌치 조임", "궤간 고정용 철제 타이바의 너트 조임 토크 설계 기준치 충족")
        ],
        "step1": "① 철근 규격 배근 및 스페이서 거치",
        "step2": "② 레일 타이바 조립 및 궤간 1,435mm 세팅",
        "step3": "③ 신호 루프 케이블 배선 이격 실측",
        "caution": "⚠️ 신호 케이블과 철근 밀착 시 유도 전자기 교란으로 열차 신호 제어 불능 초래",
        "summary": "정확한 피복 두께 준수 및 타이바 조임으로 콘크리트 강성을 확보하고 신호 계통의 전자기적 간섭을 차단합니다."
    },
    18: {
        "title": "[TCL] 거푸집 설치",
        "purpose": "거푸집 지지대는 철근이 타설압력에 의해 변위가 발생하지 않도록 앵커나 서포트로 고정",
        "deliverable": "거푸집설치 대조표, 박리제 검사철",
        "std_sum": "타설 측압 대비 서포트 앵커 W=1.0m 간격 고정. 거푸집 수평/수직 처짐 변위 ±2mm 이내 통제.",
        "specs": [
            ("거푸집 지지력 강성", "서포터 및 앵커", "콘크리트 타설 측압 지지용 거푸집 앵커 서포트 간격 W=1.0m 이내 고정"),
            ("처짐 변위 통제", "정밀 실측 레벨", "거푸집의 상하/좌우 변형 편차 및 처짐 ±2.0mm 이내 실시간 통제"),
            ("이음새 밀착 패킹", "누수 패킹 처리", "시멘트 페이스트 유출 방지를 위한 접촉 이음부 고무 테이핑 밀착")
        ],
        "step1": "① 거푸집 유닛 가선 조립",
        "step2": "② W=1.0m 간격 서포트 고정 앵커 조임",
        "step3": "③ 박리제 도포 및 이음새 고무 패킹 확인",
        "caution": "⚠️ 거푸집 서포트 부실 시 타설 중 거푸집 터짐 및 선로 이탈 대형 사고 발생",
        "summary": "타설 시 가해지는 콘크리트 자중과 측압을 지지하도록 거푸집을 고정하고 페이스트 누출을 원천 방지합니다."
    },
    19: {
        "title": "[TCL] 콘크리트 타설 및 양생",
        "purpose": "TCL은 궤도 부속자재(레일, 고정액상수지 등)가 연결되어 있어, 선형조정 및 연마감 작업이 중요",
        "deliverable": "TCL 콘크리트 품질대장, 게이지 실시간 보정일지",
        "std_sum": "TCL 도상 콘크리트 강도 ≥ 35 MPa. 타설 중 실시간 궤간척(Gauge Bar) 캔트 오차 ±2mm 보정.",
        "specs": [
            ("도상 콘크리트 강도", "공시체 28일 강도", "도상 콘크리트 설계 강도 fck ≥ 35 MPa 충족 시험성적표 확보"),
            ("실시간 선형 모니터", "궤간척 게이지 측정", "타설 진행 중 궤간(+3.0, -1.0mm) 및 캔트/수평(±2.0mm) 실시간 보정"),
            ("건조 수축 균열 양생", "습윤 마대 포설", "콘크리트 타설 후 표면 습윤 부직포 포설 및 최소 14일간 습윤 유지")
        ],
        "step1": "① 레미콘 반입 시험 및 펌프카 타설",
        "step2": "② 타설 중 실시간 궤간/캔트 선형 모니터링",
        "step3": "③ 습윤 마대 포설 및 14일 수분 양생",
        "caution": "⚠️ 타설 중 게이지 모니터링 누락 시 궤간 뒤틀림이 고착화되어 전량 할석 재시공",
        "summary": "고강도 도상 콘크리트를 균일하게 타설하며 실시간 선형 보정을 수행하고 철저한 습윤 양생을 실시합니다."
    },
    20: {
        "title": "[레일용접] 가스 압접",
        "purpose": "장대레일 제작을 위해 용접기에서 가스로 레일 단부를 가열한 후, 강한 압력을 가하여 레일을 접합",
        "deliverable": "가스압접 시공성적표, UT 비파괴보고서",
        "std_sum": "EN 14587 규격 준수. 레일 단부 가열(1200℃) 후 압송. 용접부 직선도 1m당 ±0.2mm 이내 정밀 연마.",
        "specs": [
            ("가열 온도 및 가압", "방사 온도계 측정", "압접 단부 가열 온도 1,200℃ 정밀 유지 및 규정 가압 압력 충족"),
            ("용접부 마감 직선도", "1m 정밀 룰러", "연마 완료 후 가스 압접부 수직/수평 직선도 오차 1m당 ±0.2mm 이내"),
            ("용접 비파괴 검사", "초음파 탐상(UT)", "EN 14587 규격에 따른 가스 압접부 초음파(UT) 검사 100% 합격 확보")
        ],
        "step1": "① 레일 단부 평탄 컷팅 및 가스 가열",
        "step2": "② 유압 장치 작동 압속 접합 및 버(Burr) 제거",
        "step3": "③ 직선도 ±0.2mm 연마 및 NDT 검사",
        "caution": "⚠️ 가열 불균일 및 가압 부족 시 용접 접합부 잔류 크랙으로 주행 중 레일 파단",
        "summary": "레일 접합부를 균일 가열하고 강한 압력으로 용착한 후 정밀 마감 연마를 통해 용접부 강도와 직선도를 확보합니다."
    },
    21: {
        "title": "[레일용접] 테르밋 용접",
        "purpose": "테르밋 용제를 예열된 장대레일 공간에 넣고 용융하여 모든 장대레일을 일체화",
        "deliverable": "테르밋 용접일지, MT 자분탐상 보고서",
        "std_sum": "EN 14730 규격 준수. 도가니 반응 후 슬래그 분리. 직선도 오차 ±0.2mm 이내 및 NDT 100% 합격.",
        "specs": [
            ("조인트 용접 갭", "틈새 폭 실측", "용접부 레일 끝단 간 간격 25mm±1.0mm 및 선형 정위치 고정"),
            ("용접부 예열 관리", "예열 버너 온도", "레일 끝단 900℃~1000℃ 이상 예열 및 유효 가열 시간 확인"),
            ("화학 반응 및 NDT", "비파괴(UT/MT) 검사", "EN 14730 규격에 따른 테르밋 조인트 비파괴 검사 100% 통과")
        ],
        "step1": "① 레일 조인트 갭(25mm) 세팅 및 몰드 설치",
        "step2": "② 레일 단부 가열 예열 및 용제 투입 반응",
        "step3": "③ 몰드 탈형, 게이트 제거 및 NDT 100% 검사",
        "caution": "⚠️ 예열 불충분 또는 습기 유입 시 용접부 내 기공(Blow-hole) 결함 및 강도 상실",
        "summary": "테르밋 화학반응을 통한 융착 공정 시 조인트 정밀 세팅 및 예열 조건을 준수하고 비파괴 검사로 내부 건전성을 입증합니다."
    },
    22: {
        "title": "[레일연마] 레일연마 or 밀링",
        "purpose": "레일 연마 or 밀링작업을 통해 선로의 평탄화증을 제거하여 레일 수명 향상 및 운행 안정성 개선",
        "deliverable": "선로 평탄성검사 성적표, 조도 실측야장",
        "std_sum": "레일 마무리면 평탄성 1m 기준 오차 ±0.2mm 이내 밀링. 레일 과열에 의한 열응력 크랙 방지.",
        "specs": [
            ("연마 마감 평탄성", "정밀 수준 마이크로", "연마 완료 레일 표면 완성면 1m 직선 기준 평탄성 오차 ±0.2mm 이내"),
            ("레일 열화 방지", "윤활제 분사 온도", "건식 연마 시 레일 국부 온도 100℃ 이하 통제용 냉각수 지속 살포"),
            ("파상 마모 제어", "파상 마모 실측기", "선로 10cm 간격 종단 파상 마모 높이 최대 0.05mm 이하 유지 관리")
        ],
        "step1": "① 마이크로미터 레일 초기 평탄성 실측",
        "step2": "② 연마 장비 삭감 깊이 세팅 및 윤활제 분사",
        "step3": "③ 정밀 조도계 표면 완성도 검속 및 성적서",
        "caution": "⚠️ 건식 과열 연마 시 표면 청색 열화 크랙(Blue Brittle) 발생으로 급격한 레일 훼손",
        "summary": "선로 완성면을 정밀 밀링 및 연마하여 기하학적 평탄성 오차 ±0.2mm를 달성하고 열화 균열 발생을 차단합니다."
    },
    23: {
        "title": "후속공사 인수인계",
        "purpose": "완료구간 후속공사 인수인계",
        "deliverable": "궤도 완공 인수서명부, 절연저항 성적철",
        "std_sum": "전기/신호/노반 담당자 입회 하에 궤도 회로 절연 저항 ≥ 100MΩ 검속. 준공 도면 일치 서명.",
        "specs": [
            ("궤도 절연 저항", "절연 테스트(메거)", "궤도 회로 신호 보존 및 Stray Current 방지용 절연 저항 R ≥ 100 MΩ 확보"),
            ("선로 선형 최종검속", "5대 기하 요소", "궤간, 캔트, 수평, 고저, 방향 최종 검속 및 시방 허용 편차 검증"),
            ("3자 공동 서명 날인", "인수인계 공동 확인", "전기/신호/노반 담당 감리원·현장대리인 합동 현장 검속 후 서명 날인")
        ],
        "step1": "① 궤도 완성 선형 및 절연 저항(≥100MΩ) 실측",
        "step2": "② 3자(전기/신호/노반) 공동 입회 점검",
        "step3": "③ 준공 설계도서 기명 날인 및 인수인계 서명",
        "caution": "⚠️ 절연 저항 기준 미달 상태 인수 시 누설 전류에 의한 후행 전차선 급전 시스템 마비",
        "summary": "최종 궤도의 기하선형 및 전기적 절연 성능을 검증하고, 다자간 연계 공종 합동 인수 서명을 완료합니다."
    }
}

folders_on_disk = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

html_updated = 0
for seq_num, gt in track_standards_custom_data.items():
    prefix = f"{seq_num}_"
    folder_name = None
    for f in folders_on_disk:
        if f.startswith(prefix):
            folder_name = f
            break
            
    if not folder_name:
        continue

    folder_path = os.path.join(base_dir, folder_name)
    std_dir = os.path.join(folder_path, "표준서")
    
    title = gt["title"]
    purpose = gt["purpose"]
    deliverable = gt["deliverable"]
    std_sum = gt["std_sum"]
    
    # Render specifications table rows dynamically
    specs_rows = ""
    for name, standard, spec in gt["specs"]:
        specs_rows += f"""                <tr>
                    <td style="font-weight: bold; text-align: center;">{name}</td>
                    <td style="text-align: center;">{standard}</td>
                    <td>• {spec}</td>
                </tr>\n"""

    step1 = gt["step1"]
    step2 = gt["step2"]
    step3 = gt["step3"]
    caution = gt["caution"]
    summary_text = gt["summary"]

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
            <span><span class="badge">액티비티 1:1 정합화 완료</span></span>
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
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">기술 검속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 시방 및 검사 기준</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 50%;">핵심 정량 기술 수칙 및 허용 공차</th>
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
            <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">콘크리트도상 {title} 시공 핵심 흐름</text>

            <g transform="translate(50, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e1b4b">{step1}</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 관련 시방 및 지침 검토</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 착수 전 필수 선결조건 확인</text>
            </g>

            <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

            <g transform="translate(340, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">{step2}</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 정량적 시방 정밀 삭감/타설</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 실시간 선형 모니터링 보정</text>
            </g>

            <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

            <g transform="translate(630, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">{step3}</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 비파괴 NDT 및 3자 합동 실측</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 준공 기명 서명 및 후행 인계</text>
            </g>

            <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
            <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">{caution}</text>
        </svg>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> {summary_text}
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

    html_updated += 1
    print(f"[{html_updated}/23] Regenerated Personalized Technical Standard HTML for WBS 9000-6-{seq_num}.")

print(f"\n🎉 Successfully Overwritten {html_updated} Standard HTML files with personalized specs!")
