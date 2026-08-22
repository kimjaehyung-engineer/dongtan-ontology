import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import { ProjectInputs, AlternativeSpec } from '../../types';
import { AlternativeSpanScheduleResult, SpanDailyState } from '../../engine/structureScheduleEngine';
import { 
  Box, 
  Layers, 
  RotateCw, 
  ZoomIn, 
  ZoomOut, 
  Eye, 
  Maximize2, 
  Sun, 
  Sparkles, 
  Play, 
  Pause, 
  RotateCcw,
  CheckCircle2,
  Clock,
  Compass,
  Move,
  Info,
  Sliders,
  Flame,
  ShieldCheck,
  AlertTriangle,
  Navigation,
  User
} from 'lucide-react';

interface DigitalTwin3DViewerProps {
  inputs: ProjectInputs;
  selectedAlt: AlternativeSpec;
  schedule: AlternativeSpanScheduleResult;
  dailyStates: SpanDailyState[];
  currentDay: number;
  onDayChange?: (day: number) => void;
  selectedSpanIdx: number;
  onSelectSpan: (idx: number) => void;
}

// 3D 점 및 투영 구조체
interface Point3D {
  x: number; // 종방향 (길이 0 ~ L)
  y: number; // 횡방향 (폭 -B/2 ~ +B/2)
  z: number; // 연직방향 (0: GL, -H: 굴착바닥)
}

interface Point2D {
  x: number;
  y: number;
  depth: number;
}

export const DigitalTwin3DViewer: React.FC<DigitalTwin3DViewerProps> = ({
  inputs,
  selectedAlt,
  schedule,
  dailyStates,
  currentDay,
  onDayChange,
  selectedSpanIdx,
  onSelectSpan
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // 3D 카메라 궤도 파라미터
  const [yaw, setYaw] = useState<number>(38); // 방위각 (deg)
  const [pitch, setPitch] = useState<number>(26); // 앙각 (deg)
  const [zoom, setZoom] = useState<number>(1.15); // 줌 배율
  const [panX, setPanX] = useState<number>(0);
  const [panY, setPanY] = useState<number>(0);

  // 4D 재생 컨트롤러 상태
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playSpeed, setPlaySpeed] = useState<number>(0.5); // 기본 0.5x (슬로우모션), 1x, 2x, 4x

  // 렌더링 필터 옵션
  const [showExcavationGround, setShowExcavationGround] = useState<boolean>(true);
  const [showShoringStruts, setShowShoringStruts] = useState<boolean>(true);
  const [showRcStructure, setShowRcStructure] = useState<boolean>(true);
  const [showKingPosts, setShowKingPosts] = useState<boolean>(true);
  const [autoRotate, setAutoRotate] = useState<boolean>(false);

  // 🌟 시점 모드 (외부 조감도 vs 1인칭 사람 내부 시점 vs 단면 투시)
  const [viewMode, setViewMode] = useState<'orbit' | 'first_person' | 'xray'>('orbit');
  const [walkX, setWalkX] = useState<number>(0); // 1인칭 보행 X 위치
  const [walkStory, setWalkStory] = useState<number>(0); // 0: B2층, 1: B1층

  // 마우스 인터랙션 상태
  const isDraggingRef = useRef<boolean>(false);
  const lastMousePosRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const mouseButtonRef = useRef<number>(0);

  const L = schedule.totalLengthM || 120; // 총 연장 (120m)
  const B = inputs.excavationWidth || 20; // 본체 폭 (20m)
  const H = inputs.excavationDepth || 15; // 굴착 깊이 (15m)
  const numSpans = schedule.numSpans || 6;
  const spanLength = schedule.spanLengthM || 20;
  const totalDays = schedule.totalDurationDays || 100;
  const isAnchor = selectedAlt.type === 'ALL_ANCHOR';
  const isHybrid = selectedAlt.type === 'HYBRID';
  const isCompStrut = selectedAlt.type === 'COMPOSITE_STRUT';

  // 🌟 완공 후 차량 10초 쇼케이스 타이머 레프
  const completedHoldTimerRef = useRef<any>(null);
  const [trafficCountdown, setTrafficCountdown] = useState<number | null>(null);
  const [animFrame, setAnimFrame] = useState<number>(0);

  // 1인칭 사람 시점 전환 시 스팬 위치 동기화
  useEffect(() => {
    setWalkX(selectedSpanIdx * spanLength + spanLength / 2);
  }, [selectedSpanIdx, spanLength]);

  // 차량 주행 부드러운 렌더 루프 (도로 포장 완료 시 상시 애니메이션 구동)
  useEffect(() => {
    let reqId: number;
    const loop = () => {
      setAnimFrame(prev => (prev + 1) % 100000);
      reqId = requestAnimationFrame(loop);
    };
    reqId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(reqId);
  }, []);

  // 4D 자동 재생 타이머 (완공 시 10초간 차량 주행 관람 후 자동 정지)
  useEffect(() => {
    if (!isPlaying) {
      if (completedHoldTimerRef.current) {
        clearTimeout(completedHoldTimerRef.current);
        completedHoldTimerRef.current = null;
      }
      setTrafficCountdown(null);
      return;
    }

    // 최종 완공 일차 도달 시
    if (currentDay >= totalDays) {
      if (!completedHoldTimerRef.current) {
        let remainingSec = 10;
        setTrafficCountdown(remainingSec);

        const countdownInterval = setInterval(() => {
          remainingSec -= 1;
          if (remainingSec > 0) {
            setTrafficCountdown(remainingSec);
          } else {
            clearInterval(countdownInterval);
          }
        }, 1000);

        completedHoldTimerRef.current = setTimeout(() => {
          setIsPlaying(false);
          setTrafficCountdown(null);
          clearInterval(countdownInterval);
          completedHoldTimerRef.current = null;
        }, 10000); // 🌟 정확히 10초 동안 주행 후 자동 정지
      }
      return;
    }

    const intervalMs = Math.max(100, Math.round(500 / playSpeed));
    const interval = setInterval(() => {
      if (onDayChange) {
        onDayChange(currentDay + 1);
      }
    }, intervalMs);

    return () => clearInterval(interval);
  }, [isPlaying, currentDay, totalDays, playSpeed, onDayChange]);

  // 3D -> 2D 투영 변환 함수 (외부 조감도 vs 1인칭 사람 내부 시점)
  const project3D = useCallback((pt: Point3D, width: number, height: number): Point2D => {
    let cx = 0;
    let cy = 0;
    let cz = 0;
    let cameraDist = 220 / zoom;
    let fov = 380;

    if (viewMode === 'first_person') {
      // 🚶 1인칭 사람 시점: 사람 눈높이 (바닥 위 1.6m) 기준
      const storyH = (H - 5.0 - 1.8) / 2;
      const eyeZ = -H + 1.8 + walkStory * storyH + 1.6; // 사람 눈높이 EL
      cx = pt.x - walkX;
      cy = pt.y - 0; // 중심 통로 (Y=0)
      cz = pt.z - eyeZ;
      fov = 500;
      cameraDist = 12.0; // 사람 시각 광각 렌즈
    } else {
      // 🌐 3D 외부 조감도 시점: 전체 구조물 중심 기준
      cx = pt.x - L / 2;
      cy = pt.y;
      cz = pt.z + H / 2;
      fov = 380;
      cameraDist = 220 / zoom;
    }

    const radYaw = (yaw * Math.PI) / 180;
    const radPitch = (pitch * Math.PI) / 180;

    // Yaw 수평 회전
    const x1 = cx * Math.cos(radYaw) - cy * Math.sin(radYaw);
    const y1 = cx * Math.sin(radYaw) + cy * Math.cos(radYaw);
    const z1 = cz;

    // Pitch 상하 앙각 회전
    const x2 = x1;
    const y2 = y1 * Math.cos(radPitch) - z1 * Math.sin(radPitch);
    const z2 = y1 * Math.sin(radPitch) + z1 * Math.cos(radPitch);

    // 원근 투영 (Perspective)
    const effectiveDepth = viewMode === 'first_person' ? Math.max(0.5, cameraDist + y2) : Math.max(1, cameraDist + y2);
    const scale = (fov / effectiveDepth) * (viewMode === 'first_person' ? 1.0 : zoom);

    const screenX = width / 2 + x2 * scale + (viewMode === 'first_person' ? 0 : panX);
    const screenY = height / 2 - z2 * scale + (viewMode === 'first_person' ? 0 : panY);

    return { x: screenX, y: screenY, depth: y2 };
  }, [viewMode, walkX, walkStory, yaw, pitch, zoom, panX, panY, L, H]);

  // 마우스 이벤트 핸들러
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    isDraggingRef.current = true;
    lastMousePosRef.current = { x: e.clientX, y: e.clientY };
    mouseButtonRef.current = e.button;
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDraggingRef.current) return;
    const dx = e.clientX - lastMousePosRef.current.x;
    const dy = e.clientY - lastMousePosRef.current.y;
    lastMousePosRef.current = { x: e.clientX, y: e.clientY };

    if (mouseButtonRef.current === 0 && !e.shiftKey) {
      setYaw(prev => (prev + dx * 0.5 + 360) % 360);
      setPitch(prev => Math.max(-85, Math.min(85, prev - dy * 0.5)));
    } else {
      if (viewMode === 'first_person') {
        // 1인칭에서 마우스 우클릭 드래그는 앞뒤 보행 이동
        setWalkX(prev => Math.max(2, Math.min(L - 2, prev - dy * 0.1)));
      } else {
        setPanX(prev => prev + dx);
        setPanY(prev => prev + dy);
      }
    }
  };

  // 키보드 보행 이벤트 (W, S, A, D 또는 방향키)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (viewMode !== 'first_person') return;
      if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
        setWalkX(prev => Math.min(L - 2, prev + 2.0)); // 2m 전진
      } else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
        setWalkX(prev => Math.max(2, prev - 2.0)); // 2m 후진
      } else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
        setYaw(prev => (prev - 10 + 360) % 360); // 좌회전
      } else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
        setYaw(prev => (prev + 10) % 360); // 우회전
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [viewMode, L]);

  const handleMouseUp = () => {
    isDraggingRef.current = false;
  };

  // 줌인 / 줌아웃 함수 (+ - 버튼 연동)
  const handleZoomIn = () => {
    setZoom(prev => Math.min(3.5, Number((prev * 1.2).toFixed(2))));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(0.4, Number((prev / 1.2).toFixed(2))));
  };

  const handleZoomReset = () => {
    setZoom(1.15);
    setPanX(0);
    setPanY(0);
  };

  // 마우스 휠 스크롤은 페이지 스크롤 간섭 방지를 위해 비활성화
  const handleWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    // 휠 줌 비활성화 (버튼 전용)
  };

  // 자동 회전 타이머
  useEffect(() => {
    if (!autoRotate) return;
    const interval = setInterval(() => {
      setYaw(prev => (prev + 0.3) % 360);
    }, 30);
    return () => clearInterval(interval);
  }, [autoRotate]);

  // 3D 씬 그리기 렌더 루프
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // 1. 배경 클리어 (다크 테크니컬 BIM 그라디언트)
    const bgGrad = ctx.createLinearGradient(0, 0, 0, height);
    bgGrad.addColorStop(0, '#090d16');
    bgGrad.addColorStop(1, '#020617');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, width, height);

    // 2. 바닥 그리드 (Ground Grid at EL -H)
    ctx.strokeStyle = 'rgba(71, 85, 105, 0.25)';
    ctx.lineWidth = 1;
    const gridStep = 10;
    for (let gx = -20; gx <= L + 20; gx += gridStep) {
      const p1 = project3D({ x: gx, y: -B * 1.6, z: -H }, width, height);
      const p2 = project3D({ x: gx, y: B * 1.6, z: -H }, width, height);
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();
    }
    for (let gy = -B * 1.6; gy <= B * 1.6; gy += gridStep) {
      const p1 = project3D({ x: -20, y: gy, z: -H }, width, height);
      const p2 = project3D({ x: L + 20, y: gy, z: -H }, width, height);
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();
    }

    // 3. 지표면 기준선 (GL 0.0m 테두리 및 상부 토피 5m 경계)
    const gl1 = project3D({ x: 0, y: -B / 2 - 1.5, z: 0 }, width, height);
    const gl2 = project3D({ x: L, y: -B / 2 - 1.5, z: 0 }, width, height);
    const gl3 = project3D({ x: L, y: B / 2 + 1.5, z: 0 }, width, height);
    const gl4 = project3D({ x: 0, y: B / 2 + 1.5, z: 0 }, width, height);

    ctx.strokeStyle = 'rgba(56, 189, 248, 0.45)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(gl1.x, gl1.y);
    ctx.lineTo(gl2.x, gl2.y);
    ctx.lineTo(gl3.x, gl3.y);
    ctx.lineTo(gl4.x, gl4.y);
    ctx.closePath();
    ctx.stroke();
    ctx.setLineDash([]);

    // 4. 흙막이 H-Pile 엄지말뚝 & 토류판 벽체 (되메우기 시 위로 슝슝 인발 애니메이션)
    const pileSpacing = 1.8;
    const numPiles = Math.floor(L / pileSpacing);

    // 되메우기 태스크 연동 인발 진행률 계산
    const backfillTask = schedule?.tasks.find(t => t.type === 'backfill');
    const isBackfilling = backfillTask && currentDay >= backfillTask.startDay;
    const isBackfillFinished = backfillTask && currentDay >= backfillTask.endDay;
    const backfillExtractProg = isBackfilling
      ? Math.min(1.0, (currentDay - backfillTask.startDay) / Math.max(1, backfillTask.durationDays))
      : 0;

    if (showExcavationGround && !isBackfillFinished) {
      [-B / 2, B / 2].forEach((wallY) => {
        // H-Pile 기둥 실시간 인발 (위로 슝슝 뽑아올림)
        for (let i = 0; i <= numPiles; i++) {
          const px = Math.min(L, i * pileSpacing);
          
          // 말뚝별 시차를 둔 다이내믹 슝슝 인발 오프셋
          let liftZ = 0;
          let isExtractedOut = false;

          if (isBackfilling) {
            const pilePhase = (i / numPiles);
            const pileExtractFactor = Math.max(0, Math.min(1.0, (backfillExtractProg * 1.5 - pilePhase * 0.5)));
            // 위로 최대 25m까지 슝 솟구쳐서 지상 밖으로 인양
            liftZ = pileExtractFactor * (H * 1.8);
            if (pileExtractFactor >= 0.98) isExtractedOut = true;
          }

          if (!isExtractedOut) {
            const topP = project3D({ x: px, y: wallY, z: liftZ }, width, height);
            const botP = project3D({ x: px, y: wallY, z: -H * 1.35 + liftZ }, width, height);

            // 인발 중일 때는 황금색/주황색으로 빛나며 굵어짐
            ctx.strokeStyle = isBackfilling ? '#f59e0b' : 'rgba(217, 119, 6, 0.65)';
            ctx.lineWidth = isBackfilling ? 3.0 : 2.5;
            ctx.beginPath();
            ctx.moveTo(topP.x, topP.y);
            ctx.lineTo(botP.x, botP.y);
            ctx.stroke();

            // 슝슝 위로 뽑혀 올라가는 크레인 와이어 & 인발 모션 라인
            if (isBackfilling && liftZ > 0.5) {
              const craneTopP = project3D({ x: px, y: wallY, z: liftZ + 8.0 }, width, height);
              ctx.strokeStyle = 'rgba(254, 240, 138, 0.7)';
              ctx.lineWidth = 1.2;
              ctx.setLineDash([2, 2]);
              ctx.beginPath();
              ctx.moveTo(topP.x, topP.y);
              ctx.lineTo(craneTopP.x, craneTopP.y);
              ctx.stroke();
              ctx.setLineDash([]);
            }
          }
        }

        // 토류판 판넬 면 (되메우기 전까지만 잔류)
        if (!isBackfilling) {
          const w1 = project3D({ x: 0, y: wallY, z: 0 }, width, height);
          const w2 = project3D({ x: L, y: wallY, z: 0 }, width, height);
          const w3 = project3D({ x: L, y: wallY, z: -H }, width, height);
          const w4 = project3D({ x: 0, y: wallY, z: -H }, width, height);

          ctx.fillStyle = wallY < 0 ? 'rgba(180, 83, 9, 0.16)' : 'rgba(180, 83, 9, 0.08)';
          ctx.beginPath();
          ctx.moveTo(w1.x, w1.y);
          ctx.lineTo(w2.x, w2.y);
          ctx.lineTo(w3.x, w3.y);
          ctx.lineTo(w4.x, w4.y);
          ctx.closePath();
          ctx.fill();
        }
      });

      // 🌟 엄지말뚝 인발 중 단 1개의 대표 3D 안내 배지
      if (isBackfilling && !isBackfillFinished) {
        const midP = project3D({ x: L / 2, y: 0, z: 4.0 }, width, height);
        ctx.fillStyle = '#f59e0b';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText('🏗️ [Phase 4] 되메우기 & 엄지말뚝(H-Pile) 지상 인발 회수 중 ⬆️', midP.x - 145, midP.y - 10);
      }
    }

    // 5. 🌟 가시설 지보재 (버팀보 & 어스앵커) 3D 렌더링 (콘크리트 타설 전 내부 위치)
    if (showShoringStruts) {
      selectedAlt.supports.forEach((sup, tierIdx) => {
        const supZ = -sup.depth;
        const strutSpacing = isCompStrut ? 5.0 : 4.0;
        const numStruts = Math.floor(L / strutSpacing);

        if (isAnchor || (isHybrid && sup.type === 'GROUND_ANCHOR')) {
          // 어스앵커 경사체 (배면 정착장 사선 3D)
          const anchorAngleRad = (sup.angle * Math.PI) / 180;
          const freeLen = sup.freeLength || 10;
          const bondLen = sup.bondLength || 8;
          const totalLen = freeLen + bondLen;

          for (let i = 0; i <= numStruts; i++) {
            const sx = i * strutSpacing;
            const headL = project3D({ x: sx, y: -B / 2, z: supZ }, width, height);
            const tipL = project3D({ 
              x: sx, 
              y: -B / 2 - totalLen * Math.cos(anchorAngleRad), 
              z: supZ - totalLen * Math.sin(anchorAngleRad) 
            }, width, height);

            ctx.strokeStyle = 'rgba(16, 185, 129, 0.85)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(headL.x, headL.y);
            ctx.lineTo(tipL.x, tipL.y);
            ctx.stroke();

            const headR = project3D({ x: sx, y: B / 2, z: supZ }, width, height);
            const tipR = project3D({ 
              x: sx, 
              y: B / 2 + totalLen * Math.cos(anchorAngleRad), 
              z: supZ - totalLen * Math.sin(anchorAngleRad) 
            }, width, height);

            ctx.beginPath();
            ctx.moveTo(headR.x, headR.y);
            ctx.lineTo(tipR.x, tipR.y);
            ctx.stroke();
          }
        } else {
          // 강관 버팀보 (스팬별 실시간 순차 절단/해체 전까지 100% 굳건히 가시화)
          for (let i = 0; i <= numStruts; i++) {
            const sx = i * strutSpacing;
            const spanIdx = Math.min(numSpans - 1, Math.floor(sx / spanLength));
            const spanState = dailyStates[spanIdx];
            
            // 해당 스팬의 해당 단 버팀보 절단/해체 여부 정밀 확인
            const numStories = spanState?.storyStates?.length || 2;
            const storyH = (H - 5.0 - 1.8) / numStories;
            // 버팀보 높이에 대응하는 스토리 인덱스
            const matchedStoryIdx = Math.min(numStories - 1, Math.max(0, Math.floor((supZ - (-H + 1.8)) / storyH)));
            const matchedStory = spanState?.storyStates?.[matchedStoryIdx];
            const matchedWProg = matchedStory ? (matchedStory.wallProgress > 1 ? matchedStory.wallProgress / 100 : matchedStory.wallProgress) : 0;

            // 🌟 [핵심] 굴착, 기초, 외벽 1단 타설 중(matchedWProg <= 0.50)에는 버팀보가 무조건 100% 선명하게 보임!
            // 1단 타설이 끝나고 산소 절단/해체 단계(0.50 ~ 0.54)를 거쳐 2단 타설이 시작될 때(> 0.54) 비로소 해체 완료됨
            const isCuttingDeTensioning = matchedWProg >= 0.48 && matchedWProg <= 0.54; // 산소 절단 & 잭 감압 중
            const isStrutFullyRemoved = matchedStory?.strutReleased || matchedWProg > 0.54 || spanState?.strutReleaseStatus === 'released';

            if (!isStrutFullyRemoved) {
              const pLeft = project3D({ x: sx, y: -B / 2, z: supZ }, width, height);
              const pRight = project3D({ x: sx, y: B / 2, z: supZ }, width, height);

              // 산소 절단 및 볼트 해체 중이면 주황/황금빛 점멸 효과
              if (isCuttingDeTensioning) {
                ctx.strokeStyle = (Date.now() % 400 < 200) ? '#f59e0b' : '#ef4444';
                ctx.lineWidth = isCompStrut ? 5 : 4;
              } else {
                ctx.strokeStyle = isCompStrut ? '#4f46e5' : '#ef4444';
                ctx.lineWidth = isCompStrut ? 4 : 3;
              }

              ctx.beginPath();
              ctx.moveTo(pLeft.x, pLeft.y);
              ctx.lineTo(pRight.x, pRight.y);
              ctx.stroke();

              // 띠장 (Wale) 브라켓
              ctx.fillStyle = '#b91c1c';
              ctx.fillRect(pLeft.x - 2.5, pLeft.y - 2.5, 5, 5);
              ctx.fillRect(pRight.x - 2.5, pRight.y - 2.5, 5, 5);
            }
          }
        }
      });
    }

    // 6. 🌟 중간말뚝 (King Post) 3D 렌더링 (모든 구조물 축조 완료 전까지 100% 굳건히 지속 가시화)
    if (showKingPosts && !isAnchor) {
      const kingPostSpacing = 4.0;
      const numKingPosts = Math.floor(L / kingPostSpacing);

      for (let i = 0; i <= numKingPosts; i++) {
        const kx = i * kingPostSpacing;
        
        // 🌟 [핵심] 모든 구조물 축조가 100% 완료되고 되메우기(Phase 4) 단계에 진입하기 전까지는 중간말뚝 100% 계속 유지!
        const isExtracted = isBackfilling || isBackfillFinished;

        if (!isExtracted) {
          const topP = project3D({ x: kx, y: 0, z: 0 }, width, height);
          const botP = project3D({ x: kx, y: 0, z: -H * 1.35 }, width, height);

          // 굵은 3D H형강 중간말뚝 (주황/황금빛)
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 3.5;
          ctx.beginPath();
          ctx.moveTo(topP.x, topP.y);
          ctx.lineTo(botP.x, botP.y);
          ctx.stroke();

          // 중간말뚝 중심 하이라이트선
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.moveTo(topP.x, topP.y);
          ctx.lineTo(botP.x, botP.y);
          ctx.stroke();
        }
      }
    }

    // 🌟 글로벌 3D 씬 렌더 큐 (Global Scene Depth Sort - 6개 스팬 전체의 깊이를 일괄 정렬하여 면 뒤집힘/투명 비침 완전 박멸)
    type SceneFace = {
      pts: Point2D[];
      color: string;
      avgDepth: number;
      strokeColor: string;
      strokeWidth: number;
    };

    const sceneFaces: SceneFace[] = [];

    const addBox3D = (
      x1: number, x2: number,
      y1: number, y2: number,
      z1: number, z2: number,
      colors: { top: string; front: string; side: string; back?: string; bottom?: string },
      strokeColor = '#0f172a',
      strokeWidth = 1.6
    ) => {
      if (z2 <= z1 || x2 <= x1 || y2 <= y1) return;

      const rawFaces = [
        // 1. 상면 (+Z)
        { rawPts: [{ x: x1, y: y1, z: z2 }, { x: x2, y: y1, z: z2 }, { x: x2, y: y2, z: z2 }, { x: x1, y: y2, z: z2 }], color: colors.top },
        // 2. 전면 (-Y)
        { rawPts: [{ x: x1, y: y1, z: z1 }, { x: x2, y: y1, z: z1 }, { x: x2, y: y1, z: z2 }, { x: x1, y: y1, z: z2 }], color: colors.front },
        // 3. 우측면 (+X)
        { rawPts: [{ x: x2, y: y1, z: z1 }, { x: x2, y: y2, z: z1 }, { x: x2, y: y2, z: z2 }, { x: x2, y: y1, z: z2 }], color: colors.side },
        // 4. 좌측면 (-X)
        { rawPts: [{ x: x1, y: y2, z: z1 }, { x: x1, y: y1, z: z1 }, { x: x1, y: y1, z: z2 }, { x: x1, y: y2, z: z2 }], color: colors.side },
        // 5. 후면 (+Y)
        { rawPts: [{ x: x2, y: y2, z: z1 }, { x: x1, y: y2, z: z1 }, { x: x1, y: y2, z: z2 }, { x: x2, y: y2, z: z2 }], color: colors.back || colors.front },
        // 6. 하면 (-Z)
        { rawPts: [{ x: x1, y: y2, z: z1 }, { x: x2, y: y2, z: z1 }, { x: x2, y: y1, z: z1 }, { x: x1, y: y1, z: z1 }], color: colors.bottom || colors.top }
      ];

      rawFaces.forEach(f => {
        let totalDepth = 0;
        const pts = f.rawPts.map(p => {
          const proj = project3D(p, width, height);
          totalDepth += (proj.depth ?? 0);
          return proj;
        });
        sceneFaces.push({
          pts,
          color: f.color,
          avgDepth: totalDepth / 4,
          strokeColor,
          strokeWidth
        });
      });
    };

    const addCylinder3D = (
      cx: number, cy: number,
      radius: number,
      z1: number, z2: number,
      colors: { top: string; side: string; bottom?: string },
      strokeColor = '#0f172a'
    ) => {
      if (z2 <= z1 || radius <= 0) return;
      const numSegments = 10;
      const dTheta = (2 * Math.PI) / numSegments;

      const topPts: Point3D[] = [];
      const botPts: Point3D[] = [];

      for (let i = 0; i < numSegments; i++) {
        const theta1 = i * dTheta;
        const theta2 = (i + 1) * dTheta;
        const x1 = cx + radius * Math.cos(theta1);
        const y1 = cy + radius * Math.sin(theta1);
        const x2 = cx + radius * Math.cos(theta2);
        const y2 = cy + radius * Math.sin(theta2);

        topPts.push({ x: x1, y: y1, z: z2 });
        botPts.push({ x: x1, y: y1, z: z1 });

        const rawPts = [
          { x: x1, y: y1, z: z1 },
          { x: x2, y: y2, z: z1 },
          { x: x2, y: y2, z: z2 },
          { x: x1, y: y1, z: z2 }
        ];

        let totalDepth = 0;
        const pts = rawPts.map(p => {
          const proj = project3D(p, width, height);
          totalDepth += (proj.depth ?? 0);
          return proj;
        });

        sceneFaces.push({
          pts,
          color: colors.side,
          avgDepth: totalDepth / 4,
          strokeColor,
          strokeWidth: 1.2
        });
      }

      // 상면 & 하면 원형 캡
      [
        { raw: topPts, color: colors.top },
        { raw: botPts, color: colors.bottom || colors.top }
      ].forEach(cap => {
        let totalDepth = 0;
        const pts = cap.raw.map(p => {
          const proj = project3D(p, width, height);
          totalDepth += (proj.depth ?? 0);
          return proj;
        });
        sceneFaces.push({
          pts,
          color: cap.color,
          avgDepth: totalDepth / cap.raw.length,
          strokeColor,
          strokeWidth: 1.2
        });
      });
    };

    // 7. 🌟 4D 실시간 본체 RC 콘크리트 구조물 수집
    if (showRcStructure && dailyStates.length > 0) {
      const clearance = 0.8;
      const structHalfB = B / 2 - clearance;
      const wallThick = 1.2;

      dailyStates.forEach((state, spanIdx) => {
        const xStart = spanIdx * spanLength;
        const xEnd = xStart + spanLength;
        const isSelected = spanIdx === selectedSpanIdx;

        const getNormProg = (val: number) => (val > 1 ? val / 100 : val);
        const fProg = getNormProg(state.foundationProgress);
        const midProg = getNormProg(state.midSlabProgress);
        const topProg = getNormProg(state.topSlabProgress);

        // 7-1. 바닥 매트 기초
        if (fProg >= 0.2) {
          const fH = 1.8;
          const pourProg = Math.min(1.0, (fProg - 0.2) / 0.8);
          const curZ = -H + fH * pourProg;
          const fColors = state.foundationStatus === 'completed'
            ? { top: '#cbd5e1', front: '#64748b', side: '#475569', back: '#475569', bottom: '#334155' }
            : { top: '#94a3b8', front: '#64748b', side: '#475569', back: '#475569', bottom: '#334155' };

          addBox3D(xStart, xEnd, -structHalfB, structHalfB, -H, curZ, fColors, '#0f172a', 1.8);
        }

        // 7-2. 층별 지하 외벽 (Perimeter RC Walls - B2 및 B1 양측 동시 2단 분할타설)
        let isStory0WallDone = false;
        let isTopStoryWallDone = false;

        if (state.storyStates && state.storyStates.length > 0) {
          state.storyStates.forEach((story, sIdx) => {
            const wProg = getNormProg(story.wallProgress);
            if (wProg >= 0.95 || story.wallStatus === 'completed') {
              if (sIdx === 0) isStory0WallDone = true;
              if (sIdx === state.storyStates.length - 1) isTopStoryWallDone = true;
            }

            if (wProg > 0.01) {
              const numStories = state.storyStates.length;
              const storyH = (H - 5.0 - 1.8) / numStories;
              const zBase = -H + 1.8 + sIdx * storyH;
              const zMidJoint = zBase + storyH * 0.5; // 🌟 1단과 2단 사이 수평 시공이음(Joint) 레벨

              const isCompleted = story.wallStatus === 'completed' || wProg >= 0.98;

              // 🌟 [명확한 2단 분할타설 3D 시각화]
              if (wProg <= 0.5 && !isCompleted) {
                // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                // [1단계] 버팀보 하단 1단(Stage 1) 타설 중 (버팀보 지탱 중)
                // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                const stage1Prog = wProg / 0.5;
                const zCurTop1 = zBase + (storyH * 0.5) * stage1Prog;
                const wColors1 = { top: '#cbd5e1', front: '#64748b', side: '#475569', back: '#475569', bottom: '#334155' };

                // 좌/우 외벽 1단 양쪽 완벽 동시 타설
                addBox3D(xStart, xEnd, -structHalfB, -structHalfB + wallThick, zBase, zCurTop1, wColors1, '#0f172a', 2.0);
                addBox3D(xStart, xEnd, structHalfB - wallThick, structHalfB, zBase, zCurTop1, wColors1, '#0f172a', 2.0);
              } else {
                // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                // [2단계 완료 & 3단계] 1단 완료 매스 + 2단 연결 타설
                // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                // 1) 1단 벽체 (하부 50% 영구 솔리드 콘크리트)
                const wColors1 = { top: '#334155', front: '#475569', side: '#334155', back: '#334155', bottom: '#1e293b' };
                addBox3D(xStart, xEnd, -structHalfB, -structHalfB + wallThick, zBase, zMidJoint, wColors1, '#0284c7', 2.2);
                addBox3D(xStart, xEnd, structHalfB - wallThick, structHalfB, zBase, zMidJoint, wColors1, '#0284c7', 2.2);

                // 2) 2단 벽체 (버팀보 해체 후 상부 개방 공간에 연결 타설)
                const stage2Prog = isCompleted ? 1.0 : Math.min(1.0, (wProg - 0.5) / 0.5);
                const zCurTop2 = zMidJoint + (storyH * 0.5) * stage2Prog;
                const wColors2 = isCompleted
                  ? { top: '#e2e8f0', front: '#64748b', side: '#475569', back: '#475569', bottom: '#334155' }
                  : { top: '#93c5fd', front: '#3b82f6', side: '#1d4ed8', back: '#1d4ed8', bottom: '#1e3a8a' };

                addBox3D(xStart, xEnd, -structHalfB, -structHalfB + wallThick, zMidJoint, zCurTop2, wColors2, '#0f172a', 2.0);
                addBox3D(xStart, xEnd, structHalfB - wallThick, structHalfB, zMidJoint, zCurTop2, wColors2, '#0f172a', 2.0);
              }
            }
          });
        }

        // 7-3. 층별 원형 RC 기둥
        if (state.storyStates && state.storyStates.length > 0) {
          const numStories = state.storyStates.length;
          const storyH = (H - 5.0 - 1.8) / numStories;
          const colRadius = 0.5;
          const colOffsets = [3.0, 10.0, 17.0];

          state.storyStates.forEach((story, sIdx) => {
            const sColProg = getNormProg(story.columnProgress);
            const isColActive = sColProg > 0.01 || (sIdx === 0 && fProg > 0.8) || (sIdx === 1 && midProg > 0.8);

            if (isColActive) {
              const zBase = -H + 1.8 + sIdx * storyH;
              const curProg = story.columnStatus === 'completed' || (sIdx === 0 && midProg > 0) || (sIdx === 1 && topProg > 0) ? 1.0 : Math.max(0.1, sColProg);
              const zCurTop = zBase + storyH * curProg;

              const cColors = story.columnStatus === 'completed' || (sIdx === 0 && midProg > 0) || (sIdx === 1 && topProg > 0)
                ? { top: '#cbd5e1', side: '#64748b', bottom: '#334155' }
                : { top: '#94a3b8', side: '#475569', bottom: '#334155' };

              colOffsets.forEach(offX => {
                const colX = xStart + offX;
                addCylinder3D(colX, 0, colRadius, zBase, zCurTop, cColors, '#0f172a');
              });
            }
          });
        }

        // 7-4. 중간 슬래브 (버팀보 간섭 관통부 블록아웃 및 2차 후타설 분할 메움 구현)
        if (midProg > 0.01 && isStory0WallDone) {
          const midZTop = -H + 1.8 + (H - 5.0 - 1.8) / 2;
          const slabThick = 0.8;
          const midZBot = midZTop - slabThick;

          const pourProg = Math.max(0.1, midProg);
          const curZ = midZBot + slabThick * pourProg;
          const mColors = state.midSlabStatus === 'completed'
            ? { top: '#cbd5e1', front: '#64748b', side: '#475569', back: '#475569' }
            : { top: '#94a3b8', front: '#64748b', side: '#475569', back: '#475569' };

          // 1) 본체 중간 슬래브 타설
          addBox3D(xStart, xEnd, -structHalfB + wallThick, structHalfB - wallThick, midZBot, curZ, mColors, '#0f172a', 1.8);

          // 2) 🌟 버팀보 공법일 때: 슬래브를 관통하는 중간말뚝(King Post) 위치마다 관통 슬리브(Penetration Sleeve) & 방수링 렌더링
          if (!isAnchor) {
            const kingPostSpacing = 4.0;
            const startK = Math.ceil(xStart / kingPostSpacing);
            const endK = Math.floor(xEnd / kingPostSpacing);

            for (let k = startK; k <= endK; k++) {
              const kx = k * kingPostSpacing;
              if (kx >= xStart && kx <= xEnd) {
                const sSize = 0.9; // 0.9m x 0.9m 관통 슬리브
                const sleeveColors = { top: '#f59e0b', front: '#d97706', side: '#b45309', back: '#b45309', bottom: '#78350f' };
                addBox3D(kx - sSize / 2, kx + sSize / 2, -sSize / 2, sSize / 2, midZBot, curZ, sleeveColors, '#b45309', 2.0);
              }
            }
          }
        }

        // 7-5. 최상부 지붕 슬래브 (중간말뚝 관통 슬리브 포함)
        if (topProg > 0.01 && (isTopStoryWallDone || state.topSlabStatus === 'completed')) {
          const topZTop = -5.0;
          const roofThick = 1.2;
          const topZBot = topZTop - roofThick;

          const pourProg = Math.max(0.1, topProg);
          const curZ = topZBot + roofThick * pourProg;
          const rColors = state.topSlabStatus === 'completed'
            ? { top: '#94a3b8', front: '#64748b', side: '#475569', back: '#475569' }
            : { top: '#64748b', front: '#475569', side: '#334155', back: '#334155' };

          // 1) 본체 지붕 슬래브
          addBox3D(xStart, xEnd, -structHalfB, structHalfB, topZBot, curZ, rColors, '#020617', 2.0);

          // 2) 지붕 슬래브를 관통하는 중간말뚝 관통 슬리브
          if (!isAnchor) {
            const kingPostSpacing = 4.0;
            const startK = Math.ceil(xStart / kingPostSpacing);
            const endK = Math.floor(xEnd / kingPostSpacing);

            for (let k = startK; k <= endK; k++) {
              const kx = k * kingPostSpacing;
              if (kx >= xStart && kx <= xEnd) {
                const sSize = 0.9;
                const sleeveColors = { top: '#f59e0b', front: '#d97706', side: '#b45309', back: '#b45309', bottom: '#78350f' };
                addBox3D(kx - sSize / 2, kx + sSize / 2, -sSize / 2, sSize / 2, topZBot, curZ, sleeveColors, '#b45309', 2.0);
              }
            }
          }
        }

        // 7-6. 스팬 선택 하이라이트 박스 (Active Wireframe)
        if (isSelected) {
          const sp1 = project3D({ x: xStart, y: -B / 2, z: 0 }, width, height);
          const sp2 = project3D({ x: xEnd, y: -B / 2, z: 0 }, width, height);
          const sp3 = project3D({ x: xEnd, y: B / 2, z: 0 }, width, height);
          const sp4 = project3D({ x: xStart, y: B / 2, z: 0 }, width, height);

          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.moveTo(sp1.x, sp1.y);
          ctx.lineTo(sp2.x, sp2.y);
          ctx.lineTo(sp3.x, sp3.y);
          ctx.lineTo(sp4.x, sp4.y);
          ctx.closePath();
          ctx.stroke();

          // 스팬 명칭 라벨
          ctx.fillStyle = '#38bdf8';
          ctx.font = 'bold 11px monospace';
          ctx.fillText(`Span ${spanIdx + 1}`, sp1.x, sp1.y - 8);
        }
      });

      // 🌟 [핵심 시공 시퀀스] 6개 스팬 전체 구조물 완료 ➡️ 토피 5m 되메우기 ➡️ 도로 포장 ➡️ 교통 개통
      const backfillTask = schedule?.tasks.find(t => t.type === 'backfill');
      const paveTask = schedule?.tasks.find(t => t.type === 'road_pavement');

      const isBackfillActive = backfillTask && currentDay >= backfillTask.startDay;
      const isBackfillDone = backfillTask && currentDay >= backfillTask.endDay;
      const backfillProg = backfillTask && isBackfillActive
        ? Math.min(1.0, Math.max(0.05, (currentDay - backfillTask.startDay) / Math.max(1, backfillTask.durationDays)))
        : 0;

      const isPaveActive = paveTask && currentDay >= paveTask.startDay;
      const isPaveDone = paveTask && currentDay >= paveTask.endDay;
      const paveProg = paveTask && isPaveActive
        ? Math.min(1.0, Math.max(0.05, (currentDay - paveTask.startDay) / Math.max(1, paveTask.durationDays)))
        : 0;

      // 🌟 7-7. [Phase 4] 6개 스팬 전체 골조 완료 후 토피 5m 일괄 층다짐 되메우기 (EL -5.0m ~ -0.3m)
      if (isBackfillActive) {
        const curSoilZ = isBackfillDone ? -0.3 : -5.0 + 4.7 * backfillProg;
        const soilColors = {
          top: '#b45309',   // 양질의 다짐 토사 표면
          front: '#78350f', // 토사 층단면
          side: '#78350f',
          back: '#78350f',
          bottom: '#451a03'
        };
        addBox3D(0, L, -B / 2, B / 2, -5.0, curSoilZ, soilColors, '#78350f', 1.0);
      }

      // 🌟 7-8. [Phase 5] 되메우기 완료 후 도로 아스팔트 포장층 (EL -0.3m ~ 0.0m)
      if (isPaveActive) {
        const roadColors = {
          top: '#1e293b',   // 짙은 다크 아스팔트 노면
          front: '#0f172a', // 포장 단면
          side: '#0f172a',
          back: '#0f172a',
          bottom: '#020617'
        };
        addBox3D(0, L, -B / 2, B / 2, -0.3, 0.0, roadColors, '#020617', 1.5);
      }

      // 🌟 [핵심] 6개 스팬 전체의 모든 3D 솔리드 면을 깊이순 일괄 정렬 후 렌더링
      sceneFaces.sort((a, b) => b.avgDepth - a.avgDepth);

      sceneFaces.forEach(f => {
        ctx.fillStyle = f.color;
        ctx.beginPath();
        ctx.moveTo(f.pts[0].x, f.pts[0].y);
        for (let i = 1; i < f.pts.length; i++) {
          ctx.lineTo(f.pts[i].x, f.pts[i].y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = f.strokeColor;
        ctx.lineWidth = f.strokeWidth;
        ctx.stroke();
      });

      // 🌟 [핵심] 해체 전까지 콘크리트 위에 100% 선명하게 가로지르는 3D 강관 버팀보 렌더링
      if (showShoringStruts && !isAnchor && selectedAlt?.supports) {
        const renderedStatusSpans = new Set<number>();

        selectedAlt.supports.forEach((sup, tierIdx) => {
          if (isHybrid && sup.type === 'GROUND_ANCHOR') return;
          const supZ = -sup.depth;
          const strutSpacing = isCompStrut ? 5.0 : 4.0;
          const numStruts = Math.floor(L / strutSpacing);

          for (let i = 0; i <= numStruts; i++) {
            const sx = i * strutSpacing;
            const spanIdx = Math.min(numSpans - 1, Math.floor(sx / spanLength));
            const spanState = dailyStates[spanIdx];

            const numStories = spanState?.storyStates?.length || 2;
            const storyH = (H - 5.0 - 1.8) / numStories;
            const matchedStoryIdx = Math.min(numStories - 1, Math.max(0, Math.floor((supZ - (-H + 1.8)) / storyH)));
            const matchedStory = spanState?.storyStates?.[matchedStoryIdx];
            const matchedWProg = matchedStory ? (matchedStory.wallProgress > 1 ? matchedStory.wallProgress / 100 : matchedStory.wallProgress) : 0;

            // 1단 타설 중(wProg <= 0.50)에는 버팀보가 콘크리트 위를 100% 관통하여 가로질러 보여야 함!
            const isCutting = matchedWProg >= 0.48 && matchedWProg <= 0.54;
            const isFullyRemoved = matchedStory?.strutReleased || matchedWProg > 0.54 || spanState?.strutReleaseStatus === 'released';

            if (!isFullyRemoved) {
              const pLeft = project3D({ x: sx, y: -B / 2, z: supZ }, width, height);
              const pRight = project3D({ x: sx, y: B / 2, z: supZ }, width, height);

              // 굵은 3D 입체 버팀보 강관 (붉은색/인디고색)
              ctx.strokeStyle = isCutting ? ((Date.now() % 400 < 200) ? '#f59e0b' : '#ef4444') : (isCompStrut ? '#4f46e5' : '#ef4444');
              ctx.lineWidth = isCompStrut ? 6.0 : 5.0;
              ctx.beginPath();
              ctx.moveTo(pLeft.x, pLeft.y);
              ctx.lineTo(pRight.x, pRight.y);
              ctx.stroke();

              // 강관 중앙 하이라이트 광택선 (3D 입체감 부여)
              ctx.strokeStyle = isCutting ? '#fef08a' : (isCompStrut ? '#818cf8' : '#fca5a5');
              ctx.lineWidth = 1.8;
              ctx.beginPath();
              ctx.moveTo(pLeft.x, pLeft.y - 1);
              ctx.lineTo(pRight.x, pRight.y - 1);
              ctx.stroke();

              // 좌/우 띠장(Wale) 브라켓
              ctx.fillStyle = '#991b1b';
              ctx.fillRect(pLeft.x - 3.5, pLeft.y - 3.5, 7, 7);
              ctx.fillRect(pRight.x - 3.5, pRight.y - 3.5, 7, 7);
            }
          }
        });

        // 🌟 [핵심] 3D 씬 전체에서 오직 단 1개의 대표 상태 텍스트만 표시!
        const activeSpanState = dailyStates[selectedSpanIdx];
        const activeStory = activeSpanState?.storyStates?.[0];
        const activeWProg = activeStory ? (activeStory.wallProgress > 1 ? activeStory.wallProgress / 100 : activeStory.wallProgress) : 0;
        
        if (activeWProg >= 0.48 && activeWProg <= 0.54) {
          const midPos = project3D({ x: selectedSpanIdx * spanLength + spanLength / 2, y: 0, z: -H + 1.8 + (H - 5.0 - 1.8) * 0.5 }, width, height);
          ctx.fillStyle = '#f59e0b';
          ctx.font = 'bold 12px sans-serif';
          ctx.fillText('🔥 [Span ' + (selectedSpanIdx + 1) + '] 버팀보 산소 절단 & 해체 중', midPos.x - 100, midPos.y - 15);
        }
      }

      // 🌟 [핵심] 구조물 축조 중 중간말뚝(King Post)의 슬래브 관통(Penetration) 3D 오버레이 렌더링
      if (showKingPosts && !isAnchor && !isBackfilling && !isBackfillFinished) {
        const kingPostSpacing = 4.0;
        const numKingPosts = Math.floor(L / kingPostSpacing);
        const midSlabZ = -H + 1.8 + (H - 5.0 - 1.8) / 2;
        const roofSlabZ = -5.0;

        for (let i = 0; i <= numKingPosts; i++) {
          const kx = i * kingPostSpacing;
          const topP = project3D({ x: kx, y: 0, z: 0 }, width, height);
          const botP = project3D({ x: kx, y: 0, z: -H * 1.35 }, width, height);

          // 1) 굵은 3D 황금빛 H형강 중간말뚝 수직 관통 기둥
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 4.0;
          ctx.beginPath();
          ctx.moveTo(topP.x, topP.y);
          ctx.lineTo(botP.x, botP.y);
          ctx.stroke();

          // 2) 중간말뚝 중심 하이라이트선
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(topP.x, topP.y);
          ctx.lineTo(botP.x, botP.y);
          ctx.stroke();

          // 3) 🌟 중간 슬래브 관통 방수 지수링 (Waterstop Collar Ring at Mid Slab)
          const midCollarP = project3D({ x: kx, y: 0, z: midSlabZ }, width, height);
          ctx.fillStyle = '#ea580c';
          ctx.fillRect(midCollarP.x - 4, midCollarP.y - 2, 8, 4);
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 1;
          ctx.strokeRect(midCollarP.x - 4, midCollarP.y - 2, 8, 4);

          // 4) 🌟 지붕 슬래브 관통 방수 지수링 (Waterstop Collar Ring at Roof Slab)
          const roofCollarP = project3D({ x: kx, y: 0, z: roofSlabZ }, width, height);
          ctx.fillStyle = '#ea580c';
          ctx.fillRect(roofCollarP.x - 4, roofCollarP.y - 2, 8, 4);
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 1;
          ctx.strokeRect(roofCollarP.x - 4, roofCollarP.y - 2, 8, 4);
        }
      }

      // 🌟 7-9. [최종 완공 개통] 모든 도로 포장 100% 완료(isPaveDone) 시에만 차선 도색 및 차량 주행 허용
      if (isPaveDone) {
        const roadMaxX = L;

        // 1) 노란색 이중 중앙선 (Double Yellow Centerlines)
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 2.0;
        const cLine1A = project3D({ x: 0, y: -0.15, z: 0.02 }, width, height);
        const cLine1B = project3D({ x: roadMaxX, y: -0.15, z: 0.02 }, width, height);
        const cLine2A = project3D({ x: 0, y: 0.15, z: 0.02 }, width, height);
        const cLine2B = project3D({ x: roadMaxX, y: 0.15, z: 0.02 }, width, height);

        ctx.beginPath();
        ctx.moveTo(cLine1A.x, cLine1A.y);
        ctx.lineTo(cLine1B.x, cLine1B.y);
        ctx.moveTo(cLine2A.x, cLine2A.y);
        ctx.lineTo(cLine2B.x, cLine2B.y);
        ctx.stroke();

        // 2) 흰색 차선 점선 (White Dashed Lane Lines)
        ctx.strokeStyle = '#f8fafc';
        ctx.lineWidth = 1.5;
        const numDashes = Math.floor(roadMaxX / 4.0);
        for (let d = 0; d < numDashes; d++) {
          if (d % 2 === 0) {
            const x1 = d * 4.0;
            const x2 = x1 + 2.5;
            // 상행 차선
            const p1 = project3D({ x: x1, y: 4.5, z: 0.02 }, width, height);
            const p2 = project3D({ x: x2, y: 4.5, z: 0.02 }, width, height);
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
            // 하행 차선
            const p3 = project3D({ x: x1, y: -4.5, z: 0.02 }, width, height);
            const p4 = project3D({ x: x2, y: -4.5, z: 0.02 }, width, height);
            ctx.beginPath();
            ctx.moveTo(p3.x, p3.y);
            ctx.lineTo(p4.x, p4.y);
            ctx.stroke();
          }
        }

        // 3) 🚗 실시간 주행 3D 차량들 (Live Moving Vehicles)
        const timeTick = Date.now() / 1000;
        const vehicles = [
          // 상행 차선 차량들 (+X 방향)
          { baseSpeed: 18, offset: 0, laneY: 2.8, color: '#ef4444', type: 'sedan', length: 4.2, width: 1.8, height: 1.4 },
          { baseSpeed: 14, offset: 40, laneY: 6.5, color: '#3b82f6', type: 'suv', length: 4.8, width: 2.0, height: 1.7 },
          { baseSpeed: 11, offset: 80, laneY: 6.5, color: '#f59e0b', type: 'bus', length: 9.0, width: 2.4, height: 2.8 },
          // 하행 차선 차량들 (-X 방향)
          { baseSpeed: 16, offset: 25, laneY: -2.8, color: '#e2e8f0', type: 'sedan', length: 4.4, width: 1.8, height: 1.4, reverse: true },
          { baseSpeed: 12, offset: 65, laneY: -6.5, color: '#10b981', type: 'truck', length: 7.5, width: 2.3, height: 2.5, reverse: true },
          { baseSpeed: 19, offset: 105, laneY: -2.8, color: '#a855f7', type: 'sedan', length: 4.0, width: 1.8, height: 1.4, reverse: true }
        ];

        vehicles.forEach(v => {
          const travelDist = (timeTick * v.baseSpeed + v.offset) % (roadMaxX + 20);
          const curX = v.reverse ? roadMaxX - travelDist + 10 : travelDist - 10;

          if (curX >= -5 && curX <= roadMaxX + 5) {
            const vZ = 0.05;
            const halfL = v.length / 2;
            const halfW = v.width / 2;

            const v1 = project3D({ x: curX - halfL, y: v.laneY - halfW, z: vZ }, width, height);
            const v2 = project3D({ x: curX + halfL, y: v.laneY - halfW, z: vZ }, width, height);
            const vTop1 = project3D({ x: curX - halfL, y: v.laneY - halfW, z: vZ + v.height }, width, height);
            const vTop2 = project3D({ x: curX + halfL, y: v.laneY - halfW, z: vZ + v.height }, width, height);
            const vTop3 = project3D({ x: curX + halfL, y: v.laneY + halfW, z: vZ + v.height }, width, height);
            const vTop4 = project3D({ x: curX - halfL, y: v.laneY + halfW, z: vZ + v.height }, width, height);

            // 차체 측면
            ctx.fillStyle = v.color;
            ctx.beginPath();
            ctx.moveTo(v1.x, v1.y);
            ctx.lineTo(v2.x, v2.y);
            ctx.lineTo(vTop2.x, vTop2.y);
            ctx.lineTo(vTop1.x, vTop1.y);
            ctx.closePath();
            ctx.fill();
            ctx.strokeStyle = '#0f172a';
            ctx.lineWidth = 1.2;
            ctx.stroke();

            // 차체 지붕 상면
            ctx.fillStyle = v.color;
            ctx.beginPath();
            ctx.moveTo(vTop1.x, vTop1.y);
            ctx.lineTo(vTop2.x, vTop2.y);
            ctx.lineTo(vTop3.x, vTop3.y);
            ctx.lineTo(vTop4.x, vTop4.y);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // 헤드라이트 조명 빔
            const headX = v.reverse ? curX - halfL : curX + halfL;
            const dirX = v.reverse ? -4.0 : 4.0;
            const hBeam1 = project3D({ x: headX, y: v.laneY, z: vZ + 0.4 }, width, height);
            const hBeam2 = project3D({ x: headX + dirX, y: v.laneY, z: vZ }, width, height);

            ctx.strokeStyle = 'rgba(254, 240, 138, 0.4)';
            ctx.lineWidth = 3.0;
            ctx.beginPath();
            ctx.moveTo(hBeam1.x, hBeam1.y);
            ctx.lineTo(hBeam2.x, hBeam2.y);
            ctx.stroke();
          }
        });
      }
    }

    // 8. 3D 나침반 / 좌표축 인디케이터
    const axisOrigin = { x: 45, y: height - 45 };
    const axisLen = 28;
    const radYaw = (yaw * Math.PI) / 180;
    const radPitch = (pitch * Math.PI) / 180;

    const axX = axisOrigin.x + axisLen * Math.cos(radYaw);
    const axY = axisOrigin.y - axisLen * Math.sin(radYaw) * Math.sin(radPitch);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(axisOrigin.x, axisOrigin.y);
    ctx.lineTo(axX, axY);
    ctx.stroke();
    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 9px monospace';
    ctx.fillText('X(L)', axX + 2, axY);

    const ayX = axisOrigin.x - axisLen * Math.sin(radYaw);
    const ayY = axisOrigin.y - axisLen * Math.cos(radYaw) * Math.sin(radPitch);
    ctx.strokeStyle = '#22c55e';
    ctx.beginPath();
    ctx.moveTo(axisOrigin.x, axisOrigin.y);
    ctx.lineTo(ayX, ayY);
    ctx.stroke();
    ctx.fillStyle = '#22c55e';
    ctx.fillText('Y(B)', ayX + 2, ayY);

    const azX = axisOrigin.x;
    const azY = axisOrigin.y - axisLen * Math.cos(radPitch);
    ctx.strokeStyle = '#38bdf8';
    ctx.beginPath();
    ctx.moveTo(axisOrigin.x, axisOrigin.y);
    ctx.lineTo(azX, azY);
    ctx.stroke();
    ctx.fillStyle = '#38bdf8';
    ctx.fillText('Z(H)', azX + 2, azY);

  }, [
    yaw,
    pitch,
    zoom,
    panX,
    panY,
    inputs,
    selectedAlt,
    schedule,
    dailyStates,
    currentDay,
    selectedSpanIdx,
    showExcavationGround,
    showShoringStruts,
    showRcStructure,
    showKingPosts,
    project3D
  ]);

  // 카메라 뷰 프리셋
  const setCameraPreset = (preset: 'iso' | 'top' | 'side' | 'front' | 'inside') => {
    switch (preset) {
      case 'iso':
        setYaw(38);
        setPitch(26);
        setZoom(1.15);
        setPanX(0);
        setPanY(0);
        break;
      case 'top':
        setYaw(0);
        setPitch(85);
        setZoom(1.2);
        setPanX(0);
        setPanY(0);
        break;
      case 'side':
        setYaw(0);
        setPitch(5);
        setZoom(1.25);
        setPanX(0);
        setPanY(0);
        break;
      case 'front':
        setYaw(90);
        setPitch(10);
        setZoom(1.3);
        setPanX(0);
        setPanY(0);
        break;
      case 'inside':
        setYaw(45);
        setPitch(-15);
        setZoom(1.8);
        setPanX(0);
        setPanY(50);
        break;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl overflow-hidden shadow-2xl text-white font-sans space-y-0">
      {/* 1. 상단 3D 디지털 트윈 툴바 */}
      <div className="bg-slate-950 px-4 py-2.5 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-indigo-600 text-white shadow-xs">
            <Box className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-black text-white flex items-center gap-1.5">
                <span>3D 디지털 트윈 BIM 시뮬레이터</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/30 text-indigo-300 font-mono">
                  실시간 4D 연동 중 (Day {currentDay}/{totalDays}일)
                </span>
              </h3>
            </div>
            <p className="text-[11px] text-slate-400">
              L={L}m × B={B}m × H={H}m | 360° 마우스 드래그 자유 회전 및 층별 콘크리트 축조 릴레이 묘사
            </p>
          </div>
        </div>

        {/* 카메라 프리셋 및 시점 스위처 버튼 그룹 */}
        <div className="flex flex-wrap items-center gap-2">
          {/* 🌟 3D 시점 모드 스위처 (외부 조감도 vs 1인칭 사람 내부 보행 vs 단면 투시) */}
          <div className="flex items-center bg-slate-950 p-0.5 rounded-lg border border-slate-700 text-xs">
            <button
              onClick={() => {
                setViewMode('orbit');
                setCameraPreset('iso');
              }}
              className={`px-3 py-1 rounded font-bold transition-all flex items-center gap-1.5 ${
                viewMode === 'orbit' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>🌐 외부 조감도</span>
            </button>
            <button
              onClick={() => {
                setViewMode('first_person');
                setYaw(0);
                setPitch(0);
              }}
              className={`px-3 py-1 rounded font-bold transition-all flex items-center gap-1.5 ${
                viewMode === 'first_person' ? 'bg-emerald-600 text-white shadow-xs animate-pulse' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Navigation className="w-3.5 h-3.5" />
              <span>🚶 1인칭 사람 시점 (내부)</span>
            </button>
            <button
              onClick={() => {
                setViewMode('xray');
                setCameraPreset('front');
              }}
              className={`px-3 py-1 rounded font-bold transition-all flex items-center gap-1.5 ${
                viewMode === 'xray' ? 'bg-amber-600 text-white shadow-xs' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>✂️ 단면 X-Ray</span>
            </button>
          </div>

          <div className="h-4 w-px bg-slate-700 mx-1" />

          {/* 카메라 뷰 프리셋 */}
          <button
            onClick={() => setCameraPreset('iso')}
            className="px-2.5 py-1 rounded hover:bg-slate-800 text-slate-300 hover:text-white font-bold transition-all"
            title="아이소메트릭 사시도"
          >
            📐 ISO
          </button>
          <button
            onClick={() => setCameraPreset('side')}
            className="px-2.5 py-1 rounded hover:bg-slate-800 text-slate-300 hover:text-white font-bold transition-all"
            title="종방향 측면 투시"
          >
            🧭 종단
          </button>
          <button
            onClick={() => setCameraPreset('front')}
            className="px-2.5 py-1 rounded hover:bg-slate-800 text-slate-300 hover:text-white font-bold transition-all"
            title="횡단 정면 투시"
          >
            🔍 횡단
          </button>
          {/* 줌인(+) / 줌아웃(-) 버튼 그룹 */}
          <div className="flex items-center bg-slate-950 px-1 py-0.5 rounded-lg border border-slate-700 gap-1 text-xs">
            <button
              onClick={handleZoomIn}
              className="flex items-center gap-1 px-2.5 py-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-black transition-all shadow-xs"
              title="화면 확대 (+)"
            >
              <ZoomIn className="w-3.5 h-3.5" />
              <span>+ 확대</span>
            </button>
            <button
              onClick={handleZoomOut}
              className="flex items-center gap-1 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white font-black transition-all"
              title="화면 축소 (-)"
            >
              <ZoomOut className="w-3.5 h-3.5" />
              <span>- 축소</span>
            </button>
            <button
              onClick={handleZoomReset}
              className="px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white font-mono text-[11px]"
              title="줌 100% 초기화"
            >
              {Math.round(zoom * 100)}%
            </button>
          </div>

          <div className="h-4 w-px bg-slate-700 mx-1" />

          {/* 자동 회전 토글 */}
          <button
            onClick={() => setAutoRotate(!autoRotate)}
            className={`flex items-center gap-1 px-2.5 py-1 rounded font-bold transition-all ${
              autoRotate ? 'bg-indigo-600 text-white' : 'hover:bg-slate-800 text-slate-300'
            }`}
            title="360도 자동 회전 On/Off"
          >
            <RotateCw className={`w-3.5 h-3.5 ${autoRotate ? 'animate-spin' : ''}`} />
            <span>자동회전</span>
          </button>

          {/* 리셋 */}
          <button
            onClick={() => {
              setViewMode('orbit');
              setCameraPreset('iso');
              handleZoomReset();
            }}
            className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white"
            title="카메라 위치 & 줌 초기화"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 🌟 공법 1 (분할타설 및 버팀보 순차해체) 실시간 시퀀스 상태 바 */}
      <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex flex-wrap items-center justify-between text-xs gap-2">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-indigo-900/60 text-indigo-300 font-bold font-mono text-[10px] border border-indigo-700/50">
            공법 1 시퀀스
          </span>
          <div className="flex items-center gap-1.5 text-slate-300 text-[11px]">
            <span>① 기초 타설(발목지지)</span>
            <span className="text-slate-500">➡️</span>
            <span>② 1차 외벽 타설</span>
            <span className="text-slate-500">➡️</span>
            <span className="text-amber-300 font-bold flex items-center gap-0.5">
              <Flame className="w-3 h-3 text-amber-400" />
              <span>③ 14MPa 양생대기(토압전이)</span>
            </span>
            <span className="text-slate-500">➡️</span>
            <span className="text-rose-400 font-bold">④ 버팀보 절단/해체</span>
            <span className="text-slate-500">➡️</span>
            <span>⑤ 2차 외벽/기둥/슬래브</span>
          </div>
        </div>

        <div className="text-[11px] text-slate-400 font-mono">
          현재 활성 스팬: <strong className="text-indigo-300">Span {selectedSpanIdx + 1}</strong> (
          {dailyStates[selectedSpanIdx]?.strutReleaseStatus === 'curing_waiting'
            ? '⚠️ 14MPa 양생 대기 중'
            : dailyStates[selectedSpanIdx]?.foundationStatus === 'in_progress'
            ? '기초 콘크리트 타설 중'
            : dailyStates[selectedSpanIdx]?.topSlabStatus === 'completed'
            ? '본체 축조 완료'
            : '외벽/기둥/슬래브 축조 진행 중'}
          )
        </div>
      </div>

      {/* 2. 메인 3D 뷰포트 캔버스 영역 */}
      <div className="relative w-full h-[480px] bg-slate-950 select-none overflow-hidden">
        <canvas
          ref={canvasRef}
          width={1200}
          height={480}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onWheel={handleWheel}
          className="w-full h-full cursor-grab active:cursor-grabbing block"
        />

        {/* 🌟 완공 후 차량 10초 쇼케이스 카운트다운 배너 */}
        {trafficCountdown !== null && (
          <div className="absolute top-3 right-3 bg-indigo-900/95 backdrop-blur-md border border-indigo-500/80 rounded-xl px-4 py-2.5 text-xs text-white space-y-1 shadow-2xl z-20 animate-pulse">
            <div className="flex items-center gap-2 font-black text-sm text-yellow-300">
              <span>🚗 도로 개통 & 차량 주행 쇼케이스</span>
              <span className="px-2 py-0.5 rounded-full bg-yellow-400 text-slate-950 font-mono text-xs">
                {trafficCountdown}초 후 자동 정지
              </span>
            </div>
            <p className="text-[11px] text-indigo-200">
              6개 스팬 지하 구조물 축조 ➡️ 토피 5m 되메우기 ➡️ 도로 포장 및 차선 도색 완료 후 최종 개통 주행 중!
            </p>
          </div>
        )}

        {/* 🌟 1인칭 사람 시점 HUD 오버레이 */}
        {viewMode === 'first_person' ? (
          <div className="absolute top-3 left-3 bg-slate-900/90 backdrop-blur-md border border-emerald-500/50 rounded-xl p-3.5 text-xs text-slate-200 space-y-2 shadow-2xl max-w-sm">
            <div className="flex items-center justify-between border-b border-slate-700/80 pb-2">
              <div className="flex items-center gap-1.5 text-emerald-400 font-black text-sm">
                <Navigation className="w-4 h-4" />
                <span>🚶 1인칭 사람 시각 내부 모드</span>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-mono font-bold text-[10px] border border-emerald-700">
                눈높이 1.6m
              </span>
            </div>

            <div className="space-y-1 text-[11px] text-slate-300 font-mono">
              <div>• 현재 위치: <strong className="text-white font-bold">STA. {(walkX).toFixed(1)}m</strong> (Span {Math.min(numSpans, Math.floor(walkX / spanLength) + 1)})</div>
              <div>• 층별 위치: <strong className="text-amber-400 font-bold">{walkStory === 0 ? 'B2 승강장층 (EL -11.6m)' : 'B1 대합실층 (EL -7.5m)'}</strong></div>
              <div>• 시선 각도: 수평 {yaw.toFixed(0)}° / 앙각 {pitch.toFixed(0)}°</div>
            </div>

            {/* 층간 엘리베이터 이동 버튼 */}
            <div className="flex items-center gap-2 pt-1">
              <span className="text-[11px] text-slate-400">층간 이동:</span>
              <button
                onClick={() => setWalkStory(0)}
                className={`px-2.5 py-1 rounded text-xs font-bold transition-all ${
                  walkStory === 0 ? 'bg-indigo-600 text-white shadow-xs' : 'bg-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                B2 승강장
              </button>
              <button
                onClick={() => setWalkStory(1)}
                className={`px-2.5 py-1 rounded text-xs font-bold transition-all ${
                  walkStory === 1 ? 'bg-indigo-600 text-white shadow-xs' : 'bg-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                B1 대합실
              </button>
            </div>

            <div className="text-[10px] text-slate-400 bg-slate-950/80 p-2 rounded border border-slate-800">
              💡 <strong>키보드 조작:</strong> [W / ↑] 전진, [S / ↓] 후진, [A / D] 좌우회전<br/>
              💡 <strong>마우스 조작:</strong> 좌클릭 드래그로 360° 둘러보기
            </div>
          </div>
        ) : (
          /* 일반 3D 내비게이션 안내 오버레이 */
          <div className="absolute top-3 left-3 bg-slate-900/85 backdrop-blur-xs border border-slate-800 rounded-lg p-2.5 text-[11px] text-slate-300 space-y-1 shadow-lg pointer-events-none">
            <div className="flex items-center gap-1 text-slate-400 font-bold text-[10px]">
              <Compass className="w-3 h-3 text-indigo-400" />
              <span>3D 내비게이션 안내</span>
            </div>
            <div>• <strong>360° 회전:</strong> 좌클릭 드래그 ({yaw.toFixed(0)}°, {pitch.toFixed(0)}°)</div>
            <div>• <strong>화면 확대/축소:</strong> 상단/좌하단 <span className="text-amber-400 font-bold font-mono">[+] [-]</span> 버튼 클릭 ({Math.round(zoom * 100)}%)</div>
            <div>• <strong>1인칭 진입:</strong> 상단 <span className="text-emerald-400 font-bold">[🚶 1인칭 사람 시점]</span> 클릭</div>
          </div>
        )}

        {/* 🌟 1인칭 사람 보행 인터랙티브 조작 패널 (화면 하단 중앙) */}
        {viewMode === 'first_person' && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 bg-slate-900/95 backdrop-blur-md border border-slate-700 px-4 py-2.5 rounded-2xl shadow-2xl">
            {/* 위치 슬라이더 */}
            <div className="flex items-center gap-3 w-72">
              <span className="text-[10px] text-slate-400 font-mono">0m</span>
              <input
                type="range"
                min={2}
                max={L - 2}
                step={1}
                value={walkX}
                onChange={e => setWalkX(Number(e.target.value))}
                className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              />
              <span className="text-[10px] text-slate-400 font-mono">{L}m</span>
            </div>

            {/* 보행 버튼 그룹 */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setYaw(prev => (prev - 15 + 360) % 360)}
                className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs active:scale-95 border border-slate-700 flex items-center gap-1"
                title="좌측 15도 회전"
              >
                ◀ 좌회전
              </button>

              <button
                onClick={() => setWalkX(prev => Math.min(L - 2, prev + 2.5))}
                className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs active:scale-95 shadow-md flex items-center gap-1"
                title="앞으로 2.5m 전진 (W / ↑)"
              >
                ▲ 2.5m 전진
              </button>

              <button
                onClick={() => setWalkX(prev => Math.max(2, prev - 2.5))}
                className="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-black text-xs active:scale-95 border border-slate-700 flex items-center gap-1"
                title="뒤로 2.5m 후진 (S / ↓)"
              >
                ▼ 2.5m 후진
              </button>

              <button
                onClick={() => setYaw(prev => (prev + 15) % 360)}
                className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs active:scale-95 border border-slate-700 flex items-center gap-1"
                title="우측 15도 회전"
              >
                ▶ 우회전
              </button>
            </div>
          </div>
        )}

        {/* 좌측 하단 플로팅 줌 컨트롤러 패널 (외부 모드일 때만 표시) */}
        {viewMode !== 'first_person' && (
          <div className="absolute bottom-3 left-3 flex items-center gap-1 bg-slate-900/90 backdrop-blur-xs border border-slate-700 p-1.5 rounded-lg shadow-xl">
            <button
              onClick={handleZoomIn}
              className="flex items-center gap-1 px-3 py-1.5 rounded-md bg-indigo-600 hover:bg-indigo-500 text-white font-black text-xs transition-all shadow-sm active:scale-95"
              title="화면 확대 (+)"
            >
              <ZoomIn className="w-4 h-4" />
              <span>+ 확대</span>
            </button>

            <button
              onClick={handleZoomOut}
              className="flex items-center gap-1 px-3 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-white font-black text-xs transition-all shadow-sm active:scale-95 border border-slate-700"
              title="화면 축소 (-)"
            >
              <ZoomOut className="w-4 h-4" />
              <span>- 축소</span>
            </button>

            <button
              onClick={handleZoomReset}
              className="px-2 py-1 rounded bg-slate-950 text-indigo-300 font-mono text-[11px] hover:text-white"
              title="줌 리셋 (100%)"
            >
              100%
            </button>
          </div>
        )}

        {/* 우측 상단 렌더링 필터 레이어 스위처 */}
        <div className="absolute top-3 right-3 bg-slate-900/90 backdrop-blur-xs border border-slate-800 rounded-lg p-2 text-xs space-y-1.5 shadow-lg">
          <div className="text-[10px] font-bold text-slate-400 border-b border-slate-800 pb-1 flex items-center justify-between">
            <span>3D BIM 레이어 필터</span>
            <Layers className="w-3 h-3 text-indigo-400" />
          </div>
          <label className="flex items-center gap-1.5 cursor-pointer text-slate-300 hover:text-white">
            <input
              type="checkbox"
              checked={showExcavationGround}
              onChange={(e) => setShowExcavationGround(e.target.checked)}
              className="rounded accent-amber-500"
            />
            <span>흙막이 H-Pile & 토류판</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-slate-300 hover:text-white">
            <input
              type="checkbox"
              checked={showShoringStruts}
              onChange={(e) => setShowShoringStruts(e.target.checked)}
              className="rounded accent-rose-500"
            />
            <span>{isAnchor ? '어스앵커 경사체' : '강관 버팀보 & 띠장'}</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-slate-300 hover:text-white">
            <input
              type="checkbox"
              checked={showRcStructure}
              onChange={(e) => setShowRcStructure(e.target.checked)}
              className="rounded accent-blue-500"
            />
            <span>본체 RC 구조물 (기초/외벽/슬래브)</span>
          </label>
          {!isAnchor && !isCompStrut && (
            <label className="flex items-center gap-1.5 cursor-pointer text-slate-300 hover:text-white">
              <input
                type="checkbox"
                checked={showKingPosts}
                onChange={(e) => setShowKingPosts(e.target.checked)}
                className="rounded accent-amber-500"
              />
              <span>중간말뚝 (King Post)</span>
            </label>
          )}
        </div>

        {/* 하단 범례 오버레이 */}
        <div className="absolute bottom-3 right-3 bg-slate-900/90 backdrop-blur-xs border border-slate-800 rounded-lg p-2 px-3 text-[10.5px] flex flex-wrap items-center gap-3 text-slate-300">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded bg-slate-300 border border-slate-500" />
            <span>굳은 콘크리트 (t=0.6~1.6m)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded bg-slate-500 border border-slate-400" />
            <span>타설 진행 중</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded bg-yellow-500 animate-pulse border border-yellow-300" />
            <span>14MPa 양생 대기</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded bg-red-500" />
            <span>가설 지보재 (버팀보/앵커)</span>
          </div>
        </div>
      </div>

      {/* 3. 🌟 3D 뷰어 내장 실시간 4D 타임라인 재생 컨트롤러 바 */}
      <div className="bg-slate-950 px-4 py-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4">
        {/* 재생 / 일시정지 / 리셋 버튼 그룹 */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg font-bold text-xs shadow-md transition-all ${
              isPlaying
                ? 'bg-rose-600 hover:bg-rose-700 text-white'
                : 'bg-emerald-600 hover:bg-emerald-700 text-white'
            }`}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current" />}
            <span>{isPlaying ? '일시정지' : '4D 흐름 재생'}</span>
          </button>

          <button
            onClick={() => {
              setIsPlaying(false);
              if (onDayChange) onDayChange(0);
            }}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white"
            title="Day 0으로 초기화"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          {/* 배속 스위처 (0.5x 슬로우모션 추가) */}
          <div className="flex items-center bg-slate-900 rounded-lg p-0.5 border border-slate-800 text-[11px] font-bold gap-0.5">
            {[0.5, 1, 2, 4].map(spd => (
              <button
                key={`spd-${spd}`}
                onClick={() => setPlaySpeed(spd)}
                className={`px-2 py-0.5 rounded ${
                  playSpeed === spd ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
              >
                {spd}x
              </button>
            ))}
          </div>
        </div>

        {/* 메인 Day 슬라이더 트랙 */}
        <div className="flex-1 min-w-[240px] flex items-center gap-3">
          <span className="text-xs font-mono font-bold text-indigo-400 whitespace-nowrap">
            Day {currentDay} / {totalDays}일
          </span>
          <input
            type="range"
            min={0}
            max={totalDays}
            value={currentDay}
            onChange={(e) => {
              if (onDayChange) onDayChange(Number(e.target.value));
            }}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
          />
          <span className="text-xs font-mono text-slate-400 whitespace-nowrap">
            {Math.round((currentDay / Math.max(1, totalDays)) * 100)}% 진행
          </span>
        </div>

        {/* 현재 스팬 선택 배지 */}
        <div className="flex items-center gap-1.5">
          {Array.from({ length: numSpans }).map((_, idx) => (
            <button
              key={`span-btn-${idx}`}
              onClick={() => onSelectSpan(idx)}
              className={`px-2 py-1 rounded text-[11px] font-bold font-mono transition-all ${
                selectedSpanIdx === idx
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              S{idx + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
