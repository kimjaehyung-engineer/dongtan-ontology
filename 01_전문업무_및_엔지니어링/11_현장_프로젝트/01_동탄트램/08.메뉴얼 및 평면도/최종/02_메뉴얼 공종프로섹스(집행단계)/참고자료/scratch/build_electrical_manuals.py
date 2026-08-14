import os, sys, json, re

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\전기분야'

# WBS 11 ~ 32 metadata & HTML generator definition
wbs_data = {
    11: {
        "wbs": "9000-3-11",
        "task": "전기설비 제작 사양서 작성 / 승인",
        "folder": "11_전기설비 제작 사양서 작성 _ 승인",
        "prefix": "전기설비 제작 사양서 작성 _ 승인",
        "method": "전기설비(변압기, 정류기, ESS, GIS, SCADA) 공장 제작 착수 전 발주처 특기시방서 및 KDS 47 00 00 철도설계기준에 따른 상세 기술사양서 및 공장 제작 승인도면(Shop Drawing) 검토",
        "color": "amber",
        "step1_title": "공학적 기술사양서 대조", "step1_desc": "변압기 용량, 정류기 정격, ESS 배터리 세부 기술사양서 검토 및 시방 규격 1:1 대조 파악",
        "step2_title": "제작도면(Shop Drawing) 검토", "step2_desc": "19인치 제어 랙 치수, 부스바 접속 피치, 내진 설계 단자 체결도 및 3D BIM 외형 실측 검증",
        "step3_title": "시험 및 인증 수수 수칙", "step3_desc": "공인기관 시험성적서(KTR/KTL) 제출 수수 및 KESC 사용전검사 필수 시험 항목 사전 포함 확인",
        "step4_title": "감리단 승인 및 배포", "step4_desc": "책임감리단 공학적 승인 제출, 최종 결재 승인도서 수령 및 제작사 공장 제작 공식 통보 완수"
    },
    12: {
        "wbs": "9000-3-12",
        "task": "시공 계획 수립 / 승인",
        "folder": "12_시공 계획 수립 _ 승인",
        "prefix": "시공 계획 수립 _ 승인",
        "method": "전기분야 공정별(변전소, 전차선, 케이블 포설) 상세 시공계획서 수립, 예정공정표(Critical Path) 검토, 시공 순서 및 안전/품질 관리대책 수립 후 감리단 공학적 승인 완수",
        "color": "blue",
        "step1_title": "공종별 상세 시공절차 수립", "step1_desc": "변전기기 반입, Cable Tray 설치, 전차선 지주 입립 시공 순서 및 3D BIM 공정 수립",
        "step2_title": "주공정선(CP) & 예정공정표", "step2_desc": "한전 22.9kV 수전 마일스톤 및 차량 시운전 일정에 부합하는 주공정선(Critical Path) 최적화",
        "step3_title": "안전/품질/환경 관리계획", "step3_desc": "고소 작업 안전 펜스, 활선 가압 안전 구획, 소음/진동 저감 및 비산먼지 방지 대책 수립",
        "step4_title": "감리단 시공계획 승인", "step4_desc": "전기분야 시공계획서 종합 작성, 책임감리단 결재 승인 제출 및 현장 시공팀 공식 배포"
    },
    13: {
        "wbs": "9000-3-13",
        "task": "자재공급원/기자재 제작도서 승인",
        "folder": "13_자재공급원_기자재 제작도서 승인",
        "prefix": "자재공급원_기자재 제작도서 승인",
        "method": "전기자재 공급원 자격 검증(KS/KC 인증, 공장등록증, 납품실적), 제조사 시험성적서 대조 및 공장 제작 승인도면(Shop Drawing) 감리단 적격 승인 수검",
        "color": "indigo",
        "step1_title": "자재공급원 적격성 검증", "step1_desc": "제조사 공장등록증, 사업자등록증, ISO 품질인증서 및 유사 철도/트램 납품 실적 검증",
        "step2_title": "시험성적서 & KS/KC 대조", "step2_desc": "국가 공인기관(KTR, KTL) 시험성적서 원본, KS/KC 인증서 유효기간 및 시방 부합성 대조",
        "step3_title": "제작도서(Shop Drawing) 승인", "step3_desc": "제작도면, 단선결선도, 부품 배치도 및 유지보수용 예비품 목록 감리단 공학 승인 제출",
        "step4_title": "자재공급원 승인 통보", "step4_desc": "감리단 승인 완료된 자재공급원 승인서 수령 및 현장 자재 입고/제작사 발주 최종 확정"
    },
    14: {
        "wbs": "9000-3-14",
        "task": "전기설비 공정제작 / 제작사 공장검사",
        "folder": "14_전기설비 공정제작 _ 제작사 공장검사",
        "prefix": "전기설비 공정제작 _ 제작사 공장검사",
        "method": "정류기, 변압기, ESS, GIS, SCADA 제작사 공장 공정 제작 관리 및 감리단/발주처 입회 공장시험(FAT: Factory Acceptance Test) 수행과 시험성적서 승인 완수",
        "color": "emerald",
        "step1_title": "공장 제작 공정 진척 관리", "step1_desc": "제작사 부품 조달 현황, 외함 판금/도장 및 내부 배선 조립 공정 공정표 100% 관리",
        "step2_title": "FAT 공장시험 절차서 검토", "step2_desc": "공장인수시험(FAT) 절차서, 절연저항, 내전압, 변압비 및 구조 검사 항목 사전 확정",
        "step3_title": "감리단 입회 FAT 시험", "step3_desc": "책임감리단 및 품질담당자 입회하에 정류기/변압기 FAT 공장시험 수행 및 부합성 검측",
        "step4_title": "공장시험성적서 승인 & 출하", "step4_desc": "FAT 시험 성과표 서명, 공장시험성적서 감리단 최종 승인 및 현장 출하 반입 승인 통보"
    },
    15: {
        "wbs": "9000-3-15",
        "task": "본공사 전 선행공정 인수인계 점검",
        "folder": "15_본공사 전 선행공정 인수인계 점검",
        "prefix": "본공사 전 선행공정 인수인계 점검",
        "method": "토목, 노반(궤도), 건축 선행 공정 완성도 실측, 변전실/개구부/공동구 간섭 점검, 자재 반입구 및 반입 동선 인수인계 합동 점검 수행",
        "color": "teal",
        "step1_title": "선행 공종 완성도 실측", "step1_desc": "건축 변전실 구조물 완성도, 노반 궤도 시공 상태 및 전기 설치 간섭 여부 정밀 실측",
        "step2_title": "반입구 & 운반경로 확인", "step2_desc": "수배전반, 변압기 반입구 개구부 치수, 양중 크레인 작업 위치 및 공동구 인입 경로 체크",
        "step3_title": "인수인계 체크리스트 작성", "step3_desc": "토목/건축-전기 간 선행 공정 인수인계 점검표 작성 및 미비사항 시정 조치 요구",
        "step4_title": "인수인계 양해각서 체결", "step4_desc": "선행 공종 담당자와 전기 시공팀 간 인수인계 확인서 체결 및 전기 본공사 착수 승인"
    },
    16: {
        "wbs": "9000-3-16",
        "task": "장비반입 및 안전교육",
        "folder": "16_장비반입 및 안전교육",
        "prefix": "장비반입 및 안전교육",
        "method": "고소작업차, 케이블 포설차, 활선 작업 장비 현장 반입 동선/적치장 확인, 장비 Spec 및 안전검사필증 점검, 작업원 특별안전교육 실시",
        "color": "cyan",
        "step1_title": "장비 반입동선 & 적치장", "step1_desc": "장비 진입 경로 및 적치장 사전확인, 타분야 작업 일정 및 지상/지하 구조물 간섭 협의",
        "step2_title": "장비 Spec & 검사필증 점검", "step2_desc": "산업안전보건공단 안전 검사합격증, 장비 Spec, 조종원 면허증 및 일일 점검표 1:1 검증",
        "step3_title": "작업원 특별안전교육 실시", "step3_desc": "고소 작업 및 고압전기 취급 작업원 대상 특별안전교육 실시 및 서명 교육일지 작성",
        "step4_title": "장비 반입 승인 & 작업 착수", "step4_desc": "장비 반입 승인표 부착, 현장 안전관리자 최종 점검 및 전기 시공 장비 투입 허가"
    },
    17: {
        "wbs": "9000-3-17",
        "task": "자재 반입 및 검수",
        "folder": "17_자재 반입 및 검수",
        "prefix": "자재 반입 및 검수",
        "method": "전기자재 현장 반입 하차 위치/동선 통제, 승인된 자재공급원 일치 여부(Serial No., Serial Tag) 검수, 도면 규격 및 수량 1:1 대조 확인",
        "color": "sky",
        "step1_title": "하차 위치 & 반입동선 통제", "step1_desc": "자재 하차 통제 구획 설정, 크레인 양중 신호수 배치 및 자재 반입 동선 안전 확보",
        "step2_title": "자재공급원 일치성 검수", "step2_desc": "승인된 자재공급원서와 반입 자재 제조사, 모델명, Serial Number 및 인증 표찰 대조",
        "step3_title": "규격, 수량 & 외관 검사", "step3_desc": "납품 인보이스 대조, 도면 규격/수량 일치 검수 및 파손/스크래치 외관 결함 검측",
        "step4_title": "자재검측요청서 감리 승인", "step4_desc": "자재 검수 입회 서명, 자재검측요청서 감리단 결재 승인 및 자재 창고 입고 등록"
    },
    18: {
        "wbs": "9000-3-18",
        "task": "전철전력설비 반입 및 설치",
        "folder": "18_전철전력설비 반입 및 설치",
        "prefix": "전철전력설비 반입 및 설치",
        "method": "변전소 수배전반, 정류기, ESS, 특고압반 및 정거장 전기실 기기 반입/설치, 시공 샘플 감리 협의 후 시험시공 및 도면 일치성 최종 검측",
        "color": "amber",
        "step1_title": "시험시공 & 시공샘플 승인", "step1_desc": "감리/감독 협의를 통한 시공 샘플 대상 선정, 시험시공 수행 및 시공 기준서 확정",
        "step2_title": "특고압반/변압기/ESS 반입", "step2_desc": "정거장 전기실 및 변전소 내 특고압반, 저압반, 변압기, ESS 기계적 수평 안착 설치",
        "step3_title": "특고압 케이블 단자 접속", "step3_desc": "22.9kV 특고압 케이블 포설, 단체 터미널 압착, 토크 렌치 수치 준수 및 절연 처리",
        "step4_title": "설치 완료 감리 검측", "step4_desc": "도면 준수 여부 및 접지선 체결 상태 검측, 시공 완료 보고서 감리단 최종 승인"
    },
    19: {
        "wbs": "9000-3-19",
        "task": "수전용 케이블 트레이 및 케이블 포설",
        "folder": "19_수전용 케이블 트레이 및 케이블 포설",
        "prefix": "수전용 케이블 트레이 및 케이블 포설",
        "method": "한전 책임분계점으로부터 수전 전기실까지 케이블 트레이 수평/수직 고정 설치, 특고압 케이블 포설 및 단말 접속, 절연저항/내전압 시험 완수",
        "color": "indigo",
        "step1_title": "한전 책임분계점 트레이 설치", "step1_desc": "한전 인수점 지중 맨홀부터 수전 전기실까지 Cable Tray 수평도 및 고정 행거 설치",
        "step2_title": "특고압 케이블 포설 작업", "step2_desc": "케이블 장력계 사용 허용 장력 준수, 곡률 반경(외경 12배 이상) 확보 및 포설 검측",
        "step3_title": "특고압 단말 접속 & 접지", "step3_desc": "엘보 커넥터 및 종단 접속 키트 시공, 차폐층 접지선 단자 체결 및 성형 처리",
        "step4_title": "절연저항 & 내전압 시험", "step4_desc": "5,000V Megger 절연저항 측정, DC 내전압 시험 성과표 작성 및 감리단 검측 승인"
    },
    20: {
        "wbs": "9000-3-20",
        "task": "수전 및 전기공급(급전)",
        "folder": "20_수전 및 전기공급(급전)",
        "prefix": "수전 및 전기공급(급전)",
        "method": "KESC 사용전검사 합격증 수령, 전기가압계획 수립 및 한전 가입 요청, 수전 전 기기별 자체시험 수행 후 통신/신호/기계 공종별 단계적 전기공급(급전) 시행",
        "color": "emerald",
        "step1_title": "사용전검사 필증 수령", "step1_desc": "한국전기안전공사 KESC 사용전검사 합격 필증 수령 및 수전 사전 조건 완수",
        "step2_title": "전기가압계획 & 한전 요청", "step2_desc": "수전 전 안전 구획 펜스, 경고 표찰 설치, 가압계획서 제출 및 한전 수전 가입 요청",
        "step3_title": "수전 전 기기별 자체시험", "step3_desc": "보호계전기 동작 시험, GIS 인터록, 변압기 무부하 절연 시험 등 수전 전 시험 완수",
        "step4_title": "22.9kV 수전 & 단계별 급전", "step4_desc": "한전 22.9kV 수전, 정류기/ESS 가압 및 기계/신호/통신 분야별 일정에 따른 급전 통보"
    },
    21: {
        "wbs": "9000-3-21",
        "task": "종합연동시험(SCADA) 실시",
        "folder": "21_종합연동시험(SCADA) 실시",
        "prefix": "종합연동시험(SCADA) 실시",
        "method": "책임감리단 입회하에 트램관제실(OCC)과 현장 변전소/정류기/ESS 기기 간 SCADA 원격 감시/제어/계측(DI/DO/AI/AO) 종합연동시험 수행 및 검측 승인",
        "color": "purple",
        "step1_title": "종합연동시험 계획서 작성", "step1_desc": "감리단 제출용 SCADA 종합연동시험 계획서, 포인트 맵 및 점검 절차서 작성",
        "step2_title": "현장 기기-관제 인터페이스", "step2_desc": "변전소 RTU와 트램관제실(OCC) 서버 간 IEC 61850 / Modbus 통신 연동 시험",
        "step3_title": "DI/DO/AI/AO 신호 검측", "step3_desc": "차단기 개폐 제어(DO), 상태 감시(DI), 전압/전류 계측(AI) 및 락아웃 1:1 검증",
        "step4_title": "연동시험 성과표 감리 승인", "step4_desc": "감리단 입회 최종 시험 수행, SCADA 연동시험 성과표 결재 및 관제 승인 완수"
    },
    22: {
        "wbs": "9000-3-22",
        "task": "공종별 시험",
        "folder": "22_공종별 시험",
        "prefix": "공종별 시험",
        "method": "철도종합시험운행 시행지침 제6조(공종별시험)에 의거하여 변전, 전차선, 전력 설비 공종별 절연, 보호계전기, 통전 시험을 정밀 수행하고 보고서 승인",
        "color": "rose",
        "step1_title": "철도종합시험 지침 기준 수립", "step1_desc": "철도종합시험운행 시행지침 제6조에 따른 전기 공종별 시험 항목 및 절차서 확정",
        "step2_title": "변전/전차선/전력 시험 수행", "step2_desc": "정류기 변환 효율, 전차선 높이/편위 및 750V DC 전압 강화 성능 정밀 시험",
        "step3_title": "보호계전기 차단 시퀀스", "step3_desc": "단락/지락 사고 전류 주입 시험, 디지털 릴레이 차단 시퀀스 및 인터록 검증",
        "step4_title": "공종별 시험 결과 보고서", "step4_desc": "공종별 시험 성과표 종합 작성, 책임감리단 및 발주처 승인 결재 완수"
    },
    23: {
        "wbs": "9000-3-23",
        "task": "차량 투입 전 점검",
        "folder": "23_차량 투입 전 점검",
        "prefix": "차량 투입 전 점검",
        "method": "노반/궤도 시공상태 점검, 트램 건축한계(폭 3,600mm) 검사, 전차선 750V DC 가압, 차량충전설비, 신호/통신 작동상태 합동 사전 점검 완수",
        "color": "amber",
        "step1_title": "노반/궤도 & 건축한계 검사", "step1_desc": "궤도 시공 정밀도 확인 및 트램 차량 건축한계(폭 3,600mm) 간섭 여부 레이저 실측",
        "step2_title": "전차선 가압 & 편위 점검", "step2_desc": "전차선 DC 750V 가압 상태, 팬터그래프 접촉 높이 및 선로 중심 편위(±100mm) 검측",
        "step3_title": "차량충전설비 & 신호/통신", "step3_desc": "정거장 및 차량기지 급속 충전 스티치, 무선통신(LTE-R) 및 신호 연동 작동 점검",
        "step4_title": "차량 투입 허가서 체결", "step4_desc": "차량/전기/신호/궤도 합동 점검표 작성, 책임감리단 차량 현장 투입 승인서 교부"
    },
    24: {
        "wbs": "9000-3-24",
        "task": "차량 시운전",
        "folder": "24_차량 시운전",
        "prefix": "차량 시운전",
        "method": "철도안전법 제26조(철도차량 형식승인)에 의거하여 본선 구간 트램 차량, 전차선 전력, 신호, 통신 시스템 간 인터페이스 시험 및 동력 성능 시운전 수행",
        "color": "blue",
        "step1_title": "철도안전법 제26조 형식승인", "step1_desc": "철도안전법 철도차량 형식승인 절차에 따른 본선 구간 전기-차량 시운전 계획 수립",
        "step2_title": "본선 구간 동력 시운전", "step2_desc": "트램 차량 속도별(10/30/50km/h) 주행 시 전차선 집전 상태, 전압 강하 및 집전 성능 검측",
        "step3_title": "차량-전력-신호 인터페이스", "step3_desc": "회생제동 energy 반환, ESS 충방전 모드 전환 및 차상-지상 신호 인터페이스 검증",
        "step4_title": "차량 시운전 성과표 승인", "step4_desc": "차량 시운전 측정 데이터 종합 분석, 시운전 성과표 감리단 및 교통안전공단 제출"
    },
    25: {
        "wbs": "9000-3-25",
        "task": "운영자 교육시행",
        "folder": "25_운영자 교육시행",
        "prefix": "운영자 교육시행",
        "method": "전기설비(변전, 전차선, SCADA, ESS) 제작사 취급 설명 매뉴얼 기반 운영사 및 관제 유지보수자 대상 이론/실습 교육 시행 및 교육 이수증 교부",
        "color": "indigo",
        "step1_title": "운영자 교육 교재/매뉴얼", "step1_desc": "전기자재 제작사 작성 운영/유지보수 매뉴얼, 비상 조치 절차서 및 교육 교재 검토",
        "step2_title": "변전/전력설비 이론 교육", "step2_desc": "운영사 관제자 및 전기 기술자 대상 22.9kV GIS, 정류기, ESS 작동 원리 강의 시행",
        "step3_title": "현장 기기 조작 실습 교육", "step3_desc": "현장 차단기 수동/전동 개폐, LOCAL/REMOTE 전환 및 비상 트립 리셋 실습 수행",
        "step4_title": "교육 이수증 교부 & 결과보고", "step4_desc": "운영자 교육 평가 시행, 교육 이수증 교부 및 교육결과 보고서 결재 완수"
    },
    26: {
        "wbs": "9000-3-26",
        "task": "사전점검",
        "folder": "26_사전점검",
        "prefix": "사전점검",
        "method": "철도종합시험운행 시행지침 제8조(사전점검)에 따라 발주처-운영자 합동 사전점검계획 수립, 시설물 검증 가능성 점검 후 7일 이내 한국교통안전공단 제출 완수",
        "color": "emerald",
        "step1_title": "철도종합시험 지침 제8조 수립", "step1_desc": "철도종합시험운행 시행지침 제8조에 의거, 발주처-운영자 합동 사전점검 계획서 수립",
        "step2_title": "발주처-운영자 합동 사전점검", "step2_desc": "전기/전차선/SCADA 공종별 시설물의 시설물검증시험 수행 가능 여부 100% 점검",
        "step3_title": "결함사항 시정 조치 및 이행", "step3_desc": "합동 사전점검 중 도출된 지적사항 현장 시정 조치 및 재검측 확인서 서명",
        "step4_title": "교통안전공단 보고서 제출", "step4_desc": "점검 완료 후 7일 이내 사전점검 결과보고서를 한국교통안전공단에 공식 제출"
    },
    27: {
        "wbs": "9000-3-27",
        "task": "시설물 검증시험",
        "folder": "27_시설물 검증시험",
        "prefix": "시설물 검증시험",
        "method": "철도종합시험운행 시행지침 제12조/제13조에 의거 시설물검증시험계획 전문기관 승인, 시설물 정상작동, 안전상태, 차량 운행 적합성 검증 후 7일 내 공단 제출",
        "color": "purple",
        "step1_title": "지침 제12조 검증계획 승인", "step1_desc": "시설물검증시험계획을 운영자와 협의 수립하고 한국교통안전공단 전문기관 승인 수검",
        "step2_title": "제13조 시설물 검증시험 시행", "step2_desc": "전기 시설물 정상작동 상태, 전차선 가압 안전성, 차량-전력 연계성 100% 실측 검증",
        "step3_title": "안전상태 & 차량 적합성", "step3_desc": "최대 주행 속도 시 집전 상태, 전압 변동율 및 비상 차단 안전 성능 종합 검측",
        "step4_title": "7일 이내 공단 결과보고 제출", "step4_desc": "시설물검증시험 결과보고서 작성, 점검 후 7일 이내 한국교통안전공단 공식 제출"
    },
    28: {
        "wbs": "9000-3-28",
        "task": "영업시운전",
        "folder": "28_영업시운전",
        "prefix": "영업시운전",
        "method": "철도종합시험운행 시행지침 제22조/제23조에 의거 영업시운전계획 수립/승인, 영업 조건 열차운행, 종사자 업무 숙달 검증 후 결과보고서 공단 제출 및 국토부 보고",
        "color": "rose",
        "step1_title": "지침 제22조 시운전계획 승인", "step1_desc": "운영자-발주처 협의 영업시운전계획 수립, 국토부 전문기관(교통안전공단) 승인 완수",
        "step2_title": "제23조 영업시운전 시행", "step2_desc": "실제 영업 타임테이블 기반 열차운행체계, 관제/유지보수 종사자 업무 숙달 검증",
        "step3_title": "전기/급전 시스템 안정성", "step3_desc": "연속 주행 시 변전소 급전 용량, ESS 충방전 연동 및 전력 품질 안정성 최종 확검",
        "step4_title": "7일 내 공단 제출 & 국토부 보고", "step4_desc": "결과보고서 7일 내 공단 제출, 공단 14일 내 국토부 보고 후 국토부 7일 내 승인 통보"
    },
    29: {
        "wbs": "9000-3-29",
        "task": "전기 사용신청",
        "folder": "29_전기 사용신청",
        "prefix": "전기 사용신청",
        "method": "관할 한국전력공사에 전기사용신청서, 건축허가서, 수전 도면 및 위임장 제출 수속(소요 기간 약 1개월 관리) 및 수전 합의 완수",
        "color": "amber",
        "step1_title": "전기사용신청 서류 종합 작성", "step1_desc": "관할 한국전력공사 제출용 전기사용신청서, 변전소 용량 계산서 및 위임장 작성",
        "step2_title": "건축허가서 & 수전도면 첨부", "step2_desc": "지자체 건축허가신청서, 22.9kV 수전 단선결선도 및 변전실 배치 평면도 첨부 검토",
        "step3_title": "한전 접수 & 처리기간(1개월)", "step3_desc": "한전 관할 지정 접수, 처리기간 1개월 기준 예정공정표 마일스톤 연동 추적 통제",
        "step4_title": "수전 통지서 수령 & 완료", "step4_desc": "한전 수전 승인 통지서 수령, 공사비 계상 확인 및 변전소 가압 준비 완료"
    },
    30: {
        "wbs": "9000-3-30",
        "task": "공사계획신고",
        "folder": "30_공사계획신고",
        "prefix": "공사계획신고",
        "method": "관할 한국전기안전공사에 전기 공사 착수 전 공사계획서, 기술자 자격증, 감리원 배치서 및 도면 제출 수속 완료",
        "color": "blue",
        "step1_title": "공사계획서 & 신고서 작성", "step1_desc": "전기사업법 시행규칙에 맞춘 공사계획서 및 전기설비 공사계획신고서 정밀 작성",
        "step2_title": "감리원 배치서 & 기술자 자격", "step2_desc": "책임감리원 배치확인서, 전기공사기술자 자격 수첩 및 현장대리인 선임서 첨부",
        "step3_title": "한국전기안전공사 접수", "step3_desc": "관할 한국전기안전공사(KESC) 공사 착수 전 신고서 제출 및 기술 검토 수속",
        "step4_title": "공사계획신고 수리 필증 교부", "step4_desc": "전기안전공사 수리 필증 교부 수령, 현장 공무 대장 보관 및 공사 착수 공식 확인"
    },
    31: {
        "wbs": "9000-3-31",
        "task": "노면전차선로 적합성 검증",
        "folder": "31_전차선로 적합성 검증",
        "prefix": "전차선로 적합성 검증",
        "method": "한국전기철도기술협회에 차량 시운전 전까지 수량조서, 시공도면 및 시험성적서 제출(처리기간 15일)하여 적합성 검증 승인 완수",
        "color": "indigo",
        "step1_title": "전차선로 수량조서 & 도면", "step1_desc": "노면전차선로 지주, 강성 가선, 브래킷 수량조서 및 시공 승인도면(Shop Drawing) 작성",
        "step2_title": "전기철도기술협회 서류 제출", "step2_desc": "차량 시운전 착수 전 한국전기철도기술협회 적합성 검증 신청서 및 시험 성과표 제출",
        "step3_title": "처리기간 15일 추적 관리", "step3_desc": "협회 기술 검토 처리기간 15일 이내 보완 요구사항 대응 및 현장 실측 확인",
        "step4_title": "적합성 검증확인서 발급", "step4_desc": "한국전기철도기술협회 적합성 검증확인서 최종 발급 수령 및 시운전 승인 수검"
    },
    32: {
        "wbs": "9000-3-32",
        "task": "전기 사용전검사 (전력/전차선/송변전)",
        "folder": "32_전기 사용전검사 (전력_전차선_송변전)",
        "prefix": "전기 사용전검사 (전력_전차선_송변전)",
        "method": "전기사업법 제63조, 도로법 제56조, 도로교통법 제69조에 의거 한국전기안전공사 사용전검사(7일전 신청), 지자체 도로점용허가(2주전), 경찰서 도로공사신고(3일전) 통합 수검 완료",
        "color": "emerald",
        "step1_title": "전기사업법 제63조 사용전검사", "step1_desc": "전기설비 설치 완료 후 7일 전 사용전검사신청서, 감리배치서, 단선도, 자재성적서 제출",
        "step2_title": "도로법 제56조 도로점용허가", "step2_desc": "지방국토청/지자체에 도로점용 2주 전 신청, 7~10일 소요 도로점용허가서 교부 완료",
        "step3_title": "도로교통법 제69조 도로공사신고", "step3_desc": "관할 경찰서에 공사 3일 전 도로공사신고서 제출, 2~3일 소요 승인 필증 수령",
        "step4_title": "전력/전차선/송변전 합격증", "step4_desc": "한국전기안전공사 현장 입회 수검, 사용전검사 합격증 발급 수령 및 전력 가압 완수"
    }
}

# Template code generators
def gen_standard_html(idx, d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 전기분야 - {d['task']} 표준서 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Electrical Standard (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 표준서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: 현장 전철전력팀 (책임감리단 공조) | "{d['step1_title']}, {d['step2_title']} & 표준 수칙"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-8">
        
        <!-- ⚖️ 근거 법령, 국가 설계기준 및 입찰안내서 검토 기준 -->
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 국가 기준 · 업무 표준 규정 (Legal & Bidding Verification)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">업무이행 표준</span>
            </div>
            
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 전기사업법, 건설기술 진흥법, KDS 47 00 00 철도설계기준 및 입찰안내서에 의거하여, <strong>{d['task']}에 대한 상세 기준 및 감리단 공학적 승인 수칙</strong>을 체계적으로 확정하는 표준입니다.
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                
                <!-- Card 1 -->
                <div class="bg-amber-50/70 p-4 rounded-xl border border-amber-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-amber-900 text-xs">📌 {d['step1_title']}</span>
                        <span class="text-[10px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded border border-amber-300">단계 1</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step1_desc']}"</strong>
                    </p>
                </div>

                <!-- Card 2 -->
                <div class="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-indigo-900 text-xs">📐 {d['step2_title']}</span>
                        <span class="text-[10px] bg-indigo-200 text-indigo-900 font-bold px-2 py-0.5 rounded border border-indigo-300">단계 2</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step2_desc']}"</strong>
                    </p>
                </div>

                <!-- Card 3 -->
                <div class="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-emerald-900 text-xs">🛡️ {d['step3_title']}</span>
                        <span class="text-[10px] bg-emerald-200 text-emerald-900 font-bold px-2 py-0.5 rounded border border-emerald-300">단계 3</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step3_desc']}"</strong>
                    </p>
                </div>

                <!-- Card 4 -->
                <div class="bg-sky-50/70 p-4 rounded-xl border border-sky-200/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-sky-900 text-xs">📄 {d['step4_title']}</span>
                        <span class="text-[10px] bg-sky-200 text-sky-900 font-bold px-2 py-0.5 rounded border border-sky-300">단계 4</span>
                    </div>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">
                        <strong>"{d['step4_desc']}"</strong>
                    </p>
                </div>

            </div>
        </div>

        <!-- 🎯 표준 목적 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl">
            <h3 class="text-base font-bold text-amber-950 mb-2 flex items-center gap-2">
                <span>🎯</span> 표준 목적 (Objective)
            </h3>
            <p class="text-slate-800 text-sm font-medium leading-relaxed">
                {d['method']}
            </p>
        </div>

        <!-- 📜 업무수행 수칙 -->
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span>📜</span> 업무수행 핵심 수칙 (Execution Rules)
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-red-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 1</span>
                        <h4 class="font-bold text-slate-900 text-sm">시방 기준 100% 검증 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        철도설계기준 및 발주처 시방서 기준과의 부합성을 사전 검측하고 오차 발생 시 즉시 감리단과 협의함.
                    </p>
                </div>

                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">수칙 2</span>
                        <h4 class="font-bold text-slate-900 text-sm">산출물 결재 승인 수칙</h4>
                    </div>
                    <p class="text-slate-700 text-xs leading-relaxed">
                        모든 검측 서표 및 보고서는 책임감리단 공식 결재 승인을 완료받아 관리대장에 공식 보관함.
                    </p>
                </div>
            </div>
        </div>

        <!-- 📦 증빙 산출물 -->
        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <h3 class="text-base font-bold text-emerald-950 mb-1 flex items-center gap-2">
                    <span>📦</span> 증빙 산출물 (Deliverables)
                </h3>
                <p class="text-slate-700 text-xs font-medium">{d['task']} 관련 승인 보고서, 검측 성과표 및 감리 결재 문서 사본</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">
                최종 승인 완료
            </span>
        </div>

    </div>
</div>
</body>
</html>
"""

def gen_guideline_html(idx, d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 전기분야 - {d['task']} 상세 수행지침서 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        .clickable-diagram {{
            cursor: zoom-in !important;
            transition: all 0.25s ease !important;
            position: relative !important;
        }}
        .clickable-diagram:hover {{
            transform: scale(1.01) !important;
            box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important;
        }}
        .clickable-diagram::after {{
            content: "🔍 클릭하여 대형 확대보기";
            position: absolute; bottom: 12px; right: 16px;
            background: rgba(15, 23, 42, 0.8); color: #ffffff;
            font-size: 11px; font-weight: 700; padding: 4px 12px;
            border-radius: 20px; backdrop-filter: blur(4px);
            pointer-events: none; opacity: 0.9;
        }}
        .zoom-modal {{
            display: none; position: fixed; z-index: 9999;
            left: 0; top: 0; width: 100%; height: 100%;
            overflow: auto; background-color: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(6px); align-items: center; justify-content: center;
        }}
        .zoom-modal.active {{ display: flex; }}
        .zoom-modal-content {{
            background-color: #ffffff; margin: auto; padding: 28px;
            border: 1px solid #cbd5e1; width: 95%; max-width: 1100px; max-height: 90vh;
            border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative; overflow-y: auto; text-align: center;
        }}
        .zoom-close {{
            color: #64748b; position: absolute; right: 20px; top: 16px;
            font-size: 32px; font-weight: bold; cursor: pointer;
        }}
        .zoom-close:hover {{ color: #ef4444; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Electrical Guideline (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: 현장 전철전력팀 (책임감리단 공조) | "{d['step1_title']}, {d['step2_title']} 수행 방법론"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        
        <!-- 💡 검토 개요 및 목표 -->
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 {d['task']} 업무수행 방법 및 절차</h4>
            <p class="bg-white p-4 rounded-xl border border-amber-300 font-medium text-slate-900 leading-relaxed text-xs sm:text-sm">
                {d['method']}
            </p>
        </div>

        <!-- 🚀 4단계 상세 검토 방법 및 수행 절차 -->
        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🛠️</span> {d['task']} 상세 수행 절차
            </h2>

            <div class="grid grid-cols-1 gap-6">
                
                <!-- STEP 1 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 01</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step1_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">단계 1</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step1_desc']}<br>
                        • <strong>세부 지침:</strong> 설계도서 및 시방서 기준과 1:1 대조 실측하여 오차 범위를 허용 기준 내 통제함.
                    </p>
                </div>

                <!-- STEP 2 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-indigo-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 02</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step2_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-indigo-700 bg-indigo-100 px-2.5 py-0.5 rounded-full">단계 2</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step2_desc']}<br>
                        • <strong>세부 지침:</strong> 현장 실측 및 3D BIM 간섭 검토를 통해 시공 장애 요소를 사전에 소멸시킴.
                    </p>
                </div>

                <!-- STEP 3 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 03</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step3_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">단계 3</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step3_desc']}<br>
                        • <strong>세부 지침:</strong> 안전 및 품질 기준 준수 여부를 검측하고 불합격 요소 발생 시 즉시 시정 조치함.
                    </p>
                </div>

                <!-- STEP 4 -->
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-teal-600 text-white font-bold text-xs px-3 py-1 rounded-full">STEP 04</span>
                            <h3 class="font-bold text-base text-slate-900">{d['step4_title']}</h3>
                        </div>
                        <span class="text-xs font-semibold text-teal-700 bg-teal-100 px-2.5 py-0.5 rounded-full">단계 4</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
                        • <strong>수행 방식:</strong> {d['step4_desc']}<br>
                        • <strong>세부 지침:</strong> 최종 결과 보고서 작성 후 책임감리단 공식 승인 제출 및 현장 공유 완수.
                    </p>
                </div>

            </div>
        </div>

        <!-- 🖼️ 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2">
                <span class="text-amber-600">🖼️</span> {d['task']} 상세 수행 절차도
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_r{idx}_elec', '[WBS {d['wbs']}] {d['task']} 상세 수행 절차도')">
                <svg id="svg_r{idx}_elec" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="200" fill="#f8fafc" rx="8"/>
                    <rect x="15" y="15" width="520" height="170" fill="#ffffff" stroke="#d97706" stroke-width="2" rx="6"/>
                    <text x="275" y="38" font-size="13" font-weight="black" fill="#b45309" text-anchor="middle">⚡ 동탄트램 {d['task']} 상세 수행 절차도</text>
                    <line x1="25" y1="46" x2="525" y2="46" stroke="#e2e8f0" stroke-width="1.5"/>
                    
                    <g transform="translate(25, 55)">
                        <rect x="0" y="0" width="145" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="6"/>
                        <text x="72.5" y="22" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">1. {d['step1_title'][:10]}</text>
                        <text x="12" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 시방 기준 1:1 대조</text>
                        <text x="12" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 사전 준비 수칙 검측</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="22" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">2. {d['step2_title'][:10]}</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#0f172a">• 3D BIM 간섭 조정</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#0f172a">• 실측 시공 기준 수립</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="22" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">3. {d['step4_title'][:10]}</text>
                        <text x="10" y="45" font-size="8" font-weight="bold" fill="#15803d">• 감리단 최종 결재</text>
                        <text x="10" y="65" font-size="8" font-weight="bold" fill="#15803d">• 업무 승인 완수</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS {d['wbs']} {d['task']} 승인 보고서 감리단 최종 결재 완수</text>
                </svg>
            </div>
        </div>

    </div>
</div>

<!-- 🟣 시공 도식 확대 팝업 모달 -->
<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 {d['task']} 2D Visual 도식 확대 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
    </div>
</div>

<script>
    function openDiagramZoom(elementId, titleText) {{
        const srcEl = document.getElementById(elementId);
        if (!srcEl) return;
        
        const zoomBody = document.getElementById('zoomBody');
        document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "{d['task']} 도식 대형 확대 보기");
        zoomBody.innerHTML = srcEl.outerHTML;
        
        const innerSvg = zoomBody.querySelector('svg');
        if (innerSvg) {{
            innerSvg.setAttribute('width', '100%');
            innerSvg.setAttribute('height', '520px');
            innerSvg.style.maxWidth = '1050px';
        }}
        document.getElementById('zoomModal').classList.add('active');
    }}

    function closeZoomModal() {{
        document.getElementById('zoomModal').classList.remove('active');
    }}

    function closeZoomModalOutside(event) {{
        if (event.target.id === 'zoomModal') closeZoomModal();
    }}

    window.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') closeZoomModal();
    }});
</script>
</body>
</html>
"""

def gen_checklist_html(idx, d):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 전기분야 - {d['task']} 체크리스트 (WBS {d['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        .zoom-modal {{
            display: none; position: fixed; z-index: 9999;
            left: 0; top: 0; width: 100%; height: 100%;
            overflow: auto; background-color: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(6px); align-items: center; justify-content: center;
        }}
        .zoom-modal.active {{ display: flex; }}
        .zoom-modal-content {{
            background-color: #ffffff; margin: auto; padding: 28px;
            border: 1px solid #cbd5e1; width: 95%; max-width: 1100px; max-height: 90vh;
            border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative; overflow-y: auto; text-align: center;
        }}
        .zoom-close {{
            color: #64748b; position: absolute; right: 20px; top: 16px;
            font-size: 32px; font-weight: bold; cursor: pointer;
        }}
        .zoom-close:hover {{ color: #ef4444; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <!-- 🔵 헤더 영역 -->
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Electrical Checklist (WBS {d['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{d['task']} 체크리스트</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {d['wbs']} | 주관: 현장 전철전력팀 (책임감리단 공조) | "16개 정밀 검측 문항 1:1 수평대응 서식 (~하였는가? 어미 100% 통일)"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-6">
        
        <!-- 💡 체크리스트 점검의 핵심 의미 -->
        <div class="bg-amber-50 border-2 border-amber-300 p-5 sm:p-6 rounded-2xl text-xs text-amber-950 space-y-3 shadow-sm">
            <div class="flex items-center justify-between border-b border-amber-200 pb-2.5">
                <h4 class="font-black text-sm text-amber-900 flex items-center gap-2">
                    <span class="text-base">⚠️</span> {d['task']} 체크리스트 점검의 핵심 의미
                </h4>
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">시공 전/중 검측</span>
            </div>
            
            <p class="text-slate-800 leading-relaxed font-semibold">
                본 체크리스트는 동탄트램 전기분야 {d['task']} 업무 이행에 대해 <strong>{d['method']} 관련 실무 요소를 100% 사전 검측하여 시공 하자 및 안전 사고를 예방하기 위한 필수 서식</strong>입니다.
            </p>
        </div>

        <!-- 📊 1:1 정밀 수평대응 3컬럼 체크리스트 테이블 (16개 핵심 문항) -->
        <div class="overflow-x-auto border border-slate-200 rounded-xl shadow-sm">
            <table class="w-full text-left border-collapse text-xs">
                <thead>
                    <tr class="bg-slate-100 border-b border-slate-200 text-slate-700">
                        <th class="p-4 font-bold w-44 text-center border-r border-slate-200">검토 단계 (Procedure)</th>
                        <th class="p-4 font-bold border-r border-slate-200">필수 검측 및 확인 항목 (Inspection Criteria)</th>
                        <th class="p-4 font-bold w-32 text-center">점검 결과</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 bg-white">
                    
                    <!-- STEP 1 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-amber-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 1</span>
                            <span class="font-bold text-slate-900 text-xs">{d['step1_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[{d['step1_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">1. {d['step1_desc']} 사항을 관련 규정에 따라 정밀 검측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[시방 기준 수치 대조]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">2. 발주처 특기시방서 및 KDS 47 00 00 철도설계기준 허용 오차 범위 준수 여부를 대조하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[자공급원 및 세부 사양 확인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">3. 승인된 자재공급원서 및 제작 사양서와의 일치 여부를 1:1 현장 실측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-amber-900 text-[11px] block mb-0.5">[사전 검측 서표 작성]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">4. 해당 공종 착수 전 필수 서표 및 검측 체크리스트 작성을 완료하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                    <!-- STEP 2 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-indigo-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 2</span>
                            <span class="font-bold text-slate-900 text-xs">{d['step2_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[{d['step2_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">5. {d['step2_desc']} 수칙 준수 여부를 현장에서 실측 확인하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[3D BIM 간섭 여부]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">6. 타 공종(토목, 신호, 통신, 차량)과의 3D 공간 간섭 및 미비점을 조율하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[시공 정밀도 및 배치 실측]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">7. 정거장 및 변전소 내 설비 배치 평면도 상의 치수 정밀도를 실측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-indigo-900 text-[11px] block mb-0.5">[현장 조건 변경 승인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">8. 현장 조건 변동 발생 시 감리단 사전 서면 승인 절차를 이행하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                    <!-- STEP 3 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-emerald-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 3</span>
                            <span class="font-bold text-slate-900 text-xs">{d['step3_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[{d['step3_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">9. {d['step3_desc']} 항목을 정밀 검사하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[안전 및 보호구 착용]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">10. 활선 작업 및 고소 작업 투입 인력의 안전 보호구 착용 상태를 검측하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[시험 성과표 기록]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">11. 절연저항, 내전압, 접지저항 등 계측 수치를 성과표에 누락 없이 기록하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80 border-b-2 border-slate-300">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-emerald-900 text-[11px] block mb-0.5">[부적합 항목 시정]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">12. 검측 시 발생한 불합격 및 결함 항목의 시정 조치를 완료하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                    <!-- STEP 4 (4개 문항) -->
                    <tr class="hover:bg-slate-50/80">
                        <td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                            <span class="bg-teal-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP 4</span>
                            <span class="font-bold text-slate-900 text-xs">{d['step4_title'][:10]}</span>
                        </td>
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[{d['step4_title']}]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">13. {d['step4_desc']} 사항을 책임감리단에 정식 제출하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[감리 입회 검측 서명]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">14. 책임감리원 입회 검측을 수검하고 서명을 완수하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[승인서 사본 보관]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">15. 최종 결재 승인을 완료받은 서표 및 승인서 사본을 공무 대장에 보관하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>
                    <tr class="hover:bg-slate-50/80">
                        <td class="p-3.5 border-r border-slate-200">
                            <span class="font-bold text-teal-900 text-[11px] block mb-0.5">[다음 공정 착수 승인]</span>
                            <p class="text-slate-800 font-medium leading-relaxed">16. 본 검측 결과에 따라 다음 단계 공정 착수 승인을 완료하였는가?</p>
                        </td>
                        <td class="p-3.5 align-middle text-center bg-slate-50/30">
                            <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                                <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                            </label>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>

    </div>
</div>
</body>
</html>
"""

print("Starting HTML generation for WBS 11 to 32...")
for idx in range(11, 33):
    d = wbs_data[idx]
    folder_path = os.path.join(base_dir, d['folder'])
    os.makedirs(folder_path, exist_ok=True)
    
    # 1. Standard HTML
    std_dir = os.path.join(folder_path, '표준서')
    os.makedirs(std_dir, exist_ok=True)
    std_file = os.path.join(std_dir, f"{d['prefix']}_표준서.html")
    with open(std_file, 'w', encoding='utf-8') as f:
        f.write(gen_standard_html(idx, d))
    print(f"Generated: {std_file}")
    
    # 2. Guideline HTML
    gui_dir = os.path.join(folder_path, '수행지침')
    os.makedirs(gui_dir, exist_ok=True)
    gui_file = os.path.join(gui_dir, f"{d['prefix']}_수행지침.html")
    with open(gui_file, 'w', encoding='utf-8') as f:
        f.write(gen_guideline_html(idx, d))
    print(f"Generated: {gui_file}")
    
    # 3. Checklist HTML
    chk_dir = os.path.join(folder_path, '체크리스트')
    os.makedirs(chk_dir, exist_ok=True)
    chk_file = os.path.join(chk_dir, f"{d['prefix']}_체크리스트.html")
    with open(chk_file, 'w', encoding='utf-8') as f:
        f.write(gen_checklist_html(idx, d))
    print(f"Generated: {chk_file}")

print("\nALL HTML FILES GENERATED SUCCESSFULLY!")
