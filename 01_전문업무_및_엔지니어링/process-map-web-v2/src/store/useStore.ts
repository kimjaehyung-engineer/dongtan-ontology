import React from 'react';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import {
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  MarkerType,
  reconnectEdge,
} from 'reactflow';
import type {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
} from 'reactflow';
import { initialNodes, initialEdges } from './initialData';

// 마우스 움직임에 따른 캔버스상 좌표(비반응형) 추적용 전역 레퍼런스
export const lastCanvasMousePos = { x: 500, y: 300 };

export type NodeData = {
  label?: string;
  department?: string;
  purpose?: string;
  method?: string;
  result?: string;
  swimlane?: string;
  color?: string;
  // New fields
  status?: 'normal' | 'warning' | 'danger' | 'done' | 'todo' | 'inprogress' | 'na';  // 진행 상태
  daysRemaining?: number;  // D-day 잔여일
  fileUrl?: string;  // 첨부 파일/링크
  note?: string;  // 메모
  cooperation?: string;  // 협조 부서 (쉼표 구분)
  date?: string;  // 마일스톤 기한/기간 정보
  width?: number;
  height?: number;
  textStyle?: {
    bgColor?: string;
    borderStyle?: string;
    borderWidth?: number;
    fontSize?: number;
    color?: string;
  };
};

type RFState = {
  nodes: Node<NodeData>[];
  edges: Edge[];
  past: { nodes: Node<NodeData>[]; edges: Edge[] }[];
  future: { nodes: Node<NodeData>[]; edges: Edge[] }[];
  takeSnapshot: () => void;
  undo: () => void;
  redo: () => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  onReconnect: (oldEdge: Edge, newConnection: Connection) => void;
  addNode: (node: Node<NodeData>) => void;
  setNodesAndEdges: (nodes: Node<NodeData>[], edges: Edge[]) => void;
  updateNodeData: (nodeId: string, data: Partial<NodeData>) => void;
  updateNodeStyle: (nodeId: string, style: React.CSSProperties) => void;
  deleteNode: (nodeId: string) => void;
  updateEdge: (edgeId: string, edgePatch: Partial<Edge>) => void;
  deleteEdge: (edgeId: string) => void;
  isSelectMode: boolean;
  setSelectMode: (val: boolean) => void;
  copiedStyle: {
    type?: string;
    color?: string;
    textStyle?: any;
    status?: 'normal' | 'warning' | 'danger' | 'done' | 'todo' | 'inprogress' | 'na';
    department?: string;
    style?: React.CSSProperties;
  } | null;
  setCopiedStyle: (style: {
    type?: string;
    color?: string;
    textStyle?: any;
    status?: 'normal' | 'warning' | 'danger' | 'done' | 'todo' | 'inprogress' | 'na';
    department?: string;
    style?: React.CSSProperties;
  } | null) => void;
};

const useStore = create<RFState>()(
  persist(
    (set, get) => ({
      nodes: initialNodes,
      edges: initialEdges,
      past: [],
      future: [],
      isSelectMode: false,
      setSelectMode: (val: boolean) => set({ isSelectMode: val }),
      copiedStyle: null,
      setCopiedStyle: (style) => set({ copiedStyle: style }),
      takeSnapshot: () => {
        const { nodes, edges, past } = get();
        // JSON 직렬화를 통한 깔끔한 딥 카피 진행
        const snapshot = JSON.parse(JSON.stringify({ nodes, edges }));
        
        // 직전 스냅샷과 현재 노드/엣지 내용이 완벽히 동일하다면 중복 기록 패스
        if (past.length > 0) {
          const last = past[past.length - 1];
          if (JSON.stringify(last.nodes) === JSON.stringify(nodes) && 
              JSON.stringify(last.edges) === JSON.stringify(edges)) {
            return;
          }
        }

        const newPast = [...past, snapshot];
        if (newPast.length > 50) {
          newPast.shift(); // 히스토리 최대 50개 유지
        }

        set({
          past: newPast,
          future: [], // 새로운 작업을 수행하면 다시 실행(redo) 스택은 초기화
        });
      },
      undo: () => {
        const { past, future, nodes, edges } = get();
        if (past.length === 0) return;

        const previous = past[past.length - 1];
        const newPast = past.slice(0, past.length - 1);
        const current = JSON.parse(JSON.stringify({ nodes, edges }));

        set({
          nodes: previous.nodes,
          edges: previous.edges,
          past: newPast,
          future: [...future, current],
        });
      },
      redo: () => {
        const { past, future, nodes, edges } = get();
        if (future.length === 0) return;

        const next = future[future.length - 1];
        const newFuture = future.slice(0, future.length - 1);
        const current = JSON.parse(JSON.stringify({ nodes, edges }));

        set({
          nodes: next.nodes,
          edges: next.edges,
          past: [...past, current],
          future: newFuture,
        });
      },
      onNodesChange: (changes: NodeChange[]) => {
        const constrainedChanges = changes.map((change) => {
          if (change.type === 'position' && change.position) {
            const node = get().nodes.find((n) => n.id === change.id);
            if (node) {
              if (node.type === 'verticalLine') {
                // Lock Y position to its current Y position for horizontal-only movement
                return {
                  ...change,
                  position: {
                    ...change.position,
                    y: node.position.y,
                  },
                };
              } else if (node.type === 'rowDivider') {
                // Lock X position to 0 for vertical-only movement
                return {
                  ...change,
                  position: {
                    ...change.position,
                    x: 0,
                  },
                };
              }
            }
          }
          return change;
        });

        set({
          nodes: applyNodeChanges(constrainedChanges, get().nodes),
        });
      },
      onEdgesChange: (changes: EdgeChange[]) => {
        set({
          edges: applyEdgeChanges(changes, get().edges),
        });
      },
      onConnect: (connection: Connection) => {
        get().takeSnapshot();
        const edge = { 
          ...connection, 
          type: 'smoothstep', 
          style: { stroke: '#94a3b8', strokeWidth: 2 },
          markerEnd: { type: MarkerType.ArrowClosed, width: 22, height: 22, color: '#94a3b8' } 
        };
        set({
          edges: addEdge(edge, get().edges),
        });
      },
      onReconnect: (oldEdge: Edge, newConnection: Connection) => {
        get().takeSnapshot();
        set({
          edges: reconnectEdge(oldEdge, newConnection, get().edges),
        });
      },
      addNode: (node) => {
        get().takeSnapshot();
        set({
          nodes: [...get().nodes, node],
        });
      },
      setNodesAndEdges: (nodes, edges) => {
        set({ nodes, edges });
      },
      updateNodeData: (nodeId, data) => {
        set({
          nodes: get().nodes.map((node) => {
            if (node.id === nodeId) {
              node.data = { ...node.data, ...data };
            }
            return node;
          }),
        });
      },
      updateNodeStyle: (nodeId, style) => {
        get().takeSnapshot();
        set({
          nodes: get().nodes.map((node) => {
            if (node.id === nodeId) {
              return { ...node, style: { ...node.style, ...style } };
            }
            return node;
          }),
        });
      },
      deleteNode: (nodeId) => {
        get().takeSnapshot();
        set({
          nodes: get().nodes.filter((n) => n.id !== nodeId),
          edges: get().edges.filter((e) => e.source !== nodeId && e.target !== nodeId),
        });
      },
      updateEdge: (edgeId, edgePatch) => {
        get().takeSnapshot();
        set({
          edges: get().edges.map((edge) => {
            if (edge.id === edgeId) {
              return { ...edge, ...edgePatch };
            }
            return edge;
          }),
        });
      },
      deleteEdge: (edgeId) => {
        get().takeSnapshot();
        set({
          edges: get().edges.filter((e) => e.id !== edgeId),
        });
      },
    }),
    {
      name: 'process-map-storage-v2',
      version: 4,
      migrate: (persistedState: any, version: number) => {
        let state = persistedState;

        if (version < 1) {
          if (state && state.nodes) {
            let updatedNodes = [...state.nodes];
            const hasHeadOffice = updatedNodes.some(n => n.id === 'swimlane-본사');
            if (!hasHeadOffice) {
              // 1. 'swimlane-본사' 행 추가
              updatedNodes.push({
                id: 'swimlane-본사',
                type: 'swimlane',
                position: { x: 0, y: 1850 },
                data: { label: '본사' },
                style: { width: 2500, height: 300, zIndex: -1 },
                draggable: false,
                selectable: true,
              });

              // 2. 'swimlane-인허가' 및 기존 노드 보정
              updatedNodes = updatedNodes.map(n => {
                if (n.id === 'swimlane-인허가') {
                  return { ...n, position: { ...n.position, y: 2150 } };
                }
                if (n.id === 'rdiv-5') {
                  return { ...n, position: { ...n.position, y: 1850 } };
                }
                if (n.type === 'verticalLine') {
                  return { ...n, data: { ...n.data, height: 2300 } };
                }
                return n;
              });

              // 3. 신규 본사와 인허가 사이 구분선 'rdiv-6' (y=2150) 추가
              const hasRdiv6 = updatedNodes.some(n => n.id === 'rdiv-6');
              if (!hasRdiv6) {
                updatedNodes.push({ 
                  id: 'rdiv-6', 
                  type: 'rowDivider', 
                  position: { x: 0, y: 2150 }, 
                  data: {}, 
                  draggable: true, 
                  selectable: false, 
                  style: { zIndex: 10 } 
                });
              }
            }
            state = { ...state, nodes: updatedNodes };
          }
        }

        if (version < 2) {
          if (state && state.nodes) {
            let updatedNodes = [...state.nodes];

            // 1. Shift positions of non-layout cards (action, text, image) in swimlanes down by 200px
            updatedNodes = updatedNodes.map(n => {
              if (n.type === 'action' || n.type === 'text' || n.type === 'image') {
                if (n.position.y >= 150) {
                  return { ...n, position: { ...n.position, y: n.position.y + 200 } };
                }
              }

              // 2. Shift layout swimlanes down to make room for Checklist row
              if (n.type === 'swimlane') {
                if (n.id === 'swimlane-공무') return { ...n, position: { x: 0, y: 350 }, style: { ...n.style, height: 400 } };
                if (n.id === 'swimlane-공사') return { ...n, position: { x: 0, y: 750 }, style: { ...n.style, height: 400 } };
                if (n.id === 'swimlane-품질') return { ...n, position: { x: 0, y: 1150 }, style: { ...n.style, height: 300 } };
                if (n.id === 'swimlane-안전') return { ...n, position: { x: 0, y: 1450 }, style: { ...n.style, height: 300 } };
                if (n.id === 'swimlane-관리') return { ...n, position: { x: 0, y: 1750 }, style: { ...n.style, height: 300 } };
                if (n.id === 'swimlane-본사') return { ...n, position: { x: 0, y: 2050 }, style: { ...n.style, height: 300 } };
                if (n.id === 'swimlane-인허가') return { ...n, position: { x: 0, y: 2350 }, style: { ...n.style, height: 300 } };
              }

              // 3. Shift dividers down
              if (n.type === 'rowDivider') {
                if (n.id === 'rdiv-1') return { ...n, position: { ...n.position, y: 750 } };
                if (n.id === 'rdiv-2') return { ...n, position: { ...n.position, y: 1150 } };
                if (n.id === 'rdiv-3') return { ...n, position: { ...n.position, y: 1450 } };
                if (n.id === 'rdiv-4') return { ...n, position: { ...n.position, y: 1750 } };
                if (n.id === 'rdiv-5') return { ...n, position: { ...n.position, y: 2050 } };
                if (n.id === 'rdiv-6') return { ...n, position: { ...n.position, y: 2350 } };
              }

              // 4. Update vertical lines height and start Y position
              if (n.type === 'verticalLine') {
                return {
                  ...n,
                  position: { ...n.position, y: 0 },
                  data: { ...n.data, height: 2650 }
                };
              }

              return n;
            });

            // 5. Add 'swimlane-마일스톤'
            const hasMilestoneSwimlane = updatedNodes.some(n => n.id === 'swimlane-마일스톤');
            if (!hasMilestoneSwimlane) {
              updatedNodes.push({
                id: 'swimlane-마일스톤',
                type: 'swimlane',
                position: { x: 0, y: 0 },
                data: { label: '마일스톤' },
                style: { width: 2500, height: 150, zIndex: -1 },
                draggable: false,
                selectable: true,
              });
            }

            // 6. Add 'swimlane-체크리스트'
            const hasChecklistSwimlane = updatedNodes.some(n => n.id === 'swimlane-체크리스트');
            if (!hasChecklistSwimlane) {
              updatedNodes.push({
                id: 'swimlane-체크리스트',
                type: 'swimlane',
                position: { x: 0, y: 150 },
                data: { label: '체크리스트' },
                style: { width: 2500, height: 200, zIndex: -1 },
                draggable: false,
                selectable: true,
              });
            }

            // 7. Add 'rdiv-milestone' and 'rdiv-checklist'
            const hasRdivMilestone = updatedNodes.some(n => n.id === 'rdiv-milestone');
            if (!hasRdivMilestone) {
              updatedNodes.push({
                id: 'rdiv-milestone',
                type: 'rowDivider',
                position: { x: 0, y: 150 },
                data: {},
                draggable: true,
                selectable: false,
                style: { zIndex: 10 }
              });
            }
            const hasRdivChecklist = updatedNodes.some(n => n.id === 'rdiv-checklist');
            if (!hasRdivChecklist) {
              updatedNodes.push({
                id: 'rdiv-checklist',
                type: 'rowDivider',
                position: { x: 0, y: 350 },
                data: {},
                draggable: true,
                selectable: false,
                style: { zIndex: 10 }
              });
            }

            state = { ...state, nodes: updatedNodes };
          }
        }

        if (version < 3) {
          if (state && state.nodes) {
            state = {
              ...state,
              nodes: state.nodes.map((n: any) => {
                if (n.type === 'swimlane') {
                  return { ...n, selectable: true };
                }
                return n;
              })
            };
          }
        }

        if (version < 4) {
          if (state && state.nodes) {
            const existing = new Set(state.nodes.map((n: any) => n.id));
            const toAdd = [
              {
                id: 'txt-cl-1', type: 'text',
                position: { x: 100, y: 175 },
                data: {
                  label: '✅ 설계도서 검토 완료\n✅ 관계기관 협의 완료\n⬜ 착공신고 접수\n⬜ 착수 전 Big Room',
                  textStyle: { bgColor: 'white', borderStyle: 'solid', fontSize: 12, color: '#1e293b' },
                },
                style: { width: 200, height: 130, zIndex: 5 },
              },
              {
                id: 'txt-cl-2', type: 'text',
                position: { x: 550, y: 175 },
                data: {
                  label: '📋 발주 전 점검사항\n⬜ 현장설명서 배포\n⬜ 입찰공고 게시\n✅ 예산 확보 확인',
                  textStyle: { bgColor: 'yellow', borderStyle: 'solid', fontSize: 12, color: '#92400e' },
                },
                style: { width: 200, height: 130, zIndex: 5 },
              },
              {
                id: 'txt-cl-3', type: 'text',
                position: { x: 950, y: 175 },
                data: {
                  label: '🔍 계약 전 확인사항\n✅ 계약서 검토\n⬜ 보증보험 징구\n⬜ 착공계 제출',
                  textStyle: { bgColor: 'blue', borderStyle: 'solid', fontSize: 12, color: '#1e3a5f' },
                },
                style: { width: 200, height: 130, zIndex: 5 },
              },
              {
                id: 'txt-cl-4', type: 'text',
                position: { x: 1450, y: 175 },
                data: {
                  label: '📌 착공 준비 체크\n⬜ 시공계획서 승인\n⬜ 안전관리계획 승인\n⬜ 시공상세도 승인',
                  textStyle: { bgColor: 'green', borderStyle: 'solid', fontSize: 12, color: '#14532d' },
                },
                style: { width: 200, height: 130, zIndex: 5 },
              },
            ].filter((n: any) => !existing.has(n.id));

            state = { ...state, nodes: [...state.nodes, ...toAdd] };
          }
        }

        return state;
      },
      partialize: (state) => ({
        nodes: state.nodes,
        edges: state.edges,
        past: state.past,
        future: state.future,
      }),
    }
  )
);

export default useStore;
