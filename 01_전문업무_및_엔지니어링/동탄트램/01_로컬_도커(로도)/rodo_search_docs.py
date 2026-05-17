import os
import sys
import fitz  # PyMuPDF

# UTF-8 출력 강제 (윈도우 콘솔 한글 깨짐 방지)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# 설계 보고서가 들어있는 기본 폴더 경로
TARGET_DIR = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서"

# 기본적으로 검색에서 제외할 무거운 CAD 도면 및 부록 키워드 (기본 텍스트 검색에 비효율적)
SKIP_KEYWORDS = ["도면", "설계도", "부록", "계산서", "기본설계도", "도면집"]

def search_keyword_in_pdfs(keyword, search_all=False):
    if not os.path.exists(TARGET_DIR):
        print(f"[ERROR] 대상 디렉토리가 존재하지 않습니다: {TARGET_DIR}")
        return

    print("=" * 75)
    print(f" 🔍 [RODO] 로컬 도면/설계서 통합 키워드 검색 엔진")
    print(f" - 검색 대상 폴더: {TARGET_DIR}")
    print(f" - 검색 키워드: '{keyword}'")
    if search_all:
        print(f" - 검색 모드: 전체 파일 검색 (도면/부록 포함)")
    else:
        print(f" - 검색 모드: 텍스트 보고서 중심 검색 (속도 최적화 모드)")
    print("=" * 75)

    # 검색 대상 파일 리스트업 및 필터링
    all_pdf_files = []
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                
                # 검색 최적화: 도면/부록 건너뛰기 여부 결정
                should_skip = False
                if not search_all:
                    for skip_kw in SKIP_KEYWORDS:
                        if skip_kw in file:
                            should_skip = True
                            break
                
                if not should_skip:
                    all_pdf_files.append(file_path)

    total_files = len(all_pdf_files)
    print(f"총 {total_files}개의 후보 문서를 스캔합니다...\n")

    found_results = []
    
    for idx, file_path in enumerate(all_pdf_files, 1):
        file_name = os.path.basename(file_path)
        
        # 분야(공종) 추출
        relative_path = os.path.relpath(file_path, TARGET_DIR)
        path_parts = relative_path.split(os.sep)
        discipline = path_parts[1] if len(path_parts) > 1 else "공통"
        
        # 실시간 진행 상황 출력 (한 줄 지우고 덮어쓰기)
        sys.stdout.write(f"\r⏳ [{idx}/{total_files}] 스캔 중: {discipline} - {file_name[:30]}...")
        sys.stdout.flush()
        
        try:
            doc = fitz.open(file_path)
            matching_pages = []
            snippets = {}
            
            for page_idx in range(len(doc)):
                page = doc[page_idx]
                text_instances = page.search_for(keyword)
                
                if text_instances:
                    page_num = page_idx + 1
                    matching_pages.append(page_num)
                    
                    # 상위 2개 페이지만 프리뷰 스니펫 생성
                    if len(matching_pages) <= 2:
                        text_content = page.get_text()
                        for line in text_content.split('\n'):
                            if keyword in line:
                                snippets[page_num] = line.strip()
                                break
                        if page_num not in snippets:
                            snippets[page_num] = text_content[:120].replace('\n', ' ').strip() + "..."
            
            if matching_pages:
                found_results.append({
                    "discipline": discipline,
                    "file_name": file_name,
                    "file_path": file_path,
                    "total_pages": len(doc),
                    "pages": matching_pages,
                    "snippets": snippets
                })
                
        except Exception as e:
            # 에러 방지
            pass

    # 진행 안내 줄바꿈
    print("\n\n" + "=" * 75)

    # 결과 출력
    if not found_results:
        print(f"❌ 검색어 '{keyword}'에 매칭되는 설계 문서 및 보고서를 찾지 못했습니다.")
        if not search_all:
            print("💡 도면/계산서/부록 파일까지 모두 검색하려면 뒤에 '--all' 옵션을 붙여보세요.")
            print("   예시: python rodo_search_docs.py 오산천교 --all")
        print("=" * 75)
        return

    print(f"🎉 총 {len(found_results)}개의 관련 설계서 파일을 발견했습니다!\n")
    
    for i, res in enumerate(found_results, 1):
        print(f"[{i}] 분야: {res['discipline']} | 파일명: {res['file_name']}")
        print(f" 📂 로컬 경로: {res['file_path']}")
        print(f" 📄 발견 페이지 (총 {len(res['pages'])}곳): {res['pages']}")
        print(f" 📝 실제 언급 내용 (미리보기):")
        for pg, snip in res['snippets'].items():
            print(f"   - [P.{pg}]: \"{snip}\"")
        print("-" * 75)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python rodo_search_docs.py [검색할 키워드] [--all]")
        print("옵션: --all (도면, 계산서, 부록 파일까지 전체 검색)")
        print("예시: python rodo_search_docs.py 오산천교")
        sys.exit(1)
        
    # --all 옵션이 붙어 있는지 확인
    search_all = False
    args = sys.argv[1:]
    if "--all" in args:
        search_all = True
        args.remove("--all")
        
    search_keyword = " ".join(args)
    search_keyword_in_pdfs(search_keyword, search_all)
