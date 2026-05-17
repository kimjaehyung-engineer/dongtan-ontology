import argparse
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def extract_value_from_pdf(pdf_path, target_metric):
    """
    [STEP 2] 실제 PDF 문서에서 값을 추출하는 엔진 (Gemini API 또는 PDF 파서 위치)
    ※ 현재는 자동화 파이프라인 시연을 위해 '기준 미달' 상태의 Mock 데이터를 반환합니다.
    """
    print(f"   [문서 분석 중...] {pdf_path}")
    print(f"   [타겟 데이터 찾기...] '{target_metric}' 수치 스캔 중...")
    
    # 향후 여기에 PyMuPDF(fitz) 또는 Gemini 1.5 Pro API를 연결하여
    # PDF 내용을 통째로 넘기고 수치를 뽑아오는 로직이 들어갑니다.
    
    mock_extracted_data = {
        "곡선반경": 15.0, # (기준 20m에 미달하도록 세팅)
        "플랫폼 폭": 1.8, # (기준 2.0m에 미달하도록 세팅)
        "구배": 3.0       # (기준 2.5‰ 초과하도록 세팅)
    }
    
    return mock_extracted_data.get(target_metric, None)

def validate_station_design(station_keyword):
    """[STEP 3] 추출된 값을 기준과 비교하고 위배(VIOLATION) 관계를 생성"""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # 1. 대상 정거장과 연결된 문서 및 기준들을 모두 가져옵니다.
        q_find = """
        MATCH (n)-[:HAS_DOCUMENT]->(d:Document)
        MATCH (n)-[:TECHNICAL_REQ]->(s:Standard)
        WHERE n.name CONTAINS $keyword
        RETURN n.name as station, d.file_path as doc_path, s.name as std_name,
               s.target_metric as metric, s.operator as op, s.limit_value as limit, s.unit as unit
        """
        results = session.run(q_find, keyword=station_keyword)
        records = list(results)
        
        if not records:
            print(f"RODO: '{station_keyword}'와 연결된 문서 및 기준을 찾을 수 없습니다.")
            return
            
        print(f"\n🚀 RODO: [{records[0]['station']}] 자동 설계 검증 파이프라인 가동\n")
        
        for rec in records:
            station = rec['station']
            doc_path = rec['doc_path']
            std_name = rec['std_name']
            metric = rec['metric']
            op = rec['op']
            limit = float(rec['limit'])
            unit = rec['unit']
            
            print(f"👉 [검증 대상]: {std_name} (기준: {metric} {op} {limit}{unit})")
            
            # 문서에서 실제 설계치 추출
            actual_value = extract_value_from_pdf(doc_path, metric)
            
            if actual_value is None:
                print("   [결과] 문서에서 해당 수치를 찾지 못했습니다.\n")
                continue
                
            print(f"   [추출된 실제 설계값]: {actual_value}{unit}")
            
            # 비교 연산 수행
            is_compliant = False
            if op == ">=": is_compliant = actual_value >= limit
            elif op == "<=": is_compliant = actual_value <= limit
            elif op == "==": is_compliant = actual_value == limit
            
            if is_compliant:
                print("   ✅ [판단]: 기준 충족 (PASS)\n")
            else:
                print("   🚨 [판단]: 기준 미달 (VIOLATION) - 지식망에 리스크 업데이트 진행")
                
                # 위배 사항을 지식망에 업데이트 (VIOLATION 관계 생성)
                q_violation = """
                MATCH (n), (s:Standard)
                WHERE n.name = $station AND s.name = $std_name
                MERGE (n)-[v:VIOLATION]->(s)
                SET v.actual_value = $actual,
                    v.issue_description = '설계보고서 수치 기준 미달',
                    v.detected_from = $doc_path
                """
                session.run(q_violation, station=station, std_name=std_name, actual=actual_value, doc_path=doc_path)
                print("   [업데이트 완료] 지식망에 VIOLATION 관계선이 추가되었습니다.\n")
                
    driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="설계 문서 자동 검증 에이전트")
    parser.add_argument("keyword", type=str, help="검증할 정거장 키워드 (예: 103, 동탄역)")
    args = parser.parse_args()
    
    validate_station_design(args.keyword)
