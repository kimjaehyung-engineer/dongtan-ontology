import { ProjectInputs, SoilLayer, WallSection, SupportStage } from '../types';

export const DEFAULT_SOILS: SoilLayer[] = [
  {
    id: 'soil-1',
    name: '매립층 (Fill)',
    topDepth: 0.0,
    bottomDepth: 3.0,
    gamma: 18.0,
    gammaSat: 19.0,
    cohesion: 5.0,
    frictionAngle: 26.0,
    Es: 15000,
    kh0: 12000,
    NValue: 8,
    isCohesive: false,
    color: '#94a3b8'
  },
  {
    id: 'soil-2',
    name: '풍화토 (Weathered Soil)',
    topDepth: 3.0,
    bottomDepth: 8.0,
    gamma: 19.0,
    gammaSat: 20.0,
    cohesion: 12.0,
    frictionAngle: 30.0,
    Es: 35000,
    kh0: 25000,
    NValue: 25,
    isCohesive: false,
    color: '#d97706'
  },
  {
    id: 'soil-3',
    name: '풍화암 (Weathered Rock)',
    topDepth: 8.0,
    bottomDepth: 14.0,
    gamma: 21.0,
    gammaSat: 22.0,
    cohesion: 30.0,
    frictionAngle: 35.0,
    Es: 80000,
    kh0: 60000,
    NValue: 50,
    isCohesive: false,
    color: '#78350f'
  },
  {
    id: 'soil-4',
    name: '연암 (Soft Rock)',
    topDepth: 14.0,
    bottomDepth: 25.0,
    gamma: 24.0,
    gammaSat: 25.0,
    cohesion: 100.0,
    frictionAngle: 40.0,
    Es: 250000,
    kh0: 150000,
    NValue: 50,
    isCohesive: false,
    color: '#475569'
  }
];

export const DEFAULT_WALL: WallSection = {
  id: 'wall-1',
  name: 'H-300x300x10x15 @ 1.5m',
  type: 'H_PILE',
  spacing: 1.5,
  EI: (2.05e8 * 20400.0 * 1e-8) / 1.5, // ~27,880 kNm2/m
  EA: (2.05e8 * 119.8 * 1e-4) / 1.5,
  Zx: 1360.0,
  totalLength: 17.0,
  yieldStrength: 235.0,
  allowBendingStress: 140.0,
  hPileSpec: 'H-300x300x10x15',
  laggingType: '낙엽송 목재 토류판 (t=8.0cm)',
  laggingThickness: 80
};

export const DEFAULT_SUPPORTS: SupportStage[] = [
  {
    id: 'sup-1',
    stageIndex: 1,
    type: 'STRUT',
    depth: 1.5,
    angle: 0,
    horizSpacing: 3.5,
    preload: 60,
    springStiffness: 45000,
    freeLength: 0,
    bondLength: 0,
    allowableCapacity: 1250,
    specName: '강관 Φ508.0x9.0t',
    strutSpec: '강관 Φ508.0x9.0t',
    waleSpec: '2-H 300x300x10x15',
    unbracedLength: 6.0
  },
  {
    id: 'sup-2',
    stageIndex: 2,
    type: 'STRUT',
    depth: 4.5,
    angle: 0,
    horizSpacing: 3.5,
    preload: 80,
    springStiffness: 45000,
    freeLength: 0,
    bondLength: 0,
    allowableCapacity: 1250,
    specName: '강관 Φ508.0x9.0t',
    strutSpec: '강관 Φ508.0x9.0t',
    waleSpec: '2-H 300x300x10x15',
    unbracedLength: 6.0
  },
  {
    id: 'sup-3',
    stageIndex: 3,
    type: 'STRUT',
    depth: 7.5,
    angle: 0,
    horizSpacing: 3.5,
    preload: 100,
    springStiffness: 45000,
    freeLength: 0,
    bondLength: 0,
    allowableCapacity: 1250,
    specName: '강관 Φ508.0x9.0t',
    strutSpec: '강관 Φ508.0x9.0t',
    waleSpec: '2-H 300x300x10x15',
    unbracedLength: 6.0
  },
  {
    id: 'sup-4',
    stageIndex: 4,
    type: 'STRUT',
    depth: 10.0,
    angle: 0,
    horizSpacing: 3.5,
    preload: 100,
    springStiffness: 45000,
    freeLength: 0,
    bondLength: 0,
    allowableCapacity: 1250,
    specName: '강관 Φ508.0x9.0t',
    strutSpec: '강관 Φ508.0x9.0t',
    waleSpec: '2-H 300x300x10x15',
    unbracedLength: 6.0
  }
];

export const DEFAULT_PROJECT_INPUTS: ProjectInputs = {
  projectName: '가시설 벽체 지지공법(Strut vs Anchor) 사전 최적설계',
  siteLocation: '도심지 본선 개착구간 가시설 현장',
  excavationDepth: 12.0,
  excavationWidth: 18.0,
  totalWallPerimeter: 120.0,
  soils: DEFAULT_SOILS,
  wall: DEFAULT_WALL,
  supports: DEFAULT_SUPPORTS,
  waterTableBehind: 3.0,
  waterTableInside: 12.0,
  surcharge: 20.0,
  boundaryDistance: 8.0,
  deckingConfig: {
    useDecking: true,
    trafficLoadType: 'KL-510',
    trafficLoadValue: 20.0,
    deckBeamSpec: 'H-400x400x13x21',
    deckBeamSpacing: 2.0,
    kingPostSpec: 'H-300x300x10x15',
    kingPostSpacing: 3.5,
    kingPostNumRows: 1,
    kingPostTotalLength: 17.0
  }
};

export const SITE_PRESETS: { name: string; desc: string; data: Partial<ProjectInputs> }[] = [
  {
    name: '1. 도심지 일반 복합지반 (12m 굴착)',
    desc: '매립토 3m + 풍화토 5m + 풍화암 6m + 연암 착저 표준 단면',
    data: {
      excavationDepth: 12.0,
      excavationWidth: 18.0,
      totalWallPerimeter: 120.0,
      waterTableBehind: 3.0,
      surcharge: 20.0,
      boundaryDistance: 12.0,
      soils: DEFAULT_SOILS,
      wall: DEFAULT_WALL
    }
  },
  {
    name: '2. 연약 점토층 우세 지반 (10m 굴착 / 히빙 검토)',
    desc: '상부 8m 실트질 점토층 (c=28kN/m2, phi=0), 히빙 및 변위 집중',
    data: {
      excavationDepth: 10.0,
      excavationWidth: 15.0,
      totalWallPerimeter: 100.0,
      waterTableBehind: 2.0,
      surcharge: 15.0,
      boundaryDistance: 15.0,
      soils: [
        { id: 's1', name: '매립층', topDepth: 0, bottomDepth: 2, gamma: 17, gammaSat: 18, cohesion: 5, frictionAngle: 24, Es: 12000, kh0: 10000, NValue: 5, isCohesive: false, color: '#94a3b8' },
        { id: 's2', name: '연약점토층', topDepth: 2, bottomDepth: 8, gamma: 17.5, gammaSat: 18.5, cohesion: 28, frictionAngle: 0, Es: 10000, kh0: 8000, NValue: 4, isCohesive: true, color: '#38bdf8' },
        { id: 's3', name: '풍화토', topDepth: 8, bottomDepth: 13, gamma: 19, gammaSat: 20, cohesion: 15, frictionAngle: 30, Es: 35000, kh0: 25000, NValue: 25, isCohesive: false, color: '#d97706' },
        { id: 's4', name: '풍화암', topDepth: 13, bottomDepth: 22, gamma: 21, gammaSat: 22, cohesion: 35, frictionAngle: 35, Es: 90000, kh0: 70000, NValue: 50, isCohesive: false, color: '#78350f' },
      ],
      wall: {
        id: 'wall-clay',
        name: 'H-350x350x12x19 @ 1.5m',
        type: 'H_PILE',
        spacing: 1.5,
        EI: (2.05e8 * 40300.0 * 1e-8) / 1.5,
        EA: (2.05e8 * 173.9 * 1e-4) / 1.5,
        Zx: 2300.0,
        totalLength: 16.0,
        yieldStrength: 235.0,
        allowBendingStress: 140.0,
        hPileSpec: 'H-350x350x12x19',
        laggingType: '낙엽송 목재 토류판 (t=10.0cm)',
        laggingThickness: 100
      }
    }
  },
  {
    name: '3. 대심도 굴착 (18m 굴착 / 지하 5층 규모)',
    desc: '굴착깊이 18m, H-400 단면, 지하수위 강하 및 다단 복합 지보',
    data: {
      excavationDepth: 18.0,
      excavationWidth: 24.0,
      totalWallPerimeter: 180.0,
      waterTableBehind: 4.0,
      surcharge: 25.0,
      boundaryDistance: 16.0,
      soils: [
        { id: 's1', name: '매립층', topDepth: 0, bottomDepth: 3, gamma: 18, gammaSat: 19, cohesion: 5, frictionAngle: 26, Es: 15000, kh0: 12000, NValue: 8, isCohesive: false, color: '#94a3b8' },
        { id: 's2', name: '풍화토', topDepth: 3, bottomDepth: 9, gamma: 19, gammaSat: 20, cohesion: 15, frictionAngle: 32, Es: 40000, kh0: 30000, NValue: 30, isCohesive: false, color: '#d97706' },
        { id: 's3', name: '풍화암', topDepth: 9, bottomDepth: 16, gamma: 22, gammaSat: 23, cohesion: 40, frictionAngle: 36, Es: 100000, kh0: 80000, NValue: 50, isCohesive: false, color: '#78350f' },
        { id: 's4', name: '연암/경암', topDepth: 16, bottomDepth: 30, gamma: 25, gammaSat: 26, cohesion: 120, frictionAngle: 42, Es: 300000, kh0: 200000, NValue: 50, isCohesive: false, color: '#475569' },
      ],
      wall: {
        id: 'wall-deep',
        name: 'H-400x400x13x21 @ 1.8m',
        type: 'H_PILE',
        spacing: 1.8,
        EI: (2.05e8 * 66600.0 * 1e-8) / 1.8,
        EA: (2.05e8 * 218.7 * 1e-4) / 1.8,
        Zx: 3330.0,
        totalLength: 24.0,
        yieldStrength: 235.0,
        allowBendingStress: 140.0,
        hPileSpec: 'H-400x400x13x21',
        laggingType: '숏크리트 + 와이어메쉬 (t=15.0cm)',
        laggingThickness: 150
      }
    }
  },
  {
    name: '4. 인접 건물 근접 협소 부지 (앵커 경계 침범 제한)',
    desc: '부지경계 이격거리 4m로 앵커 자유장 침범 제한, Strut 및 하이브리드 추천',
    data: {
      excavationDepth: 11.0,
      excavationWidth: 14.0,
      totalWallPerimeter: 90.0,
      waterTableBehind: 3.5,
      surcharge: 30.0,
      boundaryDistance: 4.0,
      soils: DEFAULT_SOILS,
      wall: DEFAULT_WALL
    }
  }
];
