import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))

idx = text.find('function renderConstructionSections()')
if idx != -1:
    end_idx = text.find('function ', idx + 10)
    func_text = text[idx:end_idx]
    print("Contains leaderLineStart in renderConstructionSections:", "leaderLineStart" in func_text)
    print("Contains dimLine in renderConstructionSections:", "dimLine" in func_text)

idx2 = text.find('function selectConstructionSection(')
if idx2 != -1:
    end_idx2 = text.find('function ', idx2 + 10)
    func_text2 = text[idx2:end_idx2]
    print("Contains lStart in selectConstructionSection:", "lStart" in func_text2)
    print("Contains dimHighlight in selectConstructionSection:", "dimHighlight" in func_text2)

print("\nSnippet of renderConstructionSections:")
print(func_text[500:1200])
