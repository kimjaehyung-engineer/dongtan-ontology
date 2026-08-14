# -*- coding: utf-8 -*-
"""
동탄도시철도(트램) 전기분야 33개 공종 총 99개 HTML (표준서, 수행지침, 체크리스트) 
통신분야 모던 템플릿 기반 전면 업그레이드 생성 스크립트
"""

import os
import sys

BASE_DIR = r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\전기분야"

# 33개 공종 메타데이터 정의
TASKS_DATA = {
    1: {
        "num": 1,
        "folder": "1_설계적정성 검토",
        "wbs": "9000-3-1",
        "name": "설계적정성 검토",
        "subtitle": "입찰도서, KEC 규격, 22.9kV 수전용량, 전차선 가선방식 & 8대 이종 시스템 인터페이스 무결성 수칙",
        "overview": "동탄도시철도(트램) 전기공종의 시공 착수 전 설계 적정성 및 사양을 종합 검토하여 설계도서 오류, 변전소 용량 부족, 전압강하 리스크 및 시공 간섭을 사전에 차단하기 위한 기술 표준 수칙입니다. KEC(한국전기설비규정), 22.9kV 특고압 수전용량(≥3,000kVA), DC 750V 정류기 용량 및 전차선 가선방식, 배관/배선 규격(점유율≤40%, 이격거리≥300mm)을 정밀 검증합니다.",
        "kpi": [
            ("22.9kV 특고압 수전", "수전용량 ≥ 3,000kVA (변전소 N+1 다중화)"),
            ("DC 750V 급전 전압강하", "최대 전압강하율 ≤ 5% 이내 유지 (말단 기준)"),
            ("전기설비 이격거리", "약전류/통신선로와 이격 ≥ 300mm 확보"),
            ("공학 기준 준수율", "KEC(한국전기설비규정) 및 철도설계기준 100% 충족")
        ],
        "tech_specs": [
            ("22.9kV 특고압 수전 설비", "한전 공급 규격 22.9kV-y, GIS 진공차단기 차단용량 ≥ 25kA", "착수 전 1회", "오차 0%"),
            ("DC 750V 정류기반", "24펄스 다이오드 정류기, 정격용량 2,000kW 2Bank 구성", "공장검사/현장", "정격 전압 ±2%"),
            ("강체전차선(T-Bar) 지지물", "지지간격 L≤5.0m, 가선높이 H=4,500mm ±10mm", "매 5m 간격", "오차 ±10mm"),
            ("접지설비(공통접지)", "통합 공통접지망 구축, 접지저항치 R ≤ 1.0Ω", "타설 전/후", "R ≤ 1.0Ω")
        ],
        "steps": [
            ("STEP 1 WHAT", "설계도서 및 특고압 수전용량 대조 검토 (WHAT TO REVIEW)", [
                "22.9kV 한전 수전인입 설계도서 및 수전계약 용량(≥3,000kVA) 적정성을 전산 시뮬레이션으로 검증합니다.",
                "DC 750V 정류기반(24펄스) 및 직류차단기(HSCB) 차단용량의 기술사양서 일치 여부를 대조합니다.",
                "강체전차선(T-Bar) 가선높이(H=4,500mm)와 토목 교량/터널 구조물 한계 한계치를 1:1 오버레이 검토합니다."
            ]),
            ("STEP 2 WHEN", "타설 전 수전/인입 배관 매설 위치 검증 (WHEN TO VERIFY)", [
                "정거장 및 변전소 골조 콘크리트 타설 7일 전 특고압 케이블 트렌치 및 인입 슬리브 매설 위치를 현장 실측합니다.",
                "배관 굴절 반경(R ≥ 10D) 및 점유율(≤40%)을 KEC 기준에 맞춰 전수 확인합니다.",
                "철근 배근 간섭 부위 발생 시 설계변경 절차를 거쳐 타설 48시간 전 보강 조치를 완료합니다."
            ]),
            ("STEP 3 WHO", "전기/토목/신호/궤도 4자 인터페이스 엔지니어링 협의 (WHO TO COORDINATE)", [
                "전기 책임엔지니어 주관 하에 토목(트렌치), 신호(궤도회로), 궤도(레일접지) 4자 합동 기술회의를 소집합니다.",
                "레일 귀선전류 귀로와 통신/신호 유도장해 방지용 차폐 차폐선(Shield Wire) 접지 경로를 단일화합니다.",
                "합동 검토 결과는 인터페이스 검토대장에 전산 등록하고 감리원 서명/날인을 체결합니다."
            ]),
            ("STEP 4 WHERE", "변전실 및 TPS실 장비 반입동선 & 층고 실측 (WHERE TO MEASURE)", [
                "정거장 전기실 및 지상 변전소 장비 반입구 폭(W ≥ 2,500mm)과 천장 유효 층고(H ≥ 3,500mm)를 실측합니다.",
                "바닥 무근 콘크리트 하중(장비 중량 ≥ 8.5ton/대) 및 방진패드 설치 면적을 구조 검토합니다.",
                "케이블 피트 및 트레이 관통부 방화구획(Fire-Stop 2시간 내화) 씰링 사양을 확인합니다."
            ]),
            ("STEP 5 HOW", "설계적정성 최종 검토보고서 감리원 승인 체결 (HOW TO APPROVE)", [
                "12대 필수 설계 적정성 체크리스트를 100% 대조 작성하고 보완요구사항 조치계획을 첨부합니다.",
                "설계변경이 필요한 항목은 즉시 발주처/감리단에 설계변경 품의서를 공식 접수합니다.",
                "최종 승인된 검토보고서를 동탄트램 사업관리시스템(PMIS)에 등록하여 시공 기준 문서로 확정합니다."
            ])
        ],
        "glossary": {
            "kec_standard": ("⚡ 한국전기설비규정(KEC) 적합성", "국제표준(IEC)을 기반으로 한 국내 전기설비 통합 기술기준으로 접지방식, 배선공사, 감전보호 및 과전류 보호장치 선정의 필수 법정 기준입니다."),
            "substation_capacity": ("🔋 변전소 22.9kV 수전 및 N+1 다중화", "변전소 변압기 또는 정류기 1대 고장 시에도 잔여 설비로 트램 본선 열차 운행에 지장이 없도록 이중화 수전 및 상호 절체 기능을 확보하는 전력망 구축 수칙입니다."),
            "tbar_catenary": ("🚊 DC 750V 강체전차선(T-Bar) 가선", "알루미늄 T형 강체에 전차선을 압착 삽입하여 전식 및 단선 위험을 원천 차단하고 구조물 한계 내에서 일정한 가선높이(4,500mm)를 유지하는 가선 시스템입니다.")
        },
        "diagram_title": "[WBS 9000-3-1] 전기 설계적정성 & 변전 계통 정밀 검토 도식",
        "diagram_svg": '''<svg id="svg_r3_1" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
    <rect x="25" y="20" width="230" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
    <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">⚡ 22.9kV 특고압 수전 & KEC 검토</text>
    <text x="45" y="75" font-size="11" font-weight="bold" fill="#334155">• 수전용량 ≥ 3,000kVA N+1 이중화</text>
    <text x="45" y="98" font-size="11" font-weight="bold" fill="#334155">• 케이블 점유율 ≤ 40%, R ≥ 10D</text>

    <path d="M 260 80 L 290 80" stroke="#2563eb" stroke-width="3"/>
    <polygon points="290,75 300,80 290,85" fill="#2563eb"/>

    <rect x="295" y="20" width="230" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
    <text x="410" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">🚊 DC 750V 정류기 & T-Bar 가선</text>
    <text x="315" y="75" font-size="11" font-weight="bold" fill="#334155">• 24펄스 정류기 전압강하 ≤ 5%</text>
    <text x="315" y="98" font-size="11" font-weight="bold" fill="#334155">• 강체 가선높이 H=4,500mm ±10mm</text>
    <text x="275" y="162" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">설계적정성 검토 완료 및 PMIS 통합 관리대장 등재 완료</text>
</svg>''',
        "checklist_items": [
            ("설계도서 적정성", "한전 22.9kV 수전 계약용량(≥3,000kVA) 및 인입 루트가 현장 여건과 일치하는가?"),
            ("KEC 규정 준수", "접지시스템(통합접지 R≤1.0Ω) 및 배선공사 규격이 한국전기설비규정(KEC)을 100% 충족하는가?"),
            ("정류기 용량 검토", "DC 750V 24펄스 정류기반(2,000kW 2Bank) 용량 및 N+1 예비율이 확보되었는가?"),
            ("전압강하 시뮬레이션", "변전소 간 최대 부하 운행 시 본선 말단 급전선 전압강하율이 5% 이내로 검증되었는가?"),
            ("강체전차선 이격거리", "T-Bar 전차선 가선높이(4,500mm)와 토목 구조물(터널/교량) 간 이격거리(≥150mm)가 확보되었는가?"),
            ("배관/트레이 점유율", "특고압/고압 케이블 트레이 및 전선관 단면적 점유율이 40% 이하로 적정 설계되었는가?"),
            ("이종 선로 이격거리", "강전류 전력선과 신호/통신 약전류 선로 간 이격거리(≥300mm) 및 차폐 격벽이 반영되었는가?"),
            ("변전실 반입동선", "변전소 변압기/GIS 장비 반입구 폭(≥2.5m) 및 천장 층고(≥3.5m)가 현장 실측치와 일치하는가?"),
            ("레일 귀선전류 간섭", "레일 귀선전류 누설 방지용 매설 차폐 접지망 및 전식방지(Electrolysis) 대책이 수립되었는가?"),
            ("방화구획 씰링 사양", "전기실 및 피트 관통부 내화 2시간 이상의 방화 충전재(Fire-Stop) 사양이 누락 없이 설계되었는가?"),
            ("SCADA 연동 인터페이스", "변전설비/차단기 감시제어용 SCADA RTU 통신 프로토콜(IEC 61850/DNP3.0)이 정의되었는가?"),
            ("4자 합동 서명 체결", "전기/토목/신호/궤도 4자 합동 검토회의록 작성 및 책임감리원 최종 승인 날인이 완료되었는가?")
        ]
    }
}

# 33개 공종 공통 생성 데이터 보강 엔진
DEFAULT_TASKS_CONFIG = [
    (1, "1_설계적정성 검토", "설계적정성 검토", "입찰도서, KEC 규격, 22.9kV 수전용량, 전차선 가선방식 & 8대 이종 시스템 인터페이스 무결성 수칙", "⚡ KEC & 22.9kV 수전계통", "🚊 DC 750V & T-Bar 가선"),
    (2, "2_발주전략 KOM", "발주전략 KOM", "전력/변전/전차선 장납기 기자재 조달 및 공구별 발주 착수 전략 수립 수칙", "📦 GIS/변압기 장납기 발주", "📅 공구별 납기 일정 공정관리"),
    (3, "3_토목 _ 건축 인터페이스 협의", "토목 _ 건축 인터페이스 협의", "변전소 하중 구조검토, 케이블 트렌치, 기초 패드 및 관통 슬리브 매설 정밀 협의", "🧱 트렌치/슬리브 매설 검측", "🏢 변전실 하중/층고 실측"),
    (4, "4_신호 _ 통신 _ 기계 _ PSD _ 차량 인터페이스 협의", "신호 _ 통신 _ 기계 _ PSD _ 차량 인터페이스 협의", "신호 궤도회로, 통신 SCADA, PSD 전원 공급, 차량 팬터그래프 접촉 인터페이스 무결성 검증", "📡 신호/통신 이격거리 확보", "🚋 차량 팬터그래프 접촉 검측"),
    (5, "5_전기설비 제작사 인터페이스 협의", "전기설비 제작사 인터페이스 협의", "GIS, 수배전반, 정류기반, SCADA RTU 제작사 기술 사양 및 취부 규격 일치화", "🏭 제작사 도면 1:1 대조", "🔌 제어 인터페이스 결선 표준"),
    (6, "6_관제 및 운영사 인터페이스 협의", "관제 및 운영사 인터페이스 협의", "통합관제센터 전력 SCADA HMI 연동, 비상 차단(EPO) 절차 및 유지보수 운영 협의", "🖥️ SCADA 관제 HMI 프로토콜", "🚨 비상 전력 차단(EPO) 연동"),
    (7, "7_발주처 품질 요구사항 검토", "발주처 품질 요구사항 검토", "화성시/발주처 특기시방서, KRSA 철도표준규격 및 고품질 전기자재 검증 수칙", "📋 발주처 특기시방 대조", "🛡️ KRSA 인증 자재 전수 확인"),
    (8, "8_자재 _ 인원 _ 장비 등 투입 사전 검토", "자재 _ 인원 _ 장비 등 투입 사전 검토", "전기 특급기술자, 활선작업 자격자, 가선 전용 장비 및 특고압 시험장비 투입 사전 승인", "👷 공종별 자격 보유자 선임", "🚜 활선 가선차 안전 인증"),
    (9, "9_인허가 준비", "인허가 준비", "한전 수전 인허가, 전기안전공사 공사계획신고 및 특고압 전력 수급 기본계획 수립", "⚡ 한전 수전 계약 및 협의", "📑 한국전기안전공사 기술검토"),
    (10, "10_착수 전 Big Room 회의", "착수 전 Big Room 회의", "전기/토목/궤도/신호/시스템 전 분야 합동 3D BIM 간섭 검토 및 현장 공정 락인", "🤝 5개 공종 합동 Big Room", "📐 3D BIM 전기배관 간섭 제로"),
    (11, "11_전기설비 제작 사양서 작성 _ 승인", "전기설비 제작 사양서 작성 _ 승인", "22.9kV GIS, 변압기, 정류기, HSCB, 배전반 상세 제작사양서 승인 및 보증치 확정", "📝 제작사양서 정밀 기술검토", "🔍 공인인증기관(KEMA/KERI) 시험성적서"),
    (12, "12_시공 계획 수립 _ 승인", "시공 계획 수립 _ 승인", "전철전력, 송변전, 전차선로, 동력설비 단계별 상세 시공계획서 수립 및 감리원 승인", "📊 단계별 시공 공정 계획", "🛡️ 특고압 취급 안전작업 절차"),
    (13, "13_자재공급원_기자재 제작도서 승인", "자재공급원_기자재 제작도서 승인", "KS/KRSA 인증 시험성적서, 자재공급원 승인신청서 및 제조공장 품질보증체계 승인", "📑 자재공급원 사전 심사", "🏭 공장 품질시스템 ISO 인증"),
    (14, "14_전기설비 공정제작 _ 제작사 공장검사", "전기설비 공정제작 _ 제작사 공장검사", "공장 입회검사(FAT), 내전압 시험, 부분방전 시험 및 차단기 동작 특성 공학 검증", "🔍 FAT 공장 입회 시험", "⚡ 내전압 & 부분방전 시험"),
    (15, "15_본공사 전 선행공정 인수인계 점검", "본공사 전 선행공정 인수인계 점검", "토목 구조물, 변전실 건축 마감, 케이블 트렌치 및 기초 패드 수평도 선행 점검", "📏 패드 수평도 오차 ≤ 2mm", "🧹 트렌치 수밀/청결 상태 확인"),
    (16, "16_장비반입 및 안전교육", "장비반입 및 안전교육", "중량물 반입 양중계획서 검토, 크레인 안전검사 및 특고압 활선 안전 특별교육", "🏗️ 중량물 양중 크레인 안전", "🦺 특고압 안전보호구 착용 교육"),
    (17, "17_자재 반입 및 검수", "자재 반입 및 검수", "현장 반입 자재 외관 손상 검사, 시험성적서 1:1 대조 및 수불대장 전산 등록", "📦 현장 자재 외관/치수 검수", "📑 납품 성적서 원본 대조"),
    (18, "18_전철전력설비 반입 및 설치", "전철전력설비 반입 및 설치", "변전소 변압기, 정류기반, GIS 큐비클 거치 및 앵커볼트 체결 토크 정밀 검측", "⚙️ 볼트 체결 토크 검측", "📐 수평/수직 설치 오차 점검"),
    (19, "19_수전용 케이블 트레이 및 케이블 포설", "수전용 케이블 트레이 및 케이블 포설", "특고압 22.9kV CNCV 케이블 포설 장력 제어, 곡률반경(R≥10D) 준수 및 트레이 고정", "〰️ 포설 장력 & 곡률반경 관리", "🔒 트레이 고정 및 접지 본딩"),
    (20, "20_수전 및 전기공급(급전)", "수전 및 전기공급(급전)", "한전 22.9kV 특고압 본선 수전 가압, 상회전 시험, 보호계전기 연동 및 무부하 가압", "⚡ 22.9kV 본선 가압 시험", "🔄 상회전 & 계전기 인터록 검증"),
    (21, "21_종합연동시험(SCADA) 실시", "종합연동시험(SCADA) 실시", "전력 SCADA 원격 감시제어, 차단기 트립/투입 100% 연동 및 비상 절체 시험", "🖥️ SCADA 원격 제어 응답 검증", "⏱️ 긴급 차단 시퀀스 100% 연동"),
    (22, "22_공종별 시험", "공종별 시험", "절연내력 시험, 접지저항 측정, 계전기 특성시험 및 직류 급전계통 단락시험", "🧪 계전기 동작 특성 시험", "📉 접지저항 R ≤ 1.0Ω 전수 검측"),
    (23, "23_차량 투입 전 점검", "차량 투입 전 점검", "트램 차량 반입 전 가선 전압(DC 750V) 무부하 안정도, 이격거리 및 급전구간 확인", "🚋 전차선 직류 750V 가압 확인", "📏 팬터그래프 가선 동선 점검"),
    (24, "24_차량 시운전", "차량 시운전", "차량 본선 주행 시 집전 상태, 가선 이도 변화, 아크(Arc) 발생 유무 및 전압강하 측정", "📈 주행 중 집전 상태 모니터링", "⚡ 전차선 아크 발생 제로화"),
    (25, "25_운영자 교육시행", "운영자 교육시행", "운영사 유지보수요원 대상 변전설비 조작, SCADA 운용 및 비상정전 대처 교육", "👨‍🏫 운영자 실무 조작 교육", "📖 비상 복구 매뉴얼 숙달"),
    (26, "26_사전점검", "사전점검", "철도종합시험운행 전 한국교통안전공단/전문기관 전기시설물 100% 사전 점검", "🔍 종합 사전 점검 리스트 대조", "🛠️ 지적사항 조치 결과 승인"),
    (27, "27_시설물 검증시험", "시설물 검증시험", "최대 부하 트램 다중 운행 시 변전소 부하 분담, 급전 전압 안정성 및 고조파 분석", "📊 최대 부하 운행 시 전력 품질", "🌊 고조파 왜곡률(THD) 기준 충족"),
    (28, "28_영업시운전", "영업시운전", "실제 영업 타임테이블 기반 24시간 무중단 전력 공급 및 비상 발전기 자동 절체 검증", "🕒 24시간 연속 무결성 급전", "🚨 비상 발전 ATS 자동 전환"),
    (29, "29_전기 사용신청", "전기 사용신청", "한국전력공사 정식 수전 계약 체결, 계량기(MOF) 봉인 및 전기 사용신청 완료", "⚡ 한전 수전 계약 및 계량기 봉인", "📑 전기 수급 합의서 체결"),
    (30, "30_공사계획신고", "공사계획신고", "전기사업법에 따른 산업통상자원부/지자체 특고압 전기설비 공사계획신고 및 수리", "📑 공사계획신고서 공식 수리", "🏛️ 전기사업법 법정 요건 완수"),
    (31, "31_전차선로 적합성 검증", "전차선로 적합성 검증", "강체/가공 전차선로 마모도, 가선 편위(±200mm), 압상량 및 전기철도기술기준 검증", "📐 전차선 편위 & 압상량 실측", "📏 마모 한계선 레이저 측정"),
    (32, "32_전기 사용전검사 (전력_전차선_송변전)", "전기 사용전검사 (전력_전차선_송변전)", "한국전기안전공사(KESCO) 주관 사용전검사 수검 및 법정 사용전검사 합격증 취득", "🏛️ KESCO 법정 사용전검사", "📜 전기설비 사용전검사 합격증"),
    (33, "33_Task_33", "준공도서 및 최종 인수인계", "전기분야 준공도면(As-Built), 시험성적서, 유지관리 지침서 편철 및 운영사 최종 인수인계", "📁 준공도서(As-Built) 편철", "🤝 운영사 최종 인수인계 체결")
]

def build_task_data(task_tuple):
    num, folder, name, subtitle, tag1, tag2 = task_tuple
    wbs = f"9000-3-{num}"
    
    overview = f"동탄도시철도(트램) 전기공종의 WBS {wbs} ({name}) 업무를 완벽하게 수행하기 위한 마스터 표준 및 기술 수칙입니다. KEC(한국전기설비규정), 철도설계기준 및 현장 공학 기준을 100% 준수하여 전력 수급 안전성, 인터페이스 무결성 및 무재해 시공 품질을 확보합니다. (주관: 현장 전기팀/공무팀)"
    
    kpi = [
        ("품질 기준 적합률", "KEC 및 철도표준시방서 기준 100% 충족"),
        ("안전 무사고 달성", "특고압 활선 안전수칙 및 정전작업 100% 이행"),
        ("인터페이스 무결성", "토목/건축/신호/궤도/차량 간섭 Zero화 달성"),
        ("공정 준수율", "마스터 공정표 대비 일정 지연 0일 유지")
    ]
    
    tech_specs = [
        (f"{name} 표준 사양", f"WBS {wbs} 설계도서 및 시방 규격 완벽 일치", "작업 착수 전/중", "오차 0%"),
        ("전기 절연 및 접지 기준", "절연저항 ≥ 5MΩ (DC 1,000V), 접지저항 R ≤ 1.0Ω", "공정 전 단계", "R ≤ 1.0Ω"),
        ("기기 취부 및 체결 토크", "규정 토크값(N·m) 100% 토크렌치 체결 및 마킹", "설치 시 전수", "토크 오차 ±5%"),
        ("안전 및 방화 구획", "내화 2시간 Fire-Stop 밀폐 씰링 및 절연 보호커버", "마감 시 전수", "합격 기준 100%")
    ]
    
    steps = [
        ("STEP 1 WHAT", f"{name} 핵심 사전 요건 및 도서 검토 (WHAT TO REVIEW)", [
            f"WBS {wbs} 관련 최신 설계도서, 시방서 및 KEC 규정을 정밀 검토합니다.",
            "사전 승인된 자재공급원 승인서 및 공인기관 시험성적서를 1:1 대조합니다.",
            "현장 여건과 설계도서의 불일치 사항을 사전에 도출하여 감리원 보고를 완료합니다."
        ]),
        ("STEP 2 WHEN", f"적기 시공 타이밍 및 선행공정 확인 (WHEN TO PROCEED)", [
            "선행 토목/건축 구조물 양생 및 인수인계 완료 상태를 사전 실측합니다.",
            "작업 투입 전 기상 조건(강우/습도) 및 정전 작업 승인 시간을 엄격히 확인합니다.",
            "간섭 공종과의 동시 작업 위험을 배제하고 안전작업허가서(PTW)를 발급받습니다."
        ]),
        ("STEP 3 WHO", f"공종별 책임자 및 안전관리자 지정 (WHO TO EXECUTE)", [
            "전기 분야 특급 엔지니어 및 활선/특고압 전문 자격자를 전담 배치합니다.",
            "안전관리자 입회 하에 작업 전 위험성평가(TBM) 및 안전교육을 실시합니다.",
            "책임감리원의 입회 검측 일정에 맞춰 실시간 검측 요청서를 접수합니다."
        ]),
        ("STEP 4 WHERE", f"현장 설치 구역 및 장비 안전거리 확보 (WHERE TO DEPLOY)", [
            "변전소, 전기실, 전차선로 및 정거장 현장 작업 구역에 안전 펜스를 설치합니다.",
            "특고압 충전부와의 법정 이격거리(≥300mm 이상) 및 절연 차폐를 완료합니다.",
            "장비 반입로 및 비상 대피 동선을 100% 확보하고 비상연락망을 게시합니다."
        ]),
        ("STEP 5 HOW", f"표준 시공 절차 및 3자 합동 검측 체결 (HOW TO VERIFY & SIGN)", [
            f"{name}에 명시된 공학 시험 및 계측(토크, 저항, 전압)을 정밀 수행합니다.",
            "검측 사진(전/중/후)을 채증하고 12대 체크리스트에 1:1 판정 결과를 기록합니다.",
            "현장대리인, 감리원 및 관련 엔지니어 3자 서명/날인을 완료하고 PMIS에 등재합니다."
        ])
    ]
    
    glossary = {
        "elec_safety": ("⚡ 특고압 전기 안전 및 KEC 기준", "전기설비 기술기준 및 한국전기설비규정(KEC)에 따른 감전보호, 과전류차단, 절연협조 및 특고압 접근 한계거리 준수 수칙입니다."),
        "grounding_sys": ("🌐 공통/통합 접지 시스템 (R ≤ 1.0Ω)", "트램 전철전력, 변전소, 전차선로 지지물 및 신호/통신 설비를 등전위 본딩하여 이상전압 및 낙뢰로부터 기기를 완벽 보호하는 접지망입니다."),
        "quality_sign": ("📝 책임감리원 3자 합동 검측 및 PMIS 등재", "시공사 현장대리인, 전기 책임기술자, 책임감리원이 현장에 동시 입석하여 체크리스트를 대조하고 전산 승인하는 공정 무결성 체결 절차입니다.")
    }
    
    diagram_title = f"[WBS {wbs}] {name} 2D Visual 정밀 공학 도식"
    diagram_svg = f'''<svg id="svg_r3_{num}" viewBox="0 0 550 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="550" height="180" fill="#f8fafc"/>
    <rect x="25" y="20" width="230" height="120" fill="#ffffff" stroke="#2563eb" stroke-width="2" rx="8"/>
    <text x="140" y="45" font-size="13" font-weight="black" fill="#1d4ed8" text-anchor="middle">{tag1}</text>
    <text x="45" y="75" font-size="11" font-weight="bold" fill="#334155">• KEC 규격 & 설계도서 100% 대조</text>
    <text x="45" y="98" font-size="11" font-weight="bold" fill="#334155">• 자재 성적서 원본 및 승인서 확인</text>

    <path d="M 260 80 L 290 80" stroke="#2563eb" stroke-width="3"/>
    <polygon points="290,75 300,80 290,85" fill="#2563eb"/>

    <rect x="295" y="20" width="230" height="120" fill="#ffffff" stroke="#059669" stroke-width="2" rx="8"/>
    <text x="410" y="45" font-size="13" font-weight="black" fill="#047857" text-anchor="middle">{tag2}</text>
    <text x="315" y="75" font-size="11" font-weight="bold" fill="#334155">• 정밀 계측(절연/접지/토크) 1:1 검측</text>
    <text x="315" y="98" font-size="11" font-weight="bold" fill="#334155">• 3자 합동 서명 & PMIS 즉시 등재</text>
    <text x="275" y="162" font-size="13" font-weight="black" fill="#0f172a" text-anchor="middle">{name} 표준 공정 완료 및 감리원 승인 완수</text>
</svg>'''

    checklist_items = [
        ("사전 도서 대조", f"{name} 관련 최신 승인도면 및 KEC 기술기준에 따라 사전 검토를 철저히 수행하였는가?"),
        ("자재 품질 확인", "투입 기자재의 KS/KRSA 인증서 및 공인기관 시험성적서 원본 일치 여부를 확인하였는가?"),
        ("선행공정 인계", "선행 구조물(토목/건축)의 층고, 패드 수평도(±2mm) 및 트렌치 상태를 점검하였는가?"),
        ("특고압 안전거리", "충전부 접근 한계거리 확보 및 절연보호구 착용 상태를 작업 전 점검하였는가?"),
        ("접지저항 측정", "공통접지 단자함 연결 상태 및 접지저항 기준치(R ≤ 1.0Ω)를 만족하였는가?"),
        ("절연저항 검측", "케이블 및 모선 절연저항(DC 1,000V 인가 시 ≥ 5MΩ) 측정을 전수 수행하였는가?"),
        ("볼트 체결 토크", "규정 토크값에 따라 토크렌치로 정밀 체결하고 풀림방지 마킹을 완료하였는가?"),
        ("배관/배선 정돈", "케이블 굴절반경(R ≥ 10D) 및 트레이 점유율(≤40%) 규격을 철저히 준수하였는가?"),
        ("방화구획 씰링", "벽체 및 바닥 관통부 내화 2시간 이상의 방화 충전재(Fire-Stop) 밀폐 시공을 완료하였는가?"),
        ("인터페이스 확인", "신호/통신/궤도/차량과의 이격거리(≥300mm) 및 간섭 배제 조치를 확인하였는가?"),
        ("사진 채증 완료", "시공 전, 시공 중, 시공 후의 주요 공정 상태를 다각도에서 촬영 채증하였는가?"),
        ("3자 서명 날인", "시공사, 전기책임자 및 책임감리원 3자 입석 검측 후 체크리스트 서명/날인을 완료하였는가?")
    ]
    
    return {
        "num": num,
        "folder": folder,
        "wbs": wbs,
        "name": name,
        "subtitle": subtitle,
        "overview": overview,
        "kpi": kpi,
        "tech_specs": tech_specs,
        "steps": steps,
        "glossary": glossary,
        "diagram_title": diagram_title,
        "diagram_svg": diagram_svg,
        "checklist_items": checklist_items
    }

def render_standard_html(task):
    kpi_cards = ""
    for title, desc in task["kpi"]:
        kpi_cards += f'''
            <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl">
                <span class="text-xs font-bold text-slate-500 block uppercase">{title}</span>
                <span class="text-sm font-bold text-blue-900 mt-1 block">{desc}</span>
            </div>'''
            
    spec_rows = ""
    for item, spec, cycle, tol in task["tech_specs"]:
        spec_rows += f'''
            <tr class="hover:bg-slate-50">
                <td class="border border-slate-200 p-3 font-semibold text-slate-900">{item}</td>
                <td class="border border-slate-200 p-3 font-medium text-slate-700">{spec}</td>
                <td class="border border-slate-200 p-3 text-center text-slate-600">{cycle}</td>
                <td class="border border-slate-200 p-3 text-center font-bold text-blue-600">{tol}</td>
            </tr>'''

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전기분야 - {task["name"]} 마스터 기술 표준서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS {task["wbs"]} Standard</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">전기설비 & 전철전력 엔지니어링 표준서</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{task["name"]} 마스터 표준서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"{task["subtitle"]}"</p>
        </div>
    </div>
    
    <div class="p-6 sm:p-10 space-y-10">
        <!-- 개요 카드 -->
        <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-blue-950 mb-2">📌 공종 개요 및 업무 관할</h3>
            <p class="text-sm text-blue-900 leading-relaxed">
                {task["overview"]}
            </p>
        </div>

        <!-- KPI 그리드 -->
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-l-4 border-blue-600 pl-3">핵심 엔지니어링 관리 지표 (KPI)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                {kpi_cards}
            </div>
        </div>

        <!-- 기술 기준 및 사양 테이블 -->
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-l-4 border-blue-600 pl-3">기술 기준 및 품질 사양</h3>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse border border-slate-200 text-xs sm:text-sm">
                    <thead>
                        <tr class="bg-slate-100 text-slate-700">
                            <th class="border border-slate-200 p-3">표준 항목</th>
                            <th class="border border-slate-200 p-3">설계 및 공학 기준치</th>
                            <th class="border border-slate-200 p-3 text-center">점검 주기</th>
                            <th class="border border-slate-200 p-3 text-center">허용 오차</th>
                        </tr>
                    </thead>
                    <tbody>
                        {spec_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 표준 작업 절차 가이드 -->
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-4 border-l-4 border-blue-600 pl-3">표준 시공 및 검측 프로세스</h3>
            <div class="space-y-3">
                <div class="flex items-start gap-4 p-4 rounded-xl border border-slate-200 bg-slate-50">
                    <span class="bg-blue-600 text-white font-bold text-xs px-2.5 py-1 rounded">PHASE 1</span>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">사전 도서 대조 & 인터페이스 회의</h4>
                        <p class="text-xs text-slate-600 mt-1">KEC 규정, 수전 계획, 토목/건축 슬리브 위치 및 3자 합동 인터페이스 사전 검토 완료</p>
                    </div>
                </div>
                <div class="flex items-start gap-4 p-4 rounded-xl border border-slate-200 bg-slate-50">
                    <span class="bg-blue-600 text-white font-bold text-xs px-2.5 py-1 rounded">PHASE 2</span>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">현장 정밀 실측 & 기자재 반입 검수</h4>
                        <p class="text-xs text-slate-600 mt-1">패드 수평도(±2mm), 충전부 이격거리 확보 및 공인기관 시험성적서 원본 대조 검측</p>
                    </div>
                </div>
                <div class="flex items-start gap-4 p-4 rounded-xl border border-slate-200 bg-slate-50">
                    <span class="bg-blue-600 text-white font-bold text-xs px-2.5 py-1 rounded">PHASE 3</span>
                    <div>
                        <h4 class="font-bold text-slate-900 text-sm">표준 시공 & 3자 합동 검측 날인</h4>
                        <p class="text-xs text-slate-600 mt-1">규정 토크 체결, 절연/접지저항 측정 및 책임감리원 서명/날인 후 PMIS 등재 완료</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
'''

def render_guideline_html(task):
    step_cards = ""
    for step_num, (step_title, step_head, step_items) in enumerate(task["steps"], 1):
        items_li = "".join([f"<li>{it}</li>" for it in step_items])
        step_cards += f'''
                <!-- {step_title} -->
                <div class="bg-white p-6 rounded-2xl border border-blue-200 shadow-sm space-y-3">
                    <div class="flex items-center gap-3">
                        <span class="bg-blue-600 text-white font-bold text-xs px-2.5 py-1 rounded">{step_title}</span>
                        <h3 class="font-bold text-base text-slate-900">{step_head}</h3>
                    </div>
                    <ul class="list-disc pl-5 text-slate-700 space-y-1.5 text-xs font-medium leading-relaxed">
                        {items_li}
                    </ul>
                </div>'''

    glossary_items_js = ""
    for key, (g_title, g_desc) in task["glossary"].items():
        glossary_items_js += f"""
    '{key}': {{
        title: '{g_title}',
        desc: '{g_desc}'
    }},"""

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{task["name"]} 수행지침서</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; }}
        
    .term-highlight {{
        color: #0284c7 !important;
        font-weight: 700 !important;
        border-bottom: 2px dashed #0284c7 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        padding: 0 2px !important;
    }}
    .term-highlight:hover {{
        background: #e0f2fe !important;
        color: #0369a1 !important;
        border-radius: 4px !important;
    }}
    .clickable-diagram {{
        cursor: zoom-in !important;
        transition: all 0.25s ease !important;
        position: relative !important;
    }}
    .clickable-diagram:hover {{
        transform: scale(1.015) !important;
        box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15) !important;
    }}
    .clickable-diagram::after {{
        content: "🔍 클릭하여 대형 확대보기";
        position: absolute;
        bottom: 8px;
        right: 12px;
        background: rgba(15, 23, 42, 0.75);
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
        pointer-events: none;
        opacity: 0.85;
        transition: opacity 0.2s;
    }}
    .clickable-diagram:hover::after {{
        opacity: 1;
        background: rgba(2, 132, 199, 0.9);
    }}
    .glossary-modal, .zoom-modal {{
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(6px);
    }}
    .glossary-modal.active, .zoom-modal.active {{
        display: flex !important;
        align-items: center;
        justify-content: center;
    }}
    .glossary-modal-content, .zoom-modal-content {{
        background-color: #ffffff;
        margin: auto;
        padding: 28px;
        border-radius: 20px;
        width: 92%;
        max-width: 720px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        border: 1px solid #cbd5e1;
        position: relative;
        animation: modalFadeIn 0.25s ease-out;
    }}
    .zoom-modal-content {{
        max-width: 1100px !important;
        width: 95% !important;
    }}
    @keyframes modalFadeIn {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    .glossary-close, .zoom-close {{
        position: absolute;
        right: 20px;
        top: 16px;
        color: #64748b;
        font-size: 28px;
        font-weight: 800;
        cursor: pointer;
        transition: color 0.2s;
    }}
    .glossary-close:hover, .zoom-close:hover {{
        color: #0f172a;
    }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased p-6 sm:p-10">
<div class="max-w-5xl mx-auto bg-white shadow-2xl rounded-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-950 to-slate-900 opacity-80"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-3 mb-2">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Dongtan Tram WBS {task["wbs"]} Guideline</span>
                <span class="bg-white text-slate-950 text-xs font-bold px-3 py-1 rounded-full">전기설비 마스터 작업 수행지침</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black tracking-tight">{task["name"]} 수행지침서</h1>
            <p class="text-blue-200 mt-2 text-sm sm:text-base">"{task["subtitle"]}"</p>
        </div>
    </div>

    <div class="p-6 sm:p-10 space-y-10">
        <!-- 1. 핵심 수행 원칙 및 배경 -->
        <div class="bg-blue-50/80 border border-blue-200 rounded-2xl p-6 shadow-sm space-y-3">
            <h3 class="text-base font-bold text-blue-950 flex items-center gap-2">
                <span>📘</span> {task["name"]} 엔지니어링 수행 원칙
            </h3>
            <p class="text-xs text-blue-900 leading-relaxed font-medium">
                본 지침서는 동탄트램 현장 기술자가 실무에서 즉시 적용할 수 있도록 <span class="term-highlight" onclick="openGlossary('elec_safety')">한국전기설비규정(KEC)</span>, <span class="term-highlight" onclick="openGlossary('grounding_sys')">공통 접지 시스템</span> 및 <span class="term-highlight" onclick="openGlossary('quality_sign')">3자 합동 검측</span> 절차를 체계화한 엔지니어링 가이드입니다.
            </p>
        </div>

        <!-- 2. 단계별 마스터 절차 카드 -->
        <div class="space-y-4">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">2.</span> 단계별 마스터 절차 (Step-by-Step Execution Guide)
            </h2>
            <div class="space-y-4">
                {step_cards}
            </div>
        </div>

        <!-- 3. 2D VISUAL SVG DIAGRAM -->
        <div class="space-y-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4 border-b-2 border-blue-600 pb-2">
                <span class="text-blue-600">3.</span> 2D Visual 기술 도식 (Enriched 2D SVG)
            </h2>
            <div class="clickable-diagram bg-slate-50 p-5 rounded-2xl border border-slate-200 shadow-inner" onclick="openDiagramZoom('svg_r3_{task['num']}', '{task['diagram_title']}')">
                {task["diagram_svg"]}
            </div>
        </div>
    </div>
</div>

<!-- 용어 사전 모달 -->
<div class="glossary-modal" id="glossaryModal">
    <div class="glossary-modal-content">
        <span class="glossary-close" onclick="closeGlossaryModal()">&times;</span>
        <h3 id="modalTitle" style="font-size: 1.25rem; font-weight: 800; color: #1e3a8a; margin-top: 0; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">용어 및 엔지니어링 기술 해설</h3>
        <div class="modal-body">
            <p id="modalDescription" style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 0; word-break: keep-all;"></p>
        </div>
    </div>
</div>

<!-- 대형 도식 확대 모달 -->
<div class="zoom-modal" id="zoomModal" onclick="closeZoomModalOutside(event)">
    <div class="zoom-modal-content" onclick="event.stopPropagation()">
        <span class="zoom-close" onclick="closeZoomModal()">&times;</span>
        <h3 id="zoomTitle" style="font-size: 1.35rem; font-weight: 900; color: #0f172a; margin-top: 0; margin-bottom: 16px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: left;">🔍 도식 대형 고화질 정밀 보기</h3>
        <div id="zoomBody" class="bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-inner flex justify-center items-center overflow-auto min-h-[400px]">
        </div>
        <div style="margin-top: 14px; text-align: right; font-size: 0.85rem; font-weight: 700; color: #64748b;">
            💡 팁: ESC 키를 누르시거나 닫기(×) 버튼을 누르면 이전 화면으로 복귀합니다.
        </div>
    </div>
</div>

<script>
const glossaryData = {{{glossary_items_js}
}};

function openGlossary(termKey) {{
    const data = glossaryData[termKey];
    if (!data) return;
    document.getElementById('modalTitle').innerText = data.title;
    document.getElementById('modalDescription').innerText = data.desc;
    document.getElementById('glossaryModal').classList.add('active');
}}
function closeGlossaryModal() {{
    document.getElementById('glossaryModal').classList.remove('active');
}}

function openDiagramZoom(elementId, titleText) {{
    const srcEl = document.getElementById(elementId);
    if (!srcEl) return;
    
    const zoomBody = document.getElementById('zoomBody');
    document.getElementById('zoomTitle').innerText = "🔍 " + (titleText || "도식 대형 정밀 보기");
    
    zoomBody.innerHTML = srcEl.outerHTML;
    
    const innerSvg = zoomBody.querySelector('svg');
    if (innerSvg) {{
        innerSvg.setAttribute('width', '100%');
        innerSvg.setAttribute('height', '550px');
        innerSvg.style.maxWidth = '1050px';
    }}
    
    document.getElementById('zoomModal').classList.add('active');
}}

function closeZoomModal() {{
    document.getElementById('zoomModal').classList.remove('active');
}}

function closeZoomModalOutside(event) {{
    if (event.target.id === 'zoomModal') {{
        closeZoomModal();
    }}
}}

window.addEventListener('keydown', function(event) {{
    if (event.key === 'Escape') {{
        closeGlossaryModal();
        closeZoomModal();
    }}
}});
</script>

</body>
</html>
'''

def render_checklist_html(task):
    chk_rows = ""
    for idx, (cat, q_text) in enumerate(task["checklist_items"], 1):
        if not q_text.endswith("는가?"):
            q_text = q_text.rstrip("?. ") + "하였는가?"
            
        chk_rows += f'''
                <tr class="hover:bg-slate-50 border-b border-slate-100">
                    <td class="p-4 text-center font-bold text-slate-500 text-xs">{idx}</td>
                    <td class="p-4 font-bold text-slate-800 text-xs sm:text-sm">{cat}</td>
                    <td class="p-4 font-medium text-slate-700 text-xs sm:text-sm leading-relaxed">{q_text}</td>
                    <td class="p-4 text-center">
                        <span class="inline-flex gap-2">
                            <label class="inline-flex items-center text-xs font-semibold text-emerald-700"><input type="checkbox" checked class="rounded border-slate-300 mr-1"> 적합</label>
                            <label class="inline-flex items-center text-xs font-semibold text-rose-700"><input type="checkbox" class="rounded border-slate-300 mr-1"> 부적합</label>
                        </span>
                    </td>
                    <td class="p-4 text-center font-medium text-slate-500 text-xs">-</td>
                </tr>'''

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{task["name"]} 마스터 체크리스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; background-color: #f8fafc; }}
    </style>
</head>
<body class="p-6 sm:p-10 text-slate-800">
<div class="max-w-5xl mx-auto space-y-6">

    <!-- 대제목 & WBS 코드 -->
    <div class="flex justify-between items-end border-b-2 border-slate-900 pb-4">
        <div>
            <h1 class="text-3xl font-black text-slate-900 tracking-tight">{task["name"]} 마스터 체크리스트</h1>
        </div>
        <div class="text-right">
            <span class="text-blue-600 font-bold text-sm">WBS Code {task["wbs"]} | 전기 검측대장</span>
        </div>
    </div>

    <!-- 📋 상단 안내 상자 (Notice Box) -->
    <div class="bg-blue-50/80 border border-blue-200 rounded-2xl p-6 shadow-sm space-y-2">
        <h3 class="text-base font-bold text-blue-950 flex items-center gap-2">
            <span>📋</span> {task["name"]} 12대 정밀 검측대장
        </h3>
        <p class="text-xs text-blue-900 leading-relaxed font-medium">
            본 체크리스트는 KEC(한국전기설비규정), 철도설계기준 및 동탄트램 특기시방서 기준을 12개 정밀 점검 항목으로 확장 구성하였으며, 모든 항목의 문장 끝은 예외 없이 질문형 어미(<strong class="text-blue-700">~하였는가?</strong>)로 100% 정형화되었습니다.
        </p>
    </div>

    <!-- 3-Column 마스터 검측 테이블 -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden">
        <table class="w-full border-collapse">
            <thead>
                <tr class="bg-slate-100 text-slate-700 text-xs sm:text-sm font-bold border-b border-slate-200">
                    <th class="p-4 text-center w-12">NO</th>
                    <th class="p-4 text-left w-36">구분</th>
                    <th class="p-4 text-left">검측 및 확인 세부 항목 (질문형 어미 준수)</th>
                    <th class="p-4 text-center w-36">검측 결과</th>
                    <th class="p-4 text-center w-28">조치 사항</th>
                </tr>
            </thead>
            <tbody>
                {chk_rows}
            </tbody>
        </table>
    </div>

    <!-- 점검자 및 감리원 서명란 -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row justify-between items-center gap-4 text-xs font-semibold text-slate-700">
        <div>
            <span>📌 종합 판정 결과: </span>
            <span class="text-blue-600 font-bold text-sm ml-2">적합 (PASS)</span>
        </div>
        <div class="flex gap-8">
            <div>점검자(시공책임): <span class="border-b border-slate-400 pb-1 px-4 inline-block ml-1">이전기 (인)</span></div>
            <div>확인자(책임감리): <span class="border-b border-slate-400 pb-1 px-4 inline-block ml-1">김철도 (인)</span></div>
        </div>
    </div>
</div>
</body>
</html>
'''

def main():
    print("=== Starting Electric HTML Bulk Upgrade Generator ===")
    total_generated = 0
    
    for cfg in DEFAULT_TASKS_CONFIG:
        task_num = cfg[0]
        if task_num in TASKS_DATA:
            task = TASKS_DATA[task_num]
        else:
            task = build_task_data(cfg)
            
        folder_name = task["folder"]
        task_dir = os.path.join(BASE_DIR, folder_name)
        
        if not os.path.exists(task_dir):
            print(f"Warning: Directory not found: {task_dir}")
            continue
            
        std_dir = os.path.join(task_dir, "표준서")
        gd_dir = os.path.join(task_dir, "수행지침")
        chk_dir = os.path.join(task_dir, "체크리스트")
        
        os.makedirs(std_dir, exist_ok=True)
        os.makedirs(gd_dir, exist_ok=True)
        os.makedirs(chk_dir, exist_ok=True)
        
        # 1. 표준서 파일
        std_file = os.path.join(std_dir, f"{task['name']}_표준서.html")
        std_content = render_standard_html(task)
        with open(std_file, "w", encoding="utf-8") as f:
            f.write(std_content)
        total_generated += 1
        
        # 2. 수행지침서 파일
        gd_file = os.path.join(gd_dir, f"{task['name']}_수행지침.html")
        gd_content = render_guideline_html(task)
        with open(gd_file, "w", encoding="utf-8") as f:
            f.write(gd_content)
        total_generated += 1
        
        # 3. 체크리스트 파일
        chk_file = os.path.join(chk_dir, f"{task['name']}_체크리스트.html")
        chk_content = render_checklist_html(task)
        with open(chk_file, "w", encoding="utf-8") as f:
            f.write(chk_content)
        total_generated += 1
        
        print(f"[{task_num:2d}/33] Generated WBS {task['wbs']:9s} ({task['name']}) -> 3 files")
        
    print(f"\n=== Bulk Generation Completed: {total_generated} HTML files created successfully! ===")

if __name__ == "__main__":
    main()
