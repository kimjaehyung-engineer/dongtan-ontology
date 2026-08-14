import os

def rewrite_depot():
    files = [
        "08.메뉴얼 및 평면도/동탄트램_업무_매뉴얼.html",
        "03_보고서_및_출력/지장물_이설_업무_매뉴얼.html"
    ]
    
    # Define the new, highly structured, actionable vehicle depot section
    new_section = """
        <!-- Section 4. 차량기지 -->
        <section id="sec-depot" style="margin-bottom: 5.5rem; scroll-margin-top: 4.5rem; margin-top: 1rem;">
            <div style="border-bottom: 2px solid var(--border-color); padding-bottom: 1.25rem; margin-bottom: 2.5rem; margin-top: 1rem;">
                <span class="category-tag" style="margin-bottom: 0.5rem; display: inline-block;">차량기지 실무 가이드라인 (설계·시공 통합)</span>
                <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.6rem; letter-spacing: -0.02em;">
                    4. 차량기지
                </h1>
                <p style="color: var(--text-muted); font-size: 1rem; font-weight: 500; margin: 0; line-height: 1.6;">
                    노면전차 차량기지 구축의 핵심 설계 요소를 정의하고, 설계/집행 단계에서 원가 상승 및 공기 지연 리스크를 선제 차단하기 위한 단계별 검증 규격입니다.
                </p>
            </div>

            <!-- 4.1 핵심 설계 요소 -->
            <div id="sec-depot-1" class="sub-section">
                <h3>4.1 핵심 설계 요소: 표준 기준 vs. 동탄트램 구현</h3>
                <p>
                    차량기지 계획 수립 시 자질구레한 세부 치수를 지양하고, 사업성 및 운영 효율을 좌우하는 **3대 핵심 설계 요소**를 도출하여 표준 대비 동탄트램의 설계 솔루션을 대조 제시합니다.
                </p>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 1.5rem; margin-bottom: 2rem;">
                    <thead>
                        <tr style="background-color: var(--card-bg); border-bottom: 2px solid var(--border-color);">
                            <th style="width: 25%; padding: 1rem; text-align: left; font-weight: 700;">핵심 설계 요소</th>
                            <th style="width: 35%; padding: 1rem; text-align: left; font-weight: 700; color: var(--text-secondary);">트램 차량기지 표준 기준</th>
                            <th style="width: 40%; padding: 1rem; text-align: left; font-weight: 700; color: var(--accent-color);">동탄트램 실제 구현 및 개선 효과</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 1.25rem 1rem; font-weight: 700;"><strong>① 검수 선로 배선 계획</strong></td>
                            <td style="padding: 1.25rem 1rem; color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
                                일상·월상검사선, 청소선 등을 각각 개별 독립 선로(최소 9선 이상)로 유치 배선하여 운용 효율 도모.
                            </td>
                            <td style="padding: 1.25rem 1rem; font-size: 0.9rem; line-height: 1.6;">
                                <strong>[배선 축소: 9선 ➔ 6선 직렬 배치]</strong><br>
                                유사 검수 기능선(일상+월상 / 대청소+청소)을 단일 선로상에 일렬로 통합 배치하여 검수고 면적 20%를 절감하고 초기 건축비 감소.
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 1.25rem 1rem; font-weight: 700;"><strong>② 행정·현장 동선 배치</strong></td>
                            <td style="padding: 1.25rem 1rem; color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
                                관리 업무 중심의 종합관리동과 현장 정비 중심의 검수동을 부지 여건에 따라 분리 설치 (이격 거리 무관).
                            </td>
                            <td style="padding: 1.25rem 1rem; font-size: 0.9rem; line-height: 1.6;">
                                <strong>[동선 최소화: 320m ➔ 44~56m 인접]</strong><br>
                                기존 320m의 과다 이격 배치를 수평 44m~56m로 밀착 배치하여 행정-검수 근무자 간의 도보 동선 단축 및 신속 비상 대응력 확보.
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 1.25rem 1rem; font-weight: 700;"><strong>③ 검수 설비 및 전력 안전</strong></td>
                            <td style="padding: 1.25rem 1rem; color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6;">
                                전통적인 중량 전동차용 공작기계(7종) 내역 반영 및 고압 배터리 충전 장치 임의 배치.
                            </td>
                            <td style="padding: 1.25rem 1rem; font-size: 0.9rem; line-height: 1.6;">
                                <strong>[설비 일원화 및 감전 예방]</strong><br>
                                트램 특성상 불필요한 공작기계 7종 설계 제외 및 <strong>차륜전삭기 1식으로 통합</strong>. 충전 장치를 물 세척 구역(청소선)에서 분리하여 일상선 건조 구역으로 이설하고 감전 사고 예방.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 4.2 설계 단계 리스크 방지 체크리스트 -->
            <div id="sec-depot-2" class="sub-section" style="margin-top: 3.5rem;">
                <h3>4.2 [설계 단계] 원가·공기 증가 리스크 방지 체크리스트</h3>
                <p>
                    설계 납품 및 승인 전 아래 **3가지 핵심 구조적 간섭 요건**을 사전 검증하지 않을 경우, 시공 중 재설계 및 궤도 뜯어내기 등으로 인한 원가 상승 및 공기 지연 리스크가 발생합니다.
                </p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-top: 1.5rem;">
                    <div style="padding: 1.25rem; border: 1px solid var(--border-color); border-radius: 12px; background-color: var(--bg-color);">
                        <div style="color: var(--warning-color); font-weight: 800; font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
                            ⚠️ 유치선 차량한계 간섭
                        </div>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.6; margin: 0;">
                            <strong>리스크 요인:</strong> 유치선 중심 간격 미달 시 열차 통과 중 신호기 기초 접촉 사고 발생.<br>
                            <strong>설계 검증 기준:</strong> 유치선 간격을 3.6m 이상 확보하고, 선로 사이에 설치되는 분기부 신호기 및 진로표시기 설치 폭(최소 402mm) 확보 여부를 CAD 도면에서 물리 검증할 것.
                        </p>
                    </div>
                    <div style="padding: 1.25rem; border: 1px solid var(--border-color); border-radius: 12px; background-color: var(--bg-color);">
                        <div style="color: var(--warning-color); font-weight: 800; font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
                            ⚠️ 대차 인양-크레인 작업 간섭
                        </div>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.6; margin: 0;">
                            <strong>리스크 요인:</strong> 차량 대차 분리를 위한 동시인양장치 작동 시, 상부 천장 크레인과 간섭되어 공정 마비.<br>
                            <strong>설계 검증 기준:</strong> 대차 탈거 후 차체를 임시 거치할 수 있는 <strong>250㎡(5m×50m) 규모의 전용 차체작업장</strong> 및 차량 받침대 레이아웃이 평면도상에 독립 구획되었는지 확인할 것.
                        </p>
                    </div>
                    <div style="padding: 1.25rem; border: 1px solid var(--border-color); border-radius: 12px; background-color: var(--bg-color);">
                        <div style="color: var(--warning-color); font-weight: 800; font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
                            ⚠️ 장비유치선(모타카선) 동선 꼬임
                        </div>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.6; margin: 0;">
                            <strong>리스크 요인:</strong> 레일연마차 등 유지보수 차량이 진입할 때 일반 트램 유치선 동선과 간섭되어 전 차량 출고 지연.<br>
                            <strong>설계 검증 기준:</strong> 궤도 유지보수 장비를 보관하고 독립적으로 인상할 수 있는 <strong>장비유치선(유효장 136m 이상) 1선</strong>이 유치선 상단에 별도로 노선 연결 설계되었는지 확인할 것.
                        </p>
                    </div>
                </div>
            </div>

            <!-- 4.3 시공 단계 사전 체크리스트 -->
            <div id="sec-depot-3" class="sub-section" style="margin-top: 3.5rem;">
                <h3>4.3 [시공 단계] 기지 내 주요 공종작업 전 필수 사전 체크리스트</h3>
                <p>
                    차량기지 내부 공종별 협력업체 투입 및 물리적 작업 시작 전, 현장 감리원과 시공 관리자는 아래 **공종별 필수 안전·품질 대책**이 현장에 선제 조치되었는지 검증해야 합니다.
                </p>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 1.5rem;">
                    <thead>
                        <tr style="background-color: var(--card-bg); border-bottom: 2px solid var(--border-color);">
                            <th style="width: 25%; padding: 0.75rem; text-align: left;">대상 기지 공종</th>
                            <th style="width: 50%; padding: 0.75rem; text-align: left;">작업 착수 전 필수 체크 및 검증 기준 (현장 감리 확인 사항)</th>
                            <th style="width: 25%; padding: 0.75rem; text-align: left;">허용 오차 및 비고</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td><strong>① 차륜전삭기 피트(Pit) 굴착 및 하부 기초 공사</strong></td>
                            <td style="font-size: 0.875rem; line-height: 1.6; padding: 1rem 0.75rem;">
                                <ul>
                                    <li>차륜전삭기 설치용 하부 피트(Pit) 철근 콘크리트 타설 전, 인근 기둥 구조물 기초로의 하중 전이 유무 재확인.</li>
                                    <li>전삭 작업 시 발생하는 미세 쇠가루(분철) 반출을 위한 <strong>화물차량 진입 통로(폭 5m 이상)</strong>가 골조 시공 단계에서 가로막히지 않았는지 확인.</li>
                                </ul>
                            </td>
                            <td style="font-size: 0.85rem; color: var(--text-secondary); padding: 1rem 0.75rem;">
                                피트 중심 축선 오차 ±5mm 이내 관리
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td><strong>② 배터리 충전 공급 장치 및 전기실 결선</strong></td>
                            <td style="font-size: 0.875rem; line-height: 1.6; padding: 1rem 0.75rem;">
                                <ul>
                                    <li>충전 장치가 배치될 일상/월상검사선 구역에 습기 침투 방지를 위한 배수 역류 방지 트렌치가 가동 준비되었는지 확인 (물 청소선과의 완전 격리 검증).</li>
                                    <li>2층으로 격리된 변전소/변압기실 내부 접지 저항 값 최종 측정(10옴 이하 규격 만족 여부 확인).</li>
                                </ul>
                            </td>
                            <td style="font-size: 0.85rem; color: var(--text-secondary); padding: 1rem 0.75rem;">
                                접지 저항계 실측 데이터 검수서 제출 필수
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td><strong>③ 옥상 점검대 및 안전 난간 조립</strong></td>
                            <td style="font-size: 0.875rem; line-height: 1.6; padding: 1rem 0.75rem;">
                                <ul>
                                    <li>트램 지붕의 배터리 모듈을 점검할 수 있는 대청소선 옥상점검대 설치 전, 차량 접촉 한계와의 안전 이격 거리 확보 확인.</li>
                                    <li>작업자 추락 방지 안전 고리 체결선(안전 라인)의 연속 체결 고리가 흔들림 없이 고정되었는지 인장 테스트 확인.</li>
                                </ul>
                            </td>
                            <td style="font-size: 0.85rem; color: var(--text-secondary); padding: 1rem 0.75rem;">
                                안전 고리 체결 하중 15kN 이상 견딤 테스트
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td><strong>④ 대차 도장실 환기/송풍기 시공</strong></td>
                            <td style="font-size: 0.875rem; line-height: 1.6; padding: 1rem 0.75rem;">
                                <ul>
                                    <li>분진과 유해가스가 배출되는 활성탄 필터 및 대형 송풍 설비가 건물 외부 독립 프레임 상에 배치 완료되었는지 확인.</li>
                                    <li>차륜전삭선 전용 칩 크래셔 가스 배출 덕트의 댐퍼 열림 감지 센서 연동 여부 확인.</li>
                                </ul>
                            </td>
                            <td style="font-size: 0.85rem; color: var(--text-secondary); padding: 1rem 0.75rem;">
                                배기 풍량 기본 설계 규격 대비 100% 이상 확인
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    """
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"File {filepath} not found. Skipping.")
            continue
            
        print(f"Rewriting depot section in {filepath}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Replace the section in the body
        start_sec = content.find('<!-- Section 4. 차량기지 -->')
        end_sec = content.find('<!-- Section 5. 건축계획 -->')
        if end_sec == -1:
            end_sec = content.find('<!-- Section 6. 토질 및 기초 -->')
            
        if start_sec != -1 and end_sec != -1:
            content = content[:start_sec] + new_section + "\n\n" + content[end_sec:]
            print("  Successfully updated body Section 4!")
        else:
            print("  Warning: Could not locate Section 4 boundaries in the body.")
            
        # 2. Update the sidebar aside block to reflect exactly 3 sub-items
        # Let's target the exact aside HTML code around Section 4.
        # We will find the nav-item for sec-depot.
        
        # To do this safely, we can replace the entire <li class="nav-item" data-target="sec-depot"> block
        # Let's locate it:
        start_aside_depot = content.find('<li class="nav-item" data-target="sec-depot">')
        if start_aside_depot != -1:
            # Find the closing </li> of this list item (it has a nested <ul>)
            # Since there is a nested <ul>, the closing </li> of sec-depot is after the closing </ul>.
            # We can find the closing </ul> after start_aside_depot, then find the next </li>.
            end_ul = content.find('</ul>', start_aside_depot)
            if end_ul != -1:
                end_aside_depot = content.find('</li>', end_ul)
                if end_aside_depot != -1:
                    old_sidebar_block = content[start_aside_depot:end_aside_depot + 5]
                    
                    new_sidebar_block = """<li class="nav-item" data-target="sec-depot">
            <a href="#sec-depot">4. 차량기지</a>
            <ul class="sub-nav-list">
                <li class="sub-nav-item" data-target="sec-depot-1"><a href="#sec-depot-1">4.1 핵심 설계요소 (기준 vs. 구현)</a></li>
                <li class="sub-nav-item" data-target="sec-depot-2"><a href="#sec-depot-2">4.2 설계단계 체크리스트 (원가/공기)</a></li>
                <li class="sub-nav-item" data-target="sec-depot-3"><a href="#sec-depot-3">4.3 시공단계 체크리스트 (공종작업전)</a></li>
            </ul>
        </li>"""
                    content = content[:start_aside_depot] + new_sidebar_block + content[end_aside_depot + 5:]
                    print("  Successfully updated sidebar depot block!")
                else:
                    print("  Warning: Could not find closing </li> of sec-depot aside.")
            else:
                print("  Warning: Could not find closing </ul> of sec-depot aside.")
        else:
            print("  Warning: Could not find start of sec-depot aside.")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved {filepath} successfully!")

if __name__ == '__main__':
    rewrite_depot()
