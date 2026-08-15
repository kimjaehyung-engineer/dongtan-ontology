import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';

export default function MilestoneNode({ data, selected }: NodeProps<NodeData>) {
  const label = data.label || '';
  
  let datePart = data.date || '';
  let titlePart = label;
  
  if (!datePart) {
    const match = label.match(/^(D-\d+|P\+\d+|D\+\d+|[+-]\d+|D-Day)\s*(.*)$/i);
    if (match) {
      datePart = match[1];
      titlePart = match[2] ? match[2].trim() : '';
    }
  }

  return (
    <>
      <div className="relative w-full h-full min-w-[560px] min-h-[56px]" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-end' }}>
        <div
          className={`px-8 py-3.5 rounded-md font-black text-xl sm:text-2xl shadow-xl w-full h-full z-10 relative transition-all tracking-wider text-white bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-indigo-900/60 whitespace-nowrap ${
            selected ? 'ring-2 ring-indigo-500 ring-offset-1' : ''
          }`}
          style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}
        >
          {titlePart || datePart}

          {/* Handles */}
          <Handle type="source" position={Position.Left} id="left-source" style={{ top: '35%' }} className="!bg-indigo-400" />
          <Handle type="target" position={Position.Left} id="left-target" style={{ top: '65%' }} className="!bg-indigo-400" />
          <Handle type="source" position={Position.Right} id="right-source" style={{ top: '35%' }} className="!bg-indigo-400" />
          <Handle type="target" position={Position.Right} id="right-target" style={{ top: '65%' }} className="!bg-indigo-400" />
          <Handle type="source" position={Position.Top} id="top-source" style={{ left: '35%' }} className="!bg-indigo-400" />
          <Handle type="target" position={Position.Top} id="top-target" style={{ left: '65%' }} className="!bg-indigo-400" />
          <Handle type="source" position={Position.Bottom} id="bottom-source" style={{ left: '35%' }} className="!bg-indigo-400" />
          <Handle type="target" position={Position.Bottom} id="bottom-target" style={{ left: '65%' }} className="!bg-indigo-400" />
        </div>
      </div>
      <NodeResizer color="#3b82f6" isVisible={selected} minWidth={150} minHeight={40} />
    </>
  );
}
