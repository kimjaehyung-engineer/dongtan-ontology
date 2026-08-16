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

// 6대 표준 Phase 고정 정의 (D-90, D-60, D-30, D-Day, D+10~75, D+75일 이후)
export const STANDARD_PHASES = [
  'PHASE 1: D-90 (사전조사 & 기획)',
  'PHASE 2: D-60 (인허가 & 발주)',
  'PHASE 3: D-30 (계약 & 시공계획)',
  'PHASE 4: D-Day (착공 준비 & 점검)',
  'PHASE 5: D+10~75 (본공사 집행)',
  'PHASE 6: D+75일 이후 (사후관리 & LL/평가)',
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
function classifyDepartment(
  deptRaw?: string,
  taskTitleRaw?: string
): {
  mainCategory: '현장' | '본사';
  subDept: '공무' | '공사' | '품질' | '안전' | '관리' | '본사';
  rowIndex: number;
  color: string;
} {
  const deptText = (deptRaw || '').toLowerCase().replace(/\s+/g, '');
  const titleText = (taskTitleRaw || '').toLowerCase();
  const fullText = deptText + ' ' + titleText;

  // 1. 본사 / 외주 / 스마트엔지니어링 / 견적 / 사업팀 / 외부전문가 / 혁신실 (최우선 판정: 외주구매팀, 외주관리팀 등)
  if (
    deptText.includes('본사') ||
    deptText.includes('외주') ||
    deptText.includes('구매') ||
    deptText.includes('스마트') ||
    deptText.includes('견적') ||
    deptText.includes('컴플라이언스') ||
    deptText.includes('사업팀') ||
    deptText.includes('기술팀') ||
    deptText.includes('설계팀') ||
    deptText.includes('전문가') ||
    deptText.includes('혁신실') ||
    deptText.includes('수행팀') ||
    deptText.includes('사업지원') ||
    deptText.includes('지원팀')
  ) {
    return { mainCategory: '본사', subDept: '본사', rowIndex: 5, color: '#0ea5e9' };
  }

  // 2. 공무 / 계약 / 인허가 / 소장
  if (
    deptText.includes('공무') ||
    deptText.includes('소장') ||
    deptText.includes('계약') ||
    deptText.includes('인허가') ||
    deptText.includes('기획') ||
    deptText.includes('발주') ||
    deptText.includes('화성시') ||
    deptText.includes('발주처') ||
    deptText.includes('감리')
  ) {
    return { mainCategory: '현장', subDept: '공무', rowIndex: 0, color: '#6366f1' };
  }

  // 3. 품질 / 시험 / 검측 / 검수 / 자재
  if (
    deptText.includes('품질') ||
    deptText.includes('시험') ||
    deptText.includes('검측') ||
    deptText.includes('검수') ||
    deptText.includes('자재')
  ) {
    return { mainCategory: '현장', subDept: '품질', rowIndex: 2, color: '#f59e0b' };
  }

  // 4. 안전 / 보건 / 환경
  if (deptText.includes('안전') || deptText.includes('보건') || deptText.includes('환경')) {
    return { mainCategory: '현장', subDept: '안전', rowIndex: 3, color: '#f43f5e' };
  }

  // 5. 관리 / 용지 / 총무 / 보상 / 민원
  if (
    deptText.includes('총무') ||
    deptText.includes('용지') ||
    deptText.includes('회계') ||
    deptText.includes('보상') ||
    deptText.includes('관리팀') ||
    deptText.includes('민원')
  ) {
    return { mainCategory: '현장', subDept: '관리', rowIndex: 4, color: '#8b5cf6' };
  }

  // 6. 공사 / 현장 시공 / 시스템
  if (
    deptText.includes('공사') ||
    deptText.includes('시공') ||
    deptText.includes('토목') ||
    deptText.includes('궤도') ||
    deptText.includes('건축') ||
    deptText.includes('기계') ||
    deptText.includes('전기') ||
    deptText.includes('통신') ||
    deptText.includes('신호') ||
    deptText.includes('소방') ||
    deptText.includes('운영') ||
    deptText.includes('시스템') ||
    deptText.includes('협력업체') ||
    deptText.includes('협력사') ||
    deptText.includes('시공사') ||
    deptText.includes('전문업체') ||
    deptText.includes('업체')
  ) {
    return { mainCategory: '현장', subDept: '공사', rowIndex: 1, color: '#10b981' };
  }

  // 7. 작업명(Title) 키워드로 2차 분류
  if (
    fullText.includes('인허가') ||
    fullText.includes('계약') ||
    fullText.includes('발주') ||
    fullText.includes('신청') ||
    fullText.includes('승인') ||
    fullText.includes('기공승낙')
  ) {
    return { mainCategory: '현장', subDept: '공무', rowIndex: 0, color: '#6366f1' };
  }
  if (fullText.includes('품질') || fullText.includes('시험') || fullText.includes('검측')) {
    return { mainCategory: '현장', subDept: '품질', rowIndex: 2, color: '#f59e0b' };
  }
  if (fullText.includes('안전') || fullText.includes('보건') || fullText.includes('환경') || fullText.includes('위험')) {
    return { mainCategory: '현장', subDept: '안전', rowIndex: 3, color: '#f43f5e' };
  }
  if (fullText.includes('용지') || fullText.includes('보상') || fullText.includes('총무')) {
    return { mainCategory: '현장', subDept: '관리', rowIndex: 4, color: '#8b5cf6' };
  }

  return { mainCategory: '현장', subDept: '공사', rowIndex: 1, color: '#10b981' };
}

// D-Day 숫자 파싱 헬퍼 (예: "D-90 (D-120~D-90)" -> -90, "D+15" -> 15, "D-Day" -> 0)
function parseDdayNumber(phaseStr: string, titleStr: string = ''): number | null {
  if (!phaseStr && !titleStr) return null;
  const s = (String(phaseStr) + ' ' + String(titleStr)).toUpperCase();

  if (
    s.includes('D-DAY') ||
    s.includes('DDAY') ||
    s.includes('D0') ||
    s.includes('D-0') ||
    s.includes('D+0') ||
    s.includes('P+0') ||
    s.includes('P0') ||
    s.includes('P-0') ||
    s.includes('착공')
  ) {
    return 0;
  }

  const matches = s.match(/[DP]\s*([+-]?\d+)/gi);
  if (matches && matches.length > 0) {
    const nums: number[] = [];
    matches.forEach(m => {
      const numMatch = m.match(/([+-]?\d+)/);
      if (numMatch) {
        const parsed = parseInt(numMatch[1], 10);
        if (!isNaN(parsed)) nums.push(parsed);
      }
    });
    if (nums.length > 0) {
      return nums[0];
    }
  }
  return null;
}

// 작업명/Phase 텍스트 및 D-Day 범위 기반으로 5대 Phase 열에 정확히 배치하는 핵심 도우미
function classifyPhaseIndex(phaseRaw: string, taskTitleRaw: string, rIdx: number, totalRows: number): number {
  const dNum = parseDdayNumber(phaseRaw, taskTitleRaw);

  if (dNum !== null) {
    // 1) D+75일 이후 (사후관리 & LL / Phase 6)
    if (dNum > 70) {
      return 5; // PHASE 6
    }
    // 2) D+ (본공사 집행 / Phase 5)
    if (dNum > 0) {
      return 4; // PHASE 5
    }
    // 3) D-Day (착공 준비 / Phase 4)
    if (dNum === 0) {
      return 3; // PHASE 4
    }
    // 4) 음수 D-Day 범위 분류
    // Phase 1 (사전조사 & 기획): D-90 이하 및 장기 선발주(D-240 이하 / D-120 ~ D-75)
    if (dNum <= -240 || (-150 <= dNum && dNum <= -75)) {
      return 0; // PHASE 1
    }
    // Phase 2 (인허가 & 발주): D-60 구간 (-240 < dNum <= -180 또는 -75 < dNum <= -45)
    if ((-240 < dNum && dNum <= -180) || (-75 < dNum && dNum <= -45)) {
      return 1; // PHASE 2
    }
    // Phase 3 (계약 & 시공계획): D-30 구간 (D-44 ~ D-1 또는 기타)
    return 2; // PHASE 3
  }

  // D-Day 숫자가 없을 경우 텍스트 키워드로 2차 분류
  const s = (String(phaseRaw) + ' ' + String(taskTitleRaw)).toLowerCase();
  if (s.includes('75') || s.includes('update') || s.includes('사후') || s.includes('정산') || s.includes('인계') || s.includes('업무평가') || s.includes('ll')) {
    return 5; // PHASE 6
  }
  if (s.includes('사전') || s.includes('기획') || s.includes('현황') || s.includes('측량') || s.includes('gpr') || s.includes('지반조사')) {
    return 0; // PHASE 1
  }
  if (s.includes('인허가') || s.includes('협의') || s.includes('점용') || s.includes('심의') || s.includes('경찰')) {
    return 1; // PHASE 2
  }
  if (s.includes('계약') || s.includes('발주') || s.includes('입찰') || s.includes('견적') || s.includes('선정')) {
    return 2; // PHASE 3
  }
  if (s.includes('동원') || s.includes('big room') || s.includes('교육') || s.includes('착수전')) {
    return 3; // PHASE 4
  }
  if (s.includes('시공') || s.includes('집행') || s.includes('본시공') || s.includes('검수') || s.includes('이설') || s.includes('철거')) {
    return 4; // PHASE 5
  }

  // WBS 순서 비율(0.0~1.0)에 따른 자연스러운 6분할 가로 배치
  if (totalRows <= 1) return 0;
  const ratio = rIdx / Math.max(1, totalRows - 1);
  if (ratio < 0.16) return 0;
  if (ratio < 0.33) return 1;
  if (ratio < 0.50) return 2;
  if (ratio < 0.66) return 3;
  if (ratio < 0.83) return 4;
  return 5;
}

export function buildNodesAndEdgesFromRows(
  rows: ParsedWbsRow[],
  mapTitle: string
): { nodes: Node<NodeData>[]; edges: Edge[] } {
  const nodes: Node<NodeData>[] = [];
  const edges: Edge[] = [];

  const totalRows = rows.length;

  // 1. 사전 분석: 각 행(Row 0..5) 및 Phase(0..5)별 카드 개수 집계
  const cellCountsMap: { [key: string]: number } = {};
  const classifiedItems = rows.map((row, rIdx) => {
    const cls = classifyDepartment(row.department, row.taskTitle);
    const pIdx = classifyPhaseIndex(row.phase, row.taskTitle, rIdx, totalRows);
    const cellKey = `${cls.rowIndex}_${pIdx}`;
    const stackIdx = cellCountsMap[cellKey] || 0;
    cellCountsMap[cellKey] = stackIdx + 1;
    return { row, rIdx, cls, pIdx, stackIndex: stackIdx };
  });

  // 1.1. Phase별 카드 밀도(최대 열 수)에 따라 Phase 열 폭(Column Width)을 신축적으로 동적 계산
  const phaseCols = [2, 2, 2, 2, 2, 2];
  const phaseColWidths = [1480, 1480, 1480, 1480, 1480, 1480];

  for (let p = 0; p < 6; p++) {
    let maxInPhase = 0;
    for (let r = 0; r < 6; r++) {
      const c = cellCountsMap[`${r}_${p}`] || 0;
      if (c > maxInPhase) maxInPhase = c;
    }
    if (maxInPhase > 8) {
      phaseCols[p] = 3;
      phaseColWidths[p] = 2050; // 3열: 60 + 560*2 + 480 + 390px 안전 여백
    } else if (maxInPhase > 1) {
      phaseCols[p] = 2;
      phaseColWidths[p] = 1480; // 2열: 60 + 640 + 480 + 300px 안전 여백
    } else if (maxInPhase === 1) {
      phaseCols[p] = 1;
      phaseColWidths[p] = 950;  // 1열: 60 + 480 + 410px 안전 여백
    } else {
      phaseCols[p] = 1;
      phaseColWidths[p] = 800;  // 빈 Phase
    }
  }

  // Phase별 시작 X 좌표 계산
  const phaseStartOffset = 260;
  const phaseXOffsets: number[] = [];
  let currentX = phaseStartOffset;
  for (let p = 0; p < 6; p++) {
    phaseXOffsets[p] = currentX;
    currentX += phaseColWidths[p];
  }
  const totalCanvasWidth = currentX + 40;

  // 1.2. 각 세로축 행(공무, 공사, 품질, 안전, 관리, 본사)별 실제 카드 수량에 맞게 행 높이를 신축적으로 계산
  const rowHeights = [600, 600, 600, 600, 600, 600];
  for (let r = 0; r < 6; r++) {
    let maxSubRows = 0;
    for (let p = 0; p < 6; p++) {
      const count = cellCountsMap[`${r}_${p}`] || 0;
      const numCols = phaseCols[p];
      const subRows = Math.ceil(count / numCols);
      if (subRows > maxSubRows) maxSubRows = subRows;
    }
    if (maxSubRows === 0) {
      rowHeights[r] = 450; // 카드가 없는 빈 행: 컴팩트 450px
    } else {
      rowHeights[r] = Math.max(680, maxSubRows * 560 + 120); // 서브 행당 560px + 상하 여백 120px
    }
  }

  const rowYOffsets: number[] = [];
  let currentY = 100;
  for (let i = 0; i < 6; i++) {
    rowYOffsets[i] = currentY;
    currentY += rowHeights[i];
  }
  const totalMapHeight = currentY + 300;

  // 1. Master Frame
  nodes.push({
    id: 'map-frame-master',
    type: 'mapFrame',
    position: { x: -40, y: -150 },
    data: { label: `🏢 ${mapTitle}` },
    style: { width: totalCanvasWidth + 100, height: totalMapHeight + 100, zIndex: -10 },
    draggable: false,
    selectable: false,
  });

  // 2. Swimlanes (단일 세로축 헤더 - 동적 높이 및 위치 정렬)
  const swimlaneDefs = [
    { id: 'swimlane-공무', category: '현장', label: '공무 / 계약 / 인허가', rowIndex: 0 },
    { id: 'swimlane-공사', category: '현장', label: '공사 / 현장 시공',    rowIndex: 1 },
    { id: 'swimlane-품질', category: '현장', label: '품질 / 시공 품질',    rowIndex: 2 },
    { id: 'swimlane-안전', category: '현장', label: '안전 / 보건 / 환경',   rowIndex: 3 },
    { id: 'swimlane-관리', category: '현장', label: '관리 / 용지 / 총무',   rowIndex: 4 },
    { id: 'swimlane-본사', category: '본사', label: '본사 / 전략 / 지원',  rowIndex: 5 },
  ];

  swimlaneDefs.forEach(s => {
    const yPos = rowYOffsets[s.rowIndex];
    const h = rowHeights[s.rowIndex];
    nodes.push({
      id: s.id,
      type: 'swimlane',
      position: { x: 0, y: yPos },
      data: {
        label: s.label,
        category: s.category,
        isCategoryFirst: false,
        categorySpanHeight: h,
      },
      style: { width: totalCanvasWidth, height: h, zIndex: -1 },
      draggable: false,
      selectable: true,
    });

    // Row Divider (상단 구분선)
    nodes.push({
      id: `rdiv-${s.rowIndex + 1}`,
      type: 'rowDivider',
      position: { x: 0, y: yPos },
      data: { width: totalCanvasWidth },
      draggable: true,
      selectable: false,
      style: { zIndex: 10 },
    });
  });

  // 마지막 바닥 구분선
  nodes.push({
    id: 'rdiv-bottom',
    type: 'rowDivider',
    position: { x: 0, y: currentY },
    data: { width: totalCanvasWidth },
    draggable: true,
    selectable: false,
    style: { zIndex: 10 },
  });

  // 3. Phase Headers (Vertical Columns - 동적 열 폭 반영)
  STANDARD_PHASES.forEach((phaseName, pIdx) => {
    const xPos = phaseXOffsets[pIdx];
    const w = phaseColWidths[pIdx];

    // Phase 왼쪽 시작 세로 구분선 (첫 번째 Phase만)
    if (pIdx === 0) {
      nodes.push({
        id: `vline-phase-start`,
        type: 'verticalLine',
        position: { x: xPos, y: -35 },
        data: { label: 'Start', height: totalMapHeight - 50 },
        style: { zIndex: 12 },
      });
    }

    // Phase 오른쪽 끝 세로 구분선
    nodes.push({
      id: `vline-phase-right-${pIdx}`,
      type: 'verticalLine',
      position: { x: xPos + w, y: -35 },
      data: { label: `${phaseName} End`, height: totalMapHeight - 50 },
      style: { zIndex: 12 },
    });

    const milestoneWidth = Math.min(560, w - 80);
    const centerX = xPos + (w / 2) - (milestoneWidth / 2);

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

  // 4. Action Cards Placement into 5 Standard Phases & 6 Standard Rows
  const createdCardNodes: { id: string; pIdx: number; title: string; wbsCode?: string }[] = [];

  classifiedItems.forEach(({ row, rIdx, cls, pIdx, stackIndex }) => {
    const numCols = phaseCols[pIdx];
    const colSpacing = numCols === 3 ? 560 : 640;

    const baseX = phaseXOffsets[pIdx] + 60;
    const colInCell = stackIndex % numCols;
    const rowInCell = Math.floor(stackIndex / numCols);

    const cardX = baseX + colInCell * colSpacing;
    const cardY = rowYOffsets[cls.rowIndex] + 50 + rowInCell * 560;

    const cardLabel = row.taskTitle || `액티비티-${rIdx + 1}`;
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

    createdCardNodes.push({ id: cardId, pIdx, title: cardLabel, wbsCode });
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

  // 4.6. 카드 배치 완료 후 캔버스 전체 폭/높이 동적 측정 & 마스터 프레임/스윔레인/구분선 완벽 연결
  let maxCardRightX = currentX;
  let maxCardBottomY = totalMapHeight;
  nodes.forEach(n => {
    if (n.type === 'action') {
      maxCardRightX = Math.max(maxCardRightX, n.position.x + 550);
      maxCardBottomY = Math.max(maxCardBottomY, n.position.y + 600);
    }
  });

  // Phase 6의 끝 경계선(currentX)과 카드 우측 한계에 꼭 맞게 불필요한 빈 열 없이 깔끔하게 마감
  const finalCanvasWidth = Math.max(currentX + 20, maxCardRightX + 40);
  const finalCanvasHeight = Math.max(totalMapHeight, maxCardBottomY + 150);

  // Swimlane-본사의 실제 하단 확장 높이 완벽 동기화
  const headOfficeY = rowYOffsets[5];
  const headOfficeNewHeight = Math.max(rowHeights[5], maxCardBottomY - headOfficeY + 150);

  nodes.forEach(n => {
    if (n.id === 'map-frame-master') {
      n.style = { ...(n.style || {}), width: finalCanvasWidth + 60, height: finalCanvasHeight + 150 };
    } else if (n.id === 'swimlane-본사') {
      n.style = { ...(n.style || {}), width: finalCanvasWidth, height: headOfficeNewHeight };
    } else if (n.type === 'swimlane') {
      n.style = { ...(n.style || {}), width: finalCanvasWidth };
    } else if (n.id === 'rdiv-bottom') {
      n.position = { ...n.position, y: headOfficeY + headOfficeNewHeight };
      n.data = { ...(n.data || {}), width: finalCanvasWidth };
    } else if (n.type === 'rowDivider') {
      n.data = { ...(n.data || {}), width: finalCanvasWidth };
    } else if (n.type === 'verticalLine') {
      n.data = { ...(n.data || {}), height: finalCanvasHeight + 150 };
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

    const rawData: any[] = XLSX.utils.sheet_to_json(worksheet, { defval: '' });
    if (!rawData || rawData.length === 0) return;

    const sheetRows: ParsedWbsRow[] = [];

    const cleanTaskTitle = (rawTitle: string, purpose?: string, _method?: string) => {
      if (!rawTitle) return '';
      let t = String(rawTitle).trim();

      if (t.includes('|')) {
        const parts = t.split('|').map(s => s.trim());
        if (/^(KDS|KCS|지하안전|도로교통|철도안전|도시철도|건산법|산업안전|지방계약|하수도|공공측량)/i.test(parts[0])) {
          t = parts[1] || parts[0];
        } else {
          t = parts[0];
        }
      }

      if (t.includes('\n')) {
        const lines = t.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        t = lines[0].replace(/^[-•*1-9.)\s]+/, '');
      }

      t = t.replace(/\(협업:[^)]*\)/g, '').replace(/협업:[^,]*/g, '').trim();

      if (/^(토목사업팀|포스코스마트엔지니어링팀|현장|공사팀|공무팀|외주관리팀|견적팀|품질팀|안전팀)$/i.test(t)) {
        if (purpose) {
          t = purpose.split('|')[0].split('\n')[0].replace(/^[-•*1-9.)\s]+/, '').trim();
        }
      }

      if (t.length > 38) {
        t = t.slice(0, 36) + '...';
      }
      return t;
    };

    const seenCardKeys = new Set<string>();

    rawData.forEach((rowObj: any, rIdx: number) => {
      let code = String(rowObj['L4 코드'] || rowObj['L4코드'] || rowObj['WBS코드'] || rowObj['코드'] || '').trim();
      if (!code || code === '9000') {
        const matched = Object.entries(rowObj).find(([k, v]) => k.includes('L4') || (String(v).includes('-') && /^\d+-\d+-\d+/.test(String(v))));
        if (matched) code = String(matched[1]).trim();
      }

      const pred = String(rowObj['선행 L4'] || rowObj['선행코드'] || rowObj['선행'] || rowObj['predecessor'] || '').trim();
      const succ = String(rowObj['후행 L4'] || rowObj['후행코드'] || rowObj['후행'] || rowObj['successor'] || '').trim();

      // 1. 액티비티 명칭 (작업단위 Level 4 Task/Activity)
      const rawTaskTitle = String(
        rowObj['작업단위 (Level 4 Task/Activity)'] ||
        rowObj['작업단위'] ||
        rowObj['작업명'] ||
        rowObj['명칭'] ||
        rowObj['Activity'] ||
        rowObj['activity'] ||
        ''
      ).trim();

      // 2. 일정 / D-Day
      const rawPhase = String(
        rowObj['일정 (D-Day)'] ||
        rowObj['일정'] ||
        rowObj['단계'] ||
        rowObj['Phase'] ||
        rowObj['phase'] ||
        ''
      ).trim();

      // 3. 주관 부서
      const rawDept = String(
        rowObj['주관'] ||
        rowObj['주관부서'] ||
        rowObj['담당'] ||
        rowObj['부서'] ||
        sheetName
      ).trim();

      // 4. 목적, 방법, 산출물
      const rawPurpose = String(
        rowObj['목적'] ||
        rowObj['표준서 (Standard) 요약'] ||
        rowObj['표준서'] ||
        ''
      ).trim();

      const rawMethod = String(
        rowObj['방법'] ||
        rowObj['수행지침 (Guideline) 요약'] ||
        rowObj['수행지침'] ||
        ''
      ).trim();

      const rawResult = String(
        rowObj['산출물(결과)'] ||
        rowObj['산출물'] ||
        rowObj['체크리스트 (Checklist) 요약'] ||
        rowObj['체크리스트'] ||
        ''
      ).trim();

      // 빈 행 스킵 (내용이 전무한 유령 행 제외)
      if (!code && !rawTaskTitle && !rawPurpose && !rawMethod && !rawResult) {
        return;
      }

      let finalTitle = cleanTaskTitle(rawTaskTitle, rawPurpose, rawMethod);
      if (!finalTitle || finalTitle === '-') {
        finalTitle = cleanTaskTitle(rawPurpose, rawMethod) || `액티비티-${rIdx + 1}`;
      }

      // 카드 중복 원천 방지 (Zero Duplication)
      const dedupeKey = `${code}__${finalTitle}`.toLowerCase();
      if (seenCardKeys.has(dedupeKey) && code !== '9000' && code !== '') {
        return;
      }
      seenCardKeys.add(dedupeKey);

      sheetRows.push({
        wbsCode: code || `WBS-${rIdx + 1}`,
        predecessor: pred,
        successor: succ,
        department: rawDept,
        phase: rawPhase,
        taskTitle: finalTitle,
        purpose: rawPurpose,
        method: rawMethod,
        result: rawResult,
        sheetName: sheetName,
      });
    });

    if (sheetRows.length > 0) {
      const { nodes, edges } = buildNodesAndEdgesFromRows(sheetRows, `${sheetName} 프로세스 맵`);
      const icon = getDisciplineIcon(sheetName);

      disciplineMaps.push({
        id: `disc-sheet-${sIdx + 1}`,
        name: `${icon} ${sheetName}`,
        sheetName: sheetName,
        mapTitle: `${sheetName} 프로세스 맵`,
        nodes: nodes,
        edges: edges,
        itemCount: nodes.filter(n => n.type === 'action').length,
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
