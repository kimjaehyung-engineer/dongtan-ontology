import React, { useState, useEffect, useRef, useMemo } from 'react';
import { AlternativeSpanScheduleResult, SpanTask } from '../../engine/structureScheduleEngine';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Clock,
  Hammer,
  Truck,
  Scissors,
  CheckCircle2,
  ArrowRight,
  Layers,
  Zap
} from 'lucide-react';

interface InteractiveGanttChartProps {
  schedule: AlternativeSpanScheduleResult;
  currentDay: number;
  onDayChange: (day: number | ((prev: number) => number)) => void;
  selectedSpanIdx: number;
  onSelectSpan: (spanIdx: number) => void;
}

export const InteractiveGanttChart: React.FC<InteractiveGanttChartProps> = ({
  schedule,
  currentDay,
  onDayChange,
  selectedSpanIdx,
  onSelectSpan
}) => {
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playSpeed, setPlaySpeed] = useState<number>(0.5); // 기본 0.5x (슬로우모션), 1x, 2x, 4x
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const totalDays = schedule.totalDurationDays || 1;
  const isAnchor = schedule.altType === 'ALL_ANCHOR';
  const numSpans = schedule.numSpans;

  // 자동 재생 루프
  useEffect(() => {
    if (isPlaying) {
      const intervalMs = Math.max(100, Math.round(500 / playSpeed));
      timerRef.current = setInterval(() => {
        onDayChange((prev: number) => {
          if (prev >= totalDays) {
            setIsPlaying(false);
            return totalDays;
          }
          return prev + 1;
        });
      }, intervalMs);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, playSpeed, totalDays, onDayChange]);

  const handleTogglePlay = () => {
    if (currentDay >= totalDays) {
      onDayChange(0);
    }
    setIsPlaying(!isPlaying);
  };

  const handleReset = () => {
    setIsPlaying(false);
    onDayChange(0);
  };

  // 4대 작업팀 정의 및 현재 위치 계산
  const crewList = useMemo(() => {
    const teams = [
      { 
        id: 'formwork', 
        name: '거푸집팀', 
        role: '외벽/슬래브 폼 조립', 
        icon: Hammer, 
        activeBg: 'bg-amber-500 text-white', 
        activeBorder: 'bg-white border-amber-400 ring-2 ring-amber-200',
        activeText: 'text-amber-700',
        barColor: 'bg-amber-500',
        match: (t: SpanTask) => t.type === 'foundation' || t.type === 'story_wall' 
      },
      { 
        id: 'rebar', 
        name: '철근팀', 
        role: '벽체/슬래브 철근 배근', 
        icon: Layers, 
        activeBg: 'bg-blue-600 text-white', 
        activeBorder: 'bg-white border-blue-400 ring-2 ring-blue-200',
        activeText: 'text-blue-700',
        barColor: 'bg-blue-600',
        match: (t: SpanTask) => t.type === 'story_wall' || t.type === 'foundation' 
      },
      { 
        id: 'pouring', 
        name: '타설팀', 
        role: '레미콘 타설 & 피니싱', 
        icon: Truck, 
        activeBg: 'bg-emerald-600 text-white', 
        activeBorder: 'bg-white border-emerald-400 ring-2 ring-emerald-200',
        activeText: 'text-emerald-700',
        barColor: 'bg-emerald-600',
        match: (t: SpanTask) => t.type === 'mid_slab' || t.type === 'top_slab' || t.type === 'foundation' 
      },
      { 
        id: 'strut', 
        name: '가시설팀 (버팀보 해체)', 
        role: isAnchor ? '무지보 (해체 불필요)' : '버팀보 절단/인양 & 띠장 철거', 
        icon: Scissors, 
        activeBg: 'bg-rose-600 text-white', 
        activeBorder: 'bg-white border-rose-400 ring-2 ring-rose-200',
        activeText: 'text-rose-700',
        barColor: 'bg-rose-600',
        match: (t: SpanTask) => t.type === 'strut_release_curing' || t.type === 'kingpost_waterproof' 
      }
    ];

    return teams.map(tm => {
      const taskList = schedule.tasks.filter(tm.match);
      const active = taskList.find(t => currentDay >= t.startDay && currentDay < t.endDay);
      const next = taskList.find(t => t.startDay > currentDay);
      return {
        ...tm,
        activeTask: active,
        nextTask: next,
        isCompleted: !active && !next && taskList.length > 0
      };
    });
  }, [schedule, currentDay, isAnchor]);

  // 공정 단계(스텝) 컬럼 정의 (층수에 맞춰 동적 생성)
  const steps = useMemo(() => {
    const sList: { id: string; label: string; subLabel: string; type: string; storyIndex?: number; stage?: number }[] = [
      { id: 'foundation', label: '1. 바닥 기초', subLabel: '거푸집·배근·타설', type: 'foundation' }
    ];

    for (let s = 0; s < schedule.numStories; s++) {
      const sName = schedule.storyNames[s] || `B${schedule.numStories - s}층`;
      const shortName = sName.split(' ')[0];
      
      if (!isAnchor) {
        // 스트럿 구간: 1단 하부벽 -> 버팀보 해체 -> 2단 상부벽
        sList.push({ id: `wall_1_${s}`, label: `${sList.length + 1}. ${shortName} 1단 하부벽체`, subLabel: '거푸집·배근·타설', type: 'story_wall', storyIndex: s, stage: 1 });
        sList.push({ id: `rel_${s}`, label: `${sList.length + 1}. ${shortName} 버팀보 해체`, subLabel: '14MPa 양생·인양', type: 'strut_release_curing', storyIndex: s });
        sList.push({ id: `wall_2_${s}`, label: `${sList.length + 1}. ${shortName} 2단 상부벽체`, subLabel: '거푸집·배근·타설', type: 'story_wall', storyIndex: s, stage: 2 });
      } else {
        // 어스앵커 구간: 1회 전단 일괄 타설
        sList.push({ id: `wall_${s}`, label: `${sList.length + 1}. ${shortName} 외벽체 일괄`, subLabel: '갱폼·배근·타설', type: 'story_wall', storyIndex: s });
      }

        if (s < schedule.numStories - 1) {
          // 기둥 시공 후 중간 슬래브
          sList.push({ id: `col_${s}`, label: `${sList.length + 1}. ${shortName} 중앙 원형기둥`, subLabel: 'Φ1000 @7.0m 배근·타설', type: 'story_column', storyIndex: s });
          sList.push({ id: `midslab_${s}`, label: `${sList.length + 1}. 중간 슬래브`, subLabel: '동바리·거푸집·배근·일괄타설', type: 'mid_slab', storyIndex: s });
        } else {
          // 최상층 기둥 시공 후 지붕 슬래브
          sList.push({ id: `col_${s}`, label: `${sList.length + 1}. ${shortName} 중앙 원형기둥`, subLabel: 'Φ1000 @7.0m 배근·타설', type: 'story_column', storyIndex: s });
        }
      }

      sList.push({ id: 'top_slab', label: `${sList.length + 1}. 지붕 슬래브`, subLabel: '동바리·거푸집·배근·타설 (토피 5m 지지)', type: 'top_slab' });

    if (!isAnchor) {
      sList.push({ id: 'kingpost', label: `${sList.length + 1}. 중간말뚝 인발`, subLabel: '관통부 무수축방수', type: 'kingpost_waterproof' });
    }

    return sList;
  }, [schedule, isAnchor]);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3.5 font-sans">
      {/* 1. 상단 타임라인 컨트롤 바 */}
      <div className="bg-slate-900 text-white rounded-xl p-2.5 px-4 flex flex-wrap items-center justify-between gap-3 shadow-md">
        {/* 좌측: 컨트롤 */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleReset}
            className="p-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all"
            title="Day 0 리셋"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={handleTogglePlay}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md font-bold text-xs shadow-md transition-all ${
              isPlaying
                ? 'bg-amber-500 hover:bg-amber-600 text-slate-950'
                : 'bg-emerald-500 hover:bg-emerald-600 text-white'
            }`}
          >
            {isPlaying ? (
              <>
                <Pause className="w-3.5 h-3.5 fill-current" />
                <span>일시정지</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>흐름 재생</span>
              </>
            )}
          </button>

          {/* 배속 */}
          <div className="flex items-center bg-slate-800 rounded-md p-0.5 border border-slate-700 text-xs gap-0.5">
            {[0.5, 1, 2, 4].map((speed) => (
              <button
                key={speed}
                onClick={() => setPlaySpeed(speed)}
                className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold transition-all ${
                  playSpeed === speed ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
              >
                {speed}x
              </button>
            ))}
          </div>
        </div>

        {/* 중앙: 날짜 슬라이더 */}
        <div className="flex-1 min-w-[200px] flex items-center gap-2.5">
          <span className="text-[11px] font-mono text-slate-400">D+0</span>
          <input
            type="range"
            min="0"
            max={totalDays}
            value={currentDay}
            onChange={(e) => {
              setIsPlaying(false);
              onDayChange(Number(e.target.value));
            }}
            className="flex-1 h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
          <div className="flex items-center gap-1 font-mono">
            <span className="text-xs font-black text-emerald-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
              Day {currentDay}
            </span>
            <span className="text-[10px] text-slate-400">/ {totalDays}일</span>
          </div>
        </div>

        {/* 우측: 총 공기 */}
        <div className="text-right font-mono">
          <span className="text-xs font-bold text-amber-300">
            총 {totalDays}일 ({(totalDays / 30).toFixed(1)}개월)
          </span>
        </div>
      </div>

      {/* 2. 🌟 실시간 4대 작업팀 Live Status 스트립 (팀별 고유 색상 칩) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {crewList.map((crew) => {
          const Icon = crew.icon;
          const task = crew.activeTask;

          return (
            <div
              key={`live-${crew.id}`}
              className={`p-2.5 rounded-xl border text-xs flex items-center justify-between gap-2 transition-all ${
                task
                  ? `${crew.activeBorder} shadow-sm`
                  : 'bg-slate-50 border-slate-200 text-slate-500'
              }`}
            >
              <div className="flex items-center gap-2 min-w-0">
                <span className={`p-1.5 rounded-lg shadow-2xs ${task ? crew.activeBg : 'bg-slate-200 text-slate-600'}`}>
                  <Icon className="w-3.5 h-3.5" />
                </span>
                <div className="min-w-0">
                  <div className="flex items-center gap-1">
                    <span className="font-bold text-slate-900 block truncate text-[11px]">{crew.name}</span>
                  </div>
                  {task ? (
                    <span className={`text-[10px] ${crew.activeText} font-bold block truncate`}>
                      Span {task.spanIndex + 1} {task.name.replace(/\[[^\]]+\] /, '').replace(/Span \d+ \([^)]+\) /, '')}
                    </span>
                  ) : crew.nextTask ? (
                    <span className="text-[9px] text-slate-500 block truncate">
                      Span {crew.nextTask.spanIndex + 1} 대기 (D+{crew.nextTask.startDay} 착수)
                    </span>
                  ) : (
                    <span className="text-[9px] text-slate-400 block truncate">{crew.role}</span>
                  )}
                </div>
              </div>

              {task && (
                <span className={`shrink-0 px-1.5 py-0.5 rounded font-mono font-bold text-[9px] shadow-2xs ${crew.activeBg} animate-pulse`}>
                  {Math.round(((currentDay - task.startDay) / task.durationDays) * 100)}%
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* 3. 🌟 메인: 깔끔한 『스팬 × 단계별 공정 매트릭스 흐름도 (Span Flow Matrix)』 */}
      <div className="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100/90 text-slate-700 border-b border-slate-200 text-[11px]">
                <th className="p-2.5 font-bold w-24 shrink-0 border-r border-slate-200 align-middle">구획 (스팬)</th>
                {steps.map((step) => (
                  <th key={step.id} className="p-2 font-bold text-center border-r border-slate-200 last:border-r-0 whitespace-nowrap">
                    <div className="text-slate-800 text-[11px] font-bold">{step.label}</div>
                    <div className="text-[9.5px] font-medium text-indigo-600 bg-indigo-50/80 px-1.5 py-0.5 rounded mt-0.5 inline-block">
                      {step.subLabel}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {Array.from({ length: numSpans }).map((_, spanIdx) => {
                const isSelected = selectedSpanIdx === spanIdx;

                return (
                  <tr 
                    key={`span-row-${spanIdx}`} 
                    className={`transition-colors ${isSelected ? 'bg-blue-50/40' : 'hover:bg-slate-50/50'}`}
                    onClick={() => onSelectSpan(spanIdx)}
                  >
                    {/* 스팬 헤더 셀 */}
                    <td className="p-2.5 font-bold font-mono text-slate-800 border-r border-slate-200 cursor-pointer bg-slate-50/70">
                      <div className="flex items-center justify-between gap-1.5">
                        <div className="flex items-center gap-1.5">
                          <span className={`w-2 h-2 rounded-full ${isSelected ? 'bg-blue-600' : 'bg-slate-300'}`} />
                          <span className="text-xs">Span {spanIdx + 1}</span>
                        </div>
                      </div>
                      <span className="text-[9px] text-slate-400 font-normal block pl-3.5 mt-0.5">
                        {spanIdx * schedule.spanLengthM}m ~ {Math.min(schedule.totalLengthM, (spanIdx + 1) * schedule.spanLengthM)}m
                      </span>
                    </td>

                    {/* 각 공정 단계 셀 */}
                    {steps.map((step) => {
                      // 해당 스팬 및 공정 단계의 태스크 찾기
                      const task = schedule.tasks.find(t => {
                        if (t.spanIndex !== spanIdx) return false;
                        if (t.type !== step.type) return false;
                        if ((step as any).storyIndex !== undefined && t.storyIndex !== (step as any).storyIndex) {
                          return false;
                        }
                        if ((step as any).stage === 1) {
                          return t.id.includes('_wall_1');
                        }
                        if ((step as any).stage === 2) {
                          return t.id.includes('_wall_2');
                        }
                        return true;
                      });

                      if (!task) {
                        return <td key={step.id} className="p-2 text-center border-r border-slate-200 text-slate-300 text-[10px]">-</td>;
                      }

                      const isDone = currentDay >= task.endDay;
                      const isActive = currentDay >= task.startDay && currentDay < task.endDay;
                      const isWaiting = currentDay < task.startDay;

                      return (
                        <td 
                          key={step.id} 
                          className="p-1.5 text-center border-r border-slate-200 last:border-r-0 cursor-pointer"
                          onClick={(e) => {
                            e.stopPropagation();
                            onDayChange(task.startDay);
                            onSelectSpan(spanIdx);
                          }}
                          title={`클릭 시 착수일(D+${task.startDay})로 이동\n${task.name} (${task.durationDays}일간)`}
                        >
                          <div className={`p-1.5 rounded-md border text-[10px] transition-all flex flex-col items-center justify-center gap-0.5 min-h-[44px] ${
                            isActive
                              ? 'bg-blue-600 text-white border-blue-700 shadow-md ring-2 ring-blue-300 font-bold scale-102'
                              : isDone
                              ? 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200'
                              : 'bg-white text-slate-400 border-dashed border-slate-200 hover:border-slate-300'
                          }`}>
                            <div className="flex items-center gap-1 font-mono text-[9px]">
                              {isDone ? (
                                <span className="flex items-center gap-0.5 text-emerald-600 font-bold">
                                  <CheckCircle2 className="w-3 h-3" /> 완료
                                </span>
                              ) : isActive ? (
                                <span className="flex items-center gap-0.5 text-amber-300 font-bold animate-pulse">
                                  <Zap className="w-2.5 h-2.5 fill-current" /> D+{currentDay}
                                </span>
                              ) : (
                                <span>D+{task.startDay}</span>
                              )}
                            </div>

                            <span className="text-[9px] truncate max-w-[85px] block opacity-90">
                              {task.durationDays}일 소요
                            </span>
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. 하단 직관적 안내 팁 */}
      <div className="flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-600 bg-slate-50 p-2.5 px-3.5 rounded-lg border border-slate-200">
        <div className="flex items-center gap-2">
          <span className="font-bold text-slate-800">💡 표준 시공 사이클:</span>
          <span>모든 구조체 공정은 <strong>[거푸집·동바리 조립 ➡️ 철근 배근 ➡️ 콘크리트 타설 ➡️ 양생]</strong> 순서로 진행됩니다. (임의의 셀 클릭 시 해당 착수 시점으로 이동)</span>
        </div>
        <div className="flex items-center gap-3 font-mono text-[10px]">
          <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded bg-blue-600" /> 현재 진행중</span>
          <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded bg-slate-200" /> 완료</span>
          <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded border border-dashed border-slate-300" /> 착수 대기</span>
        </div>
      </div>

      {/* 🌟 5. 작업팀별 작업기간(Work Days) vs 유휴 대기기간(Idle Days) 실시간 분석 패널 */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3.5 shadow-2xs mt-3">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded bg-indigo-600 text-white">
              <Clock className="w-4 h-4" />
            </span>
            <div>
              <h4 className="text-xs font-bold text-slate-900">
                작업팀별 실작업 기간(Work) vs 유휴 대기 기간(Idle) 종합 분석
              </h4>
              <p className="text-[10px] text-slate-500">
                가시설 간섭(14MPa 양생 대기 등)으로 인한 팀별 병목 및 실가동률(Utilization Rate) 비교
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs font-mono">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-blue-600 shadow-2xs" />
              <span className="text-slate-700 font-bold">실제 작업 기간 (Work)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-amber-400/80 border border-amber-500 shadow-2xs" />
              <span className="text-amber-800 font-bold">유휴 대기 기간 (Idle)</span>
            </div>
          </div>
        </div>

        {/* 4대 작업팀별 타임라인 바 & 수치 카드 */}
        <div className="space-y-2.5">
          {crewList.map((crew) => {
            const Icon = crew.icon;
            const taskList = schedule.tasks.filter(crew.match);
            
            // 작업 일수 및 대기 일수 산정
            const totalWorkDays = taskList.reduce((sum, t) => sum + t.durationDays, 0);
            const firstStart = taskList.length > 0 ? taskList[0].startDay : 0;
            const lastEnd = taskList.length > 0 ? taskList[taskList.length - 1].endDay : totalDays;
            const activeSpanDays = Math.max(1, lastEnd - firstStart);
            const totalIdleDays = Math.max(0, activeSpanDays - totalWorkDays);
            const utilization = Math.min(100, Math.round((totalWorkDays / activeSpanDays) * 100));

            return (
              <div key={`crew-stat-${crew.id}`} className="p-2.5 rounded-lg bg-slate-50/70 border border-slate-200 space-y-1.5">
                {/* 팀 헤더 & 수치 요약 */}
                <div className="flex flex-wrap items-center justify-between text-xs gap-2">
                  <div className="flex items-center gap-2">
                    <span className="p-1 rounded bg-white border border-slate-200 shadow-2xs text-slate-700">
                      <Icon className="w-3.5 h-3.5" />
                    </span>
                    <span className="font-bold text-slate-800 text-[11px]">{crew.name}</span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      (투입구간: D+{firstStart} ~ D+{lastEnd})
                    </span>
                  </div>

                  <div className="flex items-center gap-3 font-mono text-[11px]">
                    <span className="text-slate-600">
                      실작업: <strong className="text-blue-700 font-bold">{totalWorkDays}일</strong>
                    </span>
                    <span className="text-slate-300">|</span>
                    <span className="text-slate-600">
                      유휴대기: <strong className={`${totalIdleDays > 0 ? 'text-amber-600' : 'text-emerald-600'} font-bold`}>{totalIdleDays}일</strong>
                    </span>
                    <span className="text-slate-300">|</span>
                    <span className="px-2 py-0.5 rounded font-bold text-[10px] bg-white border border-slate-200 text-slate-800">
                      가동률: <span className={utilization >= 85 ? 'text-emerald-600' : 'text-amber-600'}>{utilization}%</span>
                    </span>
                  </div>
                </div>

                {/* 타임라인 바 트랙 (0일 ~ totalDays) */}
                <div className="relative h-6 bg-white rounded-md border border-slate-200 overflow-hidden shadow-inner flex items-center">
                  {/* 대기 구간 배경 (투입 시작일부터 종료일까지) */}
                  <div
                    className="absolute top-0 bottom-0 bg-amber-50 border-y border-amber-200/50"
                    style={{
                      left: `${(firstStart / totalDays) * 100}%`,
                      width: `${((lastEnd - firstStart) / totalDays) * 100}%`
                    }}
                    title={`대기/투입 구간: D+${firstStart} ~ D+${lastEnd}`}
                  />

                  {/* 실제 작업 블록들 */}
                  {taskList.map((task) => {
                    const leftPct = (task.startDay / totalDays) * 100;
                    const widthPct = Math.max(1.5, (task.durationDays / totalDays) * 100);
                    const isTaskDone = currentDay >= task.endDay;
                    const isTaskCurrent = currentDay >= task.startDay && currentDay < task.endDay;

                    return (
                      <div
                        key={`bar-${task.id}`}
                        onClick={() => onDayChange(task.startDay)}
                        className={`absolute top-0.5 bottom-0.5 rounded text-[9px] font-mono font-bold flex items-center justify-center text-white cursor-pointer transition-all shadow-2xs ${
                          isTaskCurrent
                            ? `${crew.barColor} ring-2 ring-slate-900 z-10 animate-pulse`
                            : isTaskDone
                            ? 'bg-slate-400 hover:bg-slate-500'
                            : `${crew.barColor} opacity-80 hover:opacity-100`
                        }`}
                        style={{
                          left: `${leftPct}%`,
                          width: `${widthPct}%`
                        }}
                        title={`${task.name}: ${task.durationDays}일간 (D+${task.startDay} ~ D+${task.endDay})`}
                      >
                        <span className="truncate px-1 text-[8.5px]">
                          {task.spanIndex + 1}스팬
                        </span>
                      </div>
                    );
                  })}

                  {/* 실시간 Day 라이브 커서 */}
                  <div
                    className="absolute top-0 bottom-0 w-0.5 bg-rose-600 z-20 pointer-events-none"
                    style={{ left: `${(currentDay / totalDays) * 100}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
