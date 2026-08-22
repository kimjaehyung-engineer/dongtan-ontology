import React from 'react';
import { ProjectInputs } from '../../types';
import { SITE_PRESETS } from '../../engine/presets';
import { 
  Building2, 
  Layers, 
  Table2, 
  PieChart, 
  FileSpreadsheet, 
  FileText, 
  Play, 
  RotateCcw,
  Sparkles,
  HelpCircle,
  FolderOpen,
  CheckCircle2,
  Calendar
} from 'lucide-react';

interface HeaderProps {
  inputs: ProjectInputs;
  onSelectPreset: (preset: Partial<ProjectInputs>) => void;
  onOpenReport: () => void;
  onOpenSunexExport: () => void;
  onOpenDetailedCost: () => void;
  onOpenScheduleBasis?: () => void;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRunAnalysis: () => void;
  isSolving: boolean;
  hasPendingChanges: boolean;
  isAllSafe?: boolean;
  isCostCommitted?: boolean;
  onCommitStructuralDesign?: () => void;
  lastCommittedTime?: string;
}

export const Header: React.FC<HeaderProps> = ({
  inputs,
  onSelectPreset,
  onOpenReport,
  onOpenSunexExport,
  onOpenDetailedCost,
  onOpenScheduleBasis,
  activeTab,
  setActiveTab,
  onRunAnalysis,
  isSolving = false,
  hasPendingChanges = false,
  isAllSafe = true,
  isCostCommitted = true,
  onCommitStructuralDesign,
  lastCommittedTime
}) => {
  return (
    <header className="bg-white border-b border-slate-300 shadow-sm sticky top-0 z-40">
      {/* 1. 최상단 타이틀 바 */}
      <div className="px-5 py-2.5 border-b border-slate-200 flex flex-wrap items-center justify-between gap-4 bg-slate-900 text-white">
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded-lg bg-blue-600 shadow-md">
            <Building2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm font-black tracking-tight text-white font-mono">
                GeoOptima Retaining 2026
              </h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/30 text-blue-300 border border-blue-400/40">
                v1.2 Commercial Pro
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              지하 가시설 벽체 지지공법(Strut vs Anchor) 사전 최적설계 시스템
            </p>
          </div>
        </div>

        {/* 🌟 강력한 구조해석 실행 버튼 & 수량/단가 산출근거 모달 버튼 */}
        <div className="flex items-center gap-2">
          {/* [구조해석 실행] 버튼 */}
          <button
            onClick={onRunAnalysis}
            disabled={isSolving}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded font-bold text-xs shadow-xs transition-all ${
              hasPendingChanges
                ? 'bg-amber-500 hover:bg-amber-600 text-slate-950 ring-2 ring-amber-300 ring-offset-1 ring-offset-slate-900 animate-pulse'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white'
            }`}
            title="수정된 지반/단면 제원으로 4대안 유한요소 탄소성 해석 재수행"
          >
            <Play className={`w-3.5 h-3.5 ${isSolving ? 'animate-spin' : 'fill-current'}`} />
            <span>{isSolving ? '해석 계산 중...' : hasPendingChanges ? '해석 재실행 (변경됨)' : '구조해석 재실행'}</span>
          </button>

          {/* 🌟 [구조해석 완료 & 공사비/수량 확정 반영] 수동 승인 버튼 */}
          <button
            onClick={onCommitStructuralDesign}
            disabled={!isAllSafe || isSolving}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded text-xs font-bold shadow-md transition-all ${
              !isAllSafe
                ? 'bg-slate-800 text-slate-500 border border-slate-700 cursor-not-allowed'
                : isCostCommitted && !hasPendingChanges
                ? 'bg-emerald-700 hover:bg-emerald-600 text-white border border-emerald-500'
                : 'bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-extrabold ring-2 ring-emerald-300 ring-offset-1 ring-offset-slate-900 animate-bounce'
            }`}
            title={!isAllSafe ? '구조안전 미달(NG) 항목이 있어 수량을 확정할 수 없습니다.' : '4대안 구조안전성 O.K 확인 완료! 확정된 수량을 공사비 내역서에 최종 동결 반영합니다.'}
          >
            <CheckCircle2 className={`w-4 h-4 ${isAllSafe ? 'text-white' : 'text-slate-500'}`} />
            <span>{isCostCommitted && !hasPendingChanges ? '✅ 구조해석 확정완료 (공사비 반영됨)' : '🔒 구조해석 완료 & 공사비 반영'}</span>
          </button>

          <div className="h-6 w-px bg-slate-700 mx-1"></div>

          {/* 🌟 수량·단가 산출근거 & 도급/실행 예산 모달 버튼 */}
          <button
            onClick={onOpenDetailedCost}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-indigo-600/90 hover:bg-indigo-600 text-white border border-indigo-500 text-xs font-bold shadow-xs transition-all"
            title="수량산출 근거 및 도급/실행 단가 상세 검증"
          >
            <FileSpreadsheet className="w-3.5 h-3.5 text-amber-300" />
            <span>수량·단가 산출근거</span>
          </button>

          {/* 🌟 공기 산정 근거서 모달 버튼 */}
          {onOpenScheduleBasis && (
            <button
              onClick={onOpenScheduleBasis}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-blue-700 hover:bg-blue-600 text-white border border-blue-500 text-xs font-bold shadow-xs transition-all"
              title="3대안 공사기간(공기) 정밀 산출 근거서 (표준품셈 & 시방서 연동)"
            >
              <Calendar className="w-3.5 h-3.5 text-amber-300" />
              <span>공기 산정 근거서</span>
            </button>
          )}

          {/* SUNEX 데이터 시트 모달 버튼 */}
          <button
            onClick={onOpenSunexExport}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold shadow-xs transition-all"
            title="SUNEX / MIDAS 연계 지반 및 단면 제원 시트"
          >
            <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-400" />
            <span>SUNEX 연계 시트</span>
          </button>

          {/* 기술검토 보고서 모달 버튼 */}
          <button
            onClick={onOpenReport}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-blue-600/90 hover:bg-blue-600 text-white border border-blue-500 text-xs font-bold shadow-xs transition-all"
            title="4대안 기술검토 보고서 생성 및 A4 인쇄"
          >
            <FileText className="w-3.5 h-3.5 text-white" />
            <span>기술보고서 (A4)</span>
          </button>
        </div>
      </div>

      {/* 2. 상용 CAD/CAE 스타일 리본 툴바 및 탭 메뉴 */}
      <div className="px-5 py-2 flex flex-wrap items-center justify-between gap-4 bg-slate-50">
        {/* 네비게이션 탭 */}
        <div className="flex items-center gap-1.5 bg-slate-200/80 p-1 rounded-lg border border-slate-300">
          <button
            onClick={() => setActiveTab('design')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeTab === 'design'
                ? 'bg-white text-blue-700 shadow-xs border border-slate-200'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>1. 단면 설계 및 실시간 해석</span>
          </button>

          <button
            onClick={() => setActiveTab('alternatives')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeTab === 'alternatives'
                ? 'bg-white text-blue-700 shadow-xs border border-slate-200'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
            }`}
          >
            <Table2 className="w-3.5 h-3.5" />
            <span>2. 3대안 다기준 비교 (Matrix)</span>
          </button>

          <button
            onClick={() => setActiveTab('cost')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeTab === 'cost'
                ? 'bg-white text-blue-700 shadow-xs border border-slate-200'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
            }`}
          >
            <PieChart className="w-3.5 h-3.5" />
            <span>3. 경제성 및 공기·LCC 분석</span>
          </button>

          <button
            onClick={() => setActiveTab('schedule4d')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeTab === 'schedule4d'
                ? 'bg-blue-600 text-white shadow-xs border border-blue-500 ring-2 ring-blue-200'
                : 'text-slate-700 hover:text-blue-700 hover:bg-slate-200/60'
            }`}
          >
            <Calendar className="w-3.5 h-3.5" />
            <span>4. 공기 산정 (개착 vs 구조물)</span>
          </button>
        </div>

        {/* 우측 프로젝트 상태 표시 */}
        <div className="flex items-center gap-2 text-xs text-slate-500 font-mono">
          <span className={`w-2 h-2 rounded-full ${isCostCommitted && !hasPendingChanges ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
          <span>
            {isCostCommitted && !hasPendingChanges
              ? `🔒 구조해석 확정 수량 반영 완료 (${lastCommittedTime || '최신'})`
              : '⚠️ 파라미터 수정됨 — [구조해석 완료 & 공사비 반영] 필요'}
          </span>
        </div>
      </div>
    </header>
  );
};
