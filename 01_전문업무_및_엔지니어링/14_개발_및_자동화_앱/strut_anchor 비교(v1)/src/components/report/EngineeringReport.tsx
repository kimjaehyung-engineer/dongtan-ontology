import React from 'react';
import { AlternativeSpec, ProjectInputs } from '../../types';
import { X, Printer, Award, FileText } from 'lucide-react';

interface EngineeringReportProps {
  isOpen: boolean;
  onClose: () => void;
  inputs: ProjectInputs;
  alternatives: AlternativeSpec[];
  selectedAlt: AlternativeSpec;
}

export const EngineeringReport: React.FC<EngineeringReportProps> = ({
  isOpen,
  onClose,
  inputs,
  alternatives,
  selectedAlt
}) => {
  if (!isOpen) return null;

  const topAlt = alternatives.find(a => a.rank === 1) || selectedAlt;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white border border-slate-300 rounded-lg w-full max-w-4xl shadow-2xl overflow-hidden flex flex-col my-auto max-h-[90vh]">
        {/* 상단 툴바 */}
        <div className="no-print px-5 py-3 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-600" />
            <h3 className="text-sm font-bold text-slate-800">가시설 지보공법 사전검토 기술보고서 (인쇄 및 PDF 출력)</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded bg-blue-600 hover:bg-blue-700 text-xs font-bold text-white shadow-sm transition-all"
            >
              <Printer className="w-3.5 h-3.5" /> 인쇄 / PDF 저장
            </button>
            <button
              onClick={onClose}
              className="p-1 rounded hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* 인쇄 영역 */}
        <div className="p-8 overflow-y-auto bg-white text-slate-900 font-sans leading-relaxed text-xs">
          {/* 표제 */}
          <div className="border-b-2 border-slate-900 pb-4 mb-6 text-center">
            <div className="text-[11px] font-bold text-slate-500 tracking-wider mb-1">
              PRELIMINARY ENGINEERING DESIGN & ALTERNATIVES EVALUATION REPORT
            </div>
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              {inputs.projectName}
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              - 가시설 벽체 및 지보공(Strut vs Ground Anchor) 사전 최적화 및 4대안 비교 기술검토서 -
            </p>
            <div className="mt-3 flex justify-between text-[10px] text-slate-500 border-t border-slate-200 pt-2 font-mono">
              <span>위치: {inputs.siteLocation}</span>
              <span>해석 엔진: C++ 1D 탄소성 지반반력법(FEM) 코어</span>
              <span>검토일자: {new Date().toLocaleDateString('ko-KR')}</span>
            </div>
          </div>

          {/* 1. 설계 기본 조건 및 지반 단면 */}
          <div className="mb-6">
            <h2 className="text-sm font-bold text-slate-900 border-l-4 border-blue-600 pl-2 mb-2">
              1. 굴착 제원 및 프로젝트 설계 조건
            </h2>
            <div className="grid grid-cols-2 gap-4 bg-slate-50 p-3 rounded border border-slate-200">
              <div>
                <p>• <strong>굴착 깊이 (H):</strong> {inputs.excavationDepth.toFixed(1)} m</p>
                <p>• <strong>굴착 폭 (B):</strong> {inputs.excavationWidth.toFixed(1)} m</p>
                <p>• <strong>가시설 총 연장 (L):</strong> {inputs.totalWallPerimeter.toFixed(1)} m</p>
              </div>
              <div>
                <p>• <strong>배후 지하수위:</strong> GL -{inputs.waterTableBehind.toFixed(1)} m</p>
                <p>• <strong>인접 부지경계 이격:</strong> {inputs.boundaryDistance.toFixed(1)} m</p>
                <p>• <strong>상부 상재하중:</strong> {inputs.surcharge.toFixed(1)} kN/㎡</p>
              </div>
            </div>
          </div>

          {/* 2. 지층 구성 및 P-y 지반반력계수 제원 */}
          <div className="mb-6">
            <h2 className="text-sm font-bold text-slate-900 border-l-4 border-blue-600 pl-2 mb-2">
              2. 지층 구성 및 P-y 지반반력계수 제원
            </h2>
            <table className="w-full text-left border-collapse border border-slate-300 text-[10.5px] eng-table">
              <thead>
                <tr>
                  <th>지층명</th>
                  <th className="text-center">심도 (m)</th>
                  <th className="text-center">단위중량 (kN/㎥)</th>
                  <th className="text-center">점착력 (kN/㎡)</th>
                  <th className="text-center">내부마찰각 (°)</th>
                  <th className="text-center">수평지반반력계수 (kN/㎥)</th>
                  <th className="text-center">N치</th>
                </tr>
              </thead>
              <tbody>
                {inputs.soils.map((s, idx) => (
                  <tr key={idx}>
                    <td>{s.name}</td>
                    <td className="text-center font-mono">GL -{s.topDepth.toFixed(1)} ~ -{s.bottomDepth.toFixed(1)}</td>
                    <td className="text-center font-mono">{s.gamma}</td>
                    <td className="text-center font-mono">{s.cohesion}</td>
                    <td className="text-center font-mono">{s.frictionAngle}°</td>
                    <td className="text-center font-mono">{s.kh0.toLocaleString()}</td>
                    <td className="text-center font-mono">{s.NValue}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* 3. 3대안 종합 비교표 */}
          <div className="mb-6">
            <h2 className="text-sm font-bold text-slate-900 border-l-4 border-blue-600 pl-2 mb-2">
              3. 가시설 지보공법 3대안 종합 성능 및 다기준 비교 평가 결과
            </h2>
            <table className="w-full text-left border-collapse border border-slate-300 text-[10.5px] eng-table">
              <thead>
                <tr>
                  <th>구분 / 대안</th>
                  <th className="text-center">지보 구성</th>
                  <th className="text-center">최대변위</th>
                  <th className="text-center">H-Pile 응력비</th>
                  <th className="text-center">근입/보일링 FS</th>
                  <th className="text-center">총 공기</th>
                  <th className="text-center">직접공사비</th>
                  <th className="text-center">시공/민원성</th>
                  <th className="text-center">종합 순위</th>
                </tr>
              </thead>
              <tbody>
                {alternatives.map((alt) => (
                  <tr key={alt.id} className={alt.rank === 1 ? 'bg-amber-50/80 font-bold' : ''}>
                    <td>
                      <strong>대안 {alt.id}</strong> ({alt.type})
                    </td>
                    <td className="text-center font-mono">{alt.supports.length}단 구성</td>
                    <td className="text-center font-mono">{alt.maxDisplacement} mm</td>
                    <td className="text-center font-mono">
                      {alt.pileStressRatio} ({alt.pileStressRatio <= 1.0 ? 'O.K' : 'N.G'})
                    </td>
                    <td className="text-center font-mono">{alt.embedmentSF} / {alt.boilingSF}</td>
                    <td className="text-center font-mono font-bold text-indigo-700">{alt.periodDays}일</td>
                    <td className="text-center font-mono text-blue-700 font-bold">
                      {(alt.totalCostWon / 1e8).toFixed(2)} 억원
                    </td>
                    <td className="text-center font-mono">
                      작업({alt.workSpaceScore}) / 경계({alt.boundaryRiskScore})
                    </td>
                    <td className="text-center">
                      {alt.rank === 1 ? <span className="text-amber-700">★ 1위 (최적)</span> : `${alt.rank}위`}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* 4. 최적 대안 상세 검토 결과 */}
          <div className="mb-6 bg-blue-50/60 p-4 rounded border border-blue-200">
            <h2 className="text-sm font-bold text-blue-900 mb-2 flex items-center gap-1.5">
              <Award className="w-4 h-4 text-amber-600" />
              4. 최적 추천 대안 상세 분석 [대안 {topAlt.id}: {topAlt.name}]
            </h2>
            <div className="space-y-1.5 text-[11px] text-slate-700">
              <p>
                • <strong>구조적 안정성</strong>: C++ 1D 비선형 탄소성 FEM 해석 결과, 최종 굴착 단계에서 벽체 최대 변위는 <strong>{topAlt.maxDisplacement}mm</strong>, H-Pile 최대 휨응력비는 <strong>{topAlt.pileStressRatio}</strong> (기준 1.0 이하)로 안전성을 확보함.
              </p>
              <p>
                • <strong>지반 파괴 안정성</strong>: 근입장 안전율 F.S = <strong>{topAlt.embedmentSF}</strong> (기준 1.2 이상), 보일링 안전율 F.S = <strong>{topAlt.boilingSF}</strong> (기준 1.5 이상), 히빙 안전율 F.S = <strong>{topAlt.heavingSF}</strong> 로 지반 파괴에 대해 안전함.
              </p>
              <p>
                • <strong>경제성 및 시공성</strong>: 총 직접공사비는 약 <strong>{(topAlt.totalCostWon / 1e6).toFixed(1)} 백만원</strong> (m당 약 {(topAlt.costPerM / 1e4).toFixed(0)}만원)으로 추정되며, {topAlt.workSpaceScore > 80 ? '내부 굴착 작업공간이 원활하여 공기 단축에 유리함.' : '부지 경계 침범 민원 리스크가 없어 인허가 및 시공 안정성이 탁월함.'}
              </p>
            </div>
          </div>

          {/* 5. 종합 결론 및 향후 설계 권고사항 */}
          <div>
            <h2 className="text-sm font-bold text-slate-900 border-l-4 border-blue-600 pl-2 mb-2">
              5. 종합 결론 및 상용 SW 상세설계 권고사항
            </h2>
            <div className="text-[11px] text-slate-700 space-y-1 text-justify">
              <p>
                1. 사전 구조 및 다기준 비교 검토 결과, <strong>{topAlt.name}</strong>이(가) 구조 안전성과 경제성, 시공성 측면에서 가장 우수한 1순위 대안으로 판정되었습니다.
              </p>
              <p>
                2. 본 보고서에 수록된 지층 정수, 벽체 강성(EI={Math.round(topAlt.wall.EI)}kNm²/m), 지보 스프링 강성을 상용 해석 프로그램(SUNEX / GEO-XD)에 연계 적용하여 단계별 2D 연속체 탄소성 상세 해석을 확정할 것을 권고합니다.
              </p>
            </div>
          </div>

          {/* 서명란 */}
          <div className="mt-8 pt-4 border-t border-slate-300 flex justify-between text-[11px] text-slate-600">
            <div>작성자: 가시설 전문 엔지니어링 자동화 시스템</div>
            <div>확인: 책임기술자 (인)</div>
          </div>
        </div>
      </div>
    </div>
  );
};
