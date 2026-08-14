# -*- coding: utf-8 -*-
"""
상부강화노반 19~36번 액티비티 1:1 맞춤형 2D 엔지니어링 SVG 도식 모듈 (Light Theme 준수)
"""

def get_svg_19_to_36(task_num, wbs_code, act_name):
    # 19. 장비 검수 지원 - 진동롤러 기진력 및 안전센서
    if task_num == 19:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">12ton 진동롤러 기진력 제원 및 AI 후방 안전감지 센서 검측도 - WBS {wbs_code}</text>

  <!-- 진동롤러 형상 -->
  <circle cx="160" cy="270" r="50" fill="#64748b" stroke="#334155" stroke-width="3"/>
  <rect x="200" y="190" width="160" height="90" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
  <circle cx="330" cy="280" r="40" fill="#475569" stroke="#1e293b" stroke-width="3"/>
  
  <!-- 운전석 캡 -->
  <polygon points="230,190 260,130 330,130 350,190" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="130" y="275" fill="#ffffff" font-size="11" font-weight="bold">진동 드럼</text>
  <text x="235" y="220" fill="#0f172a" font-size="13" font-weight="bold">12ton 롤러</text>

  <!-- AI 후방 감지 센서 레이더 빔 -->
  <path d="M360,200 L480,150 L480,250 Z" fill="#ef4444" opacity="0.25"/>
  <circle cx="360" cy="200" r="6" fill="#dc2626"/>
  <text x="375" y="195" fill="#dc2626" font-size="11" font-weight="bold">AI 인체감지 센서 (감지반경 5m)</text>

  <!-- 우측 검수 체크표 -->
  <rect x="440" y="90" width="320" height="260" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="460" y="120" fill="#0f172a" font-size="13" font-weight="bold">다짐 장비 필수 합격 기준</text>

  <rect x="460" y="135" width="280" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="475" y="160" fill="#0f172a" font-size="11" font-weight="bold">자중: 12ton 이상 (기진력 ≥ 250kN)</text>

  <rect x="460" y="185" width="280" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="475" y="210" fill="#0f172a" font-size="11" font-weight="bold">진동 주파수: 30~45Hz 정밀 제어</text>

  <rect x="460" y="235" width="280" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="475" y="260" fill="#0f172a" font-size="11" font-weight="bold">후방 어라운드뷰 및 경보음(≥85dB)</text>

  <rect x="460" y="285" width="280" height="45" rx="6" fill="#047857"/>
  <text x="480" y="312" fill="#ffffff" font-size="11" font-weight="bold">✓ 안전검수필증(스티커) 100% 부착</text>
</svg>'''

    # 20. 선로 종/횡단 측량 - 토탈스테이션 및 횡단 5포인트
    elif task_num == 20:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">선로 중심선 좌표(X,Y,Z) 및 횡단 5개 포인트 정밀 측량도 - WBS {wbs_code}</text>

  <!-- 강화노반 횡단 5개 포인트 단면 -->
  <polygon points="100,260 400,240 700,260 700,320 100,320" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  
  <!-- 중심선 & 레벨 포인트 -->
  <circle cx="400" cy="240" r="8" fill="#dc2626"/>
  <text x="360" y="225" fill="#dc2626" font-size="12" font-weight="bold">★ 선로 중심선 (CL)</text>

  <!-- 좌우 궤도 중심점 -->
  <circle cx="280" cy="248" r="6" fill="#0284c7"/>
  <text x="240" y="235" fill="#0369a1" font-size="11">좌측 궤도 (L)</text>

  <circle cx="520" cy="248" r="6" fill="#0284c7"/>
  <text x="500" y="235" fill="#0369a1" font-size="11">우측 궤도 (R)</text>

  <!-- 좌우 어깨점 -->
  <circle cx="100" cy="260" r="6" fill="#d97706"/>
  <text x="65" y="250" fill="#b45309" font-size="11">좌측 어깨</text>

  <circle cx="700" cy="260" r="6" fill="#d97706"/>
  <text x="680" y="250" fill="#b45309" font-size="11">우측 어깨</text>

  <!-- 횡단 2% 구배 표시 -->
  <text x="210" y="280" fill="#065f46" font-size="11" font-weight="bold">⟵ 구배 i=2.0%</text>
  <text x="550" y="280" fill="#065f46" font-size="11" font-weight="bold">구배 i=2.0% ⟶</text>

  <rect x="180" y="90" width="440" height="50" rx="8" fill="#f8fafc" stroke="#94a3b8"/>
  <text x="200" y="115" fill="#0f172a" font-size="12" font-weight="bold">★ 측량 허용오차: 좌표(X,Y) ±5mm | 표고(Z) ±5mm</text>
  <text x="200" y="132" fill="#475569" font-size="11">본선 10m 간격 광학 토탈스테이션 연속 검측</text>
</svg>'''

    # 21. 규준틀 설치 - 비탈 및 수평 규준틀
    elif task_num == 21:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">비탈 규준틀(사면 1:1.5) 및 수평 층다짐 눈금 규준틀 3D 설치도 - WBS {wbs_code}</text>

  <!-- 성토체 사면 형상 -->
  <polygon points="80,340 320,180 480,180 720,340" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  
  <!-- 좌측 비탈 규준틀 설치 -->
  <line x1="80" y1="340" x2="320" y2="180" stroke="#dc2626" stroke-width="4"/>
  <line x1="60" y1="350" x2="100" y2="330" stroke="#0f172a" stroke-width="2"/>
  <line x1="300" y1="190" x2="340" y2="170" stroke="#0f172a" stroke-width="2"/>
  <text x="120" y="240" fill="#991b1b" font-size="13" font-weight="bold">비탈 규준틀 (1:1.5)</text>

  <!-- 수평 규준틀 (중앙) -->
  <line x1="360" y1="130" x2="440" y2="130" stroke="#0284c7" stroke-width="4"/>
  <line x1="370" y1="130" x2="370" y2="220" stroke="#334155" stroke-width="3"/>
  <line x1="430" y1="130" x2="430" y2="220" stroke="#334155" stroke-width="3"/>
  <text x="340" y="115" fill="#0369a1" font-size="12" font-weight="bold">수평 규준틀 (F.L 기준)</text>

  <!-- 층다짐 30cm 눈금 표시 -->
  <line x1="360" y1="160" x2="440" y2="160" stroke="#059669" stroke-width="1.5" stroke-dasharray="4,2"/>
  <line x1="360" y1="190" x2="440" y2="190" stroke="#059669" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="450" y="165" fill="#047857" font-size="11">강화노반 30cm</text>
  <text x="450" y="195" fill="#047857" font-size="11">상부노반 30cm</text>

  <rect x="460" y="270" width="270" height="50" rx="8" fill="#f8fafc" stroke="#94a3b8"/>
  <text x="475" y="295" fill="#0f172a" font-size="11" font-weight="bold">설치 간격: 직선 20m, 곡선 10m</text>
  <text x="475" y="312" fill="#475569" font-size="10">망실 시 당일 재측량 100% 복구</text>
</svg>'''

    # 22. 준비배수 - 산마루측구 및 오픈트렌치
    elif task_num == 22:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">절토부 산마루측구 및 작업구간 외곽 가설 오픈트렌치 배수도 - WBS {wbs_code}</text>

  <!-- 지형 단면 -->
  <polygon points="50,140 250,140 380,260 750,260 750,370 50,370" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  
  <!-- 1. 산마루측구 (상단) -->
  <rect x="180" y="125" width="40" height="30" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
  <text x="140" y="115" fill="#0369a1" font-size="12" font-weight="bold">산마루측구 (표면수 차단)</text>

  <!-- 비탈면 빗물 흐름 -->
  <path d="M260,150 L360,240" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="4,2"/>
  <text x="240" y="205" fill="#0284c7" font-size="11">비탈면 유수</text>

  <!-- 2. 가설 오픈트렌치 (하단) -->
  <rect x="360" y="250" width="40" height="30" fill="#059669" stroke="#065f46" stroke-width="2"/>
  <text x="340" y="305" fill="#065f46" font-size="12" font-weight="bold">가설 오픈트렌치</text>

  <!-- 3. 트램 노반 성토면 -->
  <rect x="420" y="240" width="310" height="80" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="480" y="285" fill="#065f46" font-size="13" font-weight="bold">트램 노반 보호 구역 (침수 Zero)</text>

  <rect x="440" y="90" width="290" height="50" rx="8" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="455" y="115" fill="#166534" font-size="12" font-weight="bold">★ 배수 경사: 최소 i ≥ 1.0% 확보</text>
  <text x="455" y="132" fill="#15803d" font-size="11">강우 시 노반 면 물고임 원천 차단</text>
</svg>'''

    # 23. 벌개제근/표토제거 - 뿌리 발근 및 표토 20cm
    elif task_num == 23:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">벌개제근(수목/뿌리 제거) 및 유기질 표토(20cm) 굴착 제거도 - WBS {wbs_code}</text>

  <!-- 1. 표토층 (Top Soil 20cm 굴착 대상) -->
  <rect x="60" y="120" width="680" height="50" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>
  <text x="80" y="150" fill="#9a3412" font-size="13" font-weight="bold">유기질 표토층 (Top Soil 두께 20~30cm 전면 굴착 사토)</text>

  <!-- 나무 그루터기 & 뿌리 발근 형상 -->
  <rect x="180" y="90" width="40" height="30" fill="#78350f"/>
  <path d="M180,120 Q150,150 130,165 M220,120 Q250,150 270,165" stroke="#78350f" stroke-width="3"/>
  <text x="140" y="80" fill="#78350f" font-size="11" font-weight="bold">벌개제근 (뿌리 발근)</text>

  <!-- 2. 원지반면 (표토 제거 후 전압 다짐) -->
  <rect x="60" y="170" width="680" height="120" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="80" y="220" fill="#334155" font-size="13" font-weight="bold">원지반면 (Natural Ground)</text>
  <text x="80" y="245" fill="#475569" font-size="11">• 12ton 진동롤러 4회 전압 다짐</text>
  <text x="80" y="265" fill="#475569" font-size="11">• 다짐도 ≥ 90% 확보 후 노반 쌓기 착수</text>

  <rect x="420" y="200" width="300" height="60" rx="8" fill="#fef2f2" stroke="#f87171"/>
  <text x="435" y="225" fill="#991b1b" font-size="12" font-weight="bold">★ 직경 3cm 이상 유기질 잔류 뿌리 0%</text>
  <text x="435" y="245" fill="#b91c1c" font-size="11">장기 유기물 부패에 의한 지반 침하 원천 차단</text>
</svg>'''

    # 24. 구조물 및 지장물 제거 - 중앙분리대 파쇄 및 철거
    elif task_num == 24:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">기존 도로 콘크리트 중앙분리대 및 아스콘 포장 절삭 철거도 - WBS {wbs_code}</text>

  <!-- 도로 아스콘 포장층 -->
  <rect x="60" y="180" width="680" height="50" fill="#334155"/>
  <text x="80" y="210" fill="#ffffff" font-size="12" font-weight="bold">아스팔트 포장층 (절삭기 10cm 절단)</text>

  <!-- 콘크리트 중앙분리대 파쇄 -->
  <polygon points="340,180 370,90 430,90 460,180" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
  <text x="355" y="140" fill="#0f172a" font-size="12" font-weight="bold">중앙분리대</text>

  <!-- 유압 압쇄기(Crusher) 작용 -->
  <line x1="330" y1="100" x2="370" y2="130" stroke="#ef4444" stroke-width="3"/>
  <line x1="470" y1="100" x2="430" y2="130" stroke="#ef4444" stroke-width="3"/>
  <text x="330" y="75" fill="#dc2626" font-size="12" font-weight="bold">유압 무진동 압쇄(Crusher)</text>

  <rect x="60" y="260" width="680" height="90" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="80" y="290" fill="#0f172a" font-size="12" font-weight="bold">구조물 철거 안전 및 품질 기준:</text>
  <text x="80" y="315" fill="#475569" font-size="11">• 철근 및 폐콘크리트 100% 분리 배출 | • 철거 후 발생 공동 양질토 30cm 층다짐 되메우기</text>
  <text x="80" y="335" fill="#475569" font-size="11">• 소음 65dB 이하 준수 (방진망 및 소음 저감 덮개 설치)</text>
</svg>'''

    # 25. 진입로 조성 - 지오텍스타일 및 가설 복공판
    elif task_num == 25:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">중장비 가설 진입로(폭 6.0m) 단면 및 강재 복공판 지지 구조도 - WBS {wbs_code}</text>

  <!-- 가설 복공판 상판 -->
  <rect x="80" y="130" width="640" height="25" fill="#475569" stroke="#1e293b" stroke-width="2"/>
  <text x="280" y="148" fill="#ffffff" font-size="12" font-weight="bold">강재 복공판 (Lining Plate 폭 6.0m)</text>

  <!-- H-Beam 지지보 -->
  <rect x="150" y="155" width="20" height="70" fill="#334155"/>
  <rect x="390" y="155" width="20" height="70" fill="#334155"/>
  <rect x="630" y="155" width="20" height="70" fill="#334155"/>
  <text x="420" y="195" fill="#334155" font-size="11" font-weight="bold">H-Beam 주형보 (H-300)</text>

  <!-- 쇄석 기층 & 부직포 -->
  <rect x="80" y="240" width="640" height="50" fill="#cbd5e1" stroke="#64748b"/>
  <line x1="80" y1="290" x2="720" y2="290" stroke="#059669" stroke-width="3"/>
  <text x="90" y="270" fill="#1e293b" font-size="11" font-weight="bold">재생쇄석 기층 (두께 30cm, 다짐도 ≥ 95%)</text>
  <text x="90" y="315" fill="#065f46" font-size="11" font-weight="bold">고강도 토목용 부직포 (Geotextile 포설)</text>

  <rect x="420" y="330" width="300" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="435" y="355" fill="#166534" font-size="11" font-weight="bold">★ 덤프 25t 교행 가능 지지력 K30 ≥ 150</text>
</svg>'''

    # 26. 노반쌓기 - 15t 타이어롤러 프루프롤링
    elif task_num == 26:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">노반쌓기 층별 다짐 및 15ton 복륜 타이어롤러 프루프롤링 검측도 - WBS {wbs_code}</text>

  <!-- 성토층 단면 -->
  <rect x="60" y="220" width="680" height="80" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>
  <text x="80" y="260" fill="#9a3412" font-size="13" font-weight="bold">성토 1개 층 (완화 포설 두께 30cm, 다짐도 ≥ 95%)</text>
  <text x="80" y="280" fill="#c2410c" font-size="11">최적함수비 OMC ±2% 관리</text>

  <!-- 15ton 타이어롤러 주행 -->
  <rect x="420" y="130" width="180" height="60" rx="6" fill="#0284c7"/>
  <circle cx="460" cy="205" r="25" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>
  <circle cx="560" cy="205" r="25" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>
  <text x="450" y="165" fill="#ffffff" font-size="12" font-weight="bold">15t 타이어롤러</text>

  <!-- 침하량 검측 지점 -->
  <line x1="560" y1="230" x2="560" y2="250" stroke="#dc2626" stroke-width="2"/>
  <text x="575" y="245" fill="#dc2626" font-size="11" font-weight="bold">침하량 측정 (δ ≤ 5mm)</text>

  <rect x="60" y="320" width="680" height="50" rx="8" fill="#fef2f2" stroke="#f87171"/>
  <text x="80" y="350" fill="#991b1b" font-size="12" font-weight="bold">★ 프루프롤링 합격 기준: 15ton 하중 3회 주행 시 유해한 바퀴 자국(≤5mm) 및 꿀렁거림 0건</text>
</svg>'''

    # 27. 하부노반 시공 - K30 평판재하시험
    elif task_num == 27:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">하부노반(60cm) 시공 및 직경 30cm 평판재하시험(K30 ≥ 110 MN/m³) - WBS {wbs_code}</text>

  <!-- 하부노반층 단면 -->
  <rect x="60" y="230" width="680" height="80" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
  <text x="80" y="270" fill="#334155" font-size="13" font-weight="bold">하부노반층 (Lower Subgrade, 두께 60cm)</text>

  <!-- 반력 트럭 & 평판재하시험기 -->
  <rect x="260" y="100" width="280" height="70" fill="#64748b" rx="6"/>
  <circle cx="310" cy="170" r="20" fill="#1e293b"/>
  <circle cx="490" cy="170" r="20" fill="#1e293b"/>
  <text x="350" y="140" fill="#ffffff" font-size="12" font-weight="bold">반력 덤프트럭 (25t)</text>

  <!-- 유압잭 및 재하판(D=30cm) -->
  <rect x="390" y="170" width="20" height="45" fill="#dc2626"/>
  <rect x="360" y="215" width="80" height="15" fill="#0f172a"/>
  <text x="450" y="210" fill="#dc2626" font-size="11" font-weight="bold">재하판 (D=300mm)</text>

  <!-- 다이얼게이지 침하계측 -->
  <line x1="330" y1="210" x2="330" y2="230" stroke="#0284c7" stroke-width="2"/>
  <text x="240" y="220" fill="#0369a1" font-size="11">다이얼게이지 (1.25mm 침하)</text>

  <rect x="60" y="330" width="680" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="80" y="355" fill="#166534" font-size="12" font-weight="bold">★ 하부노반 검측 기준: 다짐도 ≥ 90% | K30 ≥ 110 MN/m³ | Evd ≥ 30 MPa</text>
</svg>'''

    # 28. 상부노반 시공 - 상부노반 2개층 분할 다짐
    elif task_num == 28:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">상부노반(60cm) 2개 층 분할 다짐 및 K30 ≥ 150 MN/m³ 검측도 - WBS {wbs_code}</text>

  <!-- 상부노반 2층 (상부 30cm) -->
  <rect x="60" y="110" width="680" height="60" fill="#bae6fd" stroke="#0284c7" stroke-width="2"/>
  <text x="80" y="145" fill="#0369a1" font-size="13" font-weight="bold">상부노반 2층 (마감층 30cm) [ 다짐도 ≥ 95%, 평탄성 ±10mm ]</text>
  <rect x="580" y="120" width="140" height="40" rx="6" fill="#0284c7"/>
  <text x="595" y="145" fill="#ffffff" font-size="11" font-weight="bold">K30 ≥ 150 MN/m³</text>

  <!-- 상부노반 1층 (하부 30cm) -->
  <rect x="60" y="175" width="680" height="60" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="80" y="210" fill="#0369a1" font-size="13" font-weight="bold">상부노반 1층 (기초층 30cm) [ 다짐도 ≥ 95%, Evd ≥ 45 MPa ]</text>

  <!-- 하부 지반 -->
  <rect x="60" y="240" width="680" height="70" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="80" y="280" fill="#475569" font-size="12">하부노반 지지 기저면 (K30 ≥ 110 MN/m³)</text>

  <rect x="60" y="325" width="680" height="45" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="80" y="352" fill="#166534" font-size="12" font-weight="bold">★ 상부노반 시방 기준: 수정 CBR ≥ 10% | 최대입경 ≤ 100mm | Evd ≥ 45 MPa</text>
</svg>'''

    # 29. 강화노반 시공 - SB-1 피니셔 포설 및 K30 ≥ 190
    elif task_num == 29:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">상부강화노반(SB-1, 30cm) 피니셔 포설 및 K30 ≥ 190 MN/m³ 검측도 - WBS {wbs_code}</text>

  <!-- 최상위 강화노반층 (30cm) -->
  <rect x="60" y="100" width="680" height="70" fill="#d1fae5" stroke="#059669" stroke-width="3"/>
  <text x="80" y="140" fill="#065f46" font-size="14" font-weight="900">★ 상부강화노반 SB-1 (0~30mm 입도조정쇄석, 두께 30cm)</text>
  
  <rect x="580" y="112" width="145" height="46" rx="6" fill="#047857"/>
  <text x="592" y="140" fill="#ffffff" font-size="12" font-weight="bold">K30 ≥ 190 MN/m³</text>

  <!-- 골재 피니셔 형상 -->
  <rect x="180" y="190" width="180" height="65" fill="#f59e0b" stroke="#b45309" stroke-width="2" rx="4"/>
  <polygon points="140,210 180,190 180,255 140,245" fill="#d97706"/>
  <text x="200" y="230" fill="#0f172a" font-size="12" font-weight="bold">골재 피니셔 포설</text>
  <text x="145" y="230" fill="#ffffff" font-size="9">호퍼 직투입</text>

  <!-- 탠덤롤러 마감 -->
  <rect x="420" y="200" width="140" height="55" fill="#0284c7" rx="4"/>
  <circle cx="450" cy="255" r="18" fill="#1e293b"/>
  <circle cx="530" cy="255" r="18" fill="#1e293b"/>
  <text x="440" y="230" fill="#ffffff" font-size="11" font-weight="bold">탠덤롤러 마감</text>

  <rect x="60" y="320" width="680" height="50" rx="8" fill="#ecfdf5" stroke="#10b981"/>
  <text x="80" y="350" fill="#065f46" font-size="12" font-weight="bold">★ 최종 품질 기준: 다짐도 ≥ 98% | K30 ≥ 190 MN/m³ | Evd ≥ 65 MPa | 평탄성 ±10mm</text>
</svg>'''

    # 30. 토공 유동운반/사토 - 덤프 덮개 밀폐 및 세륜
    elif task_num == 30:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">25ton 덤프트럭 자동덮개 밀폐 및 현장 세륜 100% 관리도 - WBS {wbs_code}</text>

  <!-- 덤프트럭 형상 -->
  <rect x="120" y="160" width="260" height="100" fill="#0284c7" rx="6"/>
  <polygon points="380,180 430,210 430,260 380,260" fill="#0369a1"/>
  
  <!-- 바퀴 3개 -->
  <circle cx="170" cy="270" r="25" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>
  <circle cx="230" cy="270" r="25" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>
  <circle cx="390" cy="270" r="25" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>

  <!-- 자동 덮개(호로) 밀폐선 -->
  <line x1="110" y1="160" x2="380" y2="160" stroke="#16a34a" stroke-width="6"/>
  <text x="180" y="150" fill="#166534" font-size="11" font-weight="bold">적재함 자동 덮개 100% 밀폐</text>
  <text x="200" y="215" fill="#ffffff" font-size="14" font-weight="bold">25ton 정량적재</text>

  <!-- 우측 관리 수칙 카드 -->
  <rect x="460" y="100" width="290" height="240" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="480" y="130" fill="#0f172a" font-size="13" font-weight="bold">토사 운반 안전/환경 수칙</text>

  <rect x="480" y="145" width="250" height="40" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="495" y="170" fill="#0f172a" font-size="11" font-weight="bold">1. 적재함 상단 10cm 이하 적재</text>

  <rect x="480" y="195" width="250" height="40" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="495" y="220" fill="#0f172a" font-size="11" font-weight="bold">2. 게이트 세륜기 통과 후 출차</text>

  <rect x="480" y="245" width="250" height="40" rx="6" fill="#047857"/>
  <text x="510" y="270" fill="#ffffff" font-size="11" font-weight="bold">3. 지정 사토장 송장 대조 100%</text>
</svg>'''

    # 31. 연약지반처리 - 3종 계측망
    elif task_num == 31:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">연약지반 로드형 침하판, 간극수압계, 지중경사계 3종 계측망 관리도 - WBS {wbs_code}</text>

  <!-- 성토체 단면 -->
  <polygon points="100,220 220,120 580,120 700,220" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="350" y="160" fill="#92400e" font-size="13" font-weight="bold">성토체 (프리로딩 하중)</text>

  <!-- 연약점토층 -->
  <rect x="60" y="220" width="680" height="130" fill="#e2e8f0" stroke="#64748b"/>
  <text x="80" y="250" fill="#334155" font-size="12" font-weight="bold">연약점토층</text>

  <!-- 1. 로드형 침하판 -->
  <line x1="300" y1="120" x2="300" y2="220" stroke="#dc2626" stroke-width="4"/>
  <rect x="270" y="215" width="60" height="10" fill="#991b1b"/>
  <text x="230" y="110" fill="#dc2626" font-size="11" font-weight="bold">① 지표 침하판</text>

  <!-- 2. 간극수압계 -->
  <line x1="420" y1="120" x2="420" y2="290" stroke="#0284c7" stroke-width="2"/>
  <circle cx="420" cy="290" r="8" fill="#0369a1"/>
  <text x="400" y="110" fill="#0369a1" font-size="11" font-weight="bold">② 간극수압계</text>

  <!-- 3. 지중경사계 (사면부) -->
  <line x1="640" y1="170" x2="640" y2="330" stroke="#059669" stroke-width="3"/>
  <text x="610" y="160" fill="#065f46" font-size="11" font-weight="bold">③ 지중경사계</text>

  <rect x="60" y="320" width="680" height="50" rx="8" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="80" y="350" fill="#166534" font-size="12" font-weight="bold">★ 침하 판정: 주 2회 정밀 계측 | 최종 압밀도 U ≥ 90% 확인 후 궤도 시공</text>
</svg>'''

    # 32. 절성토경계부 맹암거 - 1:4 완화 및 D200 유공관
    elif task_num == 32:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">절성토 접속부 1:4 완화구배 굴착 및 D200 유공관 횡단 맹암거 상세도 - WBS {wbs_code}</text>

  <!-- 깎기(절토) 암반부 (좌측) -->
  <polygon points="60,160 300,160 300,320 60,320" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
  <text x="90" y="240" fill="#1e293b" font-size="14" font-weight="bold">절토부 (단단한 암반)</text>

  <!-- 1:4 완화구배 전이대 (중앙) -->
  <polygon points="300,160 480,240 480,320 300,320" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="325" y="210" fill="#92400e" font-size="12" font-weight="bold">1:4 완화 전이대</text>

  <!-- 쌓기(성토)부 (우측) -->
  <polygon points="480,240 740,240 740,320 480,320" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="540" y="280" fill="#065f46" font-size="14" font-weight="bold">성토부 (토사 다짐)</text>

  <!-- 횡단 맹암거 (유공관 + 자갈) -->
  <rect x="280" y="220" width="40" height="50" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
  <circle cx="300" cy="245" r="10" fill="#ffffff" stroke="#0369a1" stroke-width="2"/>
  <text x="240" y="290" fill="#0369a1" font-size="11" font-weight="bold">D200 유공관 맹암거</text>

  <rect x="60" y="330" width="680" height="40" rx="6" fill="#fef2f2" stroke="#f87171"/>
  <text x="80" y="355" fill="#991b1b" font-size="12" font-weight="bold">★ 부등침하 방지 수칙: 접속 경계면 1:4 경사 완화 굴착 및 침투수 100% 맹암거 유도 배출</text>
</svg>'''

    # 33. 암석쌓기 - 암버력 300mm 및 공극 채움
    elif task_num == 33:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">암석쌓기(최대치수 ≤ 300mm) 층별 60cm 포설 및 모래 공극채움 물다짐도 - WBS {wbs_code}</text>

  <!-- 암석 쌓기층 단면 -->
  <rect x="60" y="140" width="680" height="120" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
  
  <!-- 암버력 돌멩이들 -->
  <polygon points="100,220 130,170 170,180 160,230" fill="#64748b"/>
  <polygon points="200,240 230,160 280,170 270,230" fill="#475569"/>
  <polygon points="320,230 350,150 400,160 390,240" fill="#64748b"/>
  <polygon points="440,240 470,170 520,180 500,230" fill="#475569"/>
  <polygon points="560,230 590,160 640,170 630,240" fill="#64748b"/>

  <text x="180" y="200" fill="#ffffff" font-size="11" font-weight="bold">암버력 (D ≤ 300mm)</text>
  <text x="430" y="200" fill="#ffffff" font-size="11" font-weight="bold">모래 공극 채움 (물다짐)</text>

  <rect x="60" y="280" width="680" height="85" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="80" y="310" fill="#0f172a" font-size="12" font-weight="bold">암석쌓기 시공 및 다짐 기준:</text>
  <text x="80" y="330" fill="#475569" font-size="11">• 1층 포설 두께 ≤ 60cm (불도저 부설) | • 암석 사이 모래 살포 후 살수 물다짐</text>
  <text x="80" y="350" fill="#475569" font-size="11">• 15ton 진동롤러 6회 다짐 (전후 침하량 차이 ≤ 2mm 확인)</text>
</svg>'''

    # 34. 방치기간 확보 - 시간-침하 곡선
    elif task_num == 34:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">성토 완료 후 방치기간(≥ 3개월) 시간-침하 수렴 곡선 그래프 - WBS {wbs_code}</text>

  <!-- 침하 그래프 축 -->
  <line x1="80" y1="120" x2="720" y2="120" stroke="#334155" stroke-width="2"/>
  <line x1="80" y1="120" x2="80" y2="340" stroke="#334155" stroke-width="2"/>
  <text x="90" y="140" fill="#0f172a" font-size="11" font-weight="bold">시간 (1개월, 2개월, 3개월, 4개월)</text>
  <text x="30" y="240" fill="#0f172a" font-size="11" font-weight="bold" transform="rotate(-90 30 240)">침하량 (mm)</text>

  <!-- 침하 수렴 곡선 -->
  <path d="M80,120 C180,260 360,300 680,310" fill="none" stroke="#dc2626" stroke-width="3.5"/>
  <circle cx="230" cy="240" r="5" fill="#dc2626"/>
  <circle cx="380" cy="295" r="5" fill="#dc2626"/>
  <circle cx="560" cy="308" r="5" fill="#dc2626"/>

  <rect x="420" y="210" width="280" height="50" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="435" y="235" fill="#166534" font-size="12" font-weight="bold">★ 침하 수렴 속도: ≤ 1.0mm/월</text>
  <text x="435" y="252" fill="#15803d" font-size="11">3개월 이상 방치 후 감리단 최종 승인</text>
</svg>'''

    # 35. 토공마무리 - 3D GNSS 자동제어 그레이더 및 3m 직선자
    elif task_num == 35:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">3D GNSS 모터그레이더 정밀 스크리딩 및 3m 직선자 평탄성 검측도 - WBS {wbs_code}</text>

  <!-- 강화노반 마무리면 -->
  <polygon points="80,240 400,225 720,240 720,300 80,300" fill="#d1fae5" stroke="#059669" stroke-width="2.5"/>
  <text x="400" y="265" fill="#065f46" font-size="13" font-weight="bold" text-anchor="middle">상부강화노반 정밀 마무리면 (횡단 배수구배 2.0%)</text>

  <!-- 3m 알루미늄 직선자 검측 -->
  <line x1="160" y1="215" x2="380" y2="215" stroke="#0f172a" stroke-width="5"/>
  <text x="210" y="205" fill="#0f172a" font-size="11" font-weight="bold">3m 직선자 (간극 오차 ≤ 10mm)</text>

  <!-- 3D 레이저/GNSS 수신기 -->
  <polygon points="540,140 520,225 560,225" fill="#0284c7"/>
  <circle cx="540" cy="135" r="8" fill="#ef4444"/>
  <text x="500" y="125" fill="#0369a1" font-size="11" font-weight="bold">3D GNSS 수신 타깃</text>

  <rect x="80" y="320" width="640" height="45" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="100" y="347" fill="#166534" font-size="12" font-weight="bold">★ 마감 검측 기준: 마감고 표고 오차 ±10mm | 평탄성 틈새 ≤ 10mm | 탠덤롤러 무진동 마감</text>
</svg>'''

    # 36. 토공 마무리면 인계 - 3자 합동 워킹 검측 및 서명
    elif task_num == 36:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">토목-궤도-감리 3자 합동 전수 검측 및 강화노반 공식 인계인수도 - WBS {wbs_code}</text>

  <!-- 3자 대표자 서명 박스 -->
  <rect x="60" y="100" width="200" height="140" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="80" y="130" fill="#166534" font-size="13" font-weight="bold">1. 토목 시공사</text>
  <text x="80" y="160" fill="#15803d" font-size="11">• 상부강화노반 완성</text>
  <text x="80" y="180" fill="#15803d" font-size="11">• K30/Evd 성적서 총괄</text>
  <text x="80" y="210" fill="#166534" font-size="12" font-weight="bold">서명 완료 (인)</text>

  <rect x="290" y="100" width="200" height="140" rx="8" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="310" y="130" fill="#0369a1" font-size="13" font-weight="bold">2. 궤도 시공사</text>
  <text x="310" y="160" fill="#0284c7" font-size="11">• 기하구조 전수 실측</text>
  <text x="310" y="180" fill="#0284c7" font-size="11">• 콘크리트도상 착공 승인</text>
  <text x="310" y="210" fill="#0369a1" font-size="12" font-weight="bold">인수 서명 (인)</text>

  <rect x="520" y="100" width="220" height="140" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="540" y="130" fill="#92400e" font-size="13" font-weight="bold">3. 책임감리단</text>
  <text x="540" y="160" fill="#b45309" font-size="11">• 36개 액티비티 전수 검측</text>
  <text x="540" y="180" fill="#b45309" font-size="11">• 공종 인계인수서 결재</text>
  <text x="540" y="210" fill="#92400e" font-size="12" font-weight="bold">최종 승인 직인 (인)</text>

  <rect x="60" y="265" width="680" height="90" rx="10" fill="#0f172a"/>
  <text x="80" y="295" fill="#10b981" font-size="13" font-weight="bold">🎉 상부강화노반 36개 공종 100% 합격 완공 및 궤도분야 인계 완료</text>
  <text x="80" y="320" fill="#94a3b8" font-size="11">• K30 ≥ 190 MN/m³ | • Evd ≥ 65 MPa | • 선로 중심선/표고 오차 ±10mm | • 횡단구배 2.0%</text>
  <text x="80" y="340" fill="#38bdf8" font-size="11">동탄도시철도(트램) 건설공사 최고 품질 노반 확보</text>
</svg>'''

    return ""
