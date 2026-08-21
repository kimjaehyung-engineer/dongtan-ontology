import React, { useState, useMemo } from 'react';
import type { ProjectInputs, AlternativeSpec } from './types';
import { DEFAULT_PROJECT_INPUTS } from './engine/presets';
import { AlternativeEvaluator } from './engine/femElastoPlasticEngine';
import { Header } from './components/layout/Header';
import { SoilLayerEditor } from './components/input/SoilLayerEditor';
import { ExcavationWallInput } from './components/input/ExcavationWallInput';
import { AnchorConfigPanel } from './components/input/AnchorConfigPanel';
import { CrossSectionSVG } from './components/visualizer/CrossSectionSVG';
import { DiagramViewer } from './components/visualizer/DiagramViewer';
import { AlternativeMatrix } from './components/comparison/AlternativeMatrix';
import { CostRadarChart } from './components/comparison/CostRadarChart';
import { SunexDataExporter } from './components/report/SunexDataExporter';
import { EngineeringReport } from './components/report/EngineeringReport';
import { DetailedCostModal } from './components/cost/DetailedCostModal';
import { LccScheduleComparison } from './components/comparison/LccScheduleComparison';
import { EngineeringBalancePanel } from './components/common/EngineeringBalancePanel';
import { SmartRemedyPanel } from './components/common/SmartRemedyPanel';
import { Zap, Sparkles, CheckCircle2, AlertCircle, Play, RefreshCw, AlertTriangle } from 'lucide-react';
import confetti from 'canvas-confetti';
import { useEffect } from 'react';

const STORAGE_KEY_DRAFT = 'geooptima_retaining_draft_inputs_v1';
const STORAGE_KEY_SOLVED = 'geooptima_retaining_solved_inputs_v1';
const STORAGE_KEY_COMMITTED = 'geooptima_retaining_committed_inputs_v1';
const STORAGE_KEY_TIME = 'geooptima_retaining_committed_time_v1';
const STORAGE_KEY_ALT_ID = 'geooptima_retaining_selected_alt_id_v1';
const STORAGE_KEY_TAB = 'geooptima_retaining_active_tab_v1';

function getStoredValue<T>(key: string, fallback: T): T {
  try {
    const item = typeof window !== 'undefined' ? window.localStorage.getItem(key) : null;
    if (!item) return fallback;
    const parsed = JSON.parse(item);
    if (typeof fallback === 'object' && fallback !== null && !Array.isArray(fallback)) {
      return { ...fallback, ...parsed };
    }
    return parsed;
  } catch (e) {
    return fallback;
  }
}

export function App() {
  // 1. draftInputs: 사용자가 폼에서 자유롭게 입력/편집 중인 상태 (localStorage 영구 복원)
  const [draftInputs, setDraftInputs] = useState<ProjectInputs>(() => 
    getStoredValue<ProjectInputs>(STORAGE_KEY_DRAFT, DEFAULT_PROJECT_INPUTS)
  );
  
  // 2. solvedInputs: [구조해석 실행] 버튼을 눌러 확정 해석된 입력 상태 (localStorage 영구 복원)
  const [solvedInputs, setSolvedInputs] = useState<ProjectInputs>(() => 
    getStoredValue<ProjectInputs>(STORAGE_KEY_SOLVED, DEFAULT_PROJECT_INPUTS)
  );

  // 3. committedCostInputs: [구조해석 완료 & 공사비/수량 반영] 수동 확정된 입력 상태
  const [committedCostInputs, setCommittedCostInputs] = useState<ProjectInputs>(() => 
    getStoredValue<ProjectInputs>(STORAGE_KEY_COMMITTED, DEFAULT_PROJECT_INPUTS)
  );
  const [isCostCommitted, setIsCostCommitted] = useState<boolean>(true);
  const [lastCommittedTime, setLastCommittedTime] = useState<string>(() => 
    getStoredValue<string>(STORAGE_KEY_TIME, '초기 기준설계')
  );

  const [activeTab, setActiveTab] = useState<string>(() => 
    getStoredValue<string>(STORAGE_KEY_TAB, 'design')
  );
  const [selectedAltId, setSelectedAltId] = useState<number>(() => 
    getStoredValue<number>(STORAGE_KEY_ALT_ID, 1)
  );
  const [currentStageIdx, setCurrentStageIdx] = useState<number>(0);
  const [isReportOpen, setIsReportOpen] = useState<boolean>(false);
  const [isSunexOpen, setIsSunexOpen] = useState<boolean>(false);
  const [isCostModalOpen, setIsCostModalOpen] = useState<boolean>(false);
  const [isSolving, setIsSolving] = useState<boolean>(false);

  // 상태 변경 시 localStorage 즉시 동기화
  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY_DRAFT, JSON.stringify(draftInputs));
    } catch (e) {}
  }, [draftInputs]);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY_SOLVED, JSON.stringify(solvedInputs));
    } catch (e) {}
  }, [solvedInputs]);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY_COMMITTED, JSON.stringify(committedCostInputs));
    } catch (e) {}
  }, [committedCostInputs]);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY_TIME, JSON.stringify(lastCommittedTime));
    } catch (e) {}
  }, [lastCommittedTime]);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY_ALT_ID, JSON.stringify(selectedAltId));
    } catch (e) {}
  }, [selectedAltId]);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY_TAB, JSON.stringify(activeTab));
    } catch (e) {}
  }, [activeTab]);

  // 새로고침/종료 시 최종 저장 보장
  useEffect(() => {
    const handleBeforeUnload = () => {
      try {
        window.localStorage.setItem(STORAGE_KEY_DRAFT, JSON.stringify(draftInputs));
        window.localStorage.setItem(STORAGE_KEY_SOLVED, JSON.stringify(solvedInputs));
        window.localStorage.setItem(STORAGE_KEY_COMMITTED, JSON.stringify(committedCostInputs));
      } catch (e) {}
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [draftInputs, solvedInputs, committedCostInputs]);

  // 전체 초기화 함수
  const handleResetToDefault = () => {
    if (window.confirm('모든 입력 조건을 초기 표준 설계값으로 리셋하시겠습니까?')) {
      try {
        localStorage.removeItem(STORAGE_KEY_DRAFT);
        localStorage.removeItem(STORAGE_KEY_SOLVED);
        localStorage.removeItem(STORAGE_KEY_COMMITTED);
        localStorage.removeItem(STORAGE_KEY_TIME);
        localStorage.removeItem(STORAGE_KEY_ALT_ID);
      } catch (e) {}
      setDraftInputs(DEFAULT_PROJECT_INPUTS);
      setSolvedInputs(DEFAULT_PROJECT_INPUTS);
      setCommittedCostInputs(DEFAULT_PROJECT_INPUTS);
      setLastCommittedTime('초기 기준설계');
      setSelectedAltId(1);
      confetti({ particleCount: 40, spread: 60, origin: { y: 0.3 } });
    }
  };

  // 입력값이 변경되었는지 여부
  const hasPendingChanges = useMemo(() => {
    return JSON.stringify(draftInputs) !== JSON.stringify(solvedInputs);
  }, [draftInputs, solvedInputs]);

  // 해석 결과 생성 (오직 solvedInputs 기준으로만 해석 수행!)
  const alternatives: AlternativeSpec[] = useMemo(() => {
    return AlternativeEvaluator.generate4Alternatives(solvedInputs);
  }, [solvedInputs]);

  // 4대안 전체 구조안전성 O.K 여부 판정
  const isAllSafe = useMemo(() => {
    return alternatives.every(alt => alt.isStructurallySafe);
  }, [alternatives]);

  // 공사비 산정용 대안 (오직 수동 확정된 committedCostInputs 기준으로만 산출!)
  const committedAlternatives: AlternativeSpec[] = useMemo(() => {
    return AlternativeEvaluator.generate4Alternatives(committedCostInputs);
  }, [committedCostInputs]);

  const selectedAlt = useMemo(() => {
    return alternatives.find(a => a.id === selectedAltId) || alternatives[0];
  }, [alternatives, selectedAltId]);

  const selectedCommittedAlt = useMemo(() => {
    return committedAlternatives.find(a => a.id === selectedAltId) || committedAlternatives[0];
  }, [committedAlternatives, selectedAltId]);

  // [구조해석 실행] 버튼 핸들러 (구조해석과 공사비 산정을 100% 동기화)
  const handleRunAnalysis = (overrideInputs?: ProjectInputs) => {
    const target = overrideInputs || draftInputs;
    setIsSolving(true);
    setTimeout(() => {
      setSolvedInputs(target);
      setCommittedCostInputs(target);
      setIsCostCommitted(true);
      if (overrideInputs) {
        setDraftInputs(overrideInputs);
      }
      const now = new Date();
      const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
      setLastCommittedTime(timeStr);
      setIsSolving(false);
      confetti({ particleCount: 30, spread: 60, origin: { y: 0.25 } });
    }, 40);
  };

  // 🌟 [구조해석 완료 & 공사비/수량 확정 반영] 수동 확정 핸들러
  const handleCommitStructuralDesign = () => {
    if (!isAllSafe) {
      alert('⚠️ 4대안 중 구조안전 미달(NG) 항목이 있어 공사비를 확정할 수 없습니다. 설계를 보정해 주세요.');
      return;
    }
    setCommittedCostInputs(solvedInputs);
    setIsCostCommitted(true);
    const now = new Date();
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    setLastCommittedTime(timeStr);
    confetti({ particleCount: 80, spread: 100, origin: { y: 0.2 } });
  };

  // 프리셋 불러오기
  const handleSelectPreset = (presetData: Partial<ProjectInputs>) => {
    const updated = { ...draftInputs, ...presetData };
    setDraftInputs(updated);
    handleRunAnalysis(updated);
  };

  // 스마트 처방 패널에서 원클릭 보정 적용 시
  const handleApplyRemedyFix = (updatedInputs: ProjectInputs) => {
    setDraftInputs(updatedInputs);
    handleRunAnalysis(updatedInputs);
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 flex flex-col font-sans">
      {/* 1. 상단 글로벌 리본 바 헤더 */}
      <Header
        inputs={draftInputs}
        onSelectPreset={handleSelectPreset}
        onOpenReport={() => setIsReportOpen(true)}
        onOpenSunexExport={() => setIsSunexOpen(true)}
        onOpenDetailedCost={() => setIsCostModalOpen(true)}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRunAnalysis={() => handleRunAnalysis()}
        isSolving={isSolving}
        hasPendingChanges={hasPendingChanges}
        isAllSafe={isAllSafe}
        isCostCommitted={isCostCommitted}
        onCommitStructuralDesign={handleCommitStructuralDesign}
        lastCommittedTime={lastCommittedTime}
      />

      {/* 2. 메인 컨텐츠 영역 */}
      <main className="flex-1 p-5 max-w-[1600px] w-full mx-auto space-y-4">
        {/* 상단 프로젝트 요약 바 & 해석 실행 배너 */}
        <div className="bg-white border border-slate-200 rounded-lg p-3 px-4 flex flex-wrap items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-4 text-xs">
            <div>
              <span className="text-slate-500 font-medium">프로젝트명: </span>
              <input
                type="text"
                value={draftInputs.projectName}
                onChange={(e) => setDraftInputs({ ...draftInputs, projectName: e.target.value })}
                className="bg-transparent text-slate-900 font-bold border-b border-transparent hover:border-slate-300 focus:border-blue-500 focus:outline-none px-1"
              />
            </div>
            <div className="h-3 w-px bg-slate-300"></div>
            <div>
              <span className="text-slate-500 font-medium">굴착 깊이: </span>
              <span className="text-blue-700 font-mono font-bold">{draftInputs.excavationDepth} m</span>
            </div>
            <div className="h-3 w-px bg-slate-300"></div>
            <div>
              <span className="text-slate-500 font-medium">굴착 폭: </span>
              <span className="text-blue-700 font-mono font-bold">{draftInputs.excavationWidth} m</span>
            </div>
            <div className="h-3 w-px bg-slate-300"></div>
            <div>
              <span className="text-slate-500 font-medium">지층: </span>
              <span className="text-amber-700 font-mono font-bold">{draftInputs.soils.length}개 층위</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* 변경 사항 감지 및 수동 해석 실행 버튼 */}
            {hasPendingChanges ? (
              <button
                onClick={() => handleRunAnalysis()}
                disabled={isSolving}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-xs shadow-md transition-all animate-pulse"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>입력치 변경됨 → [구조해석 실행]</span>
              </button>
            ) : (
              <span className="text-xs text-slate-500 flex items-center gap-1 font-mono">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                최신 해석 결과 반영됨
              </span>
            )}

            <div className="h-4 w-px bg-slate-300"></div>

            <div className="text-xs text-slate-600 flex items-center gap-1.5 font-medium">
              <Zap className="w-3.5 h-3.5 text-amber-500" />
              <span>선택 대안: </span>
              <span className="text-blue-700 font-bold">
                대안 {selectedAlt.id} ({selectedAlt.type})
              </span>
            </div>
            <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold border flex items-center gap-1 ${
              selectedAlt.isStructurallySafe
                ? 'bg-emerald-50 text-emerald-700 border-emerald-300'
                : 'bg-rose-50 text-rose-700 border-rose-300'
            }`}>
              {selectedAlt.isStructurallySafe ? <CheckCircle2 className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
              구조적 {selectedAlt.isStructurallySafe ? '안전 (O.K)' : '단면 보강 필요 (NG)'}
            </span>
          </div>
        </div>

        {/* 🌟 다목적 공학 균형도 진단 및 골든존(65%~80%) 최적 조율 패널 */}
        <EngineeringBalancePanel
          inputs={draftInputs}
          alternative={selectedAlt}
          onApplyBalancedInputs={(balanced) => handleRunAnalysis(balanced)}
        />

        {/* 🌟 구조적 NG 진단 및 공학적 최적 처방 가이드 패널 */}
        <SmartRemedyPanel
          inputs={solvedInputs}
          selectedAlt={selectedAlt}
          onApplyFix={handleApplyRemedyFix}
        />

        {/* 탭 1: 단면 설계 및 수동 해석 실행 */}
        {activeTab === 'design' && (
          <div className="space-y-4">
            {/* 좌: CAD 2D 단면도 / 우: 토목 다이어그램 (변위/모멘트/전단력/토압) */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
              <div className="lg:col-span-8">
                <CrossSectionSVG
                  alternative={selectedAlt}
                  inputs={solvedInputs}
                  currentStageIdx={currentStageIdx}
                />
              </div>
              <div className="lg:col-span-4">
                <DiagramViewer
                  alternative={selectedAlt}
                  currentStageIdx={currentStageIdx}
                  onSelectStage={setCurrentStageIdx}
                />
              </div>
            </div>

            {/* 대안 빠른 스위처 */}
            <div className="flex items-center justify-between gap-2 bg-white p-2.5 rounded-lg border border-slate-200 shadow-sm">
              <div className="flex items-center gap-2 overflow-x-auto">
                <span className="text-xs text-slate-500 font-bold whitespace-nowrap">해석 대안 전환:</span>
                {alternatives.map((alt) => (
                  <button
                    key={alt.id}
                    onClick={() => {
                      setSelectedAltId(alt.id);
                      setCurrentStageIdx(0);
                      setDraftInputs(prev => ({ ...prev, supports: alt.supports }));
                    }}
                    className={`px-3 py-1.5 rounded text-xs font-bold whitespace-nowrap transition-all flex items-center gap-1.5 border shadow-xs ${
                      alt.id === selectedAltId
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                        : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                    }`}
                  >
                    {alt.rank === 1 && <Sparkles className="w-3 h-3 text-amber-300" />}
                    {alt.name}
                    <span className="text-[10px] opacity-85">({alt.overallScore}점)</span>
                  </button>
                ))}
              </div>

              {/* 하단 해석 실행 버튼 */}
              {hasPendingChanges && (
                <button
                  onClick={() => handleRunAnalysis()}
                  disabled={isSolving}
                  className="flex items-center gap-1.5 px-4 py-1.5 rounded bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs whitespace-nowrap"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>설계 입력 완료 → 구조해석 실행</span>
                </button>
              )}
            </div>

            {/* 굴착 제원 및 H-Pile / 버팀보 / 띠장 / 앵커 사양 및 간격 입력 (대안에 따라 동적 전환) */}
            <ExcavationWallInput
              inputs={draftInputs}
              onChangeInputs={setDraftInputs}
              onRunAnalysis={handleRunAnalysis}
              selectedAltType={selectedAlt.type}
            />

            {/* 🌟 고각 어스앵커 (45° ~ 70°) 상세 설계 및 제어 패널 */}
            <AnchorConfigPanel
              inputs={draftInputs}
              onChangeSupports={(updatedSups) => setDraftInputs({ ...draftInputs, supports: updatedSups })}
              onRunAnalysis={handleRunAnalysis}
            />

            {/* 지층 다단 프로파일 및 P-y 지반정수 편집기 (draftInputs 바인딩) */}
            <SoilLayerEditor
              soils={draftInputs.soils}
              inputs={draftInputs}
              onChangeSoils={(newSoils) => setDraftInputs({ ...draftInputs, soils: newSoils })}
              onRunAnalysis={handleRunAnalysis}
            />
          </div>
        )}

        {/* 탭 2: 4대안 다기준 비교 */}
        {activeTab === 'alternatives' && (
          <div className="space-y-4">
            <AlternativeMatrix
              alternatives={alternatives}
              selectedAltId={selectedAltId}
              onSelectAlt={setSelectedAltId}
            />

            {/* 선택 대안 상세 시각화 */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 pt-2">
              <div className="lg:col-span-7">
                <CrossSectionSVG
                  alternative={selectedAlt}
                  inputs={solvedInputs}
                  currentStageIdx={selectedAlt.stageResults.length - 1}
                />
              </div>
              <div className="lg:col-span-5">
                <DiagramViewer
                  alternative={selectedAlt}
                  currentStageIdx={selectedAlt.stageResults.length - 1}
                  onSelectStage={setCurrentStageIdx}
                />
              </div>
            </div>
          </div>
        )}

        {/* 탭 3: 경제성 및 공기·LCC 종합 분석 (확정된 수량 기준 렌더링) */}
        {activeTab === 'cost' && (
          <div className="space-y-5">
            {/* 🌟 1. 공기 간섭 분석 및 LCC 총생애주기비용 비교 카드 */}
            <LccScheduleComparison
              inputs={solvedInputs}
              alternatives={alternatives}
              selectedAltId={selectedAltId}
              onSelectAlt={setSelectedAltId}
            />

            {/* 🌟 2. 직접공사비 세부 내역 및 다차원 평가 */}
            <CostRadarChart
              alternatives={alternatives}
              selectedAlt={selectedAlt}
              onSelectAlt={setSelectedAltId}
            />
          </div>
        )}
      </main>

      {/* 하단 엔지니어링 Status Bar */}
      <footer className="border-t border-slate-300 bg-white px-5 py-2 text-xs text-slate-600 flex flex-wrap items-center justify-between gap-4 font-mono shadow-inner">
        <div className="flex items-center gap-3">
          <span className="font-sans font-bold text-slate-800">GeoOptima 2026</span>
          <span>|</span>
          <span>SOLVER: C++ 1D Non-linear FEM (Winkler P-y)</span>
          <span>|</span>
          <span>MODE: Committed Structural QTO Costing</span>
        </div>
        <div className="flex items-center gap-3 text-slate-500 text-[11px]">
          <span>확정 반영 시각: {lastCommittedTime}</span>
          <span>|</span>
          <span>X: 0.00 ~ {solvedInputs.excavationWidth.toFixed(1)}m</span>
          <span>Z: 0.00 ~ -{solvedInputs.wall.totalLength.toFixed(1)}m</span>
          <span>|</span>
          <button
            onClick={handleResetToDefault}
            className="px-2 py-0.5 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold border border-slate-300 shadow-2xs transition-all flex items-center gap-1"
            title="모든 입력값과 설정을 초기 기본 상태로 되돌립니다."
          >
            <RefreshCw className="w-3 h-3 text-blue-600" />
            <span>기본값 리셋</span>
          </button>
        </div>
      </footer>

      {/* 모달들 (Single Source of Truth: 정확하게 산정된 alternatives 기준 일관성 100% 보장) */}
      <DetailedCostModal
        isOpen={isCostModalOpen}
        onClose={() => setIsCostModalOpen(false)}
        alternatives={alternatives}
        currentAltId={selectedAltId}
        inputs={solvedInputs}
      />

      <SunexDataExporter
        isOpen={isSunexOpen}
        onClose={() => setIsSunexOpen(false)}
        inputs={solvedInputs}
        selectedAlt={selectedAlt}
      />

      <EngineeringReport
        isOpen={isReportOpen}
        onClose={() => setIsReportOpen(false)}
        inputs={solvedInputs}
        alternatives={alternatives}
        selectedAlt={selectedAlt}
      />
    </div>
  );
}

export default App;
