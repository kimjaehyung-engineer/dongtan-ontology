import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure default active class on header buttons is SPLITS, not ACTS
content = content.replace(
    '<button class="btn-viewmode" id="btn-view-splits"',
    '<button class="btn-viewmode active" id="btn-view-splits"'
)

# Fix setMainTab to ensure SPLITS view is rendered cleanly when switching back to TC
old_set_main_tab = r'function setMainTab\(tab\) \{[\s\S]*?\}'

new_set_main_tab = """function setMainTab(tab) {
  currentMainTab = tab;
  const tabTc = document.getElementById("tab-main-tc");
  const tabRes = document.getElementById("tab-main-res");
  const tabEvm = document.getElementById("tab-main-evm");

  const layoutTc = document.querySelector(".app-layout");
  const viewRes = document.getElementById("container-resource-view");
  const viewEvm = document.getElementById("container-evm-view");

  [tabTc, tabRes, tabEvm].forEach(b => {
    if (b) {
      b.style.background = "transparent";
      b.style.color = "#94a3b8";
    }
  });

  if (tab === 'TC') {
    if (tabTc) { tabTc.style.background = "#0284c7"; tabTc.style.color = "#ffffff"; }
    if (layoutTc) layoutTc.style.display = "flex";
    if (viewRes) viewRes.style.display = "none";
    if (viewEvm) viewEvm.style.display = "none";
    
    // Always default back to clean 28 Construction Section Representative View (SPLITS)
    currentViewMode = 'SPLITS';
    document.querySelectorAll('.btn-viewmode').forEach(btn => btn.classList.remove('active'));
    document.getElementById('btn-view-splits')?.classList.add('active');
    
    if (typeof renderAll === 'function') {
      renderAll();
    }
  } else if (tab === 'RESOURCE') {
    if (tabRes) { tabRes.style.background = "#0284c7"; tabRes.style.color = "#ffffff"; }
    if (layoutTc) layoutTc.style.display = "none";
    if (viewRes) viewRes.style.display = "block";
    if (viewEvm) viewEvm.style.display = "none";

    renderResourceModule();
  } else if (tab === 'EVM') {
    if (tabEvm) { tabEvm.style.background = "#10b981"; tabEvm.style.color = "#ffffff"; }
    if (layoutTc) layoutTc.style.display = "none";
    if (viewRes) viewRes.style.display = "none";
    if (viewEvm) viewEvm.style.display = "block";

    renderEVMModule();
  }
}"""

if re.search(old_set_main_tab, content):
    content = re.sub(old_set_main_tab, new_set_main_tab, content, count=1)
    print("Updated setMainTab to automatically default to clean SPLITS view!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished restoring clean SPLITS view!")
