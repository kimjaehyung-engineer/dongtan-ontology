import subprocess

def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)
    print(f"[{cmd}] -> code: {res.returncode}")
    if res.stdout:
        print("  OUT:", res.stdout.strip()[:300])
    if res.stderr:
        print("  ERR:", res.stderr.strip()[:300])

print("=== Removing node_modules and release from git index ===")
run('git rm -r --cached --ignore-unmatch "01_전문업무_및_엔지니어링/14_개발_및_자동화_앱/02_process-map-web-v2/node_modules"')
run('git rm -r --cached --ignore-unmatch "01_전문업무_및_엔지니어링/14_개발_및_자동화_앱/02_process-map-web-v2/release"')

print("\n=== Amending commit ===")
run('git commit --amend -m "feat: 동탄트램 노선평면도 V1 시공구간 인출 지시선 CAD 스타일 적용, 정거장 노드 스타일(노란색/검정 테두리) 및 도면 레이어 일괄 전체 해제/선택 기능 구현"')

print("\n=== Pushing to origin main ===")
run('git push origin main')
