import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def import_violations():
    # Load the extracted JSON
    with open("extracted_violations_with_source.json", "r", encoding="utf-8") as f:
        violations = json.load(f)

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        for v in violations:
            station_name = f"{v['station']} 정거장"  # Need to match the node name in Memgraph, which usually contains '정거장'
            metric = v['metric']
            actual = v['actual_value']
            limit = v['standard_limit']
            desc = v['description']
            unit = v['unit']
            source_file = v.get('source_file', '')
            page = v.get('page', '')
            
            print(f"[PROCESS] 처리 중: {station_name} - {metric} (실제: {actual}{unit} / 기준: {limit}{unit})")
            
            # Step 1: Ensure the Station node exists
            q_station = """
            MERGE (n:Station {name: $station_name})
            RETURN n
            """
            session.run(q_station, station_name=station_name)
            
            # Step 2: Ensure the Standard node exists
            q_std = """
            MERGE (s:Standard {name: $std_name})
            SET s.target_metric = $metric, s.limit_value = $limit, s.unit = $unit
            RETURN s
            """
            std_name = f"표준: {metric}"
            session.run(q_std, std_name=std_name, metric=metric, limit=limit, unit=unit)
            
            # Step 3: Create the VIOLATION relationship
            q_rel = """
            MATCH (n:Station {name: $station_name})
            MATCH (s:Standard {name: $std_name})
            MERGE (n)-[rel:VIOLATION]->(s)
            SET rel.actual_value = $actual,
                rel.issue_description = $desc,
                rel.source_file = $source_file,
                rel.page = $page
            """
            session.run(q_rel, station_name=station_name, std_name=std_name, actual=actual, desc=desc, source_file=source_file, page=page)
            
            print(f"  [SUCCESS] [VIOLATION] 관계선 매핑 완료! (출처: {source_file} {page}p)")

    driver.close()

if __name__ == "__main__":
    print("RODO: NotebookLM 추출 데이터를 지식망에 맵핑합니다...")
    import_violations()
    print("RODO: 모든 위배 사항 맵핑이 완료되었습니다.")
