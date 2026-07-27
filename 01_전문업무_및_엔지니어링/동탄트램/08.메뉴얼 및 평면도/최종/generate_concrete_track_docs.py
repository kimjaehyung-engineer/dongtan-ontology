import os
import sys

# Base directory for Concrete Track activities
base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

# 23 Activities definition with specific technical parameters
activities = [
    {
        "folder": "1_설계적정성 검토",
        "wbs": "9000-6-1",
        "name": "설계적정성 검토",
        "dept": "궤도 / 설계",
        "supervisor": "기술지원팀 / 궤도검토팀",
        "purpose": "동탄트램 콘크리트도상 궤도 구조, 곡선부 R값, 캔트, 확폭량 및 매설궤도/슬래브도상 인터페이스의 설계 적정성 철저 검토",
        "method": "KDS 47 30 00(철도 궤도 설계기준) 및 KCS 47 30 00(궤도공사 시방서) 비교 검토, 3D BIM 궤도 선형 및 장대레일 신축 이음매 위치 검증",
        "output": "설계적정성 검토 보고서, 궤도 선형 오차 보정서, 도상 타입별(매설/PST/TCL) 인터페이스 검토서",
        "key_focus": "표준궤 1435mm (+3/-1mm), 캔트 Max 160mm, 곡선 확폭량(Slack), 51R1/60R2 홈레일 및 60kg/m 레일 적용성 검토"
    },
    {
        "folder": "2_자재 야적장 선정",
        "wbs": "9000-6-2",
        "name": "자재 야적장 선정",
        "dept": "궤도 / 공사",
        "supervisor": "현장 공사팀",
        "purpose": "60kg/m 장대레일, 51R1/60R2 홈레일, PST 프리캐스트 슬래브 패널 및 도상 자재의 보관·품질 유지를 위한 최적의 야적장 부지 선정",
        "method": "하중 지지력(지반 지지력 K70 검토), 빗물 배수계획, 크레인 및 장대레일 운반 차량 진출입 동선 분석, 방수/방습 야적 환경 조성",
        "output": "자재 야적장 선정 보고서, 야적장 배치도, 지반 지지력 성적서, 자재 보관 관리계획서",
        "key_focus": "장대레일 휨 변형 방지용 받침목 간격(2m 이내) 준수, PST 패널 적재 단수 규정 준수, 테르밋 용재 건조 보관소 확보"
    },
    {
        "folder": "3_레일 용접장 선정",
        "wbs": "9000-6-3",
        "name": "레일 용접장 선정",
        "dept": "궤도 / 용접",
        "supervisor": "현장 공사팀 / 궤도용접팀",
        "purpose": "25m 정척 레일을 150m~300m 장대레일로 1차 가스압접/플래시버트 용접하기 위한 기지 레일 용접장 입지 및 설비 선정",
        "method": "EN 14587 규격에 부합하는 자동 가스압접/플래시버트 용접기 배치, 레일 정열 롤러대 설치, 100% NDT 비파괴 검사장 및 연마 작업장 확보",
        "output": "레일 용접장 승인 신청서, 용접장 배치 및 동선 계획서, 용접 설비 정밀도 교정서",
        "key_focus": "EN 14587 적용, 용접 직선도 공차 1m 당 ±0.2mm 확보용 롤러대 수평 정밀도 교정, 비파괴검사(UT/MT) 전용구역 설치"
    },
    {
        "folder": "4_발주전략 KOM",
        "wbs": "9000-6-4",
        "name": "발주전략 KOM",
        "dept": "궤도 / 구매",
        "supervisor": "구매조달팀 / 궤도사업팀",
        "purpose": "콘크리트도상 핵심 자재(60kg 레일, 51R1 홈레일, PST 패널, 체결장치, 테르밋 용제) 발주 및 시공 협력사 선정을 위한 Kick-Off Meeting 개최",
        "method": "발주 사양서, KDS 47 30 00 품질 요구조건, 리드타임 검토, 자율 자재 시험성적서 및 공장검사 추진 일정 동기화",
        "output": "발주전략 KOM 회의록, 주요 자재 조달 일정표, 품질 표준 합의서",
        "key_focus": "KDS/KCS 시방 만족 자재 선정, EN 14730 테르밋 용제 정품 수급, PST 패널 제조공장 품질 인증 검증"
    },
    {
        "folder": "5_최고의 팀 만들기 지원",
        "wbs": "9000-6-5",
        "name": "최고의 팀 만들기 지원",
        "dept": "궤도 / 사업관리",
        "supervisor": "사업관리팀 / 궤도품질팀",
        "purpose": "트램 궤도공사의 특수성(매설궤도, 캔트, 테르밋 용접, 스핀들 정밀 조작)에 대응할 궤도 전문 엔지니어 및 숙련공 팀 구성 지원",
        "method": "국제/국내 궤도 용접 자격자(EN ISO 14730 자격 보유자) 확보, 궤도 정밀 측량사 배치, 사전 시공 시뮬레이션 및 기술 교육 시행",
        "output": "궤도공사 인력 투입 및 조직표, 전문 자격증 사본, 사전 기술교육 이수증",
        "key_focus": "테르밋 용접 자격자 및 궤도 정밀 측량 전문인력 필수 배치, 안전/품질 책임제 수립"
    },
    {
        "folder": "6_콘크리트 타설방법_계획 검토",
        "wbs": "9000-6-6",
        "name": "콘크리트 타설방법_계획 검토",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀 / 품질관리팀",
        "purpose": "도상 콘크리트(TCL f_ck ≥ 30 MPa) 및 PST 전단앵커 충전재(f_ck ≥ 45 MPa) 타설 시 콜드조인트 방지 및 고주파 바이브레이터 다짐 계획 검토",
        "method": "레미콘 운반 시간, 타설 순서(하상에서 상상으로, 캔트 이행부 주의), 펌프카 셋팅 위치, 고주파 바이브레이터 댓수 및 타설 간격 검토",
        "output": "콘크리트 타설 및 양생 계획서, 배합설계 승인서, 바이브레이터 배치도",
        "key_focus": "TCL 28일 압축강도 ≥ 30 MPa, 충전재 ≥ 45 MPa, 고주파 다짐에 의한 스핀들 게이지/매설 센서 이탈 방지대책"
    },
    {
        "folder": "7_작수전 Big Room 회의",
        "wbs": "9000-6-7",
        "name": "작수전 Big Room 회의",
        "dept": "궤도 / 종합",
        "supervisor": "사업관리단 / 궤도총괄",
        "purpose": "궤도, 노반(HBS), 건축, 신호, 전차선, 도로교통 등 다공종 간 인터페이스 및 공정 간섭사항을 착공 전 종합 협의하여 사전 해소",
        "method": "Big Room에 전 분야 관계자 소집, 3D BIM 기반 매설 배관/케이블/드레인 박스 간섭 검토 및 시공 우선순위 최종 확정",
        "output": "Big Room 회의록, 공종 간 인터페이스 승인서, 간섭 해소 조치 결과보고서",
        "key_focus": "강화노반(HBS) 인수인계 시점, 신호 궤도회로/루프센서 매설 부위 인터페이스, 도로 매설 궤도 표면 높이 동기화"
    },
    {
        "folder": "8_장비,자재 반입로_반입구 간섭 검토",
        "wbs": "9000-6-8",
        "name": "장비,자재 반입로_반입구 간섭 검토",
        "dept": "궤도 / 공정",
        "supervisor": "현장 공사팀 / 안전보건팀",
        "purpose": "장대레일 운반 트레일러, PST 패널 인양 크레인, 레미콘/펌프카 진입 시 지장물, 도로 차선 점용, 상부 전력선 간섭 검토",
        "method": "도심지 트램 노선 진입로 곡선반경 회전각 검토, 지중 매설물 하중 지지력 검토, 가설 진입판 및 교통통제 신호수 배치계획 검토",
        "output": "반입로 간섭 검토 보고서, 가설 진입로 계획도, 도로점용 허가서",
        "key_focus": "장대레일(최대 300m/분할 운반) 회전반경 확보, 크레인 작업 시 전력선 이격거리 준수"
    },
    {
        "folder": "9_자재조달계획 검토",
        "wbs": "9000-6-9",
        "name": "자재조달계획 검토",
        "dept": "궤도 / 자재",
        "supervisor": "자재팀 / 궤도공사팀",
        "purpose": "60kg 레일, 51R1 홈레일, PST 패널, 레일 체결장치, 테르밋 용제 등 핵심 궤도 자재의 생산, 검수, 현장 반입 리드타임 검토",
        "method": "월별/주별 궤도 공정표와 자재 납품 일정 동기화, 공장검사(FAT) 일정 수립, 자재 수급 지연 시 공정 보정 방안 검토",
        "output": "자재 조달 마스터 플랜, 자재 수급 리스크 관리표, 공장 검사 계획서",
        "key_focus": "해외/국내 특수 홈레일 수급 리드타임 관리, 테르밋 용재 보관 유효기간 관리"
    },
    {
        "folder": "10_자재 발주 요청",
        "wbs": "9000-6-10",
        "name": "자재 발주 요청",
        "dept": "궤도 / 자재",
        "supervisor": "자재팀 / 구매팀",
        "purpose": "KDS 47 30 00 기술 기준에 적합한 레일, 슬래브 패널, 패스너, 용접 용재의 확정 물량 산정 및 정식 발주 요청",
        "method": "설계 도면 상세 산출물량 기반 이음매/손실률 반영, 시험성적서 제출 의무화, 납품 시 승인 조건 명시",
        "output": "자재 발주 요청서, 상세 물량 산출서, 기술 규격서",
        "key_focus": "표준궤 1435mm 체결장치 오차 규격, 레일 직선도 및 화학성분 성적서 첨부"
    },
    {
        "folder": "11_시공계획 수립",
        "wbs": "9000-6-11",
        "name": "시공계획 수립",
        "dept": "궤도 / 공사",
        "supervisor": "현장 소장 / 궤도공사팀장",
        "purpose": "콘크리트도상 전체 공정의 사전준비-본시공-검사마감 3단계 세부 시공계획 수립 및 발주처/감리단 승인 획득",
        "method": "3단계 체계(사전준비 ➡️ 본시공 ➡️ 검사마감)로 정밀 구성, 궤간/캔트/용접/타설 시공 세부 지침 작성, 품질/안전 계획 통합",
        "output": "콘크리트도상 시공계획서(승인본), 품질관리계획서, 공정 마스터 스케줄",
        "key_focus": "3단계 체계 수립, 스핀들 게이지 조정, 테르밋 용접, TCL 콘크리트 타설 및 레일 연마 통합 반영"
    },
    {
        "folder": "12_자재 반입",
        "wbs": "9000-6-12",
        "name": "자재 반입",
        "dept": "궤도 / 품질",
        "supervisor": "품질관리팀 / 현장공사팀",
        "purpose": "현장에 도착한 레일, PST 패널, 체결재, 테르밋 용제의 규격, 외관, 수량 및 시험성적서 정밀 검수",
        "method": "레일 흠집/휨 검사, PST 패널 균열/치수 오차 검사, 테르밋 용제 방수 포장 상태 및 유효기간 검사, 송장 및 시험성적서 대조",
        "output": "자재 반입 검수 보고서, 품질 시험성적서, 자재 수불부",
        "key_focus": "레일 표면 흠집 검사, PST 패널 치수 공차(±2mm) 검사, 테르밋 용재 습기 침투 여부 확인"
    },
    {
        "folder": "13_[HBS] 강화노반 확인",
        "wbs": "9000-6-13",
        "name": "[HBS] 강화노반 확인",
        "dept": "궤도 / 토목 interface",
        "supervisor": "궤도공사팀 / 노반감리원",
        "purpose": "궤도 시공 전 하부 HBS(Hydraulic Bound Synthetic) 강화노반의 평탄성, 지지력, 종횡단 측량 성과 정밀 확인 및 인수인계",
        "method": "평판재하시험(K70 ≥ 150 MPa/m), 종횡단 CP 광학 측량, 노반 표면 이물질 및 균열 조사, 평탄도 측정",
        "output": "강화노반 인수인계서, 평판재하시험 결과지, 노반 종횡단 측량 성과표",
        "key_focus": "지지력 K70 ≥ 150 MPa/m 검증, 종횡단 높이 공차(±10mm) 확인 후 궤도 공정 인계"
    },
    {
        "folder": "14_[HBS] 콘크리트 타설 및 양생",
        "wbs": "9000-6-14",
        "name": "[HBS] 콘크리트 타설 및 양생",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀 / 품질팀",
        "purpose": "HBS 상부 도상 기층 콘크리트 타설 및 습윤 양생을 수행하여 슬래브 패널 및 TCL 받침 기층 확보",
        "method": "콘크리트 배합(f_ck ≥ 30 MPa), 고주파 바이브레이터 다짐, 레이턴스 제거, 7일 이상 습윤 피막 양생",
        "output": "HBS 콘크리트 타설 일지, 압축강도 시험성적서(7일/28일), 양생 관리 기록지",
        "key_focus": "f_ck ≥ 30 MPa 확보, 콜드조인트 방지 연속 타설, 표면 수평 공차 준수"
    },
    {
        "folder": "15_[반-PC 슬래브] 패널반입 및 설치",
        "wbs": "9000-6-15",
        "name": "[반-PC 슬래브] 패널반입 및 설치",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀 / 궤도측량팀",
        "purpose": "공장 제작된 PST(Pre-cast Slab Track) 반-PC 슬래브 패널을 현장 반입하여 CP 측량 기준선에 따라 정밀 거치",
        "method": "전용 4점 인양 빔 사용, 스핀들 게이지(Spindle Gauge)로 높이 및 좌우 정열, 패널 간 격차(±1mm 이내) 정밀 조정",
        "output": "슬래브 패널 거치 검측서, 패널 정열 측량 성과표, 패널 외관 검수표",
        "key_focus": "스핀들 게이지 정밀 조정, 패널 높이/좌우 오차 ±1mm 이내 제어, 인양 시 균열 방지"
    },
    {
        "folder": "16_[PST] 전단앵커설치 및 충전재 주입",
        "wbs": "9000-6-16",
        "name": "[PST] 전단앵커설치 및 충전재 주입",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀 / 품질관리팀",
        "purpose": "PST 패널의 전단 앵커(Shear Anchor) 조립 및 하부/앵커 홀 고유동·무수축 충전재 주입을 통해 수평/수직 변위 완전 고정",
        "method": "앵커 홀 청소 및 에어 불기, 초고강도 무수축 그라우트 배합(f_ck ≥ 45 MPa), 하부 주입 파이프를 통한 기포 없는 압송 주입",
        "output": "전단앵커 그라우팅 시공 일지, 충전재 28일 압축강도 시험성적서, 충전밀도 검측서",
        "key_focus": "충전재 28일 압축강도 f_ck ≥ 45 MPa, 공기 갇힘(Air Void) 방지 압송 주입, 비파괴 음향 점검"
    },
    {
        "folder": "17_[TCL] 궤광 및 철근조립",
        "wbs": "9000-6-17",
        "name": "[TCL] 궤광 및 철근조립",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀 / 궤도측량팀",
        "purpose": "궤도 콘크리트층(TCL) 시공을 위한 레일-침목-체결구 궤광(Track Skeleton) 조립, 스핀들 궤간/캔트 정밀 정열 및 도상 철근 망 조립",
        "method": "1435mm 표준궤 정밀 공차(+3/-1mm) 세팅, 스핀들 게이지로 캔트(Max 160mm) 및 수평 조정, 절연 철근 받침대 설치하여 신호 궤도회로 단락 방지",
        "output": "TCL 궤광 조립 검측서, 궤도 정열(궤간/캔트/수평) 측량표, 철근 배근 검측서",
        "key_focus": "궤간 1435mm(+3/-1mm), 캔트(Max 160mm) 및 수평 오차 ±2mm 이내 정밀 조정, 철근 절연 성능 확보"
    },
    {
        "folder": "18_[TCL] 거푸집 설치",
        "wbs": "9000-6-18",
        "name": "[TCL] 거푸집 설치",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀",
        "purpose": "TCL 콘크리트 타설용 측면 거푸집 설치, 폼타이 보강, 박리제 도포 및 콘크리트 측압 대응 정밀 고정",
        "method": "측량 기준선에 맞춘 거푸집 거치, 수밀 고무 패킹 설치로 시멘트 풀 유출 방지, 타설 중 거푸집 밀림 방지 브레이싱 고정",
        "output": "거푸집 설치 검측서, 거푸집 선형 검측표, 박리제 도포 확인서",
        "key_focus": "거푸집 측압 변형 방지, 페이스트(시멘트 풀) 유출 차단 패킹, 스핀들 거치 부위 간섭 방지"
    },
    {
        "folder": "19_[TCL] 콘크리트 타설 및 양생",
        "wbs": "9000-6-19",
        "name": "[TCL] 콘크리트 타설 및 양생",
        "dept": "궤도 / 시공",
        "supervisor": "현장 공사팀 / 품질팀",
        "purpose": "TCL 궤도 콘크리트(f_ck ≥ 30 MPa) 타설, 고주파 바이브레이터 밀실 다짐, 스핀들 미세 재조정, 표면 마감 및 습윤 피막 양생",
        "method": "캔트 하상부에서 상상부 방향 연속 타설, 콜드조인트 방지, 타설 직후/직전 궤광 정열 재측정, 7일간 피막/습윤 양생 시행",
        "output": "TCL 콘크리트 타설 보고서, 콘크리트 강도 성적서(30 MPa 이상), 궤도 정열 최종 측량 성과표",
        "key_focus": "TCL 28일 강도 ≥ 30 MPa, 고주파 바이브레이터 밀실 다짐, 타설 중 궤각/캔트 실시간 재검측"
    },
    {
        "folder": "20_[레일용접] 가스 압접",
        "wbs": "9000-6-20",
        "name": "[레일용접] 가스 압접",
        "dept": "궤도 / 용접",
        "supervisor": "궤도용접팀 / NDT검사팀",
        "purpose": "기지 또는 현장에서 레일 단면을 가스 산소-아세틸렌 불꽃 또는 플래시버트로 가열하여 고압 압접(EN 14587) 및 100% NDT 검사 시행",
        "method": "EN 14587 규격 준수, 레일 단면 청정화, 자동 가압 및 업셋(Upset), 버(Burr) 정밀 전단, NDT(UT/MT) 및 1m 룰러 직선도(±0.2mm) 측정",
        "output": "가스압접 시공 기록지, NDT 비파괴검사 성과표(UT/MT), 레일 용접부 직선도 검측표",
        "key_focus": "EN 14587 공차 준수, 용접 직선도 수직/수평 ±0.2mm/1m 이내, 비파괴검사 100% 합격"
    },
    {
        "folder": "21_[레일용접] 테르밋 용접",
        "wbs": "9000-6-21",
        "name": "[레일용접] 테르밋 용접",
        "dept": "궤도 / 용접",
        "supervisor": "궤도용접팀 / NDT검사팀",
        "purpose": "본선 현장에서 장대레일 간 최종 연결부를 테르밋(산화철+알루미늄 분말, EN 14730) 반응(약 2500℃)으로 고품질 현장 용접 및 비파괴 검사",
        "method": "레일 갭(20~25mm) 세팅, 몰드 밀봉, 휘발유/가스 예열, 테르밋 반응 점화, 몰드 해체 및 핫 쉐어링, 정밀 연마 및 UT/PT 검사",
        "output": "테르밋 용접 결과 보고서, EN 14730 NDT 검사 성과표(UT/PT), 용접부 1m 직선도 검측서",
        "key_focus": "EN 14730 규격 준수, 반응온도 ~2500℃ 산화 반응 제어, 용접 1m 직선도 ±0.2mm, UT/PT 무결함"
    },
    {
        "folder": "22_[레일연마] 레일연마 or 밀링",
        "wbs": "9000-6-22",
        "name": "[레일연마] 레일연마 or 밀링",
        "dept": "궤도 / 마감",
        "supervisor": "현장 공사팀 / 궤도검측팀",
        "purpose": "도상 타설 및 용접 완료 후 레일 두부의 탈탄층(0.2~0.3mm) 제거, 용접부 둔덕 정밀 평탄화 및 트램 차륜 접촉 프로파일 최적화",
        "method": "자동 레일 연마차/밀링차 투입, 0.2~0.3mm 단계별 정밀 절삭, 표면 조도 및 조밀 프로파일 레이저 검측",
        "output": "레일 연마/밀링 시공 보고서, 레일 프로파일 레이저 검측 성과표, 표면 조도 성적서",
        "key_focus": "레일 초기 탈탄층 0.2~0.3mm 연마, 용접 둔덕 제거(±0.1mm 이내), 차륜-레일 프로파일 최적화"
    },
    {
        "folder": "23_후속공사 인수인계",
        "wbs": "9000-6-23",
        "name": "후속공사 인수인계",
        "dept": "궤도 / 인수인계",
        "supervisor": "사업관리단 / 궤도총괄소장",
        "purpose": "콘크리트도상 궤도공사 완공 후 신호(궤도회로/차량감지), 전전류(전차선/귀선), 건축, 차량 시험운전 분야로 정밀 시설물 인수인계",
        "method": "궤도 종합 검측 보고서(궤간, 캔트, 수평, 고저, 비틀림), 용접 NDT 기록, 콘크리트 강도 성적서 포괄 제출 및 현장 합동 점검",
        "output": "궤도시설물 인수인계서, 궤도 종합 검측 성과표, 공종 간 합동 점검 확인서",
        "key_focus": "궤간/캔트/틀림 최종 성과표 첨부, 신호/전기 인터페이스 100% 정상 작동 확인 후 서명 인계"
    }
]

def get_standard_html(act):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - {act['name']} 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- 헤더 -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS {act['wbs']} Standard</span>
                <span class="bg-emerald-500 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">KDS 47 30 00 & KCS 47 30 00</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{act['name']} 기술 표준서</h1>
            <p class="text-slate-300 mt-2 text-sm sm:text-base">"동탄도시철도 콘크리트도상 궤도공학 절대 시방 및 정량적 기술 기준 규격집"</p>
        </div>
    </div>

    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 과업 개요 및 목적 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">1.</span> 과업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">공종 / 담당부서</span>
                    <p class="font-bold text-slate-800 mt-1">{act['dept']} | {act['supervisor']}</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <span class="text-xs font-bold text-blue-700 uppercase">핵심 정밀 공차</span>
                    <p class="font-bold text-slate-800 mt-1">궤간 1435mm (+3,-1mm) | 직선도 ±0.2mm/1m</p>
                </div>
            </div>
            <div class="mt-4 bg-blue-50/60 p-5 rounded-xl border border-blue-100 text-sm space-y-2">
                <p><strong>🎯 과업 목적:</strong> {act['purpose']}</p>
                <p><strong>⚙️ 수행 방법:</strong> {act['method']}</p>
                <p><strong>📑 주요 산출물:</strong> {act['output']}</p>
            </div>
        </div>

        <!-- 2. KDS / KCS 궤도공사 정량적 기술 표준 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> KDS 47 30 00 & KCS 47 30 00 궤도공사 정량적 기술 표준
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-xs sm:text-sm text-left border-collapse border border-slate-200 rounded-lg">
                    <thead class="bg-blue-900 text-white">
                        <tr>
                            <th class="p-3 border border-slate-300">구분 (Category)</th>
                            <th class="p-3 border border-slate-300">공학 규격 (Engineering Spec)</th>
                            <th class="p-3 border border-slate-300">정량적 허용 공차 (Tolerance)</th>
                            <th class="p-3 border border-slate-300">관련 시방서 (Reference)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">표준 궤간 (Track Gauge)</td>
                            <td class="p-3 border">1,435 mm (트램 표준궤)</td>
                            <td class="p-3 border font-extrabold text-blue-700">+3.0 mm, -1.0 mm</td>
                            <td class="p-3 border">KDS 47 30 00 (궤도설계)</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">캔트 (Cant / Superelevation)</td>
                            <td class="p-3 border">최대 160 mm (곡선 R-속도 연동)</td>
                            <td class="p-3 border font-extrabold text-blue-700">설계 캔트 ±2.0 mm 이내</td>
                            <td class="p-3 border">KCS 47 30 00 (궤도공사)</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">확폭량 (Slack)</td>
                            <td class="p-3 border">곡선반경 R < 250m 구간 궤간 확폭</td>
                            <td class="p-3 border font-extrabold text-blue-700">S = 10 ~ 15 mm</td>
                            <td class="p-3 border">KDS 47 30 00</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">레일 규격 (Rail Profile)</td>
                            <td class="p-3 border">매설궤도: 51R1/60R2 홈레일<br>개활/슬래브: 60kg/m Vignole 레일</td>
                            <td class="p-3 border font-extrabold text-blue-700">단면 마모/변형 공차 엄수</td>
                            <td class="p-3 border">EN 14811 / KS R 9106</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">레일 용접 (Rail Welding)</td>
                            <td class="p-3 border">테르밋 용접(EN 14730)<br>가스압접/플래시버트(EN 14587)</td>
                            <td class="p-3 border font-extrabold text-blue-700">직선도 1m당 ±0.2 mm (수직/수평)</td>
                            <td class="p-3 border">EN 14730 / EN 14587</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">비파괴 검사 (NDT Inspection)</td>
                            <td class="p-3 border">UT(초음파), MT(자분), PT(침투), RT(방사선)</td>
                            <td class="p-3 border font-extrabold text-blue-700">100% 무결함 (No Defect)</td>
                            <td class="p-3 border">EN 14730 NDT 기준</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">도상 콘크리트 (TCL)</td>
                            <td class="p-3 border">Track Concrete Layer 28일 압축강도</td>
                            <td class="p-3 border font-extrabold text-blue-700">f_ck ≥ 30 MPa</td>
                            <td class="p-3 border">KCS 47 30 00 (콘크리트도상)</td>
                        </tr>
                        <tr>
                            <td class="p-3 font-bold bg-slate-50 border">PST 슬래브 충전재</td>
                            <td class="p-3 border">전단 앵커 무수축 그라우트 28일 강도</td>
                            <td class="p-3 border font-extrabold text-blue-700">f_ck ≥ 45 MPa</td>
                            <td class="p-3 border">Pre-cast Slab Spec</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 액티비티 특화 상세 기술 시방 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> [{act['name']}] 세부 시방 및 품질 관리 수칙
            </h2>
            <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 text-sm space-y-3">
                <div class="flex items-start gap-2">
                    <span class="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-0.5 rounded mt-0.5">핵심포인트</span>
                    <p class="text-slate-700"><strong>{act['key_focus']}</strong></p>
                </div>
                <ul class="space-y-2 text-slate-600 list-disc list-inside">
                    <li>KDS 47 30 00 궤도 설계기준 및 국토교통부 트램 건설 규칙을 엄격히 준수한다.</li>
                    <li>모든 시공 단계에서 1,435mm 정밀 궤간 유지와 스핀들 게이지 미세 조정을 통한 캔트/수평 정밀도를 확보한다.</li>
                    <li>도상 콘크리트 타설 시 고주파 바이브레이터 다짐을 실시하되 스핀들 기둥 및 매설 센서에 직접 접촉을 금지한다.</li>
                    <li>용접 작업 시 EN 14730 / EN 14587 규격에 따른 예열 및 반응온도(~2500℃) 제어를 철저히 이행한다.</li>
                </ul>
            </div>
        </div>

        <!-- 4. 협력사 시공/공사관리 자문 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">4.</span> 협력사 시공 / 공사관리 자문 (Subcontractor Advisory)
            </h2>
            <div class="bg-amber-50 p-5 rounded-xl border border-amber-200 text-sm text-slate-700 space-y-2">
                <p>📌 <strong>협력사 필수 이행 사항:</strong></p>
                <ul class="list-disc list-inside space-y-1 text-slate-600">
                    <li>궤도 정밀 측량사 및 테르밋 용접 전문 자격증(EN ISO 14730) 보유자 현장 전담 배치</li>
                    <li>자재 반입 시 공장 시험성적서 및 KCS 시방 규격 적합성 사전에 검수 승인 획득</li>
                    <li>콘크리트 타설 전 스핀들 게이지 이탈 방지 락킹 장치 확인 및 거푸집 측압 보강 검측 필수</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- 푸터 -->
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS {act['wbs']} | 궤도공학 콘크리트도상
    </div>
</div>
</body>
</html>
"""

def get_guideline_html(act):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - {act['name']} 작업 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- 헤더 -->
    <div class="bg-emerald-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS {act['wbs']} Guideline</span>
                <span class="bg-amber-400 text-slate-950 text-xs font-bold px-3 py-1 rounded-full">3단계 체계적 수행지침</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{act['name']} 작업 수행지침서</h1>
            <p class="text-emerald-200 mt-2 text-sm sm:text-base">"사전준비 ➡️ 본시공 ➡️ 검사마감 3단계 체계에 따른 현장 실무 가이드북"</p>
        </div>
    </div>

    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 작업 개요 및 준비사항 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">1.</span> 작업 개요 및 수행 목적 (Preparation & Overview)
            </h2>
            <div class="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100 text-sm space-y-2">
                <p><strong>🎯 수행 목적:</strong> {act['purpose']}</p>
                <p><strong>⚙️ 세부 방법:</strong> {act['method']}</p>
                <p><strong>📋 최종 산출물:</strong> {act['output']}</p>
            </div>
        </div>

        <!-- 2. 3단계 체계별 세부 작업 수행지침 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">2.</span> 3단계 체계별 세부 작업 수행절차 (Structured 3-Step Procedure)
            </h2>

            <div class="space-y-6 relative pl-6 border-l-4 border-emerald-500">
                <!-- Step 1: 사전 준비 단계 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 1. 사전 준비 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">하부 노반(HBS) 인수인계, CP 측량 및 자재/장비 세팅</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li>하부 HBS 강화노반 지지력(K70 ≥ 150 MPa/m) 및 평탄성 사전 검측 확인</li>
                        <li>광학 정밀 측량기를 이용한 궤도 중심선(CP) 및 기준점 검증 (허용 오차 ±1mm 이내)</li>
                        <li>60kg/m 레일, 51R1 홈레일, PST 슬래브 패널 및 테르밋 용제 반입 검수 및 정위치 배치</li>
                        <li>스핀들 게이지(Spindle Gauge), 정밀 궤간척, 고주파 바이브레이터 장비 정밀도 사전 교정</li>
                    </ul>
                </div>

                <!-- Step 2: 본 시공 단계 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 2. 본 시공 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">PST/TCL 궤광 조립, 스핀들 캔트 정밀 조정, 용접 및 콘크리트 타설</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>스핀들 게이지 조정:</strong> 1,435mm 표준궤(+3,-1mm) 유지 및 캔트(최대 160mm) 미세 정밀 조정</li>
                        <li><strong>레일 용접 조작:</strong> 테르밋 용접(EN 14730) 반응온도(~2500℃) 제어, 몰드 20~25mm 갭 예열 후 용융 주입</li>
                        <li><strong>도상 철근 조립:</strong> 신호 궤도회로 단락 방지용 절연 철근 받침대 배치 및 배근</li>
                        <li><strong>콘크리트 타설:</strong> TCL(f_ck ≥ 30 MPa) 및 PST 충전재(f_ck ≥ 45 MPa) 타설 시 고주파 바이브레이터 밀실 다짐, 콜드조인트 방지 연속 타설</li>
                    </ul>
                </div>

                <!-- Step 3: 검사 및 마감 단계 -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative">
                    <div class="absolute -left-[35px] top-4 bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded uppercase">Step 3. 검사 및 마감 단계</span>
                    <h3 class="text-base font-bold text-slate-900 mt-2 mb-2">궤도 정밀 검측, 레일 연마/밀링, 장대레일 릴리싱 및 최종 승인</h3>
                    <ul class="space-y-1.5 text-xs sm:text-sm text-slate-600 list-disc list-inside">
                        <li><strong>궤도 정밀 검측:</strong> 궤간(1435mm), 캔트(±2mm), 수평(±2mm), 고저(±2mm/10m), 비틀림(1.5mm/3m) 실시간 검측</li>
                        <li><strong>레일 초기 연마:</strong> 0.2~0.3mm 표면 탈탄층 절삭 및 용접 둔덕 제거 (프로파일 오차 ±0.1mm 이내)</li>
                        <li><strong>장대레일 릴리싱:</strong> 설정온도(t_0) 이행 및 유압 텐셔너를 통한 잔류 응력 제거 및 체결 조임</li>
                        <li><strong>품질 마감:</strong> 7일간 습윤 피막 양생, NDT 비파괴검사 성과표 작성 및 후속공종 승인 인계</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 3. 하자 예방 및 위험요인 관리 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-emerald-600 pb-2">
                <span class="text-emerald-600">3.</span> 하자 예방 및 LLBS 위험요인 관리 (Risk Management)
            </h2>
            <div class="bg-rose-50 p-5 rounded-xl border border-rose-200 text-sm text-slate-700 space-y-2">
                <p class="font-bold text-rose-900">⚠️ 주요 위험요인 및 방지대책:</p>
                <ul class="list-disc list-inside space-y-1 text-slate-600 text-xs sm:text-sm">
                    <li><strong>스핀들 게이지 이탈:</strong> 콘크리트 타설 중 진동에 의한 높이 변형 방지를 위해 이공구 잠금장치 상시 점검</li>
                    <li><strong>콜드조인트 발생:</strong> 레미콘 배차 간격을 30분 이내로 유지하고, 수직타설 인터페이스 부위 습윤 유지</li>
                    <li><strong>장대레일 좌굴:</strong> 레일 온도 변화에 따른 신축 관리 및 장대레일 설정온도(t_0) 범위 이외 시 시공 금지</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- 푸터 -->
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침서 | WBS {act['wbs']} | 궤도공학 콘크리트도상
    </div>
</div>
</body>
</html>
"""

def get_checklist_html(act):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘크리트도상 - {act['name']} 완료 검측 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- 헤더 -->
    <div class="bg-amber-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-amber-800 to-slate-900 opacity-60"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-amber-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS {act['wbs']} Checklist</span>
                <span class="bg-white text-amber-950 text-xs font-bold px-3 py-1 rounded-full">실시간 O/X 검측 도구</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{act['name']} 완료 검측 체크리스트</h1>
            <p class="text-amber-200 mt-2 text-sm sm:text-base">"궤도 틀림, 용접 NDT, 콘크리트 강도 및 LLBS 리스크 완벽 검증 체크리스트"</p>
        </div>
    </div>

    <div class="p-6 sm:p-10 space-y-8">
        <!-- 1. 정밀 궤도 검측 체크리스트 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">1.</span> 정밀 궤도 검측 및 시방 기준 체크항목 (Track Geometry Inspection)
            </h2>
            <div class="space-y-3 text-sm">
                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3 hover:bg-amber-50/50 transition-colors">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">궤간 (Track Gauge) 정밀도 준수 여부:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">표준궤 1,435 mm 기준 공차 (+3.0 mm, -1.0 mm) 이내임을 정밀 궤간척으로 확인하였는가?</p>
                    </div>
                </div>

                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3 hover:bg-amber-50/50 transition-colors">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">캔트 (Cant) 및 수평 (Cross-level) 정밀도:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">설계 캔트(최대 160mm) 대비 오차 ±2.0mm 이내이며, 좌우 레일 수평 오차가 ±2.0mm 이내인가?</p>
                    </div>
                </div>

                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3 hover:bg-amber-50/50 transition-colors">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">고저 (Longitudinal Level) 및 비틀림 (Twist) 오차:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">10m당 고저 오차 ±2.0mm 이내, 3m당 비틀림 오차 1.5mm 이내를 정밀 검측하였는가?</p>
                    </div>
                </div>

                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3 hover:bg-amber-50/50 transition-colors">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">레일 용접부 NDT 검사 및 1m 직선도:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">테르밋/가스압접 비파괴검사(UT/MT/PT) 100% 무결함 합격 및 1m 룰러 측정 시 수직/수평 ±0.2mm 이내인가?</p>
                    </div>
                </div>

                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3 hover:bg-amber-50/50 transition-colors">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">도상 콘크리트 및 충전재 압축강도:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">TCL 28일 압축강도 f_ck ≥ 30 MPa, PST 앵커 무수축 그라우트 f_ck ≥ 45 MPa 시험성적서를 확인했는가?</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. LLBS 집행단계 리스크 점검사항 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">2.</span> 집행단계 리스크 점검사항 (LLBS Risk Checklist)
            </h2>
            <div class="space-y-3 text-sm">
                <div class="p-4 bg-amber-50/60 rounded-xl border border-amber-200 flex items-start gap-3">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">장대레일 신축 및 좌굴 방지 조치:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">레일 설정온도(t_0) 측정 후 장력 보정(릴리싱)을 완료하고 체결볼트 규정 토크로 조였는가?</p>
                    </div>
                </div>

                <div class="p-4 bg-amber-50/60 rounded-xl border border-amber-200 flex items-start gap-3">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">고주파 다짐 및 매설 센서/스핀들 보호:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">바이브레이터 진동 시 신호 루프 센서 및 스핀들 게이지 지지대에 직접 타격이 없도록 조치하였는가?</p>
                    </div>
                </div>

                <div class="p-4 bg-amber-50/60 rounded-xl border border-amber-200 flex items-start gap-3">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">콜드조인트 방지 및 연속 타설 관리:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">레미콘 운반 지연이 없도록 제어하고, 이음부 발생 시 수평 조인트 처리 수칙을 준수했는가?</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. 협력사 공사관리 검측 확인사항 -->
        <div>
            <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2 border-b-2 border-amber-600 pb-2">
                <span class="text-amber-600">3.</span> 협력사 공사관리 검측 확인사항 (Subcontractor Verification)
            </h2>
            <div class="space-y-3 text-sm">
                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">용접원 자격 및 용재 관리:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">테르밋 용접원 전문 자격증(EN ISO 14730) 유효성과 용재 방수 보관 유효기간을 사전 검증했는가?</p>
                    </div>
                </div>

                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-3">
                    <input type="checkbox" class="w-5 h-5 mt-0.5 text-amber-600 rounded border-slate-300 focus:ring-amber-500 cursor-pointer">
                    <div>
                        <strong class="text-slate-900">스핀들 게이지 고정 및 거푸집 밀림 검사:</strong>
                        <p class="text-xs text-slate-600 mt-0.5">타설 직전 스핀들 게이지 락킹 상태와 거푸집 측압 브레이싱 고정 상태를 현장 확인하였는가?</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 4. 검측 서명란 -->
        <div class="mt-8 pt-6 border-t border-slate-200">
            <h3 class="text-sm font-bold text-slate-800 mb-4">✍️ 최종 검측 승인 서명란 (Inspection Sign-off)</h3>
            <div class="grid grid-cols-3 gap-4 text-center text-xs">
                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <p class="text-slate-500 font-bold">검측자 (시공사)</p>
                    <p class="mt-6 text-slate-400">성명: ____________ (서명)</p>
                </div>
                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <p class="text-slate-500 font-bold">확인자 (감리원)</p>
                    <p class="mt-6 text-slate-400">성명: ____________ (서명)</p>
                </div>
                <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <p class="text-slate-500 font-bold">승인자 (현장대리인)</p>
                    <p class="mt-6 text-slate-400">성명: ____________ (서명)</p>
                </div>
            </div>
        </div>
    </div>

    <!-- 푸터 -->
    <div class="bg-slate-900 text-slate-400 p-6 text-center text-xs border-t border-slate-800">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS {act['wbs']} | 궤도공학 콘크리트도상
    </div>
</div>
</body>
</html>
"""

total_files = 0
for act in activities:
    folder_path = os.path.join(base_dir, act['folder'])
    
    # 1. 표준서
    std_dir = os.path.join(folder_path, "표준서")
    os.makedirs(std_dir, exist_ok=True)
    act_clean_name = act['folder'].split('_', 1)[1] if '_' in act['folder'] else act['folder']
    std_file = os.path.join(std_dir, f"{act_clean_name}_표준서.html")
    with open(std_file, 'w', encoding='utf-8') as f:
        f.write(get_standard_html(act))
    total_files += 1

    # 2. 수행지침
    gui_dir = os.path.join(folder_path, "수행지침")
    os.makedirs(gui_dir, exist_ok=True)
    gui_file = os.path.join(gui_dir, f"{act_clean_name}_수행지침.html")
    with open(gui_file, 'w', encoding='utf-8') as f:
        f.write(get_guideline_html(act))
    total_files += 1

    # 3. 체크리스트
    chk_dir = os.path.join(folder_path, "체크리스트")
    os.makedirs(chk_dir, exist_ok=True)
    chk_file = os.path.join(chk_dir, f"{act_clean_name}_체크리스트.html")
    with open(chk_file, 'w', encoding='utf-8') as f:
        f.write(get_checklist_html(act))
    total_files += 1

print(f"Successfully generated/updated all {total_files} HTML files across 23 activities!")
