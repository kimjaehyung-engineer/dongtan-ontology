# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

SERVER_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")

with open(SERVER_PATH, "r", encoding="utf-8") as f:
    code = f.read()

old_needle = '''                        # [신규 9대 전문 기술제안서 맞춤형 라우팅 가중치]
                        if any(k in query_lower for k in ["신호", "cbtc", "atp", "ato", "차상", "지상신호"]) and "신호" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["전기", "급전", "충전", "수변전", "변전소", "전차선"]) and "전기" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["철도", "궤도", "레일", "분기기", "선형", "무도상"]) and "철도" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["건축", "캐노피", "디자인", "체험시설", "정거장배치"]) and "건축" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["토목구조", "u타입", "지하차도", "기존구조물"]) and "토목구조" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["토목시공", "공기단축", "품질관리", "스마트건설"]) and "토목시공" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["통신", "lte-r", "영상감시", "cctv", "afc", "mis"]) and "통신" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["기계", "소방", "검수설비", "공조", "소화"]) and "기계" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["토질", "기초", "지반조사", "비탈면", "가시설"]) and "토질" in dn: doc_bonus += 40
                        if "입찰안내서" in query_lower and "입찰안내서" in dn: doc_bonus += 60
                        if ("기술제안" in query_lower or "4편" in query_lower) and "4편" in dn: doc_bonus += 30'''

new_replacement = '''                        # [신규 9대 전문 기술제안서 정밀 도메인 라우팅 가중치]
                        if any(k in query_lower for k in ["신호", "cbtc", "atp", "ato", "차상", "지상신호"]) and "신호" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["전기", "급전", "충전", "수변전", "변전소", "전차선"]) and "전기" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["철도", "궤도", "레일", "분기기", "선형", "무도상"]) and "철도" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["건축", "캐노피", "디자인", "체험시설", "정거장배치"]) and "건축" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["토목구조", "u타입", "지하차도", "기존구조물"]) and "토목구조" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["토목시공", "공기단축", "품질관리", "스마트건설"]) and "토목시공" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["통신", "lte-r", "영상감시", "cctv", "afc", "mis"]) and "통신" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["기계", "소방", "검수설비", "공조", "소화"]) and "기계" in dn: doc_bonus += 80
                        if any(k in query_lower for k in ["토질", "기초", "지반조사", "비탈면", "가시설"]) and ("토질 및 기초" in dn or "기본설계 기술제안_ 토질" in dn): doc_bonus += 50
                        if "기술제안" in query_lower and "기본설계 기술제안" in dn: doc_bonus += 25
                        if "입찰안내서" in query_lower and "입찰안내서" in dn: doc_bonus += 60
                        if ("4편" in query_lower or ("기술제안" in query_lower and not any(f in query_lower for f in ["신호", "전기", "철도", "궤도", "통신", "건축", "기계", "구조", "시공"]))) and "4편" in dn: doc_bonus += 30'''

if old_needle in code:
    code = code.replace(old_needle, new_replacement, 1)
    with open(SERVER_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    print("SUCCESS: Updated routing bonuses in server.py")
else:
    print("FAIL: needle not found in server.py")
