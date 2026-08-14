# -*- coding: utf-8 -*-
"""
동탄트램 기계설비·소방설비 19~36번 액티비티 1:1 전용 고해상도 2D 기술도식 (Light Theme 준수)
"""

MECH_SVGS_PART2 = {
    19: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">능동지하차도 트램 전용터널 제연(Jet Fan) 및 건식 연결송수관 상세도</text>

  <rect x="50" y="70" width="700" height="110" rx="8" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="400" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">능동지하차도 트램 전용 터널 (단면)</text>

  <rect x="150" y="105" width="100" height="35" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="200" y="127" text-anchor="middle" font-size="10" font-weight="bold" fill="#991b1b">Jet Fan (제연팬)</text>

  <path d="M 250 122 L 550 122" stroke="#dc2626" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
  <text x="400" y="115" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">임계풍속 배연 기류 (V ≥ 2.5 m/s)</text>

  <path d="M 550 155 L 150 155" stroke="#16a34a" stroke-width="3" stroke-dasharray="5,3" fill="none"/>
  <text x="350" y="170" text-anchor="middle" font-size="10" font-weight="bold" fill="#15803d">승객 안전 피난 방향 (연기 반대 방향 ⟶ 비상계단)</text>

  <rect x="50" y="195" width="700" height="90" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="70" y="220" font-size="11" font-weight="bold" fill="#15803d">■ 터널 제연 및 연결송수관 안전 기준 (도시철도건설규칙 제67조)</text>
  <text x="70" y="240" font-size="11" fill="#334155">• 3D CFD 화재 시뮬레이션 검증 ⟶ 화재 발생 30초 내 임계풍속(2.5m/s) 도출</text>
  <text x="70" y="260" font-size="11" fill="#334155">• 50m 간격 건식 연결송수관 방수구함(D100 Sch40) 및 소방차 전용 송수구 가설</text>
</svg>''',

    20: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">공기조화기(AHU) 방진스프링 마운트 거치 및 딥 드레인트랩 상세도</text>

  <rect x="150" y="70" width="500" height="90" rx="6" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="100" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af">공기조화기 케이싱 (AHU Casing)</text>
  <text x="400" y="125" text-anchor="middle" font-size="11" fill="#334155">송풍기부 | 냉온수 코일부 | 미디엄/프리 필터부</text>

  <rect x="180" y="160" width="40" height="25" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
  <rect x="380" y="160" width="40" height="25" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
  <rect x="580" y="160" width="40" height="25" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="200" y="177" text-anchor="middle" font-size="9" font-weight="bold" fill="#854d0e">스프링</text>
  <text x="400" y="177" text-anchor="middle" font-size="9" font-weight="bold" fill="#854d0e">스프링</text>
  <text x="600" y="177" text-anchor="middle" font-size="9" font-weight="bold" fill="#854d0e">스프링</text>

  <rect x="100" y="185" width="600" height="25" fill="#94a3b8"/>
  <text x="400" y="202" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">기초 콘크리트 패드 (두께 ≥ 200mm, 강도 24MPa)</text>

  <path d="M 630 145 L 630 230 L 660 230 L 660 210 L 700 210" stroke="#0284c7" stroke-width="3" fill="none"/>
  <text x="685" y="195" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">딥 U-Trap (봉수 100mm)</text>

  <rect x="50" y="225" width="550" height="65" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="70" y="248" font-size="11" font-weight="bold" fill="#15803d">✔ 방진 마운트 정적 변위 ≥ 25mm ⟶ 진동 전달 차단율 90% 이상 확보</text>
  <text x="70" y="268" font-size="11" fill="#334155">• 흡입 부압에 의한 응축수 역류 방지 딥 U-Trap 시공 ⟶ 바닥 침수 완벽 방지</text>
</svg>''',

    21: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">급수·급탕 STS 배관 무용접 프레스 압착 공법 및 수압시험 상세도</text>

  <rect x="60" y="90" width="260" height="40" fill="#94a3b8" rx="2"/>
  <text x="190" y="115" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">STS304 강관 (KSD 3595)</text>

  <rect x="320" y="80" width="60" height="60" rx="4" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
  <text x="350" y="115" text-anchor="middle" font-size="10" font-weight="bold" fill="#0f172a">프레스<br>피팅</text>

  <rect x="380" y="90" width="260" height="40" fill="#94a3b8" rx="2"/>
  <text x="510" y="115" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">STS304 강관 (KSD 3595)</text>

  <circle cx="335" cy="110" r="6" fill="#dc2626"/>
  <circle cx="365" cy="110" r="6" fill="#dc2626"/>
  <text x="350" y="70" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">EPDM 고무 오링 압착</text>

  <rect x="60" y="170" width="320" height="100" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="220" y="195" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">1. 전동 압착 및 게이지 검측</text>
  <text x="80" y="220" font-size="10" fill="#334155">• 삽입선(Insert Line) 마킹 후 전동공구 압착</text>
  <text x="80" y="240" font-size="10" fill="#334155">• 전용 육각 판정 게이지(Go/No-Go) 전수 검사</text>
  <text x="80" y="260" font-size="10" fill="#334155">• 압착 누락률 0.0% 달성</text>

  <rect x="400" y="170" width="340" height="100" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="570" y="195" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">2. 1.0MPa 수압 및 염소소독</text>
  <text x="420" y="220" font-size="10" fill="#334155">• 설계압력 2배인 1.0MPa 60분 수압 무누수</text>
  <text x="420" y="240" font-size="10" fill="#334155">• 차아염소산나트륨 50ppm 24시간 살균 소독</text>
  <text x="420" y="260" font-size="10" fill="#334155">• 먹는물 수질기준 46개 항목 100% 적합</text>
</svg>''',

    22: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">오배수 배관 자연유하 구배(1/100) 및 집수조 자동교번 배수펌프</text>

  <path d="M 60 90 L 350 120" stroke="#854d0e" stroke-width="6" fill="none"/>
  <text x="200" y="95" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">오수관로 자연유하 구배 (i ≥ 1/100)</text>

  <rect x="350" y="110" width="380" height="150" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
  <text x="440" y="130" font-size="11" font-weight="bold" fill="#0f172a">지하 집수조 (Sump Pit)</text>

  <rect x="390" y="170" width="60" height="70" rx="4" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
  <text x="420" y="205" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">배수펌프1<br>(상용)</text>

  <rect x="490" y="170" width="60" height="70" rx="4" fill="#22c55e" stroke="#15803d" stroke-width="1.5"/>
  <text x="520" y="205" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">배수펌프2<br>(예비)</text>

  <path d="M 420 170 L 420 80 L 680 80" stroke="#0284c7" stroke-width="3" fill="none"/>
  <path d="M 520 170 L 520 80" stroke="#0284c7" stroke-width="3" fill="none"/>
  <text x="600" y="70" text-anchor="middle" font-size="10" font-weight="bold" fill="#0284c7">토출 배수관 ⟶ 공공하수관로</text>

  <rect x="580" y="140" width="130" height="100" rx="4" fill="#fefce8" stroke="#ca8a04" stroke-width="1"/>
  <text x="645" y="160" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">4단 수위제어</text>
  <text x="590" y="180" font-size="9" fill="#334155">④ 고수위 경보</text>
  <text x="590" y="195" font-size="9" fill="#334155">③ 2대 동시 기동</text>
  <text x="590" y="210" font-size="9" fill="#334155">② 1대 기동 (교번)</text>
  <text x="590" y="225" font-size="9" fill="#334155">① 펌프 정지 (LWL)</text>
</svg>''',

    23: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">차량기지 오폐수처리장(연면적 90㎡, 35㎥/일) 정화 처리 공정도</text>

  <rect x="50" y="80" width="120" height="85" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="110" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#b91c1c">1. 원수 유입조</text>
  <text x="110" y="125" text-anchor="middle" font-size="9" fill="#334155">중정비(23.3㎥/일)</text>
  <text x="110" y="145" text-anchor="middle" font-size="9" fill="#334155">경정비(4.1㎥/일)</text>

  <rect x="190" y="80" width="120" height="85" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="250" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#a16207">2. 유수분리기</text>
  <text x="250" y="125" text-anchor="middle" font-size="9" fill="#334155">비중차 유분 분리</text>
  <text x="250" y="145" text-anchor="middle" font-size="9" fill="#334155">오일 스키머 회수</text>

  <rect x="330" y="80" width="130" height="85" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="395" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#1d4ed8">3. 화학응집침전조</text>
  <text x="395" y="125" text-anchor="middle" font-size="9" fill="#334155">PAC/폴리머 투입</text>
  <text x="395" y="145" text-anchor="middle" font-size="9" fill="#334155">Floc 형성 및 침전</text>

  <rect x="480" y="80" width="120" height="85" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="540" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">4. 활성탄 흡착탑</text>
  <text x="540" y="125" text-anchor="middle" font-size="9" fill="#334155">유기물/중금속 흡착</text>
  <text x="540" y="145" text-anchor="middle" font-size="9" fill="#334155">최종 고도 정화</text>

  <rect x="620" y="80" width="120" height="85" rx="6" fill="#dbeafe" stroke="#0284c7" stroke-width="1.5"/>
  <text x="680" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#0369a1">5. 수질 TMS 방류</text>
  <text x="680" y="125" text-anchor="middle" font-size="9" fill="#334155">BOD ≤ 20mg/L</text>
  <text x="680" y="145" text-anchor="middle" font-size="9" fill="#334155">COD ≤ 20mg/L</text>

  <path d="M 170 122 L 190 122" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 310 122 L 330 122" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 460 122 L 480 122" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 600 122 L 620 122" stroke="#0284c7" stroke-width="2" fill="none"/>

  <rect x="50" y="195" width="690" height="75" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="70" y="220" font-size="11" font-weight="bold" fill="#0f172a">■ 환경 오염 방지 및 수질 TMS 원격 감시 체계</text>
  <text x="70" y="240" font-size="11" fill="#334155">• 화학 응집 침전 슬러지: 필터프레스 탈수기 압착 케이크 위탁 처리</text>
  <text x="70" y="260" font-size="11" fill="#334155">• 24시간 실시간 환경청 TMS 연동 수질 측정 ⟶ 수질 사고 Zero 보장</text>
</svg>''',

    24: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">차량기지 청소선 차체 자동세척설비(세차기) 시스템 상세도</text>

  <rect x="80" y="80" width="640" height="110" rx="6" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="400" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">트램 청소선 자동세척기 갠트리 (속도 3~5km/h 통과)</text>

  <rect x="110" y="115" width="100" height="60" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1"/>
  <text x="160" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#1e40af">① 초벌 세척</text>
  <text x="160" y="160" text-anchor="middle" font-size="9" fill="#334155">고압 수세 노즐</text>

  <rect x="230" y="115" width="110" height="60" rx="4" fill="#fef08a" stroke="#ca8a04" stroke-width="1"/>
  <text x="285" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">② 세제 분사</text>
  <text x="285" y="160" text-anchor="middle" font-size="9" fill="#334155">중성 약품 노즐</text>

  <rect x="360" y="115" width="110" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/>
  <text x="415" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#991b1b">③ EVA 브러시</text>
  <text x="415" y="160" text-anchor="middle" font-size="9" fill="#334155">무스크래치 세척</text>

  <rect x="490" y="115" width="100" height="60" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="540" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#15803d">④ 고압 린스</text>
  <text x="540" y="160" text-anchor="middle" font-size="9" fill="#334155">깨끗한 청수 헹굼</text>

  <rect x="610" y="115" width="90" height="60" rx="4" fill="#e0e7ff" stroke="#4338ca" stroke-width="1"/>
  <text x="655" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#3730a3">⑤ 송풍 건조</text>
  <text x="655" y="160" text-anchor="middle" font-size="9" fill="#334155">윈드 블로워</text>

  <rect x="80" y="210" width="640" height="65" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="100" y="235" font-size="11" font-weight="bold" fill="#0f172a">■ 세척수 회수 및 도장 보호 성능</text>
  <text x="100" y="255" font-size="11" fill="#334155">• 바닥 STS 그레이팅 트렌치 포집 ⟶ 세척수 85% 이상 회수 및 폐수처리장 이송</text>
</svg>''',

    25: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">정화조 관리층 3종 음압 탈취 시스템 및 2단 약액세정탑 상세도</text>

  <rect x="60" y="80" width="280" height="110" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="200" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">정화조실 (음압 -20Pa 유지)</text>
  <text x="200" y="130" text-anchor="middle" font-size="10" fill="#334155">황화수소(H2S) / 메탄(CH4) 포집 후드</text>
  <text x="200" y="150" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">방폭 가스감지 센서 연동</text>

  <path d="M 340 135 L 430 135" stroke="#0284c7" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
  <text x="385" y="125" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">FRP 덕트</text>

  <rect x="430" y="70" width="310" height="130" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="585" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">2단 약액세정 및 활성탄 탈취탑</text>
  <text x="450" y="120" font-size="10" fill="#334155">1단계: 산/알칼리 약품 세정 (스크러버)</text>
  <text x="450" y="140" font-size="10" fill="#334155">2단계: 고성능 첨착 활성탄 흡착 베드</text>
  <text x="450" y="160" font-size="10" font-weight="bold" fill="#15803d">최종 배출: 복합악취 희석배수 ≤ 500 이하</text>

  <rect x="60" y="215" width="680" height="60" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="80" y="240" font-size="11" font-weight="bold" fill="#0f172a">■ 밀폐공간 안전 및 악취 누출 100% 차단</text>
  <text x="80" y="260" font-size="11" fill="#334155">• 출입문 개폐 시에도 외부 공기가 안으로만 빨려 들어가는 3종 음압 환기(15~20회/h)</text>
</svg>''',

    26: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">STS 호스릴 옥내소화전설비(분말소화기 내장) 구조 및 방수압 상세도</text>

  <rect x="80" y="75" width="260" height="140" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="210" y="100" text-anchor="middle" font-size="13" font-weight="bold" fill="#991b1b">STS304 호스릴 소화전함</text>
  
  <circle cx="210" cy="140" r="30" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
  <text x="210" y="145" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">호스릴(25m)</text>

  <rect x="110" y="185" width="200" height="20" fill="#dc2626" rx="2"/>
  <text x="210" y="198" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">ABC 분말소화기 3.3kg 2대</text>

  <rect x="380" y="75" width="360" height="140" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="560" y="100" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">소화전 방수 성능 기준 (NFTC 102)</text>
  <text x="400" y="125" font-size="11" fill="#334155">• 노즐 방수압력: 0.17 MPa 이상 ~ 0.7 MPa 이하</text>
  <text x="400" y="145" font-size="11" fill="#334155">• 정격 방수량: ≥ 130 L/min (20분 이상 방수수량)</text>
  <text x="400" y="165" font-size="11" fill="#334155">• 1인 조작성: 호스 전개 인장력 ≤ 5kgf</text>
  <text x="400" y="185" font-size="11" font-weight="bold" fill="#15803d">• 배치 기준: 보행거리 25m 이내 전수 배치</text>

  <rect x="80" y="230" width="660" height="45" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="400" y="257" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">✔ 기존 일반 소화전 대비 혼자서도 즉시 방수 가능한 호스릴 시스템 전면 적용</text>
</svg>''',

    27: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">연결송수관설비 ↔ 스프링클러 주배관·송수구 물리적 완전 분리 계통도</text>

  <rect x="60" y="80" width="310" height="125" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="215" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">1. 연결송수관설비 (독립 관로)</text>
  <text x="80" y="130" font-size="10" fill="#334155">• 고압 스케줄 탄소강관 (Sch 40)</text>
  <text x="80" y="150" font-size="10" fill="#334155">• 소방차 전용 독립 쌍구형 송수구</text>
  <text x="80" y="170" font-size="10" font-weight="bold" fill="#1d4ed8">• 2.0 MPa 고압 내력 시험 합격</text>

  <rect x="430" y="80" width="310" height="125" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="585" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#991b1b">2. 스프링클러설비 (독립 관로)</text>
  <text x="450" y="130" font-size="10" fill="#334155">• 알람밸브(유수검지장치) 전용 배관</text>
  <text x="450" y="150" font-size="10" fill="#334155">• 스프링클러 전용 옥외 송수구 분리</text>
  <text x="450" y="170" font-size="10" font-weight="bold" fill="#991b1b">• 1.5 MPa 내압 시험 합격</text>

  <line x1="370" y1="140" x2="430" y2="140" stroke="#dc2626" stroke-width="3" stroke-dasharray="4,4"/>
  <text x="400" y="135" text-anchor="middle" font-size="12" font-weight="bold" fill="#dc2626">✕</text>
  <text x="400" y="155" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">겸용 금지</text>

  <rect x="60" y="220" width="680" height="55" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="252" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 개정 화재안전기준 100% 준수 ⟶ 소방차 고압 가압 시 스프링클러 파손 원천 차단</text>
</svg>''',

    28: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">변전소·전기실 큐비클 내부 고체에어로졸 자동소화장치 상세도</text>

  <rect x="80" y="70" width="300" height="150" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="230" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">특고압/저압 수배전반 큐비클</text>

  <rect x="180" y="105" width="100" height="30" rx="4" fill="#dc2626"/>
  <text x="230" y="125" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">고체에어로졸 소화기</text>

  <path d="M 230 135 L 180 180 M 230 135 L 230 190 M 230 135 L 280 180" stroke="#ea580c" stroke-width="2.5" stroke-dasharray="3,2"/>
  <text x="230" y="210" text-anchor="middle" font-size="9" font-weight="bold" fill="#ea580c">초미세 소화 입자 방출 (3초 진압)</text>

  <rect x="420" y="70" width="320" height="150" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="580" y="95" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">고체에어로졸 소화 성능</text>
  <text x="440" y="125" font-size="11" fill="#334155">• KFI 소공간용 자동소화장치 인증품</text>
  <text x="440" y="145" font-size="11" fill="#334155">• 비전도성 친환경 약제 (전기 기기 손상 0%)</text>
  <text x="440" y="165" font-size="11" font-weight="bold" fill="#dc2626">• 소화기 작동 즉시 주차단기(ACB) 자동 트립</text>
  <text x="440" y="185" font-size="11" fill="#334155">• 본선 31개 역사 및 차량기지 전수 설치</text>

  <rect x="80" y="235" width="660" height="40" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="400" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">■ 판넬 내부 전기 화재 발생 시 3초 이내 초기 진압 ⟶ 대형 변전실 전소 방지</text>
</svg>''',

    29: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">변전실 가스소화구역 과압배출구(P.R.D) 댐퍼 작동 메커니즘</text>

  <rect x="150" y="80" width="500" height="40" fill="#94a3b8"/>
  <text x="400" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">방화벽체 (2시간 내화 콘크리트)</text>

  <rect x="320" y="80" width="160" height="40" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
  <text x="400" y="105" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">P.R.D 댐퍼 프레임</text>

  <path d="M 350 120 L 380 160" stroke="#dc2626" stroke-width="3"/>
  <circle cx="390" cy="170" r="10" fill="#334155"/>
  <text x="420" y="175" font-size="10" font-weight="bold" fill="#334155">카운터웨이트 추</text>

  <rect x="60" y="185" width="680" height="85" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="80" y="210" font-size="12" font-weight="bold" fill="#15803d">과압배출 댐퍼 작동 기준 (NFPA 2001)</text>
  <text x="80" y="235" font-size="11" fill="#334155">• 가스 방출 시 실내 압력 200Pa 도달 즉시 댐퍼 블레이드 자동 개방 ⟶ 벽체 파손 방지</text>
  <text x="80" y="255" font-size="11" fill="#334155">• 과압 해소 후 자중으로 즉시 닫혀 소화약제 설계 농도 10분 이상 유지</text>
</svg>''',

    30: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">소방펌프실 가설 및 3대 필수 성능시험(체절·정격·150% 부하) 곡선도</text>

  <rect x="60" y="75" width="280" height="135" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="200" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">소방펌프실 주요 배관 구성</text>
  <text x="80" y="125" font-size="10" fill="#334155">• 주펌프(다단원심) + 충압펌프(보조)</text>
  <text x="80" y="145" font-size="10" fill="#334155">• 오리피스 유량계 성능시험배관</text>
  <text x="80" y="165" font-size="10" fill="#334155">• D20 순환배관 + 릴리프밸브</text>
  <text x="80" y="185" font-size="10" fill="#334155">• 압력챔버 기압수조 자동기동</text>

  <rect x="360" y="75" width="380" height="135" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="550" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#854d0e">3대 법정 성능시험 합격 기준</text>
  <text x="380" y="125" font-size="10" fill="#334155">1. 체절운전: 밸브 폐쇄 시 압력 ≤ 정격의 140%</text>
  <text x="380" y="145" font-size="10" fill="#334155">2. 정격부하: 100% 유량 시 정격압력 ≥ 100%</text>
  <text x="380" y="165" font-size="10" fill="#334155">3. 피크부하: 150% 유량 시 정격압력 ≥ 65%</text>
  <text x="380" y="185" font-size="10" font-weight="bold" fill="#dc2626">4. 릴리프밸브: 체절압력 미만에서 정확히 개방</text>

  <rect x="60" y="225" width="680" height="45" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="252" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 소방감리원 및 관할 소방서 입회 하에 3대 성능시험 100% 합격 검증 완료</text>
</svg>''',

    31: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">정거장 MRL 인승용 승강기(17/24인승) 및 한국승강기안전공단 검사</text>

  <rect x="80" y="75" width="280" height="135" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="220" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">MRL 기계실 없는 권상기</text>
  <text x="100" y="125" font-size="10" fill="#334155">• PMSM 영구자석 기어리스 권상기</text>
  <text x="100" y="145" font-size="10" fill="#334155">• 승강로 수직도 오차 ≤ ±5mm</text>
  <text x="100" y="165" font-size="10" fill="#334155">• 가이드레일 단차 ≤ 0.05mm</text>
  <text x="100" y="185" font-size="10" fill="#334155">• 승차감 진동 ≤ 15 gal 달성</text>

  <rect x="380" y="75" width="360" height="135" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="560" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">4대 핵심 안전장치 연동</text>
  <text x="400" y="125" font-size="10" fill="#334155">• 128채널 3D 다점 적외선 도어센서</text>
  <text x="400" y="145" font-size="10" fill="#334155">• 정전 시 자동 착상 구출장치(ARD)</text>
  <text x="400" y="165" font-size="10" fill="#334155">• 조속기 및 비상정지장치(Safety Gear)</text>
  <text x="400" y="185" font-size="10" font-weight="bold" fill="#15803d">• 2중 비상통화장치 (24h 방재실 연결)</text>

  <rect x="80" y="225" width="660" height="45" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="400" y="252" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">■ 한국승강기안전공단(KoELSA) 완성검사 100% 합격 ⟶ 법정 운행 필증 획득</text>
</svg>''',

    32: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">차량기지 종합검수고 관통형(양방향 도어) 3~5ton 화물용 EV 상세도</text>

  <rect x="100" y="80" width="600" height="110" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>
  <text x="400" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">화물용 대형 승강로 (정격 적재 3,000 ~ 5,000kg)</text>

  <rect x="120" y="115" width="80" height="60" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="160" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#991b1b">전면 도어<br>(Front Door)</text>

  <rect x="220" y="115" width="360" height="60" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">지게차 진입 바닥 H형강 + 4.5T 체크플레이트 보강</text>

  <rect x="600" y="115" width="80" height="60" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="640" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#991b1b">후면 도어<br>(Rear Door)</text>

  <rect x="100" y="205" width="600" height="65" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="120" y="230" font-size="11" font-weight="bold" fill="#15803d">■ 관통형(Through Type) 화물 운반 메커니즘</text>
  <text x="120" y="250" font-size="11" fill="#334155">• 지게차가 1층에서 자재 적재 진입 ⟶ 2층 자재창고에서 회전 없이 반대편 문으로 직진 퇴출</text>
</svg>''',

    33: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">직접디지털제어(DDC/IP DDC) 아키텍처 및 백업 서버 무중단 이중화</text>

  <rect x="60" y="75" width="220" height="110" rx="6" fill="#0f172a"/>
  <text x="170" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#38bdf8">중앙 관제 메인 서버</text>
  <text x="170" y="130" text-anchor="middle" font-size="10" fill="#94a3b8">Active Mode (실시간 관제)</text>
  <text x="170" y="155" text-anchor="middle" font-size="10" fill="#22c55e">● Normal Running</text>

  <rect x="520" y="75" width="220" height="110" rx="6" fill="#1e293b"/>
  <text x="630" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#facc15">중앙 관제 백업 서버</text>
  <text x="630" y="130" text-anchor="middle" font-size="10" fill="#94a3b8">Standby Mode (실시간 미러링)</text>
  <text x="630" y="155" text-anchor="middle" font-size="10" fill="#facc15">● 0초 자동 절환 대기</text>

  <path d="M 280 130 L 520 130" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,4"/>
  <text x="400" y="120" text-anchor="middle" font-size="10" font-weight="bold" fill="#0284c7">Heartbeat 이중화 동기화</text>

  <rect x="60" y="205" width="680" height="65" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="80" y="230" font-size="11" font-weight="bold" fill="#0f172a">■ IP DDC 필드 제어반 및 국제표준 BACnet 프로토콜 연동</text>
  <text x="80" y="250" font-size="11" fill="#334155">• 공조기, 환기팬, 펌프, 밸브 수천 개 I/O 포인트 Point-to-Point 100% 일치 검증</text>
</svg>''',

    34: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">화재수신반 경보 연동 공조기 즉시 정지 및 제연팬 배연 모드 자동 인터록</text>

  <rect x="50" y="80" width="160" height="85" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="130" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#991b1b">1. 화재 감지</text>
  <text x="130" y="125" text-anchor="middle" font-size="10" fill="#334155">연기/열 감지기</text>
  <text x="130" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">화재 수신반 경보</text>

  <path d="M 210 122 L 290 122" stroke="#dc2626" stroke-width="3" fill="none" marker-end="url(#arrow)"/>

  <rect x="290" y="80" width="200" height="85" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
  <text x="390" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#854d0e">2. 공조기 전원 차단</text>
  <text x="390" y="125" text-anchor="middle" font-size="10" fill="#334155">MCC 마그네틱 B접점</text>
  <text x="390" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">3초 내 100% 즉시 정지</text>

  <path d="M 490 122 L 560 122" stroke="#16a34a" stroke-width="3" fill="none" marker-end="url(#arrow)"/>

  <rect x="560" y="80" width="190" height="85" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="655" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">3. 제연팬 자동 기동</text>
  <text x="655" y="125" text-anchor="middle" font-size="10" fill="#334155">제연댐퍼 자동 개방</text>
  <text x="655" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#15803d">고온 유독가스 배연</text>

  <rect x="50" y="195" width="700" height="75" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="70" y="220" font-size="11" font-weight="bold" fill="#0f172a">■ 하드와이어드(Hardwired) 물리적 안전 인터록 검증</text>
  <text x="70" y="240" font-size="11" fill="#334155">• DDC 컴퓨터 통신 에러 발생 시에도 순수 전기적 릴레이 신호로 공조기 무조건 강제 차단</text>
  <text x="70" y="260" font-size="11" fill="#334155">• 관할 소방서 입회 실부하 화재 모의 연동 시험 100% 합격</text>
</svg>''',

    35: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">공조 덕트 및 수배관 TAB(풍량/수량 밸런싱) 정밀 측정·조정</text>

  <rect x="60" y="75" width="320" height="120" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="220" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">1. 공조 덕트 풍량 TAB</text>
  <text x="80" y="125" font-size="10" fill="#334155">• 피토관 주풍량 측정 및 볼륨댐퍼(VD) 조정</text>
  <text x="80" y="145" font-size="10" fill="#334155">• 플로우 후드 이용 디퓨저 취출 풍량 측정</text>
  <text x="80" y="165" font-size="10" font-weight="bold" fill="#1d4ed8">• 설계 풍량 대비 오차율 ≤ ±10% 이내 교정</text>

  <rect x="420" y="75" width="320" height="120" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="580" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">2. 수배관 유량 TAB</text>
  <text x="440" y="125" font-size="10" fill="#334155">• 초음파 비파괴 유량계 실제 통수량 실측</text>
  <text x="440" y="145" font-size="10" fill="#334155">• 밸런싱 밸브 차압(ΔP) 조절 코일 유량 배분</text>
  <text x="440" y="165" font-size="10" font-weight="bold" fill="#15803d">• 펌프 양정 및 수배관 저항 밸런싱 완료</text>

  <rect x="60" y="210" width="680" height="60" rx="4" fill="#fefce8" stroke="#ca8a04" stroke-width="1"/>
  <text x="400" y="235" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">✔ 실내 소음(NC 35~40) 및 실별 온·습도 균일도 100% 입증 공인 TAB 보고서 획득</text>
</svg>''',

    36: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">소방시설 완공검사필증 획득 및 시설물 종합 인수인계 마스터 플랜</text>

  <rect x="60" y="75" width="200" height="95" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="160" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">1. 소방 완공필증 획득</text>
  <text x="80" y="125" font-size="10" fill="#334155">• 관할 소방서 합동 실사</text>
  <text x="80" y="145" font-size="10" fill="#334155">• 소방 완공검사증명서 수령</text>

  <rect x="300" y="75" width="200" height="95" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">2. As-Built 준공도서</text>
  <text x="320" y="125" font-size="10" fill="#334155">• 2D/3D 최종 준공도면</text>
  <text x="320" y="145" font-size="10" fill="#334155">• 시운전 성적서 및 매뉴얼</text>

  <rect x="540" y="75" width="200" height="95" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
  <text x="640" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#854d0e">3. 예비품 &amp; 운영자 교육</text>
  <text x="560" y="125" font-size="10" fill="#334155">• 2년분 유지관리 예비품</text>
  <text x="560" y="145" font-size="10" fill="#334155">• 40시간 이상 실무 교육</text>

  <path d="M 260 122 L 300 122" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 500 122 L 540 122" stroke="#0284c7" stroke-width="2" fill="none"/>

  <rect x="60" y="190" width="680" height="85" rx="4" fill="#0f172a"/>
  <text x="400" y="215" text-anchor="middle" font-size="13" font-weight="bold" fill="#38bdf8">화성도시공사 기계·소방 운영유지관리팀 무결점 최종 인수인계 완료</text>
  <text x="400" y="240" text-anchor="middle" font-size="11" fill="#ffffff">✔ 시설물 안전성 100% 입증 | ✔ 법적 인허가 준공 필증 완비 | ✔ 시민 안전 운행 보장</text>
</svg>'''
}

print(f"기계설비 전용 SVG 도식 Part 2 (19~36번): {len(MECH_SVGS_PART2)}개 로드 완료!")
