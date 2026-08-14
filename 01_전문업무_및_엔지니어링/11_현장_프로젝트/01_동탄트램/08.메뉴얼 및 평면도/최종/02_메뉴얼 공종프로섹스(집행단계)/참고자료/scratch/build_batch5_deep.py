import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

rows_data = [
    {
        'row': 32,
        'wbs': '9000-7-31',
        'dir_name': '30_사면 다짐 검측',
        'file_prefix': '사면 다짐 검측',
        'title': '사면 다짐 검측',
        'std_legal': 'KCS 47 10 25 성토 사면 구배 및 다짐 규정',
        'badge': '사면 다짐 / 거적 덮개',
        'objective': '성토 사면 구배(1:1.5 이하) 및 사면 다짐도(≥90%)를 검측하고, 우천 시 사면 유실 방지를 위한 식생 거적 덮개(Jute Mat) 부설 및 가배수로 설치를 완수하여 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 사면 구배 1:1.5 & 다짐도 90% 수칙', '성토 사면 경사는 1:1.5 이하이어야 하며 사면 전용 다짐 장비로 다짐도 90% 이상을 확보함.'),
            ('수칙 2: 식생 거적 덮개 부설 수칙', '사면 토사 유출을 방지하기 위해 쥬트 매트(Jute Mat) 거적 덮개를 30cm 겹침 부설함.')
        ],
        'deliv': '사면 다짐 검측 성과표, 사면 경사 측량 야장, 식생 거적 부설 사진 및 감리 승인서',
        'steps': [
            ('STEP 01', '성토 사면 경사(1:1.5) 측량', '광학 레벨 및 경사 측정기로 사면 비탈면 경사(1:1.5 이하)를 실측함.'),
            ('STEP 02', '사면 전용 다짐 장비 다짐', '경사 다짐 롤러 및 소형 램머로 사면 밀도(다짐도 ≥90%)를 검측함.'),
            ('STEP 03', '식생 거적 덮개(Jute Mat) 부설', '사면 세굴 방지용 거적 덮개를 30cm 겹침 부설하고 앵커 핀을 1m 간격 고정함.'),
            ('STEP 04', '사면 다짐 검측 성과 감리 승인', '사면 검측 요청서를 제출하여 책임감리원 서면 승인을 결재받음.')
        ],
        'diagram_title': '🏔️ 동탄트램 성토 사면 다짐 및 식생 거적 덮개 절차도',
        'diagram_nodes': [('1. 사면 경사 측량', '경사 1:1.5 이하 검측'), ('2. 사면 다짐/거적부설', '다짐도 90%/Jute Mat'), ('3. 감리 서면승인', '사면 다짐서 결재')],
        'chk_items': [
            '1. 성토 사면 경사(1:1.5 이하)가 도면과 일치함을 확인하였는가?',
            '2. 사면 전용 경사 다짐 롤러 및 램머 장비를 반입하였는가?',
            '3. 사면 토사 다짐도가 90% 이상임을 들밀도 시험으로 검측하였는가?',
            '4. 사면 세굴 및 유실 유무를 시각 및 레벨 측량하였는가?',
            '5. 식생 거적 덮개(Jute Mat) 품질 및 승인 자재 여부를 점검하였는가?',
            '6. 거적 덮개 상하 이음 겹침 폭(30cm 이상)을 확보하였는가?',
            '7. 앵커 핀(J형 철근 핀, 1m 간격) 고정 상태를 확인하였는가?',
            '8. 사면 어깨부 가배수로(0.4×0.4m) 설치 여부를 검측하였는가?',
            '9. 우천 시 사면 우수 집중 집수 턱 조치 여부를 점검하였는가?',
            '10. 사면 녹화 씨앗 뿜칠(Hydroseeding) 발아 상태를 점검하였는가?',
            '11. 사면 배수구 끝단 침사지 유입 연결 부위를 검측하였는가?',
            '12. 사면 다짐 전 과정 현장 사진을 촬영 철하였는가?',
            '13. 사면 다짐 검측 요청서를 감리단에 공식 접수하였는가?',
            '14. 책임감리원 1:1 현장 입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 사면 검측 승인서를 수령하였는가?',
            '16. 승인된 사면 성과표를 현장 품질 대장에 철하여 보관하고 있는가?'
        ]
    },
    {
        'row': 33,
        'wbs': '9000-7-32',
        'dir_name': '31_배수시설 시공 검측',
        'file_prefix': '배수시설 시공 검측',
        'title': '배수시설 시공 검측',
        'std_legal': 'KCS 47 10 25 노반 배수 구조물 시방 규정',
        'badge': '배수 구조물 / 인버트 사춤',
        'objective': '상부강화노반 인접 산마루 측구(U형 0.4×0.4m), 집수정 덮개(주철 그레이팅), 맹암거 유공관 연결 부위 모타르 사춤을 검측하고 통수 능력을 완수하여 감리 승인을 받음에 있다.',
        'rules': [
            ('수칙 1: 측구 구배 0.5% & 인버트 사춤 수칙', 'U형 측구 및 집수정 바닥은 통수가 원활하도록 0.5% 이상 종단 구배 및 인버트 모타르를 형성함.'),
            ('수칙 2: 주철 그레이팅 덮개 고정 수칙', '집수정 상부 주철 그레이팅 덮개는 이탈 방지 볼트 체결을 완료함.')
        ],
        'deliv': '배수시설 검측 성과표, U형 측구/집수정 측량 야장, 통수 시험 사진 및 감리 승인서',
        'steps': [
            ('STEP 01', 'U형 측구 기초 콘크리트 & 터파기', '측구 기초 터파기 깊이 및 버림 콘크리트(두께 10cm) 타설을 검측함.'),
            ('STEP 02', 'U형 측구 PC관 부설 & 집수정 성형', 'U형 측구(0.4×0.4m) 부설 및 집수정 바닥 인버트 모타르 사춤을 시행함.'),
            ('STEP 03', '주철 그레이팅 덮개 볼트 체결', '집수정 상부 주철 그레이팅 덮개를 체결하고 통수 담수 시험을 하였는가?'),
            ('STEP 04', '배수시설 검측 성과표 감리 승인', '배수 검측 요청서를 제출하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '🌊 동탄트램 배수시설(U형 측구 & 집수정) 시공 및 검측 절차도',
        'diagram_nodes': [('1. 측구 터파기/기초', '버림 콘크리트 10cm'), ('2. U형측구/집수정', '인버트 모타르 사춤'), ('3. 감리 서면승인', '배수시설 검측서 결재')],
        'chk_items': [
            '1. U형 측구(0.4×0.4m) 버림 콘크리트 타설 두께(10cm)를 확인하였는가?',
            '2. U형 측구 PC 제품 공인 기관 시험성적서를 확인하였는가?',
            '3. 측구 종단 배수 구배가 0.5% 이상임을 광학 레벨로 측량하였는가?',
            '4. 측구 이음부 시멘트 모타르 사춤 밀실도를 검측하였는가?',
            '5. 집수정 바닥 물고임 방지 인버트 모타르 곡면 성형을 하였는가?',
            '6. 맹암거 유공관(Ø200mm) 집수정 연결 부위 틈새 사춤을 확인하였는가?',
            '7. 집수정 상부 주철 그레이팅 덮개 규격 및 도막 도장을 점검하였는가?',
            '8. 그레이팅 덮개 이탈 방지 잠금 볼트 체결 상태를 확인하였는가?',
            '9. 배수로 내 토사 및 잔재물 통수 준설 상태를 점검하였는가?',
            '10. 담수 시험을 통해 배수로 물흐름(통수 능력)이 원활함을 확인하였는가?',
            '11. 측구 뒤채움 토사 층다짐(다짐도 ≥90%) 상태를 검측하였는가?',
            '12. 배수구 끝단 하천 연결 부위 세굴 방지 사석 부설을 확인하였는가?',
            '13. 배수시설 완성 시공 사진첩을 작성하였는가?',
            '14. 책임감리원 1:1 현장 입회 검측을 시행하였는가?',
            '15. 책임감리원 직인이 날인된 배수시설 승인서를 수령하였는가?',
            '16. 승인된 배수 성과를 현장 관리 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 34,
        'wbs': '9000-7-33',
        'dir_name': '32_완성면 보호',
        'file_prefix': '완성면 보호',
        'title': '완성면 보호',
        'std_legal': 'KCS 47 10 25 다짐 완성면 유지 관리 규정',
        'badge': '완성면 보호 / 통제 바리케이트',
        'objective': '다짐 및 강성 검측이 완수된 상부강화노반 완성면에 덤프트럭 및 중장비 무단 주행을 차단(가설 펜스/바리케이트 설치)하고, 살수 수분 유지 및 비닐 덮개를 부설하여 궤도 시공팀 인계 전까지 보존함에 있다.',
        'rules': [
            ('수칙 1: 중장비 통제 바리케이트 수칙', '완성면 입구에 통제 바리케이트 및 위험 표지판을 설치하여 중장비 무단 진입을 100% 차단함.'),
            ('수칙 2: 노반 표면 살수 & 비닐 덮개 수칙', '건조에 따른 골재 이탈을 방지하기 위해 일일 살수 및 강우 시 비닐 덮개를 부설함.')
        ],
        'deliv': '완성면 보호 점검표, 통제 펜스 부설 사진, 살수 일지 및 감리 승인서',
        'steps': [
            ('STEP 01', '완성면 통제 바리케이트 & 표지판 설치', '강화노반 완성면 경계에 통제 펜스 및 주행 금지 표지판을 비치함.'),
            ('STEP 02', '일일 살수 & 비닐 덮개 부설', '골재 이탈 예방용 미세 분무 살수를 시행하고 비 비닐 덮개를 야적함.'),
            ('STEP 03', '궤도 인수 전 일일 훼손 현측 점검', '일일 완성면 훼손 여부를 점검하고 장비 무단 진입을 통제함.'),
            ('STEP 04', '완성면 보호 점검 대장 감리 승인', '보호 대장을 작성하여 책임감리원 서면 승인을 결재받음.')
        ],
        'diagram_title': '🚧 동탄트램 강화노반 완성면 무단 주행 통제 및 보호 절차도',
        'diagram_nodes': [('1. 통제 바리케이트', '중장비 무단진입 차단'), ('2. 살수/비닐 덮개', '골재이탈 예방 살수'), ('3. 감리 서면승인', '완성면 보호대장 결재')],
        'chk_items': [
            '1. 강화노반 완성면 통제 바리케이트를 설치하였는가?',
            '2. "통행 금지 및 강화노반 보호 구역" 표지판을 비치하였는가?',
            '3. 완성면 덤프트럭 및 중장비 무단 통행을 100% 차단하였는가?',
            '4. 건조 기후 시 표면 살수차 미세 분무 살수를 시행하였는가?',
            '5. 강우 특보 시 완성면 전체 비닐 덮개 부설을 조치하였는가?',
            '6. 타 공종(신호, 통신 관로 작업) 무단 굴착 방지 협의를 이행하였는가?',
            '7. 노반 표면 골재 박리 및 세립분 유실 유무를 점검하였는가?',
            '8. 완성면 세륜 슬러지 및 외부 토사 오염 유입을 차단하였는가?',
            '9. 궤도 시공팀 인수 전까지 일일 완성면 점검표를 작성하고 있는가?',
            '10. 노반 단부 사면 토사 침시 방지 가배수로 가동을 점검하였는가?',
            '11. 야간 완성면 안내 경광등 및 야광 띠 설치를 하였는가?',
            '12. 현장 순찰조를 편성하여 주간 2회 이상 완성면을 전수 현측하고 있는가?',
            '13. 완성면 보존 상태 사진첩을 정밀 수록하였는가?',
            '14. 책임감리원 1:1 입회하에 완성면 보호 상태를 수검하였는가?',
            '15. 책임감리원 직인이 날인된 완성면 보호 승인서를 수령하였는가?',
            '16. 승인된 보호 대장을 현장 공무 대장에 등록 보관하고 있는가?'
        ]
    },
    {
        'row': 35,
        'wbs': '9000-7-34',
        'dir_name': '33_공사일지 작성',
        'file_prefix': '공사일지 작성',
        'title': '공사일지 작성',
        'std_legal': '건설기술진흥법 시행규칙 & 공사기록 작성 규정',
        'badge': '공사일지 / 법정 기록',
        'objective': '건설기술 진흥법에 의거하여 일일 투입 인원, 동원 장비, 사토/성토 물량(m³), 노반 다짐도 및 레벨 시험 성적을 정밀 공사일지에 수록하고 감리 서면 결재를 완료함에 있다.',
        'rules': [
            ('수칙 1: 일일 공사 데이터 100% 기록 수칙', '인원, 장비, 물량, 기상 조건 및 품질 시험 결과를 일일 공사일지에 누락 없이 정밀 수록함.'),
            ('수칙 2: 전산 시스템 및 서면 결재 수칙', '공사일지는 건설공사관리시스템(CIMS/CSI)에 등록하고 책임감리원 일일 결재를 받음.')
        ],
        'deliv': '일일 공사일지 원본, 장비/인원 집계표, 자재 수불 대장 및 감리 결재서',
        'steps': [
            ('STEP 01', '일일 인원 · 장비 · 물량 데이터 집계', '작업조 인원, 강동 롤러 등 장비 및 토공 성토 물량(m³)을 정밀 집계함.'),
            ('STEP 02', '품질 시험 성적 & TBM 사항 수록', '들밀도 시험, K30 평판재하 수치 및 일일 TBM 내용을 공사일지에 부착함.'),
            ('STEP 03', '전산 시스템(CSI/CIMS) 일일 등록', '국토교통부 및 현장 전산 관리 시스템에 일일 일지를 수록 등록함.'),
            ('STEP 04', '책임감리원 일일 서면 결재 수검', '공사일지를 작성하여 매일 책임감리원 공학적 직인 결재를 완수함.')
        ],
        'diagram_title': '📝 동탄트램 일일 공사일지 작성 및 감리 결재 절차도',
        'diagram_nodes': [('1. 데이터 정밀집계', '인원/장비/물량 집계'), ('2. 전산 시스템 등록', 'CSI/CIMS 전산 등록'), ('3. 감리 서면승인', '일일 공사일지 결재')],
        'chk_items': [
            '1. 건설기술 진흥법 표준 서식에 맞춘 공사일지를 작성하였는가?',
            '2. 일일 작업조 투입 인원 수(직종별)를 정밀 기록하였는가?',
            '3. 반입 및 가동 건설기계 장비(롤러, 백호 등) 수량을 집계하였는가?',
            '4. 일일 토사 성토 및 쇄석 포설 물량(m³)을 기록하였는가?',
            '5. 당일 시행한 다짐도, K30, Ev2 시험 결과를 수록하였는가?',
            '6. 일일 기상 조건(최고/최저 기온, 강수량 mm)을 기록하였는가?',
            '7. 작업전 일일 TBM 및 위험성 평가 결과 요약을 포함하였는가?',
            '8. 당일 자재 반입 물량 및 수불 현황을 기록하였는가?',
            '9. 안전보건 점검 사항 및 지하시설물 협의 내용을 포함하였는가?',
            '10. 공사일지 전산 관리 시스템(CIMS/CSI) 등록을 마쳤는가?',
            '11. 공사일지 첨부 서류(출하증, 시험성적서)를 철하였는가?',
            '12. 현장 대리인(현장소장) 결재 날인 상태를 확인하였는가?',
            '13. 책임감리원 일일 서면 결재를 매일 수검하고 있는가?',
            '14. 감리원 지적 사항 및 조치 결과 내용을 수록하였는가?',
            '15. 승인된 공사일지 원본을 현장 사무실에 보관하고 있는가?',
            '16. 준공용 공사 기록 대장에 공사일지를 전산 바인딩하였는가?'
        ]
    },
    {
        'row': 36,
        'wbs': '9000-7-35',
        'dir_name': '35_검측 및 승인 관리',
        'file_prefix': '검측 및 승인 관리',
        'title': '검측 및 승인 관리',
        'std_legal': '건설기술진흥법 & KCS 47 10 25 총괄 검측 규정',
        'badge': '총괄 검측 / 승인 대장',
        'objective': '상부강화노반 시공 전 과정의 검측 요청서(공사 착수 24시간 전 제출), 검측 체크리스트, 3대 공학 수치(다짐도, K30, Ev2) 성적표 및 감리 승인 공문을 총괄 대장으로 수록 관리함에 있다.',
        'rules': [
            ('수칙 1: 공사 착수 24시간 전 검측 제출 수칙', '모든 공종별 검측 요청서는 시공 최소 24시간 전 책임감리단에 공식 접수함.'),
            ('수칙 2: 검측 승인 총괄 대장 전산화 수칙', '발행된 모든 검측 승인 공문 및 체크리스트를 전산 대장에 100% 수록함.')
        ],
        'deliv': '검측 총괄 대장, 검측 요청서 모음집, 승인 공문 바인더 및 감리 최종 결재서',
        'steps': [
            ('STEP 01', '공종별 검측 요청서 24시간 전 제출', '원지반, 하부노반, 강화노반 검측 요청서를 감리단에 공식 접수함.'),
            ('STEP 02', '책임감리원 1:1 현장 입회 검측', '감리원 입회하에 레벨, 다짐도, K30, Ev2를 1:1 현장 수검함.'),
            ('STEP 03', '검측 체크리스트 서명 & 승인 공문', '16개 문항 체크리스트 감리 서명 및 적정 승인 공문을 수령함.'),
            ('STEP 04', '검측 총괄 승인 대장 바인딩', '승인 공문 및 성적표를 총괄 대장에 등록하여 감리 결재를 완수함.')
        ],
        'diagram_title': '📑 동탄트램 강화노반 총괄 검측 및 승인 공문 관리 절차도',
        'diagram_nodes': [('1. 검측요청 24h 전', '공문/체크리스트 제출'), ('2. 감리 1:1 입회', '3대 공학수치 현측'), ('3. 감리 서면승인', '검측 총괄대장 결재')],
        'chk_items': [
            '1. 검측 요청서를 공사 착수 최소 24시간 전 감리단에 제출하였는가?',
            '2. 검측 체크리스트 16개 정밀 문항을 100% 점검하였는가?',
            '3. 현장 책임감리원 1:1 입회 검측을 시행하였는가?',
            '4. 다짐도(≥95%), K30(≥110), Ev2(≥60) 합격 성적표를 첨부하였는가?',
            '5. 광학 레벨 측량 야장 및 BIM 좌표 대조표를 확인하였는가?',
            '6. 검측 현장 사진(전, 중, 후 컷)을 1:1 부착하였는가?',
            '7. 불합격 발생 시 부적합 조치 결과서를 즉시 첨부하였는가?',
            '8. 책임감리원 직인이 날인된 검측 승인 통보서를 받았는가?',
            '9. 검측 번호 부여 및 연번 관리 대장을 구축하였는가?',
            '10. 공종별(원지반, 하부, 상부, 강화노반) 검측 서류를 바인딩하였는가?',
            '11. 검측 승인 문서를 전산 시스템에 100% 업로드 하였는가?',
            '12. 발주처 정기 감평 시 검측 총괄 대장을 비치하였는가?',
            '13. 검측 성과에 대해 시공 대리인 및 품질 관리자 서명을 필하였는가?',
            '14. 감리원 지적 사항 100% 보완 완수 여부를 확인하였는가?',
            '15. 검측 총괄 대장에 대해 책임감리원 최종 서면 승인을 결재받았는가?',
            '16. 승인된 총괄 대장을 준공 아카이빙 폴더에 보관하고 있는가?'
        ]
    },
    {
        'row': 37,
        'wbs': '9000-7-36',
        'dir_name': '36_토공 마무리면 인계',
        'file_prefix': '토공 마무리면 인계',
        'title': '토공 마무리면 인계',
        'std_legal': 'KCS 47 10 25 강화노반 최종 인계인수 규정',
        'badge': '최종 인계 / 3자 서명',
        'objective': '완성된 상부강화노반 마무리면(표고 오차 ±10mm, K30 ≥110 MN/m³, Ev2 ≥60 MPa)을 토공 시공사-궤도 시공사-책임감리단 3자 합동 현측을 거쳐 궤도 콘크리트 도상 팀에 100% 최종 인계인수함에 있다.',
        'rules': [
            ('수칙 1: 3자(토공-궤도-감리) 합동 현측 수칙', '인계 전 토공 시공사, 궤도 시공사, 책임감리원이 합동으로 표고 및 K30 강성을 재확인함.'),
            ('수칙 2: 토공 마무리면 인계인수서 체결 수칙', '합동 현측 완료 후 3자 서명이 날인된 마무리면 인계인수 합의서를 작성 수속함.')
        ],
        'deliv': '토공 마무리면 인계인수서(3자 서명), 최종 종합 성적표, 합동 측량 야장 및 감리 승인 공문',
        'steps': [
            ('STEP 01', '3자(토공-궤도-감리) 합동 현측 세팅', '인계 구간(STA 0k+000 ~ 0k+500)에 대해 3자 합동 검측 일정을 수립함.'),
            ('STEP 02', '표고 오차(±10mm) & K30(≥110) 재검측', '궤도 설치 인접 부위 중심선 레벨 및 평판재하 K30 강도를 합동 재확인함.'),
            ('STEP 03', '토공 마무리면 인계인수서 3자 서명', '결과 이상 없음을 확인하고 인계인수 합의서에 토공, 궤도, 감리 3자 서명함.'),
            ('STEP 04', '상부강화노반 최종 완공 통보', '인계인수서 및 최종 성과표를 발주처에 공식 통보하여 노반 공사를 완수함.')
        ],
        'diagram_title': '🏁 동탄트램 상부강화노반 궤도 시공팀 최종 인계인수 절차도',
        'diagram_nodes': [('1. 3자 합동 현측', '표고 ±10mm / K30 110'), ('2. 인계인수서 서명', '토공-궤도-감리 3자 서명'), ('3. 발주처 완공통보', '강화노반 최종 완공')],
        'chk_items': [
            '1. 상부강화노반 전체 시공 구간 완공 여부를 확인하였는가?',
            '2. 토공 시공사, 궤도 시공사, 책임감리단 3자 합동 현측 일정을 수립하였는가?',
            '3. 합동 측량 결과 마무리면 표고 오차가 ±10mm 이내임을 재확인하였는가?',
            '4. 합동 K30 평판재하시험(≥110 MN/m³)을 재실시하여 확인하였는가?',
            '5. 합동 Ev2 동적 변형계수(≥60 MPa, Ev2/Ev1≤2.2) 수치를 검측하였는가?',
            '6. 맹암거 유공관 배수 집수정 통수 상태를 3자 공동 점검하였는가?',
            '7. 강화노반 마무리면 이물질 및 토사 오염 제로 상태를 확인하였는가?',
            '8. 궤도 도상 시공용 3D 좌표 기준점(CP/TBM)을 궤도 팀에 인계하였는가?',
            '9. 3자 서명이 날인된 "토공 마무리면 인계인수 합의서"를 작성하였는가?',
            '10. 인계 후 궤도 공사 착수 전까지의 노반 보호 책임을 명확히 규정하였는가?',
            '11. 종합 품질 성적서(다짐도, K30, Ev2, 입도) 바인더를 인계하였는가?',
            '12. 종합 안전 및 환경 준공 서류를 정리 접수하였는가?',
            '13. 발주처(화성시/LH)에 상부강화노반 완공 공문을 공식 제출하였는가?',
            '14. 책임감리원 직인이 날인된 인계인수 최종 승인 공문을 수령하였는가?',
            '15. 강화노반 준공 도면 및 3D BIM 최종본을 시스템 등록하였는가?',
            '16. 승인된 인계인수 문서를 준공 영구 아카이빙 대장에 철하여 보관하고 있는가?'
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

print("Batch 5 (Row 32 ~ Row 37) 6개 액티비티 총 18개 HTML 딥빌드 최종 완성!")
