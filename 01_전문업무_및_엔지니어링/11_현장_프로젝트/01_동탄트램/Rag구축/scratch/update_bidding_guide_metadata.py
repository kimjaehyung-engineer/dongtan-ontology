import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

meta_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents\_metadata_index.json")

with open(meta_path, 'r', encoding='utf-8') as f:
    meta = json.load(f)

doc_key = "입찰안내서(동탄트램).pdf"

# Full 21 sections based on Table of Contents (618 pages total)
sections = [
    # 제1장 일반사항
    {
        "title": "제1장 일반사항 - 1. 입찰안내서에 대한 유의사항",
        "start_page": 3,
        "end_page": 33,
        "facility": ["1공구 본선", "2공구 본선", "차량기지", "공통"],
        "summary": "동탄 도시철도 건설공사(1단계) 기본설계 기술제안입찰의 목적, 용어 정의, 우선적용 기준, 법령 준수 및 입찰 유의사항 규정"
    },
    {
        "title": "제1장 일반사항 - 2. 기본설계 기술제안입찰 공사설명서",
        "start_page": 34,
        "end_page": 47,
        "facility": ["1공구 본선", "2공구 본선", "차량기지"],
        "summary": "공사명, 공사위치, 사업규모, 노선현황, 공사기간(총공사 및 우선시공분), 추정공사비 및 주요 공종별 공사 범위 설명"
    },
    {
        "title": "제1장 일반사항 - 3. 입찰서 목록",
        "start_page": 48,
        "end_page": 54,
        "facility": ["공통"],
        "summary": "기술제안입찰 제출도서 목록, 서식 규격, 제출 부수 및 입찰 등록 서류 목록"
    },
    # 제2장 입찰에 관한 사항
    {
        "title": "제2장 입찰에 관한 사항 - 1. 입찰 유의서",
        "start_page": 57,
        "end_page": 68,
        "facility": ["공통"],
        "summary": "입찰참가자격, 현장설명회, 입찰보증금, 입찰서 작성 및 제출 방법, 입찰의 무효 기준"
    },
    {
        "title": "제2장 입찰에 관한 사항 - 2. 공사입찰특별유의서 I, II",
        "start_page": 69,
        "end_page": 91,
        "facility": ["공통"],
        "summary": "일괄입찰 및 기술제안입찰 특별유의서, 공동도급계약 조건, 제안서 작성비용 보상기준"
    },
    {
        "title": "제2장 입찰에 관한 사항 - 3. 청렴계약(서약)제 적용",
        "start_page": 92,
        "end_page": 92,
        "facility": ["공통"],
        "summary": "청렴계약 이행서약서 작성 요령 및 부정당업자 제재 규정"
    },
    # 제3장 계약에 관한 사항
    {
        "title": "제3장 계약에 관한 사항 - 1. 계약 일반조건",
        "start_page": 95,
        "end_page": 141,
        "facility": ["공통"],
        "summary": "지방자치단체 공사계약 일반조건 준용, 계약보증금, 지체상금, 착공 및 준공 규정"
    },
    {
        "title": "제3장 계약에 관한 사항 - 2. 공사계약특수조건 I, II (설계변경/리스크)",
        "start_page": 142,
        "end_page": 198,
        "facility": ["공통", "1공구 본선", "2공구 본선", "차량기지"],
        "summary": "기술제안입찰 계약특수조건, 설계변경 허용/불가 사유, 지반조건 상이 시 처리기준, 물가변동(ESC), 인허가 민원 리스크 분담"
    },
    {
        "title": "제3장 계약에 관한 사항 - 3. 청렴계약 특수조건",
        "start_page": 199,
        "end_page": 199,
        "facility": ["공통"],
        "summary": "청렴계약 특수조건 준수 의무 및 위반 시 계약 해제/해지 조항"
    },
    {
        "title": "제3장 계약에 관한 사항 - 4. 공동계약 운용요령",
        "start_page": 200,
        "end_page": 224,
        "facility": ["공통"],
        "summary": "공동이행방식 공동수급체 구성, 출자비율, 대표자 권한 및 구성원 상호 연대책임 운용기준"
    },
    # 제4장 기술에 관한 사항
    {
        "title": "제4장 기술에 관한 사항 - 1. 기술제안 일반지침",
        "start_page": 227,
        "end_page": 240,
        "facility": ["공통", "1공구 본선", "2공구 본선", "차량기지"],
        "summary": "기본설계 기술제안 원칙, 공사비 절감, 성능 개선, 공기단축, 안전확보 및 특화계획 기본 가이드라인"
    },
    {
        "title": "제4장 기술에 관한 사항 - 2. 실시설계 지침 (지반/토목/구조/궤도)",
        "start_page": 241,
        "end_page": 355,
        "facility": ["1공구 본선", "2공구 본선", "차량기지", "토목/지반", "궤도"],
        "summary": "지반조사(시추간격/심도) 기준, 흙막이 가시설 및 터파기 설계지침, 비탈면 최소안전율, 구조물 설계하중, 트램 궤도 선형 및 궤도구조 설계기준"
    },
    {
        "title": "제4장 기술에 관한 사항 - 3. 시공지침",
        "start_page": 356,
        "end_page": 367,
        "facility": ["1공구 본선", "2공구 본선", "차량기지"],
        "summary": "공종별 시공 기준, 품질시험 규정, 토공 및 가시설 시공 시 유의사항, 시공계측 관리 기준"
    },
    {
        "title": "제4장 기술에 관한 사항 - 4. 공사총칙에 대한 지침",
        "start_page": 368,
        "end_page": 496,
        "facility": ["공통", "1공구 본선", "2공구 본선", "차량기지"],
        "summary": "공사 현장관리, 지장물 이설 지침, 교통처리계획(도심지 차로 확보), 환경영향저감, 소음진동·비산먼지 관리 및 안전관리 의무"
    },
    {
        "title": "제4장 기술에 관한 사항 - 5. 인터페이스 및 통합 시행조건",
        "start_page": 497,
        "end_page": 505,
        "facility": ["1공구-2공구 경계", "트램차량-인프라 연계", "차량기지"],
        "summary": "1공구-2공구 접속부 시공 인터페이스, 트램 차량-노반-궤도-시스템(전철전력/신호/통신) 인터페이스 조정 및 통합시운전 조건"
    },
    {
        "title": "제4장 기술에 관한 사항 - 6. 설계도서 작성지침",
        "start_page": 506,
        "end_page": 535,
        "facility": ["공통"],
        "summary": "설계도면(CAD), 수량산출서, 단가산출서, 구조/수리/지반계산서 및 시방서 작성 표준 규격"
    },
    {
        "title": "제4장 기술에 관한 사항 - 7. 기술제안서 작성지침",
        "start_page": 536,
        "end_page": 546,
        "facility": ["공통"],
        "summary": "기술제안서 규격(A3/A4 쪽수 제한), 작성 항목별 작성순서, 제안도면 축척 및 핵심 제안사항 명기 기준"
    },
    # 제5장 공사관리
    {
        "title": "제5장 공사관리 - 1. 공사관리지침",
        "start_page": 549,
        "end_page": 571,
        "facility": ["공통"],
        "summary": "공정관리(PERT/CPM), 기성관리, 하도급 관리, 감리감독관 검측 절차 및 안전보건관리체계 구축 지침"
    },
    {
        "title": "제5장 공사관리 - 2. 공사관리계획서 작성지침",
        "start_page": 572,
        "end_page": 582,
        "facility": ["공통"],
        "summary": "공정관리계획, 현장조직도, 비상대응계획, 안전·환경관리계획서 작성 및 제출 기준"
    },
    # 제6장 평가에 관한 사항
    {
        "title": "제6장 평가에 관한 사항 - 1. 일반사항",
        "start_page": 585,
        "end_page": 585,
        "facility": ["공통"],
        "summary": "기술제안서 평가위원회 구성, 운영 원칙 및 심의 절차 개요"
    },
    {
        "title": "제6장 평가에 관한 사항 - 2. 기술제안입찰 낙찰자 결정 세부기준",
        "start_page": 586,
        "end_page": 591,
        "facility": ["공통"],
        "summary": "가중치기준방식 종합평점 산정(기술점수+가격점수), 부적격 처리 요건 및 낙찰적격자 심사 기준"
    },
    {
        "title": "제6장 평가에 관한 사항 - 3. 기술제안서 평가지침 (배점/감점)",
        "start_page": 592,
        "end_page": 599,
        "facility": ["공통", "토목/지반", "궤도", "시스템"],
        "summary": "분야별 평가항목 및 배점표(설계의 적정성, 시공계획의 타당성, 안전성 등), 실격 및 감점 기준(쪽수 초과, 지침 위반)"
    },
    {
        "title": "제6장 평가에 관한 사항 - 4. 1차(우선시공분) 실시설계 평가 & 낙찰자 결정",
        "start_page": 600,
        "end_page": 618,
        "facility": ["공통"],
        "summary": "우선시공분 실시설계 적격 심의, 최종 낙찰자 결정 통보 및 계약 체결 절차"
    }
]

meta[doc_key] = {
    "total_pages": 618,
    "sections": sections
}

with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"Successfully updated _metadata_index.json with {len(sections)} sections for '{doc_key}'!")
