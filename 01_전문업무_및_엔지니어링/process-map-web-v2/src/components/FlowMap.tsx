import React, { useCallback, useRef } from 'react';
import ReactFlow, { Background, Controls, MiniMap, ReactFlowProvider, SelectionMode } from 'reactflow';
import type { Node } from 'reactflow';
import 'reactflow/dist/style.css';
import useStore from '../store/useStore';
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

const nodeTypes = {
  action: ActionNode,
  milestone: MilestoneNode,
  swimlane: SwimlaneNode,
  rowDivider: RowDividerNode,
  text: TextNode,
  image: ImageNode,
  verticalLine: VerticalLineNode,
  checklistItem: ChecklistItemNode,
};

const edgeTypes = {
  smoothstep: AdjustableEdge,
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
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, addNode, deleteNode, onReconnect, isSelectMode } = useStore();

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

    ctrlDragOrigin.current.tempNodeIds = [];
  }, [deleteNode]);

  return (
    <div className="w-full h-full bg-slate-100">
      <ReactFlow
        className={isSelectMode ? 'select-mode-active' : ''}
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onReconnect={onReconnect}
        deleteKeyCode={['Backspace', 'Delete']}
        onNodeDragStart={onNodeDragStart}
        onNodeDragStop={onNodeDragStop}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        panOnDrag={!isSelectMode}
        selectionOnDrag={isSelectMode}
        selectionMode={SelectionMode.Partial}
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
