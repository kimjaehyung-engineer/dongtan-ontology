import type { Node, Edge } from 'reactflow';
import { MarkerType } from 'reactflow';
import type { NodeData } from '../store/useStore';
import preEarthworkData from '../data/preEarthworkActivities.json';

export function generatePreEarthworkNodesAndEdges(): { nodes: Node<NodeData>[]; edges: Edge[] } {
  const nodes: Node<NodeData>[] = [];
  const edges: Edge[] = [];

  const totalCanvasWidth = 8800;
  const gongmuRowHeight = 1600;   // 공무 행: 카드 8개 → 2단 배치 (상단 4개, 하단 4개)
  const stdRowHeight = 1080;      // 나머지 행: 표준 높이
  const gongmuTop = -20;
  const gongmuBottom = gongmuTop + gongmuRowHeight; // 1580

  // 0. Master Outer Boundary Frame Container
  nodes.push({
    id: 'map-frame-master',
    type: 'mapFrame',
    position: { x: -40, y: -150 },
    data: { label: '🏢 동탄도시철도(트램) 건설공사 · 사전토공사 프로세스 맵' },
    style: { width: totalCanvasWidth + 80, height: 7220, zIndex: -10 },
    draggable: false,
    selectable: false,
  });

  // 2. Swimlanes - 공무행만 1600px, 나머지 1080px
  const swimlanes = [
    { id: 'swimlane-공무', category: '현장', label: '🏢 공무 / 계약 / 인허가', y: gongmuTop,         height: gongmuRowHeight, isCategoryFirst: true,  categorySpanHeight: gongmuRowHeight + stdRowHeight * 4 },
    { id: 'swimlane-공사', category: '현장', label: '🏗️ 공사 / 현장 시공',    y: gongmuBottom,       height: stdRowHeight,    isCategoryFirst: false, categorySpanHeight: gongmuRowHeight + stdRowHeight * 4 },
    { id: 'swimlane-품질', category: '현장', label: '🛡️ 품질 / 시공 품질',    y: gongmuBottom + 1080, height: stdRowHeight,   isCategoryFirst: false, categorySpanHeight: gongmuRowHeight + stdRowHeight * 4 },
    { id: 'swimlane-안전', category: '현장', label: '🚨 안전 / 보건 / 환경',   y: gongmuBottom + 2160, height: stdRowHeight,   isCategoryFirst: false, categorySpanHeight: gongmuRowHeight + stdRowHeight * 4 },
    { id: 'swimlane-관리', category: '현장', label: '💼 관리 / 용지 / 총무',   y: gongmuBottom + 3240, height: stdRowHeight,   isCategoryFirst: false, categorySpanHeight: gongmuRowHeight + stdRowHeight * 4 },
    { id: 'swimlane-본사', category: '본사', label: '🏛️ 본사 / 전략 / 지원',  y: gongmuBottom + 4320, height: stdRowHeight,   isCategoryFirst: true,  categorySpanHeight: stdRowHeight },
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

  // Horizontal Row Dividers
  swimlanes.forEach((s, i) => {
    nodes.push({ id: `rdiv-${i + 1}`, type: 'rowDivider', position: { x: 0, y: s.y }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } });
  });
  // 마지막 하단 구분선
  const lastSwimlane = swimlanes[swimlanes.length - 1];
  nodes.push({ id: 'rdiv-bottom', type: 'rowDivider', position: { x: 0, y: lastSwimlane.y + (lastSwimlane.height || stdRowHeight) }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } });

  // 3. Phase Vertical Guideline Lines & Headers
  const totalHeight = (lastSwimlane.y + (lastSwimlane.height || stdRowHeight)) - gongmuTop + 100;
  const phases = [
    { id: 'phase-d90',  x: 350,  title: '📅 PHASE 1: D-90 (사전조사 & 기획)' },
    { id: 'phase-d60',  x: 1200, title: '📋 PHASE 2: D-60 (인허가 & 발주)' },
    { id: 'phase-d30',  x: 2350, title: '🔍 PHASE 3: D-30 (계약 & 시공계획)' },
    { id: 'phase-dday', x: 4400, title: '🚀 PHASE 4: D-Day (착공 준비 & 점검)' },
    { id: 'phase-exec', x: 5100, title: '⚡ PHASE 5: D+10~75 (본공사 집행)' },
  ];

  phases.forEach((p, idx) => {
    nodes.push({
      id: `vline-${p.id}`,
      type: 'verticalLine',
      position: { x: p.x, y: -70 },
      data: { label: p.title.split(':')[1]?.trim() || '', height: totalHeight },
      style: { zIndex: 5 },
    });

    nodes.push({
      id: `header-${p.id}`,
      type: 'milestone',
      position: { x: p.x + 10, y: -56 },
      data: {
        label: p.title,
        date: `Phase ${idx + 1}`,
        status: 'normal',
      },
    });
  });

  // ─── 4. 카드 배치 좌표 ─────────────────────────────────────────────────
  // 공무 행 (1600px): 상단 서브행 Y = 200, 하단 서브행 Y = 900
  const gongmuRow1Y = 200;   // 상단: 발주·자재·용지·인허가 (D-90~D-30 초기)
  const gongmuRow2Y = 900;   // 하단: 교통대책·기공승낙·설계변경 (D-30~D-Day)
  // 공사 행: Center Y = gongmuBottom + 540 = 2120
  const gongsaY = gongmuBottom + 540;
  // 품질 행: Center Y
  const pumjilY = gongmuBottom + 1080 + 540;
  // 안전 행: Center Y
  const anjeonY = gongmuBottom + 2160 + 540;
  // 관리 행: Center Y
  const gwanriY = gongmuBottom + 3240 + 540;

  const cardPositions: Record<number, { x: number; y: number; color?: string }> = {
    // --- Row 1: [현장] 🏢 공무 ── 상단 서브행 (D-90 ~ D-30 초기) ---
    2:  { x: 480,  y: gongmuRow1Y, color: '#6366f1' }, // 발주전략 KOM        (Phase 1: D-90)
    6:  { x: 1380, y: gongmuRow1Y, color: '#6366f1' }, // 자재발주 요청        (Phase 2: D-60)
    7:  { x: 2420, y: gongmuRow1Y, color: '#6366f1' }, // 용지 사용 Risk       (Phase 3: D-30)
    9:  { x: 2940, y: gongmuRow1Y, color: '#6366f1' }, // 인허가 절차 진행     (Phase 3: D-30)

    // --- Row 1: [현장] 🏢 공무 ── 하단 서브행 (D-30 후반 ~ D-Day) ---
    10: { x: 2940, y: gongmuRow2Y, color: '#818cf8' }, // 교통대책 승인        (Phase 3: D-30)
    12: { x: 3460, y: gongmuRow2Y, color: '#818cf8' }, // 기공승낙 적정성      (Phase 3: D-30)
    18: { x: 4480, y: gongmuRow2Y, color: '#818cf8' }, // 설계변경 착수전      (Phase 4: D-Day)
    19: { x: 5180, y: gongmuRow2Y, color: '#818cf8' }, // 설계변경 지원        (Phase 5: D+)

    // --- Row 2: [현장] 🏗️ 공사 (1개 단일 행) ---
    1:  { x: 480,  y: gongsaY, color: '#10b981' }, // Site Survey
    5:  { x: 1380, y: gongsaY, color: '#10b981' }, // 교통처리계획
    8:  { x: 2420, y: gongsaY, color: '#10b981' }, // 착수전 Big Room
    11: { x: 2940, y: gongsaY, color: '#10b981' }, // 지장물 검토
    16: { x: 3460, y: gongsaY, color: '#10b981' }, // 시공계획 수립
    20: { x: 4480, y: gongsaY, color: '#10b981' }, // 교통안전시설 설치
    22: { x: 5180, y: gongsaY, color: '#059669' }, // 벌목/벌근제거
    23: { x: 5700, y: gongsaY, color: '#059669' }, // 기존구조물/지장물 철거
    24: { x: 6220, y: gongsaY, color: '#059669' }, // 진입로 조성
    25: { x: 6740, y: gongsaY, color: '#059669' }, // 배수/환경시설
    26: { x: 7260, y: gongsaY, color: '#047857' }, // 토공 굴착
    28: { x: 7780, y: gongsaY, color: '#047857' }, // 쌓기 및 다짐
    30: { x: 8300, y: gongsaY, color: '#047857' }, // 강화노반 인계인수

    // --- Row 3: [현장] 🛡️ 품질 ---
    15: { x: 2940, y: pumjilY, color: '#f59e0b' }, // 시공계획서 검토
    17: { x: 3460, y: pumjilY, color: '#f59e0b' }, // 설계변경 검토
    27: { x: 7260, y: pumjilY, color: '#d97706' }, // 노상토 지지력

    // --- Row 4: [현장] 🚨 안전 ---
    3:  { x: 1380, y: anjeonY, color: '#f43f5e' }, // Site Survey Risk
    4:  { x: 1900, y: anjeonY, color: '#f43f5e' }, // 최고의 팀 만들기
    13: { x: 2420, y: anjeonY, color: '#e11d48' }, // 민원 저감 대책
    21: { x: 4480, y: anjeonY, color: '#e11d48' }, // 장비 검수 지원
    29: { x: 7260, y: anjeonY, color: '#be123c' }, // 현장지원

    // --- Row 5: [현장] 💼 관리 ---
    14: { x: 3460, y: gwanriY, color: '#8b5cf6' }, // 용지보상 Risk
  };

  preEarthworkData.forEach((act) => {
    const pos = cardPositions[act.num] || { x: 200 + act.num * 400, y: 1115, color: '#3b82f6' };
    const nodeId = `node-act-${act.num}`;
    const isPrep = act.num <= 21;

    const isCpNode = [1, 2, 6, 7, 9, 10, 11, 16, 20, 22, 24, 26, 28, 30].includes(act.num);

    let mainCat = '현장';
    let subDept = '공사';

    if ([2, 6, 7, 9, 10, 12, 18, 19].includes(act.num)) {
      mainCat = '현장';
      subDept = '공무';
    } else if ([15, 17, 27].includes(act.num)) {
      mainCat = '현장';
      subDept = '품질';
    } else if ([3, 4, 13, 21, 29].includes(act.num)) {
      mainCat = '현장';
      subDept = '안전';
    } else if ([14].includes(act.num)) {
      mainCat = '현장';
      subDept = '관리';
    } else if (act.department?.includes('본사')) {
      mainCat = '본사';
      subDept = '본사';
    }

    nodes.push({
      id: nodeId,
      type: 'action',
      position: { x: pos.x, y: pos.y },
      data: {
        label: `[#${act.num}] ${act.title}`,
        category: mainCat,
        department: `${mainCat} · ${subDept}`,
        cooperation: act.support || '',
        purpose: act.purpose,
        method: act.method,
        result: act.output,
        status: isPrep ? 'normal' : 'done',
        color: pos.color || '#3b82f6',
        note: `공종코드: ${act.code} | 일정: ${act.schedule}`,
        swimlane: subDept,
        isCritical: isCpNode,
      },
      style: { width: 480, height: 500 },
    });
  });

  // 5. Logical Dependency Process Flow Connections (사전토공사 전체 선행/후행 화살표 연결)
  const dependencyFlows: [number, number, string?][] = [
    [1, 2, '현장조사 ➔ 발주전략'],
    [1, 3, '현장조사 ➔ Risk검토'],
    [3, 4, 'Risk검토 ➔ 팀구성'],
    [1, 5, '현장조사 ➔ 교통계획'],
    [5, 10, '교통계획 ➔ 경찰서승인'],
    [2, 6, '발주전략 ➔ 자재선발주'],
    [2, 7, '발주전략 ➔ 용지Risk'],
    [7, 8, '용지Risk ➔ Big Room'],
    [7, 9, '용지Risk ➔ 인허가접수'],
    [9, 12, '인허가 ➔ 기공승낙'],
    [7, 14, '용지Risk ➔ 용지보상'],
    [8, 11, 'Big Room ➔ 지장물조사'],
    [11, 16, '지장물조사 ➔ 시공계획수립'],
    [16, 15, '시공계획 ➔ 품질검토'],
    [16, 17, '시공계획 ➔ 설계변경검토'],
    [17, 18, '설계변경검토 ➔ 서류작성'],
    [18, 19, '서류작성 ➔ 발주처승인'],
    [4, 13, '팀구성 ➔ 민원저감'],
    [16, 20, '시공계획 ➔ 교통안전설치'],
    [20, 21, '교통안전 ➔ 장비검수'],
    [20, 22, '교통안전 ➔ 벌목/벌근'],
    [22, 23, '벌목 ➔ 구조물철거'],
    [22, 24, '벌목 ➔ 진입로조성'],
    [24, 25, '진입로 ➔ 배수/환경'],
    [24, 26, '진입로 ➔ 토공굴착'],
    [26, 28, '굴착 ➔ 다짐/성토'],
    [28, 27, '다짐 ➔ 노상토지질시험'],
    [27, 29, '품질시험 ➔ 현장안전점검'],
    [28, 30, '다짐 ➔ 강화노반인계'],
    [29, 30, '안전점검 ➔ 최종인계인수'],
  ];

  dependencyFlows.forEach(([src, tgt, label]) => {
    const srcPos = cardPositions[src];
    const tgtPos = cardPositions[tgt];

    let sourceHandle = 'right-source';
    let targetHandle = 'left-target';

    if (srcPos && tgtPos) {
      if (tgtPos.y < srcPos.y - 100) {
        // Target is in a higher swimlane row
        sourceHandle = 'top-source';
        targetHandle = 'bottom-target';
      } else if (tgtPos.y > srcPos.y + 100) {
        // Target is in a lower swimlane row
        sourceHandle = 'bottom-source';
        targetHandle = 'top-target';
      } else {
        // Target is in the same swimlane row
        sourceHandle = 'right-source';
        targetHandle = 'left-target';
      }
    }

    const isCp = [
      [1, 2], [2, 6], [1, 5], [5, 10], [7, 9], [9, 12], [8, 11],
      [11, 16], [16, 20], [20, 22], [22, 24], [24, 26], [26, 28], [28, 30]
    ].some(([s, t]) => s === src && t === tgt);

    const strokeColor = isCp ? '#b91c1c' : '#0f172a';
    const strokeWidth = isCp ? 6.5 : 6;
    const arrowSize = 20;

    edges.push({
      id: `edge-${src}-${tgt}`,
      source: `node-act-${src}`,
      target: `node-act-${tgt}`,
      sourceHandle,
      targetHandle,
      type: 'smoothstep',
      animated: isCp,
      label: label || '',
      style: {
        stroke: strokeColor,
        strokeWidth: strokeWidth,
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: strokeColor,
        width: arrowSize,
        height: arrowSize,
      },
    });
  });

  return { nodes, edges };
}
