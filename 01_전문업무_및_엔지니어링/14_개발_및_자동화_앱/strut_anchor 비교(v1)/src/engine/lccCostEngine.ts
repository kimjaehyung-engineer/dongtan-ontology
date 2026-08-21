import { AlternativeSpec, ProjectInputs } from '../types';
import { ConstructionScheduleEngine, AlternativeScheduleResult } from './constructionScheduleEngine';

export interface LccCostBreakdown {
  altId: number;
  altName: string;
  altType: string;
  directCostWon: number;               // 직접공사비 (도급/실행 가설+해체)
  durationDays: number;                // 전체 공기 (일수)
  durationMonths: number;              // 전체 공기 (개월)
  timeDependentIndirectCostWon: number;// 공기 비례 현장운영 간접비
  jointRemediationCostWon: number;     // 분할타설 조인트 방수보강비
  totalLccWon: number;                 // 총 LCC 공사비 (직접 + 간접 + 조인트)
  savedLccWonComparedToBaseline: number;
  rank: number;
  isLccRecommended: boolean;
  notes: string;
}

export interface LccAnalysisResult {
  monthlyIndirectCostWon: number;      // 월간 현장운영 고정간접비 (기본 4,500만원)
  jointUnitCostWon: number;            // 조인트 1개소당 방수처리비 (기본 80만원)
  scheduleResults: AlternativeScheduleResult[];
  lccBreakdowns: LccCostBreakdown[];
  bestLccAltId: number;
  bestLccAltName: string;
  keyInsights: string[];
}

export class LccCostEngine {
  public static DEFAULT_MONTHLY_INDIRECT_COST = 45000000; // 4,500만원 / 월
  public static DEFAULT_JOINT_UNIT_COST = 800000;          // 80만원 / 개소

  public static calculateLcc(
    inputs: ProjectInputs,
    alternatives: AlternativeSpec[],
    monthlyIndirect: number = LccCostEngine.DEFAULT_MONTHLY_INDIRECT_COST,
    jointUnitCost: number = LccCostEngine.DEFAULT_JOINT_UNIT_COST,
    numCrews: number = 1
  ): LccAnalysisResult {
    const schedules = ConstructionScheduleEngine.calculateSchedules(inputs, alternatives, numCrews);

    const breakdowns: LccCostBreakdown[] = alternatives.map((alt) => {
      const sch = schedules.find(s => s.altId === alt.id) || schedules[0];
      const directCostWon = alt.totalCostWon;

      // 공기 비례 간접비 = 공기(개월) x 월 현장관리비
      const timeDependentIndirectCostWon = Math.round(sch.totalDurationMonths * monthlyIndirect);

      // 분할타설 조인트 방수비 = 조인트 개소수 x 단가
      const jointRemediationCostWon = sch.blockOutJointCount * jointUnitCost;

      // 총 LCC
      const totalLccWon = directCostWon + timeDependentIndirectCostWon + jointRemediationCostWon;

      return {
        altId: alt.id,
        altName: alt.name,
        altType: alt.type,
        directCostWon,
        durationDays: sch.totalDurationDays,
        durationMonths: sch.totalDurationMonths,
        timeDependentIndirectCostWon,
        jointRemediationCostWon,
        totalLccWon,
        savedLccWonComparedToBaseline: 0,
        rank: 1,
        isLccRecommended: false,
        notes: alt.type === 'ALL_ANCHOR'
          ? '무지보 시공으로 조인트 방수비 0원 및 공기 대폭 단축'
          : alt.type === 'ALL_STRUT'
          ? '직접비는 가장 저렴하나 분할타설 및 공기 지연으로 간접비 발생'
          : '공기와 직접비의 균형 잡힌 절충안'
      };
    });

    // 1안(기준안) 대비 절감액 산출
    const baselineLcc = breakdowns[0]?.totalLccWon || 1;
    breakdowns.forEach(b => {
      b.savedLccWonComparedToBaseline = baselineLcc - b.totalLccWon;
    });

    // LCC 순위 정렬
    const sorted = [...breakdowns].sort((a, b) => a.totalLccWon - b.totalLccWon);
    sorted.forEach((item, idx) => {
      const target = breakdowns.find(b => b.altId === item.altId);
      if (target) {
        target.rank = idx + 1;
        if (idx === 0) target.isLccRecommended = true;
      }
    });

    const bestAlt = sorted[0];

    // 주요 공학적/경제적 인사이트
    const keyInsights: string[] = [
      `1안(버팀보)은 직접공사비가 ${(breakdowns[0].directCostWon / 1e8).toFixed(1)}억원으로 가장 저렴하지만, 버팀보 관통에 따른 분할타설 및 해체로 총 공기 ${breakdowns[0].durationDays}일(간접비 ${(breakdowns[0].timeDependentIndirectCostWon / 1e8).toFixed(2)}억원)이 소요됩니다.`,
      `2안(어스앵커)은 토공 단계에서 정착장 그라우트 양생(20일)이 소요되나, 본구조물 일체 연속타설(36일 단축) 및 해체 단순화(17일 단축)로 총 공기 ${breakdowns[1].durationDays}일(50일 단축)을 달성합니다.`,
      `종합 LCC 관점에서는 ${bestAlt.altName}이(가) 총 ${(bestAlt.totalLccWon / 1e8).toFixed(1)}억원으로 가장 경제적인 최적 대안으로 판정되었습니다.`
    ];

    return {
      monthlyIndirectCostWon: monthlyIndirect,
      jointUnitCostWon: jointUnitCost,
      scheduleResults: schedules,
      lccBreakdowns: breakdowns,
      bestLccAltId: bestAlt.altId,
      bestLccAltName: bestAlt.altName,
      keyInsights
    };
  }
}
