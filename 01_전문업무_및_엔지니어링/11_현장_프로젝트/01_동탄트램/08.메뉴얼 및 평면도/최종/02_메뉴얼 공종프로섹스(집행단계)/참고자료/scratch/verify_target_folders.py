import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

target_folders = [
    '2_발주전략 KOM',
    '3_철도보호지구에서의 행위신고(필요시)',
    '4_착수전 측량 Data 확인',
    '5_지장물이설 협의',
    '6_용지보상RISK 검토',
    '7_최고의 팀 만들기 지원',
    '8_시공계획서 수립 승인',
    '8_작업조 편성',
    '9_장비 수급 계획',
    '10_노반 재료 입도 DB 확보',
    '11_사토장 _ 토사 수급 계획 확인',
    '12_배수 처리 계획 수립',
    '13_안전관리계획 수립 승인',
    '14_품질관리계획 수립 승인',
    '15_환경관리계획 수립 승인',
    '16_교통소통 대책 수립 승인(필요시)',
    '17_하도급 검토 승인',
    '18_자재승인',
    '19_시험다짐',
    '20_원지반 검측',
    '21_하부노반 검측',
    '22_상부노반 시공(배수 유공관 포함)',
    '23_상부강화노반 시공',
    '24_다짐 검측',
    '25_평판재하시험',
    '26_강성 검측(K30, EV2)',
    '27_평탄성 검측',
    '28_노반 종 횡단 검측',
    '29_부적합 사항 조치',
    '30_사면 다짐 검측',
    '31_배수시설 시공 검측',
    '32_완성면 보호',
    '33_공사일지 작성',
    '35_검측 및 승인 관리',
    '36_토공 마무리면 인계'
]

print(f"Target Folders Count: {len(target_folders)}")

all_ok = True
count_summary = 0

for tf in target_folders:
    full_path = os.path.join(base_root, tf)
    if not os.path.exists(full_path):
        print(f"[MISSING FOLDER] {tf}")
        all_ok = False
        continue
    
    std_p = os.path.join(full_path, '표준서')
    gui_p = os.path.join(full_path, '수행지침')
    chk_p = os.path.join(full_path, '체크리스트')
    
    std_files = [f for f in os.listdir(std_p) if f.endswith('.html')] if os.path.exists(std_p) else []
    gui_files = [f for f in os.listdir(gui_p) if f.endswith('.html')] if os.path.exists(gui_p) else []
    chk_files = [f for f in os.listdir(chk_p) if f.endswith('.html')] if os.path.exists(chk_p) else []
    
    total = len(std_files) + len(gui_files) + len(chk_files)
    count_summary += total
    
    if len(std_files) >= 1 and len(gui_files) >= 1 and len(chk_files) >= 1:
        print(f"[OK] {tf} : Total {total} files (Std:{len(std_files)}, Gui:{len(gui_files)}, Chk:{len(chk_files)})")
    else:
        print(f"[FAIL] {tf} : Std:{len(std_files)}, Gui:{len(gui_files)}, Chk:{len(chk_files)}")
        all_ok = False

print(f"\nFinal Result: Total {count_summary} Deep Build HTML files verified across {len(target_folders)} target folders!")
