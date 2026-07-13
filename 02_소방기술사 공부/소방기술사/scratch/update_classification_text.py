import os
import shutil
from bs4 import BeautifulSoup

def update_classification_text(file_path):
    print(f"Updating classification text under diagram inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_pipe_text_update"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Target card element
    card = soup.find(id="common_pipe_classification")
    if not card:
        print("Error: Could not find element with id='common_pipe_classification'")
        return False
        
    # Remove existing lists and tables after the zoomable-media container
    media_div = card.find(class_="zoomable-media")
    if not media_div:
        print("Error: Could not find zoomable-media div inside card")
        return False
        
    # Extract everything after the media_div inside the card
    siblings_to_remove = list(media_div.find_next_siblings())
    for sibling in siblings_to_remove:
        sibling.decompose()
        
    # 2. HTML to insert (Strictly without any '**' characters)
    new_text_html = r"""
    <!-- 직관적 비유 분석 섹션 -->
    <div style="margin-top: 30px; margin-bottom: 30px;">
        <h3 style="font-size: 1.2rem; font-weight: 800; color: var(--accent); margin-bottom: 18px; border-left: 4px solid var(--accent); padding-left: 10px;">
            1. 소방 배관의 성질별 직관적 비유와 이해
        </h3>
        <p class="desc" style="font-size: 0.92rem; color: var(--text-secondary); margin-bottom: 20px; line-height: 1.7;">
            소화 용수를 화점까지 실어 나르는 수송 혈관인 배관은 재질마다 고유한 물리적 방어 기작을 갖습니다. 실전 연상을 위해 일상 사물에 빗대어 분류합니다.
        </p>
        
        <div style="display: grid; grid-template-columns: 1fr; gap: 20px; margin-bottom: 25px;">
            <!-- 탄소강관 -->
            <div style="background-color: var(--bg-secondary); border: 1px solid var(--border); border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.01);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span style="background-color: rgba(239, 68, 68, 0.08); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 700;">탄소강관</span>
                    <span style="font-weight: 700; color: var(--text-primary); font-size: 0.95rem;">철제 플레이트 아머 (무거운 갑옷)</span>
                </div>
                <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.7; margin: 0;">
                    무겁고 단단하며 외부 기계적 충격에 잘 견디는 고전적 갑옷과 같습니다. 다만 산소와 수분에 장기 노출 시 내부에서 붉은 녹(부식)이 슬어 관이 얇아집니다. 고압을 견디기 위해서는 강관의 벽 두께(스케줄 번호)를 상향하여 물리적 강도를 높여야 합니다.
                </p>
            </div>
            
            <!-- 스테인리스강관 -->
            <div style="background-color: var(--bg-secondary); border: 1px solid var(--border); border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.01);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span style="background-color: rgba(16, 185, 129, 0.08); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 700;">스테인리스강관</span>
                    <span style="font-weight: 700; color: var(--text-primary); font-size: 0.95rem;">미래형 첨단 티타늄 슈트 (경량 방호복)</span>
                </div>
                <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.7; margin: 0;">
                    크롬 합금으로 형성된 부동태 피막 덕분에 물에 항시 젖어 있어도 녹이 슬지 않습니다. 강관 대비 인장 강도가 2배에 달해 얇은 두께(Sch 10)만으로도 고압을 안정적으로 견디며 건물 전체의 하중을 덜어줍니다. 단, 구리나 탄소강 등 타 금속과 닿으면 스스로 산화되는 전위차 부식(갈바닉)이 일어나므로 완벽한 절연이 요구됩니다.
                </p>
            </div>
            
            <!-- 합성수지관 -->
            <div style="background-color: var(--bg-secondary); border: 1px solid var(--border); border-radius: 10px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.01);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span style="background-color: rgba(59, 130, 246, 0.08); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.2); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 700;">합성수지관</span>
                    <span style="font-weight: 700; color: var(--text-primary); font-size: 0.95rem;">기능성 아웃도어 의류 (방수 자켓)</span>
                </div>
                <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.7; margin: 0;">
                    가볍고 유연하며 부식 및 스케일 우려가 없고 마찰 손실이 극도로 적습니다. 그러나 불꽃(열)에 닿으면 즉시 녹아내리는 치명적인 약점이 있어 직사광선이나 지상 노출 배관으로는 쓸 수 없습니다. 지반 침하를 버티는 지하 매설관이나 상시 물이 차 있고 천장 내부에 숨겨진 습식 계통(CPVC)에 한정하여 능력을 발휘합니다.
                </p>
            </div>
        </div>
    </div>

    <!-- 6대 파이프 종류 핵심 비교표 -->
    <div style="margin-top: 30px; margin-bottom: 30px;">
        <h3 style="font-size: 1.2rem; font-weight: 800; color: var(--accent); margin-bottom: 18px; border-left: 4px solid var(--accent); padding-left: 10px;">
            2. 소방 파이프 종류별 엔지니어링 특징 비교
        </h3>
        
        <table class="premium-data-table" style="width: 100%; border-collapse: collapse; margin: 15px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <thead>
                <tr style="background-color: var(--bg-secondary); border-bottom: 2px solid var(--border);">
                    <th style="padding: 12px; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); font-size: 0.85rem; text-align: center; width: 15%;">분류</th>
                    <th style="padding: 12px; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); font-size: 0.85rem; text-align: center; width: 22%;">재질 규격 및 가공</th>
                    <th style="padding: 12px; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); font-size: 0.85rem; text-align: center; width: 23%;">설계 한계 (압력/온도)</th>
                    <th style="padding: 12px; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); font-size: 0.85rem; text-align: center; width: 10%;">조도 (C)</th>
                    <th style="padding: 12px; font-weight: 800; color: var(--text-primary); font-size: 0.85rem; text-align: center; width: 30%;">소방 설계 핵심 요점</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">배관용 탄소강관</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">KS D 3507 (SPP)<br>아연도금 백관 / 흑관<br>전기저항용접(ERW), 단접</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">압력: 1.2 MPa 미만<br>온도: 350도 이하 안전<br>(400도 탄소 석출)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; text-align: center; color: var(--text-secondary); font-family: monospace;">습식: 120<br>건식: 100</td>
                    <td style="padding: 12px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">가장 범용적인 소화 배관이나 장기 사용 시 부식 및 스케일로 마찰 손실 증가. 건식 계통은 산소 유입으로 부식 가속.</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                    <td style="padding: 12px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">압력 탄소강관</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">KS D 3562 (SPPS)<br>이음매 없는 무계목(Seamless)<br>또는 고품질 ERW</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">압력: 1.2 MPa 이상 고압<br>온도: 350도 이하 안전<br>(400도 초과 시 취성 발생)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; text-align: center; color: var(--text-secondary); font-family: monospace;">습식: 120<br>건식: 100</td>
                    <td style="padding: 12px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">스프링클러 가압수송장치 토출측 및 고층부 수계 입상관 필수. 스케줄 번호 단위로 벽 두께를 상향 설계.</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">스테인리스강관</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">KS D 3576 (배관용)<br>KS D 3595 (일반배관용)<br>Cr-Ni계 고합금강</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">압력: 1.2 MPa 이상 고압 대응<br>온도: 고온 안정성 최상<br>(탄소강 온도 극복)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; text-align: center; color: #10b981; font-weight: 700; font-family: monospace;">150</td>
                    <td style="padding: 12px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">강관의 1600배에 달하는 반영구적 내부식성. Sch 10 규격의 박막 배관으로 경량화 실현. 갈바닉 전식 방지용 절연 부속 필수.</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                    <td style="padding: 12px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">라이닝 강관</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">KS D 3565 등<br>강관 내경부 피복 코팅<br>모르타르 / 합성수지(PE)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">압력: 모재 강관 성능 준용<br>온도: 피복재 융점 한계 준수<br>(PE 라이닝 저온 권장)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; text-align: center; color: var(--text-secondary); font-family: monospace;">모르타르: 140<br>수지피복: 150</td>
                    <td style="padding: 12px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">강재의 강도와 수지의 매끄러움 및 방청성을 결합. 가공 시 접합 단면부의 라이닝 손상 방지 대책이 시공 신뢰성 좌우.</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 12px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">CPVC 수지관</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">KS M 3414 (내열성 PVC)<br>염소화 처리 공법<br>자기소화성 소재</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">압력: 1.2 MPa 미만 (수계)<br>온도: 자기소화성 보유<br>(890도 화염 12분 저항)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; text-align: center; color: #10b981; font-weight: 700; font-family: monospace;">150</td>
                    <td style="padding: 12px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">부식 및 스케일이 전혀 발생하지 않아 영구적인 조도 보장. 시공 하중이 매우 낮고 접착 용융 결합으로 시공 속도 극대화.</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                    <td style="padding: 12px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">PE 수지관</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">KS D 3607 등<br>폴리에틸렌 압출 성형<br>고밀도/중밀도 수지</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; color: var(--text-secondary);">압력: 1.2 MPa 미만<br>온도: 120~140도 용융<br>(극저온 내동파성 우수)</td>
                    <td style="padding: 12px; border-right: 1px solid var(--border); font-size: 0.82rem; text-align: center; color: #10b981; font-weight: 700; font-family: monospace;">150</td>
                    <td style="padding: 12px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">지반 변동 및 동결 팽창에 강해 옥외 소방수 매설 배관에 주용 적용. 화재 열 변형 한계로 인해 지상 노출 시공은 금지됨.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- 소방공학적 적용 한계 수치 총정리 -->
    <div style="margin-top: 30px; margin-bottom: 10px;">
        <h3 style="font-size: 1.2rem; font-weight: 800; color: var(--accent); margin-bottom: 18px; border-left: 4px solid var(--accent); padding-left: 10px;">
            3. 소방공학 설계 한계 및 수치적 판정 기준
        </h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <!-- 사용 압력 및 온도 한계 -->
            <div style="background-color: var(--bg-secondary); border: 1px solid var(--border); border-radius: 10px; padding: 18px;">
                <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--text-primary); margin: 0 0 12px 0; border-bottom: 1px solid var(--border); padding-bottom: 8px;">
                    사용 압력 및 열적 안전 경계
                </h4>
                <ul style="margin: 0; padding-left: 18px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;">
                    <li style="margin-bottom: 8px;">
                        <span style="color: var(--accent); font-weight: 700;">1.2 MPa 기준선:</span> 펌프의 체절 운전 압력 또는 계통 최대압력이 1.2 MPa를 초과할 경우 일반 SPP 강관은 사용할 수 없으며, 고정 스케줄 번호(Sch 40 이상)를 지정한 SPPS 또는 고압용 STS 배관(KS D 3576)을 의무 적용해야 합니다.
                    </li>
                    <li>
                        <span style="color: var(--accent); font-weight: 700;">400도 탄소 석출 한계:</span> 탄소강 배관은 350도 이하 작동이 안전하며, 400도를 돌파하여 장시간 운전 시 강 내부의 탄소가 석출(흑연화 현상)되어 강관의 결정 입계가 깨지고 연성을 상실하여 고압 취성 붕괴를 일으킵니다.
                    </li>
                </ul>
            </div>
            
            <!-- 조도계수 및 전식 방지 -->
            <div style="background-color: var(--bg-secondary); border: 1px solid var(--border); border-radius: 10px; padding: 18px;">
                <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--text-primary); margin: 0 0 12px 0; border-bottom: 1px solid var(--border); padding-bottom: 8px;">
                    수리 조도계수 및 전이 부식 차단
                </h4>
                <ul style="margin: 0; padding-left: 18px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;">
                    <li style="margin-bottom: 8px;">
                        <span style="color: var(--accent); font-weight: 700;">Hazen-Williams 조도계수:</span> 배관 재질에 따라 내마찰 등급(C값)을 다르게 부여합니다. 부식 가혹도가 큰 건식 강관은 패널티 값인 C=100을, 아연도금 습식은 C=120을, 부식이 없고 영구 평활도가 유지되는 STS 및 CPVC는 최고치인 C=150을 대입하여 설계합니다.
                    </li>
                    <li>
                        <span style="color: var(--accent); font-weight: 700;">이종 금속 갈바닉 전위차:</span> 스테인리스관과 강관 또는 구리관을 혼용 배치할 때 발생하는 전지식 이온 부식을 원천 봉쇄하기 위해, 전위차가 다른 두 전극 배관 사이에 전도성 전로를 차단하는 절연 플랜지나 절연 개스킷 부속 시공을 필수화합니다.
                    </li>
                </ul>
            </div>
        </div>
    </div>
    """
    
    # 3. Append after media_div inside card
    media_div.insert_after(BeautifulSoup(new_svg_html if 'new_svg_html' in locals() else new_text_html, "html.parser"))
    print("Successfully updated structured text below diagram inside BeautifulSoup DOM.")
    
    # 4. Save back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = update_classification_text(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
