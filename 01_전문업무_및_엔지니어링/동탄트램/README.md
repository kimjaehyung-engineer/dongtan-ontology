# 동탄트램 지식 그래프 (Dongtan Tram Knowledge Graph)

이 프로젝트는 동탄트램 RFP(입찰안내서)의 제약 사항과 기술 요구사항 간의 관계를 분석하기 위한 Memgraph 기반 지식 그래프 환경입니다.

## 🚀 실행 방법

1. **Docker Desktop 실행**
2. **컨테이너 시작**:
   PowerShell에서 로컬 Docker 설정 디렉터리로 이동한 뒤 실행합니다.
   ```powershell
   Set-Location "<저장소 경로>\01_전문업무_및_엔지니어링\동탄트램\01_로컬_도커(로도)"
   docker compose up -d
   ```
3. **Memgraph Lab 접속**:
   브라우저에서 [http://localhost:3000](http://localhost:3000)으로 접속합니다.
   - **Bolt URI**: `bolt://localhost:7687`
   - 로컬 Docker 기본 구성은 사용자명과 비밀번호를 사용하지 않습니다.

4. **데이터 임포트**:
   Memgraph Lab의 쿼리창에 `01_로컬_도커(로도)/import_data.cypher` 파일의 내용을 복사하여 붙여넣고 실행합니다.

## 환경변수 설정

Python 스크립트는 운영체제의 환경변수를 직접 읽습니다. `.env.example`은 필요한 변수명을 보여주는 템플릿이며, `.env` 파일을 자동으로 읽지는 않습니다.

클라우드 작업에는 다음 세 변수가 모두 필요합니다.

| 변수 | 설명 |
|---|---|
| `DONGTAN_CLOUD_URI` | Memgraph Cloud Bolt URI (`bolt+ssc://...`) |
| `DONGTAN_CLOUD_USER` | 클라우드 사용자명 |
| `DONGTAN_CLOUD_PASSWORD` | 클라우드 비밀번호 |

PowerShell 세션에 설정하는 예시는 다음과 같습니다. 실제 값은 저장소에 기록하지 마세요.

```powershell
$env:DONGTAN_CLOUD_URI = "<Memgraph Cloud URI>"
$env:DONGTAN_CLOUD_USER = "<사용자명>"
$env:DONGTAN_CLOUD_PASSWORD = "<비밀번호>"
```

로컬 인증을 활성화한 경우에는 `DONGTAN_LOCAL_URI`, `DONGTAN_LOCAL_USER`, `DONGTAN_LOCAL_PASSWORD`를 사용할 수 있습니다. `DONGTAN_NODES_CSV`, `DONGTAN_RELATIONSHIPS_CSV`, `DONGTAN_ONTOLOGY_OUTPUT`으로 기본 데이터·출력 경로도 재정의할 수 있습니다.

클라우드 JSON의 기본 출력은 `03_보고서_및_출력/ontology.json`입니다. 별도 웹 앱의 공개 데이터 파일을 직접 갱신해야 한다면 `DONGTAN_ONTOLOGY_OUTPUT`에 해당 파일 경로를 설정하세요.

## 보안 주의사항

- `.env`와 `.env.*` 파일은 Git에서 제외되며 `.env.example`만 추적합니다.
- 비밀번호, 사용자명, 실제 클라우드 주소를 코드·문서·테스트에 직접 기록하지 마세요.
- 과거 Git 커밋에 노출된 자격증명은 코드에서 삭제하는 것만으로 무효화되지 않습니다. 해당 자격증명을 Memgraph Cloud에서 회전하고 접근 로그를 확인해야 합니다. Git 이력 정리는 별도의 운영 작업입니다.

## 테스트

공통 설정, 경로 처리, 비밀정보 재유입 방지, 안전한 하위 프로세스 호출은 외부 패키지 없이 검증할 수 있습니다.

```powershell
Set-Location "<저장소 경로>\01_전문업무_및_엔지니어링\동탄트램"
python -m unittest discover -s tests -t . -v
```

## 📂 파일 구조
- `00_원본_데이터/`: RFP 노드·관계 CSV 데이터
- `01_로컬_도커(로도)/docker-compose.yml`: Memgraph와 Memgraph Lab 컨테이너 설정
- `01_로컬_도커(로도)/import_data.cypher`: 데이터 로드용 Cypher 스크립트
- `02_클라우드_원격/`: 클라우드 동기화·업로드 스크립트
- `03_보고서_및_출력/`: 보고서와 기본 JSON 출력 위치
- `dongtan_runtime.py`: 공통 접속 설정, 프로젝트 경로, 안전한 Python 스크립트 실행
