import { ProjectInputs, AlternativeSpec } from '../types';

export interface SchedulePhaseResult {
  name: string;
  durationDays: number;
  description: string;
  subTasks: { 
    name: string; 
    days: number; 
    formula: string;
    note: string; 
    standardBasis: string;
  }[];
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

    // 1. 굴착 깊이 연동 표준 지하 층수 (전 대안 동일)
    let numStories = 3;
    if (H <= 5.0) numStories = 1;
    else if (H <= 9.0) numStories = 2;
    else if (H <= 13.0) numStories = 3;
    else if (H <= 17.0) numStories = 4;
    else numStories = 5;

    // 대안별 공기 산출
    const results: AlternativeScheduleResult[] = alternatives.map((alt) => {
      const isAnchor = alt.type === 'ALL_ANCHOR';
      const isHybrid = alt.type === 'HYBRID';
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
        anchorGroutCuringDays = numTiers * 5; // 단수 x 5일 정착장 조강 양생 대기
        blockOutCount = 0;
      } else if (isHybrid) {
        dailyExcavationRate = 560;
        anchorGroutCuringDays = Math.ceil(numTiers / 2) * 5; // 상부 앵커단 x 5일
        strutInstallDays = Math.floor(numTiers / 2) * 2.5;
        blockOutCount = Math.floor(numTiers / 2) * Math.ceil(L / 3.5);
      } else {
        // ALL_STRUT
        dailyExcavationRate = 450;
        anchorGroutCuringDays = 0; // 버팀보 가압 즉시 굴착
        strutInstallDays = numTiers * 2.5; // 단수 x 2.5일
        blockOutCount = numTiers * Math.ceil(L / 3.5);
      }

      const pureExcavationDays = Math.ceil(totalVolumeM3 / dailyExcavationRate);
      const earthworkTotalDays = pureExcavationDays + anchorGroutCuringDays + Math.round(strutInstallDays);

      const earthworkPhase: SchedulePhaseResult = {
        name: '토공 굴착 & 가시설 지보 가설',
        durationDays: earthworkTotalDays,
        description: isAnchor 
          ? `무지보 2개 반출구 고속 양중(${dailyExcavationRate}㎥/일) + 앵커 정착장 조강 양생대기(${anchorGroutCuringDays}일)`
          : `버팀보 간섭 2개 반출구 양중(${dailyExcavationRate}㎥/일) + 강관 버팀보 단별 가설(${Math.round(strutInstallDays)}일)`,
        subTasks: [
          { 
            name: '토공 굴착 및 수직 양중 반출', 
            days: pureExcavationDays, 
            formula: `총 토공량 ${totalVolumeM3.toLocaleString()}㎥ ÷ 일일 양중량 ${dailyExcavationRate}㎥/일 = ${pureExcavationDays}일`,
            note: isAnchor ? '장애물 없는 오픈 Clamshell 0.8㎥ x 2개소 연속 양중' : '버팀보 격자 간섭으로 선회 반경 및 양중 속도 31% 감쇄',
            standardBasis: '표준품셈 3-1-2 굴착기계 토사 수직 양중 기준'
          },
          ...(anchorGroutCuringDays > 0 ? [{ 
            name: '어스앵커 천공/주입 및 정착장 양생대기', 
            days: anchorGroutCuringDays, 
            formula: `앵커 ${Math.ceil(numTiers / (isHybrid ? 2 : 1))}개단 × 단당 조강 양생 5일 = ${anchorGroutCuringDays}일`,
            note: '정착장 그라우트 설계강도(14MPa) 발현 전 하부 굴착 금지 (도로교설계기준)',
            standardBasis: '국토교통부 지반공사 표준시방서 KCS 11 70 05 어스앵커공'
          }] : []),
          ...(strutInstallDays > 0 ? [{ 
            name: '강관 버팀보 가설 및 프리로드 가압', 
            days: Math.round(strutInstallDays), 
            formula: `버팀보 ${isHybrid ? Math.floor(numTiers / 2) : numTiers}개단 × 단당 가설 2.5일 = ${Math.round(strutInstallDays)}일`,
            note: '띠장 브라켓 용접 + 강관 거치 + 유압잭 프리로드 가압 (양생 대기 0일 즉시 굴착)',
            standardBasis: '표준품셈 3-2-2 가설 강재 거치 및 해체 품'
          }] : [])
        ]
      };

      // -------------------------------------------------------------
      // 2단계: 지하 RC 본구조물 축조 (단일 작업반 1개 팀 기준)
      // -------------------------------------------------------------
      let daysPerStory = 28; // All-Strut 기본 (철근 7일 + 거푸집 8일 + 타설양생 7일 + 해체채움 6일)
      let rebarDaysPerStory = 7.0;
      let formDaysPerStory = 8.0;
      let postPourDaysPerStory = 6.0;
      let rebarRatio = 0.65;
      let formRatio = 0.55;

      if (isAnchor) {
        daysPerStory = 16; // 무지보 일체타설 (철근 4.5일 + 대형시스템폼 4.5일 + 타설양생 7일)
        rebarDaysPerStory = 4.5;
        formDaysPerStory = 4.5;
        postPourDaysPerStory = 0.0;
        rebarRatio = 1.0;
        formRatio = 1.0;
      } else if (isHybrid) {
        daysPerStory = 21;
        rebarDaysPerStory = 5.5;
        formDaysPerStory = 6.0;
        postPourDaysPerStory = 3.0;
        rebarRatio = 0.82;
        formRatio = 0.78;
      }

      // 복수 작업팀 투입 시 공기 단축 계수
      const crewFactor = numCrews > 1 ? (1.0 / (numCrews * 0.75)) : 1.0;
      const structureTotalDays = Math.ceil(numStories * daysPerStory * crewFactor);

      const structurePhase: SchedulePhaseResult = {
        name: `지하 ${numStories}층 RC 본구조물 축조`,
        durationDays: structureTotalDays,
        description: isAnchor
          ? `대형 시스템 폼 1회 일체 연속 타설 (분할타설 0회 / 관통부 누수 리스크 제로)`
          : `버팀보 관통 벽체 분할 타설 (총 ${blockOutCount}개소 블록아웃 및 2차 채움 타설 발생)`,
        subTasks: [
          { 
            name: `철근 가공조립 (${numCrews}개 팀)`, 
            days: Math.round(numStories * rebarDaysPerStory * crewFactor), 
            formula: `지하 ${numStories}개층 × 층당 ${rebarDaysPerStory.toFixed(1)}일 ÷ 작업계수(${crewFactor.toFixed(2)}) = ${Math.round(numStories * rebarDaysPerStory * crewFactor)}일`,
            note: isAnchor ? '장애물 없는 대구획 연속 배근 (작업능률 100%)' : `버팀보 파이프 사이 관통 꿰기 배근으로 작업능률 ${(rebarRatio * 100).toFixed(0)}% 저하`,
            standardBasis: '건축공사 표준시방서 KCS 41 30 00 철근공사 품셈'
          },
          { 
            name: `거푸집 및 블록아웃 설치`, 
            days: Math.round(numStories * formDaysPerStory * crewFactor), 
            formula: `지하 ${numStories}개층 × 층당 ${formDaysPerStory.toFixed(1)}일 ÷ 작업계수(${crewFactor.toFixed(2)}) = ${Math.round(numStories * formDaysPerStory * crewFactor)}일`,
            note: isAnchor ? '대형 시스템폼(갱폼) 크레인 일체 인양 조립' : `버팀보 관통부 개별 박스아웃, 지수판 매립, 분할 거푸집 현장 가공 (${blockOutCount}개소)`,
            standardBasis: '건축공사 표준시방서 KCS 41 30 05 거푸집공사'
          },
          { 
            name: `콘크리트 타설 및 양생`, 
            days: Math.round(numStories * 7.0), 
            formula: `지하 ${numStories}개층 × 층당 양생 7.0일 = ${Math.round(numStories * 7.0)}일`,
            note: '슬래브/외벽 타설 후 설계기준강도(fck ≥ 14MPa) 발현 양생 필수 기간',
            standardBasis: '콘크리트구조기준 KDS 14 20 00 압축강도 발현 양생 기준'
          },
          ...(!isAnchor ? [{ 
            name: `버팀보 철거 및 관통부 2차 채움타설`, 
            days: Math.round(numStories * postPourDaysPerStory * crewFactor), 
            formula: `지하 ${numStories}개층 × 층당 ${postPourDaysPerStory.toFixed(1)}일 = ${Math.round(numStories * postPourDaysPerStory * crewFactor)}일`,
            note: '구조물 강도 확보 후 버팀보 순차 절단/인양 + 박스아웃 무수축 그라우트 2차 타설 & 방수',
            standardBasis: '지하 가설공사 시방서 관통부 조인트 사후 보수 시방'
          }] : [])
        ]
      };

      // -------------------------------------------------------------
      // 3단계: 가시설 해체 및 되메우기
      // -------------------------------------------------------------
      let dismantleDays = 25;
      let dismantleCutDays = 15;
      let backfillDays = 10;

      if (isAnchor) {
        dismantleDays = 8;
        dismantleCutDays = 3;
        backfillDays = 5;
      } else if (isHybrid) {
        dismantleDays = 19;
        dismantleCutDays = 10;
        backfillDays = 9;
      }

      const dismantlePhase: SchedulePhaseResult = {
        name: '가시설 해체 & 토사 되메우기',
        durationDays: dismantleDays,
        description: isAnchor
          ? '앵커 두부/지압판 단순 산소 절단 후 일괄 연속 되메우기 (최단 공기)'
          : '구조물 층별 강도 발현 후 버팀보 순차 절단/인양 + 래커 이설 + 단계별 되메우기',
        subTasks: [
          { 
            name: isAnchor ? '어스앵커 두부 절단 및 정리' : '강관 버팀보 순차 절단 및 크레인 양중', 
            days: dismantleCutDays, 
            formula: isAnchor ? `전체 ${numTiers}단 앵커 헤드 산소 절단 = 3일` : `버팀보 ${numTiers}단 층별 순차 절단/크레인 반출 = ${dismantleCutDays}일`,
            note: isAnchor ? '두부 1m 깊이 산소 절단 후 즉시 마감' : '지하 구조물 손상 방지 보양 후 버팀보 1본씩 크레인 인양',
            standardBasis: '표준품셈 3-2-2 가설재 해체 및 인양 품'
          },
          { 
            name: '토사 되메우기 및 층다짐', 
            days: backfillDays, 
            formula: `배후 공간 굴착토 되메우기 층별 다짐 = ${backfillDays}일`,
            note: '수평 30cm 층다짐 밀도 95% 관리 (도로 침하 방지)',
            standardBasis: '토목공사 표준시방서 되메우기 및 다짐 관리 기준'
          }
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
