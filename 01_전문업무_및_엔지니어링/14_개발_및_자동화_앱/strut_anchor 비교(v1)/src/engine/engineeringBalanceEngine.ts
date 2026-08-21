import { ProjectInputs, AlternativeSpec, SupportStage, WallSection } from '../types';
import { H_PILE_DATABASE, STRUT_DATABASE, WALE_DATABASE } from './sectionDB';
import { KingPostEngine } from './kingPostEngine';

export interface BalanceMetric {
  name: string;
  category: 'WALL' | 'STRUT' | 'KING_POST' | 'WALE' | 'EMBEDMENT';
  actualRatio: number;      // 실제 응력비 (0.0 ~ 1.5)
  idealMinRatio: number;    // 이상적 하한 (예: 0.60)
  idealMaxRatio: number;    // 이상적 상한 (예: 0.82)
  status: 'OPTIMAL' | 'OVERLOAD' | 'UNDERLOAD' | 'CRITICAL_NG';
  statusText: string;
  weight: number;
}

export interface EquilibriumDiagnosis {
  overallScore: number;     // 균형 종합 점수 (0 ~ 100점, 85점 이상이면 완벽한 균형)
  isHarmonized: boolean;    // 모든 부재가 골든존(0.60~0.85)에 진입했는지 여부
  metrics: BalanceMetric[];
  bottleneckMember: string; // 하중이 가장 집중된 편중 부재
  recommendations: string[];
  suggestedBalancedInputs: ProjectInputs; // 균형점이 맞춰진 추천 파라미터
}

export class EngineeringBalanceEngine {
  /**
   * 가시설 전체 구조계의 다목적 역학 균형도(Equilibrium Harmony) 진단 및 최적 균형점 탐색
   */
  public static diagnoseEquilibrium(
    inputs: ProjectInputs,
    alt: AlternativeSpec
  ): EquilibriumDiagnosis {
    const stageRes = alt.stageResults[alt.stageResults.length - 1];
    const wallStress = alt.pileStressRatio;
    const embedSF = alt.embedmentSF;
    
    // 버팀보 최대 응력비
    let maxStrutRatio = 0.65;
    const allSupportResults = alt.stageResults.flatMap(sr => sr.supports || []);
    if (allSupportResults.length > 0) {
      const strutResults = allSupportResults.filter(s => s.type === 'STRUT');
      if (strutResults.length > 0) {
        maxStrutRatio = Math.max(...strutResults.map(s => s.strutStressRatio || (s.axialForce / Math.max(1, s.allowableForce))));
      }
    }
    maxStrutRatio = Number(maxStrutRatio.toFixed(2));

    // 중간말뚝 좌굴 응력비
    const kpRes = KingPostEngine.evaluateKingPost(inputs, inputs.deckingConfig || {
      useDecking: true,
      trafficLoadType: 'KL-510',
      trafficLoadValue: 20.0,
      deckBeamSpec: 'H-400x400x13x21',
      deckBeamSpacing: 2.0,
      kingPostSpec: 'H-300x300x10x15',
      kingPostSpacing: 3.5,
      kingPostNumRows: 1,
      kingPostTotalLength: inputs.excavationDepth + 5.0
    }, inputs.soils);
    const kingPostRatio = kpRes.bucklingStressRatio;

    // 띠장 최대 응력비 (실제 FEM 해석 결과에서 envelope 추출)
    let waleRatio = 0.60;
    if (allSupportResults.length > 0) {
      const waleRatios = allSupportResults.map(s => s.waleStressRatio || 0).filter(r => r > 0);
      if (waleRatios.length > 0) {
        waleRatio = Math.max(...waleRatios);
      }
    }
    waleRatio = Number(waleRatio.toFixed(2));

    // 메트릭 판정
    const evaluateMetric = (
      name: string,
      category: 'WALL' | 'STRUT' | 'KING_POST' | 'WALE' | 'EMBEDMENT',
      val: number,
      min: number,
      max: number,
      weight: number
    ): BalanceMetric => {
      let status: 'OPTIMAL' | 'OVERLOAD' | 'UNDERLOAD' | 'CRITICAL_NG' = 'OPTIMAL';
      let statusText = '✓ 이상적 적정 하중 분담 (Golden Zone)';

      if (val > 1.0) {
        status = 'CRITICAL_NG';
        const overPct = Math.round((val - 1.0) * 100);
        statusText = `✕ 허용내력 초과 (${Math.round(val * 100)}%, +${overPct}% 초과 위험)`;
      } else if (val > max) {
        status = 'OVERLOAD';
        const excess = Math.round((val - max) * 100);
        statusText = `⚠ 하중 편중 과다 (+${excess}% 목표 초과)`;
      } else if (val < min) {
        status = 'UNDERLOAD';
        statusText = '○ 과다 안전설계 (비경제/자재 과잉)';
      }

      return {
        name,
        category,
        actualRatio: val,
        idealMinRatio: min,
        idealMaxRatio: max,
        status,
        statusText,
        weight
      };
    };

    const metrics: BalanceMetric[] = [
      evaluateMetric('엄지말뚝 벽체 휨응력', 'WALL', wallStress, 0.65, 0.85, 30),
      evaluateMetric('버팀보 축력 및 좌굴', 'STRUT', maxStrutRatio, 0.55, 0.80, 25),
      evaluateMetric('중간말뚝 좌굴 응력', 'KING_POST', kingPostRatio, 0.40, 0.75, 20),
      evaluateMetric('띠장(Wale) 휨응력', 'WALE', waleRatio, 0.60, 0.85, 15),
      evaluateMetric('지반 근입장 전도안전', 'EMBEDMENT', Number((1.5 / Math.max(0.5, embedSF)).toFixed(2)), 0.60, 0.85, 10),
    ];

    // 균형 점수 계산 (각 메트릭이 골든존에 가까울수록 100점에 수렴)
    let scoreSum = 0;
    metrics.forEach(m => {
      let metricScore = 100;
      if (m.status === 'OPTIMAL') {
        metricScore = 100;
      } else if (m.status === 'OVERLOAD') {
        metricScore = Math.max(40, 100 - (m.actualRatio - m.idealMaxRatio) * 200);
      } else if (m.status === 'UNDERLOAD') {
        metricScore = Math.max(60, 100 - (m.idealMinRatio - m.actualRatio) * 100);
      } else {
        metricScore = 20;
      }
      scoreSum += metricScore * (m.weight / 100);
    });

    const overallScore = Math.round(scoreSum);
    const isHarmonized = metrics.every(m => m.status === 'OPTIMAL');

    // 병목 및 추천 사항 도출
    const overloaded = metrics.filter(m => m.status === 'OVERLOAD' || m.status === 'CRITICAL_NG');
    const underloaded = metrics.filter(m => m.status === 'UNDERLOAD');

    let bottleneckMember = '모든 부재가 완벽한 황금 균형(Golden Balance)을 이루고 있습니다.';
    const recommendations: string[] = [];

    if (overloaded.length > 0) {
      bottleneckMember = `${overloaded.map(o => o.name).join(', ')} 에 하중이 편중되어 있습니다.`;
      if (overloaded.some(o => o.category === 'WALL')) {
        recommendations.push('엄지말뚝 간격을 1.8m로 유지하고 지보재 프리로드를 10~15% 상향하여 벽체 휨모멘트를 완화하세요.');
      }
      if (overloaded.some(o => o.category === 'STRUT')) {
        recommendations.push('버팀보 수평 간격을 3.5m로 조정하여 1본당 지배 하중을 분산시키고 좌굴 응력을 낮추세요.');
      }
      if (overloaded.some(o => o.category === 'KING_POST')) {
        recommendations.push('중간말뚝과의 강결 결합을 유지하며 중간말뚝 간격을 3.0~3.5m로 배치하세요.');
      }
    } else if (underloaded.length > 0) {
      bottleneckMember = `${underloaded.map(u => u.name).join(', ')} 이 다소 과다설계되어 있습니다.`;
      recommendations.push('부재 규격을 한 단계 슬림화하거나 간격을 소폭 확대하여 경제성을 추가 확보할 수 있습니다.');
    } else {
      recommendations.push('버팀보에 과도한 하중이 집중되지 않고, 중간말뚝 좌굴과 벽체 휨응력이 최적의 안전율(0.68~0.78)로 완벽히 균형을 이루고 있습니다.');
    }

    // 최적 균형 추천 파라미터 생성
    const balancedWall: WallSection = {
      ...inputs.wall,
      spacing: 1.8,
      hPileSpec: 'H-300x300x10x15',
      totalLength: inputs.excavationDepth + 5.0
    };

    const balancedSups: SupportStage[] = inputs.supports.map((s, idx) => {
      if (s.type === 'STRUT') {
        return {
          ...s,
          horizSpacing: 3.5,
          strutSpec: '강관 Φ508.0x9.0t',
          preload: Math.min(180, 100 + idx * 25), // 과도하지 않은 적정 프리로드
          waleSpec: '2-H 300x300x10x15'
        };
      } else if (s.type === 'GROUND_ANCHOR') {
        return {
          ...s,
          angle: 55, // 55° 고각 최적 균형
          horizSpacing: 2.0,
          preload: 140 + idx * 25,
          waleSpec: '2-H 300x300x10x15'
        };
      }
      return s;
    });

    const suggestedBalancedInputs: ProjectInputs = {
      ...inputs,
      wall: balancedWall,
      supports: balancedSups,
      deckingConfig: {
        ...(inputs.deckingConfig || {
          useDecking: true,
          trafficLoadType: 'KL-510',
          trafficLoadValue: 20.0,
          deckBeamSpec: 'H-400x400x13x21',
          deckBeamSpacing: 2.0,
          kingPostSpec: 'H-300x300x10x15',
          kingPostSpacing: 3.5,
          kingPostNumRows: 1,
          kingPostTotalLength: inputs.excavationDepth + 5.0
        }),
        kingPostSpacing: 3.5 // 강결 최적 간격
      }
    };

    return {
      overallScore,
      isHarmonized,
      metrics,
      bottleneckMember,
      recommendations,
      suggestedBalancedInputs
    };
  }
}
