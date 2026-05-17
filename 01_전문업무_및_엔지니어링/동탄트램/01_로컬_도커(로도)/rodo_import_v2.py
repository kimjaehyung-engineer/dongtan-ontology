import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def import_risks():
    with open("extracted_risks.json", "r", encoding="utf-8") as f:
        risks = json.load(f)

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # 기존 VIOLATION 엣지 삭제 (스키마 업그레이드를 위해)
        session.run("MATCH ()-[v:VIOLATION]->() DELETE v")
        print("RODO: 다차원 스키마 업그레이드 준비 (기존 VIOLATION 관계선 삭제 완료)")

        for r in risks:
            loc = r['location']
            disc = r['discipline']
            metric = r['metric']
            actual = r['actual_value']
            limit = r['standard_limit']
            desc = r['description']
            unit = r['unit']
            source_file = r.get('source_file', '')
            page = r.get('page', '')
            
            # 고유 리스크 노드 이름 생성
            risk_name = f"리스크: {loc} {metric}"
            
            print(f"[PROCESS] 다차원 매핑 중: {risk_name}")
            
            # 1. Location(위치) 노드 생성 (Station 라벨도 추가로 붙여서 기존 구조와 호환성 유지)
            q_loc = """
            MERGE (n:Location {name: $loc})
            SET n:Station
            RETURN n
            """
            session.run(q_loc, loc=loc)
            
            # 2. Discipline(공종) 노드 생성
            q_disc = """
            MERGE (d:Discipline {name: $disc})
            RETURN d
            """
            session.run(q_disc, disc=disc)
            
            # 3. Standard(기준) 노드 생성
            q_std = """
            MERGE (s:Standard {name: $std_name})
            SET s.target_metric = $metric, s.limit_value = $limit, s.unit = $unit
            RETURN s
            """
            std_name = f"표준: {metric}"
            session.run(q_std, std_name=std_name, metric=metric, limit=limit, unit=unit)
            
            # 4. Document(출처 문서) 노드 생성 및 물리 경로 매핑
            # BASE_PATHS와 매칭되는 실제 로컬 절대 경로 확보
            BASE_PATHS = {
                "01. 설계보고서(건축).pdf": r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서\1공구\건축",
                "01. 설계보고서_궤도.pdf": r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서\1공구\궤도",
                "01. 종합요약보고서.pdf": r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서\1공구\토목"
            }
            
            doc_path = "경로 미지정"
            for doc_name, base_dir in BASE_PATHS.items():
                if doc_name in source_file:
                    import os
                    doc_path = os.path.join(base_dir, doc_name).replace("\\", "/")
                    break

            q_doc = """
            MERGE (d:Document {name: $source_file})
            SET d.absolute_path = $doc_path
            RETURN d
            """
            session.run(q_doc, source_file=source_file, doc_path=doc_path)
            
            # 5. Risk 노드 생성, 3방향 연결 및 Document와의 EVIDENCE_IN 관계 구축
            q_risk = """
            MATCH (loc:Location {name: $loc})
            MATCH (disc:Discipline {name: $disc})
            MATCH (s:Standard {name: $std_name})
            MATCH (doc:Document {name: $source_file})
            
            MERGE (r:Risk {name: $risk_name})
            SET r.actual_value = $actual,
                r.issue_description = $desc
                
            MERGE (r)-[:OCCURS_AT]->(loc)
            MERGE (r)-[:BELONGS_TO]->(disc)
            MERGE (r)-[:VIOLATES]->(s)
            MERGE (r)-[ev:EVIDENCE_IN]->(doc)
            SET ev.page = $page
            """
            session.run(q_risk, risk_name=risk_name, loc=loc, disc=disc, std_name=std_name, 
                        actual=actual, desc=desc, source_file=source_file, page=page)
            
            print(f"  [SUCCESS] {disc} 공종 - {loc} 위치 (출처 문서 노드 연계) 매핑 완료!")

    driver.close()
    print("\nRODO: [완료] 다차원(위치+공종+출처문서) 지식망 업그레이드가 성공적으로 적용되었습니다.")

if __name__ == "__main__":
    import_risks()
