# 동탄트램 지식 그래프 (Dongtan Tram Knowledge Graph)

이 프로젝트는 동탄트램 RFP(입찰안내서)의 제약 사항과 기술 요구사항 간의 관계를 분석하기 위한 Neo4j 기반 지식 그래프 환경입니다.

## 🚀 실행 방법

1. **Docker Desktop 실행**: (현재 이미 실행 중인 것으로 보입니다.)
2. **컨테이너 시작**:
   터미널(PowerShell)에서 아래 명령어를 실행하세요:
   ```powershell
   cd "c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
   docker-compose up -d
   ```
3. **Neo4j 접속**:
   브라우저에서 [http://localhost:7474](http://localhost:7474)로 접속합니다.
   - **Username**: `neo4j`
   - **Password**: `password123`

4. **데이터 임포트**:
   Neo4j Browser의 쿼리창에 `import_data.cypher` 파일의 내용을 복사하여 붙여넣고 실행하세요.

## 📂 파일 구조
- `docker-compose.yml`: Neo4j 컨테이너 설정
- `import/`: 데이터 소스 (CSV) 저장 폴더
- `import_data.cypher`: 데이터 로드용 Cypher 스크립트
- `rfp_nodes.csv`: RFP 요구사항 노드 데이터
- `rfp_relationships.csv`: 요구사항 간의 관계 데이터
