import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

# Design criteria mapping per discipline
designer_specs = {
    "사전토공사": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 토질·기초 및 철도계획 설계기준 연계 (분야별설계기준 검토서)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>토질 및 기초 설계기준:</strong> 「구조물기초 설계기준」, 「도로포장 설계시공지침」 및 「토목공사 일반표준시방서」 준수</li>
            <li><strong>철도계획 선로 기하구조:</strong> 본선 최소곡선반경 R=25m, 정거장 R=300m 이상, 본선 최대구배 60‰ 이하 적용</li>
            <li><strong>선로 중심간격 및 한계:</strong> 본선 중심간격 3.5m 이상 (차량한계 2.7m x 3.6m, 건축한계 3.1m x 3.8m) 적용</li>
            <li><strong>교통처리 및 도로점용 지침:</strong> 「도로공사장 교통관리지침(국토교통부 2024.6)」 준수 - 1차로 최소 폭 3.5m, 2차로 6.5m, 임시보도 1.5m 이상 확보</li>
        </ul>
    </div>
    """,
    
    "상부강화노반": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 토질·기초 및 노반 구조 설계기준 연계 (분야별설계기준 검토서)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>토질 및 기초 설계기준:</strong> KCS 11 00 00 (토공사), KDS 47 10 00 (철도 노반 설계기준) 및 KCS 47 10 25 (강화노반) 규정 완전 이행</li>
            <li><strong>지반 지지력 및 변형성 기준:</strong> 평판재하시험 지반반력계수 K30 ≥ 110 MN/m³, 변형계수 Ev2 ≥ 120 MPa, 강성 균질성 Ev2/Ev1 ≤ 2.2 충족</li>
            <li><strong>다짐도 및 입도 관리:</strong> 수정 AASHTO 다짐시험 기준 다짐도 ≥ 95%, 강화노반 쇄석 최대 입경 ≤ 100mm, 0.075mm 체 통과량 ≤ 15% 제한</li>
            <li><strong>배수 및 침하 제어:</strong> 횡단 배수구배 2.0% 준수, 절성토 경계부 계단식 층따기(1:4) 및 맹암거 설치, 연약지반 수렴 잔여침하속도 ≤ 1.0mm/월 제어</li>
        </ul>
    </div>
    """,
    
    "콘크리트도상": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 궤도·선로 분야 설계기준 연계 (분야별설계기준 검토서 Rev.0)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>궤도 설계기준 (KDS 47 30 00):</strong> 1435mm 표준궤 정밀 허용공차 (+3.0mm, -1.0mm), 무캔트/캔트 제어 및 곡선 확폭량(Slack 10~15mm) 적용</li>
            <li><strong>레일 종별 및 홈레일:</strong> 매설궤도 구간 홈레일(51R1/60R2) 및 도상 구간 60kg 레일 시방 준수</li>
            <li><strong>레일 용접 기술기준:</strong> 테르밋 용접(EN 14730) 및 가스압접/플래시버트 용접(EN 14587) 준수, NDT(UT/MT) 100% 검사, 1m 직선도 공차 ±0.2mm</li>
            <li><strong>콘크리트도상 강도 스펙:</strong> TCL 궤도 콘크리트 28일 압축강도 f_ck ≥ 30 MPa, PST 프리캐스트 패널 충전재 강도 f_ck ≥ 45 MPa 충족</li>
        </ul>
    </div>
    """,
    
    "건축": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 건축구조 및 기계·소방 분야 설계기준 연계 (분야별설계기준 검토서)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>건축구조 설계기준 (KDS 41 00 00):</strong> 건축물 내진설계기준, 풍하중 및 차량기지 검수고 피트(Pit) 수밀 방수 시방 적용</li>
            <li><strong>크레인 및 하중 조건:</strong> 검수고 5~10t 천장 크레인(Trolley Crane) 동적 하중 반영, OCC 관제실 Access Floor 내진 앵커링 준수</li>
            <li><strong>소방시설 설계기준:</strong> 소방시설공사업법 및 국가화재안전기술기준(NFSC 101/102/103) 준수, 관제실/변전소 가스계 소화설비 룸인티그리티(N50) 적용</li>
            <li><strong>인터페이스 CSD 3D BIM:</strong> 건축 구조체 슬리브 및 개구부에 대한 MEP, 토목, 궤도, 전기, 신호, 통신 사전 3D BIM 검토 수칙 적용</li>
        </ul>
    </div>
    """,
    
    "신호분야": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 신호 및 제어 시스템 설계기준 연계 (분야별설계기준 검토서)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>안전성 검증 규격:</strong> IEC 61508 / IEC 62278 / IEC 62425 규격 준수 전자연동장치(CBI) SIL 4 (Safety Integrity Level 4) 적용</li>
            <li><strong>축차계수기 및 선로전환기:</strong> Axle Counter 듀얼 센서 레일 체결 토크 45~50 Nm, 선로전환기 전환력 4.5~6.0 kN, 밀착 유격 ≤ 1.5mm</li>
            <li><strong>교차로 트램 우선신호:</strong> PPC 보드 및 LTE 모뎀 연동 신호 처리 지연시간 ≤ 100ms, TOD 연동 트램 전용 우선 녹색 현시 보장</li>
            <li><strong>인터페이스 표준:</strong> 신호-궤도-전량-차량 간 SIL 4 통합 시험 및 비상 정지 안전 인터록 시방 준수</li>
        </ul>
    </div>
    """,
    
    "통신분야": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 정보통신 및 전송망 설계기준 연계 (분야별설계기준 검토서)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>LTE-R 무선망 설계기준:</strong> 700MHz Band 28 대역 음영지역 제로화, RSSI ≥ -95dBm, RSRP ≥ -105dBm, 핸드오버 성공률 ≥ 99.5% 확보</li>
            <li><strong>광백본망 케이블 기준:</strong> 72-Core 싱글모드 광케이블 (SMF, ITU-T G.652D) 이중화 링 망, OTDR 접속 손실 ≤ 0.05dB/splice</li>
            <li><strong>CCTV 및 PIS/PA 기준:</strong> 4K (8MP, 30fps) IP CCTV 및 NVR 24시간 이중화, PIS 안내 오차 ≤ 1초, PA 비상방송 STI ≥ 0.6</li>
            <li><strong>PSD 통신 인터페이스:</strong> 승강장안전문(PSD) Safety Loop 쇄정 통신 지연 ≤ 100ms, CAN/Ethernet 이중화 인터록 준수</li>
        </ul>
    </div>
    """,
    
    "전기분야": """
    <div class="designer-criteria-box" style="background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 18px; margin-top: 15px;">
        <h4 style="color: #0369A1; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem;">📄 [설계사 작성] 전기·전력 및 급전 설비 설계기준 연계 (분야별설계기준 검토서)</h4>
        <ul style="margin: 0; padding-left: 20px; color: #1E293B; font-size: 0.92rem; line-height: 1.7;">
            <li><strong>전력 수전 및 급전 기준:</strong> 22.9kV AC 수전 → 12-Pulse 다이오드 정류 변압기 → DC 750V (허용전압 DC 500V~900V) 정격 급전</li>
            <li><strong>전차선 및 급속 충전:</strong> 가공전차선 강체 T-Bar 편위 오차 ±15mm, 무전차선 승강장 대전류 급속 충전(DC 750V/1000A) ESS 30초 내 80% 충전</li>
            <li><strong>누설전류(Stray Current) 방지:</strong> 주행레일 비접지 귀선 계통, 누설전류 방지 디오드 접지 장치(Polarization Cell) 레일-대지 전압 ≤ 120V (EN 50122-2)</li>
            <li><strong>SCADA 및 특고압 시방:</strong> 22.9kV XLPE 케이블 절연저항 ≥ 2,000 MΩ, SCADA 원격제어 응답시간 ≤ 100ms 및 전기 사용전검사 필 준수</li>
        </ul>
    </div>
    """
}

updated_count = 0

for disc_name, criteria_html in designer_specs.items():
    disc_path = os.path.join(base_attach_dir, disc_name)
    if not os.path.exists(disc_path):
        continue
        
    for root, dirs, files in os.walk(disc_path):
        for f in files:
            if f.endswith('_표준서.html'):
                file_path = os.path.join(root, f)
                with open(file_path, 'r', encoding='utf-8') as html_file:
                    content = html_file.read()
                
                # Check if designer criteria section is already inserted
                if 'designer-criteria-box' in content:
                    continue
                
                # Insert the designer criteria into Section 3
                pattern = r'(<h2>3\. 첨부서류 연계 상세 설계기준 \(Design Criteria\)</h2>)'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, r'\1\n' + criteria_html, content)
                    with open(file_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(new_content)
                    updated_count += 1

print(f"Update complete! Embedded designer criteria into {updated_count} 표준서.html files.")
