import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';

export default function RowDividerNode({ data }: NodeProps<NodeData>) {
  return (
    <div
      className="group cursor-row-resize flex items-center"
      style={{ width: 4000, height: 16, marginLeft: -200 }}
    >
      {/* 행 구분선: 항상 보이는 회색 점선 */}
      <div className="w-full h-[2px] border-t-2 border-dashed border-slate-300 group-hover:border-blue-500 group-hover:border-solid transition-colors pointer-events-none" />
    </div>
  );
}
