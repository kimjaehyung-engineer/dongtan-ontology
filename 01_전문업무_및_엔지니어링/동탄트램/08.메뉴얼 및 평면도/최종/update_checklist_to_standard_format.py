import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반"

# Compile master data again for 36 activities
master_ground_truth = {
    1: {
        "title": "지반조사 상세검토",
        "chk_sum": "N치<4 연약지반 개량 범위, PBT 원지반 지지력 K30 확인, 암반 파쇄대 50cm 치환 계획 승인",
        "chk_items": [
            "지반 물리탐사(GPR, 탄성파) 성과표 및 N치 < 4 연약지반 구간 도면 대조 분석 완료 여부",
            "원지반 K30 지지력계수 및 허용응력 Qa ≥ 150 kN/m² 만족 여부",
            "절토 구간 암반 경계 및 파쇄대 치환 깊이(최소 50cm 이상) 도면 반영 및 감리단 승인 여부"
        ]
    },
    2: {
        "title": "발주전략 KOM",
        "chk_sum": "품질이행 확약서 날인, 다짐 장비 반입 계약서 확인, K30 ≥ 110 MN/m³ 품질기준 의결",
        "chk_items": [
            "강화노반 CPM 마스터 스케줄 및 궤도 인계 목표일 일원화 협약 체결 여부",
            "1층 포설 다짐 두께 30cm 이하 및 다짐 장비 조합(10t 진동, 15t 타이어) 확정 서약 여부",
            "쇄석 혼합 골재 일일 500m³ 이상 반입 수급 계약서 및 공급업체 품질 성적서 확인 여부"
        ]
    },
    3: {
        "title": "철도보호지구에서의 행위신고(필요시)",
        "chk_sum": "철도공단 행위신고 승인 필증, 레일 침하핀 및 경사계 계측 모니터링, 철도운행안전원 상주 확인",
        "chk_items": [
            "국가철도공단 철도보호지구 행위신고 최종 허가 승인 공문 수신 완료 여부",
            "기존 선로 레일 침하핀 및 경사계 10m 간격 설치 및 허용 침하량 ±5mm 이내 실시간 계측 여부",
            "철도운행안전원 현장 100% 상주 배치 및 장비 회전 반경 내 전차선 방호망 시공 완료 여부"
        ]
    },
    4: {
        "title": "착수전 측량 Data 확인",
        "chk_sum": "GRS80 기준점 매핑, TBM 100m 간격 가설, 수준 측량 오차 ±10mm 이내 검측 성적서",
        "chk_items": [
            "GRS80 세계측지계 TBM/CP 기준점 100% 매핑 및 가설 TBM 100m 간격 설치 여부",
            "선로 중심선 계획고 오차 ±10mm 이내 정밀 수준 측량 검속 완료 여부",
            "종횡단 측량 야장 및 CAD 지형단면도 작성 후 감리단 서명 승인 여부"
        ]
    },
    5: {
        "title": "지장물이설 협의",
        "chk_sum": "3D BIM 간섭 검증, 강화노반 직하부 관로 이격거리 H≥1.5m 만족, 위수탁 계약 승인",
        "chk_items": [
            "5대 지장물 위탁관리기관(한전, KT, 삼천리, 난방, 맑은물)과 합동 3D BIM Clash Zero 간섭 검증을 진행한다.",
            "강화노반 직하부 신규 관로 매설 구간의 수평 및 수직 이격거리 H≥1.5m 확보 여부를 검속한다.",
            "이설 범위 확정에 따른 위수탁 설계변경 요건 및 사후 정산(Provisional Sum) 요건을 합의서로 작성한다."
        ]
    },
    6: {
        "title": "용지보상RISK 검토",
        "chk_sum": "미보상 필지 현장 경계목 설치, 무단진입 차단 가설 펜스 설치, 용지 매수 관리대장 확인",
        "chk_items": [
            "토지 수용 대장 조서를 분석하여 노반 시공 폭 및 비탈면 경계 내 미보상 사유지 필지를 전수 파악한다.",
            "현장 경계 측량을 시행하여 미보상 사유지 부지 구역에 붉은색 목재 기준 말뚝을 고정한다.",
            "공사 장비의 사유지 무단 진입을 방지하는 높이 1.8m 이상의 차단 가설 펜스 및 출입 금지 안내판을 시공한다."
        ]
    },
    7: {
        "title": "최고의 팀 만들기 지원",
        "chk_sum": "유자격 시험원 면허 대조, 다짐장비 조종원 경력증명서 확인, 시공전 품질 교육 서명",
        "chk_items": [
            "토공 기술사 및 PBT/PFWD 시험 전문 유자격 시험원에 대한 건설재료시험기사 면허 원본을 대조 심사한다.",
            "진동 롤러, 모터 그레이더 등 주요 다짐 장비 조종원의 적격성 및 건설기계 조종면허를 검증한다.",
            "강화노반 1층 다짐 두께 30cm 및 품질 기준(K30)을 현장 근로자에게 소집 품질 교육 시행한다."
        ]
    },
    8: {
        "title": "연약지반 처리공법 검토(필요시)",
        "chk_sum": "PVD/DCM 지반개량 시공계획 승인, 계측 침하판 레벨 측정, 허용 잔류침하 2.5cm 이내 판정",
        "chk_items": [
            "연약지반 설계기준 KDS 11 30 00에 근거하여 PVD 배수 간격 및 DCM 시멘트 배합 조건을 심사 결정한다.",
            "성토 구간 50m 간격 계측 침하판 및 간극수압계를 고정 설치하고 실시간 계측 레벨을 기록한다.",
            "침하 수렴 계측 곡선을 분석하여 트램 궤도 허용 잔류침하량 2.5cm 이하 최종 도달 여부를 확인한다."
        ]
    },
    9: {
        "title": "토공 유동표 확인",
        "chk_sum": "Mass-Curve 토공 유동 선도 확인, 평균 운반거리 5km 이내 지정 사토장 반입 일치",
        "chk_items": [
            "종단 마무리면 계획고 기준 Mass-Curve 계산식을 적용하여 절토-성토 간 토량 수량 균형을 대조한다.",
            "덤프트럭 평균 운반거리 5km 이내 최적 유동 노선 매핑 및 가설 통행로 승인 상태를 확인한다.",
            "지정 사토장 및 토취장의 일일 반출입 운반 물량 기록 및 전산 대장의 정합성을 전수 대조한다."
        ]
    },
    10: {
        "title": "기공승낙 적정성 검토",
        "chk_sum": "임시 사용 기공승낙서 100% 확보, 지적 편집도 기준 경계 실측, 미승낙 필지 차단 펜스",
        "chk_items": [
            "가설 진입 도로 및 가설 침사지 부지 내 사유 부지 필지 소유자의 기공승낙서 원본을 수집 검속한다.",
            "기공승낙서 첨부 인감증명서의 진위 여부 및 토지대장 상 실소유자 정합성을 대조 확인한다.",
            "미승낙 사유 부지에 대한 중장비 무단 침입을 차단하는 가설 펜스 및 출입 방지 철망을 시공한다."
        ]
    },
    11: {
        "title": "폐기물처리계획 수립",
        "chk_sum": "올바로시스템 배출자 신고증 구비, 폐기물 적재함 비산방지막, 보관 기한(90일) 준수",
        "chk_items": [
            "건설폐기물의 재활용촉진에 관한 법률 및 폐기물관리법에 따른 현장 분리 배출 계획을 수립한다.",
            "환경부 올바로시스템(Allbaro)에 접속하여 배출자 자격 등록 및 배출자 신고증 승인을 획득한다.",
            "현장 야적 폐기물 보관소의 우수 유입 방지 차수 비닐 및 비산방지 방진망을 고정 설치한다."
        ]
    },
    12: {
        "title": "철도운행협의(필요시)",
        "chk_sum": "야간 차단작업 승인서 확보, 철도운행안전원 상주 여부, 비상 적색 신호수 배치 확인",
        "chk_items": [
            "철도 인접 야간 차단작업 시간대(01:00~04:30) 승인을 위해 한국철도공사 및 관련 지자체 협의 공문을 구비한다.",
            "철도운행안전원의 무전기(VHF) 주파수 동기화 상태 및 운행선 인접 안전 이수증을 대조 심사한다.",
            "열차 진입 전 작업 장비의 안전한 선로 외곽 가설 통행로 퇴피 및 비상 신호수(적색 깃발 소지) 배치를 통제한다."
        ]
    },
    13: {
        "title": "작수전 Big Room 회의",
        "chk_sum": "BIM 간섭 해결 회의록 서명, K30/Ev2 품질 규격 합의, 협소구간 LCLM 적용 범위 의결",
        "chk_items": [
            "3D BIM 노반-궤도 구조물 설계 도면 간섭 모델을 최종 매핑하여 검격 한계선(Clearance H≥1.5m)을 의결한다.",
            "KCS 47 10 25 기준 노반 지지지수 K30 ≥ 110 MN/m³ 품질 관리 및 1층 30cm 다짐 기준을 통일 의결한다.",
            "장비 진입 협소부의 LCLM 유동성채움재 품질 규격 및 배합 시험 조건을 시공 마스터 CPM에 반영 확정한다."
        ]
    },
    14: {
        "title": "시공 계획 수립",
        "chk_sum": "시공계획서 감리단 최종 승인, 시험성토 다짐 계획서 구비, 들밀도/PBT 시험 빈도 확인",
        "chk_items": [
            "KCS 11 20 00 토공 및 KCS 47 10 25 강화노반 시방에 부합하는 시공계획서를 빌드하여 감리단 기술 결재를 득한다.",
            "10톤 진동 롤러 + 15톤 타이어 롤러 다짐 장비 조합 및 구간 L≥50m 시험성토(Trial Compaction) 계획을 빌드한다.",
            "층다짐 두께 30cm 이하 규정, OMC 최적 함수비 범위 및 현장 밀도 측정 시험 빈도를 스케줄링한다."
        ]
    },
    15: {
        "title": "사토장_토취장 선정 검토(필요시)",
        "chk_sum": "수정 CBR 10% 이상 시험성적서, 골재 입도 분석 규격 일치, 사토장 인허가 승인 필증",
        "chk_items": [
            "KS F 2320 수정 CBR 기준을 준수하여 토취장 후보지의 수정 CBR ≥ 10% 적합 품질성적서를 심사 확인한다.",
            "골재 입도분석 시험(KS F 2302)을 수행하여 최대입경 100mm 이하, 흙분 5% 이하 시방 만족 상태를 전수 대조한다.",
            "지정 사토장의 적법 환경 인허가 승인 문서 사본 및 덤프 운반 단가 실정보고서를 감리단에 제출한다."
        ]
    },
    16: {
        "title": "공사사전준비",
        "chk_sum": "자동 세륜기 및 슬러지 보관함 설치, 비산 방진망 지주대 고정, 살수차 현장 배치",
        "chk_items": [
            "현장 주 출입구 비산먼지 차단 자동 세륜기 배관 정비 및 슬러지 보관함 밀폐를 검속한다.",
            "가설 울타리 주변 비산먼지 억제 방진망(높이 2.4m 이상) 지주 버팀대를 견고히 고정 설치한다.",
            "비산 먼지 발생 시 즉각 대처할 수 있는 15톤 살수차 상시 대기 및 임시 침사지 사전 준설을 시행한다."
        ]
    },
    17: {
        "title": "임시배수시설",
        "chk_sum": "가배수로 배수 구배 2.0% 확보 측량, 가배수로 규격 시방 준수, 비상 양수 펌프 대기",
        "chk_items": [
            "포설면 가배수로 횡단 배수 구배 2.0% 이상 정밀 수준 측량 및 모터 그레이더 성형을 확인한다.",
            "측부 가설 임시 배수로 단면 규격(폭 0.5m, 깊이 0.5m 이상) 굴착 시방을 만족 시공한다.",
            "가설 집수정 내 투수 필터 부직포 포설 및 비상 수중 양수 펌프(3인치 이상) 전원 가동 대기 상태를 검속한다."
        ]
    },
    18: {
        "title": "쌓기재료 검사",
        "chk_sum": "로트별 골재 시험성적서 원본 대조, 최대입경 100mm 및 흙분 5% 이하 확인, 불량재 반출 기록",
        "chk_items": [
            "현장 반입 쇄석 골재의 로트별(500m³ 단위 1회) 품질 샘플 채취 및 시험원 입회 시험을 의뢰한다.",
            "KS F 2302 입도분석 시험을 거쳐 최대입경 100mm 이하, 200번체 5% 이하 골재 품질 상태를 대조 심사한다.",
            "품질 미달 불합격 골재의 혼입 방지용 야적 구역 격리 및 즉시 반출 대장 기재를 통제한다."
        ]
    },
    19: {
        "title": "장비 검수 지원",
        "chk_sum": "다짐 장비 자체 안전검사 필증 확인, 유압 오일 미세 누유 점검, 조종원 특별안전 교육 수료",
        "chk_items": [
            "반입 다짐 장비의 자체 유효 안전검사 필증 원본과 유무를 정밀 대조 검속한다.",
            "롤러 및 그레이더 엔진룸 유압 밸브 균열 및 오일 누유 상태를 확인 점검한다.",
            "일일 작업 개시 전 조종원 음주 여부 측정 및 후방 안전 센서 작동 시험을 수행 기록한다."
        ]
    },
    20: {
        "title": "선로 종_횡단 및 용지경계측량",
        "chk_sum": "GRS80 좌표 트램 중심선 측량 야장, 노반 수준 표고 오차 ±10mm 이내, 용지 경계 말뚝 콘크리트 고정",
        "chk_items": [
            "GRS80 세계측지계 좌표 기준 선로 중심선 10m 간격 수준 측량을 정밀 시행한다.",
            "노반 완성 표고 계획 오차 ±10mm 이내 관리 한계선을 스프레이 라인 마킹한다.",
            "수용 용지 경계 보상 말뚝의 무단 유실 방지를 위한 가설 콘크리트 근가 고정을 확인 승인한다."
        ]
    },
    21: {
        "title": "규준틀 설치",
        "chk_sum": "직선 50m / 곡선 20m 설치 간격 준수, 버팀목 견고 고정 상태, 계획 표고 오차 ±10mm 이내 마킹",
        "chk_items": [
            "직선 구간 50m, 곡선 구간 20m 설치 간격 법면 경사 어깨선 지점을 수준 측량한다.",
            "목재 규준틀 및 경사 지지용 목재 버팀대를 땅속 깊이 50cm 이상 견고히 고정 매설한다.",
            "규준틀 상판에 표고 오차 ±10mm 이내 계획선을 표시하고 법면 경사 1:1.5 설계 구배 로프를 고정한다."
        ]
    },
    22: {
        "title": "원지반 검사 및 다짐",
        "chk_sum": "성토 기초면 지하수위 노반 하부 1.0m 이하 저하, 배수 트렌치 자갈 필터 통수, 측구 필터 부직포 포설",
        "chk_items": [
            "성토 기초 지반 유입수 조사를 실시하여 지하수위가 노반 하부 1.0m 이하 저하되는지 측량 확인한다.",
            "종단 배수 트렌치(폭 0.6m)를 굴착하여 자갈 필터재(입경 25~40mm) 포설 상태를 정밀 검속한다.",
            "트렌치 연계 가설 집수정 단면 잔재물 청소 및 수중 양수기 작동 상태를 전수 확인한다."
        ]
    },
    23: {
        "title": "구조물 기초 굴착 (필요시)",
        "chk_sum": "유기질 표토(15~30cm) 100% 제거, 수목 뿌리 1.0m 이하 완전 굴착 반출, 바닥면 상대다짐도 95% 합격",
        "chk_items": [
            "성토 범위 내 지장 수목 뿌리를 백호 장비로 깊이 1.0m 이상 100% 굴착 제거 반출한다.",
            "유기물 함유 표토(평균 15~30cm)를 평삭 제거하여 지정 사토장으로 사토 이송 대장에 기록한다.",
            "벌개제근 완료 바닥면의 진동 롤러 4회 정속 다짐 후 들밀도시험 다짐도 95% 이상을 층별 검속한다."
        ]
    },
    24: {
        "title": "구조물 및 지장물 제거",
        "chk_sum": "지중 간섭 구조물 100% 굴착 철거, 되메우기 골재 시험성적서 확인, 되메우기 층별 다짐도 95% 승인",
        "chk_items": [
            "노반 다짐 구간 내 간섭 지중 폐옹벽, 폐암거 등 지하 장애물 철거 구역 측량을 실시한다.",
            "유압 브레이커 장비 투입 파쇄 굴착 및 폐콘크리트 잔재를 임시 야적장으로 전량 반출한다.",
            "철거 후 굴착 빈 공동 구역에 양질의 토사를 포설하여 1층 30cm 이하 층다짐 95% 이상을 검속 완료한다."
        ]
    },
    25: {
        "title": "진입로 조성",
        "chk_sum": "가설 도로 폭 6.0m 및 종단 구배 10% 이하, 쇄석(40mm) 200mm 부설 다짐, 출입구 세륜기 연계",
        "chk_items": [
            "덤프트럭 교행이 가능한 가설 통행로 노폭 W≥6.0m 및 종단 구배 10% 이하 마감 측량을 검속한다.",
            "노면 요철을 평삭하고 투수성 쇄석 골재(입경 40mm)를 두께 200mm 이상 균일하게 부설한다.",
            "10톤 진동 롤러 6회 이상 왕복 다짐으로 노면 강도를 확보하고 주 출입구 세륜기와 통행 연동한다."
        ]
    },
    26: {
        "title": "강화노반(상부노반) 쇄석 포설",
        "chk_sum": "성토 1층 다짐 완결 두께 30cm 이하 준수, 들밀도시험 상대 다짐도 95% 이상, OMC 함수비 오차범위",
        "chk_items": [
            "토취장 반입 사질토를 모터 그레이더로 1층 포설 다짐 두께 30cm 이하로 균일하게 포설 성형한다.",
            "최적함수비(OMC) 충족을 위해 반입 골재 함수량을 확인 측정하고 살수차 살수량을 조정한다.",
            "10톤 진동 롤러 층다짐 실시 후 층별 들밀도시험 상대 다짐도 95% 이상 합격 여부를 검속한다."
        ]
    },
    27: {
        "title": "강화노반 다짐 및 시공성 검토",
        "chk_sum": "하부노반 총 두께 90cm 분할 다짐, PBT 결과 Ev2 ≥ 80 MPa 확보, 다짐비 Ev2/Ev1 ≤ 2.5 만족",
        "chk_items": [
            "하부노반 총 설계 두께 90cm 성토를 위해 30cm 두께 단위로 3층 분할 포설 및 다짐을 시행한다.",
            "층별 들밀도 95% 확인 후 최종 마무리면 표면에 100m 간격 평판재하시험(PBT)을 배치한다.",
            "평판재하시험 결과 변형계수 Ev2 ≥ 80 MPa 및 다짐비 Ev2/Ev1 ≤ 2.5 만족 여부를 검측 날인한다."
        ]
    },
    28: {
        "title": "노반 완성면 평판재하시험(PBT)",
        "chk_sum": "상부노반 시공 두께 30cm 준수, K30 ≥ 90 MN/m³ 확보, Ev2 ≥ 100 MPa 및 Ev2/Ev1 ≤ 2.2 충족",
        "chk_items": [
            "하부노반 완료면 표면 이물질 청소 상태 확인 및 상부노반 쇄석 골재 30cm를 균일 포설한다.",
            "OMC 관리 다짐 95% 완료 후 마무리면 100m 간격 PBT 평판재하시험을 의뢰한다.",
            "PBT 시험성적서상 노반반력계수 K30 ≥ 90 MN/m³ 및 변형계수 Ev2 ≥ 100 MPa 만족을 확인한다."
        ]
    },
    29: {
        "title": "강화노반 시공",
        "chk_sum": "PBT K30≥110MN/m³ 성적서, PFWD Ev2≥120MPa, Ev2/Ev1≤2.2, 쇄석 최대입경 100mm 이하, 층다짐 30cm 검속",
        "chk_items": [
            "PBT 평판재하시험 지지력 계수 K30 ≥ 110 MN/m³ 100% 달성 성적서 확인 여부",
            "PFWD 변형계수 Ev2 ≥ 120 MPa 및 다짐비 Ev2/Ev1 ≤ 2.2 만족 여부",
            "쇄석 혼합 골재 최대입경 100mm 이하 및 1층 다짐 두께 30cm 이하 준수 여부"
        ]
    },
    30: {
        "title": "강화노반 표고 및 종_횡단 검측",
        "chk_sum": "지정 사토장 반입 확인서 100% 확보, 덤프트럭 적재 초과 방지 계근, 운반 노선 먼지 억제 살수",
        "chk_items": [
            "덤프트럭 사토 물량 일지와 지정 사토장 환경 인허가 반입 영수증을 전수 대조 점검한다.",
            "운반 덤프트럭의 비산방지용 자동 덮개 설치 상태 및 오일 누유 방지판을 검속한다.",
            "현장 덤프 반출 경로 가설 도로 살수 가동 일지 및 환경부 올바로시스템 확인서를 서명 결재한다."
        ]
    },
    31: {
        "title": "배수시설(측구_유공관) 시공",
        "chk_sum": "침하 계측 데이터 정기 결재, 트램 허용 잔류침하량 2.5cm 이하 수렴 판정서, DCM 코어 28일 압축강도",
        "chk_items": [
            "PVD/DCM 개량 지반 침하 계측 데이터 주간 보고서 정기 결재 여부",
            "계측 분석 결과 트램 허용 잔류침하량 2.5cm 이하 최종 수렴 판정서 교부 여부",
            "DCM 지반 개량 코어 품질 압축강도(28일 강도) 시방 만족 확인 여부"
        ]
    },
    32: {
        "title": "사면보호공 시공(필요시)",
        "chk_sum": "유공관 종단 배수 구배 2.0% 이상, 투수 부직포 세굴방지 감싸기, 집수정 통수 연동 시험",
        "chk_items": [
            "맹암거 D200mm 유압 유공관 종단 배수 구배 2.0% 이상 정밀 부설 여부",
            "투수 부직포 세굴 방지 30cm 중첩 감싸기 및 쇄석(25~40mm) 채움 검속 여부",
            "측구 집수정 접속부 무오류 통수 시험 완료 및 감리단 검측 서명 여부"
        ]
    },
    33: {
        "title": "강화노반 완공후 품질_계측 관리",
        "chk_sum": "발파암 최대 입경 300mm 이하 준수, 암석 공극 투수성 쇄석 100% 충전, 층두께 60cm 및 롤러 8회 다짐",
        "chk_items": [
            "발파암 및 암석 재료 최대 입경 300mm 이하 선별 규격 준수 여부",
            "암석 공극 채움용 투수성 쇄석 골재 100% 충전 및 평탄화 시공 상태 여부",
            "암석쌓기 1층 포설 두께 60cm 이하 준수 및 롤러 8회 다짐 상태 여부"
        ]
    },
    34: {
        "title": "방치기간 확보",
        "chk_sum": "계획 방치 기간(3~6개월) 이행 대장, 일 침하량 ≤0.1mm 수렴 확인, 감리단 궤도팀 공동 서명 날인",
        "chk_items": [
            "설계 계획 성토 완료 후 방치 기간(3~6개월) 계측 대장 연속 작성 준수 여부",
            "침하 계측 결과 일일 침하량 ≤0.1mm 이하 수렴 및 침하 곡선 안정 확인 여부",
            "방치 기간 종료 및 궤도 시공팀 인계 승인서 감리단 최종 승인 날인 여부"
        ]
    },
    35: {
        "title": "완공 측량 및 3D 데이터 작성",
        "chk_sum": "완성면 횡단 배수 구배 2.0% 정지, 노반 완성고 오차 ±10mm 이내 만족, 완성면 평탄성 시험 검속",
        "chk_items": [
            "완성면 모터 그레이더 정밀 평삭 횡단 배수 구배 2.0% 이상 정지 상태 여부",
            "노반 완성 마무리면 표고 실측 오차 계획고 기준 ±10mm 이내 만족 여부",
            "완성면 평탄성 시험 및 15톤 타이어 롤러 최종 다짐 흔적 평탄성 여부"
        ]
    },
    36: {
        "title": "토공 마무리면 인계",
        "chk_sum": "감리단/토공/궤도 3자 공동 서명 날인, K30 ≥ 110 및 Ev2 ≥ 120 성적서 원본 첨부, CAD GIS 노반 대장 준공 제출",
        "chk_items": [
            "노반 완공 궤도 인계인수서 감리단/토공/궤도 시공팀 3자 공동 서명 날인 여부",
            "K30 ≥ 110 MN/m³ 및 Ev2 ≥ 120 MPa 최종 품질 성적서 원본 첨부 완료 여부",
            "준공 준측량 도면 및 CAD GIS 노반 이관 대장 데이터 감리단 승인 완료 여부"
        ]
    }
}

# Add default items for WBS 4 to 36 not fully detailed above to guarantee 100% complete coverage
for i in range(4, 37):
    if i in master_ground_truth:
        continue
    folder_names = [
        "4_착수전 측량 Data 확인", "5_지장물이설 협의", "6_용지보상RISK 검토", "7_최고의 팀 만들기 지원",
        "8_연약지반 처리공법 검토(필요시)", "9_토공 유동표 확인", "10_기공승낙 적정성 검토", "11_폐기물처리계획 수립",
        "12_철도운행협의(필요시)", "13_작수전 Big Room 회의", "14_시공 계획 수립", "15_사토장_토취장 선정 검토(필요시)",
        "16_공사사전준비", "17_임시배수시설", "18_쌓기재료 검사", "19_장비 검수 지원",
        "20_선로 종_횡단 및 용지경계측량", "21_규준틀 설치", "22_원지반 검사 및 다짐", "23_구조물 기초 굴착 (필요시)",
        "24_구조물 및 지장물 제거", "25_진입로 조성", "26_강화노반(상부노반) 쇄석 포설", "27_강화노반 다짐 및 시공성 검토",
        "28_노반 완성면 평판재하시험(PBT)", "29_강화노반 시공", "30_강화노반 표고 및 종_횡단 검측", "31_배수시설(측구_유공관) 시공",
        "32_사면보호공 시공(필요시)", "33_강화노반 완공후 품질_계측 관리", "34_방치기간 확보", "35_완공 측량 및 3D 데이터 작성", "36_토공 마무리면 인계"
    ]
    fname = folder_names[i-4]
    title = fname.split("_", 1)[1]
    
    master_ground_truth[i] = {
        "title": title,
        "chk_sum": f"{title} 시방 이행, 1층 다짐 두께 30cm 이하, K30≥110MN/m³, 오차 ±10mm 100% 검속",
        "chk_items": [
            f"{title} 과업 시방 기준 및 공학 품질 지표 100% 이행 여부",
            "1층 포설 다짐 두께 30cm 이하 준수 및 들밀도 상대다짐도 95% 만족 여부",
            "계획 표고 오차 ±10mm 이내 검속 및 감리단 최종 승인 서명 여부"
        ]
    }

folders_on_disk = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

html_updated = 0
for seq_num, gt in master_ground_truth.items():
    prefix = f"{seq_num}_"
    folder_name = None
    for f in folders_on_disk:
        if f.startswith(prefix):
            folder_name = f
            break
            
    if not folder_name:
        print(f"⚠️ No folder found on disk for WBS {seq_num}")
        continue

    folder_path = os.path.join(base_dir, folder_name)
    chk_dir = os.path.join(folder_path, "체크리스트")
    os.makedirs(chk_dir, exist_ok=True)

    title = gt["title"]
    chk_sum = gt["chk_sum"]
    chk_items = gt["chk_items"]

    # Generate Checklist Rows HTML dynamically
    chk_rows_html = ""
    for idx, chk_item in enumerate(chk_items, 1):
        chk_rows_html += f"""
            <tr>
                <td style="text-align: center; font-weight: bold;">{idx}</td>
                <td style="font-weight: bold; color: var(--accent-blue);">{title} 특화 항목 {idx}</td>
                <td>{chk_item}</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>"""

    # Complete optimized Checklist Template
    chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상부강화노반 - {title} 검측 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #ffffff;
            --bg-table-header: #f8fafc;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-blue: #1e3a8a;
            --accent-cyan: #0284c7;
            --border-color: #cbd5e1;
        }}
        body {{
            font-family: 'Pretendard', 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 20px;
            color: var(--text-primary);
            background: #ffffff;
            line-height: 1.5;
        }}
        .checklist-container {{
            max-width: 1000px;
            margin: 0 auto;
            border: 2px solid #0f172a;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .top-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 25px;
        }}
        .top-table td {{
            border: 1px solid var(--border-color);
            padding: 10px 12px;
            font-size: 0.9rem;
        }}
        .sign-title {{
            background: var(--bg-table-header);
            text-align: center;
            font-weight: bold;
            width: 15%;
        }}
        .sign-box {{
            height: 60px;
            text-align: center;
            vertical-align: middle;
            font-size: 0.85rem;
            color: #94a3b8;
        }}
        .header-section {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 3px solid var(--accent-blue);
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--accent-blue);
            margin: 0;
        }}
        .wbs-code {{
            font-size: 1.05rem;
            font-weight: bold;
            color: var(--accent-cyan);
        }}
        .summary-box {{
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #166534;
        }}
        .main-table {{
            width: 100% !important;
            max-width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 25px;
        }}
        .main-table th {{
            background: var(--bg-table-header);
            border: 1px solid var(--border-color);
            padding: 12px 10px;
            font-size: 0.9rem;
            font-weight: bold;
            text-align: center;
        }}
        .main-table td {{
            border: 1px solid var(--border-color);
            padding: 12px 15px;
            font-size: 0.9rem;
            vertical-align: middle;
        }}
        .result-cell {{
            text-align: center;
            white-space: nowrap;
            font-size: 0.85rem;
            font-weight: bold;
        }}
        .footer-logo {{
            text-align: center;
            font-weight: bold;
            font-size: 1.1rem;
            margin-top: 40px;
            color: var(--text-secondary);
            letter-spacing: 2px;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
        }}
        @media print {{
            body {{ padding: 0; }}
            .checklist-container {{ border: none; padding: 0; box-shadow: none; }}
            .main-table th {{ background: #f1f5f9 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .summary-box {{ background: #ffffff !important; border: 1px solid #000000 !important; }}
        }}
    </style>
</head>
<body>
<div class="checklist-container">
    <!-- 결재인 및 기본 메타 정보 -->
    <table class="top-table">
        <tr>
            <td class="sign-title">공 사 명</td>
            <td style="width: 35%; font-weight: bold;">동탄도시철도(트램) 건설공사</td>
            <td rowspan="2" class="sign-title" style="width: 8%;">결<br><br>재</td>
            <td class="sign-title" style="width: 14%;">협력회사</td>
            <td class="sign-title" style="width: 14%;">원도급사</td>
            <td class="sign-title" style="width: 14%;">감 리 단</td>
        </tr>
        <tr>
            <td class="sign-title">검측위치</td>
            <td>상부강화노반 작업구간 (WBS 중심선)</td>
            <td class="sign-box">인 / 서명</td>
            <td class="sign-box">인 / 서명</td>
            <td class="sign-box">인 / 서명</td>
        </tr>
    </table>

    <div class="header-section">
        <h1 class="title">{title} 검측 체크리스트</h1>
        <div class="wbs-code">WBS Code: 9000-7-{seq_num}</div>
    </div>

    <!-- 엑셀 요약 동치 박스 -->
    <div class="summary-box">
        <h4 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #166534;">📋 WBS 엑셀 연동 핵심 요약 (Checklist Summary)</h4>
        <pre style="white-space: pre-wrap; font-family: inherit; margin: 0; font-size: 0.95rem; font-weight: bold; color: #166534;">{chk_sum}</pre>
    </div>

    <!-- 100% 가로폭 검측 테이블 -->
    <table class="main-table">
        <thead>
            <tr>
                <th style="width: 5%;">No</th>
                <th style="width: 25%;">검측 구분 및 항목</th>
                <th style="width: 55%;">정량적 검측 세부 수칙 및 허용 공차 (KCS 47 10 25)</th>
                <th style="width: 15%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            {chk_rows_html}
            <tr>
                <td style="text-align: center; font-weight: bold;">4</td>
                <td style="font-weight: bold; color: var(--accent-blue);">1층 다짐 두께 준수</td>
                <td>1층 포설 및 다짐 완료 두께 <strong>30cm 이하</strong> 엄격 이행 여부</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">5</td>
                <td style="font-weight: bold; color: var(--accent-blue);">상대 다짐도 (들밀도)</td>
                <td>들밀도시험 상대 다짐도 <strong>95% 이상</strong> 달성 (KS F 2312 D다짐 기준) 여부</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">6</td>
                <td style="font-weight: bold; color: var(--accent-blue);">노반 반력계수 (K30)</td>
                <td>PBT 평판재하시험 지지력 계수 <strong>K30 ≥ 110 MN/m³</strong> 성적서 확인 여부</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">7</td>
                <td style="font-weight: bold; color: var(--accent-blue);">변형계수 (Ev2)</td>
                <td>PFWD 시험 2차 변형계수 <strong>Ev2 ≥ 120 MPa</strong> 및 <strong>Ev2/Ev1 ≤ 2.2</strong> 비율 충족 여부</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">8</td>
                <td style="font-weight: bold; color: var(--accent-blue);">완성면 계획고 오차</td>
                <td>완성면 계획고 종횡단 허용 공차 <strong>±10mm 이내</strong> 준수 및 구배 <strong>2.0%</strong> 확보 여부</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">9</td>
                <td style="font-weight: bold; color: var(--accent-blue);">인계인수서 날인</td>
                <td>감리단, 시공사 및 후행 궤도 시공팀 3자 완공 마무리면 공동 서명 날인 여부</td>
                <td class="result-cell">☐ 합격 &nbsp; ☐ 불합격 &nbsp; ☐ 보류</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-logo">
        동탄도시철도 건설공사 책임감리단
    </div>
</div>
</body>
</html>"""

    chk_fp = os.path.join(chk_dir, f"{folder_name}_체크리스트.html")
    with open(chk_fp, 'w', encoding='utf-8') as f:
        f.write(chk_html)

    html_updated += 1
    print(f" Checklist Updated WBS {seq_num:02d} [{folder_name}] to Standard Print Format.")

print(f"\n🎉 Successfully Standardized {html_updated} Checklist HTML Files!")
