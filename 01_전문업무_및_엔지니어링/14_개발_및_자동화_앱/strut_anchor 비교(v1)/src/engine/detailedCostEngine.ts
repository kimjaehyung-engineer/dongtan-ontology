import { ProjectInputs, AlternativeSpec, SupportStage, WallSection, CostItem } from '../types';
import { H_PILE_DATABASE, STRUT_DATABASE, WALE_DATABASE, DECK_BEAM_DATABASE } from './sectionDB';

export interface QuantityItem {
  id: string;
  category: 'WALL' | 'LAGGING' | 'WALE' | 'STRUT' | 'BRACING' | 'DECKING' | 'ANCHOR' | 'GENERAL';
  categoryName: string;
  itemCode: string;             // 내역코드 (ex: 2-1-2-1-10)
  name: string;
  spec: string;
  unit: string;
  formula: string;              // 산출 공식
  formulaDetail: string;        // 공식 세부 해설
  quantity: number;
  contractUnitCost: number;     // 도급단가 (원)
  executionUnitCost: number;    // 실행단가 (원)
  contractAmount: number;       // 도급금액 (원)
  executionAmount: number;      // 실행금액 (원)
  materialCost?: number;
  laborCost?: number;
  expenseCost?: number;
  costBasis: string;            // 단가산출 근거
}

export interface DetailedCostResult {
  altId: number;
  altName: string;
  rentalMonths: number;
  steelRentalRateMonthly: number;
  items: QuantityItem[];
  totalContractCost: number;
  totalExecutionCost: number;
  costSavings: number;
  executionRatio: number;
}

export class DetailedCostEngine {
  // 최신 표준품셈 & 물가정보지 기준 도급 및 실행 표준 단가 DB (가설 6개월 손료 기준, 내역서 2.1.2 세부 공종 매핑)
  public static readonly DEFAULT_UNIT_COSTS = {
    // 1. 말뚝박기용 천공 및 항타 (2-1-2-1)
    DRILL_SOIL: { contract: 42000, execution: 33600, mat: 4000, lab: 18000, exp: 20000, basis: '내역 2-1-2-1-10 / 품셈 3-2-1 오거크레인 천공(토사, D500)' },
    DRILL_ROCK: { contract: 68000, execution: 54400, mat: 6000, lab: 28000, exp: 34000, basis: '내역 2-1-2-1-10 / 품셈 3-2-1 T4 컴프레셔 천공(풍화암/연암)' },
    HOLE_BACKFILL: { contract: 11000, execution: 8800, mat: 3000, lab: 4000, exp: 4000, basis: '내역 2-1-2-1-20 / 천공홀 모래/토사 되메우기' },
    RIG_SETUP: { contract: 2500000, execution: 2000000, mat: 0, lab: 1200000, exp: 1300000, basis: '내역 2-1-2-1-30 / 오거크레인 장비 조립 및 해체 (회당)' },

    // 2. 강재사용료 및 소운반 (2-1-2-2, 2-1-2-3)
    H_PILE_RENTAL: { contract: 380000, execution: 304000, mat: 285000, lab: 45000, exp: 50000, basis: '내역 2-1-2-3-30 / 물가정보 H형강 6개월 임대손료(월 2.5% x 6 = 15%)' },
    STEEL_TRANSPORT: { contract: 12000, execution: 9600, mat: 0, lab: 5000, exp: 7000, basis: '내역 2-1-2-2-20 / 강재 현장 반입 및 소운반(설치/철거)' },

    // 3. H-Pile 가설, 이음, 두부정리 및 인발 (2-1-2-4)
    H_PILE_SPLICE: { contract: 480000, execution: 384000, mat: 120000, lab: 260000, exp: 100000, basis: '내역 2-1-2-4-10 / H-Pile 현장 맞댐용접 이음 및 비파괴검사' },
    H_PILE_HEAD_CUT: { contract: 35000, execution: 28000, mat: 5000, lab: 22000, exp: 8000, basis: '내역 2-1-2-4-30 / H-Pile 산소 절단 및 두부정리' },
    H_PILE_EXTRACT: { contract: 65000, execution: 52000, mat: 5000, lab: 32000, exp: 28000, basis: '내역 2-1-2-4-20 / 바이브로해머 엄지말뚝 인발' },
    EXTRACT_BACKFILL: { contract: 8500, execution: 6800, mat: 2500, lab: 3000, exp: 3000, basis: '내역 2-1-2-4-23 / 인발 후 홀 그라우팅/토사 채움' },

    // 4. 토류판 (목재, 강재, 숏크리트 2-1-2-9)
    LAGGING_INSTALL: { contract: 32000, execution: 25600, mat: 19200, lab: 9600, exp: 3200, basis: '내역 2-1-2-9-10 / 낙엽송 판재(t=8cm, 3회 유용손료) + 끼우기' },
    LAGGING_DISMANTLE: { contract: 12000, execution: 9600, mat: 0, lab: 9000, exp: 3000, basis: '내역 2-1-2-9-30 / 목재 토류판 해체 및 잔재 처리' },
    STEEL_LAGGING_INSTALL: { contract: 48000, execution: 38400, mat: 35000, lab: 8000, exp: 5000, basis: '내역 2-1-2-9-15 / 강재 토류판(t=6~8mm) 6개월 임대손료 + 끼우기 (㎡당)' },
    STEEL_LAGGING_DISMANTLE: { contract: 15000, execution: 12000, mat: 0, lab: 10000, exp: 5000, basis: '내역 2-1-2-9-35 / 강재 토류판 인양 해체 및 반출 (㎡당)' },
    SHOTCRETE_LAGGING: { contract: 55000, execution: 44000, mat: 30000, lab: 18000, exp: 7000, basis: '내역 2-1-2-9-20 / 숏크리트 타설(t=15cm) + 와이어메쉬 #8 부착 (㎡당)' },

    // 5. 띠장재 (2-1-2-6)
    WALE_RENTAL_INSTALL: { contract: 420000, execution: 336000, mat: 315000, lab: 55000, exp: 50000, basis: '내역 2-1-2-6-10 / 2-H 300x300 손료(6개월) + 띠장 가설' },
    WALE_SPLICE_CORNER: { contract: 185000, execution: 148000, mat: 45000, lab: 95000, exp: 45000, basis: '내역 2-1-2-6-20,30 / 띠장 조인트 연결 및 우각부 코너보강' },
    BEAM_HANGER: { contract: 25000, execution: 20000, mat: 8000, lab: 12000, exp: 5000, basis: '내역 2-1-2-6-40 / 띠장 받침 앵글/철근 보걸이 설치 및 용접' },
    WALE_DISMANTLE: { contract: 35000, execution: 28000, mat: 0, lab: 22000, exp: 13000, basis: '내역 2-1-2-6-12 / 띠장재 해체 및 인양' },

    // 6. 버팀보 (Strut, 2-1-2-7)
    STRUT_RENTAL_INSTALL: { contract: 450000, execution: 360000, mat: 337500, lab: 62500, exp: 50000, basis: '내역 2-1-2-7-10 / 강관 Φ508x9t 6개월 손료 + 버팀보 가설' },
    // 합성사각강관: 고강도 특허 자재 손료 + 모듈러 무중간말뚝 볼트 가설비 반영 (톤당 1,200,000원)
    COMPOSITE_STRUT_RENTAL_INSTALL: { contract: 1200000, execution: 960000, mat: 900000, lab: 180000, exp: 120000, basis: '신기술/특허 4-Box 합성사각강관 6개월 손료 + 모듈러 볼트 가설' },
    SCREW_JACK: { contract: 120000, execution: 96000, mat: 75000, lab: 30000, exp: 15000, basis: '내역 2-1-2-7-40 / 1000kN 스크류잭 설치 및 프리로드 유압재하' },
    COMPOSITE_STRUT_JACK: { contract: 380000, execution: 304000, mat: 250000, lab: 80000, exp: 50000, basis: '합성사각강관 전용 2000kN 고용량 유압 프리로드잭 & 단부 접합 브래킷' },
    WEDGE_BLOCK: { contract: 95000, execution: 76000, mat: 45000, lab: 35000, exp: 15000, basis: '내역 2-1-2-7-30 / 화타쐐기(K-1 Type) 제작 및 밀착설치' },
    STRUT_DISMANTLE: { contract: 45000, execution: 36000, mat: 0, lab: 28000, exp: 17000, basis: '내역 2-1-2-7-15 / 강관 버팀보 해체 및 인양 반출' },
    COMPOSITE_STRUT_DISMANTLE: { contract: 85000, execution: 68000, mat: 0, lab: 55000, exp: 30000, basis: '합성사각강관 볼트 분해 및 크레인 인양' },

    // 7. 보강재 및 중간말뚝 (2-1-2-8)
    BRACING_STEEL: { contract: 380000, execution: 304000, mat: 285000, lab: 50000, exp: 45000, basis: '내역 2-1-2-8-10,20 / ㄷ-형강 및 L-형강 수평/수직 가새 보강재 손료/설치' },
    KING_POST_SOCKET_DRILL: { contract: 75000, execution: 60000, mat: 8000, lab: 35000, exp: 32000, basis: '내역 2-1-2-8-60 / 중간말뚝 암반소켓 천공 및 크레인 거치' },
    KING_POST_RENTAL: { contract: 380000, execution: 304000, mat: 285000, lab: 45000, exp: 50000, basis: '내역 2-1-2-8-60 / H-300 중간말뚝 강재사용료(6개월)' },
    KING_POST_RIGID_JOINT: { contract: 165000, execution: 132000, mat: 65000, lab: 75000, exp: 25000, basis: '내역 2-1-2-8-50 / 중간말뚝-스트럿 완전 강결 거셋브라켓 및 스티프너' },
    KING_POST_WATERPROOF: { contract: 85000, execution: 68000, mat: 35000, lab: 38000, exp: 12000, basis: '내역 2-1-2-8-65 / 중간말뚝 바닥 슬래브 관통부 지수판 방수처리' },

    // 8. 복공판 및 주형보 (2-1-2-5)
    DECK_PLATE: { contract: 65000, execution: 52000, mat: 45000, lab: 12000, exp: 8000, basis: '내역 2-1-2-5-70 / 무늬강판 복공판(2000x1000x200) 6개월 임대손료 및 설치' },
    DECK_BEAM_RENTAL: { contract: 450000, execution: 360000, mat: 337500, lab: 62500, exp: 50000, basis: '내역 2-1-2-5-10 / H-400 주형보 6개월 손료 + 거치' },
    DECK_BRACING: { contract: 165000, execution: 132000, mat: 55000, lab: 80000, exp: 30000, basis: '내역 2-1-2-5-30,60 / 주형보 브레이싱(X-1) 및 피스브라켓 제작설치' },

    // 9. 어스앵커 (2-1-2-10)
    ANCHOR_DRILL_GROUT: { contract: 48000, execution: 38400, mat: 15000, lab: 18000, exp: 15000, basis: '내역 2-1-2-10-10,40 / 앵커천공(D135) + 시멘트 가압 그라우팅 (m당)' },
    ANCHOR_STRAND_INSTALL: { contract: 18000, execution: 14400, mat: 11000, lab: 5000, exp: 2000, basis: '내역 2-1-2-10-30 / SWPC 7B 12.7mm 강연선 가공조립 및 삽입 (m당)' },
    ANCHOR_TENSION_TEST: { contract: 65000, execution: 52000, mat: 8000, lab: 38000, exp: 19000, basis: '내역 2-1-2-10-50 / 유압잭 인장시험, PC콘 조립 및 락오프 정착 (공당)' },
    ANCHOR_BASE_PLATE: { contract: 120000, execution: 96000, mat: 65000, lab: 35000, exp: 20000, basis: '내역 2-1-2-10-60 / 일반앵커 지압판(Base Plate) 제작 및 설치 (공당)' },
    HIGH_ANGLE_SPECIAL_BRACKET: { contract: 380000, execution: 304000, mat: 260000, lab: 80000, exp: 40000, basis: '고각(45°~70°) 특수 경사 지압 브래킷 6개월 임대손료 & 띠장 거셋 보강 (공당 38만원)' },
    ANCHOR_STRAND_REMOVE: { contract: 25000, execution: 20000, mat: 0, lab: 18000, exp: 7000, basis: '내역 2-1-2-10-80 / 제거식 어스앵커 강선 인발 및 제거 (공당)' },
    ANCHOR_RIG_SETUP: { contract: 1800000, execution: 1440000, mat: 0, lab: 900000, exp: 900000, basis: '내역 2-1-2-10-90 / 크롤러 드릴 천공장비 조립 및 해체 (회당)' }
  };

  /**
   * 프로젝트 입력 및 4대안에 따른 실제 내역서 2.1.2 세부 공종 전체 목록(QTO) 자동 산출
   * 
   * [기하학적 수량 산출 기준 일원화]
   * - L_wall = inputs.totalWallPerimeter (양측 벽체 전체 둘레 연장, m)
   * - L_long = inputs.totalWallPerimeter / 2.0 (종방향 굴착 연장, m)
   * - B = inputs.excavationWidth (횡방향 굴착폭, m)
   * - H = inputs.excavationDepth (굴착 심도, m)
   */
  public static calculateDetailedCost(
    alt: AlternativeSpec,
    inputs: ProjectInputs,
    rentalMonths: number = 6,
    customUnitCosts?: Record<string, { contract: number; execution: number }>
  ): DetailedCostResult {
    const H = inputs.excavationDepth;
    const B = inputs.excavationWidth;
    const L_wall = inputs.totalWallPerimeter; // 총 벽체 둘레 연장 (기본 100m)
    const L_long = L_wall / 2.0;              // 종방향 굴착 연장 (기본 50m)
    const wall = alt.wall;
    const totalLength = wall.totalLength;     // 말뚝 총 심도 (굴착고 + 근입장)
    const S_h = wall.spacing || 1.5;

    const items: QuantityItem[] = [];

    // ==========================================
    // 1. 말뚝박기용 천공 및 항타 (2-1-2-1)
    // ==========================================
    const numHPiles = Math.ceil(L_wall / S_h);
    const hPileTotalLengthM = numHPiles * totalLength;
    const drillSoilM = Number((hPileTotalLengthM * 0.55).toFixed(1));
    const drillRockM = Number((hPileTotalLengthM * 0.45).toFixed(1));

    items.push({
      id: '2-1-2-1-10',
      category: 'WALL',
      categoryName: '1. 말뚝박기용 천공 및 항타 (2-1-2-1)',
      itemCode: '2-1-2-1-10',
      name: '말뚝박기용 천공 (토사층, D500mm 케이싱사용)',
      spec: `천공경 D500mm (토사층 L=${drillSoilM}m, ${numHPiles}본)`,
      unit: 'm',
      formula: `총 벽체연장(${L_wall}m) ÷ 말뚝간격(${S_h}m) × 심도(${totalLength}m) × 55%`,
      formulaDetail: `토사구간 오거크레인 천공`,
      quantity: drillSoilM,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.DRILL_SOIL.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.DRILL_SOIL.execution,
      contractAmount: Math.round(drillSoilM * this.DEFAULT_UNIT_COSTS.DRILL_SOIL.contract),
      executionAmount: Math.round(drillSoilM * this.DEFAULT_UNIT_COSTS.DRILL_SOIL.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.DRILL_SOIL.basis
    });

    items.push({
      id: '2-1-2-1-11',
      category: 'WALL',
      categoryName: '1. 말뚝박기용 천공 및 항타 (2-1-2-1)',
      itemCode: '2-1-2-1-10',
      name: '말뚝박기용 천공 (풍화암/연암, T4 컴프레셔)',
      spec: `천공경 D500mm (암반층 L=${drillRockM}m, ${numHPiles}본)`,
      unit: 'm',
      formula: `총 벽체연장(${L_wall}m) ÷ 말뚝간격(${S_h}m) × 심도(${totalLength}m) × 45%`,
      formulaDetail: `암반소켓 T4 천공`,
      quantity: drillRockM,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.DRILL_ROCK.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.DRILL_ROCK.execution,
      contractAmount: Math.round(drillRockM * this.DEFAULT_UNIT_COSTS.DRILL_ROCK.contract),
      executionAmount: Math.round(drillRockM * this.DEFAULT_UNIT_COSTS.DRILL_ROCK.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.DRILL_ROCK.basis
    });

    items.push({
      id: '2-1-2-1-20',
      category: 'WALL',
      categoryName: '1. 말뚝박기용 천공 및 항타 (2-1-2-1)',
      itemCode: '2-1-2-1-20',
      name: '천공홀 되메우기 (φ500mm)',
      spec: `천공경 φ500mm 모래/토사 채움`,
      unit: 'm',
      formula: `말뚝 총 천공길이(${hPileTotalLengthM}m) × 85%`,
      formulaDetail: `파일 근입 후 상하부 공극 채움`,
      quantity: Number((hPileTotalLengthM * 0.85).toFixed(1)),
      contractUnitCost: this.DEFAULT_UNIT_COSTS.HOLE_BACKFILL.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.HOLE_BACKFILL.execution,
      contractAmount: Math.round((hPileTotalLengthM * 0.85) * this.DEFAULT_UNIT_COSTS.HOLE_BACKFILL.contract),
      executionAmount: Math.round((hPileTotalLengthM * 0.85) * this.DEFAULT_UNIT_COSTS.HOLE_BACKFILL.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.HOLE_BACKFILL.basis
    });

    items.push({
      id: '2-1-2-1-30',
      category: 'WALL',
      categoryName: '1. 말뚝박기용 천공 및 항타 (2-1-2-1)',
      itemCode: '2-1-2-1-30',
      name: '천공 항타 장비 조립 및 해체',
      spec: `오거크레인 & T4 플랜트`,
      unit: '회',
      formula: `공구별 2회 (초기 반입설치 1회 + 철거 1회)`,
      formulaDetail: `장비 조립 및 해체`,
      quantity: 2,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.RIG_SETUP.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.RIG_SETUP.execution,
      contractAmount: 2 * this.DEFAULT_UNIT_COSTS.RIG_SETUP.contract,
      executionAmount: 2 * this.DEFAULT_UNIT_COSTS.RIG_SETUP.execution,
      costBasis: this.DEFAULT_UNIT_COSTS.RIG_SETUP.basis
    });

    // ==========================================
    // 2. 강재사용료 및 운반 (2-1-2-2, 2-1-2-3)
    // ==========================================
    const hPileUnitWeightKg = H_PILE_DATABASE.find(hp => hp.spec === (wall.hPileSpec || 'H-300x300x10x15'))?.weight || 94.0;
    const hPileTotalWeightTon = Number(((hPileTotalLengthM * hPileUnitWeightKg) / 1000.0).toFixed(2));

    items.push({
      id: '2-1-2-3-30',
      category: 'WALL',
      categoryName: '2. 강재사용료 및 소운반 (2-1-2-2, 2-1-2-3)',
      itemCode: '2-1-2-3-30',
      name: `H-Pile 강재사용료 (${wall.hPileSpec || 'H-300x300x10x15'})`,
      spec: `${wall.hPileSpec || 'H-300x300x10x15'} (6개월 임대손료 15%)`,
      unit: 'ton',
      formula: `본수(${numHPiles}본) × 심도(${totalLength}m) × 단위중량(${hPileUnitWeightKg}kg/m) ÷ 1,000`,
      formulaDetail: `총 ${hPileTotalLengthM}m, 가설 6개월 손료`,
      quantity: hPileTotalWeightTon,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_RENTAL.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_RENTAL.execution,
      contractAmount: Math.round(hPileTotalWeightTon * this.DEFAULT_UNIT_COSTS.H_PILE_RENTAL.contract),
      executionAmount: Math.round(hPileTotalWeightTon * this.DEFAULT_UNIT_COSTS.H_PILE_RENTAL.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.H_PILE_RENTAL.basis
    });

    items.push({
      id: '2-1-2-2-20',
      category: 'WALL',
      categoryName: '2. 강재사용료 및 소운반 (2-1-2-2, 2-1-2-3)',
      itemCode: '2-1-2-2-20',
      name: 'H-Pile 현장 반입 및 소운반 (설치 및 철거)',
      spec: `크레인 소운반 및 야적장 정렬`,
      unit: 'ton',
      formula: `H-Pile 총 중량(${hPileTotalWeightTon} ton)`,
      formulaDetail: `현장내 소운반`,
      quantity: hPileTotalWeightTon,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.STEEL_TRANSPORT.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.STEEL_TRANSPORT.execution,
      contractAmount: Math.round(hPileTotalWeightTon * this.DEFAULT_UNIT_COSTS.STEEL_TRANSPORT.contract),
      executionAmount: Math.round(hPileTotalWeightTon * this.DEFAULT_UNIT_COSTS.STEEL_TRANSPORT.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.STEEL_TRANSPORT.basis
    });

    // ==========================================
    // 3. H-Pile 가설, 이음, 두부정리 및 인발 (2-1-2-4)
    // ==========================================
    const numSplices = Math.ceil(numHPiles * 0.7); // 70% 이음 적용
    items.push({
      id: '2-1-2-4-10',
      category: 'WALL',
      categoryName: '3. H-Pile 박기, 가설 및 철거 (2-1-2-4)',
      itemCode: '2-1-2-4-10',
      name: 'H-Pile 현장 맞댐용접 이음',
      spec: `${wall.hPileSpec || 'H-300x300'} 플랜지/웨브 맞댐용접`,
      unit: '개소',
      formula: `이음 개소수 (${numSplices}개소)`,
      formulaDetail: `12m 초과 말뚝 연결 용접`,
      quantity: numSplices,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_SPLICE.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_SPLICE.execution,
      contractAmount: numSplices * this.DEFAULT_UNIT_COSTS.H_PILE_SPLICE.contract,
      executionAmount: numSplices * this.DEFAULT_UNIT_COSTS.H_PILE_SPLICE.execution,
      costBasis: this.DEFAULT_UNIT_COSTS.H_PILE_SPLICE.basis
    });

    items.push({
      id: '2-1-2-4-30',
      category: 'WALL',
      categoryName: '3. H-Pile 박기, 가설 및 철거 (2-1-2-4)',
      itemCode: '2-1-2-4-30',
      name: 'H-Pile 산소 절단 및 두부정리',
      spec: `계획고 상부 잔여 두부 절단정리`,
      unit: '개소',
      formula: `말뚝 총 본수 (${numHPiles}본)`,
      formulaDetail: `두부정리`,
      quantity: numHPiles,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_HEAD_CUT.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_HEAD_CUT.execution,
      contractAmount: numHPiles * this.DEFAULT_UNIT_COSTS.H_PILE_HEAD_CUT.contract,
      executionAmount: numHPiles * this.DEFAULT_UNIT_COSTS.H_PILE_HEAD_CUT.execution,
      costBasis: this.DEFAULT_UNIT_COSTS.H_PILE_HEAD_CUT.basis
    });

    items.push({
      id: '2-1-2-4-20',
      category: 'WALL',
      categoryName: '3. H-Pile 박기, 가설 및 철거 (2-1-2-4)',
      itemCode: '2-1-2-4-20',
      name: 'H-Pile 인발 및 철거 (바이브로해머)',
      spec: `구조물 완료 후 엄지말뚝 인발`,
      unit: '본',
      formula: `말뚝 총 본수 (${numHPiles}본)`,
      formulaDetail: `바이브로 인발`,
      quantity: numHPiles,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_EXTRACT.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.H_PILE_EXTRACT.execution,
      contractAmount: numHPiles * this.DEFAULT_UNIT_COSTS.H_PILE_EXTRACT.contract,
      executionAmount: numHPiles * this.DEFAULT_UNIT_COSTS.H_PILE_EXTRACT.execution,
      costBasis: this.DEFAULT_UNIT_COSTS.H_PILE_EXTRACT.basis
    });

    items.push({
      id: '2-1-2-4-23',
      category: 'WALL',
      categoryName: '3. H-Pile 박기, 가설 및 철거 (2-1-2-4)',
      itemCode: '2-1-2-4-23',
      name: 'H-Pile 인발 후 공극 되메우기',
      spec: `인발 공동 시멘트/모래 충전`,
      unit: 'm',
      formula: `인발 총 길이 (${hPileTotalLengthM}m)`,
      formulaDetail: `공동 함몰 방지 채움`,
      quantity: hPileTotalLengthM,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.EXTRACT_BACKFILL.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.EXTRACT_BACKFILL.execution,
      contractAmount: Math.round(hPileTotalLengthM * this.DEFAULT_UNIT_COSTS.EXTRACT_BACKFILL.contract),
      executionAmount: Math.round(hPileTotalLengthM * this.DEFAULT_UNIT_COSTS.EXTRACT_BACKFILL.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.EXTRACT_BACKFILL.basis
    });

    // ==========================================
    // 4. 토류판 설치 및 철거 (2-1-2-9)
    // ==========================================
    const laggingAreaM2 = Number((L_wall * H).toFixed(1));
    const laggingType = inputs.wall.laggingType || '낙엽송 목재 토류판 (t=8.0cm)';
    const isSteelLagging = laggingType.includes('강재');
    const isShotcrete = laggingType.includes('숏크리트');

    if (isSteelLagging) {
      items.push({
        id: '2-1-2-9-15',
        category: 'LAGGING',
        categoryName: '4. 토류판 설치 및 철거 (2-1-2-9)',
        itemCode: '2-1-2-9-15',
        name: `강재 토류판 설치 (${laggingType})`,
        spec: `${laggingType} (6개월 손료 + 끼우기)`,
        unit: '㎡',
        formula: `총 벽체연장(${L_wall}m) × 굴착깊이(${H}m)`,
        formulaDetail: `강재 토류판 시공 면적 (${laggingAreaM2}㎡)`,
        quantity: laggingAreaM2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_INSTALL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_INSTALL.execution,
        contractAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_INSTALL.contract),
        executionAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_INSTALL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_INSTALL.basis
      });

      items.push({
        id: '2-1-2-9-35',
        category: 'LAGGING',
        categoryName: '4. 토류판 설치 및 철거 (2-1-2-9)',
        itemCode: '2-1-2-9-35',
        name: `강재 토류판 해체 및 크레인 인양`,
        spec: `되메우기 시 강재 토류판 순차 인양 반출`,
        unit: '㎡',
        formula: `토류판 면적(${laggingAreaM2} ㎡)`,
        formulaDetail: `강재 토류판 인양 철거`,
        quantity: laggingAreaM2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_DISMANTLE.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_DISMANTLE.execution,
        contractAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_DISMANTLE.contract),
        executionAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_DISMANTLE.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.STEEL_LAGGING_DISMANTLE.basis
      });
    } else if (isShotcrete) {
      items.push({
        id: '2-1-2-9-20',
        category: 'LAGGING',
        categoryName: '4. 토류판 설치 및 철거 (2-1-2-9)',
        itemCode: '2-1-2-9-20',
        name: `숏크리트 타설 및 와이어메쉬 시공`,
        spec: `t=150mm 습식 숏크리트 + 용접철망 부착`,
        unit: '㎡',
        formula: `총 벽체연장(${L_wall}m) × 굴착깊이(${H}m)`,
        formulaDetail: `숏크리트 전면 타설`,
        quantity: laggingAreaM2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.SHOTCRETE_LAGGING.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.SHOTCRETE_LAGGING.execution,
        contractAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.SHOTCRETE_LAGGING.contract),
        executionAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.SHOTCRETE_LAGGING.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.SHOTCRETE_LAGGING.basis
      });
    } else {
      // 목재 토류판
      items.push({
        id: '2-1-2-9-10',
        category: 'LAGGING',
        categoryName: '4. 토류판 설치 및 철거 (2-1-2-9)',
        itemCode: '2-1-2-9-10',
        name: `목재 토류판 설치 (${laggingType})`,
        spec: `${laggingType} (3회 유용손료)`,
        unit: '㎡',
        formula: `총 벽체연장(${L_wall}m) × 굴착깊이(${H}m)`,
        formulaDetail: `토류판 시공 전면적`,
        quantity: laggingAreaM2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.LAGGING_INSTALL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.LAGGING_INSTALL.execution,
        contractAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.LAGGING_INSTALL.contract),
        executionAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.LAGGING_INSTALL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.LAGGING_INSTALL.basis
      });

      items.push({
        id: '2-1-2-9-30',
        category: 'LAGGING',
        categoryName: '4. 토류판 설치 및 철거 (2-1-2-9)',
        itemCode: '2-1-2-9-30',
        name: '목재 토류판 해체 및 철거',
        spec: `되메우기 시 토류판 순차 인양`,
        unit: '㎡',
        formula: `토류판 면적(${laggingAreaM2} ㎡)`,
        formulaDetail: `철거 공종`,
        quantity: laggingAreaM2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.LAGGING_DISMANTLE.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.LAGGING_DISMANTLE.execution,
        contractAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.LAGGING_DISMANTLE.contract),
        executionAmount: Math.round(laggingAreaM2 * this.DEFAULT_UNIT_COSTS.LAGGING_DISMANTLE.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.LAGGING_DISMANTLE.basis
      });
    }

    // ==========================================
    // 5. 띠장재 (2-1-2-6) - 단별 전체 벽체 연장 L_wall 기준
    // ==========================================
    let totalWaleWeightTon = 0;
    alt.supports.forEach((sup, idx) => {
      const waleSpec = sup.waleSpec || '2-H 300x300x10x15';
      const isTwoH = waleSpec.startsWith('2-H');
      const numBeams = isTwoH ? 2 : 1;
      const waleOpt = WALE_DATABASE.find(w => w.spec === waleSpec) || WALE_DATABASE[0];
      const singleBeamWeight = isTwoH ? waleOpt.weight / 2.0 : waleOpt.weight;
      // 전체 벽체 연장 L_wall에 대해 양열 띠장 연장
      const tierWeightTon = Number(((L_wall * numBeams * singleBeamWeight) / 1000.0).toFixed(2));
      totalWaleWeightTon += tierWeightTon;

      items.push({
        id: `2-1-2-6-${idx + 1}`,
        category: 'WALE',
        categoryName: '5. 띠장재 설치 및 철거 (2-1-2-6)',
        itemCode: '2-1-2-6-10',
        name: `띠장재 ${idx + 1}단 손료 & 설치 (${waleSpec})`,
        spec: `${waleSpec} (전체 벽체연장 ${L_wall}m, EL -${sup.depth}m)`,
        unit: 'ton',
        formula: `벽체연장(${L_wall}m) × 열수(${numBeams}) × 단위중량(${singleBeamWeight.toFixed(1)}kg/m) ÷ 1,000`,
        formulaDetail: `${idx + 1}단 띠장 6개월 손료 + 가설`,
        quantity: tierWeightTon,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.WALE_RENTAL_INSTALL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.WALE_RENTAL_INSTALL.execution,
        contractAmount: Math.round(tierWeightTon * this.DEFAULT_UNIT_COSTS.WALE_RENTAL_INSTALL.contract),
        executionAmount: Math.round(tierWeightTon * this.DEFAULT_UNIT_COSTS.WALE_RENTAL_INSTALL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.WALE_RENTAL_INSTALL.basis
      });
    });

    const numWaleJoints = Math.ceil((L_wall * alt.supports.length) / 10);
    items.push({
      id: '2-1-2-6-20',
      category: 'WALE',
      categoryName: '5. 띠장재 설치 및 철거 (2-1-2-6)',
      itemCode: '2-1-2-6-20',
      name: '띠장재 조인트 연결 및 우각부 코너보강',
      spec: `C-1 Type 이음판 & D-1 Type 우각부 브라켓`,
      unit: '개소',
      formula: `10m 간격 이음 + 코너부 (${numWaleJoints}개소)`,
      formulaDetail: `띠장 연속 이음 및 코너 보강`,
      quantity: numWaleJoints,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.WALE_SPLICE_CORNER.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.WALE_SPLICE_CORNER.execution,
      contractAmount: numWaleJoints * this.DEFAULT_UNIT_COSTS.WALE_SPLICE_CORNER.contract,
      executionAmount: numWaleJoints * this.DEFAULT_UNIT_COSTS.WALE_SPLICE_CORNER.execution,
      costBasis: this.DEFAULT_UNIT_COSTS.WALE_SPLICE_CORNER.basis
    });

    const numHangers = Math.ceil((L_wall * alt.supports.length) / S_h);
    items.push({
      id: '2-1-2-6-40',
      category: 'WALE',
      categoryName: '5. 띠장재 설치 및 철거 (2-1-2-6)',
      itemCode: '2-1-2-6-40',
      name: '띠장 받침 보걸이 (철근/앵글 브라켓) 설치',
      spec: `O-1 / O-2 Type 엄지말뚝 부착 용접`,
      unit: '개소',
      formula: `말뚝 교차점마다 1개소 (${numHangers}개소)`,
      formulaDetail: `띠장 처짐 방지 받침 브라켓`,
      quantity: numHangers,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.BEAM_HANGER.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.BEAM_HANGER.execution,
      contractAmount: numHangers * this.DEFAULT_UNIT_COSTS.BEAM_HANGER.contract,
      executionAmount: numHangers * this.DEFAULT_UNIT_COSTS.BEAM_HANGER.execution,
      costBasis: this.DEFAULT_UNIT_COSTS.BEAM_HANGER.basis
    });

    items.push({
      id: '2-1-2-6-12',
      category: 'WALE',
      categoryName: '5. 띠장재 설치 및 철거 (2-1-2-6)',
      itemCode: '2-1-2-6-12',
      name: '띠장재 해체 및 크레인 인양 철거',
      spec: `구조물 축조 후 띠장 절단 및 인양 반출 (${totalWaleWeightTon} ton)`,
      unit: 'ton',
      formula: `띠장 총 중량 (${totalWaleWeightTon} ton)`,
      formulaDetail: `순차 해체 공종`,
      quantity: totalWaleWeightTon,
      contractUnitCost: this.DEFAULT_UNIT_COSTS.WALE_DISMANTLE.contract,
      executionUnitCost: this.DEFAULT_UNIT_COSTS.WALE_DISMANTLE.execution,
      contractAmount: Math.round(totalWaleWeightTon * this.DEFAULT_UNIT_COSTS.WALE_DISMANTLE.contract),
      executionAmount: Math.round(totalWaleWeightTon * this.DEFAULT_UNIT_COSTS.WALE_DISMANTLE.execution),
      costBasis: this.DEFAULT_UNIT_COSTS.WALE_DISMANTLE.basis
    });

    // ==========================================
    // 6. 버팀보 (Strut, 2-1-2-7) - 종방향 굴착연장 L_long 기준 본수 산정
    // ==========================================
    const struts = alt.supports.filter(s => s.type === 'STRUT' || (s.type as any) === 'COMPOSITE_STRUT');
    let totalStrutCount = 0;
    let totalStrutWeightTon = 0;

    if (struts.length > 0) {
      struts.forEach((st, idx) => {
        const isComp = alt.type === 'COMPOSITE_STRUT' || (st.type as any) === 'COMPOSITE_STRUT' || (st.strutSpec && st.strutSpec.includes('사각'));
        const strutSpacing = st.horizSpacing || (isComp ? 5.0 : 3.5);
        // 종방향 연장 L_long을 수평간격으로 나눈 횡방향 가로지름 본수
        const numStrutsPerTier = Math.ceil(L_long / strutSpacing);
        totalStrutCount += numStrutsPerTier;
        const strutOpt = STRUT_DATABASE.find(sd => sd.spec === st.strutSpec) || (isComp ? STRUT_DATABASE[6] : STRUT_DATABASE[0]);
        const tierWeightTon = Number(((numStrutsPerTier * B * strutOpt.weight) / 1000.0).toFixed(2));
        totalStrutWeightTon += tierWeightTon;

        const rentalCost = isComp ? this.DEFAULT_UNIT_COSTS.COMPOSITE_STRUT_RENTAL_INSTALL : this.DEFAULT_UNIT_COSTS.STRUT_RENTAL_INSTALL;

        items.push({
          id: `2-1-2-7-${idx + 1}`,
          category: 'STRUT',
          categoryName: '6. 버팀보 설치 및 철거 (2-1-2-7)',
          itemCode: '2-1-2-7-10',
          name: isComp ? `합성사각강관(4-Box) 버팀보 ${idx + 1}단 손료 & 가설` : `강관 버팀보(Strut) ${idx + 1}단 손료 & 설치`,
          spec: `${st.specName} (@ ${strutSpacing}m, 굴착폭 ${B}m 가로지름)`,
          unit: 'ton',
          formula: `본수(${numStrutsPerTier}본) × 굴착폭(${B}m) × 단위중량(${strutOpt.weight}kg/m) ÷ 1,000`,
          formulaDetail: `종방향 ${L_long}m ÷ 간격 ${strutSpacing}m = ${numStrutsPerTier}본`,
          quantity: tierWeightTon,
          contractUnitCost: rentalCost.contract,
          executionUnitCost: rentalCost.execution,
          contractAmount: Math.round(tierWeightTon * rentalCost.contract),
          executionAmount: Math.round(tierWeightTon * rentalCost.execution),
          costBasis: rentalCost.basis
        });
      });

      // 스크류잭 또는 합성사각강관 전용 2000kN 고용량 유압잭
      const isCompAlt = alt.type === 'COMPOSITE_STRUT';
      const jackCost = isCompAlt ? this.DEFAULT_UNIT_COSTS.COMPOSITE_STRUT_JACK : this.DEFAULT_UNIT_COSTS.SCREW_JACK;

      items.push({
        id: '2-1-2-7-40',
        category: 'STRUT',
        categoryName: '6. 버팀보 설치 및 철거 (2-1-2-7)',
        itemCode: '2-1-2-7-40',
        name: isCompAlt ? '합성사각강관 전용 고용량(2000kN) 유압 프리로드잭 & 접합브래킷' : '스크류잭 (1000kN) 설치 및 프리로드 재하',
        spec: isCompAlt ? '2000kN 유압 프리로드 가압 및 특수 고정브래킷' : `유압잭 프리로드 가압 + 스크류잭 고정`,
        unit: '개소',
        formula: `버팀보 총 본수 (${totalStrutCount}본)`,
        formulaDetail: `버팀보 단부마다 1개소`,
        quantity: totalStrutCount,
        contractUnitCost: jackCost.contract,
        executionUnitCost: jackCost.execution,
        contractAmount: totalStrutCount * jackCost.contract,
        executionAmount: totalStrutCount * jackCost.execution,
        costBasis: jackCost.basis
      });

      // 화타쐐기 (K-1 Type)
      items.push({
        id: '2-1-2-7-30',
        category: 'STRUT',
        categoryName: '6. 버팀보 설치 및 철거 (2-1-2-7)',
        itemCode: '2-1-2-7-30',
        name: '화타쐐기 (K-1 Type) 제작 및 밀착설치',
        spec: `띠장-버팀보 접합부 유격 제거용 특수 쐐기`,
        unit: '개소',
        formula: `버팀보 총 본수 (${totalStrutCount}개소)`,
        formulaDetail: `접합부마다 1개소`,
        quantity: totalStrutCount,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.WEDGE_BLOCK.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.WEDGE_BLOCK.execution,
        contractAmount: totalStrutCount * this.DEFAULT_UNIT_COSTS.WEDGE_BLOCK.contract,
        executionAmount: totalStrutCount * this.DEFAULT_UNIT_COSTS.WEDGE_BLOCK.execution,
        costBasis: this.DEFAULT_UNIT_COSTS.WEDGE_BLOCK.basis
      });

      // 버팀보 해체 및 인양 반출
      const dismantleCost = isCompAlt ? this.DEFAULT_UNIT_COSTS.COMPOSITE_STRUT_DISMANTLE : this.DEFAULT_UNIT_COSTS.STRUT_DISMANTLE;
      items.push({
        id: '2-1-2-7-15',
        category: 'STRUT',
        categoryName: '6. 버팀보 설치 및 철거 (2-1-2-7)',
        itemCode: '2-1-2-7-15',
        name: isCompAlt ? '합성사각강관 볼트 분해 및 크레인 인양' : '강관 버팀보(Strut) 순차 해체 및 크레인 인양',
        spec: `본구조물 타설 강도 발현 후 단별 절단/인양 반출 (${Number(totalStrutWeightTon.toFixed(2))} ton)`,
        unit: 'ton',
        formula: `버팀보 총 중량 (${Number(totalStrutWeightTon.toFixed(2))} ton)`,
        formulaDetail: `구조물 축조 연계 해체 공종`,
        quantity: Number(totalStrutWeightTon.toFixed(2)),
        contractUnitCost: dismantleCost.contract,
        executionUnitCost: dismantleCost.execution,
        contractAmount: Math.round(totalStrutWeightTon * dismantleCost.contract),
        executionAmount: Math.round(totalStrutWeightTon * dismantleCost.execution),
        costBasis: dismantleCost.basis
      });
    }

    // ==========================================
    // 7. 어스앵커 (2-1-2-10) - 양측 전체 벽체 L_wall 기준 본수 산정
    // ==========================================
    const anchors = alt.supports.filter(s => s.type === 'GROUND_ANCHOR');
    if (anchors.length > 0) {
      anchors.forEach((anc, idx) => {
        const anchorSpacing = anc.horizSpacing || 2.0;
        // 양측 전체 벽체 L_wall에 설치되는 앵커 총 본수
        const totalAnchorsInTier = Math.ceil(L_wall / anchorSpacing);
        const singleLenM = (anc.freeLength || 6.0) + (anc.bondLength || 5.5);
        const totalDrillM = Number((totalAnchorsInTier * singleLenM).toFixed(1));

        items.push({
          id: `2-1-2-10-10-${idx + 1}`,
          category: 'ANCHOR',
          categoryName: '7. 어스앵커 천공, 강선, 인장 (2-1-2-10)',
          itemCode: '2-1-2-10-10',
          name: `어스앵커 ${idx + 1}단 천공 및 그라우팅`,
          spec: `D135mm 천공 + 시멘트 가압 주입 (${totalAnchorsInTier}공, L=${singleLenM.toFixed(1)}m)`,
          unit: 'm',
          formula: `양측본수(${totalAnchorsInTier}공) × 길이(${singleLenM.toFixed(1)}m)`,
          formulaDetail: `전체 벽체연장 ${L_wall}m ÷ 간격 ${anchorSpacing}m = ${totalAnchorsInTier}공`,
          quantity: totalDrillM,
          contractUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_DRILL_GROUT.contract,
          executionUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_DRILL_GROUT.execution,
          contractAmount: Math.round(totalDrillM * this.DEFAULT_UNIT_COSTS.ANCHOR_DRILL_GROUT.contract),
          executionAmount: Math.round(totalDrillM * this.DEFAULT_UNIT_COSTS.ANCHOR_DRILL_GROUT.execution),
          costBasis: this.DEFAULT_UNIT_COSTS.ANCHOR_DRILL_GROUT.basis
        });

        items.push({
          id: `2-1-2-10-30-${idx + 1}`,
          category: 'ANCHOR',
          categoryName: '7. 어스앵커 천공, 강선, 인장 (2-1-2-10)',
          itemCode: '2-1-2-10-30',
          name: `PC강선 가공조립 및 삽입 (SWPC 7B 12.7mm)`,
          spec: `SWPC 12.7mm 4가닥 인장재 조립`,
          unit: 'm',
          formula: `앵커 총 연장 (${totalDrillM} m)`,
          formulaDetail: `강연선 자재 및 조립가공`,
          quantity: totalDrillM,
          contractUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_STRAND_INSTALL.contract,
          executionUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_STRAND_INSTALL.execution,
          contractAmount: Math.round(totalDrillM * this.DEFAULT_UNIT_COSTS.ANCHOR_STRAND_INSTALL.contract),
          executionAmount: Math.round(totalDrillM * this.DEFAULT_UNIT_COSTS.ANCHOR_STRAND_INSTALL.execution),
          costBasis: this.DEFAULT_UNIT_COSTS.ANCHOR_STRAND_INSTALL.basis
        });

        // 🌟 인장시험, PC콘 조립 및 락오프 (공당 단가 적용으로 현실화)
        items.push({
          id: `2-1-2-10-50-${idx + 1}`,
          category: 'ANCHOR',
          categoryName: '7. 어스앵커 천공, 강선, 인장 (2-1-2-10)',
          itemCode: '2-1-2-10-50',
          name: `유압잭 인장시험, PC콘 조립 및 락오프(Lock-off)`,
          spec: `설계축력 120% 인장시험 및 쐐기 정착 (공당)`,
          unit: '공',
          formula: `양측 앵커 본수 (${totalAnchorsInTier}공)`,
          formulaDetail: `인장시험 및 정착 (공당 단가)`,
          quantity: totalAnchorsInTier,
          contractUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_TENSION_TEST.contract,
          executionUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_TENSION_TEST.execution,
          contractAmount: totalAnchorsInTier * this.DEFAULT_UNIT_COSTS.ANCHOR_TENSION_TEST.contract,
          executionAmount: totalAnchorsInTier * this.DEFAULT_UNIT_COSTS.ANCHOR_TENSION_TEST.execution,
          costBasis: this.DEFAULT_UNIT_COSTS.ANCHOR_TENSION_TEST.basis
        });

        // 고각 앵커 전용 특수 경사 지압 브래킷 (공당 38만원으로 현실적 임대손료 적용)
        if ((anc.angle || 45) >= 40) {
          items.push({
            id: `2-1-2-10-SP-${idx + 1}`,
            category: 'ANCHOR',
            categoryName: '7. 어스앵커 천공, 강선, 인장 (2-1-2-10)',
            itemCode: '2-1-2-10-SP',
            name: `고각 앵커 ${idx + 1}단 특수 경사 지압 브래킷 & 띠장 거셋`,
            spec: `경사각 ${anc.angle || 45}° 고각 지압 브래킷 (6개월 손료 380,000원/공)`,
            unit: '개소',
            formula: `양측 앵커 본수 (${totalAnchorsInTier}공)`,
            formulaDetail: `고각(${anc.angle || 45}°) 지압력 전달 특수 가공조립품`,
            quantity: totalAnchorsInTier,
            contractUnitCost: this.DEFAULT_UNIT_COSTS.HIGH_ANGLE_SPECIAL_BRACKET.contract,
            executionUnitCost: this.DEFAULT_UNIT_COSTS.HIGH_ANGLE_SPECIAL_BRACKET.execution,
            contractAmount: Math.round(totalAnchorsInTier * this.DEFAULT_UNIT_COSTS.HIGH_ANGLE_SPECIAL_BRACKET.contract),
            executionAmount: Math.round(totalAnchorsInTier * this.DEFAULT_UNIT_COSTS.HIGH_ANGLE_SPECIAL_BRACKET.execution),
            costBasis: this.DEFAULT_UNIT_COSTS.HIGH_ANGLE_SPECIAL_BRACKET.basis
          });
        } else {
          // 일반 앵커 BasePlate
          items.push({
            id: `2-1-2-10-60-${idx + 1}`,
            category: 'ANCHOR',
            categoryName: '7. 어스앵커 천공, 강선, 인장 (2-1-2-10)',
            itemCode: '2-1-2-10-60',
            name: `일반앵커 지압판(Base Plate) 제작설치`,
            spec: `표준 지압판 BasePlate`,
            unit: '개소',
            formula: `양측 앵커 본수 (${totalAnchorsInTier}공)`,
            formulaDetail: `지압판 제작설치`,
            quantity: totalAnchorsInTier,
            contractUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_BASE_PLATE.contract,
            executionUnitCost: this.DEFAULT_UNIT_COSTS.ANCHOR_BASE_PLATE.execution,
            contractAmount: Math.round(totalAnchorsInTier * this.DEFAULT_UNIT_COSTS.ANCHOR_BASE_PLATE.contract),
            executionAmount: Math.round(totalAnchorsInTier * this.DEFAULT_UNIT_COSTS.ANCHOR_BASE_PLATE.execution),
            costBasis: this.DEFAULT_UNIT_COSTS.ANCHOR_BASE_PLATE.basis
          });
        }
      });
    }

    // ==========================================
    // 8. 복공판 및 주형보 (2-1-2-5) - 종방향 굴착연장 L_long × 폭 B 기준
    // ==========================================
    if (inputs.deckingConfig?.useDecking) {
      const decking = inputs.deckingConfig;
      const deckAreaM2 = Number((L_long * B).toFixed(1));
      items.push({
        id: '2-1-2-5-70',
        category: 'DECKING',
        categoryName: '8. 복공판 및 주형보 (2-1-2-5)',
        itemCode: '2-1-2-5-70',
        name: '복공판 (Deck Plate) 임대 및 설치',
        spec: `t=200mm 미끄럼방지 무늬강판 (${decking.trafficLoadType} 하중 지지)`,
        unit: '㎡',
        formula: `종방향연장(${L_long}m) × 굴착폭(${B}m)`,
        formulaDetail: `차량 통행용 복공 전면적 산출`,
        quantity: deckAreaM2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.DECK_PLATE.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.DECK_PLATE.execution,
        contractAmount: Math.round(deckAreaM2 * this.DEFAULT_UNIT_COSTS.DECK_PLATE.contract),
        executionAmount: Math.round(deckAreaM2 * this.DEFAULT_UNIT_COSTS.DECK_PLATE.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.DECK_PLATE.basis
      });

      const deckBeamSpacing = decking.deckBeamSpacing || 2.0;
      const numDeckBeams = Math.ceil(L_long / deckBeamSpacing);
      const deckBeamOpt = DECK_BEAM_DATABASE.find(db => db.spec === decking.deckBeamSpec) || DECK_BEAM_DATABASE[0];
      const deckBeamWeightTon = Number(((numDeckBeams * B * deckBeamOpt.weight) / 1000.0).toFixed(2));

      items.push({
        id: '2-1-2-5-10',
        category: 'DECKING',
        categoryName: '8. 복공판 및 주형보 (2-1-2-5)',
        itemCode: '2-1-2-5-10',
        name: '복공 주형보(Deck Girder) 손료 & 거치',
        spec: `${decking.deckBeamSpec || 'H-400x400x13x21'} (@ ${deckBeamSpacing}m)`,
        unit: 'ton',
        formula: `본수(${numDeckBeams}본) × 굴착폭(${B}m) × 단위중량(${deckBeamOpt.weight}kg/m) ÷ 1,000`,
        formulaDetail: `종방향 ${L_long}m ÷ 간격 ${deckBeamSpacing}m = ${numDeckBeams}본`,
        quantity: deckBeamWeightTon,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.DECK_BEAM_RENTAL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.DECK_BEAM_RENTAL.execution,
        contractAmount: Math.round(deckBeamWeightTon * this.DEFAULT_UNIT_COSTS.DECK_BEAM_RENTAL.contract),
        executionAmount: Math.round(deckBeamWeightTon * this.DEFAULT_UNIT_COSTS.DECK_BEAM_RENTAL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.DECK_BEAM_RENTAL.basis
      });

      items.push({
        id: '2-1-2-5-30',
        category: 'DECKING',
        categoryName: '8. 복공판 및 주형보 (2-1-2-5)',
        itemCode: '2-1-2-5-30',
        name: '주형보 브레이싱 및 피스브라켓 제작설치',
        spec: `X-1 Type 브레이싱 & 피스브라켓`,
        unit: '개소',
        formula: `주형보 교차점 (${numDeckBeams * 2}개소)`,
        formulaDetail: `주형보 좌굴 방지 브레이싱`,
        quantity: numDeckBeams * 2,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.DECK_BRACING.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.DECK_BRACING.execution,
        contractAmount: (numDeckBeams * 2) * this.DEFAULT_UNIT_COSTS.DECK_BRACING.contract,
        executionAmount: (numDeckBeams * 2) * this.DEFAULT_UNIT_COSTS.DECK_BRACING.execution,
        costBasis: this.DEFAULT_UNIT_COSTS.DECK_BRACING.basis
      });
    }

    // ==========================================
    // 9. 보강재 및 중간말뚝 (2-1-2-8)
    // ==========================================
    const hasStrut = alt.type === 'ALL_ANCHOR' ? false : (alt.supports && alt.supports.some((s: any) => s.type === 'STRUT'));
    // 합성사각강관(대안 4)은 초고강성 폐합단면으로 무중간말뚝 단일지간 (중간말뚝 및 가새 전량 삭제 0원)
    const isCompositeStrutAlt = alt.type === 'COMPOSITE_STRUT';
    const requiresKingPost = hasStrut && !isCompositeStrutAlt && (B >= 10.0 || inputs.deckingConfig?.useDecking);
    
    if (requiresKingPost) {
      const decking = inputs.deckingConfig;
      const kingSpacing = decking?.kingPostSpacing || 3.5;
      const numKingPostRows = B >= 25.0 ? 2 : 1; // 굴착폭 25m 이상 시 2열 중간말뚝
      const numKingPosts = Math.ceil(L_long / kingSpacing) * numKingPostRows;
      const kingTotalLenM = decking?.kingPostTotalLength || (H + 4.5); // 근입장 포함
      const kingWeightKg = 94.0; // H-300x300x10x15 (94.0 kg/m)
      const kingWeightTon = Number(((numKingPosts * kingTotalLenM * kingWeightKg) / 1000.0).toFixed(2));

      items.push({
        id: '2-1-2-8-60',
        category: 'BRACING',
        categoryName: '9. 보강재 및 중간말뚝 (2-1-2-8)',
        itemCode: '2-1-2-8-60',
        name: '중간말뚝(King Post) 암반소켓 천공 & 거치',
        spec: `H-300x300x10x15 (L=${kingTotalLenM.toFixed(1)}m, ${numKingPosts}본)`,
        unit: 'm',
        formula: `본수(${numKingPosts}본) × 길이(${kingTotalLenM.toFixed(1)}m)`,
        formulaDetail: `굴착폭 ${B}m 버팀보 좌굴길이 구속용 중간말뚝 천공 및 거치`,
        quantity: numKingPosts * kingTotalLenM,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_SOCKET_DRILL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_SOCKET_DRILL.execution,
        contractAmount: Math.round((numKingPosts * kingTotalLenM) * this.DEFAULT_UNIT_COSTS.KING_POST_SOCKET_DRILL.contract),
        executionAmount: Math.round((numKingPosts * kingTotalLenM) * this.DEFAULT_UNIT_COSTS.KING_POST_SOCKET_DRILL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.KING_POST_SOCKET_DRILL.basis
      });

      items.push({
        id: '2-1-2-8-61',
        category: 'BRACING',
        categoryName: '9. 보강재 및 중간말뚝 (2-1-2-8)',
        itemCode: '2-1-2-8-60',
        name: '중간말뚝 H형강 강재사용료 (6개월 손료)',
        spec: `H-300x300x10x15 6개월 손료`,
        unit: 'ton',
        formula: `중간말뚝 총 중량 (${kingWeightTon} ton)`,
        formulaDetail: `강재 임대 손료`,
        quantity: kingWeightTon,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_RENTAL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_RENTAL.execution,
        contractAmount: Math.round(kingWeightTon * this.DEFAULT_UNIT_COSTS.KING_POST_RENTAL.contract),
        executionAmount: Math.round(kingWeightTon * this.DEFAULT_UNIT_COSTS.KING_POST_RENTAL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.KING_POST_RENTAL.basis
      });

      items.push({
        id: '2-1-2-8-50',
        category: 'BRACING',
        categoryName: '9. 보강재 및 중간말뚝 (2-1-2-8)',
        itemCode: '2-1-2-8-50',
        name: '중간말뚝-스트럿 완전 강결 브라켓 & 스티프너 보강',
        spec: `Lk=단간격(2.7m) 구속용 강결 브라켓`,
        unit: '개소',
        formula: `중간말뚝(${numKingPosts}본) × 버팀보(${struts.length}단) = ${numKingPosts * struts.length}개소`,
        formulaDetail: `좌굴 억제 강결 체결`,
        quantity: numKingPosts * struts.length,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_RIGID_JOINT.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_RIGID_JOINT.execution,
        contractAmount: (numKingPosts * struts.length) * this.DEFAULT_UNIT_COSTS.KING_POST_RIGID_JOINT.contract,
        executionAmount: (numKingPosts * struts.length) * this.DEFAULT_UNIT_COSTS.KING_POST_RIGID_JOINT.execution,
        costBasis: this.DEFAULT_UNIT_COSTS.KING_POST_RIGID_JOINT.basis
      });

      items.push({
        id: '2-1-2-8-65',
        category: 'BRACING',
        categoryName: '9. 보강재 및 중간말뚝 (2-1-2-8)',
        itemCode: '2-1-2-8-65',
        name: '중간말뚝 바닥 기초슬래브 관통부 지수판 방수처리',
        spec: `수팽창 지수판 + 무수축 그라우트 밀봉`,
        unit: '개소',
        formula: `중간말뚝 총 본수 (${numKingPosts}개소)`,
        formulaDetail: `기초 슬래브 관통부 지하수 유입 차단 방수`,
        quantity: numKingPosts,
        contractUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_WATERPROOF.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.KING_POST_WATERPROOF.execution,
        contractAmount: numKingPosts * this.DEFAULT_UNIT_COSTS.KING_POST_WATERPROOF.contract,
        executionAmount: numKingPosts * this.DEFAULT_UNIT_COSTS.KING_POST_WATERPROOF.execution,
        costBasis: this.DEFAULT_UNIT_COSTS.KING_POST_WATERPROOF.basis
      });

      items.push({
        id: '2-1-2-8-10',
        category: 'BRACING',
        categoryName: '9. 보강재 및 중간말뚝 (2-1-2-8)',
        itemCode: '2-1-2-8-10',
        name: 'ㄷ-형강 및 L-형강 수평/수직 가새 보강재',
        spec: `380x100 ㄷ형강 & 90x90 L형강 (G-2 Type)`,
        unit: 'ton',
        formula: `버팀보 중량의 12% 환산 (${Number((totalStrutWeightTon * 0.12).toFixed(1))} ton)`,
        formulaDetail: `버팀보 비틀림 방지 및 평면 안정성 확보 가새`,
        quantity: Number((totalStrutWeightTon * 0.12).toFixed(1)),
        contractUnitCost: this.DEFAULT_UNIT_COSTS.BRACING_STEEL.contract,
        executionUnitCost: this.DEFAULT_UNIT_COSTS.BRACING_STEEL.execution,
        contractAmount: Math.round((totalStrutWeightTon * 0.12) * this.DEFAULT_UNIT_COSTS.BRACING_STEEL.contract),
        executionAmount: Math.round((totalStrutWeightTon * 0.12) * this.DEFAULT_UNIT_COSTS.BRACING_STEEL.execution),
        costBasis: this.DEFAULT_UNIT_COSTS.BRACING_STEEL.basis
      });
    }

    // 커스텀 단가 오버라이드 적용
    if (customUnitCosts) {
      items.forEach(item => {
        if (customUnitCosts[item.id]) {
          item.contractUnitCost = customUnitCosts[item.id].contract;
          item.executionUnitCost = customUnitCosts[item.id].execution;
          item.contractAmount = Math.round(item.quantity * item.contractUnitCost);
          item.executionAmount = Math.round(item.quantity * item.executionUnitCost);
        }
      });
    }

    const totalContractCost = items.reduce((sum, it) => sum + it.contractAmount, 0);
    const totalExecutionCost = items.reduce((sum, it) => sum + it.executionAmount, 0);
    const costSavings = totalContractCost - totalExecutionCost;
    const executionRatio = Number(((totalExecutionCost / Math.max(1, totalContractCost)) * 100).toFixed(1));

    return {
      altId: alt.id,
      altName: alt.name,
      rentalMonths,
      steelRentalRateMonthly: 2.5,
      items,
      totalContractCost,
      totalExecutionCost,
      costSavings,
      executionRatio
    };
  }
}
