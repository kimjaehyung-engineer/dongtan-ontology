import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update container-resource-view and container-evm-view container styles for flex filling & zero bottom whitespace
content = content.replace(
    'id="container-resource-view" style="display: none; padding: 1.2rem; background: #0f172a; color: #f8fafc; overflow-y: auto; height: calc(100vh - 65px);"',
    'id="container-resource-view" style="display: none; flex-direction: column; padding: 1.2rem; background: #0f172a; color: #f8fafc; overflow-y: auto; height: calc(100vh - 65px);"'
)

content = content.replace(
    'id="container-evm-view" style="display: none; padding: 1.2rem; background: #0f172a; color: #f8fafc; overflow-y: auto; height: calc(100vh - 65px);"',
    'id="container-evm-view" style="display: none; flex-direction: column; padding: 1.2rem; background: #0f172a; color: #f8fafc; overflow-y: auto; height: calc(100vh - 65px);"'
)

# 2. Update renderResourceHistogram for clean X-axis, Legends, and Zero Overlap
old_histogram_func = r'function renderResourceHistogram\(\) \{[\s\S]*?function runResourceOptimization'

new_histogram_func = """function renderResourceHistogram() {
  const container = document.getElementById("resource-histogram-container");
  if (!container) return;

  const months = ["27/07", "27/10", "28/01", "28/04", "28/07", "28/10", "29/01", "29/04", "29/07", "29/10", "30/01", "30/04"];
  const laborLoads = [85, 120, 165, 185, 170, 140, 110, 95, 80, 65, 45, 30];
  const equipLoads = [18, 28, 38, 42, 36, 30, 22, 18, 15, 12, 8, 5];

  let barsHtml = "";
  const chartH = 135;
  const startY = 35;
  const barWidth = 34;
  const startX = 60;

  months.forEach((m, i) => {
    const x = startX + i * 56;
    const lH = (laborLoads[i] / 220) * chartH;
    const eH = (equipLoads[i] / 50) * (chartH * 0.6);

    const isPeak = laborLoads[i] > 175;
    const barColor = isPeak ? "#ef4444" : "#0284c7";

    barsHtml += `
      <!-- Labor Bar -->
      <rect x="${x}" y="${startY + chartH - lH}" width="${barWidth}" height="${lH}" fill="${barColor}" rx="4" opacity="0.88"/>
      <!-- Equipment Bar Overlay -->
      <rect x="${x + 6}" y="${startY + chartH - eH}" width="${barWidth - 12}" height="${eH}" fill="#f59e0b" rx="2" opacity="0.95"/>
      
      <!-- Date Label cleanly inside SVG -->
      <text x="${x + barWidth/2}" y="${startY + chartH + 20}" text-anchor="middle" fill="#94a3b8" font-size="11px" font-weight="800">${m}</text>
      <!-- Value Badge -->
      <text x="${x + barWidth/2}" y="${startY + chartH - lH - 6}" text-anchor="middle" fill="#ffffff" font-size="10px" font-weight="900">${laborLoads[i]}명</text>
    `;
  });

  container.innerHTML = `
    <svg width="100%" height="100%" viewBox="0 0 800 215" preserveAspectRatio="none">
      <!-- Grid Lines -->
      <line x1="50" y1="35" x2="760" y2="35" stroke="#334155" stroke-dasharray="4,4"/>
      <line x1="50" y1="102" x2="760" y2="102" stroke="#334155" stroke-dasharray="4,4"/>
      <line x1="50" y1="170" x2="760" y2="170" stroke="#475569" stroke-width="1.5"/>

      <!-- Limit Line (200 Limit) -->
      <line x1="50" y1="48" x2="760" y2="48" stroke="#ef4444" stroke-width="2" stroke-dasharray="6,4"/>

      <!-- Legends at top right -->
      <g transform="translate(430, 16)">
        <rect x="0" y="0" width="12" height="12" fill="#0284c7" rx="2"/>
        <text x="17" y="10" fill="#f8fafc" font-size="11px" font-weight="700">작업자 인력 (명/일)</text>

        <rect x="135" y="0" width="12" height="12" fill="#f59e0b" rx="2"/>
        <text x="152" y="10" fill="#f8fafc" font-size="11px" font-weight="700">중장비 투입 (대/일)</text>

        <line x1="260" y1="6" x2="280" y2="6" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,2"/>
        <text x="286" y="10" fill="#ef4444" font-size="11px" font-weight="900">한도 200명</text>
      </g>

      ${barsHtml}
    </svg>
  `;
}

function runResourceOptimization"""

if re.search(old_histogram_func, content):
    content = re.sub(old_histogram_func, new_histogram_func, content, count=1)
    print("Updated renderResourceHistogram with clean X-axis, legends, and zero overlap!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying histogram layout and legend fixes to HTML!")
