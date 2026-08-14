import os, sys, re

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

manuals_data = [
    {
        'dir_name': '2_발주전략 KOM',
        'file_prefix': '발주전략 KOM',
        'tag': '발주전략 KOM',
        'title': '발주전략 KOM',
        'specs': ['발주처 품질 요구사항 분석', '3D BIM 도면 1:1 대조', '리스크 관리계획 수립'],
        'steps_short': '요구사항 분석, BIM 도면 대조, 리스크 수립, 감리 승인'
    },
    {
        'dir_name': '3_철도보호지구에서의 행위신고(필요시)',
        'file_prefix': '철도보호지구에서의 행위신고(필요시)',
        'tag': '철도보호지구 행위신고',
        'title': '철도보호지구에서의 행위신고',
        'specs': ['궤도 중심 30m 경계 측량', '철도안전법 제45조 법정 인허가', '운행선안전관리자 상주 배치'],
        'steps_short': '30m 경계 측량, 서류 작성, 관할기관 신고, 안전관리자 배치'
    },
    {
        'dir_name': '4_착수전 측량 Data 확인',
        'file_prefix': '착수전 측량 Data 확인',
        'tag': '착수전 측량 Data 확인',
        'title': '착수전 측량 Data 확인',
        'specs': ['GRS80 세계측지계 좌표 대조', '수준측량 오차 ≤ 5mm√K', 'TBM 인조점 3개소 매설'],
        'steps_short': 'CP/TBM 인수, 현장 광학 재측량, 인조점 매설, BIM 승인'
    },
    {
        'dir_name': '5_지장물이설 협의',
        'file_prefix': '지장물이설 협의',
        'tag': '지장물이설 협의',
        'title': '지장물이설 협의',
        'specs': ['GPR 지중 레이더 탐사', '인력 시탐 줄파기 1.5m', '점용기관 1:1 현장 입회'],
        'steps_short': 'GPR/줄파기, 점용기관 입회, 매달기 방호, 3D BIM 매핑'
    },
    {
        'dir_name': '6_용지보상RISK 검토',
        'file_prefix': '용지보상RISK 검토',
        'tag': '용지보상RISK 검토',
        'title': '용지보상RISK 검토',
        'specs': ['토지보상법 미보상 필지 추출', '높이 1.8m 가설 펜스 차단', '3D 우회 토공 동선 수립'],
        'steps_short': '수용 조서 대조, 사유지 펜스 격리, 우회 공정 수립, 감리 승인'
    },
    {
        'dir_name': '7_최고의 팀 만들기 지원',
        'file_prefix': '최고의 팀 만들기 지원',
        'tag': '최고의 팀 만들기',
        'title': '최고의 팀 만들기 지원',
        'specs': ['토공 전문 기술자 1:1 전담 배치', '주간 상생 소통 회의', '일일 안전 TBM 및 복지 지원'],
        'steps_short': '전문인력 배치, 주간 소통 회의, 근로 복지 지원, One-Team 결재'
    },
    {
        'dir_name': '8_시공계획서 수립 승인',
        'file_prefix': '시공계획서 수립 승인',
        'tag': '시공계획서 수립 승인',
        'title': '시공계획서 수립 승인',
        'specs': ['건진법 제89조 8대 목차 준수', 'KCS 47 10 25 다짐 수치 명시', '50m 현장 시험다짐 계획'],
        'steps_short': '계획서 본안 작성, 착공 14일전 제출, 보완 조치, 서면 승인'
    },
    {
        'dir_name': '8_작업조 편성',
        'file_prefix': '작업조 편성',
        'tag': '작업조 편성',
        'title': '작업조 편성',
        'specs': ['공종별 전담 기술 수첩 검증', '건설기계 조종원 면허 1:1 대조', '일일 음주 측정 및 TBM'],
        'steps_short': '기술자 배치, 조종원 면허 대조, 일일 TBM/음주측정, 조직표 승인'
    },
    {
        'dir_name': '9_장비 수급 계획',
        'file_prefix': '장비 수급 계획',
        'tag': '장비 수급 계획',
        'title': '장비 수급 계획',
        'specs': ['자중 10ton+ 강동 진동 롤러', '3D GPS 제어 모터그레이더', '반입 건설기계 정기검사 수검'],
        'steps_short': '장비 사양 확정, 반입 전 안전점검, 센서 교정, 장비 수급 승인'
    },
    {
        'dir_name': '10_노반 재료 입도 DB 확보',
        'file_prefix': '노반 재료 입도 DB 확보',
        'tag': '노반 재료 입도 DB',
        'title': '노반 재료 입도 DB 확보',
        'specs': ['골재 최대입경 50mm 이하', '#200체 통과량 5% 이하', '수정다짐 CBR 30% 이상'],
        'steps_short': '공급원 사전승인, 1,000m³당 체가름, CBR/입도 DB, 감리 승인'
    },
    {
        'dir_name': '11_사토장 _ 토사 수급 계획 확인',
        'file_prefix': '사토장 _ 토사 수급 계획 확인',
        'tag': '사토장 / 토사 수급',
        'title': '사토장 / 토사 수급 계획 확인',
        'specs': ['화성시 정식 사토장 인허가', '최대건조밀도 γd max ≥ 1.90g/cm³', '토양오염 8개 항목 검사'],
        'steps_short': '사토장 인허가 검증, 토사 물리/오염 시험, 수불 대장 관리, 감리 승인'
    },
    {
        'dir_name': '12_배수 처리 계획 수립',
        'file_prefix': '배수 처리 계획 수립',
        'tag': '배수 처리 계획',
        'title': '배수 처리 계획 수립',
        'specs': ['성토 사면 가배수로 0.6×0.6m', '가침사지 2개소 용량 설계', 'HDPE 유공관 Ø200mm 구배 ≥0.5%'],
        'steps_short': '가배수로/침사지 설계, 유공관/부직포 검수, 양수 펌프 비치, 배수 승인'
    },
    {
        'dir_name': '13_안전관리계획 수립 승인',
        'file_prefix': '안전관리계획 수립 승인',
        'tag': '안전관리계획 수립 승인',
        'title': '안전관리계획 수립 승인',
        'specs': ['건진법 제62조 안전계획 수립', '국토안전관리원 정밀 심사', 'CSI 안전관리종합망 전산 등록'],
        'steps_short': '안전계획서 작성, 정밀 심사 수검, CSI 전산 등록, 감리 서면승인'
    },
    {
        'dir_name': '14_품질관리계획 수립 승인',
        'file_prefix': '품질관리계획 수립 승인',
        'tag': '품질관리계획 수립 승인',
        'title': '품질관리계획 수립 승인',
        'specs': ['다짐도 500m³당 1회', 'K30 2,000m²당 1회', 'Ev2 1,000m²당 1회 시험'],
        'steps_short': '시험 빈도 수립, 시험 장비 교정, 착공 14일전 제출, 서면 승인'
    },
    {
        'dir_name': '15_환경관리계획 수립 승인',
        'file_prefix': '환경관리계획 수립 승인',
        'tag': '환경관리계획 수립 승인',
        'title': '환경관리계획 수립 승인',
        'specs': ['비산먼지 발생사업 신고', '이동식 세륜기 깊이 1.2m', '가설 방음벽 3m (65dB 이하)'],
        'steps_short': '환경 시설 설계, 지자체 신고, 세륜기/살수차 가동, 환경 승인'
    },
    {
        'dir_name': '16_교통소통 대책 수립 승인(필요시)',
        'file_prefix': '교통소통 대책 수립 승인(필요시)',
        'tag': '교통소통 대책 승인',
        'title': '교통소통 대책 수립 승인',
        'specs': ['동탄경찰서 교통안전 심의', '차선 점용 허가증 수령', '전담 안전 신호수 2인 2조'],
        'steps_short': '교통 우회 설계, 경찰서 심의, 신호수/경광등 배치, 교통 승인'
    },
    {
        'dir_name': '17_하도급 검토 승인',
        'file_prefix': '하도급 검토 승인',
        'tag': '하도급 검토 승인',
        'title': '하도급 검토 승인',
        'specs': ['토공 전문건설업 면허 확인', '하도급율 82% 이상 확보', '노무비 전용계좌 지정'],
        'steps_short': '면허/실적 검증, 적정성 심사표 작성, 노무비 계좌 지정, 하도급 승인'
    },
    {
        'dir_name': '18_자재승인',
        'file_prefix': '자재승인',
        'tag': '자재승인',
        'title': '자재승인',
        'specs': ['KS F 2527 쇄석골재', 'HDPE 유공관 및 부직포 200g/m²', '공인 기관 시험성적서 검수'],
        'steps_short': '공급원 서류 검토, 공인 기관 시험, 승인 신청서 제출, 현장 반입 검수'
    },
    {
        'dir_name': '19_시험다짐',
        'file_prefix': '시험다짐',
        'tag': '시험다짐',
        'title': '시험다짐',
        'specs': ['50m 현장 시험구간 포설', '강동 롤러 4~6회 다짐 횟수 확정', '침하량 Δh ≤ 1mm 측정'],
        'steps_short': '50m 구간 선정, 30cm 포설, 다짐 횟수별 침하 측정, 결과 보고서 승인'
    },
    {
        'dir_name': '20_원지반 검측',
        'file_prefix': '원지반 검측',
        'tag': '원지반 검측',
        'title': '원지반 검측',
        'specs': ['유기질 표토 15~30cm 제거', '원지반 K30 ≥ 70 MN/m³', '덤프트럭 펌핑 연약지반 점검'],
        'steps_short': '표토 제거/다짐, 표고 레벨 측량, K30 시험/펌핑 점검, 원지반 승인'
    },
    {
        'dir_name': '21_하부노반 검측',
        'file_prefix': '하부노반 검측',
        'tag': '하부노반 검측',
        'title': '하부노반 검측',
        'specs': ['층두께 30cm 이하 포설', '다짐도 90% 이상 (KS F 2311)', 'K30 ≥ 90 MN/m³ 지비력'],
        'steps_short': '30cm 층포설/다짐, 들밀도/K30 시험, 마무리면 측량, 하부노반 승인'
    },
    {
        'dir_name': '22_상부노반 시공(배수 유공관 포함)',
        'file_prefix': '상부노반 시공(배수 유공관 포함)',
        'tag': '상부노반 시공',
        'title': '상부노반 시공(배수 유공관 포함)',
        'specs': ['맹암거 HDPE 유공관 천공 상향 배치', '투수성 부직포 겹침 30cm', '소형 램머 다짐'],
        'steps_short': '토사 30cm 포설, 맹암거 터파기/부직포, HDPE 유공관 부설, 상부노반 승인'
    },
    {
        'dir_name': '23_상부강화노반 시공',
        'file_prefix': '상부강화노반 시공',
        'tag': '상부강화노반 시공',
        'title': '상부강화노반 시공',
        'specs': ['3D GPS 쇄석 50mm 포설', '최적함수비 OMC 분무 살수', '강동 4회+타이어 2회 롤링'],
        'steps_short': '3D GPS 쇄석 포설, OMC 분무 살수, 강동/타이어 다짐, 마무리면 측량'
    },
    {
        'dir_name': '24_다짐 검측',
        'file_prefix': '다짐 검측',
        'tag': '다짐 검측',
        'title': '다짐 검측',
        'specs': ['노반 다짐도 ≥ 95%', 'K30 ≥ 110 MN/m³', 'Ev2 ≥ 60 MPa (Ev2/Ev1 ≤ 2.2)'],
        'steps_short': '들밀도 시험(95%+), K30 재하(110+), Ev2 측정(60+), 다짐 보고서 승인'
    },
    {
        'dir_name': '25_평판재하시험',
        'file_prefix': '평판재하시험',
        'tag': '평판재하시험',
        'title': '평판재하시험',
        'specs': ['Ø300mm 재하판 산모래 밀착', '15t 유압 잭 하중 재하', 'K30 ≥ 110 MN/m³ 성적서'],
        'steps_short': '재하판 밀착 부설, 유압 잭/게이지 세팅, 단계별 하중 측정, K30 승인'
    },
    {
        'dir_name': '26_강성 검측(K30, EV2)',
        'file_prefix': '강성 검측(K30, EV2)',
        'tag': '강성 검측',
        'title': '강성 검측(K30, EV2)',
        'specs': ['DIN 18134 LWD 측정', '2차 변형계수 Ev2 ≥ 60 MPa', '변형계수 비율 Ev2/Ev1 ≤ 2.2'],
        'steps_short': 'LWD 장비 교정, 1,000m²당 무작위 측정, Ev1/Ev2 재하, 강성 보고서 승인'
    },
    {
        'dir_name': '27_평탄성 검측',
        'file_prefix': '평탄성 검측',
        'tag': '평탄성 검측',
        'title': '평탄성 검측',
        'specs': ['3m 알루미늄 직선자 밀착', '20m 간격 연속 측정', '최대 갭 오차 ±10mm 통제'],
        'steps_short': '3m 직선자 검교정, 20m 간격 연속 검측, 요철 삭평/재다짐, 평탄성 승인'
    },
    {
        'dir_name': '28_노반 종 횡단 검측',
        'file_prefix': '노반 종 횡단 검측',
        'tag': '노반 종 횡단 검측',
        'title': '노반 종 횡단 검측',
        'specs': ['GRS80 광학 토탈스테이션', '궤도 중심선 오차 ±10mm', '계획 표고 오차 ±10mm'],
        'steps_short': '토탈스테이션 세팅, 10m 간격 중심선/표고 실측, 3D BIM 대조, 종횡단 승인'
    },
    {
        'dir_name': '29_부적합 사항 조치',
        'file_prefix': '부적합 사항 조치',
        'tag': '부적합 사항 조치',
        'title': '부적합 사항 조치',
        'specs': ['감리 NCR 수령', '표면 15cm 파쇄 및 OMC 재다짐', '1:1 재검측 서면 종결'],
        'steps_short': 'NCR 통지서 수령, 표면 15cm 파쇄/재다짐, 1:1 재검측, NCR 종결 승인'
    },
    {
        'dir_name': '30_사면 다짐 검측',
        'file_prefix': '사면 다짐 검측',
        'tag': '사면 다짐 검측',
        'title': '사면 다짐 검측',
        'specs': ['성토 사면 경사 1:1.5 이하', '사면 다짐도 90% 이상', '식생 거적 덮개 Jute Mat 부설'],
        'steps_short': '사면 경사 측량, 경사 다짐 롤러 다짐, 거적 덮개 부설, 사면 검측 승인'
    },
    {
        'dir_name': '31_배수시설 시공 검측',
        'file_prefix': '배수시설 시공 검측',
        'tag': '배수시설 시공 검측',
        'title': '배수시설 시공 검측',
        'specs': ['U형 측구 0.4×0.4m 인버트 사춤', '집수정 물고임 방지', '주철 그레이팅 덮개 체결'],
        'steps_short': '측구 기초 터파기, U형 측구/집수정 부설, 그레이팅 덮개 체결, 배수 승인'
    },
    {
        'dir_name': '32_완성면 보호',
        'file_prefix': '완성면 보호',
        'tag': '완성면 보호',
        'title': '완성면 보호',
        'specs': ['통제 바리케이트 무단진입 차단', '표면 이탈 방지 미세 살수', '비 비닐 덮개 부설'],
        'steps_short': '통제 바리케이트 설치, 미세 살수/비닐 덮개, 일일 완성면 점검, 보호 승인'
    },
    {
        'dir_name': '33_공사일지 작성',
        'file_prefix': '공사일지 작성',
        'tag': '공사일지 작성',
        'title': '공사일지 작성',
        'specs': ['인원/장비/성토 물량 일일 집계', '품질 시험 성적 기록', 'CSI 시스템 전산 등록'],
        'steps_short': '데이터 정밀 집계, 품질 성적 수록, CSI 시스템 등록, 감리 일일 결재'
    },
    {
        'dir_name': '35_검측 및 승인 관리',
        'file_prefix': '검측 및 승인 관리',
        'tag': '검측 및 승인 관리',
        'title': '검측 및 승인 관리',
        'specs': ['공사 착수 24시간 전 검측 제출', '1:1 현장 감리 입회', '검측 총괄 대장 전산화'],
        'steps_short': '검측 요청서 24h전 제출, 감리 1:1 현장 입회, 승인 공문 수령, 총괄 대장 결재'
    },
    {
        'dir_name': '36_토공 마무리면 인계',
        'file_prefix': '토공 마무리면 인계',
        'tag': '토공 마무리면 인계',
        'title': '토공 마무리면 인계',
        'specs': ['토공-궤도-감리 3자 합동 현측', '표고 오차 ±10mm & K30 ≥ 110', '인계인수서 3자 서명'],
        'steps_short': '3자 합동 현측 세팅, 표고/K30 재검측, 인계인수서 서명, 완공 통보'
    }
]

print(f"업데이트 대상 수행지침서 개수: {len(manuals_data)}")

updated_count = 0

for item in manuals_data:
    gui_dir = os.path.join(base_root, item['dir_name'], '수행지침')
    target_file = os.path.join(gui_dir, f"{item['file_prefix']}_수행지침.html")
    
    if not os.path.exists(target_file):
        print(f"❌ 파일 없음: {target_file}")
        continue

    spec1 = item['specs'][0]
    spec2 = item['specs'][1]
    spec3 = item['specs'][2]
    tag_name = item['tag']
    title_name = item['title']
    steps_short = item['steps_short']

    # 이미지와 100% 동일한 고급 오버뷰 콜아웃 박스 구조
    overview_box_html = f"""<!-- 💡 [이미지 동일 규격] 세부 수행절차 개요 콜아웃 박스 -->
        <div class="bg-blue-50/60 border border-blue-200/80 p-6 rounded-2xl text-slate-800 text-sm font-normal leading-relaxed shadow-sm space-y-2.5">
            <h4 class="font-bold text-base text-slate-900 flex items-center gap-2 m-0">
                <span class="text-base">💡</span> [{tag_name}] {title_name} 4단계 세부 수행절차 개요
            </h4>
            <p class="m-0 text-slate-700 leading-relaxed text-xs sm:text-sm">
                본 수행지침서는 동탄트램 상부강화노반 시공 시 <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">{spec1}</span>, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">{spec2}</span>, <span class="text-blue-600 font-semibold underline decoration-dashed decoration-blue-400 underline-offset-4">{spec3}</span>을 완수하기 위한 4단계 체계별 세부 작업 수행절차({steps_short})로 구성됩니다. 각 단계별 카드 내부에 정밀 2D visual 기술 도식과 대형 확대 모달(<code class="bg-blue-100/80 text-blue-900 px-1.5 py-0.5 rounded font-mono text-xs">openDiagramZoom</code>)이 수록되어 있습니다.
            </p>
        </div>"""

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 기존 개요 박스 영역 치환 (bg-amber-50 클래스 영역 찾기)
    pattern = r'<!-- 💡 검토 개요 및 목표 -->\s*<div class="bg-amber-50.*?</div>\s*</div>'
    
    if re.search(r'bg-amber-50', content):
        # bg-amber-50 div 정규식 치환
        content_new = re.sub(
            r'<div class="bg-amber-50 border border-amber-200 p-6 rounded-2xl text-sm text-amber-950 space-y-3">.*?</div>\s*</div>',
            overview_box_html,
            content,
            flags=re.DOTALL
        )
    else:
        # 혹시 이미 변형되었을 경우 대체 치환
        content_new = re.sub(
            r'<!-- 💡 실무 수행 개요 -->.*?</div>\s*</div>',
            overview_box_html,
            content,
            flags=re.DOTALL
        )

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    updated_count += 1

print(f"SUCCESS: 총 {updated_count}개 상부강화노반 수행지침서 HTML 문서의 상단 개요 박스를 첨부 이미지 양식과 100% 동일하게 업데이트 완료!")
