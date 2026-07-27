import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

def convert_checklist_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace common passive endings with ~하였는가?
    replacements = [
        ("확인 여부", "확인하였는가?"),
        ("검측 여부", "검측하였는가?"),
        ("측정 여부", "측정하였는가?"),
        ("보정 여부", "보정하였는가?"),
        ("설치 여부", "설치하였는가?"),
        ("도포 여부", "도포하였는가?"),
        ("체결 여부", "체결하였는가?"),
        ("제거 여부", "제거하였는가?"),
        ("전단 여부", "전단하였는가?"),
        ("실시 여부", "실시하였는가?"),
        ("확인", "확인하였는가?"),
    ]
    
    # We do careful string replacements or targeted regex for rows
    import re
    # Match patterns inside <td> lines that end with '여부' or '확인' before closing tag or line end
    # Example: <strong>[직전 측량]</strong> 타설 직전 스핀들 궤간/캔트 레벨 정밀 상태 측량 여부
    content_new = re.sub(r'([가-힣a-zA-C0-9%\.\+\-\(\)±\s]+?)(?:여부|확인)(?=\s*<\/div>|\s*<\/td>|\s*<)', r'\1하였는가?', content)
    # Fix double '하였는가?' if any
    content_new = content_new.replace("하였는가?하였는가?", "하였는가?")
    content_new = content_new.replace("확인하였는가?하였는가?", "확인하였는가?")
    
    if content != content_new:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_new)
        print(f"✅ Updated Checklist phrasing to '~하였는가?': {filepath}")

# Target WBS folders (17, 18, 19, 20)
for item in os.listdir(base_dir):
    folder = os.path.join(base_dir, item)
    if os.path.isdir(folder) and ('17' in item or '18' in item or '19' in item or '20' in item):
        chk_dir = os.path.join(folder, "체크리스트")
        if os.path.exists(chk_dir):
            for fname in os.listdir(chk_dir):
                if fname.endswith(".html"):
                    convert_checklist_file(os.path.join(chk_dir, fname))

print("\n🎉 COMPLETED UPDATING ALL CHECKLISTS TO END WITH '~하였는가?'!")
