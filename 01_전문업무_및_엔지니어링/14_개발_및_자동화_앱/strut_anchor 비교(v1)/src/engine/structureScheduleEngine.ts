import { ProjectInputs, AlternativeSpec } from '../types';

export type ConstructionTaskType = 
  | 'foundation'              // 바닥 기초 (Invert / Bottom Slab)
  | 'story_wall'              // 층별 벽체 타설
  | 'story_column'            // 층별 중앙 RC 기둥 (철근·거푸집·타설)
  | 'strut_release_curing'    // 버팀보 해체 및 양생 대기
  | 'mid_slab'                // 중간 슬래브 (Concourse / Intermediate Slab)
  | 'top_slab'                // 상부 슬래브 (Top Slab / Roof)
  | 'kingpost_waterproof'     // 중간말뚝 관통부 인발/마감 및 누수방수
  | 'backfill'                // 토피 5m 전 구간 일괄 층다짐 되메우기
  | 'road_pavement';          // 아스팔트 도로 포장 및 노면 차선 도색

export type ElementStatus = 'not_started' | 'in_progress' | 'curing_waiting' | 'completed' | 'released';

export interface SpanTask {
  id: string;
  spanIndex: number;
  spanName: string;
  type: ConstructionTaskType;
  taskGroup: 'RC_STRUCTURE' | 'INTERFERENCE_SUPPORT' | 'PRE_POST' | 'FINISHING'; // 공종 분류 (RC본체 / 가시설간섭영향 / 선후행 / 마감)
  crewName?: string;          // 담당 작업조 (예: 'Crew A (1조)', 'Crew B (2조)')
  storyIndex?: number;        // 층 인덱스 (0: B2/최하층, 1: B1/중간층 등)
  storyName?: string;         // 'B2층', 'B1층'
  name: string;
  durationDays: number;
  startDay: number;
  endDay: number;
  isInterference: boolean;
  description: string;
  bottleneckType?: 'split_pour' | 'curing_wait' | 'kingpost_leak' | 'none';
}

export interface StoryState {
  storyIndex: number;
  storyName: string;          // 'B2 승강장층', 'B1 대합실층'
  wallStatus: ElementStatus;
  wallProgress: number;
  columnStatus: ElementStatus; // 중앙 RC 기둥 상태
  columnProgress: number;     // 중앙 RC 기둥 진행률 (0.0 ~ 1.0)
  slabStatus: ElementStatus;  // 해당 층의 상부 슬래브 상태 (최상층은 TopSlab)
  slabProgress: number;
  strutReleased: boolean;
}

export interface SpanDailyState {
  spanIndex: number;
  spanName: string;
  stationRange: string;
  numStories: number;
  storyStates: StoryState[];

  foundationStatus: ElementStatus;
  foundationProgress: number;

  columnStatus: ElementStatus; // 대표 기둥 상태
  columnProgress: number;     // 대표 기둥 진행률

  midSlabStatus: ElementStatus; // 2층 이상일 때 중간슬래브 대표 상태
  midSlabProgress: number;

  topSlabStatus: ElementStatus;
  topSlabProgress: number;

  strutReleaseStatus: ElementStatus;
  isStrutInterfering: boolean;

  kingPostStatus: ElementStatus;
  isKingPostInterfering: boolean;

  overallSpanProgress: number;
  currentActiveTaskName: string;
}

export interface AlternativeSpanScheduleResult {
  altId: number;
  altName: string;
  altType: string;
  totalLengthM: number;
  spanLengthM: number;
  numSpans: number;
  numStories: number;
  storyNames: string[];
  numCrews: number;
  totalDurationDays: number;
  tasks: SpanTask[];
  bottleneckSummary: {
    splitPourDelayDays: number;
    curingWaitDelayDays: number;
    kingPostDelayDays: number;
    totalInterferenceLossDays: number;
  };
}

export interface StructureGeometryInfo {
  excavationDepth: number;
  excavationWidth: number;
  totalLength: number;
  structWidth: number;         // 본체 구조물 폭 (m)
  structInnerWidth: number;    // 내부 순폭 (m)
  wallThickness: number;       // 외벽 두께 (m)
  numStories: number;          // 지하 층수
  storyNames: string[];        // 층별 명칭
  storyHeights: number[];      // 층별 높이 (m)
  overburdenSoilDepth: number; // 상부 토피고 (m)
  baseSlabThickness: number;   // 바닥 기초 두께 (m)
  roofSlabThickness: number;   // 지붕 슬래브 두께 (m)
  numSpans: number;            // 스팬 개수
  spanLength: number;          // 스팬 길이 (20m)
  floorAreaPerStoryM2: number; // 층당 바닥 면적 (m2)
  totalFloorAreaM2: number;    // 총 연면적 (m2)
  pourVolumePerSpanM3: number; // 스팬당 콘크리트 타설량 (m3)
}

export class StructureScheduleEngine {
  public static readonly DEFAULT_SPAN_LENGTH = 20;

  /**
   * 굴착 제원(H, B, L)에 따른 본체 구조물 폭, 층수, 연장, 단면 제원 자동 도출
   */
  public static determineStructureGeometry(inputs: ProjectInputs, customSpanLength: number = 20): StructureGeometryInfo {
    const H = inputs.excavationDepth;
    const B = inputs.excavationWidth;
    // 🌟 가시설 연장 L: 사용자 입력값 그대로 연계 (예: 100m 입력 시 L=100m)
    const totalLength = inputs.totalWallPerimeter > 0 ? inputs.totalWallPerimeter : 100.0;
    const spanLength = customSpanLength > 0 ? customSpanLength : 20.0;
    const numSpans = Math.max(1, Math.ceil(totalLength / spanLength));

    // 본체 구조물 폭: 굴착폭 B에서 좌우 가설 여유폭(각 0.8m, 합 1.6m) 차감
    const wallThickness = 0.8;
    const clearanceTotal = 1.6;
    const structWidth = Math.max(6.0, Number((B - clearanceTotal).toFixed(1)));
    const structInnerWidth = Math.max(4.4, Number((structWidth - 2 * wallThickness).toFixed(1)));

    // 층수 및 층별 높이 자동 판정
    const { numStories, storyNames, storyHeights } = this.determineStationStories(H);

    // 상부 토피 피복고 (사용자 요청: 약 5.0m 피복 가정)
    const overburdenSoilDepth = Number(Math.max(2.0, Math.min(8.0, 5.0)).toFixed(1));
    const baseSlabThickness = 1.0;
    const roofSlabThickness = 1.0;

    // 면적 및 물량
    const floorAreaPerStoryM2 = Math.round(totalLength * structWidth);
    const totalFloorAreaM2 = floorAreaPerStoryM2 * numStories;
    const pourVolumePerSpanM3 = Math.round(spanLength * structWidth * 1.2 + spanLength * 2 * wallThickness * (H - overburdenSoilDepth));

    return {
      excavationDepth: H,
      excavationWidth: B,
      totalLength,
      structWidth,
      structInnerWidth,
      wallThickness,
      numStories,
      storyNames,
      storyHeights,
      overburdenSoilDepth,
      baseSlabThickness,
      roofSlabThickness,
      numSpans,
      spanLength,
      floorAreaPerStoryM2,
      totalFloorAreaM2,
      pourVolumePerSpanM3
    };
  }

  /**
   * 굴착 깊이(H) 및 상부 피복(약 5m)에 따른 지하 정거장 적정 층수 판정
   */
  public static determineStationStories(H: number): { numStories: number; storyNames: string[]; storyHeights: number[] } {
    const overburden = 5.0; // 상부 5m 피복
    const netHeight = Math.max(4.0, H - overburden - 2.0); // 순 구조물 내부 높이

    if (netHeight <= 5.5 || H <= 12.0) {
      return {
        numStories: 1,
        storyNames: ['B1층 (단층 박스 / 대합실)'],
        storyHeights: [netHeight]
      };
    } else if (H <= 20.0) {
      // 12.0m ~ 20.0m: 표준 지하 2층 정거장 (H=15m일 때 B2 4.5m + B1 4.0m 등)
      const b2Height = Math.max(3.5, Number((netHeight * 0.55).toFixed(1)));
      const b1Height = Math.max(3.5, Number((netHeight - b2Height).toFixed(1)));
      return {
        numStories: 2,
        storyNames: ['B2 승강장층 (Platform)', 'B1 대합실층 (Concourse)'],
        storyHeights: [b2Height, b1Height]
      };
    } else if (H <= 28.0) {
      // 20.0m ~ 28.0m: 3층 환승 정거장
      const b3Height = 5.5;
      const b2Height = 4.5;
      const b1Height = Math.max(4.0, netHeight - b3Height - b2Height);
      return {
        numStories: 3,
        storyNames: ['B3 승강장층', 'B2 환승·설비층', 'B1 대합실층'],
        storyHeights: [b3Height, b2Height, b1Height]
      };
    } else {
      return {
        numStories: 4,
        storyNames: ['B4 승강장층', 'B3 환승홀', 'B2 기계실층', 'B1 대합실층'],
        storyHeights: [5.5, 4.5, 4.5, 4.5]
      };
    }
  }

  /**
   * 4대안의 20m 스팬, 작업조(Crew) 투입 방식 및 굴착깊이 연동 층별 구조물 축조 일정 산출
   */
  public static calculateSpanSchedules(
    inputs: ProjectInputs,
    alternatives: AlternativeSpec[],
    customSpanLength: number = 20,
    numCrews: number = 2 // 기본 2개 작업조 동시 투입 (패스트트랙)
  ): AlternativeSpanScheduleResult[] {
    const H = inputs.excavationDepth;
    const totalLength = inputs.totalWallPerimeter > 0 ? inputs.totalWallPerimeter : 100.0;
    const spanLength = customSpanLength > 0 ? customSpanLength : 20.0;
    const numSpans = Math.max(1, Math.ceil(totalLength / spanLength));

    const { numStories, storyNames } = this.determineStationStories(H);

    return alternatives.map(alt => {
      const isAnchor = alt.type === 'ALL_ANCHOR';
      const isHybrid = alt.type === 'HYBRID';
      const isCompStrut = alt.type === 'COMPOSITE_STRUT';
      const hasKingPost = alt.type === 'ALL_STRUT' || (alt.type === 'HYBRID' && inputs.excavationWidth >= 20);

      // 단위 소요일수 (스팬당 기준)
      const foundationDays = isAnchor ? 6 : (isCompStrut ? 6 : (isHybrid ? 7 : 8));
      const wallPerStoryDays = isAnchor ? 4 : (isCompStrut ? 5 : (isHybrid ? 5 : 6));
      const strutReleasePerStoryDays = isAnchor ? 0 : (isCompStrut ? 2 : (isHybrid ? 3 : 5)); // 층별 버팀보 해체 및 양생
      const midSlabPerStoryDays = isAnchor ? 5 : (isCompStrut ? 5 : (isHybrid ? 6 : 7));
      const topSlabDays = isAnchor ? 6 : (isCompStrut ? 6 : (isHybrid ? 7 : 8));
      const kingPostDays = (!isAnchor && hasKingPost) ? (isHybrid ? 2 : 3) : 0;

      const tasks: SpanTask[] = [];

      // 작업조별 직전 완료 시점 추적
      // numCrews = 1: 단일조 순차
      // numCrews = 2: 2개조 분할 (Crew A: 앞쪽 스팬들, Crew B: 뒤쪽 스팬들 동시 착수)
      // numCrews = 3: 3개조 급속
      const crewLastEnd: number[] = Array(numCrews).fill(0);
      const crewStoryEnd: number[][] = Array(numCrews).fill(0).map(() => Array(numStories).fill(0));

      for (let i = 0; i < numSpans; i++) {
        const spanName = `Span ${i + 1} (${(i * spanLength).toFixed(0)}m~${Math.min(totalLength, (i + 1) * spanLength).toFixed(0)}m)`;
        
        // 작업조 배정: 2개조 기준 i < Math.ceil(numSpans/2) -> Crew A, 나머지 -> Crew B
        const crewIdx = numCrews === 1 ? 0 : (i < Math.ceil(numSpans / numCrews) ? 0 : (numCrews === 3 && i >= Math.ceil((2 * numSpans) / 3) ? 2 : 1));
        const crewLabel = numCrews === 1 ? 'Crew 1 (전체)' : `Crew ${String.fromCharCode(65 + crewIdx)} (${crewIdx + 1}조)`;

        // 1. 바닥 기초 (Invert)
        const fStart = crewLastEnd[crewIdx];
        const fEnd = fStart + foundationDays;
        crewLastEnd[crewIdx] = fEnd;

        tasks.push({
          id: `span_${i}_foundation`,
          spanIndex: i,
          spanName,
          type: 'foundation',
          taskGroup: 'RC_STRUCTURE',
          crewName: crewLabel,
          name: `[${crewLabel}] ${spanName} 바닥 기초(Invert) 거푸집·배근·타설`,
          durationDays: foundationDays,
          startDay: fStart,
          endDay: fEnd,
          isInterference: !isAnchor && hasKingPost,
          description: isAnchor ? '무지보 공간 바닥 거푸집 ➡️ 철근 배근 ➡️ 콘크리트 연속 타설' : '중간말뚝 주변 철근 꿰기 배근 ➡️ 거푸집 마감 ➡️ 기초 콘크리트 타설',
          bottleneckType: 'none'
        });

        let currentDayTracker = fEnd;

        // 2. 층별 축조 순환 (최하층 B2 -> 중간층 -> 최상층 B1)
        for (let s = 0; s < numStories; s++) {
          const storyName = storyNames[s] || `B${numStories - s}층`;
          const isTopStory = s === numStories - 1;

          // 스트럿 구간 여부 판단: 앵커가 아니거나 하이브리드의 스트럿 적용 층
          const hasStrutInThisStory = !isAnchor && (alt.type === 'ALL_STRUT' || (alt.type === 'HYBRID' && s < numStories - 1) || alt.type === 'COMPOSITE_STRUT');

          if (hasStrutInThisStory) {
            // [스트럿 구간 2단 분할 타설 프로세스]
            // (1-1) 1단 하부 양측외벽(L/R) 타설 (버팀보 하단 레벨까지)
            const stage1Days = Math.max(3, Math.ceil(wallPerStoryDays / 2));
            const w1Start = Math.max(currentDayTracker, crewStoryEnd[crewIdx][s]);
            const w1End = w1Start + stage1Days;
            currentDayTracker = w1End;

            tasks.push({
              id: `span_${i}_story_${s}_wall_1`,
              spanIndex: i,
              spanName,
              type: 'story_wall',
              taskGroup: 'RC_STRUCTURE',
              crewName: crewLabel,
              storyIndex: s,
              storyName,
              name: `[${crewLabel}] ${spanName} ${storyName} 1단 하부벽체(L/R) 거푸집·배근·타설 (버팀보 하단)`,
              durationDays: stage1Days,
              startDay: w1Start,
              endDay: w1End,
              isInterference: true,
              description: `${storyName} 버팀보 하단 높이까지 1단 거푸집 조립 ➡️ 철근 배근 ➡️ 1차 벽체 콘크리트 타설`,
              bottleneckType: 'split_pour'
            });

            // (1-2) 14MPa 양생 확인 및 버팀보 해체 (가시설팀)
            const relStart = currentDayTracker;
            const relEnd = relStart + strutReleasePerStoryDays;
            currentDayTracker = relEnd;

            tasks.push({
              id: `span_${i}_story_${s}_strut_release`,
              spanIndex: i,
              spanName,
              type: 'strut_release_curing',
              taskGroup: 'INTERFERENCE_SUPPORT',
              crewName: '가시설팀 (버팀보 해체)',
              storyIndex: s,
              storyName,
              name: `⚠️ [가시설팀] ${spanName} ${storyName} 14MPa 양생 & 버팀보 절단/인양`,
              durationDays: strutReleasePerStoryDays,
              startDay: relStart,
              endDay: relEnd,
              isInterference: true,
              description: `1단 콘크리트 압축강도 14MPa 발현 5일 대기 후 ${storyName} 버팀보 절단 및 크레인 인양`,
              bottleneckType: 'curing_wait'
            });

            // (1-3) 2단 상부 양측외벽(L/R) 연결 타설 (버팀보 해체 후 상부 슬래브 하단까지)
            const stage2Days = Math.max(3, Math.floor(wallPerStoryDays / 2));
            const w2Start = currentDayTracker;
            const w2End = w2Start + stage2Days;
            currentDayTracker = w2End;

            tasks.push({
              id: `span_${i}_story_${s}_wall_2`,
              spanIndex: i,
              spanName,
              type: 'story_wall',
              taskGroup: 'RC_STRUCTURE',
              crewName: crewLabel,
              storyIndex: s,
              storyName,
              name: `[${crewLabel}] ${spanName} ${storyName} 2단 상부벽체(L/R) 거푸집·배근·타설 (슬래브 하단)`,
              durationDays: stage2Days,
              startDay: w2Start,
              endDay: w2End,
              isInterference: false,
              description: `버팀보 해체 후 개방된 공간에서 상부 슬래브 하단까지 2단 거푸집 조립 ➡️ 철근 배근 ➡️ 2차 연결 타설`,
              bottleneckType: 'none'
            });

          } else {
            // [어스앵커/무지보 구간: 1회 전단 일괄 타설]
            const wStart = Math.max(currentDayTracker, crewStoryEnd[crewIdx][s]);
            const wEnd = wStart + wallPerStoryDays;
            currentDayTracker = wEnd;

            tasks.push({
              id: `span_${i}_story_${s}_wall`,
              spanIndex: i,
              spanName,
              type: 'story_wall',
              taskGroup: 'RC_STRUCTURE',
              crewName: crewLabel,
              storyIndex: s,
              storyName,
              name: `[${crewLabel}] ${spanName} ${storyName} 외벽체(L/R) 전단 일괄 거푸집·배근·타설`,
              durationDays: wallPerStoryDays,
              startDay: wStart,
              endDay: wEnd,
              isInterference: false,
              description: `${storyName} 버팀보 간섭 없는 무지보 공간에서 대형 갱폼/거푸집 조립 ➡️ 철근 배근 ➡️ 1회 전단 일괄 타설`,
              bottleneckType: 'none'
            });
          }

          // (2) 층별 중앙 RC 기둥 축조 (슬래브 자중, 상부 뒷채움 토사 및 도로 교통하중 지지용)
          const colDays = 3; // 스팬당 기둥 4~5본 철근배근·거푸집·타설 3일 소요
          const colStart = currentDayTracker;
          const colEnd = colStart + colDays;
          currentDayTracker = colEnd;

          tasks.push({
            id: `span_${i}_story_${s}_column`,
            spanIndex: i,
            spanName,
            type: 'story_column',
            taskGroup: 'RC_STRUCTURE',
            crewName: crewLabel,
            storyIndex: s,
            storyName,
            name: `[${crewLabel}] ${spanName} ${storyName} 중앙 원형 RC 기둥(Φ1,000 @7.0m) 나선철근·원형폼·타설`,
            durationDays: colDays,
            startDay: colStart,
            endDay: colEnd,
            isInterference: false,
            description: `${storyName} 상부 슬래브 및 뒷채움 토사·교통하중 지지용 중앙 원형 RC 기둥(Φ1,000mm @7.0m 간격) 나선철근 배근 ➡️ 원형 폼 조립 ➡️ 콘크리트 타설`,
            bottleneckType: 'none'
          });

          // (3) 중간 슬래브 타설 (최상층이 아닌 경우)
          if (!isTopStory) {
            const midStart = currentDayTracker;
            const midEnd = midStart + midSlabPerStoryDays;
            currentDayTracker = midEnd;
            crewStoryEnd[crewIdx][s] = midEnd;

            tasks.push({
              id: `span_${i}_story_${s}_midslab`,
              spanIndex: i,
              spanName,
              type: 'mid_slab',
              taskGroup: 'RC_STRUCTURE',
              crewName: crewLabel,
              storyIndex: s,
              storyName,
              name: `[${crewLabel}] ${spanName} ${storyName} 중간 슬래브 거푸집·배근·타설`,
              durationDays: midSlabPerStoryDays,
              startDay: midStart,
              endDay: midEnd,
              isInterference: !isAnchor && hasKingPost,
              description: `${storyName} 상부 대합실 바닥 시스템 동바리 & 거푸집 조립 ➡️ 철근 배근 ➡️ 콘크리트 타설`,
              bottleneckType: 'none'
            });
          } else {
            crewStoryEnd[crewIdx][s] = currentDayTracker;
          }
        }

        // 3. 최상부 슬래브 (Top Slab / Roof - 뒷채움 토사 및 교통하중 지지)
        const topStart = currentDayTracker;
        const topEnd = topStart + topSlabDays;
        currentDayTracker = topEnd;
        crewLastEnd[crewIdx] = topEnd;

        tasks.push({
          id: `span_${i}_top_slab`,
          spanIndex: i,
          spanName,
          type: 'top_slab',
          taskGroup: 'RC_STRUCTURE',
          crewName: crewLabel,
          name: `[${crewLabel}] ${spanName} 지붕 슬래브(Roof) 거푸집·배근·타설 (토피 5m 하중지지)`,
          durationDays: topSlabDays,
          startDay: topStart,
          endDay: topEnd,
          isInterference: !isAnchor && hasKingPost,
          description: '지하 정거장 최상단 지붕 시스템 동바리 & 거푸집 조립 ➡️ 철근 배근 ➡️ 콘크리트 일체 타설',
          bottleneckType: 'none'
        });

        // 4. [핵심 영향 공종] 중간말뚝 인발 및 방수 마감 (Strut/Hybrid)
        if (kingPostDays > 0) {
          const kpStart = currentDayTracker;
          const kpEnd = kpStart + kingPostDays;
          currentDayTracker = kpEnd;
          crewLastEnd[crewIdx] = kpEnd;

          tasks.push({
            id: `span_${i}_kingpost`,
            spanIndex: i,
            spanName,
            type: 'kingpost_waterproof',
            taskGroup: 'INTERFERENCE_SUPPORT',
            crewName: '특수 인발/방수조',
            name: `⚠️ [영향 공종] ${spanName} 중간말뚝(King Post) 인발 & 관통부 무수축방수`,
            durationDays: kingPostDays,
            startDay: kpStart,
            endDay: kpEnd,
            isInterference: true,
            description: '슬래브 관통 중간말뚝 산소 절단/인양 + 무수축 그라우트 3중 방수 마감',
            bottleneckType: 'kingpost_leak'
          });
        }
      }

      // 🌟 [Phase 4 & 5] 6개 스팬 전 구획 구조물 완료 후 전 구간 일괄 되메우기 ➡️ 도로 포장 ➡️ 교통 개통
      const rcMaxEndDay = Math.max(...tasks.map(t => t.endDay), 0);

      // (1) 토피 5m 양질토사 전 구간 일괄 층다짐 되메우기 (8일)
      const backfillDays = 8;
      const backfillStart = rcMaxEndDay;
      const backfillEnd = backfillStart + backfillDays;

      tasks.push({
        id: 'global_phase4_backfill',
        spanIndex: numSpans - 1,
        spanName: '전 구간 (120m)',
        type: 'backfill',
        taskGroup: 'FINISHING',
        crewName: '토공·다짐조',
        name: `[Phase 4] 6개 스팬 전 구간(120m) 토피 5m 양질토사 층다짐 되메우기`,
        durationDays: backfillDays,
        startDay: backfillStart,
        endDay: backfillEnd,
        isInterference: false,
        description: '지하 구조물 100% 완료 후 지표면(EL 0m)까지 5m 토피 양질 토사 반입 ➡️ 20cm 층다짐(95% 다짐도) 일괄 되메우기',
        bottleneckType: 'none'
      });

      // (2) 아스팔트 도로 포장 및 차선 도색 (5일)
      const paveDays = 5;
      const paveStart = backfillEnd;
      const paveEnd = paveStart + paveDays;

      tasks.push({
        id: 'global_phase5_pavement',
        spanIndex: numSpans - 1,
        spanName: '전 구간 (120m)',
        type: 'road_pavement',
        taskGroup: 'FINISHING',
        crewName: '포장·도색조',
        name: `[Phase 5] 아스팔트 도로 포장(기층/표층) 및 노면 차선 도색`,
        durationDays: paveDays,
        startDay: paveStart,
        endDay: paveEnd,
        isInterference: false,
        description: '보조기층 다짐 ➡️ 아스팔트 기층/표층 포장 ➡️ 중앙선 및 주행 차선 도색 완료',
        bottleneckType: 'none'
      });

      const totalDurationDays = paveEnd;

      const splitPourDelayDays = numSpans * numStories * (isAnchor ? 0 : 2);
      const curingWaitDelayDays = numSpans * numStories * strutReleasePerStoryDays;
      const kingPostDelayDays = numSpans * kingPostDays;
      const totalInterferenceLossDays = splitPourDelayDays + curingWaitDelayDays + kingPostDelayDays;

      return {
        altId: alt.id,
        altName: alt.name,
        altType: alt.type,
        totalLengthM: totalLength,
        spanLengthM: spanLength,
        numSpans,
        numStories,
        storyNames,
        numCrews,
        totalDurationDays,
        tasks,
        bottleneckSummary: {
          splitPourDelayDays,
          curingWaitDelayDays,
          kingPostDelayDays,
          totalInterferenceLossDays
        }
      };
    });
  }

  /**
   * 일자별 스팬 및 층별 상태 평가
   */
  public static evaluateDailyState(
    schedule: AlternativeSpanScheduleResult,
    currentDay: number
  ): SpanDailyState[] {
    const { numSpans, spanLengthM, totalLengthM, numStories, storyNames, tasks } = schedule;
    const spanStates: SpanDailyState[] = [];

    for (let i = 0; i < numSpans; i++) {
      const spanTasks = tasks.filter(t => t.spanIndex === i);
      const spanName = `Span ${i + 1}`;
      const stationRange = `${(i * spanLengthM).toFixed(0)}m ~ ${Math.min(totalLengthM, (i + 1) * spanLengthM).toFixed(0)}m`;

      const getTaskStateById = (idPrefix: string): { status: ElementStatus; progress: number } => {
        const task = spanTasks.find(t => t.id.startsWith(idPrefix));
        if (!task) return { status: 'completed', progress: 1.0 };

        if (currentDay < task.startDay) {
          return { status: 'not_started', progress: 0.0 };
        } else if (currentDay >= task.endDay) {
          return { status: 'completed', progress: 1.0 };
        } else {
          const elapsed = currentDay - task.startDay;
          const prog = Math.min(1.0, Math.max(0.0, elapsed / Math.max(1, task.durationDays)));
          const isCuring = task.type === 'strut_release_curing';
          return {
            status: isCuring ? 'curing_waiting' : 'in_progress',
            progress: prog
          };
        }
      };

      const foundation = getTaskStateById(`span_${i}_foundation`);
      const topSlab = getTaskStateById(`span_${i}_top_slab`);
      const kingPost = getTaskStateById(`span_${i}_kingpost`);

      // 층별 상태 평가
      const storyStates: StoryState[] = [];
      let midSlabStatus: ElementStatus = 'not_started';
      let midSlabProgress = 0;
      let representativeColStatus: ElementStatus = 'not_started';
      let representativeColProgress = 0;
      let hasCuringWait = false;

      for (let s = 0; s < numStories; s++) {
        const sName = storyNames[s] || `B${numStories - s}층`;
        
        // 🌟 층별 모든 외벽 태스크(stage1, stage2 등) 정밀 종합 평가
        const storyWallTasks = spanTasks.filter(t => t.id.startsWith(`span_${i}_story_${s}_wall`));
        let wallStatus: ElementStatus = 'completed';
        let wallProgress = 1.0;

        if (storyWallTasks.length > 0) {
          const totalWallDays = storyWallTasks.reduce((sum, t) => sum + t.durationDays, 0);
          let totalElapsed = 0;
          let anyInProgress = false;
          let allNotStarted = true;

          storyWallTasks.forEach(t => {
            if (currentDay >= t.endDay) {
              totalElapsed += t.durationDays;
              allNotStarted = false;
            } else if (currentDay >= t.startDay) {
              totalElapsed += (currentDay - t.startDay);
              anyInProgress = true;
              allNotStarted = false;
            }
          });

          wallProgress = Math.min(1.0, Math.max(0.0, totalElapsed / Math.max(1, totalWallDays)));
          if (wallProgress >= 0.99) {
            wallStatus = 'completed';
          } else if (anyInProgress || wallProgress > 0) {
            wallStatus = 'in_progress';
          } else if (allNotStarted) {
            wallStatus = 'not_started';
          }
        }

        const colState = getTaskStateById(`span_${i}_story_${s}_column`);
        const strutState = getTaskStateById(`span_${i}_story_${s}_strut_release`);
        const slabState = s === numStories - 1 
          ? topSlab 
          : getTaskStateById(`span_${i}_story_${s}_midslab`);

        if (s === 0) {
          representativeColStatus = colState.status;
          representativeColProgress = colState.progress;
        }

        if (s === 0 && numStories > 1) {
          midSlabStatus = slabState.status;
          midSlabProgress = slabState.progress;
        }

        if (strutState.status === 'curing_waiting') {
          hasCuringWait = true;
        }

        storyStates.push({
          storyIndex: s,
          storyName: sName,
          wallStatus,
          wallProgress,
          columnStatus: colState.status,
          columnProgress: colState.progress,
          slabStatus: slabState.status,
          slabProgress: slabState.progress,
          strutReleased: strutState.status === 'completed' || strutState.status === 'released'
        });
      }

      const isStrutInterfering = hasCuringWait;
      const isKingPostInterfering = (schedule.altType !== 'ALL_ANCHOR' && kingPost.status !== 'completed');

      const activeTask = spanTasks.find(t => currentDay >= t.startDay && currentDay < t.endDay);
      const currentActiveTaskName = activeTask ? activeTask.name : (currentDay >= Math.max(...spanTasks.map(t => t.endDay)) ? '모든 구조물 축조 완료' : '착수 대기');

      const totalSpanDays = spanTasks.reduce((acc, t) => acc + t.durationDays, 0);
      let completedSpanDays = 0;
      spanTasks.forEach(t => {
        if (currentDay >= t.endDay) completedSpanDays += t.durationDays;
        else if (currentDay > t.startDay) completedSpanDays += (currentDay - t.startDay);
      });
      const overallSpanProgress = Math.min(100, Math.round((completedSpanDays / Math.max(1, totalSpanDays)) * 100));

      spanStates.push({
        spanIndex: i,
        spanName,
        stationRange,
        numStories,
        storyStates,
        foundationStatus: foundation.status,
        foundationProgress: foundation.progress,
        columnStatus: representativeColStatus,
        columnProgress: representativeColProgress,
        midSlabStatus,
        midSlabProgress,
        topSlabStatus: topSlab.status,
        topSlabProgress: topSlab.progress,
        strutReleaseStatus: hasCuringWait ? 'curing_waiting' : 'not_started',
        isStrutInterfering,
        kingPostStatus: kingPost.status,
        isKingPostInterfering,
        overallSpanProgress,
        currentActiveTaskName
      });
    }

    return spanStates;
  }
}
