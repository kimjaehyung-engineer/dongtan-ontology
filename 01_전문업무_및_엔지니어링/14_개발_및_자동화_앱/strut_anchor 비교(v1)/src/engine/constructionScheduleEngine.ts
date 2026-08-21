import { ProjectInputs, AlternativeSpec } from '../types';

export interface SchedulePhaseResult {
  name: string;
  durationDays: number;
  description: string;
  subTasks: { name: string; days: number; note: string }[];
}

export interface AlternativeScheduleResult {
  altId: number;
  altName: string;
  altType: string;
  numStories: number;
  totalVolumeM3: number;
  totalDurationDays: number;
  totalDurationMonths: number;
  savedDaysComparedToBaseline: number;
  savedMonthsComparedToBaseline: number;
  phases: {
    earthwork: SchedulePhaseResult;
    structure: SchedulePhaseResult;
    dismantle: SchedulePhaseResult;
  };
  blockOutJointCount: number;
  rebarEfficiencyRatio: number;
  formworkEfficiencyRatio: number;
}

export class ConstructionScheduleEngine {
  /**
   * 굴착 제원 및 가시설 지보 조건에 따른 4대안 공정 일정(Schedule) 정밀 산출
   * @param inputs 프로젝트 공통 입력 제원
   * @param alternatives 4대안 스펙 목록
   * @param numCrews 투입 작업팀 수 (기본 1팀)
   */
  public static calculateSchedules(
    inputs: ProjectInputs,
    alternatives: AlternativeSpec[],
    numCrews: number = 1
  ): AlternativeScheduleResult[] {
    const H = inputs.excavationDepth;
    const B = inputs.excavationWidth;
    const L = inputs.totalWallPerimeter / 2.0; // 평면 종방향 길이 (약 100m)
    const totalVolumeM3 = Math.round(L * B * H); // 총 토공 굴착량 (m3)

    // 1. 굴착 깊이 연동 표준 지하 층수 (1~4안 전 대안 100% 동일)
    let numStories = 3;
    if (H <= 5.0) numStories = 1;
    else if (H <= 9.0) numStories = 2;
    else if (H <= 13.0) numStories = 3;
    else if (H <= 17.0) numStories = 4;
    else numStories = 5;

    // 4대안별 공기 산출
    const results: AlternativeScheduleResult[] = alternatives.map((alt) => {
      const isAnchor = alt.type === 'ALL_ANCHOR';
      const isHybrid = alt.type === 'HYBRID';
      const isOptimized = alt.type === 'OPTIMIZED';
      const numTiers = alt.supports.length;

      // -------------------------------------------------------------
      // 1단계: 토공 굴착, 지보재 가설 및 [앵커 그라우트 양생 대기기간]
      // -------------------------------------------------------------
      let dailyExcavationRate = 450; // m3/day (버팀보 간섭 2개소 수직양중 기준)
      let anchorGroutCuringDays = 0;
      let strutInstallDays = 0;
      let blockOutCount = 0;

      if (isAnchor) {
        dailyExcavationRate = 650; // 무지보 2개소 수직양중 고속 상차
        anchorGroutCuringDays = numTiers * 5; // 4단 x 5일 = 20일 정착장 양생 대기
        blockOutCount = 0;
      } else if (isHybrid) {
        dailyExcavationRate = 560;
        anchorGroutCuringDays = Math.ceil(numTiers / 2) * 5; // 상부 2단 x 5일 = 10일
        strutInstallDays = Math.floor(numTiers / 2) * 2.5;
        blockOutCount = Math.floor(numTiers / 2) * Math.ceil(L / 3.5);
      } else if (isOptimized) {
        dailyExcavationRate = 520;
        anchorGroutCuringDays = 5; // 상부 1단만 앵커
        strutInstallDays = (numTiers - 1) * 2.5;
        blockOutCount = (numTiers - 1) * Math.ceil(L / 4.5);
      } else {
        // ALL_STRUT
        dailyExcavationRate = 450;
        anchorGroutCuringDays = 0; // 버팀보 가압 즉시 굴착
        strutInstallDays = numTiers * 2.5; // 4단 x 2.5일 = 10일
        blockOutCount = numTiers * Math.ceil(L / 3.5);
      }

      const pureExcavationDays = Math.ceil(totalVolumeM3 / dailyExcavationRate);
      const earthworkTotalDays = pureExcavationDays + anchorGroutCuringDays + Math.round(strutInstallDays);

      const earthworkPhase: SchedulePhaseResult = {
        name: '토공 굴착 & 가시설 지보',
        durationDays: earthworkTotalDays,
        description: isAnchor 
          ? `무지보 2개 반출구 고속 양중(${dailyExcavationRate}㎥/일) + 앵커 정착장 양생대기(${anchorGroutCuringDays}일)`
          : `버팀보 간섭 2개 반출구 양중(${dailyExcavationRate}㎥/일) + 버팀보 가설(${Math.round(strutInstallDays)}일)`,
        subTasks: [
          { name: '토공 굴착 및 수직 양중 반출', days: pureExcavationDays, note: `2개소 개구부 Clamshell/백호 양중 (${dailyExcavationRate}㎥/일)` },
          ...(anchorGroutCuringDays > 0 ? [{ name: '어스앵커 천공/주입 및 정착장 양생대기', days: anchorGroutCuringDays, note: `단당 5일 압축강도 발현 대기 (${anchorGroutCuringDays}일)` }] : []),
          ...(strutInstallDays > 0 ? [{ name: '강관 버팀보 가설 및 프리로드 가압', days: Math.round(strutInstallDays), note: `단당 2.5일 소요, 양생대기 0일` }] : [])
        ]
      };

      // -------------------------------------------------------------
      // 2단계: 지하 RC 본구조물 축조 (단일 작업반 1개 팀 기준)
      // -------------------------------------------------------------
      let daysPerStory = 28; // All-Strut 기본 (철근 7일 + 거푸집 8일 + 1차타설/양생 7일 + 해체/채움 6일)
      let rebarRatio = 0.65;
      let formRatio = 0.55;

      if (isAnchor) {
        daysPerStory = 16; // 무지보 일체타설 (철근 4.5일 + 대형시스템폼 4.5일 + 일체타설/양생 7일)
        rebarRatio = 1.0;
        formRatio = 1.0;
      } else if (isHybrid) {
        daysPerStory = 21;
        rebarRatio = 0.82;
        formRatio = 0.78;
      } else if (isOptimized) {
        daysPerStory = 24;
        rebarRatio = 0.75;
        formRatio = 0.70;
      }

      // 복수 작업팀 투입 시 공기 단축 계수
      const crewFactor = numCrews > 1 ? (1.0 / (numCrews * 0.75)) : 1.0;
      const structureTotalDays = Math.ceil(numStories * daysPerStory * crewFactor);

      const structurePhase: SchedulePhaseResult = {
        name: `지하 ${numStories}층 RC 본구조물 축조`,
        durationDays: structureTotalDays,
        description: isAnchor
          ? `대형 시스템 폼 1회 일체 연속 타설 (분할타설 0회 / 관통부 누수 리스크 제로)`
          : `버팀보 관통 벽체 분할 타설 (총 ${blockOutCount}개소 블록아웃 및 2차 채움 타설)`,
        subTasks: [
          { name: `철근 가공조립 (1개 팀)`, days: Math.round(numStories * (isAnchor ? 4.5 : 7.0) * crewFactor), note: isAnchor ? '장애물 없는 연속 배근' : '버팀보 사이 꿰기 배근' },
          { name: `거푸집 및 블록아웃 설치`, days: Math.round(numStories * (isAnchor ? 4.5 : 8.0) * crewFactor), note: isAnchor ? '대형 시스템폼 일체 시공' : '관통부 맞춤 박스아웃 및 지수판 가공' },
          { name: `콘크리트 타설 및 양생`, days: Math.round(numStories * 7.0), note: '설계기준강도 발현 양생' },
          ...(!isAnchor ? [{ name: `버팀보 철거 및 2차 채움 타설`, days: Math.round(numStories * (isHybrid ? 3.0 : 6.0) * crewFactor), note: '무수축 그라우트 채움 및 콜드조인트 방수' }] : [])
        ]
      };

      // -------------------------------------------------------------
      // 3단계: 가시설 해체 및 되메우기
      // -------------------------------------------------------------
      let dismantleDays = 25;
      if (isAnchor) dismantleDays = 8; // 앵커 두부 절단 후 즉시 일괄 되메우기
      else if (isHybrid) dismantleDays = 19;
      else if (isOptimized) dismantleDays = 24;

      const dismantlePhase: SchedulePhaseResult = {
        name: '가시설 해체 & 되메우기',
        durationDays: dismantleDays,
        description: isAnchor
          ? '앵커 두부/지압판 단순 절단 후 일괄 연속 되메우기 (공기 최단)'
          : '구조물 층별 강도 발현 후 버팀보 순차 절단/인양 + 래커 이설 + 단계별 되메우기',
        subTasks: [
          { name: isAnchor ? '어스앵커 두부 절단 및 정리' : '강관 버팀보 순차 절단 및 크레인 양중', days: isAnchor ? 3 : 15, note: isAnchor ? '산소절단 3일' : '층별 순차 해체/인양' },
          { name: '토사 되메우기 및 다짐', days: isAnchor ? 5 : 10, note: '수평 층다짐 밀도 95% 관리' }
        ]
      };

      const totalDurationDays = earthworkTotalDays + structureTotalDays + dismantleDays;
      const totalDurationMonths = Number((totalDurationDays / 30.0).toFixed(1));

      return {
        altId: alt.id,
        altName: alt.name,
        altType: alt.type,
        numStories,
        totalVolumeM3,
        totalDurationDays,
        totalDurationMonths,
        savedDaysComparedToBaseline: 0,
        savedMonthsComparedToBaseline: 0,
        phases: {
          earthwork: earthworkPhase,
          structure: structurePhase,
          dismantle: dismantlePhase
        },
        blockOutJointCount: blockOutCount,
        rebarEfficiencyRatio: rebarRatio,
        formworkEfficiencyRatio: formRatio
      };
    });

    // 1안(기준안) 대비 단축 일수 계산
    const baselineDays = results[0]?.totalDurationDays || 167;
    results.forEach(r => {
      r.savedDaysComparedToBaseline = Math.max(0, baselineDays - r.totalDurationDays);
      r.savedMonthsComparedToBaseline = Number((r.savedDaysComparedToBaseline / 30.0).toFixed(1));
    });

    return results;
  }
}
