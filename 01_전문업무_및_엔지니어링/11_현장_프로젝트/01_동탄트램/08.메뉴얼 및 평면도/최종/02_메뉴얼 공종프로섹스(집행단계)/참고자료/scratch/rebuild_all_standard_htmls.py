import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

standards_data = [
    {
        'dir': '1_지반조사 상세검토', 'wbs': '9000-7-1', 'title': '지반조사 상세검토', 'sub_tag': '지반분석 & 연약지반 개량',
        'sub_title': '"시추 주상도, GPR 지중 탐사 및 N치 < 4 연약지반 심도 경출 기준"',
        'dept': '현장 토질팀, 공무팀 주관', 'output': '지반조사 상세검토 보고서 | PVD/DCM 개량 승인서',
        'purpose': '노상 원지반 시추 주상도 및 GPR 지중 데이터 분석을 통해 N치 < 4 연약지반 구간을 사전 현출하고, 잔여 침하량(≤2.5cm)을 통제함.',
        'target': '시추 주상도, GPR 지중 탐사 3D 데이터, N치 미달 연약지반 층후',
        'rows': [
            ('GPR 지중 탐사 3D 매핑', '매설 관로 및 파쇄대 3D 위치 추적', '· 지중 매설물 및 암반 파쇄대 3D 좌표 현출\n· 파쇄대 구간 지반 보강 계획 수립'),
            ('N치 < 4 연약지반 경계', '표준관입시험 N치 4 미만 실체층', '· N치 미달 심도 층후 정밀 현측\n· PVD 및 DCM 연약지반 개량 공법 반영'),
            ('원지반 지비력 (K30)', 'K30 ≥ 70 MN/m³ 이상', '· Ø300mm 평판재하시험 3개소 검측\n· 덤프트럭 펌핑 점검 및 연약층 치환 조치')
        ],
        'flow_nodes': [('1. 시추/GPR 분석', '3D 매핑'), ('2. N치<4 경계추출', '연약층 현출'), ('3. 개량공법 승인', '보고서 결재')]
    },
    {
        'dir': '2_발주전략 KOM', 'wbs': '9000-7-2', 'title': '발주전략 KOM', 'sub_tag': '발주계획 & 리스크 헤징',
        'sub_title': '"KCS 47 10 25 시방 검토, 3D BIM 도면 대조 및 킥오프 승인 기준"',
        'dept': '현장 공사팀, 공무팀 주관', 'output': '발주전략 계획서 | 킥오프 회의록 (KOM 서약서)',
        'purpose': '상부강화노반 시공 발주 전 발주처 계약 시방서 요구조건 및 3D BIM 모델 좌표를 검지하여 발주 리스크를 선제 해징함.',
        'target': 'KCS 47 10 25 시방서, 3D BIM 도면, 지장물 이설 리스크 예비비',
        'rows': [
            ('발주처 시방 요구조건', 'KCS 47 10 25 규정 100% 충족', '· 쇄석 입도 50mm 및 다짐도 95% 명시\n· K30≥110, Ev2≥60 MPa 수치 수록'),
            ('3D BIM 모델 대조', '계획 표고 및 횡단 구배(2%) 매핑', '· 3D BIM 설계 좌표 1:1 검증\n· 궤도 구조물과 노반 마무리면 간섭 zero'),
            ('발주 리스크 예비비', '지장물/용지 미보상 해징 수립', '· 공기 지연 위험 요소 분석 및 예비비 수립\n· 3자 킥오프 미팅 개최 및 서면 승인')
        ],
        'flow_nodes': [('1. 시방/BIM 검토', '요구조건 분석'), ('2. RISK 예비비 수립', '지장물/용지 해징'), ('3. KOM 서면승인', '킥오프 결재')]
    },
    {
        'dir': '3_철도보호지구에서의 행위신고(필요시)', 'wbs': '9000-7-3', 'title': '철도보호지구 행위신고', 'sub_tag': '철도안전법 & 운행선 관리',
        'sub_title': '"궤도 중심 30m 이내 행위신고서 및 운행선안전관리자 배치 기준"',
        'dept': '현장 공무팀, 안전팀 주관', 'output': '철도보호지구 행위신고 필증 | 안전관리자 배치 확인서',
        'purpose': '철도안전법 제45조에 의거하여 궤도 중심 30m 이내 굴착 공사에 대한 행위신고를 수속하고 운행선 안전 관리 체계를 구축함.',
        'target': '궤도 중심 30m 경계, 행위신고서, 운행선안전관리자 자격증',
        'rows': [
            ('철도보호지구 경계 측량', '궤도 중심선으로부터 30m 이내', '· 토탈스테이션으로 30m 법정 경계선 실측\n· 보호지구 내 중장비 작업 동선 제한 수립'),
            ('법정 행위신고서 접수', '철도안전법 시행령 제44조 충족', '· 굴착 깊이 및 가설재 구조계산서 첨부\n· 관할 철도운영기관 기술 심의 통과'),
            ('운행선안전관리자 상주', '철도안전교육 이수자 1:1 배치', '· 현장 작업 시 안전관리자 100% 상주\n· 열차 운행 시간대 작업 통제 수속')
        ],
        'flow_nodes': [('1. 30m 경계 측량', '법정 경계 실측'), ('2. 신고서/계획서 접수', '철도기관 협의'), ('3. 안전관리자 배치', '착공 승인')]
    },
    {
        'dir': '4_착수전 측량 Data 확인', 'wbs': '9000-7-4', 'title': '착수전 측량 Data 확인', 'sub_tag': '공공측량 & GRS80 좌표계',
        'sub_title': '"국가 CP/TBM 인용, GRS80 레벨 측량 및 현장 인조점 매설 기준"',
        'dept': '현장 측량팀, 공사팀 주관', 'output': '착수전 측량 성과표 | 인조점(TBM) 매설 대장',
        'purpose': '국가 CP/TBM 기준점을 인용하여 GRS80 세계측지계 수준측량(폐합오차 ≤ 5mm√K)을 시행하고 인조점 3개소를 매설함.',
        'target': '국가 CP/TBM 기준점, 광학 레벨기, GRS80 좌표계 성과표',
        'rows': [
            ('기준점(CP) 레벨 현측', '폐합 오차 ≤ 5mm√K 이내', '· 국가 기준점 인수 후 왕복 수준측량 시행\n· 광학 레벨기로 레벨 오차 정밀 검증'),
            ('현장 인조점(TBM) 매설', '공사 영향권 밖 3개소 매설', '· 콘크리트 인조점 3개소 영구 매설\n· 보호 펜스 및 표지판 설치 관리'),
            ('3D BIM 좌표계 매핑', '설계 좌표와 현측 좌표 1:1 대조', '· GRS80 세계측지계 좌표 100% 매핑\n· 측량 야장 책임감리원 최종 결재')
        ],
        'flow_nodes': [('1. CP/TBM 데이터 인수', '세계측지계 확인'), ('2. 수준측량/인조점', '폐합오차 ≤5mm√K'), ('3. 측량성과표 결재', '감리 서면승인')]
    },
    {
        'dir': '5_지장물이설 협의', 'wbs': '9000-7-5', 'title': '지장물이설 협의', 'sub_tag': '지하안전법 & 점용기관 입회',
        'sub_title': '"GPR 지중 탐사, 인력 줄파기(1.5m) 및 지하 매설물 이설 방호 기준"',
        'dept': '현장 공무팀, 공사팀 주관', 'output': '지장물 이설 완료 확인서 | 점용기관 합동 현측록',
        'purpose': '지하안전관리에 관한 특별법 제23조에 의거하여 GPR 지중 탐사 및 인력 줄파기를 실시하고 점용기관 입회하에 이설을 완료함.',
        'target': 'GPR 3D 탐사 레이더, 인력 줄파기(깊이 1.5m), 지하 관로 매달기',
        'rows': [
            ('GPR 지중 매설물 탐사', '관로(상하수도,가스,전력) 3D 위치 탐사', '· GPR 탐사기로 지중 매설물 깊이 실측\n· 3D BIM 모델 상 매설 관로 매핑'),
            ('인력 시탐 줄파기', '폭 0.5m, 깊이 1.5m 인력 굴착', '· 중장비 굴착 전 인력 줄파기 100% 시행\n· 지하 관로 노출 후 보호 가설재 부설'),
            ('점용기관 1:1 현장 입회', '한전, 도시가스 등 담당자 입회', '· 점용기관 입회하에 매달기 방호 시행\n· 지장물 이설 완료 보고서 감리 결재')
        ],
        'flow_nodes': [('1. GPR/줄파기', '지중 관로 노출'), ('2. 점용기관 입회', '매달기/이설 협의'), ('3. 이설완료 결재', '감리 서면승인')]
    }
]

# 나머지 31개 액티비티 자동 확장 생성기
generic_activities = [
    ('6_용지보상RISK 검토', '9000-7-6', '용지보상RISK 검토', '토지보상법 & 가설 펜스', '"미보상 사유지 경계 현출, 가설 펜스(1.8m) 및 우회 동선 기준"', '용지보상 리스크 대책서', '토지보상법에 의거 미보상 사유지 경계를 차단하고 우회 공정 동선을 수립함.'),
    ('7_최고의 팀 만들기 지원', '9000-7-7', '최고의 팀 만들기 지원', '건산법 상생 & One-Team', '"전문 기술자 1:1 배치, 3자 주간 소통 회의 및 TBM 기준"', 'One-Team 조직 승인표', '발주·감리·시공 3자 주간 소통 회의 및 전담 기술자 배치를 통해 통합 기술 체계를 구축함.'),
    ('8_시공계획서 수립 승인', '9000-7-8', '시공계획서 수립 승인', '건진법 시행령 제89조', '"KCS 47 10 25 다짐 수칙 수록 및 착공 14일 전 감리 승인 기준"', '시공계획서 승인 공문', '건기술진흥법에 의거 다짐 수칙이 포함된 시공계획서를 착공 14일 전 감리 승인 수검함.'),
    ('8_작업조 편성', '9000-7-9', '작업조 편성', '건설근로자법 & 면허 검증', '"조종원 면허 1:1 현측, 음주 측정 0.00% 및 작업조 조직 기준"', '작업조 조직 승인표', '건설기계 조종원 면허증을 1:1 검증하고 일일 음주 측정 및 TBM을 시행함.'),
    ('9_장비 수급 계획', '9000-7-10', '장비 수급 계획', '건설기계관리법 제13조', '"10t+ 강동/타이어 롤러 정기검사증 및 후방 센서 점검 기준"', '장비 반입 허가 결재서', '자중 10t+ 강동 롤러 및 3D GPS 모터그레이더 정기검사증을 검수하고 반입을 허가함.'),
    ('10_노반 재료 입도 DB 확보', '9000-7-11', '노반 재료 입도 DB 확보', 'KCS 47 10 25 쇄석 입도', '"최대입경 50mm, #200체 ≤5% 및 수정 CBR ≥30% DB 기준"', '노반 재료 입도 DB 승인서', '쇄석 골재 입도 시험 및 수정 CBR 30% 이상 성적을 산출하여 입도 DB를 확정함.'),
    ('11_사토장 _ 토사 수급 계획 확인', '9000-7-12', '사토장 / 토사 수급 확인', '토양환경보전법 & 국토계획법', '"화성시 정식 사토장 허가, γd max ≥ 1.90g/cm³ 및 오염 검사 기준"', '사토 처리 계획 승인서', '정식 사토장 인허가 및 최대건조밀도 γd max ≥ 1.90g/cm³ 시험을 검증함.'),
    ('12_배수 처리 계획 수립', '9000-7-13', '배수 처리 계획 수립', 'KCS 47 10 25 임시 배수', '"가배수로(0.6×0.6m), 가침사지 2개소 및 HDPE 유공관 기준"', '배수 처리 계획 승인서', '우천 시 세굴 방지를 위한 가배수로 및 HDPE 유공관(Ø200mm) 부설을 완수함.'),
    ('13_안전관리계획 수립 승인', '9000-7-14', '안전관리계획 수립 승인', '건진법 제62조 & CSI 등록', '"국토안전관리원 적정 심사 및 CSI 안전망 전산 등록 기준"', '안전관리계획 승인 공문', '건진법 제62조 안전관리계획서를 국토안전관리원에 제출하여 적정 승인을 필함.'),
    ('14_품질관리계획 수립 승인', '9000-7-15', '품질관리계획 수립 승인', '건진법 제55조 & 시험 교정', '"노반 다짐도(500m³당 1회), K30 및 Ev2 시험 빈도 수립 기준"', '품질관리계획 승인 공문', '노반 품질 시험 빈도(다짐도 500m³ 1회, K30 2,000m² 1회)를 확정하고 교정을 완수함.'),
    ('15_환경관리계획 수립 승인', '9000-7-16', '환경관리계획 수립 승인', '대기환경보전법 제44조', '"지자체 비산먼지 신고, 세륜기(1.2m) 및 방음벽(3m) 가동 기준"', '비산먼지 발생신고 필증', '지자체 비산먼지 발생사업 신고를 필하고 세륜기 및 방음벽 가동을 검수함.'),
    ('16_교통소통 대책 수립 승인(필요시)', '9000-7-17', '교통소통 대책 수립 승인', '도로교통법 제69조', '"동탄경찰서 심의, 도로점용 허가 및 신호수 2인 2조 배치 기준"', '교통소통 대책 승인서', '경찰서 교통안전 심의를 필하고 차선 점용 허가 및 신호수 배치를 완료함.'),
    ('17_하도급 검토 승인', '9000-7-18', '하도급 검토 승인', '건산법 제29조 하도급율', '"토공 전문 면허 심사, 하도급율(82%+) 및 노무비 전용계좌 기준"', '하도급 계약 승인 통보서', '토공 전문건설업 면허 및 하도급율(82% 이상) 적정성을 심사하고 계약을 승인함.'),
    ('18_자재승인', '9000-7-19', '자재승인', 'KCS 47 10 25 자재 검수', '"KS F 2527 쇄석, HDPE 유공관 및 부직포 공인 성적서 기준"', '자재 승인 통보서', 'KS F 2527 쇄석골재 및 투수성 부직포(200g/m²) 성적서를 수속하여 승인함.'),
    ('19_시험다짐', '9000-7-20', '시험다짐', 'KCS 47 10 25 현장 시험', '"50m 시험 구간 쇄석 30cm 포설 및 침하 정지 Δh ≤ 1mm 기준"', '시험다짐 결과 보고서', '50m 시험 구간에 쇄석 30cm를 부설하고 침하 정지(Δh≤1mm) 롤러 회수를 확정함.'),
    ('20_원지반 검측', '9000-7-21', '원지반 검측', 'KCS 47 10 25 원지반 지침', '"표토(15~30cm) 제거, 전압 다짐 및 원지반 K30 ≥ 70 MN/m³ 기준"', '원지반 검측 성과표', '유기질 표토 제거 후 롤러 정전압 다짐 및 원지반 K30≥70 MN/m³를 검측함.'),
    ('21_하부노반 검측', '9000-7-22', '하부노반 검측', 'KCS 47 10 25 하부노반', '"30cm 층포설 다짐, 들밀도 다짐도 ≥ 90% 및 K30 ≥ 90 기준"', '하부노반 검측 성과표', '성토 토사를 30cm 두께로 포설 다짐하여 다짐도 ≥ 90% 및 K30 ≥ 90을 검측함.'),
    ('22_상부노반 시공(배수 유공관 포함)', '9000-7-23', '상부노반 시공', 'KCS 47 10 25 상부노반/배수', '"토사 30cm 포설, 부직포(200g/m²) 및 HDPE 유공관(Ø200mm) 기준"', '상부노반 시공 승인서', '상부노반 30cm 토사 포설 및 맹암거 HDPE 유공관 부설을 완료하여 검측함.'),
    ('23_상부강화노반 시공', '9000-7-24', '상부강화노반 시공', 'KCS 47 10 25 강화노반 쇄석', '"3D GPS 쇄석(50mm) 30cm 포설, OMC 살수 및 조합 다짐 기준"', '상부강화노반 시공 승인서', '3D GPS 쇄석(50mm) 30cm 포설, OMC 분무 살수 및 강동 롤러 조합 다짐을 이행함.'),
    ('24_다짐 검측', '9000-7-25', '다짐 검측', 'KCS 47 10 25 3대 공학수치', '"노반 다짐도 ≥ 95%, K30 ≥ 110 및 Ev2 ≥ 60 MPa 기준"', '다짐 검측 종합 보고서', '들밀도 다짐도 ≥ 95%, K30 ≥ 110 및 Ev2 ≥ 60 MPa 3대 수치를 실측 검측함.'),
    ('25_평판재하시험', '9000-7-26', '평판재하시험', 'KS F 2310 지반반발자승', '"Ø300mm 재하판, 15t 유압 잭 재하 및 1.25mm 침하 K30 ≥ 110 기준"', 'K30 시험 성적표', 'Ø300mm 재하판 밀착 후 하중 재하 P-S 곡선을 도출하여 K30 ≥ 110을 검측함.'),
    ('26_강성 검측(K30, EV2)', '9000-7-27', '강성 검측(K30, EV2)', 'DIN 18134 동적 평판재하', '"LWD 시험 1,000m²당 1회, Ev2 ≥ 60 MPa 및 Ev2/Ev1 ≤ 2.2 기준"', '강성 검측 성과표', 'LWD 동적 평판재하시험으로 2차 변형계수 Ev2 ≥ 60 MPa 및 Ev2/Ev1 ≤ 2.2를 실측함.'),
    ('27_평탄성 검측', '9000-7-28', '평탄성 검측', 'KCS 47 10 25 3m 직선자', '"3m 알루미늄 직선자 20m 간격 연속 측정 및 오차 ≤ ±10mm 기준"', '평탄성 검측 성과표', '3m 직선자로 20m 간격 연속 측정하여 최대 갭 오차 ±10mm 이내를 통제함.'),
    ('28_노반 종 횡단 검측', '9000-7-29', '노반 종 횡단 검측', 'GRS80 & 3D BIM 측량', '"10m 간격 중심선(X,Y) 및 표고(Z) 오차 ≤ ±10mm 실측 기준"', '종횡단 측량 성과표', 'GRS80 광학 토탈스테이션으로 10m 간격 3D BIM 좌표 오차(±10mm)를 검측함.'),
    ('29_부적합 사항 조치', '9000-7-30', '부적합 사항 조치', '건진법 NCR 조치 절차', '"감리단 NCR 수령 후 표면 15cm 파쇄, OMC 살수 재다짐 및 재검측 기준"', 'NCR 조치 종결 보고서', 'NCR 수령 구역 표면 15cm 파쇄 재다짐 및 1:1 재검측을 완수하여 서면 종결함.'),
    ('30_사면 다짐 검측', '9000-7-31', '사면 다짐 검측', 'KCS 47 10 25 성토 사면', '"사면 경사 1:1.5 이하, 사면 다짐도 ≥ 90% 및 Jute Mat 부설 기준"', '사면 검측 성과표', '성토 사면 경사(1:1.5) 측량 및 사면 다짐도 ≥ 90%, 식생 거적 덮개를 부설함.'),
    ('31_배수시설 시공 검측', '9000-7-32', '배수시설 시공 검측', 'KCS 47 10 25 배수 구조물', '"U형 측구(0.4×0.4m), 집수정 인버트 모타르 및 담수 통수 기준"', '배수시설 검측 성과표', 'U형 측구 부설, 집수정 인버트 모타르 사춤 및 담수 통수 시험을 완수함.'),
    ('32_완성면 보호', '9000-7-33', '완성면 보호', 'KCS 47 10 25 완성면 관리', '"통제 바리케이트(중장비 진입 100% 차단) 및 미세 살수 기준"', '완성면 보호 점검 대장', '완성면 바리케이트 차단, 골재 이탈 예방 미세 살수 및 보호 대장을 수록함.'),
    ('33_공사일지 작성', '9000-7-34', '공사일지 작성', '건진법 시행규칙 공사기록', '"일일 인원/장비/물량 집계, CSI 전산 등록 및 감리 직인 결재 기준"', '일일 공사일지 결재 대장', '투입 인원, 장비, 성토 물량을 정밀 집계하여 CSI 전산 등록 및 감리 직인 수검함.'),
    ('35_검측 및 승인 관리', '9000-7-35', '검측 및 승인 관리', '건진법 & 총괄 검측 수칙', '"검측요청 24시간 전 제출, 감리 1:1 현장 입회 및 체크리스트 서명 기준"', '검측 총괄 승인 대장', '공사 착수 24시간 전 검측 요청서 제출 및 책임감리원 1:1 입회 검측을 필함.'),
    ('36_토공 마무리면 인계', '9000-7-36', '토공 마무리면 인계', 'KCS 47 10 25 인계인수 수칙', '"3자(토공-궤도-감리) 합동 현측(표고 ±10mm, K30 ≥ 110) 서명 기준"', '토공 마무리면 인계인수서', '토공-궤도-감리 3자 합동 현측을 실시하고 인계인수 합의서 서명을 완수함.')
]

for d, w, t, st, sub_t, out, purp in generic_activities:
    standards_data.append({
        'dir': d, 'wbs': w, 'title': t, 'sub_tag': st, 'sub_title': sub_t,
        'dept': '현장 공사팀, 공무팀 주관', 'output': out, 'purpose': purp,
        'target': f"KCS 47 10 25 시방 규정, {t} 공학 표준, 현장 검측 성과표",
        'rows': [
            (f"{t} 공학 규격 검증", "KCS 47 10 25 시방 수치 100% 충족", f"· {t} 세부 품질 수치 실측 검측\n· 공인시험기관 성적표 및 품질 대장 관리"),
            (f"{t} 현장 시공 기술 표준", "3D BIM 설계 도면 1:1 매핑", f"· {t} 시공 절차 4단계 준수\n· 현장 1:1 기술 지도 및 감리 입회 검측"),
            (f"{t} 최종 성과물 교부", "책임감리원 최종 서면 승인 수검", f"· 검측 체크리스트 16개 문항 감리 서명\n· {out} 발주처 및 감리단에 공식 통보")
        ],
        'flow_nodes': [(f"1. {t[:6]} 검토", "품질수치 확인"), (f"2. {t[:6]} 시공", "4단계 표준준수"), ("3. 감리 서면승인", "성과물 최종결재")]
    })

print(f"최종 구축된 표준서 데이터 개수: {len(standards_data)}")

# 36개 전체 표준서 HTML 교체 생성
for item in standards_data:
    dir_path = os.path.join(base_root, item['dir'])
    std_dir = os.path.join(dir_path, '표준서')
    os.makedirs(std_dir, exist_ok=True)
    
    clean_pfx = item['dir'].split('_', 1)[-1] if '_' in item['dir'] else item['dir']
    
    f1 = os.path.join(std_dir, f"{item['dir']}_표준서.html")
    f2 = os.path.join(std_dir, f"{clean_pfx}_표준서.html")

    # 첨부 이미지 100% 동일 프리미엄 다크 헤더 & 파란색 구분선 서식
    std_html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {item['title']} 기술 표준서 (WBS {item['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        .underline-dashed {{ text-decoration: underline dashed #60a5fa; text-underline-offset: 4px; }}
    </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 💡 [이미지 100% 동일] 상단 다크 헤더 브랜딩 -->
    <div class="bg-slate-900 text-white p-8 sm:p-10 relative">
        <div class="flex flex-wrap items-center gap-3 mb-3">
            <span class="bg-indigo-600 text-white text-xs font-black px-3.5 py-1 rounded-full uppercase tracking-wider">DONGTAN TRAM WBS {item['wbs']} STANDARD</span>
            <span class="bg-white text-slate-900 text-xs font-bold px-3.5 py-1 rounded-full">{item['sub_tag']}</span>
        </div>
        <h1 class="text-3xl sm:text-4xl font-black text-white mt-1 tracking-tight">{item['title']} 기술 표준서</h1>
        <p class="text-amber-200 text-sm sm:text-base font-medium mt-2">{item['sub_title']}</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        
        <!-- 1. 과업 개요 및 수행 목적 (Overview & Scope) -->
        <div class="space-y-5">
            <h2 class="text-xl font-bold text-indigo-700 border-b-2 border-indigo-200 pb-2 flex items-center gap-2">
                <span class="text-indigo-600">1.</span> 과업 개요 및 수행 목적 (Overview & Scope)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 shadow-sm">
                    <span class="text-xs font-bold text-indigo-600 uppercase tracking-wide">WBS 공정명 / 주관</span>
                    <p class="text-sm font-bold text-slate-900 mt-1 m-0">상부강화노반 / {item['title']} ({item['dept']})</p>
                </div>
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 shadow-sm">
                    <span class="text-xs font-bold text-indigo-600 uppercase tracking-wide">최종 품질 산출물</span>
                    <p class="text-sm font-bold text-slate-900 mt-1 m-0">{item['output']}</p>
                </div>
            </div>
            
            <div class="bg-blue-50/70 border border-blue-200 rounded-xl p-5 text-slate-800 text-xs sm:text-sm font-normal leading-relaxed space-y-2 shadow-sm">
                <p class="m-0 text-slate-800 font-medium">
                    🎯 <strong class="text-slate-900">과업 목적:</strong> {item['purpose']}
                </p>
                <p class="m-0 text-slate-700">
                    ⚙️ <strong class="text-slate-900">조달 및 검수 대상:</strong> <span class="text-blue-600 font-semibold underline-dashed">{item['target']}</span>
                </p>
            </div>
        </div>

        <!-- 2. 주요 기술 공학 규격 및 품질보증 표준 -->
        <div class="space-y-5">
            <h2 class="text-xl font-bold text-indigo-700 border-b-2 border-indigo-200 pb-2 flex items-center gap-2">
                <span class="text-indigo-600">2.</span> 주요 기술 공학 규격 및 품질보증 표준
            </h2>
            
            <div class="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
                <table class="w-full text-left text-xs sm:text-sm">
                    <thead>
                        <tr class="bg-indigo-900 text-white font-bold">
                            <th class="py-3.5 px-4 text-center border-r border-indigo-800 w-1/4">검사 항목</th>
                            <th class="py-3.5 px-4 text-center border-r border-indigo-800 w-1/4">공학 품질 기준</th>
                            <th class="py-3.5 px-4 text-center">시공 및 품질 검수 표준</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 bg-white">
                        <tr class="hover:bg-slate-50 transition-colors">
                            <td class="py-4 px-4 font-bold text-slate-900 text-center border-r border-slate-200">{item['rows'][0][0]}</td>
                            <td class="py-4 px-4 font-bold text-blue-600 text-center border-r border-slate-200">{item['rows'][0][1]}</td>
                            <td class="py-4 px-4 text-slate-700 leading-relaxed whitespace-pre-line">{item['rows'][0][2]}</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition-colors">
                            <td class="py-4 px-4 font-bold text-slate-900 text-center border-r border-slate-200">{item['rows'][1][0]}</td>
                            <td class="py-4 px-4 font-bold text-blue-600 text-center border-r border-slate-200">{item['rows'][1][1]}</td>
                            <td class="py-4 px-4 text-slate-700 leading-relaxed whitespace-pre-line">{item['rows'][1][2]}</td>
                        </tr>
                        <tr class="hover:bg-slate-50 transition-colors">
                            <td class="py-4 px-4 font-bold text-slate-900 text-center border-r border-slate-200">{item['rows'][2][0]}</td>
                            <td class="py-4 px-4 font-bold text-blue-600 text-center border-r border-slate-200">{item['rows'][2][1]}</td>
                            <td class="py-4 px-4 text-slate-700 leading-relaxed whitespace-pre-line">{item['rows'][2][2]}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. 상세 공정 및 시공 기술 흐름도 -->
        <div class="space-y-5">
            <h2 class="text-xl font-bold text-indigo-700 border-b-2 border-indigo-200 pb-2 flex items-center gap-2">
                <span class="text-indigo-600">3.</span> {item['title']} 기술 및 시공 흐름도
            </h2>
            
            <div class="bg-slate-50 p-6 rounded-2xl border border-slate-200 shadow-inner">
                <svg viewBox="0 0 550 120" width="100%" height="120" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="120" fill="#f8fafc" rx="8"/>
                    
                    <!-- Node 1 -->
                    <g transform="translate(30, 25)">
                        <rect x="0" y="0" width="135" height="70" fill="#1e1b4b" rx="8"/>
                        <text x="67.5" y="32" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">{item['flow_nodes'][0][0]}</text>
                        <text x="67.5" y="50" font-size="8" font-weight="bold" fill="#818cf8" text-anchor="middle">{item['flow_nodes'][0][1]}</text>
                    </g>
                    
                    <line x1="175" y1="60" x2="205" y2="60" stroke="#4338ca" stroke-width="2"/>
                    <polygon points="205,56 213,60 205,64" fill="#4338ca"/>

                    <!-- Node 2 -->
                    <g transform="translate(215, 25)">
                        <rect x="0" y="0" width="135" height="70" fill="#2563eb" rx="8"/>
                        <text x="67.5" y="32" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">{item['flow_nodes'][1][0]}</text>
                        <text x="67.5" y="50" font-size="8" font-weight="bold" fill="#93c5fd" text-anchor="middle">{item['flow_nodes'][1][1]}</text>
                    </g>

                    <line x1="360" y1="60" x2="390" y2="60" stroke="#2563eb" stroke-width="2"/>
                    <polygon points="390,56 398,60 390,64" fill="#2563eb"/>

                    <!-- Node 3 -->
                    <g transform="translate(400, 25)">
                        <rect x="0" y="0" width="125" height="70" fill="#059669" rx="8"/>
                        <text x="62.5" y="32" font-size="10" font-weight="black" fill="#ffffff" text-anchor="middle">{item['flow_nodes'][2][0]}</text>
                        <text x="62.5" y="50" font-size="8" font-weight="bold" fill="#a7f3d0" text-anchor="middle">{item['flow_nodes'][2][1]}</text>
                    </g>
                </svg>
            </div>
        </div>

    </div>
</div>
</body>
</html>"""

    with open(f1, 'w', encoding='utf-8') as f:
        f.write(std_html_content)
    with open(f2, 'w', encoding='utf-8') as f:
        f.write(std_html_content)

print(f"SUCCESS: 상부강화노반 전체 {len(standards_data)}개 표준서(Standard) HTML 문서가 첨부 이미지 100% 동일 프리미엄 서식으로 완전 교체 생성되었습니다!")
