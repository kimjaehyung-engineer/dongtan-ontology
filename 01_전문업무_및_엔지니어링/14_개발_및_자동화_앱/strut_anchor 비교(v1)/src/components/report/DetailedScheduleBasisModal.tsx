import React, { useState } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { ConstructionScheduleEngine, AlternativeScheduleResult } from '../../engine/constructionScheduleEngine';
import {
  X,
  Printer,
  Calendar,
  Clock,
  Layers,
  ArrowRight,
  TrendingDown,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Info,
  Users,
  HardHat,
  Truck,
  Building2,
  FileText
} from 'lucide-react';

interface DetailedScheduleBasisModalProps {
  isOpen: boolean;
  onClose: () => void;
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAltId: number;
}

export const DetailedScheduleBasisModal: React.FC<DetailedScheduleBasisModalProps> = ({
  isOpen,
  onClose,
  inputs,
  alternatives,
  selectedAltId
}) => {
  const [activeAltId, setActiveAltId] = useState<number>(selectedAltId || 1);
  const [numCrews, setNumCrews] = useState<number>(1);

  if (!isOpen) return null;

  const schedules = ConstructionScheduleEngine.calculateSchedules(inputs, alternatives, numCrews);
  const activeSchedule = schedules.find(s => s.altId === activeAltId) || schedules[0];
  const baselineSchedule = schedules[0];

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-300 w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* 모달 상단 헤더 */}
        <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800 shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-indigo-600 shadow-md">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white font-mono">
                  가시설 지보공법별 공사기간(공기) 정밀 산출 근거서
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/30 text-indigo-300 border border-indigo-400/40 font-mono">
                  건설공사 표준품셈 & 도로교설계기준 연동
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">
                굴착심도 EL -{inputs.excavationDepth.toFixed(1)}m, 굴착폭 {inputs.excavationWidth}m, 연장 {inputs.totalWallPerimeter}m 기준 정밀 공정 일정 산출 근거
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all border border-slate-700"
            >
              <Printer className="w-4 h-4" />
              <span>A4 인쇄</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* 탭 전환 바 (3개 대안 선택 & 작업팀 수 시뮬레이션) */}
        <div className="bg-slate-100 px-6 py-3 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 shrink-0">
          {/* 3대안 탭 */}
          <div className="flex items-center gap-2">
            {schedules.map((sch) => {
              const isSelected = sch.altId === activeAltId;
              return (
                <button
                  key={sch.altId}
                  onClick={() => setActiveAltId(sch.altId)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all border ${
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-600 shadow-sm ring-2 ring-blue-300'
                      : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <span>대안 {sch.altId}: {sch.altName.split('(')[0]}</span>
                  <span className={`px-2 py-0.5 rounded text-[11px] font-mono ${isSelected ? 'bg-blue-700 text-white' : 'bg-slate-100 text-slate-600'}`}>
                    {sch.totalDurationDays}일
                  </span>
                </button>
              );
            })}
          </div>

          {/* 작업팀 수 옵션 */}
          <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-slate-300 text-xs font-mono">
            <Users className="w-3.5 h-3.5 text-indigo-600" />
            <span className="text-slate-600 font-bold">투입 골조팀:</span>
            <div className="flex rounded border border-slate-300 overflow-hidden">
              <button
                onClick={() => setNumCrews(1)}
                className={`px-2.5 py-0.5 font-bold ${numCrews === 1 ? 'bg-indigo-600 text-white' : 'bg-slate-50 text-slate-700'}`}
              >
                1팀 (표준)
              </button>
              <button
                onClick={() => setNumCrews(2)}
                className={`px-2.5 py-0.5 font-bold ${numCrews === 2 ? 'bg-indigo-600 text-white' : 'bg-slate-50 text-slate-700'}`}
              >
                2팀 (교대 증원)
              </button>
            </div>
          </div>
        </div>

        {/* 모달 메인 스크롤 영역 */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-800">
          {/* 🌟 1. 대안별 종합 공기 비교 요약 카드 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {schedules.map((sch) => {
              const isSelected = sch.altId === activeAltId;
              const isFastest = sch.totalDurationDays === Math.min(...schedules.map(s => s.totalDurationDays));

              return (
                <div
                  key={sch.altId}
                  onClick={() => setActiveAltId(sch.altId)}
                  className={`cursor-pointer rounded-xl p-4 border transition-all ${
                    isSelected
                      ? 'bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-500 shadow-md ring-2 ring-blue-400'
                      : 'bg-white border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-bold font-mono text-slate-500">
                      대안 {sch.altId} • {sch.altType}
                    </span>
                    {isFastest && (
                      <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-extrabold text-[10px] border border-emerald-300">
                        ⚡ 최단 공기
                      </span>
                    )}
                  </div>

                  <h4 className="text-sm font-bold text-slate-900 mb-3">
                    {sch.altName}
                  </h4>

                  <div className="space-y-1.5 text-xs font-mono">
                    <div className="flex justify-between py-1 border-b border-slate-200/80">
                      <span className="text-slate-500">① 벽체 & 중간말뚝</span>
                      <strong className="text-slate-800">{sch.phases.wallAndPiles.durationDays}일</strong>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-200/80">
                      <span className="text-slate-500">② 단계별 굴착 & 지보</span>
                      <strong className="text-slate-800">{sch.phases.stepwiseExcavation.durationDays}일</strong>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-200/80">
                      <span className="text-slate-500">③ 지하 RC 본체 축조</span>
                      <strong className="text-slate-800">{sch.phases.structure.durationDays}일</strong>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-200/80">
                      <span className="text-slate-500">④ 해체, 인발 & 되메우기</span>
                      <strong className="text-slate-800">{sch.phases.dismantle.durationDays}일</strong>
                    </div>
                    <div className="flex justify-between pt-2 text-sm">
                      <span className="font-bold text-slate-700 font-sans">총 소요 공기</span>
                      <strong className="font-black text-blue-700">
                        {sch.totalDurationDays}일 ({sch.totalDurationMonths}개월)
                      </strong>
                    </div>
                    <div className="flex justify-between text-[11px] text-emerald-700 font-bold">
                      <span>기준안 대비 단축</span>
                      <span>
                        {sch.altId === 1 ? '-' : `▲ ${sch.savedDaysComparedToBaseline}일 (${sch.savedMonthsComparedToBaseline}개월 단축)`}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* 🌟 2. 선택된 대안의 4단계 세부 공종별 정밀 산출 근거표 */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-600" />
                <span>[대안 {activeSchedule.altId}] 전주기(Phase 1~4) 세부 시공단계별 작업 일수 산출 내역</span>
              </h4>
              <span className="text-xs text-slate-500 font-mono">
                벽체외주: {activeSchedule.wallPerimeterM.toFixed(0)}m / 총 토공량: {activeSchedule.totalVolumeM3.toLocaleString()} ㎥ / 지하 {activeSchedule.numStories}층 구조물
              </span>
            </div>

            {/* Phase 1: 흙막이벽체 및 중간말뚝 시공 */}
            <div className="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-xs">
              <div className="bg-slate-100 px-4 py-2.5 border-b border-slate-200 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <HardHat className="w-4 h-4 text-slate-700" />
                  <strong className="text-xs text-slate-950 font-bold">
                    {activeSchedule.phases.wallAndPiles.name}
                  </strong>
                </div>
                <span className="text-xs font-mono font-bold text-slate-900 bg-slate-200/80 px-2 py-0.5 rounded">
                  소계: {activeSchedule.phases.wallAndPiles.durationDays}일
                </span>
              </div>
              <div className="p-4 space-y-3 text-xs">
                <p className="text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200 leading-relaxed">
                  <strong>공학적 산정 특성:</strong> {activeSchedule.phases.wallAndPiles.description}
                </p>
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50">
                      <th className="py-2.5 px-3">세부 작업 공종</th>
                      <th className="py-2.5 px-3 text-center">소요 일수</th>
                      <th className="py-2.5 px-3">📐 구체적 산출 수식 (Formula)</th>
                      <th className="py-2.5 px-3">현장 시공 특성 및 표준품셈 근거</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-xs">
                    {activeSchedule.phases.wallAndPiles.subTasks.map((t, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/80">
                        <td className="py-2.5 px-3 font-sans font-bold text-slate-800">{t.name}</td>
                        <td className="py-2.5 px-3 text-center font-mono font-bold text-blue-700 bg-blue-50/40">{t.days}일</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-indigo-800 bg-indigo-50/30">
                          {t.formula || `${t.days}일`}
                        </td>
                        <td className="py-2.5 px-3 font-sans text-slate-600 space-y-0.5">
                          <div>{t.note}</div>
                          {t.standardBasis && (
                            <div className="text-[11px] text-slate-500 font-mono">
                              ↳ <span className="underline decoration-slate-300">{t.standardBasis}</span>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Phase 2: 단계별 굴착 & 가시설 지보 가설 */}
            <div className="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-xs">
              <div className="bg-amber-50 px-4 py-2.5 border-b border-amber-200 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Truck className="w-4 h-4 text-amber-700" />
                  <strong className="text-xs text-amber-950 font-bold">
                    {activeSchedule.phases.stepwiseExcavation.name}
                  </strong>
                </div>
                <span className="text-xs font-mono font-bold text-amber-900 bg-amber-200/60 px-2 py-0.5 rounded">
                  소계: {activeSchedule.phases.stepwiseExcavation.durationDays}일
                </span>
              </div>
              <div className="p-4 space-y-3 text-xs">
                <p className="text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200 leading-relaxed">
                  <strong>공학적 산정 특성:</strong> {activeSchedule.phases.stepwiseExcavation.description}
                </p>

                {/* 🌟 단계별 굴착/지보 세부 사이클 테이블 */}
                <div className="border border-amber-200/80 rounded-lg overflow-hidden">
                  <div className="bg-amber-100/60 px-3 py-1.5 font-bold text-[11px] text-amber-900 border-b border-amber-200">
                    🔍 구조해석 연동 단계별(Tier-by-Tier) 굴착 및 지보재 가설 사이클 상세
                  </div>
                  <table className="w-full text-left border-collapse text-[11px]">
                    <thead>
                      <tr className="bg-amber-50/50 text-slate-600 border-b border-amber-200">
                        <th className="py-2 px-2.5 font-bold">단계명 (Stage)</th>
                        <th className="py-2 px-2.5 text-center font-bold">굴착심도</th>
                        <th className="py-2 px-2.5 font-bold">지반 종류 & 강도</th>
                        <th className="py-2 px-2.5 text-center font-bold">일일 속도</th>
                        <th className="py-2 px-2.5 text-center font-bold">순수굴착</th>
                        <th className="py-2 px-2.5 text-center font-bold">지보가설</th>
                        <th className="py-2 px-2.5 text-center font-bold text-rose-700">양생대기</th>
                        <th className="py-2 px-2.5 text-center font-bold text-blue-700">합계</th>
                        <th className="py-2 px-2.5 font-bold">세부 시공 메커니즘</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-amber-100">
                      {activeSchedule.stepwiseCycles.map((c, cIdx) => (
                        <tr key={`cycle-${cIdx}`} className="hover:bg-amber-50/40">
                          <td className="py-2 px-2.5 font-bold text-slate-800 font-sans">{c.stageName}</td>
                          <td className="py-2 px-2.5 text-center font-mono font-bold text-slate-700">GL-{c.excavationDepth.toFixed(1)}m</td>
                          <td className="py-2 px-2.5 font-sans font-medium text-amber-900 bg-amber-50/20">
                            <span className="px-1.5 py-0.5 rounded bg-amber-100/80 text-[10.5px]">
                              {c.dominantSoilName || '토사'}
                            </span>
                          </td>
                          <td className="py-2 px-2.5 text-center font-mono text-slate-700 font-semibold">{c.dailyExcavationRate || 500} ㎥/일</td>
                          <td className="py-2 px-2.5 text-center font-mono text-slate-700">{c.pureExcavationDays}일</td>
                          <td className="py-2 px-2.5 text-center font-mono text-slate-700">{c.supportInstallDays > 0 ? `${c.supportInstallDays}일` : '-'}</td>
                          <td className="py-2 px-2.5 text-center font-mono font-bold text-rose-600">
                            {c.curingWaitDays > 0 ? `⚠️ ${c.curingWaitDays}일` : '-'}
                          </td>
                          <td className="py-2 px-2.5 text-center font-mono font-bold text-blue-700 bg-blue-50/30">
                            {c.totalCycleDays}일
                          </td>
                          <td className="py-2 px-2.5 text-slate-600 font-sans text-[10.5px]">{c.description}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Phase 3: 지하 RC 본구조물 축조 */}
            <div className="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-xs">
              <div className="bg-blue-50 px-4 py-2.5 border-b border-blue-200 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Building2 className="w-4 h-4 text-blue-700" />
                  <strong className="text-xs text-blue-950 font-bold">
                    {activeSchedule.phases.structure.name}
                  </strong>
                </div>
                <span className="text-xs font-mono font-bold text-blue-900 bg-blue-200/60 px-2 py-0.5 rounded">
                  소계: {activeSchedule.phases.structure.durationDays}일
                </span>
              </div>
              <div className="p-4 space-y-3 text-xs">
                <p className="text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200 leading-relaxed">
                  <strong>공학적 산정 특성:</strong> {activeSchedule.phases.structure.description}
                  {activeSchedule.blockOutJointCount > 0 && (
                    <span className="text-rose-600 font-bold block mt-1">
                      ⚠️ 버팀보 관통 벽체 분할타설로 인해 총 {activeSchedule.blockOutJointCount}개소 박스아웃 및 후속 무수축 그라우트 2차 타설 작업 발생
                    </span>
                  )}
                </p>
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-200 text-slate-500 font-bold bg-blue-50/40">
                      <th className="py-2.5 px-3">세부 작업 공종</th>
                      <th className="py-2.5 px-3 text-center">소요 일수</th>
                      <th className="py-2.5 px-3">📐 구체적 산출 수식 (Formula)</th>
                      <th className="py-2.5 px-3">현장 시공 특성 및 표준시방서 근거</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-xs">
                    {activeSchedule.phases.structure.subTasks.map((t, idx) => (
                      <tr key={idx} className="hover:bg-blue-50/20">
                        <td className="py-2.5 px-3 font-sans font-bold text-slate-800">{t.name}</td>
                        <td className="py-2.5 px-3 text-center font-mono font-bold text-blue-700 bg-blue-50/40">{t.days}일</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-indigo-800 bg-indigo-50/30">
                          {t.formula || `${t.days}일`}
                        </td>
                        <td className="py-2.5 px-3 font-sans text-slate-600 space-y-0.5">
                          <div>{t.note}</div>
                          {t.standardBasis && (
                            <div className="text-[11px] text-slate-500 font-mono">
                              ↳ <span className="underline decoration-slate-300">{t.standardBasis}</span>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Phase 4: 가시설 해체, 중간말뚝 인발 및 되메우기 */}
            <div className="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-xs">
              <div className="bg-emerald-50 px-4 py-2.5 border-b border-emerald-200 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                  <strong className="text-xs text-emerald-950 font-bold">
                    {activeSchedule.phases.dismantle.name}
                  </strong>
                </div>
                <span className="text-xs font-mono font-bold text-emerald-900 bg-emerald-200/60 px-2 py-0.5 rounded">
                  소계: {activeSchedule.phases.dismantle.durationDays}일
                </span>
              </div>
              <div className="p-4 space-y-3 text-xs">
                <p className="text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200 leading-relaxed">
                  <strong>공학적 산정 특성:</strong> {activeSchedule.phases.dismantle.description}
                </p>
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-200 text-slate-500 font-bold bg-emerald-50/40">
                      <th className="py-2.5 px-3">세부 작업 공종</th>
                      <th className="py-2.5 px-3 text-center">소요 일수</th>
                      <th className="py-2.5 px-3">📐 구체적 산출 수식 (Formula)</th>
                      <th className="py-2.5 px-3">현장 시공 특성 및 표준품셈 근거</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-xs">
                    {activeSchedule.phases.dismantle.subTasks.map((t, idx) => (
                      <tr key={idx} className="hover:bg-emerald-50/20">
                        <td className="py-2.5 px-3 font-sans font-bold text-slate-800">{t.name}</td>
                        <td className="py-2.5 px-3 text-center font-mono font-bold text-blue-700 bg-blue-50/40">{t.days}일</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-indigo-800 bg-indigo-50/30">
                          {t.formula || `${t.days}일`}
                        </td>
                        <td className="py-2.5 px-3 font-sans text-slate-600 space-y-0.5">
                          <div>{t.note}</div>
                          {t.standardBasis && (
                            <div className="text-[11px] text-slate-500 font-mono">
                              ↳ <span className="underline decoration-slate-300">{t.standardBasis}</span>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* 🌟 3. 공학적 핵심 산출 수식 및 시공 간섭 계수 안내 */}
          <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-3 text-xs">
            <h4 className="font-bold text-slate-900 flex items-center gap-2">
              <Info className="w-4 h-4 text-blue-600" />
              <span>공사기간(공기) 정밀 산출 공식 및 실무 계수 기준</span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px] leading-relaxed text-slate-600">
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <strong className="text-slate-800 block mb-1">1. 토공 굴착 및 수직양중 능력</strong>
                <ul className="list-disc list-inside space-y-0.5">
                  <li><strong>무지보 개방 굴착 (All-Anchor)</strong>: Clamshell 0.8㎥ x 2개소 = <strong>650 ㎥/일</strong></li>
                  <li><strong>버팀보 간섭 굴착 (All-Strut)</strong>: 선회/양중 간섭 감쇄 = <strong>450 ㎥/일</strong> (31% 감쇄)</li>
                  <li><strong>앵커 정착장 양생 대기</strong>: 단당 조강그라우트 5일 압축강도 발현 후 다음 단 굴착</li>
                </ul>
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <strong className="text-slate-800 block mb-1">2. 지하 RC 골조 축조 사이클 및 외벽 분할타설</strong>
                <ul className="list-disc list-inside space-y-0.5">
                  <li><strong>무지보 일체 타설 (All-Anchor)</strong>: 대형 갱폼으로 바닥 슬래브 + 지하외벽 1회 일체타설 (누수 취약 조인트 0개소)</li>
                  <li><strong>버팀보 관통 외벽 2-Lift 분할타설 (All-Strut)</strong>: 버팀보 하단 1차 외벽타설 → 14MPa 강도발현 후 버팀보 해체 → 상단 2차 수직 분할타설 & 박스아웃 무수축 그라우트 채움</li>
                  <li><strong>철근 배근 능률비</strong>: 무지보 100% 대비 버팀보 파이프 꿰기 배근 시 <strong>65% 수준</strong>으로 저하</li>
                  <li><strong>슬래브 분할타설</strong>: 가시설 총 연장에 따라 층당 2~3개 구획(Zone) 릴레이 시공</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* 모달 하단 닫기 바 */}
        <div className="bg-slate-100 px-6 py-3 border-t border-slate-200 flex justify-end shrink-0">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs transition-all shadow-xs"
          >
            확인 및 닫기
          </button>
        </div>
      </div>
    </div>
  );
};
