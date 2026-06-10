import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';

export default function ChecklistHeaderNode({ data, selected }: NodeProps<NodeData>) {
  const label = data.label || '본공사수행';
  const ts = data.textStyle || {};
  
  const bgColor = ts.bgColor || '#1e293b'; // 기본 다크네이비
  const textColor = ts.color || '#ffffff'; // 기본 흰색
  const borderStyle = ts.borderStyle || 'solid'; // 기본 실선
  const borderWidth = ts.borderWidth !== undefined ? ts.borderWidth : 1; // 기본 1px
  const fontSize = ts.fontSize || 12; // 기본 12px

  return (
    <>
      <div className="relative w-full h-full min-w-[120px] min-h-[36px] flex items-center justify-center">
        <div
          className={`px-4 py-2 rounded-md font-bold shadow-md 
                     flex items-center justify-center w-full h-full z-10 relative 
                     transition-all duration-150
                     ${selected ? 'ring-2 ring-blue-500 ring-offset-2' : ''}`}
          style={{
            backgroundColor: bgColor,
            color: textColor,
            borderStyle: borderStyle !== 'none' ? borderStyle : 'none',
            borderWidth: borderStyle !== 'none' ? `${borderWidth}px` : '0px',
            borderColor: textColor === '#ffffff' ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.15)',
            fontSize: `${fontSize}px`,
          }}
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
