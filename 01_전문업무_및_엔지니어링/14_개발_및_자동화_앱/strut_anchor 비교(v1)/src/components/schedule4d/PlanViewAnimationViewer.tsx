import React from 'react';
import { SpanDailyState, AlternativeSpanScheduleResult } from '../../engine/structureScheduleEngine';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { Map, AlertTriangle, ShieldCheck, CheckCircle2, ArrowRight } from 'lucide-react';

interface PlanViewAnimationViewerProps {
  inputs: ProjectInputs;
  selectedAlt: AlternativeSpec;
  schedule: AlternativeSpanScheduleResult;
  dailyStates: SpanDailyState[];
  currentDay: number;
  selectedSpanIdx: number;
  onSelectSpan: (idx: number) => void;
}

export const PlanViewAnimationViewer: React.FC<PlanViewAnimationViewerProps> = ({
  inputs,
  selectedAlt,
  schedule,
  dailyStates,
  currentDay,
  selectedSpanIdx,
  onSelectSpan
}) => {
  const B = inputs.excavationWidth;
  const totalLength = schedule.totalLengthM;
  const numSpans = schedule.numSpans;
  const spanLength = schedule.spanLengthM;

  const isAnchor = selectedAlt.type === 'ALL_ANCHOR';
  const isCompStrut = selectedAlt.type === 'COMPOSITE_STRUT';
  const hasKingPost = selectedAlt.type === 'ALL_STRUT' || (selectedAlt.type === 'HYBRID' && B >= 20);

  // SVG 좌표계 (가로: 연장 L, 세로: 굴착폭 B)
  const svgWidth = 960;
  const svgHeight = 360;
  const paddingX = 60;
  const paddingTop = 50;
  const paddingBottom = 45;

  const drawW = svgWidth - paddingX * 2;
  const drawH = svgHeight - paddingTop - paddingBottom;

  const scaleX = drawW / totalLength;
  const scaleY = drawH / Math.max(12, B);

  const topWallY = paddingTop;
  const bottomWallY = topWallY + B * scaleY;
  const centerY = (topWallY + bottomWallY) / 2;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
      {/* 헤더 바 */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-teal-50 text-teal-600">
            <Map className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold text-slate-800">
                평면도 실시간 축조 진행 & 가시설 배치 현황 (Top Plan View)
              </h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-teal-100 text-teal-800 font-mono">
                L = {totalLength.toFixed(0)}m × B = {B.toFixed(1)}m | Day {currentDay}/{schedule.totalDurationDays}일
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              상공에서 바라본 120m 평면 축조 릴레이 및 스팬별 버팀보 격자 해체 상태 묘사
            </p>
          </div>
        </div>

        {/* 범례 */}
        <div className="flex items-center gap-3 text-[10px] text-slate-600 font-medium">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-emerald-500"></span> 바닥/슬래브 타설중
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-amber-400"></span> 14MPa 양생대기
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-slate-500"></span> 슬래브 완료
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded bg-rose-500"></span> 버팀보 해체구간
          </span>
        </div>
      </div>

      {/* SVG 평면도 캔버스 */}
      <div className="relative bg-slate-50 rounded-lg overflow-hidden border border-slate-300 shadow-inner flex justify-center">
        <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full h-auto max-h-[400px] select-none">
          <defs>
            {/* 패턴: 미타설 굴착 바닥 */}
            <pattern id="planSoilGround" width="14" height="14" patternUnits="userSpaceOnUse">
              <rect width="14" height="14" fill="#f8fafc" />
              <circle cx="7" cy="7" r="0.8" fill="#e2e8f0" />
            </pattern>
            {/* 패턴: 콘크리트 완료 */}
            <pattern id="planConcDone" width="12" height="12" patternUnits="userSpaceOnUse">
              <rect width="12" height="12" fill="#94a3b8" />
              <circle cx="3" cy="3" r="0.8" fill="#cbd5e1" />
              <circle cx="9" cy="9" r="0.8" fill="#cbd5e1" />
            </pattern>
            {/* 패턴: 타설 진행중 */}
            <pattern id="planConcProg" width="12" height="12" patternUnits="userSpaceOnUse">
              <rect width="12" height="12" fill="#10b981" />
              <path d="M0 12 L12 0" stroke="#a7f3d0" strokeWidth="2.0" />
            </pattern>
          </defs>

          {/* 1. 상부 & 하부 배면 지반 */}
          <rect x="0" y="0" width={svgWidth} height={topWallY} fill="#f1f5f9" />
          <rect x="0" y={bottomWallY} width={svgWidth} height={svgHeight - bottomWallY} fill="#f1f5f9" />

          {/* 2. 상부 & 하부 H-Pile 엄지말뚝 벽체 라인 */}
          <rect x={paddingX} y={topWallY - 5} width={drawW} height="5" fill="#2563eb" />
          <rect x={paddingX} y={bottomWallY} width={drawW} height="5" fill="#2563eb" />
          <text x={paddingX - 45} y={topWallY} fill="#2563eb" fontSize="9" fontFamily="sans-serif" fontWeight="bold">
            좌측벽체
          </text>
          <text x={paddingX - 45} y={bottomWallY + 4} fill="#2563eb" fontSize="9" fontFamily="sans-serif" fontWeight="bold">
            우측벽체
          </text>

          {/* 3. 어스앵커 배면 그라우팅선 (Anchor안인 경우) */}
          {isAnchor && (
            <g>
              {Array.from({ length: Math.ceil(totalLength / 5) }).map((_, aIdx) => {
                const ax = paddingX + aIdx * (5 * scaleX);
                return (
                  <g key={`anchor-plan-${aIdx}`}>
                    {/* 상단 앵커선 */}
                    <line x1={ax} y1={topWallY} x2={ax} y2={topWallY - 24} stroke="#0284c7" strokeWidth="2" strokeDasharray="3 2" />
                    <circle cx={ax} cy={topWallY - 24} r="2.5" fill="#0369a1" />
                    {/* 하단 앵커선 */}
                    <line x1={ax} y1={bottomWallY} x2={ax} y2={bottomWallY + 24} stroke="#0284c7" strokeWidth="2" strokeDasharray="3 2" />
                    <circle cx={ax} cy={bottomWallY + 24} r="2.5" fill="#0369a1" />
                  </g>
                );
              })}
            </g>
          )}

          {/* 4. 스팬별 평면 영역 및 타설 상태 렌더링 */}
          {dailyStates.map((state, sIdx) => {
            const spanX = paddingX + sIdx * (spanLength * scaleX);
            const spanW = spanLength * scaleX;
            const isSelected = selectedSpanIdx === sIdx;
            const spanCenterX = spanX + spanW / 2;

            const {
              foundationStatus,
              topSlabStatus,
              strutReleaseStatus,
              overallSpanProgress,
              kingPostStatus
            } = state;

            const isStrutDismantling = strutReleaseStatus === 'in_progress';
            const isStrutReleased = strutReleaseStatus === 'completed' || strutReleaseStatus === 'released';
            const isStrutWaiting = strutReleaseStatus === 'curing_waiting';

            // 평면 콘크리트 상태 결정 (슬래브 완료 > 기초 완료 > 타설중 > 미착수)
            let fillPattern = 'url(#planSoilGround)';
            if (topSlabStatus === 'completed') fillPattern = 'url(#planConcDone)';
            else if (overallSpanProgress > 0) fillPattern = 'url(#planConcProg)';

            return (
              <g key={`plan-span-${sIdx}`} onClick={() => onSelectSpan(sIdx)} className="cursor-pointer">
                {/* 스팬 평면 바닥 슬래브 타설 영역 */}
                <rect
                  x={spanX}
                  y={topWallY}
                  width={spanW}
                  height={bottomWallY - topWallY}
                  fill={fillPattern}
                  stroke="#cbd5e1"
                  strokeWidth="1"
                />

                {/* 스팬 수직 분할 경계선 */}
                <line x1={spanX} y1={topWallY - 10} x2={spanX} y2={bottomWallY + 10} stroke={isSelected ? '#2563eb' : '#94a3b8'} strokeWidth={isSelected ? '2' : '1'} strokeDasharray={isSelected ? 'none' : '3 3'} />

                {/* 스팬 상단 라벨 */}
                <text x={spanCenterX} y={topWallY - 14} fill={isSelected ? '#1d4ed8' : '#475569'} fontSize="9" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                  {state.spanName}
                </text>

                {/* ------------------------------------------------------------- */}
                {/* 평면 버팀보 파이프 (Strut) 횡방향 배치 */}
                {/* ------------------------------------------------------------- */}
                {!isAnchor && (
                  <g>
                    {/* 스팬 내 2~3본의 횡방향 버팀보 */}
                    {[0.25, 0.5, 0.75].map((posRatio, pIdx) => {
                      const sx = spanX + spanW * posRatio;
                      return (
                        <g key={`strut-pipe-${pIdx}`} opacity={isStrutReleased ? 0.2 : 1}>
                          <line
                            x1={sx}
                            y1={topWallY}
                            x2={sx}
                            y2={bottomWallY}
                            stroke={isStrutReleased ? '#94a3b8' : isStrutDismantling ? '#f43f5e' : isStrutWaiting ? '#f59e0b' : isCompStrut ? '#9333ea' : '#ef4444'}
                            strokeWidth={isStrutDismantling ? '3' : '4'}
                            strokeDasharray={isStrutReleased ? '4 3' : isStrutDismantling ? '3 2' : 'none'}
                          />
                        </g>
                      );
                    })}

                    {/* 버팀보 해체/절단 상태 뱃지 */}
                    {isStrutDismantling && (
                      <g>
                        <rect x={spanCenterX - 35} y={centerY - 10} width="70" height="20" fill="#fff1f2" stroke="#f43f5e" rx="3" />
                        <text x={spanCenterX} y={centerY + 3} fill="#e11d48" fontSize="8" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                          ✂️ 버팀보 해체중
                        </text>
                      </g>
                    )}

                    {isStrutWaiting && (
                      <g>
                        <rect x={spanCenterX - 40} y={centerY - 10} width="80" height="20" fill="#fffbeb" stroke="#f59e0b" rx="3" />
                        <text x={spanCenterX} y={centerY + 3} fill="#b45309" fontSize="8" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                          ⏳ 14MPa 양생
                        </text>
                      </g>
                    )}
                  </g>
                )}

                {/* ------------------------------------------------------------- */}
                {/* 중간말뚝 (King Post) 평면 중심점 */}
                {/* ------------------------------------------------------------- */}
                {hasKingPost && (
                  <circle
                    cx={spanCenterX}
                    cy={centerY}
                    r="4.5"
                    fill={kingPostStatus === 'released' ? '#cbd5e1' : '#d97706'}
                    stroke="#1e293b"
                    strokeWidth="1.2"
                  />
                )}

                {/* 스팬 상태 요약 텍스트 */}
                <rect x={spanCenterX - 32} y={bottomWallY - 22} width="64" height="15" fill="#ffffff" fillOpacity="0.9" stroke="#cbd5e1" rx="2" />
                <text x={spanCenterX} y={bottomWallY - 11} fill="#1e293b" fontSize="8" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                  {overallSpanProgress >= 100 ? '축조 완료' : overallSpanProgress > 0 ? `진행 (${overallSpanProgress}%)` : '착수 대기'}
                </text>

                {/* 선택 스팬 하이라이트 테두리 */}
                {isSelected && (
                  <rect x={spanX} y={topWallY} width={spanW} height={bottomWallY - topWallY} fill="#3b82f6" fillOpacity="0.08" stroke="#2563eb" strokeWidth="2.5" />
                )}
              </g>
            );
          })}

          {/* 치수선: 굴착 폭 B */}
          <g>
            <line x1={paddingX + drawW + 15} y1={topWallY} x2={paddingX + drawW + 15} y2={bottomWallY} stroke="#475569" strokeWidth="1" />
            <line x1={paddingX + drawW + 10} y1={topWallY} x2={paddingX + drawW + 20} y2={topWallY} stroke="#475569" strokeWidth="1" />
            <line x1={paddingX + drawW + 10} y1={bottomWallY} x2={paddingX + drawW + 20} y2={bottomWallY} stroke="#475569" strokeWidth="1" />
            <text x={paddingX + drawW + 35} y={centerY + 3} fill="#0f172a" fontSize="9" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
              B={B.toFixed(1)}m
            </text>
          </g>

          {/* 치수선: 총 연장 L */}
          <g>
            <line x1={paddingX} y1={bottomWallY + 22} x2={paddingX + drawW} y2={bottomWallY + 22} stroke="#475569" strokeWidth="1" />
            {Array.from({ length: numSpans + 1 }).map((_, idx) => {
              const x = paddingX + idx * (spanLength * scaleX);
              return (
                <g key={`plan-tick-${idx}`}>
                  <line x1={x} y1={bottomWallY + 18} x2={x} y2={bottomWallY + 26} stroke="#475569" strokeWidth="1" />
                  <text x={x} y={bottomWallY + 36} fill="#64748b" fontSize="8" fontFamily="monospace" textAnchor="middle">
                    {(idx * spanLength).toFixed(0)}m
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
      </div>

      {/* 하단 평면도 해설 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 text-[11px] pt-1">
        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">① 전체 120m 공간 조망</span>
          <p className="text-slate-600">
            상공에서 평면 전체를 조망하여 현재 어떤 스팬에서 바닥 타설, 버팀보 해체, 슬래브 타설이 일어나는지 한눈에 파악합니다.
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">② 횡방향 버팀보 격자 해체</span>
          <p className="text-slate-600">
            {isAnchor
              ? '내부 무지보(Open Cut) 공간으로 횡방향 장애물 없이 100% 개방 시공.'
              : '붉은색 횡방향 버팀보가 순차적으로 해체/점선화되며 다음 단계 상부 슬래브 타설 공간이 확보됩니다.'}
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">③ 스팬 직접 클릭 연동</span>
          <p className="text-slate-600">
            원하는 평면 스팬 블록을 클릭하면 간트차트 및 횡단면도가 해당 위치로 즉시 동기화됩니다.
          </p>
        </div>
      </div>
    </div>
  );
};
