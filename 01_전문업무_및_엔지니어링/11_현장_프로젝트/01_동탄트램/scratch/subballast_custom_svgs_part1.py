# -*- coding: utf-8 -*-
"""
상부강화노반 1~18번 액티비티 1:1 맞춤형 2D 엔지니어링 SVG 도식 모듈 (Light Theme 준수)
"""

def get_svg_1_to_18(task_num, wbs_code, act_name):
    # 1. 지반조사 상세검토 - SPT 시추 주상도 및 N치 프로파일
    if task_num == 1:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">지반조사 SPT 시추 주상도 및 N치 심도별 프로파일 - WBS {wbs_code}</text>
  <rect x="660" y="30" width="105" height="26" rx="6" fill="#047857"/>
  <text x="675" y="47" fill="#ffffff" font-size="11" font-weight="bold">KDS 47 10 00</text>
  
  <!-- 시추 주상도 단면 (좌측) -->
  <rect x="50" y="90" width="220" height="60" fill="#fed7aa" stroke="#c2410c" stroke-width="1.5"/>
  <text x="60" y="125" fill="#9a3412" font-size="12" font-weight="bold">매립토/토사 (0 ~ 3.0m) [N=4~8]</text>
  
  <rect x="50" y="150" width="220" height="70" fill="#fde68a" stroke="#d97706" stroke-width="1.5"/>
  <text x="60" y="190" fill="#b45309" font-size="12" font-weight="bold">풍화토층 (3.0 ~ 7.5m) [N=15~25]</text>
  
  <rect x="50" y="220" width="220" height="70" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>
  <text x="60" y="260" fill="#334155" font-size="12" font-weight="bold">풍화암층 (7.5 ~ 12.0m) [N=50/15]</text>
  
  <rect x="50" y="290" width="220" height="80" fill="#cbd5e1" stroke="#475569" stroke-width="1.5"/>
  <text x="60" y="335" fill="#1e293b" font-size="12" font-weight="bold">연암/경암층 (12.0m 이하) [N > 50/5]</text>

  <!-- 지하수위선 (W.L) -->
  <line x1="40" y1="130" x2="280" y2="130" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="6,3"/>
  <text x="290" y="135" fill="#0369a1" font-size="12" font-weight="bold">▼ 지하수위 (G.L -2.5m)</text>

  <!-- 우측 N치 그래프 -->
  <rect x="390" y="90" width="360" height="280" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="390" y1="90" x2="390" y2="370" stroke="#334155" stroke-width="2"/>
  <line x1="390" y1="370" x2="750" y2="370" stroke="#334155" stroke-width="2"/>
  <text x="400" y="110" fill="#0f172a" font-size="12" font-weight="bold">N치 (타격수/30cm 관입)</text>
  <text x="450" y="390" fill="#475569" font-size="11">N=10</text>
  <text x="530" y="390" fill="#475569" font-size="11">N=25</text>
  <text x="610" y="390" fill="#475569" font-size="11">N=40</text>
  <text x="690" y="390" fill="#475569" font-size="11">N=50+</text>

  <!-- N치 곡선 -->
  <polyline points="430,110 440,140 540,180 680,240 730,310" fill="none" stroke="#dc2626" stroke-width="3"/>
  <circle cx="430" cy="110" r="5" fill="#dc2626"/>
  <circle cx="440" cy="140" r="5" fill="#dc2626"/>
  <circle cx="540" cy="180" r="5" fill="#dc2626"/>
  <circle cx="680" cy="240" r="5" fill="#dc2626"/>
  <circle cx="730" cy="310" r="5" fill="#dc2626"/>

  <rect x="400" y="270" width="220" height="40" rx="6" fill="#fef2f2" stroke="#f87171"/>
  <text x="410" y="295" fill="#991b1b" font-size="11" font-weight="bold">★ 잔류침하 관리기준: S ≤ 10cm</text>
</svg>'''

    # 2. 발주전략 KOM - 3자 협의체 및 마일스톤 프로세스
    elif task_num == 2:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">발주전략 3자 협의체(KOM) 및 토공 추진 마일스톤 - WBS {wbs_code}</text>
  
  <!-- 3자 협의체 노드 -->
  <circle cx="160" cy="160" r="55" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="135" y="155" fill="#0369a1" font-size="13" font-weight="bold">발주처</text>
  <text x="120" y="175" fill="#0284c7" font-size="11">화성시/사업단</text>

  <circle cx="360" cy="160" r="55" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="340" y="155" fill="#92400e" font-size="13" font-weight="bold">감리단</text>
  <text x="325" y="175" fill="#b45309" font-size="11">품질/안전 총괄</text>

  <circle cx="260" cy="270" r="55" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="240" y="265" fill="#166534" font-size="13" font-weight="bold">시공사</text>
  <text x="225" y="285" fill="#15803d" font-size="11">토공 전담팀</text>

  <!-- 3자 연결선 -->
  <line x1="215" y1="160" x2="305" y2="160" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="185" y1="205" x2="230" y2="235" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="335" y1="205" x2="290" y2="235" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4"/>

  <!-- 우측 마일스톤 프로세스 박스 -->
  <rect x="460" y="90" width="300" height="280" rx="10" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="480" y="120" fill="#0f172a" font-size="13" font-weight="bold">토공/강화노반 핵심 마일스톤</text>

  <rect x="480" y="140" width="260" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="495" y="165" fill="#0f172a" font-size="11" font-weight="bold">1. 골재원(SB-1) 사전 승인 및 시험</text>

  <rect x="480" y="195" width="260" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="495" y="220" fill="#0f172a" font-size="11" font-weight="bold">2. 시험시공(Test Strip 50m) 완료</text>

  <rect x="480" y="250" width="260" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="495" y="275" fill="#0f172a" font-size="11" font-weight="bold">3. 본선 층별 다짐 및 K30/Evd 검측</text>

  <rect x="480" y="305" width="260" height="42" rx="6" fill="#047857"/>
  <text x="510" y="330" fill="#ffffff" font-size="11" font-weight="bold">4. 궤도(도상) 분야 마무리면 인계</text>
</svg>'''

    # 3. 철도보호지구 행위신고 - 운행선 이격 및 자동변위계 센서
    elif task_num == 3:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">철도보호지구(30m) 인접공사 안전관리 및 레일 자동변위계측 - WBS {wbs_code}</text>

  <!-- 기존 운행선 궤도 (좌측) -->
  <rect x="50" y="200" width="180" height="150" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>
  <rect x="70" y="180" width="20" height="20" fill="#334155"/>
  <rect x="150" y="180" width="20" height="20" fill="#334155"/>
  <line x1="60" y1="180" x2="180" y2="180" stroke="#0f172a" stroke-width="4"/>
  <text x="75" y="235" fill="#0f172a" font-size="12" font-weight="bold">기존 운행선 궤도</text>
  <text x="70" y="255" fill="#475569" font-size="10">(SRT / GTX / 국철)</text>

  <!-- 레일 자동변위계 센서 -->
  <circle cx="80" cy="170" r="6" fill="#ef4444"/>
  <circle cx="160" cy="170" r="6" fill="#ef4444"/>
  <text x="65" y="155" fill="#dc2626" font-size="11" font-weight="bold">자동변위계</text>

  <!-- 30m 철도보호지구 경계선 -->
  <line x1="300" y1="90" x2="300" y2="370" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,3"/>
  <text x="240" y="110" fill="#b91c1c" font-size="12" font-weight="bold">30m 보호지구 경계선</text>

  <!-- 트램 굴착/성토 구간 (우측) -->
  <rect x="360" y="230" width="380" height="120" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="440" y="280" fill="#065f46" font-size="14" font-weight="bold">트램 상부강화노반 시공구역</text>
  <text x="460" y="305" fill="#047857" font-size="11">[ 굴착 및 진동롤러 다짐 작업 ]</text>

  <!-- 열차감시원 배치 -->
  <rect x="315" y="140" width="130" height="50" rx="6" fill="#fef2f2" stroke="#f87171"/>
  <text x="325" y="160" fill="#991b1b" font-size="11" font-weight="bold">열차감시원 상주</text>
  <text x="325" y="178" fill="#b91c1c" font-size="10">2인 1조 무전기 감시</text>

  <rect x="520" y="100" width="220" height="45" rx="6" fill="#f8fafc" stroke="#94a3b8"/>
  <text x="530" y="125" fill="#0f172a" font-size="11" font-weight="bold">★ 레일 허용변위: Δ ≤ 2.0mm</text>
</svg>'''

    # 4. 착수전 측량 Data 확인 - GNSS RTK 및 TBM 레벨링
    elif task_num == 4:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">GNSS RTK 위성측량 및 TBM 기준점 왕복 레벨 검측 - WBS {wbs_code}</text>

  <!-- 인공위성 GNSS -->
  <circle cx="120" cy="110" r="22" fill="#0284c7"/>
  <rect x="70" y="105" width="25" height="10" fill="#38bdf8"/>
  <rect x="145" y="105" width="25" height="10" fill="#38bdf8"/>
  <text x="95" y="150" fill="#0369a1" font-size="11" font-weight="bold">GNSS 위성</text>

  <!-- RTK 수신기 & 삼각대 -->
  <line x1="120" y1="135" x2="220" y2="250" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3,3"/>
  <polygon points="220,250 200,340 240,340" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <circle cx="220" cy="245" r="10" fill="#0284c7"/>
  <text x="180" y="360" fill="#0f172a" font-size="12" font-weight="bold">GNSS RTK 수신기</text>

  <!-- TBM 가수준점 -->
  <rect x="360" y="290" width="70" height="50" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
  <polygon points="395,260 380,290 410,290" fill="#ef4444"/>
  <text x="350" y="360" fill="#991b1b" font-size="12" font-weight="bold">TBM 기준점</text>

  <!-- 토탈스테이션 광학 측량 -->
  <polygon points="560,240 535,340 585,340" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <rect x="545" y="225" width="30" height="20" fill="#d97706"/>
  <text x="515" y="360" fill="#0f172a" font-size="12" font-weight="bold">광학 토탈스테이션</text>

  <!-- 레이저 시준선 -->
  <line x1="575" y1="235" x2="720" y2="235" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,2"/>
  <rect x="710" y="220" width="10" height="120" fill="#ffffff" stroke="#0f172a"/>
  <text x="685" y="360" fill="#0f172a" font-size="12" font-weight="bold">표척(Staff)</text>

  <rect x="420" y="100" width="330" height="50" rx="8" fill="#ecfdf5" stroke="#10b981"/>
  <text x="435" y="125" fill="#065f46" font-size="12" font-weight="bold">★ 기준점 폐합오차: e ≤ 1.0mm√K</text>
  <text x="435" y="142" fill="#047857" font-size="11">원지반 횡단 20m 간격 3D BIM 정합성 검증</text>
</svg>'''

    # 5. 지장물이설 협의 - 3D GPR 지하 레이더 탐사 및 매달기 방호공
    elif task_num == 5:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">3D GPR 지하 지장물 레이더 탐사 및 매설관 매달기 방호공 - WBS {wbs_code}</text>

  <!-- 지표면 및 GPR 탐사기 -->
  <line x1="50" y1="140" x2="750" y2="140" stroke="#334155" stroke-width="3"/>
  <rect x="100" y="100" width="70" height="40" rx="6" fill="#0284c7"/>
  <circle cx="115" cy="140" r="8" fill="#0f172a"/>
  <circle cx="155" cy="140" r="8" fill="#0f172a"/>
  <text x="80" y="90" fill="#0369a1" font-size="11" font-weight="bold">3D GPR 탐사기</text>

  <!-- 전자기파 방사선 -->
  <path d="M135,140 L80,240 L190,240 Z" fill="#38bdf8" opacity="0.2"/>
  <path d="M135,140 L50,320 L220,320 Z" fill="#38bdf8" opacity="0.1"/>

  <!-- 지하 매설관로 단면 -->
  <!-- 1. 한전 22.9kV 전력구 -->
  <rect x="260" y="200" width="60" height="50" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
  <text x="240" y="270" fill="#991b1b" font-size="11" font-weight="bold">한전 22.9kV 전력구</text>

  <!-- 2. 도시가스관 -->
  <circle cx="410" cy="240" r="25" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
  <text x="380" y="285" fill="#b45309" font-size="11" font-weight="bold">도시가스관(D=300)</text>

  <!-- 3. 광통신관로 -->
  <circle cx="530" cy="210" r="18" fill="#10b981" stroke="#047857" stroke-width="2"/>
  <text x="500" y="245" fill="#047857" font-size="11" font-weight="bold">광통신관로</text>

  <!-- 4. 상수도관 -->
  <circle cx="650" cy="250" r="30" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
  <text x="620" y="300" fill="#0369a1" font-size="11" font-weight="bold">상수관(D=500)</text>

  <!-- 매달기 방호 H-Beam -->
  <rect x="330" y="160" width="260" height="15" fill="#475569"/>
  <line x1="410" y1="175" x2="410" y2="215" stroke="#ef4444" stroke-width="2"/>
  <text x="360" y="155" fill="#334155" font-size="11" font-weight="bold">H-Beam 매달기 방호공</text>

  <rect x="50" y="340" width="700" height="40" rx="8" fill="#fef2f2" stroke="#f87171"/>
  <text x="70" y="365" fill="#991b1b" font-size="12" font-weight="bold">★ 중장비 굴착 전 인력 줄파기(Trench) 100% 필수 | 관리기관 3자 입회</text>
</svg>'''

    # 6. 용지보상RISK 검토 - 지적경계 및 도로점용
    elif task_num == 6:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">지적경계 복원측량 및 정거장 환승구역 용지보상 분석도 - WBS {wbs_code}</text>

  <!-- 도로 구역 및 트램 전용차선 -->
  <rect x="60" y="120" width="680" height="140" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2"/>
  <text x="80" y="145" fill="#334155" font-size="13" font-weight="bold">동탄대로 공공 도로구역 (폭 40m)</text>

  <!-- 중앙 트램 노반 -->
  <rect x="240" y="160" width="320" height="80" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="320" y="205" fill="#065f46" font-size="14" font-weight="bold">트램 본선 노반 (폭 8.0m)</text>

  <!-- 정거장 환승시설 확폭 저촉 구간 -->
  <rect x="560" y="140" width="160" height="100" fill="#fef3c7" stroke="#d97706" stroke-width="2" stroke-dasharray="4,4"/>
  <text x="575" y="185" fill="#92400e" font-size="12" font-weight="bold">정거장 환승데크</text>
  <text x="575" y="205" fill="#b45309" font-size="10">(사유지 저촉 검토 구역)</text>

  <!-- LX 지적경계 말뚝 -->
  <polygon points="560,110 550,140 570,140" fill="#dc2626"/>
  <text x="515" y="105" fill="#dc2626" font-size="11" font-weight="bold">LX 경계말뚝</text>

  <rect x="60" y="290" width="680" height="80" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="80" y="320" fill="#0f172a" font-size="12" font-weight="bold">용지보상 리스크 관리 포인트:</text>
  <text x="80" y="345" fill="#475569" font-size="11">• 정거장 엘리베이터/계단실 부지 도로구역 편입 확인 | • 화성시 도로점용허가 100% 득</text>
</svg>'''

    # 7. 최고의 팀 만들기 지원 - 안전 TBM 및 One-Team 프로세스
    elif task_num == 7:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">일일 Safety TBM(Tool Box Meeting) 및 One-Team 안전품질 체계 - WBS {wbs_code}</text>

  <!-- TBM 미팅 원형 배치도 -->
  <circle cx="240" cy="230" r="90" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <circle cx="240" cy="180" r="16" fill="#15803d"/>
  <text x="210" y="155" fill="#166534" font-size="11" font-weight="bold">작업반장(Leader)</text>

  <!-- 팀원 원형 배치 -->
  <circle cx="180" cy="220" r="12" fill="#0284c7"/>
  <circle cx="300" cy="220" r="12" fill="#0284c7"/>
  <circle cx="200" cy="270" r="12" fill="#0284c7"/>
  <circle cx="280" cy="270" r="12" fill="#0284c7"/>
  <text x="200" y="240" fill="#0f172a" font-size="12" font-weight="bold">TBM 100%</text>

  <!-- 우측 일일 점검 4단계 카드 -->
  <rect x="420" y="90" width="340" height="280" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="440" y="120" fill="#0f172a" font-size="13" font-weight="bold">일일 안전보건 필수 4대 수칙</text>

  <rect x="440" y="140" width="300" height="45" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="455" y="167" fill="#0f172a" font-size="11" font-weight="bold">1. 출근 시 음주측정 100% (0.00% 통과)</text>

  <rect x="440" y="195" width="300" height="45" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="455" y="222" fill="#0f172a" font-size="11" font-weight="bold">2. 개인보호구(안전모/안전화/조끼) 착용 점검</text>

  <rect x="440" y="250" width="300" height="45" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="455" y="277" fill="#0f172a" font-size="11" font-weight="bold">3. 중장비 신호수 2인 1조 배치 확인</text>

  <rect x="440" y="305" width="300" height="45" rx="6" fill="#047857"/>
  <text x="470" y="332" fill="#ffffff" font-size="11" font-weight="bold">4. 당일 위험성평가(JSA) 교육 서명</text>
</svg>'''

    # 8. 연약지반 처리공법 검토 - PBD 및 프리로딩 단면
    elif task_num == 8:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">연약점토층 PBD(플라스틱 보드 드레인) 및 프리로딩 성토 단면도 - WBS {wbs_code}</text>

  <!-- 프리로딩 성토체 -->
  <polygon points="120,180 200,100 600,100 680,180" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="350" y="145" fill="#92400e" font-size="13" font-weight="bold">프리로딩 성토 하중 (Preloading)</text>

  <!-- 샌드매트 수평배수층 -->
  <rect x="80" y="180" width="640" height="30" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5"/>
  <text x="340" y="200" fill="#9a3412" font-size="11" font-weight="bold">수평 배수재 (샌드매트 두께 50cm)</text>

  <!-- 연약점토층 -->
  <rect x="80" y="210" width="640" height="160" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>
  <text x="90" y="235" fill="#334155" font-size="12" font-weight="bold">연약점토층 (N ≤ 4)</text>

  <!-- PBD 수직 드레인 타설선 -->
  <line x1="180" y1="180" x2="180" y2="360" stroke="#0284c7" stroke-width="4"/>
  <line x1="260" y1="180" x2="260" y2="360" stroke="#0284c7" stroke-width="4"/>
  <line x1="340" y1="180" x2="340" y2="360" stroke="#0284c7" stroke-width="4"/>
  <line x1="420" y1="180" x2="420" y2="360" stroke="#0284c7" stroke-width="4"/>
  <line x1="500" y1="180" x2="500" y2="360" stroke="#0284c7" stroke-width="4"/>
  <line x1="580" y1="180" x2="580" y2="360" stroke="#0284c7" stroke-width="4"/>
  <line x1="660" y1="180" x2="660" y2="360" stroke="#0284c7" stroke-width="4"/>

  <!-- 배수 화살표 -->
  <path d="M180,240 L180,195 M260,240 L260,195 M340,240 L340,195 M420,240 L420,195" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="440" y="250" fill="#0369a1" font-size="11" font-weight="bold">간극수 상부 배출</text>

  <rect x="520" y="310" width="190" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="530" y="335" fill="#166534" font-size="11" font-weight="bold">★ 압밀도 U ≥ 90% 달성 목표</text>
</svg>'''

    # 9. 토공 유동표 확인 - 매스커브(Mass Curve)
    elif task_num == 9:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">토공 유동표 매스커브(Mass Curve, 유토곡선) 및 토량 밸런스 - WBS {wbs_code}</text>

  <!-- 매스커브 그래프 축 -->
  <line x1="80" y1="230" x2="720" y2="230" stroke="#334155" stroke-width="2"/>
  <line x1="80" y1="90" x2="80" y2="360" stroke="#334155" stroke-width="2"/>
  <text x="90" y="110" fill="#0f172a" font-size="11" font-weight="bold">누적토량 (+절토 / -성토)</text>
  <text x="680" y="220" fill="#0f172a" font-size="11" font-weight="bold">거리(Sta.)</text>

  <!-- 유토곡선 파형 -->
  <path d="M80,230 Q220,90 360,230 T640,230" fill="none" stroke="#0284c7" stroke-width="3.5"/>
  <polygon points="80,230 220,110 360,230" fill="#38bdf8" opacity="0.2"/>
  <polygon points="360,230 500,350 640,230" fill="#f87171" opacity="0.2"/>

  <text x="180" y="170" fill="#0369a1" font-size="13" font-weight="bold">절토구간 (+15,000m³)</text>
  <text x="460" y="290" fill="#b91c1c" font-size="13" font-weight="bold">성토구간 (-14,200m³)</text>

  <!-- 유토 화살표 -->
  <line x1="220" y1="220" x2="500" y2="220" stroke="#059669" stroke-width="3" stroke-dasharray="6,3"/>
  <text x="310" y="210" fill="#047857" font-size="12" font-weight="bold">토사 직접 유용 (평균거리 450m)</text>

  <rect x="480" y="90" width="240" height="45" rx="6" fill="#ecfdf5" stroke="#10b981"/>
  <text x="495" y="118" fill="#065f46" font-size="11" font-weight="bold">★ 토량환산계수 L=1.25, C=0.88 적용</text>
</svg>'''

    # 10. 기공승낙 적정성 검토 - 우회 차선도
    elif task_num == 10:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">도로 기공승낙에 따른 공사 중 교통 우회 차선 배치도 - WBS {wbs_code}</text>

  <!-- 상행선 2차로 유지 -->
  <rect x="50" y="90" width="700" height="60" fill="#e2e8f0" stroke="#94a3b8"/>
  <line x1="50" y1="120" x2="750" y2="120" stroke="#ffffff" stroke-width="2" stroke-dasharray="8,6"/>
  <text x="70" y="125" fill="#334155" font-size="12" font-weight="bold">상행선 (차선 폭 B ≥ 3.0m 유지) ➔ ➔</text>

  <!-- 중앙 트램 공사구간 (RPP 가설방음벽 밀폐) -->
  <rect x="50" y="165" width="700" height="90" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5"/>
  <text x="250" y="215" fill="#991b1b" font-size="14" font-weight="bold">🚧 트램 상부강화노반 공사 구역 (중앙 통제)</text>

  <!-- 하행선 2차로 유지 -->
  <rect x="50" y="270" width="700" height="60" fill="#e2e8f0" stroke="#94a3b8"/>
  <line x1="50" y1="300" x2="750" y2="300" stroke="#ffffff" stroke-width="2" stroke-dasharray="8,6"/>
  <text x="70" y="305" fill="#334155" font-size="12" font-weight="bold">하행선 (차선 폭 B ≥ 3.0m 유지) ➔ ➔</text>

  <!-- 싸인카 및 신호수 -->
  <rect x="60" y="180" width="50" height="60" rx="4" fill="#f59e0b"/>
  <text x="65" y="215" fill="#ffffff" font-size="10" font-weight="bold">싸인카</text>

  <circle cx="130" cy="210" r="10" fill="#dc2626"/>
  <text x="115" y="235" fill="#991b1b" font-size="9" font-weight="bold">신호수</text>

  <rect x="500" y="345" width="250" height="35" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="515" y="368" fill="#166534" font-size="11" font-weight="bold">★ 출퇴근 피크타임(07~09, 17~19) 통제 금지</text>
</svg>'''

    # 11. 폐기물처리계획 수립 - 올바로 시스템
    elif task_num == 11:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">건설폐기물 성상별 분리선별 및 올바로(Allbaro) 전자인계 시스템 - WBS {wbs_code}</text>

  <!-- 폐기물 분리 야적 구획 (좌측) -->
  <rect x="50" y="100" width="160" height="110" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="65" y="130" fill="#0f172a" font-size="12" font-weight="bold">폐아스팔트 콘크리트</text>
  <text x="65" y="150" fill="#475569" font-size="10">• 순환골재 재활용</text>
  <text x="65" y="170" fill="#475569" font-size="10">• 방진덮개 100%</text>

  <rect x="50" y="230" width="160" height="110" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>
  <text x="65" y="260" fill="#0f172a" font-size="12" font-weight="bold">폐콘크리트(경계석 등)</text>
  <text x="65" y="280" fill="#475569" font-size="10">• 철근 분리 파쇄</text>
  <text x="65" y="300" fill="#475569" font-size="10">• 침출수 방지턱</text>

  <!-- 공인 계량대 (중앙) -->
  <rect x="280" y="170" width="160" height="100" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="310" y="210" fill="#92400e" font-size="13" font-weight="bold">공인 계량대</text>
  <text x="300" y="235" fill="#b45309" font-size="11">중량 실측 & 송장발행</text>

  <!-- 올바로 전산 전송 (우측) -->
  <rect x="510" y="140" width="230" height="160" rx="10" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="535" y="175" fill="#065f46" font-size="14" font-weight="bold">환경부 올바로(Allbaro)</text>
  <text x="535" y="205" fill="#047857" font-size="11">• 차량번호 자동 인식</text>
  <text x="535" y="225" fill="#047857" font-size="11">• 전자인계서 실시간 승인</text>
  <text x="535" y="245" fill="#047857" font-size="11">• 반출량 1:1 대사 검증</text>
  <text x="535" y="275" fill="#059669" font-size="12" font-weight="bold">✓ 인계오차 0% 달성</text>
</svg>'''

    # 12. 철도운행협의 - 야간 차단작업
    elif task_num == 12:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">운행선 인접구간 야간 차단시간대(01:00~04:30) 단전 및 접지 절차 - WBS {wbs_code}</text>

  <!-- 타임라인 바 -->
  <rect x="50" y="110" width="700" height="40" fill="#e2e8f0" rx="6"/>
  <rect x="200" y="110" width="350" height="40" fill="#0f172a" rx="6"/>
  <text x="70" y="135" fill="#475569" font-size="12">막차운행 (~01:00)</text>
  <text x="240" y="135" fill="#38bdf8" font-size="13" font-weight="bold">★ 야간 차단작업 시간 (01:00 ~ 04:30)</text>
  <text x="580" y="135" fill="#475569" font-size="12">첫차개시 (05:00~)</text>

  <!-- 3단계 안전 승인 박스 -->
  <rect x="50" y="180" width="220" height="170" rx="8" fill="#fef2f2" stroke="#f87171" stroke-width="2"/>
  <text x="70" y="210" fill="#991b1b" font-size="13" font-weight="bold">STEP 1. 단전 확인</text>
  <text x="70" y="235" fill="#b91c1c" font-size="11">• 25kV 전차선 단전 통보</text>
  <text x="70" y="255" fill="#b91c1c" font-size="11">• 검전기로 잔류전압 0V 확인</text>
  <text x="70" y="275" fill="#b91c1c" font-size="11">• 철도전기안전원 입회</text>

  <rect x="290" y="180" width="220" height="170" rx="8" fill="#fef3c7" stroke="#fbbf24" stroke-width="2"/>
  <text x="310" y="210" fill="#92400e" font-size="13" font-weight="bold">STEP 2. 단락접지 체결</text>
  <text x="310" y="235" fill="#b45309" font-size="11">• 전차선-레일 강제 접지</text>
  <text x="310" y="255" fill="#b45309" font-size="11">• 오송전 감전사고 방지</text>
  <text x="310" y="275" fill="#b45309" font-size="11">• 단락접지구 2개소 설치</text>

  <rect x="530" y="180" width="220" height="170" rx="8" fill="#f0fdf4" stroke="#4ade80" stroke-width="2"/>
  <text x="550" y="210" fill="#166534" font-size="13" font-weight="bold">STEP 3. 작업종료/복구</text>
  <text x="550" y="235" fill="#15803d" font-size="11">• 건축한계 지장물 전수 점검</text>
  <text x="550" y="255" fill="#15803d" font-size="11">• 단락접지구 회수 확인</text>
  <text x="550" y="275" fill="#15803d" font-size="11">• 04:30 이전 관제 완료보고</text>
</svg>'''

    # 13. 작수전 Big Room 회의 - 8대 공종 BIM 간섭
    elif task_num == 13:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">8대 공종 Big Room 통합 인터페이스 및 3D BIM 간섭 검토 - WBS {wbs_code}</text>

  <!-- BIM 3D 통합 모델 뷰 (좌측) -->
  <rect x="50" y="90" width="340" height="280" rx="10" fill="#0f172a" stroke="#334155"/>
  <text x="70" y="125" fill="#38bdf8" font-size="13" font-weight="bold">BIM LOD 350 통합 모델</text>
  
  <line x1="70" y1="200" x2="360" y2="200" stroke="#10b981" stroke-width="4"/>
  <text x="70" y="190" fill="#10b981" font-size="11">강화노반 표면 (EL+25.40)</text>

  <rect x="120" y="215" width="80" height="40" fill="#ef4444" opacity="0.8"/>
  <text x="125" y="240" fill="#ffffff" font-size="10" font-weight="bold">신호 본드함</text>

  <circle cx="280" cy="240" r="20" fill="#f59e0b" opacity="0.8"/>
  <text x="260" y="245" fill="#ffffff" font-size="10" font-weight="bold">배수관</text>

  <!-- 우측 8대 공종 매트릭스 -->
  <rect x="410" y="90" width="350" height="280" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="430" y="120" fill="#0f172a" font-size="13" font-weight="bold">공종별 인터페이스 체크 매트릭스</text>

  <rect x="430" y="140" width="310" height="45" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="445" y="167" fill="#0f172a" font-size="11" font-weight="bold">토목 ↔ 궤도: 다우웰바 및 노반 마감고 ±10mm</text>

  <rect x="430" y="195" width="310" height="45" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="445" y="222" fill="#0f172a" font-size="11" font-weight="bold">토목 ↔ 전기: 전주기초(Mast) 매설 위치 확정</text>

  <rect x="430" y="250" width="310" height="45" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="445" y="277" fill="#0f172a" font-size="11" font-weight="bold">토목 ↔ 통신/신호: 횡단 케이블트러프 선매설</text>

  <rect x="430" y="305" width="310" height="45" rx="6" fill="#047857"/>
  <text x="460" y="332" fill="#ffffff" font-size="11" font-weight="bold">★ 노반 시공 후 재굴착 0건 서약</text>
</svg>'''

    # 14. 시공 계획 수립 - KCS 47 10 25 다짐 계획
    elif task_num == 14:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">KCS 47 10 25 상부강화노반 종합 시공계획 및 장비 조합도 - WBS {wbs_code}</text>

  <!-- 장비 조합 흐름 -->
  <rect x="50" y="100" width="200" height="120" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="70" y="130" fill="#166534" font-size="13" font-weight="bold">1. 포설 장비</text>
  <text x="70" y="155" fill="#15803d" font-size="11">• 모터그레이더 (3.6m)</text>
  <text x="70" y="175" fill="#15803d" font-size="11">• 골재 피니셔 (두께30cm)</text>
  <text x="70" y="195" fill="#15803d" font-size="11">• 횡단 2% 구배 형성</text>

  <rect x="290" y="100" width="200" height="120" rx="8" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="310" y="130" fill="#0369a1" font-size="13" font-weight="bold">2. 다짐 장비</text>
  <text x="310" y="155" fill="#0284c7" font-size="11">• 12ton 진동롤러 (4~6회)</text>
  <text x="310" y="175" fill="#0284c7" font-size="11">• 15ton 타이어롤러 (2회)</text>
  <text x="310" y="195" fill="#0284c7" font-size="11">• 10ton 탠덤 마감롤러</text>

  <rect x="530" y="100" width="220" height="120" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="550" y="130" fill="#92400e" font-size="13" font-weight="bold">3. 품질 검측 장비</text>
  <text x="550" y="155" fill="#b45309" font-size="11">• 들밀도시험 (KS F 2311)</text>
  <text x="550" y="175" fill="#b45309" font-size="11">• 평판재하 PBT (K30)</text>
  <text x="550" y="195" fill="#b45309" font-size="11">• 동적 LFWD (Evd)</text>

  <!-- 하단 시험시공 박스 -->
  <rect x="50" y="250" width="700" height="120" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="70" y="280" fill="#0f172a" font-size="13" font-weight="bold">시험시공(Test Strip) 50m 구간 운영 기준:</text>
  <text x="70" y="305" fill="#475569" font-size="11">• 목적: 현장 골재 맞춤 최적 다짐 횟수, 완화 계수 및 최적함수비(OMC) 산출</text>
  <text x="70" y="325" fill="#475569" font-size="11">• 검측: 층별 다짐도 ≥ 98%, K30 ≥ 190 MN/m³, Evd ≥ 65 MPa 도달 여부 입증 후 본 시공 착수</text>
</svg>'''

    # 15. 사토장/토취장 선정 검토 - 운반 경로 및 토질시험
    elif task_num == 15:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">토취장 골재 품질시험 및 사토장 운반 동선 검토도 - WBS {wbs_code}</text>

  <!-- 토취장 (좌측) -->
  <rect x="50" y="110" width="200" height="140" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="70" y="140" fill="#065f46" font-size="13" font-weight="bold">승인 토취장 (석산)</text>
  <text x="70" y="165" fill="#047857" font-size="11">• 입도조정쇄석 SB-1</text>
  <text x="70" y="185" fill="#047857" font-size="11">• 수정 CBR ≥ 80%</text>
  <text x="70" y="205" fill="#047857" font-size="11">• 마모율 ≤ 35%</text>
  <text x="70" y="225" fill="#047857" font-size="11">• 소성지수 PI ≤ 6</text>

  <!-- 운반 도로망 (중앙) -->
  <line x1="260" y1="180" x2="520" y2="180" stroke="#64748b" stroke-width="6" stroke-dasharray="12,6"/>
  <text x="320" y="165" fill="#0f172a" font-size="12" font-weight="bold">덤프 운반로 (L ≤ 15km)</text>
  <text x="340" y="210" fill="#475569" font-size="10">주거지 우회 동선</text>

  <!-- 사토장 (우측) -->
  <rect x="530" y="110" width="220" height="140" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="550" y="140" fill="#92400e" font-size="13" font-weight="bold">지정 사토장 (화성시)</text>
  <text x="550" y="165" fill="#b45309" font-size="11">• 개발행위허가 완료</text>
  <text x="550" y="185" fill="#b45309" font-size="11">• 수용용량 ≥ 50,000m³</text>
  <text x="550" y="205" fill="#b45309" font-size="11">• 진입로 폭 B ≥ 6.0m</text>
  <text x="550" y="225" fill="#b45309" font-size="11">• 세륜시설 가동 확인</text>

  <rect x="50" y="280" width="700" height="90" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="70" y="310" fill="#0f172a" font-size="12" font-weight="bold">환경 및 안전 통제 수칙:</text>
  <text x="70" y="335" fill="#475569" font-size="11">• 25ton 덤프 적재함 덮개 자동 개폐 밀폐 | • 과적 0건 통제 | • 노면 청소차 상시 순찰</text>
</svg>'''

    # 16. 공사사전준비 - 세륜기 및 방음벽
    elif task_num == 16:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">현장 진출입로 자동세륜기 및 RPP 가설방음벽(H=3.0m) 배치도 - WBS {wbs_code}</text>

  <!-- 가설 RPP 방음벽 라인 -->
  <rect x="50" y="90" width="700" height="20" fill="#cbd5e1" stroke="#475569"/>
  <text x="280" y="105" fill="#1e293b" font-size="11" font-weight="bold">RPP 가설방음벽 (H=3.0m + 방진망)</text>

  <!-- 진출입 게이트 & 자동 세륜기 -->
  <rect x="180" y="160" width="220" height="120" rx="8" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="210" y="190" fill="#0369a1" font-size="13" font-weight="bold">자동 롤러식 세륜기</text>
  <text x="210" y="215" fill="#0284c7" font-size="11">• 타이어 3회전 세척</text>
  <text x="210" y="235" fill="#0284c7" font-size="11">• 고압 측면 살수 노즐</text>
  <text x="210" y="255" fill="#0284c7" font-size="11">• 슬러지 자동 수거조</text>

  <!-- 살수차 상시대기 -->
  <rect x="450" y="160" width="200" height="120" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="480" y="190" fill="#166534" font-size="13" font-weight="bold">이동식 살수차(16t)</text>
  <text x="480" y="215" fill="#15803d" font-size="11">• 진출입로 상시 살수</text>
  <text x="480" y="235" fill="#15803d" font-size="11">• 비산먼지 100% 억제</text>
  <text x="480" y="255" fill="#15803d" font-size="11">• 안개 분무 노즐 장착</text>

  <rect x="50" y="320" width="700" height="50" rx="8" fill="#fef2f2" stroke="#f87171"/>
  <text x="70" y="350" fill="#991b1b" font-size="12" font-weight="bold">★ 토공 차량 현장 출차 시 세륜 미이행 덤프 출차 절대 불허 (게이트 상시 감시)</text>
</svg>'''

    # 17. 임시배수시설 - 3단 침사지 및 펌프
    elif task_num == 17:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">가설 배수로 및 3단 토사 침전 침사지 배수 계통도 - WBS {wbs_code}</text>

  <!-- 가설 U형 플륨관 배수로 -->
  <rect x="50" y="110" width="200" height="60" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>
  <text x="65" y="145" fill="#334155" font-size="12" font-weight="bold">U형 플륨관 (D=400mm, i ≥ 0.5%)</text>

  <!-- 3단 침사지 수조 -->
  <rect x="300" y="100" width="130" height="180" fill="#fed7aa" stroke="#c2410c" stroke-width="2"/>
  <text x="320" y="130" fill="#9a3412" font-size="12" font-weight="bold">1차 침사지</text>
  <text x="320" y="150" fill="#c2410c" font-size="10">(굵은 모래 침전)</text>

  <rect x="440" y="120" width="130" height="160" fill="#fde68a" stroke="#d97706" stroke-width="2"/>
  <text x="460" y="150" fill="#92400e" font-size="12" font-weight="bold">2차 침사지</text>
  <text x="460" y="170" fill="#b45309" font-size="10">(미세 실트 침전)</text>

  <rect x="580" y="140" width="130" height="140" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="600" y="170" fill="#0369a1" font-size="12" font-weight="bold">3차 상등수조</text>
  <text x="600" y="190" fill="#0284c7" font-size="10">(맑은 물 방류)</text>

  <!-- 자동 수중펌프 -->
  <circle cx="645" cy="240" r="16" fill="#047857"/>
  <text x="615" y="270" fill="#065f46" font-size="10" font-weight="bold">수중 양수펌프</text>

  <!-- 방류 화살표 -->
  <line x1="250" y1="140" x2="300" y2="140" stroke="#0284c7" stroke-width="3"/>
  <line x1="430" y1="160" x2="440" y2="160" stroke="#0284c7" stroke-width="3"/>
  <line x1="570" y1="180" x2="580" y2="180" stroke="#0284c7" stroke-width="3"/>

  <rect x="50" y="320" width="700" height="50" rx="8" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="70" y="350" fill="#166534" font-size="12" font-weight="bold">★ 방류수 탁도 기준 준수 | 10년 빈도 확률강우량 배수 용량 확보</text>
</svg>'''

    # 18. 쌓기재료 검사 - 입도분포곡선 및 CBR
    elif task_num == 18:
        return f'''<svg viewBox="0 0 800 420" class="w-full h-auto bg-slate-50 border border-slate-300 rounded-xl shadow-inner font-sans" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="800" height="420" fill="#f8fafc"/>
  <rect x="20" y="20" width="760" height="380" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="20" y="20" width="760" height="46" rx="12" fill="#0f172a"/>
  <rect x="20" y="54" width="760" height="12" fill="#0f172a"/>
  <text x="40" y="48" fill="#ffffff" font-size="14" font-weight="bold">쌓기재료 체가름 입도분포곡선 및 D다짐/수정 CBR 품질 기준 - WBS {wbs_code}</text>

  <!-- 입도분포 그래프 (좌측) -->
  <rect x="50" y="90" width="340" height="260" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="70" y="115" fill="#0f172a" font-size="12" font-weight="bold">입도분포 곡선 (반대수 방안지)</text>
  <line x1="80" y1="310" x2="360" y2="310" stroke="#334155" stroke-width="2"/>
  <line x1="80" y1="130" x2="80" y2="310" stroke="#334155" stroke-width="2"/>
  
  <path d="M85,300 C150,290 220,180 340,140" fill="none" stroke="#0284c7" stroke-width="3"/>
  <text x="140" y="240" fill="#0369a1" font-size="11" font-weight="bold">양입도 곡선 (Cu > 6, 1 < Cc < 3)</text>

  <!-- 우측 시험 기준표 -->
  <rect x="410" y="90" width="350" height="260" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="430" y="120" fill="#0f172a" font-size="13" font-weight="bold">쌓기재료 공학적 품질 합격 기준</text>

  <rect x="430" y="135" width="310" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="445" y="160" fill="#0f172a" font-size="11" font-weight="bold">최대입경: 상부노반 ≤ 100mm, 하부 ≤ 150mm</text>

  <rect x="430" y="185" width="310" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="445" y="210" fill="#0f172a" font-size="11" font-weight="bold">#200체(0.075mm) 통과율: ≤ 15% (동상방지)</text>

  <rect x="430" y="235" width="310" height="42" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="445" y="260" fill="#0f172a" font-size="11" font-weight="bold">소성지수(PI): PI ≤ 10 (비팽창성 토사)</text>

  <rect x="430" y="285" width="310" height="45" rx="6" fill="#047857"/>
  <text x="450" y="312" fill="#ffffff" font-size="11" font-weight="bold">수정 CBR: CBR ≥ 10% (4일 수침 몰드)</text>
</svg>'''

    return ""
