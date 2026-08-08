# -*- coding: utf-8 -*-
import os

gemini_dir = r"C:\Users\sskjh\.gemini"
print("Scanning .gemini for any backups:")

# Find files with .html extension in AppData or .gemini that might be backups
for root, dirs, files in os.walk(gemini_dir):
    for f in files:
        if "동탄트램_업무_매뉴얼" in f:
            path = os.path.join(root, f)
            print(f"Found match: {path}, size: {os.path.getsize(path)} bytes")
