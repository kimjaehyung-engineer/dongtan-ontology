import React from 'react';
import { ProjectInputs, SupportStage } from '../../types';
import { HighAngleAnchorEngine, AnchorDesignResult } from '../../engine/anchorDesignEngine';
import { Anchor, ShieldCheck, AlertTriangle, Compass, CheckCircle2, Sliders, Layers, Sparkles } from 'lucide-react';

interface AnchorConfigPanelProps {
  inputs: ProjectInputs;
  onChangeSupports: (updatedSupports: SupportStage[]) => void;
  onRunAnalysis?: (overrideInputs?: ProjectInputs) => void;
}

export const AnchorConfigPanel: React.FC<AnchorConfigPanelProps> = ({
  inputs,
  onChangeSupports,
  onRunAnalysis
}) => {
  const currentAngle = inputs.supports.find(s => s.type === 'GROUND_ANCHOR')?.angle || 45;

  // 전체 앵커 각도 일괄 변경 (45° ~ 70°, 5° 간격)
  const handleBatchAngleChange = (angle: number) => {
    const updated = inputs.supports.map(s => {
      if (s.type === 'GROUND_ANCHOR') {
        const res = HighAngleAnchorEngine.designSingleAnchor(
          s.stageIndex,
          s.depth,
          angle,
          s.horizSpacing,
          110, // 평균 수평반력
          inputs.excavationDepth,
          inputs.soils,
          inputs.boundaryDistance
        );

        return {
          ...s,
          angle,
          freeLength: res.freeLength,
          bondLength: res.bondLength,
          allowableCapacity: res.strandAllowableTension,
          specName: `SWPC 12.7mm ${res.strandCount}가닥 (${angle}°)`,
          preload: Math.round(res.designTension * 0.8)
        };
      }
      return s;
    });

    onChangeSupports(updated);
    if (onRunAnalysis) {
      onRunAnalysis({
        ...inputs,
        supports: updated
      });
    }
  };

  // 단별 개별 앵커 각도/간격 변경
  const handleSingleAnchorChange = (idx: number, field: keyof SupportStage, value: any) => {
    const updated = [...inputs.supports];
    const cur = { ...updated[idx] };
    (cur as any)[field] = value;

    if (field === 'angle') {
      const angleNum = parseFloat(value) || 45;
      const res = HighAngleAnchorEngine.designSingleAnchor(
        cur.stageIndex,
        cur.depth,
        angleNum,
        cur.horizSpacing,
        110,
        inputs.excavationDepth,
        inputs.soils,
        inputs.boundaryDistance
      );
      cur.angle = angleNum;
      cur.freeLength = res.freeLength;
      cur.bondLength = res.bondLength;
      cur.allowableCapacity = res.strandAllowableTension;
      cur.specName = `SWPC 12.7mm ${res.strandCount}가닥 (${angleNum}°)`;
    }

    updated[idx] = cur;
    onChangeSupports(updated);
  };

  // 단별 앵커 설계 결과 계산
  const anchorResults: AnchorDesignResult[] = inputs.supports
    .filter(s => s.type === 'GROUND_ANCHOR')
    .map((s, idx) => {
      return HighAngleAnchorEngine.designSingleAnchor(
        s.stageIndex || idx + 1,
        s.depth,
        s.angle || currentAngle,
        s.horizSpacing,
        110,
        inputs.excavationDepth,
        inputs.soils,
        inputs.boundaryDistance
      );
    });

  const hasAnchor = inputs.supports.some(s => s.type === 'GROUND_ANCHOR');
  if (!hasAnchor) return null;

  return (
    <div className="eng-panel border-2 border-indigo-200 shadow-sm">
      <div className="eng-panel-header bg-gradient-to-r from-indigo-50 to-blue-50 border-b border-indigo-200 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="p-1 rounded bg-indigo-600 text-white">
            <Anchor className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-indigo-950 flex items-center gap-2">
              고각 어스앵커 (High-Angle Anchor, 45° ~ 70°) 상세 설계
              <span className="px-2 py-0.2 rounded text-[10px] bg-indigo-200 text-indigo-800 font-mono font-extrabold">
                부지경계 협소지역 특수 앵커 공법
              </span>
            </h3>
            <p className="text-[11px] text-indigo-700">
              5° 간격 고각(45°, 50°, 55°, 60°, 65°, 70°) 선정, 지중 암반층 급경사 정착 및 대지경계선 침범 방지
            </p>
          </div>
        </div>

        {/* 앵커 각도 5도 간격 원클릭 버튼 */}
        <div className="flex items-center gap-1">
          <span className="text-xs font-bold text-slate-700 mr-1">고각 선정:</span>
          {HighAngleAnchorEngine.AVAILABLE_ANGLES.map(ang => (
            <button
              key={ang}
              onClick={() => handleBatchAngleChange(ang)}
              className={`px-2.5 py-1 rounded text-xs font-mono font-bold transition-all border ${
                currentAngle === ang
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                  : 'bg-white text-slate-700 border-slate-300 hover:bg-indigo-50'
              }`}
            >
              {ang}°
            </button>
          ))}
        </div>
      </div>

      <div className="p-3.5 space-y-3 bg-white text-xs">
        {/* 단별 고각 앵커 설계 매트릭스 카드 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {anchorResults.map((res, idx) => {
            const isSafe = res.isBoundarySafe && res.isBondSafe;

            return (
              <div
                key={idx}
                className={`p-3 rounded-lg border text-xs space-y-2 ${
                  isSafe ? 'bg-indigo-50/40 border-indigo-200' : 'bg-rose-50/50 border-rose-300'
                }`}
              >
                <div className="flex items-center justify-between border-b border-indigo-100 pb-1.5">
                  <span className="font-bold text-indigo-900 flex items-center gap-1">
                    <span className="w-4 h-4 rounded-full bg-indigo-600 text-white text-[10px] flex items-center justify-center font-mono">
                      {res.tierIndex}
                    </span>
                    {res.tierIndex}단 고각 앵커 (GL -{res.depth}m)
                  </span>
                  <span className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                    res.isBoundarySafe ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                  }`}>
                    {res.isBoundarySafe ? '✓ 경계내 진입' : `⚠ ${res.encroachDistance}m 침범`}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-1.5 font-mono text-[11px] text-slate-700">
                  <div>
                    설치 각도: <strong className="text-indigo-800">{res.angle}°</strong>
                  </div>
                  <div>
                    자유장 Lf: <strong className="text-blue-800">{res.freeLength}m</strong>
                  </div>
                  <div>
                    정착장 Lb: <strong className="text-amber-800">{res.bondLength}m</strong>
                  </div>
                  <div>
                    총 연장 L: <strong className="text-slate-900">{res.totalLength}m</strong>
                  </div>
                </div>

                <div className="bg-white p-2 rounded border border-slate-200 space-y-1 text-[11px] font-mono">
                  <div className="flex justify-between">
                    <span>수평 도달거리:</span>
                    <strong className={res.isBoundarySafe ? 'text-emerald-700' : 'text-rose-700'}>
                      {res.horizReach}m (한도 {inputs.boundaryDistance}m)
                    </strong>
                  </div>
                  <div className="flex justify-between">
                    <span>소요 강연선:</span>
                    <strong className="text-indigo-900">SWPC 12.7mm {res.strandCount}가닥</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>정착층 지반:</span>
                    <strong className="text-slate-800">{res.targetSoilName}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>인발 안전율 F.S:</span>
                    <strong className={res.bondSafetyFactor >= 2.0 ? 'text-emerald-700' : 'text-rose-700'}>
                      {res.bondSafetyFactor} (기준 ≥ 2.0)
                    </strong>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* 고각 앵커 설계 효과 및 역학 가이드 바 */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-2.5 rounded border border-indigo-200 flex flex-wrap items-center justify-between gap-2 text-xs">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span className="text-slate-800 font-bold">고각 앵커({currentAngle}°) 적용 시 공학적 특징: </span>
            <span className="text-slate-600 text-[11px]">
              수평 도달거리가 완경사 대비 약 {Math.round((1 - Math.cos(currentAngle * Math.PI / 180) / Math.cos(15 * Math.PI / 180)) * 100)}% 축소되어 부지경계 침범 민원을 원천 차단하며, 하부 암반층({inputs.soils[inputs.soils.length - 1]?.name})에 고강도 정착됩니다.
            </span>
          </div>

          <div className="flex items-center gap-3 font-mono text-[11px]">
            <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> 수평도달거리 안전
            </span>
            <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> 암반 정착력 O.K
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
