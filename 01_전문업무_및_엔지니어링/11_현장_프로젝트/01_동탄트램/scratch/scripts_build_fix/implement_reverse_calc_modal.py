import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add "Q값 역산 계산기" button to container-resource-view header
old_res_header = r'<div style="display: flex; gap: 0.6rem;">\s*<button onclick="runResourceOptimization\(\)"'

new_res_header = """<div style="display: flex; gap: 0.6rem;">
        <button onclick="openReverseCalcModal()" style="padding: 0.6rem 1.2rem; background: #8b5cf6; color: #ffffff; border: none; border-radius: 8px; font-size: 0.88rem; font-weight: 900; cursor: pointer; box-shadow: 0 4px 12px rgba(139,92,246,0.4);">
          🔄 Q값(물량)·생산성 기반 자원 역산 계산기
        </button>
        <button onclick="runResourceOptimization()\""""

if re.search(old_res_header, content):
    content = re.sub(old_res_header, new_res_header, content, count=1)
    print("Added Reverse Calculator Button to Resource View Header!")

# 2. Add Modal HTML before </body>
modal_html = """
  <!-- ============================================================================ -->
  <!-- 🔄 Q값(물량) & 생산성 기반 소요자원 역산 계산기 팝업 모달 -->
  <!-- ============================================================================ -->
  <div id="modal-reverse-calc" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15,23,42,0.85); backdrop-filter: blur(4px); z-index: 9999; align-items: center; justify-content: center;">
    <div style="background: #1e293b; width: 680px; max-width: 92vw; border-radius: 14px; border: 1px solid #334155; box-shadow: 0 20px 40px rgba(0,0,0,0.6); padding: 1.5rem; color: #f8fafc; position: relative;">
      
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 0.8rem; margin-bottom: 1.2rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
          <span style="font-size: 1.4rem;">🔄</span>
          <div>
            <h3 style="font-size: 1.15rem; font-weight: 900; color: #a78bfa; margin: 0;">Q값(물량) & 생산성 기반 소요자원 역산 시뮬레이터</h3>
            <p style="font-size: 0.78rem; color: #94a3b8; margin: 0;">소요기간(D) 대비 총 물량(Q)과 일일 생산성(q)으로 일일 장비 대수 및 보통인부 수 역산</p>
          </div>
        </div>
        <button onclick="closeReverseCalcModal()" style="background: transparent; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer; padding: 0.2rem 0.5rem;">✕</button>
      </div>

      <!-- 공종별 표준 프리셋 선택 -->
      <div style="margin-bottom: 1.2rem; background: #0f172a; padding: 0.8rem; border-radius: 8px;">
        <label style="font-size: 0.8rem; color: #38bdf8; font-weight: 800; display: block; margin-bottom: 0.4rem;">📌 공종별 일일 생산성 표준 프리셋 (Quick Preset)</label>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
          <button onclick="applyPreset('EARTH')" style="padding: 0.35rem 0.7rem; background: #334155; color: #ffffff; border: 1px solid #475569; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">🚜 토공/굴착 (350m³/대, 30m³/명)</button>
          <button onclick="applyPreset('CIVIL')" style="padding: 0.35rem 0.7rem; background: #334155; color: #ffffff; border: 1px solid #475569; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">🏗️ 노반/다짐 (400m³/대, 50m³/명)</button>
          <button onclick="applyPreset('TRACK')" style="padding: 0.35rem 0.7rem; background: #334155; color: #ffffff; border: 1px solid #475569; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">🚊 궤도 부설 (60m/대, 20m/명)</button>
          <button onclick="applyPreset('SYS')" style="padding: 0.35rem 0.7rem; background: #334155; color: #ffffff; border: 1px solid #475569; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">⚡ 시스템/배선 (100m/대, 35m/명)</button>
        </div>
      </div>

      <!-- 입력 데이터 폼 -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem;">
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">대상 액티비티 선택</label>
          <select id="rc-select-activity" onchange="onRcActivityChange()" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.82rem;">
            <!-- Options populated by JS -->
          </select>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">액티비티 소요기간 (D)</label>
          <input type="number" id="rc-duration" readonly style="width: 100%; padding: 0.5rem; background: #1e293b; border: 1px solid #334155; color: #38bdf8; font-weight: 900; border-radius: 6px; font-size: 0.85rem;" value="30"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">총 작업 물량 (Q값 - m³ 또는 m)</label>
          <input type="number" id="rc-quantity" oninput="calculateReverseResource()" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.85rem;" value="12000"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">인력 일일 생산성 (q_labor - m³/명/일)</label>
          <input type="number" id="rc-prod-labor" oninput="calculateReverseResource()" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.85rem;" value="30"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">장비 일일 생산성 (q_equip - m³/대/일)</label>
          <input type="number" id="rc-prod-equip" oninput="calculateReverseResource()" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.85rem;" value="350"/>
        </div>
        <div>
          <label style="font-size: 0.78rem; color: #94a3b8; font-weight: 700; display: block; margin-bottom: 0.3rem;">자재 수급 단위비 (만원/단위)</label>
          <input type="number" id="rc-mat-rate" oninput="calculateReverseResource()" style="width: 100%; padding: 0.5rem; background: #0f172a; border: 1px solid #334155; color: #ffffff; border-radius: 6px; font-size: 0.85rem;" value="15"/>
        </div>
      </div>

      <!-- 역산 결과 대시보드 카전 -->
      <div style="background: rgba(139,92,246,0.12); border: 1px solid rgba(139,92,246,0.3); border-radius: 10px; padding: 1rem; margin-bottom: 1.2rem;">
        <h4 style="font-size: 0.85rem; font-weight: 800; color: #a78bfa; margin: 0 0 0.6rem 0;">📊 공학적 소요자원 역산(Back-calculation) 결과</h4>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; text-align: center;">
          <div style="background: #0f172a; padding: 0.6rem; border-radius: 8px;">
            <div style="font-size: 0.72rem; color: #94a3b8;">필요 총 인-일</div>
            <div style="font-size: 1.15rem; font-weight: 900; color: #38bdf8;" id="rc-res-mandays">400 Man-Days</div>
          </div>
          <div style="background: #0f172a; padding: 0.6rem; border-radius: 8px;">
            <div style="font-size: 0.72rem; color: #94a3b8;">일일 필요 작업자 (L)</div>
            <div style="font-size: 1.25rem; font-weight: 900; color: #34d399;" id="rc-res-daily-labor">13 명/일</div>
          </div>
          <div style="background: #0f172a; padding: 0.6rem; border-radius: 8px;">
            <div style="font-size: 0.72rem; color: #94a3b8;">일일 필요 중장비 (E)</div>
            <div style="font-size: 1.25rem; font-weight: 900; color: #f59e0b;" id="rc-res-daily-equip">2 대/일</div>
          </div>
          <div style="background: #0f172a; padding: 0.6rem; border-radius: 8px;">
            <div style="font-size: 0.72rem; color: #94a3b8;">추정 총 직접비</div>
            <div style="font-size: 1.15rem; font-weight: 900; color: #a78bfa;" id="rc-res-totalcost">4,250 만원</div>
          </div>
        </div>
      </div>

      <!-- 액션 버튼 -->
      <div style="display: flex; justify-content: flex-end; gap: 0.6rem;">
        <button onclick="closeReverseCalcModal()" style="padding: 0.55rem 1.2rem; background: #334155; color: #ffffff; border: none; border-radius: 6px; font-size: 0.85rem; font-weight: 700; cursor: pointer;">취소</button>
        <button onclick="applyReverseResourceToActivity()" style="padding: 0.55rem 1.4rem; background: #8b5cf6; color: #ffffff; border: none; border-radius: 6px; font-size: 0.88rem; font-weight: 900; cursor: pointer; box-shadow: 0 4px 12px rgba(139,92,246,0.4);">
          ✅ 역산된 자원 산출값 액티비티에 적용
        </button>
      </div>

    </div>
  </div>
"""

body_end_idx = content.find('</body>')
if body_end_idx != -1:
    content = content[:body_end_idx] + modal_html + "\n" + content[body_end_idx:]
    print("Injected Reverse Calculator Modal HTML!")

# 3. Add JS Functions for Modal & Calculation
modal_js_code = """
// ============================================================================
// 🔄 Q값(물량) & 생산성 기반 소요자원 역산 시뮬레이터 JS
// ============================================================================
function openReverseCalcModal(targetIndex = 0) {
  const modal = document.getElementById("modal-reverse-calc");
  const select = document.getElementById("rc-select-activity");
  if (!modal || !select || !window.RAW_ACTIVITIES) return;

  enrichActivitiesWithResources();

  // Populate activity options
  let optionsHtml = "";
  RAW_ACTIVITIES.slice(0, 80).forEach((act, idx) => {
    optionsHtml += `<option value="${idx}">[${act.zone || '1공구'}] ${act.ades || ''} (${act.ed || 30}일)</option>`;
  });
  select.innerHTML = optionsHtml;
  select.value = targetIndex;

  modal.style.display = "flex";
  onRcActivityChange();
}

function closeReverseCalcModal() {
  const modal = document.getElementById("modal-reverse-calc");
  if (modal) modal.style.display = "none";
}

function applyPreset(presetType) {
  const qEl = document.getElementById("rc-quantity");
  const pLaborEl = document.getElementById("rc-prod-labor");
  const pEquipEl = document.getElementById("rc-prod-equip");

  if (presetType === 'EARTH') {
    if (qEl) qEl.value = 12000;
    if (pLaborEl) pLaborEl.value = 30;
    if (pEquipEl) pEquipEl.value = 350;
  } else if (presetType === 'CIVIL') {
    if (qEl) qEl.value = 8500;
    if (pLaborEl) pLaborEl.value = 50;
    if (pEquipEl) pEquipEl.value = 400;
  } else if (presetType === 'TRACK') {
    if (qEl) qEl.value = 1400;
    if (pLaborEl) pLaborEl.value = 20;
    if (pEquipEl) pEquipEl.value = 60;
  } else if (presetType === 'SYS') {
    if (qEl) qEl.value = 2500;
    if (pLaborEl) pLaborEl.value = 35;
    if (pEquipEl) pEquipEl.value = 100;
  }

  calculateReverseResource();
}

function onRcActivityChange() {
  const select = document.getElementById("rc-select-activity");
  const durEl = document.getElementById("rc-duration");
  if (!select || !durEl || !window.RAW_ACTIVITIES) return;

  const idx = parseInt(select.value) || 0;
  const act = RAW_ACTIVITIES[idx];
  if (act) {
    durEl.value = act.ed || 30;
  }

  calculateReverseResource();
}

let lastCalculatedReverseRes = null;

function calculateReverseResource() {
  const dur = Math.max(1, parseFloat(document.getElementById("rc-duration")?.value) || 30);
  const q = Math.max(1, parseFloat(document.getElementById("rc-quantity")?.value) || 10000);
  const pLabor = Math.max(0.1, parseFloat(document.getElementById("rc-prod-labor")?.value) || 30);
  const pEquip = Math.max(0.1, parseFloat(document.getElementById("rc-prod-equip")?.value) || 350);
  const matRate = Math.max(0, parseFloat(document.getElementById("rc-mat-rate")?.value) || 15);

  // Reverse formulas
  const manDays = Math.ceil(q / pLabor);
  const dailyLabor = Math.max(1, Math.ceil(manDays / dur));

  const equipDays = Math.ceil(q / pEquip);
  const dailyEquip = Math.max(1, Math.ceil(equipDays / dur));

  const laborCost = dailyLabor * dur * 25; // 25만원/명/일
  const equipCost = dailyEquip * dur * 65; // 65만원/대/일
  const matCost = Math.round(q * 0.15 * matRate);
  const totalCost = laborCost + equipCost + matCost;

  lastCalculatedReverseRes = {
    labor: dailyLabor,
    equip: dailyEquip,
    mat: q,
    laborCost,
    equipCost,
    matCost,
    totalCost
  };

  // Update UI Result Cards
  const mdEl = document.getElementById("rc-res-mandays"); if (mdEl) mdEl.textContent = `${manDays} Man-Days`;
  const dlEl = document.getElementById("rc-res-daily-labor"); if (dlEl) dlEl.textContent = `${dailyLabor} 명/일`;
  const deEl = document.getElementById("rc-res-daily-equip"); if (deEl) deEl.textContent = `${dailyEquip} 대/일`;
  const tcEl = document.getElementById("rc-res-totalcost"); if (tcEl) tcEl.textContent = `${totalCost.toLocaleString()} 만원`;
}

function applyReverseResourceToActivity() {
  const select = document.getElementById("rc-select-activity");
  if (!select || !window.RAW_ACTIVITIES || !lastCalculatedReverseRes) return;

  const idx = parseInt(select.value) || 0;
  const act = RAW_ACTIVITIES[idx];
  if (act) {
    act.resource = {
      labor: lastCalculatedReverseRes.labor,
      equip: lastCalculatedReverseRes.equip,
      mat: lastCalculatedReverseRes.mat,
      laborCost: lastCalculatedReverseRes.laborCost,
      equipCost: lastCalculatedReverseRes.equipCost,
      matCost: lastCalculatedReverseRes.matCost
    };
    act.totalCost = lastCalculatedReverseRes.totalCost;

    renderResourceModule();
    closeReverseCalcModal();
    alert(`✅ [${act.ades}] 액티비티에 역산된 소요자원(작업자 ${lastCalculatedReverseRes.labor}명/일, 장비 ${lastCalculatedReverseRes.equip}대/일)이 성공적으로 적용되었습니다!`);
  }
}
"""

script_end_idx = content.rfind('</script>')
if script_end_idx != -1:
    content = content[:script_end_idx] + "\n" + modal_js_code + "\n" + content[script_end_idx:]
    print("Injected Reverse Calculator JS Logic!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished integrating Reverse Resource Calculator into HTML!")
