import { useRef } from 'react';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';
import { Trash2, ImageOff } from 'lucide-react';

export default function ImageNode({ id, data, selected }: NodeProps<NodeData & { imageDataUrl?: string; caption?: string }>) {
  const { updateNodeData, deleteNode } = useStore();
  const d = data as any;

  return (
    <>
      <NodeResizer color="#94a3b8" isVisible={selected} minWidth={80} minHeight={60} />

      <div className={`w-full h-full flex flex-col rounded-md overflow-hidden shadow-sm border ${selected ? 'border-blue-400 ring-2 ring-blue-300' : 'border-gray-200'} bg-white`}>

        {/* 툴바 */}
        {selected && (
          <div className="absolute -top-9 right-0 flex gap-1 bg-white border border-gray-200 rounded-md shadow px-2 py-1 z-50">
            <button onClick={() => deleteNode(id)} className="p-1 rounded hover:bg-red-100 text-red-400" title="삭제">
              <Trash2 size={13} />
            </button>
          </div>
        )}

        {/* 이미지 */}
        {d.imageDataUrl ? (
          <img
            src={d.imageDataUrl}
            alt={d.caption || '이미지'}
            className="w-full flex-1 object-contain nodrag"
            draggable={false}
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-300 gap-2">
            <ImageOff size={32} />
            <span className="text-xs">이미지 없음</span>
          </div>
        )}

        {/* 캡션 */}
        <input
          className="nodrag px-2 py-1 text-xs text-center text-gray-500 border-t border-gray-100 bg-gray-50 outline-none w-full"
          value={d.caption || ''}
          placeholder="캡션 입력..."
          onChange={e => updateNodeData(id, { caption: e.target.value } as any)}
        />
      </div>
    </>
  );
}
