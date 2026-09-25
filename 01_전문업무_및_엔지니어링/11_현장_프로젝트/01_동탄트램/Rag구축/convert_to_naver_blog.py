import os
import sys
from pathlib import Path
import win32clipboard

# HTML Format 등록
CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")

def set_clipboard_html_and_text(html_content: str, plain_text: str):
    """
    Windows 클립보드에 HTML(CF_HTML)과 일반 텍스트(CF_UNICODETEXT)를 동시에 등록합니다.
    네이버 블로그 스마트에디터 ONE에 붙여넣기(Ctrl+V) 시 서식(인용구, 색상, 소제목 등)이 완벽히 유지됩니다.
    """
    fragment = html_content
    # UTF-8 바이트 길이 계산을 위한 헤더 템플릿
    header_template = (
        "Version:0.9\r\n"
        "StartHTML:{start_html:010d}\r\n"
        "EndHTML:{end_html:010d}\r\n"
        "StartFragment:{start_fragment:010d}\r\n"
        "EndFragment:{end_fragment:010d}\r\n"
    )
    
    dummy_header = header_template.format(start_html=0, end_html=0, start_fragment=0, end_fragment=0)
    start_html = len(dummy_header.encode('utf-8'))
    prefix = "<html><body><!--StartFragment-->"
    suffix = "<!--EndFragment--></body></html>"
    
    start_fragment = start_html + len(prefix.encode('utf-8'))
    fragment_bytes = fragment.encode('utf-8')
    end_fragment = start_fragment + len(fragment_bytes)
    end_html = end_fragment + len(suffix.encode('utf-8'))
    
    actual_header = header_template.format(
        start_html=start_html,
        end_html=end_html,
        start_fragment=start_fragment,
        end_fragment=end_fragment
    )
    
    clipboard_bytes = (actual_header + prefix + fragment + suffix).encode('utf-8')
    
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        # HTML 포맷 복사
        win32clipboard.SetClipboardData(CF_HTML, clipboard_bytes)
        # 일반 텍스트 포맷 복사
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, plain_text)
    finally:
        win32clipboard.CloseClipboard()

def build_post_1_html():
    return """
<div style="font-family: 'Nanum Gothic', 'Pretendard', sans-serif; max-width: 760px; margin: 0 auto; color: #222222; font-size: 16px; line-height: 1.85; letter-spacing: -0.3px; word-break: keep-all;">

  <!-- 포스팅 헤더 박스 -->
  <div style="margin-bottom: 25px;">
    <span style="display: inline-block; background-color: #03C75A; color: #ffffff; font-size: 13px; font-weight: bold; padding: 4px 10px; border-radius: 20px; margin-bottom: 10px;">동탄트램 현장 AI 일지 #1</span>
    <h1 style="font-size: 26px; font-weight: 800; color: #111111; line-height: 1.4; margin: 8px 0 16px 0;">
      지반조사 결과와 설계정수, 그 흩어진 연결고리를 온톨로지(Ontology)로 꿰어보기
    </h1>
  </div>

  <!-- 인용구 박스 (현장의 고민) -->
  <div style="background-color: #F8F9FA; border-left: 5px solid #03C75A; padding: 18px 22px; border-radius: 0 10px 10px 0; margin: 25px 0;">
    <p style="margin: 0 0 8px 0; font-size: 17px; font-weight: 700; color: #028A3E;">
      ❝ "소장님, 이번 흙막이 가시설에 적용된 풍화암 마찰각 35도요.<br>
      이거 어떤 시험 거쳐서 계산된 건지 근거 좀 바로 찾아봐주세요." ❞
    </p>
    <p style="margin: 0; font-size: 15px; color: #666666; line-height: 1.6;">
      현장에서 이런 요청을 받을 때마다, 지반조사보고서와 토질설계보고서, 가시설 구조계산서까지 서너 권의 책을 책상 위에 펼쳐두고 한참을 대조해야 합니다. 못 할 일은 아니지만, 매번 이 책 저 책 넘나들며 숫자의 출처를 확인하는 과정은 꽤 번거롭고 손이 많이 가는 일입니다.
    </p>
  </div>

  <p>
    안녕하세요!<br>
    동탄도시철도(동탄트램) 현장에서 토목·지반 엔지니어링 실무를 담당하고 있는 엔지니어입니다.
  </p>

  <p>
    요즘 생성형 AI나 RAG(검색 증강 생성)에 대한 이야기가 많지만, 실제 건설 실무에 곧바로 적용하기에는 현실적인 간극이 큽니다.<br>
    저는 최근 AI 툴과 구글 API를 활용해, 우리 현장의 기술 도서들을 유기적으로 연결해 주는 
    <span style="background-color: #E8F8EE; color: #038A3E; padding: 2px 6px; border-radius: 4px; font-weight: 700;">현장 맞춤형 RAG 시스템 구축</span>을 이제 막 시작했습니다.
  </p>

  <p>
    아직 완제품이 나온 상태는 아니고, 프로토타입을 만들어보며 하나씩 테스트하고 있는 <strong>초기 단계(현재진행형)</strong>입니다.<br>
    첫 글에서는 기술적인 코드 이야기 전에, <strong>"현장에서 왜 이런 시스템이 필요하다고 느꼈는지"</strong>, 그리고 <strong>"왜 온톨로지(Ontology)라는 개념에 관심을 갖게 되었는지"</strong>에 대해 가볍게 이야기해 보려 합니다.
  </p>

  <hr style="border: none; border-top: 1px dashed #D9DCE0; margin: 35px 0;">

  <!-- 섹션 1 -->
  <h2 style="font-size: 21px; font-weight: 800; color: #111111; border-left: 4px solid #03C75A; padding-left: 12px; margin: 30px 0 16px 0;">
    1. 흐름은 뻔한데, 왜 서류는 다 따로 놀까?
  </h2>

  <p>
    토목 현장, 특히 지하 터파기나 가시설 공사를 관리하다 보면 지반 데이터의 근거를 확인해야 하는 상황이 자주 생깁니다.<br>
    일반적으로 지반 데이터는 다음과 같은 흐름으로 설계에 반영됩니다.
  </p>

  <!-- 단계 카드 박스 -->
  <div style="background-color: #FAFAFB; border: 1px solid #E5E7EB; border-radius: 10px; padding: 18px 22px; margin: 20px 0;">
    <div style="margin-bottom: 12px;">
      <span style="background: #2563EB; color: #ffffff; font-size: 12px; font-weight: bold; padding: 2px 8px; border-radius: 4px;">1단계: 지반조사 (Fact)</span><br>
      <span style="font-size: 15px; color: #374151; margin-top: 4px; display: inline-block;">현장 시추조사(주상도 작성, N치 측정) 및 시료 채취 후 실내 토질시험(체분석, 전단시험 등)</span>
    </div>
    <div style="margin-bottom: 12px;">
      <span style="background: #0D9488; color: #ffffff; font-size: 12px; font-weight: bold; padding: 2px 8px; border-radius: 4px;">2단계: 정수 산정 (Process)</span><br>
      <span style="font-size: 15px; color: #374151; margin-top: 4px; display: inline-block;">시험 결과를 통계 정리하고 지반공학 제안 공식/경험식을 적용해 점착력(c), 마찰각(Φ), 변형계수(E) 도출</span>
    </div>
    <div>
      <span style="background: #7C3AED; color: #ffffff; font-size: 12px; font-weight: bold; padding: 2px 8px; border-radius: 4px;">3단계: 설계 반영 (Result)</span><br>
      <span style="font-size: 15px; color: #374151; margin-top: 4px; display: inline-block;">도출된 지반정수로 터파기 흙막이 가시설 벽체 해석, 침하 검토, 본선 궤도 하부 지지력 검토 수행</span>
    </div>
  </div>

  <p>
    논리적으로는 아주 깔끔한 흐름이지만, 문제는 <strong>실제 문서들이 각기 다른 보고서로 분리되어 있다는 점</strong>입니다.
  </p>

  <ul style="padding-left: 20px; line-height: 1.9; color: #444444; margin-bottom: 20px;">
    <li>현장 시추 결과와 N치는 <strong>[지반조사보고서]</strong>에 있고,</li>
    <li>정수를 산정하고 보정한 계산 근거는 <strong>[토질 및 기초 설계보고서]</strong> 부록에 숨어 있으며,</li>
    <li>최종 적용된 수치는 <strong>[가시설 계산서]</strong>나 <strong>[지반정수 총괄표]</strong>에 적혀 있습니다.</li>
    <li>(기본계획 단계와 기술제안, 실시설계 단계의 문서가 나뉘어 있으면 확인해야 할 도서는 더 늘어납니다.)</li>
  </ul>

  <p>
    결국 엔지니어가 중간에서 수동으로 이 책 저 책을 넘나들며 숫자의 출처를 일일이 대조해야 합니다.<br>
    어려운 작업이라기보다는, <span style="background: #FEF3C7; padding: 2px 6px; border-radius: 3px; font-weight: 700;">반복적이고 꽤나 번거로운 일</span>입니다.
  </p>

  <hr style="border: none; border-top: 1px dashed #D9DCE0; margin: 35px 0;">

  <!-- 섹션 2 -->
  <h2 style="font-size: 21px; font-weight: 800; color: #111111; border-left: 4px solid #03C75A; padding-left: 12px; margin: 30px 0 16px 0;">
    2. "온톨로지(Ontology)를 구축하면 그 연결관계를 짚어준다는데?"
  </h2>

  <p>
    단순히 특정 단어를 찾아주는 키워드 검색(Ctrl + F)이나 일반 문서 요약 챗봇은 이 번거로움을 근본적으로 해결해 주지 못합니다.<br>
    ChatGPT 같은 거대언어모델(LLM)은 뛰어난 언어 능력을 가졌지만, 본질적으로는 <strong>'다음에 올 그럴싸한 단어를 확률적으로 생성하는 두뇌'</strong>일 뿐입니다. 텍스트 문서 안에 "시추공 DT-00", "마찰각 35도", "가시설 벽체"라는 단어가 적혀 있어도, 컴퓨터는 이 단어들이 서로 어떤 역학적 인과관계로 얽혀 있는지 알지 못합니다.
  </p>

  <p>
    우리가 현장에서 진짜 필요로 하는 것은 단어 검색이 아니라, <strong>"보고서와 보고서 사이를 관통하는 엄격한 공학적 인과관계(Lineage)"</strong>입니다.<br>
    이 갈증 끝에 주목하게 된 기술이 바로 요새 AI 지식공학에서 가장 핵심으로 떠오른 <strong>'온톨로지(Ontology, 지식 그래프)'</strong>였습니다.
  </p>

  <!-- 온톨로지 본질 개념 박스 -->
  <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 22px 24px; margin: 24px 0;">
    <h3 style="margin: 0 0 14px 0; font-size: 17px; font-weight: 700; color: #0F172A;">
      💡 온톨로지(지식 그래프)의 핵심 : 노드(Node)와 엣지(Edge)
    </h3>
    <p style="margin: 0 0 14px 0; font-size: 15px; color: #475569; line-height: 1.7;">
      온톨로지는 세상을 컴퓨터에게 가르칠 때 <strong>"데이터의 실체(노드)"</strong>와 그 실체들이 맺고 있는 <strong>"논리적 관계(엣지)"</strong>라는 최소 단위(트리플: 주어-술어-목적어)로 분해하여 지식망을 구축합니다.
    </p>
    
    <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;">
      <strong style="color: #2563EB; font-size: 15px;">● 노드 (Node, 개체/Entity) : 지식의 정거장 (명사)</strong><br>
      <span style="font-size: 14px; color: #334155; margin-top: 4px; display: inline-block;">
        세상에 독립적으로 존재하는 구체적인 대상입니다. 단순한 글자가 아니라 고유한 공학적 <strong>속성(Property)</strong>을 품고 있습니다.<br>
        <em>예: [시추공 DT-00] (속성: 위치 STA, 표고, 지하수위), [풍화암층], [설계 마찰각 35도], [101정거장 흙막이벽]</em>
      </span>
    </div>

    <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 14px 18px;">
      <strong style="color: #03C75A; font-size: 15px;">● 엣지 (Edge, 관계/Predicate) : 의미와 방향성을 가진 선 (동사/술어)</strong><br>
      <span style="font-size: 14px; color: #334155; margin-top: 4px; display: inline-block;">
        두 노드가 "어떤 이유와 논리로 이어져 있는지"를 명시하는 규칙이자 서술어입니다. 단순한 연결선이 아니라 <strong>구체적인 공학적 의미</strong>를 갖습니다.<br>
        <em>예: "~에서 관측됨(OBSERVED)", "~의 산출 근거가 됨(DERIVES)", "~에 설계 반영됨(APPLIED_TO)", "~의 위험을 유발함(RISK_OF)"</em>
      </span>
    </div>
  </div>

  <p>
    이를 우리 동탄트램 지반 엔지니어링에 대입해 보면, 보고서 속에 흩어져 있던 데이터들이 하나의 완벽한 <strong>'인과관계 체인(Knowledge Chain)'</strong>으로 엮이게 됩니다.
  </p>

  <!-- 온톨로지 인과관계 다이어그램 -->
  <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 24px 26px; margin: 24px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
    
    <!-- 노드 1 -->
    <div style="background-color: #EFF6FF; border: 1.5px solid #93C5FD; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 12px; font-weight: 800; color: #1D4ED8; margin-bottom: 2px;">[주어 노드 : 조사 원천]</div>
      <strong style="font-size: 16px; color: #1E3A8A;">시추공 DT-00</strong>
      <span style="font-size: 13px; color: #64748B; margin-left: 6px;">(속성: STA. 1+250, 지표표고 EL. 32.5m, 지하수위 GL-2.1m)</span>
    </div>

    <!-- 엣지 1 -->
    <div style="padding: 10px 0 10px 30px; border-left: 3px solid #3B82F6; margin-left: 35px; color: #1D4ED8; font-size: 14px; font-weight: 700;">
      ▼ 엣지: <strong>[OBSERVED / 심도별 지층 및 N치를 관측함]</strong>
    </div>

    <!-- 노드 2 -->
    <div style="background-color: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 12px; font-weight: 800; color: #15803D; margin-bottom: 2px;">[목적어 노드이자 다음 주어 : 팩트 데이터]</div>
      <strong style="font-size: 16px; color: #14532D;">지반조사 원시 시험치 (풍화암층)</strong>
      <span style="font-size: 13px; color: #64748B; margin-left: 6px;">(속성: 심도 7.5m~14.0m, SPT N치 50/15, 삼축시험 점착력)</span>
    </div>

    <!-- 엣지 2 -->
    <div style="padding: 10px 0 10px 30px; border-left: 3px solid #10B981; margin-left: 35px; color: #047857; font-size: 14px; font-weight: 700;">
      ▼ 엣지: <strong>[DERIVED_FROM / 공학적 제안공식 및 통계보정의 산출근거가 됨]</strong>
    </div>

    <!-- 노드 3 -->
    <div style="background-color: #FFFBEB; border: 1.5px solid #FCD34D; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 12px; font-weight: 800; color: #B45309; margin-bottom: 2px;">[목적어 노드이자 다음 주어 : 설계 입력값]</div>
      <strong style="font-size: 16px; color: #78350F;">대표 설계 지반정수</strong>
      <span style="font-size: 13px; color: #64748B; margin-left: 6px;">(속성: c = 15.0 kN/㎡, Φ = 35.0°, 변형계수 E = 85.0 MPa)</span>
    </div>

    <!-- 엣지 3 -->
    <div style="padding: 10px 0 10px 30px; border-left: 3px solid #F59E0B; margin-left: 35px; color: #B45309; font-size: 14px; font-weight: 700;">
      ▼ 엣지: <strong>[APPLIED_TO / 흙막이 단면 안정성 수치해석에 적용됨]</strong>
    </div>

    <!-- 노드 4 -->
    <div style="background-color: #FAF5FF; border: 1.5px solid #D8B4FE; border-radius: 8px; padding: 14px 18px;">
      <div style="font-size: 12px; font-weight: 800; color: #7E22CE; margin-bottom: 2px;">[최종 목적어 노드 : 공사 목적물]</div>
      <strong style="font-size: 16px; color: #581C87;">101정거장 흙막이 가시설 벽체</strong>
      <span style="font-size: 13px; color: #64748B; margin-left: 6px;">(속성: 굴착고 12.5m, 버팀보 3단 지보공, 지중연속벽 단면)</span>
    </div>

  </div>

  <p>
    이처럼 노드와 엣지로 온톨로지를 구축했을 때 얻을 수 있는 가장 결정적인 힘은 바로 <strong>'양방향 인과추적(Bi-directional Lineage)'</strong>입니다.
  </p>

  <ul style="padding-left: 20px; line-height: 1.9; color: #334155; margin-bottom: 20px;">
    <li>
      <strong>역방향 근거 추적 (Traceability):</strong><br>
      감리단이나 심의위원이 "101정거장 가시설 벽체의 마찰각 35도 근거가 뭡니까?"라고 물었을 때, 시스템은 <strong>[APPLIED_TO]</strong>와 <strong>[DERIVED_FROM]</strong>이라는 엣지(관계선)를 거꾸로 타고 올라가 <strong>"시추공 DT-00의 심도 7.5m 시험치에서 유래한 값"</strong>임을 단 1초 만에 논리적으로 증명합니다.
    </li>
    <li>
      <strong>순방향 리스크 영향도 분석 (Impact Analysis):</strong><br>
      만약 굴착 공사 중 시추공 DT-00 부근에서 지하수위가 급상승하거나 예상보다 연약층이 깊게 나온다면, 이 노드에 연결된 엣지를 추적하여 <strong>"어떤 정거장 가시설 단면을 긴급 재검토해야 하는가?"</strong>를 사전에 자동으로 경보할 수 있습니다.
    </li>
    <li>
      <strong>환각(Hallucination)의 원천 차단:</strong><br>
      AI가 문장을 그럴싸하게 지어내는 것이 아니라, <strong>엄격하게 검증된 노드와 엣지의 경로(Path)만을 따라 답변</strong>하기 때문에 거짓말을 하지 못합니다.
    </li>
  </ul>

  <p>
    <span style="background-color: #E8F8EE; color: #038A3E; padding: 3px 8px; border-radius: 4px; font-weight: 700;">
      "단순한 텍스트 챗봇이 아니라, 보고서 간의 인과관계를 엣지로 꿰어주는 온톨로지 시스템을 우리 현장에 직접 구축해보자!"
    </span><br>
    이것이 무모해 보였던 이 프로젝트를 끝내 시작하게 만든 진짜 원동력이었습니다.
  </p>

  <hr style="border: none; border-top: 1px dashed #D9DCE0; margin: 35px 0;">

  <!-- 섹션 3 -->
  <h2 style="font-size: 21px; font-weight: 800; color: #111111; border-left: 4px solid #03C75A; padding-left: 12px; margin: 30px 0 16px 0;">
    3. 왜 '지반조사'를 첫 번째 MVP(최소 기능 제품)로 선택했는가?
  </h2>

  <p>
    물론 최종적인 목표는 지반에만 머무르지 않습니다.<br>
    현장에는 구조물(정거장, 교량), 가시설, 궤도, 공정표, 시방서, 그리고 설계변경 이력까지 수많은 엔지니어링 도서들이 존재합니다. 장기적으로는 이 모든 현장 문서들을 하나의 지식망으로 연결하는 것이 궁극적인 지향점입니다.
  </p>

  <p>
    하지만 처음부터 현장 전체 도서를 모두 다루는 것은 현실적으로 불가능합니다.<br>
    그래서 데이터의 구조가 가장 까다롭고, 공학적 인과관계가 뚜렷한 <strong>'지반조사 및 지반설계' 분야를 첫 번째 MVP(Minimum Viable Product, 최소 기능 제품)로 선정</strong>하여 테스트해보기로 했습니다.
  </p>

  <ul style="padding-left: 20px; line-height: 1.9; color: #444444; margin-bottom: 20px;">
    <li>시추주상도라는 정형화된 격자 표(Table)가 존재함</li>
    <li>N치, 심도, 지하수위 같은 정량적 수치와 지층명 같은 비정형 텍스트가 공존함</li>
    <li>'조사 → 정수 산정 → 가시설 설계'라는 명확한 단계별 인과관계를 가지고 있음</li>
  </ul>

  <p>
    즉, <strong>가장 복잡하고 까다로운 지반 도메인에서 온톨로지와 RAG의 결합 모델을 성공적으로 검증해 낸다면, 향후 다른 공종(구조, 궤도, 시방서 등)으로 확장하는 것은 훨씬 수월할 것</strong>이라는 판단이었습니다.
  </p>

  <hr style="border: none; border-top: 1px dashed #D9DCE0; margin: 35px 0;">

  <!-- 섹션 4 -->
  <h2 style="font-size: 21px; font-weight: 800; color: #111111; border-left: 4px solid #03C75A; padding-left: 12px; margin: 30px 0 16px 0;">
    4. 구글 API를 활용해 이제 막 시작한 단계
  </h2>

  <p>
    아이디어는 명확했지만, 실제 구현은 차근차근 풀어가야 할 과제들이 많았습니다.
  </p>

  <p>
    지반조사보고서는 일반 텍스트뿐만 아니라 시추주상도 같은 2D 표와 도면 이미지가 많아서 일반적인 텍스트 파서로는 제대로 읽어내기 힘듭니다.<br>
    그래서 복잡한 문서 구조를 비교적 잘 인식하는 <strong>Google GenAI(Gemini) API</strong>의 멀티모달 기능을 활용하기로 했고,<br>
    정밀한 수치 조건(예: N치 범위, 심도 등)은 오차 없이 뽑아내기 위해 <strong>경량 SQL 데이터베이스(SQLite)</strong>를 함께 결합하는 방식을 잡았습니다.
  </p>

  <p>
    현재는 다음과 같은 기초 작업들을 하나씩 구현하고 테스트해보는 중입니다.
  </p>

  <div style="background-color: #F8FAFC; border-left: 4px solid #64748B; padding: 14px 18px; margin: 18px 0; font-size: 15px; color: #334155;">
    • 주요 시추주상도 PDF에서 시추공 번호와 심도별 데이터를 정형 데이터로 추출<br>
    • 정밀한 수치 필터링을 위한 질의-SQL 연동<br>
    • 시추공, 지층, 주요 구조물 위치를 잇는 지식 그래프(온톨로지) 프로토타입 구성<br>
    • 구글 API 호출 시 대용량 파일 업로드 부하를 줄이기 위한 파일 캐싱 처리
  </div>

  <p>
    아직 갈 길이 멀고, 실제로 의도한 대로 완벽하게 연결관계를 짚어내기까지는 여러 가지 튜닝과 수정이 필요한 상태입니다.
  </p>

  <hr style="border: none; border-top: 1px dashed #D9DCE0; margin: 35px 0;">

  <!-- 섹션 5 -->
  <h2 style="font-size: 21px; font-weight: 800; color: #111111; border-left: 4px solid #03C75A; padding-left: 12px; margin: 30px 0 16px 0;">
    5. 앞으로의 연재 계획
  </h2>

  <p>
    이 블로그 연재는 완성된 솔루션을 소개하는 글이 아닙니다.<br>
    실제 건설현장 문서를 가지고 RAG와 온톨로지 시스템을 만들어가면서, <strong>"어떤 고민을 했고, 어떤 기술적 문제에 부딪혔으며, 이를 어떻게 풀어가고 있는지"</strong>를 담담하게 기록하는 일지 형식에 가깝습니다.
  </p>

  <p>
    앞으로 대략 이런 주제들을 순서대로 다뤄보려 합니다.
  </p>

  <ol style="padding-left: 20px; line-height: 1.9; color: #444444; margin-bottom: 25px;">
    <li><strong>기존 벡터 검색의 아쉬움:</strong> 일반적인 텍스트 청킹으로 시추주상도 표를 다루기 어려웠던 이유</li>
    <li><strong>구글 Gemini API 적용:</strong> 도면과 표가 섞인 복합 기술도서를 읽히는 과정</li>
    <li><strong>파일 관리와 캐싱:</strong> 대용량 기술도서를 효율적으로 다루기 위한 캐시 구조 설계</li>
    <li><strong>정형 데이터(SQL) 결합:</strong> N치, 지하수위 같은 정량적 데이터를 오차 없이 조회하기 위한 하이브리드 구성</li>
    <li><strong>온톨로지 구현과 연결관계 시각화:</strong> 시추 데이터에서 설계 반영까지의 인과관계를 엮는 과정</li>
    <li><strong>현장 실무 관점의 UI:</strong> 근거 페이지 확인과 결과 추적(Trace) 기능</li>
    <li><strong>MVP 검증 이후의 확장:</strong> 지반을 넘어 현장 전체 도서(구조, 궤도, 공정 등)로 확장하기 위한 로드맵</li>
  </ol>

  <p>
    현업에서 기술도서 검토 업무를 하시며 비슷한 번거로움을 느끼셨던 분들이나, 도메인 특화 RAG를 준비하시는 분들과 유용한 고민을 함께 나눌 수 있는 계기가 되었으면 합니다.
  </p>

  <div style="background-color: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 15px 18px; margin: 25px 0; color: #065F46; font-size: 15px;">
    <strong>[다음 글 예고]</strong><br>
    다음 글에서는 <strong>"일반적인 벡터 임베딩 방식으로 시추주상도 문서를 처리하려 했을 때 마주했던 현실적인 한계"</strong>에 대해 정리해 보겠습니다.
  </div>

  <!-- 태그 영역 -->
  <div style="margin-top: 35px; padding-top: 15px; border-top: 1px solid #EEEEEE; font-size: 14px; color: #028A3E;">
    #스마트건설 #동탄트램 #건설RAG #지반엔지니어링 #온톨로지 #지식그래프 #생성형AI #GeminiAPI #건설DX
  </div>

</div>
"""

def main():
    html_content = build_post_1_html()
    
    # 1. HTML 파일 저장
    output_html_path = Path(__file__).parent / "naver_blog_post_01.html"
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>동탄트램 RAG 구축기 #1</title>
</head>
<body style="background-color: #f0f2f5; padding: 30px 15px;">
  <div style="background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); max-width: 800px; margin: 0 auto;">
    {html_content}
  </div>
</body>
</html>""")
    print(f"[OK] HTML 파일 생성 완료: {output_html_path}")

    # 2. 클립보드에 HTML(CF_HTML) 복사
    plain_text = "동탄트램 RAG 구축기 #1 본문입니다. 네이버 블로그에 붙여넣기(Ctrl+V) 하세요."
    try:
        set_clipboard_html_and_text(html_content, plain_text)
        print("[SUCCESS] 클립보드에 네이버 블로그 서식(CF_HTML) 복사 완료!")
        print(">> 지금 바로 네이버 블로그 스마트에디터에 가서 'Ctrl + V'를 누르시면 됩니다!")
    except Exception as e:
        print(f"[ERROR] 클립보드 복사 실패: {e}")

if __name__ == "__main__":
    main()
