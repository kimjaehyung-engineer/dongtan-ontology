import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update renderNaverMapView implementation to feature traffic=on & Kakao map_type=TRAFFIC
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

  const lat = item.lat || 37.2024;
  const lng = item.lng || 127.0412;

  // 1. Naver Live Traffic Layer Enabled URL (traffic=on)
  const naverTrafficUrl = `https://map.naver.com/v5/?c=${lng},${lat},15,0,0,0,dh&traffic=on`;
  const naverSearchTrafficUrl = `https://map.naver.com/p/search/${encodeURIComponent(searchQuery)}?c=${lng},${lat},15,0,0,0,dh&traffic=on`;
  
  // 2. Kakao Map Direct Traffic Congestion Layer URL (map_type=TRAFFIC - 100% Live Red/Yellow/Green Lines)
  const kakaoTrafficUrl = `https://map.kakao.com/?map_type=TRAFFIC&q=${encodeURIComponent(searchQuery)}`;
  
  // 3. UTIC National Traffic Information Center Live Traffic & CCTV URL
  const uticUrl = `https://www.utic.go.kr/map/map.do?searchKeyword=${encodeURIComponent(searchQuery)}`;

  if (locTitle) locTitle.textContent = `${name} 실시간 교통상황 & 위치 (${item.tool} #${item.no})`;
  if (metaAddr) metaAddr.innerHTML = `📍 <strong>실시간 연동:</strong> ${searchQuery} | 🚦 <strong>실시간 도로 소통:</strong> 초록(원활) / 노랑(서행) / 빨강(정체) | ⏱️ STA ${item.startSta}m ~ ${item.endSta}m`;

  if (actionBtns) {
    actionBtns.innerHTML = `
      <a href="${naverTrafficUrl}" target="_blank" style="background: #03c75a; color: #ffffff; text-decoration: none; padding: 0.55rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(3,199,90,0.3); transition: transform 0.15s ease;">
        <span>🚦</span> 네이버 실시간 교통지도 (traffic=on)
      </a>
      <a href="${kakaoTrafficUrl}" target="_blank" style="background: #fee500; color: #191919; text-decoration: none; padding: 0.55rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(254,229,0,0.3); transition: transform 0.15s ease;">
        <span>💬</span> 카카오맵 실시간 혼잡도 (Traffic ON)
      </a>
      <a href="${uticUrl}" target="_blank" style="background: #0284c7; color: #ffffff; text-decoration: none; padding: 0.55rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(2,132,199,0.3); transition: transform 0.15s ease;">
        <span>📡</span> 국가교통정보센터(UTIC) CCTV
      </a>
    `;
  }

  // Google Maps iframe embed using official POI query
  if (iframe) {
    const embedUrl = `https://maps.google.com/maps?q=${encodeURIComponent(searchQuery)}&t=m&z=16&ie=UTF8&iwloc=&output=embed`;
    iframe.src = embedUrl;
  }
}"""

if re.search(old_func_pattern, content):
    content = re.sub(old_func_pattern, lambda m: new_func_code, content, count=1)
    print("Updated renderNaverMapView with traffic=on & Kakao map_type=TRAFFIC!")

# Update tip text inside modal-naver-map-container
old_tip = r'<span style="color: #0284c7; font-weight: 700;">💡 팁:[\s\S]*?</span>'
new_tip = '<span style="color: #0284c7; font-weight: 700;">💡 팁: 네이버 지도 화면 우측 상단 [레이어 아이콘 🥞] ➔ [교통정보] 버튼을 누르시면 실시간 도로 혼잡 색상(초록/노랑/빨강)이 온/오프됩니다. (카카오맵 버튼 클릭 시 100% 즉시 활성화)</span>'

if re.search(old_tip, content):
    content = re.sub(old_tip, new_tip, content, count=1)
    print("Updated Naver Map Layer Usage Tip Box!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying traffic=on fix to V1 HTML!")
