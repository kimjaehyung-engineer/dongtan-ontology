import { ProjectInputs, AlternativeSpec } from '../types';

export interface ScheduleSubTask {
  name: string;
  days: number;
  formula: string;
  note: string;
  standardBasis: string;
  bottleneckType?: 'none' | 'anchor_grout_curing' | 'strut_split_pour' | 'strut_curing_wait' | 'kingpost_driving' | 'kingpost_extraction';
}

export interface SchedulePhaseResult {
  name: string;
  durationDays: number;
  description: string;
  subTasks: ScheduleSubTask[];
}

export interface StepwiseExcavationCycle {
  tierIndex: number;
  stageName: string;
  excavationDepth: number; // 해당 단계 굴착 심도 (m)
  excavationVolumeM3: number; // 해당 단계 굴착 토량
  dominantSoilName?: string; // 해당 단의 주요 지층 및 강도 (ex: "풍화암 (N=40)", "연암 (브레이커 파쇄)")
  dailyExcavationRate?: number; // 지층 강도 & 가시설 지보 간섭 반영 일일 굴착속도 (㎥/일)
  pureExcavationDays: number; // 순수 굴착 일수
  supportInstallDays: number; // 지보재 설치 일수
  curingWaitDays: number; // 앵커 그라우트 정착장 조강 양생 대기 일수 (5일)
  totalCycleDays: number; // 해당 단 총 소요일수
  isAnchorTier: boolean;
  description: string;
}

export interface AlternativeScheduleResult {
  altId: number;
  altName: string;
  altType: string;
  numStories: number;
  totalVolumeM3: number;
  wallPerimeterM: number;
  totalDurationDays: number;
  totalDurationMonths: number;
  savedDaysComparedToBaseline: number;
  savedMonthsComparedToBaseline: number;
  phases: {
    wallAndPiles: SchedulePhaseResult;    // Phase 1: 흙막이벽체 및 중간말뚝 시공
    stepwiseExcavation: SchedulePhaseResult; // Phase 2: 단계별 굴착 & 지보 가설 (자립고 굴착 ➡️ 지보 ➡️ 앵커양생)
    structure: SchedulePhaseResult;        // Phase 3: 지하 본체 RC 구조물 축조 (거푸집·배근·타설)
    dismantle: SchedulePhaseResult;        // Phase 4: 가시설 해체, 중간말뚝 인발 및 되메우기
  };
  stepwiseCycles: StepwiseExcavationCycle[];
  blockOutJointCount: number;
  rebarEfficiencyRatio: number;
  formworkEfficiencyRatio: number;
  timeDrivers: {
    wallPileDays: number;
    earthworkDays: number;
    anchorGroutDelayDays: number;
    structureDays: number;
    strutSplitDelayDays: number;
    kingPostLossDays: number;
    dismantleDays: number;
  };
}

export class ConstructionScheduleEngine {
  /**
   * 굴착 제원 및 가시설 지보 조건에 따른 4대안 전주기(Phase 1~4) 공정 일정 정밀 산출
   */
  public static calculateSchedules(
    inputs: ProjectInputs,
    alternatives: AlternativeSpec[],
    numCrews: number = 1
  ): AlternativeScheduleResult[] {
    const H = inputs.excavationDepth;
    const B = inputs.excavationWidth;
    const totalPerimeter = inputs.totalWallPerimeter > 0 ? inputs.totalWallPerimeter : 100.0 * 2 + B * 2;
    const L = inputs.totalWallPerimeter > 0 ? inputs.totalWallPerimeter / 2.0 : 100.0;
    const floorAreaM2 = Math.round(L * B);
    const totalVolumeM3 = Math.round(floorAreaM2 * H);

    // 굴착 깊이에 따른 지하 층수
    let numStories = 2;
    if (H <= 8.0) numStories = 1;
    else if (H <= 16.0) numStories = 2;
    else if (H <= 24.0) numStories = 3;
    else numStories = 4;

    const results: AlternativeScheduleResult[] = alternatives.map((alt) => {
      const isAnchor = alt.type === 'ALL_ANCHOR';
      const isHybrid = alt.type === 'HYBRID';
      const isCompStrut = alt.type === 'COMPOSITE_STRUT';
      const numTiers = alt.supports.length;

      // =========================================================================
      // Phase 1: 흙막이벽체 및 중간말뚝(King Post) 시공
      // =========================================================================
      // 벽체 근입장(H_embed) 및 총 시공 심도
      const embedDepth = Number((H * 0.35).toFixed(1));
      const totalWallDepth = H + embedDepth;
      const pileSpacing = 1.8; // H-Pile 간격 (m)
      const numWallPiles = Math.ceil(totalPerimeter / pileSpacing);
      
      // 오거 천공(T4/DRA) + H-Pile 건입 + 밀크 주입 현장 현실 생산성 (일일 3본/장비조)
      const dailyPileDriveRate = 3;
      const wallPileDays = Math.ceil(numWallPiles / dailyPileDriveRate);

      // 중간말뚝(King Post) 본수 및 시공 일수
      // - ALL_STRUT: 스팬 4.0m, 굴착폭에 따라 중간말뚝 설치 (B >= 16m일 때 필수)
      // - HYBRID: 굴착폭 B >= 20m일 때 하부 스트럿용 중간말뚝 일부 설치
      // - ALL_ANCHOR / COMPOSITE_STRUT: 무중간말뚝 (0본)
      let numKingPosts = 0;
      if (alt.type === 'ALL_STRUT') {
        const rows = B >= 22 ? 2 : (B >= 14 ? 1 : 0);
        numKingPosts = rows * Math.ceil(L / 4.0);
      } else if (alt.type === 'HYBRID' && B >= 20) {
        numKingPosts = Math.ceil(L / 6.0);
      }

      const dailyKingPostRate = 3; // 복공/하중 지지용 대형 중간말뚝 정밀 천공 (일일 3본/조)
      const kingPostInstallDays = numKingPosts > 0 ? Math.ceil(numKingPosts / dailyKingPostRate) : 0;
      const phase1TotalDays = wallPileDays + kingPostInstallDays;

      const phase1: SchedulePhaseResult = {
        name: 'Phase 1. 흙막이벽체 및 중간말뚝 시공',
        durationDays: phase1TotalDays,
        description: `엄지말뚝 ${numWallPiles}본 천공·건입(${wallPileDays}일, 3본/일)` + 
          (numKingPosts > 0 ? ` + 중간말뚝(King Post) ${numKingPosts}본 정밀 항타(${kingPostInstallDays}일, 3본/일)` : ' + 무중간말뚝 공법(중간말뚝 시공 0일)'),
        subTasks: [
          {
            name: `H-Pile 흙막이벽체 천공 및 항타 (총 ${numWallPiles}본)`,
            days: wallPileDays,
            formula: `외주연장 ${totalPerimeter.toFixed(0)}m ÷ @1.8m = ${numWallPiles}본 ÷ 3본/일 = ${wallPileDays}일`,
            note: `벽체 깊이 ${totalWallDepth.toFixed(1)}m (굴착 ${H}m + 근입장 ${embedDepth}m) 대형 오거/T4 천공 및 H-Pile 건입 (1일 3본 현장 실적 적용)`,
            standardBasis: '토목공사 표준품셈 3-2 가설 흙막이 말뚝 시공 (DRA 천공+근입 3본/일)',
            bottleneckType: 'none'
          },
          ...(numKingPosts > 0 ? [{
            name: `중간말뚝(King Post) 천공 및 근입 (${numKingPosts}본)`,
            days: kingPostInstallDays,
            formula: `중간말뚝 ${numKingPosts}본 ÷ 일일 3본 = ${kingPostInstallDays}일`,
            note: '지하 정거장 지지 및 버팀보 교차 지지용 중간말뚝 정밀 천공 및 하부 근입 (일일 3본)',
            standardBasis: '가설공사 표준시방서 KCS 21 30 00 복공 및 중간말뚝공 (3본/일)',
            bottleneckType: 'kingpost_driving' as const
          }] : [{
            name: '중간말뚝 무배치 (시공 일수 0일 단축)',
            days: 0,
            formula: '무중간말뚝 공법 적용으로 King Post 천공/항타 생략',
            note: isAnchor ? '어스앵커 무지보 방식으로 내부 말뚝 불필요' : '합성사각 고강성 강관 적용으로 무중간말뚝 구현',
            standardBasis: '엔지니어링 사전설계 최적화 기준',
            bottleneckType: 'none' as const
          }])
        ]
      };

      // =========================================================================
      // Phase 2: 단계별 굴착 & 지보 가설 (자립고 굴착 ➡️ 지보 ➡️ 앵커양생 반복 사이클)
      // 🌟 지반 종류(토사, 풍화암, 연암) 및 강도(N치)에 따른 단별 굴착 생산성 동적 산정
      // =========================================================================
      const stepwiseCycles: StepwiseExcavationCycle[] = [];
      let totalEarthworkDays = 0;
      let totalAnchorCuringDelayDays = 0;
      let totalStrutInstallDays = 0;

      // 단별 지보 깊이 목록
      const tierDepths = alt.supports.map(s => s.depth);
      let prevDepth = 0;

      for (let t = 0; t <= numTiers; t++) {
        const isLastBottom = t === numTiers;
        const currentTierDepth = isLastBottom ? H : tierDepths[t];
        const stepDepth = Math.max(1.5, currentTierDepth - prevDepth);
        const stepVol = Math.round(floorAreaM2 * stepDepth);

        // 🌟 단별 지층(토사/풍화토/풍화암/연암) 및 N치에 따른 기저 굴착 속도 산출
        let weightedSoilRate = 600;
        const matchedSoilNames: string[] = [];

        if (inputs.soils && inputs.soils.length > 0) {
          let sumLayerRate = 0;
          for (const layer of inputs.soils) {
            const overlapTop = Math.max(prevDepth, layer.topDepth);
            const overlapBottom = Math.min(currentTierDepth, layer.bottomDepth);
            const overlapLen = Math.max(0, overlapBottom - overlapTop);

            if (overlapLen > 0) {
              const fraction = overlapLen / stepDepth;
              const nVal = layer.NValue || 20;
              const lname = layer.name.toLowerCase();

              // 토목 표준품셈 기계굴착 생산성 (백호 0.7~1.0㎥ 기준)
              let layerBase = 650; // 일반 토사 650 ㎥/일
              if (lname.includes('연암') || lname.includes('경암') || lname.includes('rock') || (!lname.includes('풍화') && nVal >= 50)) {
                layerBase = 220; // 연암/경암 브레이커 파쇄 220 ㎥/일
                matchedSoilNames.push(`${layer.name}(연암/브레이커)`);
              } else if (lname.includes('풍화암') || nVal >= 35) {
                layerBase = 420; // 풍화암 리핑/브레이커 420 ㎥/일
                matchedSoilNames.push(`${layer.name}(N=${nVal})`);
              } else if (lname.includes('풍화토') || (nVal >= 15 && nVal < 35)) {
                layerBase = 620; // 풍화토 620 ㎥/일
                matchedSoilNames.push(`${layer.name}(N=${nVal})`);
              } else {
                layerBase = 750; // 매립토/퇴적토/점토 750 ㎥/일
                matchedSoilNames.push(`${layer.name}(N=${nVal})`);
              }

              sumLayerRate += fraction * layerBase;
            }
          }
          if (sumLayerRate > 0) weightedSoilRate = sumLayerRate;
        }

        // 지보 형식 및 작업공간 간섭 보정계수
        let spaceEfficiency = 0.65; // All Strut: 4.0m 격자 + 중간말뚝 15본 간섭 (35% 감쇄)
        if (isAnchor) {
          spaceEfficiency = 1.00;   // All Anchor: 무지보 100% 개방 고속 양중
        } else if (isCompStrut) {
          spaceEfficiency = 0.85;   // Composite Strut: 5.0m 광폭 무말뚝 양호 공간
        } else if (isHybrid) {
          spaceEfficiency = t <= 1 ? 0.92 : 0.70; // 상부 앵커 개방, 하부 스트럿
        }

        const tierDailyRate = Math.max(100, Math.round(weightedSoilRate * spaceEfficiency));
        const stepPureExcDays = Math.max(2, Math.ceil(stepVol / tierDailyRate));
        const dominantSoilStr = matchedSoilNames.length > 0 ? matchedSoilNames.join('/') : '혼합토사';

        let stepSupportDays = 0;
        let stepCuringDays = 0;
        let isAnchorThisTier = false;

        if (!isLastBottom) {
          const supportType = alt.supports[t]?.type;
          isAnchorThisTier = isAnchor || supportType === 'GROUND_ANCHOR';

          if (isAnchorThisTier) {
            // 어스앵커: 천공 + 그라우트 주입 2일 + ⚠️ 정착장 조강 양생 5일 대기
            stepSupportDays = 2;
            stepCuringDays = 5;
            totalAnchorCuringDelayDays += 5;
          } else {
            // 스트럿: 띠장 + 버팀보 거치 + 유압잭 가압 (양생대기 0일, 즉시 차기 굴착)
            stepSupportDays = isCompStrut ? 2 : 2.5;
            stepCuringDays = 0;
            totalStrutInstallDays += stepSupportDays;
          }
        }

        const stepTotalDays = stepPureExcDays + stepSupportDays + stepCuringDays;
        totalEarthworkDays += stepTotalDays;

        stepwiseCycles.push({
          tierIndex: t + 1,
          stageName: isLastBottom ? `최종 바닥 굴착 (GL-${prevDepth.toFixed(1)}m ~ GL-${H.toFixed(1)}m)` : `${t + 1}차 굴착 & ${t + 1}단 ${isAnchorThisTier ? '어스앵커' : '버팀보'} 가설`,
          excavationDepth: currentTierDepth,
          excavationVolumeM3: stepVol,
          dominantSoilName: dominantSoilStr,
          dailyExcavationRate: tierDailyRate,
          pureExcavationDays: stepPureExcDays,
          supportInstallDays: stepSupportDays,
          curingWaitDays: stepCuringDays,
          totalCycleDays: stepTotalDays,
          isAnchorTier: isAnchorThisTier,
          description: isLastBottom 
            ? `최종 심도 GL-${H.toFixed(1)}m [${dominantSoilStr}] 굴착(${stepPureExcDays}일, ${tierDailyRate}㎥/일) 및 버림타설`
            : `[${dominantSoilStr}] 굴착(${stepPureExcDays}일, ${tierDailyRate}㎥/일) ➡️ ${isAnchorThisTier ? '앵커 천공/그라우팅(2일) + ⚠️정착장 5일 양생대기' : '버팀보 가설 및 프리로드 가압(2일, 양생 0일)'}`
        });

        prevDepth = currentTierDepth;
      }

      const phase2: SchedulePhaseResult = {
        name: 'Phase 2. 단계별 굴착 & 가시설 지보 가설',
        durationDays: totalEarthworkDays,
        description: isAnchor 
          ? `지층 강도 연동 무지보 고속양중 + 앵커 ${numTiers}단 정착장 양생대기(${totalAnchorCuringDelayDays}일)`
          : `지층 강도 연동 버팀보 간섭양중 + 강관 버팀보 ${numTiers}단 가압 가설(${totalStrutInstallDays.toFixed(0)}일, 굴착 즉시 착수)`,
        subTasks: [
          {
            name: `단계별 지반 굴착 (총 ${totalVolumeM3.toLocaleString()}㎥) 및 토류판 설치`,
            days: stepwiseCycles.reduce((sum, c) => sum + c.pureExcavationDays, 0),
            formula: `단별 지층 강도(토사 650~750 ㎥/일 vs 풍화암 420 vs 연암 220) × 지보간섭 계수 연동`,
            note: isAnchor ? '버팀보 없는 Clamshell/백호 고속 양중 (토류판 굴착 병행)' : '버팀보 간섭으로 백호 선회 반경 및 크레인 양중 속도 감쇄',
            standardBasis: '표준품셈 3-1-2 지반 강도별 굴착기계 토사/암반 수직 양중 기준'
          },
          ...(totalAnchorCuringDelayDays > 0 ? [{
            name: `어스앵커 천공·그라우팅 & ⚠️정착장 양생 대기`,
            days: totalAnchorCuringDelayDays + stepwiseCycles.filter(c => c.isAnchorTier).reduce((s, c) => s + c.supportInstallDays, 0),
            formula: `앵커 ${stepwiseCycles.filter(c => c.isAnchorTier).length}단 × (시공 2일 + 정착장 조강 양생 5일 대기) = ${totalAnchorCuringDelayDays + stepwiseCycles.filter(c => c.isAnchorTier).length * 2}일`,
            note: '정착장 그라우트 설계강도(14MPa) 발현 전 하부 굴착 금지 (도로교설계기준)',
            standardBasis: '국토교통부 지반공사 표준시방서 KCS 11 70 05 어스앵커공',
            bottleneckType: 'anchor_grout_curing' as const
          }] : []),
          ...(totalStrutInstallDays > 0 ? [{
            name: `강관 버팀보 가설 및 유압잭 프리로드 가압`,
            days: Math.round(totalStrutInstallDays),
            formula: `버팀보 ${numTiers}단 × 단당 가설 2.0~2.5일 = ${Math.round(totalStrutInstallDays)}일`,
            note: '띠장 브라켓 거치 + 강관 버팀보 거치 + 유압잭 가압 즉시 하부 굴착 (양생 대기 0일)',
            standardBasis: '표준품셈 3-2-2 가설 강재 거치 및 해체 품'
          }] : [])
        ]
      };

      // =========================================================================
      // Phase 3: 지하 RC 본체 구조물 축조 (바닥기초 ➡️ 층별 벽체/슬래브 ➡️ 지붕)
      // =========================================================================
      const maxPourArea = isAnchor ? 1000 : (isCompStrut ? 850 : (isHybrid ? 800 : 650));
      const numPourZones = Math.max(1, Math.ceil(floorAreaM2 / maxPourArea));
      const totalPourSegments = numStories * numPourZones;

      let blockOutCount = 0;
      let rebarRatio = 1.0;
      let formRatio = 1.0;
      let daysPerZoneRebar = 4.0;
      let daysPerZoneForm = 4.5;
      let daysPerZonePour = 4.0;
      let daysPerZonePost = 0.0;

      if (!isAnchor) {
        if (isCompStrut) {
          daysPerZoneRebar = 4.8;
          daysPerZoneForm = 5.2;
          daysPerZonePour = 4.5;
          daysPerZonePost = 3.0;
          rebarRatio = 0.85;
          formRatio = 0.80;
          blockOutCount = numTiers * Math.ceil(L / 5.0);
        } else if (isHybrid) {
          daysPerZoneRebar = 5.0;
          daysPerZoneForm = 5.5;
          daysPerZonePour = 4.5;
          daysPerZonePost = 2.5;
          rebarRatio = 0.82;
          formRatio = 0.78;
          blockOutCount = Math.floor(numTiers / 2) * Math.ceil(L / 3.5);
        } else {
          // ALL_STRUT
          daysPerZoneRebar = 6.0;
          daysPerZoneForm = 7.0;
          daysPerZonePour = 5.0;
          daysPerZonePost = 4.5;
          rebarRatio = 0.65;
          formRatio = 0.55;
          blockOutCount = numTiers * Math.ceil(L / 3.5);
        }
      }

      const overlapFactor = numPourZones > 1 ? 0.75 : 1.0;
      const crewFactor = numCrews > 1 ? (1.0 / (numCrews * 0.75)) : 1.0;

      const subRebarDays = Math.ceil(totalPourSegments * daysPerZoneRebar * overlapFactor * crewFactor);
      const subFormDays = Math.ceil(totalPourSegments * daysPerZoneForm * overlapFactor * crewFactor);
      const subPourDays = Math.ceil(numStories * (7.0 + (numPourZones - 1) * 3.0));
      const subPostDays = !isAnchor ? Math.ceil(totalPourSegments * daysPerZonePost * overlapFactor * crewFactor) : 0;

      const subColumnDays = Math.ceil(numStories * (numPourZones * 2.5)); // 층별/구획별 기둥 철근·거푸집·타설

      const phase3TotalDays = subRebarDays + subFormDays + subColumnDays + subPourDays + subPostDays;

      const phase3: SchedulePhaseResult = {
        name: `Phase 3. 지하 ${numStories}층 본체 RC 구조물 축조`,
        durationDays: phase3TotalDays,
        description: isAnchor
          ? `무지보 공간 대형 갱폼/동바리 조립 ➡️ 중앙 기둥 및 외벽·슬래브 배근 ➡️ 1회 전단 일괄 타설 (${numPourZones}구획 연속 시공)`
          : `버팀보 간섭 1단 하부벽체 타설 ➡️ ⚠️14MPa 양생 5일 대기 ➡️ 버팀보 해체 ➡️ 중앙 기둥 및 2단 상부벽체 타설 (${blockOutCount}개소 분할)`,
        subTasks: [
          {
            name: `동바리 및 벽체/슬래브 거푸집 조립 (층당 ${numPourZones}개 구획)`,
            days: subFormDays,
            formula: `총 ${totalPourSegments}구획 × ${daysPerZoneForm.toFixed(1)}일 × 오버랩 = ${subFormDays}일`,
            note: isAnchor ? '대형 갱폼/테이블폼 크레인 일체 인양 조립 (능률 100%)' : `버팀보 관통 박스아웃 및 분할 거푸집 현장 가공 (${blockOutCount}개소)`,
            standardBasis: '건축공사 표준시방서 KCS 41 30 05 거푸집공사'
          },
          {
            name: `외벽 및 슬래브 철근 가공 조립 및 배근 (층당 ${numPourZones}개 구획)`,
            days: subRebarDays,
            formula: `총 ${totalPourSegments}구획 × ${daysPerZoneRebar.toFixed(1)}일 × 오버랩 = ${subRebarDays}일`,
            note: isAnchor ? '방해물 없는 대구획 연속 배근' : `버팀보 파이프 사이 관통 꿰기 배근으로 작업능률 ${(rebarRatio * 100).toFixed(0)}% 감쇄`,
            standardBasis: '건축공사 표준시방서 KCS 41 30 00 철근공사'
          },
          {
            name: `중앙 RC 기둥(900×900) 축조 (토피 5m 뒷채움·교통하중 지지)`,
            days: subColumnDays,
            formula: `지하 ${numStories}개층 × ${numPourZones}구획 × 2.5일 = ${subColumnDays}일`,
            note: '상부 슬래브 자중, 상부 5m 되메우기 토압 및 도로교통하중(DB-24) 지지용 중앙 사각 RC 기둥 철근배근·기둥폼·타설',
            standardBasis: '콘크리트구조기준 KDS 14 20 50 기둥 설계'
          },
          {
            name: `콘크리트 타설 및 1차 양생 (바닥 기초 / 슬래브 / 외벽)`,
            days: subPourDays,
            formula: `지하 ${numStories}개층 × 타설 및 양생 = ${subPourDays}일`,
            note: isAnchor ? '층당 1회 일괄 타설 (Cold Joint 방지)' : '버팀보 하단까지만 1차 분할 타설',
            standardBasis: '콘크리트구조기준 KDS 14 20 00'
          },
          ...(!isAnchor ? [{
            name: `⚠️ 버팀보 14MPa 양생 확인 & 해체 후 2단 상부벽체 연결 타설`,
            days: subPostDays,
            formula: `총 ${totalPourSegments}구획 × 2차 분할/해체 ${daysPerZonePost.toFixed(1)}일 = ${subPostDays}일`,
            note: `1단 콘크리트 14MPa 강도 발현 5일 대기 후 버팀보 해체 ➡️ 외벽 상부 2단 연결 타설`,
            standardBasis: '지하 가설공사 표준시방서 KCS 21 30 00',
            bottleneckType: 'strut_curing_wait' as const
          }] : [])
        ]
      };

      // =========================================================================
      // Phase 4: 가시설 완전 해체 & 중간말뚝 인발 및 되메우기
      // =========================================================================
      let dismantleDays = 25;
      let dismantleCutDays = 15;
      let kingPostExtractDays = numKingPosts > 0 ? Math.ceil(numKingPosts / 6) : 0;
      let backfillDays = 10;

      if (isAnchor) {
        dismantleDays = 8;
        dismantleCutDays = 3;
        kingPostExtractDays = 0;
        backfillDays = 5;
      } else if (isCompStrut) {
        dismantleDays = 16;
        dismantleCutDays = 8;
        kingPostExtractDays = 0;
        backfillDays = 8;
      } else if (isHybrid) {
        dismantleDays = 19;
        dismantleCutDays = 10;
        kingPostExtractDays = numKingPosts > 0 ? 3 : 0;
        backfillDays = 9;
      }

      const phase4TotalDays = dismantleCutDays + kingPostExtractDays + backfillDays;

      const phase4: SchedulePhaseResult = {
        name: 'Phase 4. 가시설 해체, 중간말뚝 인발 & 되메우기',
        durationDays: phase4TotalDays,
        description: isAnchor
          ? '앵커 두부 1m 산소 절단 후 일괄 연속 되메우기 (최단 공기 8일)'
          : `최상단 가시설재 반출 + 중간말뚝 ${numKingPosts}본 인발 및 3중 무수축방수 마감(${kingPostExtractDays}일) + 되메우기`,
        subTasks: [
          {
            name: isAnchor ? '어스앵커 두부 절단 및 마감' : '최상단 지보재 절단 및 크레인 반출',
            days: dismantleCutDays,
            formula: isAnchor ? '앵커 헤드 산소 절단 = 3일' : `가설 강재 해체/반출 = ${dismantleCutDays}일`,
            note: isAnchor ? '두부 1m 깊이 산소 절단 후 마감' : '지하 구조물 보양 후 잔여 강재 크레인 인양',
            standardBasis: '표준품셈 3-2-2 가설재 해체 품'
          },
          ...(kingPostExtractDays > 0 ? [{
            name: `⚠️ 중간말뚝(King Post) 인발 및 슬래브 관통부 3중 무수축방수 마감`,
            days: kingPostExtractDays,
            formula: `중간말뚝 ${numKingPosts}본 ÷ 일일 6본 인발 = ${kingPostExtractDays}일`,
            note: '슬래브 관통 말뚝 산소 절단/인양 + 수웰링 실란트 및 무수축 몰탈 3중 방수 마감',
            standardBasis: '토목공사 표준시방서 관통부 누수 방지 시방',
            bottleneckType: 'kingpost_extraction' as const
          }] : []),
          {
            name: '토사 되메우기 및 층다짐',
            days: backfillDays,
            formula: `배후 공간 되메우기 층별 다짐 = ${backfillDays}일`,
            note: '수평 30cm 층다짐 밀도 95% 관리',
            standardBasis: '토목공사 표준시방서 되메우기 기준'
          }
        ]
      };

      const totalDurationDays = phase1TotalDays + totalEarthworkDays + phase3TotalDays + phase4TotalDays;
      const totalDurationMonths = Number((totalDurationDays / 30.0).toFixed(1));

      return {
        altId: alt.id,
        altName: alt.name,
        altType: alt.type,
        numStories,
        totalVolumeM3,
        wallPerimeterM: totalPerimeter,
        totalDurationDays,
        totalDurationMonths,
        savedDaysComparedToBaseline: 0,
        savedMonthsComparedToBaseline: 0,
        phases: {
          wallAndPiles: phase1,
          stepwiseExcavation: phase2,
          structure: phase3,
          dismantle: phase4
        },
        stepwiseCycles,
        blockOutJointCount: blockOutCount,
        rebarEfficiencyRatio: rebarRatio,
        formworkEfficiencyRatio: formRatio,
        timeDrivers: {
          wallPileDays: phase1TotalDays,
          earthworkDays: totalEarthworkDays,
          anchorGroutDelayDays: totalAnchorCuringDelayDays,
          structureDays: phase3TotalDays,
          strutSplitDelayDays: subPostDays,
          kingPostLossDays: kingPostInstallDays + kingPostExtractDays,
          dismantleDays: phase4TotalDays
        }
      };
    });

    // 1안(기준안) 대비 단축 일수 계산
    const baselineDays = results[0]?.totalDurationDays || 180;
    results.forEach(r => {
      r.savedDaysComparedToBaseline = Math.max(0, baselineDays - r.totalDurationDays);
      r.savedMonthsComparedToBaseline = Number((r.savedDaysComparedToBaseline / 30.0).toFixed(1));
    });

    return results;
  }
}

