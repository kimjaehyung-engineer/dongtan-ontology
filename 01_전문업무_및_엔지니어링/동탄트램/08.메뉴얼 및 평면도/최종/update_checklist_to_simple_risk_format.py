import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반"

# Compile 36 WBS activity detailed risk ground truth
wbs_risk_db = {
    1: {
        "title": "지반조사 상세검토",
        "chk_sum": "N치<4 연약지반 개량 범위, PBT 원지반 지지력 K30 확인, 암반 파쇄대 50cm 치환 계획 승인",
        "pre": "설계 시 주상도 분석 누락 및 지하 물리탐사(GPR) 탐사 결과 불일치로 인한 연약지반 누락 리스크",
        "ing": "N치 < 4 연약지반 구간의 치환 또는 공법 개량 판단 지연으로 다짐 시 지반 연화 현상 발생 리스크",
        "post": "원지반 반력계수 K30 검속 실패로 인한 상부 옹벽 및 강화노반 기초 지지력 약화 리스크"
    },
    2: {
        "title": "발주전략 KOM",
        "chk_sum": "품질이행 확약서 날인, 다짐 장비 반입 계약서 확인, K30 ≥ 110 MN/m³ 품질기준 의결",
        "pre": "협력사 및 골재 납품업체 간 품질 표준(KCS 47 10 25) 공유 미비 및 시공 장비 수급 지연 리스크",
        "ing": "현장 층다짐 30cm 이하 규격 미이행 및 진동롤러/타이어롤러의 부적절한 다짐 조합 운용 리스크",
        "post": "골재 시험성적서 미비로 인한 자재 승인 반려 및 전체 공정 스케줄 마스터 지연 리스크"
    },
    3: {
        "title": "철도보호지구에서의 행위신고(필요시)",
        "chk_sum": "철도공단 행위신고 승인 필증, 레일 침하핀 및 경사계 계측 모니터링, 철도운행안전원 상주 확인",
        "pre": "국가철도공단 행위신고(선로 30m 이내) 지연으로 인한 본공사 착수 금지 및 과태료 리스크",
        "ing": "야간 인접 굴착 시 선로 침하 감시핀(허용치 ±5mm) 및 경사계 계측 모니터링 누락 리스크",
        "post": "철도공단 준공 승인 연기로 인한 노반 준공 불허 및 궤도팀 인계 불능 리스크"
    },
    4: {
        "title": "착수전 측량 Data 확인",
        "chk_sum": "GRS80 기준점 매핑, TBM 100m 간격 가설, 수준 측량 오차 ±10mm 이내 검측 성적서",
        "pre": "국가 가설 TBM 기준점 검교정 유실로 인한 선로 계획 종단 및 중심 좌표 왜곡 리스크",
        "ing": "GRS80 세계측지계 좌표계 혼용 및 수준 측량 기준고 오차(±10mm 초과) 발생 리스크",
        "post": "측량 야장 불일치로 인한 법면 깎기선 이탈 및 부지 경계 침범 분쟁 리스크"
    },
    5: {
        "title": "지장물이설 협의",
        "chk_sum": "3D BIM 간섭 검증, 강화노반 직하부 관로 이격거리 H≥1.5m 만족, 위수탁 계약 승인",
        "pre": "5대 지장물 위탁관리기관과의 3D BIM 간섭 검증 지연 및 이설 범위 마찰 리스크",
        "ing": "노반 직하부 신설 관로의 수평/수직 이격거리(H < 1.5m) 협의 기준 미달 및 파손 리스크",
        "post": "위수탁 설계변경 및 사후 정산(Provisional Sum) 단가 합의 지연으로 공사비 분쟁 리스크"
    },
    6: {
        "title": "용지보상RISK 검토",
        "chk_sum": "미보상 필지 현장 경계목 설치, 무단진입 차단 가설 펜스 설치, 용지 매수 관리대장 확인",
        "pre": "토지 수용 대장 및 미보상 사유지 필지 파악 누락으로 인한 장비 진입 차단 리스크",
        "ing": "사유지 무단 진입으로 인한 민원 발생 및 공사 중지 가처분 소송 리스크",
        "post": "경계 측량 말뚝 분실로 인한 비탈면 경계 시공선 침범 및 복구 공사 비용 발생 리스크"
    },
    7: {
        "title": "최고의 팀 만들기 지원",
        "chk_sum": "유자격 시험원 면허 대조, 다짐장비 조종원 경력증명서 확인, 시공전 품질 교육 서명",
        "pre": "토공 기술사 및 PBT/PFWD 자격 시험원의 배치 지연에 따른 품질 검측 신뢰도 하락 리스크",
        "ing": "다짐장비(진동롤러, 그레이더) 조종원의 시방서(1층 30cm 다짐) 숙지 미흡 및 불량 포설 리스크",
        "post": "검측 책임 부재로 인한 품질 기록 대장 부실화 및 발주처 합동 검사 반려 리스크"
    },
    8: {
        "title": "연약지반 처리공법 검토(필요시)",
        "chk_sum": "PVD/DCM 지반개량 시공계획 승인, 계측 침하판 레벨 측정, 허용 잔류침하 2.5cm 이내 판정",
        "pre": "PVD 배수재 품질 성적 및 DCM 시멘트 최적 배합 설계 오류로 인한 지반 개량 실패 리스크",
        "ing": "계측 침하판 레벨 측정 주기 미준수 및 침하 수렴 곡선 기울기 판독 오류 리스크",
        "post": "허용 잔류침하량(≤ 2.5cm) 한계치 초과 상태에서 후행 노반 공사 강행 시 침하 하자 리스크"
    },
    9: {
        "title": "토공 유동표 확인",
        "chk_sum": "Mass-Curve 토공 유동 선도 확인, 평균 운반거리 5km 이내 지정 사토장 반입 일치",
        "pre": "Mass-Curve 토공 유동 산출 공식 오류로 인한 현장 토사 불균형 및 성토재 부족 리스크",
        "ing": "덤프트럭 토사 반출 노선 미확정 및 평균 운반거리(5km) 초과로 인한 운반비 증가 리스크",
        "post": "토공 반입출 전산대장과 송장 수량 불일치로 인한 기성 정산 삭감 리스크"
    },
    10: {
        "title": "기공승낙 적정성 검토",
        "chk_sum": "임시 사용 기공승낙서 100% 확보, 지적 편집도 기준 경계 실측, 미승낙 필지 차단 펜스",
        "pre": "가설 도로 및 임시 침사지 부지의 기공승낙서(인감증명서 첨부) 미확보 리스크",
        "ing": "지적도 경계 착오로 미승낙 필지 무단 침범 및 지주 민원 제기에 의한 공기 지연 리스크",
        "post": "임시 토지 반환 시 원상복구 합의 각서 미비로 인한 추가 토지 복구비용 지출 리스크"
    },
    11: {
        "title": "폐기물처리계획 수립",
        "chk_sum": "올바로시스템 배출자 신고증 구비, 폐기물 적재함 비산방지막, 보관 기한(90일) 준수",
        "pre": "건설폐기물 배출자 신고 및 올바로시스템(Allbaro) 인허가 등록 지연 리스크",
        "ing": "임시 야적 옹벽/지장 철거 폐기물의 혼합 보관 및 비산 먼지 방지 차막 유실 리스크",
        "post": "폐기물 적법 보관 기한(90일) 초과에 따른 벌금 부과 및 친환경 건설 평가 벌점 리스크"
    },
    12: {
        "title": "철도운행협의(필요시)",
        "chk_sum": "야간 차단작업 승인서 확보, 철도운행안전원 상주 여부, 비상 적색 신호수 배치 확인",
        "pre": "기존선 인접 야간 차단작업 시간대(01:00~04:30) 코레일 최종 승인 공문 미구비 리스크",
        "ing": "철도운행안전원 무전기(VHF) 주파수 동기화 실패 및 경보음 누락으로 열차 충돌 위험 리스크",
        "post": "차단 해제 시간(04:30) 내 장비 퇴피 실패로 첫 차 열차 운행 지연 및 민형사상 배상 리스크"
    },
    13: {
        "title": "작수전 Big Room 회의",
        "chk_sum": "BIM 간섭 해결 회의록 서명, K30/Ev2 품질 규격 합의, 협소구간 LCLM 적용 범위 의결",
        "pre": "노반-궤도-전기-신호 간 인터페이스 간섭 해결을 위한 3D BIM 미조정 리스크",
        "ing": "협소 구간 다짐 불량 예방을 위한 LCLM(유동성채움재) 배합 기준 설정 누락 리스크",
        "post": "부서 간 의결 문서 유실 및 WBS 선후행 인수인계 한계점 설정 부재 리스크"
    },
    14: {
        "title": "시공 계획 수립",
        "chk_sum": "시공계획서 감리단 최종 승인, 시험성토 다짐 계획서 구비, 들밀도/PBT 시험 빈도 확인",
        "pre": "KCS 47 10 25 기준을 미준수한 시공계획서 반려로 인한 실공사 착수 스케줄 지연 리스크",
        "ing": "시험성토(구간 L≥50m) 다짐 회수 미측정 및 다짐 장비 조합 불량 리스크",
        "post": "들밀도시험 및 PBT 평판재하시험 계획 수립 누락으로 품질 보증 불합격 리스크"
    },
    15: {
        "title": "사토장_토취장 선정 검토(필요시)",
        "chk_sum": "수정 CBR 10% 이상 시험성적서, 골재 입도 분석 규격 일치, 사토장 인허가 승인 필증",
        "pre": "토취장 쇄석 골재의 수정 CBR ≥ 10% 미달 및 입도 분석 시험 규격 반려 리스크",
        "ing": "사토장의 법적 환경 인허가(토석채취/폐기) 서류 무효화에 따른 토사 반출 차단 리스크",
        "post": "사토장 이동 거리 실정보고 미비에 따른 공사비 감액 및 기성 삭감 리스크"
    },
    16: {
        "title": "공사사전준비",
        "chk_sum": "자동 세륜기 및 슬러지 보관함 설치, 비산 방진망 지주대 고정, 살수차 현장 배치",
        "pre": "현장 주 출입구 비산먼지 억제 세륜기 고장 및 방진망(H≥2.4m) 풍압 붕괴 리스크",
        "ing": "살수차 미가동 및 비산 먼지 다량 발생에 따른 인근 주민 집단 민원 및 공사 정지 리스크",
        "post": "세륜기 폐수 여과 장치 불량 및 토사 섞인 진흙 슬러지 하천 무단 방류 고발 리스크"
    },
    17: {
        "title": "임시배수시설",
        "chk_sum": "가배수로 배수 구배 2.0% 확보 측량, 가배수로 규격 시방 준수, 비상 양수 펌프 대기",
        "pre": "우기 대비 임시 배수로 가구배(종단 2.0% 미만) 협소 굴착에 따른 우수 정체 리스크",
        "ing": "가배수로 법면 토사 슬라이딩 붕괴 및 배수로 종점 가설 침사지 용량 초과 리스크",
        "post": "강우 연화로 인한 성토 지반 붕괴 및 인접 사유지 농경지 침수 피해 배상 리스크"
    },
    18: {
        "title": "쌓기재료 검사",
        "chk_sum": "로트별 골재 시험성적서 원본 대조, 최대입경 100mm 및 흙분 5% 이하 확인, 불량재 반출 기록",
        "pre": "반입 쇄석 골재의 로트별(500m³ 단위) 채취 품질 샘플 분석 누락 및 미검증 쇄석 유입 리스크",
        "ing": "최대입경 100mm 초과 조대 골재 혼입 및 200번체(흙분) 5% 초과 골재 포설에 의한 다짐 불량 리스크",
        "post": "품질 규격 불량 골재의 노반 혼입으로 인한 장기 노반 반력계수(K30) 저하 리스크"
    },
    19: {
        "title": "장비 검수 지원",
        "chk_sum": "다짐 장비 자체 안전검사 필증 확인, 유압 오일 미세 누유 점검, 조종원 특별안전 교육 수료",
        "pre": "투입 10t 진동롤러 및 그레이더의 법적 건설기계 정기검사증 유효 기간 만료 리스크",
        "ing": "장비 엔진 유압 호스 균열로 인한 강화노반면 토양 기름 오염 및 화재 리스크",
        "post": "조종원 음주 측정 및 장비 후방 충돌 감지 센서 미작동으로 인한 인명 안전 재해 리스크"
    },
    20: {
        "title": "선로 종_횡단 및 용지경계측량",
        "chk_sum": "GRS80 좌표 트램 중심선 측량 야장, 노반 수준 표고 오차 ±10mm 이내, 용지 경계 말뚝 콘크리트 고정",
        "pre": "선로 중심선 수준 측량 지점(10m 간격) 오차 마킹으로 계획고 누적 변위 리스크",
        "ing": "종단 배수 측구 완성 횡단 구배(2.0%) 미달 및 측량 기기 검교정 누락 리스크",
        "post": "용지보상 사유지 경계 말뚝 훼손으로 미보상 필지 침범 옹벽 시공 및 소송 리스크"
    },
    21: {
        "title": "규준틀 설치",
        "chk_sum": "직선 50m / 곡선 20m 설치 간격 준수, 버팀목 견고 고정 상태, 계획 표고 오차 ±10mm 이내 마킹",
        "pre": "직선 50m / 곡선 20m 간격 미준수로 인한 법면 경사 꺾임 및 형상 불량 리스크",
        "ing": "규준틀 버팀목 매설 깊이 부족으로 다짐 장비 진동에 의한 지지선 이탈 및 표고 왜곡 리스크",
        "post": "법면 경사 1:1.5 설계 구배 오차 누적으로 법면 사면 토사 유실 및 붕괴 리스크"
    },
    22: {
        "title": "원지반 검사 및 다짐",
        "chk_sum": "성토 기초면 지하수위 노반 하부 1.0m 이하 저하, 배수 트렌치 자갈 필터 통수, 측구 필터 부직포 포설",
        "pre": "성토 바닥면 지하수위 수준 조사 누락 및 지하수위 노반 하부 1.0m 저하 실패 리스크",
        "ing": "배수 트렌치 내 투수 필터재(25~40mm 자갈) 입도 불량 및 흙분 유입 차단 리스크",
        "post": "원지반 모세관 상승수로 인한 완성 노반면 지반 연화 및 영구 부등침하 하자 리스크"
    },
    23: {
        "title": "구조물 기초 굴착 (필요시)",
        "chk_sum": "유기질 표토(15~30cm) 100% 제거, 수목 뿌리 1.0m 이하 완전 굴착 반출, 바닥면 상대다짐도 95% 합격",
        "pre": "성토 기초면의 유기물 함유 표토(두께 15~30cm) 깎기 및 집토 작업 누락 리스크",
        "ing": "지장 수목 뿌리의 깊이 1.0m 이하 잔재물 미굴착 방치로 유기물 부패 공동 리스크",
        "post": "표토 제거 후 원지반 평탄화 다짐(상대다짐도 95% 미만)에 의한 노반 침하 유발 리스크"
    },
    24: {
        "title": "구조물 및 지장물 제거",
        "chk_sum": "지중 간섭 구조물 100% 굴착 철거, 되메우기 골재 시험성적서 확인, 되메우기 층별 다짐도 95% 승인",
        "pre": "노반 시공 구간 내 지하 간섭 폐콘크리트 옹벽, 폐암거 등 지중 장애물 탐색 실패 리스크",
        "ing": "철거 후 공동 되메우기 시 층다짐 30cm 이행 누락 및 입경 불량 성토재 포설 리스크",
        "post": "되메우기 구역 지지력(K30) 미확보로 인한 상부 궤도 콘크리트 침하 및 균열 리스크"
    },
    25: {
        "title": "진입로 조성",
        "chk_sum": "가설 도로 폭 6.0m 및 종단 구배 10% 이하, 쇄석(40mm) 200mm 부설 다짐, 출입구 세륜기 연계",
        "pre": "덤프트럭 교행 가설 도로 노폭(6.0m 미만) 협소에 따른 중장비 정체 및 전도 사고 리스크",
        "ing": "가설 도로 종단 경사 10% 초과로 다짐 쇄석 부설면의 중장비 미끄러짐 리스크",
        "post": "가설 도로 투수 골재(40mm) 다짐 부족으로 흙탕물 다량 발생 및 인근 세륜기 과부하 리스크"
    },
    26: {
        "title": "강화노반(상부노반) 쇄석 포설",
        "chk_sum": "성토 1층 다짐 완결 두께 30cm 이하 준수, 들밀도시험 상대 다짐도 95% 이상, OMC 함수비 오차범위",
        "pre": "성토 포설층 1층 다짐 두께 30cm 초과 포설 및 그레이더 평삭 각도 오차 리스크",
        "ing": "다짐 시 골재 최적함수비(OMC) 측정 주기 누락 및 건조 다짐에 의한 지지력 부족 리스크",
        "post": "층별 들밀도시험 상대 다짐도 95% 미달 상태에서 상부층 성토 강행 시 층간 분리 리스크"
    },
    27: {
        "title": "강화노반 다짐 및 시공성 검토",
        "chk_sum": "하부노반 총 두께 90cm 분할 다짐, PBT 결과 Ev2 ≥ 80 MPa 확보, 다짐비 Ev2/Ev1 ≤ 2.5 만족",
        "pre": "하부노반 총 설계 두께 90cm에 대한 30cm 단위 3회 분할 다짐 미이행 리스크",
        "ing": "다짐 완료 표면 PBT 평판재하시험 Ev2 ≥ 80 MPa 미확보 및 다짐 부실 리스크",
        "post": "변형계수 다짐비 Ev2/Ev1 > 2.5 초과 발생으로 장기 지반 과다 침하 하자 리스크"
    },
    28: {
        "title": "노반 완성면 평판재하시험(PBT)",
        "chk_sum": "상부노반 시공 두께 30cm 준수, K30 ≥ 90 MN/m³ 확보, Ev2 ≥ 100 MPa 및 Ev2/Ev1 ≤ 2.2 충족",
        "pre": "상부노반 쇄석층 부설 두께 30cm 미달 및 표면 요철 정지 작업 미비 리스크",
        "ing": "완성면 PBT K30 < 90 MN/m³ 또는 Ev2 < 100 MPa 발생 시 보강 대책 지연 리스크",
        "post": "다짐비 Ev2/Ev1 > 2.2 초과 상태로 합격 처리 시 동결융해 및 트램 궤간 틀림 리스크"
    },
    29: {
        "title": "강화노반 시공",
        "chk_sum": "PBT K30≥110MN/m³ 성적서, PFWD Ev2≥120MPa, Ev2/Ev1≤2.2, 쇄석 최대입경 100mm 이하, 층다짐 30cm 검속",
        "pre": "트램 핵심 지지구조물인 강화노반(30cm) 쇄석 혼합재의 입도 승인 성적서 오류 리스크",
        "ing": "포설 및 다짐 시 OMC 범위(최적함수비) 이탈 및 1층 30cm 다짐 두께 이행 불량 리스크",
        "post": "PBT K30 < 110 MN/m³ 또는 PFWD Ev2 < 120 MPa 발생으로 후행 콘크리트도상 인계 불허 리스크"
    },
    30: {
        "title": "강화노반 표고 및 종_횡단 검측",
        "chk_sum": "지정 사토장 반입 확인서 100% 확보, 덤프트럭 적재 초과 방지 계근, 운반 노선 먼지 억제 살수",
        "pre": "지정 사토장 계약 수량 초과 반출 및 올바로시스템 실시간 인수인계 입력 누락 리스크",
        "ing": "덤프트럭 과적 및 적재함 덮개 미개폐 상태 주행에 따른 토사 낙하 환경 고발 리스크",
        "post": "덤프 운반 노선 살수 가동 정지로 대기 비산먼지 민원 및 지자체 공사 중단 명령 리스크"
    },
    31: {
        "title": "배수시설(측구_유공관) 시공",
        "chk_sum": "침하 계측 데이터 정기 결재, 트램 허용 잔류침하량 2.5cm 이하 수렴 판정서, DCM 코어 28일 압축강도",
        "pre": "DCM 개량 지반 코어의 강도 시험 누락 및 성토 계측 침하판 50m 간격 배치 오류 리스크",
        "ing": "침하 변동 데이터 분석 누락 및 시간-침하 곡선 일일 0.1mm 이하 수렴 확인 부재 리스크",
        "post": "허용 잔류침하량(2.5cm) 미수렴 지반에 트램 궤도 포설 강행으로 인한 궤도 영구 전단 변형 리스크"
    },
    32: {
        "title": "사면보호공 시공(필요시)",
        "chk_sum": "유공관 종단 배수 구배 2.0% 이상, 투수 부직포 세굴방지 감싸기, 집수정 통수 연동 시험",
        "pre": "맹암거 터파기 단면 경사면의 다짐 불량 및 종단 배수 구배(2.0% 미만) 설치 오류 리스크",
        "ing": "D200mm 유공관 주위 투수성 필터 부직포 겹침(30cm 미만) 부족 및 토사 폐색 리스크",
        "post": "맹암거 쇄석(25~40mm) 채움 부족으로 인한 지중수 정체 및 성토 법면 슬라이딩 붕괴 리스크"
    },
    33: {
        "title": "강화노반 완공후 품질_계측 관리",
        "chk_sum": "발파암 최대 입경 300mm 이하 준수, 암석 공극 투수성 쇄석 100% 충전, 층두께 60cm 및 롤러 8회 다짐",
        "pre": "암석쌓기 재료의 최대 입경(300mm 초과) 조대석 혼입 및 시방 입도 선별 누락 리스크",
        "ing": "암석 층쌓기 포설 두께 60cm 초과 포설 및 진동 롤러 왕복 8회 다짐 부족 리스크",
        "post": "암석 간 조대 공극 쇄석 골재 살수 충전 미비로 인한 집중호우 시 성토 법면 유실 리스크"
    },
    34: {
        "title": "방치기간 확보",
        "chk_sum": "계획 방치 기간(3~6개월) 이행 대장, 일 침하량 ≤0.1mm 수렴 확인, 감리단 궤도팀 공동 서명 날인",
        "pre": "성토 완료 후 설계상 계획된 방치 기간(3~6개월) 미확보 상태의 속행 시공 강행 리스크",
        "ing": "주간 단위 수준 측량 대장 유실 및 침하 계측판 장비 충격에 의한 파손 누락 리스크",
        "post": "3주 연속 1.0mm 이하(일 침하량 ≤0.1mm) 미수렴 상태에서 후행 인수 강행 시 부등침하 리스크"
    },
    35: {
        "title": "완공 측량 및 3D 데이터 작성",
        "chk_sum": "완성면 횡단 배수 구배 2.0% 정지, 노반 완성고 오차 ±10mm 이내 만족, 완성면 평탄성 시험 검속",
        "pre": "노반 완성 마무리면 10m 간격 정밀 수준 측량 누락 및 높이 좌표 야장 오류 리스크",
        "ing": "모터 그레이더 평삭 칼날 구배 고정 오류로 마무리면 횡단 배수 구배 2.0% 미달 리스크",
        "post": "마무리면 표고 실측 오차(±10mm 초과) 및 평탄성 불량으로 콘크리트도상 기초 두께 하자 리스크"
    },
    36: {
        "title": "토공 마무리면 인계",
        "chk_sum": "감리단/토공/궤도 3자 공동 서명 날인, K30 ≥ 110 및 Ev2 ≥ 120 성적서 원본 첨부, CAD GIS 노반 대장 준공 제출",
        "pre": "GRS80 세계측지계 좌표 대조 GIS 준공 데이터 작성 오류 및 CAD 도서 불일치 리스크",
        "ing": "감리단/토공/궤도 시공팀 3자 합동 교차 수준 실측 생략에 따른 현장 치수 정합성 상실 리스크",
        "post": "K30 ≥ 110 성적서 원본 누락 및 인계인수서 날인 지연으로 인한 궤도 공정 착수 지연 리스크"
    }
}

# Fill default values for the remaining WBS numbers if any
for i in range(4, 37):
    if i in wbs_risk_db:
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
    wbs_risk_db[i] = {
        "title": title,
        "chk_sum": f"{title} 시방 이행, 1층 다짐 두께 30cm 이하, K30≥110MN/m³, 오차 ±10mm 100% 검속",
        "pre": f"{title} 착수 전 도면 검토 소홀 및 설계 정합성 미확인에 따른 시공 오류 리스크",
        "ing": f"{title} 시공 중 1층 다짐 두께 30cm 초과 포설 및 들밀도 시험 관리 소홀 리스크",
        "post": f"{title} 공사 완료 후 계획고 ±10mm 초과 마감 및 후행 공정 인계 지연 리스크"
    }

folders_on_disk = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

html_updated = 0
for seq_num, risks in wbs_risk_db.items():
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

    title = risks["title"]
    chk_sum = risks["chk_sum"]
    pre_risk = risks["pre"]
    ing_risk = risks["ing"]
    post_risk = risks["post"]

    # Simpler standard Risk Checklist HTML Template
    chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상부강화노반 - {title} 리스크 체크리스트</title>
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
        <span class="meta">WBS Code 9000-7-{seq_num} | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">{chk_sum}</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 47 10 25 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>• <strong>[설계/조사 리스크]</strong> {pre_risk}<br>• <strong>[인터페이스 누락]</strong> 선행 공정 인수 상태 실측 확인 및 부지 사용권 적정성 검속 여부</td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>• <strong>[시공 불량 리스크]</strong> {ing_risk}<br>• <strong>[다짐 및 배수 미비]</strong> 1층 포설 다짐 두께 30cm 이하 엄격 관리, 다짐도 95% 이상 및 최적함수비 OMC 범위 유지 여부</td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>• <strong>[인수 지연 리스크]</strong> {post_risk}<br>• <strong>[인계 불능 예방]</strong> 노반 완성면 표고 오차 ±10mm 이내 준수, 종횡단 배수구배 2.0% 만족, PBT K30 ≥ 110 MN/m³ 및 PFWD Ev2 ≥ 120 MPa 확보 검속 여부</td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | 상부강화노반
    </div>
</div>
</body>
</html>"""

    chk_fp = os.path.join(chk_dir, f"{folder_name}_체크리스트.html")
    with open(chk_fp, 'w', encoding='utf-8') as f:
        f.write(chk_html)

    html_updated += 1

print(f"\n🎉 Successfully Standardized {html_updated} Checklist HTML Files to Simple 3-Stage Risk Layout!")
