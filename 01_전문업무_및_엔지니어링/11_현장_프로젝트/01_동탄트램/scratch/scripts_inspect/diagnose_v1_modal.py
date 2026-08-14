import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("CSS .modal-overlay present:", '.modal-overlay' in text)
print("CSS .modal-overlay.open present:", '.modal-overlay.open' in text)
print("CSS .modal-overlay.active present:", '.modal-overlay.active' in text)

idx_func = text.find('function openIntersectionModal')
if idx_func != -1:
    print("\nCurrent openIntersectionModal func snippet:")
    print(text[idx_func:idx_func+1000])

idx_modal = text.find('id="intersection-zoom-modal"')
if idx_modal != -1:
    print("\nModal HTML markup snippet:")
    print(text[idx_modal-50:idx_modal+600])

