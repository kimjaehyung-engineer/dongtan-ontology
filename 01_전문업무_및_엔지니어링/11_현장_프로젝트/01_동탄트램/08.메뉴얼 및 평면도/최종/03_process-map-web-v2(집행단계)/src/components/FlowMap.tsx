import React, { useCallback, useRef, useEffect } from 'react';
import ReactFlow, { Background, Controls, MiniMap, ReactFlowProvider, SelectionMode, useReactFlow, MarkerType, ConnectionMode, ConnectionLineType } from 'reactflow';
import type { Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';
import useStore, { lastCanvasMousePos } from '../store/useStore';
import ActionNode from './ActionNode';
import MilestoneNode from './MilestoneNode';
import SwimlaneNode from './SwimlaneNode';
import RowDividerNode from './RowDividerNode';
import TextNode from './TextNode';
import ImageNode from './ImageNode';
import VerticalLineNode from './VerticalLineNode';
import AdjustableEdge from './AdjustableEdge';
import { v4 as uuidv4 } from 'uuid';

import ChecklistItemNode from './ChecklistItemNode';
import ChecklistHeaderNode from './ChecklistHeaderNode';
import TableTitleNode from './TableTitleNode';
import MapFrameNode from './MapFrameNode';

const nodeTypes = {
  action: ActionNode,
  milestone: MilestoneNode,
  swimlane: SwimlaneNode,
  rowDivider: RowDividerNode,
  text: TextNode,
  image: ImageNode,
  verticalLine: VerticalLineNode,
  checklistItem: ChecklistItemNode,
  checklistHeader: ChecklistHeaderNode,
  tableTitle: TableTitleNode,
  mapFrame: MapFrameNode,
};

const edgeTypes = {
  default: AdjustableEdge,
  smoothstep: AdjustableEdge,
  straight: AdjustableEdge,
  step: AdjustableEdge,
  dashed: AdjustableEdge,
};

interface FlowMapProps {
  onNodeDoubleClick?: (event: React.MouseEvent, node: Node) => void;
  onEdgeDoubleClick?: (event: React.MouseEvent, edge: any) => void;
}

export default function FlowMap({ onNodeDoubleClick, onEdgeDoubleClick }: FlowMapProps) {
  return (
    <ReactFlowProvider>
      <FlowMapInner onNodeDoubleClick={onNodeDoubleClick} onEdgeDoubleClick={onEdgeDoubleClick} />
    </ReactFlowProvider>
  );
}

function FlowMapInner({ onNodeDoubleClick, onEdgeDoubleClick }: FlowMapProps) {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, addNode, deleteNode, onReconnect, isSelectMode, fitViewTrigger, activeDisciplineId } = useStore();
  const { project, fitView } = useReactFlow();

  // 창 크기(Window Resize) 및 공종 전환 시 전체 맵 카드가 100% 한눈에 보이도록 동적 Fit View
  useEffect(() => {
    const handleResize = () => {
      if (nodes.length > 0) {
        fitView({ padding: 0.12, duration: 200 });
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [fitView, nodes.length]);

  // 수동 맞춤 버튼 클릭 트리거 연동
  useEffect(() => {
    if (fitViewTrigger > 0) {
      fitView({ padding: 0.12, duration: 300 });
    }
  }, [fitViewTrigger, fitView]);

  // 공종/맵 전환 시 자동 Fit View
  useEffect(() => {
    if (nodes.length > 0) {
      const timer = setTimeout(() => {
        fitView({ padding: 0.12, duration: 300 });
      }, 150);
      return () => clearTimeout(timer);
    }
  }, [activeDisciplineId, fitView]);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const projected = project({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
    lastCanvasMousePos.x = projected.x;
    lastCanvasMousePos.y = projected.y;
  }, [project]);

  // Ctrl+드래그 복사: 드래그 시작 시 Ctrl 눌려있으면 임시 더미 복사본을 생성해 원래 자리를 지킴 (다중 선택 대응)
  const ctrlDragOrigin = useRef<{
    nodes: { node: Node; originalPosition: { x: number; y: number } }[];
    draggedNodeId: string;
    draggedNodeOriginalPosition: { x: number; y: number };
    tempNodeIds: string[];
    held: boolean;
  }>({
    nodes: [],
    draggedNodeId: '',
    draggedNodeOriginalPosition: { x: 0, y: 0 },
    tempNodeIds: [],
    held: false,
  });

  const onNodeDragStart = useCallback((event: React.MouseEvent, node: Node) => {
    // 드래그 시작 직전 상태를 히스토리에 스냅샷으로 저장 (Ctrl+Z용)
    useStore.getState().takeSnapshot();

    if (event.ctrlKey) {
      const { nodes: currentNodes } = useStore.getState();
      const selectedNodes = currentNodes.filter(n => n.selected);
      const isDraggedNodeSelected = selectedNodes.some(n => n.id === node.id);
      const nodesToCopy = isDraggedNodeSelected ? selectedNodes : [node];

      // 임시 더미 노드들 생성
      const tempIds: string[] = [];
      const nodesToCopyData = nodesToCopy.map(n => {
        const tempId = uuidv4();
        tempIds.push(tempId);
        
        // 원래 자리에 더미 노드를 생성해 기존 카드가 계속 보이게 함
        addNode({
          ...n,
          id: tempId,
          selected: false,
          draggable: false,
          position: { ...n.position },
        });

        return {
          node: n,
          originalPosition: { ...n.position }
        };
      });

      ctrlDragOrigin.current = {
        nodes: nodesToCopyData,
        draggedNodeId: node.id,
        draggedNodeOriginalPosition: { ...node.position },
        tempNodeIds: tempIds,
        held: true
      };
    } else {
      ctrlDragOrigin.current.held = false;
      ctrlDragOrigin.current.tempNodeIds = [];
    }
  }, [addNode]);

  const onNodeDragStop = useCallback((_event: React.MouseEvent, node: Node) => {
    if (!ctrlDragOrigin.current.held) return;
    ctrlDragOrigin.current.held = false;

    const { nodes: nodesToCopy, draggedNodeOriginalPosition, tempNodeIds } = ctrlDragOrigin.current;

    // 1. 임시 더미 노드 즉시 제거
    tempNodeIds.forEach(id => {
      deleteNode(id);
    });

    // 2. 드래그 오프셋(델타) 계산
    const deltaX = node.position.x - draggedNodeOriginalPosition.x;
    const deltaY = node.position.y - draggedNodeOriginalPosition.y;

    // 3. 노드 ID 매핑 생성 (새로 복사할 노드들을 위해)
    const idMap: Record<string, string> = {};
    nodesToCopy.forEach(item => {
      idMap[item.node.id] = uuidv4();
    });

    // 4. 원래 노드들의 원래 위치로 복원할 노드 변경 사항 준비
    const restoreChanges = nodesToCopy.map(item => ({
      type: 'position' as const,
      id: item.node.id,
      position: item.originalPosition,
    }));

    // 5. 새 복사 노드들 생성
    const newDuplicatedNodes: Node[] = nodesToCopy.map(item => {
      return {
        ...item.node,
        id: idMap[item.node.id],
        position: {
          x: item.originalPosition.x + deltaX,
          y: item.originalPosition.y + deltaY,
        },
        selected: true, // 복사된 노드들을 선택 상태로 만들어 바로 다음 동작이 가능하게 함
      };
    });

    // 6. 새 복사 노드들 간의 엣지 복제
    const { edges: currentEdges } = useStore.getState();
    const newDuplicatedEdges: Edge[] = [];
    currentEdges.forEach(e => {
      if (idMap[e.source] && idMap[e.target]) {
        newDuplicatedEdges.push({
          ...e,
          id: uuidv4(),
          source: idMap[e.source],
          target: idMap[e.target],
          selected: false,
        });
      }
    });

    // 7. 스토어 상태 변경 적용
    const nextNodes = useStore.getState().nodes.map(n => {
      // 복사된 원본 노드들은 선택 해제
      if (idMap[n.id]) {
        return { ...n, selected: false };
      }
      return n;
    });

    // 8. 노드 위치 복구 적용 및 추가
    const restoreNodes = restoreChanges.reduce((acc, change) => {
      return acc.map(n => {
        if (n.id === change.id) {
          return { ...n, position: change.position };
        }
        return n;
      });
    }, nextNodes);

    // 업데이트 적용
    useStore.getState().setNodesAndEdges(
      [...restoreNodes, ...newDuplicatedNodes],
      [...currentEdges, ...newDuplicatedEdges]
    );

    // 드래그가 종료되었을 때, 액티비티 카드가 위치한 세로축(스윔레인 행)에 맞춰 담당부서(data.department) 자동 동기화
    if (node.type === 'action') {
      const { nodes: latestNodes, edges: latestEdges, setNodesAndEdges } = useStore.getState();
      const droppedY = node.position.y;
      
      const matchedSwimlane = latestNodes.find(
        n => n.type === 'swimlane' &&
        droppedY >= n.position.y - 150 &&
        droppedY < n.position.y + ((n.style?.height as number) || 1080)
      );

      if (matchedSwimlane) {
        const label = (matchedSwimlane.data?.label as string) || '';
        let subDept = '공사';
        let mainCat = '현장';

        if (label.includes('공무') || label.includes('인허가') || label.includes('계약')) subDept = '공무';
        else if (label.includes('품질')) subDept = '품질';
        else if (label.includes('안전') || label.includes('보건') || label.includes('환경')) subDept = '안전';
        else if (label.includes('관리') || label.includes('용지') || label.includes('총무')) subDept = '관리';
        else if (label.includes('본사')) { subDept = '본사'; mainCat = '본사'; }

        const newDeptText = `${mainCat} · ${subDept}`;

        const updatedNodes = latestNodes.map(n => {
          if (n.id === node.id) {
            return {
              ...n,
              data: {
                ...n.data,
                department: newDeptText,
                swimlane: subDept,
                category: mainCat,
              },
            };
          }
          return n;
        });
        setNodesAndEdges(updatedNodes, latestEdges);
      }
    }

    ctrlDragOrigin.current.tempNodeIds = [];
  }, [deleteNode]);

  const processedNodes = React.useMemo(() => {
    return nodes.map(node => {
      if (node.type === 'swimlane') {
        return {
          ...node,
          draggable: isSelectMode,
        };
      }
      return node;
    });
  }, [nodes, isSelectMode]);

  const onEdgeClick = useCallback((event: React.MouseEvent, clickedEdge: Edge) => {
    event.stopPropagation();
    const { edges: currentEdges, setNodesAndEdges, nodes: currentNodes } = useStore.getState();

    const isAlreadySelected = !!clickedEdge.selected;

    const nextEdges = currentEdges.map(e => {
      if (e.id === clickedEdge.id) {
        return {
          ...e,
          selected: !isAlreadySelected,
          style: {
            ...(e.style || {}),
            zIndex: !isAlreadySelected ? 999 : 1,
          },
        };
      }
      return e;
    });

    setNodesAndEdges(currentNodes, nextEdges);
  }, []);

  return (
    <div className="w-full h-full bg-slate-100" onMouseMove={handleMouseMove}>
      <ReactFlow
        className={isSelectMode ? 'select-mode-active' : ''}
        nodes={processedNodes}
        edges={edges}
        connectionMode={ConnectionMode.Loose}
        connectionRadius={150}
        reconnectRadius={100}
        isValidConnection={() => true}
        connectionLineType={ConnectionLineType.SmoothStep}
        connectionLineStyle={{ stroke: '#000000', strokeWidth: 6, opacity: 1 }}
        defaultEdgeOptions={{
          type: 'smoothstep',
          style: { stroke: '#000000', strokeWidth: 6, opacity: 1 },
          markerEnd: { type: MarkerType.ArrowClosed, width: 18, height: 18, color: '#000000' },
          markerStart: undefined,
        }}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onReconnect={onReconnect}
        edgesFocusable={true}
        edgesUpdatable={true}
        elementsSelectable={true}
        deleteKeyCode={['Backspace', 'Delete']}
        onNodeDragStart={onNodeDragStart}
        onNodeDragStop={onNodeDragStop}
        onEdgeClick={onEdgeClick}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        panOnDrag={!isSelectMode}
        zoomOnPinch={true}
        preventScrolling={true}
        selectionOnDrag={isSelectMode}
        selectionMode={SelectionMode.Full}
        selectionKeyCode={isSelectMode ? null : 'Shift'}
        onNodeDoubleClick={onNodeDoubleClick}
        onEdgeDoubleClick={onEdgeDoubleClick}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.1}
        snapToGrid={true}
        snapGrid={[20, 20]}
      >
        <Background color="#ccc" gap={16} />
        <Controls />
        <MiniMap zoomable pannable nodeColor={(n) => {
          if (n.type === 'action') return '#fca5a5';
          if (n.type === 'milestone') return '#334155';
          if (n.type === 'swimlane') return '#e2e8f0';
          return '#eee';
        }} />
      </ReactFlow>
    </div>
  );
}
