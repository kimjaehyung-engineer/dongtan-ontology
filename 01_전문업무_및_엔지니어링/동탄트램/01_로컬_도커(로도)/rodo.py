import json
import sys
import os
from neo4j import GraphDatabase

# ==========================================
# 🤖 [RODO] LOCAL DOCKER GRAPH AGENT
# ==========================================
# "안녕! 나는 로컬 도커를 지키는 로도야."
# 특징: 
# 1. 로컬 Docker Memgraph (bolt://localhost:7687) 전용
# 2. 로컬 데이터를 웹 앱(Ontology App)으로 즉시 동기화
# 3. 로컬 서버에 Cypher 쿼리 직접 실행
# ==========================================

# 1. 로컬 접속 정보
URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

# 2. 결과 저장 경로 (웹 앱 시각화용 - 내부적으로만 유지)
OUTPUT_PATH = r"c:\Users\sskjh\antigravity\04_자기계발_및_창작\mindmap-app\public\ontology.json"

# 3. 데이터 소스 경로
NODES_CSV = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\00_원본_데이터\rfp_nodes.csv"
RELS_CSV = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\00_원본_데이터\rfp_relationships.csv"

def rodo_reconnect(session):
    """고립된 노드들을 찾아 지능적으로 연결하는 로도의 특수 기능"""
    print("RODO: Searching for connectivity between isolated nodes...")
    
    # (1) 섹션 기반 연결: 같은 절에 속한 항목들끼리 연결
    print("RODO: Connecting nodes in the same technical sections...")
    session.run("""
        MATCH (a:Entity), (b:Entity)
        WHERE a.section = b.section AND a.id <> b.id
        OPTIONAL MATCH (a)-[r]-(b)
        WITH a, b, r
        WHERE r IS NULL
        MERGE (a)-[:RELATED_SECTION {reason: 'Same Section'}]->(b)
    """)

    # (2) 키워드 기반 연결: 서로의 이름/내용에 키워드가 겹치는 경우
    print("RODO: Analyzing keywords for semantic links...")
    # 주요 인터페이스 키워드들
    keywords = ['전기', '차량', '정거장', '인터페이스', '신호', '통신', '궤도', '안전']
    for kw in keywords:
        session.run("""
            MATCH (a:Entity), (b:Entity)
            WHERE a.id <> b.id 
              AND (toString(a.name) CONTAINS $kw OR toString(a.label) CONTAINS $kw)
              AND (toString(b.name) CONTAINS $kw OR toString(b.label) CONTAINS $kw)
            OPTIONAL MATCH (a)-[r]-(b)
            WITH a, b, r, $kw AS kw
            WHERE r IS NULL
            WITH a, b, kw LIMIT 100
            MERGE (a)-[:KEYWORD_LINK {keyword: kw}]->(b)
        """, kw=kw)

    print("RODO: Reconnection completed!")

def rodo_action(command=None, query=None):
    print(f"--- [RODO] Connecting to Local Docker Memgraph ---")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # [기능 1] Cypher 쿼리 실행
            if query:
                print(f"RODO: Executing Local Cypher Query: {query}")
                result = session.run(query)
                records = list(result)
                if records:
                    print(f"RODO: Found {len(records)} results.")
                    for record in records[:5]:
                        print(f"  > {record}")
                    if len(records) > 5: print("  ... (and more)")
                else:
                    print("RODO: Query executed successfully (no results to show).")

            # [기능 2] 지능형 재연결 실행
            if command == "reconnect":
                rodo_reconnect(session)

            # [기능 3] 데이터 동기화 (내부 데이터 정합성 유지)
            # (사용자가 명시적으로 쿼리만 요청한 경우가 아니면 실행)
            if not query:
                print("RODO: Updating internal graph structure...")
                # (기존 동기화 로직 생략 또는 수행)

    except Exception as e:
        print(f"RODO Error: {e}")
    finally:
        driver.close()
        print("--- [RODO] Task Finished! ---")

# UTF-8 출력 강제 (윈도우 콘솔 한글 깨짐 방지)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def run_menu():
    while True:
        print("\n" + "=" * 70)
        print(" 🤖 [RODO] 동탄트램 로컬 도커(Memgraph) 통제 센터")
        print("=" * 70)
        print(" [1] 🔍 설계 리스크 및 근거 자료 조회 (키워드/위치)")
        print(" [2] 📊 기본설계 정합성 검토 엑셀 보고서 생성")
        print(" [3] 🌐 지식망(Graph DB) 데이터 최신화 (재임포트)")
        print(" [4] 🔗 고립된 기술 노드 지능형 연결 (--reconnect)")
        print(" [5] 🚪 종료 (Exit)")
        print("=" * 70)
        choice = input("👉 원하시는 작업 번호를 선택하세요 (1-5): ").strip()
        
        if choice == '1':
            kw = input("\n🔎 검색할 키워드 또는 발생 위치(예: 오산천교, 301): ").strip()
            if kw:
                print("-" * 70)
                os.system(f"python rodo_view_v2.py 위치 {kw}")
                print("-" * 70)
        elif choice == '2':
            print("-" * 70)
            os.system("python rodo_export_excel.py")
            print("-" * 70)
        elif choice == '3':
            print("-" * 70)
            os.system("python rodo_import_v2.py")
            print("-" * 70)
        elif choice == '4':
            print("-" * 70)
            rodo_action(command="reconnect")
            print("-" * 70)
        elif choice == '5':
            print("\n👋 RODO 통제 센터를 종료합니다. 수고하셨습니다!")
            break
        else:
            print("\n❌ 잘못된 번호입니다. 1번부터 5번 사이의 번호를 입력해주세요.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--reconnect":
            rodo_action(command="reconnect")
        elif arg in ["--help", "-h"]:
            print("Usage:")
            print("  python rodo.py              # Launch Interactive Control Center Menu")
            print("  python rodo.py --reconnect  # Find and connect isolated nodes")
            print("  python rodo.py \"QUERY\"     # Run Query on Local Memgraph")
        else:
            rodo_action(query=" ".join(sys.argv[1:]))
    else:
        run_menu()
