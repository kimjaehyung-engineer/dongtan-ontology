import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# 1. Target 5: 지장물 조사 (위탁기관 합동)
dir_joint_survey = os.path.join(base_dir, "5_지장물 조사 (위탁기관 합동)")
# 2. Target 5: 착수전 Big Room 회의
dir_bigroom = os.path.join(base_dir, "5_착수전 Big Room 회의")
# 3. Target 6: 관리기관(맑은물사업소) 협의
dir_malkeunmul = os.path.join(base_dir, "6_관리기관(맑은물사업소) 협의")

print("Performing precise target overwrite for 3 activities...")

def write_html(target_dir, file_type, content):
    sub_dir = os.path.join(target_dir, file_type)
    if os.path.exists(sub_dir):
        for f in os.listdir(sub_dir):
            if f.endswith('.html'):
                f_path = os.path.join(sub_dir, f)
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"  ✅ Written {file_type}: {f_path}")

# Overwrite Act 1: Joint Survey
if os.path.exists(dir_joint_survey):
    print("\nUpdating '5_지장물 조사 (위탁기관 합동)'...")
    write_html(dir_joint_survey, "표준서", act_joint_survey_std)
    write_html(dir_joint_survey, "수행지침", act_joint_survey_gui)
    write_html(dir_joint_survey, "체크리스트", act_joint_survey_chk)

# Overwrite Act 2: Big Room
if os.path.exists(dir_bigroom):
    print("\nUpdating '5_착수전 Big Room 회의'...")
    write_html(dir_bigroom, "표준서", act_bigroom_std)
    write_html(dir_bigroom, "수행지침", act_bigroom_gui)
    write_html(dir_bigroom, "체크리스트", act_bigroom_chk)

# Overwrite Act 3: Malkeunmul
if os.path.exists(dir_malkeunmul):
    print("\nUpdating '6_관리기관(맑은물사업소) 협의'...")
    write_html(dir_malkeunmul, "표준서", act_malkeunmul_std)
    write_html(dir_malkeunmul, "수행지침", act_malkeunmul_gui)
    write_html(dir_malkeunmul, "체크리스트", act_malkeunmul_chk)

print("\n🎉 Precise overwrite complete for all 3 target activities!")
