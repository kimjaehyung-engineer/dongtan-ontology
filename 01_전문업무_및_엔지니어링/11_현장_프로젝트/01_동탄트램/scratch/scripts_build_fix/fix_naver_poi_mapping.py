import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update renderNaverMapView JS implementation in content
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

  // Official Naver Map Search URL centered on Official POI Pin
  const naverSearchUrl = `https://map.naver.com/v5/search/${encodeURIComponent(searchQuery)}`;
  // Official Kakao Map Search URL
  const kakaoSearchUrl = `https://map.kakao.com/link/search/${encodeURIComponent(searchQuery)}`;

  if (locTitle) locTitle.textContent = `${name} 현장 공식 위치 (${item.tool} #${item.no})`;
  if (metaAddr) metaAddr.innerHTML = `📍 <strong>네이버 공식 검색 쿼리:</strong> ${searchQuery} | <strong>체이닝:</strong> STA ${item.startSta}m ~ ${item.endSta}m`;

  if (actionBtns) {
    actionBtns.innerHTML = `
      <a href="${naverSearchUrl}" target="_blank" style="background: #03c75a; color: #ffffff; text-decoration: none; padding: 0.5rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(3,199,90,0.3); transition: transform 0.15s ease;">
        <span>N</span> 네이버 지도 공식 핀 위치 보기 (새 탭)
      </a>
      <a href="${kakaoSearchUrl}" target="_blank" style="background: #fee500; color: #191919; text-decoration: none; padding: 0.5rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(254,229,0,0.3); transition: transform 0.15s ease;">
        <span>💬</span> 카카오맵 공식 핀 보기
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
    print("Updated renderNaverMapView with Official POI Query Search Engine!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying Naver Map Official POI Search engine to V1 HTML!")
