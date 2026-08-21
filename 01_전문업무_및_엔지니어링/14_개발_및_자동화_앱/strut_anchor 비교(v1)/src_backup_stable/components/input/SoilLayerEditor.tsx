import React from 'react';
import { SoilLayer } from '../../types';
import { Plus, Trash2, Layers } from 'lucide-react';

interface SoilLayerEditorProps {
  soils: SoilLayer[];
  onChangeSoils: (soils: SoilLayer[]) => void;
}

export const SoilLayerEditor: React.FC<SoilLayerEditorProps> = ({ soils, onChangeSoils }) => {
  const handleUpdateLayer = (index: number, field: keyof SoilLayer, value: any) => {
    const updated = [...soils];
    updated[index] = { ...updated[index], [field]: value };
    onChangeSoils(updated);
  };

  const handleAddLayer = () => {
    const last = soils[soils.length - 1];
    const top = last ? last.bottomDepth : 0;
    const newLayer: SoilLayer = {
      id: `soil-${Date.now()}`,
      name: `신규지층 ${soils.length + 1}`,
      topDepth: top,
      bottomDepth: top + 5.0,
      gamma: 20.0,
      gammaSat: 21.0,
      cohesion: 20.0,
      frictionAngle: 32.0,
      Es: 50000,
      kh0: 40000,
      NValue: 30,
      isCohesive: false,
      color: '#fbbf24'
    };
    onChangeSoils([...soils, newLayer]);
  };

  const handleDeleteLayer = (index: number) => {
    if (soils.length <= 1) return;
    const updated = soils.filter((_, idx) => idx !== index);
    onChangeSoils(updated);
  };

  return (
    <div className="eng-panel">
      <div className="eng-panel-header">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" />
          <div>
            <h3 className="text-xs font-bold text-slate-800">지층 프로파일 및 비선형 지반정수 (Soil & P-y Properties)</h3>
            <p className="text-[11px] text-slate-500">C++ 1D 탄소성 지반스프링(kh0) 및 주동/수동 한계토압 산정 물성</p>
          </div>
        </div>
        <button
          onClick={handleAddLayer}
          className="flex items-center gap-1 px-2.5 py-1 rounded bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-bold transition-all shadow-sm"
        >
          <Plus className="w-3.5 h-3.5" /> 지층 추가
        </button>
      </div>

      <div className="p-3 overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse eng-table">
          <thead>
            <tr>
              <th className="w-12 text-center">색상</th>
              <th className="w-36">지층명</th>
              <th className="w-32 text-center">심도 (m)</th>
              <th className="w-32 text-center">단위중량 γ/γsat</th>
              <th className="w-20 text-center">점착력 c</th>
              <th className="w-20 text-center">마찰각 φ</th>
              <th className="w-24 text-center">변형계수 Es</th>
              <th className="w-24 text-center">반력계수 kh0</th>
              <th className="w-16 text-center">N치</th>
              <th className="w-14 text-center">점성토</th>
              <th className="w-12 text-center">삭제</th>
            </tr>
          </thead>
          <tbody className="font-mono text-slate-700 bg-white">
            {soils.map((soil, idx) => (
              <tr key={soil.id} className="hover:bg-slate-50">
                <td className="text-center py-1">
                  <input
                    type="color"
                    value={soil.color}
                    onChange={(e) => handleUpdateLayer(idx, 'color', e.target.value)}
                    className="w-5 h-5 rounded cursor-pointer border border-slate-300 bg-white"
                  />
                </td>
                <td>
                  <input
                    type="text"
                    value={soil.name}
                    onChange={(e) => handleUpdateLayer(idx, 'name', e.target.value)}
                    className="bg-white border border-slate-300 rounded px-2 py-0.5 text-slate-800 text-xs w-full font-sans focus:border-blue-500 focus:outline-none"
                  />
                </td>
                <td className="text-center">
                  <div className="flex items-center justify-center gap-1">
                    <input
                      type="number"
                      step="0.5"
                      value={soil.topDepth}
                      onChange={(e) => handleUpdateLayer(idx, 'topDepth', parseFloat(e.target.value) || 0)}
                      className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-12 text-right focus:border-blue-500 focus:outline-none"
                    />
                    <span className="text-slate-400 font-sans">~</span>
                    <input
                      type="number"
                      step="0.5"
                      value={soil.bottomDepth}
                      onChange={(e) => handleUpdateLayer(idx, 'bottomDepth', parseFloat(e.target.value) || 0)}
                      className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-12 text-right focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </td>
                <td className="text-center">
                  <div className="flex items-center justify-center gap-1">
                    <input
                      type="number"
                      step="0.5"
                      value={soil.gamma}
                      onChange={(e) => handleUpdateLayer(idx, 'gamma', parseFloat(e.target.value) || 0)}
                      className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-11 text-right focus:border-blue-500 focus:outline-none"
                      title="습윤 단위중량 (kN/m3)"
                    />
                    <span className="text-slate-400 font-sans">/</span>
                    <input
                      type="number"
                      step="0.5"
                      value={soil.gammaSat}
                      onChange={(e) => handleUpdateLayer(idx, 'gammaSat', parseFloat(e.target.value) || 0)}
                      className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-11 text-right focus:border-blue-500 focus:outline-none"
                      title="포화 단위중량 (kN/m3)"
                    />
                  </div>
                </td>
                <td className="text-center">
                  <input
                    type="number"
                    step="1"
                    value={soil.cohesion}
                    onChange={(e) => handleUpdateLayer(idx, 'cohesion', parseFloat(e.target.value) || 0)}
                    className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-14 text-right focus:border-blue-500 focus:outline-none"
                    title="점착력 c (kN/m2)"
                  />
                </td>
                <td className="text-center">
                  <input
                    type="number"
                    step="1"
                    value={soil.frictionAngle}
                    onChange={(e) => handleUpdateLayer(idx, 'frictionAngle', parseFloat(e.target.value) || 0)}
                    className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-14 text-right focus:border-blue-500 focus:outline-none"
                    title="내부마찰각 φ (°)"
                  />
                </td>
                <td className="text-center">
                  <input
                    type="number"
                    step="1000"
                    value={soil.Es}
                    onChange={(e) => handleUpdateLayer(idx, 'Es', parseFloat(e.target.value) || 0)}
                    className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-16 text-right focus:border-blue-500 focus:outline-none"
                    title="변형계수 Es (kN/m2)"
                  />
                </td>
                <td className="text-center">
                  <input
                    type="number"
                    step="1000"
                    value={soil.kh0}
                    onChange={(e) => handleUpdateLayer(idx, 'kh0', parseFloat(e.target.value) || 0)}
                    className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-16 text-right focus:border-blue-500 focus:outline-none"
                    title="수평지반반력계수 kh0 (kN/m3)"
                  />
                </td>
                <td className="text-center">
                  <input
                    type="number"
                    value={soil.NValue}
                    onChange={(e) => handleUpdateLayer(idx, 'NValue', parseFloat(e.target.value) || 0)}
                    className="bg-white border border-slate-300 rounded px-1 py-0.5 text-slate-800 text-xs w-12 text-right focus:border-blue-500 focus:outline-none"
                    title="SPT N치"
                  />
                </td>
                <td className="text-center">
                  <input
                    type="checkbox"
                    checked={soil.isCohesive}
                    onChange={(e) => handleUpdateLayer(idx, 'isCohesive', e.target.checked)}
                    className="rounded border-slate-300 text-blue-600 focus:ring-0 cursor-pointer"
                    title="점성토 여부"
                  />
                </td>
                <td className="text-center">
                  <button
                    onClick={() => handleDeleteLayer(idx)}
                    disabled={soils.length <= 1}
                    className="p-1 rounded hover:bg-rose-50 text-slate-400 hover:text-rose-600 disabled:opacity-30 transition-all"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
