import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

# Discipline-specific subcontractor advisory text mappings derived from Wirye Tram Contractors (Jeongju & Tripol Construction)
advisory_data = {
    "콘크리트도상": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 시공업체(정주건설·트리폴건설) 자문 반영
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>시공 순서 최우선 원칙:</strong> 누적 시공 오차로 인한 전체 선형 틀어짐을 방지하기 위해 분기기(Turnout) 구간을 최선순위로 선시공할 것 (트리폴건설 자문)</li>
                <li><strong>탑다운 타설 환경제어:</strong> 하절기 및 낮 타설 시 일사열에 의한 레일 신장 및 궤각 뒤틀림(Buckling) 발생 위험이 크므로 궤도 탑다운 콘크리트는 반드시 야간 타설 수행 (정주건설 자문)</li>
                <li><strong>레일 반입 길이 규격:</strong> 홈레일 18m 반입 시 도심지 가로수 및 장애물 저촉 여부 사전 검토 필수, 20m 반입 시 운반차량 최소 회전반경 확보 및 25m 특수통행허가 취득 (정주건설 자문)</li>
                <li><strong>교차로/횡단부 공법:</strong> 교통 전면 통제 최소화를 위해 교차로·횡단부는 프리캐스트 PST 패널 공법을 적용하고 양생 3일 조강/초속경 콘크리트 연계 시공 (정주/트리폴 자문)</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 시공업체 현장 수행지침 (정주건설·트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>1km 단위 공구 분할 관리:</strong> 레일 뒤틀림 리스크 방지를 위해 과도한 분할은 금지하되 도심지 차선 점용 효율성을 위해 1km 단위로 공사구간을 분할하여 공정 제어</li>
                <li><strong>일반구간 ➡️ 횡단부 ➡️ 전이구간 수칙:</strong> 일반구간 현장타설 후 도로 횡단부 PST 설치, 최종 전이구간 현장타설 순서로 단계별 연계 시공</li>
                <li><strong>하절기 야간 타설 온도 관리:</strong> 대기온도 30℃ 이상 하절기에는 레일 온도 상승으로 인한 신장 방지를 위해 22:00~06:00 야간 타설 수칙 엄수</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 시공 오차 누적 방지를 위해 분기기(Turnout) 구간을 최선순위로 선시공하였는가? (트리폴건설 자문)</li>
            <li>☐ <strong>[협력업체 자문]</strong> 하절기 일사열에 의한 레일 뒤틀림 예방을 위해 탑다운 콘크리트 타설을 야간시간대에 시행하는가? (정주건설 자문)</li>
            <li>☐ <strong>[협력업체 자문]</strong> 도로 교차로/횡단부 급속 개방을 위한 프리캐스트 PST 패널 및 양생 3일 조강 콘크리트를 준비하였는가? (정주/트리폴 자문)</li>
            <li>☐ <strong>[협력업체 자문]</strong> 18m/20m 레일 도심지 운반 시 가로수 저촉 여부 및 25m 특수통행허가증을 확보하였는가? (정주건설 자문)</li>
        </ul>
        """
    },
    
    "사전토공사": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 시공업체(정주건설·트리폴건설) 사전 토공 자문
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>가설 배치플랜트(B/P) 및 부지 확보:</strong> 궤도 조강 콘크리트 공급을 위해 현장 10km 이내 임시 B/P 및 레일/자재 야적 부지 사전 확보 필수 (정주건설 자문)</li>
                <li><strong>공동구 시공 변경 검토:</strong> 토공 완료 후 시스템 공동구 후속 시공 시 RC 현장타설 대신 양질의 모래 채움 변경안 검토로 시공성/경제성 확보 (정주건설 자문)</li>
                <li><strong>도로 점용 및 우회차로 확보:</strong> 트램 부지 외 양방향 우회 통행로 및 최소 1차선 이상 건설 장비 양중 점용 공간 사전 확보 (정주/트리폴 자문)</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 사전토공 및 차로점용 수행지침 (정주건설·트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>노선 구간 전폭 점용 수칙:</strong> 상/하선 별도 시공 시에도 단일 노선 기준 전폭 차선 통제 수칙을 적용하여 시공 안정성 확보</li>
                <li><strong>지장물 우선 처리 수칙:</strong> 한전/통신/가스관 위탁 지장물 이설이 완전히 종료된 후 굴착 및 본 토공 장비 투입</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 레일 야적 및 가설 B/P 용지가 확보되었는가? (정주건설 자문)</li>
            <li>☐ <strong>[협력업체 자문]</strong> 위탁 지장물(한전, 가스, 통신) 이설 완료 여부를 확인 후 토공에 착수하였는가? (트리폴건설 자문)</li>
        </ul>
        """
    },

    "상부강화노반": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 시공업체(정주건설·트리폴건설) 노반 자문
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>노반 완료 후 궤도 인계:</strong> 노반 공사가 최소 1~2km 구간 완료된 후 궤도 공정을 인계하여 연속성 확보 (정주건설 자문)</li>
                <li><strong>배수박스 레미콘 상하중 검토:</strong> 하부 배수박스 및 하수구조물 위 레미콘/대형 토공 장비 통과 시 상부 하중 안전성 검토 (정주건설 자문)</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 강화노반 시공 수행지침 (정주건설·트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li>강화노반 완료 후 하부 공동구 설치 시 노반 침하 및 균열이 발생하지 않도록 역순 시공 시 모래/양질 토사 채움 및 다짐 철저</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 최소 1~2km 노반 완료 후 궤도 공정에 전달 인계하였는가? (정주건설 자문)</li>
            <li>☐ <strong>[협력업체 자문]</strong> 하부 배수박스 위 대형 레미콘/장비 통과 시 구조 하중 안전성을 검토하였는가? (정주건설 자문)</li>
        </ul>
        """
    },

    "건축": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 차량기지 건축 자문 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>검수고 피트 궤도 연결부:</strong> 검수고 피트 레일과 본선 궤도 연결부 부등침하 예방을 위한 조강 콘크리트 및 이중 앵커 시방 적용</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 건축/검수고 수행지침 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li>검수고 매설 레일 타설 시 작업조를 통합 운영하여 피트 구조물과 궤도 선형 오차를 동시에 조정</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 검수고 피트 궤도 연결부 조강 콘크리트 및 레일 앵커 상태를 검측하였는가?</li>
        </ul>
        """
    },

    "신호분야": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 신호·우선신호 자문 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>교차로 신호 우선 제어:</strong> PPC 보드/LTE 모뎀 함체 위치를 도로 횡단부 굴착 작업선에서 최소 5m 이상 이격 가설하여 손상 방지</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 신호설비 수행지침 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li>선로전환기 및 축차계수기 설치 위치를 분기기 궤도 선시공 직후 통합 검측 시행</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 교차로 PPC 신호함체가 도로 굴착선에서 안전 이격 거리(5m)를 확보했는가?</li>
        </ul>
        """
    },

    "통신분야": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 통신 망 자문 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>PSD 및 광케이블 백본:</strong> PSD 신호 통신선과 광백본 72-Core 배선을 타 전력 케이블과 30cm 이상 이격 배선</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 통신설비 수행지침 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li>LTE-R 및 CCTV 함체 전원 인입 시 전차선 급전 케이블 유도장해 영향을 방지하기 위해 차폐 트레이 적용</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 통신 케이블 차폐 트레이 적용 및 전력선 이격 거리를 확인하였는가?</li>
        </ul>
        """
    },

    "전기분야": {
        "standard": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 위례선 트램 전력·전차선 자문 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>DC 750V 정류기 및 레일 귀선:</strong> 주행 레일 누설전류(Stray Current) 부식 방지를 위한 디오드 접지 장치(Polarization Cell)를 레일 콘크리트 타설 전 선제 설치</li>
            </ul>
        </div>
        """,
        "guideline": """
        <div class="subcontractor-advisory-box" style="background-color: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 18px; margin-top: 20px;">
            <h4 style="color: #B45309; margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>👷</span> [협력업체 실무 자문] 전력설비 수행지침 (정주/트리폴건설)
            </h4>
            <ul style="margin: 0; padding-left: 20px; color: #78350F; font-size: 0.92rem; line-height: 1.7;">
                <li>무전차선 승강장 대전류 급속 충전 장치 설치 시 레일 및 승강장 구조체 절연 저항 10MΩ 이상 측정 확인</li>
            </ul>
        </div>
        """,
        "checklist": """
        <ul class="bullet-list" style="margin-top: 10px;">
            <li>☐ <strong>[협력업체 자문]</strong> 누설전류(Stray Current) 방지 디오드 접지 장치가 레일 타설 전 정상 거치되었는가?</li>
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
    
    if disc_name not in advisory_data:
        continue
        
    data_for_disc = advisory_data[disc_name]
    
    for f in files:
        file_path = os.path.join(root, f)
        if f.endswith('_표준서.html'):
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            if 'subcontractor-advisory-box' not in content:
                # Insert inside section 5 or near footer
                pattern = r'(<div class="footer-note">)'
                new_content = re.sub(pattern, data_for_disc['standard'] + '\n\\1', content)
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(new_content)
                updated_std += 1
                
        elif f.endswith('_수행지침.html'):
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            if 'subcontractor-advisory-box' not in content:
                pattern = r'(<div class="footer-note">)'
                new_content = re.sub(pattern, data_for_disc['guideline'] + '\n\\1', content)
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(new_content)
                updated_gui += 1

        elif f.endswith('_체크리스트.html'):
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            if '[협력업체 자문]' not in content:
                pattern = r'(<h2>3\. 협력사 공사관리 검측 확인사항 \(Subcontractor Verification\)?</h2>)'
                new_content = re.sub(pattern, '\\1\n' + data_for_disc['checklist'], content)
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(new_content)
                updated_chk += 1

print(f"Embedding Complete!")
print(f"  - Updated {updated_std} 표준서.html files")
print(f"  - Updated {updated_gui} 수행지침.html files")
print(f"  - Updated {updated_chk} 체크리스트.html files")
