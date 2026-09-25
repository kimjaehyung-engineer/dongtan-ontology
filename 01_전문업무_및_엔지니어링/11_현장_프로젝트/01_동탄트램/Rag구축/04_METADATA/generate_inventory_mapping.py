import os
import re
from datetime import datetime
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

WORKSPACE_ROOT = Path(r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축")
SOURCE_DIR = WORKSPACE_ROOT / "01_SOURCE_DOCUMENTS"
OUTPUT_FILE = WORKSPACE_ROOT / "04_METADATA" / "문서_전처리_매핑대장.xlsx"

def extract_date(filename, mtime):
    # 파일명 내 6자리 또는 8자리 또는 4자리 날짜 패턴 탐색
    # 20230805, 230805, 0805 등
    m8 = re.search(r'(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})', filename)
    if m8:
        return f"{m8.group(1)[2:]}{m8.group(2)}{m8.group(3)}"
    
    m6 = re.search(r'\b(2[0-5])(\d{2})(\d{2})\b', filename)
    if m6:
        return f"{m6.group(1)}{m6.group(2)}{m6.group(3)}"
    
    m4 = re.search(r'\((\d{2})(\d{2})\)|_(\d{2})(\d{2})|_(\d{4})', filename)
    if m4:
        # e.g. 0805 -> 파일 수정년도와 결합
        dt = datetime.fromtimestamp(mtime)
        year_prefix = str(dt.year)[2:]
        nums = [g for g in m4.groups() if g]
        if len(nums) == 2:
            return f"{year_prefix}{nums[0]}{nums[1]}"
        elif len(nums) == 1 and len(nums[0]) == 4:
            return f"{year_prefix}{nums[0]}"
            
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime("%y%m%d")

def clean_title(filename):
    name = Path(filename).stem
    # 접두 번호 및 특수문자 정돈
    name = re.sub(r'^[#\d+._\s-]+', '', name)
    name = re.sub(r'\(\d+\)$', '', name) # (1) 같은 복사본 표기
    name = re.sub(r'[\(\)\[\]#]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    if not name:
        name = Path(filename).stem
    return name

def analyze_file(file_path):
    rel_path = file_path.relative_to(WORKSPACE_ROOT)
    rel_source_path = file_path.relative_to(SOURCE_DIR)
    parts = rel_source_path.parts
    
    # 1. 설계 단계 (Stage)
    stage_part = parts[0] if len(parts) > 0 else "공통"
    if "기본계획" in stage_part:
        stage = "기본계획"
    elif "기술제안" in stage_part or "기본설계" in stage_part:
        stage = "기술제안"
    elif "실시설계" in stage_part:
        stage = "실시설계"
    else:
        stage = "기타"
        
    # 2. 대분류 / 세부공종 (Category)
    folder_str = " / ".join(parts[1:-1]) if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
    full_str = f"{folder_str} {file_path.name}"
    
    category = "일반기타"
    if "시추주상도" in full_str:
        category = "시추주상도"
    elif "지반조사" in full_str:
        category = "지반조사보고서"
    elif "지반설계" in full_str:
        category = "지반설계보고서"
    elif "현장시험" in full_str or "유향유속" in full_str or "재하시험" in full_str or "수압시험" in full_str:
        category = "현장시험"
    elif "실내시험" in full_str:
        category = "실내시험"
    elif "설계지반정수" in full_str:
        category = "설계지반정수"
    elif "도면" in full_str or file_path.suffix.lower() in ['.dwg', '.dxf']:
        category = "지반도면"
    elif "보강" in full_str:
        category = "보강공법"
    elif "계산" in full_str or "검토" in full_str:
        category = "계산검토서"
    elif "과업" in full_str or "입찰안내서" in full_str or "조건" in full_str:
        category = "과업기준"
    elif "수량" in full_str or "공사비" in full_str:
        category = "수량공사비"

    # 3. 위치 / 공구 (Location)
    location = "전구간"
    if "1공구" in full_str or "1-1" in full_str:
        location = "1공구"
    elif "2공구" in full_str or "2-1" in full_str:
        location = "2공구"
    elif "차량기지" in full_str or "GB-" in full_str or "NGB-" in full_str:
        location = "차량기지"
    elif "정거장" in full_str:
        m_st = re.search(r'(\d{3}정거장|정거장\s*\d+)', full_str)
        if m_st:
            location = m_st.group(1).replace(" ", "")
            
    # 4. 날짜 및 크기
    stat = file_path.stat()
    file_size_kb = round(stat.st_size / 1024, 1)
    file_size_mb = round(stat.st_size / (1024 * 1024), 2)
    doc_date = extract_date(file_path.name, stat.st_mtime)
    
    # 5. 확장자 및 변환 요건
    ext = file_path.suffix.lower()
    clean_name = clean_title(file_path.name)
    
    conv_required = "유지"
    target_ext = ext
    rag_target = "파싱대상(텍스트/표)"
    
    if ext == ".hwp":
        conv_required = "PDF 변환 필수 (HWP→PDF)"
        target_ext = ".pdf"
        rag_target = "파싱대상(텍스트/표)"
    elif ext == ".dwg":
        conv_required = "DXF 및 고해상도 PDF 변환 필요"
        target_ext = ".dxf"
        rag_target = "도면분석(DXF/PDF)"
    elif ext in [".xls", ".xlsm"]:
        conv_required = "표준 XLSX 변환 권장"
        target_ext = ".xlsx"
        rag_target = "표추출대상(TABLE)"
    elif ext in [".xlsx", ".csv"]:
        conv_required = "유지"
        rag_target = "표추출대상(TABLE)"
    elif ext == ".pdf":
        conv_required = "유지"
        if category == "시추주상도":
            rag_target = "주상도추출대상(PDF)"
        elif category == "지반도면":
            rag_target = "도면분석(PDF)"
        else:
            rag_target = "파싱대상(텍스트/표)"
    elif ext in [".jpg", ".png"]:
        conv_required = "유지"
        rag_target = "이미지/차트(OCR)"
    elif ext in [".grd", ".fss", ".sec", ".dat", ".ctb", ".pc3", ".ai"]:
        conv_required = "엔지니어링 원본 보존"
        rag_target = "메타데이터참조"
        
    # 6. 표준 파일명 조합
    # [단계]_[분류]_[위치]_[정제된문서명]_[YYMMDD]_v1.0[target_ext]
    std_filename = f"{stage}_{category}_{location}_{clean_name}_{doc_date}_v1.0{target_ext}"
    # 중복 문자 정리
    std_filename = re.sub(r'_+', '_', std_filename)
    
    return {
        "rel_path": str(rel_path),
        "curr_name": file_path.name,
        "ext": ext,
        "size_kb": file_size_kb,
        "size_mb": file_size_mb,
        "stage": stage,
        "category": category,
        "location": location,
        "date": doc_date,
        "std_filename": std_filename,
        "conv_required": conv_required,
        "rag_target": rag_target
    }

def main():
    files = list(SOURCE_DIR.rglob("*"))
    files = [f for f in files if f.is_file()]
    print(f"총 발견 파일 수: {len(files)}")
    
    records = []
    for f in files:
        records.append(analyze_file(f))
        
    # 엑셀 워크북 생성
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "문서_전처리_매핑대장"
    ws.views.sheetView[0].showGridLines = True
    
    headers = [
        "No", "설계단계", "대분류(공종)", "위치/공구", 
        "현재 파일명", "변환요건", "표준화 추천 파일명", 
        "RAG 타겟 분류", "현재 확장자", "파일크기(MB)", "추정일자", "현재 상대경로"
    ]
    
    ws.append(headers)
    
    # 스타일 정의
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="맑은 고딕", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="맑은 고딕", size=10)
    bold_data_font = Font(name="맑은 고딕", size=10, bold=True)
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    conv_fill_alert = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # 연노랑 (변환필요)
    conv_font_alert = Font(name="맑은 고딕", size=10, bold=True, color="C00000")
    
    for row_idx, r in enumerate(records, start=2):
        ws.append([
            row_idx - 1,
            r["stage"],
            r["category"],
            r["location"],
            r["curr_name"],
            r["conv_required"],
            r["std_filename"],
            r["rag_target"],
            r["ext"],
            r["size_mb"],
            r["date"],
            r["rel_path"]
        ])
        
        # 행 스타일링
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = thin_border
            
            # 중앙 정렬 컬럼들
            if col_idx in [1, 2, 3, 4, 8, 9, 11]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in [10]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
            # 변환 요건 강조
            if col_idx == 6 and "필" in r["conv_required"] or "필요" in r["conv_required"] or "권장" in r["conv_required"]:
                cell.fill = conv_fill_alert
                cell.font = conv_font_alert
                
            # 표준 추천 파일명 강조
            if col_idx == 7:
                cell.font = bold_data_font
                
    # 헤더 서식 적용
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    # 열 너비 자동 조정
    ws.column_dimensions['A'].width = 6   # No
    ws.column_dimensions['B'].width = 12  # 단계
    ws.column_dimensions['C'].width = 16  # 대분류
    ws.column_dimensions['D'].width = 12  # 위치
    ws.column_dimensions['E'].width = 40  # 현재 파일명
    ws.column_dimensions['F'].width = 25  # 변환요건
    ws.column_dimensions['G'].width = 50  # 표준 추천 파일명
    ws.column_dimensions['H'].width = 18  # RAG 타겟
    ws.column_dimensions['I'].width = 12  # 확장자
    ws.column_dimensions['J'].width = 12  # 크기
    ws.column_dimensions['K'].width = 12  # 일자
    ws.column_dimensions['L'].width = 55  # 상대경로
    
    # 필터 걸기
    ws.auto_filter.ref = f"A1:L{len(records) + 1}"
    
    # 통계 시트 추가
    ws_stat = wb.create_sheet(title="포맷별_변환통계")
    ws_stat.views.sheetView[0].showGridLines = True
    
    ws_stat.append(["구분", "항목", "파일수", "비율(%)", "조치 방안"])
    for col_idx in range(1, 6):
        cell = ws_stat.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    # 통계 집계
    from collections import Counter
    ext_counts = Counter([r["ext"] for r in records])
    stage_counts = Counter([r["stage"] for r in records])
    conv_counts = Counter([r["conv_required"] for r in records])
    
    stat_rows = []
    total = len(records)
    for ext, cnt in ext_counts.most_common():
        action = "유지"
        if ext == ".hwp": action = "PDF 일괄 변환"
        elif ext == ".dwg": action = "DXF / PDF 변환"
        elif ext in [".xls", ".xlsm"]: action = "XLSX 변환"
        elif ext in [".grd", ".fss", ".sec", ".dat"]: action = "엔지니어링 파일 메타 보존"
        stat_rows.append(["확장자별", ext, cnt, round(cnt/total*100, 1), action])
        
    for r_data in stat_rows:
        ws_stat.append(r_data)
        
    ws_stat.column_dimensions['A'].width = 15
    ws_stat.column_dimensions['B'].width = 15
    ws_stat.column_dimensions['C'].width = 12
    ws_stat.column_dimensions['D'].width = 12
    ws_stat.column_dimensions['E'].width = 30
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_FILE)
    print(f"매핑 대장 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
