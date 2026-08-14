import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern to clean renderNaverMapView function cleanly
pattern = r'function renderNaverMapView\(item\)\s*\{[\s\S]*?\n\} else if[\s\S]*?iframe\.src = openMapEmbedUrl;\s*\}\s*\}'

replacement = """function renderNaverMapView(item) {
  if (!item) return;

  const locTitle = document.getElementById("naver-map-location-title");
  const metaAddr = document.getElementById("naver-map-meta-addr");
  const iframe = document.getElementById("naver-map-iframe");
  const actionBtns = document.getElementById("naver-map-action-buttons");

  const lat = item.lat || 37.2024;
  const lng = item.lng || 127.0412;

  // 100% Accurate Naver Map WGS84 Coordinate URL (Zoom level 17)
  const naverDirectUrl = `https://map.naver.com/v5/?c=${lng},${lat},17,0,0,0,dh`;
  // Kakao Map Direct Coordinate Link
  const kakaoDirectUrl = `https://map.kakao.com/link/map/${encodeURIComponent(item.name)},${lat},${lng}`;

  if (locTitle) locTitle.textContent = `${item.name} 현장 정밀 GPS 위치 (${item.tool} #${item.no})`;
  if (metaAddr) metaAddr.innerHTML = `📍 <strong>정밀 GPS 좌표:</strong> 위도 ${lat}° N, 경도 ${lng}° E | <strong>체이닝:</strong> STA ${item.startSta}m ~ ${item.endSta}m`;

  if (actionBtns) {
    actionBtns.innerHTML = `
      <a href="${naverDirectUrl}" target="_blank" style="background: #03c75a; color: #ffffff; text-decoration: none; padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(3,199,90,0.3); transition: transform 0.15s ease;">
        <span>N</span> 네이버 지도 정밀 위치 보기 (새 탭)
      </a>
      <a href="${kakaoDirectUrl}" target="_blank" style="background: #fee500; color: #191919; text-decoration: none; padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(254,229,0,0.3); transition: transform 0.15s ease;">
        <span>💬</span> 카카오맵 위치 보기
      </a>
    `;
  }

  // High precision iframe embedding using exact Lat/Lng
  if (iframe) {
    const embedUrl = `https://maps.google.com/maps?q=${lat},${lng}&t=m&z=17&ie=UTF8&iwloc=&output=embed`;
    iframe.src = embedUrl;
  }
}"""

if re.search(pattern, text):
    text = re.sub(pattern, replacement, text, count=1)
    print("Cleaned up renderNaverMapView syntax successfully!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(text)
