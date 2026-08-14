import os, sys, shutil, zipfile

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종'

v6_dir = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v6')
v7_dir = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v7')

excel_v7 = os.path.join(base_dir, '매뉴얼 BODY (집행단계)v7.xlsm')

print("1. Ensuring folder v7 exists...")
if not os.path.exists(v7_dir):
    shutil.copytree(v6_dir, v7_dir)
print(f"✓ Verified folder: {v7_dir}")

print("\n2. Updating hyperlinks inside Excel (v6 -> v7)...")
temp_excel = os.path.join(base_dir, '매뉴얼 BODY (집행단계)v7_temp.xlsm')

with zipfile.ZipFile(excel_v7, 'r') as zin, zipfile.ZipFile(temp_excel, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
            text = buffer.decode('utf-8', errors='ignore')
            if '매뉴얼BODY(집행단계-첨부폴더)v6' in text:
                text = text.replace('매뉴얼BODY(집행단계-첨부폴더)v6', '매뉴얼BODY(집행단계-첨부폴더)v7')
                buffer = text.encode('utf-8')
        zout.writestr(item, buffer)

try:
    os.replace(temp_excel, excel_v7)
    excel_final = excel_v7
    print("✓ Successfully updated original Excel file hyperlinks!")
except Exception as e:
    excel_final = temp_excel
    print(f"!! Original Excel is currently open in MS Excel. Using updated temp copy for ZIP: {e}")

print("\n3. Creating ZIP archive: 매뉴얼 BODY (집행단계)v7.zip ...")
zip_path = os.path.join(base_dir, '매뉴얼 BODY (집행단계)v7.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    # Add Excel file with standard v7 filename in ZIP
    z.write(excel_final, arcname='매뉴얼 BODY (집행단계)v7.xlsm')
    # Add v7 folder recursively
    for root, dirs, files in os.walk(v7_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_dir)
            z.write(full_path, arcname=rel_path)

print(f"✓ Created ZIP package: {zip_path} ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")
