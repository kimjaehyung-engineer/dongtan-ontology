import * as XLSX from 'xlsx';
import type { DisciplineMapItem } from '../store/useStore';

export interface ExportExcelV8Options {
  disciplineMaps: DisciplineMapItem[];
  originalFileBuffer?: ArrayBuffer | null;
  filename?: string;
}

export function exportProcessMapToExcelV8(options: ExportExcelV8Options) {
  const { disciplineMaps, originalFileBuffer, filename } = options;

  let workbook: XLSX.WorkBook;

  if (originalFileBuffer) {
    try {
      workbook = XLSX.read(originalFileBuffer, { type: 'array', cellStyles: true });
    } catch (e) {
      workbook = XLSX.utils.book_new();
    }
  } else {
    workbook = XLSX.utils.book_new();
  }

  disciplineMaps.forEach((mapItem) => {
    const sheetName = mapItem.sheetName || mapItem.name.replace(/[^\w가-힣]/g, '').trim() || '공종시트';
    const nodes = mapItem.nodes || [];
    const edges = mapItem.edges || [];

    // 1. 노드 ID ➔ L4 코드 매핑 맵
    const nodeIdToWbsMap = new Map<string, string>();
    const actionNodes = nodes.filter(n => n.type === 'action');

    actionNodes.forEach((n, idx) => {
      const wbs = n.data?.wbsCode || `WBS-${idx + 1}`;
      nodeIdToWbsMap.set(n.id, wbs);
    });

    // 2. 각 노드별 선행/후행 L4 코드 자동 연산
    const predecessorMap = new Map<string, string[]>();
    const successorMap = new Map<string, string[]>();

    edges.forEach((edge) => {
      const sourceWbs = nodeIdToWbsMap.get(edge.source);
      const targetWbs = nodeIdToWbsMap.get(edge.target);

      if (sourceWbs && targetWbs && sourceWbs !== targetWbs) {
        // Target입장에서 Source는 선행(Predecessor)
        if (!predecessorMap.has(edge.target)) {
          predecessorMap.set(edge.target, []);
        }
        const pList = predecessorMap.get(edge.target)!;
        if (!pList.includes(sourceWbs)) pList.push(sourceWbs);

        // Source입장에서 Target은 후행(Successor)
        if (!successorMap.has(edge.source)) {
          successorMap.set(edge.source, []);
        }
        const sList = successorMap.get(edge.source)!;
        if (!sList.includes(targetWbs)) sList.push(targetWbs);
      }
    });

    // 3. 엑셀 워크시트에 기입
    let worksheet = workbook.Sheets[sheetName];

    if (!worksheet) {
      // 엑셀 시트가 없으면 2차원 배열 헤더 포함 신규 생성
      const headerRow = [
        'L2 코드', 'L3 코드', 'L3 대공종명', 'L4 코드', '선행', '후행', 
        '일정 (D-Day)', '작업단위 (Level 4 Task/Activity)', '주관', '목적', '방법', '산출물(결과)'
      ];
      const rowsData: any[][] = [headerRow];

      actionNodes.forEach((n, idx) => {
        const wbs = n.data?.wbsCode || `WBS-${idx + 1}`;
        const preds = predecessorMap.get(n.id)?.join(', ') || n.data?.predecessor || '';
        const succs = successorMap.get(n.id)?.join(', ') || n.data?.successor || '';

        rowsData.push([
          '9000',
          '9000-1',
          mapItem.name,
          wbs,
          preds,
          succs,
          n.data?.date || 'D-30',
          n.data?.label || '',
          n.data?.department || '',
          n.data?.purpose || '',
          n.data?.method || '',
          n.data?.result || '',
        ]);
      });

      worksheet = XLSX.utils.aoa_to_sheet(rowsData);
      XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
    } else {
      // 기존 엑셀 시트가 존재하는 경우: Matrix cell 업데이트
      const matrix: any[][] = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });

      actionNodes.forEach((n) => {
        const wbs = n.data?.wbsCode;
        if (!wbs) return;

        const preds = predecessorMap.get(n.id)?.join(', ') || n.data?.predecessor || '';
        const succs = successorMap.get(n.id)?.join(', ') || n.data?.successor || '';

        // 행을 찾아서 Col 5 (index 4: 선행), Col 6 (index 5: 후행) 업데이트
        for (let r = 1; r < matrix.length; r++) {
          const row = matrix[r];
          if (row && Array.isArray(row)) {
            const cellWbs = row[3] ? row[3].toString().trim() : '';
            const cellTitle = row[7] || row[4] || row[5] ? (row[7] || row[4] || row[5]).toString().trim() : '';

            if (cellWbs === wbs || (n.data?.label && cellTitle === n.data.label)) {
              row[4] = preds; // 선행 L4 코드
              row[5] = succs; // 후행 L4 코드
              break;
            }
          }
        }
      });

      const updatedSheet = XLSX.utils.aoa_to_sheet(matrix);
      workbook.Sheets[sheetName] = updatedSheet;
    }
  });

  // 4. v8 브라우저 파일 다운로드 실행
  const defaultFileName = filename ? filename.replace(/\.xl[sm]{1,2}$/i, '') + 'v8.xlsm' : '매뉴얼 BODY (집행단계)v8.xlsm';
  XLSX.writeFile(workbook, defaultFileName);
}
