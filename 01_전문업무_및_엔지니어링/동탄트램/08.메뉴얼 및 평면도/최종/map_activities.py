import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# 39 Standard Activity Names in Exact Order (1 to 39)
standard_activities = [
    "Site Survey Risk 검토",
    "발주전략 KOM (도급지분)",
    "지장물 이설 요청 (위수탁고)",
    "도급자분 이설업체 선정(상_하수)",
    "지장물 조사 (위탁기관 합동)",
    "지장물 이설 계획 수립",
    "최고의 팀 만들기 지원",
    "착수전 Big Room 회의",
    "인허가 절차 진행",
    "교통처리대책 협의 및 승인",
    "민원 저감 대책 수립",
    "용지보상 Risk 파악",
    "관리기관(맑은물사업소) 협의",
    "위수탁 지장물 이설 설계",
    "상하수도 이설계획 실정보고",
    "위수탁 계약 체결",
    "도로점용_굴착행위 인허가",
    "교통통제 및 교통안전시설 설치",
    "줄따기(GPR)를 통한 기존 지장물 매설 확인",
    "이설 위치 토공 굴착",
    "신규관로 매설 및 설치",
    "무단수 연결을 위한 시설 설치",
    "신규관로 및 연결관로 접속",
    "기존관로 철거 및 원상복구",
    "광역상수관 이설 공사",
    "상수도 관로 이설 공사",
    "하수도 관로 이설 공사",
    "도시가스관 이설 공사",
    "지역난방관 이설 공사",
    "통신관로 및 케이블 이설 공사",
    "특고압 전력관로 이설 공사",
    "송유관 이설 공사",
    "상하수도 이설 시공 최종 점검",
    "위수탁 지하지장물 이설 최종 점검",
    "상하수도 이설 정산 금액 검토",
    "위수탁 처리 정산금액 지급",
    "도급자분_위수탁분 설계변경 정산",
    "공사전 선행공종에서 인수받을 사항",
    "공사중 챙겨야할 후행공종의 요구사항"
]

# Helper to normalize activity name matching
def normalize(name):
    return name.replace(" ", "").replace("_", "").replace("/", "").replace("(", "").replace(")", "").replace("-", "").lower()

# Map existing folders to target standard activities
existing_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

# Group existing folders by standard index (0 to 38)
grouped = {i: [] for i in range(len(standard_activities))}

for folder in existing_folders:
    # strip existing leading number if any
    name_part = folder
    if "_" in folder:
        parts = folder.split("_", 1)
        if parts[0].isdigit():
            name_part = parts[1]
    
    norm_folder = normalize(name_part)
    
    matched_idx = None
    for idx, std_name in enumerate(standard_activities):
        norm_std = normalize(std_name)
        if norm_folder == norm_std or norm_std in norm_folder or norm_folder in norm_std:
            matched_idx = idx
            break
    
    if matched_idx is not None:
        grouped[matched_idx].append(folder)
    else:
        print(f"⚠️ Unmatched Folder: {folder}")

print("\n=== Grouped Activity Folders Status ===")
for idx, std_name in enumerate(standard_activities, 1):
    folders = grouped[idx - 1]
    print(f"{idx:02d}. [{std_name}] -> {len(folders)} folders: {folders}")

# Execute Deduplication and Renaming Script Creation
