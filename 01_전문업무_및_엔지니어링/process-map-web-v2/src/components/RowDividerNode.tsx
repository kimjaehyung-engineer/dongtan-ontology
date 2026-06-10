import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';

export default function RowDividerNode({ data }: NodeProps<NodeData>) {
  return (
    <div
      className="group cursor-row-resize flex items-center"
      style={{ width: 4000, height: 16, marginLeft: -200 }}
    >
      {/* 기본: 투명 / 호버 시 파란색 실선으로 표시 */}
      <div className="w-full h-[2px] border-t-2 border-transparent group-hover:border-blue-400 group-hover:border-solid transition-colors pointer-events-none" />
    </div>
  );
}
