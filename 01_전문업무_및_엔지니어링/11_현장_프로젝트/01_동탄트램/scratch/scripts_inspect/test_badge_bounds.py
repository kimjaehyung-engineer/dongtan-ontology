import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

def calc_width(text_str, font_size=2.4, padding=4.0):
    w = 0
    for char in text_str:
        if ord(char) > 127:  # Hangul / CJK
            w += font_size * 0.95
        else:  # ASCII / Numbers / Brackets
            w += font_size * 0.55
    return round(w + padding, 1)

test_strings = [
    "서동탄역사거리 [7.1m]",
    "병점역공영주차장삼거리 [12.4m]",
    "동탄테크노벨리(남)교차로 [5.8m]",
    "더레이크시티3064동삼거리 [10.2m]"
]

print("=== Width Calculations (font_size=2.4px, height=4.0px) ===")
for s in test_strings:
    w = calc_width(s)
    print(f"Text: {s:35s} | Length: {len(s):2d} | Box Width: {w:4.1f}px")
