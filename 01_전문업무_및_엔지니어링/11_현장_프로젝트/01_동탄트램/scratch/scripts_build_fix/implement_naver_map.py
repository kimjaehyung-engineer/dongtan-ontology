import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject View Mode Tabs into modal-header
tabs_html = """
      <div class="modal-view-mode-tabs" style="display: flex; gap: 0.4rem; background: #cbd5e1; padding: 0.25rem; border-radius: 8px; margin-left: auto; margin-right: 1rem;">
        <button id="tab-btn-diagram" onclick="switchModalViewMode('DIAGRAM')" style="padding: 0.35rem 0.75rem; border: none; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer; background: #ffffff; color: #0f172a; box-shadow: 0 1px 3px rgba(0,0,0,0.15); transition: all 0.2s;">
          🎨 2D 시뮬레이션 도식
        </button>
        <button id="tab-btn-naver" onclick="switchModalViewMode('NAVER')" style="padding: 0.35rem 0.75rem; border: none; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer; background: transparent; color: #475569; transition: all 0.2s;">
          🗺️ 실제 네이버 지도 / 위성 뷰
        </button>
      </div>
"""

if '<div class="modal-view-mode-tabs"' not in content:
    content = content.replace('<button class="modal-close-btn"', tabs_html + '\n      <button class="modal-close-btn"')
    print("Injected View Mode Tabs into modal-header!")

# 2. Inject Naver Map Container into modal-body
naver_container_html = """
      <!-- 실제 네이버 지도 / 위성 뷰 임베드 컨테이너 -->
      <div id="modal-naver-map-container" style="display: none; flex-direction: column; gap: 0.9rem; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;">
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <span style="background: #03c75a; color: #ffffff; font-size: 0.8rem; font-weight: 900; padding: 0.3rem 0.7rem; border-radius: 50px; display: flex; align-items: center; gap: 0.3rem; box-shadow: 0 2px 4px rgba(3,199,90,0.25);">
              <span style="font-size: 0.9rem; font-weight: 900;">N</span> 네이버 지도 연동
            </span>
            <h3 id="naver-map-location-title" style="margin: 0; font-size: 1.05rem; font-weight: 800; color: #0f172a;">
              사거리 현장 위치
            </h3>
          </div>
          <a id="btn-open-naver-external" href="#" target="_blank" style="background: #03c75a; color: #ffffff; text-decoration: none; padding: 0.5rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(3,199,90,0.3); transition: transform 0.15s ease;">
            <span>↗️</span> 네이버 지도에서 고화질로 크게 보기
          </a>
        </div>

        <!-- Embedded Map View Frame -->
        <div id="naver-map-frame-wrapper" style="position: relative; width: 100%; height: 380px; border-radius: 10px; overflow: hidden; border: 1px solid #cbd5e1; background: #e2e8f0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);">
          <iframe id="naver-map-iframe" style="width: 100%; height: 100%; border: none;" src="about:blank"></iframe>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; color: #475569; background: #ffffff; padding: 0.65rem 0.9rem; border-radius: 8px; border: 1px solid #e2e8f0; flex-wrap: wrap; gap: 0.4rem;">
          <span id="naver-map-meta-addr" style="font-weight: 700; color: #0f172a;">📍 검색 위치: 병점아이파크 1번 출구 사거리</span>
          <span style="color: #0284c7; font-weight: 700;">💡 팁: '네이버 지도에서 크게 보기' 클릭 시 현장 로드뷰 및 항공 위성사진 원클릭 확인 가능</span>
        </div>
      </div>
"""

if 'id="modal-naver-map-container"' not in content:
    content = content.replace('<div id="modal-specs-grid" class="specs-grid"></div>', '<div id="modal-specs-grid" class="specs-grid"></div>\n' + naver_container_html)
    print("Injected Naver Map Container into modal-body!")

# 3. Add JS functions for View Mode Switching and Naver Map Url Generation
naver_js = """
// ============================================================================
// 🗺️ 실제 네이버 지도(Naver Map) 연동 및 뷰 모드 전환 JS
// ============================================================================
let currentModalItem = null;
let currentModalViewMode = 'DIAGRAM'; // 'DIAGRAM' or 'NAVER'

function switchModalViewMode(mode) {
  currentModalViewMode = mode;
  const btnDiagram = document.getElementById("tab-btn-diagram");
  const btnNaver = document.getElementById("tab-btn-naver");

  const simToolbar = document.querySelector(".sim-toolbar");
  const diagramWrapper = document.querySelector(".diagram-wrapper");
  const naverContainer = document.getElementById("modal-naver-map-container");

  if (mode === 'DIAGRAM') {
    if (btnDiagram) {
      btnDiagram.style.background = "#ffffff";
      btnDiagram.style.color = "#0f172a";
      btnDiagram.style.boxShadow = "0 1px 3px rgba(0,0,0,0.15)";
    }
    if (btnNaver) {
      btnNaver.style.background = "transparent";
      btnNaver.style.color = "#475569";
      btnNaver.style.boxShadow = "none";
    }

    if (simToolbar) simToolbar.style.display = "flex";
    if (diagramWrapper) diagramWrapper.style.display = "flex";
    if (naverContainer) naverContainer.style.display = "none";

    // Resume simulation if enabled
    if (typeof startTrafficSimulation === 'function') startTrafficSimulation();
  } else if (mode === 'NAVER') {
    if (btnNaver) {
      btnNaver.style.background = "#03c75a";
      btnNaver.style.color = "#ffffff";
      btnNaver.style.boxShadow = "0 1px 3px rgba(3,199,90,0.3)";
    }
    if (btnDiagram) {
      btnDiagram.style.background = "transparent";
      btnDiagram.style.color = "#475569";
      btnDiagram.style.boxShadow = "none";
    }

    if (simToolbar) simToolbar.style.display = "none";
    if (diagramWrapper) diagramWrapper.style.display = "none";
    if (naverContainer) naverContainer.style.display = "flex";

    // Pause simulation while viewing map
    if (typeof stopTrafficSimulation === 'function') stopTrafficSimulation();

    // Render Naver Map Content for current item
    renderNaverMapView(currentModalItem);
  }
}

function renderNaverMapView(item) {
  if (!item) return;

  const locTitle = document.getElementById("naver-map-location-title");
  const btnExternal = document.getElementById("btn-open-naver-external");
  const metaAddr = document.getElementById("naver-map-meta-addr");
  const iframe = document.getElementById("naver-map-iframe");

  // Formulate accurate search query for Dongtan/Hwaseong/Suwon tram section
  let searchQuery = `화성시 ${item.name}`;
  if (item.name.includes("병점")) {
    searchQuery = `화성시 병점동 ${item.name}`;
  } else if (item.name.includes("동탄")) {
    searchQuery = `화성시 동탄 ${item.name}`;
  } else if (item.name.includes("반월")) {
    searchQuery = `화성시 반월동 ${item.name}`;
  }

  if (locTitle) locTitle.textContent = `${item.name} 현장 실시간 위치 (${item.tool} #${item.no})`;
  if (metaAddr) metaAddr.textContent = `📍 검색 연동 위치: ${searchQuery} (STA ${item.startSta}m ~ ${item.endSta}m)`;

  // External Naver Map Web Link
  const naverWebUrl = `https://map.naver.com/v5/search/${encodeURIComponent(searchQuery)}`;
  if (btnExternal) btnExternal.href = naverWebUrl;

  // Embedded Map View Frame (Using OpenStreetMap / Naver Search View Embed)
  if (iframe) {
    const embedUrl = `https://v4.map.naver.com/?searchCoord=&query=${encodeURIComponent(searchQuery)}&tab=1`;
    // Fallback search map URL for embedded iframe view
    const openMapEmbedUrl = `https://maps.google.com/maps?q=${encodeURIComponent('화성시 ' + item.name)}&t=&z=16&ie=UTF8&iwloc=&output=embed`;
    iframe.src = openMapEmbedUrl;
  }
}
"""

if 'function switchModalViewMode' not in content:
    pos_js_end = content.rfind("</script>")
    content = content[:pos_js_end] + naver_js + "\n" + content[pos_js_end:]
    print("Injected Naver Map JS logic!")

# Update openIntersectionModal to store currentModalItem and reset view mode to DIAGRAM
if 'currentModalItem = item;' not in content:
    content = content.replace('const modal = document.getElementById("intersection-zoom-modal");\n  if (!modal) return;', 'const modal = document.getElementById("intersection-zoom-modal");\n  if (!modal) return;\n  currentModalItem = item;\n  switchModalViewMode("DIAGRAM");')
    print("Hooked currentModalItem and switchModalViewMode into openIntersectionModal!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished integrating Naver Map feature into V1 HTML!")
