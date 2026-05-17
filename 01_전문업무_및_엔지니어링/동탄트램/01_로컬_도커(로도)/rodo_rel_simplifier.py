from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def simplify_relationships():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Starting Relationship Refactoring...")
        
        # 통합 매핑 정의 (RegEx 패턴 기반)
        mapping = [
            # 1. RISK_IMPACT
            {
                'pattern': ".*RISK.*|.*THREAT.*|.*VULNERABILITY.*|AFFECTS|IMPACTS|INCREASES.*|DECREASES.*",
                'new_type': 'RISK_IMPACT'
            },
            # 2. TECHNICAL_REQ
            {
                'pattern': "MUST_COMPLY_WITH|REQUIRES|CONSTRAINS|MANDATORY|COMPLIES|GOVERNED_BY",
                'new_type': 'TECHNICAL_REQ'
            },
            # 3. SUPPORT_FLOW
            {
                'pattern': "OPTIMIZES.*|ENHANCES.*|SUPPORT.*|ENABLES.*|GENERATES.*|CONTRIBUTES.*",
                'new_type': 'SUPPORT_FLOW'
            },
            # 4. COMPOSITION
            {
                'pattern': "DETAILED_FACILITY|CONTAINS|PART_OF|ELEMENT|COMPONENT|HAS_PART|SUB_.*",
                'new_type': 'COMPOSITION'
            }
        ]
        
        total_refactored = 0
        
        for rule in mapping:
            print(f"RODO: Refactoring relationships matching '{rule['pattern']}' -> {rule['new_type']}...")
            
            # Memgraph에서는 관계 타입 변경을 위해 삭제 후 재생성이 필요함
            # 1. 새로운 관계 생성 (속성 복사 포함)
            q_create = f"""
            MATCH (a)-[r]->(b)
            WHERE type(r) =~ $pattern AND type(r) <> $new_type
            MERGE (a)-[r2:{rule['new_type']}]->(b)
            SET r2 = properties(r)
            RETURN count(r2) as count
            """
            res = session.run(q_create, pattern=rule['pattern'], new_type=rule['new_type'])
            count = res.single()['count']
            
            # 2. 예전 관계 삭제
            q_delete = f"""
            MATCH (a)-[r]->(b)
            WHERE type(r) =~ $pattern AND type(r) <> $new_type
            DELETE r
            """
            session.run(q_delete, pattern=rule['pattern'], new_type=rule['new_type'])
            
            print(f"RODO: Refactored {count} relationships.")
            total_refactored += count

        # 5. 그 외 남은 이름들을 RELATED_TO로 통합 (HUB_LINK, PART_OF_PROJECT, NAVIGATION 제외)
        print("RODO: Consolidating remaining minor relationships to 'RELATED_TO'...")
        q_final = """
        MATCH (a)-[r]->(b)
        WHERE NOT type(r) IN ['RISK_IMPACT', 'TECHNICAL_REQ', 'SUPPORT_FLOW', 'COMPOSITION', 'HUB_LINK', 'PART_OF_PROJECT', 'RELATED_TO']
        MERGE (a)-[r2:RELATED_TO]->(b)
        SET r2 = properties(r)
        WITH r DELETE r
        RETURN count(*) as count
        """
        res = session.run(q_final)
        final_count = res.single()['count']
        
        print(f"RODO: Final cleanup refactored {final_count} minor relationships.")
        print(f"RODO: Total relationships refactored: {total_refactored + final_count}")
        print("RODO: Relationship Simplification Completed!")

    driver.close()

if __name__ == "__main__":
    simplify_relationships()
