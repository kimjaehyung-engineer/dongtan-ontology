import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

rows_data = [
    {
        'row': 22,
        'wbs': '9000-7-21',
        'dir_name': '20_원지반 검측',
        'file_prefix': '원지반 검측',
        'title': '원지반 검측',
        'std_legal': 'KCS 47 10 25 원지반 지비력 및 표고 규정',
        'badge': '원지반 / 표고 검측',
        'objective': '상부강화노반 시공 전 표토(유기질토 15~30cm) 제거 상태, 원지반 평탄 표고(오차 ±30mm) 및 지반반발자승 K30(≥70 MN/m³) 지지력을 현장 검측하여 부적합을 사전에 100% 차단함에 있다.',
        'rules': [
            ('수칙 1: 표토 제거 및 정전압 다짐 수칙', '원지반 표토 유기질토는 전량 굴착 반출하고 전압 롤러 2회 이상 정전압 다짐을 시행함.'),
            ('수칙 2: 펌핑(Pumping) 연요 현상 검측 수칙', '중장비 주행 시 지반 펌핑 및 연약 구간 발생 여부를 시각 및 덤프 대하 시험으로 확인함.')
        ],
        'deliv': '원지반 검측 요청서, K30 평판재하 성적서, 원지반 레벨 측량 야장 및 감리 승인서',
        'steps': [
            ('STEP 01', '표토 제거 & 원지반 정전압 다짐', '유기질토(15~30cm) 제거 후 롤러 2회 정전압 사전 다짐을 시행함.'),
            ('STEP 02', '원지반 표고 & 종횡단 측량', '광학 토탈스테이션으로 원지반 중심선 레벨(오차 ±30mm)을 측량함.'),
            ('STEP 03', 'K30 평판재하시험 & 펌핑 점검', '원지반 K30(≥70 MN/m³) 시험 3개소 및 덤프트럭 펌핑 연약 지반을 검측함.'),
            ('STEP 04', '원지반 검측 성과표 감리 승인', '검측 요청서를 제출하여 책임감리원 공학적 입회 결재를 수검함.')
        ],
        'diagram_title': '📐 동탄트램 원지반 지비력 및 표고 검측 절차도',
        'diagram_nodes': [('1. 표토제거/다짐', '유기질토 15~30cm 제거'), ('2. 표고/K30 검측', 'K30 ≥70 MN/m³ 시험'), ('3. 감리 서면승인', '원지반 검측서 결재')],
        'chk_items': [
            '1. 원지반 표토(유기질토 15~30cm) 제거 상태를 확인하였는가?',
            '2. 원지반 수목 뿌리 및 유기물 쓰레기 완전 제거 여부를 점검하였는가?',
            '3. 원지반 전압 롤러 2회 이상 정전압 다짐을 시행하였는가?',
            '4. 원지반 중심선 표고 레벨 오차가 ±30mm 이내임을 측량하였는가?',
            '5. 원지반 횡단 횡단 배수 경사(2% 이상)가 형성되었는가?',
            '6. 원지반 지반반발자승 K30(≥70 MN/m³) 평판재하시험을 실시하였는가?',
            '7. 덤프트럭 주행 시 원지반 펌핑(Pumping) 연요 현상이 없음을 검측하였는가?',
            '8. 연약 지반 발굴 시 치환 토사(CBR ≥10%) 치환 깊이를 확인하였는가?',
            '9. 원지반 암노출 구역 암종 분류 및 굴착 경계선을 검토하였는가?',
            '10. 원지반 지하수 용출 구간 지상 가배수로 연결 상태를 확인하였는가?',
            '11. 원지반 측량 야장 및 사진을 공무 대장에 철하였는가?',
            '12. 광학 토탈스테이션 기준점(CP) 대조 레벨 오차를 확인하였는가?',
            '13. 원지반 검측 요청서를 공사 착수 24시간 전 제출하였는가?',
            '14. 현장 책임감리원 1:1 입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 원지반 검측 승인서를 수령하였는가?',
            '16. 승인된 원지반 성과를 하부노반 시공팀에 공식 인계하였는가?'
        ]
    },
    {
        'row': 23,
        'wbs': '9000-7-22',
        'dir_name': '21_하부노반 검측',
        'file_prefix': '하부노반 검측',
        'title': '하부노반 검측',
        'std_legal': 'KCS 47 10 25 하부노반 다짐 및 밀도 규정',
        'badge': '하부노반 / 층다짐',
        'objective': '하부노반 시공 시 층두께 30cm 이하 다짐, 다짐도 ≥90%(500m³당 1회), K30 ≥90 MN/m³ 및 표고 오차 ±20mm 이내 품질을 실측 검측하여 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 층두께 30cm 층다짐 준수 수칙', '하부노반 토사 포설 두께는 다짐 후 30cm 이하이어야 하며 모터그레이더로 평탄 작업함.'),
            ('수칙 2: 다짐도 90% & K30 90 수칙', '들밀도 시험(KS F 2311) 다짐도 90% 이상 및 평판재하시험 K30 ≥ 90 MN/m³를 검증함.')
        ],
        'deliv': '하부노반 검측 요청서, 들밀도 성적서(KS F 2311), K30 성적서 및 감리 승인서',
        'steps': [
            ('STEP 01', '하부노반 30cm 층포설 & 다짐', '성토 토사를 30cm 두께로 포설하고 10톤 강동 롤러 4회 이상 다짐을 시행함.'),
            ('STEP 02', '들밀도 & K30 평판재하시험', 'KS F 2311 들밀도 시험(다짐도 ≥90%) 및 K30(≥90 MN/m³) 3개소를 검측함.'),
            ('STEP 03', '하부노반 마무리면 레벨 측량', '광학 레벨기로 하부노반 마무리면 표고 오차(±20mm 이내)를 검측함.'),
            ('STEP 04', '하부노반 검측 서면 승인 수령', '검측 결과표를 작성하여 책임감리원 서면 결재를 완료함.')
        ],
        'diagram_title': '🚜 동탄트램 하부노반 층다짐 및 밀도 검측 절차도',
        'diagram_nodes': [('1. 30cm 층포설/다짐', '강동 롤러 4회 다짐'), ('2. 들밀도/K30 검측', '다짐도 90%/K30 90'), ('3. 감리 서면승인', '하부노반 검측서 결재')],
        'chk_items': [
            '1. 하부노반 다짐 후 층두께가 30cm 이하임을 확인하였는가?',
            '2. 성토 토사 최대입경이 100mm 이하임을 체가름 검측하였는가?',
            '3. 현장 들밀도 시험(KS F 2311) 다짐도가 90% 이상임을 실측하였는가?',
            '4. 지반반발자승 K30 값이 90 MN/m³ 이상임을 시험 성적서로 검증하였는가?',
            '5. 동적 변형계수 Ev2 값이 45 MPa 이상(Ev2/Ev1≤2.5)임을 확인하였는가?',
            '6. 하부노반 마무리면 표고 레벨 오차가 ±20mm 이내임을 측량하였는가?',
            '7. 하부노반 횡단 경사(2% 이상)가 완벽히 형성되었는가?',
            '8. 다짐 작업 시 토사 최적함수비(OMC ± 2%) 관리를 시행하였는가?',
            '9. 불합격 구간 다짐 롤러 재가동 및 재검측을 100% 이행하였는가?',
            '10. 하부노반 사면 경사(1:1.5 내외) 및 다짐 롤러 사면 인력다짐을 검측하였는가?',
            '11. 다짐도 시험 위치를 500m³당 1회 이상 무작위 선정하였는가?',
            '12. 하부노반 측량 야장 및 평판재하 사진을 공무 대장에 철하였는가?',
            '13. 하부노반 검측 요청서를 시공 24시간 전 책임감리단에 제출하였는가?',
            '14. 책임감리원 1:1 현장 입회하에 결재 수검을 진행하였는가?',
            '15. 책임감리원 직인이 날인된 하부노반 검측 승인서를 수령하였는가?',
            '16. 승인된 하부노반 성과를 상부노반 시공팀에 공식 인계하였는가?'
        ]
    },
    {
        'row': 24,
        'wbs': '9000-7-23',
        'dir_name': '22_상부노반 시공(배수 유공관 포함)',
        'file_prefix': '상부노반 시공(배수 유공관 포함)',
        'title': '상부노반 시공(배수 유공관 포함)',
        'std_legal': 'KCS 47 10 25 상부노반 및 맹암거 유공관 규정',
        'badge': '상부노반 / 맹암거 배수',
        'objective': '상부노반 층두께 30cm 시공 및 맹암거 HDPE 유공관(Ø200mm, 투수성 부직포 200g/m²)을 종단 구배 0.5% 이상으로 부설하여 노반 내부 침투수를 완벽히 배수함에 있다.',
        'rules': [
            ('수칙 1: HDPE 유공관 천공 상향 수칙', '유공관 구멍 천공 부위는 상향 45도 방향으로 배치하고 부직포로 2중 감싸기 시공함.'),
            ('수칙 2: 맹암거 유공관 파손 방지 수칙', '유공관 주위 쇄석(19~25mm) 포설 구간은 롤러 직접 주행을 금지하고 소형 램머 다짐함.')
        ],
        'deliv': '상부노반 시공일지, 유공관 자재 검수표, 맹암거 부설 사진 및 감리 승인서',
        'steps': [
            ('STEP 01', '상부노반 토사 30cm 포설', '모터그레이더로 토사를 30cm 두께로 포설하고 평탄 롤링 다짐을 시행함.'),
            ('STEP 02', '맹암거 터파기 & 부직포 부설', '맹암거 트렌치 터파기 후 투수성 부직포(200g/m²)를 트렌치 바닥에 깔아 챔버 형성함.'),
            ('STEP 03', 'HDPE 유공관(Ø200mm) 부설', '종단 구배 0.5% 이상으로 유공관을 연결 부설하고 필터 쇄석(19~25mm)을 채움.'),
            ('STEP 04', '상부노반 배수 시공 감리 승인', '맹암거 유공관 및 상부노반 성과표를 작성하여 책임감리원 결재를 완수함.')
        ],
        'diagram_title': '🛠️ 동탄트램 상부노반 및 맹암거 유공관 배수 시공 절차도',
        'diagram_nodes': [('1. 30cm 토사포설', '상부노반 층포설'), ('2. 맹암거 유공관부설', 'HDPE Ø200mm/부직포'), ('3. 감리 서면승인', '상부노반 시공 결재')],
        'chk_items': [
            '1. 상부노반 토사 층두께가 30cm 이하임을 확인하였는가?',
            '2. 맹암거 트렌치 터파기 폭(0.6m) 및 깊이(0.8m) 도면 준수 여부를 검측하였는가?',
            '3. 투수성 부직포(200g/m² 이상) 겹침 이음 길이(30cm 이상)를 확보하였는가?',
            '4. HDPE 유공관(Ø200mm) 천공 부위 상향 배치 상태를 확인하였는가?',
            '5. 맹암거 유공관 종단 배수 구배가 0.5% 이상임을 광학 레벨로 측량하였는가?',
            '6. 유공관 주위 투수성 필터 쇄석(19~25mm) 포설 높이를 검측하였는가?',
            '7. 유공관 상부 다짐 시 강동 롤러 직접 충격 금지 및 소형 램머 다짐을 시행하였는가?',
            '8. 맹암거 집수정 연결 부위 틈새 모형 시멘트 모타르 사춤을 하였는가?',
            '9. 상부노반 다짐도(≥95%) 들밀도 시험(KS F 2311)을 실시하였는가?',
            '10. 상부노반 K30 평판재하시험(≥110 MN/m³) 성적을 검증하였는가?',
            '11. 상부노반 횡단 구배(2% 이상) 형성을 확인하였는가?',
            '12. 유공관 내 이물질 및 토사 유입 방지 마개 체결을 점검하였는가?',
            '13. 우천 시 맹암거 가설 배수 통로 가동 여부를 확인하였는가?',
            '14. 맹암거 시공 매몰 전 시공 사진을 촬영 철하였는가?',
            '15. 책임감리원 입회하에 상부노반 및 맹암거 매몰 검측 결재를 수검하였는가?',
            '16. 승인된 상부노반 성과를 강화노반 시공팀에 공식 인계하였는가?'
        ]
    },
    {
        'row': 25,
        'wbs': '9000-7-24',
        'dir_name': '23_상부강화노반 시공',
        'file_prefix': '상부강화노반 시공',
        'title': '상부강화노반 시공',
        'std_legal': 'KCS 47 10 25 강화노반 쇄석 시방 규정',
        'badge': '강화노반 / 쇄석 포설',
        'objective': 'KCS 47 10 25에 의거하여 최대입경 50mm 이하 쇄석 혼합 골재를 3D GPS 모터그레이더로 포설하고, 강동 롤러 4~6회 및 타이어 롤러 마감 다짐으로 표고 오차 ±10mm 이내 강화노반을 완수함에 있다.',
        'rules': [
            ('수칙 1: 3D GPS 포설 & 살수 수칙', '쇄석 골재 포설 시 3D GPS 제어 모터그레이더를 활용하고 최적함수비(OMC ±2%) 살수를 시행함.'),
            ('수칙 2: 롤러 조합 다짐 수칙', '강동 진동 롤러(10t+) 4회 이상 및 타이어 롤러(15t+) 2회 마감 다짐으로 고밀도 강화노반을 구축함.')
        ],
        'deliv': '상부강화노반 시공일지, 쇄석 골재 입도 성적서, 살수 다짐 성과표 및 감리 승인서',
        'steps': [
            ('STEP 01', '3D GPS 모터그레이더 쇄석 포설', '최대입경 50mm 쇄석 골재를 30cm 두께로 3D GPS 자동 제어 포설함.'),
            ('STEP 02', '살수차 최적함수비(OMC) 분무 살수', '골재 재료 분리 방지 및 다짐 효율 증대를 위한 OMC 살수를 시행함.'),
            ('STEP 03', '강동 롤러 & 타이어 롤러 조합 다짐', '시험다짐에서 확정된 롤러 조합(강동 4회 + 타이어 2회) 다짐을 정밀 이행함.'),
            ('STEP 04', '강화노반 마무리면 측량 & 감리 승인', '표고 오차 ±10mm 이내 검측 성과표를 작성하여 책임감리원 승인을 결재받음.')
        ],
        'diagram_title': '🚜 동탄트램 상부강화노반 쇄석 포설 및 롤러 다짐 절차도',
        'diagram_nodes': [('1. 3D GPS 쇄석포설', '50mm 쇄석 30cm 포설'), ('2. OMC 살수/롤러다짐', '강동4회+타이어2회 다짐'), ('3. 감리 서면승인', '강화노반 시공 결재')],
        'chk_items': [
            '1. 강화노반 골재(최대입경 50mm 이하) 승인 입도 자재 반입을 확인하였는가?',
            '2. 3D GPS 자동 제어 모터그레이더로 포설 두께(30cm)를 정밀 조정하였는가?',
            '3. 쇄석 골재 포설 시 재료 분리(Segregation) 발생 유무를 검측하였는가?',
            '4. 골재 최적함수비(OMC ± 2%) 유지를 위한 살수차 분무 살수를 시행하였는가?',
            '5. 10톤 이상 강동 진동 롤러 다짐 속도(3~5km/h)를 준수하였는가?',
            '6. 강동 롤러 4회 이상 전압 다짐을 정밀 이행하였는가?',
            '7. 표면 마감용 타이어 롤러(15~25톤) 2회 이상 다짐을 시행하였는가?',
            '8. 강화노반 마무리면 표고 레벨 오차가 ±10mm 이내임을 측량하였는가?',
            '9. 강화노반 횡단 구배(2% 이상) 형성을 광학 레벨로 확인하였는가?',
            '10. 노반 단부 및 배수 구조물 인접 구역 소형 램머 다짐을 시행하였는가?',
            '11. 강화노반 표면 유연 입자 및 유기물 흙 덮임 상태가 없음을 검측하였는가?',
            '12. 다짐 작업 중 지하시설물 매설 위치 2m 이내 진동 감쇄 다짐을 조치하였는가?',
            '13. 우천 대비 강화노반 표면 비닐 덮개 비치 상태를 점검하였는가?',
            '14. 강화노반 시공 일지 및 전·후 시공 사진을 철하였는가?',
            '15. 책임감리원 1:1 입회 검측을 시행하고 시공 승인을 수검하였는가?',
            '16. 승인된 강화노반 성과를 다짐 검측 팀에 공식 인계하였는가?'
        ]
    },
    {
        'row': 26,
        'wbs': '9000-7-25',
        'dir_name': '24_다짐 검측',
        'file_prefix': '다짐 검측',
        'title': '다짐 검측',
        'std_legal': 'KCS 47 10 25 강화노반 공학 다짐 수칙',
        'badge': '공학 다짐 / K30·Ev2',
        'objective': 'KCS 47 10 25에 의거하여 완료된 상부강화노반의 다짐도 ≥95%(500m³당 1회), 평판재하시험 K30 ≥110 MN/m³(2,000m²당 1회) 및 동적 변형계수 Ev2 ≥60 MPa(Ev2/Ev1 ≤2.2)를 현측 검증하여 최종 서면 승인을 완수함에 있다.',
        'rules': [
            ('수칙 1: KCS 47 10 25 3대 수치 검증 수칙', '다짐도 ≥95%, K30 ≥110 MN/m³, Ev2 ≥60 MPa(Ev2/Ev1 ≤2.2) 3대 공학 수치를 100% 만족하여야 함.'),
            ('수칙 2: 불합격 구역 재다짐 및 재검측 수칙', '수치 미달 발생 시 해당 구역 표면 파쇄, OMC 살수 후 재다짐 및 재검측을 완료함.')
        ],
        'deliv': '다짐 검측 보고서, 들밀도 성적서(KS F 2311), K30 성적서, Ev2 성적서 및 감리 최종 승인 공문',
        'steps': [
            ('STEP 01', '현장 들밀도 시험(KS F 2311)', '500m³당 1회 들밀도 시험을 시행하여 다짐도 ≥95%를 실측 검측함.'),
            ('STEP 02', 'K30 평판재하시험(KS F 2310)', '2,000m²당 1회 K30 지반반발자승(≥110 MN/m³)을 평판재하 시험 의뢰함.'),
            ('STEP 03', '동적 변형계수 Ev2 시험', '1,000m²당 1회 Ev2(≥60 MPa) 및 Ev2/Ev1(≤2.2) 변형 계수 침하를 측정함.'),
            ('STEP 04', '다짐 검측 종합 보고서 감리 승인', '3대 공학 수치 합격 성적표를 작성하여 책임감리원 최종 서면 승인을 완수함.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 다짐도, K30 및 Ev2 공학 검측 절차도',
        'diagram_nodes': [('1. 들밀도 시험', '다짐도 ≥95% 실측'), ('2. K30 & Ev2 시험', 'K30≥110, Ev2≥60MPa'), ('3. 감리 서면승인', '다짐 검측서 최종 결재')],
        'chk_items': [
            '1. 들밀도 시험(KS F 2311) 결과 노반 다짐도가 95% 이상임을 확인하였는가?',
            '2. 평판재하시험(KS F 2310) 결과 지반반발자승 K30 값이 110 MN/m³ 이상인가?',
            '3. 동적 평판재하시험 결과 변형계수 Ev2 값이 60 MPa 이상임을 실측하였는가?',
            '4. 변형계수 비율 Ev2/Ev1 값이 2.2 이하를 만족함을 확인하였는가?',
            '5. 들밀도 시험 빈도(500m³당 1회 이상)를 준수하여 측정하였는가?',
            '6. 평판재하시험 빈도(2,000m²당 1회 이상)를 준수하여 시험하였는가?',
            '7. Ev2 시험 빈도(1,000m²당 1회 이상)를 준수하여 검측하였는가?',
            '8. 시험 위치를 노반 횡단(좌, 우, 중심) 무작위 선정하였는가?',
            '9. 평판재하시험 재하 하중판(Ø300mm) 평탄 밀착 상태를 확인하였는가?',
            '10. 시험 장비(유압 잭, 침하 측정 게이지) 교정성적서를 확인하였는가?',
            '11. 수치 미달 불합격 구역 발생 시 표면 파쇄 후 재다짐을 시행하였는가?',
            '12. 재다짐 완료 구역에 대한 재검측을 실시하여 합격 판정을 받았는가?',
            '13. 다짐 검측 위치도 및 사진첩을 정밀 수록 관리하고 있는가?',
            '14. 책임감리원 1:1 현장 입회하에 공학 검측을 진행하였는가?',
            '15. 책임감리원 직인이 날인된 다짐 검측 최종 서면 승인서를 받았는가?',
            '16. 승인된 다짐 검측 성과표를 노반 인계 인수 대장에 정밀 등록하였는가?'
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

print("Batch 3 (Row 22 ~ Row 26) 5개 액티비티 총 15개 HTML 딥빌드 완료!")
