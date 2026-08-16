import React from 'react';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import {
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
import { generatePreEarthworkNodesAndEdges } from '../utils/preEarthworkLoader';
import { generateAiContextEdges, autoAlignActionNodes } from '../utils/aiContextLinker';

// Clean up all old process-map-storage-* keys to free up quota
try {
  if (typeof window !== 'undefined' && window.localStorage) {
    const keysToRemove: string[] = [];
    for (let i = 0; i < window.localStorage.length; i++) {
      const k = window.localStorage.key(i);
      if (k && k.startsWith('process-map-storage-') && k !== 'process-map-storage-v85') {
        keysToRemove.push(k);
      }
    }
    keysToRemove.forEach(k => {
      try { window.localStorage.removeItem(k); } catch (e) {}
    });
  }
} catch (e) {
  console.warn('LocalStorage cleanup error:', e);
}

// 마우스 움직임에 따른 캔버스상 좌표(비반응형) 추적용 전역 레퍼런스
export const lastCanvasMousePos = { x: 500, y: 300 };

export interface DisciplineMapItem {
  id: string;
  name: string; // e.g. "🏗️ 사전토공사", "📡 신호", "📶 통신"
  sheetName?: string;
  mapTitle: string;
  nodes: Node<NodeData>[];
  edges: Edge[];
  itemCount: number;
}

export type NodeData = {
  label?: string;
  category?: string;               // 1차 세로축 대분류 ('현장' | '본사')
  isCategoryFirst?: boolean;       // 1차 세로축 대분류 시작 행 여부
  categorySpanHeight?: number;     // 1차 세로축 대분류 총 세로 높이
  department?: string;
  purpose?: string;
  method?: string;
  result?: string;
  swimlane?: string;
  color?: string;
  wbsCode?: string;     // L4 코드 (예: 9000-7-1)
  predecessor?: string; // 선행 L4 코드 (예: 9000-7-1)
  successor?: string;   // 후행 L4 코드 (예: 9000-7-3)
  status?: 'normal' | 'warning' | 'danger' | 'done' | 'todo' | 'inprogress' | 'na';  // 진행 상태
  daysRemaining?: number;  // D-day 잔여일
  fileUrl?: string;  // 첨부 파일/링크
  note?: string;  // 메모
  cooperation?: string;  // 협조 부서 (쉼표 구분)
  date?: string;  // 마일스톤 기한/기간 정보
  isCritical?: boolean; // CP 주경로 여부
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
  disciplineMaps: DisciplineMapItem[];
  activeDisciplineId: string;
  setDisciplineMaps: (maps: DisciplineMapItem[], activeId?: string) => void;
  selectDisciplineMap: (id: string) => void;
  addDisciplineMap: (map: DisciplineMapItem) => void;
  past: { nodes: Node<NodeData>[]; edges: Edge[] }[];
  future: { nodes: Node<NodeData>[]; edges: Edge[] }[];
  activeDetailTab: 'directive' | 'standard' | 'checklist';
  setActiveDetailTab: (tab: 'directive' | 'standard' | 'checklist') => void;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  isCpHighlight: boolean;
  toggleCpHighlight: () => void;
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
  deletedEdgeKeys: string[];
  recordDeletedEdgeKeys: (keys: string[]) => void;
  clearDeletedEdgeKeys: () => void;
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
  copiedNodes: Node<NodeData>[] | null;
  copiedEdges: Edge[] | null;
  setCopiedNodesAndEdges: (nodes: Node<NodeData>[], edges: Edge[]) => void;
  rawWorkbookBuffer: ArrayBuffer | null;
  setRawWorkbookBuffer: (buffer: ArrayBuffer | null) => void;
  fitViewTrigger: number;
  triggerFitView: () => void;
  resetToDefaultMap: () => void;
  autoConnectByAiContext: () => void;
  addSwimlaneRow: (afterId?: string, customLabel?: string) => void;
  deleteSwimlaneRow: (swimlaneId: string) => void;
  renameSwimlaneRow: (swimlaneId: string, newLabel: string) => void;
};

const defaultData = generatePreEarthworkNodesAndEdges();

const useStore = create<RFState>()(
  persist(
    (set, get) => ({
      nodes: defaultData.nodes,
      edges: defaultData.edges,
      disciplineMaps: [],
      activeDisciplineId: '',
      rawWorkbookBuffer: null,
      setRawWorkbookBuffer: (buffer: ArrayBuffer | null) => set({ rawWorkbookBuffer: buffer }),
      fitViewTrigger: 0,
      triggerFitView: () => set((state) => ({ fitViewTrigger: state.fitViewTrigger + 1 })),
      resetToDefaultMap: () => {
        const fresh = generatePreEarthworkNodesAndEdges();
        get().takeSnapshot();
        set({
          nodes: fresh.nodes,
          edges: fresh.edges,
          deletedEdgeKeys: [],
        });
      },
      autoConnectByAiContext: () => {
        const { nodes } = get();
        get().takeSnapshot();
        const alignedNodes = autoAlignActionNodes(nodes);
        const newEdges = generateAiContextEdges(alignedNodes);
        set({
          nodes: alignedNodes,
          edges: newEdges,
          deletedEdgeKeys: [],
        });
        set((state) => ({ fitViewTrigger: state.fitViewTrigger + 1 }));
      },

      // ── 행 추가: afterId 스윔레인 아래에 새 행 삽입 ──
      addSwimlaneRow: (afterId?: string, customLabel?: string) => {
        const { nodes, edges } = get();
        get().takeSnapshot();

        let afterNode = nodes.find(n => n.id === afterId && n.type === 'swimlane');
        if (!afterNode) {
          if (customLabel?.includes('품질')) {
            afterNode = nodes.find(n => n.type === 'swimlane' && ((n.data?.label as string) || '').includes('공사'))
                     || nodes.find(n => n.type === 'swimlane' && ((n.data?.label as string) || '').includes('공무'));
          }
          if (!afterNode) {
            const swimlanes = nodes.filter(n => n.type === 'swimlane');
            if (swimlanes.length > 0) {
              afterNode = swimlanes.reduce((max, n) => (n.position.y > max.position.y ? n : max), swimlanes[0]);
            }
          }
        }
        if (!afterNode) return;

        const afterY = afterNode.position.y;
        const afterH = (afterNode.style?.height as number) || 1080;
        const insertY = afterY + afterH;
        const newRowHeight = 1080;
        const rowLabel = customLabel || '📋 새 행 (더블클릭하여 이름 변경)';
        const newId = customLabel?.includes('품질') ? 'swimlane-품질' : `swimlane-new-${Date.now()}`;

        const existingNode = nodes.find(n => n.id === newId);
        if (existingNode) {
          const nextNodes = nodes.map(n => n.id === newId ? { ...n, position: { ...n.position, y: insertY }, data: { ...n.data, label: rowLabel } } : n);
          set({ nodes: nextNodes, edges });
          return;
        }

        const shifted = nodes.map(n => {
          if (n.id === newId) return n;
          if (n.position.y >= insertY - 5) {
            return { ...n, position: { ...n.position, y: n.position.y + newRowHeight } };
          }
          return n;
        });

        const masterIdx = shifted.findIndex(n => n.id === 'map-frame-master');
        if (masterIdx >= 0) {
          const m = shifted[masterIdx];
          shifted[masterIdx] = {
            ...m,
            style: { ...m.style, height: ((m.style?.height as number) || 6700) + newRowHeight },
          };
        }

        shifted.forEach((n, i) => {
          if (n.type === 'verticalLine' && n.data?.height) {
            shifted[i] = { ...n, data: { ...n.data, height: (n.data.height as number) + newRowHeight } };
          }
        });

        const totalW = (shifted.find(n => n.id === 'map-frame-master')?.style?.width as number) || 8800;
        const newSwimlane: Node<NodeData> = {
          id: newId,
          type: 'swimlane',
          position: { x: 0, y: insertY },
          data: {
            label: rowLabel,
            category: '현장',
            isCategoryFirst: false,
            categorySpanHeight: newRowHeight,
          },
          style: { width: totalW, height: newRowHeight, zIndex: -1 },
          draggable: false,
          selectable: true,
        };

        const newDivider: Node<NodeData> = {
          id: `rdiv-${Date.now()}`,
          type: 'rowDivider',
          position: { x: 0, y: insertY },
          data: {},
          draggable: true,
          selectable: false,
          style: { zIndex: 10 },
        };

        set({ nodes: [...shifted, newSwimlane, newDivider], edges });
      },

      // ── 행 삭제: 해당 스윔레인 행 제거 및 아래 행들 위로 당김 ──
      deleteSwimlaneRow: (swimlaneId: string) => {
        const { nodes, edges } = get();
        get().takeSnapshot();

        const target = nodes.find(n => n.id === swimlaneId && n.type === 'swimlane');
        if (!target) return;

        const targetY = target.position.y;
        const targetH = (target.style?.height as number) || 1080;
        const bottomY = targetY + targetH;

        // 삭제 대상 행 및 해당 Y 범위의 구분선 제거
        let filtered = nodes.filter(n => {
          if (n.id === swimlaneId) return false;
          // 해당 행 위치의 구분선도 제거
          if (n.type === 'rowDivider' && Math.abs(n.position.y - targetY) < 10) return false;
          return true;
        });

        // bottomY 이상인 노드들을 targetH만큼 위로 당김
        filtered = filtered.map(n => {
          if (n.id === 'map-frame-master') {
            return { ...n, style: { ...n.style, height: Math.max(1080, ((n.style?.height as number) || 6700) - targetH) } };
          }
          if (n.type === 'verticalLine' && n.data?.height) {
            return { ...n, data: { ...n.data, height: Math.max(1080, (n.data.height as number) - targetH) } };
          }
          if (n.position.y >= bottomY - 5) {
            return { ...n, position: { ...n.position, y: n.position.y - targetH } };
          }
          return n;
        });

        set({ nodes: filtered, edges });
      },

      // ── 행 이름 변경 ──
      renameSwimlaneRow: (swimlaneId: string, newLabel: string) => {
        const { nodes } = get();
        get().takeSnapshot();
        set({
          nodes: nodes.map(n =>
            n.id === swimlaneId ? { ...n, data: { ...n.data, label: newLabel } } : n
          ),
        });
      },
      setDisciplineMaps: (newMaps, activeId) => {
        const targetId = activeId || newMaps[0]?.id || '';
        const targetMap = newMaps.find(m => m.id === targetId) || newMaps[0];

        set({
          disciplineMaps: newMaps,
          activeDisciplineId: targetId,
          nodes: targetMap ? targetMap.nodes : [],
          edges: targetMap ? targetMap.edges : [],
          past: [],
          future: [],
        });
      },
      selectDisciplineMap: (id) => {
        const { disciplineMaps, activeDisciplineId, nodes, edges } = get();
        if (id === activeDisciplineId) return;

        // Save current active canvas state into disciplineMaps
        const updatedMaps = disciplineMaps.map(item => {
          if (item.id === activeDisciplineId) {
            return {
              ...item,
              nodes: nodes,
              edges: edges,
              itemCount: nodes.filter(n => n.type === 'action').length,
            };
          }
          return item;
        });

        const targetMap = updatedMaps.find(m => m.id === id);
        if (targetMap) {
          set({
            disciplineMaps: updatedMaps,
            activeDisciplineId: id,
            nodes: targetMap.nodes,
            edges: targetMap.edges,
            past: [],
            future: [],
          });
        }
      },
      addDisciplineMap: (map) => {
        const { disciplineMaps } = get();
        const existingIdx = disciplineMaps.findIndex(m => m.id === map.id || m.name === map.name);
        let newMaps = [...disciplineMaps];
        if (existingIdx >= 0) {
          newMaps[existingIdx] = map;
        } else {
          newMaps.push(map);
        }
        set({
          disciplineMaps: newMaps,
          activeDisciplineId: map.id,
          nodes: map.nodes,
          edges: map.edges,
          past: [],
          future: [],
        });
      },
      past: [],
      future: [],
      activeDetailTab: 'directive',
      setActiveDetailTab: (tab) => set({ activeDetailTab: tab }),
      isDarkMode: false,
      toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
      isCpHighlight: false,
      toggleCpHighlight: () => set((state) => ({ isCpHighlight: !state.isCpHighlight })),
      isSelectMode: false,
      setSelectMode: (val: boolean) => set({ isSelectMode: val }),
      copiedStyle: null,
      setCopiedStyle: (style) => set({ copiedStyle: style }),
      copiedNodes: null,
      copiedEdges: null,
      setCopiedNodesAndEdges: (nodes, edges) => set({ copiedNodes: nodes, copiedEdges: edges }),
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
      deletedEdgeKeys: [],
      recordDeletedEdgeKeys: (keys: string[]) => {
        const current = get().deletedEdgeKeys || [];
        const nextSet = new Set([...current, ...keys]);
        const nextList = Array.from(nextSet);
        set({ deletedEdgeKeys: nextList });
      },
      clearDeletedEdgeKeys: () => set({ deletedEdgeKeys: [] }),

      onNodesChange: (changes: NodeChange[]) => {
        const constrainedChanges = changes.map((change) => {
          if (change.type === 'position' && change.position) {
            const node = get().nodes.find((n) => n.id === change.id);
            if (node) {
              if (node.type === 'verticalLine') {
                return {
                  ...change,
                  position: {
                    ...change.position,
                    y: node.position.y,
                  },
                };
              } else if (node.type === 'rowDivider') {
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
        // 사용자가 엣지를 삭제하는 change 추적하여 deletedEdgeKeys에 기록
        const removedIds = changes.filter(c => c.type === 'remove').map(c => (c as any).id);
        if (removedIds.length > 0) {
          const removedEdges = get().edges.filter(e => removedIds.includes(e.id));
          const keysToRecord: string[] = [];
          removedEdges.forEach(e => {
            keysToRecord.push(e.id);
            if (e.source && e.target) {
              keysToRecord.push(`${e.source}->${e.target}`);
            }
          });
          if (keysToRecord.length > 0) {
            const current = get().deletedEdgeKeys || [];
            set({ deletedEdgeKeys: Array.from(new Set([...current, ...keysToRecord])) });
          }
        }

        set({
          edges: applyEdgeChanges(changes, get().edges),
        });
      },
      onConnect: (connection: Connection) => {
        get().takeSnapshot();

        let { source, target, sourceHandle, targetHandle } = connection;
        if (!source || !target) return;

        let srcId = source;
        let tgtId = target;
        let sHandle = (sourceHandle || 'right').replace('-source', '').replace('-target', '');
        let tHandle = (targetHandle || 'left').replace('-source', '').replace('-target', '');

        const strokeColor = '#000000';
        const strokeWidth = 6;

        const edge: Edge = { 
          id: `edge-${srcId}-${tgtId}-${Date.now().toString(36)}`,
          source: srcId,
          target: tgtId,
          sourceHandle: sHandle,
          targetHandle: tHandle,
          type: 'smoothstep',
          pathOptions: { borderRadius: 16 },
          style: { stroke: strokeColor, strokeWidth: strokeWidth, opacity: 1 },
          markerEnd: { type: MarkerType.ArrowClosed, width: 20, height: 20, color: strokeColor },
        };

        const existing = get().edges;
        set({
          edges: [...existing, edge],
        });
      },
      onReconnect: (oldEdge: Edge, newConnection: Connection) => {
        get().takeSnapshot();
        const reconnected = reconnectEdge(oldEdge, newConnection, get().edges);
        const safeReconnected = reconnected.map((e) => {
          if (e.id === oldEdge.id) {
            return {
              ...e,
              sourceHandle: newConnection.sourceHandle ?? e.sourceHandle,
              targetHandle: newConnection.targetHandle ?? e.targetHandle,
              animated: false,
              style: e.style || { stroke: '#000000', strokeWidth: 5.5 },
              markerEnd: e.markerEnd || { type: MarkerType.ArrowClosed, color: '#000000', width: 24, height: 24 },
            };
          }
          return e;
        });
        set({
          edges: safeReconnected,
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
        const targetEdge = get().edges.find(e => e.id === edgeId);
        if (targetEdge) {
          const keys = [targetEdge.id];
          if (targetEdge.source && targetEdge.target) {
            keys.push(`${targetEdge.source}->${targetEdge.target}`);
          }
          const current = get().deletedEdgeKeys || [];
          set({ deletedEdgeKeys: Array.from(new Set([...current, ...keys])) });
        }
        set({
          edges: get().edges.filter((e) => e.id !== edgeId),
        });
      },
    }),
    {
      name: 'process-map-storage-v92',
      version: 92,
      migrate: (persistedState: any, version: number) => {
        if (version < 92) {
          const fresh = generatePreEarthworkNodesAndEdges();
          return {
            nodes: fresh.nodes,
            edges: fresh.edges,
            disciplineMaps: [],
            activeDisciplineId: '',
            past: [],
            future: [],
          };
        }
        let state = persistedState;

        if (version < 27) {
          return {
            nodes: [],
            edges: [],
            disciplineMaps: [],
            activeDisciplineId: '',
            past: [],
            future: [],
          };
        }

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
            ];
            const added = toAdd.filter(n => !existing.has(n.id));
            state = { ...state, nodes: [...state.nodes, ...added] };
          }
        }

        if (version < 6) {
          const { nodes, edges } = generatePreEarthworkNodesAndEdges();
          return {
            nodes,
            edges,
            past: [],
            future: [],
          };
        }

        return state;
      },
      partialize: (state) => ({
        nodes: state.nodes,
        edges: state.edges,
        disciplineMaps: state.disciplineMaps,
        activeDisciplineId: state.activeDisciplineId,
      }),
      storage: {
        getItem: (name) => {
          try {
            const str = localStorage.getItem(name);
            return str ? JSON.parse(str) : null;
          } catch (e) {
            return null;
          }
        },
        setItem: (name, value) => {
          try {
            localStorage.setItem(name, JSON.stringify(value));
          } catch (e) {
            console.warn('LocalStorage quota exceeded, attempting fallback cleanup:', e);
            try {
              // Delete older keys if quota exceeded
              for (let i = localStorage.length - 1; i >= 0; i--) {
                const k = localStorage.key(i);
                if (k && k !== name) localStorage.removeItem(k);
              }
              // Save with minimized state (only active nodes/edges)
              const minVal = {
                state: {
                  nodes: (value as any)?.state?.nodes || [],
                  edges: (value as any)?.state?.edges || [],
                  activeDisciplineId: (value as any)?.state?.activeDisciplineId || '',
                },
                version: (value as any)?.version || 85,
              };
              localStorage.setItem(name, JSON.stringify(minVal));
            } catch (err) {
              console.error('Safe storage fallback failed silently:', err);
            }
          }
        },
        removeItem: (name) => {
          try {
            localStorage.removeItem(name);
          } catch (e) {}
        },
      },
    }
  )
);

export default useStore;
