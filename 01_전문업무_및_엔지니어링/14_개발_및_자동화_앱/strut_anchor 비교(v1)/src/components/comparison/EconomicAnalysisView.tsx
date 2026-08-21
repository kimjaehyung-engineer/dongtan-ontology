import React, { useState } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { LccCostEngine, LccAnalysisResult } from '../../engine/lccCostEngine';
import { DetailedCostEngine, DetailedCostResult } from '../../engine/detailedCostEngine';
import {
  Award,
  Calendar,
  DollarSign,
  TrendingDown,
  Clock,
  Download,
  Users,
  ShieldCheck,
  CheckCircle2,
  FileSpreadsheet,
  PieChart,
  BarChart2,
  Info,
  ChevronRight,
  Layers,
  Sparkles
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

interface EconomicAnalysisViewProps {
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAltId: number;
  onSelectAlt: (altId: number) => void;
  onOpenScheduleBasis?: () => void;
}

export const EconomicAnalysisView: React.FC<EconomicAnalysisViewProps> = ({
  inputs,
  alternatives,
  selectedAltId,
  onSelectAlt,
  onOpenScheduleBasis
}) => {
  // 서브탭 상태
  const [activeSubTab, setActiveSubTab] = useState<'LCC_SCHEDULE' | 'DETAILED_QTO' | 'RADAR_EVAL'>('LCC_SCHEDULE');
  
  // 시뮬레이션 파라미터
  const [monthlyIndirect, setMonthlyIndirect] = useState<number>(45000000); // 월 4,500만원
  const [jointUnitCost, setJointUnitCost] = useState<number>(800000); // 조인트 개소당 80만원
  const [numCrews, setNumCrews] = useState<number>(1); // 작업팀 수
  const [rentalMonths, setRentalMonths] = useState<number>(6); // 강재 손료 임대기간

  // LCC 및 공정 분석 계산
  const lccResult: LccAnalysisResult = LccCostEngine.calculateLcc(
    inputs,
    alternatives,
    monthlyIndirect,
    jointUnitCost,
    numCrews
  );

  const selectedAlt = alternatives.find(a => a.id === selectedAltId) || alternatives[0];
  const bestLccAlt = lccResult.lccBreakdowns.find(b => b.isLccRecommended) || lccResult.lccBreakdowns[0];

  // 상세 적산 내역 계산 (선택된 대안)
  const detailedCostRes: DetailedCostResult = DetailedCostEngine.calculateDetailedCost(
    selectedAlt,
    inputs,
    rentalMonths
  );

  // 1. Gantt 공정 차트 데이터
  const ganttChartData = lccResult.scheduleResults.map((sch) => ({
    altId: sch.altId,
    name: `대안 ${sch.altId}`,
    fullName: sch.altName,
    '토공 & 앵커양생': sch.phases.earthwork.durationDays,
    'RC 본구조물 축조': sch.phases.structure.durationDays,
    '가시설 해체': sch.phases.dismantle.durationDays,
    totalDays: sch.totalDurationDays,
    savedDays: sch.savedDaysComparedToBaseline,
    isSelected: sch.altId === selectedAltId
  }));

  // 2. LCC 총비용 누적 차트 데이터
  const lccCostChartData = lccResult.lccBreakdowns.map((b) => ({
    altId: b.altId,
    name: `대안 ${b.altId}`,
    fullName: b.altName,
    직접공사비: Number((b.directCostWon / 1e8).toFixed(2)),
    현장운영간접비: Number((b.timeDependentIndirectCostWon / 1e8).toFixed(2)),
    조인트방수비: Number((b.jointRemediationCostWon / 1e8).toFixed(2)),
    totalLcc: Number((b.totalLccWon / 1e8).toFixed(2)),
    rank: b.rank,
    isSelected: b.altId === selectedAltId
  }));

  // 3. 다차원 레이더 평가 데이터
  const radarData = [
    {
      subject: '구조 안전성',
      ...alternatives.reduce((acc, alt) => {
        acc[`alt_${alt.id}`] = Math.max(40, Math.min(100, Math.round(100 - (alt.pileStressRatio - 0.6) * 60)));
        return acc;
      }, {} as Record<string, number>)
    },
    {
      subject: '직접 경제성',
      ...alternatives.reduce((acc, alt) => {
        const minCost = Math.min(...alternatives.map(a => a.totalCostWon));
        acc[`alt_${alt.id}`] = Math.round(70 + ((minCost / alt.totalCostWon) * 30));
        return acc;
      }, {} as Record<string, number>)
    },
    {
      subject: '내부 작업성',
      ...alternatives.reduce((acc, alt) => {
        acc[`alt_${alt.id}`] = alt.workSpaceScore;
        return acc;
      }, {} as Record<string, number>)
    },
    {
      subject: '민원/경계 안전',
      ...alternatives.reduce((acc, alt) => {
        acc[`alt_${alt.id}`] = alt.boundaryRiskScore;
        return acc;
      }, {} as Record<string, number>)
    },
    {
      subject: '공기 단축성',
      ...alternatives.reduce((acc, alt) => {
        const minDays = Math.min(...alternatives.map(a => a.periodDays));
        acc[`alt_${alt.id}`] = Math.round(70 + ((minDays / alt.periodDays) * 30));
        return acc;
      }, {} as Record<string, number>)
    }
  ];

  const radarColors = ['#f59e0b', '#3b82f6', '#10b981', '#6366f1'];

  // CSV 내보내기 핸들러
  const handleDownloadCSV = () => {
    let csv = '\uFEFF공종명,규격,단위,수량,수량산출수식,도급단가(원),실행단가(원),도급금액(원),실행금액(원),절감액(원),단가산출근거(표준품셈)\n';
    detailedCostRes.items.forEach(it => {
      csv += `"${it.name}","${it.spec}","${it.unit}",${it.quantity},"${it.formula}",${it.contractUnitCost},${it.executionUnitCost},${it.contractAmount},${it.executionAmount},${it.contractAmount - it.executionAmount},"${it.costBasis}"\n`;
    });
    csv += `\n총 도급금액,,,${detailedCostRes.totalContractCost},,총 실행금액,,,${detailedCostRes.totalExecutionCost},절감액,${detailedCostRes.costSavings}\n`;

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `가시설_${detailedCostRes.altName}_수량단가산출서.csv`;
    link.click();
  };

  return (
    <div className="space-y-4">
      {/* 🌟 1단: 3대안 핵심 KPI 카드 (한눈 비교 & 원클릭 선택) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
        {alternatives.map((alt) => {
          const isSelected = alt.id === selectedAltId;
          const lccItem = lccResult.lccBreakdowns.find(b => b.altId === alt.id);
          const isBestLcc = lccItem?.isLccRecommended;

          return (
            <div
              key={alt.id}
              onClick={() => onSelectAlt(alt.id)}
              className={`cursor-pointer rounded-xl p-3.5 border transition-all duration-200 relative flex flex-col justify-between ${
                isSelected
                  ? 'bg-gradient-to-br from-blue-50/90 to-indigo-50/70 border-blue-500 shadow-md ring-2 ring-blue-400'
                  : 'bg-white hover:bg-slate-50/90 border-slate-200 shadow-2xs hover:border-slate-300'
              }`}
            >
              {/* 상단 뱃지 & 대안명 */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[11px] font-mono font-bold text-slate-500">
                    대안 {alt.id} • {alt.type}
                  </span>
                  <div className="flex items-center gap-1">
                    {isBestLcc && (
                      <span className="px-1.5 py-0.2 rounded bg-amber-500 text-slate-950 font-black text-[10px] shadow-2xs flex items-center gap-0.5">
                        <Award className="w-3 h-3 fill-current" /> LCC 1위
                      </span>
                    )}
                    {isSelected && (
                      <span className="px-1.5 py-0.2 rounded bg-blue-600 text-white font-bold text-[10px]">
                        선택됨
                      </span>
                    )}
                  </div>
                </div>

                <h4 className="text-xs font-bold text-slate-900 leading-tight mb-2">
                  {alt.name.split('(')[0]}
                </h4>
              </div>

              {/* 핵심 KPI 3열 지표 */}
              <div className="grid grid-cols-3 gap-1 py-2 border-y border-slate-200/70 text-center font-mono">
                <div className="bg-slate-50/80 p-1.5 rounded">
                  <span className="text-[10px] text-slate-400 block">직접공사비</span>
                  <strong className="text-xs text-blue-700 font-extrabold block">
                    {(alt.totalCostWon / 1e8).toFixed(2)}억
                  </strong>
                </div>
                <div className="bg-slate-50/80 p-1.5 rounded">
                  <span className="text-[10px] text-slate-400 block">총 공기</span>
                  <strong className="text-xs text-indigo-700 font-extrabold block">
                    {alt.periodDays}일
                  </strong>
                </div>
                <div className="bg-slate-50/80 p-1.5 rounded">
                  <span className="text-[10px] text-slate-400 block">LCC 총비용</span>
                  <strong className={`text-xs font-extrabold block ${isBestLcc ? 'text-amber-600' : 'text-slate-700'}`}>
                    {((lccItem?.totalLccWon || 0) / 1e8).toFixed(2)}억
                  </strong>
                </div>
              </div>

              {/* 하단 절감액 및 종합 점수 */}
              <div className="flex items-center justify-between pt-2 text-[11px]">
                <span className="text-slate-500 font-sans">
                  {alt.id === 1 ? '기준안' : (
                    <span className="text-emerald-700 font-bold font-mono">
                      절감 {((lccItem?.savedLccWonComparedToBaseline || 0) / 1e6).toFixed(0)}백만
                    </span>
                  )}
                </span>
                <span className="font-bold text-slate-700 font-mono text-[11.5px]">
                  종합 {alt.overallScore}점
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* 🌟 2단: 서브탭 헤더 툴바 (원하는 뷰만 깔끔하게 집중) */}
      <div className="bg-white rounded-xl shadow-xs border border-slate-200 p-2 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setActiveSubTab('LCC_SCHEDULE')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'LCC_SCHEDULE'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200'
            }`}
          >
            <BarChart2 className="w-3.5 h-3.5" />
            <span>📊 1. LCC 생애주기 총비용 & 공정 간섭 분석</span>
          </button>

          <button
            onClick={() => setActiveSubTab('DETAILED_QTO')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'DETAILED_QTO'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200'
            }`}
          >
            <FileSpreadsheet className="w-3.5 h-3.5" />
            <span>📑 2. 공종별 정밀 적산 내역서 (QTO)</span>
          </button>

          <button
            onClick={() => setActiveSubTab('RADAR_EVAL')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeSubTab === 'RADAR_EVAL'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200'
            }`}
          >
            <PieChart className="w-3.5 h-3.5" />
            <span>🎯 3. 다차원 역량 평가 (Radar)</span>
          </button>
        </div>

        {/* 우측 보조 컨트롤 (LCC 탭일 때 시뮬레이터, 적산 탭일 때 CSV 다운로드) */}
        {activeSubTab === 'LCC_SCHEDULE' && (
          <div className="flex items-center gap-3 text-xs">
            <div className="flex items-center gap-1.5 font-mono">
              <Users className="w-3.5 h-3.5 text-indigo-600" />
              <span className="text-slate-500 text-[11px]">작업팀:</span>
              <div className="flex rounded border border-slate-300 overflow-hidden text-[11px]">
                <button
                  onClick={() => setNumCrews(1)}
                  className={`px-2 py-0.5 font-bold ${numCrews === 1 ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700'}`}
                >
                  1팀
                </button>
                <button
                  onClick={() => setNumCrews(2)}
                  className={`px-2 py-0.5 font-bold ${numCrews === 2 ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700'}`}
                >
                  2팀 (증원)
                </button>
              </div>
            </div>

            <div className="h-4 w-px bg-slate-200"></div>

            <div className="flex items-center gap-1.5 font-mono">
              <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
              <span className="text-slate-500 text-[11px]">월 간접비:</span>
              <select
                value={monthlyIndirect}
                onChange={(e) => setMonthlyIndirect(Number(e.target.value))}
                className="bg-slate-50 border border-slate-300 rounded px-1.5 py-0.5 text-[11px] font-bold text-slate-800 focus:outline-none"
              >
                <option value={35000000}>3,500만원/월</option>
                <option value={45000000}>4,500만원/월 (표준)</option>
                <option value={55000000}>5,500만원/월</option>
                <option value={65000000}>6,500만원/월</option>
              </select>
            </div>
          </div>
        )}

        {activeSubTab === 'DETAILED_QTO' && (
          <div className="flex items-center gap-2">
            <button
              onClick={handleDownloadCSV}
              className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-xs transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>적산내역서 CSV 다운로드</span>
            </button>
          </div>
        )}
      </div>

      {/* 🌟 2단 상세 뷰 컨텐츠 영역 */}
      {/* 1. LCC & 공정일정 비교 뷰 */}
      {activeSubTab === 'LCC_SCHEDULE' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* 좌: 공정 일정 타임라인 (Gantt 누적 바차트) */}
            <div className="eng-panel">
              <div className="eng-panel-header flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-indigo-600" />
                  <div>
                    <h3 className="text-xs font-bold text-slate-800">공정 일정 타임라인 (Gantt 차트)</h3>
                    <p className="text-[11px] text-slate-500">토공 2개 반출구 수직양중 및 지하 {lccResult.scheduleResults[0]?.numStories}층 RC 골조 축조 공기</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {onOpenScheduleBasis && (
                    <button
                      onClick={onOpenScheduleBasis}
                      className="flex items-center gap-1 px-2.5 py-1 rounded bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold shadow-xs transition-all"
                      title="대안별 공기 정밀 산출 수식 및 표준품셈 근거서 확인"
                    >
                      <Clock className="w-3 h-3 text-amber-300" />
                      <span>공기 산정 근거서 (품셈)</span>
                    </button>
                  )}
                  <span className="text-[11px] text-indigo-700 font-mono font-bold bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                    단위: 일(Days)
                  </span>
                </div>
              </div>

              <div className="p-4 h-72 w-full bg-white">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={ganttChartData}
                    layout="vertical"
                    margin={{ top: 10, right: 30, left: 20, bottom: 5 }}
                    onClick={(e: any) => {
                      if (e && e.activePayload && e.activePayload.length > 0) {
                        const altId = e.activePayload[0].payload.altId;
                        if (altId) onSelectAlt(altId);
                      }
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                    <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} unit="일" />
                    <YAxis dataKey="name" type="category" stroke="#64748b" tick={{ fontSize: 11, fontWeight: 'bold' }} width={55} />
                    <Tooltip
                      formatter={(val: any, name: any) => [`${val}일`, name]}
                      contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '8px', fontSize: '11px' }}
                    />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '4px' }} />
                    <Bar dataKey="토공 & 앵커양생" stackId="a" fill="#f59e0b" radius={[0, 0, 0, 0]} />
                    <Bar dataKey="RC 본구조물 축조" stackId="a" fill="#3b82f6" radius={[0, 0, 0, 0]} />
                    <Bar dataKey="가시설 해체" stackId="a" fill="#94a3b8" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* 우: LCC 총생애주기비용 누적 바차트 */}
            <div className="eng-panel">
              <div className="eng-panel-header flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-emerald-600" />
                  <div>
                    <h3 className="text-xs font-bold text-slate-800">LCC 총생애주기비용 비교 (클릭 시 대안 선택)</h3>
                    <p className="text-[11px] text-slate-500">직접공사비 + 공기연동 현장운영비 + 분할타설 조인트 방수비</p>
                  </div>
                </div>
                <span className="text-[11px] text-emerald-700 font-mono font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  단위: 억원 (100M KRW)
                </span>
              </div>

              <div className="p-4 h-72 w-full bg-white">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={lccCostChartData}
                    margin={{ top: 10, right: 30, left: 10, bottom: 5 }}
                    onClick={(e: any) => {
                      if (e && e.activePayload && e.activePayload.length > 0) {
                        const altId = e.activePayload[0].payload.altId;
                        if (altId) onSelectAlt(altId);
                      }
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                    <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11, fontWeight: 'bold' }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 10 }} unit="억" />
                    <Tooltip
                      formatter={(val: any, name: any) => [`${val} 억원`, name]}
                      contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '8px', fontSize: '11px' }}
                    />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '4px' }} />
                    <Bar dataKey="직접공사비" stackId="a" fill="#3b82f6" radius={[0, 0, 0, 0]} />
                    <Bar dataKey="현장운영간접비" stackId="a" fill="#f59e0b" radius={[0, 0, 0, 0]} />
                    <Bar dataKey="조인트방수비" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* 4대안 LCC 종합 집계표 */}
          <div className="eng-panel overflow-hidden">
            <div className="eng-panel-header flex items-center justify-between">
              <h3 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-blue-600" />
                4대안 공기·간접비·LCC 총비용 정밀 비교표
              </h3>
              <span className="text-[11px] text-slate-400 font-mono">
                기준안(대안 1) 대비 절감액 산출
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 text-slate-600 border-b border-slate-200 font-bold">
                    <th className="py-2.5 px-3">대안명</th>
                    <th className="py-2.5 px-3 text-center">총 공기</th>
                    <th className="py-2.5 px-3 text-right">① 직접공사비</th>
                    <th className="py-2.5 px-3 text-right">② 현장운영간접비</th>
                    <th className="py-2.5 px-3 text-right">③ 조인트 방수비</th>
                    <th className="py-2.5 px-3 text-right">총 LCC 비용</th>
                    <th className="py-2.5 px-3 text-right">기준안 대비 절감액</th>
                    <th className="py-2.5 px-3 text-center">종합 순위</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {lccResult.lccBreakdowns.map((b) => {
                    const isSelected = b.altId === selectedAltId;
                    return (
                      <tr
                        key={b.altId}
                        onClick={() => onSelectAlt(b.altId)}
                        className={`cursor-pointer transition-colors ${
                          isSelected
                            ? 'bg-blue-50/80 font-bold'
                            : b.isLccRecommended
                            ? 'bg-amber-50/60'
                            : 'hover:bg-slate-50'
                        }`}
                      >
                        <td className="py-2 px-3 font-sans flex items-center gap-1.5">
                          {b.isLccRecommended && <Award className="w-3.5 h-3.5 text-amber-500 fill-current" />}
                          <span className={isSelected ? 'text-blue-900 font-bold' : 'text-slate-800'}>
                            대안 {b.altId}: {b.altName}
                          </span>
                        </td>
                        <td className="py-2 px-3 text-center">
                          {b.durationDays}일 <span className="text-slate-400 text-[10px]">({b.durationMonths.toFixed(1)}개월)</span>
                        </td>
                        <td className="py-2 px-3 text-right text-blue-700">
                          {(b.directCostWon / 1e8).toFixed(2)} 억
                        </td>
                        <td className="py-2 px-3 text-right text-amber-700">
                          {(b.timeDependentIndirectCostWon / 1e8).toFixed(2)} 억
                        </td>
                        <td className="py-2 px-3 text-right text-rose-700">
                          {(b.jointRemediationCostWon / 1e6).toFixed(0)} 백만
                        </td>
                        <td className="py-2 px-3 text-right font-bold text-slate-900">
                          {(b.totalLccWon / 1e8).toFixed(2)} 억원
                        </td>
                        <td className="py-2 px-3 text-right font-bold">
                          {b.altId === 1 ? (
                            <span className="text-slate-400">-</span>
                          ) : (
                            <span className="text-emerald-700">
                              -{(b.savedLccWonComparedToBaseline / 1e6).toFixed(0)} 백만원
                            </span>
                          )}
                        </td>
                        <td className="py-2 px-3 text-center font-sans">
                          {b.isLccRecommended ? (
                            <span className="px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 font-extrabold text-[10px] border border-amber-300">
                              ★ 1위 (최적)
                            </span>
                          ) : (
                            <span className="text-slate-500 font-bold">{b.rank}위</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 2. 공종별 정밀 적산 내역서 (QTO) 뷰 */}
      {activeSubTab === 'DETAILED_QTO' && (
        <div className="space-y-3">
          {/* 상단 적산 요약 헤더 */}
          <div className="bg-slate-900 text-white rounded-xl p-4 flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-400/40">
                표준품셈 기반 정밀 적산 내역서 (Single Source of Truth)
              </span>
              <h3 className="text-sm font-bold text-white mt-1">
                대안 {selectedAlt.id}: {detailedCostRes.altName}
              </h3>
              <p className="text-xs text-slate-300 mt-0.5">
                가시설 총 연장 {inputs.totalWallPerimeter}m, 굴착심도 -{inputs.excavationDepth}m, 강재 임대기간 {rentalMonths}개월 기준
              </p>
            </div>

            <div className="flex items-center gap-4 bg-slate-800/90 px-4 py-2 rounded-lg border border-slate-700 font-mono">
              <div>
                <span className="text-[10px] text-slate-400 block">도급 예정액 (원)</span>
                <strong className="text-base text-blue-400 font-extrabold">
                  {detailedCostRes.totalContractCost.toLocaleString()} 원
                </strong>
              </div>
              <div className="h-6 w-px bg-slate-700"></div>
              <div>
                <span className="text-[10px] text-slate-400 block">실행 예정액 (원)</span>
                <strong className="text-base text-emerald-400 font-extrabold">
                  {detailedCostRes.totalExecutionCost.toLocaleString()} 원
                </strong>
              </div>
              <div className="h-6 w-px bg-slate-700"></div>
              <div>
                <span className="text-[10px] text-slate-400 block">예상 실행 절감액</span>
                <strong className="text-base text-amber-300 font-extrabold">
                  {detailedCostRes.costSavings.toLocaleString()} 원 ({((detailedCostRes.costSavings / (detailedCostRes.totalContractCost || 1)) * 100).toFixed(1)}%)
                </strong>
              </div>
            </div>
          </div>

          {/* 항목별 상세 수량/단가 테이블 */}
          <div className="eng-panel overflow-hidden">
            <div className="overflow-x-auto max-h-[500px] overflow-y-auto">
              <table className="w-full text-xs text-left border-collapse">
                <thead className="sticky top-0 bg-slate-100 z-10 text-slate-700 border-b border-slate-300 font-bold shadow-xs">
                  <tr>
                    <th className="py-2.5 px-3">공종 및 항목명</th>
                    <th className="py-2.5 px-3">규격 / 사양</th>
                    <th className="py-2.5 px-3 text-center">단위</th>
                    <th className="py-2.5 px-3 text-right">수량</th>
                    <th className="py-2.5 px-3 text-right">도급단가(원)</th>
                    <th className="py-2.5 px-3 text-right">실행단가(원)</th>
                    <th className="py-2.5 px-3 text-right">도급금액(원)</th>
                    <th className="py-2.5 px-3 text-right">실행금액(원)</th>
                    <th className="py-2.5 px-3 text-right">절감액(원)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {detailedCostRes.items.map((it) => (
                    <tr key={it.id} className="hover:bg-slate-50">
                      <td className="py-2 px-3 font-sans font-bold text-slate-900">
                        {it.name}
                      </td>
                      <td className="py-2 px-3 text-slate-600 text-[11px]">
                        {it.spec}
                      </td>
                      <td className="py-2 px-3 text-center text-slate-500 font-sans">
                        {it.unit}
                      </td>
                      <td className="py-2 px-3 text-right text-slate-800 font-bold">
                        {it.quantity.toLocaleString()}
                      </td>
                      <td className="py-2 px-3 text-right text-slate-600">
                        {it.contractUnitCost.toLocaleString()}
                      </td>
                      <td className="py-2 px-3 text-right text-emerald-700">
                        {it.executionUnitCost.toLocaleString()}
                      </td>
                      <td className="py-2 px-3 text-right text-blue-700 font-bold">
                        {it.contractAmount.toLocaleString()}
                      </td>
                      <td className="py-2 px-3 text-right text-emerald-700 font-bold">
                        {it.executionAmount.toLocaleString()}
                      </td>
                      <td className="py-2 px-3 text-right text-amber-700 font-bold">
                        {(it.contractAmount - it.executionAmount).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* 3. 다차원 역량 평가 (Radar) 뷰 */}
      {activeSubTab === 'RADAR_EVAL' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          <div className="lg:col-span-7 eng-panel">
            <div className="eng-panel-header">
              <h3 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                <PieChart className="w-4 h-4 text-blue-600" />
                4대 공법 종합 역량 다차원 평가 (Multi-Criteria Radar)
              </h3>
              <span className="text-[11px] text-slate-400 font-mono">
                안전성 / 경제성 / 작업성 / 민원성 / 공기 5대 축 분석
              </span>
            </div>

            <div className="p-4 h-80 w-full bg-white">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                  <PolarGrid stroke="#e2e8f0" />
                  <PolarAngleAxis dataKey="subject" stroke="#64748b" tick={{ fill: '#334155', fontSize: 11, fontWeight: 'bold' }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 9 }} />
                  {alternatives.map((alt, idx) => (
                    <Radar
                      key={alt.id}
                      name={alt.name}
                      dataKey={`alt_${alt.id}`}
                      stroke={radarColors[idx % radarColors.length]}
                      fill={radarColors[idx % radarColors.length]}
                      fillOpacity={alt.id === selectedAlt.id ? 0.35 : 0.08}
                      strokeWidth={alt.id === selectedAlt.id ? 2.5 : 1.2}
                    />
                  ))}
                  <Tooltip
                    contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '6px', fontSize: '11px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="lg:col-span-5 eng-panel">
            <div className="eng-panel-header">
              <h3 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                대안별 역량 평가 종합 점수표
              </h3>
            </div>

            <div className="p-3.5 space-y-2.5 text-xs">
              {alternatives.map((alt) => {
                const isSelected = alt.id === selectedAltId;
                return (
                  <div
                    key={alt.id}
                    onClick={() => onSelectAlt(alt.id)}
                    className={`p-3 rounded-lg border cursor-pointer transition-all ${
                      isSelected
                        ? 'bg-blue-50 border-blue-400 shadow-xs'
                        : 'bg-white hover:bg-slate-50 border-slate-200'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-bold text-slate-900">
                        대안 {alt.id}: {alt.name.split('(')[0]}
                      </span>
                      <strong className="text-sm text-blue-700 font-mono">
                        {alt.overallScore} 점
                      </strong>
                    </div>

                    <div className="grid grid-cols-3 gap-2 text-[11px] text-slate-600 font-mono pt-1 border-t border-slate-200/60">
                      <div>작업공간: <strong>{alt.workSpaceScore}점</strong></div>
                      <div>민원안전: <strong>{alt.boundaryRiskScore}점</strong></div>
                      <div>시공성: <strong>{alt.constructabilityScore}점</strong></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* 🌟 3단: 의사결정 요약 코멘트 박스 */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-blue-500 text-white">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-white flex items-center gap-2">
              <span>엔지니어링 의사결정 분석 요약 [현재 선택: 대안 {selectedAlt.id} - {selectedAlt.name}]</span>
            </h4>
            <p className="text-[11px] text-blue-200/90 mt-0.5">
              {selectedAlt.id === 1 ? (
                <span>기준 설계안(전단 버팀보 공법)으로 총 공기 <strong>{selectedAlt.periodDays}일</strong>, 직접공사비 <strong>{(selectedAlt.totalCostWon / 1e8).toFixed(2)}억원</strong>이 소요됩니다.</span>
              ) : (
                <span>
                  기준안(대안 1) 대비 공기 <strong>{lccResult.scheduleResults.find(s => s.altId === selectedAlt.id)?.savedDaysComparedToBaseline || 0}일 단축</strong> 및 LCC 생애주기 총비용 약 <strong>{((lccResult.lccBreakdowns.find(b => b.altId === selectedAlt.id)?.savedLccWonComparedToBaseline || 0) / 1e6).toFixed(0)}백만원 절감</strong>이 기대됩니다.
                </span>
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[11px] text-blue-300 font-mono bg-blue-800/60 px-3 py-1 rounded-lg border border-blue-600">
            ★ LCC 1위 추천 공법: {bestLccAlt.altName}
          </span>
        </div>
      </div>
    </div>
  );
};
