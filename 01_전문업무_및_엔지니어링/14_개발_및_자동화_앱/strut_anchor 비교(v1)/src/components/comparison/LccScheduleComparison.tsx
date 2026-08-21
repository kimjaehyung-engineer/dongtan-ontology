import React, { useState } from 'react';
import { AlternativeSpec, ProjectInputs } from '../../types';
import { LccCostEngine, LccAnalysisResult } from '../../engine/lccCostEngine';
import {
  Clock,
  DollarSign,
  Award,
  Sparkles,
  Layers,
  ChevronRight,
  TrendingDown,
  Info,
  Calendar,
  Hammer,
  ShieldCheck,
  CheckCircle2,
  Users
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Cell
} from 'recharts';

interface LccScheduleComparisonProps {
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAltId: number;
  onSelectAlt?: (altId: number) => void;
}

export const LccScheduleComparison: React.FC<LccScheduleComparisonProps> = ({
  inputs,
  alternatives,
  selectedAltId,
  onSelectAlt
}) => {
  const [monthlyIndirect, setMonthlyIndirect] = useState<number>(45000000); // 4,500만원
  const [jointUnitCost, setJointUnitCost] = useState<number>(800000); // 80만원
  const [numCrews, setNumCrews] = useState<number>(1); // 작업팀 수 (기본 1팀)

  const lccResult: LccAnalysisResult = LccCostEngine.calculateLcc(
    inputs,
    alternatives,
    monthlyIndirect,
    jointUnitCost,
    numCrews
  );

  const bestAlt = lccResult.lccBreakdowns.find(b => b.isLccRecommended) || lccResult.lccBreakdowns[0];

  // 1. Gantt 공정 데이터 (수평 누적 바차트)
  const ganttChartData = lccResult.scheduleResults.map((sch) => {
    return {
      altId: sch.altId,
      name: `대안 ${sch.altId}`,
      fullName: sch.altName,
      '토공 & 앵커양생': sch.phases.earthwork.durationDays,
      'RC 본구조물 축조': sch.phases.structure.durationDays,
      '가시설 해체': sch.phases.dismantle.durationDays,
      totalDays: sch.totalDurationDays,
      savedDays: sch.savedDaysComparedToBaseline,
      isSelected: sch.altId === selectedAltId
    };
  });

  // 2. LCC 총비용 데이터 (누적 바차트)
  const lccCostChartData = lccResult.lccBreakdowns.map((b) => {
    return {
      altId: b.altId,
      name: `대안 ${b.altId}`,
      fullName: b.altName,
      직접공사비: Number((b.directCostWon / 1e8).toFixed(2)),
      현장운영간접비: Number((b.timeDependentIndirectCostWon / 1e8).toFixed(2)),
      조인트방수비: Number((b.jointRemediationCostWon / 1e8).toFixed(2)),
      totalLcc: Number((b.totalLccWon / 1e8).toFixed(2)),
      rank: b.rank,
      isSelected: b.altId === selectedAltId
    };
  });

  return (
    <div className="space-y-4">
      {/* 🌟 상단 LCC 종합 경제성 최적 추천 배너 */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-950 text-white rounded-xl p-4 shadow-md border border-indigo-500/30 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 text-slate-950 shadow-lg">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono font-black uppercase px-2 py-0.5 rounded bg-amber-400/20 text-amber-300 border border-amber-400/40">
                LCC 생애주기 총공사비 최적화 분석
              </span>
              <span className="text-xs text-slate-300 font-mono">
                [토공 2개 반출구 수직양중 + 지하 {lccResult.scheduleResults[0]?.numStories}층 단일작업반 기준]
              </span>
            </div>
            <h2 className="text-sm font-bold text-white mt-1">
              공기 단축 간접비 절감 반영 종합 LCC 1순위: <span className="text-amber-300">{bestAlt.altName}</span>
            </h2>
            <p className="text-xs text-slate-300/90 mt-0.5">
              직접공사비(가설+해체)에 공기 연동 현장운영비(월 {(monthlyIndirect / 1e4).toLocaleString()}만원) 및 관통부 조인트 방수비를 종합 합산한 결과입니다.
            </p>
          </div>
        </div>

        {/* 간이 시뮬레이션 툴바 (월 현장관리비 & 작업팀 수) */}
        <div className="flex items-center gap-3 bg-slate-800/80 p-2 rounded-lg border border-slate-700 text-xs">
          <div className="flex items-center gap-1.5 font-mono">
            <Users className="w-3.5 h-3.5 text-indigo-400" />
            <span className="text-slate-400 text-[11px]">작업팀 수:</span>
            <div className="flex rounded border border-slate-600 overflow-hidden">
              <button
                onClick={() => setNumCrews(1)}
                className={`px-2 py-0.5 text-[11px] font-bold ${numCrews === 1 ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
              >
                1팀 (표준)
              </button>
              <button
                onClick={() => setNumCrews(2)}
                className={`px-2 py-0.5 text-[11px] font-bold ${numCrews === 2 ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
              >
                2팀 (증원)
              </button>
            </div>
          </div>

          <div className="h-4 w-px bg-slate-600"></div>

          <div className="flex items-center gap-1.5 font-mono">
            <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-slate-400 text-[11px]">월 현장간접비:</span>
            <select
              value={monthlyIndirect}
              onChange={(e) => setMonthlyIndirect(Number(e.target.value))}
              className="bg-slate-900 border border-slate-600 rounded px-1.5 py-0.5 text-[11px] text-emerald-300 font-bold focus:outline-none"
            >
              <option value={35000000}>3,500만원/월</option>
              <option value={45000000}>4,500만원/월 (표준)</option>
              <option value={55000000}>5,500만원/월</option>
              <option value={65000000}>6,500만원/월</option>
            </select>
          </div>
        </div>
      </div>

      {/* 2열 메인 차트: [1. 공정 일정 Gantt 타임라인] & [2. LCC 종합비용 누적 바차트] */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* 1. 공정 일정 타임라인 (Gantt 누적 바차트) */}
        <div className="eng-panel">
          <div className="eng-panel-header flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-blue-600" />
              <div>
                <h3 className="text-xs font-bold text-slate-800">4대안 공정 단계별 소요 공기 (Gantt Timeline)</h3>
                <p className="text-[11px] text-slate-500">토공 굴착(양생대기) + 지하 RC 본구조물 축조 + 가시설 해체</p>
              </div>
            </div>
            <span className="text-[11px] font-mono text-blue-700 font-bold bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              단위: 일수 (Day)
            </span>
          </div>

          <div className="p-4 h-72 w-full bg-white">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={ganttChartData}
                layout="vertical"
                margin={{ top: 10, right: 30, left: 10, bottom: 5 }}
                onClick={(e: any) => {
                  if (e && e.activePayload && e.activePayload.length > 0) {
                    const clickedId = e.activePayload[0].payload.altId;
                    if (clickedId && onSelectAlt) onSelectAlt(clickedId);
                  }
                }}
              >
                <XAxis type="number" unit="일" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis type="category" dataKey="name" stroke="#64748b" tick={{ fill: '#334155', fontSize: 11, fontWeight: 'bold' }} />
                <Tooltip
                  formatter={(value: any, name: any) => [`${value}일`, name]}
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '6px', fontSize: '11px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '6px' }} />
                <Bar dataKey="토공 & 앵커양생" stackId="a" fill="#3b82f6" radius={[0, 0, 0, 0]} />
                <Bar dataKey="RC 본구조물 축조" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
                <Bar dataKey="가시설 해체" stackId="a" fill="#f59e0b" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 2. LCC 총비용 누적 바차트 */}
        <div className="eng-panel">
          <div className="eng-panel-header flex items-center justify-between">
            <div className="flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-emerald-600" />
              <div>
                <h3 className="text-xs font-bold text-slate-800">LCC 총생애주기비용 (직접비 + 공기간접비 + 조인트비)</h3>
                <p className="text-[11px] text-slate-500">공기 단축에 따른 순화폐가치(Net Monetary Value) 종합 비교</p>
              </div>
            </div>
            <span className="text-[11px] font-mono text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              단위: 억원 (100M KRW)
            </span>
          </div>

          <div className="p-4 h-72 w-full bg-white">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={lccCostChartData}
                margin={{ top: 10, right: 20, left: 10, bottom: 5 }}
                onClick={(e: any) => {
                  if (e && e.activePayload && e.activePayload.length > 0) {
                    const clickedId = e.activePayload[0].payload.altId;
                    if (clickedId && onSelectAlt) onSelectAlt(clickedId);
                  }
                }}
              >
                <XAxis dataKey="name" stroke="#64748b" tick={{ fill: '#334155', fontSize: 11, fontWeight: 'bold' }} />
                <YAxis unit="억" stroke="#64748b" tick={{ fontSize: 10 }} />
                <Tooltip
                  formatter={(value: any, name: any) => [`${value} 억원`, name]}
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '6px', fontSize: '11px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '6px' }} />
                <Bar dataKey="직접공사비" stackId="cost" fill="#2563eb" radius={[0, 0, 0, 0]} />
                <Bar dataKey="현장운영간접비" stackId="cost" fill="#f97316" radius={[0, 0, 0, 0]} />
                <Bar dataKey="조인트방수비" stackId="cost" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 3. 깔끔한 4줄 종합 비교 요약 테이블 */}
      <div className="eng-panel">
        <div className="eng-panel-header">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <div>
              <h3 className="text-xs font-bold text-slate-800">4대안 공기 및 LCC 총공사비 정량 비교 매트릭스</h3>
              <p className="text-[11px] text-slate-500">공정별 일수, 분할타설 횟수, 직접공사비, 공기간접비 및 종합 순위</p>
            </div>
          </div>
        </div>

        <div className="p-3 overflow-x-auto">
          <table className="w-full text-xs text-left border-collapse eng-table">
            <thead>
              <tr>
                <th className="py-2.5 px-3">대안 구분 및 공법명</th>
                <th className="py-2.5 px-3 text-center">토공+양생</th>
                <th className="py-2.5 px-3 text-center">구조물 축조 (분할타설)</th>
                <th className="py-2.5 px-3 text-center">가시설 해체</th>
                <th className="py-2.5 px-3 text-center">총 공기 (개월)</th>
                <th className="py-2.5 px-3 text-right">직접공사비(가설+해체)</th>
                <th className="py-2.5 px-3 text-right">현장관리 간접비</th>
                <th className="py-2.5 px-3 text-right">조인트 방수비</th>
                <th className="py-2.5 px-3 text-right font-black">LCC 총비용</th>
                <th className="py-2.5 px-3 text-center">종합 순위</th>
              </tr>
            </thead>
            <tbody>
              {lccResult.lccBreakdowns.map((b) => {
                const sch = lccResult.scheduleResults.find(s => s.altId === b.altId);
                const isSelected = b.altId === selectedAltId;
                const isBest = b.isLccRecommended;

                return (
                  <tr
                    key={b.altId}
                    onClick={() => onSelectAlt && onSelectAlt(b.altId)}
                    className={`cursor-pointer transition-all ${
                      isSelected
                        ? 'bg-blue-50/80 font-semibold'
                        : isBest
                        ? 'bg-amber-50/40 hover:bg-amber-50/70'
                        : 'hover:bg-slate-50'
                    }`}
                  >
                    <td className="py-2.5 px-3 font-bold text-slate-900 flex items-center gap-1.5">
                      <span className="text-blue-700 font-mono">대안 {b.altId}</span>
                      <span>: {b.altName}</span>
                      {isBest && (
                        <span className="px-1.5 py-0.2 rounded text-[10px] bg-amber-500 text-white font-bold">
                          LCC 1위
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-center font-mono text-slate-700">
                      {sch?.phases.earthwork.durationDays}일
                    </td>
                    <td className="py-2.5 px-3 text-center font-mono text-slate-700">
                      {sch?.phases.structure.durationDays}일
                      <span className="text-[10px] text-slate-400 block font-sans">
                        {sch?.blockOutJointCount === 0 ? '(일체타설)' : `(${sch?.blockOutJointCount}개소 분할)`}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-center font-mono text-slate-700">
                      {sch?.phases.dismantle.durationDays}일
                    </td>
                    <td className="py-2.5 px-3 text-center font-mono font-bold text-blue-900">
                      {b.durationDays}일 ({b.durationMonths}개월)
                      {sch && sch.savedDaysComparedToBaseline > 0 && (
                        <span className="text-[10px] text-emerald-600 block">
                          (▼{sch.savedDaysComparedToBaseline}일 단축)
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-slate-900">
                      {(b.directCostWon / 1e6).toFixed(1)} 백만원
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-orange-800">
                      {(b.timeDependentIndirectCostWon / 1e6).toFixed(1)} 백만원
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-rose-800">
                      {(b.jointRemediationCostWon / 1e6).toFixed(1)} 백만원
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-black text-sm text-indigo-900">
                      {(b.totalLccWon / 1e6).toFixed(1)} 백만원
                    </td>
                    <td className="py-2.5 px-3 text-center">
                      <span className={`px-2 py-0.5 rounded text-xs font-bold font-mono ${
                        b.rank === 1 ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-slate-100 text-slate-600'
                      }`}>
                        {b.rank}위
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
