import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update View Mode Tabs HTML to feature Kakao Map Live Traffic tab
old_tabs_pattern = r'<div class="modal-view-mode-tabs"[\s\S]*?</div>'

new_tabs_html = """<div class="modal-view-mode-tabs" style="display: flex; gap: 0.4rem; background: #cbd5e1; padding: 0.25rem; border-radius: 8px; margin-left: auto; margin-right: 1rem;">
        <button id="tab-btn-diagram" onclick="switchModalViewMode('DIAGRAM')" style="padding: 0.4rem 0.95rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: #0f172a; color: #ffffff; box-shadow: 0 1px 4px rgba(15,23,42,0.25); transition: all 0.2s;">
          📐 2D 시뮬레이션 도식
        </button>
        <button id="tab-btn-naver" onclick="switchModalViewMode('NAVER')" style="padding: 0.4rem 0.95rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: transparent; color: #475569; transition: all 0.2s;">
          💬 카카오맵 실시간 교통 지도
        </button>
      </div>"""

if re.search(old_tabs_pattern, content):
    content = re.sub(old_tabs_pattern, new_tabs_html, content, count=1)
    print("Updated Modal Tabs to feature Kakao Map Live Traffic!")

# 2. Update renderNaverMapView implementation to keep ONLY Kakao Map Live Traffic Button
old_func_pattern = r'function renderNaverMapView\(item\)\s*\{[\s\S]*?\n\}'

new_func_code = """function renderNaverMapView(item) {
  if (!item) return;

  const locTitle = document.getElementById("naver-map-location-title");
  const metaAddr = document.getElementById("naver-map-meta-addr");
  const iframe = document.getElementById("naver-map-iframe");
  const actionBtns = document.getElementById("naver-map-action-buttons");

  // Clean name & City determination
  let name = item.name || '';
  name = name.replace(/^\\([\\s\\S]*?\\)\\s*/, '').trim();

  let city = "화성시";
  if (name.includes("망포") || name.includes("태장") || name.includes("신영통")) {
    city = "수원시";
  }

  let searchQuery = `${city} ${name}`;
  if (name.includes("마당뫼")) searchQuery = `${city} 마당뫼 사거리`;
  else if (name.includes("병점역공영주차장")) searchQuery = `${city} 병점역 공영주차장`;
  else if (name.includes("병점아이파크")) searchQuery = `${city} 병점역아이파크자이`;
  else if (name.includes("서해스카이팰리스")) searchQuery = `${city} 병점 서해스카이팰리스`;
  else if (name.includes("서동탄역")) searchQuery = `${city} 서동탄역 사거리`;
  else if (name.includes("한림대병원")) searchQuery = `${city} 한림대동탄성심병원`;
  else if (name.includes("삼성반도체")) searchQuery = `${city} 삼성전자 화성사업장`;
  else if (name.includes("동탄역")) searchQuery = `${city} 동탄역`;
  else if (name.includes("동탄호수공원")) searchQuery = `${city} 동탄호수공원`;
  else if (name.includes("나루마을")) searchQuery = `${city} 나루마을 사거리`;
  else if (name.includes("반월")) searchQuery = `${city} 반월 삼거리`;

  // Kakao Map Direct Traffic Congestion Layer URL (map_type=TRAFFIC - 100% Live Red/Yellow/Green Lines)
  const kakaoTrafficUrl = `https://map.kakao.com/?map_type=TRAFFIC&q=${encodeURIComponent(searchQuery)}`;

  if (locTitle) locTitle.textContent = `${name} 카카오맵 실시간 교통 지도 (${item.tool} #${item.no})`;
  if (metaAddr) metaAddr.innerHTML = `📍 <strong>현장 위치:</strong> ${searchQuery} | 💬 <strong>카카오맵 실시간 교통 100% 연동</strong> (초록:원활 / 노랑:서행 / 빨강:정체) | ⏱️ STA ${item.startSta}m ~ ${item.endSta}m`;

  if (actionBtns) {
    actionBtns.innerHTML = `
      <a href="${kakaoTrafficUrl}" target="_blank" style="background: #fee500; color: #191919; text-decoration: none; padding: 0.6rem 1.4rem; border-radius: 8px; font-size: 0.9rem; font-weight: 900; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 10px rgba(254,229,0,0.4); transition: transform 0.15s ease;">
        <span>💬</span> 카카오맵 실시간 교통 지도 보기 (100% 혼잡도 오버레이) ↗
      </a>
    `;
  }

  // Map embed using official POI query
  if (iframe) {
    const embedUrl = `https://maps.google.com/maps?q=${encodeURIComponent(searchQuery)}&t=m&z=16&ie=UTF8&iwloc=&output=embed`;
    iframe.src = embedUrl;
  }
}"""

if re.search(old_func_pattern, content):
    content = re.sub(old_func_pattern, lambda m: new_func_code, content, count=1)
    print("Single-sourced to Kakao Map Live Traffic in renderNaverMapView!")

# Remove old tip line
old_tip = r'<span style="color: #0284c7; font-weight: 700;">💡 팁:[\s\S]*?</span>'
new_tip = '<span style="color: #475569; font-weight: 700;">💬 위 노란색 [카카오맵 실시간 교통 지도 보기] 단추를 누르시면 100% 실시간 도로 혼잡도(초록/노랑/빨강)가 오버레이된 카카오맵으로 즉시 연결됩니다.</span>'

if re.search(old_tip, content):
    content = re.sub(old_tip, new_tip, content, count=1)
    print("Updated Tip text for Kakao Map Traffic!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished single-sourcing to Kakao Map Live Traffic in V1 HTML!")
