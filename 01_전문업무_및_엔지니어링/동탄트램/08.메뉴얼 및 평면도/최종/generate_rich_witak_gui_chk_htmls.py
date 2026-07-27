import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

def make_full_witak_guideline_html(folder_name, act_name, wbs):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - {act_name} 위수탁 5대 관종 수행지침</title>
    <style>
        body {{ font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 25px; background: #f8fafc; color: #0f172a; line-height: 1.6; }}
        .container {{ max-width: 950px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 3px solid #16a34a; padding-bottom: 18px; margin-bottom: 25px; }}
        .title {{ font-size: 1.9rem; font-weight: 900; color: #14532d; margin: 0; }}
        .meta-info {{ font-size: 0.9rem; color: #475569; margin-top: 8px; font-weight: 600; }}
        h2 {{ font-size: 1.35rem; font-weight: 800; color: #15803d; border-left: 5px solid #22c55e; padding-left: 12px; margin-top: 30px; margin-bottom: 18px; }}
        .card {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px; margin-bottom: 16px; }}
        .card-header {{ font-weight: 800; font-size: 1.05rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
        .bullet-list {{ margin: 0; padding-left: 20px; font-size: 0.9rem; color: #334155; }}
        .bullet-list li {{ margin-bottom: 6px; }}
        .footer-note {{ margin-top: 35px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 18px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">{act_name} 현장 수행지침 (Playbook)</h1>
        <div class="meta-info">Dongtan Tram WBS {wbs} | 위수탁 지장물 5대 관종 정밀 시공 지침</div>
    </div>

    <h2>📌 위수탁 지장물 5대 관종별 3단계 정밀 수행 지침</h2>

    <div class="card" style="border-left: 5px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">🔥 [도시가스관 - ㈜삼천리 / 한국가스공사]</div>
        <ul class="bullet-list">
            <li><strong>① 사전 준비:</strong> 가스 밸브 차단 후 배관 내 질소 퍼지(N₂ Purge)를 실시하여 잔류 산소 농도를 1.0% 이하로 제어합니다.</li>
            <li><strong>② 본 이설:</strong> 신규 가스관을 매설하고 궤도 최소 이격거리(H ≥ 1.5m)를 확보한 후 용접부 RT(방사선투과검사) 100% 1급을 획득합니다.</li>
            <li><strong>③ 검사 마감:</strong> 이중 피복 CP 전기방식 테이핑 시공 및 기밀시험을 통과한 후 가스 공급을 안정적으로 재개합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #0284c7;">
        <div class="card-header" style="color: #0284c7;">♨️ [지역난방관 - 한국지역난방공사 동탄지사]</div>
        <ul class="bullet-list">
            <li><strong>① 사전 준비:</strong> 열수송관 보온재 점검 및 누수 감지선 도통 시험을 실시하여 절연저항 100MΩ 이상을 확인합니다.</li>
            <li><strong>② 본 이설:</strong> 이중보온관 현장 융착 접합 및 용접부 NDT(비파괴검사) 100% 무결함을 검증합니다.</li>
            <li><strong>③ 검사 마감:</strong> 난방수 110℃ / 16bar 수압시험을 1시간 동안 유지하고 보호 샌드(Sand Bedding) 되메우기를 시행합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #166534;">
        <div class="card-header" style="color: #166534;">📶 [통신관로 및 광케이블 - KT / SKT / LGU+]</div>
        <ul class="bullet-list">
            <li><strong>① 사전 준비:</strong> 신규 통신 핸드홀 및 다공관 매설을 완료하고 심야 무중단 절체 스케줄을 수립합니다.</li>
            <li><strong>② 본 이설:</strong> 심야 시간대(01:00~05:00)를 이용하여 서비스 중단 없는 Cut-over 광케이블 접속 작업을 수행합니다.</li>
            <li><strong>③ 검사 마감:</strong> OTDR 광 접속 손실 측정(≤ 0.05dB 이내) 성과표를 획득하고 핸드홀 인입부를 방서/수밀 처리합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #1e3a8a;">
        <div class="card-header" style="color: #1e3a8a;">⚡ [특고압 전력관 - 한국전력공사 경기본부]</div>
        <ul class="bullet-list">
            <li><strong>① 사전 준비:</strong> 한전 감독관 입회 하 22.9kV 지중 전력관로 매설 심도(1.5m 이상) 인력 시굴 위치를 검증합니다.</li>
            <li><strong>② 본 이설:</strong> TR-CNCV 특고압 케이블 끌기(Pulling) 및 케이블 입선 작업을 시방 규정에 맞게 시행합니다.</li>
            <li><strong>③ 검사 마감:</strong> 절연저항(≥ 2,000MΩ), 내전압(60kV 10분), 전력 맨홀 접지저항(≤ 10Ω) 성적서를 교부받고 인수를 완료합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #0d9488;">
        <div class="card-header" style="color: #0d9488;">🏞️ [광역상수관 - 한국수자원공사 K-water]</div>
        <ul class="bullet-list">
            <li><strong>① 사전 준비:</strong> D800mm 이상 광역 관로 무단수 천공(Hot Tapping) 장비 세팅 및 수밀 링 장착을 완료합니다.</li>
            <li><strong>② 본 이설:</strong> 바이패스 관로 가설 후 이송 수압 15kg/cm² 이탈방지 조인트 및 곡관부 방호 콘크리트를 타설합니다.</li>
            <li><strong>③ 검사 마감:</strong> 24시간 연속 수압 유지 시험 및 수돗물 잔류염소 소독 수질 검사에 합격한 후 정식 통수합니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS {wbs} | 지장물이설
    </div>
</div>
</body>
</html>"""

def make_full_witak_checklist_html(folder_name, act_name, wbs):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - {act_name} 위수탁 5대 관종 체크리스트</title>
    <style>
        body {{ font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 25px; background: #f8fafc; color: #0f172a; line-height: 1.6; }}
        .container {{ max-width: 950px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 3px solid #0284c7; padding-bottom: 18px; margin-bottom: 25px; }}
        .title {{ font-size: 1.9rem; font-weight: 900; color: #0369a1; margin: 0; }}
        .meta-info {{ font-size: 0.9rem; color: #475569; margin-top: 8px; font-weight: 600; }}
        h2 {{ font-size: 1.35rem; font-weight: 800; color: #0284c7; border-left: 5px solid #38bdf8; padding-left: 12px; margin-top: 30px; margin-bottom: 18px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle; }}
        th {{ background: #f1f5f9; color: #1e293b; font-weight: 700; text-align: center; }}
        .footer-note {{ margin-top: 35px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 18px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">{act_name} 실시간 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS {wbs} | 위수탁 지장물 5대 관종 O/X 품질 검측표</div>
    </div>

    <h2>📋 위수탁 지장물 5대 관종 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 10%;">구분</th>
                <th style="width: 72%;">위수탁 지장물 핵심 공학 검측 항목 (정량 지수)</th>
                <th style="width: 18%;">검측 결과</th>
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

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS {wbs} | 지장물이설
    </div>
</div>
</body>
</html>"""

print(f"Generating rich Witak Guideline & Checklist HTMLs under '{base_dir}'...")

gui_count = 0
chk_count = 0

for root, dirs, files in os.walk(base_dir):
    folder_name = os.path.basename(root)
    match = re.match(r'^(\d+)_(.+)$', folder_name)
    act_num = match.group(1) if match else "1"
    act_name = match.group(2) if match else folder_name
    wbs = f"2000-1-{act_num}"

    for f in files:
        f_path = os.path.join(root, f)
        if f.endswith('.html'):
            if '수행지침' in f:
                new_html = make_full_witak_guideline_html(folder_name, act_name, wbs)
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(new_html)
                gui_count += 1
            elif '체크리스트' in f:
                new_html = make_full_witak_checklist_html(folder_name, act_name, wbs)
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(new_html)
                chk_count += 1

print(f"🎉 Fully upgraded {gui_count} Guideline HTML files & {chk_count} Checklist HTML files with pristine Witak 5-Pipeline standards!")
