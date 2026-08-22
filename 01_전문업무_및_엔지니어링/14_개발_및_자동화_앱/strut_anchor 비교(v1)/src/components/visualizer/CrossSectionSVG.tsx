import React from 'react';
import { AlternativeSpec, ProjectInputs } from '../../types';
import { Compass, Maximize2, ZoomIn, ZoomOut } from 'lucide-react';

interface CrossSectionSVGProps {
  alternative: AlternativeSpec;
  inputs: ProjectInputs;
  currentStageIdx?: number;
}

export const CrossSectionSVG: React.FC<CrossSectionSVGProps> = ({
  alternative,
  inputs,
  currentStageIdx = alternative.stageResults.length - 1
}) => {
  const stageRes = alternative.stageResults[currentStageIdx] || alternative.stageResults[alternative.stageResults.length - 1];
  const excDepth = stageRes.excavationDepth;
  const totalLength = alternative.wall.totalLength;
  const excWidth = inputs.excavationWidth;

  const isCompositeStrutAlt = alternative.type === 'COMPOSITE_STRUT';
  const isAllAnchorAlt = alternative.type === 'ALL_ANCHOR';

  const svgWidth = 840;
  const svgHeight = 540;
  const topMargin = 75;
  const leftMargin = 160;
  const groundY = topMargin + 25; // y = 100 (상부 넉넉한 공간 확보)

  const maxDepth = Math.max(totalLength + 3, 20);
  const scaleY = (svgHeight - groundY - 40) / maxDepth;
  // 굴착 폭(B) 변화에 맞춰 뷰포트 내 완벽 비율 자동 스케일링
  const scaleX = Math.min(16.0, Math.max(7.5, 380 / Math.max(12, excWidth)));

  const wallLeftX = leftMargin + 60;
  const wallRightX = wallLeftX + excWidth * scaleX;
  const boundaryX = wallLeftX - inputs.boundaryDistance * scaleX;

  return (
    <div className="eng-panel flex flex-col items-center">
      <div className="eng-panel-header w-full">
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-blue-600" />
          <div>
            <h3 className="text-xs font-bold text-slate-800 flex items-center gap-2">
              <span>2D 가시설 단면 뷰포트 (Cross-Section Viewport) — {alternative.name}</span>
              {isCompositeStrutAlt && (
                <span className="px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-800 text-[10px] font-bold border border-indigo-200">
                  ✨ 무중간말뚝 장지간 (Single-Span B={excWidth}m)
                </span>
              )}
            </h3>
            <p className="text-[11px] text-slate-500">
              시공단계: <strong>{stageRes.stageName}</strong> (현재 굴착고: <span className="text-blue-700 font-mono font-bold">-{excDepth.toFixed(1)}m</span> / 벽체연장: {totalLength.toFixed(1)}m)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-[11px] text-slate-600 font-medium">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-1.5 bg-cyan-500 inline-block rounded-sm"></span> 지하수위 (G.W.L)
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-1.5 bg-amber-500 inline-block rounded-sm"></span> 지보재 (Strut/Anchor)
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-1.5 bg-rose-500 inline-block rounded-sm"></span> 대지경계선
          </div>
        </div>
      </div>

      <div className="w-full p-3 flex justify-center bg-slate-100/60 overflow-x-auto">
        <div className="bg-white border border-slate-300 rounded shadow-inner p-1 cad-viewport">
          <svg width={svgWidth} height={svgHeight} className="select-none font-sans text-xs">
            <defs>
              {/* 공학 해치 패턴 */}
              <pattern id="soil-cad-hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" strokeWidth="0.8" opacity="0.4" />
              </pattern>
              {/* 합성사각강관 전용 해치 */}
              <pattern id="comp-box-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <line x1="0" y1="0" x2="0" y2="8" stroke="#3b82f6" strokeWidth="1" opacity="0.6" />
              </pattern>
              {/* 화살표 마커 */}
              <marker id="arrow-cad" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#d97706" />
              </marker>
            </defs>

            {/* 1. 지층 레이어 배경 */}
            {inputs.soils.map((soil) => {
              const y1 = groundY + soil.topDepth * scaleY;
              const y2 = groundY + soil.bottomDepth * scaleY;
              const h = y2 - y1;

              return (
                <g key={soil.id}>
                  {/* 좌측 배면 지반 */}
                  <rect x={20} y={y1} width={wallLeftX - 20} height={h} fill={soil.color} fillOpacity="0.2" />
                  <rect x={20} y={y1} width={wallLeftX - 20} height={h} fill="url(#soil-cad-hatch)" />

                  {/* 우측 배면 지반 */}
                  <rect x={wallRightX} y={y1} width={svgWidth - wallRightX - 20} height={h} fill={soil.color} fillOpacity="0.2" />
                  <rect x={wallRightX} y={y1} width={svgWidth - wallRightX - 20} height={h} fill="url(#soil-cad-hatch)" />

                  {/* 굴착저면 하부 중앙 지반 */}
                  {soil.bottomDepth * scaleY > excDepth * scaleY && (
                    <rect
                      x={wallLeftX}
                      y={Math.max(groundY + excDepth * scaleY, y1)}
                      width={excWidth * scaleX}
                      height={y2 - Math.max(groundY + excDepth * scaleY, y1)}
                      fill={soil.color}
                      fillOpacity="0.2"
                    />
                  )}

                  {/* 지층 경계선 및 텍스트 */}
                  <line x1={20} y1={y2} x2={svgWidth - 20} y2={y2} stroke="#94a3b8" strokeWidth="1" strokeDasharray="4 2" />
                  <text x={30} y={y1 + 14} fill="#334155" fontSize="10.5" fontWeight="bold">
                    {soil.name} (N={soil.NValue}, c={soil.cohesion}kN/m², φ={soil.frictionAngle}°)
                  </text>
                </g>
              );
            })}

            {/* 2. 대지경계선 */}
            {boundaryX > 20 && (
              <g>
                <line x1={boundaryX} y1={25} x2={boundaryX} y2={svgHeight - 20} stroke="#e11d48" strokeWidth="1.8" strokeDasharray="6 3" />
                <text x={boundaryX - 6} y={35} fill="#e11d48" fontSize="10" textAnchor="end" fontWeight="bold">
                  부지경계선 ({inputs.boundaryDistance}m)
                </text>
              </g>
            )}

            {/* 3. 상재하중 화살표 (배면 지표) */}
            <g>
              <rect x={40} y={groundY - 18} width={wallLeftX - 50} height={16} fill="#fef3c7" stroke="#d97706" strokeWidth="1" rx="2" />
              <text x={wallLeftX / 2 + 10} y={groundY - 6} fill="#b45309" fontSize="9.5" textAnchor="middle" fontWeight="bold">
                상재하중 q = {inputs.surcharge} kN/m²
              </text>
              {Array.from({ length: 6 }).map((_, i) => (
                <line
                  key={i}
                  x1={50 + i * ((wallLeftX - 70) / 5)}
                  y1={groundY - 15}
                  x2={50 + i * ((wallLeftX - 70) / 5)}
                  y2={groundY}
                  stroke="#d97706"
                  strokeWidth="1.8"
                  markerEnd="url(#arrow-cad)"
                />
              ))}
            </g>

            {/* 4. 지하수위선 (G.W.L) */}
            {inputs.waterTableBehind < maxDepth && (
              <g>
                <line
                  x1={20}
                  y1={groundY + inputs.waterTableBehind * scaleY}
                  x2={wallLeftX}
                  y2={groundY + inputs.waterTableBehind * scaleY}
                  stroke="#0284c7"
                  strokeWidth="2"
                  strokeDasharray="5 3"
                />
                <line
                  x1={wallRightX}
                  y1={groundY + inputs.waterTableBehind * scaleY}
                  x2={svgWidth - 20}
                  y2={groundY + inputs.waterTableBehind * scaleY}
                  stroke="#0284c7"
                  strokeWidth="2"
                  strokeDasharray="5 3"
                />
                <text x={35} y={groundY + inputs.waterTableBehind * scaleY - 5} fill="#0284c7" fontSize="10" fontWeight="bold">
                  ▼ G.W.L -{inputs.waterTableBehind.toFixed(1)}m
                </text>
              </g>
            )}

            {/* 5. 굴착 공간 및 바닥선 */}
            <rect
              x={wallLeftX}
              y={groundY}
              width={excWidth * scaleX}
              height={excDepth * scaleY}
              fill="#f8fafc"
              stroke="#cbd5e1"
              strokeWidth="1"
            />
            <line
              x1={wallLeftX}
              y1={groundY + excDepth * scaleY}
              x2={wallRightX}
              y2={groundY + excDepth * scaleY}
              stroke="#dc2626"
              strokeWidth="2.5"
            />
            <text x={wallLeftX + (excWidth * scaleX) / 2} y={groundY + excDepth * scaleY - 6} fill="#dc2626" fontSize="11" textAnchor="middle" fontWeight="bold">
              굴착 바닥면 (EL -{excDepth.toFixed(1)}m)
            </text>

            {/* 6. 좌/우 H-Pile 가시설 벽체 */}
            {/* 좌측 벽체 */}
            <rect
              x={wallLeftX - 6}
              y={groundY}
              width={12}
              height={totalLength * scaleY}
              fill="#2563eb"
              stroke="#1e40af"
              strokeWidth="1.5"
              rx="1"
            />
            {/* 우측 벽체 */}
            <rect
              x={wallRightX - 6}
              y={groundY}
              width={12}
              height={totalLength * scaleY}
              fill="#2563eb"
              stroke="#1e40af"
              strokeWidth="1.5"
              rx="1"
            />

            {/* 벽체 하단 토사/암반 근입장 */}
            <line
              x1={wallLeftX - 12}
              y1={groundY + totalLength * scaleY}
              x2={wallLeftX + 12}
              y2={groundY + totalLength * scaleY}
              stroke="#1e40af"
              strokeWidth="2.5"
            />
            <text x={wallLeftX + 14} y={groundY + totalLength * scaleY + 4} fill="#1e40af" fontSize="9.5" fontWeight="bold">
              근입하단 (EL -{totalLength.toFixed(1)}m)
            </text>

            {/* 7. 복공판(Deck Plate) 및 주형보(Deck Beam) & 교통하중 렌더링 */}
            {inputs.deckingConfig?.useDecking && (
              <g>
                {/* 상부 복공판 (Deck Plate) */}
                <rect
                  x={wallLeftX}
                  y={groundY - 10}
                  width={excWidth * scaleX}
                  height={10}
                  fill="#475569"
                  stroke="#1e293b"
                  strokeWidth="1.5"
                />
                {/* 복공판 요철 무늬 */}
                {Array.from({ length: Math.floor(excWidth / 2) }).map((_, i) => (
                  <line
                    key={i}
                    x1={wallLeftX + (i + 1) * 2 * scaleX}
                    y1={groundY - 10}
                    x2={wallLeftX + (i + 1) * 2 * scaleX}
                    y2={groundY}
                    stroke="#94a3b8"
                    strokeWidth="1"
                  />
                ))}

                {/* 주형보 (Deck Girder / Beam) */}
                <rect
                  x={wallLeftX}
                  y={groundY}
                  width={excWidth * scaleX}
                  height={8}
                  fill="#1e3a8a"
                  stroke="#172554"
                  strokeWidth="1.2"
                />

                {/* Level 2: 교통하중(차량) 뱃지 */}
                <g transform={`translate(${wallLeftX + (excWidth * scaleX) / 2 - 60}, ${groundY - 48})`}>
                  <rect x="0" y="0" width="120" height="20" rx="4" fill="#ffffff" stroke="#2563eb" strokeWidth="1.5" className="shadow-xs" />
                  <text x="60" y="14" fill="#1e40af" fontSize="10" fontWeight="bold" textAnchor="middle">
                    🚛 {inputs.deckingConfig.trafficLoadType || 'KL-510'} 교통하중
                  </text>
                </g>

                {/* Level 3: 복공 제원 텍스트 */}
                <g transform={`translate(${wallLeftX + 6}, ${groundY - 26})`}>
                  <rect x="0" y="0" width="230" height="15" rx="2" fill="#ffffff" fillOpacity="0.9" />
                  <text x="2" y="11" fill="#334155" fontSize="9.5" fontWeight="bold">
                    복공판 (t=200mm) + 주형보 ({inputs.deckingConfig.deckBeamSpec || 'H-400x400'})
                  </text>
                </g>
              </g>
            )}

            {/* 8. 중간말뚝 (King Post) - 합성사각강관(대안 4) 및 올앵커(대안 2)는 무중간말뚝으로 완전 제외 */}
            {!isCompositeStrutAlt && !isAllAnchorAlt && inputs.deckingConfig?.useDecking !== false && (() => {
              const kpLength = inputs.deckingConfig?.kingPostTotalLength || (excDepth + 5.0);
              const kpCenterX = wallLeftX + (excWidth * scaleX) / 2;
              return (
                <g>
                  {/* 중간말뚝 H-Pile 본체 */}
                  <rect
                    x={kpCenterX - 4}
                    y={groundY}
                    width={8}
                    height={kpLength * scaleY}
                    fill="#64748b"
                    stroke="#334155"
                    strokeWidth="1.5"
                    rx="1"
                  />
                  {/* 중간말뚝 캡 플레이트 */}
                  <rect
                    x={kpCenterX - 8}
                    y={groundY - 2}
                    width={16}
                    height={4}
                    fill="#334155"
                  />
                  {/* 중간말뚝 하단 암반 근입선 */}
                  <line
                    x1={kpCenterX - 10}
                    y1={groundY + kpLength * scaleY}
                    x2={kpCenterX + 10}
                    y2={groundY + kpLength * scaleY}
                    stroke="#334155"
                    strokeWidth="2"
                  />
                  <text x={kpCenterX + 12} y={groundY + kpLength * scaleY + 3} fill="#475569" fontSize="9" fontWeight="bold">
                    중간말뚝 근입 (EL -{kpLength.toFixed(1)}m)
                  </text>
                  {/* 중간말뚝 설명 라벨 */}
                  <g transform={`translate(${kpCenterX + 10}, ${groundY + 15})`}>
                    <rect x="0" y="0" width="190" height="16" rx="2" fill="#ffffff" fillOpacity="0.9" stroke="#cbd5e1" strokeWidth="0.8" />
                    <text x="4" y="12" fill="#334155" fontSize="9.5" fontWeight="bold">
                      중간말뚝 ({inputs.deckingConfig?.kingPostSpec || 'H-300x300'} @ {inputs.deckingConfig?.kingPostSpacing || 3.5}m, L={kpLength.toFixed(1)}m)
                    </text>
                  </g>
                </g>
              );
            })()}

            {/* 9. 지보공 렌더링 (Strut / Composite Strut / Ground Anchor) */}
            {alternative.supports.map((sup, idx) => {
              if (sup.depth > excDepth + 0.1) return null;
              const supY = groundY + sup.depth * scaleY;
              const angleRad = (sup.angle * Math.PI) / 180;

              const isCompStrut = isCompositeStrutAlt || (sup.type as any) === 'COMPOSITE_STRUT' || (sup.specName && sup.specName.includes('사각')) || (sup.strutSpec && sup.strutSpec.includes('사각'));
              const isStrut = sup.type === 'STRUT' || isCompStrut;

              if (isStrut) {
                if (isCompStrut) {
                  // 🌟 4대안: 합성사각강관(4-Box) 전용 고강성 박스 단면 렌더링
                  return (
                    <g key={sup.id}>
                      {/* 광폭 2-H 400 띠장 (Wale) */}
                      <rect x={wallLeftX - 12} y={supY - 8} width={10} height={16} fill="#1e3a8a" stroke="#172554" strokeWidth="1.2" rx="1" />
                      <rect x={wallRightX + 2} y={supY - 8} width={10} height={16} fill="#1e3a8a" stroke="#172554" strokeWidth="1.2" rx="1" />

                      {/* 2000kN 고용량 유압 프리로드 잭 & 접합 브래킷 */}
                      <rect x={wallLeftX} y={supY - 6} width={16} height={12} fill="#2563eb" stroke="#1d4ed8" strokeWidth="1" rx="1" />
                      <rect x={wallRightX - 16} y={supY - 6} width={16} height={12} fill="#2563eb" stroke="#1d4ed8" strokeWidth="1" rx="1" />

                      {/* 4-Box 450형 합성사각강관 본체 (두꺼운 박스형태 + 해치) */}
                      <rect
                        x={wallLeftX + 16}
                        y={supY - 5.5}
                        width={excWidth * scaleX - 32}
                        height={11}
                        fill="#3b82f6"
                        stroke="#1d4ed8"
                        strokeWidth="1.8"
                        rx="2"
                      />
                      <rect
                        x={wallLeftX + 16}
                        y={supY - 5.5}
                        width={excWidth * scaleX - 32}
                        height={11}
                        fill="url(#comp-box-hatch)"
                        rx="2"
                      />

                      {/* 텍스트 표기 (프리미엄 인디고 박스) */}
                      <g transform={`translate(${wallLeftX + 24}, ${supY - 16})`}>
                        <rect x="0" y="0" width="280" height="15" rx="3" fill="#ffffff" fillOpacity="0.95" stroke="#3b82f6" strokeWidth="1" />
                        <text x="5" y="11" fill="#1e40af" fontSize="10" fontWeight="bold">
                          {idx + 1}단 4-Box 합성사각강관 450형 (@5.0m 광폭, 무중간말뚝 L={excWidth}m)
                        </text>
                      </g>
                    </g>
                  );
                } else {
                  // 재래식 강관 원형 버팀보 렌더링
                  return (
                    <g key={sup.id}>
                      {/* 띠장 (Wale) */}
                      <rect x={wallLeftX - 10} y={supY - 6} width={8} height={12} fill="#d97706" stroke="#92400e" strokeWidth="1" />
                      <rect x={wallRightX + 2} y={supY - 6} width={8} height={12} fill="#d97706" stroke="#92400e" strokeWidth="1" />

                      {/* 강관 버팀보 */}
                      <line x1={wallLeftX} y1={supY} x2={wallRightX} y2={supY} stroke="#f59e0b" strokeWidth="6" />
                      
                      {/* 중간말뚝 - 스트럿 강결 접합부 (Rigid Joint Gusset Plate / Bracket) */}
                      {inputs.deckingConfig?.useDecking !== false && (
                        <g>
                          <rect
                            x={wallLeftX + (excWidth * scaleX) / 2 - 8}
                            y={supY - 8}
                            width={16}
                            height={16}
                            fill="#1e293b"
                            stroke="#f59e0b"
                            strokeWidth="1.5"
                            rx="2"
                          />
                          <circle cx={wallLeftX + (excWidth * scaleX) / 2} cy={supY} r="3" fill="#f59e0b" />
                        </g>
                      )}

                      {/* 텍스트 표기 (흰색 배경 박스) */}
                      <g transform={`translate(${wallLeftX + 15}, ${supY - 14})`}>
                        <rect x="0" y="0" width="230" height="14" rx="2" fill="#ffffff" fillOpacity="0.85" />
                        <text x="2" y="11" fill="#92400e" fontSize="10" fontWeight="bold">
                          {idx + 1}단 Strut ({sup.specName}, Lk=B/2 강결)
                        </text>
                      </g>
                    </g>
                  );
                }
              } else if (sup.type === 'GROUND_ANCHOR') {
                const dx_free = sup.freeLength * Math.cos(angleRad) * scaleX;
                const dy_free = sup.freeLength * Math.sin(angleRad) * scaleY;

                const dx_bond = sup.bondLength * Math.cos(angleRad) * scaleX;
                const dy_bond = sup.bondLength * Math.sin(angleRad) * scaleY;

                // 좌측 앵커 (좌하향 일직선)
                const anchorLeftFreeEndX = wallLeftX - dx_free;
                const anchorLeftFreeEndY = supY + dy_free;
                const anchorLeftBondEndX = anchorLeftFreeEndX - dx_bond;
                const anchorLeftBondEndY = anchorLeftFreeEndY + dy_bond;

                // 우측 앵커 (우하향 일직선)
                const anchorRightFreeEndX = wallRightX + dx_free;
                const anchorRightFreeEndY = supY + dy_free;
                const anchorRightBondEndX = anchorRightFreeEndX + dx_bond;
                const anchorRightBondEndY = anchorRightFreeEndY + dy_bond;

                const isOverBoundary = anchorLeftBondEndX < boundaryX;

                return (
                  <g key={sup.id}>
                    {/* 띠장 */}
                    <rect x={wallLeftX - 10} y={supY - 6} width={8} height={12} fill="#d97706" stroke="#92400e" strokeWidth="1" />
                    <rect x={wallRightX + 2} y={supY - 6} width={8} height={12} fill="#d97706" stroke="#92400e" strokeWidth="1" />

                    {/* 좌측 앵커 자유장 (파란 실선) */}
                    <line x1={wallLeftX} y1={supY} x2={anchorLeftFreeEndX} y2={anchorLeftFreeEndY} stroke="#0284c7" strokeWidth="3" />
                    {/* 좌측 앵커 정착장 (두꺼운 주황색 그라우트) */}
                    <line
                      x1={anchorLeftFreeEndX}
                      y1={anchorLeftFreeEndY}
                      x2={anchorLeftBondEndX}
                      y2={anchorLeftBondEndY}
                      stroke="#d97706"
                      strokeWidth="9"
                      strokeLinecap="round"
                    />

                    {/* 우측 앵커 자유장 (파란 실선) */}
                    <line x1={wallRightX} y1={supY} x2={anchorRightFreeEndX} y2={anchorRightFreeEndY} stroke="#0284c7" strokeWidth="3" />
                    {/* 우측 앵커 정착장 (두꺼운 주황색 그라우트) */}
                    <line
                      x1={anchorRightFreeEndX}
                      y1={anchorRightFreeEndY}
                      x2={anchorRightBondEndX}
                      y2={anchorRightBondEndY}
                      stroke="#d97706"
                      strokeWidth="9"
                      strokeLinecap="round"
                    />

                    {/* 앵커 라벨 (중앙 흰색 배경) */}
                    <g transform={`translate(${wallLeftX + 15}, ${supY - 14})`}>
                      <rect x="0" y="0" width="255" height="15" rx="2" fill="#ffffff" fillOpacity="0.9" stroke="#cbd5e1" strokeWidth="0.8" />
                      <text x="4" y="11" fill="#0369a1" fontSize="10" fontWeight="bold">
                        {idx + 1}단 Anchor ({sup.angle}°, L={sup.freeLength + sup.bondLength}m, EL -{sup.depth.toFixed(1)}m)
                      </text>
                    </g>

                    {isOverBoundary && (
                      <g transform={`translate(${anchorLeftBondEndX - 10}, ${anchorLeftBondEndY + 12})`}>
                        <rect x="0" y="0" width="135" height="14" rx="2" fill="#fff1f2" stroke="#f43f5e" strokeWidth="0.8" />
                        <text x="4" y="10" fill="#e11d48" fontSize="9" fontWeight="bold">
                          ⚠ 부지경계 침범 ({Math.abs((boundaryX - anchorLeftBondEndX) / scaleX).toFixed(1)}m)
                        </text>
                      </g>
                    )}
                  </g>
                );
              }
              return null;
            })}

            {/* 10. 심도 눈금자 (EL Ruler) */}
            <g>
              <line x1={15} y1={groundY} x2={15} y2={groundY + maxDepth * scaleY} stroke="#475569" strokeWidth="1.2" />
              {Array.from({ length: Math.floor(maxDepth / 2) + 1 }).map((_, i) => {
                const d = i * 2;
                const y = groundY + d * scaleY;
                return (
                  <g key={i}>
                    <line x1={10} y1={y} x2={15} y2={y} stroke="#475569" strokeWidth="1" />
                    <text x={8} y={y + 3} fill="#475569" fontSize="8.5" textAnchor="end" fontFamily="monospace" fontWeight="bold">
                      -{d}m
                    </text>
                  </g>
                );
              })}
            </g>

            {/* 11. Level 1: 최상단 치수선 (굴착폭 B - y = 25 위치) */}
            <g>
              <line x1={wallLeftX} y1={25} x2={wallRightX} y2={25} stroke="#334155" strokeWidth="1.2" />
              <line x1={wallLeftX} y1={20} x2={wallLeftX} y2={30} stroke="#334155" strokeWidth="1.2" />
              <line x1={wallRightX} y1={20} x2={wallRightX} y2={30} stroke="#334155" strokeWidth="1.2" />
              <g transform={`translate(${wallLeftX + (excWidth * scaleX) / 2 - 50}, 15)`}>
                <rect x="0" y="0" width="100" height="18" fill="#ffffff" stroke="#cbd5e1" strokeWidth="1" rx="3" />
                <text x="50" y="13" fill="#0f172a" fontSize="10.5" textAnchor="middle" fontWeight="bold" fontFamily="monospace">
                  굴착폭 B = {excWidth.toFixed(1)} m
                </text>
              </g>
            </g>
          </svg>
        </div>
      </div>
    </div>
  );
};
