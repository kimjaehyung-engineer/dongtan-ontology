import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298"
gui_folder = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야\7_발주처 품질 요구사항 검토\수행지침"

img_map = {
    "telecom_materials_cctv_1785117831508.jpg": "telecom_materials_cctv.jpg",
    "otdr_power_meter_1785117806286.jpg": "otdr_power_meter.jpg",
    "spectrum_analyzer_lter_1785117819856.jpg": "spectrum_analyzer_lter.jpg"
}

# Copy images to target guideline folder
for orig_name, target_name in img_map.items():
    src_p = os.path.join(artifact_dir, orig_name)
    dst_p = os.path.join(gui_folder, target_name)
    if os.path.exists(src_p):
        shutil.copy(src_p, dst_p)
        print(f"   ✓ [IMAGE COPIED] {target_name} -> {gui_folder}")

# HTML Image insertion blocks
step1_img_html = """
                    <!-- 📸 STEP 1 실제 장비 사진 (광케이블, 4K CCTV, PIS/PA, LTE-R 안테나) -->
                    <div class="mt-4 bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <span class="text-xs font-bold text-blue-900 block mb-2">📸 실무 자재 사진: 72-Core 광케이블, 4K IP CCTV, PIS전광판, LTE-R 안테나</span>
                        <img src="./telecom_materials_cctv.jpg" alt="주요 통신 자재 실물 사진" class="w-full h-48 object-cover rounded-lg border border-slate-300 shadow-sm cursor-pointer" onclick="openDiagramZoom('img_step1_tag', 'STEP 1 주요 통신 자재 현장 사진')">
                        <img id="img_step1_tag" src="./telecom_materials_cctv.jpg" alt="주요 통신 자재" class="hidden">
                    </div>
"""

step2_img_html = """
                    <!-- 📸 STEP 2 실제 장비 사진 (OTDR 광파동 측정기 & 광파워미터) -->
                    <div class="mt-4 bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <span class="text-xs font-bold text-indigo-900 block mb-2">📸 실무 측정 장비 사진: OTDR(광파동 측정기) 및 광파워미터(1310/1550nm)</span>
                        <img src="./otdr_power_meter.jpg" alt="OTDR 및 광파워미터 측정 장비 실물 사진" class="w-full h-48 object-cover rounded-lg border border-slate-300 shadow-sm cursor-pointer" onclick="openDiagramZoom('img_step2_tag', 'STEP 2 OTDR 및 광파워미터 측정 장비 현장 사진')">
                        <img id="img_step2_tag" src="./otdr_power_meter.jpg" alt="OTDR 측정 장비" class="hidden">
                    </div>
"""

step3_img_html = """
                    <!-- 📸 STEP 3 실제 장비 사진 (LTE-R 전파 스펙트럼 분석기) -->
                    <div class="mt-4 bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <span class="text-xs font-bold text-cyan-900 block mb-2">📸 실무 측정 장비 사진: LTE-R 무선망 전파 측정 장비(스펙트럼 분석기)</span>
                        <img src="./spectrum_analyzer_lter.jpg" alt="LTE-R 스펙트럼 분석기 실물 사진" class="w-full h-48 object-cover rounded-lg border border-slate-300 shadow-sm cursor-pointer" onclick="openDiagramZoom('img_step3_tag', 'STEP 3 LTE-R 무선망 스펙트럼 분석기 현장 사진')">
                        <img id="img_step3_tag" src="./spectrum_analyzer_lter.jpg" alt="스펙트럼 분석기" class="hidden">
                    </div>
"""

for fn in os.listdir(gui_folder):
    if fn.endswith('.html'):
        fp = os.path.join(gui_folder, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject images into Step 1, Step 2, Step 3 cards if not present
        if "telecom_materials_cctv.jpg" not in content:
            content = content.replace("</div>\n                    \n                    <div class=\"clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3\" onclick=\"openDiagramZoom('svg_step1'", f"{step1_img_html}\n</div>\n                    \n                    <div class=\"clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3\" onclick=\"openDiagramZoom('svg_step1'")
        
        if "otdr_power_meter.jpg" not in content:
            content = content.replace("</div>\n\n                    <div class=\"clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3\" onclick=\"openDiagramZoom('svg_step2'", f"{step2_img_html}\n</div>\n\n                    <div class=\"clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3\" onclick=\"openDiagramZoom('svg_step2'")

        if "spectrum_analyzer_lter.jpg" not in content:
            content = content.replace("</div>\n\n                    <div class=\"clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3\" onclick=\"openDiagramZoom('svg_step3'", f"{step3_img_html}\n</div>\n\n                    <div class=\"clickable-diagram bg-slate-50 p-4 rounded-xl border border-slate-200 mt-3\" onclick=\"openDiagramZoom('svg_step3'")

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✓ [HTML IMAGE INJECTED] Guideline -> {fn}")

print("\n🎉 SUCCESSFULLY GENERATED AND INJECTED TELECOM EQUIPMENT IMAGES INTO WBS 9000-2-7 GUIDELINE HTMLs!")
