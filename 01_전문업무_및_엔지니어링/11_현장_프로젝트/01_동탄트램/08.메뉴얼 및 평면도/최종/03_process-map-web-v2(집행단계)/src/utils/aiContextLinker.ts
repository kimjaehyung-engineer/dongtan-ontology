import type { Node, Edge } from 'reactflow';
import { MarkerType } from 'reactflow';
import type { NodeData } from '../store/useStore';

// 표준 사전토공사 30개 액티비티 번호별 최적 정밀 대칭 정렬 좌표 (X, Y)
// 공무 행 1600px (2단), 나머지 1080px. gongmuBottom = 1580
const PRESET_CARD_POSITIONS: Record<number, { x: number; y: number; color?: string }> = {
  // Row 1: [현장] 🏢 공무 ── 상단 서브행 (Y = 200, D-90 ~ D-30 초기)
  2:  { x: 480,  y: 200, color: '#6366f1' }, // 발주전략 KOM
  6:  { x: 1380, y: 200, color: '#6366f1' }, // 자재발주 요청
  7:  { x: 2420, y: 200, color: '#6366f1' }, // 용지 사용 Risk
  9:  { x: 2940, y: 200, color: '#6366f1' }, // 인허가 절차 진행

  // Row 1: [현장] 🏢 공무 ── 하단 서브행 (Y = 900, D-30 후반 ~ D-Day)
  10: { x: 2940, y: 900, color: '#818cf8' }, // 교통대책 승인
  12: { x: 3460, y: 900, color: '#818cf8' }, // 기공승낙 적정성
  18: { x: 4480, y: 900, color: '#818cf8' }, // 설계변경 착수전
  19: { x: 5180, y: 900, color: '#818cf8' }, // 설계변경 지원

  // Row 2: [현장] 🏗️ 공사 (Center Y = 2120)
  1:  { x: 480,  y: 2120, color: '#10b981' }, // Site Survey
  5:  { x: 1380, y: 2120, color: '#10b981' }, // 교통처리계획
  8:  { x: 2420, y: 2120, color: '#10b981' }, // 착수전 Big Room
  11: { x: 2940, y: 2120, color: '#10b981' }, // 지장물 검토
  16: { x: 3460, y: 2120, color: '#10b981' }, // 시공계획 수립
  20: { x: 4480, y: 2120, color: '#10b981' }, // 교통안전시설 설치
  22: { x: 5180, y: 2120, color: '#059669' }, // 벌목/벌근제거
  23: { x: 5700, y: 2120, color: '#059669' }, // 기존구조물/지장물 철거
  24: { x: 6220, y: 2120, color: '#059669' }, // 진입로 조성
  25: { x: 6740, y: 2120, color: '#059669' }, // 배수/환경시설
  26: { x: 7260, y: 2120, color: '#047857' }, // 토공 굴착
  28: { x: 7780, y: 2120, color: '#047857' }, // 쌓기 및 다짐
  30: { x: 8300, y: 2120, color: '#047857' }, // 강화노반 인계인수

  // Row 3: [현장] 🛡️ 품질 (Center Y = 3200)
  15: { x: 2940, y: 3200, color: '#f59e0b' }, // 시공계획서 검토
  17: { x: 3460, y: 3200, color: '#f59e0b' }, // 설계변경 검토
  27: { x: 7260, y: 3200, color: '#d97706' }, // 노상토 지지력

  // Row 4: [현장] 🚨 안전 (Center Y = 4280)
  3:  { x: 1380, y: 4280, color: '#f43f5e' }, // Site Survey Risk
  4:  { x: 1900, y: 4280, color: '#f43f5e' }, // 최고의 팀 만들기
  13: { x: 2420, y: 4280, color: '#e11d48' }, // 민원 저감 대책
  21: { x: 4480, y: 4280, color: '#e11d48' }, // 장비 검수 지원
  29: { x: 7260, y: 4280, color: '#be123c' }, // 현장지원

  // Row 5: [현장] 💼 관리 (Center Y = 5360)
  14: { x: 3460, y: 5360, color: '#8b5cf6' }, // 용지보상 Risk
};

/**
 * 액티비티 카드들의 가로축(D-Day 일정 Phase) 및 세로축(부서 Swimlane) 정밀 격자 균등/대칭 정렬
 * 1. 상단 Phase 헤더 상자 및 구분선과 겹침 0% 완벽 차단
 * 2. 1개 구획 내 카드가 2개일 경우 열 중심(Center) 기준으로 좌우 완벽 대칭 배치
 */
export function autoAlignActionNodes(nodes: Node<NodeData>[]): Node<NodeData>[] {
  const cellGroups: { [cellKey: string]: Node<NodeData>[] } = {};

  nodes.forEach(node => {
    if (node.type !== 'action') return;
    const dept = (node.data?.swimlane || node.data?.department || '').toLowerCase();
    let yBase = 2120;

    if (dept.includes('공무') || dept.includes('인허가') || dept.includes('계약')) yBase = 200;
    else if (dept.includes('공사') || dept.includes('시공')) yBase = 2120;
    else if (dept.includes('품질')) yBase = 3200;
    else if (dept.includes('안전') || dept.includes('보건') || dept.includes('환경')) yBase = 4280;
    else if (dept.includes('관리') || dept.includes('용지') || dept.includes('총무')) yBase = 5360;
    else if (dept.includes('본사') || dept.includes('전략')) yBase = 6440;

    let colCenter = 3375; // Phase 3 기본
    if (node.position.x < 1200) colCenter = 775;
    else if (node.position.x < 2350) colCenter = 1775;
    else if (node.position.x < 4400) colCenter = 3375;
    else if (node.position.x < 5100) colCenter = 4750;
    else colCenter = 6150;

    const cellKey = `${yBase}_${colCenter}`;
    if (!cellGroups[cellKey]) cellGroups[cellKey] = [];
    cellGroups[cellKey].push(node);
  });

  return nodes.map(node => {
    if (node.type !== 'action') return node;

    const num = (node.data as any)?.num || parseInt(node.id.replace(/[^0-9]/g, ''), 10);

    // 1. 사전토공사 표준 프리셋 좌표가 있으면 100% 미세 정밀 대칭 좌표 적용
    if (num && PRESET_CARD_POSITIONS[num]) {
      const preset = PRESET_CARD_POSITIONS[num];
      return {
        ...node,
        position: { x: preset.x, y: preset.y },
      };
    }

    // 2. 일반 동적 카드의 경우: 2개일 때 열 중심 기준 양쪽 대칭 배치
    const dept = (node.data?.swimlane || node.data?.department || '').toLowerCase();
    let yBase = 2120;
    if (dept.includes('공무') || dept.includes('인허가') || dept.includes('계약')) yBase = 200;
    else if (dept.includes('공사') || dept.includes('시공')) yBase = 2120;
    else if (dept.includes('품질')) yBase = 3200;
    else if (dept.includes('안전') || dept.includes('보건') || dept.includes('환경')) yBase = 4280;
    else if (dept.includes('관리') || dept.includes('용지') || dept.includes('총무')) yBase = 5360;
    else if (dept.includes('본사') || dept.includes('전략')) yBase = 6440;

    let colCenter = 3375;
    if (node.position.x < 1200) colCenter = 775;
    else if (node.position.x < 2350) colCenter = 1775;
    else if (node.position.x < 4400) colCenter = 3375;
    else if (node.position.x < 5100) colCenter = 4750;
    else colCenter = 6150;

    const cellKey = `${yBase}_${colCenter}`;
    const group = cellGroups[cellKey] || [];
    const indexInGroup = group.findIndex(g => g.id === node.id);

    let finalX = node.position.x;
    let finalY = yBase;

    if (group.length === 1) {
      finalX = colCenter;
    } else if (group.length === 2) {
      finalX = indexInGroup === 0 ? colCenter - 260 : colCenter + 260;
    } else {
      finalX = colCenter + (indexInGroup - (group.length - 1) / 2) * 500;
    }

    return {
      ...node,
      position: { x: finalX, y: finalY },
    };
  });
}

/**
 * AI 맥락 기반 자동 화살표 연결 엔진 (AI Context Edge Linker)
 * 캔버스에 있는 액티비티 카드들의 제목, 목적, 방법, 일정(X축), 부서(Y축) 맥락을 종합 분석하여
 * 공정 순서(선행 ➔ 후행)에 맞는 최적의 연결선(화살표)을 자동으로 맺어줍니다.
 */
export function generateAiContextEdges(nodes: Node<NodeData>[]): Edge[] {
  const actionNodes = nodes.filter(n => n.type === 'action');
  if (actionNodes.length < 2) return [];

  const edges: Edge[] = [];
  const addedSet = new Set<string>();

  // 1. 노드 위치 맵 구축
  const nodePosMap: { [id: string]: { x: number; y: number } } = {};
  actionNodes.forEach(n => {
    nodePosMap[n.id] = { x: n.position.x, y: n.position.y };
  });

  // 2. 두 노드 간 최단거리 핸들 쌍 계산 (상하/좌우 최적 꺾임)
  const getShortestHandlePair = (sId: string, tId: string) => {
    const sPos = nodePosMap[sId] || { x: 0, y: 0 };
    const tPos = nodePosMap[tId] || { x: 0, y: 0 };
    const dx = tPos.x - sPos.x;
    const dy = tPos.y - sPos.y;

    if (Math.abs(dx) < 400 && Math.abs(dy) > 100) {
      return dy > 0
        ? { sourceHandle: 'bottom', targetHandle: 'top-target' }
        : { sourceHandle: 'top', targetHandle: 'bottom-target' };
    }
    return dx >= 0
      ? { sourceHandle: 'right', targetHandle: 'left-target' }
      : { sourceHandle: 'left', targetHandle: 'right-target' };
  };

  const addEdge = (sourceId: string, targetId: string, label?: string, isCp?: boolean) => {
    if (sourceId === targetId) return;
    const edgeId = `edge-ai-${sourceId}-${targetId}`;
    if (addedSet.has(edgeId)) return;
    addedSet.add(edgeId);

    const { sourceHandle, targetHandle } = getShortestHandlePair(sourceId, targetId);
    const strokeColor = isCp ? '#b91c1c' : '#0f172a';
    const strokeWidth = isCp ? 6.5 : 6;
    const arrowSize = 20;

    edges.push({
      id: edgeId,
      source: sourceId,
      target: targetId,
      sourceHandle,
      targetHandle,
      type: 'smoothstep',
      animated: isCp ?? false,
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
  };

  // 3. 번호(num) 또는 ID 기반 선후행 맵 확인
  const numToNodeMap: { [num: number]: Node<NodeData> } = {};
  actionNodes.forEach(n => {
    const num = (n.data as any)?.num || parseInt(n.id.replace(/[^0-9]/g, ''), 10);
    if (num && !isNaN(num)) {
      numToNodeMap[num] = n;
    }
  });

  // 표준 사전토공사 30개 기본 선후행 맵
  const defaultFlows: [number, number, string?][] = [
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

  let defaultMatchCount = 0;
  defaultFlows.forEach(([srcNum, tgtNum, label]) => {
    if (numToNodeMap[srcNum] && numToNodeMap[tgtNum]) {
      defaultMatchCount++;
      const isCp = [
        [1, 2], [2, 6], [1, 5], [5, 10], [7, 9], [9, 12], [8, 11],
        [11, 16], [16, 20], [20, 22], [22, 24], [24, 26], [26, 28], [28, 30]
      ].some(([s, t]) => s === srcNum && t === tgtNum);

      addEdge(numToNodeMap[srcNum].id, numToNodeMap[tgtNum].id, label, isCp);
    }
  });

  // 기본 맵 규칙으로 연결되었으면 반환
  if (defaultMatchCount >= 5) {
    return edges;
  }

  // 4. 일반 임의 카드들의 경우: X축 시간순 + 공정 키워드 텍스트 맥락 추론 연결
  const sortedNodes = [...actionNodes].sort((a, b) => a.position.x - b.position.x || a.position.y - b.position.y);

  for (let i = 0; i < sortedNodes.length - 1; i++) {
    const srcNode = sortedNodes[i];
    const srcText = `${srcNode.data?.label || ''} ${srcNode.data?.purpose || ''} ${srcNode.data?.method || ''}`.toLowerCase();

    // 가장 인접한 후행 노드 탐색
    let bestTarget = sortedNodes[i + 1];

    for (let j = i + 1; j < Math.min(i + 4, sortedNodes.length); j++) {
      const tgtCandidate = sortedNodes[j];
      const tgtText = `${tgtCandidate.data?.label || ''} ${tgtCandidate.data?.purpose || ''} ${tgtCandidate.data?.method || ''}`.toLowerCase();

      // 키워드 관련성 체크 (조사 ➔ 승인/계획, 계획 ➔ 시공/설치, 시공 ➔ 검사/인계)
      if (
        (srcText.includes('조사') && (tgtText.includes('계획') || tgtText.includes('승인') || tgtText.includes('인허가'))) ||
        (srcText.includes('계획') && (tgtText.includes('설치') || tgtText.includes('시공') || tgtText.includes('발주'))) ||
        (srcText.includes('설치') && (tgtText.includes('굴착') || tgtText.includes('철거') || tgtText.includes('검수'))) ||
        (srcText.includes('굴착') && (tgtText.includes('성토') || tgtText.includes('다짐') || tgtText.includes('시험'))) ||
        (srcText.includes('다짐') && (tgtText.includes('시험') || tgtText.includes('인계') || tgtText.includes('완공')))
      ) {
        bestTarget = tgtCandidate;
        break;
      }
    }

    addEdge(srcNode.id, bestTarget.id, '', false);
  }

  return edges;
}
