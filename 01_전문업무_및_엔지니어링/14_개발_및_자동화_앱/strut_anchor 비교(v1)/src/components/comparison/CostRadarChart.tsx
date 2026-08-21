import React from 'react';
import { AlternativeSpec } from '../../types';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from 'recharts';
import { DollarSign, PieChart, ShieldCheck, CheckCircle2, Sparkles } from 'lucide-react';

interface CostRadarChartProps {
  alternatives: AlternativeSpec[];
  selectedAlt: AlternativeSpec;
  onSelectAlt?: (altId: number) => void;
}

export const CostRadarChart: React.FC<CostRadarChartProps> = ({
  alternatives,
  selectedAlt,
  onSelectAlt
}) => {
  const radarData = [
    { subject: '구조안전성', fullMark: 100 },
    { subject: '직접경제성', fullMark: 100 },
    { subject: '작업공간확보', fullMark: 100 },
    { subject: '경계선/민원안전', fullMark: 100 },
    { subject: '시공성/공기', fullMark: 100 },
  ].map((item) => {
    const res: any = { subject: item.subject };
    alternatives.forEach((alt) => {
      let val = 80;
      if (item.subject === '구조안전성') val = Math.max(50, 100 - (alt.pileStressRatio - 0.5) * 50);
      else if (item.subject === '직접경제성') {
        const minCost = Math.min(...alternatives.map(a => a.totalCostWon));
        val = 70 + ((minCost / alt.totalCostWon) * 30);
      } else if (item.subject === '작업공간확보') val = alt.workSpaceScore;
      else if (item.subject === '경계선/민원안전') val = alt.boundaryRiskScore;
      else if (item.subject === '시공성/공기') val = alt.constructabilityScore;
      res[`alt_${alt.id}`] = Math.round(val);
    });
    return res;
  });

  const costBarData = alternatives.map((alt) => ({
    id: alt.id,
    name: `대안 ${alt.id}`,
    fullName: alt.name,
    공사비: Number((alt.totalCostWon / 1e6).toFixed(1)),
    m당단가: Math.round(alt.costPerM / 1e4),
    isSelected: alt.id === selectedAlt.id,
  }));

  const radarColors = ['#d97706', '#2563eb', '#059669', '#7c3aed'];

  return (
    <div className="space-y-4">
      {/* 4대안 빠른 전환 탭 바 */}
      <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-wrap items-center justify-between gap-3 shadow-xs">
        <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
          <DollarSign className="w-4 h-4 text-blue-600" />
          비교 대상 대안 선택 (클릭 시 물량 및 내역서 즉시 연동):
        </span>
        <div className="flex flex-wrap items-center gap-2">
          {alternatives.map((alt) => {
            const isSelected = alt.id === selectedAlt.id;
            return (
              <button
                key={alt.id}
                onClick={() => onSelectAlt && onSelectAlt(alt.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  isSelected
                    ? 'bg-blue-600 text-white shadow-md ring-2 ring-blue-300'
                    : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                }`}
              >
                {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-blue-200" />}
                <span>대안 {alt.id}: {alt.name.split('(')[0]}</span>
                <span className="font-mono text-[10px] opacity-90 font-bold">
                  ({(alt.totalCostWon / 1e6).toFixed(1)}백만)
                </span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* 1. 레이더 차트 */}
        <div className="eng-panel">
          <div className="eng-panel-header">
            <div className="flex items-center gap-2">
              <PieChart className="w-4 h-4 text-blue-600" />
              <div>
                <h3 className="text-xs font-bold text-slate-800">4대 공법 종합 역량 다차원 평가 (Multi-Criteria Radar)</h3>
                <p className="text-[11px] text-slate-500">안전성, 경제성, 작업성, 민원안전성 다차원 비교</p>
              </div>
            </div>
          </div>

          <div className="p-4 h-64 w-full bg-white">
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

        {/* 2. 총 공사비 바 차트 (바 클릭 시 대안 전환) */}
        <div className="eng-panel">
          <div className="eng-panel-header">
            <div className="flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-emerald-600" />
              <div>
                <h3 className="text-xs font-bold text-slate-800">대안별 직접공사비 비교 (클릭하여 대안 선택)</h3>
                <p className="text-[11px] text-slate-500">가시설 총 연장 {selectedAlt.wallLengthPerimeter}m 기준 물량 산출 (백만원)</p>
              </div>
            </div>
            <span className="text-[11px] text-blue-600 font-bold bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              현재 선택: 대안 {selectedAlt.id}
            </span>
          </div>

          <div className="p-4 h-64 w-full bg-white">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={costBarData}
                margin={{ top: 20, right: 20, left: 10, bottom: 5 }}
                onClick={(e: any) => {
                  if (e && e.activePayload && e.activePayload.length > 0) {
                    const clickedAltId = e.activePayload[0].payload.id;
                    if (clickedAltId && onSelectAlt) {
                      onSelectAlt(clickedAltId);
                    }
                  }
                }}
              >
                <XAxis dataKey="name" stroke="#64748b" tick={{ fill: '#334155', fontSize: 11, fontWeight: 'bold' }} />
                <YAxis stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} unit=" 백만" />
                <Tooltip
                  formatter={(value: any, name: any, props: any) => [
                    `${value} 백만원 (${props.payload.fullName})`,
                    '총 직접공사비'
                  ]}
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '6px', fontSize: '11px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                />
                <Bar dataKey="공사비" radius={[4, 4, 0, 0]} className="cursor-pointer">
                  {costBarData.map((entry) => (
                    <Cell
                      key={`cell-${entry.id}`}
                      fill={entry.isSelected ? '#2563eb' : '#94a3b8'}
                      stroke={entry.isSelected ? '#1d4ed8' : '#64748b'}
                      strokeWidth={entry.isSelected ? 2 : 1}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 3. 선택 대안의 공사비 상세 내역표 (실시간 연동) */}
      <div className="eng-panel">
        <div className="eng-panel-header">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <div>
              <h3 className="text-xs font-bold text-slate-800 flex items-center gap-2">
                <span>선택 대안 상세 물량 및 내역서</span>
                <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 font-mono text-[11px] font-bold">
                  [대안 {selectedAlt.id}: {selectedAlt.name}]
                </span>
              </h3>
              <p className="text-[11px] text-slate-500">표준품셈 및 실적공사비 기반 직접공사비 세부 산출</p>
            </div>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-500">m당 시공단가: </span>
            <span className="text-xs font-bold text-blue-700 font-mono">
              {(selectedAlt.costPerM / 1e4).toLocaleString()} 만원/m
            </span>
          </div>
        </div>

        <div className="p-3 overflow-x-auto">
          <table className="w-full text-xs text-left border-collapse eng-table">
            <thead>
              <tr>
                <th className="py-2 px-3">공종 및 자재 항목</th>
                <th className="py-2 px-3 text-right">수량</th>
                <th className="py-2 px-3 text-center">단위</th>
                <th className="py-2 px-3 text-right">단가 (원)</th>
                <th className="py-2 px-3 text-right">금액 (원)</th>
                <th className="py-2 px-3 text-right">비중 (%)</th>
              </tr>
            </thead>
            <tbody>
              {selectedAlt.costBreakdown.map((item, idx) => {
                const ratio = ((item.totalPrice / selectedAlt.totalCostWon) * 100).toFixed(1);
                return (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="py-2 px-3 font-medium text-slate-800">{item.name}</td>
                    <td className="py-2 px-3 text-right font-mono">{item.quantity.toLocaleString()}</td>
                    <td className="py-2 px-3 text-center text-slate-500">{item.unit}</td>
                    <td className="py-2 px-3 text-right font-mono">{item.unitPrice.toLocaleString()}</td>
                    <td className="py-2 px-3 text-right font-mono font-bold text-slate-900">
                      {item.totalPrice.toLocaleString()}
                    </td>
                    <td className="py-2 px-3 text-right font-mono text-slate-500">{ratio}%</td>
                  </tr>
                );
              })}
              <tr className="bg-slate-100/80 font-bold border-t-2 border-slate-300">
                <td className="py-2.5 px-3 text-center" colSpan={4}>
                  합 계 (직접공사비 총액)
                </td>
                <td className="py-2.5 px-3 text-right font-mono text-blue-900 text-sm">
                  {selectedAlt.totalCostWon.toLocaleString()} 원
                </td>
                <td className="py-2.5 px-3 text-right font-mono text-blue-900">100.0%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
