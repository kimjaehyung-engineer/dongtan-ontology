import React from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { EngineeringBalanceEngine, EquilibriumDiagnosis, BalanceMetric } from '../../engine/engineeringBalanceEngine';
import { Scale, CheckCircle2, AlertTriangle, Sparkles, Sliders, ArrowRight, ShieldCheck, Zap, HelpCircle } from 'lucide-react';

interface EngineeringBalancePanelProps {
  inputs: ProjectInputs;
  alternative: AlternativeSpec;
  onApplyBalancedInputs: (balancedInputs: ProjectInputs) => void;
}

export const EngineeringBalancePanel: React.FC<EngineeringBalancePanelProps> = ({
  inputs,
  alternative,
  onApplyBalancedInputs
}) => {
  const diag: EquilibriumDiagnosis = EngineeringBalanceEngine.diagnoseEquilibrium(inputs, alternative);

  return (
    <div className="eng-panel border-2 border-emerald-300 shadow-sm bg-gradient-to-br from-white via-emerald-50/20 to-teal-50/30">
      <div className="eng-panel-header bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white flex flex-wrap items-center justify-between gap-3 p-3.5">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-emerald-500 text-slate-950 font-bold shadow-md">
            <Scale className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold text-white tracking-tight">
                가시설 다목적 공학 균형도 진단 (Multi-Objective Equilibrium Optimizer)
              </h3>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-extrabold bg-emerald-400/20 text-emerald-300 border border-emerald-400/40">
                골든존(65%~80%) 수렴 프로세스
              </span>
            </div>
            <p className="text-[11px] text-emerald-200/80">
              어느 한 부재에 과도한 하중이 쏠리지 않고, 좌굴·휨응력·지반지지력이 최적의 안전율로 상호 균형을 이루도록 정밀 조율
            </p>
          </div>
        </div>

        {/* 종합 균형 점수 뱃지 & 원클릭 최적 조율 버튼 */}
        <div className="flex items-center gap-3">
          <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-emerald-500/40 text-center font-mono">
            <span className="text-[10px] text-slate-400 block">역학 균형 지수</span>
            <span className={`text-base font-black ${
              diag.overallScore >= 85 ? 'text-emerald-400' : diag.overallScore >= 70 ? 'text-amber-400' : 'text-rose-400'
            }`}>
              {diag.overallScore} <span className="text-xs font-normal text-slate-400">/ 100점</span>
            </span>
          </div>

          <button
            onClick={() => onApplyBalancedInputs(diag.suggestedBalancedInputs)}
            className="flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-extrabold bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 shadow-md hover:shadow-lg transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <Sparkles className="w-4 h-4 fill-current" />
            <span>⚡ 최적 적정 균형점으로 원클릭 자동 조율</span>
          </button>
        </div>
      </div>

      <div className="p-4 space-y-3 text-xs">
        {/* 5대 핵심 부재별 하중 분담 및 골든존 게이지 그리드 */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-2.5">
          {diag.metrics.map((m, idx) => {
            const pct = Math.min(100, Math.round(m.actualRatio * 100));
            const isOptimal = m.status === 'OPTIMAL';
            const isOverload = m.status === 'OVERLOAD' || m.status === 'CRITICAL_NG';

            return (
              <div
                key={idx}
                className={`p-3 rounded-lg border text-xs space-y-1.5 transition-all ${
                  isOptimal
                    ? 'bg-white border-emerald-300 shadow-xs'
                    : isOverload
                    ? 'bg-rose-50/70 border-rose-300'
                    : 'bg-amber-50/50 border-amber-200'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-bold text-slate-800 text-[11.5px]">{m.name}</span>
                  <span className={`text-[10px] font-mono font-bold px-1.5 py-0.2 rounded ${
                    isOptimal ? 'bg-emerald-100 text-emerald-800' : isOverload ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {isOptimal ? '✓ 골든존' : isOverload ? '⚠ 하중집중' : '○ 과다설계'}
                  </span>
                </div>

                <div className="flex items-baseline justify-between font-mono">
                  <span className="text-[10px] text-slate-500">실제 응력비:</span>
                  <strong className={`text-sm ${
                    isOptimal ? 'text-emerald-700' : isOverload ? 'text-rose-700' : 'text-slate-700'
                  }`}>
                    {pct}%
                  </strong>
                </div>

                {/* 프로그레스 바 (골든존 60~80% 가이드라인 포함) */}
                <div className="space-y-0.5">
                  <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden relative">
                    {/* 골든존 배경 표시 (60% ~ 80%) */}
                    <div className="absolute left-[60%] w-[20%] h-full bg-emerald-200/80 z-0"></div>
                    <div
                      className={`h-full rounded-full transition-all duration-500 z-10 relative ${
                        isOptimal ? 'bg-emerald-600' : isOverload ? 'bg-rose-600' : 'bg-blue-500'
                      }`}
                      style={{ width: `${Math.min(100, pct)}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-[9px] text-slate-400 font-mono">
                    <span>0%</span>
                    <span className="text-emerald-600 font-bold">목표: {Math.round(m.idealMinRatio*100)}~{Math.round(m.idealMaxRatio*100)}%</span>
                    <span>100%</span>
                  </div>
                </div>

                <p className="text-[10px] text-slate-600 font-sans leading-tight">
                  {m.statusText}
                </p>
              </div>
            );
          })}
        </div>

        {/* 종합 진단 및 맞춤 엔지니어링 권고사항 */}
        <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 flex-1">
            <div className="p-1 rounded bg-emerald-100 text-emerald-800">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <span className="font-bold text-slate-900">구조계 균형 상태: </span>
              <span className="text-slate-700 font-semibold">{diag.bottleneckMember}</span>
              <p className="text-[11px] text-slate-500 mt-0.5">
                {diag.recommendations.join(' ')}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-slate-600 font-mono text-[11px] bg-slate-50 px-3 py-1.5 rounded border border-slate-200">
            <span>• 버팀보 과하중 방지</span>
            <span>|</span>
            <span>• 중간말뚝 강결 좌굴 억제</span>
            <span>|</span>
            <span>• 경제성 극대화</span>
          </div>
        </div>
      </div>
    </div>
  );
};
