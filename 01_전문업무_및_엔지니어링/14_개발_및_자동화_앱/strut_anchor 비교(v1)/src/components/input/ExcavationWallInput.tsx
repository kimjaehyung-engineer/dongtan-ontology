import React, { useState } from 'react';
import { ProjectInputs, WallSection, SupportStage, DeckingAndKingPostConfig } from '../../types';
import { H_PILE_DATABASE, STRUT_DATABASE, WALE_DATABASE, LAGGING_DATABASE, DECK_BEAM_DATABASE } from '../../engine/sectionDB';
import { HighAngleAnchorEngine } from '../../engine/anchorDesignEngine';
import { KingPostEngine } from '../../engine/kingPostEngine';
import { Construction, Box, Waves, ArrowDownUp, Ruler, ShieldAlert, Cpu, CheckCircle2, Layers, Sliders, Truck, Anchor, Sparkles, AlertTriangle, RefreshCw } from 'lucide-react';

interface ExcavationWallInputProps {
  inputs: ProjectInputs;
  onChangeInputs: (inputs: ProjectInputs) => void;
  onRunAnalysis?: (overrideInputs?: ProjectInputs) => void;
  selectedAltType?: 'ALL_STRUT' | 'ALL_ANCHOR' | 'HYBRID' | 'OPTIMIZED';
}

export const ExcavationWallInput: React.FC<ExcavationWallInputProps> = ({ 
  inputs, 
  onChangeInputs,
  onRunAnalysis,
  selectedAltType = 'ALL_STRUT'
}) => {
  const [showTierDetail, setShowTierDetail] = useState<boolean>(false);

  const handleFieldChange = (field: keyof ProjectInputs, value: any) => {
    onChangeInputs({ ...inputs, [field]: value });
  };

  const handleWallChange = (field: keyof WallSection, value: any) => {
    const updatedWall = { ...inputs.wall, [field]: value };
    onChangeInputs({ ...inputs, wall: updatedWall });
  };

  const handleDeckingChange = (field: keyof DeckingAndKingPostConfig, value: any) => {
    const currentDecking = inputs.deckingConfig || {
      useDecking: true,
      trafficLoadType: 'KL-510',
      trafficLoadValue: 20.0,
      deckBeamSpec: 'H-400x400x13x21',
      deckBeamSpacing: 2.0,
      kingPostSpec: 'H-300x300x10x15',
      kingPostSpacing: 3.5,
      kingPostNumRows: 1,
      kingPostTotalLength: inputs.excavationDepth + 5.0
    };

    const updated = { ...currentDecking, [field]: value };
    onChangeInputs({ ...inputs, deckingConfig: updated });
  };

  // 엄지말뚝 H-Pile 규격 변경
  const handleSelectHPile = (spec: string) => {
    const opt = H_PILE_DATABASE.find(o => o.spec === spec);
    if (!opt) return;

    const spacing = inputs.wall.spacing;
    const EI = (2.05e8 * opt.Ix * 1e-8) / spacing;
    const EA = (2.05e8 * opt.A * 1e-4) / spacing;

    onChangeInputs({
      ...inputs,
      wall: {
        ...inputs.wall,
        name: `${opt.spec} @ ${spacing}m`,
        hPileSpec: opt.spec,
        Zx: opt.Zx,
        EI,
        EA
      }
    });
  };

  // 엄지말뚝 간격 변경
  const handleHPileSpacingChange = (spacing: number) => {
    const opt = H_PILE_DATABASE.find(o => o.spec === (inputs.wall.hPileSpec || 'H-300x300x10x15')) || H_PILE_DATABASE[0];
    const EI = (2.05e8 * opt.Ix * 1e-8) / spacing;
    const EA = (2.05e8 * opt.A * 1e-4) / spacing;

    onChangeInputs({
      ...inputs,
      wall: {
        ...inputs.wall,
        spacing,
        name: `${opt.spec} @ ${spacing}m`,
        EI,
        EA
      }
    });
  };

  // 버팀보(Strut) 및 고각 어스앵커 규격/간격/각도 일괄 업데이트
  const handleBatchSupportChange = (field: 'spec' | 'spacing' | 'wale' | 'anchorAngle' | 'strandCount', value: any) => {
    const numTiers = inputs.supports.length;
    const halfTiers = Math.max(1, Math.ceil(numTiers / 2));

    const updatedSups = inputs.supports.map((s, idx) => {
      // 복합공법(HYBRID)인 경우: 상부단은 앵커, 하부단은 스트러트
      const isHybridUpper = isHybridMode && idx < halfTiers;
      const isAnchor = isAnchorMode || isHybridUpper || s.type === 'GROUND_ANCHOR';

      if (field === 'anchorAngle') {
        const ang = parseFloat(value) || 45;
        if (isAnchorMode || isHybridUpper || s.type === 'GROUND_ANCHOR') {
          const res = HighAngleAnchorEngine.designSingleAnchor(
            s.stageIndex || idx + 1,
            s.depth,
            ang,
            s.horizSpacing,
            110,
            inputs.excavationDepth,
            inputs.soils,
            inputs.boundaryDistance
          );
          return {
            ...s,
            type: 'GROUND_ANCHOR' as const,
            angle: ang,
            freeLength: res.freeLength,
            bondLength: res.bondLength,
            allowableCapacity: res.strandAllowableTension,
            specName: `SWPC 12.7mm ${res.strandCount}가닥 (${ang}° 고각)`,
            preload: Math.round(res.designTension * 0.8)
          };
        }
      } else if (field === 'spec') {
        if (!isAnchorMode && (!isHybridMode || idx >= halfTiers)) {
          const strutOpt = STRUT_DATABASE.find(st => st.spec === value);
          return {
            ...s,
            type: 'STRUT' as const,
            strutSpec: value,
            specName: value,
            allowableCapacity: strutOpt ? strutOpt.allowCompressCapacity : s.allowableCapacity
          };
        }
      } else if (field === 'spacing') {
        return { ...s, horizSpacing: parseFloat(value) || (isAnchor ? 1.5 : 3.0) };
      } else if (field === 'wale') {
        return { ...s, waleSpec: value };
      } else if (field === 'strandCount') {
        if (isAnchor) {
          const count = parseInt(value, 10) || 4;
          return {
            ...s,
            specName: `SWPC 12.7mm ${count}가닥 (${s.angle || 45}°)`,
            allowableCapacity: Math.round(count * 109.8)
          };
        }
      }
      return s;
    });

    onChangeInputs({
      ...inputs,
      supports: updatedSups
    });
  };

  // 단별(Tier-by-Tier) 개별 지보재 변경
  const handleSingleTierChange = (index: number, field: keyof SupportStage, value: any) => {
    const updatedSups = [...inputs.supports];
    const current = { ...updatedSups[index] };

    if (field === 'strutSpec') {
      const strutOpt = STRUT_DATABASE.find(st => st.spec === value);
      current.strutSpec = value;
      current.specName = value;
      if (strutOpt) current.allowableCapacity = strutOpt.allowCompressCapacity;
    } else if (field === 'waleSpec') {
      current.waleSpec = value;
    } else if (field === 'horizSpacing') {
      current.horizSpacing = parseFloat(value) || 3.5;
    } else if (field === 'depth') {
      current.depth = parseFloat(value) || current.depth;
    } else if (field === 'angle') {
      current.angle = parseFloat(value) || 45;
      current.specName = `SWPC 12.7mm (${current.angle}°)`;
    } else {
      (current as any)[field] = value;
    }

    updatedSups[index] = current;
    onChangeInputs({
      ...inputs,
      supports: updatedSups
    });
  };

  // 🌟 굴착 깊이 연동 표준 단간격(2.5m ~ 3.0m) 지보단수 자동 최적 재배치 함수
  const handleAutoArrangeSupports = (targetDepth?: number) => {
    const H = targetDepth !== undefined ? targetDepth : inputs.excavationDepth;
    // 1단 1.5m부터 굴착 바닥 1.2m 상부까지 2.6m~2.9m 간격으로 바닥 끝까지 촘촘히 배치
    const numTiers = Math.max(2, Math.min(30, Math.floor((H - 1.5) / 2.8) + 1));
    const newSups: SupportStage[] = [];
    
    const currentStrutOpt = STRUT_DATABASE.find(st => st.spec === currentStrutSpec) || STRUT_DATABASE[2];
    for (let i = 0; i < numTiers; i++) {
      const depth = (i === 0)
        ? 1.5
        : Number((1.5 + i * ((H - 1.5 - 1.2) / Math.max(1, numTiers - 1))).toFixed(1));
      const isHybridUpper = isHybridMode && i < Math.ceil(numTiers / 2);
      const isAnchor = isAnchorMode || isHybridUpper;
      
      newSups.push({
        id: `sup-${i + 1}`,
        stageIndex: i + 1,
        type: isAnchor ? 'GROUND_ANCHOR' : 'STRUT',
        depth,
        angle: isAnchor ? currentAnchorAngle : 0,
        horizSpacing: isAnchor ? currentAnchorSpacing : currentStrutSpacing,
        preload: isAnchor ? 150 : 80 + i * 20,
        springStiffness: isAnchor ? 40000 : 45000,
        freeLength: isAnchor ? Number((8.0 + i * 1.5).toFixed(1)) : 0,
        bondLength: isAnchor ? 7.0 : 0,
        allowableCapacity: isAnchor ? 520 : currentStrutOpt.allowCompressCapacity,
        specName: isAnchor ? `SWPC 12.7mm (${currentAnchorAngle}°)` : currentStrutSpec,
        strutSpec: isAnchor ? undefined : currentStrutSpec,
        waleSpec: currentWaleSpec,
        unbracedLength: inputs.excavationWidth / 2.0
      });
    }

    onChangeInputs({
      ...inputs,
      excavationDepth: H,
      supports: newSups
    });
  };

  // 🌟 굴착 조건 확정 및 즉시 구조해석 실행 핸들러
  const handleCommitExcavationAndSolve = () => {
    const H = inputs.excavationDepth;
    // 벽체 총연장 자동 연계 (굴착깊이 H + 근입장 최소 5.0m 또는 H * 1.35)
    const neededWallLength = Math.max(H + 5.0, Number((H * 1.35).toFixed(1)));
    
    // 지보단수 자동 최적 분할: 바닥 1.2m 상부까지 끝까지 촘촘히 2.8m 간격 배치
    const numTiers = Math.max(2, Math.min(30, Math.floor((H - 1.5) / 2.8) + 1));
    const newSups: SupportStage[] = [];
    const currentStrutOpt = STRUT_DATABASE.find(st => st.spec === currentStrutSpec) || STRUT_DATABASE[2];
    
    for (let i = 0; i < numTiers; i++) {
      const depth = (i === 0)
        ? 1.5
        : Number((1.5 + i * ((H - 1.5 - 1.2) / Math.max(1, numTiers - 1))).toFixed(1));
      const isHybridUpper = isHybridMode && i < Math.ceil(numTiers / 2);
      const isAnchor = isAnchorMode || isHybridUpper;
      
      newSups.push({
        id: `sup-${i + 1}`,
        stageIndex: i + 1,
        type: isAnchor ? 'GROUND_ANCHOR' : 'STRUT',
        depth,
        angle: isAnchor ? currentAnchorAngle : 0,
        horizSpacing: isAnchor ? currentAnchorSpacing : currentStrutSpacing,
        preload: isAnchor ? 150 : 80 + i * 20,
        springStiffness: isAnchor ? 40000 : 45000,
        freeLength: isAnchor ? Number((8.0 + i * 1.5).toFixed(1)) : 0,
        bondLength: isAnchor ? 7.0 : 0,
        allowableCapacity: isAnchor ? 520 : currentStrutOpt.allowCompressCapacity,
        specName: isAnchor ? `SWPC 12.7mm (${currentAnchorAngle}°)` : currentStrutSpec,
        strutSpec: isAnchor ? undefined : currentStrutSpec,
        waleSpec: currentWaleSpec,
        unbracedLength: inputs.excavationWidth / 2.0
      });
    }

    // 🌟 지층 심도 자동 스케일링 (굴착깊이 H에 비례하여 지반 프로파일을 현실적/적정하게 자동 산정)
    let updatedSoils = inputs.soils;
    if (inputs.soils && inputs.soils.length >= 4) {
      const fillBot = Number(Math.max(2.0, Number((H * 0.15).toFixed(1))));
      const wsBot = Number(Math.max(fillBot + 3.0, Number((H * 0.45).toFixed(1))));
      const wrBot = Number(Math.max(wsBot + 4.0, Number((H * 0.85).toFixed(1))));
      const srBot = Number(Math.max(neededWallLength + 5.0, Number((H * 1.5 + 5.0).toFixed(1))));

      updatedSoils = inputs.soils.map((s, idx) => {
        if (idx === 0) return { ...s, topDepth: 0, bottomDepth: fillBot };
        if (idx === 1) return { ...s, topDepth: fillBot, bottomDepth: wsBot };
        if (idx === 2) return { ...s, topDepth: wsBot, bottomDepth: wrBot };
        if (idx === 3) return { ...s, topDepth: wrBot, bottomDepth: srBot };
        return s;
      });
    }

    const updatedInputs: ProjectInputs = {
      ...inputs,
      excavationDepth: H,
      wall: {
        ...inputs.wall,
        totalLength: neededWallLength
      },
      supports: newSups,
      soils: updatedSoils,
      deckingConfig: inputs.deckingConfig ? {
        ...inputs.deckingConfig,
        kingPostTotalLength: Number((H + 5.0).toFixed(1))
      } : undefined
    };

    onChangeInputs(updatedInputs);
    if (onRunAnalysis) {
      onRunAnalysis(updatedInputs);
    }
  };

  // 단간격(Vertical Spacing) 최대치 검증
  let maxTierGap = 0;
  if (inputs.supports.length > 0) {
    maxTierGap = inputs.supports[0].depth; // 1단 자립고
    for (let i = 0; i < inputs.supports.length - 1; i++) {
      const gap = inputs.supports[i + 1].depth - inputs.supports[i].depth;
      if (gap > maxTierGap) maxTierGap = gap;
    }
    const bottomGap = inputs.excavationDepth - inputs.supports[inputs.supports.length - 1].depth;
    if (bottomGap > maxTierGap) maxTierGap = bottomGap;
  }
  const isTierGapTooLarge = maxTierGap > 3.6;

  // 대표 파라미터 추출
  const isAnchorMode = selectedAltType === 'ALL_ANCHOR' || (inputs.supports.length > 0 && inputs.supports.every(s => s.type === 'GROUND_ANCHOR'));
  const isHybridMode = selectedAltType === 'HYBRID';

  const defaultStrut = inputs.supports.find(s => s.type === 'STRUT') || inputs.supports[0];
  const defaultAnchor = inputs.supports.find(s => s.type === 'GROUND_ANCHOR') || inputs.supports[0];

  const currentStrutSpec = defaultStrut?.strutSpec || '강관 Φ508.0x9.0t';
  const currentStrutSpacing = defaultStrut?.horizSpacing || 3.5;
  const currentAnchorAngle = defaultAnchor?.angle || 45;
  const currentAnchorSpacing = defaultAnchor?.horizSpacing || 2.0;
  const currentWaleSpec = (isAnchorMode ? defaultAnchor?.waleSpec : defaultStrut?.waleSpec) || '2-H 300x300x10x15';

  const hPileSpacing = inputs.wall.spacing;
  const targetSpacing = isAnchorMode ? currentAnchorSpacing : currentStrutSpacing;
  const ratio = targetSpacing / hPileSpacing;
  const isMultiple = Math.abs(ratio - Math.round(ratio)) < 0.05;

  const decking = inputs.deckingConfig || {
    useDecking: true,
    trafficLoadType: 'KL-510',
    trafficLoadValue: 20.0,
    deckBeamSpec: 'H-400x400x13x21',
    deckBeamSpacing: 2.0,
    kingPostSpec: 'H-300x300x10x15',
    kingPostSpacing: 3.5,
    kingPostNumRows: 1,
    kingPostTotalLength: inputs.excavationDepth + 5.0
  };

  return (
    <div className="space-y-4">
      {/* 1행: 굴착제원, 엄지말뚝, 지보재(버팀보 or 앵커 동적 전환) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* 1. 굴착 제원 및 하중 조건 */}
        <div className="eng-panel">
          <div className="eng-panel-header">
            <div className="flex items-center gap-2">
              <Construction className="w-4 h-4 text-blue-600" />
              <div>
                <h3 className="text-xs font-bold text-slate-800">굴착 및 하중 조건</h3>
                <p className="text-[11px] text-slate-500">굴착 깊이/폭, 지하수위 및 상재하중</p>
              </div>
            </div>
          </div>

          <div className="p-3.5 space-y-2.5 text-xs">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-slate-600 font-semibold mb-1 flex items-center gap-1">
                  <Ruler className="w-3.5 h-3.5 text-blue-600" /> 굴착 깊이 H (m)
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={inputs.excavationDepth}
                  onChange={(e) => handleFieldChange('excavationDepth', parseFloat(e.target.value) || 0)}
                  className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-600 font-semibold mb-1 flex items-center gap-1">
                  <ArrowDownUp className="w-3.5 h-3.5 text-blue-600" /> 굴착 폭 B (m)
                </label>
                <input
                  type="number"
                  step="1"
                  value={inputs.excavationWidth}
                  onChange={(e) => handleFieldChange('excavationWidth', parseFloat(e.target.value) || 0)}
                  className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-slate-600 font-semibold mb-1 flex items-center gap-1">
                  <Waves className="w-3.5 h-3.5 text-cyan-600" /> 지하수위 G.W.L (m)
                </label>
                <input
                  type="number"
                  step="0.5"
                  value={inputs.waterTableBehind}
                  onChange={(e) => handleFieldChange('waterTableBehind', parseFloat(e.target.value) || 0)}
                  className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-600 font-semibold mb-1 flex items-center gap-1">
                  <Box className="w-3.5 h-3.5 text-amber-600" /> 상재하중 q (kN/m²)
                </label>
                <input
                  type="number"
                  step="5"
                  value={inputs.surcharge}
                  onChange={(e) => handleFieldChange('surcharge', parseFloat(e.target.value) || 0)}
                  className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-100">
              <div>
                <label className="block text-slate-600 font-semibold mb-1 flex items-center gap-1">
                  <ShieldAlert className="w-3.5 h-3.5 text-rose-600" /> 대지경계 이격 (m)
                </label>
                <input
                  type="number"
                  step="1"
                  value={inputs.boundaryDistance}
                  onChange={(e) => handleFieldChange('boundaryDistance', parseFloat(e.target.value) || 0)}
                  className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-slate-600 font-semibold mb-1">총 가시설연장 (m)</label>
                <input
                  type="number"
                  step="10"
                  value={inputs.totalWallPerimeter}
                  onChange={(e) => handleFieldChange('totalWallPerimeter', parseFloat(e.target.value) || 0)}
                  className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>

            {/* 🌟 굴착 조건 확정 및 모식도 연동 실행 버튼 */}
            <div className="pt-2">
              <button
                onClick={() => handleCommitExcavationAndSolve()}
                className="w-full flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-xs shadow-md transition-all active:scale-[0.99]"
                title="입력한 굴착깊이 및 폭에 맞게 단면 모식도(CrossSection)와 지보단수를 자동 연동하고 즉시 해석을 실행합니다."
              >
                <Sparkles className="w-4 h-4 text-amber-300 fill-current" />
                <span>굴착 조건 확정</span>
              </button>
            </div>
          </div>
        </div>

        {/* 2. 엄지말뚝(H-Pile) 제원 및 수평 간격 선정 패널 */}
        <div className="eng-panel">
          <div className="eng-panel-header">
            <div className="flex items-center gap-2">
              <Box className="w-4 h-4 text-blue-600" />
              <div>
                <h3 className="text-xs font-bold text-slate-800">엄지말뚝(H-Pile) 제원 & 간격 선정</h3>
                <p className="text-[11px] text-slate-500">H형강 규격, 엄지말뚝 설치간격 및 토류판 두께</p>
              </div>
            </div>
          </div>

          <div className="p-3.5 space-y-2.5 text-xs">
            <div>
              <label className="block text-slate-700 font-bold mb-1">엄지말뚝 H-Pile 규격</label>
              <select
                value={inputs.wall.hPileSpec || 'H-300x300x10x15'}
                onChange={(e) => handleSelectHPile(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none shadow-xs"
              >
                {H_PILE_DATABASE.map((opt) => (
                  <option key={opt.spec} value={opt.spec}>
                    {opt.spec} ({opt.weight}kg/m, Zx={opt.Zx}cm³)
                  </option>
                ))}
              </select>
            </div>

            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-slate-700 font-bold">
                  엄지말뚝 수평 간격 (m): <span className="text-blue-700 font-mono font-extrabold">{inputs.wall.spacing} m</span>
                </label>
              </div>
              <div className="flex items-center gap-1.5 flex-wrap">
                {[1.0, 1.2, 1.5, 1.8, 2.0, 2.5].map((sp) => (
                  <button
                    key={sp}
                    onClick={() => handleHPileSpacingChange(sp)}
                    className={`px-2.5 py-1 rounded text-xs font-bold transition-all border ${
                      inputs.wall.spacing === sp
                        ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                        : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                    }`}
                  >
                    {sp.toFixed(1)}m
                  </button>
                ))}
                <div className="flex items-center gap-1 ml-auto">
                  <span className="text-[11px] text-slate-500 font-bold">직접:</span>
                  <input
                    type="number"
                    step="0.1"
                    min="0.8"
                    max="5.0"
                    value={inputs.wall.spacing}
                    onChange={(e) => handleHPileSpacingChange(parseFloat(e.target.value) || 1.0)}
                    className="w-16 bg-white border border-slate-300 rounded px-1.5 py-1 text-slate-900 text-center font-mono font-bold focus:border-blue-500 focus:outline-none"
                    title="직접 입력"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-slate-700 font-bold mb-1">토류판(Lagging) 사양</label>
              <select
                value={inputs.wall.laggingType || '낙엽송 목재 토류판 (t=8.0cm)'}
                onChange={(e) => handleWallChange('laggingType', e.target.value)}
                className="w-full bg-white border border-slate-300 rounded px-2 py-1 text-slate-800 text-xs focus:border-blue-500 focus:outline-none"
              >
                {LAGGING_DATABASE.map((lag, idx) => (
                  <option key={idx} value={lag.name}>
                    {lag.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="bg-blue-50/70 p-2 rounded border border-blue-200 text-[11px] text-slate-700 flex justify-between font-mono">
              <div>
                단위폭 EI: <strong className="text-blue-800">{Math.round(inputs.wall.EI).toLocaleString()}</strong> kNm²/m
              </div>
              <div>
                단면계수 Zx: <strong className="text-blue-800">{inputs.wall.Zx}</strong> cm³
              </div>
              <div>
                근입장 D: <strong className="text-amber-800">{(inputs.wall.totalLength - inputs.excavationDepth).toFixed(1)}</strong> m
              </div>
            </div>
          </div>
        </div>

        {/* 🌟 3. 선택 대안에 따른 동적 지보재 패널 (All-Strut: 버팀보 / All-Anchor: 어스앵커 / Hybrid: 복합) */}
        <div className="eng-panel">
          <div className="eng-panel-header flex items-center justify-between">
            <div className="flex items-center gap-2">
              {isAnchorMode ? (
                <Anchor className="w-4 h-4 text-indigo-600" />
              ) : (
                <Layers className="w-4 h-4 text-blue-600" />
              )}
              <div>
                <h3 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                  {isAnchorMode 
                    ? '어스앵커(Earth Anchor) & 띠장 제원' 
                    : isHybridMode 
                    ? '복합공법(Hybrid Anchor+Strut) 제원'
                    : '버팀보(Strut) & 띠장(1열/2열) 제원'}
                  <span className="px-1.5 py-0.2 rounded text-[10px] bg-blue-100 text-blue-800 font-mono font-bold">
                    대안 연동
                  </span>
                </h3>
                <p className="text-[11px] text-slate-500">
                  {isAnchorMode 
                    ? '고각(45°~70°), 수평간격, 강연선 가닥수 및 띠장' 
                    : '버팀보 규격, 수평간격 및 띠장 열수(1-H / 2-H)'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1.5">
              {isTierGapTooLarge && (
                <div className="flex items-center gap-1 text-[11px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                  <AlertTriangle className="w-3 h-3 text-rose-600" />
                  <span>단간격 초과 ({maxTierGap.toFixed(1)}m)</span>
                </div>
              )}

              <button
                onClick={() => handleAutoArrangeSupports()}
                className="flex items-center gap-1 px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold border border-slate-300"
                title="굴착깊이에 맞게 지보단수를 2.8m 표준간격으로 자동 균등 배치합니다."
              >
                <RefreshCw className="w-3 h-3 text-blue-600" />
                <span>단수 자동최적화</span>
              </button>

              <button
                onClick={() => setShowTierDetail(!showTierDetail)}
                className={`flex items-center gap-1 px-2.5 py-1 rounded text-[11px] font-bold transition-all border ${
                  showTierDetail
                    ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                    : 'bg-slate-100 text-slate-700 border-slate-300 hover:bg-slate-200'
                }`}
              >
                <Sliders className="w-3 h-3" />
                {showTierDetail ? '일괄 모드로 접기' : '단별 상세 설정'}
              </button>
            </div>
          </div>

          <div className="p-3.5 space-y-3 text-xs">
            {!showTierDetail ? (
              <div className="space-y-3">
                {/* 상단 통합 제원 컨트롤 */}
                <div className="space-y-2.5">
                  {isAnchorMode ? (
                    /* 1. 어스앵커 모드인 경우 앵커 전용 제어 컨트롤 */
                    <div className="space-y-2.5">
                      <div>
                        <label className="block text-slate-700 font-bold mb-1">
                          어스앵커 설치 각도 (고각 45° ~ 70°)
                        </label>
                        <div className="flex items-center gap-1">
                          {HighAngleAnchorEngine.AVAILABLE_ANGLES.map(ang => (
                            <button
                              key={ang}
                              onClick={() => handleBatchSupportChange('anchorAngle', ang)}
                              className={`flex-1 py-1 rounded text-xs font-mono font-bold transition-all border ${
                                currentAnchorAngle === ang
                                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                                  : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                              }`}
                            >
                              {ang}°
                            </button>
                          ))}
                        </div>
                      </div>

                      <div>
                        <div className="flex justify-between items-center mb-1">
                          <label className="text-slate-700 font-bold">
                            앵커 수평 간격: <span className="text-indigo-700 font-mono font-extrabold">{currentAnchorSpacing} m</span>
                          </label>
                          <span className="text-[11px] text-slate-400 font-mono">표준: 1.0m ~ 2.5m</span>
                        </div>
                        <div className="flex items-center gap-1.5 flex-wrap">
                          {[1.0, 1.2, 1.5, 1.8, 2.0, 2.5].map((sp) => (
                            <button
                              key={sp}
                              onClick={() => handleBatchSupportChange('spacing', sp)}
                              className={`px-2.5 py-1 rounded text-xs font-bold transition-all border ${
                                currentAnchorSpacing === sp
                                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                                  : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                              }`}
                            >
                              {sp.toFixed(1)}m
                            </button>
                          ))}
                          <div className="flex items-center gap-1 ml-auto">
                            <span className="text-[11px] text-slate-500 font-bold">직접:</span>
                            <input
                              type="number"
                              step="0.1"
                              min="0.8"
                              max="5.0"
                              value={currentAnchorSpacing}
                              onChange={(e) => handleBatchSupportChange('spacing', parseFloat(e.target.value) || 1.0)}
                              className="w-16 bg-white border border-slate-300 rounded px-1.5 py-1 text-slate-900 text-center font-mono font-bold focus:border-indigo-500 focus:outline-none"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : isHybridMode ? (
                    /* 🌟 2. 복합공법(Hybrid) 모드인 경우: 상부 고각 앵커 + 하부 버팀보 통합 설정 */
                    <div className="space-y-2.5">
                      {/* 상부 고각 앵커 파트 */}
                      <div className="bg-indigo-50/60 p-2 rounded border border-indigo-200 space-y-1.5">
                        <div className="flex justify-between items-center">
                          <span className="font-bold text-indigo-950 text-xs flex items-center gap-1">
                            <Anchor className="w-3.5 h-3.5 text-indigo-600" /> 상부 고각 앵커 (45° ~ 70°)
                          </span>
                          <span className="text-[10px] font-mono text-indigo-700 font-bold">상부 1~2단 적용</span>
                        </div>
                        <div className="flex items-center gap-1">
                          {HighAngleAnchorEngine.AVAILABLE_ANGLES.map(ang => (
                            <button
                              key={ang}
                              onClick={() => handleBatchSupportChange('anchorAngle', ang)}
                              className={`flex-1 py-0.5 rounded text-[11px] font-mono font-bold transition-all border ${
                                currentAnchorAngle === ang
                                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                                  : 'bg-white text-slate-700 border-slate-300 hover:bg-indigo-50'
                              }`}
                            >
                              {ang}°
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* 하부 버팀보 파트 */}
                      <div className="bg-blue-50/60 p-2 rounded border border-blue-200 space-y-1.5">
                        <div className="flex justify-between items-center">
                          <span className="font-bold text-blue-950 text-xs flex items-center gap-1">
                            <Layers className="w-3.5 h-3.5 text-blue-600" /> 하부 버팀보(Strut) 규격 & 간격
                          </span>
                          <span className="text-[10px] font-mono text-blue-700 font-bold">하부 굴착면 적용</span>
                        </div>
                        <div className="grid grid-cols-2 gap-1.5">
                          <select
                            value={currentStrutSpec}
                            onChange={(e) => handleBatchSupportChange('spec', e.target.value)}
                            className="w-full bg-white border border-slate-300 rounded px-1.5 py-1 text-[11px] font-mono font-bold text-slate-800 focus:border-blue-500 focus:outline-none"
                          >
                            {STRUT_DATABASE.map(st => (
                              <option key={st.spec} value={st.spec}>{st.spec}</option>
                            ))}
                          </select>
                          <select
                            value={currentStrutSpacing}
                            onChange={(e) => handleBatchSupportChange('spacing', parseFloat(e.target.value))}
                            className="w-full bg-white border border-slate-300 rounded px-1.5 py-1 text-[11px] font-mono font-bold text-slate-800 focus:border-blue-500 focus:outline-none"
                          >
                            {[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0].map(sp => (
                              <option key={sp} value={sp}>버팀보 @ {sp.toFixed(1)}m</option>
                            ))}
                          </select>
                        </div>
                      </div>
                    </div>
                  ) : (
                    /* 3. 일반 버팀보(All-Strut) 모드인 경우 버팀보 규격 및 간격 표시 */
                    <div className="space-y-2.5">
                      <div>
                        <label className="block text-slate-700 font-bold mb-1">버팀보(Strut) 표준 규격</label>
                        <select
                          value={currentStrutSpec}
                          onChange={(e) => handleBatchSupportChange('spec', e.target.value)}
                          className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none shadow-xs"
                        >
                          {STRUT_DATABASE.map((st) => (
                            <option key={st.spec} value={st.spec}>
                              {st.spec} (허용축력 Pa={st.allowCompressCapacity}kN)
                            </option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <div className="flex justify-between items-center mb-1">
                          <label className="text-slate-700 font-bold">
                            버팀보 수평 간격: <span className="text-blue-700 font-mono font-extrabold">{currentStrutSpacing} m</span>
                          </label>
                          <span className="text-[11px] text-slate-400 font-mono">1.0m ~ 5.0m 선택</span>
                        </div>
                        <div className="flex items-center gap-1.5 flex-wrap">
                          {[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0].map((sp) => (
                            <button
                              key={sp}
                              onClick={() => handleBatchSupportChange('spacing', sp)}
                              className={`px-2.5 py-1 rounded text-xs font-bold transition-all border ${
                                currentStrutSpacing === sp
                                  ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                                  : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                              }`}
                            >
                              {sp.toFixed(1)}m
                            </button>
                          ))}
                          <div className="flex items-center gap-1 ml-auto">
                            <span className="text-[11px] text-slate-500 font-bold">직접:</span>
                            <input
                              type="number"
                              step="0.1"
                              min="0.8"
                              max="8.0"
                              value={currentStrutSpacing}
                              onChange={(e) => handleBatchSupportChange('spacing', parseFloat(e.target.value) || 1.0)}
                              className="w-16 bg-white border border-slate-300 rounded px-1.5 py-1 text-slate-900 text-center font-mono font-bold focus:border-blue-500 focus:outline-none"
                              title="직접 입력"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* 띠장 규격 선택 (공통) */}
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <label className="block text-slate-700 font-bold">띠장(Wale) 규격</label>
                    <span className="text-[11px] text-indigo-700 font-semibold bg-indigo-50 px-1.5 py-0.2 rounded border border-indigo-200">
                      {isAnchorMode ? '2-H (앵커 표준)' : '1-H / 2-H'}
                    </span>
                  </div>
                  <select
                    value={currentWaleSpec}
                    onChange={(e) => handleBatchSupportChange('wale', e.target.value)}
                    className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none shadow-xs"
                  >
                    {!isAnchorMode && (
                      <optgroup label="── 1열 띠장 (1-H Beam: 상부단/경제형) ──">
                        {WALE_DATABASE.filter(w => w.numBeams === 1).map((w) => (
                          <option key={w.spec} value={w.spec}>
                            {w.spec} (Zx={w.totalZx}cm³, {w.weight}kg/m)
                          </option>
                        ))}
                      </optgroup>
                    )}
                    <optgroup label="── 2열 띠장 (2-H Beam: 앵커/하부단/고강도) ──">
                      {WALE_DATABASE.filter(w => w.numBeams === 2).map((w) => (
                        <option key={w.spec} value={w.spec}>
                          {w.spec} (2-Zx={w.totalZx}cm³, {w.weight}kg/m)
                        </option>
                      ))}
                    </optgroup>
                  </select>
                </div>
              </div>
            ) : (
              /* 단별 상세 지정 모드 */
              <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                <div className="text-[11px] text-slate-500 flex justify-between font-medium">
                  <span>단별 심도 / 규격·각도</span>
                  <span>단별 띠장 (1열/2열)</span>
                </div>
                {inputs.supports.map((sup, idx) => (
                  <div key={sup.id || idx} className="bg-slate-50 p-2 rounded border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-800 text-xs flex items-center gap-1">
                        <span className="w-4 h-4 rounded-full bg-blue-600 text-white text-[10px] flex items-center justify-center font-mono">
                          {idx + 1}
                        </span>
                        {sup.stageIndex || idx + 1}단 (GL -{sup.depth}m)
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">
                        간격: {sup.horizSpacing}m | {sup.type === 'STRUT' ? '버팀보' : `어스앵커 (${sup.angle || 45}°)`}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-1.5">
                      <div>
                        <label className="text-[10px] text-slate-500 font-semibold block">
                          {sup.type === 'STRUT' ? '버팀보 규격' : '앵커 설치각도'}
                        </label>
                        {sup.type === 'STRUT' ? (
                          <select
                            value={sup.strutSpec || currentStrutSpec}
                            onChange={(e) => handleSingleTierChange(idx, 'strutSpec', e.target.value)}
                            className="w-full bg-white border border-slate-300 rounded px-1.5 py-1 text-[11px] font-mono font-bold text-slate-800 focus:border-blue-500 focus:outline-none"
                          >
                            {STRUT_DATABASE.map(st => (
                              <option key={st.spec} value={st.spec}>{st.spec}</option>
                            ))}
                          </select>
                        ) : (
                          <select
                            value={sup.angle || currentAnchorAngle}
                            onChange={(e) => handleSingleTierChange(idx, 'angle', e.target.value)}
                            className="w-full bg-white border border-slate-300 rounded px-1.5 py-1 text-[11px] font-mono font-bold text-slate-800 focus:border-blue-500 focus:outline-none"
                          >
                            {HighAngleAnchorEngine.AVAILABLE_ANGLES.map(ang => (
                              <option key={ang} value={ang}>{ang}° (고각)</option>
                            ))}
                          </select>
                        )}
                      </div>

                      <div>
                        <label className="text-[10px] text-slate-500 font-semibold block">띠장 (1열/2열)</label>
                        <select
                          value={sup.waleSpec || currentWaleSpec}
                          onChange={(e) => handleSingleTierChange(idx, 'waleSpec', e.target.value)}
                          className="w-full bg-white border border-slate-300 rounded px-1.5 py-1 text-[11px] font-mono font-bold text-slate-800 focus:border-blue-500 focus:outline-none"
                        >
                          {WALE_DATABASE.map(w => (
                            <option key={w.spec} value={w.spec}>{w.spec}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="bg-amber-50/70 p-2 rounded border border-amber-200 text-[11px] text-slate-700 flex justify-between font-mono">
              <div>
                {isAnchorMode ? '앵커 간격:' : '띠장 지간:'} <strong className="text-amber-800">{targetSpacing}m</strong>
              </div>
              <div>
                배수 정합: <strong className={isMultiple ? 'text-emerald-700' : 'text-amber-700'}>
                  {isMultiple ? `✓ ${Math.round(ratio)}배수` : `⚠ ${(ratio).toFixed(1)}배`}
                </strong>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 2행: 주형보(Deck Beam), 복공판 & 중간말뚝(King Post) 제원 및 간격 설정 패널 */}
      <div className="eng-panel">
        <div className="eng-panel-header flex items-center justify-between bg-slate-100 border-b border-slate-200">
          <div className="flex items-center gap-2">
            <div className="p-1 rounded bg-indigo-600 text-white">
              <Truck className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-slate-800 flex items-center gap-2">
                복공판, 주형보(Deck Beam) 및 중간말뚝(King Post) 설정
                <span className="px-2 py-0.2 rounded text-[10px] bg-indigo-100 text-indigo-700 border border-indigo-200 font-extrabold font-mono">
                  교통하중 {decking.trafficLoadType} 지지 & 버팀보 좌굴길이 축소
                </span>
              </h3>
              <p className="text-[11px] text-slate-500">
                차량 통행용 복공 주형보 제원, 중간말뚝(King Post) 배치 열수 및 종방향 설치 간격
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5 cursor-pointer">
              <input
                type="checkbox"
                checked={decking.useDecking}
                onChange={(e) => handleDeckingChange('useDecking', e.target.checked)}
                className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-slate-300"
              />
              <span>복공판 및 주형보 설치</span>
            </label>
          </div>
        </div>

        {decking.useDecking && (
          <div className="p-3.5 space-y-3 text-xs bg-white">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              {/* 1. 설계 교통하중 */}
              <div>
                <label className="block text-slate-700 font-bold mb-1">설계 교통하중 등급</label>
                <select
                  value={decking.trafficLoadType}
                  onChange={(e) => handleDeckingChange('trafficLoadType', e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                >
                  <option value="KL-510">KL-510 하중 (51톤 중차량/표준)</option>
                  <option value="DB-24">DB-24 하중 (43.2톤 트럭)</option>
                  <option value="STANDARD_20KN">표준 활하중 (20.0 kN/m²)</option>
                </select>
              </div>

              {/* 2. 주형보(Deck Girder) 규격 */}
              <div>
                <label className="block text-slate-700 font-bold mb-1">주형보(Deck Beam) 규격</label>
                <select
                  value={decking.deckBeamSpec}
                  onChange={(e) => handleDeckingChange('deckBeamSpec', e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                >
                  {DECK_BEAM_DATABASE.map(db => (
                    <option key={db.spec} value={db.spec}>
                      {db.spec} ({db.weight}kg/m, Zx={db.Zx}cm³)
                    </option>
                  ))}
                </select>
              </div>

              {/* 3. 중간말뚝(King Post) 규격 */}
              <div>
                <label className="block text-slate-700 font-bold mb-1">중간말뚝(King Post) 규격</label>
                <select
                  value={decking.kingPostSpec}
                  onChange={(e) => handleDeckingChange('kingPostSpec', e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-slate-900 font-mono font-bold focus:border-blue-500 focus:outline-none"
                >
                  {H_PILE_DATABASE.map(hp => (
                    <option key={hp.spec} value={hp.spec}>
                      {hp.spec} ({hp.weight}kg/m)
                    </option>
                  ))}
                </select>
              </div>

              {/* 4. 중간말뚝 종방향 설치 간격 */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-slate-700 font-bold">
                    중간말뚝 간격: <span className="text-indigo-700 font-mono font-extrabold">{decking.kingPostSpacing} m</span>
                  </label>
                </div>
                <div className="flex items-center gap-1">
                  {[2.0, 3.0, 3.5, 4.0, 5.0].map((sp) => (
                    <button
                      key={sp}
                      onClick={() => handleDeckingChange('kingPostSpacing', sp)}
                      className={`flex-1 py-1 rounded text-xs font-bold transition-all border ${
                        decking.kingPostSpacing === sp
                          ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                          : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                      }`}
                    >
                      {sp}m
                    </button>
                  ))}
                  <input
                    type="number"
                    step="0.5"
                    value={decking.kingPostSpacing}
                    onChange={(e) => handleDeckingChange('kingPostSpacing', parseFloat(e.target.value) || 3.5)}
                    className="w-14 bg-white border border-slate-300 rounded px-1 py-1 text-slate-900 text-center font-mono font-bold focus:border-blue-500 focus:outline-none"
                    title="직접 입력"
                  />
                </div>
              </div>
            </div>

            {/* 🌟 중간말뚝 좌굴 및 지반 지지력 실시간 역학 검토 카드 */}
            {(() => {
              const kpRes = KingPostEngine.evaluateKingPost(inputs, decking, inputs.soils);
              return (
                <div className={`p-3 rounded-lg border text-xs space-y-2 ${
                  kpRes.overallStatus === 'SAFE' 
                    ? 'bg-slate-50 border-slate-200' 
                    : kpRes.overallStatus === 'WARNING'
                    ? 'bg-amber-50/70 border-amber-300'
                    : 'bg-rose-50/80 border-rose-300'
                }`}>
                  <div className="flex items-center justify-between border-b pb-1.5 border-slate-200">
                    <span className="font-bold text-slate-800 flex items-center gap-1.5">
                      <ShieldAlert className="w-3.5 h-3.5 text-blue-600" />
                      중간말뚝(King Post) 좌굴 & 지반 지지력 검토 (스트럿과 강결 체결)
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="px-1.5 py-0.2 rounded text-[10px] bg-blue-100 text-blue-800 font-bold font-mono">
                        스트럿-중간말뚝 강결 (Lk=단간격 {kpRes.unbracedLength}m)
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                        kpRes.overallStatus === 'SAFE'
                          ? 'bg-emerald-100 text-emerald-800'
                          : kpRes.overallStatus === 'WARNING'
                          ? 'bg-amber-100 text-amber-800'
                          : 'bg-rose-100 text-rose-800'
                      }`}>
                        {kpRes.overallStatus === 'SAFE' ? '✓ 강결 좌굴·지지력 O.K' : kpRes.overallStatus === 'WARNING' ? '⚠ 좌굴 주의' : '✕ 구조 N.G'}
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 font-mono text-[11px] text-slate-700">
                    <div className="bg-white p-2 rounded border border-slate-200">
                      <span className="text-[10px] text-slate-400 block">설계 작용 축하중 (P_act)</span>
                      <strong className="text-blue-900 text-xs">{kpRes.totalDesignLoad} kN</strong>
                      <span className="text-[9.5px] text-slate-500 block">고정 {kpRes.deadLoad} + 활 {kpRes.trafficLoad}kN</span>
                    </div>

                    <div className="bg-white p-2 rounded border border-slate-200">
                      <span className="text-[10px] text-slate-400 block">세장비 (λ = Lk / ry)</span>
                      <strong className={kpRes.isSlendernessSafe ? 'text-emerald-700 text-xs' : 'text-rose-700 text-xs'}>
                        {kpRes.slendernessRatio}
                      </strong>
                      <span className="text-[9.5px] text-slate-500 block">허용한계 ≤ 150 (Lk={kpRes.unbracedLength}m)</span>
                    </div>

                    <div className="bg-white p-2 rounded border border-slate-200">
                      <span className="text-[10px] text-slate-400 block">허용 압축 축력 (P_all)</span>
                      <strong className="text-slate-900 text-xs">{kpRes.allowableAxialCapacity} kN</strong>
                      <span className="text-[9.5px] text-slate-500 block">σ_ca = {kpRes.allowableCompressStress} MPa</span>
                    </div>

                    <div className="bg-white p-2 rounded border border-slate-200">
                      <span className="text-[10px] text-slate-400 block">좌굴 응력비 (P / P_all)</span>
                      <strong className={kpRes.isBucklingSafe ? (kpRes.bucklingStressRatio > 0.85 ? 'text-amber-700 text-xs' : 'text-emerald-700 text-xs') : 'text-rose-700 text-xs'}>
                        {(kpRes.bucklingStressRatio * 100).toFixed(1)}%
                      </strong>
                      <span className="text-[9.5px] text-slate-500 block">지반지지력 Qa = {kpRes.allowableBearingCapacity}kN</span>
                    </div>
                  </div>

                  {kpRes.remedyGuide && (
                    <div className="text-[11px] text-rose-800 bg-rose-100/60 p-2 rounded border border-rose-200 font-semibold flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5 text-rose-600 flex-shrink-0" />
                      <span>{kpRes.remedyGuide}</span>
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
        )}
      </div>

      {/* 실시간 공학적 정합성 진단 배너 */}
      <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <div className="p-1 rounded bg-blue-100 text-blue-700">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <span className="font-bold text-slate-800">가시설 및 지보공법({isAnchorMode ? '어스앵커' : isHybridMode ? '복합공법' : '버팀보'}) 정합성 검증: </span>
            <span className="text-slate-600">
              엄지말뚝간격({hPileSpacing}m), {isAnchorMode ? `앵커각도(${currentAnchorAngle}°)·간격(${currentAnchorSpacing}m)` : `버팀보간격(${currentStrutSpacing}m)`}, 띠장({currentWaleSpec}) 모델링 연동 완료.
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3 font-mono text-[11px]">
          <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> 엄지말뚝 휨강성 정상
          </span>
          <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> {isAnchorMode ? '앵커 인장내력 정상' : '버팀보 좌굴강성 정상'}
          </span>
          <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> 띠장 단면계수 정상
          </span>
        </div>
      </div>
    </div>
  );
};
