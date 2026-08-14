import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Helper JS code
helper_js = """
// ============================================================================
// 🧹 정거장 명칭 단축 및 중복 숫자 제거 정제 엔진
// ============================================================================
function formatCleanStationLabel(id, stnName) {
  if (!stnName) return id;

  let str = String(stnName).trim();

  // If exact match to simple station name pattern e.g. "202 정거장", "202역", "202"
  if (str === id || str === `${id}정거장` || str === `${id}역` || str === `${id} 정거장` || str === `${id} 역`) {
    return id;
  }

  // Remove leading id prefix e.g. "210 정거장 (본선 종점 전방)" -> "(본선 종점 전방)"
  str = str.replace(new RegExp(`^${id}\\\\s*(정거장|역)?\\\\s*`), '').trim();
  str = str.replace(/정거장$/, '').trim();

  // Strip wrapping parentheses if present
  if (str.startsWith('(') && str.endsWith(')')) {
    str = str.substring(1, str.length - 1).trim();
  }

  if (!str || str === id) return id;

  return `${id} (${str})`;
}
"""

if 'function formatCleanStationLabel' not in content:
    idx = content.find('function renderStationTargetOverlay')
    if idx != -1:
        content = content[:idx] + helper_js + '\n' + content[idx:]
        print("Injected formatCleanStationLabel helper function!")

# Update renderStationTargetOverlay to use formatCleanStationLabel
old_badge_code = r'const fullLabelText = `🚊 \${cleanStnLabel}`;'
new_badge_code = 'const fullLabelText = `🚊 ${formatCleanStationLabel(id, detail ? detail.name : id)}`;'

if re.search(old_badge_code, content):
    content = re.sub(old_badge_code, new_badge_code, content, count=1)
    print("Updated SVG map badge in renderStationTargetOverlay!")

# Update quickNav option generation code in renderInteractiveElements
old_opt_code = r'let optName = detail\.name \|\| id;[\s\S]*?option\.textContent = optName;'
new_opt_code = 'option.textContent = formatCleanStationLabel(id, detail ? detail.name : id);'

if re.search(old_opt_code, content):
    content = re.sub(old_opt_code, new_opt_code, content, count=1)
    print("Updated quickNav dropdown option formatting to use formatCleanStationLabel!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished cleaning duplicate station numbers in V1 HTML!")
