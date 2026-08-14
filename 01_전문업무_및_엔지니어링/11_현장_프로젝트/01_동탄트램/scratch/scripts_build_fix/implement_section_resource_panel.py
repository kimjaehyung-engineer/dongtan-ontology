import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Resource Monitoring Panel to the bottom of v-filter-tray
panel_html = """
      <!-- 좌측 하단 여백: 선택 시공구간 자원 현황 & 실시간 입력 패널 -->
      <div class="tray-resource-panel" style="margin-top: 1rem; padding: 0.85rem; background: #0f172a; border-radius: 10px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
        <div style="font-size: 0.82rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 0.4rem;">
          <span>👷 선택구간 자원 현황</span>
          <span id="panel-sec-name" style="font-size: 0.75rem; color: #a78bfa; font-weight: 900;">(본)1-17-305정거장</span>
        </div>

        <div id="panel-resource-content" style="font-size: 0.76rem; color: #cbd5e1; line-height: 1.6;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
            <span style="color: #94a3b8;">• 총 소요공기:</span>
            <b id="panel-sec-days" style="color: #ffffff;">60 일</b>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
            <span style="color: #94a3b8;">• 투입 인력:</span>
            <b id="panel-sec-labor" style="color: #38bdf8;">15 명/일 (조종원 2, 인부 13)</b>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
            <span style="color: #94a3b8;">• 투입 장비:</span>
            <b id="panel-sec-equip" style="color: #f59e0b;">3 대/일 (백호 1, 덤프 2)</b>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
            <span style="color: #94a3b8;">• 추정 직접비:</span>
            <b id="panel-sec-cost" style="color: #10b981;">3.85 억원 (320만원/m)</b>
          </div>
        </div>

        <button onclick="openSectionResourceEditModal()" style="margin-top: 0.65rem; width: 100%; padding: 0.45rem; background: #0284c7; color: #ffffff; border: none; border-radius: 6px; font-size: 0.78rem; font-weight: 800; cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 6px rgba(2,132,199,0.4);">
          ✏️ 선택 구간 자원 직접 수정/입력
        </button>
      </div>
"""

filter_tray_end = r'</aside>'
if filter_tray_end in content:
    content = content.replace('</aside>', panel_html + '\n    </aside>', 1)
    print("Injected Resource Monitoring Panel into Left Sidebar (v-filter-tray)!")

# 2. Add Section Resource Edit Modal HTML
edit_modal_html = """
  <!-- ============================================================================ -->
  <!-- ✏️ 선택 시공구간 자원 실시간 수정/입력 팝업 모달 -->
  <!-- ============================================================================ -->
  <div id="modal-sec-res-edit" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15,23,42,0.85); backdrop-filter: blur(4px); z-index: 9999; align-items: center; justify-content: center;">
    <div style="background: #1e293b; width: 560px; max-width: 90vw; border-radius: 14px; border: 1px solid #334155; box-shadow: 0 20px 40px rgba(0,0,0,0.6); padding: 1.5rem; color: #f8fafc;">
      
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 0.8rem; margin-bottom: 1.2rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
          <span style="font-size: 1.3rem;">✏️</span>
          <div>
            <h3 style="font-size: 1.1rem; font-weight: 900; color: #38bdf8; margin: 0;" id="edit-sec-modal-title">시공구간 자원 직접 수정/입력</h3>
            <p style="font-size: 0.78rem; color: #94a3b8; margin: 0;">선택된 시공구간의 투입 인력(명/일), 장비(대/일), 자재 및 직접 공사비 수정</p>
          </div>
        </div>
        <button onclick="closeSectionResourceEditModal()" style="background: transparent; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer;">✕</button>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem;">
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">일일 투입 작업자 수 (명/일)</label>
          <input type="number" id="edit-sec-labor" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #38bdf8; font-weight: 900; border-radius: 6px; font-size: 0.85rem;" value="15"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">세부 인력 구성 (텍스트)</label>
          <input type="text" id="edit-sec-labor-desc" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.82rem;" value="조종원 2, 특별인부 13"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">일일 투입 중장비 수 (대/일)</label>
          <input type="number" id="edit-sec-equip" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #f59e0b; font-weight: 900; border-radius: 6px; font-size: 0.85rem;" value="3"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">세부 장비 구성 (텍스트)</label>
          <input type="text" id="edit-sec-equip-desc" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.82rem;" value="백호 1, 덤프 2"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">총 추정 직접공사비 (억원)</label>
          <input type="number" step="0.01" id="edit-sec-cost" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #10b981; font-weight: 900; border-radius: 6px; font-size: 0.85rem;" value="3.85"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">구간 연장 (m)</label>
          <input type="number" id="edit-sec-dist" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.85rem;" value="250"/>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 0.6rem;">
        <button onclick="closeSectionResourceEditModal()" style="padding: 0.5rem 1.2rem; background: #334155; color: #ffffff; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 700; cursor: pointer;">취소</button>
        <button onclick="saveSectionResourceEdit()" style="padding: 0.5rem 1.4rem; background: #0284c7; color: #ffffff; border: none; border-radius: 6px; font-size: 0.85rem; font-weight: 900; cursor: pointer; box-shadow: 0 4px 12px rgba(2,132,199,0.4);">
          ✅ 자원 변경사항 저장 & 전면 업데이트
        </button>
      </div>

    </div>
  </div>
"""

body_end_idx = content.find('</body>')
if body_end_idx != -1:
    content = content[:body_end_idx] + edit_modal_html + "\n" + content[body_end_idx:]
    print("Injected Section Resource Edit Modal HTML!")

# 3. Add JS functions for Section Resource Panel & Modal
js_section_panel_code = """
// ============================================================================
// 👷 좌측 하단 선택 시공구간 자원 모니터링 & 편집 패널 JS
// ============================================================================
let currentSelectedSectionData = null;

function updateSelectedSectionResourcePanel(secItem) {
  if (!secItem) {
    // Default fallback to first section if available
    if (window.SECTION_SPLITS && SECTION_SPLITS.length > 0) {
      secItem = SECTION_SPLITS[0];
    } else {
      return;
    }
  }

  currentSelectedSectionData = secItem;

  const nameEl = document.getElementById("panel-sec-name");
  const daysEl = document.getElementById("panel-sec-days");
  const laborEl = document.getElementById("panel-sec-labor");
  const equipEl = document.getElementById("panel-sec-equip");
  const costEl = document.getElementById("panel-sec-cost");

  const totD = secItem.totalDays || 60;
  const laborCount = secItem.customLabor || (10 + (totD % 12));
  const laborDesc = secItem.customLaborDesc || `조종원 2, 보통인부 ${laborCount - 2}`;
  const equipCount = secItem.customEquip || (2 + (totD % 3));
  const equipDesc = secItem.customEquipDesc || `백호 1, 덤프 ${equipCount - 1}`;
  const costW = secItem.customCost || ((totD * 6.5) / 100).toFixed(2);
  const distM = secItem.distM || 250;
  const unitCost = ((costW * 10000) / Math.max(1, distM)).toFixed(0);

  if (nameEl) nameEl.textContent = secItem.sectionName || '선택 구간';
  if (daysEl) daysEl.textContent = `${totD} 일`;
  if (laborEl) laborEl.textContent = `${laborCount} 명/일 (${laborDesc})`;
  if (equipEl) equipEl.textContent = `${equipCount} 대/일 (${equipDesc})`;
  if (costEl) costEl.textContent = `${costW} 억원 (${unitCost}만원/m)`;
}

function openSectionResourceEditModal() {
  if (!currentSelectedSectionData && window.SECTION_SPLITS && SECTION_SPLITS.length > 0) {
    currentSelectedSectionData = SECTION_SPLITS[0];
  }
  if (!currentSelectedSectionData) return;

  const modal = document.getElementById("modal-sec-res-edit");
  const titleEl = document.getElementById("edit-sec-modal-title");
  const laborEl = document.getElementById("edit-sec-labor");
  const laborDescEl = document.getElementById("edit-sec-labor-desc");
  const equipEl = document.getElementById("edit-sec-equip");
  const equipDescEl = document.getElementById("edit-sec-equip-desc");
  const costEl = document.getElementById("edit-sec-cost");
  const distEl = document.getElementById("edit-sec-dist");

  const totD = currentSelectedSectionData.totalDays || 60;
  const laborCount = currentSelectedSectionData.customLabor || (10 + (totD % 12));
  const laborDesc = currentSelectedSectionData.customLaborDesc || `조종원 2, 보통인부 ${laborCount - 2}`;
  const equipCount = currentSelectedSectionData.customEquip || (2 + (totD % 3));
  const equipDesc = currentSelectedSectionData.customEquipDesc || `백호 1, 덤프 ${equipCount - 1}`;
  const costW = currentSelectedSectionData.customCost || ((totD * 6.5) / 100).toFixed(2);
  const distM = currentSelectedSectionData.distM || 250;

  if (titleEl) titleEl.textContent = `✏️ [${currentSelectedSectionData.sectionName}] 자원 직접 수정`;
  if (laborEl) laborEl.value = laborCount;
  if (laborDescEl) laborDescEl.value = laborDesc;
  if (equipEl) equipEl.value = equipCount;
  if (equipDescEl) equipDescEl.value = equipDesc;
  if (costEl) costEl.value = costW;
  if (distEl) distEl.value = distM;

  if (modal) modal.style.display = "flex";
}

function closeSectionResourceEditModal() {
  const modal = document.getElementById("modal-sec-res-edit");
  if (modal) modal.style.display = "none";
}

function saveSectionResourceEdit() {
  if (!currentSelectedSectionData) return;

  const laborCount = parseInt(document.getElementById("edit-sec-labor")?.value) || 12;
  const laborDesc = document.getElementById("edit-sec-labor-desc")?.value || '조종원 2, 보통인부 10';
  const equipCount = parseInt(document.getElementById("edit-sec-equip")?.value) || 3;
  const equipDesc = document.getElementById("edit-sec-equip-desc")?.value || '백호 1, 덤프 2';
  const costW = parseFloat(document.getElementById("edit-sec-cost")?.value) || 3.5;
  const distM = parseInt(document.getElementById("edit-sec-dist")?.value) || 250;

  currentSelectedSectionData.customLabor = laborCount;
  currentSelectedSectionData.customLaborDesc = laborDesc;
  currentSelectedSectionData.customEquip = equipCount;
  currentSelectedSectionData.customEquipDesc = equipDesc;
  currentSelectedSectionData.customCost = costW;
  currentSelectedSectionData.distM = distM;

  updateSelectedSectionResourcePanel(currentSelectedSectionData);
  if (typeof renderAll === 'function') renderAll();
  closeSectionResourceEditModal();

  alert(`✅ [${currentSelectedSectionData.sectionName}] 구간 자원 정보가 저장되고 2D 공정표와 자원 데이터가 즉시 업데이트되었습니다!`);
}

// Automatically bind updateSelectedSectionResourcePanel on window.onload
window.addEventListener('load', () => {
  setTimeout(() => {
    if (window.SECTION_SPLITS && window.SECTION_SPLITS.length > 0) {
      updateSelectedSectionResourcePanel(window.SECTION_SPLITS[0]);
    }
  }, 500);
});
"""

script_end_idx = content.rfind('</script>')
if script_end_idx != -1:
    content = content[:script_end_idx] + "\n" + js_section_panel_code + "\n" + content[script_end_idx:]
    print("Injected Section Resource Panel JS Logic!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished integrating Section Resource Panel into HTML!")
