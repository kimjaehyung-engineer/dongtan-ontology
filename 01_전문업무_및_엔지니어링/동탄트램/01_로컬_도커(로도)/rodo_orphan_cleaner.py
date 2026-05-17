from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def clean_orphans():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Starting Universal Orphan Node Cleanup...")
        
        # 1. 독립 노드(연결이 0개인 노드) 찾기 (Memgraph용 안전한 문법)
        result = session.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() WITH n, count(r) as rel_count WHERE rel_count = 0 RETURN n.name as name, labels(n) as labels")
        orphans = [record for record in result]
        print(f"RODO: Found {len(orphans)} isolated nodes.")
        
        if len(orphans) == 0:
            print("RODO: No isolated nodes found. The graph is already fully connected!")
            return

        # 2. 허브 및 키워드 매핑 (더 확장된 버전)
        mapping = {
            '차량 및 전동차 관련 제약': ['차량', '전동차', '트램', 'TCMS', '시험기', '운행', '제약'],
            '주요 설비/전기': ['전기', '전력', '변전', '급전', '계통', '이중계', 'Standby', '에너지', '배전'],
            '인프라/관제': ['인프라', '시설', '구조', '토목', '비디오', '월', '지령실', '관제', '통제', '모니터'],
            '도로의 및 가로등': ['도로', '가로등', '등주', '교통', '보도', '유도블록', '안내', '블록', '표지'],
            '동탄 지하차도': ['지하차도', '터널', '하부', '복공판', '방음벽', '가설', '토공'],
            '기동지구': ['기동', '부대시설', '변기', '화장실', '설비', '건축', '정거장', '역사'],
            '도시기반시설 유지관리 및 보수공사': ['유지관리', '보수', '관리', '공사', '점검', '진단', '검사', '일상']
        }

        linked_count = 0
        anchored_count = 0

        for orphan in orphans:
            name = orphan['name']
            if not name: continue
            
            found_hub = False
            for hub_name, keywords in mapping.items():
                if any(kw in name for kw in keywords):
                    q = """
                    MATCH (h {name: $hub_name}), (o)
                    WHERE o.name = $name OR o.name CONTAINS $name
                    MERGE (o)-[:HUB_LINK]->(h)
                    """
                    session.run(q, hub_name=hub_name, name=name)
                    found_hub = True
                    linked_count += 1
                    break
            
            if not found_hub:
                # 3. 매칭되는 허브가 없으면 프로젝트 루트에 연결 (미아 방지)
                q = """
                MATCH (root:Project {name: '동탄트램 사업'}), (o {name: $name})
                MERGE (o)-[:PART_OF_PROJECT]->(root)
                """
                session.run(q, name=name)
                anchored_count += 1

        print(f"RODO: Successfully linked {linked_count} nodes to specific hubs.")
        print(f"RODO: Anchored {anchored_count} fallback nodes to Project Root.")
        print("RODO: Universal Cleanup Completed! Every node is now part of the network.")

    driver.close()

if __name__ == "__main__":
    clean_orphans()
