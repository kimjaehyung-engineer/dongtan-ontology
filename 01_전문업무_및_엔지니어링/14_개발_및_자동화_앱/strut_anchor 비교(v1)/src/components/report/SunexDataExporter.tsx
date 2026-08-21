import React, { useState } from 'react';
import { AlternativeSpec, ProjectInputs } from '../../types';
import { X, Copy, Check, FileSpreadsheet, Download } from 'lucide-react';

interface SunexDataExporterProps {
  isOpen: boolean;
  onClose: () => void;
  inputs: ProjectInputs;
  selectedAlt: AlternativeSpec;
}

export const SunexDataExporter: React.FC<SunexDataExporterProps> = ({
  isOpen,
  onClose,
  inputs,
  selectedAlt
}) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const generateSunexFormat = () => {
    let text = `=================================================================\n`;
    text += `[SUNEX / GEO-XD 연계 모델링 파라미터 시트]\n`;
    text += `프로젝트명: ${inputs.projectName}\n`;
    text += `검토 대안: ${selectedAlt.name}\n`;
    text += `=================================================================\n\n`;

    text += `1. 지층 물성 데이터 (Soil Layer Parameters)\n`;
    text += `No\t지층명\t상부심도(m)\t하부심도(m)\t습윤γ(kN/m3)\t포화γ(kN/m3)\tc(kN/m2)\tφ(°)\tEs(kN/m2)\tkh0(kN/m3)\tN치\n`;
    inputs.soils.forEach((s, idx) => {
      text += `${idx + 1}\t${s.name}\t${s.topDepth}\t${s.bottomDepth}\t${s.gamma}\t${s.gammaSat}\t${s.cohesion}\t${s.frictionAngle}\t${s.Es}\t${s.kh0}\t${s.NValue}\n`;
    });

    text += `\n2. 가시설 벽체 사양 (Wall Section Parameters)\n`;
    text += `벽체형식: ${selectedAlt.wall.type} (${selectedAlt.wall.name})\n`;
    text += `수평간격: ${selectedAlt.wall.spacing} m\n`;
    text += `단위폭당 휨강성 EI: ${Math.round(selectedAlt.wall.EI)} kN·m²/m\n`;
    text += `단위폭당 축강성 EA: ${Math.round(selectedAlt.wall.EA)} kN/m\n`;
    text += `단면계수 Zx: ${selectedAlt.wall.Zx} cm³/본\n`;
    text += `총 벽체길이 L: ${selectedAlt.wall.totalLength} m (굴착고: ${inputs.excavationDepth}m, 근입장: ${(selectedAlt.wall.totalLength - inputs.excavationDepth).toFixed(1)}m)\n`;

    text += `\n3. 지보공 단계별 모델링 파라미터 (Support Elements)\n`;
    text += `단\t구분\t설치심도(m)\t각도(°)\t수평간격(m)\t선행하중(kN)\t축강성(kN/m)\t자유장(m)\t정착장(m)\t허용내력(kN)\t규격\n`;
    selectedAlt.supports.forEach((sup, idx) => {
      text += `${idx + 1}\t${sup.type}\t${sup.depth}\t${sup.angle}\t${sup.horizSpacing}\t${sup.preload}\t${sup.springStiffness}\t${sup.freeLength}\t${sup.bondLength}\t${sup.allowableCapacity}\t${sup.specName}\n`;
    });

    text += `\n4. 하중 및 수위 조건 (Boundary & Loads)\n`;
    text += `상재하중 q: ${inputs.surcharge} kN/m²\n`;
    text += `배면 지하수위 G.W.L: -${inputs.waterTableBehind} m\n`;
    text += `굴착 폭 B: ${inputs.excavationWidth} m\n`;
    text += `=================================================================\n`;
    return text;
  };

  const textContent = generateSunexFormat();

  const handleCopy = () => {
    navigator.clipboard.writeText(textContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SUNEX_Input_${selectedAlt.type}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-lg w-full max-w-3xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* 모달 헤더 */}
        <div className="px-4 py-3 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-emerald-600" />
            <div>
              <h3 className="text-sm font-bold text-slate-900">상용 SW (SUNEX / GEO-XD) 연계 데이터 시트</h3>
              <p className="text-xs text-slate-500">해석 모델링에 필요한 지반정수, 벽체 강성, 지보 스프링 파라미터</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 텍스트 영역 */}
        <div className="p-4 flex-1 overflow-y-auto bg-slate-50">
          <pre className="bg-white p-4 rounded border border-slate-200 text-xs font-mono text-slate-800 leading-relaxed overflow-x-auto select-all shadow-inner">
            {textContent}
          </pre>
        </div>

        {/* 하단 버튼 */}
        <div className="px-4 py-3 border-t border-slate-200 bg-white flex items-center justify-between">
          <span className="text-xs text-slate-500">
            * 엑셀 또는 SUNEX 입력창에 바로 붙여넣기(Ctrl+V) 하실 수 있습니다.
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={handleDownload}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 border border-slate-300 transition-all"
            >
              <Download className="w-3.5 h-3.5" /> TXT 다운로드
            </button>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded bg-blue-600 hover:bg-blue-700 text-xs font-bold text-white shadow-sm transition-all"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? '복사 완료!' : '클립보드 전체 복사'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
