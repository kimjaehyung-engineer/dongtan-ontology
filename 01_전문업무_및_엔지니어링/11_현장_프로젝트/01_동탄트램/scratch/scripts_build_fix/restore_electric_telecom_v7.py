import os, sys, shutil, zipfile

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종'

src_dir = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)')
v7_dir = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v7')

sectors_to_restore = ['전기분야', '통신분야']

print("=== Restoring Electric & Telecom sectors to v7 folder ===")

for sec in sectors_to_restore:
    s_path = os.path.join(src_dir, sec)
    d_path = os.path.join(v7_dir, sec)
    if os.path.exists(s_path):
        print(f"Copying '{sec}' from original master to v7...")
        if os.path.exists(d_path):
            shutil.rmtree(d_path)
        shutil.copytree(s_path, d_path)
        print(f"✓ Restored '{sec}' successfully!")

# Verify restored HTML file counts in v7
print("\n=== Verifying HTML counts in v7 after restoration ===")
for item in sorted(os.listdir(v7_dir)):
    sub_p = os.path.join(v7_dir, item)
    if os.path.isdir(sub_p):
        html_count = 0
        for r, d, files in os.walk(sub_p):
            for f in files:
                if f.endswith('.html') or f.endswith('.htm'):
                    html_count += 1
        print(f"  Folder '{item}': {html_count} HTML files")

# Create v7 ZIP Archive containing Excel & Attachment folder
excel_v7 = os.path.join(base_dir, '매뉴얼 BODY (집행단계)v7.xlsm')
zip_v7_path = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v7.zip')

print(f"\nCreating ZIP Archive: {zip_v7_path}...")
with zipfile.ZipFile(zip_v7_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add Excel file if exists
    if os.path.exists(excel_v7):
        zf.write(excel_v7, os.path.basename(excel_v7))
        print(f"  + Added Excel: {os.path.basename(excel_v7)}")
    
    # Add v7 attachment folder
    for root, dirs, files in os.walk(v7_dir):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, base_dir)
            zf.write(full_p, rel_p)

print("✓ Successfully created v7 ZIP archive!")
