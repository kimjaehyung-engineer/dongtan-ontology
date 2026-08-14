import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

rows_data = [
    {
        'row': 27,
        'wbs': '9000-7-26',
        'dir_name': '25_평판재하시험',
        'file_prefix': '평판재하시험',
        'title': '평판재하시험',
        'std_legal': 'KS F 2310 & KCS 47 10 25 지반반발자승 규정',
        'badge': 'K30 시험 / KS F 2310',
        'objective': 'KS F 2310에 의거하여 완료된 상부강화노반 표면에서 Ø300mm 재하판과 유압 잭을 활용해 지반반발자승 K30(≥110 MN/m³, 2,000m²당 1회)을 정밀 측정하고 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: K30 ≥ 110 MN/m³ 수칙', '강화노반 평판재하시험 지반반발자승 K30 목표치 110 MN/m³ 이상을 100% 만족하여야 함.'),
            ('수칙 2: 재하판 밀착 & 2,000m² 빈도 수칙', '재하판 하부 산모래 평탄 밀착 시공 및 2,000m²당 1회 이상 무작위 검측을 시행함.')
        ],
        'deliv': '평판재하시험 성적서(KS F 2310), P-S 곡선 그래프, 시험 위치도 및 감리 승인서',
        'steps': [
            ('STEP 01', '재하판 하부 평탄성 및 산모래 부설', 'Ø300mm 재하판 하부에 산모래를 부설하고 평탄 밀착 상태를 검측함.'),
            ('STEP 02', '유압 잭 & 침하 게이지 정밀 교정', '15t 유압 잭 및 0.01mm 정밀도 다이얼 게이지 2개를 반사침 세팅함.'),
            ('STEP 03', '단계별 재하 하중 및 침하량(1.25mm) 측정', '하중 단계별 P-S 하중-침하 곡선을 도출하여 K30 값을 산출함.'),
            ('STEP 04', 'K30 시험 성적표 감리 서면 승인', 'K30 ≥110 MN/m³ 합격 성적서를 부착하여 책임감리원 결재를 완수함.')
        ],
        'diagram_title': '📊 동탄트램 강화노반 K30 평판재하시험 및 지비력 측정 절차도',
        'diagram_nodes': [('1. Ø300mm 재하판 설치', '산모래 부설/밀착'), ('2. 유압잭 재하하중', 'P-S 하중침하곡선'), ('3. 감리 서면승인', 'K30 ≥110 성적서 결재')],
        'chk_items': [
            '1. 평판재하시험 표준 규격(KS F 2310)을 준수하였는가?',
            '2. 재하 하중판(Ø300mm) 수평 상태 및 하부 밀착을 확인하였는가?',
            '3. 유압 잭 하중 지지용 반력 장비(15톤 이상 덤프트럭)를 세팅하였는가?',
            '4. 다이얼 게이지(0.01mm 정밀도) 2개 이상을 정밀 교정하였는가?',
            '5. 시험 빈도(2,000m²당 1회 이상)를 준수하여 시험하였는가?',
            '6. 지반반발자승 K30 값이 110 MN/m³ 이상임을 확인하였는가?',
            '7. 하중 침하 1.25mm 기준 K30 강도 산식을 정밀 계산하였는가?',
            '8. 하중 단계별(35, 70, 105, 140 kN/m² 등) 침하량을 측정하였는가?',
            '9. P-S(하중-침하) 그래프 곡선 비선형성을 검증하였는가?',
            '10. 시험 구역 내 강우 직후 수분 침투에 따른 영향을 차단하였는가?',
            '11. K30 미달 구역 발생 시 해당 층 파쇄 후 재다짐을 조치하였는가?',
            '12. 시험 장비 공인 교정성적서 유효 기간을 점검하였는가?',
            '13. 평판재하시험 전 과정 현장 사진을 촬영 철하였는가?',
            '14. 책임감리원 1:1 현장 입회하에 기술 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 K30 성적표 승인을 받았는가?',
            '16. 승인된 K30 성과표를 노반 품질 관리 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 28,
        'wbs': '9000-7-27',
        'dir_name': '26_강성 검측(K30, EV2)',
        'file_prefix': '강성 검측(K30, EV2)',
        'title': '강성 검측(K30, EV2)',
        'std_legal': 'DIN 18134 & KCS 47 10 25 변형계수 규정',
        'badge': '강성 검측 / Ev2·Ev1',
        'objective': 'DIN 18134 및 KCS 47 10 25에 의거하여 강화노반의 2차 변형계수 Ev2(≥60 MPa) 및 변형계수 비율 Ev2/Ev1(≤2.2)을 동적 평판재하시험(LWD)으로 1,000m²당 1회 검측하여 탄성 복원 강성을 완수함에 있다.',
        'rules': [
            ('수칙 1: Ev2 ≥ 60 MPa 수칙', '동적 변형계수 Ev2 지반 탄성 탄성 계수 목표치 60 MPa 이상을 100% 만족하여야 함.'),
            ('수칙 2: Ev2/Ev1 ≤ 2.2 비율 수칙', '1차/2차 변형계수 비율 Ev2/Ev1 이 2.2 이하임을 확인하여 다짐 밀집도를 판정함.')
        ],
        'deliv': '강성 검측 보고서(DIN 18134), Ev2 성적서, Ev2/Ev1 분석표 및 감리 승인서',
        'steps': [
            ('STEP 01', '동적 평판재하시험기(LWD) 교정', 'LWD 가속도 센서 및 전자식 강성 측정기를 정밀 교정함.'),
            ('STEP 02', '1,000m²당 1회 무작위 포인트 선정', '강화노반 1,000m²마다 시험 지점 3개소를 무작위 지정함.'),
            ('STEP 03', '1차/2차 하중 재하 & Ev2/Ev1 산출', '1차(Ev1) 및 2차(Ev2) 하중 충격을 가해 변형 계수 비율을 도출함.'),
            ('STEP 04', '강성 검측 종합 보고서 감리 승인', 'Ev2 ≥60 MPa 성적표를 작성하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 동적 변형계수 Ev2 및 Ev2/Ev1 강성 검측 절차도',
        'diagram_nodes': [('1. LWD 장비 교정', '가속도 센서 세팅'), ('2. Ev1/Ev2 재하', 'Ev2 ≥60, Ev2/Ev1≤2.2'), ('3. 감리 서면승인', '강성 검측서 결재')],
        'chk_items': [
            '1. 동적 평판재하시험(DIN 18134 규격) 장비를 준비하였는가?',
            '2. 2차 변형계수 Ev2 값이 60 MPa 이상임을 실측하였는가?',
            '3. 변형계수 비율 Ev2/Ev1 값이 2.2 이하를 만족하는가?',
            '4. 1차 변형계수 Ev1 값이 공학적 기준을 만족함을 확인하였는가?',
            '5. 강성 검측 시험 빈도(1,000m²당 1회 이상)를 준수하였는가?',
            '6. 동적 평판재하시험기(LWD) 낙하 추 중량 및 낙하 높이를 확인하였는가?',
            '7. 지반 센서 침하량 측정 정밀도(0.001mm) 교정 성적을 검증하였는가?',
            '8. 시험 지점을 노반 궤도 중심선 및 양측 1.5m 부근으로 분산하였는가?',
            '9. 강성 수치 미달 구역 발생 시 쇄석 추가 포설 및 재다짐을 조치하였는가?',
            '10. 재다짐 완료 구역 Ev2 재시험을 시행하여 합격 판정을 받았는가?',
            '11. 강성 검측 위치별 GPS 좌표 및 침하 데이터를 시스템에 기록하였는가?',
            '12. 강우 직후 노반 수분 과다 상태에서의 강성 측정 오류를 방지하였는가?',
            '13. 강성 검측 성적표에 측정 기사 및 현장 대리인 서명을 필하였는가?',
            '14. 책임감리원 1:1 입회하에 기술 검측을 실시하였는가?',
            '15. 책임감리원 직인이 날인된 강성 검측 최종 승인서를 수령하였는가?',
            '16. 승인된 강성 검측 성과표를 노반 품질 관리 대장에 철하여 보관하고 있는가?'
        ]
    },
    {
        'row': 29,
        'wbs': '9000-7-28',
        'dir_name': '27_평탄성 검측',
        'file_prefix': '평탄성 검측',
        'title': '평탄성 검측',
        'std_legal': 'KCS 47 10 25 3m 직선자 평탄성 규정',
        'badge': '평탄성 / ±10mm',
        'objective': 'KCS 47 10 25에 의거하여 완료된 상부강화노반 표면을 3m 직선자(Straight Edge)로 종횡단 연속 측정하여 최대 오차 ±10mm 이내의 평탄성을 완수함에 있다.',
        'rules': [
            ('수칙 1: 3m 직선자 오차 ±10mm 수칙', '노반 표면 3m 직선자 갭 오차는 ±10mm 이하이어야 하며 초과 시 즉시 삭평/재다짐함.'),
            ('수칙 2: 20m 간격 연속 측정 수칙', '종단 및 횡단 20m 간격으로 직선자 측정 마크를 표시하고 전수 실측함.')
        ],
        'deliv': '평탄성 검측 야장, 3m 직선자 오차 성과표, 불량 수정 사진 및 감리 승인서',
        'steps': [
            ('STEP 01', '3m 알루미늄 직선자 검교정', '변형이 없는 3m 알루미늄 평탄 측정자 및 테이퍼 쐐기 핑거 게이지를 준비함.'),
            ('STEP 02', '20m 간격 종횡단 연속 검측', '노반 중심선 및 좌우 궤도 부근 20m 간격으로 직선자를 밀착 측정함.'),
            ('STEP 03', '요철(오목/볼록) 지점 현출 & 수정', '오목 부위(10mm 초과) OMC 살수 재다짐 및 볼록 부위 모터그레이더 삭평을 조치함.'),
            ('STEP 04', '평탄성 검측 성과표 감리 승인', '평탄성 야장을 정리하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '📏 동탄트램 강화노반 3m 직선자 평탄성 검측 절차도',
        'diagram_nodes': [('1. 3m 직선자 준비', '테이퍼 게이지 교정'), ('2. 20m 간격 연속검측', '오차 ±10mm 이내 실측'), ('3. 감리 서면승인', '평탄성 성과표 결재')],
        'chk_items': [
            '1. 3m 알루미늄 평탄성 직선자 변형 유무를 점검하였는가?',
            '2. 테이퍼 쐐기 핑거 게이지(0.5mm 정밀도)를 준비하였는가?',
            '3. 3m 직선자 측정 최대 갭 오차가 ±10mm 이내임을 확인하였는가?',
            '4. 종단 방향 20m 간격 연속 측정을 시행하였는가?',
            '5. 횡단 방향 트램 궤도 선로부 3m 측정 마크를 검측하였는가?',
            '6. 오목 지점(10mm 초과) 발생 시 쇄석 보충 및 살수 재다짐을 하였는가?',
            '7. 볼록 지점(10mm 초과) 발생 시 모터그레이더 정밀 삭평을 시행하였는가?',
            '8. 강화노반 마무리면 돌출 거대 쇄석(50mm 초과) 제거 상태를 점검하였는가?',
            '9. 평탄성 측정 위치별 갭 오차(mm)를 야장에 상세 수록하였는가?',
            '10. 트램 궤도 콘크리트 도상 인접부 평탄도 연계성을 검토하였는가?',
            '11. 불합격 요철 구역 수정 후 재측량을 100% 완료하였는가?',
            '12. 평탄성 검측 현장 사진(직선자 밀착 컷)을 촬영 철하였는가?',
            '13. 평탄성 검측 요청서를 감리단에 공식 접수하였는가?',
            '14. 책임감리원 1:1 입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 평탄성 승인서를 수령하였는가?',
            '16. 승인된 평탄성 야장을 현장 품질 관리 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 30,
        'wbs': '9000-7-29',
        'dir_name': '28_노반 종 횡단 검측',
        'file_prefix': '노반 종 횡단 검측',
        'title': '노반 종 횡단 검측',
        'std_legal': 'KCS 47 10 25 강화노반 중심선 및 표고 측량 규정',
        'badge': '종횡단 / 중심선 오차',
        'objective': 'GRS80 광학 토탈스테이션으로 강화노반 궤도 중심선 이탈 오차(±10mm), 마무리면 표고 오차(±10mm) 및 횡단 배수 경사(2% 이상)를 10m 간격 실측하여 3D BIM 좌표 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 중심선 & 표고 오차 ±10mm 수칙', '트램 선로 중심선 평면 위치 및 계획 표고 오차는 ±10mm 이하로 관리함.'),
            ('수칙 2: 10m 간격 횡단 측량 야장 수칙', '10m 간격 횡단 측량을 시행하고 3D BIM CAD 설계 좌표와 1:1 대조함.')
        ],
        'deliv': '종횡단 측량 성과표, 3D BIM 좌표 대조표, 횡단도면 및 감리 승인서',
        'steps': [
            ('STEP 01', 'GRS80 광학 토탈스테이션 정밀 세팅', '인근 CP/TBM 기준점을 후시하여 레벨 및 평면 좌표를 정밀 세팅함.'),
            ('STEP 02', '10m 간격 중심선 & 표고 실측', '10m 간격으로 궤도 중심선(X,Y) 및 마무리면 표고(Z)를 현측함.'),
            ('STEP 03', '3D BIM CAD 좌표 1:1 대조', '측량 성과 데이터를 3D BIM 모델 좌표계에 매핑하여 오차(±10mm)를 검증함.'),
            ('STEP 04', '종횡단 성과표 감리 서면 승인', '종횡단 측량 성과표를 작성하여 책임감리원 최종 승인을 완료함.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 종횡단 측량 및 3D BIM 좌표 검측 절차도',
        'diagram_nodes': [('1. GRS80 측량세팅', 'CP/TBM 후시 점검'), ('2. 10m 간격 측량', '중심선/표고 ±10mm'), ('3. 감리 서면승인', '3D BIM 성과표 결재')],
        'chk_items': [
            '1. 광학 토탈스테이션 및 자동 레벨 교정성적서를 확인하였는가?',
            '2. 트램 궤도 중심선 평면 이탈 오차가 ±10mm 이내임을 측량하였는가?',
            '3. 강화노반 마무리면 계획 표고 레벨 오차가 ±10mm 이내인가?',
            '4. 종단 방향 10m 간격 정밀 측량을 시행하였는가?',
            '5. 횡단 경사(2% 이상)가 좌우 균형 있게 형성되었는가?',
            '6. 노반 횡단 폭(설계 폭 대비 0 ~ +10cm 이내)을 실측하였는가?',
            '7. 곡선 구간 확폭 및 가고(Cant) 형성 상태를 검측하였는가?',
            '8. 측량 데이터를 3D BIM 모델 좌표계와 1:1 대조하였는가?',
            '9. 표고 오차 초과 구간 절토 삭평 및 성토 재다짐을 조치하였는가?',
            '10. 배수 집수정 인접 구간 접속 표고 레벨 일치성을 점검하였는가?',
            '11. 종횡단 측량 야장에 측량 기사 및 확인자 서명을 필하였는가?',
            '12. 측량 핀 및 경계 말뚝 훼손 방지 보호 조치를 이행하였는가?',
            '13. 종횡단 측량 성과표를 착공전 측량 성과표와 비교 검증하였는가?',
            '14. 책임감리원 1:1 입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 종횡단 승인서를 수령하였는가?',
            '16. 승인된 종횡단 성과표를 인계인수 서류에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 31,
        'wbs': '9000-7-30',
        'dir_name': '29_부적합 사항 조치',
        'file_prefix': '부적합 사항 조치',
        'title': '부적합 사항 조치',
        'std_legal': '건설기술진흥법 & KCS 47 10 25 NCR 절차 규정',
        'badge': 'NCR 조치 / 표면 파쇄',
        'objective': '다짐, K30, Ev2, 평탄성, 표고 검측에서 부적합(NCR) 발생 시 해당 구역 표면 파쇄(두께 15cm 이상), 살수 재다짐 및 1:1 재검측을 시행하여 지적 사항을 100% 소멸하고 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 표면 15cm 파쇄 및 재다짐 수칙', '부적합 판정 구역은 단순 전압을 금지하고 표면 15cm 이상 긁어내어 살수 재다짐함.'),
            ('수칙 2: 1:1 재검측 & NCR 소멸 수칙', '재다짐 완료 후 다짐도, K30, Ev2를 1:1 재검측하여 감리단 NCR 소멸 서명을 받음.')
        ],
        'deliv': '부적합 조치 결과서(NCR), 원인 분석 보고서, 재검측 성적서 및 감리 승인서',
        'steps': [
            ('STEP 01', '감리단 부적합 통지서(NCR) 수령', 'NCR 발행 지점의 지번, 위치 및 미달 수치(예: 다짐도 92%)를 확인함.'),
            ('STEP 02', '표면 15cm 파쇄 & OMC 살수 재다짐', '모터그레이더 리퍼로 15cm 파쇄 후 최적함수비 살수 및 롤러 재다짐을 시행함.'),
            ('STEP 03', '1:1 재검측(다짐도/K30/Ev2) 실시', '재다짐 구역에 대해 들밀도, K30, Ev2 시험을 1:1 재실시하여 합격 수치를 도출함.'),
            ('STEP 04', 'NCR 조치 결과 보고서 감리 승인', '조치 전·후 사진 및 재검측 성적서를 제출하여 감리 서면 종결 승인을 받음.')
        ],
        'diagram_title': '⚠️ 동탄트램 강화노반 부적합(NCR) 조치 및 재다짐 절차도',
        'diagram_nodes': [('1. NCR 발행 수령', '부적합 위치 현출'), ('2. 표면15cm 파쇄/재다짐', 'OMC 살수 및 롤러다짐'), ('3. 감리 서면승인', '1:1 재검측 NCR 종결')],
        'chk_items': [
            '1. 책임감리단 발행 부적합 통지서(NCR) 내용을 확인하였는가?',
            '2. 부적합 발생 원인(함수비 과다/부족, 다짐 횟수 부족 등)을 정밀 분석하였는가?',
            '3. 부적합 구역 범주를 현측하고 적색 경계 띠를 설치하였는가?',
            '4. 단순 추가 롤링을 금지하고 표면 15cm 이상 긁어내기(파쇄)를 시행하였는가?',
            '5. 파쇄 골재의 최적함수비(OMC ± 2%) 유지를 위한 살수를 시행하였는가?',
            '6. 강동 롤러 4회 이상 재다짐을 정밀 이행하였는가?',
            '7. 재다짐 구역 들밀도 시험(KS F 2311) 다짐도 95% 이상을 재확인하였는가?',
            '8. 재다짐 구역 K30 평판재하시험(≥110 MN/m³)을 재실시하였는가?',
            '9. 재다짐 구역 Ev2(≥60 MPa) 및 Ev2/Ev1(≤2.2)을 재검측하였는가?',
            '10. 재측량 결과 표고 레벨 오차가 ±10mm 이내로 복원되었는가?',
            '11. 부적합 조치 전, 중, 후 현장 사진을 1:1 촬영 철하였는가?',
            '12. 재발 방지를 위한 작업조 및 장비 조종원 교육을 실시하였는가?',
            '13. 부적합 조치 결과 보고서를 작성하여 감리단에 공식 제출하였는가?',
            '14. 책임감리원 현장 재입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 NCR 종결 서면 승인을 받았는가?',
            '16. 승인된 NCR 조치 보고서를 현장 품질 대장에 철하여 보관하고 있는가?'
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

print("Batch 4 (Row 27 ~ Row 31) 5개 액티비티 총 15개 HTML 딥빌드 완료!")
