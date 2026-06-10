import React, { useCallback, useRef } from 'react';
import type { NodeProps } from 'reactflow';
import { useReactFlow } from 'reactflow';
import useStore from '../store/useStore';
import type { NodeData } from '../store/useStore';

export default function SwimlaneNode({ id, data, selected }: NodeProps<NodeData>) {
  const { getZoom } = useReactFlow();
  const isResizing = useRef(false);

  // ── 왼쪽 레이블 클릭 → 선택 ──────────────────────
  const handleLabelClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  // ── 커스텀 리사이즈 드래그 ────────────────────────
  const startResize = useCallback(
    (e: React.MouseEvent, dir: 'right' | 'bottom' | 'corner') => {
      e.preventDefault();
      e.stopPropagation();

      if (isResizing.current) return;
      isResizing.current = true;

      const zoom = getZoom();
      useStore.getState().takeSnapshot();

      const { nodes: snap } = useStore.getState();
      const node = snap.find(n => n.id === id);
      if (!node) { isResizing.current = false; return; }

      const origW      = (node.style?.width  as number) ?? 2500;
      const origH      = (node.style?.height as number) ?? 300;
      const origBottom = node.position.y + origH;
      const startX     = e.clientX;
      const startY     = e.clientY;

      const onMove = (ev: MouseEvent) => {
        const dx = (ev.clientX - startX) / zoom;
        const dy = (ev.clientY - startY) / zoom;

        const newW = Math.max(800, origW + (dir !== 'bottom' ? dx : 0));
        const newH = Math.max(80,  origH + (dir !== 'right'  ? dy : 0));

        const { edges, setNodesAndEdges } = useStore.getState();

        const next = snap.map(n => {
          // 현재 스윔레인 크기만 변경 (다른 노드는 건드리지 않음)
          if (n.id === id) {
            return { ...n, style: { ...n.style, width: newW, height: newH } };
          }
          return n;
        });

        setNodesAndEdges(next, edges);
      };

      const onUp = () => {
        isResizing.current = false;
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup',   onUp);
      };

      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup',   onUp);
    },
    [id, getZoom]
  );

  return (
    <div className="relative w-full h-full overflow-visible">

      {/* ── 배경 (nodrag: 이 영역을 클릭해도 노드를 드래그하지 않음) ── */}
      <div
        className={`nodrag absolute inset-0 bg-slate-50/60 ${
          selected ? 'ring-2 ring-inset ring-blue-400 bg-blue-50/20' : ''
        }`}
      />

      {/* ── 왼쪽 레이블 바 ── */}
      <div
        onClick={handleLabelClick}
        className="nodrag absolute left-0 top-0 bottom-0 w-16 bg-slate-200 border-r border-slate-300
                   flex items-center justify-center cursor-pointer select-none
                   hover:bg-slate-300/80 transition-colors z-10"
      >
        <span className="transform -rotate-90 text-lg font-bold text-slate-600 tracking-widest whitespace-nowrap">
          {data.label}
        </span>
      </div>

      {/* ── 오른쪽 리사이즈 핸들 (visible stripe) ── */}
      <div
        onMouseDown={e => startResize(e, 'right')}
        className="nodrag absolute top-0 bottom-0 right-0 z-20 flex items-center justify-end"
        style={{ width: 16, cursor: 'ew-resize' }}
      >
        {/* 핸들 시각화: 세로 점 3개 */}
        <div className="flex flex-col gap-1 mr-1 opacity-30 hover:opacity-90 transition-opacity pointer-events-none">
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
        </div>
      </div>

      {/* ── 아래쪽 리사이즈 핸들 (visible stripe) ── */}
      <div
        onMouseDown={e => startResize(e, 'bottom')}
        className="nodrag absolute left-0 right-0 bottom-0 z-20 flex flex-col items-center justify-end"
        style={{ height: 16, cursor: 'ns-resize' }}
      >
        {/* 핸들 시각화: 가로 점 3개 */}
        <div className="flex flex-row gap-1 mb-1 opacity-30 hover:opacity-90 transition-opacity pointer-events-none">
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
        </div>
      </div>

      {/* ── 우하단 코너 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'corner')}
        className="nodrag absolute bottom-0 right-0 z-30 flex items-center justify-center"
        style={{ width: 20, height: 20, cursor: 'nwse-resize' }}
      >
        <div className="w-3 h-3 rounded-full bg-blue-500 border-2 border-white shadow-md
                        opacity-40 hover:opacity-100 transition-opacity duration-150" />
      </div>

    </div>
  );
}
