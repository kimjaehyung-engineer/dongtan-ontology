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
    const floorAreaM2 = Math.round(L * B); // 층당 바닥 슬래브 면적 (m2)
    const totalVolumeM3 = Math.round(floorAreaM2 * H); // 총 토공 굴착량 (m3)

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
      // 2단계: 지하 RC 본구조물 축조 (총 가시설 연장 및 바닥면적별 슬래브 분할 타설 구획 반영)
      // -------------------------------------------------------------
      // 1회 최대 타설 가능 면적: 어스앵커 무지보 1,000㎡/구획 vs 버팀보 간섭 650㎡/구획
      const maxPourAreaPerZone = isAnchor ? 1000 : (isHybrid ? 800 : 650);
      const numPourZonesPerFloor = Math.max(1, Math.ceil(floorAreaM2 / maxPourAreaPerZone));
      const totalPourSegments = numStories * numPourZonesPerFloor;

      let daysPerZoneRebar = 4.0; // 구획당 철근
      let daysPerZoneForm = 4.5;  // 구획당 거푸집
      let daysPerZonePour = 4.0;  // 구획당 타설 및 초기양생
      let daysPerZonePost = 0.0;

      let rebarRatio = 1.0;
      let formRatio = 1.0;

      if (!isAnchor) {
        if (isHybrid) {
          daysPerZoneRebar = 5.0;
          daysPerZoneForm = 5.5;
          daysPerZonePour = 4.5;
          daysPerZonePost = 2.5;
          rebarRatio = 0.82;
          formRatio = 0.78;
        } else {
          // ALL_STRUT
          daysPerZoneRebar = 6.0;
          daysPerZoneForm = 7.0;
          daysPerZonePour = 5.0;
          daysPerZonePost = 4.5;
          rebarRatio = 0.65;
          formRatio = 0.55;
        }
      }

      // 구획간 순환 병행 시공 계수 (오버랩 계수 0.75 적용)
      const overlapFactor = numPourZonesPerFloor > 1 ? 0.75 : 1.0;
      const crewFactor = numCrews > 1 ? (1.0 / (numCrews * 0.75)) : 1.0;

      const subRebarDays = Math.ceil(totalPourSegments * daysPerZoneRebar * overlapFactor * crewFactor);
      const subFormDays = Math.ceil(totalPourSegments * daysPerZoneForm * overlapFactor * crewFactor);
      const subPourDays = Math.ceil(numStories * (7.0 + (numPourZonesPerFloor - 1) * 3.0)); // 층당 콘크리트 양생 및 구획 릴레이
      const subPostDays = !isAnchor ? Math.ceil(totalPourSegments * daysPerZonePost * overlapFactor * crewFactor) : 0;

      const structureTotalDays = subRebarDays + subFormDays + subPourDays + subPostDays;

      const structurePhase: SchedulePhaseResult = {
        name: `지하 ${numStories}층 RC 본구조물 축조 (층당 ${numPourZonesPerFloor}구획 분할)`,
        durationDays: structureTotalDays,
        description: isAnchor
          ? `가시설 연장 L=${L.toFixed(0)}m(바닥 ${floorAreaM2.toLocaleString()}㎡) → 층당 ${numPourZonesPerFloor}개 대구획 연속타설 (관통부 누수 0개소)`
          : `가시설 연장 L=${L.toFixed(0)}m(바닥 ${floorAreaM2.toLocaleString()}㎡) → 층당 ${numPourZonesPerFloor}개 구획 분할타설 (총 ${blockOutCount}개소 관통 박스아웃 발생)`,
        subTasks: [
          { 
            name: `철근 가공조립 (층당 ${numPourZonesPerFloor}개 구획)`, 
            days: subRebarDays, 
            formula: `총 ${totalPourSegments}개 구획(5층×${numPourZonesPerFloor}구획) × 구획당 ${daysPerZoneRebar.toFixed(1)}일 × 오버랩(${overlapFactor}) = ${subRebarDays}일`,
            note: isAnchor ? '장애물 없는 대구획 연속 배근 (작업능률 100%)' : `버팀보 파이프 사이 관통 꿰기 배근으로 작업능률 ${(rebarRatio * 100).toFixed(0)}% 저하`,
            standardBasis: '건축공사 표준시방서 KCS 41 30 00 철근공사 품셈'
          },
          { 
            name: `거푸집 및 블록아웃 설치`, 
            days: subFormDays, 
            formula: `총 ${totalPourSegments}개 구획 × 구획당 ${daysPerZoneForm.toFixed(1)}일 × 오버랩(${overlapFactor}) = ${subFormDays}일`,
            note: isAnchor ? '대형 시스템폼(갱폼) 크레인 일체 인양 조립' : `버팀보 관통부 개별 박스아웃, 지수판 매립, 분할 거푸집 현장 가공 (${blockOutCount}개소)`,
            standardBasis: '건축공사 표준시방서 KCS 41 30 05 거푸집공사'
          },
          { 
            name: `슬래브 분할 콘크리트 타설 및 양생`, 
            days: subPourDays, 
            formula: `지하 ${numStories}개층 × [기본양생 7일 + 구획릴레이 ${(numPourZonesPerFloor - 1) * 3}일] = ${subPourDays}일`,
            note: `층당 ${numPourZonesPerFloor}회 분할 타설 (1회 레미콘 800~1,000㎥ 공급 한계 및 시공이음 콜드조인트 방지)`,
            standardBasis: '콘크리트구조기준 KDS 14 20 00 슬래브 시공이음(Joint) 및 양생 기준'
          },
          ...(!isAnchor ? [{ 
            name: `버팀보 철거 및 관통부 2차 채움타설`, 
            days: subPostDays, 
            formula: `총 ${totalPourSegments}개 구획 × 구획당 ${daysPerZonePost.toFixed(1)}일 × 오버랩(${overlapFactor}) = ${subPostDays}일`,
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
