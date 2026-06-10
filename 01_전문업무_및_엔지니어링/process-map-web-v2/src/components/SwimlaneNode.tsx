import React, { useCallback } from 'react';
import type { NodeProps } from 'reactflow';
import { useReactFlow } from 'reactflow';
import useStore from '../store/useStore';
import type { NodeData } from '../store/useStore';

export default function SwimlaneNode({ id, data, selected }: NodeProps<NodeData>) {
  const { getZoom } = useReactFlow();

  // ── 왼쪽 레이블 클릭 → 선택 ──────────────────────────
  const handleLabelClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    const { nodes, setNodesAndEdges, edges } = useStore.getState();
    const updated = nodes.map(n => ({
      ...n,
      selected: n.id === id ? true : (e.ctrlKey || e.shiftKey ? n.selected : false),
    }));
    setNodesAndEdges(updated, edges);
  };

  // ── 커스텀 리사이즈 핸들 ─────────────────────────────
  const startResize = useCallback(
    (e: React.MouseEvent, dir: 'right' | 'bottom' | 'corner') => {
      e.preventDefault();
      e.stopPropagation();

      const zoom = getZoom();
      useStore.getState().takeSnapshot();

      // 드래그 시작 시점의 상태를 모두 스냅샷
      const { nodes: snap } = useStore.getState();
      const node = snap.find(n => n.id === id);
      if (!node) return;

      const origW = (node.style?.width  as number) ?? 2500;
      const origH = (node.style?.height as number) ?? 300;
      const origBottom = node.position.y + origH;
      const startX = e.clientX;
      const startY = e.clientY;

      const onMove = (ev: MouseEvent) => {
        // 스크린 픽셀 → 캔버스 단위 변환
        const dx = (ev.clientX - startX) / zoom;
        const dy = (ev.clientY - startY) / zoom;

        const newW = Math.max(800,  origW + (dir !== 'bottom' ? dx : 0));
        const newH = Math.max(80,   origH + (dir !== 'right'  ? dy : 0));

        const { edges, setNodesAndEdges } = useStore.getState();

        // 드래그 시작 시점의 스냅샷(snap)을 기준으로 계산 → 누적 오차 없음
        const next = snap.map(n => {
          if (n.id === id) {
            return { ...n, style: { ...n.style, width: newW, height: newH } };
          }
          // 모든 스윔레인 가로폭 동기화
          if (n.type === 'swimlane') {
            return { ...n, style: { ...n.style, width: newW } };
          }
          // 세로 리사이즈: 현재 스윔레인 하단보다 아래에 있는 노드 밀기
          if (dir !== 'right' && n.type !== 'verticalLine' && n.position.y >= origBottom - 2) {
            return { ...n, position: { ...n.position, y: n.position.y + dy } };
          }
          // 수직선 높이 확장
          if (dir !== 'right' && n.type === 'verticalLine') {
            return { ...n, data: { ...n.data, height: ((n.data.height as number) ?? 2650) + dy } };
          }
          return n;
        });

        setNodesAndEdges(next, edges);
      };

      const onUp = () => {
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup',  onUp);
      };

      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup',  onUp);
    },
    [id, getZoom]
  );

  return (
    <div className="relative w-full h-full" style={{ pointerEvents: 'none' }}>

      {/* 배경 */}
      <div
        className={`absolute inset-0 bg-slate-50/60 ${
          selected ? 'ring-2 ring-inset ring-blue-400 bg-blue-50/20' : ''
        }`}
      />

      {/* ── 왼쪽 레이블 바 ── */}
      <div
        onClick={handleLabelClick}
        onMouseDown={e => e.stopPropagation()}
        style={{ pointerEvents: 'auto' }}
        className="absolute left-0 top-0 bottom-0 w-16 bg-slate-200 border-r border-slate-300
                   flex items-center justify-center cursor-pointer
                   hover:bg-slate-300/80 transition-colors z-10 select-none"
      >
        <span className="transform -rotate-90 text-lg font-bold text-slate-600 tracking-widest whitespace-nowrap">
          {data.label}
        </span>
      </div>

      {/* ── 오른쪽 경계 (가로 리사이즈) ── */}
      <div
        onMouseDown={e => startResize(e, 'right')}
        style={{ pointerEvents: 'auto' }}
        title="드래그하여 너비 조절"
        className="absolute top-0 bottom-0 right-0 w-2 z-20 cursor-ew-resize
                   hover:bg-blue-500/40 transition-colors"
      />

      {/* ── 아래쪽 경계 (세로 리사이즈) ── */}
      <div
        onMouseDown={e => startResize(e, 'bottom')}
        style={{ pointerEvents: 'auto' }}
        title="드래그하여 높이 조절"
        className="absolute left-0 right-0 bottom-0 h-2 z-20 cursor-ns-resize
                   hover:bg-blue-500/40 transition-colors"
      />

      {/* ── 우하단 코너 ── */}
      <div
        onMouseDown={e => startResize(e, 'corner')}
        style={{ pointerEvents: 'auto' }}
        title="드래그하여 크기 조절"
        className="absolute bottom-0 right-0 w-5 h-5 z-30 cursor-nwse-resize group"
      >
        <div
          className="absolute bottom-0.5 right-0.5 w-3.5 h-3.5 rounded-full
                     bg-blue-500 border-2 border-white shadow-md
                     opacity-0 group-hover:opacity-100 transition-opacity duration-150"
        />
      </div>

    </div>
  );
}
