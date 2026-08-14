import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

rows_data = [
    {
        'row': 10,
        'wbs': '9000-7-9',
        'dir_name': '8_작업조 편성',
        'file_prefix': '작업조 편성',
        'title': '작업조 편성',
        'std_legal': '건설산업기본법 & KCS 47 10 25 작업조 규정',
        'badge': '건진법 / 상생조직',
        'objective': '상부강화노반 시공을 위해 쇄석 다짐, 레벨 측량, 맹암거 유공관 부설 전문 기술자 및 숙련 중장비 조종원으로 구성된 전담 작업조를 편성하고, 일일 TBM 및 음주 측정을 실시하여 시공 불량을 사전에 100% 차단함에 있다.',
        'rules': [
            ('수칙 1: 전문 기술자 전담 수칙', '강화노반 다짐, 레벨 측량, 배수구조물 등 주요 공종은 기술 수첩 및 경력이 검증된 전담 인력을 배치함.'),
            ('수칙 2: 안전교육 & 음주 측정 수칙', '작업조 전원에 대해 일일 작업 전 TBM, 음주 측정 및 위험성 평가를 시행하고 대장에 비치함.')
        ],
        'deliv': '작업조 편성표, 근로자 자격 검증 대장, 일일 TBM 대장 및 감리 승인서',
        'steps': [
            ('STEP 01', '공종별 전문 기술자 1:1 배치', '다짐, 측량, 배수 전담 숙련 기술 수첩 보유자를 현장에 전담 배치함.'),
            ('STEP 02', '중장비 조종원 면허 & 경력 대조', '덤프트럭, 강동 롤러, 백호 조종원 면허 및 조종 경력을 1:1 실측 확인함.'),
            ('STEP 03', '일일 TBM & 비상연락망 구축', '작업 착수 전 TBM을 실시하고 관제실 및 감리단 비상 연락망을 100% 현장 게시함.'),
            ('STEP 04', '작업조 조직표 감리 승인', '작업조 편성 대장을 작성하여 책임감리원 공학적 입회 결재를 수검함.')
        ],
        'diagram_title': '👷 동탄트램 강화노반 작업조 편성 및 운영 절차도',
        'diagram_nodes': [('1. 전문인력 배치', '기술자 자격 대조'), ('2. 조종원 면허검증', '장비 경력 확인'), ('3. 감리단 승인', '조직표 결재 완수')],
        'chk_items': [
            '1. 강화노반 다짐, 레벨 측량, 배수 전담 기술자 자격 수첩을 확인하였는가?',
            '2. 강동 롤러, 덤프트럭, 백호 조종원 면허증 및 경력을 1:1 검증하였는가?',
            '3. 신규 반입 근로자 대상 건설업 기초안전보건교육 수료증을 확인하였는가?',
            '4. 작업조별 리더(반장) 및 안전 담당자를 명확히 지정하였는가?',
            '5. 작업 착수 전 위험성 평가 결과를 작업원과 100% 공유하였는가?',
            '6. 일일 TBM 실시 및 서명부를 현장 안전 대장에 철하였는가?',
            '7. 작업전 근로자 음주 측정 및 건강 상태를 일일 점검하였는가?',
            '8. 야간 및 고온/저온 시 비상 대피용 체계를 작업조에 전달하였는가?',
            '9. 작업조별 적정 인원 배치를 통해 과로 및 공기 지연을 예방하였는가?',
            '10. 현장 휴게 공간 및 개인 보호구 지급 상태를 점검하였는가?',
            '11. 비상 시 관제실 및 응급병원 24시간 연락망을 공유하였는가?',
            '12. 외국인 근로자 대상 다국어 안전 수칙 교육을 시행하였는가?',
            '13. 작업조 변경 발생 시 24시간 이내 감리단에 변경 신고하였는가?',
            '14. 시공성 개선 아이디어 제안 제도를 작업조에 안내하였는가?',
            '15. 책임감리원 입회하에 작업조 조직표 서면 결재를 완료하였는가?',
            '16. 승인된 작업조 현황판을 현장 사무실에 게시 보관하고 있는가?'
        ]
    },
    {
        'row': 11,
        'wbs': '9000-7-10',
        'dir_name': '9_장비 수급 계획',
        'file_prefix': '장비 수급 계획',
        'title': '장비 수급 계획',
        'std_legal': '건설기계관리법 & KCS 47 10 25 장비 조합 규정',
        'badge': '장비 관리 / 다짐 사양',
        'objective': '강화노반 고밀도 다짐(다짐도 ≥95%, K30≥110 MN/m³)을 달성하기 위해 10톤 이상 강동 진동 롤러, 타이어 롤러, 3D GPS 제어 모터그레이더 등 검증된 건설기계를 수급하고 사전 안전 점검을 완수함에 있다.',
        'rules': [
            ('수칙 1: 다짐 장비 사양 준수 수칙', '강동 진동 롤러는 자중 10ton 이상, 기중 진동력 250kN 이상의 공학 사양 장비를 반입함.'),
            ('수칙 2: 건설기계 정기검사 수칙', '반입되는 모든 중장비는 건설기계 정기검사합격증 및 후방 경보기/카메라 작동을 100% 점검함.')
        ],
        'deliv': '장비 수급 계획서, 건설기계 반입 검수표, 정기검사 합격증 사본 및 감리 승인서',
        'steps': [
            ('STEP 01', '다짐 장비 조합 사양 확정', '강동 롤러(10t+), 타이어 롤러(15~25t), 모터그레이더(3.7m) 사양을 1:1 결정함.'),
            ('STEP 02', '건설기계 반입전 안전 점검', '유압 누유, 후방 감지 센서, 경고등 및 신호수 배치 상태를 현장 수검함.'),
            ('STEP 03', '진동수/속도 자동 기록계 점검', '강동 롤러 다짐 속도(3~5km/h) 및 진동수(30~45Hz) 센서를 정밀 교정함.'),
            ('STEP 04', '장비 수급 승인서 감리 결재', '장비 수급 계획서 및 반입 검수표를 작성하여 책임감리원 최종 승인을 결재함.')
        ],
        'diagram_title': '🚜 동탄트램 강화노반 장비 수급 및 다짐 장비 조합 절차도',
        'diagram_nodes': [('1. 장비 사양 확정', '강동롤러 10t+ 선정'), ('2. 반입 전 안전점검', '후방센서/검사증 확인'), ('3. 감리 승인', '반입 승인서 결재')],
        'chk_items': [
            '1. 강동 진동 롤러(10ton 이상, 진동력 250kN 이상) 사양을 확인하였는가?',
            '2. 표면 마감용 타이어 롤러(15~25ton) 반입 계획을 수립하였는가?',
            '3. 3D GPS 제어 시스템이 장착된 모터그레이더(3.7m)를 확보하였는가?',
            '4. 백호 굴착기(0.8~1.0m³) 버킷 이탈 방지 핀 체결을 점검하였는가?',
            '5. 반입 건설기계의 정기검사합격증 유효 기간을 확인하였는가?',
            '6. 중장비 후방 경보기 및 후방 카메라 작동 여부를 100% 점검하였는가?',
            '7. 강동 롤러 다짐 속도계(3~5km/h) 및 진동 센서를 교정하였는가?',
            '8. 장비 유압 호스 누유 및 브레이크 제동 성능을 검사하였는가?',
            '9. 전담 신호수 배치 및 경광봉 지급 현황을 확인하였는가?',
            '10. 장비 조종석 비상 정지 스위치 정상 가동 여부를 점검하였는가?',
            '11. 현장 내 중장비 주행 전용 도로 및 속도 제한(20km/h) 표지를 설치하였는가?',
            '12. 비상 시 장비 견인용 와이어 로프 상태를 확인하였는가?',
            '13. 장비 주유 및 정비 구역 기름 유출 방지 포를 설치하였는가?',
            '14. 예비 다짐 롤러 확보를 통해 장비 고장 시 공정 연체를 예방하였는가?',
            '15. 책임감리원 입회하에 장비 반입 점검표 승인을 결재받았는가?',
            '16. 승인된 장비 목록을 현장 공무 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 12,
        'wbs': '9000-7-11',
        'dir_name': '10_노반 재료 입도 DB 확보',
        'file_prefix': '노반 재료 입도 DB 확보',
        'title': '노반 재료 입도 DB 확보',
        'std_legal': 'KCS 47 10 25 & KS F 2302 골재 입도 시험 기준',
        'badge': '자재 시험 / KCS 규격',
        'objective': '상부강화노반용 쇄석 혼합 골재의 공학적 물성(최대입경 50mm, #200체 통과량 ≤5%, 마모율 ≤40%, CBR ≥30%)을 현장 체가름 시험을 통해 사전 검증하고 입도 DB 관리 대장을 구축함에 있다.',
        'rules': [
            ('수칙 1: KCS 47 10 25 입경 준수 수칙', '강화노반 골재 최대 입경은 50mm 이하이어야 하며 200번체 통과량은 5% 이하로 엄격 관리함.'),
            ('수칙 2: 1,000m³당 1회 시험 수칙', '현장 반입 골재 1,000m³당 1회 이상 체가름 시험을 시행하고 입도 곡선을 DB 수록함.')
        ],
        'deliv': '노반 골재 공급원 승인서, 입도분석 시험성적서(KS F 2302), CBR 성적서 및 감리 승인서',
        'steps': [
            ('STEP 01', '석산 공급원 사전 승인 수검', '골재 석산 공급원 입도 성적서, 마모율(≤40%), 편평석 비율을 검토함.'),
            ('STEP 02', '현장 반입 골재 체가름 시험', '반입 1,000m³마다 KS F 2302 체가름 시험을 실시하여 50mm 통과율을 검측함.'),
            ('STEP 03', '입도 곡선 & CBR DB 매핑', '수정 다짐 CBR(≥30%) 및 입도 분포 곡선(Upper/Lower Bound)을 DB 수록함.'),
            ('STEP 04', '입도 DB 보고서 감리 최종 승인', '골재 입도 DB 대장을 정리하여 책임감리단 공학적 입회 결재를 수검함.')
        ],
        'diagram_title': '🪨 동탄트램 강화노반 골재 입도 DB 구축 절차도',
        'diagram_nodes': [('1. 공급원 사전승인', '입도/마모율 성적서'), ('2. 현장 체가름 시험', '1,000m³당 1회 검측'), ('3. 감리 DB 승인', '입도 곡선 대장 결재')],
        'chk_items': [
            '1. 강화노반 골재 석산 공급원 승인 서류를 확인하였는가?',
            '2. 골재 최대 입경이 50mm 이하임을 체가름 시험으로 검증하였는가?',
            '3. #200번 체(0.075mm) 통과량이 5% 이하임을 실측하였는가?',
            '4. 골재 마모율이 40% 이하(KS F 2508)임을 시험성적서로 확인하였는가?',
            '5. 편평·세장석 함유율이 20% 이하임을 검측하였는가?',
            '6. 수정 다짐 CBR 값이 30% 이상임을 확인하였는가?',
            '7. 현장 반입 1,000m³당 1회 이상 체가름 시험을 시행하였는가?',
            '8. 시험용 표준체(50mm, 37.5mm, 19mm, 4.75mm 등) 교정 상태를 확인하였는가?',
            '9. 골재 입도 분포 곡선이 KCS 표준 범주 내에 명확히 위치함을 매핑하였는가?',
            '10. 유기 불순물 및 흙덩어리 함유 여부를 시각 및 세척 시험하였는가?',
            '11. 골재 야적장 비닐 덮개 설치를 통해 빗물에 의한 세립분 유실을 예방하였는가?',
            '12. 불합격 골재 반출 전용 야적 구역을 구별 지정하였는가?',
            '13. 골재 함수비 변화에 따른 다짐도 영향을 사전 시험하였는가?',
            '14. 입도 시험 야장 및 성적서를 입도 DB 시스템에 정밀 등록하였는가?',
            '15. 책임감리원 입회하에 노반 재료 입도 DB 최종 결재를 마쳤는가?',
            '16. 승인된 입도 DB를 현장 품질 관리대장에 철하여 보관하고 있는가?'
        ]
    },
    {
        'row': 13,
        'wbs': '9000-7-12',
        'dir_name': '11_사토장 _ 토사 수급 계획 확인',
        'file_prefix': '사토장 _ 토사 수급 계획 확인',
        'title': '사토장 / 토사 수급 계획 확인',
        'std_legal': '토양환경보전법 & KCS 47 10 25 토사 수불 규정',
        'badge': '토사 수불 / 환경 기준',
        'objective': '상부강화노반 토공 굴착 사토 및 성토 토사의 반출·반입 수급 계획을 수립하고, 정식 인허가 사토장 확보 및 토양 오염 시험 성적서 대조를 통해 사토 민원 및 공정 지연을 사전에 100% 예방함에 있다.',
        'rules': [
            ('수칙 1: 지자체 인허가 사토장 준수 수칙', '사토장은 지자체(화성시) 정식 인허가 사토장이어야 하며 세륜 시설 및 운반 거리를 검증함.'),
            ('수칙 2: 유용 토사 수정다짐 수칙', '성토용 반입 토사는 수정다짐 최대건조밀도(γd max ≥ 1.90 g/cm³) 성적서를 확보함.')
        ],
        'deliv': '사토장 인허가서 사본, 토사 수급 수불 대장, 토양오염 시험성적서 및 감리 승인서',
        'steps': [
            ('STEP 01', '사토장 인허가 서류 & 세륜기 검증', '화성시 정식 사토장 인허가증, 세륜 시설 및 운반 경로(거리 km)를 확인함.'),
            ('STEP 02', '반입 토사 오염도 & 물리 시험', '토양 오염 8개 항목 성적서 및 수정 다짐 시험(최대건조밀도 ≥1.90g/cm³)을 검측함.'),
            ('STEP 03', '토사 수불 운반 대장 일일 기록', '덤프 출하증 및 일일 사토/성토 물량(m³)을 수불 대장에 현장 등록함.'),
            ('STEP 04', '토사 수급 계획서 감리 승인', '사토장 지정 승인서 및 수급 대장에 대해 책임감리원 최종 서면 결재를 완수함.')
        ],
        'diagram_title': '🚚 동탄트램 토사 수급 및 사토장 운반 관리 절차도',
        'diagram_nodes': [('1. 사토장 인허가확인', '화성시 인허가서 대조'), ('2. 토질/오염 시험', 'γd max ≥1.90g/cm³'), ('3. 감리 승인', '토사 수불대장 결재')],
        'chk_items': [
            '1. 사토장의 지자체(화성시/수원시) 정식 개발행위 허가증을 확인하였는가?',
            '2. 사토장 운반 거리(km) 및 덤프트럭 운반 노선 안전성을 검토하였는가?',
            '3. 사토장 입구 자동 세륜 세차 시설 정상 가동 여부를 점검하였는가?',
            '4. 반입 성토 토사의 수정 다짐 최대건조밀도(≥1.90 g/cm³)를 확인하였는가?',
            '5. 반입 토사의 최적함수비(OMC ± 2%) 범주를 시험 검증하였는가?',
            '6. 토양오염우려기준 8개 항목(중금속, 중유 등) 시험성적서를 부착하였는가?',
            '7. 덤프트럭 덮개 체결을 통해 운반 중 토사 낙하 민원을 차단하였는가?',
            '8. 일일 사토/성토 물량(m³) 출하증 전수 확인 및 수불 대장을 기록하였는가?',
            '9. 우천 시 사토장 토사 유출 방지 침사지 및 덮개 설치를 점검하였는가?',
            '10. 토사운반 차량 속도 제한(30km/h) 및 안전 교육을 실시하였는가?',
            '11. 사토장 부지 소유자 동의서 및 사용 승인 기간을 확인하였는가?',
            '12. 현장 내 일시 야적 토사의 사면 비닐 덮개 부설 여부를 검측하였는가?',
            '13. 사토지 경계 지적 조사 및 인접 농지 피해 예방 조치를 이행하였는가?',
            '14. 토사 수급 변경 발생 시 48시간 이내 감리단 보고 절차를 수립하였는가?',
            '15. 책임감리원 입회하에 사토장 지정 승인서를 수검 결재하였는가?',
            '16. 승인된 사토 대장을 현장 공무 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 14,
        'wbs': '9000-7-13',
        'dir_name': '12_배수 처리 계획 수립',
        'file_prefix': '배수 처리 계획 수립',
        'title': '배수 처리 계획 수립',
        'std_legal': 'KCS 47 10 25 & 하천법 가설 배수 규정',
        'badge': '가배수 / 노반 보호',
        'objective': '상부강화노반 시공 중 우천에 의한 노반 연화 및 토사 유출을 방지하기 위하여 가배수로(B=0.6m, H=0.6m), 침사지 2개소, 맹암거 유공관(HDPE Ø200mm) 수급 계획을 수립하고 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 성토 사면 가배수로 수칙', '성토 및 노반 굴착 구역에는 종배수로(0.6×0.6m) 및 집수용 침사지를 필수 설치함.'),
            ('수칙 2: 맹암거 유공관 배수 구배 수칙', '노반 가설 배수 유공관 배수 구배는 0.5% 이상을 확보하고 부직포(200g/m²)를 감쌈.')
        ],
        'deliv': '배수 처리 계획서, 가배수로/침사지 도면, 유공관 시험성적서 및 감리 승인서',
        'steps': [
            ('STEP 01', '가배수로 & 침사지 구배 설계', '성토 사면 종배수로(B=0.6m) 및 용량 계산에 따른 가침사지 2개소를 설계함.'),
            ('STEP 02', 'HDPE 유공관 & 부직포 성적 확인', 'Ø200mm HDPE 유공관 투과율 및 투수성 부직포(200g/m²) 시험성적서를 검측함.'),
            ('STEP 03', '수중 펌프 & 양수 설비 비치', '집수정 양수 펌프(200L/min 이상) 및 비상 발전기를 현장에 정밀 배치함.'),
            ('STEP 04', '배수 계획서 감리 최종 승인', '배수 처리 계획서 및 배수 통로 도면에 대해 책임감리원 서면 결재를 완수함.')
        ],
        'diagram_title': '🌊 동탄트램 강화노반 가배수로 및 배수 처리 절차도',
        'diagram_nodes': [('1. 가배수로/침사지 설계', '종배수로 0.6x0.6m'), ('2. 유공관/부직포 검수', 'HDPE Ø200mm 성적서'), ('3. 감리 승인', '배수계획서 결재')],
        'chk_items': [
            '1. 노반 성토 구간 가배수로(B=0.6m, H=0.6m) 설치 도면을 확인하였는가?',
            '2. 가침사지(2개소 이상) 용량 계산서 및 침전 효율성을 검증하였는가?',
            '3. 맹암거 HDPE 유공관(Ø200mm) 시험성적서를 대조 확인하였는가?',
            '4. 투수성 부직포(200g/m² 이상) 세립분 차단 성능을 검측하였는가?',
            '5. 맹암거 유공관 배수 종단 구배가 0.5% 이상임을 측량 확인하였는가?',
            '6. 우천 시 수중 양수 펌프(200L/min 이상) 2대 이상을 현장 배치하였는가?',
            '7. 양수 펌프 가동용 비상 발전기 유류 및 전기 안전을 점검하였는가?',
            '8. 토공 마무리면 횡단 배수 경사(2% 이상)를 형성하였는가?',
            '9. 종배수로 끝단 탁수 방지 방류형 집수통 설치 여부를 점검하였는가?',
            '10. 토사 침전에 따른 배수로 주간 준설 계획을 수립하였는가?',
            '11. 인접 도로 및 민가로의 우수 유입 방지 가설 턱을 시공하였는가?',
            '12. 유공관 주위 투수성 쇄석(19~25mm) 필터재 입도를 확인하였는가?',
            '13. 집중호우 대비 일일 배수 통제 담당자를 지정 운영하고 있는가?',
            '14. 태풍 및 태풍 특보 시 비상 배수 가동 체계를 구축하였는가?',
            '15. 책임감리원 입회하에 배수 처리 계획서 서면 승인을 결재받았는가?',
            '16. 승인된 배수 도면을 현장 시공팀에 전달하여 이행 관리하고 있는가?'
        ]
    },
    {
        'row': 15,
        'wbs': '9000-7-14',
        'dir_name': '13_안전관리계획 수립 승인',
        'file_prefix': '안전관리계획 수립 승인',
        'title': '안전관리계획 수립 승인',
        'std_legal': '건설기술진흥법 제62조 & 산업안전보건법 제42조',
        'badge': '법정 안전 / CSI 등록',
        'objective': '건설기술 진흥법 제62조에 의거하여 상부강화노반 공사 중 중장비 충돌, 지하시설물 파손 및 운행선 인접 위험 요소를 차단하는 안전관리계획서를 수립하고 국토안전관리원 심사 및 감리 승인을 완수함에 있다.',
        'rules': [
            ('수칙 1: 건진법 제62조 심사 수칙', '안전관리계획서는 정밀 심사 기관(국토안전관리원) 적정 판정 및 감리 서면 승인 후 착공함.'),
            ('수칙 2: CSI 안전관리시스템 등록 수칙', '승인된 안전관리계획서를 건설공사 안전관리 종합정보망(CSI)에 지체 없이 등록함.')
        ],
        'deliv': '안전관리계획서 본안, 국토안전관리원 심사결과통보서, CSI 등록증 및 감리 승인 공문',
        'steps': [
            ('STEP 01', '안전관리계획서 6대 분야 작성', '중장비, 지하 매설물, 추락/전도 방지 및 운행선 안전 계획을 작성함.'),
            ('STEP 02', '국토안전관리원 정밀 심사 수검', '전문 심사 기관에 계획서를 제출하여 기술 심사 보완 지적을 반영함.'),
            ('STEP 03', 'CSI 시스템 전산 등록', '국토교통부 CSI 건설공사 안전관리 종합정보망에 계획서를 최종 등록함.'),
            ('STEP 04', '감리단 최종 서면 승인 수령', '책임감리원 최종 적정 승인 공문을 교부받고 본시공 안전 착수를 시행함.')
        ],
        'diagram_title': '🛡️ 동탄트램 안전관리계획 수립 및 CSI 시스템 승인 절차도',
        'diagram_nodes': [('1. 안전계획서 작성', '6대 분야 위험성 반영'), ('2. CSI 전산 등록', '국토안전관리원 심사'), ('3. 감리 서면승인', '최종 승인공문 수령')],
        'chk_items': [
            '1. 건설기술 진흥법 제62조에 따른 안전관리계획서 6대 분야를 작성하였는가?',
            '2. 상부강화노반 중장비 전도 및 충돌 방지 안전 대책을 명시하였는가?',
            '3. 철도 경계 30m 이내 운행선 인접 작업 안전 수칙을 포함하였는가?',
            '4. 지하 매설 관로(가스, 전력) 파손 방지 현장 통제 대책을 수립하였는가?',
            '5. 안전보건총괄책임자 및 현장 안전관리자 선임계를 확인하였는가?',
            '6. 국토안전관리원 등 지정 기관에 안전관리계획서 심사를 신청하였는가?',
            '7. 전문 심사 기관의 보완 요구 사항을 1:1 보완 조치하였는가?',
            '8. 심사 기관으로부터 최종 "적정" 판정 통보서를 수령하였는가?',
            '9. 국토교통부 CSI 건설공사 안전관리 종합정보망에 계획서를 등록하였는가?',
            '10. 일일 TBM 및 위험성 평가 정례 가동 계획을 반영하였는가?',
            '11. 비상사태 발생 시 비상 대응 훈련 및 응급 이송 체계를 구축하였는가?',
            '12. 신규 근로자 및 장비 조종원 특별 안전교육 계획을 수립하였는가?',
            '13. 안전관리비 사용 계획서 및 현장 집행 대시보드를 구비하였는가?',
            '14. 감리단에 심사 결과서 및 보완 완료본을 공식 제출하였는가?',
            '15. 책임감리원 직인이 날인된 안전관리계획서 최종 승인서를 받았는가?',
            '16. 승인된 안전관리계획서를 현측에 게시하고 준수 관리하고 있는가?'
        ]
    }
]

# 딥빌드 HTML 생성 로직
for item in rows_data:
    target_dir = os.path.join(base_root, item['dir_name'])
    std_dir = os.path.join(target_dir, '표준서')
    gui_dir = os.path.join(target_dir, '수행지침')
    chk_dir = os.path.join(target_dir, '체크리스트')
    
    os.makedirs(std_dir, exist_ok=True)
    os.makedirs(gui_dir, exist_ok=True)
    os.makedirs(chk_dir, exist_ok=True)

    file_pfx = item['file_prefix']

    # 1. 표준서 HTML
    std_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {item['title']} 표준서 (WBS {item['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Standard (WBS {item['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{item['title']} 표준서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {item['wbs']} | 주관: 현장 공사팀 / 공무팀 | "{item['std_legal']}"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-8">
        <div class="bg-slate-50 border border-slate-200 p-6 rounded-2xl shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                    <span class="text-amber-600">⚖️</span> 근거 법령 · 국가 건설기준 (Engineering Standard)
                </h3>
                <span class="text-[11px] bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full border border-red-200 uppercase">{item['badge']}</span>
            </div>
            <p class="text-slate-700 text-xs leading-relaxed font-medium">
                본 표준서는 <strong>{item['std_legal']}</strong>에 의거하여 동탄트램 상부강화노반 시공 시 {item['title']} 과업의 공학적·법적 이행 절차를 완수하기 위한 표준 지침입니다.
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div class="bg-amber-50/70 p-4 rounded-xl border border-amber-200/80 space-y-2">
                    <span class="font-bold text-amber-900 text-xs">📌 1. {item['steps'][0][1]}</span>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">"{item['steps'][0][2]}"</p>
                </div>
                <div class="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200/80 space-y-2">
                    <span class="font-bold text-indigo-900 text-xs">📐 2. {item['steps'][1][1]}</span>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">"{item['steps'][1][2]}"</p>
                </div>
                <div class="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200/80 space-y-2">
                    <span class="font-bold text-emerald-900 text-xs">🛡️ 3. {item['steps'][2][1]}</span>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">"{item['steps'][2][2]}"</p>
                </div>
                <div class="bg-sky-50/70 p-4 rounded-xl border border-sky-200/80 space-y-2">
                    <span class="font-bold text-sky-900 text-xs">📄 4. {item['steps'][3][1]}</span>
                    <p class="text-slate-800 leading-relaxed text-[11px] font-medium">"{item['steps'][3][2]}"</p>
                </div>
            </div>
        </div>

        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl">
            <h3 class="text-base font-bold text-amber-950 mb-2 flex items-center gap-2"><span>🎯</span> 표준 목적 (Objective)</h3>
            <p class="text-slate-800 text-sm font-medium leading-relaxed">{item['objective']}</p>
        </div>

        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-b-2 border-amber-600 pb-2 flex items-center gap-2"><span>📜</span> 업무수행 핵심 수칙</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <span class="bg-red-600 text-white text-xs font-bold px-2.5 py-1 rounded">{item['rules'][0][0]}</span>
                    <p class="text-slate-700 text-xs leading-relaxed">{item['rules'][0][1]}</p>
                </div>
                <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-2">
                    <span class="bg-amber-600 text-white text-xs font-bold px-2.5 py-1 rounded">{item['rules'][1][0]}</span>
                    <p class="text-slate-700 text-xs leading-relaxed">{item['rules'][1][1]}</p>
                </div>
            </div>
        </div>

        <div class="bg-emerald-50 border border-emerald-200 p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <h3 class="text-base font-bold text-emerald-950 mb-1 flex items-center gap-2"><span>📦</span> 증빙 산출물</h3>
                <p class="text-slate-700 text-xs font-medium">{item['deliv']}</p>
            </div>
            <span class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-sm text-center">승인 완료</span>
        </div>
    </div>
</div>
</body>
</html>"""

    # 2. 수행지침 HTML
    gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {item['title']} 상세 수행지침서 (WBS {item['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        .clickable-diagram {{ cursor: zoom-in !important; transition: all 0.25s ease !important; position: relative !important; }}
        .clickable-diagram:hover {{ transform: scale(1.01) !important; box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important; }}
        .clickable-diagram::after {{ content: "🔍 클릭하여 대형 확대보기"; position: absolute; bottom: 12px; right: 16px; background: rgba(15, 23, 42, 0.8); color: #ffffff; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; backdrop-filter: blur(4px); pointer-events: none; opacity: 0.9; }}
        .zoom-modal {{ display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(15, 23, 42, 0.75); backdrop-filter: blur(6px); align-items: center; justify-content: center; }}
        .zoom-modal.active {{ display: flex; }}
        .zoom-modal-content {{ background-color: #ffffff; margin: auto; padding: 28px; border: 1px solid #cbd5e1; width: 95%; max-width: 1100px; max-height: 90vh; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); position: relative; overflow-y: auto; text-align: center; }}
        .zoom-close {{ color: #64748b; position: absolute; right: 20px; top: 16px; font-size: 32px; font-weight: bold; cursor: pointer; }}
        .zoom-close:hover {{ color: #ef4444; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Guideline (WBS {item['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{item['title']} 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {item['wbs']} | 주관: 현장 공사팀 / 공무팀 | "{item['std_legal']}"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">
            <h4 class="font-bold text-base flex items-center gap-2">💡 {item['title']} 실무 수행 개요</h4>
            <p class="bg-white p-4 rounded-xl border border-amber-300 font-medium text-slate-900 leading-relaxed text-xs sm:text-sm">
                {item['objective']}
            </p>
        </div>

        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2"><span class="text-amber-600">🛠️</span> {item['title']} 4단계 상세 수행 절차</h2>
            <div class="grid grid-cols-1 gap-6">
                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-600 text-white font-bold text-xs px-3 py-1 rounded-full">{item['steps'][0][0]}</span>
                            <h3 class="font-bold text-base text-slate-900">{item['steps'][0][1]}</h3>
                        </div>
                        <span class="text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">단계 1</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">• <strong>수행 지침:</strong> {item['steps'][0][2]}</p>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-indigo-600 text-white font-bold text-xs px-3 py-1 rounded-full">{item['steps'][1][0]}</span>
                            <h3 class="font-bold text-base text-slate-900">{item['steps'][1][1]}</h3>
                        </div>
                        <span class="text-xs font-semibold text-indigo-700 bg-indigo-100 px-2.5 py-0.5 rounded-full">단계 2</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">• <strong>수행 지침:</strong> {item['steps'][1][2]}</p>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-3 py-1 rounded-full">{item['steps'][2][0]}</span>
                            <h3 class="font-bold text-base text-slate-900">{item['steps'][2][1]}</h3>
                        </div>
                        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">단계 3</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">• <strong>수행 지침:</strong> {item['steps'][2][2]}</p>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-4 shadow-sm">
                    <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-teal-600 text-white font-bold text-xs px-3 py-1 rounded-full">{item['steps'][3][0]}</span>
                            <h3 class="font-bold text-base text-slate-900">{item['steps'][3][1]}</h3>
                        </div>
                        <span class="text-xs font-semibold text-teal-700 bg-teal-100 px-2.5 py-0.5 rounded-full">단계 4</span>
                    </div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed bg-white p-4 rounded-xl border border-slate-200">• <strong>수행 지침:</strong> {item['steps'][3][2]}</p>
                </div>
            </div>
        </div>

        <div class="space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2"><span class="text-amber-600">🖼️</span> {item['title']} 상세 수행 절차도</h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_{item['row']}', '[WBS {item['wbs']}] {item['title']} 상세 수행 절차도')">
                <svg id="svg_{item['row']}" viewBox="0 0 550 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="550" height="200" fill="#f8fafc" rx="8"/>
                    <rect x="15" y="15" width="520" height="170" fill="#ffffff" stroke="#d97706" stroke-width="2" rx="6"/>
                    <text x="275" y="38" font-size="13" font-weight="black" fill="#b45309" text-anchor="middle">{item['diagram_title']}</text>
                    <line x1="25" y1="46" x2="525" y2="46" stroke="#e2e8f0" stroke-width="1.5"/>
                    
                    <g transform="translate(25, 55)">
                        <rect x="0" y="0" width="145" height="85" fill="#fffbeb" stroke="#d97706" stroke-width="1.5" rx="6"/>
                        <text x="72.5" y="25" font-size="10" font-weight="black" fill="#b45309" text-anchor="middle">{item['diagram_nodes'][0][0]}</text>
                        <text x="12" y="52" font-size="8" font-weight="bold" fill="#0f172a">• {item['diagram_nodes'][0][1]}</text>
                    </g>
                    
                    <line x1="170" y1="97.5" x2="210" y2="97.5" stroke="#d97706" stroke-width="2"/>
                    <polygon points="210,93.5 218,97.5 210,101.5" fill="#d97706"/>

                    <g transform="translate(220, 55)">
                        <rect x="0" y="0" width="140" height="85" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5" rx="6"/>
                        <text x="70" y="25" font-size="10" font-weight="black" fill="#6b21a8" text-anchor="middle">{item['diagram_nodes'][1][0]}</text>
                        <text x="10" y="52" font-size="8" font-weight="bold" fill="#0f172a">• {item['diagram_nodes'][1][1]}</text>
                    </g>

                    <line x1="360" y1="97.5" x2="390" y2="97.5" stroke="#9333ea" stroke-width="2"/>
                    <polygon points="390,93.5 398,97.5 390,101.5" fill="#9333ea"/>

                    <g transform="translate(400, 55)">
                        <rect x="0" y="0" width="125" height="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="6"/>
                        <text x="62.5" y="25" font-size="10" font-weight="black" fill="#15803d" text-anchor="middle">{item['diagram_nodes'][2][0]}</text>
                        <text x="10" y="52" font-size="8" font-weight="bold" fill="#15803d">• {item['diagram_nodes'][2][1]}</text>
                    </g>

                    <rect x="30" y="152" width="490" height="24" fill="#0f172a" rx="4"/>
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS {item['wbs']} {item['title']} 승인 완수</text>
                </svg>
            </div>
        </div>
    </div>
</div>

<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 {item['title']} 2D Visual 도식 확대 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]"></div>
    </div>
</div>

<script>
    function openDiagramZoom(elementId, titleText) {{
        const srcEl = document.getElementById(elementId);
        if (!srcEl) return;
        const zoomBody = document.getElementById('zoomBody');
        document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "{item['title']} 도식 확대 보기");
        zoomBody.innerHTML = srcEl.outerHTML;
        const innerSvg = zoomBody.querySelector('svg');
        if (innerSvg) {{ innerSvg.setAttribute('width', '100%'); innerSvg.setAttribute('height', '520px'); innerSvg.style.maxWidth = '1050px'; }}
        document.getElementById('zoomModal').classList.add('active');
    }}
    function closeZoomModal() {{ document.getElementById('zoomModal').classList.remove('active'); }}
    function closeZoomModalOutside(event) {{ if (event.target.id === 'zoomModal') closeZoomModal(); }}
    window.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeZoomModal(); }});
</script>
</body>
</html>"""

    # 3. 체크리스트 HTML
    tr_items = ""
    for idx, q_text in enumerate(item['chk_items']):
        step_num = (idx // 4) + 1
        step_title = item['steps'][step_num - 1][1]
        
        row_td = ""
        if idx % 4 == 0:
            row_td = f"""<td rowspan="4" class="p-4 align-middle text-center bg-slate-50/50 border-r border-slate-200">
                <span class="bg-amber-600 text-white font-bold text-[10px] px-2 py-0.5 rounded block mb-1">STEP {step_num}</span>
                <span class="font-bold text-slate-900 text-xs">{step_title}</span>
            </td>"""
            
        border_b = "border-b-2 border-slate-300" if (idx % 4 == 3) else ""
        tr_items += f"""<tr class="hover:bg-slate-50/80 {border_b}">
            {row_td}
            <td class="p-3.5 border-r border-slate-200">
                <p class="text-slate-800 font-medium leading-relaxed">{q_text}</p>
            </td>
            <td class="p-3.5 align-middle text-center bg-slate-50/30">
                <label class="inline-flex items-center justify-center gap-1.5 font-bold text-slate-700 cursor-pointer">
                    <input type="checkbox" class="chk-item w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"/> 확인완료
                </label>
            </td>
        </tr>"""

    chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {item['title']} 체크리스트 (WBS {item['wbs']})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    
    <div class="bg-slate-900 text-white p-8 relative">
        <span class="bg-amber-500 text-slate-900 text-xs font-black px-3 py-1 rounded-full uppercase">Dongtan Tram Checklist (WBS {item['wbs']})</span>
        <h1 class="text-3xl font-black mt-2">{item['title']} 체크리스트</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {item['wbs']} | 주관: 현장 공사팀 / 공무팀 | "16개 정밀 검측 문항 1:1 수평대응 서식 (~하였는가? 어미 100% 통일)"</p>
    </div>
    
    <div class="p-6 sm:p-8 space-y-6">
        <div class="bg-amber-50 border-2 border-amber-300 p-5 sm:p-6 rounded-2xl text-xs text-amber-950 space-y-3 shadow-sm">
            <div class="flex items-center justify-between border-b border-amber-200 pb-2.5">
                <h4 class="font-black text-sm text-amber-900 flex items-center gap-2"><span class="text-base">⚠️</span> {item['title']} 체크리스트 점검의 핵심 의미</h4>
                <span class="text-[11px] font-bold bg-red-600 text-white px-2.5 py-0.5 rounded-full">{item['badge']}</span>
            </div>
            <p class="text-slate-800 leading-relaxed font-semibold">{item['objective']}</p>
        </div>

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
                    {tr_items}
                </tbody>
            </table>
        </div>
    </div>
</div>
</body>
</html>"""

    # 파일 작성
    with open(os.path.join(std_dir, f"{file_pfx}_표준서.html"), 'w', encoding='utf-8') as f:
        f.write(std_html)
    with open(os.path.join(gui_dir, f"{file_pfx}_수행지침.html"), 'w', encoding='utf-8') as f:
        f.write(gui_html)
    with open(os.path.join(chk_dir, f"{file_pfx}_체크리스트.html"), 'w', encoding='utf-8') as f:
        f.write(chk_html)

print("Batch 1 (Row 10 ~ Row 15) 6개 액티비티 총 18개 HTML 딥빌드 수정 완료!")
