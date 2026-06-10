import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';

export default function ChecklistHeaderNode({ data, selected }: NodeProps<NodeData>) {
  const label = data.label || '본공사수행';

  return (
    <>
      <div className="relative w-full h-full min-w-[120px] min-h-[36px] flex items-center justify-center">
        <div
          className={`bg-slate-800 text-white px-4 py-2 rounded-md font-bold text-xs shadow-md 
                     flex items-center justify-center w-full h-full z-10 relative 
                     transition-all duration-150 border border-slate-700
                     ${selected ? 'ring-2 ring-blue-500 ring-offset-2' : ''}`}
        >
          <span className="text-center break-all whitespace-pre-wrap">{label}</span>
          
          {/* 핸들들 */}
          <Handle type="target" position={Position.Left} className="!bg-slate-400" />
          <Handle type="source" position={Position.Right} className="!bg-slate-400" />
          <Handle type="source" position={Position.Bottom} id="down" className="!bg-slate-400" />
          <Handle type="target" position={Position.Top} id="up" className="!bg-slate-400" />
        </div>
      </div>
      <NodeResizer 
        color="#3b82f6" 
        isVisible={selected} 
        minWidth={80} 
        minHeight={30} 
      />
    </>
  );
}
