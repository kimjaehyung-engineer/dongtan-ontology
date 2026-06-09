import { MarkerType } from 'reactflow';
import type { Node, Edge } from 'reactflow';
import type { NodeData } from './useStore';

export const initialNodes: Node<NodeData>[] = [
  // --- Swimlanes (Background) ---
  {
    id: 'swimlane-공무',
    type: 'swimlane',
    position: { x: 0, y: 150 },
    data: { label: '공무' },
    style: { width: 2500, height: 400, zIndex: -1 },
    draggable: false,
    selectable: false,
  },
  {
    id: 'swimlane-공사',
    type: 'swimlane',
    position: { x: 0, y: 550 },
    data: { label: '공사' },
    style: { width: 2500, height: 400, zIndex: -1 },
    draggable: false,
    selectable: false,
  },
  {
    id: 'swimlane-품질',
    type: 'swimlane',
    position: { x: 0, y: 950 },
    data: { label: '품질' },
    style: { width: 2500, height: 300, zIndex: -1 },
    draggable: false,
    selectable: false,
  },
  {
    id: 'swimlane-안전',
    type: 'swimlane',
    position: { x: 0, y: 1250 },
    data: { label: '안전' },
    style: { width: 2500, height: 300, zIndex: -1 },
    draggable: false,
    selectable: false,
  },
  {
    id: 'swimlane-관리',
    type: 'swimlane',
    position: { x: 0, y: 1550 },
    data: { label: '관리' },
    style: { width: 2500, height: 300, zIndex: -1 },
    draggable: false,
    selectable: false,
  },
  {
    id: 'swimlane-본사',
    type: 'swimlane',
    position: { x: 0, y: 1850 },
    data: { label: '본사' },
    style: { width: 2500, height: 300, zIndex: -1 },
    draggable: false,
    selectable: false,
  },
  {
    id: 'swimlane-인허가',
    type: 'swimlane',
    position: { x: 0, y: 2150 },
    data: { label: '인허가' },
    style: { width: 2500, height: 300, zIndex: -1 },
    draggable: false,
    selectable: false,
  },

  // --- Row Dividers (draggable horizontal lines, same mechanism as vertical milestone lines) ---
  { id: 'rdiv-1', type: 'rowDivider', position: { x: 0, y: 550 }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } },
  { id: 'rdiv-2', type: 'rowDivider', position: { x: 0, y: 950 }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } },
  { id: 'rdiv-3', type: 'rowDivider', position: { x: 0, y: 1250 }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } },
  { id: 'rdiv-4', type: 'rowDivider', position: { x: 0, y: 1550 }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } },
  { id: 'rdiv-5', type: 'rowDivider', position: { x: 0, y: 1850 }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } },
  { id: 'rdiv-6', type: 'rowDivider', position: { x: 0, y: 2150 }, data: {}, draggable: true, selectable: false, style: { zIndex: 10 } },

  // --- Vertical Lines (under milestones, only in the swimlane areas) ---
  { id: 'vline-1', type: 'verticalLine', position: { x: 500, y: 150 }, data: { height: 2300 }, draggable: true, style: { zIndex: 10 } },
  { id: 'vline-2', type: 'verticalLine', position: { x: 900, y: 150 }, data: { height: 2300 }, draggable: true, style: { zIndex: 10 } },
  { id: 'vline-3', type: 'verticalLine', position: { x: 1400, y: 150 }, data: { height: 2300 }, draggable: true, style: { zIndex: 10 } },
  { id: 'vline-4', type: 'verticalLine', position: { x: 1900, y: 150 }, data: { height: 2300 }, draggable: true, style: { zIndex: 10 } },

  // --- Milestones (Top) ---
  {
    id: 'm-d210',
    type: 'milestone',
    position: { x: 400, y: 50 },
    data: { label: 'D-210 철도 통신공사 발주' },
  },
  {
    id: 'm-d180',
    type: 'milestone',
    position: { x: 800, y: 50 },
    data: { label: 'D-180 철도 통신공사 계약' },
  },
  {
    id: 'm-d90',
    type: 'milestone',
    position: { x: 1300, y: 50 },
    data: { label: 'D-90 착수 전 Big Room 회의' },
  },
  {
    id: 'm-d60',
    type: 'milestone',
    position: { x: 1800, y: 50 },
    data: { label: 'D-60 시공계획 수립 / 승인' },
  },

  // --- Actions ---
  {
    id: 'a1',
    type: 'action',
    position: { x: 200, y: 200 },
    data: {
      label: '설계적정성 검토',
      department: '현장 공무팀',
      purpose: '설계적정성 및 시공성 검토',
      method: '- 입찰 요구사항에 대한 설계 반영여부 검토\n- 설계도서 및 물량산출 상세 검토\n- 타 시스템과의 인터페이스 가능 여부 확인',
      result: '회의록, 설계검토 보고서',
      color: '#fca5a5' // red-300
    },
  },
  {
    id: 'a2',
    type: 'action',
    position: { x: 200, y: 600 },
    data: {
      label: '발주전략 KOM',
      department: '현장 소장',
      purpose: '통신설비 공사 발주 전략수립',
      method: '- 통신설비 설계 및 현장여건 검토\n- 통신설비 공사 시공실적 업체 Pool 검토',
      result: 'KOM 검토결과서, 현장설명서',
      color: '#fca5a5'
    },
  },
  {
    id: 'a3',
    type: 'action',
    position: { x: 800, y: 200 },
    data: {
      label: '통신설비 제작사 인터페이스 협의',
      department: '현장 시스템팀',
      purpose: '통신설비 제작 연동방안 검토',
      method: '- 내부 인터페이스 및 인허가사항 확인',
      result: '인터페이스 회의록 및 관리대장',
      color: '#d1d5db' // gray-300
    },
  },
  {
    id: 'a4',
    type: 'action',
    position: { x: 1300, y: 600 },
    data: {
      label: '착수 전 Big Room 회의',
      department: '현장소장',
      purpose: '착공 시 선행공정 간섭사항 및 각종 Risk에 대한 대책 수립',
      method: '- 공정별 간섭사항 검토 (노반/궤도/전기/신호/PSD/차량)\n- 당사/타사 장비 반입계획/상호운영 연계 검토',
      result: 'Big Room 회의록(참석자 전원 서명)',
      color: '#fca5a5'
    },
  },
];

export const initialEdges: Edge[] = [
  { id: 'e-m210-m180', source: 'm-d210', target: 'm-d180', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 } },
  { id: 'e-m180-m90', source: 'm-d180', target: 'm-d90', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 } },
  { id: 'e-m90-m60', source: 'm-d90', target: 'm-d60', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 } },
  { id: 'e-a1-a2', source: 'a1', target: 'a2', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 } },
  { id: 'e-a2-a3', source: 'a2', target: 'a3', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 } },
  { id: 'e-a3-a4', source: 'a3', target: 'a4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 } },
];
