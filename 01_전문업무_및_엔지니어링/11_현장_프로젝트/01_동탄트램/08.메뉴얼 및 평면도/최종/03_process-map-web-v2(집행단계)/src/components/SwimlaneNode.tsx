import React, { useCallback, useRef, useState } from 'react';
import type { NodeProps } from 'reactflow';
import { useReactFlow } from 'reactflow';
import useStore from '../store/useStore';
import type { NodeData } from '../store/useStore';

export default function SwimlaneNode({ id, data, selected }: NodeProps<NodeData>) {
  const { getZoom } = useReactFlow();
  const isDarkMode = useStore(state => state.isDarkMode);
  const renameSwimlaneRow = useStore(state => state.renameSwimlaneRow);
  const isResizing = useRef(false);
  const label = (data.label as string) || '';
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(label);

  // ── 🎨 세련된 회색(그레이) 세로축 배경 & 초고대비 찐한 검정색 타이플 ──────────
  let headerStyle = {
    accentLine: 'bg-indigo-600',
    rowBgLight: 'bg-slate-50/70 border-slate-200/90',
    rowBgDark: 'bg-slate-900/70 border-slate-800/90',
    titleWords: ['공무'],
  };

  if (label.includes('공사') || label.includes('시공')) {
    headerStyle = {
      accentLine: 'bg-emerald-600',
      rowBgLight: 'bg-slate-100/50 border-slate-200/90',
      rowBgDark: 'bg-slate-900/80 border-slate-800/90',
      titleWords: ['공사'],
    };
  } else if (label.includes('품질')) {
    headerStyle = {
      accentLine: 'bg-amber-600',
      rowBgLight: 'bg-slate-50/70 border-slate-200/90',
      rowBgDark: 'bg-slate-900/70 border-slate-800/90',
      titleWords: ['품질'],
    };
  } else if (label.includes('안전')) {
    headerStyle = {
      accentLine: 'bg-rose-600',
      rowBgLight: 'bg-slate-100/50 border-slate-200/90',
      rowBgDark: 'bg-slate-900/80 border-slate-800/90',
      titleWords: ['안전'],
    };
  } else if (label.includes('관리') || label.includes('용지') || label.includes('총무')) {
    headerStyle = {
      accentLine: 'bg-purple-600',
      rowBgLight: 'bg-slate-50/70 border-slate-200/90',
      rowBgDark: 'bg-slate-900/70 border-slate-800/90',
      titleWords: ['관리'],
    };
  } else if (label.includes('본사')) {
    headerStyle = {
      accentLine: 'bg-slate-700',
      rowBgLight: 'bg-slate-100/50 border-slate-200/90',
      rowBgDark: 'bg-slate-900/80 border-slate-800/90',
      titleWords: ['본사'],
    };
  } else {
    // 사용자 지정 새 행 등
    const shortLabel = label.replace(/[🏢🏗️🛡️🚨💼🏛️📋]/g, '').trim().split(/[\s\/]+/)[0] || '새행';
    headerStyle = {
      accentLine: 'bg-teal-600',
      rowBgLight: 'bg-slate-50/70 border-slate-200/90',
      rowBgDark: 'bg-slate-900/70 border-slate-800/90',
      titleWords: [shortLabel],
    };
  }

  const bgClass = isDarkMode ? headerStyle.rowBgDark : headerStyle.rowBgLight;

  // ── 더블클릭 이름 변경 ────────────────────────
  const handleDoubleClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    setEditValue(label);
    setIsEditing(true);
  }, [label]);

  const handleRenameSubmit = useCallback(() => {
    const trimmed = editValue.trim();
    if (trimmed && trimmed !== label) {
      renameSwimlaneRow(id, trimmed);
    }
    setIsEditing(false);
  }, [editValue, label, id, renameSwimlaneRow]);



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
        const deltaH = newH - origH;

        const { edges, setNodesAndEdges } = useStore.getState();
        const next = snap.map(n => {
          if (n.id === id) {
            return {
              ...n,
              style: { ...n.style, width: newW, height: newH }
            };
          }

          if (n.type === 'swimlane') {
            const currentW = (n.style?.width as number) ?? 2500;
            const targetW = dir !== 'bottom' ? newW : currentW;
            const origY = n.position.y;
            const targetY = (dir !== 'right' && origY >= node.position.y + origH - 5)
              ? origY + deltaH
              : origY;

            return {
              ...n,
              position: { ...n.position, y: targetY },
              style: { ...n.style, width: targetW }
            };
          }

          if (n.type === 'verticalLine') {
            const currentHeight = (n.data?.height as number) ?? 1700;
            const targetHeight = dir !== 'right' ? Math.max(500, currentHeight + deltaH) : currentHeight;
            return {
              ...n,
              data: { ...n.data, height: targetHeight }
            };
          }

          const origY = n.position.y;
          if (dir !== 'right' && origY >= node.position.y + origH - 5) {
            return {
              ...n,
              position: { ...n.position, y: origY + deltaH }
            };
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

  const accentRing = selected ? 'ring-4 ring-inset ring-blue-500' : '';

  return (
    <div className="relative w-full h-full overflow-visible">
      {/* ── 행 배경 ── */}
      <div className={`nodrag absolute inset-0 ${bgClass} ${accentRing} transition-colors border-b-2`} />

      {/* ── 🌟 [세련된 회색 세로축 헤더 & 찐한 검정색 타이포그래피] ── */}
      <div
        className={`nodrag absolute left-0 top-0 bottom-0 w-60 bg-slate-200/90 dark:bg-slate-800 border-r-4 border-slate-400 dark:border-slate-700 select-none flex flex-col items-center justify-center p-3 transition-all z-20 shadow-md`}
        onDoubleClick={handleDoubleClick}
      >
        {/* 순백색 카드 뱃지 프레임 */}
        <div className="relative flex flex-col items-center justify-center text-center gap-2 w-full my-auto bg-white border-2 border-slate-300 shadow-md px-4 py-6 rounded-2xl">
          {isEditing ? (
            <input
              autoFocus
              className="text-lg font-black text-slate-950 text-center bg-blue-50 border-2 border-blue-400 rounded-lg px-2 py-1 w-full outline-none"
              value={editValue}
              onChange={e => setEditValue(e.target.value)}
              onBlur={handleRenameSubmit}
              onKeyDown={e => {
                if (e.key === 'Enter') handleRenameSubmit();
                if (e.key === 'Escape') setIsEditing(false);
              }}
            />
          ) : (
            <div className="flex flex-col items-center justify-center gap-1.5 w-full">
              {/* 메인 부서명 (아이콘 + 부서명) */}
              <div className="text-xl sm:text-2xl md:text-[21px] font-black text-slate-950 dark:text-slate-950 tracking-tight leading-snug">
                {(() => {
                  const parts = label.split('/');
                  return parts[0]?.trim() || label;
                })()}
              </div>
              {/* 상세 세부 업무 영역 (계약/인허가, 현장 시공 등) */}
              {label.includes('/') && (
                <div className="text-xs sm:text-[12.5px] font-extrabold text-slate-700 bg-slate-100/90 px-2.5 py-1 rounded-md border border-slate-200 shadow-2xs whitespace-nowrap">
                  {label.split('/').slice(1).join('/').trim()}
                </div>
              )}
            </div>
          )}
        </div>


      </div>

      {/* ── 오른쪽 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'right')}
        className="nodrag absolute top-0 bottom-0 right-0 z-20 flex items-center justify-end"
        style={{ width: 16, cursor: 'ew-resize' }}
      >
        <div className="flex flex-col gap-1 mr-1 opacity-30 hover:opacity-100 transition-opacity pointer-events-none">
          <div className="w-2 h-2 rounded-full bg-slate-400" />
          <div className="w-2 h-2 rounded-full bg-slate-400" />
          <div className="w-2 h-2 rounded-full bg-slate-400" />
        </div>
      </div>

      {/* ── 아래쪽 리사이즈 핸들 ── */}
      <div
        onMouseDown={e => startResize(e, 'bottom')}
        className="nodrag absolute left-0 right-0 bottom-0 z-20 flex flex-col items-center justify-end"
        style={{ height: 16, cursor: 'ns-resize' }}
      >
        <div className="flex flex-row gap-1 mb-1 opacity-30 hover:opacity-100 transition-opacity pointer-events-none">
          <div className="w-2 h-2 rounded-full bg-slate-400" />
          <div className="w-2 h-2 rounded-full bg-slate-400" />
          <div className="w-2 h-2 rounded-full bg-slate-400" />
        </div>
      </div>
    </div>
  );
}
