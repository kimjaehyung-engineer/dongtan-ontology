import sys
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace duplicated setMainTab block containing the orphan }); line
duplicated_set_main_tab_pattern = r'function setMainTab\(tab\) \{[\s\S]*?function recalculateEVM'

clean_set_main_tab_block = """function setMainTab(tab) {
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
}

function recalculateEVM"""

if re.search(duplicated_set_main_tab_pattern, content):
    content = re.sub(duplicated_set_main_tab_pattern, clean_set_main_tab_block, content, count=1)
    print("Cleaned up setMainTab duplicate block and orphan }); token!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying JS syntax fix to HTML!")
