import subprocess

def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)
    print(f"[{cmd}] -> code: {res.returncode}")
    if res.stdout:
        print("  OUT:", res.stdout.strip()[:200])
    if res.stderr:
        print("  ERR:", res.stderr.strip()[:200])

print("=== STEP 1: Hard unstage all tracked index changes ===")
run("git reset origin/main")

print("\n=== STEP 2: Verify git status after unstage ===")
res_status = subprocess.run("git status --short", capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)
print(f"Status lines: {len(res_status.stdout.splitlines())}")

print("\n=== STEP 3: Stage ONLY 2 files ===")
run('git add "08.메뉴얼 및 평면도/동탄트램 노선평면도/동탄트램_노선평면도V1.html"')
run('git add ".gitignore"')

print("\n=== STEP 4: Create SINGLE CLEAN COMMIT ===")
run('git commit -m "feat: 동탄트램 노선평면도 V1 시공구간 인출 지시선 CAD 스타일 적용, 정거장 노드 스타일(노란색/검정 테두리) 및 도면 레이어 일괄 전체 해제/선택 기능 구현"')

print("\n=== STEP 5: Push to origin main ===")
run('git push origin main')
