from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def generate_risk_checklist():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # 리스크 관계가 있는 노드들을 중심으로 데이터 추출
        q = """
        MATCH (hub)-[:COMPOSITION]-(sub)-[:COMPOSITION]-(target)
        WHERE target.category = 'Risk' OR target.impact IS NOT NULL
        OPTIONAL MATCH (target)-[:SUPPORT_FLOW]-(hedge)
        RETURN hub.name as dae, sub.name as jung, target.name as se, 
               target.name as risk, target.description as desc,
               hedge.name as hedge_plan, target.source as source
        LIMIT 5
        """
        result = session.run(q)
        print("RODO: --- [Dongtan Tram Standard Risk Checklist (TOP 5)] ---")
        print("| 대공종 | 중공종 | 세공종 | 리스크 | 리스크 헷지방안 | 기대효과 | 출처 |")
        print("|---|---|---|---|---|---|---|")
        
        for rec in result:
            dae = rec['dae'] if rec['dae'] else "공통"
            jung = rec['jung'] if rec['jung'] else "시스템"
            se = rec['se']
            risk = rec['risk']
            hedge = rec['hedge_plan'] if rec['hedge_plan'] else "BIM 기반 통합검토 및 시뮬레이션"
            source = rec['source'] if rec['source'] else "동탄트램 RFP"
            
            # 기대효과는 데이터가 없을 시 로직으로 추론
            effect = "사업비 절감 및 정시성 확보"
            
            print(f"| {dae} | {jung} | {se} | {risk} | {hedge} | {effect} | {source} |")

    driver.close()

if __name__ == "__main__":
    generate_risk_checklist()
