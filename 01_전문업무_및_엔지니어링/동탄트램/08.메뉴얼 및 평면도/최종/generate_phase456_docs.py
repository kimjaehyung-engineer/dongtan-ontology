import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

# -----------------------------------------------------------------------------
# Signal (신호분야 - 22 Activities) Detailed Data Dictionary
# -----------------------------------------------------------------------------
signal_details = {
    "9000-1-1": {
        "title": "설계적정성 검토",
        "purp": "신호시스템(CBI, 축차계수기, 선로전환기, 트램 우선신호 등) 설계적정성, 시공성 및 SIL 4 안전성 종합 검토",
        "meth": "입찰안내서/RFP 요구사항 대조, 국가철도공단 KCS/KEC/IEC 62278 표준 검토, 전자연동장치(CBI) 정거장/유치선 선로용량 계산, 교차로 우선신호(PPC) 인터페이스 적정성 검토",
        "outp": "신호설계 적정성 검토 보고서, 인터페이스 조치계획서, 기술검토 회의록",
        "std": """● [SIL 4 안전성 규격] 전자연동장치(CBI)는 IEC 61508/62278/62425 기준 SIL 4 (Safety Integrity Level 4) 인증을 득한 2oo3 (2-out-of-3) 또는 2oo2 철도 전용 안전 컴퓨터 시스템 적용.
● [위험고장간격/안전율] CBI 시스템의 위험고장간격(MTBF) ≥ 10^9 시간 이상, 위험감소계수(RRF) > 10,000 만족.
● [축차계수기 정밀도] 축차계수기(Axle Counter) Wheel Detector(RSR180/SK30) 레일 웨브 장착 토크 45~50 Nm, 차량 열차 축 검지 오차 0 ppm (무오차), 반응속도 ≤ 50ms.
● [선로전환기 전환력] 전동/유압식 선로전환기 쇄정장치(Claw Lock) 전환력 4.5~6.0 kN, 밀착검지 갭 1.5mm 이하, 쇄정오차 2.0mm 초과 시 신호 정지 현시 연동.
● [트램 우선신호 PPC 연동] 교차로 PPC(Priority Pass Control) 보드와 LTE-R/LTE 모뎀 연동 신호 처리 지연시간 ≤ 100ms, 트램 접근 시 전용 녹색 현시(Priority Green) 신호주기 TOD 연동 100% 보장.""",
        "crit": """● [KCS 42 00 00] 철도신호공사 표준시방서 및 국가철도공단 KR C-14030 (전자연동장치 기술기준)
● [IEC 62278 / EN 50126] 철도 신뢰성·가용성·유지보수성·안전성(RAMS) 규격
● [IEC 62425] 철도 신호용 안전관련 전자제어시스템 규격 (SIL 4)
● [노면전차 가이드라인] 국토교통부 트램 전용 우선신호 제어기 및 신호기 설치 기술기준""",
        "adv": """● [자문 의견] 전자연동장치(CBI) 하드웨어 2중화/3중화 카드 수급 일정을 고려하여 발주 6개월 전 제작 승인 완료 필요.
● [현장 관리] 교차로 트램 우선신호 제어기 함체는 도로 제어기 함체와 이격거리 2m 이상 확보하여 노이즈 간섭 방지.""",
        "steps": """[Step 1: 사전 준비 & 인터페이스 체크]
1) 입찰 요구도서와 신호 기본/실시 설계도서의 진로수, 선로전환기 개수, 정거장 및 유치선 배선도 일치성 검토.
2) 도로교통공단 및 지자체 교통신호 제어기와 트램 PPC(우선신호제어기) 간 물리적/논리적 인터페이스(RS-485 / Ethernet) 사전 조사.
3) 전자연동장치(CBI) 수용 기능실(OCC/정거장 신호기계실)의 항온항습(22±2℃, 50±10%) 및 전원(AC 220V/DC 110V UPS 2시간) 환경 검토.

[Step 2: 설비 검토 & 기술 규격 검증]
1) CBI 중앙처리장치(CPU), 입출력(I/O) 모듈, Vital Relay 접점 수량 및 SIL 4 인증서 유효성 검증.
2) 축차계수기(Axle Counter) 평가장치(Evaluator Board)와 지상 센서 간 임피던스 매칭 및 케이블(Shielded Twisted Pair) 감쇄량 검토.
3) 선로전환기(Point Machine) 쇄정 기커버, 내부 밀착 스위치 접점 정밀도 및 스트로크(110mm/140mm) 검토.

[Step 3: 시험, 시운전 & SIL 검증]
1) CBI 연동도표(Interlocking Table) 시뮬레이션 시험으로 과주 방지(Overlap), 쇄정(Locking), 수동 해제 기능 검증.
2) 우선신호 제어기(PPC)와 LTE 모뎀 간 TOD 연동 테스트 시행 및 신호 현시 응답속도(≤ 100ms) 데이터 측정.
3) 최종 설계적정성 검토보고서를 작성하여 감리단 및 발주처 승인 득함.""",
        "risk": """● [LLBS 리스크 1] 교차로 일반차량 신호제어기와 트램 우선신호 제어기 간 통신 프로토콜 미동기화로 신호 딜레이 및 트램 정지 발생 (대책: PPC 프로토콜 사전 100% 팩토리 시험 실시)
● [LLBS 리스크 2] 유치선 선로전환기 밀착검지 갭 허용 오차(1.5mm) 초과로 인한 연동 불능 및 쇄정 오류 (대책: 시공 전 쇄정 간격 1.0mm 이내 정밀 정렬 수칙 적용)""",
        "chk": """[✔] 전자연동장치(CBI) SIL 4 (IEC 62425) 정식 승인 인증서가 첨부 완료되었는가?
[✔] 정거장 및 유치선 선로전환기 쇄정 간격(1.5mm 이하) 및 밀착검지 센서 사양이 설계와 일치하는가?
[✔] 축차계수기(RSR180) 센서의 레일 체결 토크(45~50 Nm) 규격 및 케이블 차폐 기준이 명시되었는가?
[✔] 교차로 우선신호(PPC) 보드와 LTE 모뎀 간 통신 지연시간(≤ 100ms) 목표값이 표준서에 반영되었는가?
[✔] 신호기계실 UPS 비상 전원(최소 2시간 공급) 및 항온항습 조건(22±2℃)이 설계에 포함되었는가?""",
        "lchk": """[✔] 교차로 지상 감지기(Loop/RF-ID) 및 LTE-R 신호 송수신 간섭 가능성이 사전에 검토되었는가?
[✔] 궤도 분기기 부속 자재와 선로전환기 설치 위치 간 간섭 여부를 3D BIM으로 검증하였는가?""",
        "vchk": """[✔] 신호 전문 협력사의 CBI 소프트웨어 툴 승인 및 기술자 자격증 유효성을 확인하였는가?"""
    },
    "9000-1-2": {
        "title": "착수준비 KOM",
        "purp": "신호분야 공사 발주 전 조직/자재/공정/하자리스크 관리 및 본사-현장 착수 킥오프(KOM) 수립",
        "meth": "신호선형 변동요인 검토, 시공성 및 하자 발생 리스크 분석, 본사-현장 착수 회의 개최, 기술지원 체계 구축",
        "outp": "착수 KOM 결과보고서, 현장설명서 특기시방서, 신호공사 실행예산서",
        "std": """● [착수 준비 기준] 신호공사 착수 전 본사-현장 인터페이스 표준 절차서(SOP) 작성 100% 이행.
● [하자 예방 기준] 타 현장 신호설비 하자사례(선로전환기 쇄정장치 유격, 축차계수기 오작동) 개선대책 100% 시방 반영.
● [품질 관리] SIL 4 인증품 및 철도표준자재(KRS) 구매 사양서 작성 및 감리 승인 절차 규정 준수.
● [안전 관리] 신호 현장 작업자 철도안전원 자격 보유율 100% 확보.""",
        "crit": """● 국가철도공단 철도건설사업 관리지침
● KCS 42 10 00 (신호설비 시공관리지침)
● 당사 품질/안전보건 경영시스템 (ISO 9001/45001)""",
        "adv": """● [자문 의견] 외산 자재(축차계수기, 특수 선로전환기)의 조달 리드타임(최소 8개월)을 고려하여 착수 직후 자재발주 추진 필요.""",
        "steps": """[Step 1: 착수전 인적/물적 자원 준비]
1) 신호 전문기술자(철도신호기술사, 기사) 선임 및 조직도 구성.
2) 신호설비 자재 반입 일정 및 야적장(신호기계실 주변) 공간 확보.

[Step 2: 착수 회의 & 시공성/리스크 분석]
1) 본사-현장 합동 착수 KOM 회의 개최 및 신호분야 R&R 확정.
2) 궤도, 전력, 건축, 통신 공종과의 인터페이스 항목 추출.

[Step 3: 실행계획 확정 & 전파]
1) 현장설명서 및 특기시방서에 하자 방지 항목 추가.
2) 착수 KOM 회의록 작성 및 전 현장 인원 배포.""",
        "risk": """● [LLBS 리스크] 주요 자재 조달 지연에 따른 신호공기 연쇄 지연 (대책: 자재 조달 롱리드 아이템 우선 발주)""",
        "chk": """[✔] 신호분야 착수 KOM 회의록 및 본사-현장 R&R 정의서가 작성되었는가?
[✔] SIL 4 및 KRS 주요 신호 자재 수급 리드타임이 공정표(P6)에 반영되었는가?
[✔] 과거 신호 하자 사례 반영 특기시방서가 완성되었는가?""",
        "lchk": """[✔] 선행 궤도/건축 공종 인도 시점과 신호 자재 반입 일정 간 간섭이 없는지 확인하였는가?""",
        "vchk": """[✔] 협력사 기술 인력의 철도신호 자격증 및 경력증명서 검증을 완료하였는가?"""
    }
}

# Generic fallback builder for Signal activities not individually detailed
def get_signal_data(l4_code, name):
    if l4_code in signal_details:
        return signal_details[l4_code]
    
    # Generic highly enriched signal template
    return {
        "title": name,
        "purp": f"신호분야 {name} 과업의 정밀 시공, SIL 4 안전성 확보 및 기술 기준 준수",
        "meth": f"{name} 관련 국가철도공단 KCS 42 00 00, IEC 62278(RAMS), IEC 62425(SIL 4) 규격에 따른 정밀 작업 및 시험 검증",
        "outp": f"{name} 결과보고서, 검측승인서, 안전검증서, 품질기록서",
        "std": f"""● [SIL 4 안전성] 본 과업은 IEC 61508/62278/62425 SIL 4 신뢰성 및 안전성 절대 기준을 준수한다.
● [정량 수치] 전자연동장치(CBI) 응답시간 ≤ 200ms, 축차계수기(Axle Counter) 오차 0 ppm, 선로전환기 쇄정 유격 ≤ 1.5mm.
● [우선신호 연동] PPC 보드-LTE-R 통신 지연 ≤ 100ms, 교차로 트램 우선신호 제어 100% 정상 작동.
● [품질 공차] 신호기 가시거리 ≥ 200m, LED 초점 정밀도 오차 ±0.5° 이내 제어.""",
        "crit": f"""● KCS 42 00 00 철도신호공사 표준시방서
● KR C-14030 전자연동장치 및 철도신호 제어설비 기술기준
● IEC 62278 / IEC 62425 / EN 50126 철도 안전 규격
● 노면전차(트램) 신호 및 우선신호 제어 시스템 가이드라인""",
        "adv": f"""● [자문 의견] {name} 수행 시 타 공종(궤도, 전력, 통신, 차량)과의 사전 인터페이스 체크리스트를 100% 이행할 것.
● [현장 관리] 작업 전 안전교육 이수 및 철도보호지구 작업 안전 수칙 필수 준수.""",
        "steps": f"""[Step 1: 사전 준비 & 인터페이스 체크]
1) {name} 수행을 위한 설계도서, KCS 시방서 및 SIL 4 기술기준 검토.
2) 궤도, 전력, 통신, 차량 분야 담당자와 현장 인터페이스 및 작업 구간 선점 조율.
3) 투입 계측기(신호발생기, 절연저항계, 오실로스코프 등) 검교정 유효필증 부착 여부 확인.

[Step 2: 장비 반입/설치 & 케이블 포설/작업 수행]
1) {name} 작업 지침 및 안전 수칙에 따라 설비 설치 및 배선 작업 시행.
2) 케이블 차폐 및 접지(접지저항 ≤ 10 Ω) 상태를 실시간 측정한 후 기록.
3) 선로전환기, 축차계수기, PPC 보드 등 핵심 기기의 치수 공차 및 토크(45~50 Nm) 준수.

[Step 3: 시험, 시운전, 검측 & SIL Verification]
1) 단위시험, 연동시험 및 1,000km 무결점 시운전 데이터 측정.
2) SIL 4 안전성 적합성 검증서 작성 및 감리단 검측 승인 득함.
3) 잔여 자재 정리 및 현장 안전 구역 원상 복구 후 준공 도서 작성.""",
        "risk": f"""● [LLBS 리스크 1] {name} 작업 중 케이블 손상으로 인한 CBI 신호 절단 및 연동 오류 발생 (대책: 관로 포설 시 롤러 사용 및 매입 깊이 1.2m 이상 확보)
● [LLBS 리스크 2] 신호 제어기 함체 침수 및 접지 불량으로 인한 결뢰 유입 (대책: IP65 방수 함체 및 독립 접지망 10Ω 이하 구축)""",
        "chk": f"""[✔] {name} 기술 표준 및 정량적 치수 공차가 설계도서 기준을 만족하는가?
[✔] SIL 4 안전성 요구사항 및 KCS 42 00 00 시방 기준이 이행되었는가?
[✔] 케이블 절연저항(≥ 100 MΩ) 및 접지저항(≤ 10 Ω) 측정 결과가 적정한가?
[✔] 선로전환기 쇄정 유격(1.5mm 이하) 및 축차계수기 레일 체결 토크(45~50 Nm)가 확인되었는가?
[✔] 교차로 우선신호(PPC) 연동 및 신호 현시 상태가 정상 작동하는가?""",
        "lchk": f"""[✔] {name} 수행 중 궤도/전력/통신 선행 공정과의 물리적 간섭이 없는지 점검했는가?
[✔] 우기/동절기 기상 악화 시 기계실 및 함체 방수/방진(IP65) 보호 조치가 완료되었는가?""",
        "vchk": f"""[✔] 협력사 현장 대리인 및 기술자의 철도신호 자격 보유 및 품질 교육이 이행되었는가?"""
    }

# -----------------------------------------------------------------------------
# Telecom (통신분야 - 32 Activities) Data Builder
# -----------------------------------------------------------------------------
def get_telecom_data(l4_code, name):
    return {
        "title": name,
        "purp": f"통신분야 {name} 과업의 정밀 시공, LTE-R 무선망 음영 제로화, 72-Core 광케이블망 및 승강장/PSD 연동 기술기준 준수",
        "meth": f"{name} 관련 KCS 41 00 00, LTE-R 기술규격(700MHz Band 28), 광케이블(ITU-T G.652D) 및 방송통신설비 설치기준 준수",
        "outp": f"{name} 기술검토서, 품질시험성적서, LTE-R 무선망 측정데이터, 준공검사 확인서",
        "std": f"""● [LTE-R 무선 커버리지] 700MHz Band 28 대역 음영지역 제로화. 수신신호강도 RSSI ≥ -95 dBm, RSRP ≥ -105 dBm, SINR ≥ 3 dB, 핸드오버 성공률 ≥ 99.5%, 무선 지연시간 ≤ 50ms.
● [72-Core 광백본망] 72-Core 싱글모드 광케이블(SMF) 이중화 링 토폴로지. OTDR 접속 손실 ≤ 0.05 dB/splice, 총 광감쇄량 ≤ 0.35 dB/km (1310nm) / ≤ 0.25 dB/km (1550nm).
● [4K IP CCTV] Ultra HD 4K (8MP, 3840x2160), 30fps, H.265 코덱, ONVIF Profile S/G, 24시간 NVR 이중화 저장.
● [승강장 가이던스 PIS/PA] PIS 도착 안내 오차 ≤ 1초, PA 비상방송 명료도 STI ≥ 0.6, 소음 연동 음량 자동 조절(AGC).
● [PSD 인터페이스] PSD Safety Loop 쇄정 신호 통신 지연 ≤ 100ms, 캔 통신/Ethernet 이중화 인터록 100% 보장.""",
        "crit": f"""● KCS 41 00 00 정보통신공사 표준시방서
● 방송통신설비의 기술기준에 관한 규정 (과학기술정보통신부 고시)
● TTAK.KO-06.0369 (LTE 기반 철도무선통신망 무선인터페이스 규격)
● ITU-T G.652D (특성화 싱글모드 광섬유 케이블 규격)
● KCMVP (국가정보원 암호모듈 검증 기준 - LTE-R 보안적합성)""",
        "adv": f"""● [자문 의견] LTE-R 기지국(RU/DU) 및 안테나 설치 시 터널 및 정거장 기공승낙 및 관제 연동 시험을 사전 수행할 것.
● [현장 관리] 광케이블 접속 작업 시 먼지 방지 텐트 설치 및 Fusion Splicer 광학계 청결 유지 필수.""",
        "steps": f"""[Step 1: 사전 준비 & 음영지역 시뮬레이션]
1) {name} 도면, 광통신 링 구성도, LTE-R 전파 전파(Propagation) 시뮬레이션 데이터 검토.
2) 토목, 건축, 전기, PSD 분야와의 관로/케이블 트레이/기능실 배치 인터페이스 사전 협의.
3) 광파측정기, OTDR, 전파분석기(Spectrum Analyzer) 검교정 필증 확인.

[Step 2: 설비 반입/설치, 광케이블 접속 & 관제 연동]
1) 72-Core 광케이블 포설 및 접속(Fusion Splicer), 4K IP CCTV, PIS/PA, PSD 연동 설비 설치.
2) 케이블 굽힘 반경(외경의 20배 이상) 준수 및 광접속함체 방수 처리(IP68).
3) 관제 센터(OCC) NVR, 통신 서버 및 LTE-R 코어망 인터페이스 케이블 래킹.

[Step 3: 단위/통합 시험, 무선국 허가 & 보안 검증]
1) OTDR 및 광파워메터 측정으로 전 구간 광감쇄량 데이터 확보.
2) LTE-R 무선국 준공검사(KCA) 및 KCMVP 보안적합성 검증 이행.
3) 정보통신 사용전검사 필증 획득 및 감리단 검측 최종 승인.""",
        "risk": f"""● [LLBS 리스크 1] 터널 및 고층 건물 밀집구간 LTE-R 전파 음영 발생으로 통신 절단 (대책: 누설동축케이블 LCX 및 안테나 각도 정밀 시뮬레이션 및 추가 보강)
● [LLBS 리스크 2] 광케이블 포설 중 허용 장력 초과로 인한 코어 단선 (대책: 장력계 부착 윈치 사용 및 허용 장력 150kgf 이하 준수)""",
        "chk": f"""[✔] LTE-R 무선망 RSSI(≥ -95dBm) 및 RSRP(≥ -105dBm) 목표 수준이 달성되었는가?
[✔] 72-Core 광케이블 OTDR 접속 손실(≤ 0.05dB/splice) 및 총 감쇄량이 시방 기준 이내인가?
[✔] 4K IP CCTV 영상 해상도(3840x2160) 및 NVR 24시간 이중화 저장 기능이 정상인가?
[✔] 승강장 PIS 안내 표시 오차(≤ 1초) 및 PA 방송 명료도(STI ≥ 0.6)가 검증되었는가?
[✔] PSD Safety Loop 연동 통신 반응속도(≤ 100ms) 및 이중화 인터록이 작동하는가?""",
        "lchk": f"""[✔] 자가용전기통신설비 신고 및 LTE-R 무선국 허가 서류가 관할 관청에 정식 접수되었는가?
[✔] KCMVP 국가정보원 암호모듈 승인서가 확보되어 보안적합성을 충족하였는가?""",
        "vchk": """[✔] 정보통신 전문 협력사의 자격 면허 및 현장 감리원 검측 확인을 완료하였는가?"""
    }

# -----------------------------------------------------------------------------
# Electrical (전기분야 - 32 Activities) Data Builder
# -----------------------------------------------------------------------------
def get_electrical_data(l4_code, name):
    return {
        "title": name,
        "purp": f"전기분야 {name} 과업의 정밀 시공, 변전소 DC 750V 급전, 전차선/무전차선 정거장 정차 급속 충전 및 누설전류(Stray Current) 부식 방지 기술기준 준수",
        "meth": f"{name} 관련 KEC(한국전기설비규정), KCS 44 00 00, EN 50122(철도 접지 및 누설전류) 및 특고압(22.9kV) 수전 지침 준수",
        "outp": f"{name} 기술검토서, 전기안전공사 사용전검사 필증, 시험성적서, SCADA 연동 확인서",
        "std": f"""● [변전소 DC 750V 급전] 22.9kV AC 수전 -> 12-Pulse 다이오드 정류 변압기 -> DC 750V (전압 범위 DC 500V~900V), GIS $SF_6$ 가스 압력 0.45 MPa, 차단기 차단용량 25kA.
● [전차선/무전차선 급속 충전] 가공전차선(OCS) 강체 T-Bar 편위 오차 ±15mm 이내. 무전차선 구간 정거장 급속 충전(Pantograph Rapid Charger) DC 750V / 1000A, ESS Supercapacitor 30초 내 80% 충전 완료.
● [Stray Current 디오드 접지] 레일 비접지 귀선 계통(Ungrounded DC Return). 누설전류 방지 디오드 접지 장치(Polarization Cell) 레일-대지 전압 ≤ 120V (EN 50122-2), 레일 절연저항 ≥ 10 $\Omega \cdot km$.
● [22.9kV 특고압 수전 케이블] 22.9kV XLPE (CN/CO-W) 케이블 절연저항 ≥ 2,000 M$\Omega$, AC 37.5kV 10분 내전압 시험 합격.
● [SCADA 연동] IEC 60870-5-104 원격제어 제어 응답시간 ≤ 100ms, 계측 데이터 전송 주기 ≤ 1초.""",
        "crit": f"""● KEC (한국전기설비규정 - 산업통상자원부 공고)
● KCS 44 00 00 전철전력공사 표준시방서
● EN 50122-1/2 (철도응용 - 보호접지 및 누설전류 방지 규격)
● KR C-13010 (전선로 및 변전설비 기술기준)
● 전기사업법 및 전기안전관리법 (사용전검사 규정)""",
        "adv": f"""● [자문 의견] 22.9kV 특고압 수전 및 전차선 가압 시 한전(KEPCO) 및 관제 센터와 세부 가압 일정을 사전 확정하고 안전 통제구역 설정 필수.
● [현장 관리] 정거장 급속 충전장치 접촉 부 접속부의 열화상 촬영을 통한 접촉 저항 점검 이행.""",
        "steps": f"""[Step 1: 사전 준비 & 수전/급전 수시 계획]
1) {name} 전기 단선도, 변전소 배치도, 전차선(OCS/무전차선 ESS) 상세 설계도서 검토.
2) 토목, 궤도, 건축, 신호, 차량 분야와의 인터페이스(공동관로, 궤도 귀선, 충전 암 위치) 사전 체크.
3) 절연저항계(5000V), 내전압시험기, 접지저항계 검교정 유효필증 부착 점검.

[Step 2: 설비 반입/설치, 케이블 포설 & 디오드 접지 시공]
1) 22.9kV 수전반, DC 750V 정류기, 전차선 T-Bar / 무전차선 급속 충전기 및 케이블 포설.
2) 누설전류 방지 디오드 접지장치 설치 및 주행 레일 간 절연 블록(Insulation Joint) 시공.
3) 특고압 케이블 단말 처리(Terminator) 및 삼상 일괄 접속 작업 시행.

[Step 3: 내전압/가압 시험, SCADA 연동 & 사용전검사]
1) 케이블 내전압 시험(AC 37.5kV 10분) 및 변전소 DC 750V 무부하/부하 시운전 시행.
2) SCADA 원격제어 모니터링 연동 테스트 및 디오드 접지 전압(≤ 120V) 실측.
3) 한국전기안전공사(KESC) 전기 사용전검사 승인 필증 획득 및 최종 준공.""",
        "risk": f"""● [LLBS 리스크 1] 주행레일 직류 귀선 부 절연 파손으로 누설전류(Stray Current) 발생하여 매설 배관 부식 (대책: 레일 대지 절연저항 10Ω·km 이상 확보 및 디오드 접지 모니터링)
● [LLBS 리스크 2] 무전차선 정거장 급속 충전기 펜타그래프 접촉 오차로 인한 아크(Arc) 발생 및 집전판 손상 (대책: 펜타그래프 안착 정밀도 ±10mm 이내 세팅)""",
        "chk": f"""[✔] 변전소 DC 750V 전압 정밀도(500V~900V) 및 GIS 가스 압력(0.45 MPa)이 적정한가?
[✔] 전차선 강체 T-Bar 편위 오차(±15mm 이내) 및 무전차선 급속 충전기 충전 시간(30초 80%)이 검증되었는가?
[✔] 누설전류 방지 디오드 접지장치의 레일-대지 전압(≤ 120V) 및 레일 절연저항(≥ 10Ω·km)이 달성되었는가?
[✔] 22.9kV 특고압 케이블 내전압 시험(AC 37.5kV 10분) 합격 성적서가 부착되었는가?
[✔] SCADA 원격제어 응답시간(≤ 100ms) 및 KEC 전기설비규정 기준을 충족하였는가?""",
        "lchk": f"""[✔] 한전(KEPCO) 22.9kV 수전 계통 연계 신청 및 전기안전공사 사용전검사 일정이 확정되었는가?
[✔] 변전소 및 전차선 가압 작업에 따른 현장 위험성 평가 및 안전 통제 구역 가설이 완료되었는가?""",
        "vchk": """[✔] 전기공사 전문 협력사의 전기공사기사 자격 배치 및 감리 검측 확인서를 확보했는가?"""
    }

# -----------------------------------------------------------------------------
# HTML Templates
# -----------------------------------------------------------------------------
def make_standard_html(disc_name, code, title, data):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{disc_name} - {data['title']} 기술 표준서</title>
    <style>
        :root {{
            --primary-color: #2563EB;
            --primary-light: #EFF6FF;
            --text-color: #1F2937;
            --bg-color: #F9FAFB;
            --card-bg: #FFFFFF;
            --border-color: #E5E7EB;
        }}
        body {{
            font-family: 'Inter', '맑은 고딕', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            padding: 40px;
        }}
        .header {{
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .breadcrumb {{
            font-size: 0.85rem;
            color: #6B7280;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
        }}
        .title {{
            font-size: 1.8rem;
            color: #111827;
            margin: 0;
            font-weight: 800;
        }}
        .meta-info {{
            display: flex;
            gap: 15px;
            margin-top: 12px;
            font-size: 0.9rem;
            color: #6B7280;
            flex-wrap: wrap;
        }}
        .badge {{
            background-color: var(--primary-light);
            color: var(--primary-color);
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }}
        h2 {{
            font-size: 1.25rem;
            color: #111827;
            border-left: 4px solid var(--primary-color);
            padding-left: 12px;
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            margin-bottom: 25px;
            font-size: 0.9rem;
        }}
        th, td {{
            border: 1px solid var(--border-color);
            padding: 12px 16px;
        }}
        th {{
            background-color: var(--primary-light);
            color: #1E3A8A;
            font-weight: 700;
            width: 25%;
        }}
        .bullet-list {{
            list-style: none;
            padding-left: 0;
            margin-bottom: 25px;
        }}
        .bullet-list li {{
            position: relative;
            padding-left: 20px;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }}
        .bullet-list li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--primary-color);
            font-weight: 700;
        }}
        .code-block {{
            background-color: #F3F4F6;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            margin-bottom: 20px;
            border-left: 4px solid var(--primary-color);
        }}
        .footer-note {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            font-size: 0.85rem;
            color: #9CA3AF;
            text-align: center;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS {code} Technical Standard</div>
        <h1 class="title">{data['title']} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> {disc_name} / 현장 시스템·사업관리팀</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 엔지니어링팀</span>
            <span>|</span>
            <span><span class="badge">설계 및 엔지니어링 기술 표준 규격</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr>
                <th>과업 목적</th>
                <td>{data['purp']}</td>
            </tr>
            <tr>
                <th>수행 방법</th>
                <td>{data['meth']}</td>
            </tr>
            <tr>
                <th>주요 산출물</th>
                <td>{data['outp']}</td>
            </tr>
        </tbody>
    </table>

    <h2>2. 정량적 기술 표준 (Technical Specifications & SIL)</h2>
    <div class="code-block">{data['std']}</div>

    <h2>3. 첨부서류 연계 상세 설계기준 (Design Criteria & Regulations)</h2>
    <div class="code-block">{data['crit']}</div>

    <h2>4. 하자 예방 및 기술자문 (Advisory & Lessons Learned)</h2>
    <div class="code-block">{data['adv']}</div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 철도시스템 엔지니어링 기술 표준서 | WBS {code}
    </div>
</div>
</body>
</html>
"""

def make_guideline_html(disc_name, code, title, data):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{disc_name} - {data['title']} 작업 수행지침서</title>
    <style>
        :root {{
            --primary-color: #059669;
            --primary-light: #ECFDF5;
            --text-color: #1F2937;
            --bg-color: #F9FAFB;
            --card-bg: #FFFFFF;
            --border-color: #E5E7EB;
            --danger-color: #EF4444;
        }}
        body {{
            font-family: 'Inter', '맑은 고딕', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            padding: 40px;
        }}
        .header {{
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .breadcrumb {{
            font-size: 0.85rem;
            color: #6B7280;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
        }}
        .title {{
            font-size: 1.8rem;
            color: #111827;
            margin: 0;
            font-weight: 800;
        }}
        .meta-info {{
            display: flex;
            gap: 15px;
            margin-top: 12px;
            font-size: 0.9rem;
            color: #6B7280;
            flex-wrap: wrap;
        }}
        .badge {{
            background-color: var(--primary-light);
            color: var(--primary-color);
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }}
        h2 {{
            font-size: 1.25rem;
            color: #111827;
            border-left: 4px solid var(--primary-color);
            padding-left: 12px;
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        .proc-box {{
            background-color: #F3F4F6;
            padding: 20px;
            border-radius: 8px;
            font-size: 0.93rem;
            white-space: pre-wrap;
            margin-bottom: 25px;
            line-height: 1.7;
        }}
        .risk-box {{
            background-color: #FEF2F2;
            border-left: 4px solid var(--danger-color);
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin: 25px 0;
            font-size: 0.9rem;
            color: #991B1B;
            white-space: pre-wrap;
        }}
        .footer-note {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            font-size: 0.85rem;
            color: #9CA3AF;
            text-align: center;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS {code} Execution Guideline</div>
        <h1 class="title">{data['title']} 작업 수행지침서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> {disc_name} / 현장 시공팀</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 안전품질공무팀</span>
            <span>|</span>
            <span><span class="badge">현장 작업 실행 표준 절차서</span></span>
        </div>
    </div>

    <h2>1. 작업 개요 및 기본 방침 (Overview)</h2>
    <p><strong>주요 목적:</strong> {data['purp']}</p>
    <p><strong>수행 방법:</strong> {data['meth']}</p>
    <p><strong>최종 산출물:</strong> {data['outp']}</p>

    <h2>2. 3단계 작업 절차 및 세부 행동 지침 (Procedures)</h2>
    <div class="proc-box">{data['steps']}</div>

    <h2>3. 하자 예방 및 위험요인 관리 (Risk Management - LLBS)</h2>
    <div class="risk-box"><strong>[집행단계 주요 리스크 및 하자 방지 대책]</strong><br><br>{data['risk']}</div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 철도시스템 엔지니어링 수행지침서 | WBS {code}
    </div>
</div>
</body>
</html>
"""

def make_checklist_html(disc_name, code, title, data):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{disc_name} - {data['title']} 검측 체크리스트</title>
    <style>
        :root {{
            --primary-color: #D97706;
            --primary-light: #FEF3C7;
            --text-color: #1F2937;
            --bg-color: #F9FAFB;
            --card-bg: #FFFFFF;
            --border-color: #E5E7EB;
        }}
        body {{
            font-family: 'Inter', '맑은 고딕', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            padding: 40px;
        }}
        .header {{
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .breadcrumb {{
            font-size: 0.85rem;
            color: #6B7280;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
        }}
        .title {{
            font-size: 1.8rem;
            color: #111827;
            margin: 0;
            font-weight: 800;
        }}
        .meta-info {{
            display: flex;
            gap: 15px;
            margin-top: 12px;
            font-size: 0.9rem;
            color: #6B7280;
            flex-wrap: wrap;
        }}
        .badge {{
            background-color: var(--primary-light);
            color: var(--primary-color);
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }}
        h2 {{
            font-size: 1.25rem;
            color: #111827;
            border-left: 4px solid var(--primary-color);
            padding-left: 12px;
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        .chk-box {{
            background-color: #FFFBEB;
            border: 1px solid #FDE68A;
            padding: 20px;
            border-radius: 8px;
            font-size: 0.93rem;
            white-space: pre-wrap;
            margin-bottom: 25px;
            line-height: 1.8;
            color: #92400E;
        }}
        .footer-note {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            font-size: 0.85rem;
            color: #9CA3AF;
            text-align: center;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS {code} Inspection Checklist</div>
        <h1 class="title">{data['title']} 완료 검측 체크리스트</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> {disc_name} / 품질검측팀</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 감리단 및 품질보증팀</span>
            <span>|</span>
            <span><span class="badge">현장 이행 검측 승인 도구</span></span>
        </div>
    </div>

    <h2>1. 완료 검측 세부 체크리스트 (Inspection Items)</h2>
    <div class="chk-box">{data['chk']}</div>

    <h2>2. 집행단계 리스크 점검사항 (LLBS Risk Checklist)</h2>
    <div class="chk-box">{data['lchk']}</div>

    <h2>3. 인터페이스 & 협력사 검측 확인사항 (Subcontractor Verification)</h2>
    <div class="chk-box">{data['vchk']}</div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 철도시스템 엔지니어링 체크리스트 | WBS {code}
    </div>
</div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# Main Generation Logic
# -----------------------------------------------------------------------------
disciplines = [
    ("신호분야", "9000-1", get_signal_data),
    ("통신분야", "9000-2", get_telecom_data),
    ("전기분야", "9000-3", get_electrical_data)
]

total_files_created = 0

for disc_dir_name, wbs_prefix, data_fn in disciplines:
    disc_path = os.path.join(base_dir, disc_dir_name)
    if not os.path.exists(disc_path):
        print(f"Directory not found: {disc_path}")
        continue

    folders = [f for f in os.listdir(disc_path) if os.path.isdir(os.path.join(disc_path, f))]
    print(f"\nProcessing {disc_dir_name} ({len(folders)} activities)...")

    for f_idx, folder_name in enumerate(sorted(folders, key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else 999), 1):
        folder_path = os.path.join(disc_path, folder_name)
        
        # Clean name without leading numbers
        clean_name = re.sub(r'^\d+_', '', folder_name).strip()
        
        # Determine WBS code
        code_sub = folder_name.split('_')[0]
        l4_code = f"{wbs_prefix}-{code_sub}"
        
        data = data_fn(l4_code, clean_name)
        
        # Subdirectories: 표준서, 수행지침, 체크리스트
        subdirs = {
            "표준서": (f"{clean_name}_표준서.html", make_standard_html),
            "수행지침": (f"{clean_name}_수행지침.html", make_guideline_html),
            "체크리스트": (f"{clean_name}_체크리스트.html", make_checklist_html)
        }
        
        for sub_name, (file_name, html_gen_fn) in subdirs.items():
            target_subdir = os.path.join(folder_path, sub_name)
            os.makedirs(target_subdir, exist_ok=True)
            
            target_file_path = os.path.join(target_subdir, file_name)
            html_content = html_gen_fn(disc_dir_name, l4_code, clean_name, data)
            
            with open(target_file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            total_files_created += 1

print(f"\n==================================================")
print(f"SUCCESS: Generated total {total_files_created} HTML files across Signal, Telecom, and Electrical disciplines!")
print(f"==================================================")
