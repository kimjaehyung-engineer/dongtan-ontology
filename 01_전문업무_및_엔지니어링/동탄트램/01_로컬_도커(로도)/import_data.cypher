// [동탄트램 RFP 지식 그래프] 마스터 업데이트 및 전체 출력 쿼리
// 작성일: 2026-05-16
// 특징: 기존 데이터 보존(MERGE) + 전체 신경망 시각화

// 1. 핵심 인과관계 및 인터페이스 연결 (최신 보정판)
MATCH (a {id:'RFP-J-004'}), (b {id:'RFP-A-001'}) MERGE (a)-[:PREREQUISITE_FOR_APPROVAL]->(b);
MATCH (a {id:'RFP-J-005'}), (b {id:'RFP-I-004'}) MERGE (a)-[:PROVIDES_DOOR_STATUS_TO]->(b);
MATCH (a {id:'RFP-J-006'}), (b {id:'RFP-H-001'}) MERGE (a)-[:ENSURES_COMM_INTEGRITY]->(b);
MATCH (a {id:'RFP-B-004'}), (b {id:'RFP-B-005'}) MERGE (a)-[:DETERMINES_REGEN_LOAD]->(b);
MATCH (a {id:'RFP-D-005'}), (b {id:'RFP-F-003'}) MERGE (a)-[:DIGITAL_TWIN_FOR]->(b);

// 2. 교통 처리 대책 관련 인과관계 보강
MATCH (a {id:'RFP-J-001'}), (b {id:'RFP-CD-011'}) MERGE (a)-[:ENHANCES_TRAFFIC_FLOW]->(b);
MATCH (a {id:'RFP-A-004'}), (b {id:'RFP-CD-011'}) MERGE (a)-[:CAUSES_ROAD_CLOSURE]->(b);
MATCH (a {id:'RFP-B-002'}), (b {id:'RFP-CD-011'}) MERGE (a)-[:DETERMINES_SIGNAL_CYCLE]->(b);
MATCH (a {id:'RFP-A-005'}), (b {id:'RFP-CD-011'}) MERGE (a)-[:GOVERNS_TRAFFIC_PLAN]->(b);

// 3. 전체 리스크 지도 시각화 (모든 노드와 화살표 출력)
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;
