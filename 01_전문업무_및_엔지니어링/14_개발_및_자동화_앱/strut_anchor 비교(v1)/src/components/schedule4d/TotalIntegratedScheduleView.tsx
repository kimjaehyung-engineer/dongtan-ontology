import React, { useState } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { ConstructionScheduleEngine, AlternativeScheduleResult } from '../../engine/constructionScheduleEngine';
import { DetailedScheduleBasisModal } from '../report/DetailedScheduleBasisModal';
import { 
  Building2, 
  Truck, 
  Layers, 
  Calendar, 
  Clock, 
  CheckCircle2, 
  Zap, 
  AlertTriangle, 
  TrendingDown, 
  ShieldCheck, 
  FileText,
  Activity,
  GitCommit,
  Split
} from 'lucide-react';

interface TotalIntegratedScheduleViewProps {
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAltId: number;
  onSelectAltId: (id: number) => void;
}

export const TotalIntegratedScheduleView: React.FC<TotalIntegratedScheduleViewProps> = ({
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
  const baselineTotalDays = baselineSchedule.totalDurationDays;

  return (
    <div className="space-y-4 font-sans animate-fade-in">
      {/* 1. 상단 안내 헤더 및 액션 바 */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-600 text-white shadow-md">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-black text-slate-900">
                전체 전주기(개착 토공사 + 본체 구조물 축조) 통합 공기 산정
              </h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800 font-mono">
                Phase 1 ~ Phase 4 라이프사이클 종합 모델
              </span>
            </div>
            <p className="text-xs text-slate-500">
              [Phase 1: 벽체·말뚝] ➡️ [Phase 2: 단계별 굴착/지보] ➡️ [Phase 3: RC 골조 축조] ➡️ [Phase 4: 해체·인발·되메우기] 전 공정 통합 분석
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

      {/* 2. 4대안 전체 공기 종합 비교 카드 (Side-by-Side) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {schedules.map((sch) => {
          const isSelected = sch.altId === activeAltId;
          const totalDays = sch.totalDurationDays;
          const totalMonths = sch.totalDurationMonths;
          const savedDays = Math.max(0, baselineTotalDays - totalDays);
          const savedPercent = baselineTotalDays > 0 ? Math.round((savedDays / baselineTotalDays) * 100) : 0;
          const isFastest = totalDays === Math.min(...schedules.map(s => s.totalDurationDays));

          return (
            <div
              key={sch.altId}
              onClick={() => {
                setActiveAltId(sch.altId);
                onSelectAltId(sch.altId);
              }}
              className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer relative flex flex-col justify-between ${
                isSelected
                  ? 'border-indigo-600 bg-indigo-50/40 shadow-md ring-2 ring-indigo-200'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-xs'
              }`}
            >
              {isFastest && (
                <div className="absolute -top-2.5 right-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white text-[9px] font-extrabold px-2 py-0.5 rounded-full shadow-sm flex items-center gap-1">
                  <Zap className="w-2.5 h-2.5 fill-current" />
                  <span>전체 공기 최단 (-{savedPercent}%)</span>
                </div>
              )}

              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[11px] font-bold text-slate-500">
                    대안 {sch.altId}
                  </span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold ${
                    isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700'
                  }`}>
                    {sch.altType}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 mb-2 truncate" title={sch.altName}>
                  {sch.altName}
                </h4>

                {/* 총 공사 기간 */}
                <div className="bg-slate-50 rounded-lg p-2 border border-slate-100 space-y-1 mb-2.5 font-mono">
                  <div className="flex items-baseline justify-between">
                    <span className="text-[10px] text-slate-500">총 공사 기간:</span>
                    <span className="text-base font-black text-indigo-950">
                      {totalDays} <span className="text-xs font-normal text-slate-500">일 ({totalMonths}개월)</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-500">기준안 대비:</span>
                    <span className={`font-bold ${savedDays > 0 ? 'text-emerald-600' : 'text-slate-500'}`}>
                      {savedDays > 0 ? `▲ ${savedDays}일 (${savedPercent}% 단축)` : '기준 (0일)'}
                    </span>
                  </div>
                </div>

                {/* 4단계 세부 Breakdown */}
                <div className="space-y-1 text-[10.5px] font-mono border-t border-slate-100 pt-2 mb-2">
                  <div className="flex items-center justify-between text-slate-600">
                    <span>① 벽체·말뚝:</span>
                    <strong className="text-slate-800">{sch.phases.wallAndPiles.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>② 단계별 굴착:</span>
                    <strong className="text-slate-800">{sch.phases.stepwiseExcavation.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>③ 본체 RC 골조:</span>
                    <strong className="text-slate-800">{sch.phases.structure.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-slate-600">
                    <span>④ 해체·되메우기:</span>
                    <strong className="text-slate-800">{sch.phases.dismantle.durationDays}일</strong>
                  </div>
                </div>

                {/* 개착 vs 구조물 비율 요약 */}
                <div className="border-t border-slate-100 pt-2 text-[10.5px] space-y-1 font-mono">
                  <div className="flex items-center justify-between text-amber-800 bg-amber-50/50 px-1.5 py-0.5 rounded">
                    <span>개착 소계 (①+②+④):</span>
                    <strong>{sch.phases.wallAndPiles.durationDays + sch.phases.stepwiseExcavation.durationDays + sch.phases.dismantle.durationDays}일</strong>
                  </div>
                  <div className="flex items-center justify-between text-blue-800 bg-blue-50/50 px-1.5 py-0.5 rounded">
                    <span>구조물 소계 (③):</span>
                    <strong>{sch.phases.structure.durationDays}일</strong>
                  </div>
                </div>
              </div>

              <button
                className={`mt-3 w-full py-1 rounded text-xs font-bold transition-all ${
                  isSelected
                    ? 'bg-indigo-600 text-white shadow-xs'
                    : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                }`}
              >
                {isSelected ? '선택됨 (상세 분석)' : '선택하여 상세 분석'}
              </button>
            </div>
          );
        })}
      </div>

      {/* 3. 4대안 전주기 공정 세부 종합 매트릭스 표 */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
        <div className="flex items-center gap-2 border-b border-slate-100 pb-2.5">
          <Activity className="w-4 h-4 text-indigo-600" />
          <h3 className="text-xs font-bold text-slate-900">
            4대안 전주기(Phase 1~4) 공정별 소요 일수 및 시공 영향 요약 매트릭스
          </h3>
        </div>

        <div className="border border-slate-200 rounded-lg overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-100/90 text-slate-700 border-b border-slate-200 text-[11px]">
                <th className="py-2.5 px-3 font-bold w-20 text-center">대안 구분</th>
                <th className="py-2.5 px-3 font-bold">대안명 및 지보 형식</th>
                <th className="py-2.5 px-3 font-bold text-center bg-amber-50/60 text-amber-900">Phase 1<br/>벽체·말뚝</th>
                <th className="py-2.5 px-3 font-bold text-center bg-amber-50/60 text-amber-900">Phase 2<br/>단계별 굴착</th>
                <th className="py-2.5 px-3 font-bold text-center bg-amber-100/70 text-amber-950 font-black">개착 소계</th>
                <th className="py-2.5 px-3 font-bold text-center bg-blue-50/60 text-blue-900">Phase 3<br/>RC 골조 축조</th>
                <th className="py-2.5 px-3 font-bold text-center bg-emerald-50/60 text-emerald-900">Phase 4<br/>해체·되메우기</th>
                <th className="py-2.5 px-3 font-bold text-center bg-indigo-50/80 text-indigo-950 font-black">전체 총 공기</th>
                <th className="py-2.5 px-3 font-bold">공법별 핵심 공기 영향 및 시공성 총평</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {schedules.map((sch) => {
                const isSelected = sch.altId === activeAltId;
                const excSubTotal = sch.phases.wallAndPiles.durationDays + sch.phases.stepwiseExcavation.durationDays + sch.phases.dismantle.durationDays;
                const savedDays = Math.max(0, baselineTotalDays - sch.totalDurationDays);

                return (
                  <tr 
                    key={`total-table-${sch.altId}`}
                    onClick={() => {
                      setActiveAltId(sch.altId);
                      onSelectAltId(sch.altId);
                    }}
                    className={`cursor-pointer transition-colors ${
                      isSelected ? 'bg-indigo-50/50 font-semibold' : 'hover:bg-slate-50'
                    }`}
                  >
                    <td className="py-2.5 px-3 text-center font-mono font-bold text-indigo-700">대안 {sch.altId}</td>
                    <td className="py-2.5 px-3 font-bold text-slate-900">{sch.altName}</td>
                    <td className="py-2.5 px-3 text-center font-mono text-slate-700 bg-amber-50/20">{sch.phases.wallAndPiles.durationDays}일</td>
                    <td className="py-2.5 px-3 text-center font-mono text-slate-700 bg-amber-50/20">{sch.phases.stepwiseExcavation.durationDays}일</td>
                    <td className="py-2.5 px-3 text-center font-mono font-bold text-amber-900 bg-amber-100/40">{excSubTotal}일</td>
                    <td className="py-2.5 px-3 text-center font-mono font-bold text-blue-800 bg-blue-50/30">{sch.phases.structure.durationDays}일</td>
                    <td className="py-2.5 px-3 text-center font-mono text-slate-700 bg-emerald-50/20">{sch.phases.dismantle.durationDays}일</td>
                    <td className="py-2.5 px-3 text-center font-mono font-black text-sm text-indigo-950 bg-indigo-50/60">
                      {sch.totalDurationDays}일
                      <span className="text-[10px] block font-normal text-slate-500 font-sans">
                        ({sch.totalDurationMonths}개월{savedDays > 0 ? ` · ▲${savedDays}일` : ''})
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-600 font-sans text-[11px] leading-relaxed">
                      {sch.altType === 'ALL_ANCHOR' && (
                        <span>
                          굴착 시 앵커양생(+30일) 대기가 있으나, <strong>골조 일체타설(55일) 및 무중간말뚝(0일)</strong>으로 전체 공기 압도적 1위 달성
                        </span>
                      )}
                      {sch.altType === 'COMPOSITE_STRUT' && (
                        <span>
                          <strong>중간말뚝 100% 삭제 + 모듈러 급속 가설</strong>로 버팀보 공법 중 최단 공기 달성
                        </span>
                      )}
                      {sch.altType === 'HYBRID' && (
                        <span>
                          상부 앵커 무지보 일체타설 + 하부 버팀보 조합으로 <strong>공기 단축 및 부지경계 침범 방지</strong>
                        </span>
                      )}
                      {sch.altType === 'ALL_STRUT' && (
                        <span>
                          버팀보 간섭 외벽 2단 분할타설 및 중간말뚝 15본 항타/인발로 <strong>전체 공기 최장</strong>
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* 🌟 4. [선택된 대안] 주요 액티비티(Activity)별 공기산정 근거 심층 분석 패널 */}
      <div className="bg-white rounded-xl border border-indigo-200 shadow-md p-5 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-indigo-100 pb-3">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-indigo-700 text-white shadow-xs">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-black text-slate-900">
                  [대안 {activeSchedule.altId}: {activeSchedule.altName}] 주요 액티비티(Activity)별 공기산정 근거 상세
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800 font-mono">
                  {activeSchedule.altType}
                </span>
              </div>
              <p className="text-xs text-slate-500">
                표준품셈, 투입 장비 생산성, 수량 및 공학적 시공 간섭 요인을 반영한 액티비티별 산출 수식(Formula)
              </p>
            </div>
          </div>

          {/* 대안 선택 탭 스위처 */}
          <div className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200 gap-1 text-xs">
            {schedules.map((s) => (
              <button
                key={`btn-alt-sel-${s.altId}`}
                onClick={() => {
                  setActiveAltId(s.altId);
                  onSelectAltId(s.altId);
                }}
                className={`px-3 py-1.5 rounded-md font-bold transition-all ${
                  activeAltId === s.altId
                    ? 'bg-indigo-600 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
                }`}
              >
                대안 {s.altId} ({s.altType})
              </button>
            ))}
          </div>
        </div>

        {/* Phase 1 ~ 4 세부 액티비티 카드 그리드 */}
        <div className="space-y-4">
          {/* Phase 1. 벽체 및 중간말뚝 시공 액티비티 */}
          <div className="border border-amber-200 rounded-xl overflow-hidden bg-white shadow-2xs">
            <div className="bg-amber-50 px-4 py-2.5 border-b border-amber-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-600" />
                <strong className="text-xs text-amber-950 font-bold">
                  {activeSchedule.phases.wallAndPiles.name}
                </strong>
              </div>
              <span className="text-xs font-mono font-bold text-amber-900 bg-amber-200/70 px-2 py-0.5 rounded">
                소계: {activeSchedule.phases.wallAndPiles.durationDays}일
              </span>
            </div>
            <div className="p-3.5 space-y-2 text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50/80 text-[11px]">
                    <th className="py-2 px-3 w-56">세부 액티비티 (Activity)</th>
                    <th className="py-2 px-3 text-center w-20">공기</th>
                    <th className="py-2 px-3">📐 구체적 산출 수식 및 생산성 근거 (Formula)</th>
                    <th className="py-2 px-3">현장 시공 특성 및 표준품셈 기준</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs font-sans">
                  {activeSchedule.phases.wallAndPiles.subTasks.map((t, idx) => (
                    <tr key={`p1-${idx}`} className="hover:bg-amber-50/30">
                      <td className="py-2.5 px-3 font-bold text-slate-800">{t.name}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-black text-amber-900 bg-amber-50/50">{t.days}일</td>
                      <td className="py-2.5 px-3 font-mono font-bold text-indigo-900 bg-indigo-50/20">{t.formula}</td>
                      <td className="py-2.5 px-3 text-slate-600 space-y-0.5 text-[11px]">
                        <div>{t.note}</div>
                        {t.standardBasis && <div className="text-slate-400 font-mono">↳ {t.standardBasis}</div>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Phase 2. 단계별 굴착 및 지보 가설 액티비티 */}
          <div className="border border-amber-200 rounded-xl overflow-hidden bg-white shadow-2xs">
            <div className="bg-amber-50 px-4 py-2.5 border-b border-amber-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-600" />
                <strong className="text-xs text-amber-950 font-bold">
                  {activeSchedule.phases.stepwiseExcavation.name} (단별 자립고 굴착 ➡️ 지보 가설 ➡️ 앵커양생 사이클)
                </strong>
              </div>
              <span className="text-xs font-mono font-bold text-amber-900 bg-amber-200/70 px-2 py-0.5 rounded">
                소계: {activeSchedule.phases.stepwiseExcavation.durationDays}일
              </span>
            </div>
            <div className="p-3.5 space-y-2 text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50/80 text-[11px]">
                    <th className="py-2 px-3 w-56">세부 액티비티 (Activity)</th>
                    <th className="py-2 px-3 text-center w-20">공기</th>
                    <th className="py-2 px-3">📐 구체적 산출 수식 및 생산성 근거 (Formula)</th>
                    <th className="py-2 px-3">현장 시공 특성 및 표준품셈 기준</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs font-sans">
                  {activeSchedule.phases.stepwiseExcavation.subTasks.map((t, idx) => (
                    <tr key={`p2-${idx}`} className="hover:bg-amber-50/30">
                      <td className="py-2.5 px-3 font-bold text-slate-800">{t.name}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-black text-amber-900 bg-amber-50/50">{t.days}일</td>
                      <td className="py-2.5 px-3 font-mono font-bold text-indigo-900 bg-indigo-50/20">{t.formula}</td>
                      <td className="py-2.5 px-3 text-slate-600 space-y-0.5 text-[11px]">
                        <div>{t.note}</div>
                        {t.standardBasis && <div className="text-slate-400 font-mono">↳ {t.standardBasis}</div>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Phase 3. 본체 RC 구조물 축조 액티비티 */}
          <div className="border border-blue-200 rounded-xl overflow-hidden bg-white shadow-2xs">
            <div className="bg-blue-50 px-4 py-2.5 border-b border-blue-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600" />
                <strong className="text-xs text-blue-950 font-bold">
                  {activeSchedule.phases.structure.name} (바닥기초 / 외벽 / 중간슬래브 / 지붕슬래브 축조)
                </strong>
              </div>
              <span className="text-xs font-mono font-bold text-blue-900 bg-blue-200/70 px-2 py-0.5 rounded">
                소계: {activeSchedule.phases.structure.durationDays}일
              </span>
            </div>
            <div className="p-3.5 space-y-2 text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50/80 text-[11px]">
                    <th className="py-2 px-3 w-56">세부 액티비티 (Activity)</th>
                    <th className="py-2 px-3 text-center w-20">공기</th>
                    <th className="py-2 px-3">📐 구체적 산출 수식 및 생산성 근거 (Formula)</th>
                    <th className="py-2 px-3">현장 시공 특성 및 표준품셈 기준</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs font-sans">
                  {activeSchedule.phases.structure.subTasks.map((t, idx) => (
                    <tr key={`p3-${idx}`} className="hover:bg-blue-50/30">
                      <td className="py-2.5 px-3 font-bold text-slate-800">{t.name}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-black text-blue-900 bg-blue-50/50">{t.days}일</td>
                      <td className="py-2.5 px-3 font-mono font-bold text-indigo-900 bg-indigo-50/20">{t.formula}</td>
                      <td className="py-2.5 px-3 text-slate-600 space-y-0.5 text-[11px]">
                        <div>{t.note}</div>
                        {t.standardBasis && <div className="text-slate-400 font-mono">↳ {t.standardBasis}</div>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Phase 4. 해체·인발·되메우기 액티비티 */}
          <div className="border border-emerald-200 rounded-xl overflow-hidden bg-white shadow-2xs">
            <div className="bg-emerald-50 px-4 py-2.5 border-b border-emerald-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-600" />
                <strong className="text-xs text-emerald-950 font-bold">
                  {activeSchedule.phases.dismantle.name}
                </strong>
              </div>
              <span className="text-xs font-mono font-bold text-emerald-900 bg-emerald-200/70 px-2 py-0.5 rounded">
                소계: {activeSchedule.phases.dismantle.durationDays}일
              </span>
            </div>
            <div className="p-3.5 space-y-2 text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50/80 text-[11px]">
                    <th className="py-2 px-3 w-56">세부 액티비티 (Activity)</th>
                    <th className="py-2 px-3 text-center w-20">공기</th>
                    <th className="py-2 px-3">📐 구체적 산출 수식 및 생산성 근거 (Formula)</th>
                    <th className="py-2 px-3">현장 시공 특성 및 표준품셈 기준</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs font-sans">
                  {activeSchedule.phases.dismantle.subTasks.map((t, idx) => (
                    <tr key={`p4-${idx}`} className="hover:bg-emerald-50/30">
                      <td className="py-2.5 px-3 font-bold text-slate-800">{t.name}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-black text-emerald-900 bg-emerald-50/50">{t.days}일</td>
                      <td className="py-2.5 px-3 font-mono font-bold text-indigo-900 bg-indigo-50/20">{t.formula}</td>
                      <td className="py-2.5 px-3 text-slate-600 space-y-0.5 text-[11px]">
                        <div>{t.note}</div>
                        {t.standardBasis && <div className="text-slate-400 font-mono">↳ {t.standardBasis}</div>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* 5. 4대안 핵심 액티비티 Side-by-Side 비교 대조표 */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
        <div className="flex items-center gap-2 border-b border-slate-100 pb-2.5">
          <Split className="w-4 h-4 text-indigo-600" />
          <h3 className="text-xs font-bold text-slate-900">
            4대안 주요 핵심 액티비티(Activity) 일수 Side-by-Side 비교 대조표
          </h3>
        </div>

        <div className="border border-slate-200 rounded-lg overflow-hidden">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-100/90 text-slate-700 border-b border-slate-200 text-[11px]">
                <th className="py-2.5 px-3 font-bold w-48">공종 및 주요 액티비티</th>
                <th className="py-2.5 px-3 text-center font-bold">① All-Strut<br/>(버팀보)</th>
                <th className="py-2.5 px-3 text-center font-bold bg-emerald-50 text-emerald-900">② All-Anchor<br/>(어스앵커)</th>
                <th className="py-2.5 px-3 text-center font-bold">③ Hybrid<br/>(복합형)</th>
                <th className="py-2.5 px-3 text-center font-bold bg-indigo-50 text-indigo-900">④ Composite<br/>(합성사각)</th>
                <th className="py-2.5 px-3 font-bold">공법별 액티비티 공기 차이 원인</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              <tr>
                <td className="py-2 px-3 font-bold text-slate-800">1-1. H-Pile 벽체 천공/항타</td>
                <td className="py-2 px-3 text-center font-mono">{schedules[0].phases.wallAndPiles.subTasks[0]?.days || 76}일</td>
                <td className="py-2 px-3 text-center font-mono bg-emerald-50/40 font-bold">{schedules[1].phases.wallAndPiles.subTasks[0]?.days || 76}일</td>
                <td className="py-2 px-3 text-center font-mono">{schedules[2].phases.wallAndPiles.subTasks[0]?.days || 76}일</td>
                <td className="py-2 px-3 text-center font-mono bg-indigo-50/40 font-bold">{schedules[3].phases.wallAndPiles.subTasks[0]?.days || 76}일</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">외주연장 및 H-Pile 간격(@1.8m) 동일 (1일 3본 현장 실적)</td>
              </tr>
              <tr className="bg-slate-50/40">
                <td className="py-2 px-3 font-bold text-slate-800">1-2. 중간말뚝(King Post) 항타</td>
                <td className="py-2 px-3 text-center font-mono text-rose-700 font-bold">{schedules[0].phases.wallAndPiles.subTasks[1]?.days || 20}일</td>
                <td className="py-2 px-3 text-center font-mono text-emerald-700 font-black bg-emerald-50/60">0일 ⚡</td>
                <td className="py-2 px-3 text-center font-mono">{schedules[2].phases.wallAndPiles.subTasks[1]?.days || 14}일</td>
                <td className="py-2 px-3 text-center font-mono text-indigo-700 font-black bg-indigo-50/60">0일 ⚡</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">2안/4안은 무중간말뚝 설계로 King Post 항타 공기 완전 면제</td>
              </tr>
              <tr>
                <td className="py-2 px-3 font-bold text-slate-800">2-1. 지반 단계별 굴착</td>
                <td className="py-2 px-3 text-center font-mono">{schedules[0].phases.stepwiseExcavation.subTasks[0]?.days}일</td>
                <td className="py-2 px-3 text-center font-mono bg-emerald-50/40 font-bold">{schedules[1].phases.stepwiseExcavation.subTasks[0]?.days}일 ⚡</td>
                <td className="py-2 px-3 text-center font-mono">{schedules[2].phases.stepwiseExcavation.subTasks[0]?.days}일</td>
                <td className="py-2 px-3 text-center font-mono bg-indigo-50/40 font-bold">{schedules[3].phases.stepwiseExcavation.subTasks[0]?.days}일</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">무지보 개방 공간 양중(앵커) vs 버팀보 간섭 백호 선회 감쇄(스트럿)</td>
              </tr>
              <tr className="bg-slate-50/40">
                <td className="py-2 px-3 font-bold text-slate-800">2-2. 앵커 양생대기 vs 스트럿가압</td>
                <td className="py-2 px-3 text-center font-mono text-blue-700">0일 (즉시굴착)</td>
                <td className="py-2 px-3 text-center font-mono text-rose-700 font-bold bg-emerald-50/40">+30일 대기 ⚠️</td>
                <td className="py-2 px-3 text-center font-mono">+15일 대기</td>
                <td className="py-2 px-3 text-center font-mono text-blue-700 bg-indigo-50/40">0일 (즉시굴착)</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">어스앵커는 단별 정착장 14MPa 조강 양생 5일 필수 대기</td>
              </tr>
              <tr>
                <td className="py-2 px-3 font-bold text-slate-800">3-1. 외벽 타설 방식</td>
                <td className="py-2 px-3 text-center font-mono text-rose-700">2단 분할타설</td>
                <td className="py-2 px-3 text-center font-mono text-emerald-700 font-black bg-emerald-50/60">1회 일체타설 ⚡</td>
                <td className="py-2 px-3 text-center font-mono">혼합 타설</td>
                <td className="py-2 px-3 text-center font-mono text-indigo-700 font-bold bg-indigo-50/40">광폭 시공</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">어스앵커는 대형 갱폼으로 일체타설, 스트럿은 버팀보 간섭으로 분할타설</td>
              </tr>
              <tr className="bg-slate-50/40">
                <td className="py-2 px-3 font-bold text-slate-800">3-2. 14MPa 양생 & 해체대기</td>
                <td className="py-2 px-3 text-center font-mono text-rose-700 font-bold">+23일 지연 ⚠️</td>
                <td className="py-2 px-3 text-center font-mono text-emerald-700 font-black bg-emerald-50/60">0일 (간섭없음) ⚡</td>
                <td className="py-2 px-3 text-center font-mono">+12일 지연</td>
                <td className="py-2 px-3 text-center font-mono text-indigo-700 font-bold bg-indigo-50/40">+8일 지연</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">스트럿은 외벽 1차 콘크리트 강도 발현 전까지 버팀보 해체 불가 대기</td>
              </tr>
              <tr>
                <td className="py-2 px-3 font-bold text-slate-800">4-1. 중간말뚝 인발 & 관통부 방수</td>
                <td className="py-2 px-3 text-center font-mono text-rose-700 font-bold">5일 소요</td>
                <td className="py-2 px-3 text-center font-mono text-emerald-700 font-black bg-emerald-50/60">0일 ⚡</td>
                <td className="py-2 px-3 text-center font-mono">3일 소요</td>
                <td className="py-2 px-3 text-center font-mono text-indigo-700 font-black bg-indigo-50/60">0일 ⚡</td>
                <td className="py-2 px-3 text-slate-600 text-[11px]">무중간말뚝 공법은 슬래브 관통부 인발 및 3중 무수축방수 마감 불필요</td>
              </tr>
              <tr className="bg-indigo-50/80 font-bold border-t-2 border-indigo-200">
                <td className="py-2.5 px-3 text-indigo-950 font-black">전체 총 공사 기간</td>
                <td className="py-2.5 px-3 text-center font-mono font-black text-indigo-950">{schedules[0].totalDurationDays}일</td>
                <td className="py-2.5 px-3 text-center font-mono font-black text-emerald-900 bg-emerald-100/60">{schedules[1].totalDurationDays}일 (▲{baselineTotalDays - schedules[1].totalDurationDays}일)</td>
                <td className="py-2.5 px-3 text-center font-mono font-black text-indigo-950">{schedules[2].totalDurationDays}일 (▲{baselineTotalDays - schedules[2].totalDurationDays}일)</td>
                <td className="py-2.5 px-3 text-center font-mono font-black text-indigo-900 bg-indigo-100/60">{schedules[3].totalDurationDays}일 (▲{baselineTotalDays - schedules[3].totalDurationDays}일)</td>
                <td className="py-2.5 px-3 text-indigo-900 font-sans text-[11px]">대안 2 All-Anchor 최단 공기 / 대안 4 Composite-Strut 버팀보 최적</td>
              </tr>
            </tbody>
          </table>
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
