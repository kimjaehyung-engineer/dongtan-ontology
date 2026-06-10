import React, { useCallback, useRef } from 'react';
import type { NodeProps } from 'reactflow';
import useStore from '../store/useStore';
import type { NodeData } from '../store/useStore';

export default function SwimlaneNode({ id, data, selected }: NodeProps<NodeData>) {
  const isResizingRef = useRef<null | 'right' | 'bottom' | 'corner'>(null);
  const startInfoRef = useRef({ mouseX: 0, mouseY: 0, width: 0, height: 0 });

  // ──────────────────────────────────────────
  // 왼쪽 레이블 바 클릭 → 스윔레인 선택
  // ──────────────────────────────────────────
  const handleLabelClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    const { nodes, setNodesAndEdges, edges } = useStore.getState();
    const updated = nodes.map(n => ({
      ...n,
      selected: n.id === id ? true : (e.ctrlKey || e.shiftKey ? n.selected : false)
    }));
    setNodesAndEdges(updated, edges);
  };

  // ──────────────────────────────────────────
  // 리사이즈 드래그 핸들러 (우측 / 하단 / 코너)
  // ──────────────────────────────────────────
  const startResize = useCallback((
    e: React.MouseEvent,
    dir: 'right' | 'bottom' | 'corner'
  ) => {
    e.preventDefault();
    e.stopPropagation();

    useStore.getState().takeSnapshot();

    const { nodes } = useStore.getState();
    const node = nodes.find(n => n.id === id);
    if (!node) return;

    const w = (node.style?.width as number) || 2500;
    const h = (node.style?.height as number) || 300;

    isResizingRef.current = dir;
    startInfoRef.current = {
      mouseX: e.clientX,
      mouseY: e.clientY,
      width: w,
      height: h,
    };

    const onMouseMove = (ev: MouseEvent) => {
      const dx = ev.clientX - startInfoRef.current.mouseX;
      const dy = ev.clientY - startInfoRef.current.mouseY;

      const newWidth = Math.max(800, startInfoRef.current.width + (dir !== 'bottom' ? dx : 0));
      const newHeight = Math.max(80, startInfoRef.current.height + (dir !== 'right' ? dy : 0));
      const deltaH = newHeight - startInfoRef.current.height;

      const { nodes: curNodes, edges, setNodesAndEdges } = useStore.getState();
      const thisNode = curNodes.find(n => n.id === id);
      if (!thisNode) return;
      const nodeBottom = thisNode.position.y + (thisNode.style?.height as number || 300);

      const nextNodes = curNodes.map(n => {
        if (n.id === id) {
          return { ...n, style: { ...n.style, width: newWidth, height: newHeight } };
        }
        // 다른 스윔레인 가로폭 동기화
        if (n.type === 'swimlane') {
          return { ...n, style: { ...n.style, width: newWidth } };
        }
        // 현재 스윔레인 아래에 있는 모든 노드를 deltaH 만큼 이동
        if (dir !== 'right' && deltaH !== 0 && n.type !== 'verticalLine' && n.position.y >= nodeBottom - 2) {
          const originalStartH = startInfoRef.current.height;
          const dynamicBottom = thisNode.position.y + originalStartH;
          if (n.position.y >= dynamicBottom - 2) {
            return { ...n, position: { ...n.position, y: n.position.y + dy } };
          }
        }
        // 수직 타임라인 선 높이 확장
        if (dir !== 'right' && n.type === 'verticalLine' && deltaH !== 0) {
          const curH = (n.data.height as number) || 2650;
          return { ...n, data: { ...n.data, height: curH + dy } };
        }
        return n;
      });

      setNodesAndEdges(nextNodes, edges);

      // 다음 move 의 기준점을 계속 업데이트
      startInfoRef.current.mouseX = ev.clientX;
      startInfoRef.current.mouseY = ev.clientY;
      startInfoRef.current.width = newWidth;
      startInfoRef.current.height = newHeight;
    };

    const onMouseUp = () => {
      isResizingRef.current = null;
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  }, [id]);

  return (
    <div
      className="relative w-full h-full"
      style={{ pointerEvents: 'none' }}
    >
      {/* ── 배경 ── */}
      <div
        className={`absolute inset-0 bg-gray-50/50 ${selected ? 'ring-2 ring-blue-400 bg-blue-50/10' : ''}`}
      />

      {/* ── 왼쪽 레이블 바 ── */}
      <div
        onMouseDown={e => e.stopPropagation()}
        onClick={handleLabelClick}
        style={{ pointerEvents: 'auto' }}
        className="absolute left-0 top-0 bottom-0 w-16 bg-slate-200 border-r border-slate-300
                   flex items-center justify-center cursor-pointer hover:bg-slate-300/80 transition-colors z-10"
      >
        <span className="transform -rotate-90 text-lg font-bold text-slate-600 tracking-widest whitespace-nowrap select-none">
          {data.label}
        </span>
      </div>

      {/* ── 오른쪽 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'right')}
        style={{ pointerEvents: 'auto' }}
        className="absolute top-0 bottom-0 right-0 w-2 cursor-ew-resize
                   hover:bg-blue-400/40 transition-colors z-20"
        title="좌우 크기 조절"
      />

      {/* ── 아래쪽 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'bottom')}
        style={{ pointerEvents: 'auto' }}
        className="absolute left-0 right-0 bottom-0 h-2 cursor-ns-resize
                   hover:bg-blue-400/40 transition-colors z-20"
        title="상하 크기 조절"
      />

      {/* ── 우하단 코너 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'corner')}
        style={{ pointerEvents: 'auto' }}
        className="absolute bottom-0 right-0 w-4 h-4 cursor-nwse-resize z-30
                   flex items-center justify-center group"
        title="대각선 크기 조절"
      >
        <div className="w-3 h-3 rounded-full bg-blue-400 opacity-0 group-hover:opacity-100
                        transition-all duration-150 shadow-md" />
      </div>
    </div>
  );
}
