export interface SoilLayer {
  id: string;
  name: string;
  topDepth: number;       // m
  bottomDepth: number;    // m
  gamma: number;          // kN/m3
  gammaSat: number;       // kN/m3
  cohesion: number;       // kN/m2
  frictionAngle: number;  // deg
  Es: number;             // kN/m2
  kh0: number;            // kN/m3
  NValue: number;         // N치
  isCohesive: boolean;
  color: string;
}

export type WallType = 'H_PILE' | 'CIP' | 'SCW' | 'SHEET_PILE' | 'SLURRY_WALL';

export interface HPileSectionProp {
  spec: string;
  H: number;  // mm
  B: number;  // mm
  t1: number; // mm
  t2: number; // mm
  weight: number; // kg/m
  A: number;  // cm2
  Ix: number; // cm4
  Zx: number; // cm3
  rx: number; // cm
}

export interface StrutSectionProp {
  spec: string;
  type: 'PIPE' | 'H_BEAM' | 'COMPOSITE_SQUARE';
  diameterOrH: number; // mm (원형 직경 또는 사각강관 한변 길이)
  thickness: number;   // mm
  weight: number;      // kg/m
  A: number;           // cm2
  Ix: number;          // cm4
  rx: number;          // cm
  allowCompressCapacity: number; // kN (표준 좌굴길이 6m 기준)
}

export interface WaleSectionProp {
  spec: string;        // ex: "2-H 300x300x10x15"
  hSpec: string;       // ex: "H-300x300x10x15"
  numBeams: number;    // 2열
  totalZx: number;     // cm3 (2 * Zx)
  totalIx: number;     // cm4
  weight: number;      // kg/m
}

export interface WallSection {
  id: string;
  name: string;
  type: WallType;
  spacing: number;        // m (엄지말뚝 수평 간격, ex: 1.5m, 1.8m, 2.0m)
  EI: number;             // kNm2/m (단위폭당 휨강성)
  EA: number;             // kN/m (단위폭당 축강성)
  Zx: number;             // cm3 (H형강 1본당 단면계수)
  totalLength: number;    // m (벽체 총 연장 = 굴착고 + 근입장)
  yieldStrength: number;  // MPa
  allowBendingStress: number; // MPa
  hPileSpec?: string;     // ex: "H-300x300x10x15"
  laggingType?: string;   // ex: "낙엽송 목재 8cm", "10cm", "숏크리트 t=150"
  laggingThickness?: number; // mm
}

export type SupportType = 'STRUT' | 'GROUND_ANCHOR' | 'RAKER' | 'COMPOSITE_STRUT';

export interface SupportStage {
  id: string;
  stageIndex: number;
  type: SupportType;
  depth: number;          // m (지표면 기준 설치 심도)
  angle: number;          // deg (수평 기준 각도)
  horizSpacing: number;   // m (수평 설치 간격)
  preload: number;        // kN (초기 선행재하하중)
  springStiffness: number;// kN/m (축강성)
  freeLength: number;     // m (자유장)
  bondLength: number;     // m (정착장)
  allowableCapacity: number; // kN (허용 내력)
  specName: string;       // ex: "강관 Φ508x9t", "SWPC 12.7mm 4가닥"
  strutSpec?: string;     // 버팀보 규격
  waleSpec?: string;      // 띠장 규격
  unbracedLength?: number;// m (버팀보 비지지/좌굴 길이, ex: 6m)
}

export interface ExcavationStage {
  stage: number;
  name: string;
  excavationDepth: number; // m
  waterTableBehind: number;// m
  waterTableInside: number;// m
  surcharge: number;       // kN/m2
  activeSupports: SupportStage[];
}

export interface NodeResult {
  depth: number;          // m
  displacement: number;   // mm
  rotation: number;       // rad
  bendingMoment: number;  // kNm/m
  shearForce: number;     // kN/m
  earthPressure: number;  // kN/m2
  waterPressure: number;  // kN/m2
  paLimit: number;        // kN/m2
  ppLimit: number;        // kN/m2
  isYielded: boolean;
}

export interface SupportResult {
  supportIndex: number;
  type: SupportType;
  depth: number;
  axialForce: number;     // kN
  allowableForce: number; // kN
  safetyFactor: number;
  isSafe: boolean;
  strutStressRatio?: number; // 버팀보 압축응력비 (실제축력 / 허용축력)
  waleStressRatio?: number;  // 띠장 휨응력비
  waleMoment?: number;       // kNm (띠장 작용 휨모멘트)
}

export interface StabilityResult {
  embedmentSafetyFactor: number;
  isEmbedmentSafe: boolean;
  boilingSafetyFactor: number;
  isBoilingSafe: boolean;
  heavingSafetyFactor: number;
  isHeavingSafe: boolean;
  pipingSafetyFactor: number;
  isPipingSafe: boolean;
  maxMoment: number;      // kNm/m
  maxDisplacement: number;// mm
  maxShear: number;       // kN/m
  pileStressRatio: number;
  isPileSafe: boolean;
}

export interface StageResult {
  stage: number;
  stageName: string;
  excavationDepth: number;
  nodes: NodeResult[];
  supports: SupportResult[];
  stability: StabilityResult;
}

export interface CostItem {
  name: string;
  quantity: number;
  unit: string;
  unitPrice: number;
  totalPrice: number;
}

export interface AlternativeSpec {
  id: number;
  name: string;
  type: 'ALL_STRUT' | 'ALL_ANCHOR' | 'HYBRID' | 'OPTIMIZED' | 'COMPOSITE_STRUT';
  description: string;
  wall: WallSection;
  supports: SupportStage[];
  stageResults: StageResult[];
  
  maxMoment: number;
  maxDisplacement: number;
  pileStressRatio: number;
  minSupportSF: number;
  embedmentSF: number;
  boilingSF: number;
  heavingSF: number;
  isStructurallySafe: boolean;
  
  wallLengthPerimeter: number;
  costBreakdown: CostItem[];
  totalCostWon: number;
  costPerM: number;
  
  workSpaceScore: number;
  boundaryRiskScore: number;
  constructabilityScore: number;
  periodDays: number;
  overallScore: number;
  rank: number;
}

export interface DeckBeamProp {
  spec: string;
  H: number;
  B: number;
  weight: number; // kg/m
  Zx: number;     // cm3
  Ix: number;     // cm4
  allowBendingCapacity: number; // kNm (KL-510/DB-24 교통하중 검토)
}

export interface DeckingAndKingPostConfig {
  useDecking: boolean;         // 복공판 및 주형보 설치 여부
  trafficLoadType: 'KL-510' | 'DB-24' | 'STANDARD_20KN'; // 도로교 설계기준 교통하중
  trafficLoadValue: number;    // kN/m2 (상재 교통하중)
  deckBeamSpec: string;        // 주형보 규격 (ex: H-400x400x13x21)
  deckBeamSpacing: number;     // m (주형보 종방향 간격, 보통 2.0m)
  kingPostSpec: string;        // 중간말뚝 규격 (ex: H-300x300x10x15)
  kingPostSpacing: number;     // m (중간말뚝 종방향 설치 간격, 보통 2.0m~4.0m)
  kingPostNumRows: number;     // 횡방향 열수 (1열: 중앙, 2열: 3분할 등)
  kingPostTotalLength: number; // m (중간말뚝 총 연장 = 굴착고 + 3~5m 근입)
}

export interface ProjectInputs {
  projectName: string;
  siteLocation: string;
  excavationDepth: number;
  excavationWidth: number;
  totalWallPerimeter: number;
  waterTableBehind: number;
  waterTableInside: number;
  surcharge: number;
  boundaryDistance: number;
  soils: SoilLayer[];
  wall: WallSection;
  supports: SupportStage[];
  deckingConfig?: DeckingAndKingPostConfig; // 복공판, 주형보 및 중간말뚝 설정
}
