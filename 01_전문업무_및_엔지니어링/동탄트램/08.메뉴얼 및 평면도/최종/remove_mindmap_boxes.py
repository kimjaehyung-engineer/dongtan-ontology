import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

count = 0
modified_files = []

# Pattern to find and remove .insight-box or mindmap texts
pattern_insight_box = re.compile(r'<div class="insight-box">.*?</div>', re.DOTALL)
pattern_mindmap_text = re.compile(r'.*?연상 마인드맵.*?\n?', re.IGNORECASE)

print(f"Scanning HTML files in '{base_attach_dir}' to remove mindmap/exam-related insight boxes...")

for root, dirs, files in os.walk(base_attach_dir):
    for f in files:
        if f.endswith('.html'):
            file_path = os.path.join(root, f)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = content
            
            # Remove .insight-box div completely
            if 'insight-box' in new_content:
                new_content = re.sub(pattern_insight_box, '', new_content)
                
            # Remove any lingering "꼬리에 꼬리를 무는" or "중심 이미지" or "연상 마인드맵" text
            if '연상 마인드맵' in new_content or '중심 이미지' in new_content or '꼬리에 꼬리를' in new_content:
                lines = new_content.splitlines()
                filtered_lines = [l for l in lines if not any(k in l for k in ["연상 마인드맵", "중심 이미지", "꼬리에 꼬리를"])]
                new_content = "\n".join(filtered_lines)
                
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1
                modified_files.append(os.path.basename(file_path))

print(f"\n🎉 Successfully cleaned and updated {count} HTML files! Removed all mindmap/exam-style boxes.")
print("Sample cleaned files:", modified_files[:10])
