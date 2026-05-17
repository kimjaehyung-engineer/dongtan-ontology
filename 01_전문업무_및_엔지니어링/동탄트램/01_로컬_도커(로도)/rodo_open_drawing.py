import os
import argparse
import webbrowser
import urllib.parse
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def create_dummy_files():
    """테스트용 빈 파일 생성 (실제 파일이 없을 경우 오류 방지)"""
    base_dir = "C:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/동탄트램/도면"
    os.makedirs(base_dir, exist_ok=True)
    
    files = [
        "DT-ARC-001_정거장평면도.pdf",
        "DT-ELEC-100_급전계통도.pdf",
        "DT-VEH-500_차량유지보수매뉴얼.pdf"
    ]
    for f in files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"This is a placeholder for {path}\n")

def open_drawing(keyword):
    """키워드로 노드를 검색하고 연결된 도면의 관련 페이지들을 모두 띄움"""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # 통합 스키마 지원: EVIDENCE_IN/HAS_DOCUMENT 관계선 및 absolute_path/file_path 속성 통합 지원
        q = """
        MATCH (n)-[r]->(d:Document)
        WHERE (n.name CONTAINS $keyword OR d.name CONTAINS $keyword)
          AND (type(r) = 'HAS_DOCUMENT' OR type(r) = 'EVIDENCE_IN')
        RETURN n.name as name, 
               coalesce(d.absolute_path, d.file_path) as file_path, 
               coalesce(r.pages, [r.page]) as pages
        ORDER BY case when r.page is null and r.pages is null then 0 else 1 end DESC, r.page DESC, r.pages DESC
        LIMIT 1
        """
        result = session.run(q, keyword=keyword)
        record = result.single()
        
        if record:
            node_name = record['name']
            file_path = record['file_path']
            pages = record['pages']
            
            print(f"RODO: [FOUND] Node: {node_name}")
            print(f"RODO: Document: {os.path.basename(file_path)}")
            
            if not file_path or file_path == "경로 미지정":
                print("RODO: [WARN] Path not specified.")
                driver.close()
                return
                
            # 콘솔에 깔끔하게 파일명과 페이지 번호만 출력 (CP949 호환용 이모지 제거)
            print("\n" + "="*50)
            print("[SEARCH RESULT]")
            print(f"- Node: {node_name}")
            print(f"- Document: {os.path.basename(file_path)}")
            
            # 페이지 정보 가공 및 출력
            if pages is not None:
                if not isinstance(pages, list):
                    pages = [pages]
                pages = [p for p in pages if p is not None and str(p).strip() != ""]
                
            if pages:
                print(f"- Pages: {', '.join(map(str, pages))} page")
            else:
                print("- Pages: [No Page Info]")
            print("="*50 + "\n")
            
        else:
            print(f"\n[NOT FOUND] No document found for keyword: '{keyword}'\n")

    driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="지식망 기반 도면 멀티페이지 뷰어")
    parser.add_argument("keyword", type=str, help="검색할 기술 키워드 (예: 건축, 궤도)")
    args = parser.parse_args()
    
    create_dummy_files() # 테스트용 파일 준비
    open_drawing(args.keyword)
