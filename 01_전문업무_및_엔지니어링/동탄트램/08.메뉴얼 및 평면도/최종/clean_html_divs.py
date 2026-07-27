import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file1 = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설\3_지장물 이설 요청 (위수탁고)\표준서\지장물 이설 요청 (위수탁고)_표준서.html"
file2 = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설\4_도급자분 이설업체 선정(상_하수)\표준서\도급자분 이설업체 선정(상_하수)_표준서.html"

for f_path in [file1, file2]:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        filtered = []
        for l in lines:
            if any(k in l for k in ["관종 타겟팅", "공문 발송 및 접수", "줄따기 GPR", "무단수 Cut-over", "사후 정산 및 GIS", "전문면허 검증", "적격 심사 85점", "특기시방 명시", "본사 승인 및 계약", "인력 현치 및 착수"]):
                continue
            filtered.append(l)

        with open(f_path, 'w', encoding='utf-8') as file:
            file.writelines(filtered)
        print(f"Completely cleaned {os.path.basename(f_path)}")
