import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Exact 39 Master Activity Names with Official Numbers (1 to 39)
master_activities = [
    (1, "1_Site Survey Risk 검토", "Site Survey Risk 검토"),
    (2, "2_발주전략 KOM (도급지분)", "발주전략 KOM (도급지분)"),
    (3, "3_지장물 이설 요청 (위수탁고)", "지장물 이설 요청 (위수탁고)"),
    (4, "4_도급자분 이설업체 선정(상_하수)", "도급자분 이설업체 선정(상_하수)"),
    (5, "5_지장물 조사 (위탁기관 합동)", "지장물 조사 (위탁기관 합동)"),
    (6, "6_지장물 이설 계획 수립", "지장물 이설 계획 수립"),
    (7, "7_최고의 팀 만들기 지원", "최고의 팀 만들기 지원"),
    (8, "8_착수전 Big Room 회의", "착수전 Big Room 회의"),
    (9, "9_인허가 절차 진행", "인허가 절차 진행"),
    (10, "10_교통처리대책 협의 및 승인", "교통처리대책 협의 및 승인"),
    (11, "11_민원 저감 대책 수립", "민원 저감 대책 수립"),
    (12, "12_용지보상 Risk 파악", "용지보상 Risk 파악"),
    (13, "13_관리기관(맑은물사업소) 협의", "관리기관(맑은물사업소) 협의"),
    (14, "14_위수탁 지장물 이설 설계", "위수탁 지장물 이설 설계"),
    (15, "15_상하수도 이설계획 실정보고", "상하수도 이설계획 실정보고"),
    (16, "16_위수탁 계약 체결", "위수탁 계약 체결"),
    (17, "17_도로점용_굴착행위 인허가", "도로점용_굴착행위 인허가"),
    (18, "18_교통통제 및 교통안전시설 설치", "교통통제 및 교통안전시설 설치"),
    (19, "19_줄따기(GPR)를 통한 기존 지장물 매설 확인", "줄따기(GPR)를 통한 기존 지장물 매설 확인"),
    (20, "20_이설 위치 토공 굴착", "이설 위치 토공 굴착"),
    (21, "21_신규관로 매설 및 설치", "신규관로 매설 및 설치"),
    (22, "22_무단수 연결을 위한 시설 설치", "무단수 연결을 위한 시설 설치"),
    (23, "23_신규관로 및 연결관로 접속", "신규관로 및 연결관로 접속"),
    (24, "24_기존관로 철거 및 원상복구", "기존관로 철거 및 원상복구"),
    (25, "25_광역상수관 이설 공사", "광역상수관 이설 공사"),
    (26, "26_상수도 관로 이설 공사", "상수도 관로 이설 공사"),
    (27, "27_하수도 관로 이설 공사", "하수도 관로 이설 공사"),
    (28, "28_도시가스관 이설 공사", "도시가스관 이설 공사"),
    (29, "29_지역난방관 이설 공사", "지역난방관 이설 공사"),
    (30, "30_통신관로 및 케이블 이설 공사", "통신관로 및 케이블 이설 공사"),
    (31, "31_특고압 전력관로 이설 공사", "특고압 전력관로 이설 공사"),
    (32, "32_송유관 이설 공사", "송유관 이설 공사"),
    (33, "33_상하수도 이설 시공 최종 점검", "상하수도 이설 시공 최종 점검"),
    (34, "34_위수탁 지하지장물 이설 최종 점검", "위수탁 지하지장물 이설 최종 점검"),
    (35, "35_상하수도 이설 정산 금액 검토", "상하수도 이설 정산 금액 검토"),
    (36, "36_위수탁 처리 정산금액 지급", "위수탁 처리 정산금액 지급"),
    (37, "37_도급자분_위수탁분 설계변경 정산", "도급자분_위수탁분 설계변경 정산"),
    (38, "38_공사전 선행공종에서 인수받을 사항", "공사전 선행공종에서 인수받을 사항"),
    (39, "39_공사중 챙겨야할 후행공종의 요구사항", "공사중 챙겨야할 후행공종의 요구사항")
]

# Helper to normalize activity name matching
def normalize(name):
    return name.replace(" ", "").replace("_", "").replace("/", "").replace("(", "").replace(")", "").replace("-", "").lower()

existing_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

print("Starting Deduplication and Renaming Process...")

for num, target_folder_name, clean_title in master_activities:
    norm_target = normalize(clean_title)
    
    matching_existing = []
    for f in existing_folders:
        f_norm = normalize(f)
        if norm_target in f_norm or f_norm in norm_target:
            matching_existing.append(f)
    
    if not matching_existing:
        # Create missing activity directory (e.g., 6_지장물 이설 계획 수립)
        target_path = os.path.join(base_dir, target_folder_name)
        os.makedirs(os.path.join(target_path, "표준서"), exist_ok=True)
        os.makedirs(os.path.join(target_path, "수행지침"), exist_ok=True)
        os.makedirs(os.path.join(target_path, "체크리스트"), exist_ok=True)
        print(f"  ✨ Created New Missing Activity Folder: {target_folder_name}")
    else:
        # Select the folder with the target number prefix if available, otherwise pick the first
        primary = None
        for f in matching_existing:
            if f.startswith(f"{num}_"):
                primary = f
                break
        if not primary:
            primary = matching_existing[0]
        
        # Delete duplicates (folders in matching_existing other than primary)
        for f in matching_existing:
            if f != primary:
                dup_path = os.path.join(base_dir, f)
                shutil.rmtree(dup_path)
                print(f"  🗑️ Deleted Duplicate Folder: {f}")
        
        # Rename primary folder if its name is not exact target_folder_name
        current_primary_path = os.path.join(base_dir, primary)
        target_path = os.path.join(base_dir, target_folder_name)
        if current_primary_path != target_path:
            os.rename(current_primary_path, target_path)
            print(f"  ✏️ Renamed Folder: {primary} -> {target_folder_name}")
        else:
            print(f"  ✅ Correct Folder Name Maintained: {target_folder_name}")

    # Now inside target_path, check and rename HTML files in 표준서, 수행지침, 체크리스트
    for doc_type in ["표준서", "수행지침", "체크리스트"]:
        sub_dir = os.path.join(target_path, doc_type)
        if os.path.exists(sub_dir):
            for html_file in os.listdir(sub_dir):
                if html_file.endswith(".html"):
                    # Standardize HTML filename: {target_folder_name}_{doc_type}.html
                    expected_filename = f"{target_folder_name}_{doc_type}.html"
                    curr_html_path = os.path.join(sub_dir, html_file)
                    exp_html_path = os.path.join(sub_dir, expected_filename)
                    if curr_html_path != exp_html_path:
                        if os.path.exists(exp_html_path):
                            os.remove(curr_html_path)
                        else:
                            os.rename(curr_html_path, exp_html_path)
                        print(f"    📄 Standardized HTML file: {html_file} -> {expected_filename}")

print("\n🎉 Complete Deduplication, Serial Numbering, and HTML Filename Alignment Finished!")
