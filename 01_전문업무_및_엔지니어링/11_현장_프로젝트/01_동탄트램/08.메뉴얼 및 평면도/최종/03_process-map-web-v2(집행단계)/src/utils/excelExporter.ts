import * as XLSX from 'xlsx';
import type { Node, Edge } from 'reactflow';
import type { NodeData } from '../store/useStore';
import dayjs from 'dayjs';

/**
 * 캔버스 상에서 사용자가 수정한 노드 및 최신 연결선 관계(선행/후행)를 역계산하여 
 * 원본 엑셀 (.xlsx) 서식(폰트, 셀 색상, 테두리 등)을 100% 보존하면서
 * '선행L4'와 '후행L4' 셀 값만 정밀 업데이트하여 다운로드하는 서식 보존 엑셀 익스포터
 */
export function exportWbsToExcel(
  nodes: Node<NodeData>[], 
  edges: Edge[], 
  mapTitle = '동탄트램_프로세스맵',
  rawWorkbookBuffer: ArrayBuffer | null = null
) {
  // 1. ActionNode 작업 카드들만 추출
  const actionNodes = nodes.filter(n => n.type === 'action' || !n.type);

  // 2. 각 노드 ID 및 WBS 코드 기준 노드 맵 구축
  const nodeMap = new Map<string, Node<NodeData>>();
  const wbsCodeToNodeMap = new Map<string, Node<NodeData>>();

  actionNodes.forEach(n => {
    nodeMap.set(n.id, n);
    if (n.data?.wbsCode) {
      wbsCodeToNodeMap.set(String(n.data.wbsCode).trim(), n);
    }
  });

  // 3. 엣지 연결선을 분석하여 각 노드별 선행(predecessor) 및 후행(successor) WBS 코드/ID 역계산
  const predMap = new Map<string, Set<string>>();
  const succMap = new Map<string, Set<string>>();

  edges.forEach(edge => {
    const srcNode = nodeMap.get(edge.source);
    const tgtNode = nodeMap.get(edge.target);

    if (srcNode && tgtNode) {
      const srcCode = srcNode.data?.wbsCode || srcNode.data?.label || srcNode.id;
      const tgtCode = tgtNode.data?.wbsCode || tgtNode.data?.label || tgtNode.id;

      // target 노드의 선행 목록에 srcNode의 코드 추가
      if (!predMap.has(tgtNode.id)) predMap.set(tgtNode.id, new Set());
      predMap.get(tgtNode.id)!.add(srcCode);

      // source 노드의 후행 목록에 tgtNode의 코드 추가
      if (!succMap.has(srcNode.id)) succMap.set(srcNode.id, new Set());
      succMap.get(srcNode.id)!.add(tgtCode);
    }
  });

  const dateStr = dayjs().format('YYYYMMDD_HHmm');
  const cleanTitle = mapTitle.replace(/[^a-zA-Z0-9가-힣_-]/g, '_');
  const fileName = `${cleanTitle}_서식보존_관계업데이트_${dateStr}.xlsx`;

  // 4. 원본 엑셀 바이너리가 존재하는 경우: 원본 서식 100% 보존 업데이트
  if (rawWorkbookBuffer) {
    try {
      // cellStyles, cellFormula, cellDates 등 모든 서식 정보 읽기
      const workbook = XLSX.read(rawWorkbookBuffer, {
        type: 'array',
        cellStyles: true,
        cellFormula: true,
        cellDates: true,
        cellNF: true,
        sheetStubs: true,
      });

      // 모든 워크시트를 확인하며 WBS 액티비티가 포함된 시트 서식 업데이트
      workbook.SheetNames.forEach(sheetName => {
        const worksheet = workbook.Sheets[sheetName];
        if (!worksheet || !worksheet['!ref']) return;

        const range = XLSX.utils.decode_range(worksheet['!ref']);
        let colWbsCode = -1;
        let colActivityLabel = -1;
        let colPred = -1;
        let colSucc = -1;

        // 헤더 행 탐색 (상단 15행 이내에서 컬럼 위치 자동 감지)
        for (let R = range.s.r; R <= Math.min(range.e.r, 15); ++R) {
          for (let C = range.s.c; C <= range.e.c; ++C) {
            const cellAddress = XLSX.utils.encode_cell({ r: R, c: C });
            const cell = worksheet[cellAddress];
            if (!cell || !cell.v) continue;

            const valStr = String(cell.v).trim();
            if (/WBS/i.test(valStr) || /L4/i.test(valStr) || valStr.includes('코드')) colWbsCode = C;
            if (valStr.includes('액티비티') || valStr.includes('세공종') || valStr.includes('작업명')) colActivityLabel = C;
            if (valStr.includes('선행')) colPred = C;
            if (valStr.includes('후행')) colSucc = C;
          }
          if ((colWbsCode !== -1 || colActivityLabel !== -1) && (colPred !== -1 || colSucc !== -1)) break;
        }

        // 헤더 열 위치를 발견한 경우 각 행데이터에 맞게 핀포인트 업데이트
        if (colPred !== -1 || colSucc !== -1) {
          for (let R = range.s.r; R <= range.e.r; ++R) {
            const wbsCell = colWbsCode !== -1 ? worksheet[XLSX.utils.encode_cell({ r: R, c: colWbsCode })] : null;
            const labelCell = colActivityLabel !== -1 ? worksheet[XLSX.utils.encode_cell({ r: R, c: colActivityLabel })] : null;

            const wbsVal = wbsCell?.v ? String(wbsCell.v).trim() : '';
            const labelVal = labelCell?.v ? String(labelCell.v).trim() : '';

            // 매칭되는 노드 찾기
            let targetNode = wbsCodeToNodeMap.get(wbsVal);
            if (!targetNode && labelVal) {
              targetNode = actionNodes.find(n => n.data?.label && String(n.data.label).trim() === labelVal);
            }

            if (targetNode) {
              const predsStr = Array.from(predMap.get(targetNode.id) || []).join(', ');
              const succsStr = Array.from(succMap.get(targetNode.id) || []).join(', ');

              // 선행L4 셀 덮어쓰기
              if (colPred !== -1) {
                const predCellAddr = XLSX.utils.encode_cell({ r: R, c: colPred });
                if (!worksheet[predCellAddr]) worksheet[predCellAddr] = { t: 's', v: '' };
                worksheet[predCellAddr].v = predsStr;
                worksheet[predCellAddr].w = predsStr;
              }

              // 후행L4 셀 덮어쓰기
              if (colSucc !== -1) {
                const succCellAddr = XLSX.utils.encode_cell({ r: R, c: colSucc });
                if (!worksheet[succCellAddr]) worksheet[succCellAddr] = { t: 's', v: '' };
                worksheet[succCellAddr].v = succsStr;
                worksheet[succCellAddr].w = succsStr;
              }
            }
          }
        }
      });

      // 서식 완전 보존 옵션으로 파일 내보내기 실행
      XLSX.writeFile(workbook, fileName, { cellStyles: true });
      return;
    } catch (e) {
      console.warn('원본 서식 보존 업데이트 실패, 새 시트로 대체 내보내기 진행합니다.', e);
    }
  }

  // 5. 기본 신규 시트 생성 내보내기 (fallback)
  const rows = actionNodes.map((n, idx) => {
    const d = n.data || {};
    const preds = Array.from(predMap.get(n.id) || []).join(', ');
    const succs = Array.from(succMap.get(n.id) || []).join(', ');

    return {
      'No': idx + 1,
      'WBS L4 코드': d.wbsCode || `WBS-${idx + 1}`,
      '세공종(액티비티명)': d.label || '',
      '담당부서': d.department || '공무',
      '협조부서': d.cooperation || '',
      '목적': d.purpose || '',
      '수행방법': d.method || '',
      '산출물': d.result || '',
      '선행L4 (연결)': preds,
      '후행L4 (연결)': succs,
      'CP 주경로 여부': d.isCritical ? 'O' : 'X',
      '기한/마일스톤': d.date || '',
    };
  });

  const worksheet = XLSX.utils.json_to_sheet(rows);
  worksheet['!cols'] = [
    { wch: 6 },
    { wch: 16 },
    { wch: 32 },
    { wch: 14 },
    { wch: 14 },
    { wch: 40 },
    { wch: 50 },
    { wch: 35 },
    { wch: 25 },
    { wch: 25 },
    { wch: 14 },
    { wch: 16 },
  ];

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, '프로세스맵_관계업데이트');
  XLSX.writeFile(workbook, fileName);
}
