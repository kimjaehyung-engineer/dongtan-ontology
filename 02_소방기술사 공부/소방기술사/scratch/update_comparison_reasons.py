import os
import shutil
from bs4 import BeautifulSoup

def update_comparison_reasons(file_path):
    print(f"Updating comparison table with reasons in: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_comparison_reasons"
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
        
    # 2. Find the first table inside this card (which is the comparison table)
    tables = card.find_all("table")
    if not tables:
        print("Error: No tables found inside common_pipe_classification")
        return False
        
    # The first table is the comparison table (6대 분류)
    comp_table = tables[0]
    
    # 3. New Premium Table HTML (No '**' symbols, with '※' explanations)
    new_comp_table_html = r"""
    <table class="comparison-table" style="width: 100%; border-collapse: collapse; margin: 15px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
        <thead>
            <tr style="background-color: var(--bg-secondary); border-bottom: 2px solid var(--border);">
                <th style="padding: 12px; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); font-size: 0.85rem; text-align: center; width: 15%;">분류</th>
                <th style="padding: 12px; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); font-size: 0.85rem; text-align: center; width: 35%;">주요 특성 및 물리적 강도</th>
                <th style="padding: 12px; font-weight: 800; color: var(--text-primary); font-size: 0.85rem; text-align: center; width: 50%;">소방 실무 적용처 및 선정 이유</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 14px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">강관<br>(Steel)</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    높은 인장 강도와 내압성, 내충격성을 지녀 수압 및 기계적 외력이 가해지는 배관에 최적. 단, 습식 상태에서 부식 발생 가능.
                </td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    수계소화설비(스프링클러, 소화전) 지상부 배관, 가스계 고압 배관, 감압 배관 등 소방의 핵심 중추 배관.<br>
                    <span style="color: var(--accent); display: block; margin-top: 6px; font-size: 0.82rem; line-height: 1.5;">
                        ※ 펌프 급가동 시 배관 내부에 작용하는 순간적인 고압과 거친 수격작용(워터해머)을 배관 파열 없이 유일하게 버텨낼 수 있는 기계적 인장력이 있기 때문에 지상의 압력 배관 계통에 범용적으로 적용됩니다.
                    </span>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                <td style="padding: 14px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">동관<br>(Copper)</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    내식성과 열전도율이 우수하며 마찰 손실이 적음. 가공성이 좋으나 강관 대비 기계적 충격에 약함.
                </td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    스프링클러설비 신축배관, 냉난방 겸용 배관, 소형 가압 급수용 관로.<br>
                    <span style="color: var(--accent); display: block; margin-top: 6px; font-size: 0.82rem; line-height: 1.5;">
                        ※ 구리 특유의 연성 덕분에 좁고 복잡한 이중천장 내부 공간에서도 용접 없이 쉽게 구부려(곡관 가공) 밀착 시공할 수 있으며, 열전도율이 매우 높아 화재 발생 시 헤드 주변의 열을 신속하게 감지·전달하기 때문입니다.
                    </span>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 14px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">주철관<br>(Cast Iron)</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    내식성과 내구성이 뛰어나 부식성 환경에 강하나, 취성(약한 충격에 쉽게 깨짐)이 있음.
                </td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    옥외 지중 매립용 소화용수 주배관, 배수관.<br>
                    <span style="color: var(--accent); display: block; margin-top: 6px; font-size: 0.82rem; line-height: 1.5;">
                        ※ 두께가 매우 두껍고 외부 흙(토양) 및 습기에 접촉해도 부식에 견디는 힘이 강해 수십 년간 지하에 매설해도 관벽이 손상되지 않습니다. 단, 때리는 기계적 충격(수격 등)에는 쉽게 깨지는 단점이 있어 충격이 전해지지 않는 지하 토양 속에만 묻어 사용합니다.
                    </span>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                <td style="padding: 14px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">스테인리스관<br>(STS)</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    크롬(Cr) 피막 형성으로 내부식성이 반영구적이며, 배관 두께를 얇게(박막화) 설계할 수 있어 경량화 가능.
                </td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    수계소화설비 입상배관 및 수조 흡입측 배관, 배관용 스테인리스강관(SSC/SPSU).<br>
                    <span style="color: var(--accent); display: block; margin-top: 6px; font-size: 0.82rem; line-height: 1.5;">
                        ※ 장기간 소화수가 채워진 채 대기해도 내부에 녹 찌꺼기(스케일)가 전혀 슬지 않아, 화재 시 스프링클러 헤드의 작은 미세 방사구멍이 부식 파편으로 막히는 사고를 원천 예방합니다. 또한 일반 철관보다 강도가 2배 세서 배관을 얇게 제작해도 고압을 견뎌 건물 하중을 획기적으로 낮춰줍니다.
                    </span>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 14px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">합성수지관<br>(Plastic)</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    부식이 전혀 없고 마찰손실계수(C=150)가 극히 낮아 에너지 효율이 좋으나, 고열에 취약함.
                </td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    소방용 CPVC 배관 (지하 매설 및 노출 시 천장 은폐부 시공), 지중 소수관.<br>
                    <span style="color: var(--accent); display: block; margin-top: 6px; font-size: 0.82rem; line-height: 1.5;">
                        ※ 관 내벽이 거울처럼 매끄러워 물이 마찰 저항을 거의 받지 않고 고속 송수되므로 펌프의 양정 손실을 극적으로 줄여줍니다. 단, 고열에 닿으면 변형되거나 녹아내리므로 화열로부터 보호받을 수 있는 천장 반자 내부(은폐 구역)에 숨기고 물이 항상 꽉 차서 내부 열을 흡수할 수 있는 습식 설비에 한정해 사용하도록 제한됩니다.
                    </span>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                <td style="padding: 14px; font-weight: 800; text-align: center; background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-primary);">시멘트관<br>(Cement)</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    콘크리트를 원심력으로 성형한 흄관 등. 내압력은 약함.
                </td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                    소화 배수용 대형 하수관거 및 대형 유수 유입부.<br>
                    <span style="color: var(--accent); display: block; margin-top: 6px; font-size: 0.82rem; line-height: 1.5;">
                        ※ 펌프의 강한 소화 고압력은 견디지 못해 유체 가압 송수에는 사용이 불가하지만, 자재비가 매우 저렴하고 외부 흙과 도로 위의 하중(트럭 통행 등)을 찌그러짐 없이 지탱하는 외부 압축강도가 뛰어나기 때문에 대량의 소화 배수를 하천으로 유도하는 대형 배수관로용으로 최적화되어 있습니다.
                    </span>
                </td>
            </tr>
        </tbody>
    </table>
    """
    
    # 4. Replace the old table with the new table
    comp_table.replace_with(BeautifulSoup(new_comp_table_html, "html.parser").table)
    print("Comparison table with reasons successfully replaced in DOM.")
    
    # 5. Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = update_comparison_reasons(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
