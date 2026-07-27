import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

v1_integration_data = {
    "신호분야": {
        "standard": """
        <div class="manual-v1-integration-box" style="background-color: #F0FDF4; border: 1.5px solid #22C55E; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #15803D; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> [동탄트램 업무 매뉴얼 v1 연계] 신호 분야 기술 표준 수칙
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>CBI SIL 4 및 루프 센서 보호:</strong> 전자연동장치(CBI) SIL 4 (IEC 61508/62425) 안전성 100% 확보 및 매립형 궤도 슬래브 타설 시 신호 루프 센서(Loop Coil) 매설 파손 방지 시방 준수</li>
                <li><strong>교차로 트램 우선신호(PPC):</strong> 트램 차량 접근 시 LTE-R 무선 단말과 도로교통공단 제어기 간 연동 응답시간 ≤ 100ms 확보 및 TOD 녹색 현시 보장</li>
                <li><strong>축차계수기 & 선로전환기:</strong> 분기기 궤도 선시공 후 축차계수기 듀얼 센서 토크(45~50 Nm) 및 선로전환기 전환력(4.5~6.0 kN), 밀착유격(≤ 1.5mm) 연동 검측</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="manual-v1-integration-box" style="background-color: #F0FDF4; border: 1.5px solid #22C55E; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #15803D; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> [동탄트램 업무 매뉴얼 v1 연계] 신호설비 시공 수행지침
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>매립 궤도 타설 시 센서 타격 금지:</strong> 바이브레이터 고주파 다짐 수행 시 신호 루프 코일 및 스핀들 게이지 지지대에 직접 타격이 가해지지 않도록 5cm 이상 이격 다짐 수칙 준수</li>
                <li><strong>패스트트랙 120일 인터페이스 검토:</strong> 토목·궤도·전기·신호 간 사전 인터페이스 붕괴 방지를 위해 착수 후 120일 이내 CSD 3D BIM 상세 검토 완료</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 전자연동장치(CBI) SIL 4 안전 규격 및 신호 루프 코일 매설 파손 방지 조치를 완료하였는가?</li>
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 교차로 PPC 트램 우선신호 응답시간(≤100ms) 및 도로교통 신호등 연동을 확인하였는가?</li>
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 도상 타설 시 바이브레이터가 신호 루프 센서에 직접 접촉되지 않도록 안전 보호 조치를 시행하였는가?</li>
        </ul>
        """
    },

    "전기분야": {
        "standard": """
        <div class="manual-v1-integration-box" style="background-color: #F0FDF4; border: 1.5px solid #22C55E; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #15803D; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> [동탄트램 업무 매뉴얼 v1 연계] 전기·전력 분야 기술 표준 수칙
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>수전 변전소 한전 2개 계통 이중화:</strong> 비상시 전원 정전 대비 독립된 한전 인입 선로 2개소 이중화 구성 및 DC 750V 12-Pulse 다이오드 정류 변압기 시방 준수</li>
                <li><strong>무가선(배터리) 승강장 급속 충전:</strong> 정거장 정차 30초 내 배터리 80% 급속 충전(DC 750V/1000A) 오버헤드 팬타그래프 인입 제어 및 ESS 안전장치 연동</li>
                <li><strong>표유전류(Stray Current) 상수도관 부식 방지:</strong> 레일에서 새어나오는 누설전류로 인한 지하지장물(상수도관, 철근) 부식을 방지하기 위해 레일 주변 엘라스토머 박스(Elastomer Box) 절연재 빈틈없는 부설 및 디오드 접지 적용</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="manual-v1-integration-box" style="background-color: #F0FDF4; border: 1.5px solid #22C55E; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #15803D; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> [동탄트램 업무 매뉴얼 v1 연계] 전기설비 시공 수행지침
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>매립형 궤도 접지선 동시 포설:</strong> 콘크리트 슬래브 타설 시 등전위 접지선 및 귀선 레일 절연 부착 상태를 동시 검측</li>
                <li><strong>22.9kV XLPE 케이블 유도장해 제어:</strong> 고압 전력선 배선 시 통신/신호 케이블과 최소 30cm 이상 격리 배선 및 차폐 트레이 설치</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 수전 변전소 한전 인입 선로가 2개 계통으로 독립 이중화되어 있는가?</li>
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 표유전류(Stray Current)에 의한 지하지장물 부식 방지용 엘라스토머 박스(Elastomer Box) 절연 상태를 검측했는가?</li>
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 승강장 급속 충전 장치(DC 750V/1000A) 오버헤드 펜타그래프 접촉 및 절연 저항(≥10MΩ)을 확인하였는가?</li>
        </ul>
        """
    },

    "통신분야": {
        "standard": """
        <div class="manual-v1-integration-box" style="background-color: #F0FDF4; border: 1.5px solid #22C55E; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #15803D; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> [동탄트램 업무 매뉴얼 v1 연계] 정보통신 분야 기술 표준 수칙
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>700MHz LTE-R 음영지역 제로화:</strong> 본선 및 차량기지 전 구간 수신강도 RSSI ≥ -95dBm, RSRP ≥ -105dBm, 핸드오버 성공률 ≥ 99.5% 확보</li>
                <li><strong>광백본 72-Core 이중화 링:</strong> 72-Core 싱글모드 광케이블(ITU-T G.652D) 이중화 링 백본 망 및 OTDR 접속 손실 ≤ 0.05dB/splice 관리</li>
                <li><strong>4K IP CCTV & PIS/PA/PSD 인터페이스:</strong> 24시간 이중화 4K CCTV, 승강장 PIS 시각 오차 ≤ 1초, PA 음향명료도 STI ≥ 0.6, PSD 통신 지연 ≤ 100ms 수칙 준수</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="manual-v1-integration-box" style="background-color: #F0FDF4; border: 1.5px solid #22C55E; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #15803D; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> [동탄트램 업무 매뉴얼 v1 연계] 통신설비 시공 수행지침
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>지하지장물 이설비 PS(Provisional Sum) 확인:</strong> 통신관/가스관 지하 이설 시 내역서상 PS 항목 지정 및 유관기관 협약 수칙 준수</li>
                <li><strong>전력 케이블 유도장해 차폐:</strong> 전력 케이블과 30cm 이상 금속 관로 이격 및 광배선함(OFD) 접지저항 ≤ 10Ω 시공</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 700MHz LTE-R 전 구간 무선 수신강도(RSSI ≥ -95dBm) 및 핸드오버(≥99.5%) 시험을 완료했는가?</li>
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 72-Core 광백본 이중화 링 망의 OTDR 접속 손실(≤0.05dB/splice) 성과표를 검측했는가?</li>
            <li>☐ <strong>[동탄트램 매뉴얼 v1]</strong> 통신관로 이설 시 전력선 유도장해 차폐 트레이 및 30cm 이격 시방을 준수했는가?</li>
        </ul>
        """
    }
}

updated_std = 0
updated_gui = 0
updated_chk = 0

for root, dirs, files in os.walk(base_attach_dir):
    rel_path = os.path.relpath(root, base_attach_dir)
    disc_name = rel_path.split(os.sep)[0]
    
    if disc_name not in v1_integration_data:
        continue
        
    data_for_disc = v1_integration_data[disc_name]
    
    for f in files:
        file_path = os.path.join(root, f)
        if f.endswith('_표준서.html'):
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            if 'manual-v1-integration-box' not in content:
                pattern = r'(<div class="(?:footer-note|bg-slate-900[^"]*footer[^"]*|bg-slate-900[^"]*text-slate-400)">)'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, data_for_disc['standard'] + '\n\\1', content)
                else:
                    new_content = re.sub(r'(</body>)', data_for_disc['standard'] + '\n\\1', content)
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(new_content)
                updated_std += 1
                
        elif f.endswith('_수행지침.html'):
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            if 'manual-v1-integration-box' not in content:
                pattern = r'(<div class="(?:footer-note|bg-slate-900[^"]*footer[^"]*|bg-slate-900[^"]*text-slate-400)">)'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, data_for_disc['guideline'] + '\n\\1', content)
                else:
                    new_content = re.sub(r'(</body>)', data_for_disc['guideline'] + '\n\\1', content)
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(new_content)
                updated_gui += 1

        elif f.endswith('_체크리스트.html'):
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            if '[동탄트램 매뉴얼 v1]' not in content:
                pattern = r'(<h2>3\. (?:협력사 공사관리 검측 확인사항|Subcontractor Verification).*?</h2>)'
                if re.search(pattern, content):
                    new_content = re.sub(pattern, '\\1\n' + data_for_disc['checklist'], content)
                else:
                    pattern_fallback = r'(<div class="(?:mt-8 pt-6 border-t|footer-note|bg-slate-900)">)'
                    new_content = re.sub(pattern_fallback, data_for_disc['checklist'] + '\n\\1', content)
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(new_content)
                updated_chk += 1

print(f"Dongtan Tram Manual v1 Integration Complete!")
print(f"  - Updated {updated_std} 표준서.html files in 신호/전기/통신")
print(f"  - Updated {updated_gui} 수행지침.html files in 신호/전기/통신")
print(f"  - Updated {updated_chk} 체크리스트.html files in 신호/전기/통신")
