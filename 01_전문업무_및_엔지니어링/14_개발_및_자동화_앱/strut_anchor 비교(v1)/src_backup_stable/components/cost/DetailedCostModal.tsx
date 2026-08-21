import React, { useState } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { DetailedCostEngine, DetailedCostResult, QuantityItem } from '../../engine/detailedCostEngine';
import { Calculator, X, FileSpreadsheet, Download, RefreshCw, CheckCircle2, TrendingDown, Layers, DollarSign, Calendar, Sparkles, Sliders, FileText, ChevronRight } from 'lucide-react';

interface DetailedCostModalProps {
  isOpen: boolean;
  onClose: () => void;
  alternatives: AlternativeSpec[];
  currentAltId: number;
  inputs: ProjectInputs;
}

export const DetailedCostModal: React.FC<DetailedCostModalProps> = ({
  isOpen,
  onClose,
  alternatives,
  currentAltId,
  inputs
}) => {
  const [activeTab, setActiveTab] = useState<'SUMMARY' | 'QTO' | 'UNIT_COST' | 'COMPARISON'>('SUMMARY');
  const [selectedAltId, setSelectedAltId] = useState<number>(currentAltId);
  const [rentalMonths, setRentalMonths] = useState<number>(6);
  const [customUnitCosts, setCustomUnitCosts] = useState<Record<string, { contract: number; execution: number }>>({});

  if (!isOpen) return null;

  const currentAlt = alternatives.find(a => a.id === selectedAltId) || alternatives[0];
  const costRes: DetailedCostResult = DetailedCostEngine.calculateDetailedCost(
    currentAlt,
    inputs,
    rentalMonths,
    customUnitCosts
  );

  // 모든 대안의 상세 공사비 산정
  const allAltCostResults = alternatives.map(alt => {
    return DetailedCostEngine.calculateDetailedCost(alt, inputs, rentalMonths, customUnitCosts);
  });

  // 단가 직접 수정 핸들러
  const handleUnitCostChange = (itemId: string, field: 'contract' | 'execution', value: number) => {
    const cur = customUnitCosts[itemId] || {
      contract: costRes.items.find(it => it.id === itemId)?.contractUnitCost || 0,
      execution: costRes.items.find(it => it.id === itemId)?.executionUnitCost || 0,
    };
    cur[field] = value;
    setCustomUnitCosts({ ...customUnitCosts, [itemId]: cur });
  };

  // 실행율 80% 일괄 적용
  const handleApplyBatchExecutionRate = (ratePercent: number) => {
    const updated: Record<string, { contract: number; execution: number }> = {};
    costRes.items.forEach(it => {
      const contract = customUnitCosts[it.id]?.contract || it.contractUnitCost;
      updated[it.id] = {
        contract,
        execution: Math.round(contract * (ratePercent / 100))
      };
    });
    setCustomUnitCosts(updated);
  };

  // 단가 초기화
  const handleResetUnitCosts = () => {
    setCustomUnitCosts({});
  };

  // CSV 다운로드
  const handleDownloadCSV = () => {
    let csv = '\uFEFF공종명,규격,단위,수량,수량산출수식,도급단가(원),실행단가(원),도급금액(원),실행금액(원),절감액(원),단가산출근거(표준품셈)\n';
    costRes.items.forEach(it => {
      csv += `"${it.name}","${it.spec}","${it.unit}",${it.quantity},"${it.formula}",${it.contractUnitCost},${it.executionUnitCost},${it.contractAmount},${it.executionAmount},${it.contractAmount - it.executionAmount},"${it.costBasis}"\n`;
    });
    csv += `\n총 도급금액,,,${costRes.totalContractCost},,총 실행금액,,,${costRes.totalExecutionCost},절감액,${costRes.costSavings}\n`;

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `가시설_${costRes.altName}_수량단가산출서_도급_실행.csv`;
    link.click();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fade-in">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-300 w-full max-w-6xl max-h-[92vh] flex flex-col overflow-hidden">
        {/* 모달 상단 헤더 */}
        <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-blue-600 text-white shadow-sm">
              <Calculator className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-white tracking-tight">
                  가시설 수량산출 근거(QTO) & 도급·실행 공사비 검증 시스템
                </h2>
                <span className="px-2 py-0.5 rounded text-[10px] bg-blue-500/20 text-blue-300 border border-blue-400/30 font-mono font-bold">
                  최신 표준품셈 & 물가정보지 연동
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                투명한 수량산출 공식 검증, 발주처 도급단가(설계단가) 및 시공사 실행단가(원가) 이원화 정밀 관리
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleDownloadCSV}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-sm"
            >
              <Download className="w-3.5 h-3.5" /> 엑셀(CSV) 저장
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* 제어 툴바: 대안 전환, 가설기간 개월수, 탭 네비게이션 */}
        <div className="bg-slate-100 px-6 py-3 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 text-xs">
          {/* 대안 선택 칩 */}
          <div className="flex items-center gap-1.5 overflow-x-auto">
            <span className="font-bold text-slate-700 mr-1 flex items-center gap-1">
              <Layers className="w-3.5 h-3.5 text-blue-600" /> 검토 대안:
            </span>
            {alternatives.map(alt => (
              <button
                key={alt.id}
                onClick={() => setSelectedAltId(alt.id)}
                className={`px-3 py-1 rounded text-xs font-bold transition-all border ${
                  selectedAltId === alt.id
                    ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                    : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                }`}
              >
                {alt.name}
              </button>
            ))}
          </div>

          {/* 가설기간(개월수) 및 실행율 프리셋 */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-white px-2.5 py-1 rounded border border-slate-300 font-mono text-[11px]">
              <Calendar className="w-3.5 h-3.5 text-blue-600" />
              <span className="text-slate-600">강재 손료기간:</span>
              <select
                value={rentalMonths}
                onChange={(e) => setRentalMonths(parseInt(e.target.value, 10))}
                className="bg-transparent font-bold text-blue-700 font-mono focus:outline-none cursor-pointer"
              >
                <option value={3}>3개월 (손료 7.5%)</option>
                <option value={6}>6개월 (손료 15.0%)</option>
                <option value={8}>8개월 (손료 20.0%)</option>
                <option value={12}>12개월 (손료 30.0%)</option>
              </select>
            </div>

            <div className="flex items-center gap-1">
              <span className="text-slate-500 font-medium mr-1">실행율:</span>
              {[75, 80, 85].map(rate => (
                <button
                  key={rate}
                  onClick={() => handleApplyBatchExecutionRate(rate)}
                  className="px-2 py-0.5 rounded bg-white hover:bg-indigo-50 border border-slate-300 text-[11px] font-mono font-bold text-indigo-700"
                >
                  {rate}%
                </button>
              ))}
              <button
                onClick={handleResetUnitCosts}
                className="p-1 rounded bg-white hover:bg-slate-200 border border-slate-300 text-slate-500"
                title="단가 초기화"
              >
                <RefreshCw className="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>

        {/* 탭 네비게이션 */}
        <div className="bg-white px-6 border-b border-slate-200 flex gap-4 text-xs font-bold">
          <button
            onClick={() => setActiveTab('SUMMARY')}
            className={`py-3 border-b-2 transition-all flex items-center gap-1.5 ${
              activeTab === 'SUMMARY'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <DollarSign className="w-4 h-4" /> 1. 도급 vs 실행 종합 집계표
          </button>

          <button
            onClick={() => setActiveTab('QTO')}
            className={`py-3 border-b-2 transition-all flex items-center gap-1.5 ${
              activeTab === 'QTO'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <FileText className="w-4 h-4" /> 2. 수량산출 근거 (QTO Formulas)
          </button>

          <button
            onClick={() => setActiveTab('UNIT_COST')}
            className={`py-3 border-b-2 transition-all flex items-center gap-1.5 ${
              activeTab === 'UNIT_COST'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Sliders className="w-4 h-4" /> 3. 단가산출 근거 & 일위대가 편집
          </button>

          <button
            onClick={() => setActiveTab('COMPARISON')}
            className={`py-3 border-b-2 transition-all flex items-center gap-1.5 ${
              activeTab === 'COMPARISON'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Layers className="w-4 h-4" /> 4. 4대안 공사비·원가절감 비교
          </button>
        </div>

        {/* 탭 본문 영역 */}
        <div className="p-6 overflow-y-auto flex-1 bg-slate-50/50 space-y-4">
          {/* ══════════════════════════════════════════════════════════════════
              탭 1: 종합 공사비 집계표 (도급 vs 실행 비교)
             ══════════════════════════════════════════════════════════════════ */}
          {activeTab === 'SUMMARY' && (
            <div className="space-y-4">
              {/* 상단 핵심 KPI 요약 카드 */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
                  <span className="text-[11px] text-slate-500 font-bold block">도급 예정가격 총액 (설계)</span>
                  <div className="text-xl font-extrabold text-slate-900 font-mono">
                    {(costRes.totalContractCost / 1e6).toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-xs font-normal text-slate-500">백만원</span>
                  </div>
                  <span className="text-[10px] text-slate-400">표준품셈 100% 기준</span>
                </div>

                <div className="bg-white p-4 rounded-xl border border-indigo-200 shadow-xs space-y-1 bg-indigo-50/30">
                  <span className="text-[11px] text-indigo-700 font-bold block">시공 실행예산 총액 (원가)</span>
                  <div className="text-xl font-extrabold text-indigo-700 font-mono">
                    {(costRes.totalExecutionCost / 1e6).toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-xs font-normal text-slate-500">백만원</span>
                  </div>
                  <span className="text-[10px] text-indigo-600 font-semibold">실행율 {costRes.executionRatio}% 달성</span>
                </div>

                <div className="bg-white p-4 rounded-xl border border-emerald-200 shadow-xs space-y-1 bg-emerald-50/30">
                  <span className="text-[11px] text-emerald-700 font-bold block">원가 절감 예상액 (이익)</span>
                  <div className="text-xl font-extrabold text-emerald-700 font-mono flex items-center gap-1">
                    <TrendingDown className="w-5 h-5" />
                    {(costRes.costSavings / 1e6).toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-xs font-normal text-slate-500">백만원</span>
                  </div>
                  <span className="text-[10px] text-emerald-600 font-semibold">절감율 {(100 - costRes.executionRatio).toFixed(1)}% 확보</span>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
                  <span className="text-[11px] text-slate-500 font-bold block">강재 손료 및 가설기간</span>
                  <div className="text-xl font-extrabold text-slate-800 font-mono">
                    {rentalMonths} <span className="text-xs font-normal text-slate-500">개월</span>
                  </div>
                  <span className="text-[10px] text-slate-400">월 2.5% 손료율 (총 {(2.5 * rentalMonths).toFixed(1)}%)</span>
                </div>
              </div>

              {/* 공종별 집계표 */}
              <div className="bg-white rounded-lg border border-slate-200 shadow-xs overflow-hidden">
                <div className="px-4 py-3 bg-slate-100 border-b border-slate-200 flex justify-between items-center">
                  <h4 className="text-xs font-bold text-slate-800">
                    {costRes.altName} — 공종별 수량 및 도급/실행 금액 집계표
                  </h4>
                  <span className="text-[11px] text-slate-500 font-mono">VAT 별도, 부속재 및 가설해체 포함</span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 text-[11px]">
                      <tr>
                        <th className="py-2.5 px-3">공종명 및 세부규격</th>
                        <th className="py-2.5 px-3 text-center">단위</th>
                        <th className="py-2.5 px-3 text-right">수량</th>
                        <th className="py-2.5 px-3 text-right">도급단가</th>
                        <th className="py-2.5 px-3 text-right">도급금액</th>
                        <th className="py-2.5 px-3 text-right">실행단가</th>
                        <th className="py-2.5 px-3 text-right">실행금액</th>
                        <th className="py-2.5 px-3 text-right text-emerald-700">절감액</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                      {(() => {
                        let lastCategory = '';
                        return costRes.items.map(it => {
                          const diff = it.contractAmount - it.executionAmount;
                          const isNewCategory = it.categoryName !== lastCategory;
                          lastCategory = it.categoryName;

                          return (
                            <React.Fragment key={it.id}>
                              {isNewCategory && (
                                <tr className="bg-slate-100/90 font-sans border-y border-slate-200">
                                  <td colSpan={8} className="py-2 px-3 font-bold text-slate-800 text-xs flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-blue-600"></span>
                                    <span>{it.categoryName}</span>
                                  </td>
                                </tr>
                              )}
                              <tr className="hover:bg-blue-50/40 transition-colors">
                                <td className="py-2 px-3 font-sans">
                                  <div className="flex items-center gap-2">
                                    <span className="px-1.5 py-0.5 rounded bg-slate-100 border border-slate-200 text-[10px] font-mono text-slate-600 font-bold">
                                      {it.itemCode}
                                    </span>
                                    <span className="font-bold text-slate-900">{it.name}</span>
                                  </div>
                                  <div className="text-[10px] text-slate-500 pl-1">{it.spec}</div>
                                </td>
                                <td className="py-2 px-3 text-center text-slate-600 font-bold">{it.unit}</td>
                                <td className="py-2 px-3 text-right font-bold text-slate-800">
                                  {it.quantity.toLocaleString(undefined, { maximumFractionDigits: 1 })}
                                </td>
                                <td className="py-2 px-3 text-right text-slate-700">
                                  {it.contractUnitCost.toLocaleString()} 원
                                </td>
                                <td className="py-2 px-3 text-right font-bold text-slate-900">
                                  {(it.contractAmount / 1e6).toFixed(2)} 백만원
                                </td>
                                <td className="py-2 px-3 text-right text-indigo-700 font-bold">
                                  {it.executionUnitCost.toLocaleString()} 원
                                </td>
                                <td className="py-2 px-3 text-right font-bold text-indigo-900">
                                  {(it.executionAmount / 1e6).toFixed(2)} 백만원
                                </td>
                                <td className="py-2 px-3 text-right font-bold text-emerald-700">
                                  {(diff / 1e6).toFixed(2)} 백만원
                                </td>
                              </tr>
                            </React.Fragment>
                          );
                        });
                      })()}
                    </tbody>
                    <tfoot className="bg-slate-100 font-bold text-xs border-t-2 border-slate-300 font-mono">
                      <tr>
                        <td colSpan={4} className="py-3 px-3 text-right font-sans text-slate-800">
                          합계 (Direct Construction Cost Total)
                        </td>
                        <td className="py-3 px-3 text-right text-slate-900 text-sm">
                          {(costRes.totalContractCost / 1e6).toLocaleString(undefined, { maximumFractionDigits: 1 })} 백만원
                        </td>
                        <td></td>
                        <td className="py-3 px-3 text-right text-indigo-900 text-sm">
                          {(costRes.totalExecutionCost / 1e6).toLocaleString(undefined, { maximumFractionDigits: 1 })} 백만원
                        </td>
                        <td className="py-3 px-3 text-right text-emerald-700 text-sm">
                          {(costRes.costSavings / 1e6).toLocaleString(undefined, { maximumFractionDigits: 1 })} 백만원
                        </td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              탭 2: 수량산출 근거 (QTO Formulas & Calculation Details)
             ══════════════════════════════════════════════════════════════════ */}
          {activeTab === 'QTO' && (
            <div className="space-y-3">
              <div className="bg-blue-50 border border-blue-200 p-3 rounded-lg text-xs text-blue-950 flex items-center justify-between">
                <span className="font-semibold">
                  📐 굴착 깊이(H={inputs.excavationDepth}m), 굴착 폭(B={inputs.excavationWidth}m), 가시설 총연장(L={inputs.totalWallPerimeter}m) 및 지보재 간격에 기초한 정밀 산출식
                </span>
                <span className="font-mono text-[11px] text-blue-700 font-bold">KDS 21 30 00 수량산출 기준</span>
              </div>

              <div className="space-y-2.5">
                {costRes.items.map((it, idx) => (
                  <div key={it.id} className="bg-white p-3.5 rounded-lg border border-slate-200 shadow-xs space-y-2">
                    <div className="flex items-center justify-between border-b pb-1.5 border-slate-100">
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5 rounded-full bg-slate-800 text-white text-[11px] flex items-center justify-center font-mono font-bold">
                          {idx + 1}
                        </span>
                        <span className="font-bold text-slate-900 text-xs">{it.name}</span>
                        <span className="text-[11px] text-slate-500 font-mono">[{it.spec}]</span>
                      </div>
                      <div className="font-mono text-xs">
                        산출 수량: <strong className="text-blue-700 text-sm">{it.quantity.toLocaleString()}</strong> {it.unit}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                      <div className="bg-slate-50 p-2.5 rounded border border-slate-200 space-y-1">
                        <span className="text-[10px] text-slate-400 font-bold block">공학적 계산 수식 (Formula)</span>
                        <div className="font-mono font-bold text-indigo-900 text-xs">{it.formula}</div>
                      </div>

                      <div className="bg-slate-50 p-2.5 rounded border border-slate-200 space-y-1">
                        <span className="text-[10px] text-slate-400 font-bold block">산출 세부 근거 및 변수 (Basis Details)</span>
                        <div className="text-slate-700 text-[11px]">{it.formulaDetail}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              탭 3: 단가산출 근거 & 일위대가 직접 편집 (Unit Cost Breakdown)
             ══════════════════════════════════════════════════════════════════ */}
          {activeTab === 'UNIT_COST' && (
            <div className="space-y-3">
              <div className="bg-amber-50 border border-amber-200 p-3 rounded-lg text-xs text-amber-950 flex items-center justify-between">
                <span>
                  📑 <strong>최신 건설공사 표준품셈</strong>(노무비/기계경비) 및 <strong>물가정보지</strong>(강재 임대손료 월 2.5%) 단가 근거를 제공하며, 실무 필요시 <strong>단가를 직접 수정</strong>할 수 있습니다.
                </span>
                <span className="font-mono text-[11px] text-amber-800 font-bold">도급/실행 단가 직접 수정 가능</span>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 shadow-xs overflow-hidden">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200 text-[11px]">
                    <tr>
                      <th className="py-2.5 px-3">공종명</th>
                      <th className="py-2.5 px-2 text-center">단위</th>
                      <th className="py-2.5 px-3">표준품셈 및 물가자료 산출 근거 (Cost Basis)</th>
                      <th className="py-2.5 px-3 text-right">재료비</th>
                      <th className="py-2.5 px-3 text-right">노무비</th>
                      <th className="py-2.5 px-3 text-right">경비</th>
                      <th className="py-2.5 px-3 text-right text-blue-800">도급단가 (원)</th>
                      <th className="py-2.5 px-3 text-right text-indigo-800">실행단가 (원)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                    {costRes.items.map(it => (
                      <tr key={it.id} className="hover:bg-slate-50">
                        <td className="py-2.5 px-3 font-sans font-bold text-slate-900">{it.name}</td>
                        <td className="py-2.5 px-2 text-center text-slate-600">{it.unit}</td>
                        <td className="py-2.5 px-3 font-sans text-slate-600 text-[10.5px]">
                          {it.costBasis}
                        </td>
                        <td className="py-2.5 px-3 text-right text-slate-500">{(it.materialCost ?? 0).toLocaleString()}</td>
                        <td className="py-2.5 px-3 text-right text-slate-500">{(it.laborCost ?? 0).toLocaleString()}</td>
                        <td className="py-2.5 px-3 text-right text-slate-500">{(it.expenseCost ?? 0).toLocaleString()}</td>
                        <td className="py-2.5 px-3 text-right">
                          <input
                            type="number"
                            step="1000"
                            value={it.contractUnitCost}
                            onChange={(e) => handleUnitCostChange(it.id, 'contract', parseFloat(e.target.value) || 0)}
                            className="w-24 bg-blue-50 border border-blue-300 rounded px-1.5 py-0.5 text-right font-bold text-blue-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
                          />
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <input
                            type="number"
                            step="1000"
                            value={it.executionUnitCost}
                            onChange={(e) => handleUnitCostChange(it.id, 'execution', parseFloat(e.target.value) || 0)}
                            className="w-24 bg-indigo-50 border border-indigo-300 rounded px-1.5 py-0.5 text-right font-bold text-indigo-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              탭 4: 4대안 종합 공사비 및 원가절감 비교 (Comparative Multi-Analysis)
             ══════════════════════════════════════════════════════════════════ */}
          {activeTab === 'COMPARISON' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                {allAltCostResults.map(res => {
                  const isCur = res.altId === selectedAltId;
                  return (
                    <div
                      key={res.altId}
                      className={`p-4 rounded-xl border transition-all ${
                        isCur
                          ? 'bg-blue-50/50 border-blue-400 shadow-sm'
                          : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className="flex justify-between items-center mb-2 pb-1.5 border-b border-slate-200">
                        <span className="font-bold text-slate-800 text-xs">{res.altName}</span>
                        {isCur && <span className="px-1.5 py-0.2 rounded text-[10px] bg-blue-600 text-white font-bold">현재 선택</span>}
                      </div>

                      <div className="space-y-2 font-mono text-xs">
                        <div className="flex justify-between">
                          <span className="text-slate-500 text-[11px]">도급 예정가:</span>
                          <strong className="text-slate-900">
                            {(res.totalContractCost / 1e6).toFixed(1)} 백만원
                          </strong>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-indigo-600 text-[11px]">실행 예산가:</span>
                          <strong className="text-indigo-800">
                            {(res.totalExecutionCost / 1e6).toFixed(1)} 백만원
                          </strong>
                        </div>

                        <div className="flex justify-between pt-1 border-t border-slate-100">
                          <span className="text-emerald-600 text-[11px]">원가 절감액:</span>
                          <strong className="text-emerald-700 font-bold">
                            -{(res.costSavings / 1e6).toFixed(1)} 백만원
                          </strong>
                        </div>

                        <div className="pt-2">
                          <div className="flex justify-between text-[10px] text-slate-500 mb-1">
                            <span>실행율</span>
                            <span className="font-bold text-indigo-700">{res.executionRatio}%</span>
                          </div>
                          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                            <div
                              className="bg-indigo-600 h-full rounded-full"
                              style={{ width: `${Math.min(100, res.executionRatio)}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* 모달 하단 푸터 */}
        <div className="bg-slate-100 px-6 py-3 border-t border-slate-200 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2 text-slate-500 font-mono text-[11px]">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>KDS 21 30 00 가설구조물 설계기준 및 최신 건설공사 표준품셈 100% 준수</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleDownloadCSV}
              className="px-4 py-2 rounded-lg text-xs font-bold bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 transition-all flex items-center gap-1.5"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-600" /> 엑셀 산출서 내보내기
            </button>
            <button
              onClick={onClose}
              className="px-5 py-2 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-white transition-all shadow-sm"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
