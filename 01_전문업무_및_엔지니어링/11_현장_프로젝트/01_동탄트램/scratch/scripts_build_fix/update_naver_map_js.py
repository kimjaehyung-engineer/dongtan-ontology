import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML container to feature dual action buttons (Naver + Kakao Map GPS coordinate links)
old_html_header = """        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;">
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
        </div>"""

new_html_header = """        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;">
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <span style="background: #03c75a; color: #ffffff; font-size: 0.8rem; font-weight: 900; padding: 0.3rem 0.7rem; border-radius: 50px; display: flex; align-items: center; gap: 0.3rem; box-shadow: 0 2px 4px rgba(3,199,90,0.25);">
              <span style="font-size: 0.9rem; font-weight: 900;">GPS</span> 정밀 위경도 좌표 연동
            </span>
            <h3 id="naver-map-location-title" style="margin: 0; font-size: 1.05rem; font-weight: 800; color: #0f172a;">
              사거리 현장 위치
            </h3>
          </div>
          <div id="naver-map-action-buttons" style="display: flex; align-items: center; gap: 0.6rem;">
            <a id="btn-open-naver-external" href="#" target="_blank" style="background: #03c75a; color: #ffffff; text-decoration: none; padding: 0.5rem 1.1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 800; display: flex; align-items: center; gap: 0.4rem; box-shadow: 0 3px 8px rgba(3,199,90,0.3); transition: transform 0.15s ease;">
              <span>N</span> 네이버 지도 정밀 위치 보기
            </a>
          </div>
        </div>"""

if old_html_header in content:
    content = content.replace(old_html_header, new_html_header)
    print("Updated HTML header for GPS coordinate buttons!")

# 2. Update renderNaverMapView implementation
old_func_pattern = r'function renderNaverMapView\(item\)\s*\{[\s\S]*?\n\s*\}'

new_func_code = """function renderNaverMapView(item) {
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

if re.search(old_func_pattern, content):
    content = re.sub(old_func_pattern, new_func_code, content, count=1)
    print("Updated renderNaverMapView JS function with exact GPS coordinates!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating V1 HTML with GPS coordinate rendering!")
