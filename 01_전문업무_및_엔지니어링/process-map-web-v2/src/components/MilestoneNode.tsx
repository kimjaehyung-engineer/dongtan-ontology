import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';

export default function MilestoneNode({ data, selected }: NodeProps<NodeData>) {
  const label = data.label || '';
  
  // data.date가 있으면 사용하고, 없으면 기존 label에서 파싱하여 폴백
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
      <div className="relative w-full h-full min-w-[150px] min-h-[40px] flex flex-col justify-end">
        {/* 날짜 배지: 박스 바로 위 좌측에 밀착 */}
        {datePart && (
          <div className="absolute -top-5 left-0 bg-indigo-600 text-white text-[9px] font-extrabold px-1.5 py-0.5 rounded shadow-sm z-20 select-none">
            {datePart}
          </div>
        )}
        <div className={`bg-slate-700 text-white px-4 py-2 rounded-md font-bold text-sm shadow-md flex items-center justify-center w-full h-full z-10 relative ${selected ? 'ring-2 ring-blue-500 ring-offset-2' : ''}`}>
          {titlePart || datePart}
          <Handle type="target" position={Position.Left} className="!bg-slate-400" />
          <Handle type="source" position={Position.Right} className="!bg-slate-400" />
          <Handle type="source" position={Position.Bottom} id="down" className="!bg-slate-400" />
        </div>
      </div>
      <NodeResizer color="#3b82f6" isVisible={selected} minWidth={100} minHeight={30} />
    </>
  );
}
