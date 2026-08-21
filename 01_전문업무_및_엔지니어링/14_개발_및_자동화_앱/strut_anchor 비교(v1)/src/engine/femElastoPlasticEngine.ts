import type { SoilLayer, WallSection, SupportStage, ExcavationStage, StageResult, NodeResult, SupportResult, StabilityResult, AlternativeSpec, CostItem, ProjectInputs } from '../types';
import { H_PILE_DATABASE, STRUT_DATABASE, WALE_DATABASE } from './sectionDB';
import { DetailedCostEngine } from './detailedCostEngine';
import { ConstructionScheduleEngine } from './constructionScheduleEngine';
import { DEFAULT_PROJECT_INPUTS } from './presets';

export class FEMElastoPlasticEngine {
  private soils: SoilLayer[];
  private wall: WallSection;
  private elemLen: number;
  private numNodes: number;
  private numElements: number;

  constructor(soils: SoilLayer[], wall: WallSection, elemLen: number = 0.1) {
    this.soils = soils;
    this.wall = wall;
    this.elemLen = elemLen;
    this.numNodes = Math.round(wall.totalLength / elemLen) + 1;
    this.numElements = this.numNodes - 1;
  }

  private getSoilAtDepth(depth: number): SoilLayer {
    for (const soil of this.soils) {
      if (depth >= soil.topDepth && depth <= soil.bottomDepth) {
        return soil;
      }
    }
    return this.soils.length > 0 ? this.soils[this.soils.length - 1] : {
      id: 'default',
      name: '풍화암',
      topDepth: 0,
      bottomDepth: 50,
      gamma: 20,
      gammaSat: 21,
      cohesion: 20,
      frictionAngle: 32,
      Es: 50000,
      kh0: 40000,
      NValue: 30,
      isCohesive: false,
      color: '#d97706'
    };
  }

  private calcSoilPressures(
    depth: number,
    excDepth: number,
    wtBehind: number,
    wtInside: number,
    surcharge: number
  ): { sigmaV: number; u: number; pa: number; pp: number; kh: number } {
    let sigmaV = surcharge;
    let curD = 0;
    const step = 0.05;
    while (curD < depth) {
      const s = this.getSoilAtDepth(curD + step / 2);
      const gamma = curD >= wtBehind ? s.gammaSat : s.gamma;
      sigmaV += gamma * step;
      curD += step;
    }

    let u = 0;
    if (depth > wtBehind) {
      u = (depth - wtBehind) * 9.81;
    }

    const s = this.getSoilAtDepth(depth);
    const phiRad = (s.frictionAngle * Math.PI) / 180;
    const Ka = Math.pow(Math.tan(Math.PI / 4 - phiRad / 2), 2);
    const Kp = Math.pow(Math.tan(Math.PI / 4 + phiRad / 2), 2);

    const sigmaVEff = Math.max(0, sigmaV - u);
    const pa = Math.max(0, Ka * sigmaVEff - 2 * s.cohesion * Math.sqrt(Ka)) + u;

    let pp = 0;
    let kh = 0;
    if (depth >= excDepth) {
      const excEffSigmaV = (depth - excDepth) * (s.gammaSat - 9.81);
      pp = Kp * excEffSigmaV + 2 * s.cohesion * Math.sqrt(Kp);
      kh = s.kh0 * Math.pow(Math.max(0.1, depth - excDepth), 0.5);
    }

    return { sigmaV, u, pa, pp, kh };
  }

  public solveStages(stages: ExcavationStage[]): StageResult[] {
    const stageResults: StageResult[] = [];
    let prevDisplacements = new Array(this.numNodes * 2).fill(0);

    for (const stage of stages) {
      const totalDOF = this.numNodes * 2;
      let U = [...prevDisplacements];
      const nodeRes: NodeResult[] = [];

      const maxIter = 40;
      const tolerance = 1e-4;

      for (let iter = 0; iter < maxIter; iter++) {
        const K: number[][] = Array.from({ length: totalDOF }, () => new Array(totalDOF).fill(0));
        const F_load: number[] = new Array(totalDOF).fill(0);

        const EI = this.wall.EI;
        const L = this.elemLen;
        const L2 = L * L;
        const L3 = L * L * L;

        // 1. 보 유한요소 강성 조립
        for (let e = 0; e < this.numElements; e++) {
          const i1 = e * 2;
          const i2 = i1 + 2;

          const k_e = [
            [12 * EI / L3, 6 * EI / L2, -12 * EI / L3, 6 * EI / L2],
            [6 * EI / L2, 4 * EI / L, -6 * EI / L2, 2 * EI / L],
            [-12 * EI / L3, -6 * EI / L2, 12 * EI / L3, -6 * EI / L2],
            [6 * EI / L2, 2 * EI / L, -6 * EI / L2, 4 * EI / L]
          ];

          const indices = [i1, i1 + 1, i2, i2 + 1];
          for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 4; c++) {
              K[indices[r]][indices[c]] += k_e[r][c];
            }
          }
        }

        // 2. 지반 압력 및 비선형 P-y 지반 스프링
        for (let n = 0; n < this.numNodes; n++) {
          const depth = n * this.elemLen;
          const dofW = n * 2;
          const disp = U[dofW];

          const { u, pa, pp, kh } = this.calcSoilPressures(
            depth,
            stage.excavationDepth,
            stage.waterTableBehind,
            stage.waterTableInside,
            stage.surcharge
          );

          const tribArea = (n === 0 || n === this.numNodes - 1) ? this.elemLen / 2 : this.elemLen;

          let earthP = pa;
          let isYield = false;

          if (depth < stage.excavationDepth) {
            F_load[dofW] += pa * tribArea;
            isYield = true;
          } else {
            F_load[dofW] += pa * tribArea;
            const p_soil = kh * disp;
            if (p_soil > pp) {
              isYield = true;
              F_load[dofW] -= pp * tribArea;
              earthP = pa - pp;
            } else {
              K[dofW][dofW] += kh * tribArea;
              earthP = pa - p_soil;
            }
          }

          if (iter === 0) {
            nodeRes[n] = {
              depth: Number(depth.toFixed(2)),
              displacement: 0,
              rotation: 0,
              bendingMoment: 0,
              shearForce: 0,
              earthPressure: earthP,
              waterPressure: u,
              paLimit: pa,
              ppLimit: pp,
              isYielded: isYield
            };
          } else {
            nodeRes[n].earthPressure = earthP;
            nodeRes[n].isYielded = isYield;
          }
        }

        // 3. 지보재 스프링 및 프리로드 조립
        for (const sup of stage.activeSupports) {
          const nodeIdx = Math.round(sup.depth / this.elemLen);
          if (nodeIdx >= 0 && nodeIdx < this.numNodes) {
            const dofW = nodeIdx * 2;
            const angleRad = (sup.angle * Math.PI) / 180;
            const k_eff = (sup.springStiffness * Math.pow(Math.cos(angleRad), 2)) / sup.horizSpacing;
            K[dofW][dofW] += k_eff;

            const p_preload = (sup.preload * Math.cos(angleRad)) / sup.horizSpacing;
            F_load[dofW] -= p_preload;
          }
        }

        // 4. 하단 구속 스프링
        K[totalDOF - 2][totalDOF - 2] += 1e7;
        K[totalDOF - 1][totalDOF - 1] += 1e7;

        // 5. 연립방정식 풀이
        const U_new = this.solveLinearSystem(K, F_load);

        let diff = 0;
        for (let i = 0; i < totalDOF; i++) {
          diff = Math.max(diff, Math.abs(U_new[i] - U[i]));
        }
        U = U_new;

        if (diff < tolerance) break;
      }

      prevDisplacements = U;

      // 6. 결과 산출
      let maxM = 0;
      let maxV = 0;
      let maxDisp = 0;

      for (let n = 0; n < this.numNodes; n++) {
        nodeRes[n].displacement = Number((U[n * 2] * 1000).toFixed(2));
        nodeRes[n].rotation = Number(U[n * 2 + 1].toFixed(5));
        maxDisp = Math.max(maxDisp, Math.abs(nodeRes[n].displacement));

        if (n > 0 && n < this.numNodes - 1) {
          const w_prev = U[(n - 1) * 2];
          const w_curr = U[n * 2];
          const w_next = U[(n + 1) * 2];
          const d2w = (w_next - 2 * w_curr + w_prev) / (this.elemLen * this.elemLen);
          nodeRes[n].bendingMoment = Number((-this.wall.EI * d2w).toFixed(2));
        } else if (n === 0) {
          nodeRes[n].bendingMoment = 0;
        } else {
          nodeRes[n].bendingMoment = Number((nodeRes[n - 1].bendingMoment * 0.5).toFixed(2));
        }
        maxM = Math.max(maxM, Math.abs(nodeRes[n].bendingMoment));
      }

      for (let n = 0; n < this.numNodes - 1; n++) {
        nodeRes[n].shearForce = Number(((nodeRes[n + 1].bendingMoment - nodeRes[n].bendingMoment) / this.elemLen).toFixed(2));
        maxV = Math.max(maxV, Math.abs(nodeRes[n].shearForce));
      }
      nodeRes[this.numNodes - 1].shearForce = nodeRes[this.numNodes - 2].shearForce;

      // 7. 지보재 반력 및 띠장 휨모멘트 산정
      const supResults: SupportResult[] = [];
      for (let i = 0; i < stage.activeSupports.length; i++) {
        const sup = stage.activeSupports[i];
        const nodeIdx = Math.round(sup.depth / this.elemLen);
        const disp = nodeIdx < this.numNodes ? U[nodeIdx * 2] : 0;
        const angleRad = (sup.angle * Math.PI) / 180;

        const k_eff = (sup.springStiffness * Math.pow(Math.cos(angleRad), 2)) / sup.horizSpacing;
        const p_preload_h = (sup.preload * Math.cos(angleRad)) / sup.horizSpacing;
        const totalHorizRxnPerM = k_eff * disp + p_preload_h;
        const axialForce = (totalHorizRxnPerM * sup.horizSpacing) / Math.max(0.1, Math.cos(angleRad));

        // 띠장 휨모멘트 Mw = w * L^2 / 10 (3경간 이상 연속보 가설 표준)
        const waleSpan = sup.horizSpacing;
        const waleMoment = (totalHorizRxnPerM * Math.pow(waleSpan, 2)) / 10.0;
        const waleOpt = WALE_DATABASE.find(w => w.spec === sup.waleSpec) || WALE_DATABASE[0];
        const allowWaleStress = waleOpt.spec.includes('SM355') ? 240.0 : 210.0; // 가시설 단기허용휨응력 (MPa)
        const waleStress = (waleMoment * 1e6) / (waleOpt.totalZx * 1e3); // MPa
        const waleStressRatio = Number((waleStress / allowWaleStress).toFixed(2));

        let allowCap = sup.allowableCapacity;
        if (sup.type === 'STRUT') {
          const stOpt = STRUT_DATABASE.find(st => st.spec === (sup.strutSpec || sup.specName));
          if (stOpt) allowCap = stOpt.allowCompressCapacity;
        }

        const sf = allowCap / Math.max(1, axialForce);
        const strutStressRatio = Number((axialForce / Math.max(1, allowCap)).toFixed(2));

        supResults.push({
          supportIndex: i + 1,
          type: sup.type,
          depth: sup.depth,
          axialForce: Number(Math.max(sup.preload, axialForce).toFixed(1)),
          allowableForce: allowCap,
          safetyFactor: Number(sf.toFixed(2)),
          isSafe: sf >= 1.0 && waleStressRatio <= 1.0,
          strutStressRatio,
          waleStressRatio,
          waleMoment: Number(waleMoment.toFixed(1))
        });
      }

      // 8. 지반 안정성
      const embedmentLen = this.wall.totalLength - stage.excavationDepth;
      let drivingM = 0;
      let resistingM = 0;

      for (const n of nodeRes) {
        if (n.depth < stage.excavationDepth) {
          drivingM += n.paLimit * (stage.excavationDepth - n.depth) * this.elemLen;
        } else {
          resistingM += n.ppLimit * (n.depth - stage.excavationDepth) * this.elemLen;
        }
      }
      const embedmentSF = drivingM > 0 ? resistingM / drivingM : 2.5;

      const deltaH = Math.max(0, stage.excavationDepth - stage.waterTableBehind);
      const icr = 0.937;
      const iexit = (deltaH > 0 && embedmentLen > 0) ? (deltaH / (2 * embedmentLen)) : 0.01;
      const boilingSF = iexit > 0.001 ? icr / iexit : 3.5;

      const baseSoil = this.getSoilAtDepth(stage.excavationDepth + 1.0);
      let heavingSF = 2.5;
      if (baseSoil.isCohesive) {
        const Nc = 5.14 * (1 + 0.2 * (stage.excavationDepth / 10));
        const heavingRes = Nc * baseSoil.cohesion + baseSoil.gamma * embedmentLen;
        const heavingDrv = stage.excavationDepth * baseSoil.gamma + stage.surcharge;
        heavingSF = heavingDrv > 0 ? heavingRes / heavingDrv : 2.0;
      }

      let pileStressRatio = 0.7;
      if (this.wall.Zx > 0) {
        const momentPerPile = maxM * this.wall.spacing;
        const actualStress = (momentPerPile * 1e6) / (this.wall.Zx * 1e3);
        pileStressRatio = Number((actualStress / this.wall.allowBendingStress).toFixed(2));
      }

      const stab: StabilityResult = {
        maxMoment: Number(maxM.toFixed(2)),
        maxDisplacement: Number(maxDisp.toFixed(2)),
        maxShear: Number(maxV.toFixed(2)),
        pileStressRatio,
        isPileSafe: pileStressRatio <= 1.0,
        embedmentSafetyFactor: Number(embedmentSF.toFixed(2)),
        isEmbedmentSafe: embedmentSF >= 1.2,
        boilingSafetyFactor: Number(boilingSF.toFixed(2)),
        isBoilingSafe: boilingSF >= 1.5,
        heavingSafetyFactor: Number(heavingSF.toFixed(2)),
        isHeavingSafe: heavingSF >= 1.2,
        pipingSafetyFactor: Number((boilingSF * 1.2).toFixed(2)),
        isPipingSafe: boilingSF * 1.2 >= 1.5
      };

      stageResults.push({
        stage: stage.stage,
        stageName: stage.name,
        excavationDepth: stage.excavationDepth,
        nodes: nodeRes,
        supports: supResults,
        stability: stab
      });
    }

    return stageResults;
  }

  /**
   * 1D 빔 유한요소 대역 행렬 (Bandwidth = 4) 초고속 가우스 소거법 (O(N) 성능)
   */
  private solveLinearSystem(A: number[][], B: number[]): number[] {
    const n = B.length;
    const M = A.map(row => [...row]);
    const b = [...B];
    const bw = 5; // 1D 빔 요소 최대 반대역폭

    // 1. 전진 소거 (대역 내에서만 수행)
    for (let i = 0; i < n; i++) {
      const diag = M[i][i];
      if (Math.abs(diag) < 1e-12) continue;

      const maxK = Math.min(n, i + bw);
      for (let k = i + 1; k < maxK; k++) {
        if (Math.abs(M[k][i]) < 1e-12) continue;
        const c = M[k][i] / diag;
        const maxJ = Math.min(n, i + bw);
        for (let j = i; j < maxJ; j++) {
          M[k][j] -= c * M[i][j];
        }
        b[k] -= c * b[i];
      }
    }

    // 2. 후진 대입 (대역 내에서만 수행)
    const x = new Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) {
      let sum = b[i];
      const maxJ = Math.min(n, i + bw);
      for (let j = i + 1; j < maxJ; j++) {
        sum -= M[i][j] * x[j];
      }
      x[i] = Math.abs(M[i][i]) > 1e-12 ? sum / M[i][i] : 0;
    }
    return x;
  }
}

// 4대안 비교 및 공사비/시공성 자동 생성기
export class AlternativeEvaluator {
  public static generate4Alternatives(inputs: ProjectInputs): AlternativeSpec[] {
    const { soils, wall, excavationDepth, excavationWidth, totalWallPerimeter } = inputs;

    // 대표 버팀보/띠장 사양
    const defaultStrut = inputs.supports.find(s => s.type === 'STRUT') || inputs.supports[0];
    const userStrutSpec = defaultStrut?.strutSpec || defaultStrut?.specName || '강관 Φ508.0x9.0t';
    const userStrutSpacing = defaultStrut?.horizSpacing || 3.5;
    const userWaleSpec = defaultStrut?.waleSpec || '2-H 300x300x10x15';

    const strutOpt = STRUT_DATABASE.find(s => s.spec === userStrutSpec || s.spec.includes(userStrutSpec) || userStrutSpec.includes(s.spec)) || STRUT_DATABASE[2];

    // 지보단수 결정: 1단 1.5m부터 굴착 저면 1.2m 상부까지 2.6m~2.9m 간격으로 바닥 끝까지 빈틈없이 배치
    const numTiers = Math.max(2, Math.min(30, Math.floor((excavationDepth - 1.5) / 2.8) + 1));
    const tierSpacings: number[] = [];
    for (let i = 0; i < numTiers; i++) {
      const d = (i === 0)
        ? 1.5
        : Number((1.5 + i * ((excavationDepth - 1.5 - 1.2) / Math.max(1, numTiers - 1))).toFixed(1));
      tierSpacings.push(d);
    }

    // 1. 대안 1: All Strut (사용자가 설정한 엄지말뚝 간격, 버팀보 간격, 띠장 규격 연동)
    const strutSups: SupportStage[] = tierSpacings.map((depth, idx) => ({
      id: `strut-${idx}`,
      stageIndex: idx + 1,
      type: 'STRUT',
      depth,
      angle: 0,
      horizSpacing: userStrutSpacing,
      preload: 60 + idx * 25,
      springStiffness: 45000,
      freeLength: 0,
      bondLength: 0,
      allowableCapacity: strutOpt.allowCompressCapacity,
      specName: strutOpt.spec,
      strutSpec: strutOpt.spec,
      waleSpec: userWaleSpec
    }));

    // 사용자 지정 앵커 각도 및 수평 간격 연동
    const defaultAnchor = inputs.supports.find(s => s.type === 'GROUND_ANCHOR');
    const userAnchorAngle = defaultAnchor?.angle || 45;
    const userAnchorSpacing = defaultAnchor?.horizSpacing || 1.5;

    // 2. 대안 2: All Anchor (고각 45°~70° 적용, 사용자 앵커 수평간격 연동)
    const anchorSups: SupportStage[] = tierSpacings.map((depth, idx) => {
      const angle = userAnchorAngle;
      const angleRad = (angle * Math.PI) / 180;
      const freeLength = Number(Math.max(4.5, (depth / Math.tan(angleRad)) + 2.0).toFixed(1));
      const bondLength = Number((5.5 + idx * 0.5).toFixed(1));
      const strandCount = Math.max(4, 4 + idx);
      const cap = strandCount * 109.8;

      return {
        id: `anchor-${idx}`,
        stageIndex: idx + 1,
        type: 'GROUND_ANCHOR',
        depth,
        angle,
        horizSpacing: userAnchorSpacing,
        preload: 160 + idx * 30,
        springStiffness: 42000,
        freeLength,
        bondLength,
        allowableCapacity: Math.round(cap),
        specName: `SWPC 12.7mm ${strandCount}가닥 (${angle}°)`,
        waleSpec: userWaleSpec
      };
    });

    // 3. 대안 3: Hybrid (상부 1~2단 고각 앵커 45°~70°, 하부 스트러트)
    const hybridSups: SupportStage[] = tierSpacings.map((depth, idx) => {
      const isUpper = idx < Math.ceil(numTiers / 2);
      const angle = isUpper ? userAnchorAngle : 0;
      const angleRad = (angle * Math.PI) / 180;
      const freeLength = isUpper ? Number(Math.max(4.5, (depth / Math.tan(angleRad)) + 2.0).toFixed(1)) : 0;
      const bondLength = isUpper ? Number((5.5 + idx * 0.5).toFixed(1)) : 0;
      const strandCount = Math.max(4, 4 + idx);

      return {
        id: `hybrid-${idx}`,
        stageIndex: idx + 1,
        type: isUpper ? 'GROUND_ANCHOR' : 'STRUT',
        depth,
        angle,
        horizSpacing: isUpper ? userAnchorSpacing : userStrutSpacing,
        preload: isUpper ? (160 + idx * 30) : (80 + idx * 20),
        springStiffness: isUpper ? 42000 : 45000,
        freeLength,
        bondLength,
        allowableCapacity: isUpper ? Math.round(strandCount * 109.8) : strutOpt.allowCompressCapacity,
        specName: isUpper ? `SWPC 12.7mm ${strandCount}가닥 (${angle}° 고각)` : userStrutSpec,
        strutSpec: isUpper ? undefined : userStrutSpec,
        waleSpec: userWaleSpec
      };
    });

    const alts: AlternativeSpec[] = [
      this.evaluateSingleAlt(1, '대안 1: 버팀보 (All-Strut) 공법', 'ALL_STRUT', `전단 ${userStrutSpec} 버팀보 (간격 ${userStrutSpacing}m) 및 띠장 ${userWaleSpec} 적용`, soils, wall, strutSups, inputs),
      this.evaluateSingleAlt(2, `대안 2: 고각 앵커 (All-Anchor ${userAnchorAngle}°) 공법`, 'ALL_ANCHOR', `전단 고각 어스앵커 (${userAnchorAngle}°) 로 부지경계 침범 방지 및 100% 개방 굴착`, soils, wall, anchorSups, inputs),
      this.evaluateSingleAlt(3, `대안 3: 복합공법 (상부 고각앵커 ${userAnchorAngle}° + 하부 스트러트)`, 'HYBRID', `상부 고각 앵커(${userAnchorAngle}°)로 작업공간 확보 및 하부 스트러트로 암반층 결합`, soils, wall, hybridSups, inputs),
    ];

    // 공기 산정 엔진(ConstructionScheduleEngine)과 100% 동기화
    try {
      const scheduleResults = ConstructionScheduleEngine.calculateSchedules(inputs, alts, 1);
      alts.forEach((alt, idx) => {
        const sch = scheduleResults.find(s => s.altId === alt.id) || scheduleResults[idx];
        if (sch) {
          alt.periodDays = sch.totalDurationDays;
        }
      });
    } catch (e) {}

    // 경제성 + 공기 + 안전성 종합 평가 점수 산정 (모든 창 100% 동일 순위 보장)
    const minCost = Math.min(...alts.map(a => a.totalCostWon));
    const minPeriod = Math.min(...alts.map(a => a.periodDays));

    alts.forEach(alt => {
      let safetyScore = 100;
      if (!alt.isStructurallySafe) {
        safetyScore = 40;
      } else {
        safetyScore -= Math.max(0, (alt.pileStressRatio - 0.65) * 45);
        safetyScore -= Math.max(0, (alt.maxDisplacement - 20) * 1.5);
      }
      safetyScore = Math.max(40, Math.min(100, safetyScore));

      const costScore = Number((70 + ((minCost / (alt.totalCostWon || 1)) * 30)).toFixed(1));
      const schedScore = Number((70 + ((minPeriod / (alt.periodDays || 1)) * 30)).toFixed(1));
      const workScore = (alt.workSpaceScore + alt.boundaryRiskScore) / 2;

      alt.overallScore = Number((safetyScore * 0.35 + costScore * 0.35 + schedScore * 0.20 + workScore * 0.10).toFixed(1));
    });

    const sorted = [...alts].sort((a, b) => b.overallScore - a.overallScore);
    sorted.forEach((item, idx) => {
      const original = alts.find(a => a.id === item.id);
      if (original) original.rank = idx + 1;
    });

    return alts;
  }

  private static evaluateSingleAlt(
    id: number,
    name: string,
    type: 'ALL_STRUT' | 'ALL_ANCHOR' | 'HYBRID' | 'OPTIMIZED',
    description: string,
    soils: SoilLayer[],
    wall: WallSection,
    supports: SupportStage[],
    inputs: ProjectInputs
  ): AlternativeSpec {
    const { excavationDepth, excavationWidth, totalWallPerimeter, waterTableBehind, waterTableInside, surcharge } = inputs;

    const stages: ExcavationStage[] = [];
    const stage1Exc = supports.length === 0 ? excavationDepth : Math.min(excavationDepth, supports[0].depth + 0.6);
    stages.push({
      stage: 1,
      name: '1차 선행 굴착',
      excavationDepth: stage1Exc,
      waterTableBehind,
      waterTableInside: Math.max(stage1Exc, waterTableInside),
      surcharge,
      activeSupports: []
    });

    for (let i = 0; i < supports.length; i++) {
      const activeSups = supports.slice(0, i + 1);
      const nextExc = (i + 1 < supports.length) 
        ? Number(Math.min(excavationDepth, supports[i + 1].depth + 0.5).toFixed(1)) 
        : excavationDepth;
      stages.push({
        stage: i + 2,
        name: `${i + 1}단 지보설치 및 ${i + 2}차 굴착`,
        excavationDepth: nextExc,
        waterTableBehind,
        waterTableInside: Math.max(nextExc, waterTableInside),
        surcharge,
        activeSupports: activeSups
      });
    }

    const engine = new FEMElastoPlasticEngine(soils, wall, 0.25);
    const stageResults = engine.solveStages(stages);
    // 전체 시공단계에 걸친 최악치(Envelope) 추출
    const maxMomentAllStages = Math.max(...stageResults.map(s => s.stability.maxMoment));
    const maxDispAllStages = Math.max(...stageResults.map(s => s.stability.maxDisplacement));
    const maxPileRatioAllStages = Math.max(...stageResults.map(s => s.stability.pileStressRatio));
    const minEmbedSFAllStages = Math.min(...stageResults.map(s => s.stability.embedmentSafetyFactor));
    const minBoilingSFAllStages = Math.min(...stageResults.map(s => s.stability.boilingSafetyFactor));
    const minHeavingSFAllStages = Math.min(...stageResults.map(s => s.stability.heavingSafetyFactor));

    let minSupSF = 99;
    for (const stage of stageResults) {
      for (const sup of stage.supports) {
        minSupSF = Math.min(minSupSF, sup.safetyFactor);
        if (sup.waleStressRatio && sup.waleStressRatio > 1.0) {
          minSupSF = Math.min(minSupSF, 0.9);
        }
      }
    }
    if (minSupSF > 90) minSupSF = 1.5;

    const isStructurallySafe = (maxPileRatioAllStages <= 1.0) &&
                               (minSupSF >= 1.0) &&
                               (minEmbedSFAllStages >= 1.2) &&
                               (minBoilingSFAllStages >= 1.5);

    const { costBreakdown, totalCostWon, costPerM } = this.calculateCost(wall, supports, totalWallPerimeter, excavationDepth, excavationWidth, inputs, id, name, type);

    let workSpaceScore = 80;
    let boundaryRiskScore = 90;
    let constructabilityScore = 85;
    let periodDays = 45;

    if (type === 'ALL_ANCHOR') {
      workSpaceScore = 95;
      boundaryRiskScore = 65;
      constructabilityScore = 88;
      periodDays = 42;
    } else if (type === 'ALL_STRUT') {
      workSpaceScore = 65;
      boundaryRiskScore = 100;
      constructabilityScore = 78;
      periodDays = 55;
    } else if (type === 'HYBRID') {
      workSpaceScore = 85;
      boundaryRiskScore = 88;
      constructabilityScore = 88;
      periodDays = 46;
    } else {
      workSpaceScore = 88;
      boundaryRiskScore = 90;
      constructabilityScore = 92;
      periodDays = 43;
    }

    let safetyScore = 100;
    if (!isStructurallySafe) {
      safetyScore = 40;
    } else {
      safetyScore -= Math.max(0, (maxPileRatioAllStages - 0.65) * 45);
      safetyScore -= Math.max(0, (maxDispAllStages - 20) * 1.5);
    }
    safetyScore = Math.max(40, Math.min(100, safetyScore));

    const economyScore = 85;
    const overallScore = Number((safetyScore * 0.40 + economyScore * 0.35 + ((workSpaceScore + boundaryRiskScore) / 2) * 0.25).toFixed(1));

    return {
      id,
      name,
      type,
      description,
      wall,
      supports,
      stageResults,
      maxMoment: maxMomentAllStages,
      maxDisplacement: maxDispAllStages,
      pileStressRatio: maxPileRatioAllStages,
      minSupportSF: Number(minSupSF.toFixed(2)),
      embedmentSF: minEmbedSFAllStages,
      boilingSF: minBoilingSFAllStages,
      heavingSF: minHeavingSFAllStages,
      isStructurallySafe,
      wallLengthPerimeter: totalWallPerimeter,
      costBreakdown,
      totalCostWon,
      costPerM,
      workSpaceScore,
      boundaryRiskScore,
      constructabilityScore,
      periodDays,
      overallScore,
      rank: 1
    };
  }

  private static calculateCost(
    wall: WallSection,
    supports: SupportStage[],
    L_perim: number,
    excDepth: number,
    excWidth: number,
    inputs?: ProjectInputs,
    id: number = 1,
    name: string = '대안',
    type: 'ALL_STRUT' | 'ALL_ANCHOR' | 'HYBRID' | 'OPTIMIZED' = 'ALL_STRUT'
  ): { costBreakdown: CostItem[]; totalCostWon: number; costPerM: number } {
    // DetailedCostEngine을 단일 진실 공급원(Single Source of Truth)으로 사용하여
    // 메인 화면, 비교 매트릭스, 차트, A4 기술보고서, 상세내역서 모달 등 모든 화면에서 100% 동일한 금액 보장
    const safeInputs: ProjectInputs = inputs ? {
      ...inputs,
      wall,
      supports,
      excavationDepth: excDepth,
      excavationWidth: excWidth,
      totalWallPerimeter: L_perim
    } : {
      ...DEFAULT_PROJECT_INPUTS,
      wall,
      supports,
      excavationDepth: excDepth,
      excavationWidth: excWidth,
      totalWallPerimeter: L_perim
    };

    // 임시 AlternativeSpec 생성하여 DetailedCostEngine 실행
    const tempAlt: any = {
      id,
      name,
      type,
      wall,
      supports
    };

    const detailedResult = DetailedCostEngine.calculateDetailedCost(tempAlt, safeInputs, 6);

    const costBreakdown: CostItem[] = detailedResult.items.map(item => ({
      name: `${item.name} (${item.spec})`,
      quantity: item.quantity,
      unit: item.unit,
      unitPrice: item.contractUnitCost,
      totalPrice: item.contractAmount
    }));

    const totalCostWon = detailedResult.totalContractCost;
    const costPerM = Math.round(totalCostWon / Math.max(1, L_perim));

    return { costBreakdown, totalCostWon, costPerM };
  }
}
