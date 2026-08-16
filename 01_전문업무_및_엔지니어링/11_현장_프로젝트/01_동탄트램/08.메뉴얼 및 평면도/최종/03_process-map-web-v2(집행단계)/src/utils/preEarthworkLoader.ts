import type { Node, Edge } from 'reactflow';
import type { NodeData } from '../store/useStore';
import preEarthworkData from '../data/preEarthworkActivities.json';
import { buildNodesAndEdgesFromRows, type ParsedWbsRow } from './excelWbsParser';

export function generatePreEarthworkNodesAndEdges(): { nodes: Node<NodeData>[]; edges: Edge[] } {
  const rows: ParsedWbsRow[] = (preEarthworkData || []).map((item: any) => ({
    wbsCode: item.code || '',
    department: item.department || '',
    phase: item.schedule || '',
    taskTitle: item.title || '',
    purpose: item.purpose || '',
    method: item.method || '',
    result: item.output || '',
  }));

  return buildNodesAndEdgesFromRows(rows, '동탄도시철도(트램) 건설공사 · 사전토공사 프로세스 맵');
}
