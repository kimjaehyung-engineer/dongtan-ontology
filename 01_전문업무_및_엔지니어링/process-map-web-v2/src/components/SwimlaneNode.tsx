import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';

export default function SwimlaneNode({ id, data, selected }: NodeProps<NodeData>) {
  return (
    <>
      <NodeResizer 
        color="#3b82f6" 
        isVisible={selected} 
        minWidth={1000} 
        minHeight={100} 
      />
      <div
        className={`w-full h-full bg-gray-50/50 ${selected ? 'bg-blue-50/20 ring-2 ring-blue-500' : ''} pointer-events-none`}
      >
        {/* Left label bar: 클릭 시 선택이 가능하도록 pointer-events-auto 설정 */}
        <div className="absolute left-0 top-0 bottom-0 w-16 bg-slate-200 border-r border-slate-300 flex items-center justify-center pointer-events-auto cursor-pointer hover:bg-slate-300/80 transition-colors">
          <span className="transform -rotate-90 text-lg font-bold text-slate-600 tracking-widest whitespace-nowrap select-none">
            {data.label}
          </span>
        </div>
      </div>
    </>
  );
}
