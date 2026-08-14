import os

def inspect_layout():
    files = [
        "08.메뉴얼 및 평면도/동탄트램_업무_매뉴얼.html",
        "03_보고서_및_출력/지장물_이설_업무_매뉴얼.html"
    ]
    
    output_lines = []
    
    for filepath in files:
        output_lines.append(f"\n=== Inspecting {filepath} ===")
        if not os.path.exists(filepath):
            output_lines.append(f"  File not found: {filepath}")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find body style
        body_tag_idx = content.find("<body")
        if body_tag_idx != -1:
            output_lines.append(f"Body tag: {content[body_tag_idx:body_tag_idx+100]}")
            
        # Find aside tag
        aside_tag_idx = content.find("<aside")
        if aside_tag_idx != -1:
            output_lines.append(f"Aside tag: {content[aside_tag_idx:aside_tag_idx+200]}")
            
        # Find main tag
        main_tag_idx = content.find("<main")
        if main_tag_idx != -1:
            output_lines.append(f"Main tag: {content[main_tag_idx:main_tag_idx+200]}")
            
        # Let's inspect style rules for body, aside, main
        style_idx = content.find("<style>")
        style_end = content.find("</style>")
        if style_idx != -1 and style_end != -1:
            styles = content[style_idx:style_end]
            for rule in ["body {", "aside {", "main {", "flex-direction", "@media"]:
                idx = 0
                while True:
                    rule_idx = styles.find(rule, idx)
                    if rule_idx == -1:
                        break
                    output_lines.append(f"Style rule '{rule}': {styles[rule_idx:rule_idx+180]}")
                    idx = rule_idx + len(rule)
                    
    with open("scratch/layout_inspection.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines))
    print("Done writing to scratch/layout_inspection.txt")

if __name__ == '__main__':
    inspect_layout()
