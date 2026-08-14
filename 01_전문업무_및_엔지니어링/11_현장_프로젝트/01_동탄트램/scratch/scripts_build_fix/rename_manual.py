import sys, re
sys.stdout.reconfigure(encoding='utf-8')

src = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\03_보고서_및_출력\지장물_이설_업무_매뉴얼.html"
dst = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\03_보고서_및_출력\동탄트램_업무_매뉴얼.html"

with open(src, 'rb') as f:
    raw = f.read()
html = raw.decode('utf-8', errors='replace')

print(f"[INFO] 원본 파일 길이: {len(html)} chars")

# ── 변경 1: <title> ──────────────────────────────────────────────────────────
html = re.sub(r'<title>[^<]*</title>', '<title>동탄트램 업무 매뉴얼</title>', html)
print("[OK] title 변경")

# ── 변경 2: logo-title ───────────────────────────────────────────────────────
html = re.sub(r'(<div class="logo-title">)[^<]*(</div>)',
              r'\g<1>동탄트램 업무 매뉴얼\g<2>', html)
print("[OK] logo-title 변경")

# ── 변경 3: logo-subtitle ────────────────────────────────────────────────────
html = re.sub(r'(<div class="logo-subtitle">)[^<]*(</div>)',
              r'\g<1>동탄트램 노선 기본설계 기술제안\g<2>', html)
print("[OK] logo-subtitle 변경")

# ── 변경 4: h1 본문 헤딩 (최초 1회만) ────────────────────────────────────────
html = re.sub(r'<h1>[^<]*</h1>', '<h1>동탄트램 업무 매뉴얼</h1>', html, count=1)
print("[OK] h1 변경")

# ── 변경 5: nav-list 교체 ─────────────────────────────────────────────────────
# nav-list 시작 찾기
nav_start = html.find('<ul class="nav-list">')
if nav_start == -1:
    print("[ERR] nav-list 시작 미발견!")
    sys.exit(1)

# nav-list 끝 = <main> 태그 직전 (aside가 닫히지 않은 구조)
# "</li>\r\n                        <main>" 패턴을 찾자
nav_end_pattern = re.compile(r'</li>\s*<main>', re.DOTALL)
m = nav_end_pattern.search(html, nav_start)
if not m:
    # fallback: <main> 태그 위치
    main_pos = html.find('<main>', nav_start)
    if main_pos == -1:
        print("[ERR] <main> 태그 미발견!")
        sys.exit(1)
    nav_end = main_pos
    insert = "\n        </ul>\n    </aside>\n\n    "
else:
    nav_end = m.start() + len('</li>')  # </li> 바로 뒤까지를 nav 끝으로
    insert = "\n        </ul>\n    </aside>\n\n    "

print(f"[INFO] nav_start={nav_start}, nav_end={nav_end}")
print(f"[INFO] 교체 범위 미리보기: ...{repr(html[nav_end-50:nav_end+50])}...")

new_nav = '''\
<ul class="nav-list">
            <li class="nav-item" data-target="sec-dashboard">
                <a href="#sec-dashboard">🚊 대시보드</a>
            </li>
            <!-- 1. 토공 -->
            <li class="nav-item" data-target="sec-earthwork">
                <a href="#sec-earthwork">1. 토공</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-earthwork-1"><a href="#sec-earthwork-1">1.1 토공 개요</a></li>
                    <li class="sub-nav-item" data-target="sec-earthwork-2"><a href="#sec-earthwork-2">1.2 성토 및 절토</a></li>
                </ul>
            </li>
            <!-- 2. 노반 (지장물이설 하위 포함) -->
            <li class="nav-item active" data-target="sec-intro">
                <a href="#sec-intro">2. 노반</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item active" data-target="sec-intro-1"><a href="#sec-intro-1">2.1 지장물 이설</a></li>
                    <ul class="sub-nav-list" style="padding-left:0.8rem; margin-top:0.1rem;">
                        <li class="sub-nav-item" data-target="sec-intro-1"><a href="#sec-intro-1">2.1.1 매뉴얼 목적 및 적용</a></li>
                        <li class="sub-nav-item" data-target="sec-intro-2"><a href="#sec-intro-2">2.1.2 지장물 분류 및 현황</a></li>
                        <li class="sub-nav-item" data-target="sec-intro-3"><a href="#sec-intro-3">2.1.3 관련법령/기관 협의</a></li>
                        <li class="sub-nav-item" data-target="sec-intro-4"><a href="#sec-intro-4">2.1.4 단계별 업무흐름</a></li>
                        <li class="sub-nav-item" data-target="sec-intro-5"><a href="#sec-intro-5">2.1.5 타 분야 영향 분석</a></li>
                    </ul>
                    <li class="sub-nav-item" data-target="sec-design-1"><a href="#sec-design-1">2.2 설계단계 업무지침</a></li>
                    <li class="sub-nav-item" data-target="sec-design-2"><a href="#sec-design-2">2.3 지장물 조사 절차</a></li>
                    <li class="sub-nav-item" data-target="sec-design-3"><a href="#sec-design-3">2.4 이설 승인 및 감리</a></li>
                    <li class="sub-nav-item" data-target="sec-design-4"><a href="#sec-design-4">2.5 이설계획 및 예산</a></li>
                </ul>
            </li>
            <!-- 3. 건축 -->
            <li class="nav-item" data-target="sec-architecture">
                <a href="#sec-architecture">3. 건축</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-architecture-1"><a href="#sec-architecture-1">3.1 건축 개요</a></li>
                    <li class="sub-nav-item" data-target="sec-architecture-2"><a href="#sec-architecture-2">3.2 정거장 건축계획</a></li>
                </ul>
            </li>
            <!-- 4. 차량기지 -->
            <li class="nav-item" data-target="sec-depot">
                <a href="#sec-depot">4. 차량기지</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-depot-1"><a href="#sec-depot-1">4.1 차량기지 개요</a></li>
                    <li class="sub-nav-item" data-target="sec-depot-2"><a href="#sec-depot-2">4.2 배치계획</a></li>
                </ul>
            </li>
            <!-- 5. 건축계획 -->
            <li class="nav-item" data-target="sec-arch-plan">
                <a href="#sec-arch-plan">5. 건축계획</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-arch-plan-1"><a href="#sec-arch-plan-1">5.1 환경·경관 계획</a></li>
                    <li class="sub-nav-item" data-target="sec-arch-plan-2"><a href="#sec-arch-plan-2">5.2 승강장 배치</a></li>
                </ul>
            </li>
            <!-- 6. 토질 및 기초 -->
            <li class="nav-item" data-target="sec-geotechnical">
                <a href="#sec-geotechnical">6. 토질 및 기초</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-geotechnical-1"><a href="#sec-geotechnical-1">6.1 지반 조사</a></li>
                    <li class="sub-nav-item" data-target="sec-geotechnical-2"><a href="#sec-geotechnical-2">6.2 기초 형식</a></li>
                </ul>
            </li>
            <!-- 7. 구조 -->
            <li class="nav-item" data-target="sec-structure">
                <a href="#sec-structure">7. 구조</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-structure-1"><a href="#sec-structure-1">7.1 구조 설계 기준</a></li>
                    <li class="sub-nav-item" data-target="sec-structure-2"><a href="#sec-structure-2">7.2 교량 및 고가</a></li>
                </ul>
            </li>
            <!-- 8. 시스템 (전기·통신·신호) -->
            <li class="nav-item" data-target="sec-systems">
                <a href="#sec-systems">8. 시스템 (전기·통신·신호)</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-design-1"><a href="#sec-design-1">8.1 트램 시스템 특성</a></li>
                    <li class="sub-nav-item" data-target="sec-systems-2"><a href="#sec-systems-2">8.2 전력공급 시스템</a></li>
                    <li class="sub-nav-item" data-target="sec-systems-3"><a href="#sec-systems-3">8.3 신호·통신 설계</a></li>
                </ul>
            </li>
            <!-- 9. 궤도 -->
            <li class="nav-item" data-target="sec-track">
                <a href="#sec-track">9. 궤도</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-track-1"><a href="#sec-track-1">9.1 궤도 형식</a></li>
                    <li class="sub-nav-item" data-target="sec-track-2"><a href="#sec-track-2">9.2 선형 및 구배</a></li>
                </ul>
            </li>
            <!-- 10. 검수 -->
            <li class="nav-item" data-target="sec-inspection">
                <a href="#sec-inspection">10. 검수</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-inspection-1"><a href="#sec-inspection-1">10.1 검수 기준</a></li>
                    <li class="sub-nav-item" data-target="sec-inspection-2"><a href="#sec-inspection-2">10.2 검수설비계획</a></li>
                </ul>
            </li>
            <!-- 11. 공사관리 -->
            <li class="nav-item" data-target="sec-construction">
                <a href="#sec-construction">11. 공사관리</a>
                <ul class="sub-nav-list">
                    <li class="sub-nav-item" data-target="sec-construction-1"><a href="#sec-construction-1">11.1 인허가 획득 및 착공 준비</a></li>
                    <li class="sub-nav-item" data-target="sec-construction-2"><a href="#sec-construction-2">11.2 시공 단계</a></li>
                    <li class="sub-nav-item" data-target="sec-construction-3"><a href="#sec-construction-3">11.3 완공 및 인계</a></li>
                </ul>
            </li>
        </ul>
    </aside>'''

# 실제 교체: nav_start ~ nav_end 사이를 new_nav로 교체
# nav_end는 <main> 직전까지
html_before = html[:nav_start]
html_after = html[nav_end:]
# html_after는 </li>\n  <main> ... 형태이므로 </li> 다음부터
# 실제로는 nav_end에서 html_after가 "\r\n                        <main>" 같은 것
# 확인
print(f"[DEBUG] html_after start: {repr(html_after[:80])}")

# </li>를 html_after 시작에서 찾아 제거
if html_after.lstrip().startswith('<main>'):
    # nav_end가 정확히 <main> 직전
    html = html_before + new_nav + '\n\n    ' + html_after.lstrip()
else:
    # </li>부터 시작
    close_li = html_after.find('<main>')
    if close_li >= 0:
        html = html_before + new_nav + '\n\n    ' + html_after[close_li:]
    else:
        html = html_before + new_nav + html_after

print(f"[OK] nav-list 재구성 완료, 새 길이: {len(html)} chars")

# ── 저장 ─────────────────────────────────────────────────────────────────────
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"[DONE] 저장: {dst}")
