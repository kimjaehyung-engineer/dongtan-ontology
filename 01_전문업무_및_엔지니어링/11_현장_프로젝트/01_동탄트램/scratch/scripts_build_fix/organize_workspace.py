import os
import shutil

BASE_DIR = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램"

def main():
    print("=== Starting Workspace Cleanup & Reorganization ===")

    # 1. Remove typo folder "08.메뉴얼 및 평ment도"
    typo_dir = os.path.join(BASE_DIR, "08.메뉴얼 및 평ment도")
    if os.path.exists(typo_dir):
        try:
            print(f"Removing typo directory: {typo_dir}")
            shutil.rmtree(typo_dir)
        except Exception as e:
            print(f"Skipping typo dir remove due to lock: {e}")

    # 2. Try renaming Top-level directories for consistency if not locked
    renames = [
        ("07 기본설계 추진방향보고", "07_기본설계_추진방향보고"),
        ("08.메뉴얼 및 평면도", "08_메뉴얼_및_평면도"),
        ("09.공정표", "09_공정표")
    ]
    actual_manual_dir_name = "08.메뉴얼 및 평면도"
    for old_name, new_name in renames:
        old_path = os.path.join(BASE_DIR, old_name)
        new_path = os.path.join(BASE_DIR, new_name)
        if os.path.exists(old_path) and not os.path.exists(new_path):
            try:
                print(f"Renaming directory: {old_name} -> {new_name}")
                os.rename(old_path, new_path)
                if old_name == "08.메뉴얼 및 평면도":
                    actual_manual_dir_name = new_name
            except Exception as e:
                print(f"Could not rename {old_name} (folder locked): {e}")

    if os.path.exists(os.path.join(BASE_DIR, "08_메뉴얼_및_평면도")):
        actual_manual_dir_name = "08_메뉴얼_및_평면도"

    manual_dir = os.path.join(BASE_DIR, actual_manual_dir_name)
    report_dir = os.path.join(BASE_DIR, "03_보고서_및_출력")
    scratch_dir = os.path.join(BASE_DIR, "scratch")

    # Ensure scratch exists
    os.makedirs(scratch_dir, exist_ok=True)

    # 3. Move root clutter files
    root_svg = os.path.join(BASE_DIR, "system_duct_cross_section_simple.svg")
    if os.path.exists(root_svg):
        print(f"Moving system_duct_cross_section_simple.svg to {manual_dir}")
        shutil.move(root_svg, os.path.join(manual_dir, "system_duct_cross_section_simple.svg"))

    root_excel = os.path.join(BASE_DIR, "동탄트램_기본설계_정합성_검토보고서.xlsx")
    if os.path.exists(root_excel):
        print(f"Moving 동탄트램_기본설계_정합성_검토보고서.xlsx to {report_dir}")
        shutil.move(root_excel, os.path.join(report_dir, "동탄트램_기본설계_정합성_검토보고서.xlsx"))

    # 4. Clean up inside manual_dir
    # Move temp scripts to scratch/
    temp_scripts = ["fix.py", "inspect_html.py", "scratch.js"]
    for ts in temp_scripts:
        src = os.path.join(manual_dir, ts)
        if os.path.exists(src):
            print(f"Moving {ts} to scratch")
            shutil.move(src, os.path.join(scratch_dir, ts))

    # Create scratch/backups directory
    backups_dir = os.path.join(scratch_dir, "backups")
    os.makedirs(backups_dir, exist_ok=True)

    # Move backup files in manual_dir
    manual_backups = [
        "동탄트램_업무_매뉴얼_backup.html",
        "track_types_comparison_detail_backup.png",
        "동탄트램_업무_매뉴얼v1.html"
    ]
    for mb in manual_backups:
        src = os.path.join(manual_dir, mb)
        if os.path.exists(src):
            print(f"Moving manual backup {mb} to scratch/backups")
            shutil.move(src, os.path.join(backups_dir, mb))

    # 5. Categorize files inside scratch/
    inspect_dir = os.path.join(scratch_dir, "scripts_inspect")
    build_fix_dir = os.path.join(scratch_dir, "scripts_build_fix")
    json_dir = os.path.join(scratch_dir, "data_json")
    temp_ui_dir = os.path.join(scratch_dir, "temp_js_html")

    for d in [inspect_dir, build_fix_dir, json_dir, temp_ui_dir]:
        os.makedirs(d, exist_ok=True)

    inspect_prefixes = (
        "inspect_", "check_", "find_", "diagnose_", "scan_", 
        "search_", "verify_", "list_", "parse_", "detail_", 
        "dump_", "extract_", "read_", "trace_", "analyze_", "get_", "locate_"
    )
    
    build_fix_prefixes = (
        "apply_", "build_", "fix_", "implement_", "update_", 
        "rebuild_", "restore_", "inject_", "clean_", "dedup_", 
        "format_", "interpolate_", "patch_", "reduce_", "remove_", 
        "rename_", "replace_", "revert_", "rewrite_", "shrink_", "sync_", "bundle_"
    )

    all_scratch_files = os.listdir(scratch_dir)
    for fname in all_scratch_files:
        fpath = os.path.join(scratch_dir, fname)
        if os.path.isdir(fpath):
            continue
        
        # Don't move organize_workspace.py yet
        if fname == "organize_workspace.py":
            continue

        if fname.endswith(".json"):
            shutil.move(fpath, os.path.join(json_dir, fname))
        elif fname.endswith(".js") or fname.endswith(".html"):
            shutil.move(fpath, os.path.join(temp_ui_dir, fname))
        elif fname.endswith(".png"):
            shutil.move(fpath, os.path.join(backups_dir, fname))
        elif fname.endswith(".py"):
            if fname.startswith(inspect_prefixes):
                shutil.move(fpath, os.path.join(inspect_dir, fname))
            elif fname.startswith(build_fix_prefixes):
                shutil.move(fpath, os.path.join(build_fix_dir, fname))
            else:
                if "test" in fname or "debug" in fname or "sim" in fname:
                    shutil.move(fpath, os.path.join(inspect_dir, fname))
                else:
                    shutil.move(fpath, os.path.join(build_fix_dir, fname))
        elif fname.endswith(".txt"):
            shutil.move(fpath, os.path.join(json_dir, fname))

    print("=== Workspace Cleanup Completed Successfully ===")

if __name__ == "__main__":
    main()

