import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

rows_data = [
    {
        'row': 16,
        'wbs': '9000-7-15',
        'dir_name': '14_품질관리계획 수립 승인',
        'file_prefix': '품질관리계획 수립 승인',
        'title': '품질관리계획 수립 승인',
        'std_legal': '건설기술진흥법 제55조 & KCS 47 10 25 품질 규정',
        'badge': '품질 시험 / KCS 규격',
        'objective': '건설기술 진흥법 제55조에 의거하여 강화노반 품질 시험 빈도(다짐도 500m³당 1회, K30 2,000m²당 1회, Ev2 1,000m²당 1회)가 수록된 품질관리계획서를 수립하고 감리 서면 승인을 완수함에 있다.',
        'rules': [
            ('수칙 1: 품질 시험 빈도 엄수 수칙', '노반 다짐도(≥95%), 평판재하시험 K30(≥110 MN/m³), 변형계수 Ev2(≥60 MPa) 시험 빈도를 100% 준수함.'),
            ('수칙 2: 품질 검사자 자격 수칙', '품질 시험은 건설기술인 자격을 보유한 현장 품질 관리자가 공인 교정 장비로 실시함.')
        ],
        'deliv': '품질관리계획서, 품질 시험 계획서, 교정 성적서 및 감리 최종 승인 공문',
        'steps': [
            ('STEP 01', '품질 시험 계획 & 빈도 수립', '다짐도(500m³), K30(2,000m²), Ev2(1,000m²) 공학적 시험 빈도를 설정함.'),
            ('STEP 02', '품질 시험 장비 공인 교정', '평판재하시험기, 밀도 측정기(KS F 2311) 공인 기관 교정성적서를 확보함.'),
            ('STEP 03', '착공 14일 전 감리 제출', '품질관리계획서를 제출하여 분야별 품질 감리원의 기술 심사를 수검함.'),
            ('STEP 04', '품질 승인 공문 수령', '보완 조치 결과서를 재제출하여 책임감리원 최종 적정 서면 승인을 완수함.')
        ],
        'diagram_title': '📊 동탄트램 강화노반 품질관리계획 수립 및 승인 절차도',
        'diagram_nodes': [('1. 품질 계획 작성', '시험 빈도/수치 명시'), ('2. 시험 장비 교정', '공인 성적서 확보'), ('3. 감리 서면승인', '품질 승인 공문 수령')],
        'chk_items': [
            '1. 건설기술 진흥법 제55조에 따른 품질관리계획서 본안을 작성하였는가?',
            '2. 강화노반 다짐도(≥95%, 500m³당 1회 이상) 시험 계획을 명시하였는가?',
            '3. 평판재하시험 K30(≥110 MN/m³, 2,000m²당 1회) 시험 빈도를 수록하였는가?',
            '4. 동적 평판재하시험 Ev2(≥60 MPa, Ev2/Ev1≤2.2) 기준을 포함하였는가?',
            '5. 현장 밀도 측정기(KS F 2311 들밀도 시험기) 교정성적서를 확인하였는가?',
            '6. 현장 품질관리자 선임계 및 자격 수첩을 1:1 대조하였는가?',
            '7. 품질 시험실 규모 및 시험 장비 비치 상태를 검측하였는가?',
            '8. 골재 체가름 및 마모율 시험 대장 관리 체계를 수립하였는가?',
            '9. 강우 및 동절기 품질 관리 대책을 계획서에 포함하였는가?',
            '10. 불합격 노반 구역 재다짐 및 재시험 절차를 명시하였는가?',
            '11. 품질 대시보드 및 총괄 대장 전산화 관리 체계를 구축하였는가?',
            '12. 공사 착수 14일 전 책임감리단에 계획서를 공식 제출하였는가?',
            '13. 감리원 지적 요구 사항에 대한 보완 조치표를 작성하였는가?',
            '14. 품질관리비 집행 계획서 및 영수증 철을 비치하였는가?',
            '15. 책임감리원 직인이 날인된 품질관리계획 서면 승인 공문을 수령하였는가?',
            '16. 승인된 품질 계획서를 현장 품질실에 게시 보관하고 있는가?'
        ]
    },
    {
        'row': 17,
        'wbs': '9000-7-16',
        'dir_name': '15_환경관리계획 수립 승인',
        'file_prefix': '환경관리계획 수립 승인',
        'title': '환경관리계획 수립 승인',
        'std_legal': '대기환경보전법 & 환경영향평가법 환경 기준',
        'badge': '비산먼지 / 소음저감',
        'objective': '상부강화노반 토공 굴착 및 골재 운반 시 발생되는 비산먼지, 소음·진동(65dB 이하) 및 토사 유출을 방지하기 위하여 이동식 세륜기, 방음벽(H=3m), 침사지를 설치하고 관할 시청 및 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 비산먼지 발생사업 신고 수칙', '공사 착수 전 지자체(화성시) 비산먼지 발생사업 신고 수속 및 방진 덮개를 비치함.'),
            ('수칙 2: 작업 소음 65dB 통제 수칙', '장비 가동 소음은 65dB 이하를 유지하도록 가설 방음벽을 설치하고 소음 계측을 시행함.')
        ],
        'deliv': '환경관리계획서, 비산먼지 신고 필증, 소음/진동 계측 대장 및 감리 승인서',
        'steps': [
            ('STEP 01', '비산먼지 & 소음 저감 시설 설계', '이동식 세륜기, 가설 방음벽(3m) 및 토사 방진 덮개를 설계함.'),
            ('STEP 02', '지자체 환경 신고 수속', '화성시청 비산먼지 발생사업 신고서 및 특정공사 사전신고서를 접수함.'),
            ('STEP 03', '현장 환경 시설 가동 점검', '세륜기 수조(깊이 1.2m) 가동 및 살수차 2대 상시 운영 상태를 점검함.'),
            ('STEP 04', '환경 관리 계획서 감리 승인', '환경 계획서 및 신고 필증 사본을 감리단에 제출하여 서면 결재를 완료함.')
        ],
        'diagram_title': '🌿 동탄트램 환경관리계획 수립 및 비산먼지 저감 절차도',
        'diagram_nodes': [('1. 환경시설 설계', '세륜기/방음벽 3m'), ('2. 지자체 신고', '비산먼지 신고 필증'), ('3. 감리 서면승인', '환경계획서 결재')],
        'chk_items': [
            '1. 대기환경보전법에 따른 비산먼지 발생사업 신고 필증을 수령하였는가?',
            '2. 특정공사 사전신고서(소음·진동관리법) 접수 완료 여부를 확인하였는가?',
            '3. 현장 출입구 이동식 자동 세륜 세차 시설(깊이 1.2m)을 설치하였는가?',
            '4. 공사 경계 가설 방음 방진 펜스(높이 3m 이상)를 시공하였는가?',
            '5. 토사 수송 덤프트럭 덮개 100% 체결 상태를 점검하였는가?',
            '6. 현장 내 살수차(8,000L 이상) 2대 이상을 상시 가동하고 있는가?',
            '7. 토사 야적장 방진망(차광률 80% 이상) 덮개를 부설하였는가?',
            '8. 작업장 소음 계측(기준 65dB 이하)을 주간 단위 시행하고 있는가?',
            '9. 중장비 진동 계측(기준 75dB 이하) 대장을 비치하고 있는가?',
            '10. 토사 유출 방지 오탁방지망 및 침사지 2개소를 가동하였는가?',
            '11. 건설 폐기물 분리 수거 야적장 및 관리 표지판을 설치하였는가?',
            '12. 환경 전담 관리자를 선임하고 일일 환경 점검표를 작성하였는가?',
            '13. 주거 밀집 지역 인접 작업 시 주민 사전 안내문 배포를 시행하였는가?',
            '14. 세륜 슬러지 정기 수거 및 위탁 처리 계약서를 확보하였는가?',
            '15. 책임감리원 입회하에 환경관리계획 서면 승인을 결재받았는가?',
            '16. 승인된 환경 대장을 현장 공무 파일에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 18,
        'wbs': '9000-7-17',
        'dir_name': '16_교통소통 대책 수립 승인(필요시)',
        'file_prefix': '교통소통 대책 수립 승인(필요시)',
        'title': '교통소통 대책 수립 승인(필요시)',
        'std_legal': '도로교통법 제69조 & 도로점용 허가 규정',
        'badge': '교통 안전 / 점용 허가',
        'objective': '상부강화노반 시공 중 기존 도로 점용 및 토사 운반 차량 출입 시 발생되는 교통 혼잡을 방지하기 위하여 동탄경찰서 교통 소통 협의, 안전 신호수 2인 배치 및 야간 경광등 조치를 완수함에 있다.',
        'rules': [
            ('수칙 1: 관할 경찰서 교통 협의 수칙', '도로 점용 및 차선 통제 발생 시 동탄경찰서 교통안전 심의를 통과하고 허가증을 수령함.'),
            ('수칙 2: 안전 신호수 배치 수칙', '차량 진출입로 2개소에 야간 경광봉 및 붉은색 깃발을 지닌 전담 신호수를 상주 배치함.')
        ],
        'deliv': '교통소통 대책서, 도로점용 허가증, 경찰서 협의 공문 및 감리 승인서',
        'steps': [
            ('STEP 01', '교통 우회 & 차선 점용 설계', '덤프 수송 진출입 램프, 우회 차선 및 안전 바리케이트를 설계함.'),
            ('STEP 02', '동탄경찰서 & 지자체 심의', '교통소통 대책서를 제출하여 관할 경찰서 안전 심의 통과를 완수함.'),
            ('STEP 03', '안전 시설물 현장 설치', 'LED 둔덕 경광등, 야간 유도 표지판 및 신호수 2인 2조를 배치함.'),
            ('STEP 04', '교통 대책서 감리 최종 승인', '경찰서 허가 공문 사본을 제출하여 책임감리원 최종 승인을 수검함.')
        ],
        'diagram_title': '🚦 동탄트램 교통소통 대책 수립 및 차선 통제 절차도',
        'diagram_nodes': [('1. 교통우회 설계', '우회 차선/바리케이트'), ('2. 경찰서 심의', '동탄경찰서 허가증'), ('3. 감리 서면승인', '교통대책서 결재')],
        'chk_items': [
            '1. 도로교통법에 따른 도로점용 허가증을 확보하였는가?',
            '2. 동탄경찰서 관할 교통안전 심의 통과 공문을 수령하였는가?',
            '3. 현장 진출입로 차량 가시거리(100m 이상)를 확보하였는가?',
            '4. 차량 진출입구 전담 안전 신호수 2인 이상을 상주 배치하였는가?',
            '5. 야간 유도등, LED 둔덕 경광등 및 안전 바리케이트를 설치하였는가?',
            '6. 덤프트럭 서행 유도 표지판(속도 20km/h 제한)을 게시하였는가?',
            '7. 우회 도로 표지판 및 차선 변경 안내간판을 시공하였는가?',
            '8. 보행자 전용 가설 인도 및 안전 펜스를 확보하였는가?',
            '9. 교통 혼잡 시간대(출퇴근 07~09시, 17~19시) 덤프 운행 제한을 조치하였는가?',
            '10. 신호수 대상 안전 경광봉, 호루라기 및 반사 조끼를 지급하였는가?',
            '11. 도로 노면 청소차를 매일 가동하여 토사 낙하를 청소하고 있는가?',
            '12. 비상 시 관할 경찰서 및 도로관리청 비상 연락망을 비치하였는가?',
            '13. 임시 교통 통제 시 일일 교통 일지를 작성 관리하고 있는가?',
            '14. 덤프 조종원 대상 정차 위치 및 안전 주행 교육을 실시하였는가?',
            '15. 책임감리원 입회하에 교통소통 대책 서면 승인을 결재받았는가?',
            '16. 승인된 교통 도서를 현장 공무 대장에 철하여 보관하고 있는가?'
        ]
    },
    {
        'row': 19,
        'wbs': '9000-7-18',
        'dir_name': '17_하도급 검토 승인',
        'file_prefix': '하도급 검토 승인',
        'title': '하도급 검토 승인',
        'std_legal': '건설산업기본법 제29조 & 공공공사 하도급 적정성 심사',
        'badge': '하도급 적정 / 건진법',
        'objective': '건설산업기본법 제29조에 의거하여 상부강화노반 전문 토공 하도급 업체의 적격성(면허, 시공능력평가, 하도급율 ≥82%)을 심사하고, 노무비 전용계좌 지정 및 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 전문건설업 면허 준수 수칙', '하도급 업체는 전문건설업(토공사업) 정식 면허 및 시공 실적을 보유한 업체이어야 함.'),
            ('수칙 2: 노무비 전용계좌 지정 수칙', '하도급 대금 지불 보증서 발급 및 체불 방지를 위한 노무비 전용계좌 지정서를 제출함.')
        ],
        'deliv': '하도급 통지서, 적정성 심사표, 대급지불 보증서 및 감리 최종 승인 공문',
        'steps': [
            ('STEP 01', '하도급 업체 면허 & 실적 검증', '토공 전문 면허증, 국세/지방세 완납 증명서 및 시공 실적을 대조함.'),
            ('STEP 02', '하도급 적정성 심사표 작성', '하도급율(82% 이상) 및 기술자 보유 현황 적정성 심사 점수를 도출함.'),
            ('STEP 03', '노무비 전용계좌 & 보증서 수령', '하도급 대금 지급 보증서 및 노무비 전용계좌 개설 확인서를 부착함.'),
            ('STEP 04', '하도급 검토서 감리 최종 승인', '하도급 검토 보고서를 작성하여 책임감리원 서면 결재를 수검함.')
        ],
        'diagram_title': '📑 동탄트램 하도급 검토 및 적정성 승인 절차도',
        'diagram_nodes': [('1. 면허/실적 검증', '토공 전문면허 대조'), ('2. 적정성 심사', '하도급율 82%+ 확보'), ('3. 감리 서면승인', '하도급 승인 공문 수령')],
        'chk_items': [
            '1. 건설산업기본법에 따른 하도급 통지서 본안을 구비하였는가?',
            '2. 하도급 업체의 전문건설업(토공사업) 정식 면허를 확인하였는가?',
            '3. 하도급계약 금액의 적정성 평가 점수(85점 이상)를 도출하였는가?',
            '4. 하도급율(원도급 대비 82% 이상) 기준을 준수하였는가?',
            '5. 하도급 대금 지급 보증서 발급 원본을 확인하였는가?',
            '6. 근로자 임금 체불 예방을 위한 노무비 전용계좌 지정을 완료하였는가?',
            '7. 하도급 업체 기술자(토공 전문기술인 2인 이상) 배치표를 점검하였는가?',
            '8. 하도급 업체의 국세 및 지방세 완납 증명서를 확인하였는가?',
            '9. 재하도급 일체 금지 확약서를 제출받았는가?',
            '10. 하도급 업체 건설기계 대여대금 지급 보증서 수속을 확인하였는가?',
            '11. 하도급 계약서 내 공정 거래 표준 계약서 서식을 적용하였는가?',
            '12. 하도급 업체의 안전보건 수준 평가(A등급 이상)를 시행하였는가?',
            '13. 발주처 공공공사 하도급 관리 전산망에 계약 데이터를 등록하였는가?',
            '14. 책임감리단에 하도급 검토 보고서를 공식 접수하였는가?',
            '15. 책임감리원 직인이 날인된 하도급 최종 승인 공문을 받았는가?',
            '16. 승인된 하도급 도서를 현장 공무 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 20,
        'wbs': '9000-7-19',
        'dir_name': '18_자재승인',
        'file_prefix': '자재승인',
        'title': '자재승인',
        'std_legal': '건설기술진흥법 시행규칙 제42조 & KCS 47 10 25 자재 규정',
        'badge': '공급원 승인 / 자재 검수',
        'objective': '상부강화노반에 투입되는 쇄석 혼합 골재, HDPE 유공관(Ø200mm) 및 투수성 부직포(200g/m²)의 품질(KS F 2527)을 검증하여 공급원 승인 및 현장 반입 감리 결재를 완수함에 있다.',
        'rules': [
            ('수칙 1: KS 표시 인증 자재 수칙', '모든 노반 주요 자재는 KS 표시 인증 자재 또는 공인 시험 성적서를 부착하여 승인받음.'),
            ('수칙 2: 현장 반입 자재 전수 검수 수칙', '반입 자재는 품질관리자 및 감리원 입회하에 봉인 상태 및 수량을 전수 검수함.')
        ],
        'deliv': '자재 공급원 승인 신청서, 공인 시험 성적서, KS 인증서 및 감리 승인 공문',
        'steps': [
            ('STEP 01', '자재 공급원 서류 사전 검토', '제조사 사업자등록증, KS 인증서, 공장 등록증 및 품질 성적서를 확인함.'),
            ('STEP 02', '공인 시험 기관 시험 의뢰', '쇄석 골재 마모율, CBR 및 유공관 강도 공인 기관 시험을 의뢰함.'),
            ('STEP 03', '자재 승인 신청서 감리 제출', '자재 공급원 승인 신청서 본안을 작성하여 책임감리단에 제출함.'),
            ('STEP 04', '현장 반입 자재 검수 & 결재', '감리 서면 승인 수령 후 현장 반입 자재 검수표 작성 및 최종 승인을 완료함.')
        ],
        'diagram_title': '📦 동탄트램 강화노반 투입 자재 공급원 승인 절차도',
        'diagram_nodes': [('1. 자재 서류 검토', 'KS 인증/성적서 확인'), ('2. 공인기관 시험', '마모율/CBR 시험'), ('3. 감리 서면승인', '자재 승인 공문 수령')],
        'chk_items': [
            '1. 강화노반 쇄석 혼합 골재 공급원 승인 신청서를 작성하였는가?',
            '2. 골재 제조사의 KS F 2527 인증서 및 공장 등록증을 확인하였는가?',
            '3. HDPE 배수 유공관(Ø200mm) 외압 강도 시험성적서를 확인하였는가?',
            '4. 투수성 부직포(200g/m²) 인장 강도 및 투수 계수 성적서를 검측하였는가?',
            '5. 자재 공인 시험 성적서 발급일이 6개월 이내의 유효한 것인가?',
            '6. 자재 샘플을 현장에서 봉인 채취하여 공인 기관에 시험 의뢰하였는가?',
            '7. 골재 석산의 잔여 매장량 및 일일 생산 공급 능력을 확인하였는가?',
            '8. 자재 운반 차량 운반선 및 비산먼지 방지 덮개를 점검하였는가?',
            '9. 현장 자재 야적장의 평탄성 및 빗물 차단 비닐 부설을 점검하였는가?',
            '10. 유공관 자재 충격 파손 여부를 반입 현장에서 전수 검측하였는가?',
            '11. 불합격 자재 발생 시 현장 반출 전용 구역을 구별 지정하였는가?',
            '12. 자재 수불 대장 및 일일 반입 물량을 정밀 수록 관리하고 있는가?',
            '13. 자재 제조사 품질 보증서 및 서약서를 접수하였는가?',
            '14. 책임감리단에 자재 공급원 승인 신청서를 공식 제출하였는가?',
            '15. 책임감리원 직인이 날인된 자재 최종 승인 공문을 받았는가?',
            '16. 승인된 자재 목록을 현장 품질실 전면에 게시 보관하고 있는가?'
        ]
    },
    {
        'row': 21,
        'wbs': '9000-7-20',
        'dir_name': '19_시험다짐',
        'file_prefix': '시험다짐',
        'title': '시험다짐',
        'std_legal': 'KCS 47 10 25 강화노반 시험다짐 규정',
        'badge': '시험 다짐 / 다짐 횟수',
        'objective': 'KCS 47 10 25에 의거하여 본시공 착수 전 50m 시험 구간에서 10톤 이상 강동 롤러 최적 다짐 횟수(4~6회) 및 층두께(30cm)를 결정하고 평판재하시험(K30 ≥110 MN/m³)을 완수함에 있다.',
        'rules': [
            ('수칙 1: 50m 시험 구간 설정 수칙', '본시공 노반과 동일한 조건의 50m 구간을 지정하고 층두께 30cm 포설 시험 다짐을 시행함.'),
            ('수칙 2: 최적 다짐 횟수 산출 수칙', '롤러 통과 횟수별(2회, 4회, 6회, 8회) 침하량(Δh ≤ 1mm) 및 K30 밀도를 측정하여 적정 횟수를 산정함.')
        ],
        'deliv': '시험다짐 계획서, 롤러 다짐 회수별 침하 성과표, K30 평판재하 성적서 및 감리 승인서',
        'steps': [
            ('STEP 01', '50m 시험다짐 구간 선정', '강화노반 본선 부지 중 50m 시험 구간을 지정하고 측량 레벨 기준점을 설치함.'),
            ('STEP 02', '장비 조합 & 층두께 30cm 포설', '모터그레이더로 쇄석을 30cm 두께로 평탄 부설하고 강동 롤러 10t을 반입함.'),
            ('STEP 03', '다짐 횟수별 침하량 & K30 측정', '2회, 4회, 6회 다짐 롤링 시 침하량 변위 및 평판재하시험(K30) 3개소를 측정함.'),
            ('STEP 04', '시험다짐 결과 보고서 감리 승인', '다짐 횟수(예: 강동 4회 + 타이어 2회) 확정 보고서를 승인 결재받음.')
        ],
        'diagram_title': '🚜 동탄트램 50m 시험다짐 및 최적 다짐 횟수 결정 절차도',
        'diagram_nodes': [('1. 50m 시험구간 지정', '30cm 쇄석 평탄포설'), ('2. 다짐/K30 측정', '2회/4회/6회 침하측정'), ('3. 감리 서면승인', '다짐횟수 확정결재')],
        'chk_items': [
            '1. 본시공과 동일한 조건의 50m 시험다짐 구간을 선정하였는가?',
            '2. 시험다짐용 강동 진동 롤러(10ton 이상) 장비를 반입하였는가?',
            '3. 모터그레이더로 골재 포설 두께(30cm)를 정밀 조정하였는가?',
            '4. 포설 골재의 현장 최적함수비(OMC ± 2%) 범주를 확인하였는가?',
            '5. 광학 레벨기로 다짐 전 표고 레벨 기준점을 현측하였는가?',
            '6. 롤러 2회 통과 후 침하 변위량(mm)을 측량 기록하였는가?',
            '7. 롤러 4회 통과 후 침하 변위량(mm)을 측량 기록하였는가?',
            '8. 롤러 6회 통과 후 침하 변위량(Δh ≤ 1mm 수렴)을 확인하였는가?',
            '9. 시험 구간 내 평판재하시험(KS F 2310, 3개소 이상)을 시행하였는가?',
            '10. 평판재하시험 지반반발자승 K30 값이 110 MN/m³ 이상임을 확인하였는가?',
            '11. 동적 평판재하시험 Ev2 값이 60 MPa 이상임을 실측 검증하였는가?',
            '12. 현장 들밀도 시험(KS F 2311) 다짐도가 95% 이상임을 확인하였는가?',
            '13. 시험다짐 결과 도출된 최적 다짐 횟수(예: 4~6회)를 규정하였는가?',
            '14. 시험다짐 전 과정에 대해 책임감리원 입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 시험다짐 결과 보고서 승인을 받았는가?',
            '16. 승인된 시험다짐 성과표를 본시공 다짐 지침으로 시공팀에 전달하였는가?'
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

print("Batch 2 (Row 16 ~ Row 21) 6개 액티비티 총 18개 HTML 딥빌드 완성!")
