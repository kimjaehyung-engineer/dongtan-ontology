# Project Rules - Dongtan Tram Manual Workspace

## Image Preservation Rule
* **CRITICAL:** Do NOT modify, replace, or alter the image file path `tram_diagram_korean_simple.png` or its corresponding HTML elements (`<img ... src="./tram_diagram_korean_simple.png" ...>`) inside the manual files. This simplified technical interface diagram must be preserved exactly as-is under all circumstances.

## Plan-First Policy for Heavy Token Tasks (SVG/Drawings)
* **CRITICAL:** Whenever the user requests tasks that consume a large number of tokens (such as generating, modifying, or regenerating SVG drawings or complex codes), ALWAYS formulate an `implementation_plan.md` first. DO NOT execute the code modification or start the work immediately. You MUST explicitly wait for the user's manual approval (Proceed) before proceeding to the actual execution phase.

## Section 1.3 (Cross-section Diagram & Info Panel) Freeze Policy
* **CRITICAL:** The HTML block containing the cross-section SVG drawing and its info panel table (sec-1-3 in `08.메뉴얼 및 평면도/동탄트램_업무_매뉴얼.html`) is strictly FROZEN. Do NOT modify, update, or rewrite this section under any circumstances without explicit, direct instructions from the user. If you believe modifying this section is necessary due to changes in other areas, you MUST report it to the user and obtain explicit manual approval before making any changes.

## Two-File Architecture Policy (Map & Manual Integration)
* **CRITICAL:** The project relies on a tightly coupled two-file architecture: `동탄트램_노선평면도.html` (Visual Dashboard/Map) and `동탄트램_업무_매뉴얼.html` (Detailed Engineering Encyclopedia). 
* When adding new interactive features, always design them to cross-link these two files using standardized URL query parameters (e.g., `?openModal=station&id=206`) so that the Map serves as the entry point and the Manual provides the deep-dive content via auto-scrolling and dynamic modals.



## Fixed HTML Styling & Layout Freeze Policy
* **CRITICAL:** The HTML layout, CSS design tokens, light theme defaults, dashboard column locks (`flex-wrap: nowrap`), box left alignments (`margin-left: 0`), and heading typography established for `동탄트램_업무_매뉴얼.html` are strictly FROZEN. Do NOT modify, alter, or rewrite these core styles or structural layout rules without explicit, direct instructions from the user.


## Master HTML & CSS Design Lock Policy (최종 서식 완벽 동결 조치)
* **CRITICAL:** The user has explicitly confirmed that the current formatting, typography, image presentations, uniform box borders, dashboard 2-column locks (`flex-wrap: nowrap`), flush-left alignments, and clean heading layouts established as of June 29, 2026 are **THE MOST SATISFACTORY & PERFECT**. 
* When adding, modifying, updating, or inserting text, tables, or engineering content in `동탄트램_업무_매뉴얼.html` or `동탄트램_노선평면도.html`, you MUST **NEVER** alter, modify, overwrite, or touch these CSS styles, design tokens, layout wrappers, or structural alignment rules without explicit, direct instructions from the user.

## No Browser Subagent Policy (가상 브라우저 에이전트 사용 금지)
* **CRITICAL:** The `browser_subagent` tool is STRICTLY PROHIBITED in this workspace under ALL circumstances. Do NOT invoke browser_subagent for any purpose — including UI validation, screenshot capture, page verification, or QA checks.
* All validation and verification MUST be performed exclusively through:
  - Python scripts (`run_command` with Python)
  - `grep_search` / `view_file` for code inspection
  - Direct file reads and text analysis
* This rule was established by the user on 2026-07-09 and applies permanently to all future sessions in this workspace.


## Light-Theme Only Policy for SVG & Technical Diagrams (도식/그림 밝은 계열 준수 수칙)
* **CRITICAL:** All SVG drawings, technical engineering diagrams, cross-section illustrations, and image containers embedded inside standard, guideline, or checklist HTML files MUST ALWAYS use **Light Theme backgrounds** (e.g., #f8fafc, #f1f5f9, #ffffff, #f0f9ff). 
* **NEVER** use dark or black background fills (#0f172a, #090d16, g-slate-900, g-slate-950) for SVG/diagram containers under any circumstances. Text and lines within diagrams must use high-contrast dark tones (#0f172a, #1e293b, #0369a1, #b45309) for optimal legibility.


## Flexible Step Sequence Policy for Guidelines (수행지침 단계 수 유연화 수칙)
* **CRITICAL:** When drafting Guideline HTML files (수행지침서), do NOT forcefully fix or lock the sequence to exactly 5 steps.
* **FLEXIBILITY:** The number of steps (e.g., 3-Step, 4-Step, 5-Step, or 6-Step Master Architecture) MUST be dynamically adjusted depending on the specific engineering complexity and intuitive clarity required for each individual Activity/WBS item. Choose whatever step count best explains the task to field engineers.


## Clickable Diagram Lightbox Zoom Modal Policy (도식/그림 클릭 시 대형 팝업 확대 수칙)
* **CRITICAL:** All technical diagrams, SVG cross-section drawings, and embedded images inside Guideline HTML files MUST support a **Clickable Lightbox Zoom Modal (`openDiagramZoom`)**.
* **INTERACTION:** When a user clicks on any diagram container (`class="clickable-diagram"`), a dedicated full-screen overlay modal (`#zoomModal`) MUST pop up, rendering the SVG/image in an enlarged, high-resolution view (520px+ height) so all small texts and engineering labels can be clearly read.
* **LEGIBILITY:** All SVG text font-sizes MUST be set to **11px to 14px or larger** with bold styling for immediate legibility.

## WBS 11 Construction Plan Master Page Freeze Policy (시공계획 수립 마스터 페이지 영구 동결 수칙)
* **STRICT CRITICAL:** The HTML files for WBS 11 `[공통] 시공계획 수립` (`시공계획 수립_표준서.html`, `시공계획 수립_수행지침.html`, `시공계획 수립_체크리스트.html`) are **PERMANENTLY FROZEN**. 
* **NEVER** modify, alter, overwrite, or touch the contents, scripts, interactive simulators, SVG diagrams, or styling of the WBS 11 master pages under any circumstances without explicit, direct instructions from the user.


## 1:1 Mandatory Step-by-Step Visual & Simulation Insertion Policy (단계별 그림/시뮬레이션/사진 필수 수록 룰)
* **STRICT CRITICAL:** When drafting or updating Guideline HTML files (수행지침서), EVERY single procedure step card (e.g., STEP 1, STEP 2, STEP 3, STEP 4...) MUST contain a 1:1 matching **intuitive 2D visual technical diagram, interactive simulation, or high-resolution field photo device**.
* **LEGIBILITY & INTUITIVENESS:** 
  - Never use plain abstract boxes or lines. Render actual equipment, rails, tools, molds, gauges, or worker poses so that field engineers can intuitively understand the task at first glance.
  - All SVG font-sizes MUST be set to **11px to 14px or larger** with bold styling for immediate legibility without zooming.
* **INTERACTION:** 
  - Every step visual container MUST support a **Clickable Lightbox Zoom Modal (`openDiagramZoom`)** to allow full-screen enlarged viewing (520px+ height).
  - Key technical terms inside step cards MUST link to dedicated **Glossary Explanations (`openGlossary`)**.


## Time-Chainage 공정표 2D 다이어그램 영구 무결성 및 사라짐 방지 강제 제약 수칙 (Time-Chainage Dashboard Zero-Disappearance Freeze Policy)
* **STRICT CRITICAL:** `동탄트램_Time_Chainage_공정표_대시보드.html` 파일의 SVG 2D 공정 다이어그램 렌더링 엔진(`renderSVG`, `renderAll`) 및 5대 세부 공종(토공, 노반, 상부강화노반, 궤도, 시스템) 색상 코딩 체계는 **STRICT FROZEN(영구 제약 동결)** 처리한다.
* **ZERO DISAPPEARANCE GUARANTEE:**
  1. 어떠한 경우에도 공정선이나 차트 화면이 백지화/사라짐(Disappearance/Blanking) 상태로 붕괴되는 것을 원천 금지한다.
  2. 모든 JS 렌더링 코드에는 `safeStr()`, `try-catch`, `X축 클리핑 영역 가드` 및 `Null Pointer Guard`를 반드시 100% 장착하여 예외가 터지더라도 기본 28개 시공구간 차트가 안전하게 항시 표출되어야 한다.
  3. 대시보드 수정 후에는 반드시 `node -c` 자바스크립트 구문 검사 및 28개 시공구간 자동화 검증 스크립트(`auto_validate_28_sections.py`)를 실행하여 `28 / 28 PASSED (100% 통과)` 결과를 필수 입증해야 한다.




