from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

# 트램 설계 가이드라인 기준치 (예시값 - RFP에 따라 수정 가능)
standards_data = [
    {
        "name": "표준: 최소 곡선반경(정거장)",
        "target_metric": "곡선반경",
        "operator": ">=",
        "limit_value": 20,
        "unit": "m",
        "category": "정거장 선형"
    },
    {
        "name": "표준: 플랫폼 폭",
        "target_metric": "플랫폼 폭",
        "operator": ">=",
        "limit_value": 2.0,
        "unit": "m",
        "category": "정거장 공간"
    },
    {
        "name": "표준: 최소 곡선반경(본선)",
        "target_metric": "곡선반경",
        "operator": ">=",
        "limit_value": 25,
        "unit": "m",
        "category": "본선 선형"
    },
    {
        "name": "표준: 최대 구배(본선)",
        "target_metric": "구배",
        "operator": "<=",
        "limit_value": 60,
        "unit": "‰",
        "category": "본선 선형"
    },
    {
        "name": "표준: 유치선 구배",
        "target_metric": "구배",
        "operator": "<=",
        "limit_value": 2.5,
        "unit": "‰",
        "category": "차량기지 및 정거장 유치"
    }
]

def setup_standards():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        for std in standards_data:
            q = """
            MATCH (n) WHERE n.name = $name
            SET n:Standard,
                n.target_metric = $target_metric,
                n.operator = $operator,
                n.limit_value = $limit_value,
                n.unit = $unit,
                n.category = $category
            RETURN n.name as name
            """
            result = session.run(q, **std)
            record = result.single()
            if record:
                print(f"[SUCCESS] RODO: 기준 업데이트 완료 -> [{record['name']}] (조건: {std['target_metric']} {std['operator']} {std['limit_value']}{std['unit']})")
            else:
                print(f"[WARNING] RODO: 노드를 찾지 못함 -> [{std['name']}]")
    driver.close()

if __name__ == "__main__":
    print("RODO: 정거장 설계 자동 검증을 위한 1단계 (기준 데이터 수치화) 시작...")
    setup_standards()
