import React, { useState } from 'react';
import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';

type CheckStatus = 'todo' | 'inprogress' | 'done' | 'na';

const STATUS_CONFIG: Record<CheckStatus, { label: string; color: string; bg: string; dot: string }> = {
  todo:       { label: '미착수', color: 'text-slate-400', bg: 'bg-slate-100',    dot: 'bg-slate-300' },
  inprogress: { label: '진행중', color: 'text-amber-600', bg: 'bg-amber-50',     dot: 'bg-amber-400 animate-pulse' },
  done:       { label: '완료',   color: 'text-emerald-600', bg: 'bg-emerald-50', dot: 'bg-emerald-500' },
  na:         { label: 'N/A',   color: 'text-slate-300', bg: 'bg-slate-50',     dot: 'bg-slate-200' },
};

export default function ChecklistItemNode({ data }: NodeProps<NodeData>) {
  const [status, setStatus] = useState<CheckStatus>((data.status as CheckStatus) ?? 'todo');

  const cfg = STATUS_CONFIG[status];
  const cycleStatus = () => {
    const order: CheckStatus[] = ['todo', 'inprogress', 'done', 'na'];
    const next = order[(order.indexOf(status) + 1) % order.length];
    setStatus(next);
  };

  return (
    <div
      className={`nodrag group relative flex flex-col gap-1.5 p-3 rounded-lg border
                  shadow-sm hover:shadow-md transition-all duration-150 select-none
                  ${cfg.bg} w-[160px] min-h-[80px]`}
      style={{ borderColor: status === 'done' ? '#6ee7b7' : status === 'inprogress' ? '#fcd34d' : '#e2e8f0' }}
    >
      {/* 상단: 상태 뱃지 + 완료 체크 */}
      <div className="flex items-center justify-between gap-1">
        <button
          onClick={cycleStatus}
          className={`flex items-center gap-1 text-[10px] font-semibold px-1.5 py-0.5 rounded-full
                      border transition-colors cursor-pointer
                      ${cfg.color} ${cfg.bg}`}
          style={{ borderColor: 'currentColor', opacity: 0.9 }}
          title="클릭하여 상태 변경"
        >
          <span className={`w-1.5 h-1.5 rounded-full inline-block ${cfg.dot}`} />
          {cfg.label}
        </button>

        {status === 'done' && (
          <svg className="w-4 h-4 text-emerald-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        )}
      </div>

      {/* 제목 */}
      <div className="text-xs font-semibold text-slate-700 leading-snug">
        {data.label as string}
      </div>

      {/* 담당 */}
      {data.department && (
        <div className="flex items-center gap-1 mt-auto">
          <span className="text-[10px] text-slate-400">👤</span>
          <span className="text-[10px] text-slate-400 truncate">{data.department as string}</span>
        </div>
      )}

      {/* 상태=done 일 때 상단 완료 라인 */}
      {status === 'done' && (
        <div className="absolute top-0 left-0 right-0 h-0.5 bg-emerald-400 rounded-t-lg" />
      )}
    </div>
  );
}
