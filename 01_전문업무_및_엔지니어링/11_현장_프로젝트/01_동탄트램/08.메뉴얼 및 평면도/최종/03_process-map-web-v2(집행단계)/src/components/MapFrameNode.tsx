import React from 'react';
import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';
import { FileCheck2 } from 'lucide-react';

const MapFrameNode = ({ data }: NodeProps<NodeData>) => {
  const isDarkMode = useStore(state => state.isDarkMode);

  const mainTitle = data.label || '🏢 동탄도시철도(트램) 건설공사 · 사전토공사 프로세스 맵';

  return (
    <div
      className={`map-frame-node rounded-xl transition-all pointer-events-none select-none ${
        isDarkMode
          ? 'bg-slate-950/40 border-2 border-slate-800/80 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.7)] ring-1 ring-slate-800'
          : 'bg-slate-50/50 border-2 border-slate-300/90 shadow-2xl ring-1 ring-slate-200'
      }`}
      style={{
        width: '100%',
        height: '100%',
        boxSizing: 'border-box',
      }}
    >
      {/* Top Integrated Master Header Bar (2배 대형 Executive Linear Dark 타이틀 헤더 바) */}
      <div
        className="w-full h-32 px-10 rounded-t-xl flex items-center justify-between gap-8 border-b-2 border-indigo-900/60 pointer-events-auto backdrop-blur-md bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-950 text-white shadow-2xl"
      >
        {/* Left: Project & Process Title (2배 큼직하고 웅장한 대형 타이틀) */}
        <div className="flex items-center gap-5 min-w-0">
          <div className="w-4 h-16 bg-gradient-to-b from-indigo-400 via-blue-500 to-cyan-300 rounded-full flex-shrink-0 shadow-xl shadow-indigo-500/40" />
          <div className="flex flex-col justify-center">
            <h1 className="text-2xl sm:text-4xl font-black tracking-tight text-white flex items-center gap-3 truncate drop-shadow-md">
              {mainTitle}
            </h1>
            <span className="text-sm font-black text-indigo-300 tracking-widest uppercase mt-1 drop-shadow-xs">
              ENTERPRISE PROCESS MATRIX & CHECKLIST SYSTEM
            </span>
          </div>
        </div>

        {/* Center: Phase Timeline Progress Flow (글자 크기 1.5배 확대 & 눈부신 고대비 플래티넘 화이트 테마) */}
        <div className="hidden xl:flex items-center gap-3.5 px-7 py-3.5 rounded-2xl bg-white text-slate-900 border-2 border-indigo-400 shadow-2xl backdrop-blur-md text-base sm:text-lg font-black">
          <span className="bg-indigo-600 text-white px-3 py-1 rounded-xl text-xs sm:text-sm font-black shadow-md tracking-wider">
            FLOW:
          </span>
          <span className="text-slate-950 font-black">D-90 사전조사</span>
          <span className="text-indigo-600 font-black text-xl">➔</span>
          <span className="text-slate-950 font-black">D-60 인허가</span>
          <span className="text-indigo-600 font-black text-xl">➔</span>
          <span className="text-slate-950 font-black">D-30 시공계획</span>
          <span className="text-indigo-600 font-black text-xl">➔</span>
          <span className="text-slate-950 font-black">D-Day 착공점검</span>
          <span className="text-indigo-600 font-black text-xl">➔</span>
          <span className="bg-amber-400 text-slate-950 px-3 py-1 rounded-xl shadow-md font-black border border-amber-500">
            D+10~75 본공사
          </span>
        </div>

        {/* Right: Interactive Legend Badges */}
        <div className="flex items-center gap-2.5 flex-shrink-0">
          {/* Department Color Legends */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/90 border border-slate-700/70 text-xs font-bold">
            <div className="flex items-center gap-1.5 text-indigo-300">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-sm" />
              <span>공무/계약</span>
            </div>
            <span className="text-slate-600">|</span>
            <div className="flex items-center gap-1.5 text-emerald-300">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-sm" />
              <span>시공/현장</span>
            </div>
            <span className="text-slate-600">|</span>
            <div className="flex items-center gap-1.5 text-amber-300">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-sm" />
              <span>품질/안전</span>
            </div>
          </div>

          {/* System Version Tag */}
          <div className="px-3 py-1.5 rounded-xl bg-indigo-950/80 border border-indigo-700/60 text-xs font-bold text-indigo-300 flex items-center gap-1.5">
            <FileCheck2 size={14} className="text-indigo-400" />
            <span>v2.0</span>
          </div>
        </div>
      </div>

      {/* Frame Bottom Status Footer Bar */}
      <div className="absolute bottom-4 left-8 right-8 flex items-center justify-between text-xs font-medium text-slate-500 dark:text-slate-500 pointer-events-none">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>동탄도시철도(트램) 건설공사 표준 프로세스 맵 v2.0</span>
        </div>
        <div>
          <span>MASTER BOUNDARY FRAME (5,900 x 2,150 px)</span>
        </div>
      </div>
    </div>
  );
};

export default React.memo(MapFrameNode);
