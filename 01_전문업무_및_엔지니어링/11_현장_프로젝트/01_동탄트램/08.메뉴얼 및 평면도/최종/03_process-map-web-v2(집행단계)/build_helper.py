import os
import glob
import zipfile
import subprocess
import shutil

app_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\02_process-map-web-v2"
cache_base = r"C:\Users\sskjh\AppData\Local\electron\Cache"
dist_custom = r"C:\Users\sskjh\.electron-dist-custom"
release_dir = os.path.join(app_dir, "release")

# Find zip file in cache
zip_files = glob.glob(os.path.join(cache_base, "**", "electron-*.zip"), recursive=True)
if not zip_files:
    print("No electron zip found in cache!")
else:
    cache_zip = zip_files[0]
    print("Found electron zip:", cache_zip)

    if os.path.exists(release_dir):
        try:
            shutil.rmtree(release_dir)
        except Exception as e:
            print("rmtree release warning:", e)

    os.makedirs(dist_custom, exist_ok=True)
    print("Extracting electron zip to custom dir...")
    with zipfile.ZipFile(cache_zip, "r") as zip_ref:
        zip_ref.extractall(dist_custom)
    print("Extracted successfully!")

cmd = f'npx electron-builder --win portable --config.electronDist="{dist_custom}"'
print("Executing command:", cmd)
res = subprocess.run(cmd, shell=True, cwd=app_dir)
print("Build finished with exit code:", res.returncode)
