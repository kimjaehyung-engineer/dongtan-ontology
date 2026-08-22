import React from 'react';
import { SpanDailyState, AlternativeSpanScheduleResult, StructureScheduleEngine } from '../../engine/structureScheduleEngine';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { Layers, AlertTriangle, ShieldCheck, CheckCircle2, ArrowRight, Scissors, Hammer, Sparkles } from 'lucide-react';

interface LongitudinalProfileViewerProps {
  inputs: ProjectInputs;
  selectedAlt: AlternativeSpec;
  schedule: AlternativeSpanScheduleResult;
  dailyStates: SpanDailyState[];
  currentDay: number;
  selectedSpanIdx: number;
  onSelectSpan: (idx: number) => void;
}

export const LongitudinalProfileViewer: React.FC<LongitudinalProfileViewerProps> = ({
  inputs,
  selectedAlt,
  schedule,
  dailyStates,
  currentDay,
  selectedSpanIdx,
  onSelectSpan
}) => {
  const H = inputs.excavationDepth;
  const totalLength = schedule.totalLengthM;
  const numSpans = schedule.numSpans;
  const spanLength = schedule.spanLengthM;

  const isAnchor = selectedAlt.type === 'ALL_ANCHOR';
  const isHybrid = selectedAlt.type === 'HYBRID';
  const isCompStrut = selectedAlt.type === 'COMPOSITE_STRUT';
  const hasKingPost = selectedAlt.type === 'ALL_STRUT' || (selectedAlt.type === 'HYBRID' && inputs.excavationWidth >= 20);

  const { numStories, storyNames } = StructureScheduleEngine.determineStationStories(H);

  // SVG 좌표계
  const svgWidth = 960;
  const svgHeight = 420;
  const paddingX = 60;
  const paddingTop = 55;
  const paddingBottom = 45;

  const drawW = svgWidth - paddingX * 2;
  const drawH = svgHeight - paddingTop - paddingBottom;

  const scaleX = drawW / totalLength;
  const scaleY = drawH / (H + 3.0);

  const groundY = paddingTop;
  const excBottomY = groundY + H * scaleY;

  const slabThick = 0.8 * scaleY;
  const overburdenDepth = 5.0; // 상부 5.0m 피복
  const baseSlabTopY = excBottomY - 1.0 * scaleY;
  const topSlabTopY = groundY + overburdenDepth * scaleY; // GL 아래 5.0m
  const topSlabBottomY = topSlabTopY + 1.0 * scaleY;

  // 층별 바닥/슬래브 Y 레벨
  const totalBoxHeight = Math.max(2.0, baseSlabTopY - topSlabBottomY);
  const storyHeight = totalBoxHeight / Math.max(1, numStories);
  const storyFloorYs = Array.from({ length: numStories + 1 }).map((_, idx) => {
    return baseSlabTopY - idx * storyHeight;
  });

  const strutLevels = selectedAlt.supports.map(s => groundY + s.depth * scaleY);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
      {/* 헤더 바 */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-indigo-50 text-indigo-600">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold text-slate-800">
                종단면도 실시간 축조 & 버팀보 순차 해체 시뮬레이션 [지하 {numStories}층 구조물]
              </h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800 font-mono">
                L = {totalLength.toFixed(0)}m (20m × {numSpans}스팬) | 굴착 {H.toFixed(1)}m | Day {currentDay}/{schedule.totalDurationDays}일
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              진행방향(종방향)으로 바닥기초 $\rightarrow$ <strong>지하 {numStories}개 층별 벽체/슬래브</strong> $\rightarrow$ <strong>버팀보 해체</strong> $\rightarrow$ 상부슬래브 릴레이 진행 묘사
            </p>
          </div>
        </div>

        {/* 범례 */}
        <div className="flex items-center gap-3 text-[10px] text-slate-600 font-medium">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-emerald-500"></span> 타설중
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-amber-400"></span> 14MPa 양생대기
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-rose-500"></span> 버팀보 절단/인양
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-slate-500"></span> 타설완료
          </span>
        </div>
      </div>

      {/* SVG 종단면도 캔버스 */}
      <div className="relative bg-slate-50 rounded-lg overflow-hidden border border-slate-300 shadow-inner flex justify-center">
        <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full h-auto max-h-[460px] select-none">
          <defs>
            <pattern id="soilProfileLightStory" width="16" height="16" patternUnits="userSpaceOnUse">
              <rect width="16" height="16" fill="#f1f5f9" />
              <path d="M0 16 L16 0 M0 8 L8 0 M8 16 L16 8" stroke="#cbd5e1" strokeWidth="0.8" />
            </pattern>
            <pattern id="concDoneProfileStory" width="12" height="12" patternUnits="userSpaceOnUse">
              <rect width="12" height="12" fill="#94a3b8" />
              <circle cx="3" cy="3" r="0.8" fill="#e2e8f0" />
              <circle cx="9" cy="9" r="0.8" fill="#e2e8f0" />
            </pattern>
            <pattern id="concProgProfileStory" width="12" height="12" patternUnits="userSpaceOnUse">
              <rect width="12" height="12" fill="#10b981" />
              <path d="M0 12 L12 0" stroke="#a7f3d0" strokeWidth="2.0" />
            </pattern>
          </defs>

          {/* 1. 배경 미굴착 지반 & 굴착 영역 */}
          <rect x={paddingX} y={excBottomY} width={drawW} height={svgHeight - excBottomY} fill="url(#soilProfileLightStory)" />
          <rect x={paddingX} y={groundY} width={drawW} height={excBottomY - groundY} fill="#ffffff" />

          {/* 🌟 상부 지표면 (GL ±0.00m 도로/노면 라인) */}
          <line x1={paddingX - 40} y1={groundY} x2={paddingX + drawW + 40} y2={groundY} stroke="#1e293b" strokeWidth="2.5" />
          <rect x={paddingX - 40} y={groundY - 4} width={drawW + 80} height="4" fill="#64748b" opacity="0.3" />
          <rect x={paddingX - 58} y={groundY - 24} width="84" height="20" fill="#ffffff" stroke="#1e293b" strokeWidth="1.2" rx="3" />
          <text x={paddingX - 16} y={groundY - 10} fill="#0f172a" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
            ▼ GL ±0.00m
          </text>

          {/* 🌟 상부 5.0m 토피 피복 구간 가이드선 및 치수 라벨 */}
          <g>
            <rect x={paddingX} y={groundY} width={drawW} height={topSlabTopY - groundY} fill="#f8fafc" fillOpacity="0.6" stroke="#94a3b8" strokeDasharray="3 3" strokeWidth="0.8" />
            <text x={paddingX + drawW / 2} y={groundY + (topSlabTopY - groundY) / 2 + 4} fill="#64748b" fontSize="10" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
              [상부 토피 피복층 & 지하매설물 통과 공간 (피복고 D = {overburdenDepth.toFixed(1)}m)]
            </text>
          </g>

          <line x1={paddingX} y1={excBottomY} x2={paddingX + drawW} y2={excBottomY} stroke="#64748b" strokeWidth="1.5" strokeDasharray="4 2" />
          <rect x={paddingX - 58} y={excBottomY - 8} width="52" height="16" fill="#ffffff" stroke="#cbd5e1" rx="2" />
          <text x={paddingX - 32} y={excBottomY + 4} fill="#64748b" fontSize="9" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
            EL -{H.toFixed(1)}m
          </text>

          {/* 2. 스팬별 구획선 & 종방향 기둥/가시설 렌더링 */}
          {dailyStates.map((state, sIdx) => {
            const spanX = paddingX + sIdx * (spanLength * scaleX);
            const spanW = spanLength * scaleX;
            const isSelected = selectedSpanIdx === sIdx;
            const spanCenterX = spanX + spanW / 2;

            const {
              foundationStatus,
              storyStates,
              topSlabStatus,
              kingPostStatus,
              strutReleaseStatus
            } = state;

            const isStrutDismantling = strutReleaseStatus === 'in_progress';
            const isStrutWaiting = strutReleaseStatus === 'curing_waiting';

            return (
              <g key={`span-profile-story-${sIdx}`} onClick={() => onSelectSpan(sIdx)} className="cursor-pointer">
                {/* 스팬 수직 경계선 */}
                <line x1={spanX} y1={groundY - 15} x2={spanX} y2={excBottomY} stroke={isSelected ? '#2563eb' : '#cbd5e1'} strokeWidth={isSelected ? '2' : '1'} strokeDasharray={isSelected ? 'none' : '3 3'} />
                {sIdx === numSpans - 1 && (
                  <line x1={spanX + spanW} y1={groundY - 15} x2={spanX + spanW} y2={excBottomY} stroke="#cbd5e1" strokeWidth="1" strokeDasharray="3 3" />
                )}

                {/* 🌟 실시간 작업팀(Crew) 아바타 뱃지 */}
                {(() => {
                  let teamBadge = null;
                  if (isStrutDismantling) {
                    teamBadge = { text: '✂️ 해체팀', bg: '#fee2e2', border: '#ef4444', color: '#991b1b' };
                  } else if (isStrutWaiting) {
                    teamBadge = { text: '⏳ 양생대기', bg: '#fef3c7', border: '#f59e0b', color: '#92400e' };
                  } else if (topSlabStatus === 'in_progress' || storyStates.some(s => s.slabStatus === 'in_progress')) {
                    teamBadge = { text: '🚛 타설팀', bg: '#d1fae5', border: '#10b981', color: '#065f46' };
                  } else if (storyStates.some(s => s.wallStatus === 'in_progress')) {
                    teamBadge = { text: '🏗️ 철근팀', bg: '#dbeafe', border: '#3b82f6', color: '#1e40af' };
                  } else if (foundationStatus === 'in_progress') {
                    teamBadge = { text: '🔨 거푸집팀', bg: '#ffedd5', border: '#f97316', color: '#9a3412' };
                  } else if (topSlabStatus === 'completed') {
                    teamBadge = { text: '✅ 완료', bg: '#f1f5f9', border: '#cbd5e1', color: '#475569' };
                  }

                  return (
                    <g>
                      {/* 스팬 번호 라벨 */}
                      <rect x={spanX + 2} y={groundY - 32} width={spanW - 4} height={15} fill={isSelected ? '#dbeafe' : '#f8fafc'} stroke={isSelected ? '#3b82f6' : '#e2e8f0'} rx="2" />
                      <text x={spanCenterX} y={groundY - 21} fill={isSelected ? '#1d4ed8' : '#475569'} fontSize="8.5" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                        {state.spanName}
                      </text>

                      {/* 실시간 투입 작업팀 뱃지 */}
                      {teamBadge && (
                        <g>
                          <rect x={spanCenterX - 35} y={groundY - 50} width="70" height="15" rx="3" fill={teamBadge.bg} stroke={teamBadge.border} strokeWidth="1" />
                          <text x={spanCenterX} y={groundY - 39} fill={teamBadge.color} fontSize="8" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                            {teamBadge.text}
                          </text>
                        </g>
                      )}
                    </g>
                  );
                })()}

                {/* 중간말뚝 (King Post) */}
                {hasKingPost && (
                  <g opacity={kingPostStatus === 'released' ? 0.25 : 1}>
                    <line x1={spanCenterX} y1={groundY - 10} x2={spanCenterX} y2={excBottomY} stroke={kingPostStatus === 'released' ? '#94a3b8' : '#d97706'} strokeWidth="4" strokeDasharray={kingPostStatus === 'released' ? '4 4' : 'none'} />
                  </g>
                )}

                {/* 버팀보 (Strut) 및 해체/절단/인양 애니메이션 */}
                {!isAnchor && strutLevels.map((sy, lIdx) => {
                  const storyIdx = Math.min(numStories - 1, Math.floor(((excBottomY - sy) / (excBottomY - groundY)) * numStories));
                  const isStoryReleased = storyStates[storyIdx]?.strutReleased ?? false;

                  return (
                    <g key={`strut-profile-node-${sIdx}-${lIdx}`}>
                      {isStoryReleased ? (
                        /* 해체 완료 (점선 잔상) */
                        <g opacity="0.2">
                          <line x1={spanX + 4} y1={sy} x2={spanX + spanW - 4} y2={sy} stroke="#94a3b8" strokeWidth="2" strokeDasharray="3 3" />
                        </g>
                      ) : isStrutWaiting ? (
                        /* 14MPa 강도대기 */
                        <g>
                          <rect x={spanX + 4} y={sy - 3} width={spanW - 8} height="6" fill="#f59e0b" rx="2" stroke="#d97706" strokeWidth="1" />
                          {lIdx === 0 && (
                            <g>
                              <rect x={spanCenterX - 45} y={sy - 18} width="90" height="14" fill="#fffbeb" stroke="#f59e0b" rx="2" />
                              <text x={spanCenterX} y={sy - 8} fill="#b45309" fontSize="8" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                                ⏳ 14MPa 양생대기
                              </text>
                            </g>
                          )}
                        </g>
                      ) : (
                        /* 정상 가설 상태 */
                        <rect x={spanX + 4} y={sy - 3} width={spanW - 8} height="6" fill={isCompStrut ? '#a855f7' : '#ef4444'} rx="2" />
                      )}
                    </g>
                  );
                })}

                {/* ============================================================= */}
                {/* 층수 연동 RC 본체 구조물 타설 렌더링 */}
                {/* ============================================================= */}

                {/* 1. 바닥 기초 (Invert Mat Foundation - 두께 1.8m) */}
                {foundationStatus !== 'not_started' && (
                  <g>
                    <rect
                      x={spanX + 1}
                      y={excBottomY - 1.8 * scaleY}
                      width={spanW - 2}
                      height={1.8 * scaleY}
                      fill={foundationStatus === 'completed' ? 'url(#concDoneProfileStory)' : 'url(#concProgProfileStory)'}
                      stroke="#0f172a"
                      strokeWidth="1.5"
                    />
                    {sIdx === 0 && (
                      <text x={spanX + 8} y={excBottomY - 0.7 * scaleY} fill="#1e293b" fontSize="8.5" fontFamily="monospace" fontWeight="bold">
                        기초 t=1.8m
                      </text>
                    )}
                  </g>
                )}

                {/* 2. 층별 벽체 및 중간 슬래브 */}
                {storyStates.map((st, stIdx) => {
                  const fBottomY = storyFloorYs[stIdx];
                  const fTopY = storyFloorYs[stIdx + 1];
                  const isTopStory = stIdx === numStories - 1;

                  return (
                    <g key={`profile-st-render-${sIdx}-${stIdx}`}>
                      {/* 층별 벽체/단면 */}
                      {st.wallStatus !== 'not_started' && (
                        <rect
                          x={spanX + 1}
                          y={fTopY}
                          width={spanW - 2}
                          height={fBottomY - fTopY}
                          fill={st.wallStatus === 'completed' ? 'url(#concDoneProfileStory)' : 'url(#concProgProfileStory)'}
                          stroke="#1e293b"
                          strokeWidth="1"
                        />
                      )}

                      {/* 층별 중간 슬래브 (두께 0.8m) */}
                      {!isTopStory && st.slabStatus !== 'not_started' && (
                        <g>
                          <rect
                            x={spanX + 1}
                            y={fTopY}
                            width={spanW - 2}
                            height={0.8 * scaleY}
                            fill={st.slabStatus === 'completed' ? 'url(#concDoneProfileStory)' : 'url(#concProgProfileStory)'}
                            stroke="#0f172a"
                            strokeWidth="1.5"
                          />
                          {sIdx === 0 && (
                            <text x={spanX + 8} y={fTopY + 0.6 * scaleY} fill="#0f172a" fontSize="8" fontFamily="monospace" fontWeight="bold">
                              중간슬래브 t=0.8m
                            </text>
                          )}
                        </g>
                      )}
                    </g>
                  );
                })}

                {/* 3. 최상부 슬래브 (Top Roof Slab - 두께 1.2m) */}
                {topSlabStatus !== 'not_started' && (
                  <g>
                    <rect
                      x={spanX + 1}
                      y={topSlabTopY}
                      width={spanW - 2}
                      height={1.2 * scaleY}
                      fill={topSlabStatus === 'completed' ? 'url(#concDoneProfileStory)' : 'url(#concProgProfileStory)'}
                      stroke="#0f172a"
                      strokeWidth="1.8"
                    />
                    {sIdx === 0 && (
                      <text x={spanX + 8} y={topSlabTopY + 0.9 * scaleY} fill="#0f172a" fontSize="8.5" fontFamily="monospace" fontWeight="bold">
                        지붕슬래브 t=1.2m
                      </text>
                    )}
                  </g>
                )}

                {/* 선택된 스팬 하이라이트 박스 */}
                {isSelected && (
                  <rect x={spanX} y={groundY} width={spanW} height={excBottomY - groundY} fill="#3b82f6" fillOpacity="0.06" stroke="#2563eb" strokeWidth="2" strokeDasharray="4 2" />
                )}
              </g>
            );
          })}

          {/* 하단 종방향 거리 눈금자 */}
          <g>
            <line x1={paddingX} y1={excBottomY + 20} x2={paddingX + drawW} y2={excBottomY + 20} stroke="#94a3b8" strokeWidth="1" />
            {Array.from({ length: numSpans + 1 }).map((_, idx) => {
              const x = paddingX + idx * (spanLength * scaleX);
              const dist = idx * spanLength;
              return (
                <g key={`dist-tick-story-${idx}`}>
                  <line x1={x} y1={excBottomY + 16} x2={x} y2={excBottomY + 24} stroke="#94a3b8" strokeWidth="1" />
                  <text x={x} y={excBottomY + 34} fill="#64748b" fontSize="8" fontFamily="monospace" textAnchor="middle">
                    {dist.toFixed(0)}m
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
      </div>

      {/* 하단 종단면도 핵심 가이드 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 text-[11px] pt-1">
        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">① 지하 {numStories}층 구조물 모델링</span>
          <p className="text-slate-600">
            굴착 깊이 {H.toFixed(1)}m에 따라 <strong>{storyNames.join(' → ')}</strong>로 층별 순차 축조됩니다.
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">② 층별 버팀보 순차 해체</span>
          <p className="text-slate-600">
            하부층 벽체 콘크리트 강도(14MPa) 발현 후 해당 단 버팀보가 순차 절단/인양되며 상부층 공간이 확보됩니다.
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">③ 스팬 블록 직접 선택</span>
          <p className="text-slate-600">
            종단면도 상의 각 스팬(Span 1 ~ {numSpans})을 직접 클릭하여 해당 위치의 진행 상황을 즉시 조회할 수 있습니다.
          </p>
        </div>
      </div>
    </div>
  );
};
