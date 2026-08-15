import React from 'react';
import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';

const TableTitleNode = ({ data, selected }: NodeProps<NodeData>) => {
  const isDarkMode = useStore(state => state.isDarkMode);

  // Label parsing for title and matrix subtitle
  const rawLabel = data.label || '동탄트램 사전토공사';
  
  let mainTitle = rawLabel;
  let subText = '';

  if (rawLabel.includes('(') && rawLabel.endsWith(')')) {
    const parts = rawLabel.split('(');
    mainTitle = parts[0].trim();
    subText = parts[1].replace(')', '').trim();
  }

  // Remove "2차원 프로세스 맵" and "🏗️" emoji if present
  mainTitle = mainTitle.replace(/2차원\s*프로세스\s*맵/g, '').replace(/🏗️/g, '').trim();

  // Suppress matrix subtitle if it contains timeline x department matrix text
  if (subText.includes('타임라인') || subText.includes('부서')) {
    subText = '';
  }

  return (
    <div
      className={`table-title-node px-4 py-2.5 rounded-2xl gap-4 transition-all ${
        isDarkMode
          ? `bg-slate-900/90 border-2 ${selected ? 'border-indigo-400 ring-4 ring-indigo-500/20 shadow-2xl' : 'border-slate-800 shadow-xl'}`
          : `bg-white border-2 ${selected ? 'border-indigo-600 ring-4 ring-indigo-500/15 shadow-2xl' : 'border-slate-200 shadow-lg'}`
      }`}
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flex: '1 1 0%', minWidth: 0 }}>
        {/* Left Accent Gradient Pillar */}
        <div className="w-2.5 h-10 bg-gradient-to-b from-indigo-600 via-blue-600 to-indigo-800 rounded-full flex-shrink-0 shadow-md" />

        <div className="flex flex-col flex-1 min-w-0">
          <div className="flex items-center gap-3 flex-wrap">
            <h1 className={`text-2xl font-black tracking-tight leading-tight select-none whitespace-nowrap ${
              isDarkMode ? 'text-white drop-shadow-md' : 'text-slate-900'
            }`}>
              {mainTitle}
            </h1>
          </div>

          {subText ? (
            <div className={`text-xs font-bold mt-0.5 tracking-wide whitespace-nowrap ${
              isDarkMode ? 'text-slate-400' : 'text-slate-500'
            }`}>
              📊 {subText}
            </div>
          ) : null}
        </div>
      </div>

      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: 'transparent', border: 'none', bottom: 0 }}
      />
    </div>
  );
};

export default React.memo(TableTitleNode);
