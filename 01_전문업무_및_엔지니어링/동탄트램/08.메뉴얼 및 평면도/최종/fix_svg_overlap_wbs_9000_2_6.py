import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

gui_folder = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야\6_관제 및 운영사 인터페이스 협의\수행지침"

if not os.path.exists(gui_folder):
    print("❌ ERROR: Guideline folder for WBS 9000-2-6 not found!")
    sys.exit(1)

# Fixed SVG Step 3 Replacement HTML
old_svg_step3 = """<svg id="svg_step3" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                            <g transform="translate(15, 25)">
                                <rect x="0" y="0" width="240" height="60" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="6"/>
                                <text x="120" y="25" font-size="11" font-weight="black" fill="#1d4ed8" text-anchor="middle">📺 전광판 + 🔊 스피커 (0.5초)</text>
                                <text x="120" y="45" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">"열차 도착" 글자 & 안내방송 동시 표출</text>

                                <rect x="0" y="70" width="240" height="60" fill="#ffffff" stroke="#ef4444" stroke-width="2" rx="6"/>
                                <text x="120" y="95" font-size="11" font-weight="black" fill="#b91c1c" text-anchor="middle">🚨 승강장 비상 벨 (3초 관제연결)</text>
                                <text x="120" y="115" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">버튼 조작 시 3초 관제 벨 울림 & 통화</text>
                            </g>

                            <path d="M 265 90 L 295 90" stroke="#0891b2" stroke-width="3"/>
                            <polygon points="295,85 305,90 295,95" fill="#0891b2"/>

                            <rect x="315" y="25" width="190" height="130" fill="#ffffff" stroke="#0e7490" stroke-width="2" rx="8"/>
                            <text x="410" y="55" font-size="13" font-weight="black" fill="#0e7490" text-anchor="middle">🎧 OCC 종합관제 콘솔</text>
                            <text x="410" y="85" font-size="11" font-weight="bold" fill="#334155">• 위치 맵 0.5초 동시 갱신</text>
                            <text x="410" y="108" font-size="11" font-weight="bold" fill="#334155">• 비상 벨 3초 착신 소리 연결</text>
                            <text x="410" y="135" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">✔ 3중 통합 연동 합격</text>
                        </svg>"""

new_svg_step3 = """<svg id="svg_step3" viewBox="0 0 520 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
                            <rect x="0" y="0" width="520" height="180" fill="#f8fafc"/>
                            <g transform="translate(15, 25)">
                                <rect x="0" y="0" width="220" height="60" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="6"/>
                                <text x="110" y="25" font-size="11" font-weight="black" fill="#1d4ed8" text-anchor="middle">📺 전광판 + 🔊 스피커 (0.5초)</text>
                                <text x="110" y="45" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">"열차 도착" 글자 & 방송 동시 표출</text>

                                <rect x="0" y="70" width="220" height="60" fill="#ffffff" stroke="#ef4444" stroke-width="2" rx="6"/>
                                <text x="110" y="95" font-size="11" font-weight="black" fill="#b91c1c" text-anchor="middle">🚨 승강장 비상 벨 (3초 관제)</text>
                                <text x="110" y="115" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">버튼 조작 시 3초 관제 소리 연결</text>
                            </g>

                            <path d="M 242 90 L 255 90" stroke="#0891b2" stroke-width="3"/>
                            <polygon points="255,85 262,90 255,95" fill="#0891b2"/>

                            <rect x="265" y="25" width="240" height="130" fill="#ffffff" stroke="#0e7490" stroke-width="2" rx="8"/>
                            <text x="385" y="52" font-size="13" font-weight="black" fill="#0e7490" text-anchor="middle">🎧 OCC 종합관제 콘솔</text>
                            <text x="280" y="82" font-size="11" font-weight="bold" fill="#334155">• 위치 맵 0.5초 동시 갱신</text>
                            <text x="280" y="105" font-size="11" font-weight="bold" fill="#334155">• 비상 벨 3초 착신 소리 연결</text>
                            <text x="385" y="135" font-size="11" font-weight="black" fill="#15803d" text-anchor="middle">✔ 3중 통합 연동 합격</text>
                        </svg>"""

for fn in os.listdir(gui_folder):
    if fn.endswith('.html'):
        fp = os.path.join(gui_folder, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "svg_step3" in content:
            # Replace old svg_step3 with new expanded svg_step3
            if old_svg_step3 in content:
                content = content.replace(old_svg_step3, new_svg_step3)
            else:
                # Fallback string replace using substring
                start_idx = content.find('<svg id="svg_step3"')
                end_idx = content.find('</svg>', start_idx) + 6
                if start_idx != -1 and end_idx != -1:
                    content = content[:start_idx] + new_svg_step3 + content[end_idx:]
            
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✓ [FIXED SVG STEP 3 OVERLAP] Updated: {fn}")

print("\n🎉 SUCCESSFULLY FIXED SVG STEP 3 TEXT OVERLAP IN WBS 9000-2-6 GUIDELINE HTMLs!")
