import argparse
import webbrowser
import urllib.parse
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def view_violation(keyword):
    """키워드로 정거장을 검색하여 위배(VIOLATION) 리포트를 출력하고 원본 PDF를 브라우저로 엽니다."""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # 1. 대상 정거장과 VIOLATION 관계를 가져오고, VIOLATION에 기록된 출처 파일명을 바탕으로 Document 노드를 매칭합니다.
        q = """
        MATCH (n:Station)-[v:VIOLATION]->(s:Standard)
        WHERE n.name CONTAINS $keyword
        OPTIONAL MATCH (d:Document)
        WHERE v.source_file IS NOT NULL AND v.source_file <> '' AND d.file_path CONTAINS v.source_file
        RETURN n.name as station, 
               s.name as std_name, 
               s.target_metric as metric, 
               s.limit_value as limit_val, 
               s.unit as unit,
               v.actual_value as actual,
               v.issue_description as desc,
               v.source_file as source_file,
               v.page as page,
               d.file_path as doc_path
        """
        results = session.run(q, keyword=keyword)
        records = list(results)
        
        if not records:
            print(f"RODO: '{keyword}' 키워드를 가진 정거장의 위배(VIOLATION) 사항이 지식망에 없습니다.")
            driver.close()
            return
            
        print(f"\n==================================================")
        print(f" [!] RODO 설계 위배(VIOLATION) 스캐너 리포트 [!] ")
        print(f"==================================================")
        
        doc_opened = False
        
        for rec in records:
            station = rec['station']
            std_name = rec['std_name']
            metric = rec['metric']
            limit_val = rec['limit_val']
            unit = rec['unit']
            actual = rec['actual']
            desc = rec['desc']
            source_file = rec['source_file']
            page = rec['page']
            doc_path = rec['doc_path']
            
            print(f"\n[정거장]: {station}")
            print(f" - 위배 항목: {metric}")
            print(f" - 기준 수치: {limit_val}{unit}")
            print(f" - 실제 설계: {actual}{unit} (미달/초과)")
            print(f" - 리스크 사유: {desc}")
            if source_file:
                print(f" - 출처 기록: {source_file} (Page {page})")
            
            if doc_path:
                print(f" - 연결된 물리적 문서: {doc_path}")
                # 윈도우 기본 뷰어(Acrobat 등)는 #page 파라미터를 무시하므로, Chrome/Edge를 강제 호출합니다.
                if not doc_opened:
                    file_url = "file:///" + urllib.parse.quote(doc_path.replace("\\", "/"))
                    if page:
                        file_url += f"#page={page}"
                        
                    print(f"\n[!] RODO: 핀셋 매핑 성공! 정확한 원본 파일의 해당 페이지로 점프합니다...")
                    try:
                        import subprocess
                        import os
                        
                        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                        
                        if os.path.exists(chrome_path):
                            subprocess.Popen([chrome_path, file_url])
                            doc_opened = True
                            print(f"   -> Chrome 브라우저 팝업 성공! (페이지: {page})")
                        elif os.path.exists(edge_path):
                            subprocess.Popen([edge_path, file_url])
                            doc_opened = True
                            print(f"   -> Edge 브라우저 팝업 성공! (페이지: {page})")
                        else:
                            webbrowser.open(file_url)
                            doc_opened = True
                            print(f"   -> 기본 브라우저 팝업 성공! (페이지: {page})")
                    except Exception as e:
                        print(f"   -> 도면 열기 실패. Error: {e}")
            else:
                if source_file:
                    print(f" [WARNING] '{source_file}' 문서가 로컬(도면 폴더)에 존재하지 않아 팝업할 수 없습니다.")
                else:
                    print(f" [WARNING] 해당 정거장에 연결된 원본 문서(PDF) 경로가 없습니다.")

        print(f"==================================================\n")
            
    driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="설계 위배 사항 조회 및 원본 도면 오픈")
    parser.add_argument("keyword", type=str, help="검증할 정거장 키워드 (예: 107, 306, 201)")
    args = parser.parse_args()
    
    view_violation(args.keyword)
