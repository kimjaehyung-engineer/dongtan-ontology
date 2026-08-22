import React, { useState } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { ConstructionScheduleEngine, AlternativeScheduleResult } from '../../engine/constructionScheduleEngine';
import { DetailedScheduleBasisModal } from '../report/DetailedScheduleBasisModal';
import { 
  Shovel, 
  Truck, 
  HardHat, 
  Calendar, 
  Clock, 
  AlertTriangle, 
  CheckCircle2, 
  Zap, 
  Layers, 
  FileText,
  TrendingDown,
  ShieldCheck,
  RotateCcw
} from 'lucide-react';

interface ExcavationScheduleViewProps {
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAltId: number;
  onSelectAltId: (id: number) => void;
}

export const ExcavationScheduleView: React.FC<ExcavationScheduleViewProps> = ({
  inputs,
  alternatives,
  selectedAltId,
  onSelectAltId
}) => {
  const [activeAltId, setActiveAltId] = useState<number>(selectedAltId || 1);
  const [numCrews, setNumCrews] = useState<number>(1);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const schedules = ConstructionScheduleEngine.calculateSchedules(inputs, alternatives, numCrews);
  const activeSchedule = schedules.find(s => s.altId === activeAltId) || schedules[0];
  const baselineSchedule = schedules[0];

  // 개착(토공+가시설+말뚝+해체) 공기 기준
  const getExcavationDays = (sch: AlternativeScheduleResult) => {
    return sch.phases.wallAndPiles.durationDays + sch.phases.stepwiseExcavation.durationDays + sch.phases.dismantle.durationDays;
  };

  const baselineExcDays = getExcavationDays(baselineSchedule);

  return (
    <div className="space-y-4 font-sans animate-fade-in">
      {/* 1. 상단 안내 헤더 및 액션 바 */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-amber-600 text-white shadow-md">
            <Truck className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-black text-slate-900">
                개착(토공사 & 흙막이 가시설) 공정 및 공기 산정 시스템
              </h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 font-mono">
                구조해석 단수 연동 단계별 굴착 모델
              </span>
            </div>
            <p className="text-xs text-slate-500">
              벽체·중간말뚝 시공 ➡️ 자립고 단계별 굴착 ➡️ 지보재 가설(앵커 조강양생 vs 스트럿 즉시가압) ➡️ 가시설 해체 전주기 분석
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition-all shadow-xs"
          >
            <Calendar className="w-3.5 h-3.5" />
            <span>표준품셈 연동 정밀 산출 근거서</span>
          </button>
        </div>
      </div>

      {/* 2. 4대안 개착 공기 핵심 비교 카드 (Side-by-Side) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {schedules.map((sch) => {
          const isSelected = sch.altId === activeAltId;
          const excDays = getExcavationDays(sch);
          const excMonths = Number((excDays / 30.0).toFixed(1));
          const savedExcDays = Math.max(0, baselineExcDays - excDays);
          const savedPercent = baselineExcDays > 0 ? Math.round((savedExcDays / baselineExcDays) * 100) : 0;
          const isFastest = excDays === Math.min(...schedules.map(s => getExcavationDays(s)));

          return (
            <div
              key={sch.altId}
              onClick={() => {
                setActiveAltId(sch.altId);
                onSelectAltId(sch.altId);
              }}
              className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer relative flex flex-col justify-between ${
                isSelected
                  ? 'border-amber-600 bg-amber-50/40 shadow-md ring-2 ring-amber-200'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-xs'
              }`}
            >
              {isFastest && (
                <div className="absolute -top-2.5 right-3 bg-gradient-to-r from-amber-600 to-orange-600 text-white text-[9px] font-extrabold px-2 py-0.5 rounded-full shadow-sm flex items-center gap-1">
                  <Zap className="w-2.5 h-2.5 fill-current" />
                  <span>개착 최단 공기</span>
                </div>
              )}

              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[11px] font-bold text-slate-500">
                    대안 {sch.altId}
                  </span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold ${
                    isSelected ? 'bg-amber-600 text-white' : 'bg-slate-100 text-slate-700'
                  }`}>
                    {sch.altType}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 mb-2 truncate" title={sch.altName}>
                  {sch.altName}
                </h4>

                {/* 개착 총 공기 */}
                <div className="bg-slate-50 rounded-lg p-2 border border-slate-100 space-y-1 mb-2.5 font-mono">
                  <div className="flex items-baseline justify-between">
                    <span className="text-[10px] text-slate-500">개착 총 공기:</span>
                    <span className="text-base font-black text-amber-900">
                      {excDays} <span className="text-xs font-normal text-slate-500">일 ({excMonths}개월)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-500">기준안 대비:</span>
                    <span className={`font-bold ${savedExcDays > 0 ? 'text-emerald-600' : 'text-slate-500'}`}>
                      {savedExcDays > 0 ? `▲ ${savedExcDays}일 (${savedPercent}% 단축)` : '기준 (0일)'}
                    </span>
                  </div>
                </div>

                {/* 세부 공종 Breakdown */}
                <div className="space-y-1 text-[10.5px] font-mono border-t border-slate-100 pt-2 mb-2">
                  <div className="flex items-center justify-between text-slate-600">
                    <span>① 벽체·말뚝 항타:</span>
                    <strong className="text-slate-800">{sch.phases.wallAndPiles.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>② 단계별 굴착·지보:</span>
                    <strong className="text-slate-800">{sch.phases.stepwiseExcavation.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>③ 해체·인발·되메우기:</span>
                    <strong className="text-slate-800">{sch.phases.dismantle.durationDays}일</strong>
                  </div>
                </div>

                {/* 공법별 핵심 영향 */}
                <div className="text-[10.5px] border-t border-slate-100 pt-1.5 text-slate-600">
                  <span className="text-slate-400 block text-[9.5px]">주요 공정 특징:</span>
                  <span className="font-medium text-slate-800 line-clamp-2">
                    {sch.altType === 'ALL_ANCHOR' 
                      ? '무지보 고속양중(650㎥/일) vs 앵커양생 30일 대기'
                      : sch.altType === 'COMPOSITE_STRUT'
                      ? '무중간말뚝(0본) + 모듈러 2일 가설 즉시 굴착'
                      : sch.altType === 'HYBRID'
                      ? '상부 앵커 양생대기 + 하부 스트럿 즉시 가압'
                      : '중간말뚝 15본 항타/인발 + 버팀보 간섭 양중(450㎥/일)'}
                  </span>
                </div>
              </div>

              <button
                className={`mt-3 w-full py-1 rounded text-xs font-bold transition-all ${
                  isSelected
                    ? 'bg-amber-600 text-white shadow-xs'
                    : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                }`}
              >
                {isSelected ? '선택됨 (상세 조회)' : '선택하여 상세 조회'}
              </button>
            </div>
          );
        })}
      </div>

      {/* 3. 선택된 대안의 구조해석 연동 [단계별 굴착 & 지보 가설 사이클] 정밀 테이블 */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-amber-600" />
            <h3 className="text-xs font-bold text-slate-900">
              [대안 {activeSchedule.altId}: {activeSchedule.altName}] 구조해석 단수 연동 단계별 굴착 & 지보 사이클
            </h3>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            총 토공량: {activeSchedule.totalVolumeM3.toLocaleString()} ㎥ / 굴착심도: GL-{inputs.excavationDepth}m
          </span>
        </div>

        <div className="border border-slate-200 rounded-lg overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-100/90 text-slate-700 border-b border-slate-200 text-[11px]">
                <th className="py-2.5 px-3 font-bold w-14 text-center">단수</th>
                <th className="py-2.5 px-3 font-bold">단계명 (Stage)</th>
                <th className="py-2.5 px-3 font-bold text-center">심도 (GL)</th>
                <th className="py-2.5 px-3 font-bold">지반 종류 & 강도</th>
                <th className="py-2.5 px-3 font-bold text-center">굴착 토량</th>
                <th className="py-2.5 px-3 font-bold text-center">일일 속도</th>
                <th className="py-2.5 px-3 font-bold text-center">순수 굴착</th>
                <th className="py-2.5 px-3 font-bold text-center">지보 가설</th>
                <th className="py-2.5 px-3 font-bold text-center text-rose-700">⚠️ 양생 대기</th>
                <th className="py-2.5 px-3 font-bold text-center text-blue-700">단계 합계</th>
                <th className="py-2.5 px-3 font-bold">현장 시공 메커니즘 및 연속성</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {activeSchedule.stepwiseCycles.map((c) => (
                <tr key={`exc-cycle-${c.tierIndex}`} className="hover:bg-slate-50/80">
                  <td className="py-2.5 px-3 text-center font-mono font-bold text-slate-500">{c.tierIndex}단</td>
                  <td className="py-2.5 px-3 font-bold text-slate-900 font-sans">{c.stageName}</td>
                  <td className="py-2.5 px-3 text-center font-mono font-bold text-slate-700">GL-{c.excavationDepth.toFixed(1)}m</td>
                  <td className="py-2.5 px-3 font-sans font-medium text-amber-900 bg-amber-50/30">
                    <span className="px-1.5 py-0.5 rounded bg-amber-100/70 text-[10.5px]">
                      {c.dominantSoilName || '토사'}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-center font-mono text-slate-600">{c.excavationVolumeM3.toLocaleString()} ㎥</td>
                  <td className="py-2.5 px-3 text-center font-mono text-slate-700 font-semibold">{c.dailyExcavationRate || 500} ㎥/일</td>
                  <td className="py-2.5 px-3 text-center font-mono text-slate-700">{c.pureExcavationDays}일</td>
                  <td className="py-2.5 px-3 text-center font-mono text-slate-700">{c.supportInstallDays > 0 ? `${c.supportInstallDays}일` : '-'}</td>
                  <td className="py-2.5 px-3 text-center font-mono font-bold text-rose-600 bg-rose-50/40">
                    {c.curingWaitDays > 0 ? `⚠️ ${c.curingWaitDays}일` : '-'}
                  </td>
                  <td className="py-2.5 px-3 text-center font-mono font-black text-blue-700 bg-blue-50/40">
                    {c.totalCycleDays}일
                  </td>
                  <td className="py-2.5 px-3 text-slate-600 font-sans text-[11px] leading-relaxed">
                    {c.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. 개착 공법별 핵심 영향 요인 해설 카드 */}
      <div className="border border-slate-200 rounded-xl p-4 bg-slate-50 space-y-3">
        <h4 className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
          <AlertTriangle className="w-4 h-4 text-amber-600" />
          <span>개착 단계에서 각 공법이 공기에 미치는 결정적 차이점 (엔지니어링 분석)</span>
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="bg-white p-3.5 rounded-lg border border-slate-200 shadow-2xs space-y-1.5">
            <span className="font-bold text-slate-900 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-amber-500" />
              <span>1. 앵커 정착장 조강 양생 (5일 대기)</span>
            </span>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              어스앵커는 무지보 고속 양중(650 ㎥/일)이 가능하나, <strong>단별 그라우트 설계강도(14MPa) 발현 전까지 하부 굴착이 금지</strong>되어 단당 5일씩 대기 시간이 발생합니다.
            </p>
          </div>

          <div className="bg-white p-3.5 rounded-lg border border-slate-200 shadow-2xs space-y-1.5">
            <span className="font-bold text-slate-900 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <span>2. 스트럿 가압 즉시 굴착 vs 양중 저하</span>
            </span>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              버팀보는 유압잭 프리로드 가압 즉시 차기 굴착을 할 수 있으나(양생 0일), <strong>내부 버팀보 격자 간섭으로 수직양중 속도(450 ㎥/일)가 31% 감쇄</strong>됩니다.
            </p>
          </div>

          <div className="bg-white p-3.5 rounded-lg border border-slate-200 shadow-2xs space-y-1.5">
            <span className="font-bold text-slate-900 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-600" />
              <span>3. 중간말뚝(King Post) 항타/인발 손실</span>
            </span>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              일반 스트럿은 중간말뚝 항타(8일) 및 사후 인발/3중 방수(5일)로 <strong>총 13일의 추가 공기</strong>가 발생하나, 앵커 및 합성사각은 <strong>0일로 완전 면제</strong>됩니다.
            </p>
          </div>
        </div>
      </div>

      {/* 정밀 산출 근거 모달 */}
      <DetailedScheduleBasisModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        inputs={inputs}
        alternatives={alternatives}
        selectedAltId={activeAltId}
      />
    </div>
  );
};
