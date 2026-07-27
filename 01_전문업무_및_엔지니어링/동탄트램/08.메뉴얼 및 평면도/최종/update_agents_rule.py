import sys

sys.stdout.reconfigure(encoding='utf-8')

agents_md_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\.agents\AGENTS.md"

with open(agents_md_path, 'r', encoding='utf-8') as f:
    content = f.read()

rule_addition = """

## Clickable Diagram Lightbox Zoom Modal Policy (도식/그림 클릭 시 대형 팝업 확대 수칙)
* **CRITICAL:** All technical diagrams, SVG cross-section drawings, and embedded images inside Guideline HTML files MUST support a **Clickable Lightbox Zoom Modal (`openDiagramZoom`)**.
* **INTERACTION:** When a user clicks on any diagram container (`class="clickable-diagram"`), a dedicated full-screen overlay modal (`#zoomModal`) MUST pop up, rendering the SVG/image in an enlarged, high-resolution view (520px+ height) so all small texts and engineering labels can be clearly read.
* **LEGIBILITY:** All SVG text font-sizes MUST be set to **11px to 14px or larger** with bold styling for immediate legibility.
"""

if 'Clickable Diagram Lightbox Zoom Modal Policy' not in content:
    new_content = content + rule_addition
    with open(agents_md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ SUCCESS: Added Clickable Diagram Zoom Policy to AGENTS.md")
else:
    print("ℹ️ INFO: Policy already exists in AGENTS.md")
