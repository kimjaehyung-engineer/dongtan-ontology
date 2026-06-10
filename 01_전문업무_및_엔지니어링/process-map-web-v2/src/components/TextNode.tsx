import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';
import { Trash2, Bold, Italic, AlignLeft, AlignCenter, AlignRight } from 'lucide-react';

type TextStyle = {
  bold?: boolean;
  italic?: boolean;
  align?: 'left' | 'center' | 'right';
  fontSize?: number;
  color?: string;
  bgColor?: string; // transparent, white, yellow, blue, green, purple
  borderStyle?: 'dashed' | 'solid' | 'none';
};

export default function TextNode({ id, data, selected }: NodeProps<NodeData & { textStyle?: TextStyle }>) {
  const { updateNodeData, deleteNode } = useStore();

  const ts: TextStyle = (data as any).textStyle || {};
  const fontSize = ts.fontSize || 14;
  const textColor = ts.color || '#1e293b';
  const bgColor = ts.bgColor || 'white'; // default white background for visibility
  const borderStyle = ts.borderStyle || 'dashed';

  const updateStyle = (patch: Partial<TextStyle>) => {
    updateNodeData(id, { textStyle: { ...ts, ...patch } } as any);
  };

  // 배경색 클래스 맵
  const bgClasses: Record<string, string> = {
    transparent: 'bg-transparent',
    white: 'bg-white border-slate-200',
    yellow: 'bg-amber-50 border-amber-200',
    blue: 'bg-sky-50 border-sky-200',
    green: 'bg-emerald-50 border-emerald-200',
    purple: 'bg-violet-50 border-violet-200',
  };

  // 테두리 스타일 클래스
  const borderClass = borderStyle === 'none' 
    ? 'border-none' 
    : borderStyle === 'solid' 
      ? 'border border-solid' 
      : 'border border-dashed';

  return (
    <>
      <NodeResizer color="#94a3b8" isVisible={selected} minWidth={80} minHeight={40} />

      <div className={`w-full h-full flex flex-col rounded p-1 transition-all ${bgClasses[bgColor]} ${borderClass} ${selected ? 'ring-2 ring-blue-500 border-solid shadow-md' : 'shadow-sm'}`}>

        {/* 서식 툴바 - 선택 시만 표시 */}
        {selected && (
          <div className="absolute -top-12 left-0 flex items-center gap-1 bg-white border border-gray-200 rounded-md shadow-lg px-2 py-1.5 z-50 text-gray-600 max-w-[450px] flex-wrap">
            <button onClick={() => updateStyle({ bold: !ts.bold })}
              className={`p-1 rounded hover:bg-gray-100 ${ts.bold ? 'bg-blue-100 text-blue-600' : ''}`} title="굵게">
              <Bold size={13} />
            </button>
            <button onClick={() => updateStyle({ italic: !ts.italic })}
              className={`p-1 rounded hover:bg-gray-100 ${ts.italic ? 'bg-blue-100 text-blue-600' : ''}`} title="기울임">
              <Italic size={13} />
            </button>
            
            <div className="w-px h-4 bg-gray-200 mx-1" />
            
            <button onClick={() => updateStyle({ align: 'left' })}
              className={`p-1 rounded hover:bg-gray-100 ${ts.align === 'left' || !ts.align ? 'bg-blue-100 text-blue-600' : ''}`}><AlignLeft size={13} /></button>
            <button onClick={() => updateStyle({ align: 'center' })}
              className={`p-1 rounded hover:bg-gray-100 ${ts.align === 'center' ? 'bg-blue-100 text-blue-600' : ''}`}><AlignCenter size={13} /></button>
            <button onClick={() => updateStyle({ align: 'right' })}
              className={`p-1 rounded hover:bg-gray-100 ${ts.align === 'right' ? 'bg-blue-100 text-blue-600' : ''}`}><AlignRight size={13} /></button>
            
            <div className="w-px h-4 bg-gray-200 mx-1" />
            
            {/* 글자 크기 */}
            <select
              className="text-xs border border-gray-200 rounded px-1 py-0.5 outline-none"
              value={fontSize}
              onChange={e => updateStyle({ fontSize: Number(e.target.value) })}
            >
              {[10, 12, 14, 16, 18, 22, 28, 36].map(s => (
                <option key={s} value={s}>{s}px</option>
              ))}
            </select>
            
            {/* 글자 색 */}
            <input
              type="color"
              className="w-5 h-5 rounded cursor-pointer border border-gray-200 p-0"
              value={textColor}
              onChange={e => updateStyle({ color: e.target.value })}
              title="글자 색상"
            />
            
            <div className="w-px h-4 bg-gray-200 mx-1" />

            {/* 배경색 선택 */}
            <select
              className="text-xs border border-gray-200 rounded px-1 py-0.5 outline-none"
              value={bgColor}
              onChange={e => updateStyle({ bgColor: e.target.value })}
              title="배경색"
            >
              <option value="white">하양</option>
              <option value="transparent">투명</option>
              <option value="yellow">노랑(포스트잇)</option>
              <option value="blue">파랑</option>
              <option value="green">연두</option>
              <option value="purple">보라</option>
            </select>

            {/* 테두리 스타일 선택 */}
            <select
              className="text-xs border border-gray-200 rounded px-1 py-0.5 outline-none"
              value={borderStyle}
              onChange={e => updateStyle({ borderStyle: e.target.value as any })}
              title="테두리"
            >
              <option value="dashed">점선</option>
              <option value="solid">실선</option>
              <option value="none">없음</option>
            </select>
            
            <div className="w-px h-4 bg-gray-200 mx-1" />
            
            <button onClick={() => deleteNode(id)} className="p-1 rounded hover:bg-red-100 text-red-400" title="삭제">
              <Trash2 size={13} />
            </button>
          </div>
        )}

        {/* 텍스트 영역 */}
        <textarea
          className="nodrag w-full h-full bg-transparent outline-none resize-none font-medium"
          style={{
            fontSize: `${fontSize}px`,
            fontWeight: ts.bold ? 'bold' : 'normal',
            fontStyle: ts.italic ? 'italic' : 'normal',
            textAlign: ts.align || 'left',
            color: textColor,
            lineHeight: 1.5,
            padding: '4px 6px',
          }}
          value={data.label || ''}
          placeholder="텍스트 입력..."
          onChange={e => updateNodeData(id, { label: e.target.value })}
        />
      </div>
    </>
  );
}
