import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';

export default function SwimlaneNode({ data, selected }: NodeProps<NodeData>) {
  return (
    <div
      className={`w-full h-full bg-gray-50 ${selected ? 'bg-blue-50/30' : ''}`}
    >
      {/* Left label */}
      <div className="absolute left-0 top-0 bottom-0 w-16 bg-slate-200 border-r border-slate-300 flex items-center justify-center">
        <span className="transform -rotate-90 text-lg font-bold text-slate-600 tracking-widest whitespace-nowrap">
          {data.label}
        </span>
      </div>
    </div>
  );
}
