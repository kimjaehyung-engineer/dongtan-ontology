# -*- coding: utf-8 -*-
import sys
import re
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Add ROOT_DOCS configuration helpers near DOCS_DIR
old_docs_def = 'DOCS_DIR = Path(__file__).parent / "documents"\nENV_FILE = Path(__file__).parent / ".env"'
new_docs_def = '''DOCS_DIR = Path(__file__).parent / "documents"
ENV_FILE = Path(__file__).parent / ".env"
RAG_CONFIG_FILE = Path(__file__).parent / "rag_config.json"
DEFAULT_SOURCE_DOCS = Path(r"C:\\Users\\sskjh\\antigravity\\01_전문업무_및_엔지니어링\\11_현장_프로젝트\\01_동탄트램\\Rag구축\\01_SOURCE_DOCUMENTS")

def get_configured_docs_root() -> Path:
    if RAG_CONFIG_FILE.exists():
        try:
            import json
            with open(RAG_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                custom_root = cfg.get("docs_root_path")
                if custom_root and Path(custom_root).exists() and Path(custom_root).is_dir():
                    return Path(custom_root)
        except Exception:
            pass
    if DEFAULT_SOURCE_DOCS.exists() and DEFAULT_SOURCE_DOCS.is_dir():
        return DEFAULT_SOURCE_DOCS
    return DOCS_DIR

def set_configured_docs_root(path_str: str) -> bool:
    target = Path(path_str)
    if not target.exists() or not target.is_dir():
        return False
    cfg = {}
    import json
    if RAG_CONFIG_FILE.exists():
        try:
            with open(RAG_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass
    cfg["docs_root_path"] = str(target.resolve())
    with open(RAG_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return True

def scan_folder_tree(root_dir: Path):
    valid_exts = {".pdf", ".xlsx", ".xls", ".hwp", ".hwpx", ".docx", ".txt", ".csv"}
    all_files = []
    meta_map = {}
    if META_INDEX_FILE.exists():
        try:
            import json
            with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                meta_map = json.load(f)
        except Exception:
            pass

    for p in root_dir.rglob("*"):
        if not p.is_file():
            continue
        if p.name.startswith("~") or p.name.startswith("."):
            continue
        if p.suffix.lower() not in valid_exts:
            continue
            
        rel = p.relative_to(root_dir)
        size_mb = round(p.stat().st_size / (1024 * 1024), 2)
        folders = list(rel.parent.parts)
        rel_str = str(rel).replace("\\\\", "/")
        
        doc_info = {
            "name": p.name,
            "rel_path": rel_str,
            "folders": folders,
            "size_mb": size_mb,
            "ext": p.suffix.lower()
        }
        
        if p.name in meta_map:
            m = meta_map[p.name]
            doc_info["total_pages"] = m.get("total_pages", 0)
            doc_info["sections"] = [
                {"title": s["title"], "start_page": s["start_page"], "end_page": s["end_page"], "facility": s.get("facility", [])}
                for s in m.get("sections", [])
            ]
        all_files.append(doc_info)
        
    tree_root = {"name": root_dir.name, "type": "folder", "path": "", "children": {}}
    for item in all_files:
        curr = tree_root
        accum_path = []
        for folder in item["folders"]:
            accum_path.append(folder)
            subpath = "/".join(accum_path)
            if folder not in curr["children"]:
                curr["children"][folder] = {
                    "name": folder,
                    "type": "folder",
                    "path": subpath,
                    "children": {}
                }
            curr = curr["children"][folder]
            
        curr["children"][item["name"]] = {
            "name": item["name"],
            "type": "file",
            "rel_path": item["rel_path"],
            "size_mb": item["size_mb"],
            "ext": item["ext"],
            "total_pages": item.get("total_pages", 0)
        }
        
    def dict_to_list(node):
        if node["type"] == "folder":
            folders = []
            files = []
            for k, child in node["children"].items():
                processed = dict_to_list(child)
                if processed["type"] == "folder":
                    folders.append(processed)
                else:
                    files.append(processed)
            folders.sort(key=lambda x: x["name"])
            files.sort(key=lambda x: x["name"])
            node["children"] = folders + files
            node["total_files"] = sum(c.get("total_files", 1) if c["type"] == "folder" else 1 for c in node["children"])
        return node
        
    final_tree = dict_to_list(tree_root)
    return {
        "root_path": str(root_dir),
        "total_count": len(all_files),
        "docs": all_files,
        "tree": final_tree
    }'''

if old_docs_def in code:
    code = code.replace(old_docs_def, new_docs_def, 1)
    print("Step 1: Injected docs root config and scan_folder_tree")
else:
    print("Step 1: Warning, old_docs_def not found directly, checking...")

with open("scratch/patch_code_temp.py", "w", encoding="utf-8") as f_out:
    f_out.write(code)
print("Saved temporary check.")
