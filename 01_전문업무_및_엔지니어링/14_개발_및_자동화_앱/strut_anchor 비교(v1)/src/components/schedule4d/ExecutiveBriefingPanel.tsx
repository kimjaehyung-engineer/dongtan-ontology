import React, { useState } from 'react';
import { AlternativeSpanScheduleResult } from '../../engine/structureScheduleEngine';
import { AlternativeSpec, ProjectInputs } from '../../types';
import { ConstructionScheduleEngine } from '../../engine/constructionScheduleEngine';
import { DetailedScheduleBasisModal } from '../report/DetailedScheduleBasisModal';
import { 
  Award, 
  TrendingDown, 
  AlertTriangle, 
  ShieldCheck, 
  Clock, 
  CheckCircle2, 
  Zap,
  Split,
  FileCheck,
  Calendar,
  Layers,
  Truck,
  HardHat
} from 'lucide-react';

interface ExecutiveBriefingPanelProps {
  allSchedules: AlternativeSpanScheduleResult[];
  alternatives: AlternativeSpec[];
  inputs: ProjectInputs;
  selectedAltId: number;
  onSelectAltId: (id: number) => void;
}

export const ExecutiveBriefingPanel: React.FC<ExecutiveBriefingPanelProps> = ({
  allSchedules,
  alternatives,
  inputs,
  selectedAltId,
  onSelectAltId
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const fullSchedules = ConstructionScheduleEngine.calculateSchedules(inputs, alternatives, 2);
  const baselineSchedule = fullSchedules[0] || fullSchedules.find(s => s.altType === 'ALL_STRUT');
  const baselineDays = baselineSchedule?.totalDurationDays || 180;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-4">
      {/* 상단 헤더 */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-amber-50 text-amber-600">
            <Award className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-800 flex items-center gap-2">
              <span>경영진 C-Level 보고용 4대안 전주기(Phase 1~4) 공기·간섭 비교</span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">
                토공 굴착 + RC 골조 + 인발/해체 통합
              </span>
            </h3>
            <p className="text-[11px] text-slate-500">
              벽체·중간말뚝 시공 ➡️ 단계별 굴착/지보 ➡️ 골조 축조 ➡️ 가시설 해체까지 전 공정 공기 및 병목 요인 분석
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold transition-all border border-blue-200 shadow-2xs"
        >
          <Calendar className="w-3.5 h-3.5" />
          <span>공기 정밀 산출 근거서 (품셈 연동)</span>
        </button>
      </div>

      {/* 1. 4대안 핵심 지표 비교 카드 (전체 사업 공기) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {fullSchedules.map((sched) => {
          const isSelected = sched.altId === selectedAltId;
          const savedDays = Math.max(0, baselineDays - sched.totalDurationDays);
          const savedPercent = baselineDays > 0 ? Math.round((savedDays / baselineDays) * 100) : 0;
          const isFastest = savedPercent >= 20;

          return (
            <div
              key={sched.altId}
              onClick={() => onSelectAltId(sched.altId)}
              className={`p-3 rounded-xl border-2 transition-all cursor-pointer relative flex flex-col justify-between ${
                isSelected
                  ? 'border-blue-600 bg-blue-50/40 shadow-md ring-2 ring-blue-200'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-xs'
              }`}
            >
              {isFastest && (
                <div className="absolute -top-2.5 right-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white text-[9px] font-extrabold px-2 py-0.5 rounded-full shadow-sm flex items-center gap-1">
                  <Zap className="w-2.5 h-2.5 fill-current" />
                  <span>전체 공기 최우수 (-{savedPercent}%)</span>
                </div>
              )}

              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[11px] font-bold text-slate-500">
                    대안 {sched.altId}
                  </span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold ${
                    isSelected ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'
                  }`}>
                    {sched.altType}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 mb-2 truncate" title={sched.altName}>
                  {sched.altName}
                </h4>

                {/* 총 공기 및 단축 지표 */}
                <div className="bg-slate-50 rounded-lg p-2 border border-slate-100 space-y-1 mb-2.5 font-mono">
                  <div className="flex items-baseline justify-between">
                    <span className="text-[10px] text-slate-500">총 공사 기간:</span>
                    <span className="text-base font-black text-slate-900">
                      {sched.totalDurationDays} <span className="text-xs font-normal text-slate-500">일 ({sched.totalDurationMonths}개월)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-500">기준안 대비:</span>
                    <span className={`font-bold ${savedDays > 0 ? 'text-emerald-600' : 'text-slate-500'}`}>
                      {savedDays > 0 ? `-${savedDays}일 (${savedPercent}% 단축)` : '기준 (0일)'}
                    </span>
                  </div>
                </div>

                {/* 4단계 세부 공기 Breakdown */}
                <div className="space-y-1 text-[10.5px] font-mono border-t border-slate-100 pt-2 mb-2">
                  <div className="flex items-center justify-between text-slate-600">
                    <span>① 벽체·말뚝:</span>
                    <strong className="text-slate-800">{sched.phases.wallAndPiles.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>② 단계별 굴착:</span>
                    <strong className="text-slate-800">{sched.phases.stepwiseExcavation.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>③ RC 골조 축조:</span>
                    <strong className="text-slate-800">{sched.phases.structure.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>④ 해체·되메우기:</span>
                    <strong className="text-slate-800">{sched.phases.dismantle.durationDays}일</strong>
                  </div>
                </div>

                {/* 공법별 핵심 영향 요약 */}
                <div className="space-y-1 text-[10.5px] border-t border-slate-100 pt-1.5">
                  <div className="text-slate-600">
                    <span className="text-slate-400 block text-[9.5px]">공법 영향:</span>
                    <span className="font-medium text-slate-800">
                      {sched.altType === 'ALL_ANCHOR' 
                        ? '무지보 고속양중 + 갱폼 1회 타설 (단, 앵커양생 대기)'
                        : sched.altType === 'COMPOSITE_STRUT'
                        ? '무중간말뚝 + 모듈러 급속 가설'
                        : sched.altType === 'HYBRID'
                        ? '상부 무지보 + 하부 버팀보 복합 최적화'
                        : '중간말뚝 항타/인발 + 버팀보 2단분할 타설'}
                    </span>
                  </div>
                </div>
              </div>

              {/* 하단 선택 버튼 */}
              <button
                className={`mt-3 w-full py-1 rounded text-xs font-bold transition-all ${
                  isSelected
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                }`}
              >
                {isSelected ? '선택됨 (시뮬레이션 연동)' : '대안 선택 및 시뮬레이션'}
              </button>
            </div>
          );
        })}
      </div>

      {/* 2. 한눈에 이해하는 3대 공기 지연 병목 요인 해설 카드 */}
      <div className="border border-slate-200 rounded-xl p-3.5 bg-slate-50/80 space-y-2">
        <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
          <span>경영진 보고 핵심 포인트: "왜 Strut안은 늦어지고 Anchor안은 빠른가?" (3대 병목 분석)</span>
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-rose-700">
              <Split className="w-3.5 h-3.5" />
              <span>1. 버팀보 간섭 외벽 분할타설 손실</span>
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              버팀보가 흙막이를 지지하고 있어 벽체를 한 번에 못 치고 <strong>버팀보 하단 1차 타설 $\rightarrow$ 2차 타설</strong>로 나눠 쳐야 하므로 거푸집 가공과 시공이음 방수공사로 공기가 낭비됩니다.
            </p>
          </div>

          <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-amber-700">
              <Clock className="w-3.5 h-3.5" />
              <span>2. 콘크리트 압축강도(14MPa) 양생대기 손실</span>
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              버팀보를 해체하려면 1차 타설한 외벽 콘크리트가 굳어 수평 토압을 받을 수 있을 때까지 <strong>스팬당 필수 5~6일간 작업을 중단</strong>하고 대기해야 합니다.
            </p>
          </div>

          <div className="bg-white p-3 rounded-lg border border-slate-200 shadow-xs space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-indigo-700">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>3. 중간말뚝 관통부 후속마감 & LCC 누수 하자</span>
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              본체 슬래브를 뚫고 지나간 중간말뚝(King Post)을 인양하고 박스아웃을 채우는 데 추가 3일이 소요되며, 향후 <strong>지하수 침투 누수 하자의 주원인</strong>이 됩니다.
            </p>
          </div>
        </div>
      </div>
      {/* 세부 공기 정밀 산출 근거 모달 */}
      <DetailedScheduleBasisModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        inputs={inputs}
        alternatives={alternatives}
        selectedAltId={selectedAltId}
      />
    </div>
  );
};
