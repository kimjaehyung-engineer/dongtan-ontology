import os
import json
from pathlib import Path

root = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\01_SOURCE_DOCUMENTS")

def scan_folder_tree(root_dir: Path):
    valid_exts = {".pdf", ".xlsx", ".xls", ".hwp", ".hwpx", ".docx", ".txt", ".csv"}
    all_files = []
    
    # 1. Collect all valid files
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
        
        all_files.append({
            "name": p.name,
            "rel_path": str(rel).replace("\\", "/"),
            "folders": folders,
            "size_mb": size_mb,
            "ext": p.suffix.lower()
        })
        
    # 2. Build hierarchical tree structure
    # node: { name, type: 'folder'|'file', children: {}, ... }
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
            "ext": item["ext"]
        }
        
    # Convert children dicts to sorted lists
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
        "files": all_files,
        "tree": final_tree
    }

res = scan_folder_tree(root)
print("Total files:", res["total_count"])
print("Tree:")
def print_tree(node, indent=0):
    prefix = "  " * indent
    if node["type"] == "folder":
        print(f"{prefix}[DIR] {node['name']} ({node.get('total_files', 0)} files)")
        for c in node.get("children", []):
            print_tree(c, indent + 1)
    else:
        print(f"{prefix}[FILE] {node['name']} ({node['size_mb']} MB)")

print_tree(res["tree"])
