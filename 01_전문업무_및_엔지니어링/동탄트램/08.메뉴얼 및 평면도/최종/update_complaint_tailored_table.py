import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Tailored Noise & Vibration Civil Complaint Standard Table
complaint_std_table = """
    <!-- 동탄트램 공사장 소음·진동 및 환경 민원 저감 정량 기술 시방 수칙 -->
    <h2>2. 동탄트램 공사장 소음·진동 및 환경 민원 저감 정량 기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🔇 주거지역 공사장 소음·진동 및 주민 민원 관리 정량 기술 시방</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">민원 관리 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 법령 및 규정</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 수칙 및 소음·진동 제어 기준</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">공사장 생활 소음</td>
                    <td style="text-align: center;">소음·진동관리법 시행규칙</td>
                    <td>• 주거지역 공사장 생활 소음 규제 기준 준수 (<strong>주간 ≤ 65dB, 야간 ≤ 50dB</strong>)<br>• 이동식 에어 방음벽(높이 H ≥ 3.0m) 설치 및 저소음 장비 사용</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">건축물 영향 진동</td>
                    <td style="text-align: center;">소음·진동관리법 / KCS 토공</td>
                    <td>• 인근 아파트 및 상가 건물 진동속도 <strong>v ≤ 0.2cm/sec (65dB(V))</strong> 이내 제어<br>• 굴착/파쇄 시 무진동 암파쇄 공법 적용 및 실시간 진동계 측량</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">비산먼지 및 차폐</td>
                    <td style="text-align: center;">대기환경보전법 제44조</td>
                    <td>• 공사장 경계 가설 휀스(높이 H ≥ 1.8m) 및 자동 살수포 100% 가동<br>• 토사 운반 덤프트럭 덮개 착용 및 차륜 자동 세륜기 운영</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">주민 사전 안내</td>
                    <td style="text-align: center;">화성시 환경과 / 공무팀</td>
                    <td>• 공사 착수 7일 전 인근 주민 설명회 및 안내 현수막 게시<br>• 야간 및 주말 공사 시 사전 서면 통지 및 동의서 획득</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">민원 핫라인 운영</td>
                    <td style="text-align: center;">현장 전담 민원 수습팀</td>
                    <td>• 24시간 민원 접수 전담 핫라인(Hot-line) 및 민원 수림 대장 작성<br>• 민원 발생 시 <strong>2시간 이내 현장 출동</strong> 및 당일 처리 결과 통보</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 동탄트램 민원 저감 절대 수칙:</strong> 본 과업은 주민 생활 환경 보호를 위해 <strong>소음 규제(주간 65dB 이내), 진동 제어(0.2cm/sec 이내) 및 24시간 핫라인</strong>을 상시 가동합니다.
        </div>
    </div>
"""

print("Finding Civil Complaint activity folders and updating with Noise & Vibration Standard Table...")

complaint_folders = []

for root, dirs, files in os.walk(base_dir):
    folder = os.path.basename(root)
    if "민원" in folder:
        complaint_folders.append(root)

print(f"Found {len(complaint_folders)} complaint directories: {complaint_folders}")

updated_count = 0

for c_dir in complaint_folders:
    for root, dirs, files in os.walk(c_dir):
        for f in files:
            if f.endswith('.html') and '표준서' in f:
                f_path = os.path.join(root, f)
                with open(f_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Replace Section 1 and Section 2
                content = re.sub(r'<tr>\s*<th style="width: 20%;">과업 목적</th>.*?</tr>', 
                                 '<tr><th style="width: 20%;">과업 목적</th><td>동탄트램 지장물이설 시 발생하는 소음, 진동, 비산먼지 및 교통 통제 민원 저감 대책 수립 및 주민 소통 관리</td></tr>', content, flags=re.DOTALL)
                content = re.sub(r'<tr>\s*<th>수행 방법</th>.*?</tr>', 
                                 '<tr><th>수행 방법</th><td>이동식 에어 방음벽 설치, 저소음·저진동 공법 적용, 실시간 계측 및 24시간 민원 핫라인 전담 운영</td></tr>', content, flags=re.DOTALL)
                content = re.sub(r'<tr>\s*<th>주요 산출물</th>.*?</tr>', 
                                 '<tr><th>주요 산출물</th><td>민원 저감 대책 수립 보고서, 소음·진동 실시간 계측 성과표, 민원 처리 관리 대장</td></tr>', content, flags=re.DOTALL)
                content = re.sub(r'<tr>\s*<th>관련 법령/기준</th>.*?</tr>', 
                                 '<tr><th>관련 법령/기준</th><td>소음·진동관리법, 대기환경보전법, 화성시 환경보전 조례</td></tr>', content, flags=re.DOTALL)

                # Replace section 2 with tailored Noise & Vibration Table
                content = re.sub(r'<h2>2\..*?</h2>\s*<div style="background: #f8fafc;.*?</div>\s*</div>', complaint_std_table, content, flags=re.DOTALL)

                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                updated_count += 1
                print(f" ✅ Tailored Noise & Vibration Table updated: {f_path}")

print(f"\n🎉 Successfully updated {updated_count} Civil Complaint Standard HTML files with Noise & Vibration Table!")
