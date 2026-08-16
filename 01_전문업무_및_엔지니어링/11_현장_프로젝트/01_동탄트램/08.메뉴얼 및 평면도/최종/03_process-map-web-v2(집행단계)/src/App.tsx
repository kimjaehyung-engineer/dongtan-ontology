import { useState, useRef, useEffect, useCallback } from 'react';
import FlowMap from './components/FlowMap';
import useStore, { lastCanvasMousePos } from './store/useStore';
import { v4 as uuidv4 } from 'uuid';
import dayjs from 'dayjs';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { getManualHtmlForActivity } from './utils/manualLoader';

import { MarkerType } from 'reactflow';
import { Download, Plus, Calendar, FileText, Type, GripHorizontal, GripVertical, X, Copy, Check, ExternalLink, Trash2, Undo2, Redo2, Paintbrush, Clipboard, Moon, Sun, ClipboardList, CheckSquare, Sparkles, Upload, Flame, Layers, HelpCircle, Scissors, RefreshCw, Printer, Save, HardDrive } from 'lucide-react';
import ProjectManagerModal from './components/ProjectManagerModal';
import MapBuilderWizardModal from './components/MapBuilderWizardModal';
import HelpModal from './components/HelpModal';
import A3PrintSplitModal from './components/A3PrintSplitModal';
import { parseExcelWbsToDisciplineMaps } from './utils/excelWbsParser';
import { exportWbsToExcel } from './utils/excelExporter';
import './App.css';

// D-day 잔여일 기준 상태 자동 판정
// function calcStatus(daysRemaining: number): 'normal' | 'warning' | 'danger' {
//   if (daysRemaining <= 7) return 'danger';
//   if (daysRemaining <= 21) return 'warning';
//   return 'normal';
// }

function App() {
  const { addNode, nodes, edges, updateNodeData, updateEdge, deleteEdge, setNodesAndEdges, undo, redo, takeSnapshot, past, future, isSelectMode, setSelectMode, copiedStyle, setCopiedStyle, copiedNodes, copiedEdges, setCopiedNodesAndEdges, isDarkMode, toggleDarkMode, activeDetailTab, setActiveDetailTab, isCpHighlight, toggleCpHighlight, disciplineMaps, activeDisciplineId, setDisciplineMaps, selectDisciplineMap, rawWorkbookBuffer, setRawWorkbookBuffer, triggerFitView } = useStore();
  const [startDate, setStartDate] = useState('2025-12-01');
  const [showSettings, setShowSettings] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const [showProjectManager, setShowProjectManager] = useState(false);
  const [showWizard, setShowWizard] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [showA3SplitModal, setShowA3SplitModal] = useState(false);
  const [manualModalUrl, setManualModalUrl] = useState<string | null>(null);
  const [manualModalTitle, setManualModalTitle] = useState<string>('');
  const flowRef = useRef<HTMLDivElement>(null);

  const selectedNode = nodes.find(n => n.selected);
  const selectedEdge = edges.find(e => e.selected);
  const selectedCount = nodes.filter(n => n.selected).length;

  const openManualModal = (title: string, customUrl?: string) => {
    const defaultPath = `C:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/08.메뉴얼 및 평면도/최종/02_메뉴얼 공종프로섹스(집행단계)/매뉴얼BODY(집행단계-첨부폴더)v8/`;
    const targetUrl = customUrl || defaultPath;
    setManualModalTitle(title);
    setManualModalUrl(targetUrl);
    try {
      if (targetUrl.startsWith('http://') || targetUrl.startsWith('https://')) {
        window.open(targetUrl, '_blank');
      }
    } catch (e) {}
  };

  // 노드나 에지 선택 시 사이드바 자동 오픈
  useEffect(() => {
    if (selectedNode || selectedEdge) {
      setShowSidebar(true);
    }
  }, [selectedNode?.id, selectedEdge?.id]);

  // 마스터 외곽 프레임 및 상단 밀착 레이아웃, CP 주경로 데이터 자동 동기화
  useEffect(() => {
    // 빈 화면으로 시작 (엑셀 불러오기 대기)
  }, []);

  // 선택된 개별 연결선 삭제 핸들러
  const handleDeleteSingleSelectedEdge = () => {
    const selectedEdges = edges.filter(e => e.selected);
    if (selectedEdges.length === 0) {
      alert('삭제할 연결선을 마우스로 먼저 누른(빨간색 선택) 후 삭제 버튼을 눌러주세요.');
      return;
    }
    takeSnapshot();
    const selectedIds = new Set(selectedEdges.map(e => e.id));
    const nextEdges = edges.filter(e => !selectedIds.has(e.id));
    setNodesAndEdges(nodes, nextEdges);
  };

  // 연결선 전체 스타일 일괄/선택 변경 핸들러
  const handleChangeEdgesStyleType = (styleType: string) => {
    if (edges.length === 0) {
      alert('변경할 연결선이 존재하지 않습니다.');
      return;
    }
    takeSnapshot();

    const selectedEdges = edges.filter(e => e.selected);
    const targetEdges = selectedEdges.length > 0 ? selectedEdges : edges;
    const targetIds = new Set(targetEdges.map(e => e.id));

    const nextEdges = edges.map(e => {
      if (!targetIds.has(e.id)) return e;

      if (styleType === 'dashed') {
        return {
          ...e,
          type: 'smoothstep',
          pathOptions: { borderRadius: 16 },
          style: { ...(e.style || {}), strokeDasharray: '6 4' },
        };
      } else {
        return {
          ...e,
          type: styleType,
          pathOptions: styleType === 'smoothstep' ? { borderRadius: 16 } : undefined,
          style: { ...(e.style || {}), strokeDasharray: undefined },
        };
      }
    });

    setNodesAndEdges(nodes, nextEdges);
  };

  // 선택된 연결선 화살표 방향 역전 (Source <-> Target 스와프)
  const handleReverseEdgeDirection = () => {
    const selectedEdges = edges.filter(e => e.selected);
    if (selectedEdges.length === 0) {
      alert('방향을 뒤집을 연결선을 마우스로 먼저 누른(빨간색 선택) 후 [🔄 방향 역전] 버튼을 눌러주세요.');
      return;
    }
    takeSnapshot();

    const selectedIds = new Set(selectedEdges.map(e => e.id));

    const nextEdges = edges.map(e => {
      if (!selectedIds.has(e.id)) return e;

      const swapHandle = (h: string | null | undefined) => {
        if (!h) return h;
        if (h.includes('source')) return h.replace('source', 'target');
        if (h.includes('target')) return h.replace('target', 'source');
        return h;
      };

      return {
        ...e,
        source: e.target,
        target: e.source,
        sourceHandle: swapHandle(e.targetHandle),
        targetHandle: swapHandle(e.sourceHandle),
      };
    });

    setNodesAndEdges(nodes, nextEdges);
  };

  const handleDeleteAllEdges = () => {
    if (edges.length === 0) {
      alert('삭제할 연결선이 존재하지 않습니다.');
      return;
    }
    if (window.confirm(`현재 맵에 있는 총 ${edges.length}개의 연결선을 모두 삭제하시겠습니까?`)) {
      takeSnapshot();
      setNodesAndEdges(nodes, []);
    }
  };

  const isSidebarOpen = showSidebar && ((!!selectedNode && ['action', 'milestone', 'text', 'image', 'checklistItem', 'checklistHeader', 'tableTitle'].includes(selectedNode.type || '')) || !!selectedEdge);

  const handleImportExcelWbs = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const buffer = event.target?.result as ArrayBuffer;
        setRawWorkbookBuffer(buffer);

        // 사용자가 수동으로 이동/배치 조정한 노드 위치 보존을 위한 수집
        const currentNodes = useStore.getState().nodes;
        const currentMaps = useStore.getState().disciplineMaps;

        const result = parseExcelWbsToDisciplineMaps(buffer, currentNodes, currentMaps);
        setDisciplineMaps(result.disciplineMaps);
        alert(`엑셀 다중 공종 파싱 완료!\n총 ${result.disciplineMaps.length}개 공종 시트 프로세스 맵이 업데이트되었습니다.\n\n✨ 수동으로 이동/조정한 카드의 위치 및 서식이 그대로 유지되었습니다.`);
      } catch (err: any) {
        alert(`엑셀 변환 오류: ${err.message || '파일 형식을 확인해주세요.'}`);
      }
    };
    reader.readAsArrayBuffer(file);
  };



  const handleAddNode = () => {
    takeSnapshot();
    addNode({
      id: uuidv4(),
      type: 'action',
      position: { x: lastCanvasMousePos.x - 100, y: lastCanvasMousePos.y - 40 },
      data: {
        label: '',
        department: '',
        purpose: '',
        method: '',
        result: '',
        color: '#fca5a5',
        status: 'normal',
      }
    });
  };

  const handleAddTextNode = () => {
    takeSnapshot();
    addNode({
      id: uuidv4(),
      type: 'text',
      position: { x: lastCanvasMousePos.x - 100, y: lastCanvasMousePos.y - 30 },
      data: { label: '' },
      style: { width: 200, height: 60 },
    });
  };

  const handleAddChecklistItemNode = () => {
    takeSnapshot();
    addNode({
      id: uuidv4(),
      type: 'checklistItem',
      position: { x: lastCanvasMousePos.x - 80, y: lastCanvasMousePos.y - 40 },
      data: {
        label: '새 체크리스트 항목',
        status: 'todo',
        department: '',
      },
    });
  };

  const handleAddChecklistHeaderNode = () => {
    takeSnapshot();
    addNode({
      id: uuidv4(),
      type: 'checklistHeader',
      position: { x: lastCanvasMousePos.x - 80, y: lastCanvasMousePos.y - 20 },
      data: {
        label: '본공사수행',
        status: 'normal',
      },
      style: { width: 140, height: 40 },
    });
  };

  const handleCopyStyle = useCallback(() => {
    const targetNode = nodes.find(n => n.selected);
    if (!targetNode) {
      alert('서식을 복사할 노드를 선택해주세요.');
      return;
    }

    const stylePayload: any = {
      type: targetNode.type,
      color: targetNode.data?.color,
      status: targetNode.data?.status,
      department: targetNode.data?.department,
      textStyle: targetNode.data?.textStyle ? { ...targetNode.data.textStyle } : undefined,
    };

    if (targetNode.style) {
      stylePayload.style = {
        width: targetNode.style.width,
        height: targetNode.style.height,
      };
    }

    setCopiedStyle(stylePayload);
    alert('서식이 복사되었습니다. (Ctrl+Shift+C)');
  }, [nodes, setCopiedStyle]);

  const handlePasteStyle = useCallback(() => {
    if (!copiedStyle) {
      alert('복사된 서식이 없습니다. 먼저 서식을 복사(Ctrl+Shift+C)해주세요.');
      return;
    }

    const selectedNodes = nodes.filter(n => n.selected);
    if (selectedNodes.length === 0) {
      alert('서식을 붙여넣을 노드를 선택해주세요.');
      return;
    }

    takeSnapshot();

    const updatedNodes = nodes.map(node => {
      if (!node.selected) return node;

      const newData = { ...node.data };
      let newStyle = node.style ? { ...node.style } : {};

      if (node.type === 'action') {
        if (copiedStyle.type === 'action') {
          if (copiedStyle.color !== undefined) newData.color = copiedStyle.color;
          if (copiedStyle.status !== undefined) newData.status = copiedStyle.status;
          if (copiedStyle.department !== undefined) newData.department = copiedStyle.department;
        } else if (copiedStyle.type === 'checklistHeader' || copiedStyle.type === 'text') {
          if (copiedStyle.textStyle?.bgColor) {
            newData.color = copiedStyle.textStyle.bgColor;
          }
          if (copiedStyle.status !== undefined) newData.status = copiedStyle.status;
        } else if (copiedStyle.type === 'checklistItem') {
          if (copiedStyle.status !== undefined) newData.status = copiedStyle.status;
          if (copiedStyle.department !== undefined) newData.department = copiedStyle.department;
        }
      } else if (node.type === 'text' || node.type === 'checklistHeader') {
        const currentTextStyle = newData.textStyle ? { ...newData.textStyle } : {};
        
        if (copiedStyle.type === 'text' || copiedStyle.type === 'checklistHeader') {
          if (copiedStyle.textStyle) {
            newData.textStyle = { ...currentTextStyle, ...copiedStyle.textStyle };
          }
          if (copiedStyle.style?.width !== undefined) newStyle.width = copiedStyle.style.width;
          if (copiedStyle.style?.height !== undefined) newStyle.height = copiedStyle.style.height;
        } else if (copiedStyle.type === 'action') {
          if (copiedStyle.color) {
            newData.textStyle = {
              ...currentTextStyle,
              bgColor: copiedStyle.color,
              borderStyle: currentTextStyle.borderStyle || 'solid',
              borderWidth: currentTextStyle.borderWidth !== undefined ? currentTextStyle.borderWidth : 1,
              color: currentTextStyle.color || '#1e293b',
            };
          }
        }
      } else if (node.type === 'checklistItem') {
        if (copiedStyle.status !== undefined) {
          const validStatuses = ['todo', 'inprogress', 'done', 'na'];
          if (validStatuses.includes(copiedStyle.status)) {
            newData.status = copiedStyle.status;
          } else {
            if (copiedStyle.status === 'done') {
              newData.status = 'done';
            } else if (copiedStyle.status === 'normal') {
              newData.status = 'todo';
            } else if (copiedStyle.status === 'warning' || copiedStyle.status === 'danger') {
              newData.status = 'inprogress';
            }
          }
        }
        if (copiedStyle.department !== undefined) {
          newData.department = copiedStyle.department;
        }
      }

      return {
        ...node,
        data: newData,
        style: Object.keys(newStyle).length > 0 ? newStyle : undefined,
      };
    });

    setNodesAndEdges(updatedNodes, edges);
    alert('서식이 적용되었습니다. (Ctrl+Shift+V)');
  }, [nodes, edges, copiedStyle, takeSnapshot, setNodesAndEdges]);

  const handleCopyNodes = useCallback(() => {
    let targetNodes = nodes.filter(n => n.selected);
    let targetEdges: any[] = [];

    // 만약 선택된 노드가 전혀 없다면, 전체 표(모든 노드와 모든 엣지)를 복사 대상으로 취급
    if (targetNodes.length === 0) {
      targetNodes = [...nodes];
      targetEdges = [...edges];
    } else {
      // 선택된 노드들 간의 엣지만 추출
      const selectedIds = new Set(targetNodes.map(n => n.id));
      targetEdges = edges.filter(e => selectedIds.has(e.source) && selectedIds.has(e.target));
    }

    setCopiedNodesAndEdges(
      JSON.parse(JSON.stringify(targetNodes)),
      JSON.parse(JSON.stringify(targetEdges))
    );
    
    alert(`${targetNodes.length}개의 객체(전체 또는 일부 표)가 복사되었습니다. (Ctrl+C)`);
  }, [nodes, edges, setCopiedNodesAndEdges]);

  const handlePasteNodes = useCallback(() => {
    if (!copiedNodes || copiedNodes.length === 0) {
      alert('복사된 표가 없습니다. 먼저 표를 복사(Ctrl+C)해주세요.');
      return;
    }

    takeSnapshot();

    // 1. 바운딩 박스를 계산하여 가로 오프셋 결정
    let minX = Infinity;
    let maxX = -Infinity;
    copiedNodes.forEach(node => {
      const x = node.position.x;
      let w = 200; // 기본
      if (node.type === 'swimlane') {
        w = node.style?.width ? Number(node.style.width) : 2500;
      } else if (node.type === 'verticalLine') {
        w = 10;
      } else if (node.type === 'rowDivider') {
        w = node.style?.width ? Number(node.style.width) : 2500;
      } else if (node.style?.width !== undefined) {
        w = Number(node.style.width);
      }

      if (x < minX) minX = x;
      if (x + w > maxX) maxX = x + w;
    });

    const boundsWidth = maxX - minX;
    // 옆에다 갖다붙이기 위해 너비 + 100px 만큼 우측으로 쉬프트
    const offsetX = (boundsWidth > 0 && boundsWidth < Infinity) ? boundsWidth + 100 : 300;

    // 2. ID 매핑을 통한 복제 및 우측 쉬프트 적용
    const idMap: Record<string, string> = {};
    copiedNodes.forEach(node => {
      idMap[node.id] = uuidv4();
    });

    // 기존 선택된 노드들 해제
    const nextNodes = nodes.map(n => ({ ...n, selected: false }));

    const newNodes = copiedNodes.map(node => {
      const newId = idMap[node.id];
      let newData = { ...node.data };

      // 제목 노드인 경우 번호 증가 처리
      if (node.type === 'tableTitle') {
        const currentLabel = node.data.label || '';
        const match = currentLabel.match(/^(\d+)\.\s*(.*)$/);
        if (match) {
          const num = parseInt(match[1], 10);
          newData.label = `${num + 1}. ${match[2]}`;
        } else {
          newData.label = `2. ${currentLabel}`;
        }
      }

      return {
        ...node,
        id: newId,
        position: {
          x: node.position.x + offsetX,
          y: node.position.y
        },
        data: newData,
        selected: true // 붙여넣은 요소를 즉시 선택 상태로 전환
      };
    });

    const newEdges = (copiedEdges || []).map(edge => {
      return {
        ...edge,
        id: uuidv4(),
        source: idMap[edge.source] || edge.source,
        target: idMap[edge.target] || edge.target,
        selected: false
      };
    });

    setNodesAndEdges([...nextNodes, ...newNodes], [...edges, ...newEdges]);
    alert('복사한 표를 오른쪽에 붙여넣었습니다. (Ctrl+V)');
  }, [nodes, edges, copiedNodes, copiedEdges, takeSnapshot, setNodesAndEdges]);

  // Ctrl+Z (Undo) 및 Ctrl+Y (Redo) 및 'T'/'K' 전역 단축키 핸들러
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable;

      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
        if (isInput) return;
        e.preventDefault();
        undo();
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') {
        if (isInput) return;
        e.preventDefault();
        redo();
      }
      // Ctrl+C: 노드 및 표 복사
      if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'c') {
        if (isInput) return;
        e.preventDefault();
        handleCopyNodes();
      }
      // Ctrl+V: 복사한 노드 및 표 붙여넣기
      if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'v') {
        if (isInput) return;
        e.preventDefault();
        handlePasteNodes();
      }
      // Ctrl+Shift+C: 서식 복사
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'c') {
        if (isInput) return;
        e.preventDefault();
        handleCopyStyle();
      }
      // Ctrl+Shift+V: 서식 붙여넣기
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'v') {
        if (isInput) return;
        e.preventDefault();
        handlePasteStyle();
      }
      // 'T' 단축키로 현재 마우스 위치에 텍스트 노드 즉시 추가
      if (!e.ctrlKey && !e.metaKey && !e.altKey && e.key.toLowerCase() === 't') {
        if (isInput) return;
        e.preventDefault();
        handleAddTextNode();
      }
      // 'K' 단축키로 현재 마우스 위치에 체크리스트 항목 즉시 추가
      if (!e.ctrlKey && !e.metaKey && !e.altKey && e.key.toLowerCase() === 'k') {
        if (isInput) return;
        e.preventDefault();
        handleAddChecklistItemNode();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [undo, redo, handleAddTextNode, handleAddChecklistItemNode, handleAddChecklistHeaderNode, handleCopyStyle, handlePasteStyle, handleCopyNodes, handlePasteNodes]);

  const handleChangeSelectedFontSize = (delta: number) => {
    const selectedNodes = nodes.filter(n => n.selected);
    if (selectedNodes.length === 0) {
      alert('글자 크기를 조절할 카드를 먼저 마우스로 선택해주세요. (전체 카드 일괄 통일은 [🌐 전체 일괄 통일] 드롭다운을 이용하세요)');
      return;
    }
    takeSnapshot();
    setNodesAndEdges(
      nodes.map(n => {
        if (!n.selected) return n;
        const currentSize = (n.data as any).fontSize || n.data.textStyle?.fontSize || 14.5;
        const nextSize = Math.min(28, Math.max(9, Number((currentSize + delta).toFixed(1))));
        return {
          ...n,
          data: {
            ...n.data,
            fontSize: nextSize,
            textStyle: {
              ...(n.data.textStyle || {}),
              fontSize: nextSize,
            },
          },
        };
      }),
      edges
    );
  };

  // 현재 맵의 모든 카드 글자 크기를 100% 한꺼번에 일괄 통일
  const handleApplyAllCardsFontSize = (targetSize: number) => {
    takeSnapshot();
    const updatedNodes = nodes.map(n => {
      if (['action', 'text', 'checklistItem', 'checklistHeader'].includes(n.type || '')) {
        return {
          ...n,
          data: {
            ...n.data,
            fontSize: targetSize,
            textStyle: {
              ...(n.data.textStyle || {}),
              fontSize: targetSize,
            },
          },
        };
      }
      return n;
    });

    setNodesAndEdges(updatedNodes, edges);
    alert(`🎉 현재 프로세스 맵의 모든 카드 글자 크기가 [ ${targetSize}px ]로 100% 일괄 통일되었습니다!`);
  };

  const handleDuplicateSelected = () => {
    const selectedNodes = nodes.filter(n => n.selected);
    if (selectedNodes.length === 0) return;
    takeSnapshot(); // 복제 전 스냅샷 저장

    // 노드 ID 매핑 생성
    const idMap: Record<string, string> = {};
    selectedNodes.forEach(n => {
      idMap[n.id] = uuidv4();
    });

    // 새 복사 노드들 생성 (오프셋 60)
    const newDuplicatedNodes = selectedNodes.map(n => {
      return {
        ...n,
        id: idMap[n.id],
        position: {
          x: n.position.x + 60,
          y: n.position.y + 60,
        },
        selected: true, // 복제된 노드들을 선택 상태로 만듦
      };
    });

    // 새 복사 노드들 간의 엣지 복제
    const newDuplicatedEdges: any[] = [];
    edges.forEach(e => {
      if (idMap[e.source] && idMap[e.target]) {
        newDuplicatedEdges.push({
          ...e,
          id: uuidv4(),
          source: idMap[e.source],
          target: idMap[e.target],
          selected: false,
        });
      }
    });

    // 기존 노드는 선택 해제
    const nextNodes = nodes.map(n => {
      if (idMap[n.id]) {
        return { ...n, selected: false };
      }
      return n;
    });

    setNodesAndEdges(
      [...nextNodes, ...newDuplicatedNodes],
      [...edges, ...newDuplicatedEdges]
    );
  };

  const handleDeleteSelected = () => {
    const selectedNodes = nodes.filter(n => n.selected);
    if (selectedNodes.length === 0) return;

    if (window.confirm(`선택한 ${selectedNodes.length}개의 카드를 삭제하시겠습니까?`)) {
      takeSnapshot(); // 삭제 전 스냅샷 저장
      const selectedIds = selectedNodes.map(n => n.id);
      const newNodes = nodes.filter(n => !selectedIds.includes(n.id));
      const newEdges = edges.filter(e => !selectedIds.includes(e.source) && !selectedIds.includes(e.target));
      setNodesAndEdges(newNodes, newEdges);
    }
  };

  // const handleExcelUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
  //   if (!e) return;
  // };

  // 이미지를 캔버스 중앙에 노드로 추가하는 공통 함수
  const addImageNode = useCallback((dataUrl: string) => {
    addNode({
      id: uuidv4(),
      type: 'image',
      position: { x: 400 + Math.random() * 100, y: 300 + Math.random() * 100 },
      data: { imageDataUrl: dataUrl, caption: '' } as any,
      style: { width: 320, height: 240 },
    });
  }, [addNode]);

  // Ctrl+V 클립보드 이미지 붙여넣기
  useEffect(() => {
    const onPaste = (e: ClipboardEvent) => {
      const items = e.clipboardData?.items;
      if (!items) return;
      for (const item of Array.from(items)) {
        if (item.type.startsWith('image/')) {
          const file = item.getAsFile();
          if (!file) continue;
          const reader = new FileReader();
          reader.onload = ev => addImageNode(ev.target?.result as string);
          reader.readAsDataURL(file);
        }
      }
    };
    window.addEventListener('paste', onPaste);
    return () => window.removeEventListener('paste', onPaste);
  }, [addImageNode]);

  // // 파일 선택으로 이미지 추가
  // const handleImageFile = (e: React.ChangeEvent<HTMLInputElement>) => {
  //   if (!e) return;
  // };

  // D-day 착공일 기준 마일스톤 실제 날짜 동적 파싱 및 계산
  const applyDday = () => {
    const base = dayjs(startDate);
    const { nodes: currentNodes, edges: currentEdges } = useStore.getState();

    const updatedNodes = currentNodes.map(node => {
      if (node.type === 'milestone') {
        const dateStr = node.data.date || node.data.label || '';
        const match = dateStr.match(/D-(\d+)/i) || dateStr.match(/D\+(\d+)/i);
        if (match) {
          const isPlus = dateStr.includes('+');
          const offsetDays = parseInt(match[1], 10);
          const calcDate = isPlus ? base.add(offsetDays, 'day') : base.subtract(offsetDays, 'day');
          const formattedDate = calcDate.format('YYYY.MM.DD');

          const labelPrefix = dateStr.split('(')[0]?.trim() || `D${isPlus ? '+' : '-'}${offsetDays}`;
          return {
            ...node,
            data: {
              ...node.data,
              date: `${labelPrefix} (${formattedDate})`,
            },
          };
        }
      }
      return node;
    });

    setNodesAndEdges(updatedNodes, currentEdges);
    alert(`착공일(${startDate}) 기준 마일스톤 날짜가 자동으로 계산 및 반영되었습니다!`);
  };

  const handleAlignHorizontal = () => {
    const selectedNodes = nodes.filter(n => n.selected);
    if (selectedNodes.length < 2) { alert('정렬할 노드를 2개 이상 선택하세요 (Shift+드래그 또는 Shift+클릭)'); return; }
    const targetY = selectedNodes[0].position.y;
    setNodesAndEdges(
      nodes.map(n => n.selected ? { ...n, position: { ...n.position, y: targetY } } : n),
      useStore.getState().edges
    );
  };

  const handleAlignVertical = () => {
    const selectedNodes = nodes.filter(n => n.selected);
    if (selectedNodes.length < 2) { alert('정렬할 노드를 2개 이상 선택하세요 (Shift+드래그 또는 Shift+클릭)'); return; }
    const targetX = selectedNodes[0].position.x;
    setNodesAndEdges(
      nodes.map(n => n.selected ? { ...n, position: { ...n.position, x: targetX } } : n),
      useStore.getState().edges
    );
  };


  // 전체 프로세스 맵 (모든 노드/스윔레인) 영역 100% 바운딩 박스 고해상도 캡처
  const captureFullMapCanvas = async (requestedScale?: number) => {
    const currentNodes = useStore.getState().nodes;
    const viewportEl = document.querySelector('.react-flow__viewport') as HTMLElement;
    const reactFlowEl = document.querySelector('.react-flow') as HTMLElement;
    if (!viewportEl || !reactFlowEl) return null;

    // 1. 전체 노드 바운딩 박스(최소/최대 좌표) 정확히 측정
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    currentNodes.forEach(n => {
      const x = n.position.x;
      const y = n.position.y;
      let w = 380;
      let h = 280;
      if (n.type === 'swimlane') {
        w = (n.style?.width as number) || 5500;
        h = (n.style?.height as number) || 360;
      } else if (n.type === 'phaseHeader') {
        w = (n.style?.width as number) || 450;
        h = 65;
      } else if (n.type === 'mapFrame') {
        w = (n.style?.width as number) || 5600;
        h = (n.style?.height as number) || 2800;
      } else if (n.type === 'text' || n.type === 'milestone') {
        w = 280;
        h = 100;
      }

      if (x < minX) minX = x;
      if (y < minY) minY = y;
      if (x + w > maxX) maxX = x + w;
      if (y + h > maxY) maxY = y + h;
    });

    if (minX === Infinity) { minX = 0; minY = 0; maxX = 2400; maxY = 1400; }

    const padding = 60;
    minX -= padding;
    minY -= padding;
    maxX += padding;
    maxY += padding;

    const fullW = Math.ceil(maxX - minX);
    const fullH = Math.ceil(maxY - minY);

    // 2. 고화질 보장 안전 스케일 (브라우저 메모리 오버플로우 방지 및 8K 해상도 제어)
    const targetScale = requestedScale || 2.0;
    const safeScale = Math.min(targetScale, 8192 / Math.max(fullW, fullH));

    // 3. 현재 사용자 뷰포트 상태 및 컨테이너 스타일 보존
    const origTransform = viewportEl.style.transform;
    const origWidth = reactFlowEl.style.width;
    const origHeight = reactFlowEl.style.height;
    const origOverflow = reactFlowEl.style.overflow;

    try {
      // 4. 전체 맵 노드가 (0,0)에 오도록 임시 변환 & 캡처 모드 클래스 추가 (연결점 🔵 동그라미 제거)
      reactFlowEl.classList.add('exporting-map-mode');
      viewportEl.style.transform = `translate(${-minX}px, ${-minY}px) scale(1)`;
      reactFlowEl.style.width = `${fullW}px`;
      reactFlowEl.style.height = `${fullH}px`;
      reactFlowEl.style.overflow = 'visible';

      // 5. html2canvas로 전체 맵 영역 고화질 캡처
      const canvas = await html2canvas(reactFlowEl, {
        width: fullW,
        height: fullH,
        windowWidth: fullW + 300,
        windowHeight: fullH + 300,
        scale: safeScale,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
      });

      return { canvas, safeScale };
    } finally {
      // 6. 원래 뷰포트 위치 및 스타일 즉시 복원
      reactFlowEl.classList.remove('exporting-map-mode');
      viewportEl.style.transform = origTransform;
      reactFlowEl.style.width = origWidth;
      reactFlowEl.style.height = origHeight;
      reactFlowEl.style.overflow = origOverflow;
    }
  };

  const handleExportPNG = async () => {
    try {
      document.body.style.cursor = 'wait';
      const res = await captureFullMapCanvas(2.0);
      if (!res) return;
      const link = document.createElement('a');
      link.download = `process-map-${dayjs().format('YYYYMMDD-HHmm')}.png`;
      link.href = res.canvas.toDataURL('image/png');
      link.click();
    } catch (err) {
      alert('PNG 생성 중 오류가 발생했습니다: ' + err);
    } finally {
      document.body.style.cursor = 'default';
    }
  };

  const handleExportPDF = async () => {
    try {
      document.body.style.cursor = 'wait';
      const res = await captureFullMapCanvas(2.0);
      if (!res) return;

      const { canvas, safeScale } = res;
      const imgW = canvas.width;
      const imgH = canvas.height;

      // 도면용 고화질 PDF 규격 설정
      const pdf = new jsPDF({
        orientation: imgW > imgH ? 'landscape' : 'portrait',
        unit: 'mm',
        format: [Math.max(420, (imgW / safeScale) * 0.15), Math.max(297, (imgH / safeScale) * 0.15)],
      });

      const pageW = pdf.internal.pageSize.getWidth();
      const pageH = pdf.internal.pageSize.getHeight();

      const imgData = canvas.toDataURL('image/jpeg', 0.95);
      pdf.addImage(imgData, 'JPEG', 0, 0, pageW, pageH, undefined, 'FAST');

      pdf.save(`process-map-${dayjs().format('YYYYMMDD-HHmm')}.pdf`);
    } catch (err) {
      alert('PDF 생성 중 오류가 발생했습니다: ' + err);
    } finally {
      document.body.style.cursor = 'default';
    }
  };

  const handleSave = () => {
    const state = { nodes: useStore.getState().nodes, edges: useStore.getState().edges };
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
    const link = document.createElement('a');
    link.download = `process-map-${dayjs().format('YYYYMMDD-HHmm')}.json`;
    link.href = URL.createObjectURL(blob);
    link.click();
  };

  const todayFormatted = dayjs().format('YYYY-MM-DD');

  return (
    <div className="w-screen h-screen flex flex-col font-sans transition-colors duration-300 bg-[#f8fafc] text-slate-900">
      {/* 🟢 최상단 헤더 툴바 (2단 최적화 밸런스 레이아웃) */}
      <header className={`border-b flex flex-col flex-shrink-0 z-30 transition-colors shadow-2xs select-none ${
        isDarkMode ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-900'
      }`}>
        {/* 1단: 메인 프로젝트 파일 / 데이터 내보내기 & 시스템 설정 */}
        <div className="px-4 py-1.5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3 overflow-x-auto custom-scrollbar">
          {/* 1-1. 타이틀 & 데이터 WBS 관리 */}
          <div className="flex items-center gap-2 flex-shrink-0">
            <h1 className="text-xs font-black flex items-center gap-1.5 pr-2.5 border-r border-slate-200 dark:border-slate-800">
              <svg className={`w-4 h-4 flex-shrink-0 ${isDarkMode ? 'text-indigo-400' : 'text-indigo-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span className="font-black tracking-tight text-slate-900 dark:text-white text-xs">프로세스 맵</span>
              <button
                onClick={() => setShowHelp(true)}
                className="text-[10px] font-extrabold px-2 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-slate-700 hover:bg-slate-200 transition-all flex items-center gap-1"
                title="앱 사용법 및 도움말"
              >
                <HelpCircle size={11} className="text-indigo-600" />
                <span>도움말</span>
              </button>
            </h1>

            <label className="flex items-center gap-1 px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-slate-800 font-extrabold rounded-lg text-xs border border-slate-300 shadow-2xs cursor-pointer transition-all" title="WBS 엑셀 파일 불러오기">
              <Upload size={13} className="text-slate-600" />
              <span>엑셀 WBS 불러오기</span>
              <input type="file" accept=".xlsx,.xls,.xlsm,.csv" onChange={handleImportExcelWbs} className="hidden" />
            </label>



            <button
              onClick={() => {
                const mapObj = disciplineMaps.find(m => m.id === activeDisciplineId);
                const title = mapObj ? mapObj.mapTitle : '동탄트램_프로세스맵';
                exportWbsToExcel(nodes, edges, title, rawWorkbookBuffer);
              }}
              className="flex items-center gap-1 px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-slate-800 font-extrabold rounded-lg text-xs border border-slate-300 shadow-2xs transition-all"
              title="엑셀 다운로드"
            >
              <Download size={13} className="text-slate-600" />
              <span>엑셀 내보내기</span>
            </button>

            <button
              onClick={() => setShowWizard(true)}
              className="flex items-center gap-1 px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-slate-800 font-extrabold rounded-lg text-xs border border-slate-300 shadow-2xs transition-all"
              title="새 프로세스 맵 작성 마법사"
            >
              <Sparkles size={13} className="text-indigo-600" />
              <span>새 맵 마법사</span>
            </button>

            <button
              onClick={() => {
                if (window.confirm('사전토공사 맵을 최신 표준 배치 및 공정 연결 구조로 100% 초기화하시겠습니까?')) {
                  useStore.getState().resetToDefaultMap();
                  useStore.getState().triggerFitView();
                }
              }}
              className="flex items-center gap-1 px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-900 font-extrabold rounded-lg text-xs border border-amber-300 shadow-2xs transition-all"
              title="최신 30개 사전토공사 카드 및 화살표 표준 배치로 즉시 초기화"
            >
              <RefreshCw size={13} className="text-amber-600" />
              <span>맵 초기화</span>
            </button>


            <button
              onClick={() => {
                useStore.getState().autoConnectByAiContext();
                alert('✨ AI가 카드를 부서(세로축)와 D-Day 일정(가로축)에 맞춰 균등 격자 정렬하고, 공정 맥락 화살표를 최적 연결했습니다!');
              }}
              className="flex items-center gap-1 px-2.5 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-900 font-extrabold rounded-lg text-xs border border-indigo-300 shadow-2xs transition-all"
              title="카드 위치를 가로축(일정)/세로축(부서) 균등 정렬하고 AI 공정 맥락 화살표를 동시 자동 연결"
            >
              <Sparkles size={13} className="text-indigo-600 animate-pulse" />
              <span>🤖 AI 맥락 연결 & 자동 정렬</span>
            </button>

            <button
              onClick={toggleCpHighlight}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-extrabold transition-all border ${
                isCpHighlight
                  ? 'bg-rose-600 text-white border-rose-600 shadow-xs'
                  : 'bg-slate-50 border-slate-300 text-slate-800 hover:bg-rose-50 hover:border-rose-200 hover:text-rose-700'
              }`}
              title="Critical Path 핵심 주경로 강조"
            >
              <Flame size={13} className={isCpHighlight ? 'text-white' : 'text-rose-500'} />
              <span>CP 주경로</span>
            </button>
          </div>

          {/* 1-2. 인쇄, 저장 및 설정 */}
          <div className="flex items-center gap-1.5 flex-shrink-0">
            {/* 🟢 실시간 자동저장 상태 표시 */}
            <span className="hidden md:flex items-center gap-1.5 text-[11px] font-black text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200 shadow-2xs">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>실시간 자동저장 활성화</span>
            </span>

            {/* 💾 수동 맵 저장 버튼 (100% 저장 보장) */}
            <button
              onClick={() => {
                const { nodes, edges } = useStore.getState();
                localStorage.setItem('process-map-storage-v62', JSON.stringify({
                  state: { nodes, edges, disciplineMaps: [], activeDisciplineId: '' },
                  version: 62,
                }));
                if (window.confirm('💾 현재 프로세스 맵의 모든 수정 사항(카드, 화살표, 부서배치, D-Day)이 브라우저 DB에 즉시 수동 저장되었습니다!\n\n내 컴퓨터에 저장 백업 파일(.json)도 함께 다운로드하시겠습니까?')) {
                  handleSave();
                }
              }}
              className="flex items-center gap-1.5 px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-black rounded-lg text-xs shadow-sm shadow-emerald-600/30 transition-all border border-emerald-500 cursor-pointer hover:scale-105"
              title="현재 프로세스 맵의 모든 편집 상태(카드 텍스트, 위치, 연결선, 부서)를 브라우저 및 파일로 수동 저장합니다"
            >
              <Save size={13} className="text-emerald-100" />
              <span>💾 맵 저장 (Save)</span>
            </button>

            <button
              onClick={() => setShowA3SplitModal(true)}
              className="flex items-center gap-1.5 px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold rounded-lg text-xs shadow-2xs transition-all border border-indigo-600"
              title="대형 프로세스 맵을 A3 용지 여러 장으로 분할 출력하여 카드 글씨가 100% 선명하게 보이도록 포스터 인쇄합니다"
            >
              <Printer size={13} className="text-amber-300" />
              <span>🖨️ A3 분할출력</span>
            </button>
            <button onClick={handleExportPNG} className="flex items-center gap-1 px-2 py-1 bg-slate-50 hover:bg-slate-100 text-slate-800 font-extrabold rounded-lg border border-slate-300 text-xs shadow-2xs">
              <Download size={12} className="text-slate-600" /> PNG
            </button>
            <button onClick={handleExportPDF} className="flex items-center gap-1 px-2 py-1 bg-slate-50 hover:bg-slate-100 text-slate-800 font-extrabold rounded-lg border border-slate-300 text-xs shadow-2xs">
              <FileText size={12} className="text-slate-600" /> PDF
            </button>
            <button onClick={handleSave} className="flex items-center gap-1 px-2 py-1 bg-slate-50 hover:bg-slate-100 text-slate-800 font-extrabold rounded-lg border border-slate-300 text-xs shadow-2xs" title="현재 작업 맵을 백업 파일(.json)로 내보냅니다">
              <HardDrive size={12} className="text-slate-600" /> 백업파일
            </button>

            <div className="h-4 w-px bg-slate-200 dark:bg-slate-700 mx-0.5" />

            {/* 📅 착공일 (D-Day) 설정 */}
            <div className="relative">
              <button
                onClick={() => setShowSettings(v => !v)}
                className="flex items-center gap-1 px-2 py-1 bg-slate-50 hover:bg-slate-100 border border-slate-300 text-slate-800 font-extrabold rounded-lg text-xs shadow-2xs"
                title="착공 기준일 (D-Day) 설정"
              >
                <Calendar size={12} className="text-slate-600" />
                <span>착공일</span>
              </button>

              {showSettings && (
                <div className="absolute right-0 top-full mt-2 bg-white shadow-2xl rounded-2xl border border-slate-200 text-slate-900 p-4 z-50 w-72 select-none">
                  <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-100">
                    <p className="text-xs font-black text-slate-900 flex items-center gap-1.5">
                      <Calendar size={14} className="text-indigo-600" />
                      착공 기준일 설정 (D-Day)
                    </p>
                    <button onClick={() => setShowSettings(false)} className="p-1 text-slate-400 hover:text-slate-700 rounded hover:bg-slate-100">
                      <X size={14} />
                    </button>
                  </div>
                  <div className="mb-2">
                    <label className="block text-[11px] font-bold text-slate-600 mb-1">기준 착공일 날짜 선택</label>
                    <input
                      type="date"
                      value={startDate}
                      onChange={e => setStartDate(e.target.value)}
                      className="w-full border border-indigo-200 bg-slate-50 text-slate-900 font-bold rounded px-3 py-1.5 text-xs outline-none focus:border-indigo-600"
                    />
                  </div>
                  <button
                    onClick={() => { applyDday(); setShowSettings(false); }}
                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded py-2 text-xs font-black shadow transition-all flex items-center justify-center gap-1"
                  >
                    <Check size={14} />
                    자동 계산 적용
                  </button>
                </div>
              )}
            </div>

            <button
              onClick={toggleDarkMode}
              className="p-1 rounded-lg bg-slate-50 border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-extrabold"
              title="다크/라이트 테마"
            >
              {isDarkMode ? <Sun size={13} className="text-amber-500" /> : <Moon size={13} className="text-slate-600" />}
            </button>
            <button 
              onClick={() => {
                if (window.confirm('모든 사용자 편집 데이터를 지우고 초기 상태로 복원하시겠습니까?')) {
                  localStorage.removeItem('process-map-storage-v76');
                  localStorage.removeItem('process-map-storage-v75');
                  localStorage.removeItem('process-map-wbs-cache-v2');
                  localStorage.removeItem('process-map-wbs-cache-v1');
                  localStorage.removeItem('process-map-storage-v74');
                  localStorage.removeItem('process-map-storage-v73');
                  localStorage.removeItem('process-map-storage-v72');
                  localStorage.removeItem('process-map-storage-v71');
                  localStorage.removeItem('process-map-storage-v70');
                  localStorage.removeItem('process-map-storage-v69');
                  localStorage.removeItem('process-map-storage-v68');
                  localStorage.removeItem('process-map-storage-v67');
                  localStorage.removeItem('process-map-storage-v66');
                  localStorage.removeItem('process-map-storage-v65');
                  localStorage.removeItem('process-map-storage-v64');
                  localStorage.removeItem('process-map-storage-v63');
                  localStorage.removeItem('process-map-storage-v62');
                  localStorage.removeItem('process-map-storage-v61');
                  localStorage.removeItem('process-map-storage-v60');
                  localStorage.removeItem('process-map-storage-v59');
                  localStorage.removeItem('process-map-storage-v58');
                  localStorage.removeItem('process-map-storage-v57');
                  localStorage.removeItem('process-map-storage-v56');
                  localStorage.removeItem('process-map-storage-v55');
                  localStorage.removeItem('process-map-storage-v54');
                  localStorage.removeItem('process-map-storage-v53');
                  localStorage.removeItem('process-map-storage-v52');
                  localStorage.removeItem('process-map-storage-v51');
                  localStorage.removeItem('process-map-storage-v50');
                  window.location.reload();
                }
              }} 
              className="px-2 py-1 bg-slate-50 hover:bg-red-50 text-slate-600 hover:text-red-600 font-extrabold border border-slate-300 hover:border-red-200 rounded-lg text-xs"
              title="초기화"
            >
              초기화
            </button>
            <div className="hidden 2xl:flex items-center gap-1 px-2 py-0.5 bg-slate-900 text-amber-300 border border-slate-700 rounded-lg text-xs font-mono font-bold">
              <Calendar size={11} className="text-amber-400" />
              <span>{todayFormatted}</span>
            </div>
          </div>
        </div>

        {/* 2단: 카드/캔버스 & 화살표/연결선 캔버스 편집 통합 툴바 */}
        <div className="px-4 py-1.5 bg-slate-50/70 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3 overflow-x-auto custom-scrollbar">
          {/* 🖐️ 카드/캔버스 편집 그룹 */}
          <div className="flex items-center gap-1.5 flex-shrink-0">
            <span className="text-[11px] font-black text-slate-500 pr-1 whitespace-nowrap">
              카드·캔버스:
            </span>

            {/* 이동 / 선택 세그먼트 모드 */}
            <div className="flex items-center gap-0.5 bg-slate-200/80 p-0.5 rounded-lg border border-slate-300/80">
              <button
                onClick={() => setSelectMode(false)}
                className={`flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs transition-all ${
                  !isSelectMode
                    ? 'bg-white text-indigo-700 font-black shadow-2xs border border-slate-300/80'
                    : 'text-slate-600 font-bold hover:text-slate-900'
                }`}
                title="화면 이동 모드"
              >
                🖐️ 이동
              </button>
              <button
                onClick={() => setSelectMode(true)}
                className={`flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs transition-all ${
                  isSelectMode
                    ? 'bg-white text-indigo-700 font-black shadow-2xs border border-slate-300/80'
                    : 'text-slate-600 font-bold hover:text-slate-900'
                }`}
                title="다중 선택 모드"
              >
                🖱️ 선택
              </button>
            </div>

            {/* Undo / Redo */}
            <div className="flex items-center gap-0.5">
              <button
                onClick={undo}
                disabled={past.length === 0}
                className={`p-1 rounded-lg border transition-all ${
                  past.length > 0 ? 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100' : 'bg-slate-100 border-slate-200 text-slate-300 cursor-not-allowed'
                }`}
                title="실행 취소 (Ctrl+Z)"
              >
                <Undo2 size={13} />
              </button>
              <button
                onClick={redo}
                disabled={future.length === 0}
                className={`p-1 rounded-lg border transition-all ${
                  future.length > 0 ? 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100' : 'bg-slate-100 border-slate-200 text-slate-300 cursor-not-allowed'
                }`}
                title="다시 실행 (Ctrl+Y)"
              >
                <Redo2 size={13} />
              </button>
            </div>

            {/* 서식 복사 / 붙여넣기 */}
            <div className="flex items-center gap-0.5">
              <button
                onClick={handleCopyStyle}
                disabled={selectedCount === 0}
                className={`p-1 rounded-lg border transition-all ${
                  selectedCount > 0 ? 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100' : 'bg-slate-100 border-slate-200 text-slate-300 cursor-not-allowed'
                }`}
                title="서식 복사"
              >
                <Paintbrush size={13} />
              </button>
              <button
                onClick={handlePasteStyle}
                disabled={!copiedStyle}
                className={`p-1 rounded-lg border transition-all ${
                  copiedStyle ? 'bg-indigo-600 text-white border-indigo-600 shadow-2xs' : 'bg-slate-100 border-slate-200 text-slate-300 cursor-not-allowed'
                }`}
                title="서식 붙여넣기"
              >
                <Clipboard size={13} />
              </button>
            </div>

            {/* 카드 생성 */}
            <div className="flex items-center gap-1 border-l border-slate-200 dark:border-slate-700 pl-2">
              <button onClick={handleAddNode} className="flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-slate-100 border border-slate-300 text-slate-800 font-extrabold rounded-lg text-xs shadow-2xs" title="액티비티 카드 추가">
                <Plus size={12} className="text-indigo-600" /> 카드
              </button>
              <button onClick={handleAddTextNode} className="flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-slate-100 border border-slate-300 text-slate-800 font-extrabold rounded-lg text-xs shadow-2xs" title="텍스트 추가">
                <Type size={12} className="text-slate-600" /> 텍스트
              </button>
              <button onClick={handleAddChecklistHeaderNode} className="flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-slate-100 border border-slate-300 text-slate-800 font-extrabold rounded-lg text-xs shadow-2xs" title="체크상자 추가">
                <Type size={12} className="text-slate-600" /> 체크상자
              </button>
            </div>

            {/* 정렬 */}
            <div className="flex items-center gap-0.5 border-l border-slate-200 dark:border-slate-700 pl-2">
              <button onClick={handleAlignHorizontal} className="flex items-center gap-0.5 px-1.5 py-0.5 bg-white hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-extrabold rounded-lg" title="가로 정렬">
                <GripHorizontal size={12} /> 가로
              </button>
              <button onClick={handleAlignVertical} className="flex items-center gap-0.5 px-1.5 py-0.5 bg-white hover:bg-slate-100 border border-slate-300 text-slate-700 text-xs font-extrabold rounded-lg" title="세로 정렬">
                <GripVertical size={12} /> 세로
              </button>
            </div>

            {/* 🔤 박스 글자크기 조절 (선택 카드 / 전체 일괄 통일) */}
            <div className="flex items-center gap-1 border-l border-slate-200 dark:border-slate-700 pl-2">
              <span className="text-[11px] font-black text-slate-500 whitespace-nowrap">글자크기:</span>
              <div className="flex items-center gap-0.5 bg-white border border-slate-300 rounded-lg p-0.5 shadow-2xs">
                <button
                  onClick={() => handleChangeSelectedFontSize(-1.5)}
                  className="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-black rounded text-xs transition-colors"
                  title="선택한 카드 글자 크기 축소 (-1.5px)"
                >
                  A-
                </button>
                <button
                  onClick={() => handleChangeSelectedFontSize(1.5)}
                  className="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-black rounded text-xs transition-colors"
                  title="선택한 카드 글자 크기 확대 (+1.5px)"
                >
                  A+
                </button>
              </div>
              <select
                onChange={(e) => {
                  const val = parseFloat(e.target.value);
                  if (!isNaN(val)) {
                    handleApplyAllCardsFontSize(val);
                    e.target.value = "";
                  }
                }}
                defaultValue=""
                className="bg-white border border-slate-300 rounded-lg text-xs font-black px-2 py-0.5 outline-none text-indigo-700 cursor-pointer shadow-2xs hover:bg-slate-50"
                title="현재 맵에 있는 모든 카드의 글자 크기를 한꺼번에 일괄 통일합니다."
              >
                <option value="" disabled>🌐 전체 일괄 통일 ▾</option>
                <option value="12">작게 (12px)</option>
                <option value="14.5">보통 (14.5px)</option>
                <option value="17">크게 (17px)</option>
                <option value="20">특대 (20px)</option>
              </select>
            </div>

            {/* 선택 삭제 */}
            {selectedCount > 0 && (
              <div className="flex items-center gap-1 border-l border-slate-200 dark:border-slate-700 pl-2">
                <span className="text-[11px] text-slate-600 font-bold">{selectedCount}개 선택</span>
                <button onClick={handleDuplicateSelected} className="px-1.5 py-0.5 bg-white hover:bg-slate-100 text-slate-700 font-extrabold rounded-lg border border-slate-300 text-xs" title="복제">
                  <Copy size={12} /> 복제
                </button>
                <button onClick={handleDeleteSelected} className="px-1.5 py-0.5 bg-white hover:bg-red-50 text-red-600 font-extrabold rounded-lg border border-slate-300 text-xs hover:border-red-200" title="삭제">
                  <Trash2 size={12} /> 삭제
                </button>
              </div>
            )}
          </div>

          {/* 🔗 화살표 / 연결선 편집 그룹 */}
          <div className="flex items-center gap-1.5 flex-shrink-0 border-l border-slate-200 dark:border-slate-700 pl-3">
            <span className="text-[11px] font-black text-slate-500 pr-1 whitespace-nowrap">
              화살표·연결선:
            </span>
            <select
              onChange={(e) => handleChangeEdgesStyleType(e.target.value)}
              className="bg-white border border-slate-300 rounded-lg text-xs font-extrabold px-2 py-0.5 outline-none text-slate-800 cursor-pointer shadow-2xs"
              defaultValue="smoothstep"
              title="연결선 모양 변경"
            >
              <option value="smoothstep">📐 수평수직 직각형</option>
              <option value="straight">📏 직통 직선</option>
              <option value="default">〰️ 유선형 곡선</option>
              <option value="dashed">▫️ 대시 점선</option>
            </select>
            <button
              onClick={handleReverseEdgeDirection}
              className="flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-slate-100 border border-slate-300 text-slate-800 font-extrabold rounded-lg text-xs shadow-2xs"
              title="선택 화살표 방향 역전"
            >
              <RefreshCw size={12} /> 방향역전
            </button>
            <button
              onClick={handleDeleteSingleSelectedEdge}
              className="flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-red-50 text-slate-700 hover:text-red-600 border border-slate-300 hover:border-red-200 font-extrabold rounded-lg text-xs shadow-2xs"
              title="선택 연결선 삭제"
            >
              <Scissors size={12} /> 선택선 삭제
            </button>
            <button
              onClick={handleDeleteAllEdges}
              className="flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-red-50 text-slate-700 hover:text-red-600 border border-slate-300 hover:border-red-200 font-extrabold rounded-lg text-xs shadow-2xs"
              title="전체 연결선 일괄 삭제"
            >
              <Scissors size={12} /> 전체선 삭제
            </button>
          </div>
        </div>
      </header>

      {/* 📂 공종 선택 메뉴 (다중 공종 시트 선택 탭 바 - 산뜻한 프리미엄 탭 디자인) */}
      {disciplineMaps && disciplineMaps.length > 0 && (
        <div className={`flex items-center gap-2 px-4 py-1.5 border-b flex-shrink-0 select-none overflow-x-auto custom-scrollbar transition-colors ${
          isDarkMode ? 'bg-slate-900 border-slate-800 text-slate-200' : 'bg-slate-50/90 border-slate-200/80 text-slate-800'
        }`}>
          <div className="flex items-center gap-1.5 text-xs font-extrabold text-slate-500 mr-1 flex-shrink-0">
            <Layers size={14} className="text-indigo-600" />
            <span>공종 선택:</span>
          </div>
          <div className="flex items-center gap-1.5 overflow-x-auto scrollbar-none py-0.5">
            {disciplineMaps.map((mapItem) => {
              const isActive = mapItem.id === activeDisciplineId;
              return (
                <button
                  key={mapItem.id}
                  onClick={() => selectDisciplineMap(mapItem.id)}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs transition-all flex-shrink-0 ${
                    isActive
                      ? 'bg-white text-slate-900 font-extrabold border border-slate-300 border-b-2 border-b-indigo-600 shadow-2xs'
                      : isDarkMode
                      ? 'bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700'
                      : 'bg-transparent text-slate-600 font-bold border border-transparent hover:bg-white/70 hover:text-slate-900'
                  }`}
                >
                  <span>{mapItem.name}</span>
                  <span
                    className={`px-1.5 py-0.2 text-[10px] rounded-full font-bold ${
                      isActive
                        ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/50'
                        : 'bg-slate-200/70 text-slate-500'
                    }`}
                  >
                    {mapItem.itemCount}개
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      <div className="flex-1 w-full flex overflow-hidden">
        <main ref={flowRef} className="flex-1 h-full overflow-hidden relative">
          {(!disciplineMaps || disciplineMaps.length === 0 || nodes.length === 0) && (
            <div className="absolute inset-0 z-30 flex items-center justify-center bg-indigo-950/20 backdrop-blur-md p-6 select-none">
              <div className="max-w-xl w-full bg-white border-2 border-indigo-200/90 rounded-3xl shadow-2xl shadow-indigo-500/10 p-8 text-center space-y-6 animate-fade-in">
                <div className="w-20 h-20 bg-indigo-50 rounded-2xl flex items-center justify-center mx-auto text-indigo-600 border border-indigo-200 shadow-inner">
                  <Upload size={38} className="text-indigo-600" />
                </div>

                <div className="space-y-2">
                  <h2 className="text-2xl font-black tracking-tight text-slate-900">
                    📊 WBS 엑셀 파일 불러오기
                  </h2>
                  <p className="text-sm text-slate-600 font-medium leading-relaxed">
                    공종 시트별 WBS 엑셀 파일을 불러와<br />
                    공정 프로세스 맵을 즉시 자동 생성해 보세요!
                  </p>
                </div>

                <div className="pt-1">
                  <label className="inline-flex items-center justify-center gap-2.5 px-8 py-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 hover:from-indigo-700 hover:to-purple-800 text-white font-black text-base rounded-2xl shadow-xl shadow-indigo-500/30 hover:scale-105 transition-all cursor-pointer ring-2 ring-indigo-400/50">
                    <Upload size={22} />
                    <span>📁 WBS 엑셀 파일 선택 및 불러오기</span>
                    <input type="file" accept=".xlsx,.xls,.xlsm,.csv" onChange={handleImportExcelWbs} className="hidden" />
                  </label>
                </div>

                <div className="pt-3 border-t border-indigo-100 bg-indigo-50/60 py-2.5 px-4 rounded-xl text-xs text-slate-600 font-bold flex items-center justify-center gap-3">
                  <span>💡 지원 파일: .xlsx, .xlsm, .csv</span>
                  <span>•</span>
                  <span>⚡ 공종 시트 및 WBS 항목 자동 파싱</span>
                </div>
              </div>
            </div>
          )}

          {/* 📱 모바일/태블릿 전용 터치 플로팅 퀵 툴바 */}
          <div className="fixed bottom-4 right-4 z-40 flex items-center gap-1.5 sm:hidden bg-slate-900/95 backdrop-blur-lg text-white p-2 rounded-2xl border border-slate-700/80 shadow-2xl touch-manipulation select-none">
            <button
              onClick={triggerFitView}
              className="flex items-center gap-1 px-3 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-black rounded-xl text-xs shadow-lg active:scale-95 transition-transform"
              title="화면 전체 맞춤"
            >
              <Sparkles size={14} className="text-amber-300" />
              <span>🔍 전체 맞춤</span>
            </button>
            <button
              onClick={() => setSelectMode(!isSelectMode)}
              className={`px-3 py-2 rounded-xl text-xs font-black transition-all ${
                isSelectMode ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300'
              }`}
            >
              {isSelectMode ? '🖱️ 선택' : '🖐️ 이동'}
            </button>
            <button
              onClick={handleAddNode}
              className="px-2.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-black rounded-xl text-xs shadow-sm"
              title="새 카드 추가"
            >
              <Plus size={14} />
            </button>
            <button
              onClick={() => setShowHelp(true)}
              className="p-2 bg-indigo-700 text-indigo-100 rounded-xl text-xs font-black"
              title="도움말"
            >
              <HelpCircle size={15} />
            </button>
          </div>

          <FlowMap
            onNodeDoubleClick={() => setShowSidebar(true)}
            onEdgeDoubleClick={() => setShowSidebar(true)}
          />
        </main>
        
        {/* 우측 상세 편집 사이드바 */}
        <aside className={`h-full border-l border-gray-200 bg-white shadow-lg transition-all duration-300 ease-in-out flex flex-col flex-shrink-0 ${isSidebarOpen ? 'w-96' : 'w-0 overflow-hidden border-none'}`}>
          {isSidebarOpen && (
            selectedNode ? (
              <div key={selectedNode.id} className="flex flex-col h-full w-96 text-xs text-gray-700">
                {/* Sidebar Header */}
                <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/50">
                  <div>
                    <h2 className="text-sm font-bold text-gray-800">
                      {selectedNode.type === 'action' && '📋 카드 상세 편집'}
                      {selectedNode.type === 'milestone' && '🏁 마일스톤 편집'}
                      {selectedNode.type === 'text' && '✍️ 텍스트 편집'}
                      {selectedNode.type === 'image' && '🖼️ 이미지 편집'}
                      {selectedNode.type === 'checklistItem' && '✅ 체크리스트 상세 편집'}
                      {selectedNode.type === 'checklistHeader' && '🔲 체크 글상자 편집'}
                      {selectedNode.type === 'tableTitle' && '📌 표 제목 편집'}
                    </h2>
                    <p className="text-[10px] text-gray-400 mt-0.5 font-mono">ID: {selectedNode.id.substring(0, 8)}...</p>
                  </div>
                  <button
                    onClick={() => {
                      setNodesAndEdges(
                        nodes.map(n => n.id === selectedNode.id ? { ...n, selected: false } : n),
                        edges
                      );
                    }}
                    className="p-1.5 rounded-full hover:bg-gray-200 text-gray-400 transition-colors"
                  >
                    <X size={15} />
                  </button>
                </div>

                {/* Sidebar Content (Scrollable) */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
                  {selectedNode.type === 'action' && (
                    <>
                      {/* 3-Tab Selector: 표준서 | 수행지침 | 체크리스트 (밝고 깔끔한 세그먼트) */}
                      <div className="flex border border-slate-200 bg-slate-100 p-1 rounded-xl gap-1 shadow-inner">
                        <button
                          onClick={() => setActiveDetailTab('standard')}
                          className={`flex-1 py-1.5 px-1 rounded-lg font-extrabold text-[11.5px] flex items-center justify-center gap-1.5 transition-all ${
                            activeDetailTab === 'standard'
                              ? 'bg-white text-indigo-700 shadow-2xs border border-slate-200 ring-1 ring-indigo-500/20'
                              : 'text-slate-600 font-bold hover:text-slate-900 hover:bg-slate-50'
                          }`}
                        >
                          <FileText size={13} />
                          <span>표준서</span>
                        </button>
                        <button
                          onClick={() => setActiveDetailTab('directive')}
                          className={`flex-1 py-1.5 px-1 rounded-lg font-extrabold text-[11.5px] flex items-center justify-center gap-1.5 transition-all ${
                            activeDetailTab === 'directive'
                              ? 'bg-white text-indigo-700 shadow-2xs border border-slate-200 ring-1 ring-indigo-500/20'
                              : 'text-slate-600 font-bold hover:text-slate-900 hover:bg-slate-50'
                          }`}
                        >
                          <ClipboardList size={13} />
                          <span>수행지침</span>
                        </button>
                        <button
                          onClick={() => setActiveDetailTab('checklist')}
                          className={`flex-1 py-1.5 px-1 rounded-lg font-extrabold text-[11.5px] flex items-center justify-center gap-1.5 transition-all ${
                            activeDetailTab === 'checklist'
                              ? 'bg-white text-indigo-700 shadow-2xs border border-slate-200 ring-1 ring-indigo-500/20'
                              : 'text-slate-600 font-bold hover:text-slate-900 hover:bg-slate-50'
                          }`}
                        >
                          <CheckSquare size={13} />
                          <span>체크리스트</span>
                        </button>
                      </div>

                      {/* Header Title */}
                      <div className="flex flex-col bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <label className="font-extrabold text-slate-700 text-[11px] uppercase mb-1.5 flex items-center gap-1">
                          <span>📌 액티비티 공정명</span>
                        </label>
                        <textarea
                          value={selectedNode.data.label || ''}
                          onFocus={takeSnapshot}
                          onChange={e => updateNodeData(selectedNode.id, { label: e.target.value })}
                          className="fancy-input bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-black text-slate-900 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 resize-none h-14 leading-relaxed shadow-2xs"
                          placeholder="제목을 입력하세요..."
                        />
                      </div>



                      {/* TAB 1: 📄 표준서 (Standard / Specifications & Laws) */}
                      {activeDetailTab === 'standard' && (
                        <div className="space-y-3.5 border-t border-slate-200 pt-3.5">
                          {/* 🔗 원본 HTML 매뉴얼 문서 열기 상시 강조 버튼 */}
                          <div className="bg-slate-50 border border-slate-200 text-slate-800 rounded-xl p-3 shadow-2xs flex items-center justify-between gap-2">
                            <div className="flex flex-col min-w-0">
                              <span className="text-[11px] font-black text-slate-800 flex items-center gap-1">
                                <FileText size={14} className="text-indigo-600" /> 원본 매뉴얼 HTML 문서
                              </span>
                              <span className="text-[9.5px] text-slate-500 truncate mt-0.5 font-medium">
                                {selectedNode.data.fileUrl || '매뉴얼BODY(집행단계-첨부폴더)v8 연동'}
                              </span>
                            </div>
                            <button
                              onClick={() => openManualModal(selectedNode.data.label || '표준서 매뉴얼', selectedNode.data.fileUrl)}
                              className="whitespace-nowrap px-3 py-1.5 bg-white text-indigo-700 hover:bg-indigo-50 border border-slate-300 font-extrabold rounded-lg text-xs shadow-2xs flex items-center gap-1.5 transition-all flex-shrink-0"
                            >
                              <span>열기</span>
                              <ExternalLink size={13} />
                            </button>
                          </div>

                          {/* Clean Light Card Banner */}
                          <div className="bg-slate-50 border border-slate-200 text-slate-800 rounded-xl p-3.5 text-xs space-y-2 shadow-2xs">
                            <div className="font-extrabold text-slate-800 flex items-center gap-1.5 text-xs">
                              <FileText size={15} className="text-indigo-600" />
                              <span>관련 표준 시방서 및 건설 관계 법령</span>
                            </div>
                            <div className="text-[12px] text-slate-900 leading-relaxed font-extrabold bg-white p-2.5 rounded-lg border border-slate-200 shadow-2xs">
                              {selectedNode.data.purpose || 'KDS/KCS 시방서 및 토지보상법/도로교통법 준수 요망'}
                            </div>
                          </div>

                          <div className="flex flex-col space-y-1">
                            <label className="font-bold text-slate-700 text-xs">📌 적용 법령 / 시방서 규정 상세</label>
                            <textarea
                              value={selectedNode.data.purpose || ''}
                              onFocus={takeSnapshot}
                              onChange={e => updateNodeData(selectedNode.id, { purpose: e.target.value })}
                              className="fancy-input bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-bold text-slate-900 focus:bg-white resize-y h-24 leading-relaxed shadow-2xs"
                              placeholder="예: KCS 47 10 25 시방 검토 | 지하안전법 제23조..."
                            />
                          </div>

                          <div className="flex flex-col space-y-1">
                            <label className="font-bold text-slate-700 text-xs">📎 표준서 HTML 파일 경로 / 외부 링크</label>
                            <input
                              type="text"
                              value={selectedNode.data.fileUrl || ''}
                              onFocus={takeSnapshot}
                              onChange={e => updateNodeData(selectedNode.id, { fileUrl: e.target.value })}
                              className="fancy-input bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-bold text-slate-900 shadow-2xs"
                              placeholder="C:/Users/sskjh/.../매뉴얼.html 또는 URL 입력"
                            />
                          </div>
                        </div>
                      )}

                      {/* TAB 2: 📋 수행지침 (Execution Directives & Procedures) */}
                      {activeDetailTab === 'directive' && (
                        <div className="space-y-3.5 border-t border-slate-200 pt-3.5">
                          {/* 📅 D-Day 기한 & 🧭 일정 Phase (가로축 자동 배치 & 카드 뱃지 연동) */}
                          <div className="grid grid-cols-2 gap-2.5">
                            <div className="flex flex-col space-y-1">
                              <label className="font-bold text-slate-700 text-xs">📅 D-Day 기한/일정 (뱃지 연동)</label>
                              <input
                                type="text"
                                value={selectedNode.data.date || ''}
                                onFocus={takeSnapshot}
                                onChange={e => updateNodeData(selectedNode.id, { date: e.target.value })}
                                className="fancy-input bg-amber-50/60 border border-amber-300 rounded-lg p-2 text-xs font-black text-slate-900 shadow-2xs focus:bg-white"
                                placeholder="예: D-40, D-90, D-Day"
                              />
                            </div>
                            <div className="flex flex-col space-y-1">
                              <label className="font-bold text-slate-700 text-xs">🧭 가로축 Phase (열 자동 배치)</label>
                              <select
                                value={
                                  selectedNode.position.x < 1200 ? '0' :
                                  selectedNode.position.x < 2350 ? '1' :
                                  selectedNode.position.x < 4400 ? '2' :
                                  selectedNode.position.x < 5100 ? '3' : '4'
                                }
                                onFocus={takeSnapshot}
                                onChange={e => {
                                  const pIdx = parseInt(e.target.value, 10);
                                  const phaseXMap = [480, 1380, 2940, 4480, 5180];
                                  const phaseNameMap = ['D-90', 'D-60', 'D-30', 'D-Day', 'D+10'];
                                  const targetX = phaseXMap[pIdx] || 2940;
                                  const newDate = phaseNameMap[pIdx] || 'D-30';

                                  const { nodes: currentNodes, edges: currentEdges, setNodesAndEdges } = useStore.getState();
                                  const nextNodes = currentNodes.map(n => {
                                    if (n.id === selectedNode.id) {
                                      return {
                                        ...n,
                                        position: { ...n.position, x: targetX },
                                        data: { ...n.data, date: n.data.date || newDate },
                                      };
                                    }
                                    return n;
                                  });
                                  setNodesAndEdges(nextNodes, currentEdges);
                                }}
                                className="fancy-input bg-white border border-slate-300 rounded-lg p-2 text-xs font-bold text-slate-900 shadow-2xs cursor-pointer"
                              >
                                <option value="0">Phase 1: D-90 (사전조사)</option>
                                <option value="1">Phase 2: D-60 (인허가)</option>
                                <option value="2">Phase 3: D-30 (계약/계획)</option>
                                <option value="3">Phase 4: D-Day (착공준비)</option>
                                <option value="4">Phase 5: D+ (본공사집행)</option>
                              </select>
                            </div>
                          </div>

                          <div className="grid grid-cols-2 gap-2.5">
                            <div className="flex flex-col space-y-1">
                              <label className="font-bold text-slate-700 text-xs">🏛️ 주관 부서 (행 자동 배치)</label>
                              <select
                                value={
                                  selectedNode.data.swimlane === '본사' || selectedNode.data.category === '본사' || (selectedNode.data.department || '').startsWith('본사') ? '본사' :
                                  selectedNode.data.swimlane === '공무' || (selectedNode.data.department || '').startsWith('현장 · 공무') ? '공무' :
                                  selectedNode.data.swimlane === '품질' || (selectedNode.data.department || '').startsWith('현장 · 품질') ? '품질' :
                                  selectedNode.data.swimlane === '안전' || (selectedNode.data.department || '').startsWith('현장 · 안전') ? '안전' :
                                  selectedNode.data.swimlane === '관리' || (selectedNode.data.department || '').startsWith('현장 · 관리') ? '관리' :
                                  selectedNode.data.swimlane === '공사' || (selectedNode.data.department || '').startsWith('현장 · 공사') ? '공사' :
                                  (selectedNode.data.department || '').includes('본사') ? '본사' :
                                  (selectedNode.data.department || '').includes('품질') ? '품질' :
                                  (selectedNode.data.department || '').includes('안전') ? '안전' :
                                  (selectedNode.data.department || '').includes('관리') ? '관리' :
                                  (selectedNode.data.department || '').includes('공무') ? '공무' : '공사'
                                }
                                onFocus={takeSnapshot}
                                onChange={e => {
                                  const subDept = e.target.value;
                                  const mainCat = subDept === '본사' ? '본사' : '현장';
                                  const deptBadge = `${mainCat} · ${subDept}`;

                                  const { nodes: currentNodes, edges: currentEdges, setNodesAndEdges } = useStore.getState();
                                  const swimlane = currentNodes.find(n => n.type === 'swimlane' && ((n.data?.label as string) || '').includes(subDept));
                                  const targetY = swimlane ? swimlane.position.y + 60 : selectedNode.position.y;

                                  const nextNodes = currentNodes.map(n => {
                                    if (n.id === selectedNode.id) {
                                      return {
                                        ...n,
                                        position: { ...n.position, y: targetY },
                                        data: { ...n.data, department: deptBadge, swimlane: subDept, category: mainCat },
                                      };
                                    }
                                    return n;
                                  });
                                  setNodesAndEdges(nextNodes, currentEdges);
                                }}
                                className="fancy-input bg-white border border-slate-300 rounded-lg p-2 text-xs font-bold text-slate-900 shadow-2xs cursor-pointer"
                              >
                                <option value="공무">🏢 공무 / 계약 / 인허가</option>
                                <option value="공사">🏗️ 공사 / 현장 시공</option>
                                <option value="품질">🛡️ 품질 / 시공 품질</option>
                                <option value="안전">🚨 안전 / 보건 / 환경</option>
                                <option value="관리">💼 관리 / 용지 / 총무</option>
                                <option value="본사">🏛️ 본사 / 전략 / 지원</option>
                              </select>
                            </div>

                            <div className="flex flex-col space-y-1">
                              <label className="font-bold text-slate-700 text-xs">🤝 협조 부서</label>
                              <input
                                type="text"
                                value={selectedNode.data.cooperation || ''}
                                onFocus={takeSnapshot}
                                onChange={e => updateNodeData(selectedNode.id, { cooperation: e.target.value })}
                                className="fancy-input bg-white border border-slate-300 rounded-lg p-2 text-xs font-bold text-slate-900 shadow-2xs"
                                placeholder="예: 공사팀, 감리단"
                              />
                            </div>
                          </div>

                          <div className="flex flex-col space-y-1">
                            <label className="font-bold text-slate-700 text-xs">⚙️ 상세 수행지침 절차 (1➔2➔3➔4)</label>
                            <textarea
                              value={selectedNode.data.method || ''}
                              onFocus={takeSnapshot}
                              onChange={e => updateNodeData(selectedNode.id, { method: e.target.value })}
                              className="fancy-input bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-bold text-slate-900 resize-y h-28 leading-relaxed custom-scrollbar shadow-2xs"
                              placeholder="1) 수행단계1 ➔ 2) 수행단계2..."
                            />
                          </div>

                          {/* 🔗 원본 HTML 매뉴얼 문서 열기 상시 강조 버튼 */}
                          <div className="bg-slate-50 border border-slate-200 text-slate-800 rounded-xl p-3 shadow-2xs flex items-center justify-between gap-2">
                            <div className="flex flex-col min-w-0">
                              <span className="text-[11px] font-black text-slate-800 flex items-center gap-1">
                                <ClipboardList size={14} className="text-indigo-600" /> 수행지침 원본 HTML 매뉴얼
                              </span>
                              <span className="text-[9.5px] text-slate-500 truncate mt-0.5 font-medium">
                                {selectedNode.data.fileUrl || '매뉴얼BODY(집행단계-첨부폴더)v8 연동'}
                              </span>
                            </div>
                            <button
                              onClick={() => openManualModal(selectedNode.data.label || '수행지침 매뉴얼', selectedNode.data.fileUrl)}
                              className="whitespace-nowrap px-3 py-1.5 bg-white text-indigo-700 hover:bg-indigo-50 border border-slate-300 font-extrabold rounded-lg text-xs shadow-2xs flex items-center gap-1.5 transition-all flex-shrink-0"
                            >
                              <span>열기</span>
                              <ExternalLink size={13} />
                            </button>
                          </div>

                          {/* Clean Light Card Banner */}
                          <div className="bg-slate-50 border border-slate-200 text-slate-800 rounded-xl p-3.5 text-xs space-y-2 shadow-2xs">
                            <div className="font-extrabold text-slate-800 flex items-center gap-1.5 text-xs">
                              <ClipboardList size={15} className="text-indigo-600" />
                              <span>단계별 현장 수행 절차 (Execution Directives)</span>
                            </div>
                            <div className="text-[12px] text-slate-900 leading-relaxed font-extrabold bg-white p-2.5 rounded-lg border border-slate-200 shadow-2xs">
                              {selectedNode.data.method || '1) 현장조사 ➔ 2) 심의 ➔ 3) 승인 ➔ 4) 완료'}
                            </div>
                          </div>
                        </div>
                      )}

                      {/* TAB 3: ✅ 체크리스트 (Interactive Checklist & Deliverables) */}
                      {activeDetailTab === 'checklist' && (
                        <div className="space-y-3.5 border-t border-slate-200 pt-3.5">
                          {/* 🔗 원본 HTML 매뉴얼 문서 열기 상시 강조 버튼 */}
                          <div className="bg-slate-50 border border-slate-200 text-slate-800 rounded-xl p-3 shadow-2xs flex items-center justify-between gap-2">
                            <div className="flex flex-col min-w-0">
                              <span className="text-[11px] font-black text-slate-800 flex items-center gap-1">
                                <CheckSquare size={14} className="text-indigo-600" /> 체크리스트 원본 HTML 매뉴얼
                              </span>
                              <span className="text-[9.5px] text-slate-500 truncate mt-0.5 font-medium">
                                {selectedNode.data.fileUrl || '매뉴얼BODY(집행단계-첨부폴더)v8 연동'}
                              </span>
                            </div>
                            <button
                              onClick={() => openManualModal(selectedNode.data.label || '체크리스트 매뉴얼', selectedNode.data.fileUrl)}
                              className="whitespace-nowrap px-3 py-1.5 bg-white text-indigo-700 hover:bg-indigo-50 border border-slate-300 font-extrabold rounded-lg text-xs shadow-2xs flex items-center gap-1.5 transition-all flex-shrink-0"
                            >
                              <span>열기</span>
                              <ExternalLink size={13} />
                            </button>
                          </div>
                          {/* Status Segmented Control */}
                          <div className="flex flex-col space-y-1.5">
                            <label className="font-bold text-slate-700 text-xs">🚦 이행 및 검측 상태 판정</label>
                            <div className="grid grid-cols-4 gap-1.5 p-1 bg-slate-100 rounded-xl border border-slate-200">
                              {(['normal', 'warning', 'danger', 'done'] as const).map(st => {
                                const active = (selectedNode.data.status || 'normal') === st;
                                const labelMap = { normal: '🟢 정상', warning: '🟡 주의', danger: '🔴 위험', done: '⚪ 완료' };
                                const colorMap = {
                                  normal: active ? 'bg-emerald-600 text-white shadow-2xs font-extrabold' : 'text-slate-600 font-bold hover:bg-slate-200/60',
                                  warning: active ? 'bg-amber-500 text-white shadow-2xs font-extrabold' : 'text-slate-600 font-bold hover:bg-slate-200/60',
                                  danger: active ? 'bg-rose-600 text-white shadow-2xs font-extrabold' : 'text-slate-600 font-bold hover:bg-slate-200/60',
                                  done: active ? 'bg-slate-700 text-white shadow-2xs font-extrabold' : 'text-slate-600 font-bold hover:bg-slate-200/60',
                                };
                                return (
                                  <button
                                    key={st}
                                    onClick={() => {
                                      takeSnapshot();
                                      updateNodeData(selectedNode.id, { status: st });
                                    }}
                                    className={`py-1.5 text-[10.5px] rounded-lg transition-all text-center ${colorMap[st]}`}
                                  >
                                    {labelMap[st]}
                                  </button>
                                );
                              })}
                            </div>
                          </div>

                          <div className="flex flex-col space-y-1">
                            <label className="font-bold text-slate-700 text-xs">🎁 제출 필수 산출물 (Deliverables)</label>
                            <input
                              type="text"
                              value={selectedNode.data.result || ''}
                              onFocus={takeSnapshot}
                              onChange={e => updateNodeData(selectedNode.id, { result: e.target.value })}
                              className="fancy-input bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-bold text-slate-900 shadow-2xs"
                              placeholder="예: 지자체 허가 필증, 검측 성과표..."
                            />
                          </div>

                          <div className="flex flex-col space-y-1">
                            <label className="font-bold text-slate-700 text-xs">📝 체크리스트 비고 및 미결 메모</label>
                            <textarea
                              value={selectedNode.data.note || ''}
                              onFocus={takeSnapshot}
                              onChange={e => updateNodeData(selectedNode.id, { note: e.target.value })}
                              className="fancy-input bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-bold text-slate-900 resize-y h-24 leading-relaxed shadow-2xs"
                              placeholder="현장 특이사항 및 후속조치 메모..."
                            />
                          </div>
                        </div>
                      )}
                    </>
                  )}

                  {selectedNode.type === 'milestone' && (() => {
                    let sidebarDateVal = selectedNode.data.date || '';
                    let sidebarLabelVal = selectedNode.data.label || '';

                    if (selectedNode.data.date === undefined) {
                      const m = sidebarLabelVal.match(/^(D-\d+|P\+\d+|D\+\d+|[+-]\d+|D-Day)\s*(.*)$/i);
                      if (m) {
                        sidebarDateVal = m[1];
                        sidebarLabelVal = m[2] ? m[2].trim() : '';
                      }
                    }

                    return (
                      <div className="flex flex-col space-y-4">
                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">기한 / 기간 (날짜 정보)</label>
                          <input
                            type="text"
                            value={sidebarDateVal}
                            onFocus={takeSnapshot}
                            onChange={e => {
                              updateNodeData(selectedNode.id, { 
                                date: e.target.value,
                                label: sidebarLabelVal 
                              });
                            }}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs font-semibold text-gray-800 focus:bg-white"
                            placeholder="예: P+0, D-180"
                          />
                        </div>

                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">마일스톤 단계명</label>
                          <input
                            type="text"
                            value={sidebarLabelVal}
                            onFocus={takeSnapshot}
                            onChange={e => {
                              updateNodeData(selectedNode.id, { 
                                label: e.target.value,
                                date: sidebarDateVal 
                              });
                            }}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs font-semibold text-gray-800 focus:bg-white"
                            placeholder="예: 현장개설"
                          />
                        </div>

                        {selectedNode.data.daysRemaining !== undefined && (
                          <div className="flex flex-col">
                            <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">실제 잔여일수</label>
                            <div className="bg-gray-50 border border-gray-200 rounded-lg p-2.5 text-xs text-gray-800 font-medium">
                              {selectedNode.data.daysRemaining} 일 남음
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })()}

                  {selectedNode.type === 'checklistHeader' && (() => {
                    const ts = selectedNode.data.textStyle || {};
                    const bgColor = ts.bgColor || '#1e293b';
                    const textColor = ts.color || '#ffffff';
                    const borderStyle = ts.borderStyle || 'solid';
                    const borderWidth = ts.borderWidth !== undefined ? ts.borderWidth : 1;
                    const fontSize = ts.fontSize || 12;

                    const updateStyle = (patch: any) => {
                      updateNodeData(selectedNode.id, {
                        textStyle: { ...ts, ...patch }
                      });
                    };

                    return (
                      <div className="flex flex-col space-y-4">
                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">글상자 내용</label>
                          <input
                            type="text"
                            value={selectedNode.data.label || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { label: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs font-semibold text-gray-800 focus:bg-white"
                            placeholder="예: 본공사수행"
                          />
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                          {/* 채움색 */}
                          <div className="flex flex-col">
                            <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">채움색 (배경색)</label>
                            <div className="flex items-center gap-1.5">
                              <input
                                type="color"
                                value={bgColor.startsWith('#') ? bgColor : '#1e293b'}
                                onFocus={takeSnapshot}
                                onChange={e => updateStyle({ bgColor: e.target.value })}
                                className="w-8 h-8 rounded border border-gray-200 cursor-pointer p-0"
                              />
                              <select
                                value={bgColor}
                                onChange={e => {
                                  takeSnapshot();
                                  updateStyle({ bgColor: e.target.value });
                                }}
                                className="fancy-input flex-1 bg-gray-50 border border-gray-200 rounded-lg p-1.5 text-xs text-gray-800"
                              >
                                <option value="#1e293b">짙은 남색 (기본)</option>
                                <option value="#ffffff">하양</option>
                                <option value="#f8fafc">밝은 회색</option>
                                <option value="#fef08a">노랑</option>
                                <option value="#bfdbfe">파랑</option>
                                <option value="#bbf7d0">연두</option>
                                <option value="#fbcfe8">분홍</option>
                                <option value="transparent">투명</option>
                              </select>
                            </div>
                          </div>

                          {/* 글자 색상 */}
                          <div className="flex flex-col">
                            <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">글자 색상</label>
                            <div className="flex items-center gap-1.5">
                              <input
                                type="color"
                                value={textColor.startsWith('#') ? textColor : '#ffffff'}
                                onFocus={takeSnapshot}
                                onChange={e => updateStyle({ color: e.target.value })}
                                className="w-8 h-8 rounded border border-gray-200 cursor-pointer p-0"
                              />
                              <select
                                value={textColor}
                                onChange={e => {
                                  takeSnapshot();
                                  updateStyle({ color: e.target.value });
                                }}
                                className="fancy-input flex-1 bg-gray-50 border border-gray-200 rounded-lg p-1.5 text-xs text-gray-800"
                              >
                                <option value="#ffffff">하양 (기본)</option>
                                <option value="#1e293b">짙은 남색</option>
                                <option value="#ef4444">빨강</option>
                                <option value="#3b82f6">파랑</option>
                                <option value="#10b981">초록</option>
                              </select>
                            </div>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                          {/* 테두리 선 종류 */}
                          <div className="flex flex-col">
                            <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">테두리 선 종류</label>
                            <select
                              value={borderStyle}
                              onFocus={takeSnapshot}
                              onChange={e => updateStyle({ borderStyle: e.target.value })}
                              className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800"
                            >
                              <option value="solid">실선 (solid)</option>
                              <option value="dashed">점선 (dashed)</option>
                              <option value="dotted">점선 (dotted)</option>
                              <option value="double">이중선 (double)</option>
                              <option value="none">선 없음 (none)</option>
                            </select>
                          </div>

                          {/* 테두리 선 굵기 */}
                          <div className="flex flex-col">
                            <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">테두리 선 굵기</label>
                            <select
                              value={borderWidth}
                              onFocus={takeSnapshot}
                              onChange={e => updateStyle({ borderWidth: Number(e.target.value) })}
                              className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800"
                              disabled={borderStyle === 'none'}
                            >
                              <option value={1}>1px</option>
                              <option value={2}>2px</option>
                              <option value={3}>3px</option>
                              <option value={4}>4px</option>
                              <option value={5}>5px</option>
                            </select>
                          </div>
                        </div>

                        {/* 글자 크기 */}
                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">글자 크기</label>
                          <select
                            value={fontSize}
                            onFocus={takeSnapshot}
                            onChange={e => updateStyle({ fontSize: Number(e.target.value) })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800"
                          >
                            {[10, 11, 12, 13, 14, 16, 18, 20, 24, 28].map(sz => (
                              <option key={sz} value={sz}>{sz}px</option>
                            ))}
                          </select>
                        </div>
                      </div>
                    );
                  })()}

                  {selectedNode.type === 'checklistItem' && (
                    <div className="flex flex-col space-y-3">
                      {/* 상태 조절 */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">상태</label>
                        <select
                          value={selectedNode.data.status || 'todo'}
                          onFocus={takeSnapshot}
                          onChange={(e) => updateNodeData(selectedNode.id, { status: e.target.value as any })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white cursor-pointer"
                        >
                          <option value="todo">미착수 (Slate)</option>
                          <option value="inprogress">진행중 (Amber)</option>
                          <option value="done">완료 (Emerald)</option>
                          <option value="na">N/A (Light Slate)</option>
                        </select>
                      </div>

                      {/* 내용 */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">점검 항목명 (내용)</label>
                        <textarea
                          value={selectedNode.data.label || ''}
                          onFocus={takeSnapshot}
                          onChange={(e) => updateNodeData(selectedNode.id, { label: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white resize-y h-20"
                          placeholder="점검 항목 내용을 입력하세요..."
                        />
                      </div>

                      {/* 담당 부서 / 담당자 */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">담당자/부서</label>
                        <input
                          type="text"
                          value={selectedNode.data.department || ''}
                          onFocus={takeSnapshot}
                          onChange={(e) => updateNodeData(selectedNode.id, { department: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                          placeholder="담당자 또는 담당 부서..."
                        />
                      </div>

                      {/* 협조 부서 */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">협조 부서</label>
                        <input
                          type="text"
                          value={selectedNode.data.cooperation || ''}
                          onFocus={takeSnapshot}
                          onChange={(e) => updateNodeData(selectedNode.id, { cooperation: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                          placeholder="협조 부서 입력 (쉼표 구분)..."
                        />
                      </div>

                      {/* 메모 */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">상세 내용/메모</label>
                        <textarea
                          value={selectedNode.data.note || ''}
                          onFocus={takeSnapshot}
                          onChange={(e) => updateNodeData(selectedNode.id, { note: e.target.value })}
                          rows={4}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white resize-y"
                          placeholder="추가 설명 또는 조치 결과를 입력하세요..."
                        />
                      </div>
                    </div>
                  )}

                  {selectedNode.type === 'text' && (
                    <div className="flex flex-col space-y-3">
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">텍스트 내용</label>
                        <textarea
                          value={selectedNode.data.label || ''}
                          onFocus={takeSnapshot}
                          onChange={e => updateNodeData(selectedNode.id, { label: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white resize-y h-32 leading-relaxed"
                          placeholder="텍스트를 입력하세요..."
                        />
                      </div>
                    </div>
                  )}

                  {selectedNode.type === 'image' && (
                    <div className="flex flex-col space-y-3">
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">이미지 설명 (캡션)</label>
                        <input
                          type="text"
                          value={(selectedNode.data as any).caption || ''}
                          onChange={e => updateNodeData(selectedNode.id, { caption: e.target.value } as any)}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                          placeholder="이미지 하단에 표시될 캡션..."
                        />
                      </div>
                      <div className="border border-gray-100 rounded-lg p-2 bg-gray-50 flex items-center justify-center overflow-hidden h-40">
                        <img
                          src={(selectedNode.data as any).imageDataUrl}
                          alt="미리보기"
                          className="max-h-full max-w-full object-contain rounded"
                        />
                      </div>
                    </div>
                  )}

                  {selectedNode.type === 'tableTitle' && (
                    <div className="flex flex-col space-y-3">
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">표 제목 내용</label>
                        <input
                          type="text"
                          value={selectedNode.data.label || ''}
                          onFocus={takeSnapshot}
                          onChange={e => updateNodeData(selectedNode.id, { label: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                          placeholder="표 제목을 입력하세요..."
                        />
                      </div>
                    </div>
                  )}
                </div>

              </div>
            ) : selectedEdge ? (
              <div key={selectedEdge.id} className="flex flex-col h-full w-96 text-xs text-gray-700">
                {/* Sidebar Header */}
                <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/50">
                  <div>
                    <h2 className="text-sm font-bold text-gray-800">🔗 연결선 상세 편집</h2>
                    <p className="text-[10px] text-gray-400 mt-0.5 font-mono">ID: {selectedEdge.id.substring(0, 8)}...</p>
                  </div>
                  <button
                    onClick={() => {
                      setNodesAndEdges(
                        nodes,
                        edges.map(e => e.id === selectedEdge.id ? { ...e, selected: false } : e)
                      );
                    }}
                    className="p-1.5 rounded-full hover:bg-gray-200 text-gray-400 transition-colors"
                  >
                    <X size={15} />
                  </button>
                </div>

                {/* Sidebar Content (Scrollable) */}
                <div className="flex-1 overflow-y-auto p-4 space-y-5 custom-scrollbar">
                  {/* 🔥 찐하게 (초고대비 굵은선) Quick Preset Actions */}
                  <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl space-y-2">
                    <span className="font-bold text-amber-900 text-[11px] flex items-center gap-1">
                      🔥 연결선 선명도 (찐하게)
                    </span>
                    <div className="grid grid-cols-2 gap-1.5">
                      <button
                        onClick={() => {
                          takeSnapshot();
                          const currentStroke = selectedEdge.style?.stroke || '#b91c1c';
                          // If current color is too faint or light, convert to vivid dark red/blue
                          const vividStroke = (currentStroke === '#94a3b8' || currentStroke === '#ef4444') ? '#b91c1c' : currentStroke;
                          const style = { ...selectedEdge.style, stroke: vividStroke, strokeWidth: 6, strokeDasharray: undefined };
                          let markerStart = selectedEdge.markerStart;
                          if (markerStart && typeof markerStart === 'object') {
                            markerStart = { ...markerStart, color: vividStroke, width: 18, height: 18 };
                          }
                          let markerEnd = selectedEdge.markerEnd;
                          if (markerEnd && typeof markerEnd === 'object') {
                            markerEnd = { ...markerEnd, color: vividStroke, width: 18, height: 18 };
                          }
                          updateEdge(selectedEdge.id, { style, markerStart, markerEnd });
                        }}
                        className="py-2 px-2.5 bg-red-600 hover:bg-red-700 text-white font-black rounded-lg text-xs shadow-sm transition-all flex items-center justify-center gap-1"
                        title="이 연결선을 6px 초고대비 찐한 선으로 변경"
                      >
                        🔥 찐하게 (6px)
                      </button>
                      <button
                        onClick={() => {
                          takeSnapshot();
                          const currentStroke = selectedEdge.style?.stroke || '#1d4ed8';
                          const vividStroke = (currentStroke === '#94a3b8' || currentStroke === '#ef4444') ? '#1d4ed8' : currentStroke;
                          const style = { ...selectedEdge.style, stroke: vividStroke, strokeWidth: 8, strokeDasharray: undefined };
                          let markerStart = selectedEdge.markerStart;
                          if (markerStart && typeof markerStart === 'object') {
                            markerStart = { ...markerStart, color: vividStroke, width: 20, height: 20 };
                          }
                          let markerEnd = selectedEdge.markerEnd;
                          if (markerEnd && typeof markerEnd === 'object') {
                            markerEnd = { ...markerEnd, color: vividStroke, width: 20, height: 20 };
                          }
                          updateEdge(selectedEdge.id, { style, markerStart, markerEnd });
                        }}
                        className="py-2 px-2.5 bg-indigo-700 hover:bg-indigo-800 text-white font-black rounded-lg text-xs shadow-sm transition-all flex items-center justify-center gap-1"
                        title="이 연결선을 8px 극대비 굵은 선으로 변경"
                      >
                        💪 완전 굵게 (8px)
                      </button>
                    </div>
                    <button
                      onClick={() => {
                        if (window.confirm('캔버스 위의 모든 연결선을 6px 선명한 찐한 선으로 일괄 변경하시겠습니까?')) {
                          takeSnapshot();
                          const nextEdges = edges.map(e => {
                            const isCp = e.style?.stroke === '#dc2626' || e.style?.stroke === '#b91c1c' || e.animated;
                            const strokeColor = isCp ? '#b91c1c' : '#1d4ed8';
                            const style = { ...e.style, stroke: strokeColor, strokeWidth: 6, strokeDasharray: undefined };
                            let markerStart = e.markerStart;
                            if (markerStart && typeof markerStart === 'object') {
                              markerStart = { ...markerStart, color: strokeColor, width: 18, height: 18 };
                            }
                            let markerEnd = e.markerEnd;
                            if (markerEnd && typeof markerEnd === 'object') {
                              markerEnd = { ...markerEnd, color: strokeColor, width: 18, height: 18 };
                            }
                            return { ...e, style, markerStart, markerEnd };
                          });
                          setNodesAndEdges(nodes, nextEdges);
                        }
                      }}
                      className="w-full py-1.5 px-2 bg-amber-600 hover:bg-amber-700 text-white font-extrabold rounded-lg text-[11px] shadow-xs transition-all text-center"
                    >
                      ⚡ 모든 연결선 찐하게 일괄 적용
                    </button>
                  </div>

                  <div className="flex flex-col">
                    <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">연결선 설명 (레이블)</label>
                    <input
                      type="text"
                      value={selectedEdge.label as string || ''}
                      onFocus={takeSnapshot}
                      onChange={e => updateEdge(selectedEdge.id, { label: e.target.value })}
                      className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2.5 text-xs text-gray-800 focus:bg-white"
                      placeholder="예: 승인 완료 후 진행"
                    />
                  </div>

                  <div className="flex flex-col">
                    <label className="font-semibold text-gray-500 text-[10px] uppercase mb-2">화살표 방향</label>
                    <div className="grid grid-cols-2 gap-2">
                      {[
                        { key: 'target', label: '➡️ 대상 방향 (우향)', desc: '시작 → 끝 단방향' },
                        { key: 'source', label: '⬅️ 시작 방향 (좌향)', desc: '끝 → 시작 단방향' },
                        { key: 'both', label: '↔️ 양방향', desc: '양쪽 모두 화살표' },
                        { key: 'none', label: '➖ 화살표 없음', desc: '직선으로만 표시' },
                      ].map(opt => {
                        const hasStart = !!selectedEdge.markerStart;
                        const hasEnd = !!selectedEdge.markerEnd;
                        let active = false;
                        if (opt.key === 'both') active = hasStart && hasEnd;
                        else if (opt.key === 'target') active = !hasStart && hasEnd;
                        else if (opt.key === 'source') active = hasStart && !hasEnd;
                        else if (opt.key === 'none') active = !hasStart && !hasEnd;

                        return (
                          <button
                            key={opt.key}
                            onClick={() => {
                              takeSnapshot();
                              const color = selectedEdge.style?.stroke || '#1d4ed8';
                              let markerStart: any = undefined;
                              let markerEnd: any = undefined;

                              if (opt.key === 'both' || opt.key === 'source') {
                                markerStart = {
                                  type: MarkerType.ArrowClosed,
                                  width: 18,
                                  height: 18,
                                  orient: 'auto-start-reverse',
                                  color,
                                };
                              }
                              if (opt.key === 'both' || opt.key === 'target') {
                                markerEnd = {
                                  type: MarkerType.ArrowClosed,
                                  width: 18,
                                  height: 18,
                                  color,
                                };
                              }

                              updateEdge(selectedEdge.id, { markerStart, markerEnd });
                            }}
                            className={`p-2.5 rounded-lg border text-left transition-all flex flex-col justify-center ${
                              active
                                ? 'border-blue-500 bg-blue-50 text-blue-700 shadow-sm font-bold'
                                : 'border-gray-200 bg-white hover:bg-gray-50 text-gray-700'
                            }`}
                          >
                            <span className="text-[11px]">{opt.label}</span>
                            <span className="text-[9px] text-gray-400 mt-0.5">{opt.desc}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div className="flex flex-col">
                    <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1.5 flex items-center justify-between">
                      <span>연결선 테마 색상 (선명한 고대비 색상)</span>
                      <span className="font-mono text-[9px] font-bold text-slate-700">{selectedEdge.style?.stroke || '#1d4ed8'}</span>
                    </label>
                    <div className="flex items-center gap-1.5 flex-wrap">
                      {[
                        '#0f172a', '#b91c1c', '#1d4ed8', '#047857', '#d97706', '#7c2d12', '#6b21a8', '#be123c', '#475569', '#dc2626', '#2563eb'
                      ].map(col => {
                        const isSelected = (selectedEdge.style?.stroke || '#1d4ed8') === col;
                        return (
                          <button
                            key={col}
                            onClick={() => {
                              takeSnapshot();
                              const style = { ...selectedEdge.style, stroke: col };
                              let markerStart = selectedEdge.markerStart;
                              if (markerStart && typeof markerStart === 'object') {
                                markerStart = { ...markerStart, color: col };
                              }
                              let markerEnd = selectedEdge.markerEnd;
                              if (markerEnd && typeof markerEnd === 'object') {
                                markerEnd = { ...markerEnd, color: col };
                              }
                              updateEdge(selectedEdge.id, { style, markerStart, markerEnd });
                            }}
                            className="w-6 h-6 rounded-full border border-gray-200 relative transition-transform hover:scale-110 shadow-sm flex items-center justify-center"
                            style={{ backgroundColor: col }}
                          >
                            {isSelected && <Check size={10} className="text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.5)]" />}
                          </button>
                        );
                      })}
                      <input
                        type="color"
                        value={selectedEdge.style?.stroke || '#1d4ed8'}
                        onFocus={takeSnapshot}
                        onChange={e => {
                          const col = e.target.value;
                          const style = { ...selectedEdge.style, stroke: col };
                          let markerStart = selectedEdge.markerStart;
                          if (markerStart && typeof markerStart === 'object') {
                            markerStart = { ...markerStart, color: col };
                          }
                          let markerEnd = selectedEdge.markerEnd;
                          if (markerEnd && typeof markerEnd === 'object') {
                            markerEnd = { ...markerEnd, color: col };
                          }
                          updateEdge(selectedEdge.id, { style, markerStart, markerEnd });
                        }}
                        className="w-6 h-6 rounded-full cursor-pointer border border-gray-200 p-0 overflow-hidden"
                        title="사용자 지정 색상"
                      />
                    </div>
                  </div>

                  <div className="flex flex-col">
                    <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1.5 flex items-center justify-between">
                      <span>연결선 굵기</span>
                      <span className="font-mono text-[9px] text-gray-400">{selectedEdge.style?.strokeWidth || 4}px</span>
                    </label>
                    <div className="grid grid-cols-6 gap-1 p-1 bg-gray-100 rounded-lg">
                      {([2, 3.5, 4.5, 6, 8, 10] as const).map(w => {
                        const active = (selectedEdge.style?.strokeWidth || 4) === w;
                        return (
                          <button
                            key={w}
                            onClick={() => {
                              takeSnapshot();
                              const style = { ...selectedEdge.style, strokeWidth: w };
                              updateEdge(selectedEdge.id, { style });
                            }}
                            className={`py-1.5 text-[9px] font-bold rounded-md transition-all text-center ${
                              active
                                ? 'bg-blue-600 text-white shadow-sm font-black'
                                : 'text-gray-600 hover:bg-gray-200'
                            }`}
                          >
                            {w}px
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div className="flex flex-col">
                    <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1.5">선 종류</label>
                    <div className="grid grid-cols-3 gap-1 p-1 bg-gray-100 rounded-lg">
                      {[
                        { key: 'solid', label: '실선' },
                        { key: 'dashed', label: '점선' },
                        { key: 'dotted', label: '미세 점선' },
                      ].map(opt => {
                        const styleVal = selectedEdge.style?.strokeDasharray;
                        let active = false;
                        if (opt.key === 'solid') active = !styleVal;
                        else if (opt.key === 'dashed') active = styleVal === '5,5';
                        else if (opt.key === 'dotted') active = styleVal === '2,3';

                        return (
                          <button
                            key={opt.key}
                            onClick={() => {
                              takeSnapshot();
                              let strokeDasharray: string | undefined = undefined;
                              if (opt.key === 'dashed') strokeDasharray = '5,5';
                              if (opt.key === 'dotted') strokeDasharray = '2,3';

                              const style = { ...selectedEdge.style, strokeDasharray };
                              updateEdge(selectedEdge.id, { style });
                            }}
                            className={`py-1.5 text-[10px] font-bold rounded-md transition-all text-center ${
                              active
                                ? 'bg-blue-500 text-white shadow-sm font-bold'
                                : 'text-gray-600 hover:bg-gray-200'
                            }`}
                          >
                            {opt.label}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Sidebar Footer */}
                <div className="p-4 border-t border-gray-100 bg-gray-50/50 flex">
                  <button
                    onClick={() => {
                      if (window.confirm('선택한 연결선을 삭제하시겠습니까?')) {
                        deleteEdge(selectedEdge.id);
                      }
                    }}
                    className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border border-red-200 hover:border-red-300 text-red-600 bg-red-50/30 hover:bg-red-50/60 font-semibold rounded-lg text-xs transition-colors"
                  >
                    <Trash2 size={13} />
                    연결선 삭제
                  </button>
                </div>
              </div>
            ) : null
          )}
        </aside>
      </div>

      {/* Enterprise Process Map Modals */}
      <ProjectManagerModal
        isOpen={showProjectManager}
        onClose={() => setShowProjectManager(false)}
        onOpenWizard={() => setShowWizard(true)}
      />

      <MapBuilderWizardModal
        isOpen={showWizard}
        onClose={() => setShowWizard(false)}
      />

      {/* 📖 원본 매뉴얼 HTML 열기 / 미리보기 팝업 모달 */}
      {manualModalUrl && (
        <div className="fixed inset-0 z-[9999] bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
          <div className="bg-slate-900 border-2 border-indigo-500 rounded-2xl w-full max-w-3xl shadow-2xl overflow-hidden flex flex-col text-slate-100 max-h-[85vh]">
            {/* Modal Header */}
            <div className="px-5 py-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2 min-w-0">
                <FileText size={20} className="text-indigo-400 flex-shrink-0" />
                <h3 className="font-black text-sm text-white truncate">
                  📖 {manualModalTitle || '원본 매뉴얼 HTML 열람'}
                </h3>
              </div>
              <button
                onClick={() => setManualModalUrl(null)}
                className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-5 flex-1 overflow-y-auto space-y-4 text-xs">
              <div className="bg-indigo-950/60 border border-indigo-800/80 rounded-xl p-4 space-y-2">
                <span className="font-extrabold text-indigo-300 block text-xs">📂 연결된 매뉴얼 HTML 원본 경로 / URL</span>
                <div className="flex items-center gap-2 bg-slate-950 border border-slate-800 rounded-lg p-2.5 font-mono text-[11px] text-indigo-200 break-all select-all">
                  <span className="flex-1">{manualModalUrl}</span>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(manualModalUrl);
                      alert('매뉴얼 HTML 경로가 클립보드에 복사되었습니다!\n파일 탐색기나 주소창에 붙여넣기(Ctrl+V)하여 열람하실 수 있습니다.');
                    }}
                    className="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded text-[11px] whitespace-nowrap flex items-center gap-1 flex-shrink-0 transition-colors"
                  >
                    <Copy size={12} />
                    <span>경로 복사</span>
                  </button>
                </div>
              </div>

              {/* 브라우저 미리보기 iframe (srcDoc으로 보안 차단 없이 100% 선명하게 렌더링) */}
              <div className="w-full h-[450px] bg-slate-900 rounded-xl border border-slate-700 overflow-hidden shadow-inner relative">
                <iframe
                  srcDoc={getManualHtmlForActivity(
                    selectedNode ? parseInt(selectedNode.id.replace('node-act-', '')) || 30 : 30,
                    selectedNode?.data?.label ? selectedNode.data.label.replace(/\[#\d+\]\s*/, '') : '강화노반 인계',
                    activeDetailTab
                  )}
                  className="w-full h-full border-none"
                  title="Manual HTML Preview"
                />
              </div>

              <div className="flex items-center justify-between text-[11px] text-slate-400 leading-relaxed bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span>💡 탐색기에서 원본 HTML 파일을 직접 실행하시려면 <b>[경로 복사]</b> 후 Windows 파일 탐색기 주소창(Ctrl+V)에 붙여넣으세요.</span>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="px-5 py-3.5 bg-slate-950 border-t border-slate-800 flex items-center justify-end gap-2">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(manualModalUrl);
                  alert('로컬 파일 경로가 복사되었습니다:\n' + manualModalUrl + '\n\nWindows 파일 탐색기(Win+E) 주소창에 붙여넣어 실행하실 수 있습니다.');
                }}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-black rounded-xl text-xs flex items-center gap-1.5 transition-colors shadow-md"
              >
                <Copy size={14} />
                <span>로컬 파일 경로 복사</span>
              </button>
              <button
                onClick={() => setManualModalUrl(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-xl text-xs transition-colors"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ❓ 사용 가이드 & 도움말 모달 */}
      <HelpModal isOpen={showHelp} onClose={() => setShowHelp(false)} />

      {/* 🖨️ A3 분할 출력 & 포스터 인쇄 마법사 모달 */}
      <A3PrintSplitModal
        isOpen={showA3SplitModal}
        onClose={() => setShowA3SplitModal(false)}
        mapTitle={disciplineMaps.find(m => m.id === activeDisciplineId)?.mapTitle || '동탄트램_프로세스맵'}
        captureFullCanvas={captureFullMapCanvas}
      />
    </div>
  );
}

export default App;
