import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Refined Witak Utility Technical Standards Section WITHOUT Settlement/PS talk
witak_engineering_only_section = """
    <!-- 화성시 및 5대 위탁 관리기관 위수탁 지장물 이설 정량 공학 기술 시방 기준 -->
    <h2>2. 위수탁 지장물 5대 관종별 정량적 공학 및 품질 검속 기준</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🏛️ 동탄트램 위수탁 지장물 5대 관종별 품질 검속 및 공학 시방 수칙</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">위수탁 관종</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">전담 관리기관</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 공학 시험 및 품질 검속 기준</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">도시가스관</td>
                    <td style="text-align: center;">㈜삼천리 / 한국가스공사</td>
                    <td>• 용접부 RT(방사선투과검사) 100% 1급 판정<br>• 가스 차단 후 N₂ 질소 퍼지(잔류산소 ≤ 1.0%)<br>• 이중 피복 전기방식(CP) 테이핑 및 수밀 시공</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">지역난방관</td>
                    <td style="text-align: center;">한국지역난방공사 동탄지사</td>
                    <td>• 이중보온관 NDT(비파괴검사) 100% 무결함<br>• 누수 감지선 도통 및 절연저항 ≥ 100MΩ<br>• 난방수 110℃ / 16bar 수압시험 통과</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">통신관로/케이블</td>
                    <td style="text-align: center;">KT / SKT / LGU+</td>
                    <td>• 광 접속 손실 OTDR ≤ 0.05dB 이내<br>• 심야 시간대(01:00~05:00) 무중단 Cut-over<br>• 핸드홀 인입 부위 수밀 및 방서(防鼠) 처리</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">특고압 전력관</td>
                    <td style="text-align: center;">한국전력공사 경기본부</td>
                    <td>• 22.9kV TR-CNCV 특고압 지중 관로 매설<br>• 절연저항 ≥ 2,000MΩ 및 내전압 60kV 10분 시험<br>• 전력 맨홀 접지저항 ≤ 10Ω 유지</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">광역상수관</td>
                    <td style="text-align: center;">한국수자원공사 (K-water)</td>
                    <td>• D800mm 이상 광역 관로 무단수 Tapping 차단<br>• 이송 수압 15kg/cm² 견딤 이탈방지 조인트 시공<br>• 통수 전 24시간 수압 유지 및 수돗물 염소 소독</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 트램 궤도 간섭 제어 절대 기준:</strong> 모든 위수탁 지장물은 동탄트램 궤도 구조물 및 하부 강화노반과의 <strong>수평/수직 최소 이격거리 H ≥ 1.5m 이상</strong>을 엄격히 확보하여 시공합니다.
        </div>
    </div>
"""

print(f"Purging all '사후정산/PS' references from HTML files under '{base_dir}'...")

purged_settlement_count = 0

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and '표준서' in f:
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig = content

            # Replace section 2 with engineering-only table (No settlement/PS column)
            if "위수탁 지장물 5대 관종별" in content:
                content = re.sub(r'<!-- 화성시 및 5대 위탁.*?</div>\s*</div>', witak_engineering_only_section, content, flags=re.DOTALL)
                content = re.sub(r'<h2>2\. 위수탁 지장물 5대 관종별.*?</div>\s*</div>', witak_engineering_only_section, content, flags=re.DOTALL)

            if content != orig:
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                purged_settlement_count += 1

print(f"🎉 Successfully purged settlement/PS references from {purged_settlement_count} Standard HTML files!")
