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

export type NodeData = {
  label?: string;
  department?: string;
  purpose?: string;
  method?: string;
  result?: string;
  swimlane?: string;
  color?: string;
  // New fields
  status?: 'normal' | 'warning' | 'danger' | 'done';  // 진행 상태
  daysRemaining?: number;  // D-day 잔여일
  fileUrl?: string;  // 첨부 파일/링크
  note?: string;  // 메모
  cooperation?: string;  // 협조 부서 (쉼표 구분)
  date?: string;  // 마일스톤 기한/기간 정보
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
                // Lock Y position to 150 for horizontal-only movement
                return {
                  ...change,
                  position: {
                    ...change.position,
                    y: 150,
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
      version: 1,
      migrate: (persistedState: any, version: number) => {
        if (version < 1) {
          const state = persistedState as RFState;
          if (state && state.nodes) {
            let updatedNodes = [...state.nodes];

            // 'swimlane-본사'가 아직 저장되지 않은 기존 데이터인 경우
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
                selectable: false,
              });

              // 2. 'swimlane-인허가' 및 기존 노드 보정
              updatedNodes = updatedNodes.map(n => {
                // 인허가 행 Y좌표를 2150으로 이동
                if (n.id === 'swimlane-인허가') {
                  return { ...n, position: { ...n.position, y: 2150 } };
                }
                // 구분선 rdiv-5를 y=1850으로 조정
                if (n.id === 'rdiv-5') {
                  return { ...n, position: { ...n.position, y: 1850 } };
                }
                // 마일스톤 수직 점선(verticalLine) 높이를 2300px로 연장
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

            return {
              ...state,
              nodes: updatedNodes,
            };
          }
        }
        return persistedState;
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
