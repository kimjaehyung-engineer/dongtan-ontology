import os
import re

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\strut_anchor 비교(v1)"
dist_dir = os.path.join(base_dir, "dist")
assets_dir = os.path.join(dist_dir, "assets")

index_html_path = os.path.join(dist_dir, "index.html")
with open(index_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# CSS 파일 찾아서 인라인 <style>로 치환
for fname in os.listdir(assets_dir):
    if fname.endswith(".css"):
        css_path = os.path.join(assets_dir, fname)
        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()
        # link 태그 치환
        pattern = rf'<link[^>]*href="[^"]*{re.escape(fname)}"[^>]*>'
        html_content = re.sub(pattern, lambda m: f'<style>\n{css_code}\n</style>', html_content)

# JS 파일 찾아서 인라인 <script>로 치환
for fname in os.listdir(assets_dir):
    if fname.endswith(".js"):
        js_path = os.path.join(assets_dir, fname)
        with open(js_path, "r", encoding="utf-8") as f:
            js_code = f.read()
        # script 태그 치환
        pattern = rf'<script[^>]*src="[^"]*{re.escape(fname)}"[^>]*></script>'
        html_content = re.sub(pattern, lambda m: f'<script type="module">\n{js_code}\n</script>', html_content)

out_file_path = os.path.join(base_dir, "가시설_Strut_Anchor_사전최적설계_v1.html")
with open(out_file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] Single standalone HTML created: {out_file_path} ({len(html_content)} bytes)")
