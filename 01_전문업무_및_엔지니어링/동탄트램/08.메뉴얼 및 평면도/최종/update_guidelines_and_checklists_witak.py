import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Refined Witak Utility Guideline Section
witak_guideline_section = """
    <!-- 화성시 및 5대 위탁 관리기관 위수탁 지장물 이설 3단계 수행지침 -->
    <h2>2. 위수탁 지장물 5대 관종별 3단계 수행지침 (Playbook)</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 14px 0; color: #1e3a8a; font-size: 1.05rem;">📘 위수탁 지장물 이설 공종별 3단계 정밀 시공 절차</h4>
        
        <div style="margin-bottom: 16px; background: #ffffff; padding: 14px; border-radius: 8px; border-left: 4px solid #ea580c;">
            <strong style="color: #ea580c;">🔥 [도시가스관 - ㈜삼천리 / 가스공사]</strong>
            <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li><strong>① 사전준비:</strong> 가스 밸브 차단 후 배관 내 질소 퍼지(N₂ Purge) 시행 (잔류 산소 농도 ≤ 1.0% 확인)</li>
                <li><strong>② 본 이설:</strong> 신규 배관 매설, 궤도 최소 이격거리(H ≥ 1.5m) 확보, 용접부 RT(방사선) 100% 1급 통과</li>
                <li><strong>③ 검사마감:</strong> 이중 피복 전기방식(CP) 테이핑 시공 및 기밀시험 통과 후 가스 공급 재개</li>
            </ul>
        </div>

        <div style="margin-bottom: 16px; background: #ffffff; padding: 14px; border-radius: 8px; border-left: 4px solid #0284c7;">
            <strong style="color: #0284c7;">♨️ [지역난방관 - 한국지역난방공사 동탄지사]</strong>
            <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li><strong>① 사전준비:</strong> 열수송관 보온재 상태 점검 및 누수 감지선 도통 시험 (절연저항 ≥ 100MΩ)</li>
                <li><strong>② 본 이설:</strong> 이중보온관 현장 융착 접합 및 용접부 NDT(비파괴검사) 100% 무결함 검증</li>
                <li><strong>③ 검사마감:</strong> 난방수 110℃ / 16bar 수압시험 1시간 유지 및 보호 샌드(Sand) 되메우기</li>
            </ul>
        </div>

        <div style="margin-bottom: 16px; background: #ffffff; padding: 14px; border-radius: 8px; border-left: 4px solid #166534;">
            <strong style="color: #166534;">📶 [통신관로 및 광케이블 - KT / SKT / LGU+]</strong>
            <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li><strong>① 사전준비:</strong> 신규 통신 핸드홀 및 다공관 매설 완료, 광케이블 절체 스케줄 수립</li>
                <li><strong>② 본 이설:</strong> 심야 시간대(01:00~05:00) 이용 무중단 Cut-over 광케이블 접속 작업 시행</li>
                <li><strong>③ 검사마감:</strong> OTDR 광 접속 손실 측정(≤ 0.05dB 통과) 및 핸드홀 인입부 방서/수밀 시공</li>
            </ul>
        </div>

        <div style="margin-bottom: 16px; background: #ffffff; padding: 14px; border-radius: 8px; border-left: 4px solid #1e3a8a;">
            <strong style="color: #1e3a8a;">⚡ [특고압 전력관 - 한국전력공사 경기본부]</strong>
            <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li><strong>① 사전준비:</strong> 한전 감독관 입회 하 22.9kV 지중 전력관로 매설 심도(1.5m 이상) 인력 시굴 검증</li>
                <li><strong>② 본 이설:</strong> TR-CNCV 특고압 케이블 끌기(Pulling) 및 케이블 입선 작업 시행</li>
                <li><strong>③ 검사마감:</strong> 절연저항(≥ 2,000MΩ), 내전압(60kV 10분), 전력 맨홀 접지저항(≤ 10Ω) 시험 성적서 교부</li>
            </ul>
        </div>

        <div style="background: #ffffff; padding: 14px; border-radius: 8px; border-left: 4px solid #0d9488;">
            <strong style="color: #0d9488;">🏞️ [광역상수관 - 한국수자원공사 K-water]</strong>
            <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 0.88rem; color: #334155;">
                <li><strong>① 사전준비:</strong> D800mm 이상 광역 관로 무단수 천공(Hot Tapping) 장비 세팅 및 수밀 링 장착</li>
                <li><strong>② 본 이설:</strong> 바이패스 관로 가설 후 이송 수압 15kg/cm² 이탈방지 조인트 및 곡관부 방호 콘크리트 타설</li>
                <li><strong>③ 검사마감:</strong> 24시간 연속 수압 유지 시험 및 탁도/잔류염소 소독 수질 검사 합격 후 통수</li>
            </ul>
        </div>
    </div>
"""

# Refined Witak Utility Checklist Section
witak_checklist_section = """
    <!-- 화성시 및 5대 위탁 관리기관 위수탁 지장물 이설 9대 검측 체크리스트 -->
    <h2>2. 위수탁 지장물 5대 관종별 9대 실시간 O/X 검측 체크리스트</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 14px 0; color: #1e3a8a; font-size: 1.05rem;">📋 위수탁 지장물 현장 검측 O/X 박스 항목</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 10%;">구분</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 72%;">위수탁 지장물 핵심 공학 검측 항목 (정량 지수)</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 18%;">검측 결과</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align: center; font-weight: bold;">공통</td>
                    <td>1. 모든 위수탁 지장관과 트램 궤도 구조물 간 수평/수직 최소 이격거리(H ≥ 1.5m)를 확보했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">가스</td>
                    <td>2. 도시가스관 차단 후 N₂ 질소 퍼지를 실시하여 잔류 산소 농도 ≤ 1.0% 이하를 확인했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">가스</td>
                    <td>3. 가스관 용접부에 대해 RT(방사선투과검사) 100% 1급 판정 및 CP 전기방식 피복을 완료했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">난방</td>
                    <td>4. 지역난방 이중보온관 용접부 NDT 100% 무결함 및 누수 감지선 절연저항(≥ 100MΩ)을 검측했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">난방</td>
                    <td>5. 난방수 110℃ / 16bar 수압시험을 1시간 동안 유지하여 Zero 누수를 확인했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">통신</td>
                    <td>6. 통신 광케이블 심야 절체(01~05시) 후 OTDR 광 접속 손실 측정값(≤ 0.05dB 이내)을 검측했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">전력</td>
                    <td>7. 한전 22.9kV 특고압 지중관 절연저항(≥ 2,000MΩ) 및 내전압 시험(60kV 10분)을 승인받았는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">전력</td>
                    <td>8. 전력 맨홀 접지저항(≤ 10Ω 이하) 측정 및 한전 감독관 현장 입회 서명을 확인했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">광역</td>
                    <td>9. K-water 광역상수관(D800mm 이상) 무단수 천공 및 수압 15kg/cm² 이탈방지 조인트 시공을 완료했는가?</td>
                    <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
                </tr>
            </tbody>
        </table>
    </div>
"""

print(f"Updating Guideline & Checklist HTML files under '{base_dir}' with Witak 5-Pipeline Standards...")

updated_gui_count = 0
updated_chk_count = 0

for root, dirs, files in os.walk(base_dir):
    for f in files:
        f_path = os.path.join(root, f)
        if f.endswith('.html'):
            if '수행지침' in f:
                with open(f_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if "위수탁 지장물 5대 관종별 3단계 수행지침" not in content:
                    if "<h2>2." in content:
                        content = re.sub(r'<h2>2\..*?</h2>', witak_guideline_section, content, count=1, flags=re.DOTALL)
                    else:
                        content = content.replace("<h2>3.", witak_guideline_section + "\n    <h2>3.")

                    with open(f_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    updated_gui_count += 1

            elif '체크리스트' in f:
                with open(f_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if "위수탁 지장물 5대 관종별 9대 실시간" not in content:
                    if "<h2>2." in content:
                        content = re.sub(r'<h2>2\..*?</h2>', witak_checklist_section, content, count=1, flags=re.DOTALL)
                    else:
                        content = content.replace("<h2>3.", witak_checklist_section + "\n    <h2>3.")

                    with open(f_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    updated_chk_count += 1

print(f"🎉 Successfully updated {updated_gui_count} Guideline HTML files & {updated_chk_count} Checklist HTML files!")
