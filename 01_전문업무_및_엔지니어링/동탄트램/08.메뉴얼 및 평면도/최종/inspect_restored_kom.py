import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

targets = [
    ("사전토공사", "2_발주전략 KOM"),
    ("상부강화노반", "2_발주전략 KOM"),
    ("콘크리트도상", "4_발주전략 KOM")
]

for gongjong, folder in targets:
    print(f"\n==================== {gongjong} ({folder}) ====================")
    dir_path = os.path.join(target_base, gongjong, folder)
    for sub in ['표준서', '수행지침', '체크리스트']:
        sub_dir = os.path.join(dir_path, sub)
        if os.path.exists(sub_dir):
            files = os.listdir(sub_dir)
            if files:
                fp = os.path.join(sub_dir, files[0])
                print(f"\n--- Sub: {sub} ({files[0]}) ---")
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Just print first 15 lines and search for key texts or lists
                    lines = content.split('\n')
                    print("\n".join(lines[:20]))
                    print("...")
                    # Also print any UL/OL list contents
                    import re
                    lists = re.findall(r'<ul[^>]*>.*?</ul>|<ol[^>]*>.*?</ol>|<table[^>]*>.*?</table>', content, re.DOTALL)
                    for idx, lst in enumerate(lists):
                        # Strip tags to show text content inside lists
                        text_only = re.sub(r'<[^>]*>', ' ', lst).strip()
                        text_only = re.sub(r'\s+', ' ', text_only)
                        print(f"List/Table {idx+1}: {text_only[:400]}...")
