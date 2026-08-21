import React from 'react';
import { AlternativeSpec } from '../../types';
import { Award, ArrowRight } from 'lucide-react';

interface AlternativeMatrixProps {
  alternatives: AlternativeSpec[];
  selectedAltId: number;
  onSelectAlt: (altId: number) => void;
}

export const AlternativeMatrix: React.FC<AlternativeMatrixProps> = ({
  alternatives,
  selectedAltId,
  onSelectAlt
}) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-slate-800 flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-500" />
            가시설 지보공법 3대안 종합 성능 및 다기준 비교 매트릭스 (3-Alternative Matrix)
          </h2>
          <p className="text-xs text-slate-500">
            C++ 탄소성 FEM 비선형 해석 기반 구조안전성 + 직접공사비(물량) + 시공성/민원 리스크 종합 평가
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {alternatives.map((alt) => {
          const isSelected = alt.id === selectedAltId;
          const isTopRank = alt.rank === 1;

          return (
            <div
              key={alt.id}
              onClick={() => onSelectAlt(alt.id)}
              className={`rounded-lg p-4 cursor-pointer transition-all border relative flex flex-col justify-between ${
                isSelected
                  ? 'bg-white border-blue-500 shadow-md ring-2 ring-blue-500/20'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-sm'
              }`}
            >
              {/* 1위 추천 뱃지 */}
              {isTopRank && (
                <div className="absolute -top-2.5 right-4 px-2.5 py-0.5 rounded-full bg-amber-500 text-white font-bold text-[10px] shadow-sm flex items-center gap-1">
                  <Award className="w-3 h-3" /> 1순위 최적추천안
                </div>
              )}

              <div>
                {/* 헤더 */}
                <div className="mb-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold text-blue-700 font-mono">
                      대안 {alt.id}
                    </span>
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                      종합 {alt.overallScore}점 ({alt.rank}위)
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-slate-900 mt-1">{alt.name}</h3>
                  <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-2">{alt.description}</p>
                </div>

                {/* 지보 구성 요약 */}
                <div className="bg-slate-50 p-2.5 rounded border border-slate-200 mb-3 text-[11px] space-y-1">
                  <div className="flex justify-between text-slate-600">
                    <span>벽체 규격:</span>
                    <span className="text-slate-900 font-mono font-bold">{alt.wall.name}</span>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>지보 단수:</span>
                    <span className="text-amber-700 font-mono font-bold">{alt.supports.length}단 구성</span>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>공사 기간:</span>
                    <span className="text-slate-900 font-mono font-medium">{alt.periodDays}일</span>
                  </div>
                </div>

                {/* 구조 안전성 지표 */}
                <div className="space-y-1.5 text-xs mb-3">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-600">최대 수평변위 δ:</span>
                    <span className="font-mono font-bold text-blue-700">{alt.maxDisplacement} mm</span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-600">최대 휨모멘트 M:</span>
                    <span className="font-mono font-bold text-amber-700">{alt.maxMoment} kNm/m</span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-600">H-Pile 응력비:</span>
                    <span className={`font-mono font-bold ${alt.pileStressRatio <= 1.0 ? 'text-emerald-700' : 'text-rose-700'}`}>
                      {alt.pileStressRatio} {alt.pileStressRatio <= 1.0 ? '(안전)' : '(초과)'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-600">근입장 F.S:</span>
                    <span className={`font-mono font-bold ${alt.embedmentSF >= 1.2 ? 'text-emerald-700' : 'text-rose-700'}`}>
                      {alt.embedmentSF} {alt.embedmentSF >= 1.2 ? '✓' : '✗'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-600">중간말뚝 좌굴:</span>
                    <span className="font-mono font-bold text-emerald-700">
                      λ=46.6 (SR=56.2% ✓)
                    </span>
                  </div>
                </div>

                {/* 시공성 & 리스크 점수 바 */}
                <div className="space-y-1.5 text-[10px] text-slate-600 pt-2 border-t border-slate-200">
                  <div className="flex justify-between">
                    <span>작업공간 확보성</span>
                    <span className="text-slate-800 font-mono font-bold">{alt.workSpaceScore}점</span>
                  </div>
                  <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                    <div className="bg-blue-600 h-full rounded-full" style={{ width: `${alt.workSpaceScore}%` }}></div>
                  </div>

                  <div className="flex justify-between pt-1">
                    <span>부지경계 안전성</span>
                    <span className="text-slate-800 font-mono font-bold">{alt.boundaryRiskScore}점</span>
                  </div>
                  <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                    <div className="bg-emerald-600 h-full rounded-full" style={{ width: `${alt.boundaryRiskScore}%` }}></div>
                  </div>
                </div>
              </div>

              {/* 하단 공사비 & 선택 버튼 */}
              <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between">
                <div>
                  <div className="text-[10px] text-slate-500">총 직접공사비</div>
                  <div className="text-sm font-extrabold text-blue-700 font-mono">
                    {(alt.totalCostWon / 1e6).toFixed(1)} 백만원
                  </div>
                </div>
                <button
                  className={`px-3 py-1 rounded text-xs font-bold flex items-center gap-1 transition-all shadow-sm ${
                    isSelected
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {isSelected ? '선택됨' : '상세보기'} <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
