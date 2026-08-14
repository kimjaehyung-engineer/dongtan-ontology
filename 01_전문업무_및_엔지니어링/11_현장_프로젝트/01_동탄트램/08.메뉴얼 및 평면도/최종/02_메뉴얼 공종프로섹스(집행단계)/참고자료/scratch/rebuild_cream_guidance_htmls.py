import os, sys

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

manuals_cream_data = [
    {
        'row': 3,
        'wbs': '9000-7-2',
        'dir_name': '2_발주전략 KOM',
        'file_prefix': '발주전략 KOM',
        'title': '발주전략 KOM',
        'std_legal': 'KCS 47 10 25 강화노반 시공 발주 시방서 규정',
        'desc': '본 수행지침서는 동탄트램 상부강화노반 전체 공정의 사업 착수 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 발주처 시방서 검토</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 3D BIM 도면 1:1 대조</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 RISK Factor 및 해징 전략 수립</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">KOM 미팅 결재</span>의 킥오프 추진 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '발주처 시방서 & 기술 사양 검토', '발주처 계약 시방서 KCS 47 10 25 및 입찰안내서 요구조건을 1:1 정밀 분석함.'),
            ('STEP 02', '3D BIM 설계 도면 & 좌표 검증', '상부강화노반 계획 표고, 횡단 구배(2%) 및 3D BIM 모델 좌표 연동성을 점검함.'),
            ('STEP 03', '발주 RISK Factor 및 해징 전략 수립', '지장물 이설 지연, 용지 미보상, 기후 위험 요소를 추출하고 예비비를 수립함.'),
            ('STEP 04', '발주전략 KOM 미팅 및 서면 승인', '발주처, 감리단 및 궤도 시공팀 참석 킥오프 미팅을 개최하고 결재를 완료함.')
        ],
        'diagram_title': '📐 동탄트램 발주전략 Kick-Off Meeting 절차도',
        'diagram_nodes': [('1. 시방서/BIM 검토', '계약 요구조건 분석'), ('2. RISK 전략 수립', '지장물/용지 해징'), ('3. 감리 서면승인', 'KOM 킥오프 결재')]
    },
    {
        'row': 4,
        'wbs': '9000-7-3',
        'dir_name': '3_철도보호지구에서의 행위신고(필요시)',
        'file_prefix': '철도보호지구에서의 행위신고(필요시)',
        'title': '철도보호지구 행위신고',
        'std_legal': '철도안전법 제45조 & 시행령 제44조',
        'desc': '본 수행지침서는 동탄트램 궤도 인접 공사의 법정 인허가 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 궤도 중심 30m 경계 측량</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 철도안전법 제45조 신고서 수속</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 철도운영기관 기술 협의</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">운행선안전관리자 현장 1:1 배치</span>의 법정 인허가 절차를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '철도보호지구 30m 경계 측량', '궤도 중심선으로부터 30m 이내 철도보호지구 경계선을 광학 토탈스테이션으로 실측함.'),
            ('STEP 02', '행위신고서 & 안전관리계획서 작성', '굴착 깊이, 장비 동선, 붕괴 방지 가설재 계획이 수록된 신고 서류를 수속함.'),
            ('STEP 03', '철도운영기관(철도공단) 현장 접수', '관할 철도 운영기관에 행위신고서를 제출하고 기술 검토 승인을 필함.'),
            ('STEP 04', '운행선안전관리자 현장 배치', '철도 안전교육을 이수한 전담 안전관리자를 현장 1:1 배치하여 착공 승인을 받음.')
        ],
        'diagram_title': '🚆 동탄트램 철도보호지구(30m) 행위신고 및 승인 절차도',
        'diagram_nodes': [('1. 30m 경계 측량', '철도보호지구 확인'), ('2. 신고서/계획서 접수', '철도운영기관 협의'), ('3. 감리 서면승인', '운행선 안전관리자 배치')]
    },
    {
        'row': 5,
        'wbs': '9000-7-4',
        'dir_name': '4_착수전 측량 Data 확인',
        'file_prefix': '착수전 측량 Data 확인',
        'title': '착수전 측량 Data 확인',
        'std_legal': '공공측량 작업규정 & KCS 47 10 25 측량 지침',
        'desc': '본 수행지침서는 동탄트램 노반 시공 정밀 기준점 확립 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 국가 CP/TBM 기준점 인수</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 GRS80 세계측지계 수준측량(오차 ≤ 5mm√K)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 현장 인조점 3개소 매설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3D BIM 좌표 매핑 승인</span>의 정밀 측량 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '기준점(CP) 및 삼각점 데이터 인수', '발주처 제공 국가 기준점(CP) 및 TBM 성적표를 인수하여 좌표계를 정밀 점검함.'),
            ('STEP 02', 'GRS80 세계측지계 레벨 현측', '광학 레벨기를 동원하여 왕복 왕복 수준측량(폐합오차 ≤ 5mm√K)을 시행함.'),
            ('STEP 03', '현장 인조점(TBM) 3개소 매설', '공사 영향권 밖 안전 구역에 콘크리트 인조점 3개소를 설치하고 보호 펜스를 침.'),
            ('STEP 04', '측량 성과표 작성 & 3D BIM 승인', '측량 야장을 도면과 1:1 비교 검증하여 책임감리원 최종 서면 승인을 완수함.')
        ],
        'diagram_title': '📐 동탄트램 GRS80 기준점 측량 및 레벨 검측 절차도',
        'diagram_nodes': [('1. CP/TBM 데이터 인수', '세계측지계 좌표 확인'), ('2. 수준측량/인조점', '폐합오차 ≤ 5mm√K'), ('3. 감리 서면승인', '측량 성과표 최종 결재')]
    },
    {
        'row': 6,
        'wbs': '9000-7-5',
        'dir_name': '5_지장물이설 협의',
        'file_prefix': '지장물이설 협의',
        'title': '지장물이설 협의',
        'std_legal': '지하안전관리에 관한 특별법 제23조',
        'desc': '본 수행지침서는 동탄트램 지하 안전 사전 확보 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 GPR 지중 레이더 탐사</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 인력 시탐 줄파기(1.5m)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 점용기관 1:1 현장 입회 매달기 방호</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3D BIM 위치 매핑 완료</span>의 지하 안전 방호 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', 'GPR 지중 매설물 탐사 & 매핑', 'GPR(지중탐사레이더) 장비로 관로(상하수도, 가스, 전력) 3D 위치를 탐사함.'),
            ('STEP 02', '인력 시탐 줄파기(깊이 1.5m) 시행', '중장비 굴착 전 인력 줄파기(폭 0.5m, 깊이 1.5m)로 관급 매설물을 현출함.'),
            ('STEP 03', '관할 점용기관 1:1 현장 입회 협의', '한전, 도시가스, 수자원공사 담당자 입회하에 매달기 방호 및 이설 계획을 확정함.'),
            ('STEP 04', '지장물 이설 완료 승인 & BIM 반영', '이설 완료 후 3D BIM 모델링 좌표를 업데이트하고 감리 승인을 수령함.')
        ],
        'diagram_title': '🚧 동탄트램 GPR 탐사 및 지하 지장물 이설 협의 절차도',
        'diagram_nodes': [('1. GPR 탐사/줄파기', '지중 관로 위치 현출'), ('2. 점용기관 현장입회', '매달기/이설 계획 협의'), ('3. 감리 서면승인', '지장물 이설완료 결재')]
    },
    {
        'row': 7,
        'wbs': '9000-7-6',
        'dir_name': '6_용지보상RISK 검토',
        'file_prefix': '용지보상RISK 검토',
        'title': '용지보상RISK 검토',
        'std_legal': '공익사업을 위한 토지 등의 취득 및 보상에 관한 법률',
        'desc': '본 수행지침서는 동탄트램 공정 차질 방지 및 민원 통제 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 토지보상법 미보상 필지 추출</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 높이 1.8m 가설 펜스 격리 차단</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 3D 우회 토공 동선 수립</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">우회 마일스톤 서면 결재</span>의 리스크 방어 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '토지 수용 조서 & 미보상 필지 현출', '용지보상 경계선과 토공 작업구간을 지적도와 1:1 대조하여 미보상 사유지를 추출함.'),
            ('STEP 02', '미보상 사유지 경계 가설 펜스 차단', '분쟁 예방을 위해 미보상 사유지 경계에 높이 1.8m 가설 휀스를 설치하고 진입을 차단함.'),
            ('STEP 03', '우회 토공 작업 동선 & 마일스톤 연동', '보상 지연 구간을 우회하는 변경 작업 동선을 수립하여 마일스톤에 반영함.'),
            ('STEP 04', '용지 보상 리스크 대책 감리 서면 승인', '보상 현황도 및 우회 공정 계획서를 제출하여 책임감리원 최종 결재를 수령함.')
        ],
        'diagram_title': '🗺️ 동탄트램 용지 보상 경계 확인 및 우회 공정 수립 절차도',
        'diagram_nodes': [('1. 미보상 사유지 추출', '토지 수용 조서 대조'), ('2. 가설 펜스 격리 차단', 'H1.8m 휀스 설치'), ('3. 감리 서면승인', '우회 공정 계획서 결재')]
    },
    {
        'row': 8,
        'wbs': '9000-7-7',
        'dir_name': '7_최고의 팀 만들기 지원',
        'file_prefix': '최고의 팀 만들기 지원',
        'title': '최고의 팀 만들기 지원',
        'std_legal': '건설산업기본법 상생협력 규정 & 현장 조직 지침',
        'desc': '본 수행지침서는 동탄트램 현장 시공 역량 극대화 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 전문 기술자 1:1 전담 배치</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 발주·감리·시공 3자 주간 소통 회의</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 근로자 환경 개선 및 일일 Safety TBM</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">One-Team 전담 조직표 승인</span>의 협력 조직을 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '전문 기술자 & 근로자 전담 조직 구성', '토공, 측량, 품질 전담 기술 자격자를 1:1 배치하고 현장 조직표를 수립함.'),
            ('STEP 02', '발주처·감리·시공 3자 주간 소통 회의', '매주 1회 One-Team 합동 기술 회의를 개최하여 공정 장애 요소를 즉시 해소함.'),
            ('STEP 03', '근로자 환경 개선 & 일일 Safety TBM', '휴게실, 음수대 비치 및 일일 작업 전 안전 TBM으로 근로 사기를 제고함.'),
            ('STEP 04', 'One-Team 전담 조직표 서면 결재', '조직도 및 협력 체계 승인 요청서를 제출하여 책임감리원 직인을 수령함.')
        ],
        'diagram_title': '🤝 동탄트램 발주처·감리·시공 One-Team 조직 체계 절차도',
        'diagram_nodes': [('1. 전담 조직표 수립', '전문 기술자 1:1 배치'), ('2. 주간 3자 소통 회의', '공정 장애 요소 해소'), ('3. 감리 서면승인', 'One-Team 결재 완수')]
    },
    {
        'row': 9,
        'wbs': '9000-7-8',
        'dir_name': '8_시공계획서 수립 승인',
        'file_prefix': '시공계획서 수립 승인',
        'title': '시공계획서 수립 승인',
        'std_legal': '건설기술진흥법 시행령 제89조',
        'desc': '본 수행지침서는 동탄트램 상부강화노반 시공 마스터 플로우 확립 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 건진법 제89조 8대 목차 작성</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 KCS 47 10 25 다짐 수치 명시</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 착공 14일 전 감리 접수 및 보완</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">책임감리원 최종 서면 승인</span>의 종합계획 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '시공계획서 표준 8대 목차 작성', '공정표, 장비 조합, 품질/안전/환경 관리계획이 수록된 계획서 본안을 작성함.'),
            ('STEP 02', 'KCS 47 10 25 품질 수치 수록', '다짐도 ≥95%, K30 ≥110, Ev2 ≥60 MPa 및 50m 시험다짐 계획을 명시함.'),
            ('STEP 03', '공사 착수 14일 전 감리단 공식 제출', '책임감리단에 공문 접수 후 기술 검토 의견서에 대한 보완 조치를 이행함.'),
            ('STEP 04', '책임감리원 최종 서면 승인 수령', '보완 완료된 시공계획서 최종본에 책임감리원 결재를 득하여 착공함.')
        ],
        'diagram_title': '📋 동탄트램 상부강화노반 시공계획서 수립 및 감리 승인 절차도',
        'diagram_nodes': [('1. 시공계획서 본안 작성', 'KCS 47 10 25 수치 명시'), ('2. 감리단 기술검토 제출', '착공 14일 전 접수'), ('3. 감리 서면승인', '시공계획서 최종 결재')]
    },
    {
        'row': 10,
        'wbs': '9000-7-9',
        'dir_name': '8_작업조 편성',
        'file_prefix': '작업조 편성',
        'tag': '작업조 편성',
        'title': '작업조 편성',
        'std_legal': '건설기술진흥법 & 건설근로자법 조직 수칙',
        'desc': '본 수행지침서는 동탄트램 정밀 시공 인력 검증 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 공종별 전담 기술 수첩 검증</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 건설기계 조종원 면허 1:1 대조</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 일일 음주 측정 및 Safety TBM</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">작업조 조직표 서면 승인</span>의 투입 인력 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '전담 작업조 및 면허 자격 검증', '토공 롤러 조종원, 모터그레이더 기사 및 측량 기술자 자격 수첩을 점검함.'),
            ('STEP 02', '건설기계 조종원 면허 1:1 현장 대조', '장비 반입 전 조종원 면허증 및 신원 확인을 마치고 작업에 투입함.'),
            ('STEP 03', '일일 작업 전 음주 측정 & Safety TBM', '매일 아침 음주 측정 및 작업별 위험성 평가 TBM을 정밀 실시함.'),
            ('STEP 04', '작업조 편성표 감리 서면 승인', '작업조 비상연락망 및 현장 조직표를 작성하여 책임감리원 결재를 필함.')
        ],
        'diagram_title': '👷 동탄트램 강화노반 작업조 편성 및 자격 검증 절차도',
        'diagram_nodes': [('1. 자격수첩/면허 검증', '조종원 1:1 신원 대조'), ('2. 일일 TBM/음주측정', '작업 위험성 평가'), ('3. 감리 서면승인', '작업조 조직표 결재')]
    },
    {
        'row': 11,
        'wbs': '9000-7-10',
        'dir_name': '9_장비 수급 계획',
        'file_prefix': '장비 수급 계획',
        'title': '장비 수급 계획',
        'std_legal': '건설기계관리법 제13조 정기검사 규정',
        'desc': '본 수행지침서는 동탄트램 최첨단 건설기계 투입 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 자중 10ton+ 강동 진동 롤러 선정</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 3D GPS 제어 모터그레이더 조합</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 반입 정기검사 및 후방 센서 테스트</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">장비 반입 서면 결재</span>의 스마트 장비 조합을 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '강화노반 전용 다짐/포설 장비 선정', '10t+ 강동 롤러, 15t+ 타이어 롤러 및 3D GPS 모터그레이더 사양을 확정함.'),
            ('STEP 02', '건설기계 정기검사증 & 등록증 검수', '현장 반입 전 건설기계 검사 유효 기간 및 보험 가입 여부를 100% 점검함.'),
            ('STEP 03', '장비 센서 교정 & 반입 시동 점검', '3D GPS 수신기 및 후방 카메라, 후진 경보음 가동 상태를 테스트함.'),
            ('STEP 04', '건설장비 반입 승인서 감리 결재', '장비 점검표를 부착하여 책임감리원 반입 허가 결재를 완료함.')
        ],
        'diagram_title': '🚜 동탄트램 건설장비(롤러·그레이더) 반입 검수 절차도',
        'diagram_nodes': [('1. 장비 사양 확정', '10t+ 강동/타이어 롤러'), ('2. 정기검사/센서 점검', '3D GPS/후방카메라'), ('3. 감리 서면승인', '장비 반입 허가 결재')]
    },
    {
        'row': 12,
        'wbs': '9000-7-11',
        'dir_name': '10_노반 재료 입도 DB 확보',
        'file_prefix': '노반 재료 입도 DB 확보',
        'title': '노반 재료 입도 DB 확보',
        'std_legal': 'KCS 47 10 25 강화노반 쇄석 입도 규정',
        'desc': '본 수행지침서는 동탄트램 쇄석 골재 고품질 확보 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 골재 최대입경 50mm 이하 규격 검수</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 #200체 통과량 5% 이하 제어</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 수정다짐 CBR 30% 이상 실측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">골재 입도 곡선 DB 전산 등록</span>의 재료 품질 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '골재 석산 공급원 사전 승인 수속', 'KS F 2527 쇄석 골재 석산 허가증 및 공인 기관 시험성적서를 제출함.'),
            ('STEP 02', '1,000m³당 1회 현장 체가름 시험', '반입 쇄석 최대입경(50mm 이하) 및 #200체 통과량(5% 이하)을 검측함.'),
            ('STEP 03', '수정다짐 CBR(≥30%) & 마모율 시험', 'KS F 2320 수정다짐 CBR 30% 이상 및 마모율 40% 이내 성적을 산출함.'),
            ('STEP 04', '노반 재료 입도 DB 확정 감리 승인', '골재 입도 곡선 DB를 시스템에 등록하고 책임감리원 승인을 수령함.')
        ],
        'diagram_title': '📊 동탄트램 강화노반 쇄석 골재 입도 DB 구축 절차도',
        'diagram_nodes': [('1. 석산 공급원 승인', 'KS F 2527 성적서'), ('2. 체가름/CBR 시험', '50mm 이하/CBR ≥30%'), ('3. 감리 서면승인', '골재 입도 DB 결재')]
    },
    {
        'row': 13,
        'wbs': '9000-7-12',
        'dir_name': '11_사토장 _ 토사 수급 계획 확인',
        'file_prefix': '사토장 _ 토사 수급 계획 확인',
        'title': '사토장 / 토사 수급 계획 확인',
        'std_legal': '토양환경보전법 & 국토계획법 사토 수수 규정',
        'desc': '본 수행지침서는 동탄트램 사토 환경 안전 처리 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 화성시 정식 사토장 인허가 검증</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 토사 최대건조밀도 γd max ≥ 1.90g/cm³</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 토양오염 8개 항목 검사</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">사토 수불 대장 일일 결재</span>의 사토 환경 관리를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '정식 인허가 사토장 위치 & 서류 검증', '화성시 개발행위 허가증 및 사토 처리 수량 체결 서류를 정밀 점검함.'),
            ('STEP 02', '토사 물리적 특성 & 오염도 시험', '최대건조밀도 γd max ≥ 1.90g/cm³ 및 토양오염 8개 항목 불검출을 검증함.'),
            ('STEP 03', '일일 토사 덤프 반출 수불 대장 관리', '덤프트럭 운행 송장(Manifest)을 작성하고 사토량을 일일 집계함.'),
            ('STEP 04', '토사 수급 및 사토 계획 감리 승인', '사토장 처리 계획서를 제출하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '🚚 동탄트램 사토장 인허가 및 토사 수급 검증 절차도',
        'diagram_nodes': [('1. 사토장 인허가 검증', '개발행위 허가증 확인'), ('2. 밀도/오염도 시험', 'γd max ≥ 1.90g/cm³'), ('3. 감리 서면승인', '사토 계획서 결재')]
    },
    {
        'row': 14,
        'wbs': '9000-7-13',
        'dir_name': '12_배수 처리 계획 수립',
        'file_prefix': '배수 처리 계획 수립',
        'title': '배수 처리 계획 수립',
        'std_legal': 'KCS 47 10 25 임시 배수 시설 설치 시방',
        'desc': '본 수행지침서는 동탄트램 노반 침수 및 유실 방지 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 성토 사면 가배수로(0.6×0.6m) 설치</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 가침사지 2개소 설계</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 HDPE 유공관(Ø200mm, 구배 ≥0.5%) 부설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">임시 배수 계획 감리 승인</span>의 수해 방지 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '성토 가배수로 & 가침사지 용량 설계', '우천 시 노반 세굴 방지를 위한 가배수로(0.6×0.6m) 및 가침사지 2개소를 설계함.'),
            ('STEP 02', '맹암거 HDPE 유공관 자재 검수', 'HDPE 유공관(Ø200mm) 천공 및 투수성 부직포(200g/m²) 품질을 확인함.'),
            ('STEP 03', '수중 양수 펌프(200L/min) 수급 비치', '집수정 비상 배수를 위한 비상 양수 펌프 및 전원선 배치를 하였는가?'),
            ('STEP 04', '임시 배수 처리 계획서 감리 승인', '배수 계통도를 첨부하여 책임감리원 최종 서면 결재를 수령함.')
        ],
        'diagram_title': '🌊 동탄트램 성토 가배수로 및 임시 침사지 배수 절차도',
        'diagram_nodes': [('1. 가배수로/침사지 설계', '0.6×0.6m/가침사지 2개소'), ('2. 유공관/부직포 검수', 'HDPE Ø200mm/200g/m²'), ('3. 감리 서면승인', '배수 계획서 결재')]
    },
    {
        'row': 15,
        'wbs': '9000-7-14',
        'dir_name': '13_안전관리계획 수립 승인',
        'file_prefix': '안전관리계획 수립 승인',
        'title': '안전관리계획 수립 승인',
        'std_legal': '건설기술진흥법 제62조 & 시행령 제98조',
        'desc': '본 수행지침서는 동탄트램 중대재해 제로 달성 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 건진법 제62조 안전관리계획서 작성</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 국토안전관리원 정밀 심사(적정)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 CSI 건설공사 안전관리종합망 전산 등록</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">안전계획서 감리 승인</span>의 재해 예방 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '건진법 제62조 안전관리계획서 작성', '지하시설물 굴착, 장비 붕괴 예방 및 통행 안전이 수록된 계획서를 작성함.'),
            ('STEP 02', '국토안전관리원 전산 적정성 심사', '국토안전관리원 심사 시스템에 제출하여 "적정" 판정을 수검함.'),
            ('STEP 03', 'CSI 건설공사 안전관리 종합망 등록', '전산망에 등록번호를 부여받고 현장 비상연락망을 세팅함.'),
            ('STEP 04', '책임감리원 안전관리계획 서면 승인', '심사 적정 통지서를 부착하여 책임감리원 최종 서면 승인을 완료함.')
        ],
        'diagram_title': '🛡️ 동탄트램 안전관리계획 수립 및 CSI 전산 등록 절차도',
        'diagram_nodes': [('1. 안전관리계획서 작성', '건진법 제62조 수칙'), ('2. 국토안전관리원 심사', 'CSI 종합망 전산 등록'), ('3. 감리 서면승인', '안전계획서 최종 결재')]
    },
    {
        'row': 16,
        'wbs': '9000-7-15',
        'dir_name': '14_품질관리계획 수립 승인',
        'file_prefix': '품질관리계획 수립 승인',
        'title': '품질관리계획 수립 승인',
        'std_legal': '건설기술진흥법 제55조 & 시행규칙 제50조',
        'desc': '본 수행지침서는 동탄트램 노반 공학적 강도 검증 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 다짐도(500m³당 1회) 시험 수립</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 K30(2,000m²당 1회) 평판재하 계획</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 Ev2(1,000m²당 1회) 동적변형계수 설정</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">품질관리계획 서면 결재</span>의 무결점 품질 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', 'KCS 47 10 25 품질 시험 빈도 수립', '다짐도(500m³당 1회), K30(2,000m²당 1회), Ev2(1,000m²당 1회) 계획을 수립함.'),
            ('STEP 02', '현장 시험실 & 시험 장비 교정 검수', '들밀도 시험기, 평판재하기 교정성적서 유효 기간을 점검함.'),
            ('STEP 03', '품질관리계획서 공사 착수 14일 전 제출', '책임감리단에 공식 접수 후 시험 요원 자격 상태를 검증받음.'),
            ('STEP 04', '책임감리원 품질관리계획 서면 승인', '감리단 검토 승인 공문을 수령하고 현장 시험 대장을 개설함.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 품질시험 계획 수립 및 교정 절차도',
        'diagram_nodes': [('1. 시험 빈도 수립', 'KCS 47 10 25 수칙'), ('2. 시험 장비 교정', '들밀도/K30 장비 검수'), ('3. 감리 서면승인', '품질계획서 최종 결재')]
    },
    {
        'row': 17,
        'wbs': '9000-7-16',
        'dir_name': '15_환경관리계획 수립 승인',
        'file_prefix': '환경관리계획 수립 승인',
        'title': '환경관리계획 수립 승인',
        'std_legal': '대기환경보전법 제44조 & 소음진동관리법',
        'desc': '본 수행지침서는 동탄트램 친환경 현장 조성 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 비산먼지 발생사업 신고</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 이동식 세륜기(깊이 1.2m) 가동</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 가설 방음벽(3m, 65dB 이하) 부설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">환경관리계획 감리 서면 승인</span>의 친환경 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '비산먼지 & 소음진동 관리 시설 설계', '이동식 자동 세륜기(깊이 1.2m) 및 가설 방음벽(3m)을 설계함.'),
            ('STEP 02', '지자체(화성시) 환경 발생사업 신고', '비산먼지 발생사업 및 특정공사 사전신고 증명서를 수령함.'),
            ('STEP 03', '살수차(5,000L) & 환경 측정기 배치', '현장 출입구 세륜기 설치 및 1일 3회 분무 살수를 시행함.'),
            ('STEP 04', '환경관리계획서 감리 서면 승인', '신고 필증을 부착하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '🌱 동탄트램 비산먼지·소음 환경관리 및 세륜기 가동 절차도',
        'diagram_nodes': [('1. 세륜기/방음벽 설계', '깊이 1.2m/H3m 방음벽'), ('2. 지자체 사전신고', '화성시 비산먼지 신고'), ('3. 감리 서면승인', '환경계획서 최종 결재')]
    },
    {
        'row': 18,
        'wbs': '9000-7-17',
        'dir_name': '16_교통소통 대책 수립 승인(필요시)',
        'file_prefix': '교통소통 대책 수립 승인(필요시)',
        'title': '교통소통 대책 수립 승인',
        'std_legal': '도로교통법 제69조 & 도로법 점용 규정',
        'desc': '본 수행지침서는 동탄트램 도심지 시민 원활 통행 확보 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 동탄경찰서 교통안전 심의</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 도로점용 허가증 수령</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 전담 안전 신호수(2인 2조) 및 LED 경광등 배치</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">교통소통 대책 감리 승인</span>의 원활한 교통 흐름을 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '교통 우회 처리 도면 & 신호 체계 설계', '덤프트럭 출입을 위한 가설 둔차선 및 교통 안전 표지판 배치를 도면화함.'),
            ('STEP 02', '동탄경찰서 교통안전 심의 & 점용 허가', '경찰서 관할 도로점용 허가증을 수령하고 안전 시설을 설치함.'),
            ('STEP 03', '전담 신호수(2인 2조) & 경광등 배치', '신호수 자격 이수자를 게이트에 배치하고 야간 LED 경광등을 점등함.'),
            ('STEP 04', '교통소통 대책 계획서 감리 승인', '경찰서 협의서를 부착하여 책임감리원 서면 결재를 수령함.')
        ],
        'diagram_title': '🚦 동탄트램 교통우회 처리 및 도로점용 승인 절차도',
        'diagram_nodes': [('1. 교통 우회 도면 설계', '가설 차선/표지판 배치'), ('2. 동탄경찰서 심의', '도로점용 허가증 수령'), ('3. 감리 서면승인', '교통대책서 최종 결재')]
    },
    {
        'row': 19,
        'wbs': '9000-7-18',
        'dir_name': '17_하도급 검토 승인',
        'file_prefix': '하도급 검토 승인',
        'title': '하도급 검토 승인',
        'std_legal': '건설산업기본법 제29조 & 시행령 제31조',
        'desc': '본 수행지침서는 동탄트램 공정 투명성 및 하도급 상생 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 토공 전문건설업 면허 검증</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 하도급율 82% 이상 적정성 심사</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 건설근로자 노무비 전용계좌 지정</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">하도급 계약 감리 서면 승인</span>의 투명 집행 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '하도급 업체 면허 & 시공 능력 검증', '토공 전문건설업 면허, 시공실적증명서 및 신용평가서를 심사함.'),
            ('STEP 02', '하도급 적정성 심사표 작성(82%+)', '하도급 계약 금액 비율(82% 이상)을 확인하고 내역서를 대조함.'),
            ('STEP 03', '노무비 지급 전용계좌 지정 체결', '건설근로자 노무비 체불 방지 전용 계좌를 개설하고 합의함.'),
            ('STEP 04', '하도급 계약 승인 통보서 감리 결재', '하도급 통지서를 제출하여 책임감리원 최종 서면 승인을 완수함.')
        ],
        'diagram_title': '🏢 동탄트램 하도급 계약 적정성 심사 및 승인 절차도',
        'diagram_nodes': [('1. 전문 면허/실적 검증', '토공 면허/신용평가'), ('2. 적정성 심사(82%+)', '노무비 전용계좌 지정'), ('3. 감리 서면승인', '하도급 계약 최종 결재')]
    },
    {
        'row': 20,
        'wbs': '9000-7-19',
        'dir_name': '18_자재승인',
        'file_prefix': '자재승인',
        'title': '자재승인',
        'std_legal': 'KCS 47 10 25 자재 승인 및 검수 규정',
        'desc': '본 수행지침서는 동탄트램 자재 품질 신뢰성 검증 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 KS F 2527 쇄석골재 공급원 확인</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 HDPE 유공관 및 부직포(200g/m²) 시험</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 공인 기관 시험성적서 부착</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">자재 승인 통보서 감리 결재</span>의 적합 자재 검수를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '자재 공급원 자격 서류 검토', 'KS F 2527 골재, HDPE 유공관, 투수성 부직포 사업자등록증 및 공장등록증을 확인함.'),
            ('STEP 02', '공인시험기관 시료 시험성적서 부착', '국민공인시험원에 시험을 의뢰하여 물리적/화학적 성적표를 수령함.'),
            ('STEP 03', '자재 승인 신청서 제출 & 감리 심사', '자재 샘플 및 성적표를 묶어 책임감리단에 자재 승인을 신청함.'),
            ('STEP 04', '자재 반입 현장 검수 및 승인 결재', '책임감리원 직인이 날인된 자재 승인 통보서를 득하여 반입을 허용함.')
        ],
        'diagram_title': '📦 동탄트램 노반 쇄석 및 배수 자재 승인 절차도',
        'diagram_nodes': [('1. 공급원 자격 검토', 'KS F 2527 공장등록증'), ('2. 공인기관 시험성적', '물리/화학적 성적표'), ('3. 감리 서면승인', '자재 승인 통보서 결재')]
    },
    {
        'row': 21,
        'wbs': '9000-7-20',
        'dir_name': '19_시험다짐',
        'file_prefix': '시험다짐',
        'title': '시험다짐',
        'std_legal': 'KCS 47 10 25 시험 다짐 현장 규정',
        'desc': '본 수행지침서는 동탄트램 최적 다짐 공법 도출 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 50m 현장 시험구간 포설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 쇄석 30cm 부설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 다짐 패스별 침하량(Δh ≤ 1mm) 실측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">강동 롤러 4~6회 다짐 횟수 승인</span>의 시험 시공 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '50m 현장 시험 다짐 구간 선정', '상부강화노반 시공 현장에 길이 50m, 너비 6m 시험 구간을 지정함.'),
            ('STEP 02', '골재 쇄석 30cm 층두께 부설', '모터그레이더로 승인된 쇄석 골재를 30cm 두께로 고르게 포설함.'),
            ('STEP 03', '다짐 횟수별(2,4,6,8회) 침하량 측정', '롤러 패스 수별 광학 레벨로 침하량을 실측하여 침하 정지(Δh≤1mm)를 확인함.'),
            ('STEP 04', '시험다짐 결과 보고서 감리 승인', '다짐 횟수(강동 4회, 타이어 2회)를 확정하여 책임감리원 결재를 완료함.')
        ],
        'diagram_title': '🚜 동탄트램 50m 현장 시험다짐 및 다짐 횟수 확정 절차도',
        'diagram_nodes': [('1. 50m 시험구간 포설', '쇄석 골재 30cm 부설'), ('2. 패스별 침하량 실측', '침하 정지 Δh ≤ 1mm'), ('3. 감리 서면승인', '시험다짐 보고서 결재')]
    },
    {
        'row': 22,
        'wbs': '9000-7-21',
        'dir_name': '20_원지반 검측',
        'file_prefix': '원지반 검측',
        'tag': '원지반 검측',
        'title': '원지반 검측',
        'std_legal': 'KCS 47 10 25 원지반 지비력 및 표고 규정',
        'desc': '본 수행지침서는 동탄트램 노반 최하단 정기반 확보 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 유기질 표토(15~30cm) 제거 및 전압</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 광학 레벨 표고 오차 ±30mm 측정</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 원지반 K30 ≥ 70 MN/m³ 평판재하 및 덤프 펌핑 점검</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">원지반 검측서 감리 결재</span>의 지기반 확립을 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '표토 제거 & 원지반 정전압 다짐', '유기질토(15~30cm) 제거 후 롤러 2회 정전압 사전 다짐을 시행함.'),
            ('STEP 02', '원지반 표고 & 종횡단 측량', '광학 토탈스테이션으로 원지반 중심선 레벨(오차 ±30mm)을 측량함.'),
            ('STEP 03', 'K30 평판재하시험 & 펌핑 점검', '원지반 K30(≥70 MN/m³) 시험 3개소 및 덤프트럭 펌핑 연약 지반을 검측함.'),
            ('STEP 04', '원지반 검측 성과표 감리 승인', '검측 요청서를 제출하여 책임감리원 공학적 입회 결재를 수검함.')
        ],
        'diagram_title': '📐 동탄트램 원지반 지비력 및 표고 검측 절차도',
        'diagram_nodes': [('1. 표토제거/다짐', '유기질토 15~30cm 제거'), ('2. 표고/K30 검측', 'K30 ≥70 MN/m³ 시험'), ('3. 감리 서면승인', '원지반 검측서 결재')]
    },
    {
        'row': 23,
        'wbs': '9000-7-22',
        'dir_name': '21_하부노반 검측',
        'file_prefix': '하부노반 검측',
        'title': '하부노반 검측',
        'std_legal': 'KCS 47 10 25 하부노반 다짐 및 밀도 규정',
        'desc': '본 수행지침서는 동탄트램 토공 하부 층다짐 완수 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 층두께 30cm 이하 포설 다짐</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 들밀도 다짐도 ≥ 90% (KS F 2311)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 K30 ≥ 90 MN/m³ 및 Ev2 ≥ 45 MPa 강도 검측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">하부노반 검측 승인</span>의 층다짐 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '하부노반 30cm 층포설 & 다짐', '성토 토사를 30cm 두께로 포설하고 10톤 강동 롤러 4회 이상 다짐을 시행함.'),
            ('STEP 02', '들밀도 & K30 평판재하시험', 'KS F 2311 들밀도 시험(다짐도 ≥90%) 및 K30(≥90 MN/m³) 3개소를 검측함.'),
            ('STEP 03', '하부노반 마무리면 레벨 측량', '광학 레벨기로 하부노반 마무리면 표고 오차(±20mm 이내)를 검측함.'),
            ('STEP 04', '하부노반 검측 서면 승인 수령', '검측 결과표를 작성하여 책임감리원 서면 결재를 완료함.')
        ],
        'diagram_title': '🚜 동탄트램 하부노반 층다짐 및 밀도 검측 절차도',
        'diagram_nodes': [('1. 30cm 층포설/다짐', '강동 롤러 4회 다짐'), ('2. 들밀도/K30 검측', '다짐도 90%/K30 90'), ('3. 감리 서면승인', '하부노반 검측서 결재')]
    },
    {
        'row': 24,
        'wbs': '9000-7-23',
        'dir_name': '22_상부노반 시공(배수 유공관 포함)',
        'file_prefix': '상부노반 시공(배수 유공관 포함)',
        'title': '상부노반 시공',
        'std_legal': 'KCS 47 10 25 상부노반 및 맹암거 유공관 규정',
        'desc': '본 수행지침서는 동탄트램 내부 침투수 완전 배수 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 상부노반 토사 30cm 포설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 맹암거 부직포(200g/m²) 및 HDPE 유공관(Ø200mm) 천공 상향 시공</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 배수 구배 ≥ 0.5% 및 소형 램머 다짐</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">상부노반 매몰 검측 승인</span>의 배수 노반 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '상부노반 토사 30cm 포설', '모터그레이더로 토사를 30cm 두께로 포설하고 평탄 롤링 다짐을 시행함.'),
            ('STEP 02', '맹암거 터파기 & 부직포 부설', '맹암거 트렌치 터파기 후 투수성 부직포(200g/m²)를 트렌치 바닥에 깔아 챔버 형성함.'),
            ('STEP 03', 'HDPE 유공관(Ø200mm) 부설', '종단 구배 0.5% 이상으로 유공관을 연결 부설하고 필터 쇄석(19~25mm)을 채움.'),
            ('STEP 04', '상부노반 배수 시공 감리 승인', '맹암거 유공관 및 상부노반 성과표를 작성하여 책임감리원 결재를 완수함.')
        ],
        'diagram_title': '🛠️ 동탄트램 상부노반 및 맹암거 유공관 배수 시공 절차도',
        'diagram_nodes': [('1. 30cm 토사포설', '상부노반 층포설'), ('2. 맹암거 유공관부설', 'HDPE Ø200mm/부직포'), ('3. 감리 서면승인', '상부노반 시공 결재')]
    },
    {
        'row': 25,
        'wbs': '9000-7-24',
        'dir_name': '23_상부강화노반 시공',
        'file_prefix': '상부강화노반 시공',
        'title': '상부강화노반 시공',
        'std_legal': 'KCS 47 10 25 강화노반 쇄석 시방 규정',
        'desc': '본 수행지침서는 동탄트램 상부강화노반 전체 공정의 핵심 시공 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 3D GPS 쇄석 50mm 포설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 최적함수비 OMC 살수</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 강동 4회/타이어 2회 조합 다짐</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">마무리면 표고 오차 ±10mm 통제</span>의 강화노반 다짐 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '3D GPS 모터그레이더 쇄석 포설', '최대입경 50mm 쇄석 골재를 30cm 두께로 3D GPS 자동 제어 포설함.'),
            ('STEP 02', '살수차 최적함수비(OMC) 분무 살수', '골재 재료 분리 방지 및 다짐 효율 증대를 위한 OMC 살수를 시행함.'),
            ('STEP 03', '강동 롤러 & 타이어 롤러 조합 다짐', '시험다짐에서 확정된 롤러 조합(강동 4회 + 타이어 2회) 다짐을 정밀 이행함.'),
            ('STEP 04', '강화노반 마무리면 측량 & 감리 승인', '표고 오차 ±10mm 이내 검측 성과표를 작성하여 책임감리원 승인을 결재받음.')
        ],
        'diagram_title': '🚜 동탄트램 상부강화노반 쇄석 포설 및 롤러 다짐 절차도',
        'diagram_nodes': [('1. 3D GPS 쇄석포설', '50mm 쇄석 30cm 포설'), ('2. OMC 살수/롤러다짐', '강동4회+타이어2회 다짐'), ('3. 감리 서면승인', '강화노반 시공 결재')]
    },
    {
        'row': 26,
        'wbs': '9000-7-25',
        'dir_name': '24_다짐 검측',
        'file_prefix': '다짐 검측',
        'title': '다짐 검측',
        'std_legal': 'KCS 47 10 25 강화노반 공학 다짐 수칙',
        'desc': '본 수행지침서는 동탄트램 강화노반 공학적 품질 완증 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 현장 들밀도 시험(다짐도 ≥ 95%)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 평판재하시험 K30 ≥ 110 MN/m³</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 변형계수 Ev2 ≥ 60 MPa (Ev2/Ev1 ≤ 2.2)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">다짐 검측 3대 수치 감리 서면 승인</span>의 다짐 밀집 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '현장 들밀도 시험(KS F 2311)', '500m³당 1회 들밀도 시험을 시행하여 다짐도 ≥95%를 실측 검측함.'),
            ('STEP 02', 'K30 평판재하시험(KS F 2310)', '2,000m²당 1회 K30 지반반발자승(≥110 MN/m³)을 평판재하 시험 의뢰함.'),
            ('STEP 03', '동적 변형계수 Ev2 시험', '1,000m²당 1회 Ev2(≥60 MPa) 및 Ev2/Ev1(≤2.2) 변형 계수 침하를 측정함.'),
            ('STEP 04', '다짐 검측 종합 보고서 감리 승인', '3대 공학 수치 합격 성적표를 작성하여 책임감리원 최종 서면 승인을 완수함.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 다짐도, K30 및 Ev2 공학 검측 절차도',
        'diagram_nodes': [('1. 들밀도 시험', '다짐도 ≥95% 실측'), ('2. K30 & Ev2 시험', 'K30≥110, Ev2≥60MPa'), ('3. 감리 서면승인', '다짐 검측서 최종 결재')]
    },
    {
        'row': 27,
        'wbs': '9000-7-26',
        'dir_name': '25_평판재하시험',
        'file_prefix': '평판재하시험',
        'title': '평판재하시험',
        'std_legal': 'KS F 2310 & KCS 47 10 25 지반반발자승 규정',
        'desc': '본 수행지침서는 동탄트램 지반 지비력 정밀 측정 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 Ø300mm 재하판 산모래 평탄 밀착</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 15t 유압 잭 하중 재하 및 침하 게이지 세팅</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 1.25mm 침하 하중 P-S 곡선 산출</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">K30 ≥ 110 MN/m³ 성적표 승인</span>의 지비력 평가 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '재하판 하부 평탄성 및 산모래 부설', 'Ø300mm 재하판 하부에 산모래를 부설하고 평탄 밀착 상태를 검측함.'),
            ('STEP 02', '유압 잭 & 침하 게이지 정밀 교정', '15t 유압 잭 및 0.01mm 정밀도 다이얼 게이지 2개를 반사침 세팅함.'),
            ('STEP 03', '단계별 재하 하중 및 침하량(1.25mm) 측정', '하중 단계별 P-S 하중-침하 곡선을 도출하여 K30 값을 산출함.'),
            ('STEP 04', 'K30 시험 성적표 감리 서면 승인', 'K30 ≥110 MN/m³ 합격 성적서를 부착하여 책임감리원 결재를 완수함.')
        ],
        'diagram_title': '📊 동탄트램 강화노반 K30 평판재하시험 및 지비력 측정 절차도',
        'diagram_nodes': [('1. Ø300mm 재하판 설치', '산모래 부설/밀착'), ('2. 유압잭 재하하중', 'P-S 하중침하곡선'), ('3. 감리 서면승인', 'K30 ≥110 성적서 결재')]
    },
    {
        'row': 28,
        'wbs': '9000-7-27',
        'dir_name': '26_강성 검측(K30, EV2)',
        'file_prefix': '강성 검측(K30, EV2)',
        'title': '강성 검측(K30, EV2)',
        'std_legal': 'DIN 18134 & KCS 47 10 25 변형계수 규정',
        'desc': '본 수행지침서는 동탄트램 탄성 복원력 검증 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 DIN 18134 동적 LWD 장비 교정</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 1,000m²당 무작위 포인트 1차/2차 재하</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 2차 변형계수 Ev2 ≥ 60 MPa 실측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">변형계수 비율 Ev2/Ev1 ≤ 2.2 감리 승인</span>의 탄성 강성 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '동적 평판재하시험기(LWD) 교정', 'LWD 가속도 센서 및 전자식 강성 측정기를 정밀 교정함.'),
            ('STEP 02', '1,000m²당 1회 무작위 포인트 선정', '강화노반 1,000m²마다 시험 지점 3개소를 무작위 지정함.'),
            ('STEP 03', '1차/2차 하중 재하 & Ev2/Ev1 산출', '1차(Ev1) 및 2차(Ev2) 하중 충격을 가해 변형 계수 비율을 도출함.'),
            ('STEP 04', '강성 검측 종합 보고서 감리 승인', 'Ev2 ≥60 MPa 성적표를 작성하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 동적 변형계수 Ev2 및 Ev2/Ev1 강성 검측 절차도',
        'diagram_nodes': [('1. LWD 장비 교정', '가속도 센서 세팅'), ('2. Ev1/Ev2 재하', 'Ev2 ≥60, Ev2/Ev1≤2.2'), ('3. 감리 서면승인', '강성 검측서 결재')]
    },
    {
        'row': 29,
        'wbs': '9000-7-28',
        'dir_name': '27_평탄성 검측',
        'file_prefix': '평탄성 검측',
        'title': '평탄성 검측',
        'std_legal': 'KCS 47 10 25 3m 직선자 평탄성 규정',
        'desc': '본 수행지침서는 동탄트램 노반 표면 요철 정밀 정돈 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 3m 알루미늄 직선자 검교정</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 20m 간격 종횡단 연속 실측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 최대 갭 오차 ±10mm 이내 관리</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">요철 부위 삭평/재다짐 감리 승인</span>의 평탄성 정밀 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '3m 알루미늄 직선자 검교정', '변형이 없는 3m 알루미늄 평탄 측정자 및 테이퍼 쐐기 핑거 게이지를 준비함.'),
            ('STEP 02', '20m 간격 종횡단 연속 검측', '노반 중심선 및 좌우 궤도 부근 20m 간격으로 직선자를 밀착 측정함.'),
            ('STEP 03', '요철(오목/볼록) 지점 현출 & 수정', '오목 부위(10mm 초과) OMC 살수 재다짐 및 볼록 부위 모터그레이더 삭평을 조치함.'),
            ('STEP 04', '평탄성 검측 성과표 감리 승인', '평탄성 야장을 정리하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '📏 동탄트램 강화노반 3m 직선자 평탄성 검측 절차도',
        'diagram_nodes': [('1. 3m 직선자 준비', '테이퍼 게이지 교정'), ('2. 20m 간격 연속검측', '오차 ±10mm 이내 실측'), ('3. 감리 서면승인', '평탄성 성과표 결재')]
    },
    {
        'row': 30,
        'wbs': '9000-7-29',
        'dir_name': '28_노반 종 횡단 검측',
        'file_prefix': '노반 종 횡단 검측',
        'title': '노반 종 횡단 검측',
        'std_legal': 'KCS 47 10 25 강화노반 중심선 및 표고 측량 규정',
        'desc': '본 수행지침서는 동탄트램 3D 선형 좌표 대조 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 GRS80 광학 토탈스테이션 정밀 세팅</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 10m 간격 중심선(X,Y) 및 마무리면 표고(Z) 실측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 표고 및 중심선 오차 ±10mm 관리</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3D BIM 좌표 승인 결재</span>의 3D 선형 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', 'GRS80 광학 토탈스테이션 정밀 세팅', '인근 CP/TBM 기준점을 후시하여 레벨 및 평면 좌표를 정밀 세팅함.'),
            ('STEP 02', '10m 간격 중심선 & 표고 실측', '10m 간격으로 궤도 중심선(X,Y) 및 마무리면 표고(Z)를 현측함.'),
            ('STEP 03', '3D BIM CAD 좌표 1:1 대조', '측량 성과 데이터를 3D BIM 모델 좌표계에 매핑하여 오차(±10mm)를 검증함.'),
            ('STEP 04', '종횡단 성과표 감리 서면 승인', '종횡단 측량 성과표를 작성하여 책임감리원 최종 승인을 완료함.')
        ],
        'diagram_title': '📐 동탄트램 강화노반 종횡단 측량 및 3D BIM 좌표 검측 절차도',
        'diagram_nodes': [('1. GRS80 측량세팅', 'CP/TBM 후시 점검'), ('2. 10m 간격 측량', '중심선/표고 ±10mm'), ('3. 감리 서면승인', '3D BIM 성과표 결재')]
    },
    {
        'row': 31,
        'wbs': '9000-7-30',
        'dir_name': '29_부적합 사항 조치',
        'file_prefix': '부적합 사항 조치',
        'title': '부적합 사항 조치',
        'std_legal': '건설기술진흥법 & KCS 47 10 25 NCR 절차 규정',
        'desc': '본 수행지침서는 동탄트램 시공 결함 100% 종결 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 감리단 NCR 통지서 수령 및 현출</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 표면 15cm 파쇄 및 OMC 살수 재다짐</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 1:1 재검측(다짐도/K30/Ev2) 합격</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">NCR 조치 결과 서면 종결 승인</span>의 하자 제로 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '감리단 부적합 통지서(NCR) 수령', 'NCR 발행 지점의 지번, 위치 및 미달 수치(예: 다짐도 92%)를 확인함.'),
            ('STEP 02', '표면 15cm 파쇄 & OMC 살수 재다짐', '모터그레이더 리퍼로 15cm 파쇄 후 최적함수비 살수 및 롤러 재다짐을 시행함.'),
            ('STEP 03', '1:1 재검측(다짐도/K30/Ev2) 실시', '재다짐 구역에 대해 들밀도, K30, Ev2 시험을 1:1 재실시하여 합격 수치를 도출함.'),
            ('STEP 04', 'NCR 조치 결과 보고서 감리 승인', '조치 전·후 사진 및 재검측 성적서를 제출하여 감리 서면 종결 승인을 받음.')
        ],
        'diagram_title': '⚠️ 동탄트램 강화노반 부적합(NCR) 조치 및 재다짐 절차도',
        'diagram_nodes': [('1. NCR 발행 수령', '부적합 위치 현출'), ('2. 표면15cm 파쇄/재다짐', 'OMC 살수 및 롤러다짐'), ('3. 감리 서면승인', '1:1 재검측 NCR 종결')]
    },
    {
        'row': 32,
        'wbs': '9000-7-31',
        'dir_name': '30_사면 다짐 검측',
        'file_prefix': '사면 다짐 검측',
        'title': '사면 다짐 검측',
        'std_legal': 'KCS 47 10 25 성토 사면 구배 및 다짐 규정',
        'desc': '본 수행지침서는 동탄트램 토공 사면 유실 방지 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 성토 사면 경사 1:1.5 이하 측량</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 경사 롤러/램머 사면 다짐도 ≥ 90%</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 식생 거적 덮개(Jute Mat) 30cm 겹침 부설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">사면 검측서 감리 서면 승인</span>의 사면 안정을 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '성토 사면 경사(1:1.5) 측량', '광학 레벨 및 경사 측정기로 사면 비탈면 경사(1:1.5 이하)를 실측함.'),
            ('STEP 02', '사면 전용 다짐 장비 다짐', '경사 다짐 롤러 및 소형 램머로 사면 밀도(다짐도 ≥90%)를 검측함.'),
            ('STEP 03', '식생 거적 덮개(Jute Mat) 부설', '사면 세굴 방지용 거적 덮개를 30cm 겹침 부설하고 앵커 핀을 1m 간격 고정함.'),
            ('STEP 04', '사면 다짐 검측 성과 감리 승인', '사면 검측 요청서를 제출하여 책임감리원 서면 승인을 결재받음.')
        ],
        'diagram_title': '🏔️ 동탄트램 성토 사면 다짐 및 식생 거적 덮개 절차도',
        'diagram_nodes': [('1. 사면 경사 측량', '경사 1:1.5 이하 검측'), ('2. 사면 다짐/거적부설', '다짐도 90%/Jute Mat'), ('3. 감리 서면승인', '사면 다짐서 결재')]
    },
    {
        'row': 33,
        'wbs': '9000-7-32',
        'dir_name': '31_배수시설 시공 검측',
        'file_prefix': '배수시설 시공 검측',
        'title': '배수시설 시공 검측',
        'std_legal': 'KCS 47 10 25 노반 배수 구조물 시방 규정',
        'desc': '본 수행지침서는 동탄트램 노반 배수 완결 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 U형 측구(0.4×0.4m) 버림 콘크리트 부설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 집수정 바닥 인버트 모타르 사춤</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 주철 그레이팅 덮개 볼트 체결 및 담수 시험</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">배수시설 시공 검측 승인</span>의 배수 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', 'U형 측구 기초 콘크리트 & 터파기', '측구 기초 터파기 깊이 및 버림 콘크리트(두께 10cm) 타설을 검측함.'),
            ('STEP 02', 'U형 측구 PC관 부설 & 집수정 성형', 'U형 측구(0.4×0.4m) 부설 및 집수정 바닥 인버트 모타르 사춤을 시행함.'),
            ('STEP 03', '주철 그레이팅 덮개 볼트 체결', '집수정 상부 주철 그레이팅 덮개를 체결하고 통수 담수 시험을 하였는가?'),
            ('STEP 04', '배수시설 검측 성과표 감리 승인', '배수 검측 요청서를 제출하여 책임감리원 최종 서면 승인을 결재받음.')
        ],
        'diagram_title': '🌊 동탄트램 배수시설(U형 측구 & 집수정) 시공 및 검측 절차도',
        'diagram_nodes': [('1. 측구 터파기/기초', '버림 콘크리트 10cm'), ('2. U형측구/집수정', '인버트 모타르 사춤'), ('3. 감리 서면승인', '배수시설 검측서 결재')]
    },
    {
        'row': 34,
        'wbs': '9000-7-33',
        'dir_name': '32_완성면 보호',
        'file_prefix': '완성면 보호',
        'title': '완성면 보호',
        'std_legal': 'KCS 47 10 25 다짐 완성면 유지 관리 규정',
        'desc': '본 수행지침서는 동탄트램 궤도팀 인계 전 완성면 보존 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 통제 바리케이트(중장비 진입 100% 차단)</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 건조 시 미세 살수 및 비닐 덮개 부설</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 일일 완성면 훼손 현측 점검</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">완성면 보호 대장 감리 결재</span>의 노반 보존 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '완성면 통제 바리케이트 & 표지판 설치', '강화노반 완성면 경계에 통제 펜스 및 주행 금지 표지판을 비치함.'),
            ('STEP 02', '일일 살수 & 비닐 덮개 부설', '골재 이탈 예방용 미세 분무 살수를 시행하고 비 비닐 덮개를 야적함.'),
            ('STEP 03', '궤도 인수 전 일일 훼손 현측 점검', '일일 완성면 훼손 여부를 점검하고 장비 무단 진입을 통제함.'),
            ('STEP 04', '완성면 보호 점검 대장 감리 승인', '보호 대장을 작성하여 책임감리원 서면 승인을 결재받음.')
        ],
        'diagram_title': '🚧 동탄트램 강화노반 완성면 무단 주행 통제 및 보호 절차도',
        'diagram_nodes': [('1. 통제 바리케이트', '중장비 무단진입 차단'), ('2. 살수/비닐 덮개', '골재이탈 예방 살수'), ('3. 감리 서면승인', '완성면 보호대장 결재')]
    },
    {
        'row': 35,
        'wbs': '9000-7-34',
        'dir_name': '33_공사일지 작성',
        'file_prefix': '공사일지 작성',
        'title': '공사일지 작성',
        'std_legal': '건설기술진흥법 시행규칙 & 공사기록 작성 규정',
        'desc': '본 수행지침서는 동탄트램 일일 시공 법적 증빙 기록 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 인원·장비·토공 성토 물량(m³) 정밀 집계</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 품질 시험 수치(다짐도/K30/Ev2) 수록</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 CSI 전산 관리 시스템 일일 등록</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">책임감리원 일일 서면 직인 결재</span>의 법정 기록 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '일일 인원 · 장비 · 물량 데이터 집계', '작업조 인원, 강동 롤러 등 장비 및 토공 성토 물량(m³)을 정밀 집계함.'),
            ('STEP 02', '품질 시험 성적 & TBM 사항 수록', '들밀도 시험, K30 평판재하 수치 및 일일 TBM 내용을 공사일지에 부착함.'),
            ('STEP 03', '전산 시스템(CSI/CIMS) 일일 등록', '국토교통부 및 현장 전산 관리 시스템에 일일 일지를 수록 등록함.'),
            ('STEP 04', '책임감리원 일일 서면 결재 수검', '공사일지를 작성하여 매일 책임감리원 공학적 직인 결재를 완수함.')
        ],
        'diagram_title': '📝 동탄트램 일일 공사일지 작성 및 감리 결재 절차도',
        'diagram_nodes': [('1. 데이터 정밀집계', '인원/장비/물량 집계'), ('2. 전산 시스템 등록', 'CSI/CIMS 전산 등록'), ('3. 감리 서면승인', '일일 공사일지 결재')]
    },
    {
        'row': 36,
        'wbs': '9000-7-35',
        'dir_name': '35_검측 및 승인 관리',
        'file_prefix': '검측 및 승인 관리',
        'title': '검측 및 승인 관리',
        'std_legal': '건설기술진흥법 & KCS 47 10 25 총괄 검측 규정',
        'desc': '본 수행지침서는 동탄트램 전체 검측 행정 완수 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 공사 착수 24시간 전 검측 요청서 제출</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 책임감리원 1:1 현장 입회 검측</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 16개 항목 체크리스트 서명 및 승인 공문 수령</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">검측 총괄 승인 대장 바인딩</span>의 검측 체계를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '공종별 검측 요청서 24시간 전 제출', '원지반, 하부노반, 강화노반 검측 요청서를 감리단에 공식 접수함.'),
            ('STEP 02', '책임감리원 1:1 현장 입회 검측', '감리원 입회하에 레벨, 다짐도, K30, Ev2를 1:1 현장 수검함.'),
            ('STEP 03', '검측 체크리스트 서명 & 승인 공문', '16개 문항 체크리스트 감리 서명 및 적정 승인 공문을 수령함.'),
            ('STEP 04', '검측 총괄 승인 대장 바인딩', '승인 공문 및 성적표를 총괄 대장에 등록하여 감리 결재를 완수함.')
        ],
        'diagram_title': '📑 동탄트램 강화노반 총괄 검측 및 승인 공문 관리 절차도',
        'diagram_nodes': [('1. 검측요청 24h 전', '공문/체크리스트 제출'), ('2. 감리 1:1 입회', '3대 공학수치 현측'), ('3. 감리 서면승인', '검측 총괄대장 결재')]
    },
    {
        'row': 37,
        'wbs': '9000-7-36',
        'dir_name': '36_토공 마무리면 인계',
        'file_prefix': '토공 마무리면 인계',
        'title': '토공 마무리면 인계',
        'std_legal': 'KCS 47 10 25 강화노반 최종 인계인수 규정',
        'desc': '본 수행지침서는 동탄트램 상부강화노반 준공 및 궤도팀 최종 인계 단계로서, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">1단계 토공-궤도-감리 3자 합동 현측 세팅</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">2단계 표고 오차 ±10mm 및 K30 ≥ 110/Ev2 ≥ 60 재확인</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">3단계 인계인수 합의서 3자 서명</span> ➔ <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">상부강화노반 최종 완공 통보</span>의 최종 인계 구조를 선제 파악하고, 4대 체계별 세부 작업 수행절차와 정밀 2D visual 기술 도식 및 대형 확대 모달(<code class="bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)을 제공합니다.',
        'steps': [
            ('STEP 01', '3자(토공-궤도-감리) 합동 현측 세팅', '인계 구간(STA 0k+000 ~ 0k+500)에 대해 3자 합동 검측 일정을 수립함.'),
            ('STEP 02', '표고 오차(±10mm) & K30(≥110) 재검측', '궤도 설치 인접 부위 중심선 레벨 및 평판재하 K30 강도를 합동 재확인함.'),
            ('STEP 03', '토공 마무리면 인계인수서 3자 서명', '결과 이상 없음을 확인하고 인계인수 합의서에 토공, 궤도, 감리 3자 서명함.'),
            ('STEP 04', '상부강화노반 최종 완공 통보', '인계인수서 및 최종 성과표를 발주처에 공식 통보하여 노반 공사를 완수함.')
        ],
        'diagram_title': '🏁 동탄트램 상부강화노반 궤도 시공팀 최종 인계인수 절차도',
        'diagram_nodes': [('1. 3자 합동 현측', '표고 ±10mm / K30 110'), ('2. 인계인수서 서명', '토공-궤도-감리 3자 서명'), ('3. 발주처 완공통보', '강화노반 최종 완공')]
    }
]

print(f"새 이미지 옐로우/크림 규격 재생성 대상 개수: {len(manuals_cream_data)}")

for item in manuals_cream_data:
    gui_dir = os.path.join(base_root, item['dir_name'], '수행지침')
    target_file = os.path.join(gui_dir, f"{item['file_prefix']}_수행지침.html")
    
    title_name = item['title']
    desc_content = item['desc']

    cream_gui_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>동탄트램 상부강화노반 - {title_name} 상세 수행지침서 (WBS {item['wbs']})</title>
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
        <h1 class="text-3xl font-black mt-2">{title_name} 상세 수행지침서</h1>
        <p class="text-amber-200 text-sm mt-1">L4 Code: {item['wbs']} | 주관: 현장 공사팀 / 공무팀 | "{item['std_legal']}"</p>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 💡 [첨부이미지 100% 동일 옐로우/크림 규격] 콜아웃 개요 박스 -->
        <div class="bg-amber-50/70 border border-amber-200/80 p-6 rounded-2xl text-slate-800 text-sm font-normal leading-relaxed shadow-sm space-y-2.5">
            <h4 class="font-bold text-base text-slate-900 flex items-center gap-2 m-0">
                <span class="text-base">💡</span> 동탄트램 {title_name} 실무 핵심
            </h4>
            <p class="m-0 text-slate-700 leading-relaxed text-xs sm:text-sm">
                {desc_content}
            </p>
        </div>

        <div class="space-y-8">
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2"><span class="text-amber-600">🛠️</span> {title_name} 4단계 상세 수행 절차</h2>
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
            <h2 class="text-xl font-bold text-slate-900 border-b-2 border-amber-600 pb-2 flex items-center gap-2"><span class="text-amber-600">🖼️</span> {title_name} 상세 수행 절차도</h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_{item['row']}', '[WBS {item['wbs']}] {title_name} 상세 수행 절차도')">
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
                    <text x="275" y="168" font-size="9" font-weight="black" fill="#ffffff" text-anchor="middle">✔ WBS {item['wbs']} {title_name} 승인 완수</text>
                </svg>
            </div>
        </div>
    </div>
</div>

<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 {title_name} 2D Visual 도식 확대 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]"></div>
    </div>
</div>

<script>
    function openDiagramZoom(elementId, titleText) {{
        const srcEl = document.getElementById(elementId);
        if (!srcEl) return;
        const zoomBody = document.getElementById('zoomBody');
        document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "{title_name} 도식 확대 보기");
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

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(cream_gui_html)

print("SUCCESS: 35개 상부강화노반 수행지침서 HTML 파일이 새 첨부이미지 옐로우/크림 규격과 100% 동일하게 완벽 재건축 완료되었습니다!")
