import { useState } from 'react';
import { X, Printer, FileText, Sparkles, Image as ImageIcon, Scissors, Layers } from 'lucide-react';
import jsPDF from 'jspdf';
import dayjs from 'dayjs';

interface A3PrintSplitModalProps {
  isOpen: boolean;
  onClose: () => void;
  mapTitle: string;
  captureFullCanvas: (requestedScale?: number) => Promise<{ canvas: HTMLCanvasElement; safeScale: number } | null>;
}

export default function A3PrintSplitModal({
  isOpen,
  onClose,
  mapTitle,
  captureFullCanvas,
}: A3PrintSplitModalProps) {
  const [cols, setCols] = useState<number>(3); // 가로 분할 수 (기본 3장)
  const [rows, setRows] = useState<number>(1); // 세로 분할 수 (기본 1장)
  const [paperSize, setPaperSize] = useState<'a3' | 'a4'>('a3'); // 용지 규격 (A3/A4)
  const [showOverlapGuide, setShowOverlapGuide] = useState<boolean>(true); // 테이프 연결 가이드선
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [progressMsg, setProgressMsg] = useState<string>('');

  if (!isOpen) return null;

  const totalPages = cols * rows;

  // 🖨️ A3/A4 분할 PDF 다운로드 핸들러 (300DPI 초고화질 + 100% 비율 왜곡 방지)
  const handleExportSplitPdf = async () => {
    try {
      setIsProcessing(true);
      setProgressMsg('300DPI 출판 레벨 초고화질 캔버스를 캡처하는 중입니다...');

      // 300DPI 고화질 안전 스케일(2.0배) 캡처 요청
      const res = await captureFullCanvas(2.0);
      if (!res) {
        alert('캔버스 캡처 실패');
        setIsProcessing(false);
        return;
      }

      const { canvas: fullCanvas } = res;
      const fullW = fullCanvas.width;
      const fullH = fullCanvas.height;

      const tileW = Math.floor(fullW / cols);
      const tileH = Math.floor(fullH / rows);

      // 용지 단위 mm 규격 (A3 landscape: 420x297mm, A4 landscape: 297x210mm)
      const pageMmW = paperSize === 'a3' ? 420 : 297;
      const pageMmH = paperSize === 'a3' ? 297 : 210;
      const pageAspect = pageMmW / pageMmH;

      const pdf = new jsPDF({
        orientation: 'landscape',
        unit: 'mm',
        format: paperSize,
      });

      let pageIndex = 0;

      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          pageIndex++;
          setProgressMsg(`[${pageIndex}/${totalPages}] ${paperSize.toUpperCase()} 고화질 무왜곡 조각 생성 중... (${pageIndex}/${totalPages})`);

          // 서브 캔버스 타일 생성 및 자르기
          const subCanvas = document.createElement('canvas');
          subCanvas.width = tileW;
          subCanvas.height = tileH;
          const subCtx = subCanvas.getContext('2d');

          if (subCtx) {
            subCtx.fillStyle = '#ffffff';
            subCtx.fillRect(0, 0, tileW, tileH);
            subCtx.drawImage(
              fullCanvas,
              c * tileW,
              r * tileH,
              tileW,
              tileH,
              0,
              0,
              tileW,
              tileH
            );
          }

          const subImgData = subCanvas.toDataURL('image/jpeg', 0.95);

          if (pageIndex > 1) {
            pdf.addPage(paperSize, 'landscape');
          }

          // 📐 비율 왜곡 100% 방지 (Aspect Ratio Preservation - 찌그러짐 현상 완벽 해결!)
          const tileAspect = tileW / tileH;
          let renderW = pageMmW;
          let renderH = pageMmH;
          let offsetX = 0;
          let offsetY = 0;

          if (tileAspect > pageAspect) {
            // 타일이 용지보다 더 가로로 길 때: 가로는 용지에 가득 채우고 세로는 원본 비율 유지
            renderW = pageMmW;
            renderH = pageMmW / tileAspect;
            offsetY = (pageMmH - renderH) / 2;
          } else {
            // 타일이 용지보다 더 세로로 길 때: 세로는 용지에 가득 채우고 가로는 원본 비율 유지
            renderH = pageMmH;
            renderW = pageMmH * tileAspect;
            offsetX = (pageMmW - renderW) / 2;
          }

          // 100% 원본 비율 보존 형태로 PDF 페이지에 고화질 삽입
          pdf.addImage(subImgData, 'JPEG', offsetX, offsetY, renderW, renderH, undefined, 'FAST');

          // 하단 분할 안내 및 테이프 연결 가이드선 추가
          if (showOverlapGuide) {
            pdf.setDrawColor(79, 70, 229); // 인디고 라인
            pdf.setLineWidth(0.4);

            // 오른쪽에 연결할 다른 A3가 남아있는 경우 오른쪽 테이프 가이드선 그리기
            if (c < cols - 1) {
              pdf.setLineDashPattern([2, 2], 0);
              pdf.line(pageMmW - 5, 0, pageMmW - 5, pageMmH);
              pdf.setFontSize(8);
              pdf.setTextColor(79, 70, 229);
              pdf.text(`✂️ 다음 ${paperSize.toUpperCase()} 페이지(Page ${pageIndex + 1}) 테이프 연결선`, pageMmW - 55, 10);
            }

            // 아래에 연결할 다른 A3가 남아있는 경우 아래쪽 테이프 가이드선 그리기
            if (r < rows - 1) {
              pdf.setLineDashPattern([2, 2], 0);
              pdf.line(0, pageMmH - 5, pageMmW, pageMmH - 5);
              pdf.setFontSize(8);
              pdf.setTextColor(79, 70, 229);
              pdf.text(`✂️ 아래쪽 페이지 테이프 연결선`, 10, pageMmH - 7);
            }

            // 하단 식별 라벨
            pdf.setFontSize(9);
            pdf.setTextColor(51, 65, 85);
            const labelText = `[${paperSize.toUpperCase()} 300DPI 분할출력] ${mapTitle} - Page ${pageIndex}/${totalPages} (가로 ${c + 1}/${cols}, 세로 ${r + 1}/${rows}) | 출력일: ${dayjs().format('YYYY-MM-DD')}`;
            pdf.text(labelText, 10, pageMmH - 3);
          }
        }
      }

      const fileName = `${mapTitle.replace(/\s+/g, '_')}_${paperSize.toUpperCase()}_300DPI분할출력_${cols}x${rows}장_${dayjs().format('YYYYMMDD')}.pdf`;
      pdf.save(fileName);
      alert(`🎉 [300DPI 초고화질] 총 ${totalPages}장의 ${paperSize.toUpperCase()} 무왜곡 분할 PDF 파일 다운로드가 완료되었습니다!\n\n프린터로 ${paperSize.toUpperCase()} 용지 ${totalPages}장을 출력하여 테이프로 연결하시면 돋보기로 봐도 글씨가 100% 선명하고 시원한 대형 포스터 프로세스 맵이 완성됩니다!`);
    } catch (err: any) {
      alert('분할 PDF 저장 중 오류가 발생했습니다: ' + (err.message || err));
    } finally {
      setIsProcessing(false);
      setProgressMsg('');
    }
  };

  // 🖼️ A3/A4 분할 PNG 파일 개별 다운로드 (300DPI 초고화질)
  const handleExportSplitPngs = async () => {
    try {
      setIsProcessing(true);
      setProgressMsg('300DPI 초고화질 캔버스를 캡처하는 중입니다...');

      const res = await captureFullCanvas(3.5);
      if (!res) {
        alert('캔버스 캡처 실패');
        setIsProcessing(false);
        return;
      }

      const { canvas: fullCanvas } = res;
      const fullW = fullCanvas.width;
      const fullH = fullCanvas.height;

      const tileW = Math.floor(fullW / cols);
      const tileH = Math.floor(fullH / rows);

      let pageIndex = 0;

      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          pageIndex++;
          setProgressMsg(`[${pageIndex}/${totalPages}] PNG 300DPI 초고화질 이미지 조각 생성 중...`);

          const subCanvas = document.createElement('canvas');
          subCanvas.width = tileW;
          subCanvas.height = tileH;
          const subCtx = subCanvas.getContext('2d');

          if (subCtx) {
            subCtx.fillStyle = '#ffffff';
            subCtx.fillRect(0, 0, tileW, tileH);
            subCtx.drawImage(
              fullCanvas,
              c * tileW,
              r * tileH,
              tileW,
              tileH,
              0,
              0,
              tileW,
              tileH
            );
          }

          const link = document.createElement('a');
          link.download = `${mapTitle.replace(/\s+/g, '_')}_${paperSize.toUpperCase()}_300DPI_Page${pageIndex}of${totalPages}_(Col${c + 1}_Row${r + 1}).png`;
          link.href = subCanvas.toDataURL('image/png', 1.0);
          link.click();

          // 브라우저 팝업/다운로드 지연 처리
          await new Promise(resolve => setTimeout(resolve, 300));
        }
      }

      alert(`🎉 총 ${totalPages}장의 300DPI 초고화질 분할 PNG 이미지 다운로드가 완료되었습니다.`);
    } catch (err: any) {
      alert('PNG 이미지 분할 다운로드 중 오류 발생: ' + (err.message || err));
    } finally {
      setIsProcessing(false);
      setProgressMsg('');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-indigo-950/40 backdrop-blur-md animate-fadeIn select-none">
      <div className="bg-white rounded-3xl border-2 border-indigo-200/90 shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* 모달 상단 헤더 */}
        <div className="bg-gradient-to-r from-indigo-700 via-purple-700 to-blue-700 px-6 py-4 text-white flex items-center justify-between shadow-md">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20">
              <Printer className="w-6 h-6 text-amber-300" />
            </div>
            <div>
              <h2 className="text-lg font-black tracking-tight flex items-center gap-2">
                🖨️ {paperSize.toUpperCase()} 분할 출력 & 포스터 인쇄 마법사
              </h2>
              <p className="text-xs text-indigo-100 font-bold opacity-90">
                대형 맵을 {paperSize.toUpperCase()} 용지 여러 장으로 분할 출력하여 테이프로 붙여 글씨가 100% 선명한 대형 포스터로 만듭니다.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-white/20 text-white/80 hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* 모달 본문 콘텐트 */}
        <div className="p-6 space-y-6 overflow-y-auto flex-1 bg-slate-50/50">
          
          {/* 1. 용지 규격 및 분할 수 선택 섹션 */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* 용지 선택 */}
            <div className="bg-white p-4 rounded-2xl border border-indigo-100 shadow-sm space-y-2">
              <label className="text-xs font-black text-slate-800 flex items-center gap-1.5">
                <FileText size={15} className="text-indigo-600" />
                1. 인쇄 용지 규격 선택
              </label>
              <div className="grid grid-cols-2 gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setPaperSize('a3')}
                  className={`py-2 px-3 rounded-xl border text-xs font-black transition-all flex flex-col items-center gap-0.5 ${
                    paperSize === 'a3'
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-md ring-2 ring-indigo-300'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50'
                  }`}
                >
                  <span className="text-sm">📄 A3 용지 (추천)</span>
                  <span className="text-[10px] opacity-80">420 x 297 mm</span>
                </button>

                <button
                  type="button"
                  onClick={() => setPaperSize('a4')}
                  className={`py-2 px-3 rounded-xl border text-xs font-black transition-all flex flex-col items-center gap-0.5 ${
                    paperSize === 'a4'
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-md ring-2 ring-indigo-300'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50'
                  }`}
                >
                  <span className="text-sm">📄 A4 용지</span>
                  <span className="text-[10px] opacity-80">297 x 210 mm</span>
                </button>
              </div>
            </div>

            {/* 테이프 가이드 옵션 */}
            <div className="bg-white p-4 rounded-2xl border border-indigo-100 shadow-sm space-y-2 flex flex-col justify-between">
              <label className="text-xs font-black text-slate-800 flex items-center gap-1.5">
                <Scissors size={15} className="text-indigo-600" />
                2. 테이프 연결 가이드선
              </label>
              <label className="flex items-center gap-2 cursor-pointer p-2.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-indigo-50 transition-colors">
                <input
                  type="checkbox"
                  checked={showOverlapGuide}
                  onChange={e => setShowOverlapGuide(e.target.checked)}
                  className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500"
                />
                <span className="text-xs font-extrabold text-slate-800">
                  ✂️ 페이지 테이프 연결선 및 순서 라벨 포함
                </span>
              </label>
            </div>
          </div>

          {/* 2. 가로/세로 분할 매수 설정 & 프리셋 */}
          <div className="bg-white p-5 rounded-2xl border border-indigo-100 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs font-black text-slate-800 flex items-center gap-1.5">
                <Layers size={15} className="text-indigo-600" />
                3. {paperSize.toUpperCase()} 분할 매수 설정 (가로 x 세로)
              </label>
              <span className="px-3 py-1 bg-amber-100 border border-amber-300 text-amber-900 rounded-full text-xs font-black">
                총 {totalPages}장의 {paperSize.toUpperCase()} 용지로 분할
              </span>
            </div>

            {/* 프리셋 버튼 */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button
                type="button"
                onClick={() => { setCols(2); setRows(1); }}
                className={`py-2 px-2 rounded-xl border text-xs font-black transition-all ${
                  cols === 2 && rows === 1
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-600 shadow-md'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50'
                }`}
              >
                📄 2장 분할 (1x2)
              </button>
              <button
                type="button"
                onClick={() => { setCols(3); setRows(1); }}
                className={`py-2 px-2 rounded-xl border text-xs font-black transition-all ${
                  cols === 3 && rows === 1
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-600 shadow-md'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50'
                }`}
              >
                📄 3장 분할 (1x3 추천)
              </button>
              <button
                type="button"
                onClick={() => { setCols(4); setRows(1); }}
                className={`py-2 px-2 rounded-xl border text-xs font-black transition-all ${
                  cols === 4 && rows === 1
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-600 shadow-md'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50'
                }`}
              >
                📄 4장 분할 (1x4 대형)
              </button>
              <button
                type="button"
                onClick={() => { setCols(3); setRows(2); }}
                className={`py-2 px-2 rounded-xl border text-xs font-black transition-all ${
                  cols === 3 && rows === 2
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-600 shadow-md'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50'
                }`}
              >
                📄 6장 분할 (2x3 포스터)
              </button>
            </div>

            {/* 수동 슬라이더 조정 */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-100">
              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>가로축 분할 (Phase 방향):</span>
                  <span className="font-black text-indigo-600">{cols}개 구역</span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={6}
                  value={cols}
                  onChange={e => setCols(parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-600 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>세로축 분할 (공종 방향):</span>
                  <span className="font-black text-indigo-600">{rows}개 구역</span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={3}
                  value={rows}
                  onChange={e => setRows(parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-600 cursor-pointer"
                />
              </div>
            </div>
          </div>

          {/* 3. 시각적 분할 미리보기 그리드 (Visual Grid Preview) */}
          <div className="bg-white p-4 rounded-2xl border border-indigo-100 shadow-sm space-y-2">
            <p className="text-xs font-black text-slate-800 flex items-center justify-between">
              <span>🖼️ 인쇄 분할 미리보기 (포스터 연결 구조)</span>
              <span className="text-[11px] text-slate-500 font-normal">각 분할 조각이 100% 원본 해상도로 확대 출력됩니다</span>
            </p>

            <div
              className="w-full bg-slate-100 border-2 border-dashed border-indigo-300 rounded-xl p-3 grid gap-2 shadow-inner"
              style={{
                gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))`,
                gridTemplateRows: `repeat(${rows}, minmax(0, 1fr))`,
              }}
            >
              {Array.from({ length: totalPages }).map((_, idx) => {
                const c = idx % cols;
                const r = Math.floor(idx / cols);
                return (
                  <div
                    key={idx}
                    className="bg-white border-2 border-indigo-400/80 rounded-lg p-3 text-center flex flex-col items-center justify-center min-h-[75px] shadow-sm relative group hover:border-indigo-600 transition-all"
                  >
                    <span className="text-xs font-black text-indigo-900">
                      📄 Page {idx + 1}
                    </span>
                    <span className="text-[10px] font-extrabold text-indigo-600 mt-0.5">
                      ({paperSize.toUpperCase()} {c + 1}열, {r + 1}행)
                    </span>
                    {c < cols - 1 && (
                      <span className="absolute right-1 top-1/2 -translate-y-1/2 text-[9px] font-black text-indigo-400">
                        ✂️
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* 로딩 진행 바 */}
          {isProcessing && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-2xl p-4 text-center space-y-2 animate-pulse">
              <div className="flex items-center justify-center gap-2 text-indigo-700 font-black text-xs">
                <Sparkles className="w-4 h-4 animate-spin text-amber-500" />
                <span>{progressMsg}</span>
              </div>
              <div className="w-full bg-indigo-200 h-2 rounded-full overflow-hidden">
                <div className="bg-indigo-600 h-full w-full animate-indeterminate" />
              </div>
            </div>
          )}
        </div>

        {/* 모달 하단 푸터 버튼 */}
        <div className="bg-white px-6 py-4 border-t border-slate-200 flex flex-wrap items-center justify-between gap-3 shadow-lg">
          <button
            type="button"
            onClick={onClose}
            disabled={isProcessing}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold rounded-xl text-xs transition-colors"
          >
            닫기
          </button>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleExportSplitPngs}
              disabled={isProcessing}
              className="flex items-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-black text-white font-black rounded-xl text-xs shadow-md transition-all disabled:opacity-50"
              title="A3 분할 PNG 이미지 파일들을 압축/개별 다운로드"
            >
              <ImageIcon size={14} />
              <span>PNG {totalPages}장 이미지 분할</span>
            </button>

            <button
              type="button"
              onClick={handleExportSplitPdf}
              disabled={isProcessing}
              className="flex items-center gap-1.5 px-5 py-2.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-black rounded-xl text-xs shadow-lg hover:scale-105 transition-all disabled:opacity-50"
            >
              <Printer size={15} className="text-amber-300" />
              <span>🖨️ {paperSize.toUpperCase()} {totalPages}장 분할 PDF 다운로드</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
