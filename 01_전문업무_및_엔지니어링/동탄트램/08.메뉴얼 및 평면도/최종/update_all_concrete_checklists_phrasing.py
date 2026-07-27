import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

modified_count = 0
skipped_count = 0

def process_checklist_html(filepath):
    global modified_count
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. <td> 또는 <div> 내의 문장 끝 어미 정형화
    # 패턴 예시:
    # <strong>[... ]</strong> 문장... 확인 / 여부 / 측정 / 검측 등
    
    # 먼저 공통적인 명사형/피동형 어미 치환
    # '확인 여부', '검측 여부', '측정 여부', '시험 여부', '설치 여부', '도포 여부', '체결 여부', '제거 여부', '연마 여부' -> ~하였는가?
    content = re.sub(r'([가-힣a-zA-Z0-9%\.\+\-\(\)±\s]+?)(?:여부|확인)(?=\s*<\/div>|\s*<\/td>|\s*<br\s*\/?>|\s*<)', r'\1하였는가?', content)
    
    # 2. 문장 끝이 '확인', '검측', '측정', '포설', '도포', '설치', '체결', '연마', '제거', '작성', '시험' 등으로 끝난 경우
    # <td>나 <div> 바로 앞에서 처리
    target_verbs = ['측량', '검측', '측정', '포설', '도포', '설치', '체결', '연마', '제거', '작성', '시험', '조율', '보정', '서냉', '전단', '구축', '확보', '유지', '제출', '결재']
    
    for verb in target_verbs:
        # e.g., '측량' -> '측량하였는가?' (단, 이미 '하였는가?'가 붙은 것은 예외)
        pattern = re.compile(rf'({verb})(?!하였는가\?)(?=\s*<\/div>|\s*<\/td>|\s*<br\s*\/?>)')
        content = pattern.sub(r'\1하였는가?', content)

    # 3. 띄어쓰기 및 중복 다듬기
    content = content.replace(" 하였는가?", "하였는가?")
    content = content.replace("하였는가?하였는가?", "하였는가?")
    content = content.replace("확인하였는가?하였는가?", "확인하였는가?")
    content = content.replace("하였는가? 여부", "하였는가?")
    content = content.replace("하였는가? 확인", "하였는가?")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1
        print(f"✅ Updated Checklist: {filepath}")

# Traverse all directories in 콘크리트도상
for root, dirs, files in os.walk(base_dir):
    # CRITICAL: STRICTLY SKIP WBS 11 frozen files
    if '11' in os.path.basename(root) or '시공계획' in os.path.basename(root):
        skipped_count += len(files)
        continue
    
    if os.path.basename(root) == '체크리스트':
        for file in files:
            if file.endswith('.html'):
                # Also double check filename is not WBS 11
                if '11' in file or '시공계획' in file:
                    skipped_count += 1
                    continue
                process_checklist_html(os.path.join(root, file))

print(f"\n🎉 COMPLETED ALL CONCRETE SLAB CHECKLIST UPDATES!")
print(f"Total Modified Checklist Files: {modified_count}")
print(f"Skipped WBS 11 Frozen Files: {skipped_count}")
