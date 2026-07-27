import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Tailored Traffic Control Engineering Standard Table (Replacing irrelevant utility pipe table)
traffic_control_std_table = """
    <!-- 동탄트램 공사장 교통처리대책 및 도로안전시설물 기술 시방 수칙 -->
    <h2>2. 동탄트램 공사장 교통처리대책 및 도로안전시설물 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🚦 화성동탄경찰서 및 도로공사장 교통관리지침 정량 기술 수칙</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">교통안전 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관할 협의 및 승인 기관</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 교통공학 기술 시방 및 설치 기준</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">경찰서 교통 심의</td>
                    <td style="text-align: center;">화성동탄경찰서 / 도로교통공단</td>
                    <td>• 착공 14일 전 우회도로 및 가변차선 교통처리계획서 심의 승인<br>• 국토교통부 '도로공사장 교통관리지침(2024.6)' 100% 준수<br>• 도로 점용 및 차로 차단 구간 승인 조건 이행 관리</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">차선 및 폭원 확보</td>
                    <td style="text-align: center;">화성시 도로관리과 / 공무팀</td>
                    <td>• 공사장 인접 최소 차선 폭 <strong>W ≥ 3.0m 이상</strong> 확보 (대형 버스/트럭 통행)<br>• 차로 테이퍼(Taper) 구간 길이 L ≥ 50m 설치로 완만 유도<br>• 출퇴근 시간대(07~09시, 17~19시) 가변 차로 능동 제어</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">방호 및 차폐 시설</td>
                    <td style="text-align: center;">현장 안전팀 / 시공사</td>
                    <td>• 차량 충돌 방지용 PE 방호벽 물 채움(충진율 100%) 시공<br>• 보행자 우회 안전 펜스(높이 H ≥ 1.8m) 및 비산먼지 차폐막 부착<br>• 공사장 출입구 차량 덮개 및 이동식 세륜기 가동</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">신호수 배치 수칙</td>
                    <td style="text-align: center;">현장 안전팀 / 신호수 전지대</td>
                    <td>• 공사장 전후방 <strong>50m, 100m 지점에 신호수 2인 이상</strong> 상시 배치<br>• 신호수 국가 공인 안전교육 이수자 및 경광봉/전자 신호기 휴대<br>• 덤프트럭 출입 시 도로 일시 정지 통제 및 우회 차선 유도</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">야간 시인성 조명</td>
                    <td style="text-align: center;">현장 전기팀 / 안전팀</td>
                    <td>• 야간 점멸 유도등(LED) 및 발광형 화살표 표지판 10m 간격 배치<br>• 갈매기 표지판 및 Solar 점멸등 밤샘 100% 정상 작동 점검<br>• 야간 시야 확보용 투광등(500W 이상) 공사장 출입구 조명 설치</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 동탄트램 도로 안전 제어 절대 수칙:</strong> 본 공사장은 주민 보행 안전과 차량 정체를 최소화하기 위해 <strong>경찰서 심의 승인 차선 폭(3.0m 이상)과 PE 방호벽 물 채움</strong>을 상시 점검합니다.
        </div>
    </div>
"""

print("Finding and updating Traffic Control activity folders with tailored Traffic Engineering table...")

traffic_folders = []

for root, dirs, files in os.walk(base_dir):
    folder = os.path.basename(root)
    if "교통" in folder or "10_교통" in folder or "18_교통" in folder:
        traffic_folders.append(root)

print(f"Found {len(traffic_folders)} traffic control directories: {traffic_folders}")

updated_count = 0

for t_dir in traffic_folders:
    for root, dirs, files in os.walk(t_dir):
        for f in files:
            if f.endswith('.html') and '표준서' in f:
                f_path = os.path.join(root, f)
                with open(f_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Replace section 2 with tailored Traffic Control Engineering table
                if "위수탁 지장물 5대 관종별" in content or "<h2>2." in content:
                    content = re.sub(r'<!-- 동탄트램 위수탁.*?</div>\s*</div>', traffic_control_std_table, content, flags=re.DOTALL)
                    content = re.sub(r'<h2>2\. 위수탁 지장물 5대 관종별.*?</div>\s*</div>', traffic_control_std_table, content, flags=re.DOTALL)
                    content = re.sub(r'<h2>2\..*?</h2>\s*<div style="background: #f8fafc;.*?</div>\s*</div>', traffic_control_std_table, content, flags=re.DOTALL)

                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                updated_count += 1
                print(f" ✅ Tailored Traffic Engineering Table updated: {f_path}")

print(f"\n🎉 Successfully updated {updated_count} Traffic Control Standard HTML files with Tailored Traffic Engineering Table!")
