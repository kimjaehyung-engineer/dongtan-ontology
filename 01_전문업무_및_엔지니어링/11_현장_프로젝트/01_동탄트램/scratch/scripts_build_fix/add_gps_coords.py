import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Helper function to estimate GPS lat/lng based on station and chainage (STA)
def get_estimated_gps(item):
    name = item.get('name', '')
    tool = item.get('tool', '')
    sta = item.get('startSta', 0)

    # 1공구 (Byeongjeom -> Dongtan Station -> Lake Park)
    if tool == '1공구':
        if sta < 1000: # Byeongjeom Area
            # Byeongjeom Station ~ IPARK
            t = (sta - 128.8) / (871.9 - 128.8)
            lat = 37.2078 - t * 0.0054
            lng = 127.0335 + t * 0.0077
        elif sta < 3000: # Seodongtan
            t = (sta - 1000) / 2000.0
            lat = 37.2024 + t * 0.0020
            lng = 127.0412 + t * 0.0200
        elif sta < 6000: # Central Park / Metapolis
            t = (sta - 3000) / 3000.0
            lat = 37.2044 - t * 0.0080
            lng = 127.0612 + t * 0.0200
        elif sta < 9000: # Naru Village -> Dongtan Station
            t = (sta - 6000) / 3000.0
            lat = 37.1964 + t * 0.0030
            lng = 127.0812 + t * 0.0150
        elif sta < 12000: # Techno Valley
            t = (sta - 9000) / 3000.0
            lat = 37.1994 + t * 0.0150
            lng = 127.0962 + t * 0.0100
        elif sta < 15000: # Mokdong / Shinri
            t = (sta - 12000) / 3000.0
            lat = 37.2144 - t * 0.0200
            lng = 127.1062 + t * 0.0150
        else: # Lake Park / Jangji
            t = (sta - 15000) / 3000.0
            lat = 37.1944 - t * 0.0250
            lng = 127.1212 - t * 0.0200
    else:
        # 2공구 (Mangpo -> Banwol -> Dongtan Station -> Osan)
        if sta < 2000: # Mangpo / Taejang
            t = sta / 2000.0
            lat = 37.2450 - t * 0.0150
            lng = 127.0550 + t * 0.0100
        elif sta < 5000: # Banwol / Samsung DSR / Hanlim Hospital
            t = (sta - 2000) / 3000.0
            lat = 37.2300 - t * 0.0220
            lng = 127.0650 + t * 0.0180
        elif sta < 8000: # Dongtan Station / Yeongcheon
            t = (sta - 5000) / 3000.0
            lat = 37.2080 - t * 0.0100
            lng = 127.0830 + t * 0.0130
        else: # Lake Park (North/South) -> Osan Border
            t = (sta - 8000) / 6000.0
            lat = 37.1980 - t * 0.0320
            lng = 127.0960 + t * 0.0050

    return round(lat, 5), round(lng, 5)

m = re.search(r'const intersectionData = (\[[\s\S]*?\]);', text)
if m:
    data = json.loads(m.group(1))
    for item in data:
        lat, lng = get_estimated_gps(item)
        item['lat'] = lat
        item['lng'] = lng

    new_data_json = json.dumps(data, ensure_ascii=False)
    text = text[:m.start(1)] + new_data_json + text[m.end(1):]
    print("Successfully mapped lat/lng to all items in intersectionData!")

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated V1 HTML with GPS coordinates!")
else:
    print("Could not match intersectionData!")
