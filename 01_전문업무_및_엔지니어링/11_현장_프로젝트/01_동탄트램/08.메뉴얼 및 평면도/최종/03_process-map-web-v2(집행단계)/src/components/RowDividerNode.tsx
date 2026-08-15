import React, { useCallback, useRef } from 'react';
import type { NodeProps } from 'reactflow';
import { useReactFlow } from 'reactflow';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';

export default function RowDividerNode({ id, data, selected }: NodeProps<NodeData & { width?: number }>) {
  const { updateNodeData } = useStore();
  const { getZoom } = useReactFlow();
  const isResizing = useRef(false);
  const width = data?.width ?? 4000;

  // 우측 드래그 가로 길이 조절
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

      const origW = (node.data?.width as number) ?? 4000;
      const startX = e.clientX;

      const onMove = (ev: MouseEvent) => {
        const dx = (ev.clientX - startX) / zoom;
        const newW = Math.max(200, origW + dx);
        updateNodeData(id, { width: newW });
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

  return (
    <div
      className={`group cursor-row-resize relative overflow-hidden ${selected ? 'selected-active' : ''}`}
      style={{ width: width, height: 16, marginLeft: 0 }}
    >
      <style>{`
        /* 행 구분선: 세로 구분선과 동일한 3px 찐하고 또렷한 실선 */
        .group .row-divider-inner {
          width: 100%;
          height: 3px;
          border-top: 3px solid #334155;
          transition: all 0.15s ease;
        }
        .group:hover .row-divider-inner,
        .group.selected-active .row-divider-inner {
          border-top: 3px solid #2563eb;
        }
        
        /* 리사이즈 핸들 버튼 스타일 */
        .row-divider-resize-handle {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: #3b82f6;
          border: 2px solid white;
          box-shadow: 0 1px 3px rgba(0,0,0,0.3);
          cursor: ew-resize;
          position: absolute;
          right: -5px;
          top: 0px;
          transform: translateY(-50%);
          z-index: 50;
          opacity: 0;
          transition: opacity 0.15s ease;
        }
        .group:hover .row-divider-resize-handle,
        .group.selected-active .row-divider-resize-handle {
          opacity: 1;
        }
      `}</style>
      
      <div className="row-divider-inner pointer-events-none absolute top-0 left-0 right-0" />

      {/* 우측 드래그 길이 조절용 그립 */}
      <div
        className="row-divider-resize-handle nodrag"
        onMouseDown={startResize}
      />
    </div>
  );
}
