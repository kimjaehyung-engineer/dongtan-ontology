import React from 'react';
import { SpanDailyState, AlternativeSpanScheduleResult } from '../../engine/structureScheduleEngine';
import { Layers, AlertTriangle, CheckCircle2, Clock } from 'lucide-react';

interface LongitudinalSpanViewerProps {
  schedule: AlternativeSpanScheduleResult;
  dailyStates: SpanDailyState[];
  currentDay: number;
  selectedSpanIdx: number;
  onSelectSpan: (spanIdx: number) => void;
}

export const LongitudinalSpanViewer: React.FC<LongitudinalSpanViewerProps> = ({
  schedule,
  dailyStates,
  currentDay,
  selectedSpanIdx,
  onSelectSpan
}) => {
  const isAnchor = schedule.altType === 'ALL_ANCHOR';
  const numStories = schedule.numStories || 2;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 text-blue-600">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-800 flex items-center gap-2">
              <span>종방향 블록별 시공 진행도 [지하 {numStories}층 모델]</span>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono">
                총 {schedule.totalLengthM.toFixed(0)}m / {schedule.numSpans}개 스팬 (20m 단위)
              </span>
            </h3>
            <p className="text-[11px] text-slate-500">
              스팬을 클릭하면 아래 종단면도/평면도/횡단면도 및 상세 공정이 해당 스팬으로 동기화됩니다.
            </p>
          </div>
        </div>

        {/* 범례 */}
        <div className="flex items-center gap-3 text-[10px] text-slate-600 font-medium">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-slate-200 border border-slate-300"></span> 미착수
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-emerald-500 animate-pulse"></span> 시공/타설중
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-amber-400"></span> 14MPa 양생대기
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-slate-700"></span> 타설 완료
          </span>
        </div>
      </div>

      {/* 20m 스팬 블록 그리드 */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5">
        {dailyStates.map((state, idx) => {
          const isSelected = selectedSpanIdx === idx;
          const isCompleted = state.overallSpanProgress >= 100;
          const isActive = state.overallSpanProgress > 0 && state.overallSpanProgress < 100;

          return (
            <button
              key={idx}
              onClick={() => onSelectSpan(idx)}
              className={`text-left p-3 rounded-lg border transition-all relative overflow-hidden flex flex-col justify-between ${
                isSelected
                  ? 'border-blue-500 ring-2 ring-blue-200 bg-blue-50/40 shadow-sm'
                  : isCompleted
                  ? 'border-slate-300 bg-slate-50/80 hover:border-slate-400'
                  : isActive
                  ? 'border-emerald-400 bg-emerald-50/30 ring-1 ring-emerald-200'
                  : 'border-slate-200 bg-white hover:border-slate-300 opacity-70'
              }`}
            >
              {/* 상단 스팬 헤더 */}
              <div className="flex items-center justify-between w-full mb-1.5">
                <span className={`text-xs font-bold font-mono ${isSelected ? 'text-blue-700' : 'text-slate-700'}`}>
                  {state.spanName}
                </span>
                <span className="text-[10px] text-slate-500 font-mono">
                  {state.stationRange}
                </span>
              </div>

              {/* 스팬 내부 층별 부재 축조 미니 레이아웃 */}
              <div className="space-y-1 my-1 w-full text-[10px] font-sans">
                {/* 1. 최상부 슬래브 */}
                <div className="flex items-center justify-between px-1.5 py-0.5 rounded text-[9px] font-semibold border bg-white/70">
                  <span className="text-slate-600">지붕슬래브</span>
                  <span className={getStatusBadgeClass(state.topSlabStatus)}>
                    {getStatusText(state.topSlabStatus, state.topSlabProgress)}
                  </span>
                </div>

                {/* 2. 층별 외벽/중간슬래브 */}
                {state.storyStates && state.storyStates.slice().reverse().map((st, sIdx) => {
                  return (
                    <div key={`mini-story-${sIdx}`} className="flex items-center justify-between px-1.5 py-0.5 rounded text-[9px] font-semibold border bg-white/70">
                      <span className="text-slate-600 truncate max-w-[65px]">{st.storyName}</span>
                      <span className={getStatusBadgeClass(st.wallStatus)}>
                        {getStatusText(st.wallStatus, st.wallProgress)}
                      </span>
                    </div>
                  );
                })}

                {/* 3. 바닥 기초 */}
                <div className="flex items-center justify-between px-1.5 py-0.5 rounded text-[9px] font-semibold border bg-white/70">
                  <span className="text-slate-600">바닥기초</span>
                  <span className={getStatusBadgeClass(state.foundationStatus)}>
                    {getStatusText(state.foundationStatus, state.foundationProgress)}
                  </span>
                </div>
              </div>

              {/* 하단 진행률 바 & 상태 뱃지 */}
              <div className="mt-2 pt-1.5 border-t border-slate-100 w-full">
                <div className="flex items-center justify-between text-[10px] mb-1">
                  <span className="text-slate-500 font-medium truncate max-w-[90px]" title={state.currentActiveTaskName}>
                    {state.currentActiveTaskName}
                  </span>
                  <span className="font-mono font-bold text-slate-700">
                    {state.overallSpanProgress}%
                  </span>
                </div>
                <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                  <div 
                    className={`h-full transition-all duration-300 ${
                      state.overallSpanProgress === 100 
                        ? 'bg-slate-700' 
                        : state.isStrutInterfering 
                        ? 'bg-amber-500' 
                        : 'bg-emerald-500'
                    }`}
                    style={{ width: `${state.overallSpanProgress}%` }}
                  />
                </div>
              </div>

              {/* 간섭 경고 태그 */}
              {state.isStrutInterfering && (
                <div className="absolute top-1 right-1 flex items-center gap-0.5 px-1 py-0.2 text-[8px] bg-amber-500 text-white font-bold rounded shadow-xs animate-bounce">
                  <AlertTriangle className="w-2.5 h-2.5" />
                  <span>14MPa대기</span>
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'completed':
      return 'text-slate-800 bg-slate-200 px-1 rounded font-mono';
    case 'in_progress':
      return 'text-emerald-700 bg-emerald-100 px-1 rounded font-mono font-bold animate-pulse';
    case 'curing_waiting':
      return 'text-amber-800 bg-amber-100 px-1 rounded font-mono font-bold';
    default:
      return 'text-slate-400 font-mono';
  }
}

function getStatusText(status: string, progress: number): string {
  switch (status) {
    case 'completed':
      return '완료';
    case 'in_progress':
      return `${Math.round(progress * 100)}%`;
    case 'curing_waiting':
      return '양생중';
    default:
      return '대기';
  }
}
