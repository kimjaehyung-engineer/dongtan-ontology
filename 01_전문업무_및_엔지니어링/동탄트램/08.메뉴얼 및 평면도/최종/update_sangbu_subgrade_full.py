import openpyxl
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v4.xlsx"
base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반"

# 36 Master Activities for 상부강화노반
master_activities = [
    (1, "1_지반조사 상세검토", "지반조사 상세검토", "지반 물리탐사 및 시굴 결과를 바탕으로 노난 지반 지지력과 연약지반 분포 구간을 정밀 분석"),
    (2, "2_발주전략 KOM", "발주전략 KOM", "강화노반 시공사 및 자재 공급업체 간 공정/품질 이행 목표 공유 킥오프 미팅"),
    (3, "3_철도보호지구에서의 행위신고(필요시)", "철도보호지구에서의 행위신고(필요시)", "철도보호지구(인접 30m 이내) 굴착 및 토공사 진행을 위한 법적 행위 신고 및 국가철도공단 승인"),
    (4, "4_착수전 측량 Data 확인", "착수전 측량 Data 확인", "GRS80 세계측지계 기준 선로 중심선, 중심고 및 횡단 현형 측량 성과 재검증"),
    (5, "5_지장물이설 협의", "지장물이설 협의", "강화노반 다짐 구간 내 매설 지하 지장물 이격거리(H≥1.5m) 및 공정 간섭 최종 조정"),
    (6, "6_용지보상RISK 검토", "용지보상RISK 검토", "노반 시공 폭 및 임시 작업로 확보를 위한 용지 수용 경계 점검 및 미보상 부지 차단"),
    (7, "7_최고의 팀 만들기 지원", "최고의 팀 만들기 지원", "노반/토공 전문 엔지니어 및 다짐 장비 운전원 안전/품질 교육 및 최정예 팀 편성"),
    (8, "8_연약지반 처리공법 검토(필요시)", "연약지반 처리공법 검토(필요시)", "연약지반(N치 < 4) 구간 PVD, DCM, 성토재하 공법 적용성 및 허용 잔류침하량 검토"),
    (9, "9_토공 유동표 확인", "토공 유동표 확인", "절토량 및 성토량 수량 배분 Mass-Curve 검증으로 토공 유동 운반거리 단축 및 사토 계획 수립"),
    (10, "10_기공승낙 적정성 검토", "기공승낙 적정성 검토", "사유지 경계 부지 진입로 및 진입 진출로 토지소유자 기공승낙서 인감 및 범위 검속"),
    (11, "11_폐기물처리계획 수립", "폐기물처리계획 수립", "토공 굴착 중 발생하는 건설폐기물, 오염토양 분리수거 및 올바로시스템 신고 승인"),
    (12, "12_철도운행협의(필요시)", "철도운행협의(필요시)", "기존 철도 선로 인접 구역 차단작업 시간 확보 및 신호/전력 가선 방호 조치 협의"),
    (13, "13_작수전 Big Room 회의", "작수전 Big Room 회의", "노반, 궤도, 구조물, 위탁기관 간 3D BIM 간섭 검증 및 층다짐 밀도 일원화 빅룸 협의"),
    (14, "14_시공 계획 수립", "시공 계획 수립", "KCS 11 00 00 토공사 시방 기준에 따른 다짐 장비 조합, 층다짐 두께(30cm이하) 계획 수립"),
    (15, "15_사토장_토취장 선정 검토(필요시)", "사토장_토취장 선정 검토(필요시)", "강화노반용 적합 성토재(CBR≥10) 토취장 품질 시험 및 잔여토 사토장 반출 승인"),
    (16, "16_공사사전준비", "공사사전준비", "가설 사무소, 장비 세차장, 환경오염 방지시설(세륜기, 방진망) 설치 및 수직 측량 규준틀 준비"),
    (17, "17_임시배수시설", "임시배수시설", "강우 시 노반 유실 방지를 위한 가배수로, 집수정, 침사지 설치 (배수 구배 2.0% 이상)"),
    (18, "18_쌓기재료 검사", "쌓기재료 검사", "강화노반 재료의 쇄석/입도조정 골재 품질 시험 (최대입경 100mm 이하, 흙분 5% 이하)"),
    (19, "19_장비 검수 지원", "장비 검수 지원", "진동 롤러(10톤 이상), 타이어 롤러, 모터 그레이더 등 다짐 장비 정비 상태 및 안전 검사"),
    (20, "20_선로 종_횡단 및 용지경계측량", "선로 종_횡단 및 용지경계측량", "트램 선로 중심선 기준 10m 간격 종횡단 측량 및 계획고 허용 오차(±10mm) 기준선 관리"),
    (21, "21_규준틀 설치", "규준틀 설치", "성토 비탈면 경계 및 노반 완성면 표고를 표시하는 경사 규준틀 50m 간격 설치"),
    (22, "22_준비배수", "준비배수", "성토 바닥면 지하수위 저하 및 표면수 배출을 위한 암거, 맹암거 사전 배수 공조"),
    (23, "23_벌개제근_표토제거", "벌개제근_표토제거", "시공 구역 내 유기물 함유 표토(두께 15~30cm) 및 수목 뿌리 완벽 제거 반출"),
    (24, "24_구조물 및 지장물 제거", "구조물 및 지장물 제거", "노우 구조물, 기존 관로 및 콘크리트 전주 철거 후 소정의 재료로 되메우기 다짐"),
    (25, "25_진입로 조성", "진입로 조성", "덤프트럭 및 다짐 롤러 통행용 가설 진입 도로(폭 W≥6.0m, 골재敷 200mm) 설치"),
    (26, "26_노반쌓기", "노반쌓기", "KCS 11 20 00 토공 시방에 따른 1층 다짐 두께 30cm 이하 층다짐 시공 및 다짐도 95% 확보"),
    (27, "27_하부노반 시공", "하부노반 시공", "하부노반(두께 90cm) 입도 양호 골재 부설 및 변형계수 Ev2≥80MPa, Ev2/Ev1≤2.5 검속"),
    (28, "28_상부노반 시공", "상부노반 시공", "상부노반(두께 30cm) 다짐 및 변형계수 Ev2≥100MPa, 노반반력계수 K30≥90MN/m³ 확보"),
    (29, "29_강화노반 시공", "강화노반 시공", "트램 궤도 직하부 강화노반(두께 30cm) 쇄석혼합 골재 타설, K30≥110MN/m³, Ev2≥120MPa, Ev2/Ev1≤2.2 검속"),
    (30, "30_토공 유동운반_사토", "토공 유동운반_사토", "절토 잔여 흙 덤프트럭 사토장 운반 및 비산먼지 방지 덮개 개폐 이력 관리"),
    (31, "31_연약지반처리(필요시)", "연약지반처리(필요시)", "연약지반 구간 PVD 배수재 계측(간극수압, 침하판) 및 허용 잔류침하량 2.5cm 이하 확인"),
    (32, "32_절성토경계부 배수구조물(맹암거) 시공", "절성토경계부 배수구조물(맹암거) 시공", "절성토 편성 경계 부등침하 방지를 위한 맹암거(유압관 D200mm + 투수골재) 시공"),
    (33, "33_암석쌓기", "암석쌓기", "발파 암석 재료 쌓기 시 최대 입경 300mm 이하 제한 및 공극 채움 쇄석 부설 다짐"),
    (34, "34_방치기간 확보", "방치기간 확보", "성토 완료 후 부등침하 수렴을 위한 계획 방치 기간(3~6개월) 계측 관리 및 침하판 측정"),
    (35, "35_토공마무리", "토공마무리", "모터 그레이더를 이용한 횡단 구배 2.0% 정밀 정지 작업 및 종횡단 공차 ±10mm 검속"),
    (36, "36_토공 마무리면 인계", "토공 마무리면 인계", "후행 콘크리트 궤도 시공팀 및 감리단 입회 노반 인계인수서 서명 및 GIS 대장 이관")
]

def normalize(name):
    return name.replace(" ", "").replace("_", "").replace("/", "").replace("(", "").replace(")", "").replace("-", "").lower()

existing_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

print("Starting Deduplication and Renaming for 상부강화노반 Folders...")

# Step 1: Clean & Rename Folders
for num, target_folder_name, clean_title, desc in master_activities:
    norm_target = normalize(clean_title)
    
    matching_existing = []
    for f in existing_folders:
        f_norm = normalize(f)
        if norm_target in f_norm or f_norm in norm_target:
            matching_existing.append(f)
            
    if not matching_existing:
        target_path = os.path.join(base_dir, target_folder_name)
        os.makedirs(os.path.join(target_path, "표준서"), exist_ok=True)
        os.makedirs(os.path.join(target_path, "수행지침"), exist_ok=True)
        os.makedirs(os.path.join(target_path, "체크리스트"), exist_ok=True)
        print(f"  ✨ Created New Activity Folder: {target_folder_name}")
    else:
        primary = None
        for f in matching_existing:
            if f.startswith(f"{num}_"):
                primary = f
                break
        if not primary:
            primary = matching_existing[0]
            
        for f in matching_existing:
            if f != primary:
                dup_path = os.path.join(base_dir, f)
                shutil.rmtree(dup_path)
                print(f"  🗑️ Deleted Duplicate Folder: {f}")
                
        current_primary_path = os.path.join(base_dir, primary)
        target_path = os.path.join(base_dir, target_folder_name)
        if current_primary_path != target_path:
            os.rename(current_primary_path, target_path)
            print(f"  ✏️ Renamed Folder: {primary} -> {target_folder_name}")
        else:
            print(f"  ✅ Folder Name Maintained: {target_folder_name}")

print("\n🎉 Completed Sangbu Subgrade Folder Deduplication and 1~36 Renaming!")
