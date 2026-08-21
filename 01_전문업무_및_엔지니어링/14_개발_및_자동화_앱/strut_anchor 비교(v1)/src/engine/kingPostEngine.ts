import { DeckingAndKingPostConfig, ProjectInputs, SoilLayer } from '../types';
import { H_PILE_DATABASE } from './sectionDB';

export interface KingPostCheckResult {
  spec: string;
  spacing: number;            // m
  tributaryWidth: number;     // m (굴착폭 / 2)
  tributaryArea: number;      // m2 (지배면적)
  deadLoad: number;           // kN (복공판 + 주형보 자중)
  trafficLoad: number;        // kN (KL-510 or DB-24 활하중)
  totalDesignLoad: number;    // kN (총 설계축하중 P_act)
  unbracedLength: number;     // m (좌굴 비지지길이 L_k)
  radiusGyrationMin: number;  // cm (약축 회전반경 ry)
  slendernessRatio: number;   // 세장비 lambda = Lk / ry
  isSlendernessSafe: boolean; // lambda <= 150
  allowableCompressStress: number; // MPa (허용압축응력 sigma_ca)
  allowableAxialCapacity: number;  // kN (허용축력 P_all = sigma_ca * A)
  bucklingStressRatio: number;     // 좌굴 응력비 P_act / P_all
  isBucklingSafe: boolean;         // SR <= 1.0
  allowableBearingCapacity: number;// kN (지반 허용지지력 Q_a)
  bearingSafetyFactor: number;     // F.S
  isBearingSafe: boolean;          // Q_a >= P_act
  overallStatus: 'SAFE' | 'WARNING' | 'NG';
  remedyGuide?: string;
}

export class KingPostEngine {
  /**
   * 가시설 설계기준(KDS 21 30 00) 기반 중간말뚝 좌굴 및 지반 지지력 정밀 검토
   */
  public static evaluateKingPost(
    inputs: ProjectInputs,
    decking: DeckingAndKingPostConfig,
    soils: SoilLayer[]
  ): KingPostCheckResult {
    const spec = decking.kingPostSpec || 'H-300x300x10x15';
    const spacing = decking.kingPostSpacing || 3.5;
    const hPileOpt = H_PILE_DATABASE.find(hp => hp.spec.startsWith(spec.split('x')[0])) || H_PILE_DATABASE[0];

    // 1. 지배면적 및 하중 산정
    const tributaryWidth = inputs.excavationWidth / 2.0; // 1열 중간말뚝 기준
    const tributaryArea = tributaryWidth * spacing; // m2

    // 복공판(t=200mm, 약 2.0kN/m2) + 주형보/가로보(약 1.5kN/m2)
    const deadLoadPerM2 = 3.5; // kN/m2
    const deadLoad = Number((deadLoadPerM2 * tributaryArea).toFixed(1));

    // 교통하중 (KL-510: 20.0kN/m2, DB-24: 17.5kN/m2, 20kN: 20.0kN/m2)
    const trafficLoadPerM2 = decking.trafficLoadValue || (decking.trafficLoadType === 'DB-24' ? 17.5 : 20.0);
    const trafficLoad = Number((trafficLoadPerM2 * tributaryArea).toFixed(1));

    const totalDesignLoad = Number((deadLoad + trafficLoad).toFixed(1)); // P_act (kN)

    // 2. 비지지 좌굴길이 (L_k) - 중간말뚝과 스트럿 완전 강결(Rigid Joint) 반영
    // 스트럿과의 강결 거셋/브라켓 결합으로 수평/수직 변위 및 회전 구속
    let maxTierSpacing = 3.2; // m (표준 단간격)
    if (inputs.supports && inputs.supports.length > 1) {
      for (let i = 1; i < inputs.supports.length; i++) {
        const diff = inputs.supports[i].depth - inputs.supports[i - 1].depth;
        if (diff > maxTierSpacing) maxTierSpacing = diff;
      }
    }

    // 스트럿과 강결 체결 시 좌굴 비지지길이 L_k는 최대 단간격 (약 2.7m ~ 3.2m)
    const unbracedLength = Number(maxTierSpacing.toFixed(1));

    // 3. 단면 약축 회전반경 ry 및 세장비 lambda
    // H-300x300x10x15의 공칭 A = 119.8 cm2, ry = 7.51 cm
    const areaCm2 = hPileOpt.A || 119.8; // cm2
    const ryCm = 7.51; // H-300 공칭 약축 회전반경
    const slendernessRatio = Number(((unbracedLength * 100) / ryCm).toFixed(1));
    const isSlendernessSafe = slendernessRatio <= 150.0;

    // 4. 허용 압축응력 sigma_ca (도로교/가설구조물 KDS 21 30 00 기준)
    // SS275 (Fy = 235 MPa)
    // lambda <= 20: sigma_ca = 140 MPa
    // 20 < lambda <= 93: sigma_ca = [140 - 0.82*(lambda - 20)] MPa
    // lambda > 93: sigma_ca = [11,760,000 / (6700 + lambda^2)] MPa
    let sigma_ca = 140.0;
    if (slendernessRatio <= 20) {
      sigma_ca = 140.0;
    } else if (slendernessRatio <= 93) {
      sigma_ca = 140.0 - 0.82 * (slendernessRatio - 20);
    } else {
      sigma_ca = 11760000.0 / (6700.0 + slendernessRatio * slendernessRatio);
    }
    sigma_ca = Number(sigma_ca.toFixed(1));

    // 허용 축력 P_all (kN) = sigma_ca (MPa) * A (cm2) * 0.1
    const allowableAxialCapacity = Number(((sigma_ca * areaCm2) / 10.0).toFixed(1));
    const bucklingStressRatio = Number((totalDesignLoad / Math.max(1.0, allowableAxialCapacity)).toFixed(2));
    const isBucklingSafe = bucklingStressRatio <= 1.0;

    // 5. 지반 선단 및 주면마찰 지지력 (Q_a) 산정 (착저층: N>=50 풍화암/연암 암반 소켓)
    // 도로교 및 구조물기초설계기준 풍화암/연암 선단 극한지지력 q_p = 20,000 kN/m2 (20 MPa)
    const embedLength = Math.max(3.0, (decking.kingPostTotalLength || (inputs.excavationDepth + 5.0)) - inputs.excavationDepth);
    const pilePerimeter = 1.2; // m (H-300 둘레 약 1.2m)
    const pileArea = 0.09;     // m2 (0.3m x 0.3m)

    // 암반 주면마찰력 tau_s = 250 kN/m2, 선단지지력 q_p = 20,000 kN/m2
    const ultimateSkinFriction = 250.0 * pilePerimeter * embedLength; // kN (약 1,500 kN)
    const ultimateEndBearing = 20000.0 * pileArea;                   // kN (약 1,800 kN)
    const ultimateCapacity = ultimateSkinFriction + ultimateEndBearing; // kN (약 3,300 kN)
    
    // 허용지지력 Q_a (안전율 F.S = 2.5 적용)
    const allowableBearingCapacity = Number((ultimateCapacity / 2.5).toFixed(1)); // kN (약 1,320 kN)
    const bearingSafetyFactor = Number((allowableBearingCapacity / Math.max(1.0, totalDesignLoad)).toFixed(2));
    const isBearingSafe = allowableBearingCapacity >= totalDesignLoad;

    let overallStatus: 'SAFE' | 'WARNING' | 'NG' = 'SAFE';
    let remedyGuide: string | undefined = undefined;

    if (!isBucklingSafe || !isSlendernessSafe) {
      overallStatus = 'NG';
      remedyGuide = `중간말뚝 좌굴 응력비 NG (${bucklingStressRatio} > 1.0). 중간말뚝 간격을 ${Math.max(2.0, spacing - 0.5)}m로 축소하거나 H-${hPileOpt.spec}보다 큰 H-350x350 이상으로 상향하세요.`;
    } else if (!isBearingSafe) {
      overallStatus = 'NG';
      remedyGuide = `중간말뚝 지반 지지력 부족 (Qa=${allowableBearingCapacity}kN < Pact=${totalDesignLoad}kN). 암반층 근입장을 ${embedLength + 1.5}m 이상으로 연장하거나 소켓 천공 깊이를 확대하세요.`;
    } else if (bucklingStressRatio > 0.85) {
      overallStatus = 'WARNING';
      remedyGuide = `중간말뚝 좌굴 응력비 한계 도달 (${bucklingStressRatio}). 시공 중 수평 가새(Bracing) 구속을 철저히 확인하세요.`;
    }

    return {
      spec,
      spacing,
      tributaryWidth,
      tributaryArea,
      deadLoad,
      trafficLoad,
      totalDesignLoad,
      unbracedLength,
      radiusGyrationMin: Number(ryCm.toFixed(2)),
      slendernessRatio,
      isSlendernessSafe,
      allowableCompressStress: sigma_ca,
      allowableAxialCapacity,
      bucklingStressRatio,
      isBucklingSafe,
      allowableBearingCapacity,
      bearingSafetyFactor,
      isBearingSafe,
      overallStatus,
      remedyGuide
    };
  }
}
