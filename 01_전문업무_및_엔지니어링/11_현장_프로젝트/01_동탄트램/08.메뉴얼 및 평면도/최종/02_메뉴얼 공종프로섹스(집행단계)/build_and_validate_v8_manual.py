# -*- coding: utf-8 -*-
import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)"
v6_path = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v6')
v6m_path = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v6(메일보냈던거)')
v7_path = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v7')
v8_path = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v8')

print('=== Starting v8 Build & Zero-Duplication Extraction ===', flush=True)

# Step 1: Create clean v8 directory
if os.path.exists(v8_path):
    print('Removing existing v8 folder for fresh build...', flush=True)
    shutil.rmtree(v8_path)
os.makedirs(v8_path, exist_ok=True)

# Copy master excel if exists in v7
v7_excel = os.path.join(v7_path, '매뉴얼 BODY (집행단계)v7.xlsm')
v8_excel = os.path.join(v8_path, '매뉴얼 BODY (집행단계)v8.xlsm')
if os.path.exists(v7_excel):
    shutil.copy2(v7_excel, v8_excel)
    print('Copied Master Excel to v8:', os.path.basename(v8_excel), flush=True)

# Gather all relative folder paths across v7, v6m, v6
all_folders = set()
for r_path in [v7_path, v6m_path, v6_path]:
    for root, dirs, files in os.walk(r_path):
        rel = os.path.relpath(root, r_path)
        if rel != '.':
            all_folders.add(rel)

print(f'Total unique folder paths scanned: {len(all_folders)}', flush=True)

copied_count = 0
multi_file_violations = []

def get_best_file(rel):
    # Check v7 -> v6m -> v6
    for v_name, v_root in [('v7', v7_path), ('v6m', v6m_path), ('v6', v6_path)]:
        fp = os.path.join(v_root, rel)
        if os.path.exists(fp):
            files = [f for f in os.listdir(fp) if not f.startswith('.') and not f.startswith('~$')]
            if not files:
                continue
            
            # Filter out exploded sub-files (...상세절차서.html)
            main_files = [f for f in files if not f.endswith('상세절차서.html')]
            cand_list = main_files if main_files else files
            
            # Find best file
            best_f = None
            best_score = (-1, -1, -1)
            for f in cand_list:
                full_f = os.path.join(fp, f)
                stat = os.stat(full_f)
                has_descriptive_name = 1 if len(f) > 15 and f not in ['수행지침.html', '체크리스트.html', '표준서.html'] else 0
                score = (has_descriptive_name, stat.st_size, stat.st_mtime)
                if score > best_score:
                    best_score = score
                    best_f = (full_f, f, v_name)
            if best_f:
                return best_f
    return None

for rel in sorted(all_folders):
    target_dir = os.path.join(v8_path, rel)
    os.makedirs(target_dir, exist_ok=True)
    
    bname = os.path.basename(rel)
    # If leaf document folder (수행지침, 체크리스트, 표준서)
    if bname in ['수행지침', '체크리스트', '표준서']:
        best = get_best_file(rel)
        if best:
            src_full_p, src_f, src_v = best
            
            # Determine standard target filename
            parent_dir_name = os.path.basename(os.path.dirname(rel))
            parts = parent_dir_name.split('_', 1)
            act_title = parts[1] if len(parts) > 1 and parts[0].isdigit() else parent_dir_name
            
            # Standard filename: [act_title]_[bname].html (e.g. 교통처리대책 협의 및 승인_수행지침.html)
            target_filename = f"{act_title}_{bname}.html" if f"{act_title}_{bname}.html" == src_f or src_f in ['수행지침.html', '체크리스트.html', '표준서.html'] else src_f
            
            dest_full_p = os.path.join(target_dir, target_filename)
            shutil.copy2(src_full_p, dest_full_p)
            copied_count += 1
    else:
        # Check non-document attachments (like PDFs)
        for v_root in [v7_path, v6m_path, v6_path]:
            fp = os.path.join(v_root, rel)
            if os.path.exists(fp):
                files = [f for f in os.listdir(fp) if not f.startswith('.') and not f.startswith('~$')]
                pdf_files = [f for f in files if f.lower().endswith('.pdf')]
                for pdf in pdf_files:
                    src_pdf = os.path.join(fp, pdf)
                    dest_pdf = os.path.join(target_dir, pdf)
                    if not os.path.exists(dest_pdf):
                        shutil.copy2(src_pdf, dest_pdf)

print(f'Successfully processed and copied {copied_count} primary HTML files into v8.')

# Step 2: Automated Validation
print('\n=== Starting Automated Validation of v8 ===')

leaf_doc_folders = 0
zero_dup_pass = 0
broken_file_count = 0

for root, dirs, files in os.walk(v8_path):
    rel = os.path.relpath(root, v8_path)
    bname = os.path.basename(rel)
    if bname in ['수행지침', '체크리스트', '표준서']:
        leaf_doc_folders += 1
        valid_files = [f for f in files if not f.startswith('.')]
        if len(valid_files) == 1:
            zero_dup_pass += 1
            fp = os.path.join(root, valid_files[0])
            if os.path.getsize(fp) < 100:
                broken_file_count += 1
        else:
            multi_file_violations.append((rel, valid_files))

print(f'Leaf Document Folders Checked: {leaf_doc_folders}')
print(f'1 Folder 1 File (Zero-Duplication) PASSED: {zero_dup_pass} / {leaf_doc_folders}')
print(f'Broken/Empty Files Count: {broken_file_count}')

if zero_dup_pass == leaf_doc_folders and broken_file_count == 0:
    print('\n✅ RESULT: 100% PERFECT SUCCESS! v8 build completed with zero duplication.')
else:
    print('\n⚠️ RESULT: Validation violations found:', len(multi_file_violations))
