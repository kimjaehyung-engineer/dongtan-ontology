import React, { useCallback, useRef } from 'react';
import type { NodeProps } from 'reactflow';
import { useReactFlow } from 'reactflow';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';
import { v4 as uuidv4 } from 'uuid';

export default function VerticalLineNode({ id, data, selected }: NodeProps<NodeData & { height?: number }>) {
  const { addNode, nodes, updateNodeData } = useStore();
  const { getZoom } = useReactFlow();
  const isResizing = useRef(false);
  const height = data?.height ?? 1700;

  // Ctrl+클릭 복제
  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.ctrlKey && e.button === 0) { // Left click + Ctrl
      e.stopPropagation();
      e.preventDefault();
      const currentNode = nodes.find(n => n.id === id);
      if (currentNode) {
        addNode({
          ...currentNode,
          id: uuidv4(),
          position: { x: currentNode.position.x + 100, y: currentNode.position.y },
          selected: true
        });
      }
    }
  };

  // 하단 드래그 높이(길이) 조절
  const startResize = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault();
      e.stopPropagation();

      if (isResizing.current) return;
      isResizing.current = true;

      const zoom = getZoom();
      useStore.getState().takeSnapshot(); // 스냅샷 백업

      const { nodes: snap } = useStore.getState();
      const node = snap.find(n => n.id === id);
      if (!node) {
        isResizing.current = false;
        return;
      }

      const origH = (node.data?.height as number) ?? 1700;
      const startY = e.clientY;

      const onMove = (ev: MouseEvent) => {
        const dy = (ev.clientY - startY) / zoom;
        const newH = Math.max(100, origH + dy);
        updateNodeData(id, { height: newH });
      };

      const onUp = () => {
        isResizing.current = false;
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup', onUp);
      };

      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup', onUp);
    },
    [id, getZoom, updateNodeData]
  );

  // 상단 드래그 높이(길이) 조절
  const startResizeTop = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault();
      e.stopPropagation();

      if (isResizing.current) return;
      isResizing.current = true;

      const zoom = getZoom();
      useStore.getState().takeSnapshot(); // 스냅샷 백업

      const { nodes: snap } = useStore.getState();
      const node = snap.find(n => n.id === id);
      if (!node) {
        isResizing.current = false;
        return;
      }

      const origH = (node.data?.height as number) ?? 1700;
      const origY = node.position.y;
      const startY = e.clientY;

      const onMove = (ev: MouseEvent) => {
        const dy = (ev.clientY - startY) / zoom;
        const maxDy = origH - 100; // 최소 높이 100 제한을 위한 최대 이동 거리
        const constrainedDy = Math.min(maxDy, dy);

        const newH = origH - constrainedDy;
        const newY = origY + constrainedDy;

        // 노드의 Y 위치와 높이 데이터를 연계하여 업데이트
        const nextNodes = useStore.getState().nodes.map((n) => {
          if (n.id === id) {
            return {
              ...n,
              position: { ...n.position, y: newY },
              data: { ...n.data, height: newH },
            };
          }
          return n;
        });

        useStore.getState().setNodesAndEdges(nextNodes, useStore.getState().edges);
      };

      const onUp = () => {
        isResizing.current = false;
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup', onUp);
      };

      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup', onUp);
    },
    [id, getZoom]
  );

  return (
    <div
      className={`vertical-line-container group flex justify-center relative ${selected ? 'selected-active' : ''}`}
      style={{ width: 24, height: height, marginTop: 0 }}
      onMouseDown={handleMouseDown}
    >
      <style>{`
        .vertical-line-container {
          cursor: grab;
        }
        .vertical-line-container:active {
          cursor: grabbing;
        }
        .vertical-line-container .vertical-line-inner {
          width: 0px;
          height: 100%;
          border-left: 2px dashed #94a3b8;
          transition: border-color 0.15s ease;
        }
        .vertical-line-container:hover .vertical-line-inner,
        .vertical-line-container.selected-active .vertical-line-inner {
          border-left: 2px solid #3b82f6;
        }
        /* 리사이즈 핸들 버튼 스타일 */
        .vertical-line-resize-handle,
        .vertical-line-resize-handle-top {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: #3b82f6;
          border: 2px solid white;
          box-shadow: 0 1px 3px rgba(0,0,0,0.3);
          cursor: ns-resize;
          position: absolute;
          left: 50%;
          transform: translateX(-50%);
          z-index: 50;
          opacity: 0;
          transition: opacity 0.15s ease;
        }
        .vertical-line-resize-handle {
          bottom: -5px;
        }
        .vertical-line-resize-handle-top {
          top: -5px;
        }
        .vertical-line-container:hover .vertical-line-resize-handle,
        .vertical-line-container.selected-active .vertical-line-resize-handle,
        .vertical-line-container:hover .vertical-line-resize-handle-top,
        .vertical-line-container.selected-active .vertical-line-resize-handle-top {
          opacity: 1;
        }
      `}</style>
      <div className="vertical-line-inner pointer-events-none" />
      
      {/* 상단 드래그 길이 조절용 그립 */}
      <div
        className="vertical-line-resize-handle-top nodrag"
        onMouseDown={startResizeTop}
      />

      {/* 하단 드래그 길이 조절용 그립 */}
      <div
        className="vertical-line-resize-handle nodrag"
        onMouseDown={startResize}
      />
    </div>
  );
}
