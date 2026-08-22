import React, { useState, useMemo } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { StructureScheduleEngine, AlternativeSpanScheduleResult, SpanDailyState } from '../../engine/structureScheduleEngine';
import { LongitudinalProfileViewer } from './LongitudinalProfileViewer';
import { PlanViewAnimationViewer } from './PlanViewAnimationViewer';
import { CrossSectionAnimationViewer } from './CrossSectionAnimationViewer';
import { LongitudinalSpanViewer } from './LongitudinalSpanViewer';
import { TaktFlowViewer } from './TaktFlowViewer';
import { InteractiveGanttChart } from './InteractiveGanttChart';
import { ExecutiveBriefingPanel } from './ExecutiveBriefingPanel';
import { ExcavationScheduleView } from './ExcavationScheduleView';
import { TotalIntegratedScheduleView } from './TotalIntegratedScheduleView';
import { DigitalTwin3DViewer } from './DigitalTwin3DViewer';
import { 
  Building2, 
  Layers, 
  Map, 
  Columns, 
  Activity, 
  LayoutGrid, 
  Settings, 
  Sparkles,
  Scissors,
  Truck,
  Calendar,
  CheckCircle2,
  Box
} from 'lucide-react';

export type ScheduleCategory = 'excavation' | 'structure' | 'total';
export type ViewMode = 'combined' | '3d' | 'profile' | 'plan' | 'cross' | 'takt' | 'multi';

interface StructureSchedule4DViewProps {
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAltId: number;
  onSelectAltId: (id: number) => void;
}

export const StructureSchedule4DView: React.FC<StructureSchedule4DViewProps> = ({
  inputs,
  alternatives,
  selectedAltId,
  onSelectAltId
}) => {
  // 🌟 최상위 서브 탭: 개착 공기 vs 구조물 공기 vs 전체 통합 공기
  const [activeCategory, setActiveCategory] = useState<ScheduleCategory>('total');

  const [spanLength, setSpanLength] = useState<number>(20); // 기본 20m/스팬
  const [numCrews, setNumCrews] = useState<number>(2); // 기본 2개 작업조 동시 투입
  const [currentDay, setCurrentDay] = useState<number>(0);
  const [selectedSpanIdx, setSelectedSpanIdx] = useState<number>(0);
  const [activeViewMode, setActiveViewMode] = useState<ViewMode>('combined'); // 🌟 기본: 3D 트윈 + 2D 종단면 동시 보기

  // 1. 4대안 스팬 축조 일정 계산 (작업조 수 연동)
  const allSchedules: AlternativeSpanScheduleResult[] = useMemo(() => {
    return StructureScheduleEngine.calculateSpanSchedules(inputs, alternatives, spanLength, numCrews);
  }, [inputs, alternatives, spanLength, numCrews]);

  // 2. 현재 선택된 대안의 스케줄
  const currentSchedule = useMemo(() => {
    return allSchedules.find(s => s.altId === selectedAltId) || allSchedules[0];
  }, [allSchedules, selectedAltId]);

  // 3. 선택된 대안의 스펙 객체
  const selectedAlt = useMemo(() => {
    return alternatives.find(a => a.id === selectedAltId) || alternatives[0];
  }, [alternatives, selectedAltId]);

  // 4. 현재 일자(currentDay)에서의 스팬별 상태 계산
  const dailyStates = useMemo(() => {
    if (!currentSchedule) return [];
    return StructureScheduleEngine.evaluateDailyState(currentSchedule, currentDay);
  }, [currentSchedule, currentDay]);

  // 5. 현재 선택된 스팬의 상태
  const selectedSpanState: SpanDailyState = useMemo(() => {
    if (dailyStates.length === 0) {
      return {
        spanIndex: 0,
        spanName: 'Span 1',
        stationRange: '0.0m ~ 20.0m',
        numStories: currentSchedule?.numStories || 2,
        storyStates: [],
        foundationStatus: 'not_started',
        foundationProgress: 0,
        columnStatus: 'not_started',
        columnProgress: 0,
        midSlabStatus: 'not_started',
        midSlabProgress: 0,
        topSlabStatus: 'not_started',
        topSlabProgress: 0,
        strutReleaseStatus: 'not_started',
        isStrutInterfering: false,
        kingPostStatus: 'not_started',
        isKingPostInterfering: false,
        overallSpanProgress: 0,
        currentActiveTaskName: '착수 대기'
      };
    }
    return dailyStates[Math.min(selectedSpanIdx, dailyStates.length - 1)];
  }, [dailyStates, selectedSpanIdx, currentSchedule]);

  return (
    <div className="space-y-4 font-sans animate-fade-in">
      {/* 🌟 0. 공기 산정 메인 카테고리 전환 스위처 (개착 공기 vs 구조물 공기 vs 전체 통합) */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-xl p-3 px-4 shadow-md flex flex-wrap items-center justify-between gap-3 border border-slate-700">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-indigo-600 text-white">
            <Calendar className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-xs font-bold text-white flex items-center gap-2">
              <span>공사기간(공기) 종합 산정 & 4D 시뮬레이션 시스템</span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/30 text-indigo-300 font-mono">
                3대 영역 분류
              </span>
            </h2>
            <p className="text-[11px] text-slate-400">
              {activeCategory === 'total'
                ? '🌐 [Phase 1~4 전주기] 개착 토공사 + 본체 구조물 축조 전체 공기 종합 비교'
                : activeCategory === 'excavation' 
                ? '🚚 [개착 공기] 벽체·중간말뚝 ➡️ 자립고 단계별 굴착 및 지보재 가설(양생) ➡️ 해체 공기'
                : '🏢 [본체 구조물 축조 공기] 지하 RC 본체 구조물 20m 스팬별 축조 4D 시뮬레이션'}
            </p>
          </div>
        </div>

        {/* 3대 카테고리 전환 버튼 그룹 */}
        <div className="flex items-center bg-slate-800/90 p-1 rounded-lg border border-slate-700 gap-1">
          <button
            onClick={() => setActiveCategory('excavation')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeCategory === 'excavation'
                ? 'bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 shadow-md ring-2 ring-amber-300 ring-offset-1 ring-offset-slate-900 font-extrabold'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/60'
            }`}
          >
            <Truck className="w-3.5 h-3.5" />
            <span>1. 개착 공기</span>
          </button>

          <button
            onClick={() => setActiveCategory('structure')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeCategory === 'structure'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md ring-2 ring-blue-300 ring-offset-1 ring-offset-slate-900 font-extrabold'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/60'
            }`}
          >
            <Building2 className="w-3.5 h-3.5" />
            <span>2. 본체 구조물 공기</span>
          </button>

          <button
            onClick={() => setActiveCategory('total')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-md text-xs font-bold transition-all ${
              activeCategory === 'total'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md ring-2 ring-indigo-300 ring-offset-1 ring-offset-slate-900 font-extrabold'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/60'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>3. 전체 공기 (개착 + 구조물 종합)</span>
          </button>
        </div>
      </div>

      {/* 🌟 1. [개착 공기 산정] 서브 탭 화면 */}
      {activeCategory === 'excavation' && (
        <ExcavationScheduleView
          inputs={inputs}
          alternatives={alternatives}
          selectedAltId={selectedAltId}
          onSelectAltId={onSelectAltId}
        />
      )}

      {/* 🌟 3. [전체 공기 통합 종합 비교] 서브 탭 화면 */}
      {activeCategory === 'total' && (
        <TotalIntegratedScheduleView
          inputs={inputs}
          alternatives={alternatives}
          selectedAltId={selectedAltId}
          onSelectAltId={onSelectAltId}
        />
      )}

      {/* 🌟 2. [본체 구조물 축조 공기] 서브 탭 화면 (기존 4D 시뮬레이션 일체) */}
      {activeCategory === 'structure' && (
        <div className="space-y-4">
          {/* 1. 상단 컨트롤 & 뷰 모드 전환 리본 툴바 */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-600 text-white shadow-md">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-sm font-black text-slate-900">
                    본체 RC 구조물 축조 4D 시뮬레이션 & 간트차트 시스템
                  </h2>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">
                    종단면 / 평면 / 횡단면 연동
                  </span>
                </div>
                <p className="text-xs text-slate-500">
                  진행방향(종방향) 20m 분할 타설 및 버팀보 순차 해체·절단 과정을 다각도 2D 시각화로 완벽 묘사
                </p>
              </div>
            </div>

            {/* 뷰 모드 전환 탭 & 스팬 설정 */}
            <div className="flex flex-wrap items-center gap-3">
          {/* 뷰어 선택 탭 */}
          <div className="flex flex-wrap items-center bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs gap-0.5">
            <button
              onClick={() => setActiveViewMode('combined')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === 'combined'
                  ? 'bg-gradient-to-r from-indigo-600 to-blue-600 text-white shadow-xs'
                  : 'text-slate-700 hover:text-indigo-700'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>✨ 1. 3D 트윈 + 2D 종단면 통합 (동시보기)</span>
            </button>

            <button
              onClick={() => setActiveViewMode('profile')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === 'profile'
                  ? 'bg-white text-indigo-700 shadow-xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>2. 2D 종단면도 단독</span>
            </button>

            <button
              onClick={() => setActiveViewMode('3d')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === '3d'
                  ? 'bg-white text-indigo-700 shadow-xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Box className="w-3.5 h-3.5" />
              <span>3. 3D 디지털 트윈 단독</span>
            </button>

            <button
              onClick={() => setActiveViewMode('plan')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === 'plan'
                  ? 'bg-white text-teal-700 shadow-xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Map className="w-3.5 h-3.5" />
              <span>4. 2D 평면도</span>
            </button>

            <button
              onClick={() => setActiveViewMode('cross')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === 'cross'
                  ? 'bg-white text-blue-700 shadow-xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Columns className="w-3.5 h-3.5" />
              <span>5. 2D 횡단면도</span>
            </button>

            <button
              onClick={() => setActiveViewMode('takt')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === 'takt'
                  ? 'bg-white text-indigo-700 shadow-xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Activity className="w-3.5 h-3.5 text-indigo-600" />
              <span>6. Takt 흐름선도 (LOB)</span>
            </button>

            <button
              onClick={() => setActiveViewMode('multi')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-bold transition-all ${
                activeViewMode === 'multi'
                  ? 'bg-white text-purple-700 shadow-xs border border-slate-200'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              <span>7. 전 화면 멀티뷰</span>
            </button>
          </div>

          {/* 작업조(Work Crew) 투입 방식 설정 */}
          <div className="flex items-center gap-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 text-xs">
            <span className="text-slate-600 font-medium">👷 작업조 투입:</span>
            <select
              value={numCrews}
              onChange={(e) => setNumCrews(Number(e.target.value))}
              className="bg-white border border-slate-300 rounded px-2 py-1 font-sans font-bold text-indigo-700 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value={1}>1개 작업조 (순차 시공 / 경제형)</option>
              <option value={2}>2개 작업조 (동시 분할 / 추천 · 공기 40% 단축)</option>
              <option value={3}>3개 작업조 (3구획 동시 / 최단 급속 시공)</option>
            </select>
          </div>

          {/* 스팬 길이 설정 컨트롤 */}
          <div className="flex items-center gap-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 text-xs">
            <Settings className="w-3.5 h-3.5 text-slate-500" />
            <span className="text-slate-600 font-medium">스팬 길이:</span>
            <select
              value={spanLength}
              onChange={(e) => setSpanLength(Number(e.target.value))}
              className="bg-white border border-slate-300 rounded px-2 py-1 font-mono font-bold text-blue-700 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value={15}>15m / 스팬</option>
              <option value={20}>20m / 스팬 (표준)</option>
              <option value={25}>25m / 스팬</option>
              <option value={30}>30m / 스팬</option>
            </select>
          </div>
        </div>
      </div>

      {/* 🌟 1-2. 굴착 제원 연동 본체 RC 구조물 자동 결정 제원 바 (Single Source of Truth) */}
      {(() => {
        const geom = StructureScheduleEngine.determineStructureGeometry(inputs, spanLength);
        return (
          <div className="bg-white border border-blue-200 rounded-xl p-3 px-4 shadow-sm bg-gradient-to-r from-blue-50/50 via-indigo-50/30 to-white flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <span className="p-1 rounded bg-blue-600 text-white font-bold text-[10px]">연동결과</span>
              <span className="font-bold text-slate-800">
                가시설 제원(굴착 H={inputs.excavationDepth}m · B={inputs.excavationWidth}m · L={geom.totalLength}m)에 연동된 본체 구조물 모델링:
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-2.5 font-mono">
              <div className="px-2.5 py-1 rounded-md bg-white border border-slate-200 shadow-2xs">
                <span className="text-slate-500 text-[10px] block">본체 폭 (B_struct)</span>
                <span className="font-black text-blue-700">{geom.structWidth}m</span>
                <span className="text-[9px] text-slate-400"> (순내폭 {geom.structInnerWidth}m)</span>
              </div>

              <div className="px-2.5 py-1 rounded-md bg-white border border-slate-200 shadow-2xs">
                <span className="text-slate-500 text-[10px] block">지하 층수 (Stories)</span>
                <span className="font-black text-indigo-700">지하 {geom.numStories}층</span>
                <span className="text-[9px] text-slate-400"> ({geom.storyNames.join('/')})</span>
              </div>

              <div className="px-2.5 py-1 rounded-md bg-white border border-slate-200 shadow-2xs">
                <span className="text-slate-500 text-[10px] block">총 연장 & 스팬</span>
                <span className="font-black text-slate-800">{geom.totalLength}m</span>
                <span className="text-[9px] text-slate-400"> ({geom.spanLength}m × {geom.numSpans}스팬)</span>
              </div>

              <div className="px-2.5 py-1 rounded-md bg-white border border-slate-200 shadow-2xs">
                <span className="text-slate-500 text-[10px] block">층당 바닥면적</span>
                <span className="font-black text-slate-800">{geom.floorAreaPerStoryM2.toLocaleString()}㎡</span>
                <span className="text-[9px] text-slate-400"> (연면적 {geom.totalFloorAreaM2.toLocaleString()}㎡)</span>
              </div>
            </div>
          </div>
        );
      })()}

      {/* 2. 경영진 C-Level 브리핑 요약 패널 */}
      <ExecutiveBriefingPanel
        allSchedules={allSchedules}
        alternatives={alternatives}
        inputs={inputs}
        selectedAltId={selectedAltId}
        onSelectAltId={onSelectAltId}
      />

      {/* 3. 종방향 6개 스팬 미니 진행도 맵 */}
      {currentSchedule && (
        <LongitudinalSpanViewer
          schedule={currentSchedule}
          dailyStates={dailyStates}
          currentDay={currentDay}
          selectedSpanIdx={selectedSpanIdx}
          onSelectSpan={setSelectedSpanIdx}
        />
      )}

      {/* 4. 메인 그래픽 뷰어 (선택된 모드에 따라 렌더링) */}
      {currentSchedule && (
        <div className="space-y-4">
          {/* 모드 0: 3D 디지털 트윈 뷰어 (360도 자유회전 / BIM 트윈) */}
          {(activeViewMode === 'combined' || activeViewMode === '3d' || activeViewMode === 'multi') && (
            <DigitalTwin3DViewer
              inputs={inputs}
              selectedAlt={selectedAlt}
              schedule={currentSchedule}
              dailyStates={dailyStates}
              currentDay={currentDay}
              onDayChange={setCurrentDay}
              selectedSpanIdx={selectedSpanIdx}
              onSelectSpan={setSelectedSpanIdx}
            />
          )}

          {/* 모드 1: 2D 종단면도 (Profile View - 실시간 릴레이 축조 묘사) */}
          {(activeViewMode === 'combined' || activeViewMode === 'profile' || activeViewMode === 'multi') && (
            <LongitudinalProfileViewer
              inputs={inputs}
              selectedAlt={selectedAlt}
              schedule={currentSchedule}
              dailyStates={dailyStates}
              currentDay={currentDay}
              selectedSpanIdx={selectedSpanIdx}
              onSelectSpan={setSelectedSpanIdx}
            />
          )}

          {/* 모드 2: 평면도 (Plan View) */}
          {(activeViewMode === 'plan' || activeViewMode === 'multi') && (
            <PlanViewAnimationViewer
              inputs={inputs}
              selectedAlt={selectedAlt}
              schedule={currentSchedule}
              dailyStates={dailyStates}
              currentDay={currentDay}
              selectedSpanIdx={selectedSpanIdx}
              onSelectSpan={setSelectedSpanIdx}
            />
          )}

          {/* 모드 3: 횡단면도 (Cross-Section View) */}
          {(activeViewMode === 'cross' || activeViewMode === 'multi') && (
            <CrossSectionAnimationViewer
              inputs={inputs}
              selectedAlt={selectedAlt}
              schedule={currentSchedule}
              selectedSpanState={selectedSpanState}
              currentDay={currentDay}
            />
          )}

          {/* 모드 4: Takt 선형 흐름선도 (Line of Balance View) */}
          {(activeViewMode === 'takt' || activeViewMode === 'multi') && (
            <TaktFlowViewer
              schedule={currentSchedule}
              allSchedules={allSchedules}
              currentDay={currentDay}
              onDayChange={setCurrentDay}
              selectedSpanIdx={selectedSpanIdx}
              onSelectSpan={setSelectedSpanIdx}
            />
          )}
        </div>
      )}

          {/* 5. 대화형 간트 차트 및 타임라인 컨트롤러 */}
          {currentSchedule && (
            <InteractiveGanttChart
              schedule={currentSchedule}
              currentDay={currentDay}
              onDayChange={setCurrentDay}
              selectedSpanIdx={selectedSpanIdx}
              onSelectSpan={setSelectedSpanIdx}
            />
          )}
        </div>
      )}
    </div>
  );
};
