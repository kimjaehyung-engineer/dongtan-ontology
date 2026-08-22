import React, { useState } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { SmartRemedyEngine, RemedyItem } from '../../engine/remedyEngine';
import { AlertCircle, AlertTriangle, CheckCircle2, Wrench, Sparkles, ArrowRight, ShieldCheck, ChevronDown, ChevronUp, EyeOff } from 'lucide-react';
import confetti from 'canvas-confetti';

interface SmartRemedyPanelProps {
  inputs: ProjectInputs;
  selectedAlt: AlternativeSpec;
  onApplyFix: (updatedInputs: ProjectInputs) => void;
}

export const SmartRemedyPanel: React.FC<SmartRemedyPanelProps> = ({
  inputs,
  selectedAlt,
  onApplyFix
}) => {
  // 사용자의 번거로움을 줄이기 위해 기본 접힘(false) 상태로 제공
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [isDismissed, setIsDismissed] = useState<boolean>(false);
  const effectiveInputs: ProjectInputs = {
    ...inputs,
    wall: selectedAlt.wall,
    supports: selectedAlt.supports
  };

  const remedies = SmartRemedyEngine.diagnose(effectiveInputs, selectedAlt);
  const criticalCount = remedies.filter(r => r.type === 'CRITICAL').length;
  const warningCount = remedies.filter(r => r.type === 'WARNING').length;

  const handleApplySingleFix = (remedy: RemedyItem) => {
    if (remedy.autoFixAction) {
      const updated = remedy.autoFixAction(inputs);
      onApplyFix(updated);
      confetti({ particleCount: 35, spread: 50, origin: { y: 0.3 } });
    }
  };

  const handleApplyAllFixes = () => {
    let current = { ...inputs };
    for (const remedy of remedies) {
      if (remedy.autoFixAction) {
        current = remedy.autoFixAction(current);
      }
    }
    onApplyFix(current);
    confetti({ particleCount: 60, spread: 80, origin: { y: 0.3 } });
  };

  if (isDismissed) {
    return null;
  }

  // 모든 항목이 안전하고 구조적으로도 안전한 경우에만 SAFE 녹색 배너 표시
  if (remedies.length === 0 && selectedAlt.isStructurallySafe) {
    return (
      <div className="bg-emerald-50 border border-emerald-300 rounded-lg p-2.5 px-4 flex items-center justify-between shadow-xs text-xs">
        <div className="flex items-center gap-2.5">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <div>
            <span className="font-bold text-emerald-900">
              구조 안전성 & 지반 안정성 완전 확보 (Stability 100% OK)
            </span>
            <span className="text-[11px] text-emerald-700 ml-2">
              H-Pile 휨응력, 버팀보 좌굴, 띠장, 근입장/보일링 기준 만족
            </span>
          </div>
        </div>

        <span className="px-2 py-0.5 rounded bg-emerald-600 text-white text-[11px] font-bold font-mono">
          ✓ SAFE
        </span>
      </div>
    );
  }

  return (
    <div className="bg-white border border-rose-200 rounded-lg shadow-xs overflow-hidden">
      {/* 1줄 미니 컴팩트 바 (평소에는 화면을 가리지 않음) */}
      <div className="bg-rose-50/80 px-3.5 py-2 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => setIsExpanded(!isExpanded)}>
          <div className="p-1 rounded bg-rose-600 text-white">
            <AlertCircle className="w-3.5 h-3.5" />
          </div>
          <span className="font-bold text-rose-900">
            구조 단면 검토 알림:
          </span>
          <span className="px-2 py-0.2 rounded-full text-[10px] bg-rose-200 text-rose-800 font-extrabold font-mono">
            부적합 {criticalCount}건 {warningCount > 0 && `| 주의 ${warningCount}건`}
          </span>
          <span className="text-[11px] text-rose-700 hidden sm:inline">
            (클릭하여 공학적 권장 대안 확인 {isExpanded ? '▲ 접기' : '▼ 펼치기'})
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* 일괄 자동 보정 버튼 */}
          {criticalCount > 0 && (
            <button
              onClick={handleApplyAllFixes}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold shadow-xs transition-all"
            >
              <Sparkles className="w-3 h-3 text-amber-300 animate-pulse" />
              <span>원클릭 안전 규격 일괄 보정</span>
            </button>
          )}

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 rounded hover:bg-rose-100 text-rose-700"
            title={isExpanded ? '접기' : '펼치기'}
          >
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* 상세 처방 리스트 (사용자가 펼쳤을 때만 노출) */}
      {isExpanded && (
        <div className="p-3 space-y-2.5 bg-white border-t border-rose-100">
          {remedies.map((remedy) => {
            const isCritical = remedy.type === 'CRITICAL';
            return (
              <div
                key={remedy.id}
                className={`p-3 rounded-lg border text-xs space-y-2 ${
                  isCritical
                    ? 'bg-rose-50/40 border-rose-200'
                    : 'bg-amber-50/40 border-amber-200'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className={`px-1.5 py-0.2 rounded text-[10px] font-bold font-mono ${
                        isCritical ? 'bg-rose-600 text-white' : 'bg-amber-600 text-white'
                      }`}>
                        {isCritical ? 'NG 초과' : '주의'}
                      </span>
                      <h4 className="font-bold text-slate-900 text-xs">
                        {remedy.title}
                      </h4>
                    </div>
                    <p className="text-[11px] text-slate-600 font-mono">
                      • {remedy.currentStatus}
                    </p>
                  </div>
                </div>

                {/* 권장 처방 가이드 및 원클릭 버튼 */}
                <div className="bg-white p-2.5 rounded border border-slate-200 flex flex-wrap items-center justify-between gap-2 shadow-2xs">
                  <div className="flex items-start gap-2 flex-1">
                    <Wrench className="w-3.5 h-3.5 text-blue-600 mt-0.5 shrink-0" />
                    <div>
                      <span className="font-bold text-slate-800 text-[11px]">
                        권장 조정안: <span className="text-blue-700">{remedy.primarySuggestion}</span>
                      </span>
                      {remedy.alternativeOptions && remedy.alternativeOptions.length > 0 && (
                        <p className="text-[10px] text-slate-500 mt-0.5">
                          대안 옵션: {remedy.alternativeOptions.join(' | ')}
                        </p>
                      )}
                    </div>
                  </div>

                  {remedy.autoFixAction && (
                    <button
                      onClick={() => handleApplySingleFix(remedy)}
                      className="flex items-center gap-1 px-2.5 py-1 rounded bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-[11px] font-bold transition-colors whitespace-nowrap"
                    >
                      <span>이 제안 바로 적용</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
