import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Change '정거장 명칭' to '정거장 번호' in layer panel
text = text.replace(
    '<input type="checkbox" id="toggle-labels" checked> 정거장 명칭',
    '<input type="checkbox" id="toggle-labels" checked> 정거장 번호'
)

# 2. Change '교차로 구간선 (노선 오버레이)' to '교차로 구간선' in layer panel
text = text.replace(
    '<input type="checkbox" id="toggle-intersections-lines" checked> 교차로 구간선 (노선 오버레이)',
    '<input type="checkbox" id="toggle-intersections-lines" checked> 교차로 구간선'
)

# 3. Change '교차로명 라벨 (구간연장)' to '교차로명 라벨' in layer panel
text = text.replace(
    '<input type="checkbox" id="toggle-intersections-labels" checked> 교차로명 라벨 (구간연장)',
    '<input type="checkbox" id="toggle-intersections-labels" checked> 교차로명 라벨'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated layer panel text labels successfully!")
