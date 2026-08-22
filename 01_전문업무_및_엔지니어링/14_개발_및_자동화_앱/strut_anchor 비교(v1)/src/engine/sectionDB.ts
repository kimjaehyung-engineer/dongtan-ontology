import { HPileSectionProp, StrutSectionProp, WaleSectionProp } from '../types';

// 1. 엄지말뚝 H-Pile 표준 단면 DB (단면계수 Zx 오름차순 정렬)
export const H_PILE_DATABASE: HPileSectionProp[] = [
  { spec: 'H-298x201x9x14', H: 298, B: 201, t1: 9, t2: 14, weight: 65.4, A: 83.3, Ix: 11300, Zx: 756, rx: 11.6 },
  { spec: 'H-396x199x7x11', H: 396, B: 199, t1: 7, t2: 11, weight: 56.6, A: 72.16, Ix: 20000, Zx: 1010, rx: 16.6 },
  { spec: 'H-300x300x10x15', H: 300, B: 300, t1: 10, t2: 15, weight: 94.0, A: 119.8, Ix: 20400, Zx: 1360, rx: 13.1 },
  { spec: 'H-350x350x12x19', H: 350, B: 350, t1: 12, t2: 19, weight: 137.0, A: 173.9, Ix: 40300, Zx: 2300, rx: 15.2 },
  { spec: 'H-400x400x13x21', H: 400, B: 400, t1: 13, t2: 21, weight: 172.0, A: 218.7, Ix: 66600, Zx: 3330, rx: 17.5 },
];

// 2. 버팀보 Strut 표준 단면 DB (허용압축내력 오름차순 정렬)
export const STRUT_DATABASE: StrutSectionProp[] = [
  { spec: '강관 Φ406.4x9.0t', type: 'PIPE', diameterOrH: 406.4, thickness: 9.0, weight: 88.2, A: 112.4, Ix: 22100, rx: 14.0, allowCompressCapacity: 850 },
  { spec: 'H-300x300x10x15 (Strut)', type: 'H_BEAM', diameterOrH: 300, thickness: 15, weight: 94.0, A: 119.8, Ix: 20400, rx: 13.1, allowCompressCapacity: 920 },
  { spec: '강관 Φ508.0x9.0t', type: 'PIPE', diameterOrH: 508.0, thickness: 9.0, weight: 110.8, A: 141.1, Ix: 44000, rx: 17.6, allowCompressCapacity: 1250 },
  { spec: 'H-350x350x12x19 (Strut)', type: 'H_BEAM', diameterOrH: 350, thickness: 19, weight: 137.0, A: 173.9, Ix: 40300, rx: 15.2, allowCompressCapacity: 1480 },
  { spec: '강관 Φ508.0x12.0t', type: 'PIPE', diameterOrH: 508.0, thickness: 12.0, weight: 146.8, A: 187.0, Ix: 57200, rx: 17.5, allowCompressCapacity: 1680 },
  { spec: '합성사각 4-Box 400형', type: 'COMPOSITE_SQUARE', diameterOrH: 400.0, thickness: 9.0, weight: 108.0, A: 137.6, Ix: 42500, rx: 17.6, allowCompressCapacity: 2050 },
  { spec: '합성사각 4-Box 450형', type: 'COMPOSITE_SQUARE', diameterOrH: 450.0, thickness: 12.0, weight: 125.0, A: 159.2, Ix: 62800, rx: 19.9, allowCompressCapacity: 2620 },
  { spec: '강관 Φ609.6x12.0t', type: 'PIPE', diameterOrH: 609.6, thickness: 12.0, weight: 176.8, A: 225.3, Ix: 101000, rx: 21.2, allowCompressCapacity: 2250 },
  { spec: '합성사각 4-Box 500형', type: 'COMPOSITE_SQUARE', diameterOrH: 500.0, thickness: 14.0, weight: 145.0, A: 184.7, Ix: 88600, rx: 21.9, allowCompressCapacity: 3180 },
  { spec: '강관 Φ711.2x14.0t', type: 'PIPE', diameterOrH: 711.2, thickness: 14.0, weight: 240.7, A: 306.6, Ix: 187000, rx: 24.7, allowCompressCapacity: 3100 },
  { spec: '강관 Φ812.8x14.0t', type: 'PIPE', diameterOrH: 812.8, thickness: 14.0, weight: 275.8, A: 351.3, Ix: 280000, rx: 28.2, allowCompressCapacity: 3800 },
  { spec: '강관 Φ812.8x16.0t', type: 'PIPE', diameterOrH: 812.8, thickness: 16.0, weight: 314.4, A: 400.5, Ix: 318000, rx: 28.1, allowCompressCapacity: 4300 },
];

// 3. 띠장 Wale 단면 DB (단면계수 오름차순 정렬)
export const WALE_DATABASE: WaleSectionProp[] = [
  // 1열 띠장
  { spec: '1-H 298x201x9x14', hSpec: 'H-298x201x9x14', numBeams: 1, totalZx: 756, totalIx: 11300, weight: 65.4 },
  { spec: '1-H 300x300x10x15', hSpec: 'H-300x300x10x15', numBeams: 1, totalZx: 1360, totalIx: 20400, weight: 94.0 },
  { spec: '1-H 350x350x12x19', hSpec: 'H-350x350x12x19', numBeams: 1, totalZx: 2300, totalIx: 40300, weight: 137.0 },
  { spec: '1-H 400x400x13x21', hSpec: 'H-400x400x13x21', numBeams: 1, totalZx: 3330, totalIx: 66600, weight: 172.0 },

  // 2열 띠장
  { spec: '2-H 298x201x9x14', hSpec: 'H-298x201x9x14', numBeams: 2, totalZx: 1512, totalIx: 22600, weight: 130.8 },
  { spec: '2-H 300x300x10x15', hSpec: 'H-300x300x10x15', numBeams: 2, totalZx: 2720, totalIx: 40800, weight: 188.0 },
  { spec: '2-H 350x350x12x19', hSpec: 'H-350x350x12x19', numBeams: 2, totalZx: 4600, totalIx: 80600, weight: 274.0 },
  { spec: '2-H 400x400x13x21', hSpec: 'H-400x400x13x21', numBeams: 2, totalZx: 6660, totalIx: 133200, weight: 344.0 },
  { spec: '2-H 400x400x13x21 (SM355)', hSpec: 'H-400x400x13x21', numBeams: 2, totalZx: 6660, totalIx: 133200, weight: 344.0 },
  { spec: '2-H 428x407x20x35', hSpec: 'H-428x407x20x35', numBeams: 2, totalZx: 10600, totalIx: 212000, weight: 566.0 },
];

// 4. 주형보(Deck Beam) 표준 단면 DB (교통하중 지지 거더)
export const DECK_BEAM_DATABASE = [
  { spec: 'H-400x400x13x21', H: 400, B: 400, weight: 172.0, Zx: 3330, Ix: 66600, allowBendingCapacity: 466 },
  { spec: 'H-500x200x10x16', H: 500, B: 200, weight: 89.6, Zx: 1910, Ix: 47800, allowBendingCapacity: 267 },
  { spec: 'H-350x350x12x19', H: 350, B: 350, weight: 137.0, Zx: 2300, Ix: 40300, allowBendingCapacity: 322 },
  { spec: 'H-300x300x10x15', H: 300, B: 300, weight: 94.0, Zx: 1360, Ix: 20400, allowBendingCapacity: 190 },
];

// 5. 토류판 DB (목재, 강재, 숏크리트)
export const LAGGING_DATABASE = [
  // 목재 토류판 (낙엽송)
  { name: '낙엽송 목재 토류판 (t=6.0cm)', thickness: 60, allowStress: 10.0, type: 'WOOD' },
  { name: '낙엽송 목재 토류판 (t=8.0cm)', thickness: 80, allowStress: 10.0, type: 'WOOD' },
  { name: '낙엽송 목재 토류판 (t=10.0cm)', thickness: 100, allowStress: 10.0, type: 'WOOD' },

  // 강재 토류판 (Steel Lagging / 라이닝 플레이트)
  { name: '강재 토류판 절곡형 (t=6.0mm, SS275)', thickness: 6, allowStress: 210.0, type: 'STEEL', weight: 47.1 },
  { name: '강재 토류판 절곡형 (t=8.0mm, SS275)', thickness: 8, allowStress: 210.0, type: 'STEEL', weight: 62.8 },
  { name: '강재 라이닝 플레이트 (t=10.0mm, SS275)', thickness: 10, allowStress: 210.0, type: 'STEEL', weight: 78.5 },
  { name: '강재 토류판 절곡형 (t=8.0mm, 아연도금 방청)', thickness: 8, allowStress: 210.0, type: 'STEEL', weight: 64.5 },

  // 숏크리트 라이닝
  { name: '숏크리트 + 와이어메쉬 (t=15.0cm)', thickness: 150, allowStress: 15.0, type: 'SHOTCRETE' },
];
