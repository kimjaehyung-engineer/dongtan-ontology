import React, { useState, useRef, useEffect, useCallback } from 'react';
import FlowMap from './components/FlowMap';
import useStore from './store/useStore';
import { v4 as uuidv4 } from 'uuid';
import dayjs from 'dayjs';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import * as XLSX from 'xlsx';
import { MarkerType } from 'reactflow';
import { Download, Plus, Calendar, FileText, Type, Image, FileSpreadsheet, GripHorizontal, GripVertical, X, Copy, Check, ExternalLink, Trash2, Undo2, Redo2 } from 'lucide-react';
import './App.css';

// D-day 잔여일 기준 상태 자동 판정
function calcStatus(daysRemaining: number): 'normal' | 'warning' | 'danger' {
  if (daysRemaining <= 7) return 'danger';
  if (daysRemaining <= 21) return 'warning';
  return 'normal';
}

function App() {
  const { addNode, deleteNode, nodes, edges, updateNodeData, updateEdge, deleteEdge, setNodesAndEdges, undo, redo, takeSnapshot, past, future, isSelectMode, setSelectMode } = useStore();
  const [startDate, setStartDate] = useState('2025-12-01');
  const [showSettings, setShowSettings] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);
  const flowRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const excelInputRef = useRef<HTMLInputElement>(null);

  const selectedNode = nodes.find(n => n.selected);
  const selectedEdge = edges.find(e => e.selected);
  const selectedCount = nodes.filter(n => n.selected).length;

  // 선택이 완전히 해제되면 자동으로 사이드바도 닫음
  useEffect(() => {
    if (!selectedNode && !selectedEdge) {
      setShowSidebar(false);
    }
  }, [selectedNode, selectedEdge]);

  const isSidebarOpen = showSidebar && ((!!selectedNode && ['action', 'milestone', 'text', 'image'].includes(selectedNode.type || '')) || !!selectedEdge);

  // Ctrl+Z (Undo) 및 Ctrl+Y (Redo) 전역 단축키 핸들러
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
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [undo, redo]);

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

  // 엑셀 파싱 및 프로세스 맵 자동 생성 함수
  const handleExcelUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const data = evt.target?.result;
        const workbook = XLSX.read(data, { type: 'array' });
        
        // 1. 'Body' 시트 우선 사용, 없으면 첫 시트
        const sheetName = workbook.SheetNames.includes('Body') ? 'Body' : workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        
        // 2. 2D 배열로 변환
        const rows = XLSX.utils.sheet_to_json<any[]>(sheet, { header: 1 });
        if (rows.length === 0) {
          alert('엑셀에 데이터가 없습니다.');
          return;
        }

        // 3. 헤더 매칭용 스코어 측정
        let headerIndex = 0;
        let maxScore = 0;
        const keywords = ['번호', 'id', '순번', 'no', '업무', '태스크', 'task', 'process', '주관', '부서', '담당', '팀', '시기', '기한', '산출', '결과', '리스크', '협조', '협업', '공동'];
        
        for (let i = 0; i < Math.min(20, rows.length); i++) {
          const row = rows[i];
          if (!row || !Array.isArray(row)) continue;
          let score = 0;
          row.forEach(cell => {
            const val = String(cell || '').toLowerCase();
            keywords.forEach(kw => {
              if (val.includes(kw)) score++;
            });
          });
          if (score > maxScore) {
            maxScore = score;
            headerIndex = i;
          }
        }

        const headers = rows[headerIndex] as any[];
        const dataRows = rows.slice(headerIndex + 1);

        // 4. 컬럼 인덱스 자동 감지
        let idCol = -1;
        let labelCol = -1;
        let deptCol = -1;
        let startCol = -1;
        let endCol = -1;
        let outputCol = -1;
        let riskCol = -1;
        let coopCol = -1;

        headers.forEach((header, index) => {
          const h = String(header || '').trim();
          if (/^(번호|id|순번|no)$/i.test(h)) idCol = index;
          else if (/^(프로세스명|업무명|태스크명|task|process|내용|활동명|프로세스)$/i.test(h)) labelCol = index;
          else if (/^(주관부서|주관|부서|담당|팀|role|owner|주관 부서|주관부서명)$/i.test(h)) deptCol = index;
          else if (/^(착수시기|시작|일정|시기|start|착수)$/i.test(h)) startCol = index;
          else if (/^(완료시기|기한|완료|종료|end|due|완료 시기)$/i.test(h)) endCol = index;
          else if (/^(산출물|산출문서|결과|deliverable|산출물)$/i.test(h)) outputCol = index;
          else if (/^(리스크|대책|risk|특기사항)$/i.test(h)) riskCol = index;
          else if (/^(협조부서|협조|협업|공동|cooperation|coop|협업부서)$/i.test(h)) coopCol = index;
        });

        // 매핑 실패 시 폴백
        if (idCol === -1) idCol = 0;
        if (labelCol === -1) labelCol = headers.length > 1 ? 1 : 0;
        if (deptCol === -1) {
          deptCol = headers.findIndex(h => /부서|담당|팀|역할|주관/i.test(String(h || '')));
          if (deptCol === -1) deptCol = headers.length > 6 ? 6 : (headers.length > 2 ? 2 : 0);
        }
        if (startCol === -1) startCol = headers.findIndex(h => /시기|착수|시작|일정/i.test(String(h || '')));
        if (endCol === -1) endCol = headers.findIndex(h => /기한|완료|종료/i.test(String(h || '')));
        if (outputCol === -1) outputCol = headers.findIndex(h => /산출|결과|산출물/i.test(String(h || '')));
        if (riskCol === -1) riskCol = headers.findIndex(h => /리스크|대책|위험/i.test(String(h || '')));

        // 5. 로우 파싱
        const parsedRows: any[] = [];
        dataRows.forEach((r, idx) => {
          if (!r || !r[labelCol]) return;
          
          const department = String(r[deptCol] || '미지정부서').trim();
          const label = String(r[labelCol] || '').trim();
          const id = String(r[idCol] || `p-${idx}`).trim();
          const startDate = startCol >= 0 && r[startCol] ? String(r[startCol]).trim() : '';
          const endDate = endCol >= 0 && r[endCol] ? String(r[endCol]).trim() : '';
          const output = outputCol >= 0 && r[outputCol] ? String(r[outputCol]).trim() : '';
          const risk = riskCol >= 0 && r[riskCol] ? String(r[riskCol]).trim() : '';
          const cooperation = coopCol >= 0 && r[coopCol] ? String(r[coopCol]).trim() : '';
 
          parsedRows.push({ id, label, department, startDate, endDate, output, risk, cooperation });
        });

        if (parsedRows.length === 0) {
          alert('유효한 프로세스 행 데이터를 찾지 못했습니다.');
          return;
        }

        // 6. 스윔레인 생성
        const depts = Array.from(new Set(parsedRows.map(r => r.department)));
        const newNodes: any[] = [];
        const newEdges: any[] = [];
        
        const swimlaneHeight = 320;
        const startY = 350; // Shift dynamic lanes down to 350px
        const swimlaneWidth = Math.max(2500, 500 + parsedRows.length * 280);

        // A. 마일스톤 스윔레인 및 구분선
        newNodes.push({
          id: 'swimlane-마일스톤',
          type: 'swimlane',
          position: { x: 0, y: 0 },
          data: { label: '마일스톤' },
          style: { width: swimlaneWidth, height: 150, zIndex: -1 },
          draggable: false,
          selectable: false,
        });
        newNodes.push({
          id: 'rdiv-milestone',
          type: 'rowDivider',
          position: { x: 0, y: 150 },
          data: {},
          draggable: true,
          selectable: false,
          style: { zIndex: 10 }
        });

        // B. 체크리스트 스윔레인 및 구분선
        newNodes.push({
          id: 'swimlane-체크리스트',
          type: 'swimlane',
          position: { x: 0, y: 150 },
          data: { label: '체크리스트' },
          style: { width: swimlaneWidth, height: 200, zIndex: -1 },
          draggable: false,
          selectable: false,
        });
        newNodes.push({
          id: 'rdiv-checklist',
          type: 'rowDivider',
          position: { x: 0, y: 350 },
          data: {},
          draggable: true,
          selectable: false,
          style: { zIndex: 10 }
        });

        // C. 동적 주관부서 스윔레인
        depts.forEach((dept, idx) => {
          const y = startY + idx * swimlaneHeight;
          newNodes.push({
            id: `swimlane-${dept}`,
            type: 'swimlane',
            position: { x: 0, y },
            data: { label: dept },
            style: { width: swimlaneWidth, height: swimlaneHeight, zIndex: -1 },
            draggable: false,
            selectable: false,
          });

          if (idx < depts.length - 1) {
            newNodes.push({
              id: `rdiv-${idx}`,
              type: 'rowDivider',
              position: { x: 0, y: y + swimlaneHeight },
              data: {},
              draggable: true,
              selectable: false,
              style: { zIndex: 10 }
            });
          }
        });

        // 7. 마일스톤 날짜 분석 및 상단 배치
        const getSortValue = (item: any) => {
          const text = item.endDate || item.startDate || '';
          if (text.includes('상시')) return 999;
          const dMatch = text.match(/D-(\d+)/i);
          if (dMatch) return -parseInt(dMatch[1]);
          const plusMatch = text.match(/\+(\d+)/);
          if (plusMatch) return parseInt(plusMatch[1]);
          const minusMatch = text.match(/-(\d+)/);
          if (minusMatch) return -parseInt(minusMatch[1]);
          return 999;
        };

        // 데이터 정렬
        parsedRows.sort((a, b) => getSortValue(a) - getSortValue(b));

        const milestoneLabels = Array.from(new Set(
          parsedRows
            .map(r => r.endDate || r.startDate)
            .filter(t => t && (t.includes('D-') || t.includes('+') || t.includes('-')))
        )) as string[];

        milestoneLabels.sort((a, b) => {
          const getVal = (t: string) => {
            const dMatch = t.match(/D-(\d+)/i);
            if (dMatch) return -parseInt(dMatch[1]);
            const plusMatch = t.match(/\+(\d+)/);
            if (plusMatch) return parseInt(plusMatch[1]);
            return 999;
          };
          return getVal(a) - getVal(b);
        });

        milestoneLabels.forEach((mLabel, idx) => {
          const x = 300 + idx * 450;
          newNodes.push({
            id: `m-${idx}`,
            type: 'milestone',
            position: { x, y: 50 },
            data: { label: mLabel },
          });

          // Add a default vertical line under this milestone spanning all swimlanes from y = 0
          newNodes.push({
            id: `vline-m-${idx}`,
            type: 'verticalLine',
            position: { x: x + 100, y: 0 },
            data: { height: 350 + depts.length * swimlaneHeight },
            draggable: true,
            style: { zIndex: 10 }
          });

          if (idx > 0) {
            newEdges.push({
              id: `e-m-${idx-1}-${idx}`,
              source: `m-${idx-1}`,
              target: `m-${idx}`,
              type: 'smoothstep',
              markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 }
            });
          }
        });

        // 8. 액션 카드 노드 배치
        const deptNodeCounts: Record<string, number> = {};
        const createdNodeIds: string[] = [];

        parsedRows.forEach((row, idx) => {
          const dept = row.department;
          const deptIdx = depts.indexOf(dept);
          const yBase = startY + deptIdx * swimlaneHeight;
          
          if (!deptNodeCounts[dept]) deptNodeCounts[dept] = 0;
          deptNodeCounts[dept]++;

          let x = 200 + idx * 300;
          
          const dateText = row.endDate || row.startDate;
          if (dateText) {
            const mIdx = milestoneLabels.indexOf(dateText);
            if (mIdx >= 0) {
              x = 300 + mIdx * 450;
            }
          }

          // 중복 X에 대비한 Y 오프셋
          const dupCount = newNodes.filter(n => 
            n.type === 'action' && 
            Math.abs(n.position.x - x) < 50 && 
            Math.abs(n.position.y - (yBase + 100)) < 150
          ).length;
          
          const y = yBase + 70 + (dupCount * 110);

          newNodes.push({
            id: row.id,
            type: 'action',
            position: { x, y },
            data: {
              label: row.label,
              department: row.department,
              cooperation: row.cooperation || '',
              purpose: `시기: ${row.startDate || '-'} ~ ${row.endDate || '-'}`,
              method: `입력/조건: ${row.startDate || '-'}\n완료기준: ${row.endDate || '-'}\n\n[리스크 및 대책]\n${row.risk || '-'}`,
              result: row.output || '-',
              color: '#d1d5db',
              status: 'normal',
            }
          });
          createdNodeIds.push(row.id);
        });

        // 9. 순차적 흐름선(화살표) 자동 연결
        for (let i = 0; i < createdNodeIds.length - 1; i++) {
          newEdges.push({
            id: `e-${createdNodeIds[i]}-${createdNodeIds[i+1]}`,
            source: createdNodeIds[i],
            target: createdNodeIds[i+1],
            type: 'smoothstep',
            markerEnd: { type: MarkerType.ArrowClosed, width: 30, height: 30 }
          });
        }

        setNodesAndEdges(newNodes, newEdges);
        alert(`엑셀 프로세스 맵 생성 완료!\n- 부서 스윔레인: ${depts.length}개\n- 프로세스 카드: ${parsedRows.length}개\n- 마일스톤: ${milestoneLabels.length}개`);
      } catch (err: any) {
        console.error(err);
        alert(`엑셀 파싱 에러: ${err.message}`);
      }
    };
    reader.readAsArrayBuffer(file);
    e.target.value = '';
  };

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

  // 파일 선택으로 이미지 추가
  const handleImageFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => addImageNode(ev.target?.result as string);
    reader.readAsDataURL(file);
    e.target.value = '';
  };

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

  const handleAddNode = () => {
    addNode({
      id: uuidv4(),
      type: 'action',
      position: { x: 400 + Math.random() * 80, y: 300 + Math.random() * 80 },
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
    addNode({
      id: uuidv4(),
      type: 'text',
      position: { x: 500 + Math.random() * 80, y: 350 + Math.random() * 80 },
      data: { label: '' },
      style: { width: 200, height: 60 },
    });
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
              className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-gray-50 border border-gray-200 rounded text-gray-600 hover:bg-gray-100 text-xs"
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
              className={`whitespace-nowrap flex items-center gap-1 px-2 py-1 rounded transition-all text-xs font-bold ${
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
              className={`whitespace-nowrap flex items-center gap-1 px-2 py-1 rounded transition-all text-xs font-bold ${
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
            <button onClick={handleAlignHorizontal} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-gray-50 text-gray-700 font-semibold rounded border border-gray-200 hover:bg-gray-100 transition-colors text-xs" title="선택된 노드들을 가로 일직선으로 맞춥니다">
              <GripHorizontal size={12} /> 가로 정렬
            </button>
            <button onClick={handleAlignVertical} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-gray-50 text-gray-700 font-semibold rounded border border-gray-200 hover:bg-gray-100 transition-colors text-xs" title="선택된 노드들을 세로 일직선으로 맞춥니다">
              <GripVertical size={12} /> 세로 정렬
            </button>
          </div>

          <button onClick={handleAddNode} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-600 font-semibold rounded border border-blue-200 hover:bg-blue-100 transition-colors text-xs">
            <Plus size={12} /> 카드 추가
          </button>

          <button onClick={handleAddTextNode} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-amber-50 text-amber-700 font-semibold rounded border border-amber-200 hover:bg-amber-100 transition-colors text-xs">
            <Type size={12} /> 텍스트 추가
          </button>

          <div className="w-px h-4 bg-gray-200 mx-0.5 flex-shrink-0" />

          <button onClick={handleExportPNG} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-emerald-50 text-emerald-700 font-semibold rounded border border-emerald-200 hover:bg-emerald-100 transition-colors text-xs">
            <Download size={12} /> PNG
          </button>

          <button onClick={handleExportPDF} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-rose-50 text-rose-700 font-semibold rounded border border-rose-200 hover:bg-rose-100 transition-colors text-xs">
            <FileText size={12} /> PDF (A3)
          </button>

          <button onClick={handleSave} className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-slate-800 text-white font-semibold rounded hover:bg-slate-700 transition-colors text-xs">
            <Download size={12} /> JSON 저장
          </button>

          <button 
            onClick={() => {
              if (window.confirm('모든 사용자 편집 데이터를 지우고 기본 샘플 데이터로 초기화하시겠습니까?')) {
                localStorage.removeItem('process-map-storage-v2');
                window.location.reload();
              }
            }} 
            className="whitespace-nowrap flex items-center gap-1 px-2 py-1 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 rounded transition-colors text-xs"
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
                <div className="p-4 border-t border-gray-100 bg-gray-50/50 flex gap-2">
                  {selectedNode.type === 'action' && (
                    <button
                      onClick={handleDuplicateNode}
                      className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border border-blue-200 hover:border-blue-300 text-blue-600 bg-blue-50/30 hover:bg-blue-50/60 font-semibold rounded-lg text-xs transition-colors"
                    >
                      <Copy size={13} />
                      카드 복제
                    </button>
                  )}
                  <button
                    onClick={handleDeleteNode}
                    className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 border border-red-200 hover:border-red-300 text-red-600 bg-red-50/30 hover:bg-red-50/60 font-semibold rounded-lg text-xs transition-colors"
                  >
                    <Trash2 size={13} />
                    {selectedNode.type === 'action' ? '카드 삭제' : '삭제하기'}
                  </button>
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
