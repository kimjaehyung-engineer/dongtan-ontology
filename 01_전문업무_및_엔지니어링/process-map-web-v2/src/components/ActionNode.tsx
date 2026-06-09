import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';
import { CheckCircle, AlertCircle, AlertTriangle, Clock } from 'lucide-react';

const statusConfig = {
  normal:  { bg: 'bg-green-100',  border: 'border-green-400',  icon: CheckCircle,     label: '정상',   iconColor: 'text-green-500' },
  warning: { bg: 'bg-yellow-100', border: 'border-yellow-400', icon: AlertTriangle,   label: '주의',   iconColor: 'text-yellow-500' },
  danger:  { bg: 'bg-red-100',    border: 'border-red-400',    icon: AlertCircle,     label: '위험',   iconColor: 'text-red-500' },
  done:    { bg: 'bg-gray-100',   border: 'border-gray-400',   icon: CheckCircle,     label: '완료',   iconColor: 'text-gray-400' },
};

export default function ActionNode({ id, data, selected }: NodeProps<NodeData>) {
  const status = data.status || 'normal';
  const cfg = statusConfig[status];
  const StatusIcon = cfg.icon;
  const headerColor = data.color || '#fca5a5';

  return (
    <>
      <div className={`bg-white rounded-lg shadow-md border-2 w-full h-full flex flex-col text-[11px] font-sans overflow-hidden ${selected ? 'border-blue-500 ring-2 ring-blue-100' : cfg.border} min-w-[200px] min-h-[85px]`}>
        
        {/* Header color stripe with Title on the left, status & D-day on the right */}
        <div className="px-2.5 py-1.5 flex items-center justify-between flex-shrink-0 gap-3" style={{ backgroundColor: headerColor }}>
          <div className="font-bold text-xs text-slate-800 truncate flex-1" title={data.label}>
            {data.label || '제목 없음'}
          </div>
          
          <div className="flex items-center gap-1 flex-shrink-0">
            <div className="flex items-center gap-0.5 bg-white/75 px-1.5 py-0.5 rounded text-[8px] font-bold text-slate-700 shadow-sm">
              <StatusIcon size={9} className={cfg.iconColor} />
              <span>{cfg.label}</span>
            </div>
            {data.daysRemaining !== undefined && (
              <span className="text-[8px] font-bold bg-white/75 rounded px-1.5 py-0.5 flex items-center gap-0.5 text-slate-700 shadow-sm">
                <Clock size={8} />
                D-{data.daysRemaining}
              </span>
            )}
          </div>
        </div>

        {/* Badges (Departments only) */}
        <div className="p-2 flex-1 flex flex-col justify-center min-w-0 bg-slate-50/20">
          <div className="flex flex-col gap-1">
            {data.department && (
              <div className="text-[9px] text-slate-600 truncate flex items-center">
                <span className="font-bold text-slate-400 mr-1.5 w-6 inline-block">주관</span>
                <span className="text-slate-700 font-medium">{data.department}</span>
              </div>
            )}
            {data.cooperation && (
              <div className="text-[9px] text-slate-600 truncate flex items-start">
                <span className="font-bold text-slate-400 mr-1.5 w-6 inline-block flex-shrink-0">협조</span>
                <div className="flex flex-wrap gap-1 items-center">
                  {data.cooperation.split(/[,|/]/).map((dept, i) => {
                    const cleanDept = dept.trim();
                    if (!cleanDept) return null;
                    return (
                      <span key={i} className="text-[8px] font-bold text-blue-600 bg-blue-50/60 px-1.5 py-0.5 rounded border border-blue-100/40">
                        {cleanDept}
                      </span>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>

        <Handle type="target" position={Position.Left} className="w-2 h-2" />
        <Handle type="source" position={Position.Right} className="w-2 h-2" />
        <Handle type="target" position={Position.Top} className="w-2 h-2" id="top" />
        <Handle type="source" position={Position.Bottom} className="w-2 h-2" id="bottom" />
      </div>
      <NodeResizer color="#3b82f6" isVisible={selected} minWidth={160} minHeight={80} />
    </>
  );
}
