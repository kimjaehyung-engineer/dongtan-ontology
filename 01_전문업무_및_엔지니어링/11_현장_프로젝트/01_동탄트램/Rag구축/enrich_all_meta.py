# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

rag_dir = Path(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG')
meta_file = rag_dir / "documents" / "_metadata_index.json"

with open(meta_file, 'r', encoding='utf-8') as f:
    meta = json.load(f)

# 1. 기술제안_4편 토질 및 기초(97~116).pdf
meta["기술제안_4편 토질 및 기초(97~116).pdf"] = {
    "document_name": "기술제안_4편 토질 및 기초(97~116).pdf",
    "total_pages": 22,
    "description": "동탄도시철도 건설사업 제4편 토질 및 기초 기술제안서 본문 (4대 핵심과제)",
    "sections": [
        {
            "section_id": "PROP-00",
            "task_id": "제1장 제안개요",
            "title": "제1장 제안개요 및 핵심요약 (4대 기술과제 종합)",
            "start_page": 1,
            "end_page": 3,
            "keywords": ["제안개요", "핵심요약", "4대 핵심과제", "기술제안", "토질및기초", "제4편", "요약"],
            "facility": ["본선", "차량기지", "변전소", "환승역사"]
        },
        {
            "section_id": "PROP-01",
            "task_id": "토질및기초-01",
            "title": "과제1: 지반조사 시행 및 결과 분석 (상세조사 126공 계획)",
            "start_page": 4,
            "end_page": 8,
            "keywords": ["지반조사", "126공", "추가조사", "시추조사", "CPT", "압밀시험", "동평판재하", "지질이상대", "연약지반"],
            "facility": ["본선", "차량기지"]
        },
        {
            "section_id": "PROP-02",
            "task_id": "토질및기초-02",
            "title": "과제2: 트램 콘크리트 슬래브 궤도 기초 지지력 및 침하 안정성 검토",
            "start_page": 9,
            "end_page": 13,
            "keywords": ["트램", "콘크리트 궤도", "슬래브", "지지력", "침하량", "잔류침하", "노반", "안정성", "허용침하량"],
            "facility": ["본선 궤도", "정거장"]
        },
        {
            "section_id": "PROP-03",
            "task_id": "토질및기초-03",
            "title": "과제3: 흙막이 가시설 및 비탈면 안정성, 지하안전평가 (3D FEM 수치해석)",
            "start_page": 14,
            "end_page": 18,
            "keywords": ["가시설", "흙막이", "비탈면", "수치해석", "3D FEM", "지하안전평가", "변전소", "환승역사", "안정성"],
            "facility": ["S01변전소", "S02변전소", "S03변전소", "S04변전소", "환승역사"]
        },
        {
            "section_id": "PROP-04",
            "task_id": "토질및기초-04",
            "title": "과제4: 공사중 스마트 계측관리 및 계측기 배치계획",
            "start_page": 19,
            "end_page": 22,
            "keywords": ["스마트 계측", "자동화 계측", "계측기", "배치계획", "계측관리", "변위계", "수위계", "침하계"],
            "facility": ["전 구간", "변전소", "궤도"]
        }
    ]
}

# 2. 토질_차량기지 비탈면 안정성 검토-rev01_260630.pdf
meta["토질_차량기지 비탈면 안정성 검토-rev01_260630.pdf"] = {
    "document_name": "토질_차량기지 비탈면 안정성 검토-rev01_260630.pdf",
    "total_pages": 6,
    "description": "차량기지 절토/성토 비탈면 안정성 검토 보고서 (최신 Rev.01)",
    "sections": [
        {
            "section_id": "SLOPE-01",
            "task_id": "비탈면안정성",
            "title": "차량기지 절토 및 성토 비탈면 한계평형해석 및 안전율 검토",
            "start_page": 1,
            "end_page": 6,
            "keywords": ["차량기지", "비탈면", "안정성", "절토", "성토", "안전율", "한계평형해석", "건기", "우기", "지진시", "사면안정"],
            "facility": ["차량기지"]
        }
    ]
}

with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("SUCCESS: 5 documents 100% indexed in _metadata_index.json!")
