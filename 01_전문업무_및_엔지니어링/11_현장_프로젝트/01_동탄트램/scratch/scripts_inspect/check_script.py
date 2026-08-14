import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\add_intersection_zoom_modal.py'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("Script length:", len(text))
print("Contains css_modal_code:", 'css_modal_code' in text)
print("Contains js_modal_logic:", 'js_modal_logic' in text)
print("Contains html_modal_code:", 'html_modal_code' in text)
