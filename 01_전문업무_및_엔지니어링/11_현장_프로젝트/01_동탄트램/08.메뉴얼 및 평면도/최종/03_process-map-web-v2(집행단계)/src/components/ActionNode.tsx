import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { NodeResizer } from '@reactflow/node-resizer';
import '@reactflow/node-resizer/dist/style.css';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';
import { Building2, HardHat, ShieldCheck, FileText, ClipboardList, CheckSquare, Flame } from 'lucide-react';

export default function ActionNode({ id, data, selected }: NodeProps<NodeData>) {
  const isDarkMode = useStore(state => state.isDarkMode);
  const isCpHighlight = useStore(state => state.isCpHighlight);

  const cpNumbers = [1, 2, 6, 7, 9, 10, 11, 16, 20, 22, 24, 26, 28, 30];
  const nodeNum = parseInt(id.replace(/[^0-9]/g, ''), 10);
  const isCritical = data.isCritical ?? (nodeNum ? cpNumbers.includes(nodeNum) : true);

  const isCpActive = isCpHighlight && isCritical;

  const dept = data.department || '';
  let deptTheme = {
    headerGradient: 'from-slate-900 via-indigo-950 to-slate-900',
    badgeBgLight: 'bg-indigo-50 text-indigo-950 border-indigo-200 font-black',
    badgeBgDark: 'bg-indigo-950/90 text-indigo-200 border-indigo-800 font-black',
    icon: Building2,
  };

  if (dept.includes('공사') || dept.includes('시공')) {
    deptTheme = {
      headerGradient: 'from-slate-900 via-indigo-950 to-slate-900',
      badgeBgLight: 'bg-slate-100 text-slate-900 border-slate-300 font-black',
      badgeBgDark: 'bg-slate-900 text-slate-200 border-slate-700 font-black',
      icon: HardHat,
    };
  } else if (dept.includes('품질') || dept.includes('안전') || dept.includes('기술')) {
    deptTheme = {
      headerGradient: 'from-slate-900 via-indigo-950 to-slate-900',
      badgeBgLight: 'bg-slate-100 text-slate-900 border-slate-300 font-black',
      badgeBgDark: 'bg-slate-900 text-slate-200 border-slate-700 font-black',
      icon: ShieldCheck,
    };
  }

  const DeptIcon = deptTheme.icon;

  const handleOpenTab = (e: React.MouseEvent, tab: 'standard' | 'directive' | 'checklist') => {
    e.stopPropagation();
    const { nodes, edges, setNodesAndEdges, setActiveDetailTab } = useStore.getState();
    setActiveDetailTab(tab);
    setNodesAndEdges(
      nodes.map(n => ({
        ...n,
        selected: n.id === id,
      })),
      edges
    );
  };

  const handleCardClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  return (
    <>
      <div className="relative w-full h-full overflow-visible">
        <div
          className={`rounded-lg border-2 w-full h-full font-sans transition-all duration-300 overflow-hidden shadow-xl ${
            isCpActive ? 'ring-4 ring-rose-500 border-rose-500 shadow-rose-500/30 z-20' : ''
          } bg-white text-slate-900 ${
            selected
              ? 'border-indigo-600 ring-4 ring-indigo-500/30 shadow-2xl shadow-indigo-500/20'
              : 'border-slate-300 hover:border-indigo-500 hover:shadow-2xl'
          } min-w-[380px] min-h-[460px]`}
          style={{ display: 'flex', flexDirection: 'column', height: '100%', minHeight: '460px' }}
        >
          {/* Header Stripe - 가로 100% 한 줄 서술 보장 */}
          <div
            className="px-4 py-3.5 min-h-[58px] text-white font-bold gap-2.5 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border-b border-indigo-900/40 shadow-sm"
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0, minHeight: '58px' }}
          >
            {/* 타이틀 영역: 가로 100% 한 줄 서술 및 툴팁 제공 */}
            <div className="flex items-center gap-2 min-w-0 flex-1 overflow-hidden" title={data.label || data.wbsCode || '액티비티명'}>
              <DeptIcon size={18} className="flex-shrink-0 text-white/90" />
              <span className="font-black text-white text-[16.5px] whitespace-nowrap truncate block">
                {data.label || data.wbsCode || '액티비티명'}
              </span>
            </div>

            {/* D-Day 기한 및 담당 부서 뱃지 */}
            <div className="flex items-center gap-1.5 flex-shrink-0">
              {(() => {
                let displayDate = data.date || '';
                if (!displayDate || !/^[DP][+-]?\d+/i.test(displayDate)) {
                  displayDate = nodeNum ? (nodeNum <= 2 ? 'D-90' : nodeNum <= 6 ? 'D-60' : nodeNum <= 12 ? 'D-30' : nodeNum <= 21 ? 'D-Day' : 'D+10') : 'D-Day';
                }
                if (displayDate.length > 12) displayDate = displayDate.slice(0, 10);
                return (
                  <span
                    className="px-2 py-0.5 rounded-md text-[11px] font-black bg-amber-400 text-slate-950 shadow-sm whitespace-nowrap border border-amber-500"
                    title={`D-Day / 일정: ${data.date || displayDate}`}
                  >
                    📅 {displayDate}
                  </span>
                );
              })()}
              <span
                className={`px-2 py-0.5 rounded-md text-[11px] font-extrabold shadow-sm whitespace-nowrap border ${
                  isDarkMode ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-slate-800 border-slate-300'
                }`}
                title={`주관 부서: ${data.department || '미정'}`}
              >
                🏢 {(data.department || '공사').replace('현장 · ', '').replace('본사 · ', '').slice(0, 10)}
              </span>
            </div>
          </div>

          {/* Body Content Box */}
          <div
            className={`p-4 flex-1 flex flex-col justify-between select-text ${
              isDarkMode ? 'bg-slate-900/90 text-slate-100' : 'bg-white text-slate-900'
            }`}
            onClick={handleCardClick}
          >
            <div
              className="space-y-3 overflow-y-auto custom-scrollbar pr-1"
              style={{
                flex: '1 1 auto',
                minHeight: '280px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
              }}
            >
              {/* 협조부서 명시 */}
              {data.cooperation && (
                <div className="flex items-center gap-2 mb-1 flex-wrap text-[13px]">
                  <span className={`px-2.5 py-0.5 rounded-md font-extrabold border ${
                    isDarkMode ? 'bg-slate-800 text-slate-300 border-slate-700' : 'bg-slate-200/80 text-slate-800 border-slate-300'
                  }`}>
                    🤝 협조: {data.cooperation}
                  </span>
                </div>
              )}

              {data.purpose && (
                <div className="leading-relaxed break-keep-all" style={{ fontSize: `${(data as any).fontSize || data.textStyle?.fontSize || 14.5}px` }} title={data.purpose}>
                  <span className={`font-black mr-1.5 ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`}>🎯 목적:</span>
                  <span className={isDarkMode ? 'text-slate-200' : 'text-slate-900 font-bold'}>{data.purpose}</span>
                </div>
              )}

              {data.method && (
                <div className="leading-relaxed break-keep-all whitespace-pre-line" style={{ fontSize: `${(data as any).fontSize || data.textStyle?.fontSize || 14.5}px` }} title={data.method}>
                  <span className={`font-black mr-1.5 ${isDarkMode ? 'text-amber-400' : 'text-amber-600'}`}>🛠️ 방법:</span>
                  <span className={isDarkMode ? 'text-slate-200' : 'text-slate-900 font-bold'}>{data.method}</span>
                </div>
              )}

              {data.result && (
                <div className="leading-relaxed break-keep-all" style={{ fontSize: `${(data as any).fontSize || data.textStyle?.fontSize || 14.5}px` }} title={data.result}>
                  <span className={`font-black mr-1.5 ${isDarkMode ? 'text-emerald-400' : 'text-emerald-600'}`}>📦 산출물:</span>
                  <span className={isDarkMode ? 'text-slate-200' : 'text-slate-900 font-bold'}>{data.result}</span>
                </div>
              )}

            </div>

            {/* 💡 CP 주경로 뱃지 */}
            {isCritical && (
              <div className="flex justify-end pt-1 pb-1 pr-0.5">
                <span
                  className="bg-rose-600 text-white font-black text-[12px] px-3.5 py-1 rounded-full shadow-md shadow-rose-500/30 animate-pulse flex items-center gap-1 select-none border border-rose-400/50"
                  title="핵심 주경로 (Critical Path)"
                >
                  <Flame size={13} className="text-amber-300" />
                  CP 주경로
                </span>
              </div>
            )}

            {/* Footer 3-Option Pills */}
            <div
              className={`pt-2.5 border-t text-[12.5px] ${
                isDarkMode ? 'border-slate-800' : 'border-slate-300/80'
              }`}
              style={{ flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '6px', marginTop: 'auto' }}
            >
              <button
                onClick={(e) => handleOpenTab(e, 'standard')}
                className={`py-1.5 px-2.5 rounded-md font-bold transition-all border shadow-2xs ${
                  isDarkMode
                    ? 'bg-indigo-950/60 border-indigo-700/60 text-indigo-300 hover:bg-indigo-900/80'
                    : 'bg-indigo-50 border-indigo-200 text-indigo-700 hover:bg-indigo-100'
                }`}
                style={{ flex: '1 1 0%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}
                title="KDS/KCS 법률 및 시방 표준서 열람"
              >
                <FileText size={13} />
                <span>표준서</span>
              </button>

              <button
                onClick={(e) => handleOpenTab(e, 'directive')}
                className={`py-1.5 px-2.5 rounded-md font-bold transition-all border shadow-2xs ${
                  isDarkMode
                    ? 'bg-amber-950/60 border-amber-700/60 text-amber-300 hover:bg-amber-900/80'
                    : 'bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100'
                }`}
                style={{ flex: '1 1 0%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}
                title="단계별 수행지침 및 인허가 절차 열람"
              >
                <ClipboardList size={13} />
                <span>수행지침</span>
              </button>

              <button
                onClick={(e) => handleOpenTab(e, 'checklist')}
                className={`py-1.5 px-2.5 rounded-md font-bold transition-all border shadow-2xs ${
                  isDarkMode
                    ? 'bg-emerald-950/60 border-emerald-700/60 text-emerald-300 hover:bg-emerald-900/80'
                    : 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100'
                }`}
                style={{ flex: '1 1 0%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}
                title="필수 점검 항목 및 이행 체크리스트 열람"
              >
                <CheckSquare size={13} />
                <span>체크리스트</span>
              </button>
            </div>
          </div>
        </div>

        {/* Handles: Left (Target & Source) */}
        <Handle
          type="target"
          position={Position.Left}
          id="left-target"
          isConnectable={true}
          style={{ top: '50%', left: -10, transform: 'translateY(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-indigo-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto"
        />
        <Handle
          type="source"
          position={Position.Left}
          id="left-source"
          isConnectable={true}
          style={{ top: '50%', left: -10, transform: 'translateY(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-indigo-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto opacity-0"
        />
        <Handle
          type="target"
          position={Position.Left}
          id="left"
          isConnectable={true}
          style={{ top: '50%', left: -10, transform: 'translateY(-50%)', zIndex: 59 }}
          className="opacity-0 pointer-events-none"
        />

        {/* Handles: Right (Source & Target) */}
        <Handle
          type="source"
          position={Position.Right}
          id="right-source"
          isConnectable={true}
          style={{ top: '50%', right: -10, transform: 'translateY(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-emerald-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto"
        />
        <Handle
          type="target"
          position={Position.Right}
          id="right-target"
          isConnectable={true}
          style={{ top: '50%', right: -10, transform: 'translateY(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-emerald-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto opacity-0"
        />
        <Handle
          type="source"
          position={Position.Right}
          id="right"
          isConnectable={true}
          style={{ top: '50%', right: -10, transform: 'translateY(-50%)', zIndex: 59 }}
          className="opacity-0 pointer-events-none"
        />

        {/* Handles: Top (Target & Source) */}
        <Handle
          type="target"
          position={Position.Top}
          id="top-target"
          isConnectable={true}
          style={{ left: '50%', top: -10, transform: 'translateX(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-blue-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto"
        />
        <Handle
          type="source"
          position={Position.Top}
          id="top-source"
          isConnectable={true}
          style={{ left: '50%', top: -10, transform: 'translateX(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-blue-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto opacity-0"
        />
        <Handle
          type="target"
          position={Position.Top}
          id="top"
          isConnectable={true}
          style={{ left: '50%', top: -10, transform: 'translateX(-50%)', zIndex: 59 }}
          className="opacity-0 pointer-events-none"
        />

        {/* Handles: Bottom (Source & Target) */}
        <Handle
          type="source"
          position={Position.Bottom}
          id="bottom-source"
          isConnectable={true}
          style={{ left: '50%', bottom: -10, transform: 'translateX(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-teal-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto"
        />
        <Handle
          type="target"
          position={Position.Bottom}
          id="bottom-target"
          isConnectable={true}
          style={{ left: '50%', bottom: -10, transform: 'translateX(-50%)', zIndex: 60 }}
          className="!w-7 !h-7 !bg-teal-600 !border-3 !border-white shadow-xl cursor-crosshair hover:scale-150 transition-transform pointer-events-auto opacity-0"
        />
        <Handle
          type="source"
          position={Position.Bottom}
          id="bottom"
          isConnectable={true}
          style={{ left: '50%', bottom: -10, transform: 'translateX(-50%)', zIndex: 59 }}
          className="opacity-0 pointer-events-none"
        />
      </div>

      <NodeResizer color="#4f46e5" isVisible={selected} minWidth={340} minHeight={400} lineStyle={{ border: 'none' }} />
    </>
  );
}
