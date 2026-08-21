import { SoilLayer, SupportStage, WallSection, ProjectInputs } from '../types';

export interface AnchorDesignResult {
  tierIndex: number;
  depth: number;              // m (설치 심도)
  angle: number;              // deg (45° ~ 70°)
  horizSpacing: number;       // m (수평 간격)
  horizReaction: number;      // kN (1본당 수평분담력 Rh * Sh)
  designTension: number;      // kN (소요 인장력 Td = H / cos theta)
  verticalDownForce: number;  // kN (수직 하향력 V = Td * sin theta)
  freeLength: number;         // m (자유장 Lf)
  bondLength: number;         // m (정착장 Lb)
  totalLength: number;        // m (총 앵커 길이 Lf + Lb)
  horizReach: number;         // m (수평 도달거리 = L_tot * cos theta)
  verticalReach: number;      // m (수직 도달심도 = depth + L_tot * sin theta)
  strandCount: number;        // 본 (SWPC 12.7mm 강연선 가닥수)
  strandAllowableTension: number; // kN (0.6 * Pu * n)
  strandStressRatio: number;  // 강연선 응력비 Td / Ta
  soilSkinFriction: number;   // kN/m2 (정착 지층 주면마찰력 tau_a)
  bondSafetyFactor: number;   // 정착장 인발 안전율 F.S
  isBondSafe: boolean;        // FS >= 2.0
  isBoundarySafe: boolean;    // horizReach <= boundaryDistance
  encroachDistance: number;   // m (침범 거리)
  targetSoilName: string;     // 정착층 지반명 (ex: 풍화암/연암)
}

export class HighAngleAnchorEngine {
  // 고각 앵커 표준 각도 목록 (45° ~ 70°, 5° 간격)
  public static readonly AVAILABLE_ANGLES = [45, 50, 55, 60, 65, 70];

  // SWPC 7B 12.7mm 강연선 정수
  public static readonly STRAND_PU = 183.0; // kN (1본당 인장강도)
  public static readonly STRAND_PY = 158.0; // kN (1본당 항복강도)
  public static readonly STRAND_ALLOWABLE_PER_STRAND = 183.0 * 0.6; // 109.8 kN

  public static designSingleAnchor(
    tierIndex: number,
    depth: number,
    angle: number,
    horizSpacing: number,
    horizReactionPerM: number,
    excavationDepth: number,
    soils: SoilLayer[],
    boundaryDistance: number,
    holeDiameter: number = 0.135 // m (천공경 135mm)
  ): AnchorDesignResult {
    const angleRad = (angle * Math.PI) / 180;
    const cosA = Math.cos(angleRad);
    const sinA = Math.sin(angleRad);

    // 1. 설계 인장력 Td 및 수직하향력 V
    const horizReaction = Math.max(80.0, horizReactionPerM * horizSpacing);
    const designTension = Number((horizReaction / Math.max(0.1, cosA)).toFixed(1));
    const verticalDownForce = Number((designTension * sinA).toFixed(1));

    // 2. 가상 파괴면 및 자유장 Lf 산정
    // 지표면 기준 주동파괴각 theta_a = 45 + phi/2 (평균 phi = 30° -> 60°)
    const phiAvg = 32.0;
    const failureAngleRad = ((45 + phiAvg / 2) * Math.PI) / 180;
    const wallBottomDist = (excavationDepth - depth) / Math.tan(failureAngleRad);
    // 앵커선과 파괴면의 교점까지 거리 + 안전이격 1.5m
    const minLf = Math.max(4.5, (wallBottomDist / Math.max(0.1, cosA)) + 1.5);
    const freeLength = Number(minLf.toFixed(1));

    // 3. 정착층 도달 심도 및 주면마찰력 tau_a 산정
    const midBondDepth = depth + (freeLength + 2.5) * sinA;
    let targetSoil: SoilLayer = soils[soils.length - 1];
    for (const s of soils) {
      if (midBondDepth >= s.topDepth && midBondDepth <= s.bottomDepth) {
        targetSoil = s;
        break;
      }
    }

    // 지반별 극한 주면마찰력 산정 (고각 앵커 특성상 하부 풍화암/연암 착저)
    let tau_ult = 150.0; // kN/m2
    if (targetSoil.name.includes('연암') || targetSoil.name.includes('경암') || targetSoil.frictionAngle >= 40) {
      tau_ult = 600.0; // 암반 정착
    } else if (targetSoil.name.includes('풍화암') || targetSoil.NValue >= 50) {
      tau_ult = 400.0;
    } else if (targetSoil.name.includes('풍화토') || targetSoil.NValue >= 25) {
      tau_ult = 180.0;
    } else {
      tau_ult = Math.max(80.0, targetSoil.NValue * 12.0);
    }

    // 4. 소요 정착장 Lb 산정 (FS = 2.0)
    const fs = 2.0;
    const circ = Math.PI * holeDiameter;
    const reqLb = (designTension * fs) / (circ * tau_ult);
    const bondLength = Number(Math.max(3.5, Math.min(9.5, reqLb)).toFixed(1));

    const totalLength = Number((freeLength + bondLength).toFixed(1));
    const horizReach = Number((totalLength * cosA).toFixed(1));
    const verticalReach = Number((depth + totalLength * sinA).toFixed(1));

    // 5. PC강연선 가닥수 n 결정
    const strandCount = Math.max(3, Math.ceil(designTension / this.STRAND_ALLOWABLE_PER_STRAND));
    const strandAllowableTension = Number((strandCount * this.STRAND_ALLOWABLE_PER_STRAND).toFixed(1));
    const strandStressRatio = Number((designTension / strandAllowableTension).toFixed(2));

    // 6. 정착력 안전율 및 부지경계 검토
    const actCapacity = (circ * tau_ult * bondLength);
    const bondSafetyFactor = Number((actCapacity / Math.max(1.0, designTension)).toFixed(2));
    const isBondSafe = bondSafetyFactor >= 2.0;

    const isBoundarySafe = horizReach <= boundaryDistance;
    const encroachDistance = Number(Math.max(0, horizReach - boundaryDistance).toFixed(1));

    return {
      tierIndex,
      depth,
      angle,
      horizSpacing,
      horizReaction,
      designTension,
      verticalDownForce,
      freeLength,
      bondLength,
      totalLength,
      horizReach,
      verticalReach,
      strandCount,
      strandAllowableTension,
      strandStressRatio,
      soilSkinFriction: tau_ult,
      bondSafetyFactor,
      isBondSafe,
      isBoundarySafe,
      encroachDistance,
      targetSoilName: targetSoil.name
    };
  }
}
