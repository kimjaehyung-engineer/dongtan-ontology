import React, { useCallback, useRef } from 'react';
import type { NodeProps } from 'reactflow';
import { useReactFlow } from 'reactflow';
import useStore from '../store/useStore';
import type { NodeData } from '../store/useStore';

// 행 유형별 스타일 설정
const LANE_STYLES: Record<string, {
  bgClass: string;
  labelBg: string;
  labelText: string;
  border: string;
  accentColor: string;
  accent: boolean;
}> = {
  '마일스톤': {
    bgClass: 'bg-amber-50',
    labelBg: 'bg-amber-600',
    labelText: 'text-white',
    border: 'border-amber-300',
    accentColor: 'bg-amber-400',
    accent: true,
  },
  '체크리스트': {
    bgClass: 'bg-indigo-50',
    labelBg: 'bg-indigo-600',
    labelText: 'text-white',
    border: 'border-indigo-300',
    accentColor: 'bg-indigo-400',
    accent: true,
  },
};

const DEFAULT_STYLE = {
  bgClass: 'bg-slate-50/60',
  labelBg: 'bg-slate-200',
  labelText: 'text-slate-600',
  border: 'border-slate-300',
  accentColor: 'bg-slate-400',
  accent: false,
};

export default function SwimlaneNode({ id, data, selected }: NodeProps<NodeData>) {
  const { getZoom } = useReactFlow();
  const isResizing = useRef(false);
  const label = data.label as string;
  const style = LANE_STYLES[label] ?? DEFAULT_STYLE;

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

      const origW  = (node.style?.width  as number) ?? 2500;
      const origH  = (node.style?.height as number) ?? 300;
      const startX = e.clientX;
      const startY = e.clientY;

      const onMove = (ev: MouseEvent) => {
        const dx = (ev.clientX - startX) / zoom;
        const dy = (ev.clientY - startY) / zoom;
        const newW = Math.max(800, origW + (dir !== 'bottom' ? dx : 0));
        const newH = Math.max(80,  origH + (dir !== 'right'  ? dy : 0));

        const { edges, setNodesAndEdges } = useStore.getState();
        const next = snap.map(n =>
          n.id === id ? { ...n, style: { ...n.style, width: newW, height: newH } } : n
        );
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

  const accentRing = selected ? 'ring-2 ring-inset ring-blue-400' : '';

  return (
    <div className="relative w-full h-full overflow-visible">

      {/* ── 배경 ── */}
      <div
        className={`nodrag absolute inset-0 ${style.bgClass} ${accentRing}`}
      />

      {/* 마일스톤/체크리스트 전용: 상단 강조 라인 */}
      {style.accent && (
        <div className={`absolute top-0 left-0 right-0 h-1 ${style.accentColor} opacity-60`} />
      )}

      {/* ── 왼쪽 레이블 바 ── */}
      <div
        onClick={handleLabelClick}
        className={`nodrag absolute left-0 top-0 bottom-0 w-16 ${style.labelBg}
                   border-r ${style.border}
                   flex items-center justify-center cursor-pointer select-none
                   transition-colors z-10`}
      >
        {/* accent 행: 왼쪽 세로 강조선 */}
        {style.accent && (
          <div className={`absolute left-0 top-0 bottom-0 w-1 ${style.accentColor} opacity-80 rounded-r-sm`} />
        )}
        <span className={`transform -rotate-90 text-sm font-bold ${style.labelText} tracking-widest whitespace-nowrap uppercase`}>
          {label}
        </span>
      </div>

      {/* ── 오른쪽 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'right')}
        className="nodrag absolute top-0 bottom-0 right-0 z-20 flex items-center justify-end"
        style={{ width: 16, cursor: 'ew-resize' }}
      >
        <div className="flex flex-col gap-1 mr-1 opacity-20 hover:opacity-70 transition-opacity pointer-events-none">
          <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
          <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
          <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
        </div>
      </div>

      {/* ── 아래쪽 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'bottom')}
        className="nodrag absolute left-0 right-0 bottom-0 z-20 flex flex-col items-center justify-end"
        style={{ height: 16, cursor: 'ns-resize' }}
      >
        <div className="flex flex-row gap-1 mb-1 opacity-20 hover:opacity-70 transition-opacity pointer-events-none">
          <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
          <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
          <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
        </div>
      </div>

      {/* ── 우하단 코너 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'corner')}
        className="nodrag absolute bottom-0 right-0 z-30 flex items-center justify-center group"
        style={{ width: 20, height: 20, cursor: 'nwse-resize' }}
      >
        <div className="w-3 h-3 rounded-full bg-slate-400 border-2 border-white shadow
                        opacity-0 group-hover:opacity-80 transition-opacity duration-150" />
      </div>

    </div>
  );
}
