import React from 'react';
import { SpanDailyState, AlternativeSpanScheduleResult, StructureScheduleEngine } from '../../engine/structureScheduleEngine';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { Building, AlertTriangle, ShieldCheck, CheckCircle2, ArrowRight } from 'lucide-react';

interface CrossSectionAnimationViewerProps {
  inputs: ProjectInputs;
  selectedAlt: AlternativeSpec;
  schedule: AlternativeSpanScheduleResult;
  selectedSpanState: SpanDailyState;
  currentDay: number;
}

export const CrossSectionAnimationViewer: React.FC<CrossSectionAnimationViewerProps> = ({
  inputs,
  selectedAlt,
  schedule,
  selectedSpanState,
  currentDay
}) => {
  const H = inputs.excavationDepth;
  const B = inputs.excavationWidth;
  const isAnchor = selectedAlt.type === 'ALL_ANCHOR';
  const isHybrid = selectedAlt.type === 'HYBRID';
  const isCompStrut = selectedAlt.type === 'COMPOSITE_STRUT';
  const hasKingPost = selectedAlt.type === 'ALL_STRUT' || (selectedAlt.type === 'HYBRID' && B >= 20);

  const { numStories, storyNames } = StructureScheduleEngine.determineStationStories(H);

  // SVG 좌표계 셋업
  const svgWidth = 800;
  const svgHeight = 440;
  const paddingX = 80;
  const paddingTop = 50;
  const paddingBottom = 40;

  const drawW = svgWidth - paddingX * 2;
  const drawH = svgHeight - paddingTop - paddingBottom;

  const scaleX = drawW / Math.max(15, B);
  const scaleY = drawH / Math.max(10, H + 3);

  const leftWallX = paddingX;
  const rightWallX = paddingX + B * scaleX;
  const groundY = paddingTop;
  const excBottomY = groundY + H * scaleY;
  const wallBottomY = excBottomY + 3.0 * scaleY;

  // 슬래브 두께 및 벽체 두께
  const slabThick = 0.8 * scaleY;
  const wallThick = 0.8 * scaleX;

  // 상부 토피 피복고 (사용자 요청: 약 5.0m 피복 가정)
  const overburdenDepth = 5.0;

  // 바닥 기초 및 최상단 지붕 슬래브 위치 (GL 아래 5.0m에 지붕슬래브 위치)
  const baseSlabTopY = excBottomY - 1.0 * scaleY;
  const topSlabTopY = groundY + overburdenDepth * scaleY; // 상부 5.0m 피복
  const topSlabBottomY = topSlabTopY + 1.0 * scaleY;

  // 층별 Y 좌표 계산 (최하층 바닥부터 상부 슬래브까지)
  const totalBoxHeight = Math.max(2.0, baseSlabTopY - topSlabBottomY);
  const storyHeight = totalBoxHeight / Math.max(1, numStories);

  // storyLevels: 각 층 바닥/슬래브 Y 좌표 목록
  const storyFloorYs = Array.from({ length: numStories + 1 }).map((_, idx) => {
    return baseSlabTopY - idx * storyHeight;
  });

  // 버팀보 단수 및 Y 위치
  const strutLevels = selectedAlt.supports.map(s => groundY + s.depth * scaleY);
  const kingPostCenterX = leftWallX + (B * scaleX) / 2;

  const {
    foundationStatus,
    foundationProgress,
    storyStates,
    topSlabStatus,
    topSlabProgress,
    kingPostStatus,
    isStrutInterfering
  } = selectedSpanState;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
      {/* 헤더 & 실시간 상태 알림 */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 text-blue-600">
            <Building className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold text-slate-800">
                {selectedSpanState.spanName} 2D 횡단면 실시간 축조 뷰 [지하 {numStories}층 구조물]
              </h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">
                굴착심도 {H.toFixed(1)}m 연동 (Day {currentDay} / {schedule.totalDurationDays}일)
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              현재 활성 작업: <span className="font-bold text-slate-800">{selectedSpanState.currentActiveTaskName}</span>
            </p>
          </div>
        </div>

        {/* 간섭/무간섭 상태 뱃지 */}
        <div>
          {isAnchor ? (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>무지보 개방 공간 (간섭 0개 / 지하 {numStories}층 쾌적 시공)</span>
            </div>
          ) : isStrutInterfering ? (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-100 border border-amber-300 text-amber-900 text-xs font-bold animate-pulse">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>버팀보 간섭 발생 (양생 강도 14MPa 대기 후 해체)</span>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-bold">
              <span>가시설 지보 간섭 제어 상태</span>
            </div>
          )}
        </div>
      </div>

      {/* 2D SVG 그래픽 캔버스 */}
      <div className="relative bg-slate-50 rounded-lg overflow-hidden border border-slate-300 shadow-inner flex justify-center">
        <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full h-auto max-h-[460px] select-none">
          <defs>
            {/* 패턴: 밝은 미굴착 배면 지반 */}
            <pattern id="soilGroundLightCS" width="16" height="16" patternUnits="userSpaceOnUse">
              <rect width="16" height="16" fill="#f1f5f9" />
              <path d="M0 16 L16 0 M0 8 L8 0 M8 16 L16 8" stroke="#cbd5e1" strokeWidth="0.9" />
            </pattern>
            {/* 패턴: 콘크리트 타설 완료 */}
            <pattern id="concreteFinishedCS" width="12" height="12" patternUnits="userSpaceOnUse">
              <rect width="12" height="12" fill="#94a3b8" />
              <circle cx="3" cy="3" r="0.9" fill="#e2e8f0" />
              <circle cx="9" cy="9" r="0.9" fill="#e2e8f0" />
              <circle cx="9" cy="3" r="0.7" fill="#64748b" />
            </pattern>
            {/* 패턴: 타설 진행중 */}
            <pattern id="concreteInProgressCS" width="12" height="12" patternUnits="userSpaceOnUse">
              <rect width="12" height="12" fill="#10b981" />
              <path d="M0 12 L12 0" stroke="#a7f3d0" strokeWidth="2.0" />
            </pattern>
            {/* 그림자 필터 */}
            <filter id="softShadowCS" x="-5%" y="-5%" width="110%" height="110%">
              <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" floodColor="#0f172a" floodOpacity="0.15" />
            </filter>
          </defs>

          {/* 1. 배경 지반 */}
          <rect x="0" y={groundY} width={leftWallX} height={svgHeight - groundY} fill="url(#soilGroundLightCS)" />
          <rect x={rightWallX} y={groundY} width={svgWidth - rightWallX} height={svgHeight - groundY} fill="url(#soilGroundLightCS)" />
          <rect x={leftWallX} y={excBottomY} width={B * scaleX} height={svgHeight - excBottomY} fill="#e2e8f0" />
          <rect x={leftWallX} y={groundY} width={B * scaleX} height={excBottomY - groundY} fill="#ffffff" />

          {/* 🌟 상부 지표면 (GL ±0.00m 도로/노면 라인) */}
          <line x1="0" y1={groundY} x2={svgWidth} y2={groundY} stroke="#1e293b" strokeWidth="2.5" />
          {/* 지표면 잔디/노면 블록 */}
          <rect x="0" y={groundY - 4} width={svgWidth} height="4" fill="#64748b" opacity="0.4" />
          <rect x="12" y={groundY - 24} width="84" height="20" fill="#ffffff" stroke="#1e293b" strokeWidth="1.2" rx="3" filter="url(#softShadowCS)" />
          <text x="54" y={groundY - 10} fill="#0f172a" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
            ▼ GL ±0.00m
          </text>

          {/* 🌟 상부 5.0m 토피 피복 구간 치수선 및 해칭 */}
          <g>
            {/* 좌측 피복 치수선 */}
            <line x1={leftWallX - 35} y1={groundY} x2={leftWallX - 35} y2={topSlabTopY} stroke="#0284c7" strokeWidth="1.5" />
            <line x1={leftWallX - 40} y1={groundY} x2={leftWallX - 30} y2={groundY} stroke="#0284c7" strokeWidth="1.5" />
            <line x1={leftWallX - 40} y1={topSlabTopY} x2={leftWallX - 30} y2={topSlabTopY} stroke="#0284c7" strokeWidth="1.5" />
            <rect x={leftWallX - 78} y={groundY + (topSlabTopY - groundY) / 2 - 10} width="75" height="20" fill="#f0f9ff" stroke="#0284c7" strokeWidth="1" rx="3" />
            <text x={leftWallX - 40} y={groundY + (topSlabTopY - groundY) / 2 + 4} fill="#0369a1" fontSize="9" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
              피복 {overburdenDepth.toFixed(1)}m
            </text>

            {/* 구조물 상부 되메우기 피복 영역 (점선 가이드) */}
            <rect x={leftWallX} y={groundY} width={B * scaleX} height={topSlabTopY - groundY} fill="#f8fafc" fillOpacity="0.5" stroke="#94a3b8" strokeDasharray="3 3" strokeWidth="0.8" />
            <text x={kingPostCenterX} y={groundY + (topSlabTopY - groundY) / 2 + 4} fill="#94a3b8" fontSize="9" fontFamily="sans-serif" textAnchor="middle">
              [상부 토피 피복 및 지하매설물 통과 공간 (약 5.0m)]
            </text>
          </g>
          
          <line x1={leftWallX} y1={excBottomY} x2={rightWallX} y2={excBottomY} stroke="#64748b" strokeWidth="1.5" strokeDasharray="4 2" />
          <rect x={leftWallX + 8} y={excBottomY + 4} width="110" height="16" fill="#ffffff" stroke="#cbd5e1" rx="3" />
          <text x={leftWallX + 63} y={excBottomY + 16} fill="#475569" fontSize="9" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
            굴착저면 EL -{H.toFixed(1)}m
          </text>

          {/* 2. 엄지말뚝(H-Pile) */}
          <rect x={leftWallX - 8} y={groundY} width="8" height={wallBottomY - groundY} fill="#2563eb" filter="url(#softShadowCS)" />
          <rect x={rightWallX} y={groundY} width="8" height={wallBottomY - groundY} fill="#2563eb" filter="url(#softShadowCS)" />

          {/* 3. 어스앵커 (Anchor안) */}
          {isAnchor && selectedAlt.supports.map((s, sIdx) => {
            const sy = groundY + s.depth * scaleY;
            return (
              <g key={`anchor-cs-${sIdx}`}>
                <line x1={leftWallX} y1={sy} x2={leftWallX - 60} y2={sy + 35} stroke="#0284c7" strokeWidth="3" strokeDasharray="4 2" />
                <circle cx={leftWallX - 4} cy={sy} r="4" fill="#0369a1" />
                <line x1={rightWallX} y1={sy} x2={rightWallX + 60} y2={sy + 35} stroke="#0284c7" strokeWidth="3" strokeDasharray="4 2" />
                <circle cx={rightWallX + 4} cy={sy} r="4" fill="#0369a1" />
              </g>
            );
          })}

          {/* 4. 중간말뚝 (King Post) */}
          {hasKingPost && (
            <g opacity={kingPostStatus === 'released' ? 0.25 : 1}>
              <line x1={kingPostCenterX} y1={groundY - 15} x2={kingPostCenterX} y2={wallBottomY} stroke={kingPostStatus === 'released' ? '#94a3b8' : '#d97706'} strokeWidth="5" strokeDasharray={kingPostStatus === 'released' ? '4 4' : 'none'} />
              <rect x={kingPostCenterX - 55} y={groundY - 32} width="110" height="17" fill="#ffffff" stroke={kingPostStatus === 'released' ? '#cbd5e1' : '#f59e0b'} strokeWidth="1.2" rx="3" />
              <text x={kingPostCenterX} y={groundY - 20} fill={kingPostStatus === 'released' ? '#94a3b8' : '#b45309'} fontSize="9" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">
                {kingPostStatus === 'released' ? '중간말뚝 (인발완료)' : '중간말뚝 (King Post)'}
              </text>
            </g>
          )}

          {/* 5. 강관 버팀보 (Strut) 및 해체 상태 */}
          {!isAnchor && strutLevels.map((sy, sIdx) => {
            // 해당 버팀보가 어느 층에 속하는지 판정하여 해체 여부 연동
            const storyIdx = Math.min(numStories - 1, Math.floor(((excBottomY - sy) / (excBottomY - groundY)) * numStories));
            const isReleased = storyStates[storyIdx]?.strutReleased ?? false;

            return (
              <g key={`strut-cs-${sIdx}`} opacity={isReleased ? 0.25 : 1}>
                <rect x={leftWallX} y={sy - 4} width={B * scaleX} height="8" fill={isReleased ? '#94a3b8' : isCompStrut ? '#9333ea' : '#ef4444'} rx="3" filter="url(#softShadowCS)" />
                <rect x={leftWallX + 14} y={sy - 17} width="140" height="15" fill="#ffffff" stroke={isReleased ? '#cbd5e1' : isCompStrut ? '#c084fc' : '#fca5a5'} rx="3" />
                <text x={leftWallX + 84} y={sy - 6} fill={isReleased ? '#64748b' : '#b91c1c'} fontSize="9" textAnchor="middle" fontFamily="sans-serif" fontWeight="bold">
                  {isReleased ? `[Strut ${sIdx + 1}단 해체완료]` : `[Strut ${sIdx + 1}단 ${isCompStrut ? '광폭' : '강관'}버팀보]`}
                </text>
              </g>
            );
          })}

          {/* ========================================================================= */}
          {/* 지하 층수 연동 RC 본체 구조물 축조 렌더링 */}
          {/* ========================================================================= */}

          {/* 6. 바닥 기초 (Invert Slab) */}
          {foundationStatus !== 'not_started' && (
            <g>
              <rect x={leftWallX} y={baseSlabTopY} width={B * scaleX} height={1.0 * scaleY} fill={foundationStatus === 'completed' ? 'url(#concreteFinishedCS)' : 'url(#concreteInProgressCS)'} stroke="#1e293b" strokeWidth="1.5" />
              <rect x={kingPostCenterX - 90} y={baseSlabTopY + 0.5 * scaleY - 8} width="180" height="16" fill="#ffffff" fillOpacity="0.9" stroke="#334155" strokeWidth="0.8" rx="3" />
              <text x={kingPostCenterX} y={baseSlabTopY + 0.5 * scaleY + 4} fill="#0f172a" fontSize="9" textAnchor="middle" fontWeight="bold" fontFamily="sans-serif">
                바닥 기초(Invert) {foundationStatus === 'completed' ? '완료' : `타설중 (${Math.round(foundationProgress * 100)}%)`}
              </text>
            </g>
          )}

          {/* 7. 층별 벽체 및 중간 슬래브 렌더링 */}
          {storyStates.map((st, sIdx) => {
            const floorBottomY = storyFloorYs[sIdx];
            const floorTopY = storyFloorYs[sIdx + 1];
            const isTopStory = sIdx === numStories - 1;

            return (
              <g key={`story-render-${sIdx}`}>
                {/* (1) 해당 층 좌/우 외벽 */}
                {st.wallStatus !== 'not_started' && (
                  <g>
                    {/* 좌측 외벽 */}
                    <rect x={leftWallX} y={floorTopY} width={wallThick} height={floorBottomY - floorTopY} fill={st.wallStatus === 'completed' ? 'url(#concreteFinishedCS)' : 'url(#concreteInProgressCS)'} stroke="#1e293b" strokeWidth="1.2" />
                    {/* 우측 외벽 */}
                    <rect x={rightWallX - wallThick} y={floorTopY} width={wallThick} height={floorBottomY - floorTopY} fill={st.wallStatus === 'completed' ? 'url(#concreteFinishedCS)' : 'url(#concreteInProgressCS)'} stroke="#1e293b" strokeWidth="1.2" />
                    {/* 층별 텍스트 뱃지 */}
                    <rect x={leftWallX + wallThick + 6} y={floorBottomY - (floorBottomY - floorTopY) / 2 - 8} width="130" height="16" fill="#ffffff" fillOpacity="0.9" stroke="#cbd5e1" rx="3" />
                    <text x={leftWallX + wallThick + 71} y={floorBottomY - (floorBottomY - floorTopY) / 2 + 4} fill="#1e293b" fontSize="8" fontWeight="bold" textAnchor="middle" fontFamily="sans-serif">
                      {st.storyName} {st.wallStatus === 'completed' ? '타설완료' : '타설중'}
                    </text>
                  </g>
                )}

                {/* (2) 해당 층 상부 중간 슬래브 (최상층 제외) */}
                {!isTopStory && st.slabStatus !== 'not_started' && (
                  <g>
                    <rect x={leftWallX} y={floorTopY} width={B * scaleX} height={slabThick} fill={st.slabStatus === 'completed' ? 'url(#concreteFinishedCS)' : 'url(#concreteInProgressCS)'} stroke="#1e293b" strokeWidth="1.2" />
                    <rect x={kingPostCenterX - 85} y={floorTopY + slabThick / 2 - 8} width="170" height="16" fill="#ffffff" fillOpacity="0.9" stroke="#334155" strokeWidth="0.8" rx="3" />
                    <text x={kingPostCenterX} y={floorTopY + slabThick / 2 + 4} fill="#0f172a" fontSize="9" textAnchor="middle" fontWeight="bold" fontFamily="sans-serif">
                      {st.storyName} 상부 슬래브 {st.slabStatus === 'completed' ? '완료' : '타설중'}
                    </text>
                  </g>
                )}
              </g>
            );
          })}

          {/* 8. 최상부 지붕 슬래브 (Top Slab / Roof) */}
          {topSlabStatus !== 'not_started' && (
            <g>
              <rect x={leftWallX} y={topSlabTopY} width={B * scaleX} height={1.0 * scaleY} fill={topSlabStatus === 'completed' ? 'url(#concreteFinishedCS)' : 'url(#concreteInProgressCS)'} stroke="#1e293b" strokeWidth="1.5" />
              <rect x={kingPostCenterX - 90} y={topSlabTopY + 0.5 * scaleY - 8} width="180" height="16" fill="#ffffff" fillOpacity="0.9" stroke="#334155" strokeWidth="0.8" rx="3" />
              <text x={kingPostCenterX} y={topSlabTopY + 0.5 * scaleY + 4} fill="#0f172a" fontSize="9" textAnchor="middle" fontWeight="bold" fontFamily="sans-serif">
                최상부 지붕 슬래브(Roof) {topSlabStatus === 'completed' ? '타설완료' : `타설중 (${Math.round(topSlabProgress * 100)}%)`}
              </text>
            </g>
          )}

          {/* 치수선: 굴착 폭 B */}
          <g>
            <line x1={leftWallX} y1={groundY - 18} x2={rightWallX} y2={groundY - 18} stroke="#475569" strokeWidth="1" />
            <line x1={leftWallX} y1={groundY - 23} x2={leftWallX} y2={groundY - 13} stroke="#475569" strokeWidth="1" />
            <line x1={rightWallX} y1={groundY - 23} x2={rightWallX} y2={groundY - 13} stroke="#475569" strokeWidth="1" />
            <rect x={kingPostCenterX - 50} y={groundY - 30} width="100" height="15" fill="#ffffff" stroke="#cbd5e1" rx="3" />
            <text x={kingPostCenterX} y={groundY - 19} fill="#0f172a" fontSize="10" textAnchor="middle" fontFamily="monospace" fontWeight="bold">
              굴착 폭 B = {B.toFixed(1)}m
            </text>
          </g>
        </svg>
      </div>

      {/* 하단 층수별 엔지니어링 해설 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 text-[11px] pt-1">
        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">① 굴착 심도({H.toFixed(1)}m) 연동 층수</span>
          <p className="text-slate-600">
            심도에 따라 <strong>지하 {numStories}층 구조물({storyNames.join(' + ')})</strong>로 자동 모델링되어 층별 슬래브와 외벽이 순차 축조됩니다.
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">② 층별 중간 슬래브 축조</span>
          <p className="text-slate-600">
            하부층 벽체 타설 $\rightarrow$ 해당 층 버팀보 해체 $\rightarrow$ 상부 중간 바닥 슬래브(Concourse Slab) 타설 순으로 층별 상향 축조됩니다.
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="font-bold text-slate-800 block mb-0.5">③ 공법별 층당 능률 차이</span>
          <p className="text-slate-600">
            {isAnchor
              ? '무지보로 층당 거푸집 및 철근 배근 간섭이 전혀 없어 고속 일체 시공.'
              : '층마다 버팀보 관통 및 14MPa 강도 발현 대기로 층당 5~6일 추가 지연 발생.'}
          </p>
        </div>
      </div>
    </div>
  );
};
