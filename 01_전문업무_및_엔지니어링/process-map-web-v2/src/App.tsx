import { useState, useRef, useEffect, useCallback } from 'react';
import FlowMap from './components/FlowMap';
import useStore, { lastCanvasMousePos } from './store/useStore';
import { v4 as uuidv4 } from 'uuid';
import dayjs from 'dayjs';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

import { MarkerType } from 'reactflow';
import { Download, Plus, Calendar, FileText, Type, GripHorizontal, GripVertical, X, Copy, Check, ExternalLink, Trash2, Undo2, Redo2, Paintbrush, Clipboard } from 'lucide-react';
import './App.css';

// D-day 잔여일 기준 상태 자동 판정
// function calcStatus(daysRemaining: number): 'normal' | 'warning' | 'danger' {
//   if (daysRemaining <= 7) return 'danger';
//   if (daysRemaining <= 21) return 'warning';
//   return 'normal';
// }

function App() {
  const { addNode, deleteNode, nodes, edges, updateNodeData, updateEdge, deleteEdge, setNodesAndEdges, undo, redo, takeSnapshot, past, future, isSelectMode, setSelectMode, copiedStyle, setCopiedStyle } = useStore();
  const [startDate, setStartDate] = useState('2025-12-01');
  const [showSettings, setShowSettings] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);
  const flowRef = useRef<HTMLDivElement>(null);
  // const fileInputRef = useRef<HTMLInputElement>(null);
  // const excelInputRef = useRef<HTMLInputElement>(null);

  const selectedNode = nodes.find(n => n.selected);
  const selectedEdge = edges.find(e => e.selected);
  const selectedCount = nodes.filter(n => n.selected).length;

  // 선택이 완전히 해제되면 자동으로 사이드바도 닫음
  useEffect(() => {
    if (!selectedNode && !selectedEdge) {
      setShowSidebar(false);
    }
  }, [selectedNode, selectedEdge]);

  const isSidebarOpen = showSidebar && ((!!selectedNode && ['action', 'milestone', 'text', 'image', 'checklistItem', 'checklistHeader'].includes(selectedNode.type || '')) || !!selectedEdge);

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
  }, [undo, redo, handleAddTextNode, handleAddChecklistItemNode, handleAddChecklistHeaderNode, handleCopyStyle, handlePasteStyle]);

  const handleDuplicateNode = () => {
    if (!selectedNode) return;
    takeSnapshot(); // 복제 전 스냅샷 저장
    const newId = uuidv4();
    const dupNode = {
      ...selectedNode,
      id: newId,
      selected: false,
      position: {
        x: selectedNode.position.x + 60,
        y: selectedNode.position.y + 60,
      },
      data: {
        ...selectedNode.data,
      },
    };
    addNode(dupNode);
  };

  const handleDeleteNode = () => {
    if (!selectedNode) return;
    if (window.confirm('선택한 카드를 삭제하시겠습니까?')) {
      deleteNode(selectedNode.id);
    }
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

  // D-day 자동 업데이트: 마일스톤 레이블에서 D-숫자 추출 후 계산
  const applyDday = () => {
    const base = dayjs(startDate);
    nodes.forEach(node => {
      if (node.type === 'action' && node.data.daysRemaining !== undefined) {
        const status = node.data.daysRemaining <= 7 ? 'danger' : node.data.daysRemaining <= 21 ? 'warning' : 'normal';
        updateNodeData(node.id, { status });
      }
      // 마일스톤 노드: 레이블에서 D-숫자 파싱
      if (node.type === 'milestone' && node.data.label) {
        const match = node.data.label.match(/D-(\d+)/);
        if (match) {
          const d = parseInt(match[1]);
          const targetDate = base.subtract(d, 'day');
          const remaining = targetDate.diff(dayjs(), 'day');
          updateNodeData(node.id, { daysRemaining: remaining });
        }
      }
    });
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


  const handleExportPNG = async () => {
    const el = document.querySelector('.react-flow') as HTMLElement;
    if (!el) return;
    const canvas = await html2canvas(el, { scale: 1.5, useCORS: true, backgroundColor: '#f1f5f9' });
    const link = document.createElement('a');
    link.download = `process-map-${dayjs().format('YYYYMMDD-HHmm')}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  const handleExportPDF = async () => {
    const el = document.querySelector('.react-flow') as HTMLElement;
    if (!el) return;

    // 고해상도 캡처
    const canvas = await html2canvas(el, { scale: 2, useCORS: true, backgroundColor: '#f8fafc' });
    const imgData = canvas.toDataURL('image/png');

    const imgW = canvas.width;
    const imgH = canvas.height;

    // 가로형(Landscape) A3 사이즈로 설정하여 넓은 공정표 표현
    const pdf = new jsPDF({
      orientation: imgW > imgH ? 'landscape' : 'portrait',
      unit: 'mm',
      format: 'a3',
    });

    const pageW = pdf.internal.pageSize.getWidth();
    const pageH = pdf.internal.pageSize.getHeight();
    const margin = 10;
    const contentW = pageW - margin * 2;
    const contentH = pageH - margin * 2 - 12; // 헤더 공간

    const scale = Math.min(contentW / (imgW * 0.264583), contentH / (imgH * 0.264583));
    const drawW = imgW * 0.264583 * scale;
    const drawH = imgH * 0.264583 * scale;

    // 헤더 텍스트
    pdf.setFont('helvetica', 'bold');
    pdf.setFontSize(14);
    pdf.setTextColor(30, 41, 59);
    pdf.text('프로세스 맵 – 동탄 트램', margin, margin + 6);
    pdf.setFont('helvetica', 'normal');
    pdf.setFontSize(9);
    pdf.setTextColor(100, 116, 139);
    pdf.text(`출력일시: ${dayjs().format('YYYY-MM-DD HH:mm')}`, pageW - margin, margin + 6, { align: 'right' });

    // 구분선
    pdf.setDrawColor(200, 200, 200);
    pdf.line(margin, margin + 9, pageW - margin, margin + 9);

    // 이미지 삽입
    pdf.addImage(imgData, 'PNG', margin + (contentW - drawW) / 2, margin + 12, drawW, drawH);

    pdf.save(`process-map-${dayjs().format('YYYYMMDD-HHmm')}.pdf`);
  };

  const handleSave = () => {
    const state = { nodes: useStore.getState().nodes, edges: useStore.getState().edges };
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
    const link = document.createElement('a');
    link.download = `process-map-${dayjs().format('YYYYMMDD-HHmm')}.json`;
    link.href = URL.createObjectURL(blob);
    link.click();
  };

  const today = dayjs().format('YYYY-MM-DD');

  return (
    <div className="w-screen h-screen flex flex-col font-sans">
      <header className="h-11 bg-white shadow-sm flex items-center px-4 justify-between z-10 border-b border-gray-200 flex-shrink-0">
        <h1 className="text-sm font-bold text-gray-800 flex items-center gap-1 whitespace-nowrap">
          <svg className="w-4 h-4 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span className="whitespace-nowrap">프로세스 맵 – 동탄 트램</span>
          <span className="text-xs font-normal text-gray-400 ml-1 whitespace-nowrap">{today}</span>
        </h1>

        <div className="flex items-center gap-1">
          {/* D-day 기준일 설정 */}
          <div className="relative">
            <button
              onClick={() => setShowSettings(v => !v)}
              className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-gray-50 border border-gray-200 rounded text-gray-600 hover:bg-gray-100 text-[10px]"
            >
              <Calendar size={12} />
              착공일 설정
            </button>
            {showSettings && (
              <div className="absolute right-0 top-full mt-1 bg-white shadow-lg rounded-lg border border-gray-200 p-3 z-50 w-64">
                <p className="text-xs font-bold text-gray-600 mb-2">📅 착공 기준일 (D-0)</p>
                <input
                  type="date"
                  value={startDate}
                  onChange={e => setStartDate(e.target.value)}
                  className="w-full border border-gray-300 rounded px-2 py-1 text-xs mb-2"
                />
                <button
                  onClick={() => { applyDday(); setShowSettings(false); }}
                  className="w-full bg-blue-600 text-white rounded py-1 text-xs font-bold hover:bg-blue-700"
                >
                  D-day 자동 계산 적용
                </button>
                <p className="text-[9px] text-gray-400 mt-2 leading-relaxed">
                  ⚠️ 마일스톤(D-210 등)의 날짜가 자동 계산되어 카드에 표시됩니다.<br/>
                  카드의 잔여일이 7일↓ 빨강, 21일↓ 노랑으로 자동 전환됩니다.
                </p>
              </div>
            )}
          </div>

          {/* 범례 */}
          <div className="whitespace-nowrap flex items-center gap-2 px-2 py-1 bg-gray-50 border border-gray-200 rounded text-[10px]">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-400 inline-block"></span>정상</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-400 inline-block"></span>주의</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-400 inline-block"></span>위험</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-gray-400 inline-block"></span>완료</span>
          </div>

          {/* 모드 선택 (이동/선택) */}
          <div className="flex items-center gap-0.5 border-r border-gray-200 pr-1.5 mr-1.5 bg-slate-50 p-0.5 rounded-md border border-slate-200 flex-shrink-0">
            <button
              onClick={() => setSelectMode(false)}
              className={`whitespace-nowrap flex items-center gap-1 px-2 py-1 rounded transition-all text-[10px] font-bold ${
                !isSelectMode
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
              title="화면 이동 모드 (드래그하여 캔버스를 이동합니다)"
            >
              🖐️ 이동
            </button>
            <button
              onClick={() => setSelectMode(true)}
              className={`whitespace-nowrap flex items-center gap-1 px-2 py-1 rounded transition-all text-[10px] font-bold ${
                isSelectMode
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
              title="다중 선택 모드 (드래그하여 영역 내 카드를 선택합니다)"
            >
              🖱️ 선택
            </button>
          </div>

          {/* 실행 취소 / 다시 실행 */}
          <div className="flex items-center gap-0.5 border-r border-gray-200 pr-1.5 mr-1.5 flex-shrink-0">
            <button
              onClick={undo}
              disabled={past.length === 0}
              className={`flex items-center justify-center p-1.5 rounded border transition-colors ${
                past.length > 0
                  ? 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50 cursor-pointer shadow-sm'
                  : 'bg-gray-50 border-gray-100 text-gray-300 cursor-not-allowed'
              }`}
              title="실행 취소 (Ctrl+Z)"
            >
              <Undo2 size={11} />
            </button>
            <button
              onClick={redo}
              disabled={future.length === 0}
              className={`flex items-center justify-center p-1.5 rounded border transition-colors ${
                future.length > 0
                  ? 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50 cursor-pointer shadow-sm'
                  : 'bg-gray-50 border-gray-100 text-gray-300 cursor-not-allowed'
              }`}
              title="다시 실행 (Ctrl+Y)"
            >
              <Redo2 size={11} />
            </button>
          </div>

          {/* 서식 복사 / 붙여넣기 */}
          <div className="flex items-center gap-0.5 border-r border-gray-200 pr-1.5 mr-1.5 flex-shrink-0">
            <button
              onClick={handleCopyStyle}
              disabled={selectedCount === 0}
              className={`flex items-center justify-center p-1.5 rounded border transition-all ${
                selectedCount > 0
                  ? 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50 cursor-pointer shadow-sm'
                  : 'bg-gray-50 border-gray-100 text-gray-300 cursor-not-allowed'
              }`}
              title="서식 복사 (Ctrl+Shift+C)"
            >
              <Paintbrush size={11} />
            </button>
            <button
              onClick={handlePasteStyle}
              disabled={!copiedStyle || selectedCount === 0}
              className={`flex items-center justify-center p-1.5 rounded border transition-all ${
                copiedStyle && selectedCount > 0
                  ? 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50 cursor-pointer shadow-sm'
                  : 'bg-gray-50 border-gray-100 text-gray-300 cursor-not-allowed'
              }`}
              title="서식 붙여넣기 (Ctrl+Shift+V)"
            >
              <Clipboard size={11} />
            </button>
          </div>

          {/* 다중 선택 액션 */}
          {selectedCount > 0 && (
            <div className="whitespace-nowrap flex items-center gap-1 border-r border-gray-200 pr-1.5 mr-1.5 bg-blue-50/50 px-1.5 py-0.5 rounded border border-blue-100 flex-shrink-0">
              <span className="text-[10px] text-blue-700 font-bold px-1">{selectedCount}개 선택됨</span>
              <button
                onClick={handleDuplicateSelected}
                className="whitespace-nowrap flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-blue-50 text-blue-600 font-semibold rounded border border-blue-200 transition-colors text-[10px]"
                title="선택된 카드를 모두 복제합니다"
              >
                <Copy size={10} /> 복제
              </button>
              <button
                onClick={handleDeleteSelected}
                className="whitespace-nowrap flex items-center gap-1 px-2 py-0.5 bg-white hover:bg-red-50 text-red-600 font-semibold rounded border border-red-200 transition-colors text-[10px]"
                title="선택된 카드를 모두 삭제합니다"
              >
                <Trash2 size={10} /> 삭제
              </button>
            </div>
          )}

          <div className="flex items-center gap-1 border-r border-gray-200 pr-1 mr-1 flex-shrink-0">
            <button onClick={handleAlignHorizontal} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-gray-50 text-gray-700 font-semibold rounded border border-gray-200 hover:bg-gray-100 transition-colors text-[10px]" title="선택된 노드들을 가로 일직선으로 맞춥니다">
              <GripHorizontal size={12} /> 가로 정렬
            </button>
            <button onClick={handleAlignVertical} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-gray-50 text-gray-700 font-semibold rounded border border-gray-200 hover:bg-gray-100 transition-colors text-[10px]" title="선택된 노드들을 세로 일직선으로 맞춥니다">
              <GripVertical size={12} /> 세로 정렬
            </button>
          </div>

          <button onClick={handleAddNode} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-600 font-semibold rounded border border-blue-200 hover:bg-blue-100 transition-colors text-[10px]">
            <Plus size={12} /> 카드 추가
          </button>

          <button onClick={handleAddTextNode} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-amber-50 text-amber-700 font-semibold rounded border border-amber-200 hover:bg-amber-100 transition-colors text-[10px]">
            <Type size={12} /> 텍스트 추가
          </button>


          <button onClick={handleAddChecklistHeaderNode} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-slate-800 text-slate-100 font-semibold rounded border border-slate-700 hover:bg-slate-700 transition-colors text-[10px]" title="본공사 수행 스타일의 체크 글상자를 마우스 위치에 추가합니다">
            <Type size={12} /> 체크 글박스
          </button>

          <div className="w-px h-4 bg-gray-200 mx-0.5 flex-shrink-0" />

          <button onClick={handleExportPNG} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-emerald-50 text-emerald-700 font-semibold rounded border border-emerald-200 hover:bg-emerald-100 transition-colors text-[10px]">
            <Download size={12} /> PNG
          </button>

          <button onClick={handleExportPDF} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-rose-50 text-rose-700 font-semibold rounded border border-rose-200 hover:bg-rose-100 transition-colors text-[10px]">
            <FileText size={12} /> PDF (A3)
          </button>

          <button onClick={handleSave} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-slate-800 text-white font-semibold rounded hover:bg-slate-700 transition-colors text-[10px]">
            <Download size={12} /> JSON 저장
          </button>

          <button 
            onClick={() => {
              if (window.confirm('모든 사용자 편집 데이터를 지우고 기본 샘플 데이터로 초기화하시겠습니까?')) {
                localStorage.removeItem('process-map-storage-v2');
                window.location.reload();
              }
            }} 
            className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 rounded transition-colors text-[10px]"
            title="모든 저장된 데이터를 삭제하고 초기 샘플로 복원합니다"
          >
            기본값 복원
          </button>
        </div>
      </header>

      <div className="flex-1 w-full flex overflow-hidden">
        <main ref={flowRef} className="flex-1 h-full overflow-hidden relative">
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
                      {/* Title / Label */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">업무 카드 제목</label>
                        <textarea
                          value={selectedNode.data.label || ''}
                          onFocus={takeSnapshot}
                          onChange={e => updateNodeData(selectedNode.id, { label: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs font-semibold text-gray-800 focus:bg-white resize-none h-16 leading-relaxed"
                          placeholder="제목을 입력하세요..."
                        />
                      </div>

                      {/* Status (Segmented Control) */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1.5">진행 상태</label>
                        <div className="grid grid-cols-4 gap-1 p-1 bg-gray-100 rounded-lg">
                          {(['normal', 'warning', 'danger', 'done'] as const).map(st => {
                            const active = (selectedNode.data.status || 'normal') === st;
                            const labelMap = { normal: '정상', warning: '주의', danger: '위험', done: '완료' };
                            const colorMap = {
                              normal: active ? 'bg-green-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200',
                              warning: active ? 'bg-amber-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200',
                              danger: active ? 'bg-red-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200',
                              done: active ? 'bg-gray-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200',
                            };
                            return (
                              <button
                                key={st}
                                onClick={() => {
                                  takeSnapshot();
                                  updateNodeData(selectedNode.id, { status: st });
                                }}
                                className={`py-1 text-[10px] font-bold rounded-md transition-all text-center ${colorMap[st]}`}
                              >
                                {labelMap[st]}
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      {/* Header Theme Color */}
                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1.5 flex items-center justify-between">
                          <span>카드 상단 테마 색상</span>
                          <span className="font-mono text-[9px] text-gray-400">{selectedNode.data.color || '#d1d5db'}</span>
                        </label>
                        <div className="flex items-center gap-1.5 flex-wrap">
                          {[
                            '#fca5a5', // Red-300
                            '#fdba74', // Orange-300
                            '#fde047', // Yellow-300
                            '#86efac', // Green-300
                            '#93c5fd', // Blue-300
                            '#c4b5fd', // Purple-300
                            '#f472b6', // Pink-400
                            '#cbd5e1', // Slate-300
                          ].map(col => {
                            const isSelected = selectedNode.data.color === col;
                            return (
                              <button
                                key={col}
                                onClick={() => {
                                  takeSnapshot();
                                  updateNodeData(selectedNode.id, { color: col });
                                }}
                                className="w-6 h-6 rounded-full border border-gray-200 relative transition-transform hover:scale-110 shadow-sm flex items-center justify-center"
                                style={{ backgroundColor: col }}
                              >
                                {isSelected && <Check size={10} className="text-gray-700" />}
                              </button>
                            );
                          })}
                          <input
                            type="color"
                            value={selectedNode.data.color || '#d1d5db'}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { color: e.target.value })}
                            className="w-6 h-6 rounded-full cursor-pointer border border-gray-200 p-0 overflow-hidden"
                            title="사용자 지정 색상"
                          />
                        </div>
                      </div>

                      {/* Sub-group 1: D-day & Departments */}
                      <div className="grid grid-cols-2 gap-3 border-t border-gray-100 pt-3">
                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">D-day 잔여일 (D-X)</label>
                          <input
                            type="number"
                            value={selectedNode.data.daysRemaining ?? ''}
                            onFocus={takeSnapshot}
                            onChange={e => {
                              const val = e.target.value === '' ? undefined : parseInt(e.target.value);
                              const patch: any = { daysRemaining: val };
                              if (val !== undefined) {
                                patch.status = val <= 7 ? 'danger' : val <= 21 ? 'warning' : 'normal';
                              }
                              updateNodeData(selectedNode.id, patch);
                            }}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                            placeholder="예: 210"
                          />
                        </div>
                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">주관 부서</label>
                          <input
                            type="text"
                            value={selectedNode.data.department || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { department: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                            placeholder="예: 공무"
                          />
                        </div>
                      </div>

                      <div className="flex flex-col">
                        <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">협조 부서 (쉼표로 구분)</label>
                        <input
                          type="text"
                          value={selectedNode.data.cooperation || ''}
                          onFocus={takeSnapshot}
                          onChange={e => updateNodeData(selectedNode.id, { cooperation: e.target.value })}
                          className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                          placeholder="예: 공사, 설계, 인허가"
                        />
                      </div>

                      {/* Sub-group 2: Details */}
                      <div className="border-t border-gray-100 pt-3 space-y-3">
                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">🎯 목적 (Why) 및 일정</label>
                          <input
                            type="text"
                            value={selectedNode.data.purpose || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { purpose: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                            placeholder="예: 시기: D-210 ~ D-180"
                          />
                        </div>

                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">📝 방법 (How) 및 입력 조건</label>
                          <textarea
                            value={selectedNode.data.method || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { method: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white resize-y h-24 leading-relaxed custom-scrollbar"
                            placeholder="업무 진행 방법 및 고려사항, 리스크 대책 등을 기술하세요..."
                          />
                        </div>

                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">🎁 최종 결과물 (What)</label>
                          <input
                            type="text"
                            value={selectedNode.data.result || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { result: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                            placeholder="예: 사업승인서, 협의서 완료"
                          />
                        </div>

                        <div className="flex flex-col">
                          <div className="flex items-center justify-between mb-1">
                            <label className="font-semibold text-gray-500 text-[10px] uppercase">첨부 파일 / 외부 링크</label>
                            {selectedNode.data.fileUrl && (
                              <a
                                href={selectedNode.data.fileUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:text-blue-700 flex items-center gap-0.5 text-[9px] font-bold"
                              >
                                열기 <ExternalLink size={9} />
                              </a>
                            )}
                          </div>
                          <input
                            type="text"
                            value={selectedNode.data.fileUrl || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { fileUrl: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white"
                            placeholder="https://example.com/document"
                          />
                        </div>

                        <div className="flex flex-col">
                          <label className="font-semibold text-gray-500 text-[10px] uppercase mb-1">기타 메모</label>
                          <textarea
                            value={selectedNode.data.note || ''}
                            onFocus={takeSnapshot}
                            onChange={e => updateNodeData(selectedNode.id, { note: e.target.value })}
                            className="fancy-input bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs text-gray-800 focus:bg-white resize-y h-16 leading-relaxed custom-scrollbar"
                            placeholder="자유롭게 기재할 추가 정보..."
                          />
                        </div>
                      </div>
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
                </div>

                {/* Sidebar Footer */}
                <div className="p-4 border-t border-gray-100 bg-gray-50/50 flex flex-col gap-2">
                  <div className="flex gap-2">
                    <button
                      onClick={handleCopyStyle}
                      className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border border-gray-200 hover:border-gray-300 text-gray-700 bg-white font-semibold rounded-lg text-xs transition-colors"
                      title="이 노드의 스타일을 복사합니다. (Ctrl+Shift+C)"
                    >
                      <Paintbrush size={13} />
                      서식 복사
                    </button>
                    <button
                      onClick={handlePasteStyle}
                      disabled={!copiedStyle}
                      className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border font-semibold rounded-lg text-xs transition-colors ${
                        copiedStyle
                          ? 'border-indigo-200 hover:border-indigo-300 text-indigo-600 bg-indigo-50/30 hover:bg-indigo-50/60 cursor-pointer shadow-sm'
                          : 'border-gray-100 text-gray-300 bg-gray-50 cursor-not-allowed'
                      }`}
                      title="복사된 서식을 이 노드에 붙여넣습니다. (Ctrl+Shift+V)"
                    >
                      <Clipboard size={13} />
                      서식 붙여넣기
                    </button>
                  </div>
                  <div className="flex gap-2">
                    {(selectedNode.type === 'action' || selectedNode.type === 'checklistItem' || selectedNode.type === 'checklistHeader') && (
                      <button
                        onClick={handleDuplicateNode}
                        className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border border-blue-200 hover:border-blue-300 text-blue-600 bg-blue-50/30 hover:bg-blue-50/60 font-semibold rounded-lg text-xs transition-colors"
                      >
                        <Copy size={13} />
                        {selectedNode.type === 'action' ? '카드 복제' : selectedNode.type === 'checklistItem' ? '항목 복제' : '글박스 복제'}
                      </button>
                    )}
                    <button
                      onClick={handleDeleteNode}
                      className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border border-red-200 hover:border-red-300 text-red-600 bg-red-50/30 hover:bg-red-50/60 font-semibold rounded-lg text-xs transition-colors"
                    >
                      <Trash2 size={13} />
                      {selectedNode.type === 'action' ? '카드 삭제' : selectedNode.type === 'checklistItem' ? '항목 삭제' : selectedNode.type === 'checklistHeader' ? '글박스 삭제' : '삭제하기'}
                    </button>
                  </div>
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
                              const color = selectedEdge.style?.stroke || '#94a3b8';
                              let markerStart: any = undefined;
                              let markerEnd: any = undefined;

                              if (opt.key === 'both' || opt.key === 'source') {
                                markerStart = {
                                  type: MarkerType.ArrowClosed,
                                  width: 22,
                                  height: 22,
                                  orient: 'auto-start-reverse',
                                  color,
                                };
                              }
                              if (opt.key === 'both' || opt.key === 'target') {
                                markerEnd = {
                                  type: MarkerType.ArrowClosed,
                                  width: 22,
                                  height: 22,
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
                      <span>연결선 테마 색상</span>
                      <span className="font-mono text-[9px] text-gray-400">{selectedEdge.style?.stroke || '#94a3b8'}</span>
                    </label>
                    <div className="flex items-center gap-1.5 flex-wrap">
                      {[
                        '#94a3b8', '#64748b', '#ef4444', '#f97316', '#22c55e', '#3b82f6', '#8b5cf6', '#ec4899',
                      ].map(col => {
                        const isSelected = (selectedEdge.style?.stroke || '#94a3b8') === col;
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
                        value={selectedEdge.style?.stroke || '#94a3b8'}
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
                      <span className="font-mono text-[9px] text-gray-400">{selectedEdge.style?.strokeWidth || 2}px</span>
                    </label>
                    <div className="grid grid-cols-4 gap-1 p-1 bg-gray-100 rounded-lg">
                      {([1, 2, 3, 5] as const).map(w => {
                        const active = (selectedEdge.style?.strokeWidth || 2) === w;
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
                                ? 'bg-blue-500 text-white shadow-sm font-bold'
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
    </div>
  );
}

export default App;
