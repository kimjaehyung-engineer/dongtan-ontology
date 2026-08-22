import React, { useState } from 'react';
import { AlternativeSpec, StageResult } from '../../types';
import { Activity, Play, Pause, ChevronLeft, ChevronRight } from 'lucide-react';

interface DiagramViewerProps {
  alternative: AlternativeSpec;
  currentStageIdx: number;
  onSelectStage: (idx: number) => void;
}

export const DiagramViewer: React.FC<DiagramViewerProps> = ({
  alternative,
  currentStageIdx,
  onSelectStage
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [chartType, setChartType] = useState<'displacement' | 'moment' | 'shear' | 'earthPressure'>('displacement');

  const stages = alternative.stageResults;
  const currentStage: StageResult = stages[currentStageIdx] || stages[stages.length - 1];
  const nodes = currentStage.nodes;

  React.useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        onSelectStage((currentStageIdx + 1) % stages.length);
      }, 1500);
    }
    return () => clearInterval(timer);
  }, [isPlaying, currentStageIdx, stages.length, onSelectStage]);

  const width = 360;
  const height = 480;
  const topPad = 35;
  const bottomPad = 30;
  const leftPad = 55;
  const rightPad = 30;

  const maxDepth = Math.max(alternative.wall.totalLength, 15);
  const plotH = height - topPad - bottomPad;
  const plotW = width - leftPad - rightPad;
  const midX = leftPad + plotW / 2;

  let maxVal = 1;
  if (chartType === 'displacement') {
    maxVal = Math.max(10, ...nodes.map(n => Math.abs(n.displacement)));
  } else if (chartType === 'moment') {
    maxVal = Math.max(50, ...nodes.map(n => Math.abs(n.bendingMoment)));
  } else if (chartType === 'shear') {
    maxVal = Math.max(50, ...nodes.map(n => Math.abs(n.shearForce)));
  } else {
    maxVal = Math.max(50, ...nodes.map(n => Math.max(n.earthPressure, n.ppLimit, n.paLimit)));
  }

  const getY = (depth: number) => topPad + (depth / maxDepth) * plotH;
  const getX = (val: number) => {
    if (chartType === 'earthPressure') {
      return leftPad + (val / maxVal) * plotW;
    }
    return midX + (val / maxVal) * (plotW / 2);
  };

  const mainPoints = nodes.map(n => {
    let v = 0;
    if (chartType === 'displacement') v = n.displacement;
    else if (chartType === 'moment') v = n.bendingMoment;
    else if (chartType === 'shear') v = n.shearForce;
    else v = n.earthPressure;
    return `${getX(v)},${getY(n.depth)}`;
  }).join(' ');

  const meta = {
    displacement: { title: '벽체 수평변위 (Displacement δ)', unit: 'mm', color: '#0284c7', maxStr: `${currentStage.stability.maxDisplacement} mm` },
    moment: { title: '휨모멘트 (Bending Moment M)', unit: 'kNm/m', color: '#d97706', maxStr: `${currentStage.stability.maxMoment} kNm/m` },
    shear: { title: '전단력 (Shear Force V)', unit: 'kN/m', color: '#db2777', maxStr: `${currentStage.stability.maxShear} kN/m` },
    earthPressure: { title: '작용 토압/지반반력 (Pressure p)', unit: 'kN/m²', color: '#059669', maxStr: `${Math.round(maxVal)} kN/m²` },
  }[chartType];

  return (
    <div className="eng-panel flex flex-col h-full">
      <div className="eng-panel-header">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-blue-600" />
          <div>
            <h3 className="text-xs font-bold text-slate-800">{meta.title}</h3>
            <p className="text-[11px] text-slate-500">최대치: <strong className="text-blue-700 font-mono">{meta.maxStr}</strong></p>
          </div>
        </div>

        {/* 차트 타입 선택 버튼 */}
        <div className="flex items-center bg-slate-200/80 p-0.5 rounded border border-slate-300 text-[11px]">
          <button
            onClick={() => setChartType('displacement')}
            className={`px-2 py-0.5 rounded font-bold ${chartType === 'displacement' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-600'}`}
          >
            변위 δ
          </button>
          <button
            onClick={() => setChartType('moment')}
            className={`px-2 py-0.5 rounded font-bold ${chartType === 'moment' ? 'bg-white text-amber-700 shadow-sm' : 'text-slate-600'}`}
          >
            모멘트 M
          </button>
          <button
            onClick={() => setChartType('shear')}
            className={`px-2 py-0.5 rounded font-bold ${chartType === 'shear' ? 'bg-white text-pink-700 shadow-sm' : 'text-slate-600'}`}
          >
            전단력 V
          </button>
          <button
            onClick={() => setChartType('earthPressure')}
            className={`px-2 py-0.5 rounded font-bold ${chartType === 'earthPressure' ? 'bg-white text-emerald-700 shadow-sm' : 'text-slate-600'}`}
          >
            토압 p
          </button>
        </div>
      </div>

      <div className="p-3 flex-1 flex flex-col justify-between">
        {/* 단계 컨트롤러 */}
        <div className="bg-slate-50 p-2 rounded border border-slate-200 mb-2 flex items-center justify-between gap-2 text-xs">
          <div className="flex items-center gap-1">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-1 rounded bg-blue-600 hover:bg-blue-700 text-white shadow-sm transition-all"
              title={isPlaying ? '일시정지' : '애니메이션 재생'}
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            </button>
            <button
              onClick={() => onSelectStage(Math.max(0, currentStageIdx - 1))}
              disabled={currentStageIdx === 0}
              className="p-1 rounded hover:bg-slate-200 text-slate-600 disabled:opacity-30"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <span className="font-mono text-slate-800 font-bold min-w-[70px] text-center">
              Stage {currentStage.stage} / {stages.length}
            </span>
            <button
              onClick={() => onSelectStage(Math.min(stages.length - 1, currentStageIdx + 1))}
              disabled={currentStageIdx === stages.length - 1}
              className="p-1 rounded hover:bg-slate-200 text-slate-600 disabled:opacity-30"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <span className="text-[11px] text-slate-600 truncate font-medium">
            {currentStage.stageName}
          </span>
        </div>

        {/* 차트 SVG */}
        <div className="flex justify-center items-center bg-white rounded border border-slate-200 p-1 shadow-inner">
          <svg width={width} height={height} className="select-none font-sans text-xs">
            {/* Y축 (심도) */}
            <line x1={chartType === 'earthPressure' ? leftPad : midX} y1={topPad} x2={chartType === 'earthPressure' ? leftPad : midX} y2={height - bottomPad} stroke="#94a3b8" strokeWidth="1.2" />

            {/* 심도 눈금선 */}
            {Array.from({ length: Math.floor(maxDepth / 2) + 1 }).map((_, i) => {
              const d = i * 2;
              const y = getY(d);
              return (
                <g key={i}>
                  <line x1={leftPad} y1={y} x2={width - rightPad} y2={y} stroke="#e2e8f0" strokeWidth="1" strokeDasharray="2 2" />
                  <text x={leftPad - 8} y={y + 3} fill="#64748b" fontSize="9" textAnchor="end" fontFamily="monospace" fontWeight="bold">
                    -{d}m
                  </text>
                </g>
              );
            })}

            {/* 굴착저면 */}
            <line
              x1={leftPad}
              y1={getY(currentStage.excavationDepth)}
              x2={width - rightPad}
              y2={getY(currentStage.excavationDepth)}
              stroke="#ef4444"
              strokeWidth="1.5"
              strokeDasharray="4 2"
            />
            <text x={width - rightPad - 4} y={getY(currentStage.excavationDepth) - 4} fill="#dc2626" fontSize="9" textAnchor="end" fontWeight="bold">
              굴착면 (-{currentStage.excavationDepth.toFixed(1)}m)
            </text>

            {/* 지보 위치 표기 */}
            {currentStage.supports.map((sup, idx) => {
              const isComp = alternative.type === 'COMPOSITE_STRUT' || (sup.type as any) === 'COMPOSITE_STRUT';
              const isStrut = sup.type === 'STRUT' || isComp;
              const label = isComp ? '합성Strut' : (isStrut ? 'Strut' : 'Anchor');
              return (
                <g key={idx}>
                  <circle cx={chartType === 'earthPressure' ? leftPad : midX} cy={getY(sup.depth)} r="4" fill={isComp ? '#2563eb' : '#d97706'} />
                  <text x={leftPad + 8} y={getY(sup.depth) - 2} fill={isComp ? '#1d4ed8' : '#92400e'} fontSize="8.5" fontWeight="bold">
                    {label} {sup.supportIndex} ({sup.axialForce}kN)
                  </text>
                </g>
              );
            })}

            {/* 토압 모드일 때 한계토압 */}
            {chartType === 'earthPressure' && (
              <g>
                <polyline
                  fill="none"
                  stroke="#3b82f6"
                  strokeWidth="1.2"
                  strokeDasharray="3 2"
                  points={nodes.map(n => `${getX(n.paLimit)},${getY(n.depth)}`).join(' ')}
                />
                <polyline
                  fill="none"
                  stroke="#ef4444"
                  strokeWidth="1.2"
                  strokeDasharray="3 2"
                  points={nodes.filter(n => n.depth >= currentStage.excavationDepth).map(n => `${getX(n.ppLimit)},${getY(n.depth)}`).join(' ')}
                />
              </g>
            )}

            {/* 메인 커브 */}
            <polyline
              fill="none"
              stroke={meta.color}
              strokeWidth="2.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={mainPoints}
            />

            {/* 상단 값 표기 레이블 */}
            {chartType !== 'earthPressure' ? (
              <g>
                <text x={leftPad} y={topPad - 12} fill="#64748b" fontSize="9.5" textAnchor="start" fontWeight="bold">
                  -{maxVal.toFixed(0)} {meta.unit}
                </text>
                <text x={midX} y={topPad - 12} fill="#334155" fontSize="9.5" textAnchor="middle" fontWeight="bold">
                  0
                </text>
                <text x={width - rightPad} y={topPad - 12} fill="#64748b" fontSize="9.5" textAnchor="end" fontWeight="bold">
                  +{maxVal.toFixed(0)} {meta.unit}
                </text>
              </g>
            ) : (
              <g>
                <text x={leftPad} y={topPad - 12} fill="#64748b" fontSize="9.5" fontWeight="bold">0</text>
                <text x={width - rightPad} y={topPad - 12} fill="#64748b" fontSize="9.5" textAnchor="end" fontWeight="bold">
                  {maxVal.toFixed(0)} kN/m²
                </text>
              </g>
            )}
          </svg>
        </div>

        {/* 하단 안전율 요약 */}
        <div className="mt-2 grid grid-cols-2 gap-2 text-[11px] font-mono bg-slate-50 p-2.5 rounded border border-slate-200">
          <div>
            H-Pile 응력비: <strong className={currentStage.stability.isPileSafe ? 'text-emerald-700' : 'text-rose-700'}>
              {currentStage.stability.pileStressRatio} {currentStage.stability.isPileSafe ? '(O.K)' : '(N.G)'}
            </strong>
          </div>
          <div>
            근입장 F.S: <strong className={currentStage.stability.isEmbedmentSafe ? 'text-emerald-700' : 'text-rose-700'}>
              {currentStage.stability.embedmentSafetyFactor} (기준 1.2)
            </strong>
          </div>
          <div>
            보일링 F.S: <strong className={currentStage.stability.isBoilingSafe ? 'text-emerald-700' : 'text-rose-700'}>
              {currentStage.stability.boilingSafetyFactor} (기준 1.5)
            </strong>
          </div>
          <div>
            히빙 F.S: <strong className={currentStage.stability.isHeavingSafe ? 'text-emerald-700' : 'text-rose-700'}>
              {currentStage.stability.heavingSafetyFactor} (기준 1.2)
            </strong>
          </div>
        </div>
      </div>
    </div>
  );
};
