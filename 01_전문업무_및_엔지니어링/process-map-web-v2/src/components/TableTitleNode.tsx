import React from 'react';
import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';

const TableTitleNode = ({ data, selected }: NodeProps<NodeData>) => {
  return (
    <div
      className={`table-title-node px-3 py-1 bg-transparent border-l-4 border-blue-600 flex items-center transition-all ${
        selected ? 'ring-2 ring-blue-500 ring-offset-2' : ''
      }`}
      style={{
        width: '100%',
        height: '100%',
      }}
    >
      <h2 className="text-lg font-extrabold text-slate-800 tracking-tight leading-none select-none">
        {data.label || '1. 표 제목'}
      </h2>

      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: 'transparent', border: 'none', bottom: 0 }}
      />
    </div>
  );
};

export default React.memo(TableTitleNode);
