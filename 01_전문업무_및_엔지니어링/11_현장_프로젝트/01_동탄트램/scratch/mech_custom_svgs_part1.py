# -*- coding: utf-8 -*-
"""
동탄트램 기계설비·소방설비 1~18번 액티비티 1:1 전용 고해상도 2D 기술도식 (Light Theme 준수)
"""

MECH_SVGS_PART1 = {
    1: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">동탄트램 기계·소방설비 설계적정성 검토 및 부하계산 삼각 대조도</text>
  
  <rect x="50" y="70" width="200" height="90" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="150" y="95" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">1. 공조/환기 부하계산서</text>
  <text x="150" y="120" text-anchor="middle" font-size="11" fill="#334155">정거장 대합실/승강장 부하</text>
  <text x="150" y="140" text-anchor="middle" font-size="11" fill="#334155">변전실 열량 배출(≤40℃, 10회/h)</text>

  <rect x="300" y="70" width="200" height="90" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>
  <text x="400" y="95" text-anchor="middle" font-size="13" font-weight="bold" fill="#1d4ed8">2. 설계도면 &amp; 특기시방서</text>
  <text x="400" y="120" text-anchor="middle" font-size="11" fill="#334155">KDS 47 철도설계기준 매핑</text>
  <text x="400" y="140" text-anchor="middle" font-size="11" fill="#334155">배관/덕트 관경 및 재질(STS/GI)</text>

  <rect x="550" y="70" width="200" height="90" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="650" y="95" text-anchor="middle" font-size="13" font-weight="bold" fill="#a16207">3. 수량산출서 &amp; 공사내역서</text>
  <text x="650" y="120" text-anchor="middle" font-size="11" fill="#334155">장비일람표 수량 1:1 대조</text>
  <text x="650" y="140" text-anchor="middle" font-size="11" fill="#334155">변전소 냉난방기 3대 수량 일치</text>

  <path d="M 250 115 L 300 115" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)" fill="none"/>
  <path d="M 500 115 L 550 115" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)" fill="none"/>

  <rect x="100" y="190" width="600" height="85" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="400" y="215" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">삼각 교차 대조 및 검증 결과 (종합 개선안)</text>
  <text x="120" y="240" font-size="11" font-weight="bold" fill="#047857">✔ 법적 기준: NFTC/NFPC 화재안전기준 및 도시철도건설규칙 제67조 100% 충족</text>
  <text x="120" y="260" font-size="11" font-weight="bold" fill="#0284c7">✔ 인터페이스: 건축 방화슬리브, 전기 NFR-8 내화케이블, 신호 배수공동구 선반영</text>
</svg>''',

    2: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">동탄트램 기계·소방 발주전략 킥오프 회의(KOM) 및 책임 체계도</text>

  <circle cx="150" cy="130" r="55" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="150" y="125" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">발주처 / 감리단</text>
  <text x="150" y="145" text-anchor="middle" font-size="10" fill="#334155">품질검측·공정승인</text>

  <circle cx="400" cy="130" r="55" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="125" text-anchor="middle" font-size="13" font-weight="bold" fill="#1d4ed8">원도급 시공사</text>
  <text x="400" y="145" text-anchor="middle" font-size="10" fill="#334155">공정총괄·인터페이스</text>

  <circle cx="650" cy="130" r="55" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
  <text x="650" y="125" text-anchor="middle" font-size="13" font-weight="bold" fill="#a16207">기계/소방 협력사</text>
  <text x="650" y="145" text-anchor="middle" font-size="10" fill="#334155">정밀시공·자재조달</text>

  <line x1="205" y1="130" x2="345" y2="130" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="455" y1="130" x2="595" y2="130" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,4"/>

  <rect x="50" y="210" width="700" height="70" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="235" font-size="11" font-weight="bold" fill="#0f172a">■ 4대 핵심 마일스톤 확정</text>
  <text x="70" y="255" font-size="11" fill="#334155">1) 3D BIM 간섭해소 ⟶ 2) 주요 장비(AHU/승강기) FAT 공장검수 ⟶ 3) 수압/기밀시험 ⟶ 4) 소방 완공검사</text>
</svg>''',

    3: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">LOD 350 기반 3D BIM 기계/소방/전기/건축 복합 간섭 해결 단면도</text>

  <rect x="60" y="70" width="680" height="30" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
  <text x="400" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#334155">지하 정거장 콘크리트 슬래브 (Slab Level)</text>

  <rect x="80" y="115" width="280" height="40" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="220" y="140" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">공조 메인 덕트 (상단 배치)</text>

  <rect x="420" y="125" width="180" height="20" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="510" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#991b1b">소화 주배관 (D100)</text>

  <rect x="120" y="175" width="220" height="25" rx="3" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
  <text x="230" y="192" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">전기 케이블 트레이 (하단 분리)</text>

  <line x1="60" y1="230" x2="740" y2="230" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="400" y="222" text-anchor="middle" font-size="11" font-weight="bold" fill="#475569">천장 마감선 (Ceiling Line : 유효 천장고 CH ≥ 2.7m 100% 확보)</text>

  <rect x="60" y="245" width="680" height="40" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="270" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 간섭 체크 엔진(Navisworks) 가동 결과: Hard Clash 0건, 시공상세도(CSD) 100% 승인</text>
</svg>''',

    4: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">소방시설 착공신고 및 환경 인허가 행정 추진 체계도</text>

  <rect x="60" y="75" width="150" height="75" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="135" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">1. 소방시설 착공신고</text>
  <text x="135" y="125" text-anchor="middle" font-size="10" fill="#334155">관할소방서(화성소방서)</text>

  <rect x="235" y="75" width="150" height="75" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="310" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#b91c1c">2. 소방 건축동의</text>
  <text x="310" y="125" text-anchor="middle" font-size="10" fill="#334155">주배관 분리/호스릴</text>

  <rect x="410" y="75" width="150" height="75" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="485" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#a16207">3. 위험물 저장 허가</text>
  <text x="485" y="125" text-anchor="middle" font-size="10" fill="#334155">비상발전기 유류탱크</text>

  <rect x="585" y="75" width="155" height="75" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="662" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">4. 오수/폐수 신고</text>
  <text x="662" y="125" text-anchor="middle" font-size="10" fill="#334155">차량기지 폐수처리장</text>

  <path d="M 210 112 L 235 112" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 385 112 L 410 112" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 560 112 L 585 112" stroke="#0284c7" stroke-width="2" fill="none"/>

  <rect x="60" y="175" width="680" height="100" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="400" y="200" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">법적 인허가 관리 및 준공 연계 성과</text>
  <text x="80" y="225" font-size="11" fill="#334155">• 소방시설공사업법 제13조에 의거 소방감리원 배치신고 및 착공신고 필증 수령 완료</text>
  <text x="80" y="245" font-size="11" fill="#334155">• 위험물안전관리법에 따른 유류저장탱크 방유제 용량(110%) 및 자동소화설비 완비</text>
  <text x="80" y="265" font-size="11" fill="#334155">• 물환경보전법 폐수배출시설 설치신고 완료 ⟶ 지연 리스크 0일 달성</text>
</svg>''',

    5: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">지하 기계실 대형 장비 반입 개구부(DA) 및 양중 크레인 작업도</text>

  <rect x="60" y="140" width="300" height="130" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="210" y="165" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">지하 기계실 (B2F Level)</text>

  <rect x="130" y="180" width="160" height="70" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="210" y="210" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">공기조화기(AHU) / 펌프</text>
  <text x="210" y="230" text-anchor="middle" font-size="9" fill="#475569">운반 롤러 이동 (수평 반입)</text>

  <rect x="260" y="70" width="90" height="70" fill="#ffffff" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,4"/>
  <text x="305" y="105" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">DA 개구부</text>
  <text x="305" y="120" text-anchor="middle" font-size="9" fill="#dc2626">(W2.5 x L4.0m)</text>

  <path d="M 580 80 L 320 80 L 305 180" stroke="#d97706" stroke-width="2.5" stroke-dasharray="5,3" fill="none"/>
  
  <rect x="480" y="140" width="240" height="130" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="600" y="165" text-anchor="middle" font-size="12" font-weight="bold" fill="#854d0e">양중 크레인 안전 기준</text>
  <text x="500" y="195" font-size="11" fill="#334155">• 하이드로 크레인(50ton) 작업반경</text>
  <text x="500" y="215" font-size="11" fill="#334155">• 아웃트리거 복공판 보강 (K30≥150)</text>
  <text x="500" y="235" font-size="11" fill="#334155">• 인양 안전율 ≥ 1.25 확보</text>
  <text x="500" y="255" font-size="11" fill="#334155">• 신호수 2인 1조 무전기 통제</text>
</svg>''',

    6: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">7대 공종 합동 Big Room 인터페이스 협업 및 시공 우선순위</text>

  <rect x="300" y="110" width="200" height="70" rx="35" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="400" y="140" text-anchor="middle" font-size="14" font-weight="bold" fill="#ffffff">기계 · 소방설비</text>
  <text x="400" y="160" text-anchor="middle" font-size="10" fill="#38bdf8">Big Room 협의체</text>

  <rect x="50" y="70" width="130" height="40" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1"/>
  <text x="115" y="95" text-anchor="middle" font-size="11" font-weight="bold" fill="#1d4ed8">1. 건축 (슬리브/방화)</text>

  <rect x="50" y="180" width="130" height="40" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1"/>
  <text x="115" y="205" text-anchor="middle" font-size="11" font-weight="bold" fill="#b91c1c">2. 전기 (내화케이블)</text>

  <rect x="620" y="70" width="130" height="40" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1"/>
  <text x="685" y="95" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">3. 신호 (선로배수구)</text>

  <rect x="620" y="180" width="130" height="40" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1"/>
  <text x="685" y="205" text-anchor="middle" font-size="11" font-weight="bold" fill="#a16207">4. 궤도/토목 (매설)</text>

  <line x1="180" y1="90" x2="300" y2="130" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="180" y1="200" x2="300" y2="160" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="620" y1="90" x2="500" y2="130" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="620" y1="200" x2="500" y2="160" stroke="#94a3b8" stroke-width="1.5"/>

  <rect x="50" y="245" width="700" height="40" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="400" y="270" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">■ 시공 순서 룰: 슬리브 선매립(건축) ⟶ 대형 풍도/주배관(기계) ⟶ 케이블트레이(전기/통신) ⟶ 마감</text>
</svg>''',

    7: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">트램 본선 도로 하부 지하매설 기계배관 및 지장물 이격 단면도</text>

  <rect x="50" y="70" width="700" height="25" fill="#64748b" stroke="#475569" stroke-width="1"/>
  <text x="400" y="87" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">아스팔트 도로 포장면 (GL ±0.0m)</text>

  <rect x="70" y="130" width="660" height="5" fill="#3b82f6"/>
  <text x="400" y="122" text-anchor="middle" font-size="10" font-weight="bold" fill="#2563eb">▼ 식별용 배관 경고테이프 매설 (GL -0.5m)</text>

  <circle cx="180" cy="200" r="30" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="180" y="195" text-anchor="middle" font-size="10" font-weight="bold" fill="#1e40af">상수도관</text>
  <text x="180" y="210" text-anchor="middle" font-size="9" fill="#1e40af">STS D150</text>

  <circle cx="380" cy="200" r="30" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="380" y="195" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">도시가스관</text>
  <text x="380" y="210" text-anchor="middle" font-size="9" fill="#92400e">기존 지장물</text>

  <circle cx="580" cy="200" r="30" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="580" y="195" text-anchor="middle" font-size="10" font-weight="bold" fill="#15803d">지열 PE관</text>
  <text x="580" y="210" text-anchor="middle" font-size="9" fill="#15803d">KSM 3408</text>

  <line x1="210" y1="200" x2="350" y2="200" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,3"/>
  <text x="280" y="190" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">이격 ≥ 300mm</text>

  <line x1="410" y1="200" x2="550" y2="200" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,3"/>
  <text x="480" y="190" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">이격 ≥ 300mm</text>

  <rect x="50" y="250" width="700" height="35" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="400" y="272" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">■ 기초: 모래 부설(100mm) + 되메우기 다짐도 ≥ 95% + 3D GPR 측량 좌표 GIS 등록</text>
</svg>''',

    8: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">기계설비 시공계획 및 WPS 용접/수압 품질보증 프로세스</text>

  <rect x="50" y="80" width="150" height="80" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="125" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">1. 시공계획서 수립</text>
  <text x="125" y="130" text-anchor="middle" font-size="10" fill="#334155">공종별 절차서/인원/장비</text>
  <text x="125" y="145" text-anchor="middle" font-size="10" fill="#334155">KCS 41 시방 기준</text>

  <rect x="230" y="80" width="150" height="80" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="305" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#a16207">2. WPS 용접 승인</text>
  <text x="305" y="130" text-anchor="middle" font-size="10" fill="#334155">유자격 용접사 검증</text>
  <text x="305" y="145" text-anchor="middle" font-size="10" fill="#334155">TIG + 아크 다층용접</text>

  <rect x="410" y="80" width="150" height="80" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="485" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#b91c1c">3. 비파괴검사(NDT)</text>
  <text x="485" y="130" text-anchor="middle" font-size="10" fill="#334155">방사선투과(RT ≥ 10%)</text>
  <text x="485" y="145" text-anchor="middle" font-size="10" fill="#334155">내부 결함 전수 색출</text>

  <rect x="590" y="80" width="150" height="80" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="665" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">4. 1.5배 수압시험</text>
  <text x="665" y="130" text-anchor="middle" font-size="10" fill="#334155">1.5MPa 60분 유지</text>
  <text x="665" y="145" text-anchor="middle" font-size="10" fill="#334155">누수 0건 감리 승인</text>

  <path d="M 200 120 L 230 120" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 380 120 L 410 120" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 560 120 L 590 120" stroke="#0284c7" stroke-width="2" fill="none"/>

  <rect x="50" y="180" width="690" height="90" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="400" y="205" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">■ 밀폐공간 및 화기작업 안전 통제</text>
  <text x="80" y="230" font-size="11" fill="#334155">• 지하 집수조/정화조: 복합가스(O2, H2S, CH4) 측정 + 송기마스크 착용 + 감시원 1인 상주</text>
  <text x="80" y="250" font-size="11" fill="#334155">• 배관 용접 시: 반경 11m 이내 가연물 제거 + 불꽃방지포 덮개 + ABC 소화기 2대 비치</text>
</svg>''',

    9: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">주요 기계·소방 기자재 검수 기준 및 공장검수(FAT) 체계</text>

  <rect x="50" y="75" width="320" height="95" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="210" y="100" text-anchor="middle" font-size="13" font-weight="bold" fill="#1d4ed8">1. STS 강관 검수 (KSD 3595/3576)</text>
  <text x="70" y="125" font-size="11" fill="#334155">• 밀시트(Mill Sheet) 화학성분(Ni, Cr) 100% 대조</text>
  <text x="70" y="145" font-size="11" fill="#334155">• 파이프 두께 및 진원도 마이크로미터 전수 검측</text>

  <rect x="410" y="75" width="330" height="95" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="575" y="100" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">2. 인버터 부스터펌프 공장검수(FAT)</text>
  <text x="430" y="125" font-size="11" fill="#334155">• IE3 프리미엄 고효율 모터 시험성적서</text>
  <text x="430" y="145" font-size="11" fill="#334155">• 정격 양정, 유량 및 인버터 가압 제어 시운전</text>

  <rect x="50" y="190" width="690" height="85" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="400" y="215" text-anchor="middle" font-size="13" font-weight="bold" fill="#a16207">3. 현장 반입 봉인 확인 및 불합격품 통제</text>
  <text x="80" y="240" font-size="11" fill="#334155">• 배관 단부 보호 플라스틱 캡(Cap) 체결 상태 및 KFI 인증 명판 확인</text>
  <text x="80" y="260" font-size="11" fill="#334155">• 불합격 자재 발생 시 '부적합' 붉은색 라벨 부착 및 24시간 이내 현장 반출</text>
</svg>''',

    10: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">방화구획 슬래브/벽체 관통부 내화채움구조(내화충진재) 상세도</text>

  <rect x="150" y="70" width="500" height="35" fill="#94a3b8" stroke="#64748b" stroke-width="1.5"/>
  <text x="400" y="92" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">콘크리트 방화벽체 (2시간 내화구조)</text>

  <rect x="330" y="70" width="140" height="35" fill="#cbd5e1"/>
  <text x="400" y="92" text-anchor="middle" font-size="10" font-weight="bold" fill="#1e293b">관통 슬리브</text>

  <rect x="50" y="130" width="700" height="50" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="160" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">관통 배관 / 공조 덕트 (Pipe / Duct)</text>

  <rect x="330" y="115" width="140" height="80" rx="4" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
  <text x="400" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">고밀도 미네랄울</text>
  <text x="400" y="165" text-anchor="middle" font-size="9" fill="#854d0e">(밀도 ≥ 100kg/㎥)</text>

  <rect x="310" y="110" width="20" height="90" fill="#dc2626" rx="2"/>
  <rect x="470" y="110" width="20" height="90" fill="#dc2626" rx="2"/>
  <text x="320" y="215" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">방화실란트</text>
  <text x="480" y="215" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">방화실란트</text>

  <rect x="50" y="240" width="700" height="45" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="267" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 우레탄폼 사용 전면 금지 ⟶ 공인기관 차열/차염 2시간 인증 내화채움구조 100% 시공</text>
</svg>''',

    11: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">본선/차량기지 143개소 선로전환기 하부 배수관로 공동구 연계도</text>

  <rect x="100" y="80" width="600" height="20" fill="#94a3b8"/>
  <text x="400" y="95" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">트램 레일 및 콘크리트 도상 (Track Level)</text>

  <rect x="250" y="110" width="300" height="65" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="400" y="135" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e40af">선로전환기 (Point Machine 143개소)</text>
  <text x="400" y="155" text-anchor="middle" font-size="10" fill="#334155">모터 및 기어박스 방수/침수 방지 구역</text>

  <rect x="360" y="175" width="80" height="30" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5"/>
  <text x="400" y="195" text-anchor="middle" font-size="10" font-weight="bold" fill="#9a3412">드레인 피트</text>

  <path d="M 400 205 L 400 245 L 680 245" stroke="#0284c7" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
  <text x="540" y="235" text-anchor="middle" font-size="10" font-weight="bold" fill="#0284c7">횡단 배수관 (D100/150, i≥1.0%)</text>

  <rect x="50" y="260" width="700" height="35" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="282" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 궤도 타설 전 선시공 ⟶ 동절기 전환기 결빙 및 폭우 시 침수 고장 원천 차단</text>
</svg>''',

    12: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">소방 기계설비 비상전원 간선 및 NFR-8 내화배선 체계도</text>

  <rect x="50" y="80" width="160" height="80" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="130" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">수변전실 / ATS</text>
  <text x="130" y="130" text-anchor="middle" font-size="10" fill="#334155">상용전원 + 비상발전기</text>
  <text x="130" y="145" text-anchor="middle" font-size="10" fill="#334155">10초 이내 자동절환</text>

  <path d="M 210 120 L 300 120" stroke="#dc2626" stroke-width="3" fill="none"/>
  <text x="255" y="110" text-anchor="middle" font-size="9" font-weight="bold" fill="#dc2626">NFR-8 내화케이블</text>

  <rect x="300" y="80" width="180" height="80" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="390" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#b91c1c">소방동력 MCC 제어반</text>
  <text x="390" y="130" text-anchor="middle" font-size="10" fill="#334155">과부하 트립 차단 배제</text>
  <text x="390" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#b91c1c">(오직 경보만 출력)</text>

  <path d="M 480 120 L 570 120" stroke="#dc2626" stroke-width="3" fill="none"/>

  <rect x="570" y="80" width="170" height="80" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="655" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">소방 주펌프 / 제연팬</text>
  <text x="655" y="130" text-anchor="middle" font-size="10" fill="#334155">화재 시 전원 무중단</text>
  <text x="655" y="145" text-anchor="middle" font-size="10" fill="#334155">모터 연속 운전 보장</text>

  <rect x="50" y="190" width="690" height="85" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="70" y="215" font-size="11" font-weight="bold" fill="#0f172a">■ 전기 ↔ 소방 기계 인터페이스 핵심 수칙</text>
  <text x="70" y="235" font-size="11" fill="#334155">• NFR-8 고내열 케이블 전용 금속관 단독 배선 (일반 전선 혼재 전면 금지)</text>
  <text x="70" y="255" font-size="11" fill="#334155">• 소방펌프실 통합 접지 단자함(접지저항 ≤ 10Ω) 전기분야 일괄 시공 연계</text>
</svg>''',

    13: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">저수조 사수(死水)방지 흡입배관 및 소화수위 분리 계통도</text>

  <rect x="60" y="75" width="450" height="150" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="140" y="95" font-size="11" font-weight="bold" fill="#0369a1">STS304 패널형 저수조</text>

  <line x1="285" y1="75" x2="285" y2="225" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,4"/>
  <text x="285" y="150" text-anchor="middle" font-size="9" fill="#0369a1">중앙 칸막이</text>

  <line x1="60" y1="160" x2="510" y2="160" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="430" y="150" font-size="10" font-weight="bold" fill="#dc2626">▲ 소화용수 유효수위선</text>

  <path d="M 180 145 L 180 60 L 580 60 L 580 100" stroke="#16a34a" stroke-width="3" fill="none"/>
  <text x="380" y="50" text-anchor="middle" font-size="10" font-weight="bold" fill="#16a34a">급수펌프 흡입관 (소화수위 상단에 위치 ⟶ 사수 방지)</text>

  <path d="M 400 215 L 400 60 L 680 60 L 680 150" stroke="#dc2626" stroke-width="3" fill="none"/>
  <text x="680" y="50" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626">소방펌프 흡입관 (바닥 최하단)</text>

  <rect x="550" y="100" width="180" height="125" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="640" y="125" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">수배관 안전 메커니즘</text>
  <text x="560" y="150" font-size="10" fill="#334155">• 생활용수 고갈되어도</text>
  <text x="560" y="170" font-size="10" font-weight="bold" fill="#dc2626">• 소화수량 100% 자동 보존</text>
  <text x="560" y="190" font-size="10" fill="#334155">• 물고임 부패 원천 차단</text>
  <text x="560" y="210" font-size="10" fill="#334155">• 와류방지판(Vortex) 체결</text>
</svg>''',

    14: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">지열 신재생에너지 수직 밀폐형 U-Tube 배관 및 그라우팅 단면도</text>

  <rect x="100" y="70" width="600" height="20" fill="#854d0e"/>
  <text x="400" y="85" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">지표면 (Ground Level)</text>

  <rect x="200" y="90" width="80" height="180" fill="#fef08a" stroke="#ca8a04" stroke-width="1"/>
  <text x="240" y="180" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">천공공(150m)<br>벤토나이트<br>그라우팅</text>

  <path d="M 225 90 L 225 250 A 15 15 0 0 0 255 250 L 255 90" stroke="#2563eb" stroke-width="3" fill="none"/>
  <text x="240" y="265" text-anchor="middle" font-size="9" font-weight="bold" fill="#1e40af">U-Bend</text>

  <path d="M 225 90 L 450 90 L 450 140" stroke="#2563eb" stroke-width="2" fill="none"/>
  <path d="M 255 90 L 470 90 L 470 140" stroke="#dc2626" stroke-width="2" fill="none"/>

  <rect x="420" y="140" width="280" height="110" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="560" y="165" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">지열 히트펌프 기계실 연결</text>
  <text x="440" y="190" font-size="11" fill="#334155">• 고밀도 PE관 (KSM 3408, SDR 11)</text>
  <text x="440" y="210" font-size="11" fill="#334155">• 1.0 MPa 수압시험 2시간 무누수</text>
  <text x="440" y="230" font-size="11" fill="#334155">• 열전도도 ≥ 1.8 W/m·K 그라우팅</text>
</svg>''',

    15: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">정거장·변전소 환기덕트 및 B.D.D 기류역류방지댐퍼 상세도</text>

  <rect x="60" y="80" width="200" height="90" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="160" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">전기실/변전실 환기</text>
  <text x="160" y="130" text-anchor="middle" font-size="10" fill="#334155">1종 정압 (급기 가압)</text>
  <text x="160" y="150" text-anchor="middle" font-size="10" font-weight="bold" fill="#1d4ed8">10회/h 이상, 실온 ≤40℃</text>

  <rect x="540" y="80" width="200" height="90" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="640" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#b91c1c">화장실/샤워실 배기</text>
  <text x="640" y="130" text-anchor="middle" font-size="10" fill="#334155">3종 음압 (악취 차단)</text>
  <text x="640" y="150" text-anchor="middle" font-size="10" font-weight="bold" fill="#b91c1c">15~20회/h 배기</text>

  <rect x="300" y="80" width="200" height="90" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="400" y="110" text-anchor="middle" font-size="12" font-weight="bold" fill="#a16207">B.D.D 역류방지댐퍼</text>
  <text x="400" y="130" text-anchor="middle" font-size="10" fill="#334155">동절기 외기 침입 차단</text>
  <text x="400" y="150" text-anchor="middle" font-size="10" font-weight="bold" fill="#a16207">결로/열손실 100% 방지</text>

  <path d="M 260 125 L 300 125" stroke="#0284c7" stroke-width="2" fill="none"/>
  <path d="M 500 125 L 540 125" stroke="#0284c7" stroke-width="2" fill="none"/>

  <rect x="60" y="200" width="680" height="75" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <text x="80" y="225" font-size="11" font-weight="bold" fill="#0f172a">■ 덕트 제작 및 기밀 기준 (KCS 41 00 00)</text>
  <text x="80" y="245" font-size="11" fill="#334155">• 아연도금강판(GI) 피츠버그 록 이음 + 방진스프링 행거(간격 ≤2.0m) 시공</text>
  <text x="80" y="265" font-size="11" fill="#334155">• 연기발생기 덕트 기밀 누기시험 합격 ⟶ 에너지 효율 및 실내 공기질 확보</text>
</svg>''',

    16: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">250℃ 1시간 연속운전 고내열 제연팬 및 내화풍도 상세도</text>

  <rect x="60" y="80" width="220" height="110" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="170" y="110" text-anchor="middle" font-size="13" font-weight="bold" fill="#991b1b">250℃ 고내열 제연팬</text>
  <text x="80" y="135" font-size="10" fill="#334155">• KFI 공인 250℃/1h 내열인증</text>
  <text x="80" y="155" font-size="10" fill="#334155">• H종 내열 절연 모터</text>
  <text x="80" y="175" font-size="10" fill="#334155">• 알루미늄 합금 임펠러</text>

  <rect x="310" y="105" width="80" height="60" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="350" y="130" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">불연 내열</text>
  <text x="350" y="145" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">캔버스</text>

  <rect x="420" y="80" width="320" height="110" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="580" y="110" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">내화 제연 풍도 (Smoke Duct)</text>
  <text x="440" y="135" font-size="10" fill="#334155">• 1.5mm 이상 두꺼운 아연도강판</text>
  <text x="440" y="155" font-size="10" fill="#334155">• 1,000℃ 세라믹 불연 가스켓 체결</text>
  <text x="440" y="175" font-size="10" fill="#334155">• 내진형 종·횡방향 브레이싱 지지</text>

  <rect x="60" y="215" width="680" height="60" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="240" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 화재 신호 수신 시 30초 이내 배연 모드 100% 자동 기동 ⟶ 유독가스 배출</text>
</svg>''',

    17: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">차량기지 종합검수고 국부 냉난방 및 변전소 PAC 배치도</text>

  <rect x="60" y="75" width="400" height="120" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="260" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">종합검수고 대공간 (피트 및 작업대)</text>

  <rect x="80" y="120" width="160" height="60" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="160" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">이동식 에어컨 (국부)</text>
  <text x="160" y="165" text-anchor="middle" font-size="9" fill="#334155">플렉시블 토출 주름관</text>

  <rect x="270" y="120" width="160" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="350" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b">원적외선 히터 (국부)</text>
  <text x="350" y="165" text-anchor="middle" font-size="9" fill="#334155">정비원 상주 구역 집중</text>

  <rect x="490" y="75" width="250" height="120" rx="6" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="615" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#854d0e">변전소 패키지 에어컨(PAC)</text>
  <text x="510" y="130" font-size="10" fill="#334155">• 변전소별 3대 설치 (정합성 완료)</text>
  <text x="510" y="150" font-size="10" fill="#334155">• 24시간 항온항습 (≤ 28℃ 유지)</text>
  <text x="510" y="170" font-size="10" fill="#334155">• 친환경 R-410A 냉매 적용</text>

  <rect x="60" y="215" width="680" height="60" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>
  <text x="400" y="240" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">✔ 전면 공조 대비 에너지 소비 45% 절감 + 정비 작업자 체감 쾌적성 극대화</text>
</svg>''',

    18: '''<svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background:#f8fafc; border-radius:8px; font-family:'Pretendard', sans-serif;">
  <rect x="20" y="20" width="760" height="280" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">냉온수·냉각수 배관 맞대기 용접, 비파괴(RT) 및 수압시험 상세도</text>

  <rect x="60" y="110" width="280" height="45" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>
  <text x="180" y="137" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">탄소강관 (KSD 3562)</text>

  <polygon points="340,110 355,132 340,155 370,155 355,132 370,110" fill="#ea580c"/>
  <text x="355" y="95" text-anchor="middle" font-size="10" font-weight="bold" fill="#c2410c">다층 맞대기 용접부</text>

  <rect x="370" y="110" width="280" height="45" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>
  <text x="530" y="137" text-anchor="middle" font-size="11" font-weight="bold" fill="#ffffff">탄소강관 (KSD 3562)</text>

  <rect x="60" y="195" width="310" height="75" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="215" y="220" text-anchor="middle" font-size="12" font-weight="bold" fill="#1d4ed8">1. 비파괴검사 (RT/UT ≥ 10%)</text>
  <text x="80" y="245" font-size="10" fill="#334155">• 방사선 투과 촬영 필름 판독 100% 합격</text>
  <text x="80" y="260" font-size="10" fill="#334155">• 슬래그 혼입, 기공, 미융착 결함 Zero</text>

  <rect x="410" y="195" width="330" height="75" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="575" y="220" text-anchor="middle" font-size="12" font-weight="bold" fill="#15803d">2. 1.5배 수압시험 &amp; 보온</text>
  <text x="430" y="245" font-size="10" fill="#334155">• 설계압력 1.5배(1.5MPa) 60분 무누수</text>
  <text x="430" y="260" font-size="10" fill="#334155">• 난연 고무발포 단열재(두께 40mm) 밀착</text>
</svg>'''
}

print(f"기계설비 전용 SVG 도식 Part 1 (1~18번): {len(MECH_SVGS_PART1)}개 로드 완료!")
