import * as XLSX from 'xlsx';
import type { Node, Edge } from 'reactflow';
import { MarkerType } from 'reactflow';
import type { NodeData, DisciplineMapItem } from '../store/useStore';

export interface ParsedWbsRow {
  wbsCode?: string;
  predecessor?: string;
  successor?: string;
  department: string;
  workType?: string;
  taskTitle: string;
  purpose?: string;
  phase: string;
  method?: string;
  result?: string;
  status?: string;
  sheetName?: string;
}

// 5대 표준 Phase 고정 정의
export const STANDARD_PHASES = [
  'PHASE 1: D-90 (사전조사 & 기획)',
  'PHASE 2: D-60 (인허가 & 발주)',
  'PHASE 3: D-30 (계약 & 시공계획)',
  'PHASE 4: D-Day (착공 준비 & 점검)',
  'PHASE 5: D+10~75 (본공사 집행)',
];

// 엑셀 텍스트 내의 특수기호(☐, [더블클릭]) 및 더미 안내문구 정제 헬퍼
function sanitizeMethod(rawMethod: string | undefined, taskTitle: string): string {
  if (rawMethod) {
    let cleaned = rawMethod
      .replace(/[☐☑☒\u25A1\u2610\uFFFD]/g, '')
      .replace(/\[더블클릭\]/g, '')
      .replace(/수행지침 열기/g, '')
      .trim();
    if (cleaned.length > 2) return cleaned;
  }

  const t = taskTitle.toLowerCase();
  if (t.includes('타설') || t.includes('콘크리트') || t.includes('콜드조인트')) {
    return '타설속도/인원 수급 계획 수립 및 연속 타설 지연 방지 동선 확보, 펌프카 2대 배치 관리';
  }
  if (t.includes('인터페이스') || t.includes('유관') || t.includes('검토')) {
    return '토목/전기/신호 주간 빅룸(Big Room) 회의를 통한 공종 간 정합성 체크 및 이설 간섭 수치 검증';
  }
  if (t.includes('동선') || t.includes('가설') || t.includes('반입')) {
    return '장비 반입구 및 타공종 가설 반입로 하중 지지력 검토, 도로점용 동선 시뮬레이션';
  }
  if (t.includes('외산') || t.includes('자재') || t.includes('선적')) {
    return '외국 자재 제작사 출하 검수(FAT) 일정 확인 및 통관/국내 운송 스케줄 사전 모니터링';
  }
  if (t.includes('지지력') || t.includes('품질') || t.includes('검사')) {
    return 'KCS 표준시방서 규정에 의거한 평판재하시험(PBT) 및 지지력 측정 승인';
  }
  if (t.includes('안전') || t.includes('위험') || t.includes('보건')) {
    return '작업 전 위험성평가(TBM) 실시 및 안전보호구 착용, 장비 점검표 작성';
  }
  if (t.includes('인허가') || t.includes('협의') || t.includes('승인')) {
    return '관계기관 및 지자체 사전 방문 협의, 설계도서 및 인허가 제출 서류 정밀 검토';
  }

  return '표준 시방 지침 준수 및 작업 전 안전·품질 수행절차 체크리스트 확인';
}

function sanitizeText(rawStr: string | undefined, defaultVal: string): string {
  if (!rawStr) return defaultVal;
  const cleaned = rawStr
    .replace(/[☐☑☒\u25A1\u2610\uFFFD]/g, '')
    .replace(/\[더블클릭\]/g, '')
    .replace(/수행지침 열기/g, '')
    .trim();
  return cleaned.length > 1 ? cleaned : defaultVal;
}

// 엑셀 주관부서 및 액티비티명을 표준 6대 세로축 행으로 고정 분류하는 핵심 도우미
function classifyDepartment(deptRaw: string, taskTitleRaw: string): {
  mainCategory: '현장' | '본사';
  subDept: '공무' | '공사' | '품질' | '안전' | '관리' | '본사';
  rowIndex: number;
  yBase: number;
  color: string;
} {
  const deptText = (deptRaw || '').toLowerCase().replace(/\s+/g, '');
  const titleText = (taskTitleRaw || '').toLowerCase();
  const fullText = deptText + ' ' + titleText;

  // 1. 주관부서에 '공무', '소장', '계약', '인허가' 포함 시 100% 최우선 [현장 · 공무] 행 (Row 0, yBase: 170)
  if (
    deptText.includes('공무') ||
    deptText.includes('소장') ||
    deptText.includes('계약') ||
    deptText.includes('인허가')
  ) {
    return { mainCategory: '현장', subDept: '공무', rowIndex: 0, yBase: 170, color: '' };
  }

  // 2. 주관부서에 '품질'
  if (deptText.includes('품질')) {
    return { mainCategory: '현장', subDept: '품질', rowIndex: 2, yBase: 2670, color: '' };
  }

  // 3. 주관부서에 '안전', '보건', '환경'
  if (deptText.includes('안전') || deptText.includes('보건') || deptText.includes('환경')) {
    return { mainCategory: '현장', subDept: '안전', rowIndex: 3, yBase: 3920, color: '' };
  }

  // 4. 주관부서에 '관리', '총무', '용지'
  if (deptText.includes('관리') || deptText.includes('총무') || deptText.includes('용지')) {
    return { mainCategory: '현장', subDept: '관리', rowIndex: 4, yBase: 5170, color: '' };
  }

  // 5. 주관부서에 '본사', '외주'
  if (deptText.includes('본사') || deptText.includes('외주') || deptText.includes('컴플라이언스')) {
    return { mainCategory: '본사', subDept: '본사', rowIndex: 5, yBase: 6420, color: '' };
  }

  // 6. 주관부서에 '공사', '시공', '기술'
  if (deptText.includes('공사') || deptText.includes('시공') || deptText.includes('기술')) {
    return { mainCategory: '현장', subDept: '공사', rowIndex: 1, yBase: 1420, color: '' };
  }

  // 7. 작업명(Title) 키워드로 2차 분류
  if (
    fullText.includes('공무') ||
    fullText.includes('소장') ||
    fullText.includes('계약') ||
    fullText.includes('인허가') ||
    fullText.includes('설계') ||
    fullText.includes('검토') ||
    fullText.includes('신청') ||
    fullText.includes('협의') ||
    fullText.includes('승인') ||
    fullText.includes('도면') ||
    fullText.includes('착공') ||
    fullText.includes('수전') ||
    fullText.includes('big room')
  ) {
    return { mainCategory: '현장', subDept: '공무', rowIndex: 0, yBase: 170, color: '' };
  }

  return { mainCategory: '현장', subDept: '공사', rowIndex: 1, yBase: 1420, color: '' };
}

// 작업명/Phase 텍스트 및 순서 비율(Ratio) 기반으로 5대 Phase에 적절히 분배하는 도우미
function classifyPhaseIndex(phaseRaw: string, taskTitleRaw: string, rIdx: number, totalRows: number): number {
  const text = (phaseRaw + ' ' + taskTitleRaw).toLowerCase();

  if (text.includes('d-90') || text.includes('d90') || text.includes('d-100') || text.includes('d-120') || text.includes('사전') || text.includes('조사') || text.includes('기획') || text.includes('현황') || text.includes('측량') || text.includes('gpr')) {
    return 0; // PHASE 1
  }
  if (text.includes('d-60') || text.includes('d60') || text.includes('d-70') || text.includes('d-80') || text.includes('인허가') || text.includes('협의') || text.includes('점용') || text.includes('승인') || text.includes('심의') || text.includes('경찰')) {
    return 1; // PHASE 2
  }
  if (text.includes('d-30') || text.includes('d30') || text.includes('계약') || text.includes('발주') || text.includes('입찰') || text.includes('견적') || text.includes('선정')) {
    return 2; // PHASE 3
  }
  if (text.includes('d-day') || text.includes('dday') || text.includes('p+0') || text.includes('d-0') || text.includes('착공') || text.includes('동원') || text.includes('big room') || text.includes('교육')) {
    return 3; // PHASE 4
  }
  if (text.includes('d+') || text.includes('p+') || text.includes('시공') || text.includes('집행') || text.includes('본시공') || text.includes('검수') || text.includes('이설') || text.includes('철거') || text.includes('복구')) {
    return 4; // PHASE 5
  }

  // 명시적 키워드가 없을 경우, 전체 WBS 순서 비율(0.0~1.0)을 5등분하여 자연스러운 공정 흐름으로 가로 배치
  if (totalRows <= 1) return 0;
  const ratio = rIdx / Math.max(1, totalRows - 1);
  if (ratio < 0.2) return 0;
  if (ratio < 0.4) return 1;
  if (ratio < 0.6) return 2;
  if (ratio < 0.8) return 3;
  return 4;
}

export function buildNodesAndEdgesFromRows(
  rows: ParsedWbsRow[],
  mapTitle: string
): { nodes: Node<NodeData>[]; edges: Edge[] } {
  const nodes: Node<NodeData>[] = [];
  const edges: Edge[] = [];

  const colWidth = 1800;
  const phaseStartOffset = 260;
  const totalCanvasWidth = Math.max(11500, STANDARD_PHASES.length * colWidth + 800);

  // 1. Master Frame
  nodes.push({
    id: 'map-frame-master',
    type: 'mapFrame',
    position: { x: -40, y: -150 },
    data: { label: `🏢 ${mapTitle}` },
    style: { width: totalCanvasWidth + 100, height: 7800, zIndex: -10 },
    draggable: false,
    selectable: false,
  });

  // 2. Swimlanes (단일 세로축 헤더 - y=100부터 시작하여 마일스톤 헤더와 간섭 0%)
  const swimlanes = [
    { id: 'swimlane-공무', category: '현장', label: '공무 / 계약 / 인허가', y: 100, height: 1250, isCategoryFirst: false, categorySpanHeight: 1250 },
    { id: 'swimlane-공사', category: '현장', label: '공사 / 현장 시공', y: 1350, height: 1250, isCategoryFirst: false, categorySpanHeight: 1250 },
    { id: 'swimlane-품질', category: '현장', label: '품질 / 시공 품질', y: 2600, height: 1250, isCategoryFirst: false, categorySpanHeight: 1250 },
    { id: 'swimlane-안전', category: '현장', label: '안전 / 보건 / 환경', y: 3850, height: 1250, isCategoryFirst: false, categorySpanHeight: 1250 },
    { id: 'swimlane-관리', category: '현장', label: '관리 / 용지 / 총무', y: 5100, height: 1250, isCategoryFirst: false, categorySpanHeight: 1250 },
    { id: 'swimlane-본사', category: '본사', label: '본사 / 전략 / 지원', y: 6350, height: 1250, isCategoryFirst: false, categorySpanHeight: 1250 },
  ];

  swimlanes.forEach(s => {
    nodes.push({
      id: s.id,
      type: 'swimlane',
      position: { x: 0, y: s.y },
      data: {
        label: s.label,
        category: s.category,
        isCategoryFirst: s.isCategoryFirst,
        categorySpanHeight: s.categorySpanHeight,
      },
      style: { width: totalCanvasWidth, height: s.height, zIndex: -1 },
      draggable: false,
      selectable: true,
    });
  });

  // Row Dividers
  nodes.push({ id: 'rdiv-1', type: 'rowDivider', position: { x: 0, y: 100 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });
  nodes.push({ id: 'rdiv-2', type: 'rowDivider', position: { x: 0, y: 1350 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });
  nodes.push({ id: 'rdiv-3', type: 'rowDivider', position: { x: 0, y: 2600 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });
  nodes.push({ id: 'rdiv-4', type: 'rowDivider', position: { x: 0, y: 3850 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });
  nodes.push({ id: 'rdiv-5', type: 'rowDivider', position: { x: 0, y: 5100 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });
  nodes.push({ id: 'rdiv-6', type: 'rowDivider', position: { x: 0, y: 6350 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });
  nodes.push({ id: 'rdiv-7', type: 'rowDivider', position: { x: 0, y: 7600 }, data: { width: totalCanvasWidth }, draggable: true, selectable: false, style: { zIndex: 10 } });

  // 3. Phase Headers (Vertical Columns) - y=20 위치로 내리고 40px 안전 여백으로 간섭 0% 보장
  STANDARD_PHASES.forEach((phaseName, pIdx) => {
    const xPos = phaseStartOffset + pIdx * colWidth;

    // Phase 왼쪽 구분선 (마스터 타이틀 헤더 바 경계 y=-22 너머 y=-35까지 끝까지 완전 상단 밀착)
    nodes.push({
      id: `vline-phase-${pIdx}`,
      type: 'verticalLine',
      position: { x: xPos, y: -35 },
      data: { label: phaseName, height: 7650 },
      style: { zIndex: 12 },
    });

    // Phase 오른쪽 경계 세로 구분선 (마지막 Phase 우측선 포함)
    nodes.push({
      id: `vline-phase-right-${pIdx}`,
      type: 'verticalLine',
      position: { x: xPos + colWidth, y: -35 },
      data: { label: `${phaseName} End`, height: 7650 },
      style: { zIndex: 12 },
    });

    // Phase 헤더 마일스톤 노드를 수직 정중앙(상단 32px = 하단 32px)에 정밀 배치
    const milestoneWidth = 560;
    const centerX = xPos + (colWidth / 2) - (milestoneWidth / 2);

    nodes.push({
      id: `header-phase-${pIdx}`,
      type: 'milestone',
      position: { x: centerX, y: 12 },
      data: {
        label: `📅 ${phaseName}`,
        date: `Phase ${pIdx + 1}`,
        status: 'normal',
      },
      style: { width: milestoneWidth },
    });
  });

  // 4. Action Cards Placement into 5 Standard Phases & 6 Standard Rows (카드 크기: 폭 480px, 높이 500px)
  const cellCounts: { [key: string]: number } = {};
  const createdCardNodes: { id: string; pIdx: number; title: string; wbsCode?: string }[] = [];
  const totalRows = rows.length;

  rows.forEach((row, rIdx) => {
    const cls = classifyDepartment(row.department, row.taskTitle);
    const pIdx = classifyPhaseIndex(row.phase, row.taskTitle, rIdx, totalRows);

    const cellKey = `${cls.rowIndex}_${pIdx}`;
    const stackIndex = cellCounts[cellKey] || 0;
    cellCounts[cellKey] = stackIndex + 1;

    const baseX = phaseStartOffset + pIdx * colWidth + 90;

    // 겹침 0% 완전 차단 & 시원한 가로 간격(640px): 연결선 시인성 200% 극대화
    const colInCell = stackIndex % 2;
    const rowInCell = Math.floor(stackIndex / 2);

    const cardX = baseX + colInCell * 640;
    const cardY = cls.yBase + rowInCell * 560;

    // 액티비티 명을 100% 카드 제목(상단 파랑/보라 헤더 bar)으로 바인딩!
    const cardLabel = row.taskTitle;
    const cardId = `excel-card-${rIdx + 1}`;
    const wbsCode = row.wbsCode || `WBS-${rIdx + 1}`;

    const deptBadgeText = row.department
      ? `${cls.mainCategory} · ${cls.subDept} (${row.department})`
      : `${cls.mainCategory} · ${cls.subDept}`;

    nodes.push({
      id: cardId,
      type: 'action',
      position: { x: cardX, y: cardY },
      data: {
        label: cardLabel,
        wbsCode: wbsCode,
        predecessor: row.predecessor || '',
        successor: row.successor || '',
        category: cls.mainCategory,
        department: deptBadgeText,
        purpose: sanitizeText(row.purpose, 'WBS 공정 이행 및 표준 시방 검토'),
        method: sanitizeMethod(row.method, row.taskTitle),
        result: sanitizeText(row.result, '검수 승인 및 성과품 제출'),
        status: 'normal',
        color: cls.color,
        swimlane: cls.subDept,
        isCritical: rIdx % 2 === 0,
        date: row.phase || '',
      },
      style: { width: 480, height: 500 },
    });

    createdCardNodes.push({ id: cardId, pIdx, title: row.taskTitle, wbsCode });
  });

  // 4.1. 각 Phase별 수집된 카드들의 D-Day 기한 텍스트 분석 후 상단 PHASE 헤더 상자 제목 동적 업데이트
  const phaseDdayMap: { [pIdx: number]: string[] } = {};
  rows.forEach((row, rIdx) => {
    const pIdx = classifyPhaseIndex(row.phase, row.taskTitle, rIdx, totalRows);
    if (!phaseDdayMap[pIdx]) phaseDdayMap[pIdx] = [];
    if (row.phase && row.phase.trim()) {
      phaseDdayMap[pIdx].push(row.phase.trim());
    }
  });

  STANDARD_PHASES.forEach((defaultPhaseName, pIdx) => {
    const ddays = phaseDdayMap[pIdx] || [];
    let dynamicTitle = defaultPhaseName;

    // D-Day 문자열(예: D-240~D-210, D-90, D-60 등)에서 숫자 파싱
    const numbers: number[] = [];
    ddays.forEach(dStr => {
      const matches = dStr.match(/D\s*([+-]?\d+)/gi);
      if (matches) {
        matches.forEach(m => {
          const numMatch = m.match(/([+-]?\d+)/);
          if (numMatch) {
            const parsed = parseInt(numMatch[1], 10);
            if (!isNaN(parsed)) numbers.push(parsed);
          }
        });
      }
    });

    if (numbers.length > 0) {
      const minVal = Math.min(...numbers);
      const maxVal = Math.max(...numbers);

      const formatDday = (n: number) => (n > 0 ? `D+${n}` : n === 0 ? `D-Day` : `D${n}`);
      const rangeStr = minVal === maxVal ? formatDday(minVal) : `${formatDday(minVal)}~${formatDday(maxVal)}`;

      const phaseNum = pIdx + 1;
      const subNameMatch = defaultPhaseName.match(/\((.*?)\)/);
      const subName = subNameMatch ? ` (${subNameMatch[1]})` : '';
      dynamicTitle = `PHASE ${phaseNum}: ${rangeStr}${subName}`;
    }

    const milestoneNode = nodes.find(n => n.id === `header-phase-${pIdx}`);
    if (milestoneNode && milestoneNode.data) {
      milestoneNode.data.label = `📅 ${dynamicTitle}`;
    }
  });

  // 4.5. AABB (Axis-Aligned Bounding Box) 카드 노드 강제 겹침 0% 분리 알고리즘
  const actionNodes = nodes.filter(n => n.type === 'action');
  const CARD_WIDTH = 640;
  const CARD_HEIGHT = 560;

  for (let i = 0; i < actionNodes.length; i++) {
    for (let j = i + 1; j < actionNodes.length; j++) {
      const nodeA = actionNodes[i];
      const nodeB = actionNodes[j];

      // A와 B의 겹침 감지 (Width 640px, Height 560px 사각형)
      const overlapX = Math.abs(nodeA.position.x - nodeB.position.x) < CARD_WIDTH;
      const overlapY = Math.abs(nodeA.position.y - nodeB.position.y) < CARD_HEIGHT;

      if (overlapX && overlapY) {
        // 겹침 발생 시 nodeB를 오른쪽으로 640px 밀어 수평 분리!
        nodeB.position.x += CARD_WIDTH;
      }
    }
  }

  // 4.6. 카드 배치 완료 후 캔버스 전체 폭 동적 측정 & 마스터 프레임/스윔레인/구분선 폭 넉넉히 확장
  let maxCardRightX = phaseStartOffset + STANDARD_PHASES.length * colWidth + 500;
  nodes.forEach(n => {
    if (n.type === 'action') {
      maxCardRightX = Math.max(maxCardRightX, n.position.x + 750);
    }
  });

  const finalCanvasWidth = Math.max(11500, maxCardRightX + 800);

  nodes.forEach(n => {
    if (n.id === 'map-frame-master') {
      n.style = { ...(n.style || {}), width: finalCanvasWidth + 100 };
    } else if (n.type === 'swimlane') {
      n.style = { ...(n.style || {}), width: finalCanvasWidth };
    } else if (n.type === 'rowDivider') {
      n.data = { ...(n.data || {}), width: finalCanvasWidth };
    }
  });

  // 5. Automatic Logical Process Flow Connections (L4 코드 선/후행 관계 기반 최단거리 동적 연결)
  const normalizeCode = (c: string) => {
    if (!c) return '';
    return c
      .trim()
      .toUpperCase()
      .replace(/\s+/g, '')
      .replace(/9000-0*(\d+)-0*(\d+)/g, '9000-$1-$2');
  };

  const codeToNodeIdMap: { [wbsCode: string]: string } = {};
  const labelToNodeIdMap: { [label: string]: string } = {};

  createdCardNodes.forEach(c => {
    if (c.wbsCode) {
      codeToNodeIdMap[normalizeCode(c.wbsCode)] = c.id;
    }
    if (c.title) {
      labelToNodeIdMap[c.title.trim().replace(/\s+/g, '')] = c.id;
    }
  });

  const nodePosMap: { [nodeId: string]: { x: number; y: number } } = {};
  nodes.forEach(n => {
    nodePosMap[n.id] = { x: n.position.x, y: n.position.y };
  });

  // 두 노드의 위치 관계를 계산하여 가장 가까운 4방향 핸들 쌍(left/right/top/bottom)을 동적 반환
  const getShortestHandlePair = (sId: string, tId: string) => {
    const sPos = nodePosMap[sId] || { x: 0, y: 0 };
    const tPos = nodePosMap[tId] || { x: 0, y: 0 };
    const dx = tPos.x - sPos.x;
    const dy = tPos.y - sPos.y;

    // 수직 거리가 길고 가로 X 거리가 400px 미만이면 상하 최단거리 연결
    if (Math.abs(dx) < 400 && Math.abs(dy) > 100) {
      if (dy > 0) {
        return { sourceHandle: 'bottom-source', targetHandle: 'top-target' };
      } else {
        return { sourceHandle: 'top-source', targetHandle: 'bottom-target' };
      }
    }

    // 기본 우측 출구 -> 좌측 입구 (또는 역방향)
    if (dx >= 0) {
      return { sourceHandle: 'right-source', targetHandle: 'left-target' };
    } else {
      return { sourceHandle: 'left-source', targetHandle: 'right-target' };
    }
  };

  const addedEdgesSet = new Set<string>();

  rows.forEach((row, rIdx) => {
    const currId = `excel-card-${rIdx + 1}`;

    // A. 선행 L4 코드가 있는 경우: 선행 노드 -> 현재 노드
    if (row.predecessor && row.predecessor !== '-' && row.predecessor !== '없음') {
      const predCodes = row.predecessor.split(/[,;\/\n\r]+/).map(s => s.trim()).filter(Boolean);
      predCodes.forEach((pCode, pIdx) => {
        if (pCode === '-' || pCode === '없음') return;
        const normP = normalizeCode(pCode);
        let sourceId = codeToNodeIdMap[normP];
        if (!sourceId) {
          const cleanP = pCode.replace(/\s+/g, '');
          if (labelToNodeIdMap[cleanP]) sourceId = labelToNodeIdMap[cleanP];
        }

        if (sourceId && sourceId !== currId) {
          const edgeId = `edge-${sourceId}-${currId}`;
          if (!addedEdgesSet.has(edgeId)) {
            addedEdgesSet.add(edgeId);
            const { sourceHandle, targetHandle } = getShortestHandlePair(sourceId, currId);
            edges.push({
              id: edgeId,
              source: sourceId,
              target: currId,
              sourceHandle,
              targetHandle,
              type: 'smoothstep',
              animated: false,
              pathOptions: { borderRadius: 16, offset: (pIdx % 3) * 12 },
              style: { stroke: '#000000', strokeWidth: 5.5 },
              markerEnd: { type: MarkerType.ArrowClosed, color: '#000000', width: 24, height: 24 },
            });
          }
        }
      });
    }

    // B. 후행 L4 코드가 있는 경우: 현재 노드 -> 후행 노드
    if (row.successor && row.successor !== '-' && row.successor !== '없음') {
      const succCodes = row.successor.split(/[,;\/\n\r]+/).map(s => s.trim()).filter(Boolean);
      succCodes.forEach((sCode, sIdx) => {
        if (sCode === '-' || sCode === '없음') return;
        const normS = normalizeCode(sCode);
        let targetId = codeToNodeIdMap[normS];
        if (!targetId) {
          const cleanS = sCode.replace(/\s+/g, '');
          if (labelToNodeIdMap[cleanS]) targetId = labelToNodeIdMap[cleanS];
        }

        if (targetId && targetId !== currId) {
          const edgeId = `edge-${currId}-${targetId}`;
          if (!addedEdgesSet.has(edgeId)) {
            addedEdgesSet.add(edgeId);
            const { sourceHandle, targetHandle } = getShortestHandlePair(currId, targetId);
            edges.push({
              id: edgeId,
              source: currId,
              target: targetId,
              sourceHandle,
              targetHandle,
              type: 'smoothstep',
              animated: false,
              pathOptions: { borderRadius: 16, offset: (sIdx % 3) * 12 },
              style: { stroke: '#000000', strokeWidth: 5.5 },
              markerEnd: { type: MarkerType.ArrowClosed, color: '#000000', width: 24, height: 24 },
            });
          }
        }
      });
    }
  });

  // C. 선/후행 명시적 정보가 없을 경우, 순차 연결 보조
  if (addedEdgesSet.size === 0) {
    for (let i = 0; i < createdCardNodes.length - 1; i++) {
      const curr = createdCardNodes[i];
      const next = createdCardNodes[i + 1];
      const isCp = i % 2 === 0;
      const { sourceHandle, targetHandle } = getShortestHandlePair(curr.id, next.id);

      edges.push({
        id: `edge-${curr.id}-${next.id}`,
        source: curr.id,
        target: next.id,
        sourceHandle,
        targetHandle,
        type: 'smoothstep',
        animated: false,
        pathOptions: { borderRadius: 16 },
        style: {
          stroke: isCp ? '#b91c1c' : '#000000',
          strokeWidth: isCp ? 6 : 5.5,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: isCp ? '#b91c1c' : '#000000',
          width: 18,
          height: 18,
        },
      });
    }
  }

  return { nodes, edges };
}

// ✨ 수동으로 이동/조정한 카드 위치 및 변경 서식 머지 헬퍼 함수
export function mergeExistingNodePositions(
  newNodes: Node<NodeData>[],
  existingNodes: Node<NodeData>[]
): Node<NodeData>[] {
  if (!existingNodes || existingNodes.length === 0) return newNodes;

  const byWbsCode = new Map<string, Node<NodeData>>();
  const byLabel = new Map<string, Node<NodeData>>();
  const byId = new Map<string, Node<NodeData>>();

  existingNodes.forEach(n => {
    if (n.id) byId.set(n.id, n);
    if (n.data?.wbsCode) byWbsCode.set(n.data.wbsCode.trim().toUpperCase(), n);
    if (n.data?.label) byLabel.set(n.data.label.trim(), n);
  });

  return newNodes.map(newNode => {
    let existingMatch: Node<NodeData> | undefined = undefined;

    if (newNode.id && byId.has(newNode.id)) {
      existingMatch = byId.get(newNode.id);
    } else if (newNode.data?.wbsCode && byWbsCode.has(newNode.data.wbsCode.trim().toUpperCase())) {
      existingMatch = byWbsCode.get(newNode.data.wbsCode.trim().toUpperCase());
    } else if (newNode.data?.label && byLabel.has(newNode.data.label.trim())) {
      existingMatch = byLabel.get(newNode.data.label.trim());
    }

    if (existingMatch) {
      return {
        ...newNode,
        position: {
          x: existingMatch.position.x,
          y: existingMatch.position.y,
        },
        style: existingMatch.style ? { ...newNode.style, ...existingMatch.style } : newNode.style,
        data: {
          ...newNode.data,
          color: existingMatch.data?.color || newNode.data?.color,
          status: existingMatch.data?.status || newNode.data?.status,
          note: existingMatch.data?.note || newNode.data?.note,
          fileUrl: existingMatch.data?.fileUrl || newNode.data?.fileUrl,
        },
      };
    }

    return newNode;
  });
}

export function parseExcelWbsToDisciplineMaps(
  fileBuffer: ArrayBuffer,
  existingNodes?: Node<NodeData>[],
  existingMaps?: DisciplineMapItem[]
): {
  mapTitle: string;
  disciplineMaps: DisciplineMapItem[];
} {
  const workbook = XLSX.read(fileBuffer, { type: 'array' });

  if (!workbook.SheetNames || workbook.SheetNames.length === 0) {
    throw new Error('엑셀 파일에 시트가 존재하지 않습니다.');
  }

  const sheetNames = workbook.SheetNames;
  const disciplineMaps: DisciplineMapItem[] = [];

  const getDisciplineIcon = (name: string) => {
    if (name.includes('신호')) return '📡';
    if (name.includes('통신')) return '📶';
    if (name.includes('전기') || name.includes('전철')) return '⚡';
    if (name.includes('건축') || name.includes('마감')) return '🏛️';
    if (name.includes('토공') || name.includes('굴착') || name.includes('토사') || name.includes('사전토공') || name.includes('토목')) return '🚜';
    if (name.includes('구조물') || name.includes('콘크리트') || name.includes('교량') || name.includes('배수')) return '🏗️';
    if (name.includes('터널') || name.includes('발파') || name.includes('NATM')) return '🚇';
    if (name.includes('궤도') || name.includes('선로') || name.includes('트램') || name.includes('차량')) return '🚃';
    if (name.includes('품질') || name.includes('안전') || name.includes('검사')) return '🛡️';
    if (name.includes('공무') || name.includes('계약') || name.includes('기획')) return '🏢';
    return '📋';
  };

  // 기존 수동 위치 데이터 집합 수집
  const poolExistingNodes: Node<NodeData>[] = [...(existingNodes || [])];
  if (existingMaps) {
    existingMaps.forEach(m => {
      if (m.nodes) poolExistingNodes.push(...m.nodes);
    });
  }

  sheetNames.forEach((sheetName, sIdx) => {
    // 💡 Ignore guide/help/dashboard/statistical sheets (대시보드 시트 무시)
    const sLower = sheetName.toLowerCase().replace(/\s+/g, '');
    if (
      sLower.includes('guide') ||
      sLower.includes('샘플') ||
      sLower.includes('목차') ||
      sLower.includes('대시보드') ||
      sLower.includes('대쉬보드') ||
      sLower.includes('통계') ||
      sLower.includes('dashboard') ||
      sLower.includes('summary')
    ) {
      return;
    }

    const worksheet = workbook.Sheets[sheetName];
    if (!worksheet) return;

    // 1) 헤더 기반 JSON 객체 파싱
    const rawData: any[] = XLSX.utils.sheet_to_json(worksheet, { defval: '' });
    // 2) 컬럼 위치(Column Index Position) 기반 2차원 배열 파싱
    const matrixData: any[][] = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });

    if (!rawData || rawData.length === 0) return;

    const sheetRows: ParsedWbsRow[] = [];

    rawData.forEach((rowObj: any, rIdx: number) => {
      let dept = '';
      let phase = '';
      let title = '';
      let code = '';
      let pred = '';
      let succ = '';
      let purpose = '';
      let method = '';
      let result = '';

      const isPhasePattern = (val: string) => {
        if (!val) return false;
        const v = val.toUpperCase().trim();
        return (
          /^[DP][+-]?\d+/i.test(v) ||
          v.startsWith('D-') ||
          v.startsWith('D+') ||
          v.startsWith('P-') ||
          v.startsWith('P+') ||
          v.startsWith('D0') ||
          v.startsWith('P0') ||
          v.includes('PHASE') ||
          v.includes('D-DAY') ||
          v.includes('PDAY') ||
          /D-\d+/i.test(v) ||
          /P-\d+/i.test(v) ||
          /D\+\d+/i.test(v) ||
          /P\+\d+/i.test(v)
        );
      };

      const matrixRow = matrixData[rIdx + 1] || matrixData[rIdx];
      if (matrixRow && Array.isArray(matrixRow)) {
        if (matrixRow[3] !== undefined && matrixRow[3] !== null && matrixRow[3].toString().trim().length > 0) {
          code = matrixRow[3].toString().trim();
        }

        const val4 = matrixRow[4] !== undefined && matrixRow[4] !== null ? matrixRow[4].toString().trim() : '';
        const val5 = matrixRow[5] !== undefined && matrixRow[5] !== null ? matrixRow[5].toString().trim() : '';
        const val6 = matrixRow[6] !== undefined && matrixRow[6] !== null ? matrixRow[6].toString().trim() : '';
        const val7 = matrixRow[7] !== undefined && matrixRow[7] !== null ? matrixRow[7].toString().trim() : '';
        const val8 = matrixRow[8] !== undefined && matrixRow[8] !== null ? matrixRow[8].toString().trim() : '';
        const val9 = matrixRow[9] !== undefined && matrixRow[9] !== null ? matrixRow[9].toString().trim() : '';
        const val10 = matrixRow[10] !== undefined && matrixRow[10] !== null ? matrixRow[10].toString().trim() : '';
        const val11 = matrixRow[11] !== undefined && matrixRow[11] !== null ? matrixRow[11].toString().trim() : '';

        // 선행 L4 코드 (index 4)
        if (val4 && val4 !== '-') {
          pred = val4;
        }
        // 후행 L4 코드 (index 5)
        if (val5 && val5 !== '-') {
          succ = val5;
        }

        if (isPhasePattern(val6)) {
          phase = val6;
          title = val7 || val6;
        } else if (isPhasePattern(val7)) {
          phase = val7;
          title = val6 || val7;
        } else {
          title = val6 || val7;
          phase = val7;
        }

        if (val8 && !val8.includes('목적') && !val8.includes('분석')) {
          dept = val8;
        }

        if (val9 && val9.length > 1) {
          purpose = val9;
        }

        if (val10 && val10.length > 1) {
          method = val10;
        }

        if (val11 && val11.length > 1) {
          result = val11;
        }
      }

      Object.entries(rowObj).forEach(([key, val]) => {
        const k = key.toString().trim().toLowerCase();
        const v = val ? val.toString().trim() : '';

        if (!v) return;

        if (!code && (k.includes('l4') || k.includes('코드') || k.includes('wbs'))) {
          code = v;
        }
        if (!pred && (k.includes('선행') || k.includes('predecessor'))) {
          pred = v;
        }
        if (!succ && (k.includes('후행') || k.includes('successor'))) {
          succ = v;
        }
        if (!title && (k.includes('액티비티') || k.includes('작업명') || k.includes('명칭') || k.includes('작업단위'))) {
          title = v;
        }
        if (!dept && (k.includes('부서') || k.includes('담당') || k.includes('주관'))) {
          dept = v;
        }
        if (!phase && (k.includes('단계') || k.includes('phase') || k.includes('기한') || k.includes('일정'))) {
          phase = v;
        }
        if (!purpose && (k.includes('목적') || k.includes('개요'))) {
          purpose = v;
        }
        if (!method && (k.includes('방법') || k.includes('절차') || k.includes('지침') || k.includes('수행'))) {
          method = v;
        }
        if (!result && (k.includes('산출물') || k.includes('결과') || k.includes('체크리스트'))) {
          result = v;
        }
      });

      // 액티비티 명과 Phase 기한 스왑 안전 검증 (title에 P-30, D-60 등 일정 패턴이 들어가 있는 경우 자동 스왑!)
      if (isPhasePattern(title) && phase && !isPhasePattern(phase)) {
        const temp = title;
        title = phase;
        phase = temp;
      }

      if (!dept) dept = sheetName;
      if (!title) {
        const values = Object.values(rowObj as Record<string, any>).filter((v: any) => v && v.toString().trim().length > 1);
        if (values.length > 0) {
          const candidate = (values[0] as any).toString().trim();
          if (!isPhasePattern(candidate)) title = candidate;
        }
      }

      if (title && title.length > 1) {
        sheetRows.push({
          wbsCode: code,
          predecessor: pred,
          successor: succ,
          department: dept,
          phase: phase,
          taskTitle: title,
          purpose: purpose,
          method: method,
          result: result,
          sheetName: sheetName,
        });
      }
    });

    if (sheetRows.length > 0) {
      const { nodes, edges } = buildNodesAndEdgesFromRows(sheetRows, `${sheetName} 프로세스 맵`);
      const icon = getDisciplineIcon(sheetName);

      // ✨ 수동으로 이동 조정한 카드 위치 및 서식 100% 보존 머지
      const mergedNodes = mergeExistingNodePositions(nodes, poolExistingNodes);

      disciplineMaps.push({
        id: `disc-sheet-${sIdx + 1}`,
        name: `${icon} ${sheetName}`,
        sheetName: sheetName,
        mapTitle: `${sheetName} 프로세스 맵`,
        nodes: mergedNodes,
        edges: edges,
        itemCount: mergedNodes.filter(n => n.type === 'action').length,
      });
    }
  });

  if (disciplineMaps.length === 0) {
    throw new Error('유효한 WBS 데이터 시트를 찾을 수 없습니다.');
  }

  return {
    mapTitle: disciplineMaps[0].mapTitle,
    disciplineMaps: disciplineMaps,
  };
}
