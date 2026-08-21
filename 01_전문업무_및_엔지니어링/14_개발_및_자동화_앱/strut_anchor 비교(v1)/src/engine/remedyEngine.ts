import { ProjectInputs, AlternativeSpec, SupportStage, WallSection, StageResult } from '../types';
import { H_PILE_DATABASE, STRUT_DATABASE, WALE_DATABASE, LAGGING_DATABASE } from './sectionDB';

export interface RemedyItem {
  id: string;
  type: 'CRITICAL' | 'WARNING' | 'INFO';
  target: 'H_PILE' | 'STRUT' | 'WALE' | 'EMBEDMENT' | 'BOILING' | 'HEAVING' | 'BOUNDARY';
  title: string;
  currentStatus: string;
  criteria: string;
  primarySuggestion: string;
  alternativeOptions: string[];
  autoFixAction?: (inputs: ProjectInputs) => ProjectInputs;
}

export class SmartRemedyEngine {
  public static diagnose(inputs: ProjectInputs, selectedAlt: AlternativeSpec): RemedyItem[] {
    const remedies: RemedyItem[] = [];
    const stages = selectedAlt.stageResults;
    if (!stages || stages.length === 0) return remedies;

    const wall = inputs.wall;
    const defaultStrut = inputs.supports.find(s => s.type === 'STRUT');
    const defaultWale = defaultStrut?.waleSpec || '2-H 300x300x10x15';

    // 1. 전체 시공단계(Stage 1 ~ Final) 중 최대 H-Pile 응력비 및 단계 탐색
    let worstPileStage = stages[0];
    let maxPileRatio = 0;
    for (const stage of stages) {
      if (stage.stability.pileStressRatio > maxPileRatio) {
        maxPileRatio = stage.stability.pileStressRatio;
        worstPileStage = stage;
      }
    }

    if (maxPileRatio > 1.0) {
      // 1. H-Pile 응력비 초과: 목표 응력비 0.85를 달성하는 단면 및 간격 정밀 산정
      const currentZx = wall.Zx || 1360;
      const targetRatio = 0.85;
      const neededZx = currentZx * (maxPileRatio / targetRatio);
      
      let targetHPile = H_PILE_DATABASE.find(h => h.Zx >= neededZx);
      let neededSpacing = wall.spacing || 1.5;
      let useSM355 = false;

      if (!targetHPile) {
        // 최고 규격(H-400x400x13x21, Zx=3330) 적용
        targetHPile = H_PILE_DATABASE[H_PILE_DATABASE.length - 1];
        // 만약 H-400으로도 모자라면 SM355 고강도강(fba=265MPa) 적용
        if (maxPileRatio > 1.2) {
          useSM355 = true;
        }
        const allowStressFactor = useSM355 ? (265.0 / 210.0) : 1.0;
        neededSpacing = Math.max(0.9, Math.min(2.0, Number((neededSpacing * (targetHPile.Zx / neededZx) * allowStressFactor).toFixed(1))));
      }

      const suggestionText = useSM355
        ? `H-Pile 규격을 [${targetHPile.spec} (고강도 SM355강재)] 및 간격 ${neededSpacing}m 로 최적 보정`
        : `H-Pile 규격을 [${targetHPile.spec}] (단면계수 Zx=${targetHPile.Zx}cm³) 및 간격 ${neededSpacing}m 로 최적 보정`;

      remedies.push({
        id: 'rem-hpile-stress',
        type: 'CRITICAL',
        target: 'H_PILE',
        title: `H-Pile 주열벽체 휨응력 초과 (NG) - ${worstPileStage.stageName}`,
        currentStatus: `최대 응력비 ${maxPileRatio} (허용치 대비 ${Math.round((maxPileRatio - 1.0) * 100)}% 초과, 굴착심도 -${Number(worstPileStage.excavationDepth.toFixed(1))}m)`,
        criteria: '허용 휨응력비 ≤ 1.0 (KDS 21 30 00)',
        primarySuggestion: suggestionText,
        alternativeOptions: [
          `1. H-Pile 단면 상향 (${targetHPile.spec}${useSM355 ? ' / SM355 고강도강' : ''})`,
          `2. 엄지말뚝 수평간격 축소 (${wall.spacing}m → ${neededSpacing}m)`,
          `3. 지보 단수 1단 추가로 벽체 최대 지간(Span) 단축`
        ],
        autoFixAction: (prevInputs: ProjectInputs) => {
          const allowBendingStress = useSM355 ? 265.0 : 210.0;
          const targetSp = Math.min(prevInputs.wall.spacing || 1.5, neededSpacing);
          const EI = (2.05e8 * targetHPile!.Ix * 1e-8) / targetSp;
          const EA = (2.05e8 * targetHPile!.A * 1e-4) / targetSp;
          return {
            ...prevInputs,
            wall: {
              ...prevInputs.wall,
              name: `${targetHPile!.spec}${useSM355 ? '(SM355)' : ''} @ ${targetSp}m`,
              hPileSpec: targetHPile!.spec,
              Zx: targetHPile!.Zx,
              spacing: targetSp,
              allowBendingStress,
              EI,
              EA
            }
          };
        }
      });
    }

    // 2. 전체 시공단계 중 버팀보(Strut) 압축좌굴 / 허용축력 초과 단계 탐색
    let worstStrutSup: any = null;
    let worstStrutStageName = '';
    for (const stage of stages) {
      for (const sup of stage.supports) {
        if (sup.type === 'STRUT' && sup.safetyFactor < 1.0) {
          if (!worstStrutSup || sup.safetyFactor < worstStrutSup.safetyFactor) {
            worstStrutSup = sup;
            worstStrutStageName = stage.stageName;
          }
        }
      }
    }

    if (worstStrutSup) {
      const neededCap = worstStrutSup.axialForce * 1.15; // 안전율 1.15 확보 목표
      let targetStrut = STRUT_DATABASE.find(st => st.allowCompressCapacity >= neededCap);
      let targetSpacing = defaultStrut?.horizSpacing || 3.5;

      if (!targetStrut) {
        // 최고 규격 적용 후 간격 축소
        targetStrut = STRUT_DATABASE[STRUT_DATABASE.length - 1];
        targetSpacing = Math.max(2.5, Number((targetSpacing * (targetStrut.allowCompressCapacity / neededCap)).toFixed(1)));
      }

      remedies.push({
        id: 'rem-strut-capacity',
        type: 'CRITICAL',
        target: 'STRUT',
        title: `버팀보 ${worstStrutSup.supportIndex}단 허용압축내력 초과 (NG) - ${worstStrutStageName}`,
        currentStatus: `작용축력 ${worstStrutSup.axialForce} kN > 허용내력 ${worstStrutSup.allowableForce} kN (안전율 ${worstStrutSup.safetyFactor})`,
        criteria: '안전율 FS ≥ 1.0 (허용압축응력 fca 기준)',
        primarySuggestion: `버팀보 규격을 [${targetStrut.spec}] (허용내력 Pa=${targetStrut.allowCompressCapacity}kN) 및 간격 ${targetSpacing}m 로 최적 보정`,
        alternativeOptions: [
          `1. 버팀보 관경/두께 상향 (${targetStrut.spec})`,
          `2. 버팀보 수평 설치 간격 축소 (${defaultStrut?.horizSpacing || 3.5}m → ${targetSpacing}m)`,
          `3. 중간말뚝(King Post) 배치 간격 단축으로 유효좌굴길이 Lk 축소`
        ],
        autoFixAction: (prevInputs: ProjectInputs) => {
          const updatedSups = prevInputs.supports.map(s => {
            if (s.type === 'STRUT') {
              return {
                ...s,
                strutSpec: targetStrut!.spec,
                specName: targetStrut!.spec,
                allowableCapacity: targetStrut!.allowCompressCapacity,
                horizSpacing: targetSpacing
              };
            }
            return s;
          });
          return { ...prevInputs, supports: updatedSups };
        }
      });
    }

    // 3. 전체 시공단계 중 띠장(Wale) 휨응력비 초과 탐색
    let worstWaleSup: any = null;
    let worstWaleStageName = '';
    for (const stage of stages) {
      for (const sup of stage.supports) {
        if (sup.type === 'STRUT' && (sup.waleStressRatio || 0) > 1.0) {
          if (!worstWaleSup || (sup.waleStressRatio || 0) > (worstWaleSup.waleStressRatio || 0)) {
            worstWaleSup = sup;
            worstWaleStageName = stage.stageName;
          }
        }
      }
    }

    if (worstWaleSup) {
      const currentRatio = worstWaleSup.waleStressRatio || 1.2;
      const twoBeamWales = WALE_DATABASE.filter(w => w.numBeams === 2);
      const neededWaleZx = 2720 * (currentRatio / 0.85); // 2-H 300 기본 2720 기준
      
      let targetWale = twoBeamWales.find(w => w.totalZx >= neededWaleZx);
      let targetSpacing = defaultStrut?.horizSpacing || 3.5;

      if (!targetWale) {
        // 최고 규격(2-H 400x400x13x21, 2-Zx=6660) 적용 후 지간 단축
        targetWale = twoBeamWales[twoBeamWales.length - 1];
        targetSpacing = Math.max(2.5, Number((targetSpacing * Math.sqrt(targetWale.totalZx / neededWaleZx)).toFixed(1)));
      }

      remedies.push({
        id: 'rem-wale-stress',
        type: 'CRITICAL',
        target: 'WALE',
        title: `띠장(Wale 2열) 휨응력 초과 (NG) - ${worstWaleStageName}`,
        currentStatus: `띠장 휨응력비 ${worstWaleSup.waleStressRatio} (작용모멘트 Mw=${worstWaleSup.waleMoment} kNm)`,
        criteria: '허용 휨응력비 ≤ 1.0 (2-H 단면계수 2-Zx 기준)',
        primarySuggestion: `띠장 규격을 [${targetWale.spec}] (단면계수 2-Zx=${targetWale.totalZx}cm³) 로 상향 및 간격 ${targetSpacing}m 조율`,
        alternativeOptions: [
          `1. 띠장 2-H 규격 상향 (${targetWale.spec})`,
          `2. 버팀보 수평 간격 축소로 띠장 지간(Span) 단축 (${defaultStrut?.horizSpacing || 3.5}m → ${targetSpacing}m)`,
          `3. 띠장 상하부 플랜지 보강판(Cover Plate) 부착`
        ],
        autoFixAction: (prevInputs: ProjectInputs) => {
          const updatedSups = prevInputs.supports.map(s => {
            if (s.type === 'STRUT') {
              return { ...s, waleSpec: targetWale!.spec, horizSpacing: targetSpacing };
            }
            return s;
          });
          return { ...prevInputs, supports: updatedSups };
        }
      });
    }

    // 4. 전체 시공단계 중 근입장 모멘트 평형 최소 안전율 탐색
    let minEmbedSF = 99;
    let worstEmbedStage = stages[0];
    for (const stage of stages) {
      if (stage.stability.embedmentSafetyFactor < minEmbedSF) {
        minEmbedSF = stage.stability.embedmentSafetyFactor;
        worstEmbedStage = stage;
      }
    }

    if (minEmbedSF < 1.2) {
      const addNeeded = Math.max(2.0, Math.ceil((1.35 - minEmbedSF) * 8.0));
      const neededLength = Number((wall.totalLength + addNeeded).toFixed(1));
      remedies.push({
        id: 'rem-embedment-fs',
        type: 'CRITICAL',
        target: 'EMBEDMENT',
        title: `벽체 근입장 전도 안전율 부족 (NG) - ${worstEmbedStage.stageName}`,
        currentStatus: `근입장 안전율 F.S = ${minEmbedSF} (기준 1.2 미달, 굴착심도 -${worstEmbedStage.excavationDepth}m)`,
        criteria: '수동저항모멘트 / 주동전도모멘트 F.S ≥ 1.2',
        primarySuggestion: `벽체 총 연장을 ${wall.totalLength}m에서 ${neededLength}m로 +${addNeeded}m 연장 (근입장 확보)`,
        alternativeOptions: [
          `1. 벽체 총 연장 증대 (${wall.totalLength}m → ${neededLength}m)`,
          `2. 최하단 지보 설치 위치를 굴착저면 근접 심도로 하향 배치`
        ],
        autoFixAction: (prevInputs: ProjectInputs) => {
          return {
            ...prevInputs,
            wall: {
              ...prevInputs.wall,
              totalLength: neededLength
            }
          };
        }
      });
    }

    // 5. 보일링 안전율 탐색
    let minBoilSF = 99;
    for (const stage of stages) {
      if (stage.stability.boilingSafetyFactor < minBoilSF) {
        minBoilSF = stage.stability.boilingSafetyFactor;
      }
    }

    if (minBoilSF < 1.5) {
      const addBoil = Math.max(2.0, Math.ceil((1.6 - minBoilSF) * 8.0));
      const addEmbed = Number((wall.totalLength + addBoil).toFixed(1));
      remedies.push({
        id: 'rem-boiling-fs',
        type: 'CRITICAL',
        target: 'BOILING',
        title: '굴착저면 보일링(Boiling) 안전율 부족 (NG)',
        currentStatus: `보일링 안전율 F.S = ${minBoilSF} (기준 1.5 미달)`,
        criteria: '한계동수경사 / 출구동수경사 F.S ≥ 1.5',
        primarySuggestion: `벽체 근입장을 +${addBoil}m 추가 관입하여 침투 유선 경로 대폭 연장 (총연장 ${addEmbed}m)`,
        alternativeOptions: [
          `1. 벽체 근입장 추가 관입 (총연장 ${wall.totalLength}m → ${addEmbed}m)`,
          `2. 배면 웰포인트/딥웰 지하수위 저하 공법 병행`,
          `3. 굴착저면 차수 그라우팅(JSP/SCW) 시공`
        ],
        autoFixAction: (prevInputs: ProjectInputs) => {
          return {
            ...prevInputs,
            wall: {
              ...prevInputs.wall,
              totalLength: addEmbed
            }
          };
        }
      });
    }

    // 6. 대지경계선 앵커 침범 경고
    if (selectedAlt.type === 'ALL_ANCHOR' || selectedAlt.type === 'HYBRID') {
      const longestAnchor = selectedAlt.supports.find(s => s.type === 'GROUND_ANCHOR');
      if (longestAnchor) {
        const totalAnchorLen = longestAnchor.freeLength + longestAnchor.bondLength;
        const anchorHorizReach = totalAnchorLen * Math.cos((longestAnchor.angle * Math.PI) / 180);
        if (anchorHorizReach > inputs.boundaryDistance) {
          remedies.push({
            id: 'rem-boundary-encroach',
            type: 'WARNING',
            target: 'BOUNDARY',
            title: '어스앵커 대지경계선 외측 침범 (주의)',
            currentStatus: `앵커 수평도달거리 ${anchorHorizReach.toFixed(1)}m > 부지경계 ${inputs.boundaryDistance}m (침범 ${(anchorHorizReach - inputs.boundaryDistance).toFixed(1)}m)`,
            criteria: '인접 사유지 동의 필요 또는 경계 내 시공 원칙',
            primarySuggestion: '앵커 각도를 20°~25°로 급경사화하거나 복합공법(상부 앵커+하부 스트러트) 또는 All-Strut 대안 채택',
            alternativeOptions: [
              '1. 앵커 설치 각도 급경사화 (15° → 25°)',
              '2. 대안 1 (All-Strut) 또는 대안 3 (Hybrid) 채택으로 민원 방지',
              '3. 인접 도로/사유지 영구/가설 점용 동의서 취득'
            ]
          });
        }
      }
    }

    return remedies;
  }
}
