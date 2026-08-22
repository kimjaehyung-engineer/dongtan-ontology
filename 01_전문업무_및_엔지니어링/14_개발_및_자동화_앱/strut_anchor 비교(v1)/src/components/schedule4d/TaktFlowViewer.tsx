import React from 'react';
import { AlternativeSpanScheduleResult, SpanTask } from '../../engine/structureScheduleEngine';
import { Layers, Activity, Hammer, Truck, Scissors } from 'lucide-react';

interface TaktFlowViewerProps {
  schedule: AlternativeSpanScheduleResult;
  allSchedules: AlternativeSpanScheduleResult[];
  currentDay: number;
  onDayChange: (day: number) => void;
  selectedSpanIdx: number;
  onSelectSpan: (idx: number) => void;
}

export const TaktFlowViewer: React.FC<TaktFlowViewerProps> = ({
  schedule,
  currentDay,
  onDayChange,
  selectedSpanIdx,
  onSelectSpan
}) => {
  const isAnchor = schedule.altType === 'ALL_ANCHOR';
  const totalDays = Math.max(60, schedule.totalDurationDays);
  const numSpans = schedule.numSpans;

  // SVG 좌표계
  const svgWidth = 960;
  const svgHeight = 440;
  const paddingLeft = 90;
  const paddingRight = 40;
  const paddingTop = 40;
  const paddingBottom = 50;

  const drawW = svgWidth - paddingLeft - paddingRight;
  const drawH = svgHeight - paddingTop - paddingBottom;

  const scaleX = drawW / totalDays;
  const scaleY = drawH / Math.max(1, numSpans);

  // 스팬별 태스크로부터 팀별 시계열 좌표 추출
  const getTeamPoints = (taskTypeMatcher: (t: SpanTask) => boolean) => {
    const points: { spanIdx: number; startDay: number; endDay: number; midDay: number }[] = [];
    for (let s = 0; s < numSpans; s++) {
      const match = schedule.tasks.find(t => t.spanIndex === s && taskTypeMatcher(t));
      if (match) {
        points.push({
          spanIdx: s,
          startDay: match.startDay,
          endDay: match.endDay,
          midDay: (match.startDay + match.endDay) / 2
        });
      }
    }
    return points;
  };

  const formworkPoints = getTeamPoints(t => t.type === 'foundation' || t.type === 'story_wall');
  const pouringPoints = getTeamPoints(t => t.type === 'top_slab' || t.type === 'mid_slab');
  const strutPoints = getTeamPoints(t => t.type === 'strut_release_curing');

  // 작업팀 가동률 & 대기 손실 계산
  const idleDays = schedule.bottleneckSummary.totalInterferenceLossDays;
  const utilizationRate = Math.max(50, Math.round(100 - (idleDays / totalDays) * 60));

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-4 font-sans">
      {/* 1. 상단 헤더 & 가동률 대시보드 */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold text-slate-900">
                선형 흐름선도 (Line of Balance / Takt Flow Chart)
              </h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800">
                작업팀 대기시간(Zero Idle) 최적화 뷰
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              스팬(위치)별 전문 작업팀의 연속 이동 사선 궤적 분석 (사선의 기울기가 일정할수록 생산성 극대화)
            </p>
          </div>
        </div>

        {/* 가동률 & 대기손실 지표 */}
        <div className="flex items-center gap-3 text-xs font-mono">
          <div className="px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <span className="text-slate-500 text-[10px] block">작업팀 실가동률</span>
            <span className={`text-sm font-black ${utilizationRate > 90 ? 'text-emerald-600' : 'text-amber-600'}`}>
              {utilizationRate}%
            </span>
          </div>

          <div className="px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <span className="text-slate-500 text-[10px] block">가시설 간섭 대기 손실</span>
            <span className={`text-sm font-black ${idleDays === 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
              {idleDays}일 지연
            </span>
          </div>
        </div>
      </div>

      {/* 2. 범례 (Legend) */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2 px-3 rounded-lg bg-slate-50 border border-slate-200 text-xs">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-amber-500 shadow-2xs" />
            <span className="font-bold text-slate-700">🔨 거푸집·동바리팀</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-blue-600 shadow-2xs" />
            <span className="font-bold text-slate-700">🏗️ 철근 배근팀</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-emerald-500 shadow-2xs" />
            <span className="font-bold text-slate-700">🚛 콘크리트 타설팀</span>
          </div>
          {!isAnchor && (
            <div className="flex items-center gap-1.5">
              <div className="w-3 h-3 rounded-full bg-rose-500 shadow-2xs" />
              <span className="font-bold text-rose-700">✂️ 14MPa 양생·버팀보 해체팀</span>
            </div>
          )}
        </div>

        <span className="text-[11px] text-slate-500 font-medium">
          💡 차트 위를 클릭하면 해당 일자로 시뮬레이션 커서가 이동합니다.
        </span>
      </div>

      {/* 3. LOB SVG 차트 캔버스 */}
      <div className="relative bg-white rounded-lg border border-slate-300 shadow-inner overflow-hidden flex justify-center cursor-crosshair">
        <svg 
          viewBox={`0 0 ${svgWidth} ${svgHeight}`} 
          className="w-full h-auto max-h-[460px] select-none"
          onClick={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const svgX = (clickX / rect.width) * svgWidth;
            if (svgX >= paddingLeft && svgX <= paddingLeft + drawW) {
              const clickedDay = Math.round((svgX - paddingLeft) / scaleX);
              onDayChange(Math.max(0, Math.min(totalDays, clickedDay)));
            }
          }}
        >
          <defs>
            <pattern id="gridTakt" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" strokeWidth="1" />
            </pattern>
          </defs>

          {/* 배경 그리드 */}
          <rect x={paddingLeft} y={paddingTop} width={drawW} height={drawH} fill="url(#gridTakt)" />

          {/* Y축 그리드선 & 스팬 라벨 */}
          {Array.from({ length: numSpans }).map((_, sIdx) => {
            const y = paddingTop + (numSpans - 1 - sIdx) * scaleY;
            const isSelected = selectedSpanIdx === sIdx;

            return (
              <g key={`lob-span-${sIdx}`}>
                <line 
                  x1={paddingLeft} 
                  y1={y + scaleY / 2} 
                  x2={paddingLeft + drawW} 
                  y2={y + scaleY / 2} 
                  stroke={isSelected ? '#93c5fd' : '#e2e8f0'} 
                  strokeWidth={isSelected ? 2 : 1}
                  strokeDasharray={isSelected ? 'none' : '2 2'}
                />
                <rect 
                  x="8" 
                  y={y + scaleY / 2 - 12} 
                  width="74" 
                  height="22" 
                  rx="4" 
                  fill={isSelected ? '#eff6ff' : '#ffffff'} 
                  stroke={isSelected ? '#3b82f6' : '#cbd5e1'} 
                  strokeWidth="1.2"
                  className="cursor-pointer"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectSpan(sIdx);
                  }}
                />
                <text 
                  x="45" 
                  y={y + scaleY / 2 + 2} 
                  fill={isSelected ? '#1d4ed8' : '#334155'} 
                  fontSize="10" 
                  fontFamily="monospace" 
                  fontWeight="bold" 
                  textAnchor="middle"
                  className="cursor-pointer"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectSpan(sIdx);
                  }}
                >
                  Span {sIdx + 1}
                </text>
              </g>
            );
          })}

          {/* X축 시간 라인 & 날짜 틱 */}
          {Array.from({ length: Math.ceil(totalDays / 10) + 1 }).map((_, dIdx) => {
            const d = dIdx * 10;
            if (d > totalDays) return null;
            const x = paddingLeft + d * scaleX;

            return (
              <g key={`lob-tick-${d}`}>
                <line x1={x} y1={paddingTop} x2={x} y2={paddingTop + drawH} stroke="#e2e8f0" strokeWidth="1" />
                <text x={x} y={paddingTop + drawH + 18} fill="#64748b" fontSize="9" fontFamily="monospace" textAnchor="middle">
                  D+{d}
                </text>
              </g>
            );
          })}

          {/* X축 / Y축 경계선 */}
          <line x1={paddingLeft} y1={paddingTop} x2={paddingLeft} y2={paddingTop + drawH} stroke="#475569" strokeWidth="2" />
          <line x1={paddingLeft} y1={paddingTop + drawH} x2={paddingLeft + drawW} y2={paddingTop + drawH} stroke="#475569" strokeWidth="2" />

          {/* 4. 작업팀 선형 궤적 (LOB Polylines) */}
          {/* (1) 거푸집 팀 선 */}
          {formworkPoints.length > 1 && (
            <polyline
              points={formworkPoints.map(p => `${paddingLeft + p.midDay * scaleX},${paddingTop + (numSpans - 1 - p.spanIdx) * scaleY + scaleY / 2}`).join(' ')}
              fill="none"
              stroke="#f59e0b"
              strokeWidth="4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}

          {/* (2) 타설 팀 선 */}
          {pouringPoints.length > 1 && (
            <polyline
              points={pouringPoints.map(p => `${paddingLeft + p.midDay * scaleX},${paddingTop + (numSpans - 1 - p.spanIdx) * scaleY + scaleY / 2}`).join(' ')}
              fill="none"
              stroke="#10b981"
              strokeWidth="4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}

          {/* (3) 버팀보 해체 팀 선 */}
          {strutPoints.length > 1 && (
            <polyline
              points={strutPoints.map(p => `${paddingLeft + p.midDay * scaleX},${paddingTop + (numSpans - 1 - p.spanIdx) * scaleY + scaleY / 2}`).join(' ')}
              fill="none"
              stroke="#ef4444"
              strokeWidth="3.5"
              strokeDasharray="4 2"
              strokeLinecap="round"
            />
          )}

          {/* 각 스팬별 작업 진행 바 블록 오버레이 */}
          {schedule.tasks.map((task) => {
            const y = paddingTop + (numSpans - 1 - task.spanIndex) * scaleY + 6;
            const x = paddingLeft + task.startDay * scaleX;
            const w = Math.max(6, task.durationDays * scaleX);
            const h = scaleY - 12;

            const isDone = currentDay >= task.endDay;
            const isActive = currentDay >= task.startDay && currentDay < task.endDay;

            let fillColor = '#94a3b8';
            if (task.type === 'foundation') fillColor = '#d97706';
            else if (task.type === 'story_wall') fillColor = '#3b82f6';
            else if (task.type === 'strut_release_curing') fillColor = '#ef4444';
            else if (task.type === 'mid_slab' || task.type === 'top_slab') fillColor = '#10b981';

            return (
              <g key={`lob-task-${task.id}`}>
                <rect
                  x={x}
                  y={y}
                  width={w}
                  height={h}
                  rx="3"
                  fill={fillColor}
                  opacity={isActive ? 1 : isDone ? 0.75 : 0.3}
                  stroke={isActive ? '#0f172a' : 'none'}
                  strokeWidth={isActive ? 1.5 : 0}
                />
              </g>
            );
          })}

          {/* 5. 실시간 Day 타임라인 라이브 커서 */}
          <line
            x1={paddingLeft + currentDay * scaleX}
            y1={paddingTop - 15}
            x2={paddingLeft + currentDay * scaleX}
            y2={paddingTop + drawH}
            stroke="#e11d48"
            strokeWidth="2.5"
            strokeDasharray="4 2"
          />
          <rect
            x={paddingLeft + currentDay * scaleX - 25}
            y={paddingTop - 32}
            width="50"
            height="18"
            rx="3"
            fill="#e11d48"
          />
          <text
            x={paddingLeft + currentDay * scaleX}
            y={paddingTop - 20}
            fill="#ffffff"
            fontSize="10"
            fontFamily="monospace"
            fontWeight="bold"
            textAnchor="middle"
          >
            D+{currentDay}
          </text>
        </svg>
      </div>

      {/* 4. 경영진 핵심 브리핑 요약 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
        <div className="p-3 rounded-lg bg-amber-50/70 border border-amber-200 space-y-1">
          <span className="font-bold text-amber-900 flex items-center gap-1.5">
            <Hammer className="w-4 h-4 text-amber-600" />
            <span>거푸집·철근 선행팀 연속성</span>
          </span>
          <p className="text-[11px] text-amber-800 leading-relaxed">
            1개 스팬(20m) 작업 완료 즉시 다음 스팬으로 이동하여 <strong>유휴 대기 없이 100% 연속 가동</strong>됩니다.
          </p>
        </div>

        <div className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200 space-y-1">
          <span className="font-bold text-emerald-900 flex items-center gap-1.5">
            <Truck className="w-4 h-4 text-emerald-600" />
            <span>타설팀(Pouring) 연속 순환</span>
          </span>
          <p className="text-[11px] text-emerald-800 leading-relaxed">
            선행 철근 배근이 끝나는 스팬마다 즉시 레미콘 타설팀이 투입되어 <strong>스팬 간 완벽한 릴레이</strong>를 형성합니다.
          </p>
        </div>

        <div className={`p-3 rounded-lg border space-y-1 ${isAnchor ? 'bg-blue-50/70 border-blue-200' : 'bg-rose-50/70 border-rose-200'}`}>
          <span className={`font-bold flex items-center gap-1.5 ${isAnchor ? 'text-blue-900' : 'text-rose-900'}`}>
            <Scissors className={`w-4 h-4 ${isAnchor ? 'text-blue-600' : 'text-rose-600'}`} />
            <span>{isAnchor ? '무지보 대기시간 0일' : '버팀보 양생 병목 구간'}</span>
          </span>
          <p className={`text-[11px] leading-relaxed ${isAnchor ? 'text-blue-800' : 'text-rose-800'}`}>
            {isAnchor
              ? '가시설 간섭이 전혀 없어 작업팀 정체(Idle Loss)가 0일이며 사선 궤적이 가장 가파릅니다.'
              : `14MPa 압축강도 양생 5일 대기 동안 타설팀 이동이 지연되어 총 ${idleDays}일의 대기 손실이 발생합니다.`}
          </p>
        </div>
      </div>
    </div>
  );
};
