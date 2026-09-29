import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# In server.py, update all occurrences of models_to_try to include gemma-4-26b-a4b-it
import re

# Match lists of models_to_try
def replacer(match):
    block = match.group(0)
    if "gemma-4-26b-a4b-it" not in block:
        # insert before gemini-flash-latest or at end of list
        if '"gemini-flash-latest"' in block:
            return block.replace('"gemini-flash-latest"', '"gemma-4-26b-a4b-it",\n                            "gemini-flash-latest"')
        elif "'gemini-flash-latest'" in block:
            return block.replace("'gemini-flash-latest'", "'gemma-4-26b-a4b-it',\n                            'gemini-flash-latest'")
        else:
            return block.replace("]", ',\n                            "gemma-4-26b-a4b-it"\n                        ]')
    return block

new_content = re.sub(r'models_to_try\s*=\s*\[[^\]]+\]', replacer, content)

# Also check fb_m list in fallback block:
# for fb_m in ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]:
new_content = new_content.replace(
    'for fb_m in ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]:',
    'for fb_m in ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemma-4-26b-a4b-it", "gemini-flash-latest"]:'
)

server_path.write_text(new_content, encoding="utf-8")
print("Successfully injected gemma-4-26b-a4b-it fallback across server.py!")
