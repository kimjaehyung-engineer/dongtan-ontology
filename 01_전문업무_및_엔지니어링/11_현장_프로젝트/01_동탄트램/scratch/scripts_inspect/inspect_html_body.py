import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Print main HTML container and tab layout if any
print("File length:", len(text))
idx = text.find('</head>')
print("Head ends at:", idx)
idx_body = text.find('<body')
print("Body starts at:", idx_body)
print(text[idx_body:idx_body+1500])
