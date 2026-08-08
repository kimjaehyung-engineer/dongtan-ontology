import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function selectConstructionSection(')
if idx != -1:
    end_idx = text.find('function ', idx + 10)
    func_text = text[idx:end_idx]
    print("Contains pulse-ring-1 in selectConstructionSection:", "pulse-ring-1" in func_text)
    print("Contains pulse-ring-2 in selectConstructionSection:", "pulse-ring-2" in func_text)
    print("\nSnippet of selectConstructionSection:")
    print(func_text[:500])
