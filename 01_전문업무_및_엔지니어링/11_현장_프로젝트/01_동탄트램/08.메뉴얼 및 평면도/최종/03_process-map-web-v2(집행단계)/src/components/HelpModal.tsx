import { useState } from 'react';
import { X, HelpCircle, FileSpreadsheet, GitMerge, LayoutGrid, FileText, Sparkles, CheckCircle2, BookOpen, ShieldCheck } from 'lucide-react';

interface HelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function HelpModal({ isOpen, onClose }: HelpModalProps) {
  const [activeTab, setActiveTab] = useState<'features' | 'workflow' | 'faq'>('features');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-white border border-slate-200 rounded-3xl shadow-2xl overflow-hidden flex flex-col transition-all">
        {/* 모달 헤더 (화사하고 세련된 라이트 인디고 헤더) */}
        <div className="flex items-center justify-between px-7 py-5 bg-gradient-to-r from-indigo-50 via-white to-blue-50 border-b border-slate-200 shadow-xs">
          <div className="flex items-center gap-3.5">
            <div className="p-3 bg-indigo-600 text-white rounded-2xl shadow-md shadow-indigo-200">
              <HelpCircle className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-black text-slate-900 tracking-tight">
                  프로세스 맵 자동화 웹앱 & 사용자 가이드
                </h2>
                <span className="px-2.5 py-0.5 text-[11px] font-black bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-full shadow-2xs">
                  v2.0 Official
                </span>
              </div>
              <p className="text-xs text-slate-600 font-bold mt-0.5 flex items-center gap-2">
                <span>동탄트램 및 전문 공종 WBS 기반 스마트 프로세스 맵 시스템</span>
                <span className="font-black text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200/80">
                  ✨ Designed & Developed by 김재형
                </span>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2.5 text-slate-400 hover:text-slate-800 hover:bg-slate-100 rounded-2xl transition-all"
            title="닫기"
          >
            <X size={22} />
          </button>
        </div>

        {/* 탭 네비게이션 (밝은 라이트 탭) */}
        <div className="flex items-center gap-2 px-7 py-3.5 bg-slate-50/80 border-b border-slate-200 text-xs font-black">
          <button
            onClick={() => setActiveTab('features')}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl transition-all ${
              activeTab === 'features'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200 font-black'
                : 'text-slate-600 hover:bg-slate-200/70 hover:text-slate-900'
            }`}
          >
            <Sparkles size={16} />
            <span>🚀 핵심 특징 & 기능</span>
          </button>

          <button
            onClick={() => setActiveTab('workflow')}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl transition-all ${
              activeTab === 'workflow'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200 font-black'
                : 'text-slate-600 hover:bg-slate-200/70 hover:text-slate-900'
            }`}
          >
            <BookOpen size={16} />
            <span>📖 단계별 사용 방법</span>
          </button>

          <button
            onClick={() => setActiveTab('faq')}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl transition-all ${
              activeTab === 'faq'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200 font-black'
                : 'text-slate-600 hover:bg-slate-200/70 hover:text-slate-900'
            }`}
          >
            <ShieldCheck size={16} />
            <span>💡 엑셀 팁 & FAQ</span>
          </button>
        </div>

        {/* 모달 본문 영역 (밝고 화사한 극강 가독성 레이아웃) */}
        <div className="p-7 overflow-y-auto flex-1 space-y-6 bg-white text-slate-800">
          {/* TAB 1: 핵심 특징 */}
          {activeTab === 'features' && (
            <div className="space-y-6 animate-fadeIn">
              <div className="p-5 bg-gradient-to-br from-indigo-50/90 via-blue-50/40 to-slate-50 border-2 border-indigo-200 rounded-2xl shadow-xs">
                <h3 className="text-sm font-black text-indigo-950 mb-1.5 flex items-center gap-2">
                  <span>💡 스마트 프로세스 맵이란?</span>
                </h3>
                <p className="text-xs text-slate-700 leading-relaxed font-bold">
                  본 시스템은 건설·엔지니어링 프로젝트의 엑셀 WBS(Work Breakdown Structure) 데이터를 읽어와 
                  <span className="font-extrabold text-indigo-700 underline underline-offset-2 ml-1">
                    6대 주관 부서(세로축) x 5대 공정 마일스톤(가로축)
                  </span> 격자 맵으로 1초 만에 시각화해 주는 스마트 공정 관리 솔루션입니다.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                  <div className="flex items-center gap-2.5 text-indigo-700 mb-2 font-black text-sm">
                    <div className="p-2 bg-indigo-100 rounded-xl">
                      <FileSpreadsheet size={20} />
                    </div>
                    <h4>엑셀 WBS 자동 파싱 & 맵 생성</h4>
                  </div>
                  <p className="text-xs text-slate-600 font-bold leading-relaxed">
                    엑셀 파일 내의 공종별 시트(토공, 구조물, 궤도, 신호, 전철 등)를 자동 인식하여 각 공종 전용 프로세스 맵으로 빌드합니다.
                  </p>
                </div>

                <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                  <div className="flex items-center gap-2.5 text-indigo-700 mb-2 font-black text-sm">
                    <div className="p-2 bg-emerald-100 text-emerald-700 rounded-xl">
                      <GitMerge size={20} />
                    </div>
                    <h4>L4 코드 기반 선행/후행 자동 연결</h4>
                  </div>
                  <p className="text-xs text-slate-600 font-bold leading-relaxed">
                    엑셀의 L4 코드(예: 9000-7-1)와 선행/후행 관계를 해석하여 카드 간 직각 공정선(`smoothstep`)을 최단거리로 그려줍니다.
                  </p>
                </div>

                <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                  <div className="flex items-center gap-2.5 text-indigo-700 mb-2 font-black text-sm">
                    <div className="p-2 bg-blue-100 text-blue-700 rounded-xl">
                      <LayoutGrid size={20} />
                    </div>
                    <h4>카드 겹침 0% 노드 스택 레이아웃</h4>
                  </div>
                  <p className="text-xs text-slate-600 font-bold leading-relaxed">
                    동일 마일스톤 x 동일 주관 부서 셀에 복수의 액티비티가 존재해도 폭 480px 격자로 자동 배치되어 카드 겹침이 0%입니다.
                  </p>
                </div>

                <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                  <div className="flex items-center gap-2.5 text-indigo-700 mb-2 font-black text-sm">
                    <div className="p-2 bg-amber-100 text-amber-700 rounded-xl">
                      <FileText size={20} />
                    </div>
                    <h4>표준서 & 수속 서류 1:1 팝업 연동</h4>
                  </div>
                  <p className="text-xs text-slate-600 font-bold leading-relaxed">
                    액티비티 카드의 수행지침, 법안 시방 규정, 산출물 서식 및 더블클릭 표준서 HTML 원본을 팝업으로 연동합니다.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: 단계별 사용 방법 */}
          {activeTab === 'workflow' && (
            <div className="space-y-4 animate-fadeIn">
              <div className="flex items-start gap-4 p-4 border-2 border-slate-200 rounded-2xl bg-slate-50/70 hover:bg-white transition-all">
                <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-md">1</div>
                <div>
                  <h4 className="text-sm font-black text-slate-900 flex items-center gap-2">
                    <span>📊 엑셀 WBS 불러오기</span>
                  </h4>
                  <p className="text-xs text-slate-600 font-bold mt-1 leading-relaxed">
                    상단 툴바의 <span className="font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">📊 엑셀 WBS</span> 버튼을 눌러 WBS 엑셀 파일(예: v7 파일)을 업로드합니다. 
                    모든 공종 시트가 즉시 일괄 파싱됩니다.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 border-2 border-slate-200 rounded-2xl bg-slate-50/70 hover:bg-white transition-all">
                <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-md">2</div>
                <div>
                  <h4 className="text-sm font-black text-slate-900 flex items-center gap-2">
                    <span>📂 공종 선택 메뉴 탐색</span>
                  </h4>
                  <p className="text-xs text-slate-600 font-bold mt-1 leading-relaxed">
                    상단 툴바 아래 <span className="font-black text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">공종 선택 메뉴</span>에서 
                    원하는 공종(예: 🚜 토공, 🏗️ 구조물, 🚃 궤도 등)을 선택하면 전용 프로세스 맵으로 전환됩니다.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 border-2 border-slate-200 rounded-2xl bg-slate-50/70 hover:bg-white transition-all">
                <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-md">3</div>
                <div>
                  <h4 className="text-sm font-black text-slate-900 flex items-center gap-2">
                    <span>📅 착공일 기준 마일스톤 달력 반영</span>
                  </h4>
                  <p className="text-xs text-slate-600 font-bold mt-1 leading-relaxed">
                    상단 <span className="font-black text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">📅 D-Day 마일스톤 설정</span>을 선택 후 기준 착공일을 입력하면 
                    D-90, D-60, D-30 등 실제 달력 날짜가 맵 상단에 계산됩니다.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 border-2 border-slate-200 rounded-2xl bg-slate-50/70 hover:bg-white transition-all">
                <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-md">4</div>
                <div>
                  <h4 className="text-sm font-black text-slate-900 flex items-center gap-2">
                    <span>🔴 연결선 클릭 시 빨간색 강조 & 개별/전체 삭제</span>
                  </h4>
                  <p className="text-xs text-slate-600 font-bold mt-1 leading-relaxed">
                    연결선을 마우스로 클릭하면 <span className="font-black text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">강렬한 빨간색 실선</span>으로 전환되어 
                    진행 방향이 한눈에 강조되며, <span className="font-black text-slate-800">Delete</span> 키 또는 툴바의 <span className="font-black text-rose-700">✂️ 연결선 전체 삭제</span>로 손쉽게 정리 가능합니다.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 border-2 border-slate-200 rounded-2xl bg-slate-50/70 hover:bg-white transition-all">
                <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-md">5</div>
                <div>
                  <h4 className="text-sm font-black text-slate-900 flex items-center gap-2">
                    <span>📄 수행지침 / 체크리스트 열람 & 팝업 표준서</span>
                  </h4>
                  <p className="text-xs text-slate-600 font-bold mt-1 leading-relaxed">
                    카드의 <span className="font-black text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">수행지침</span> 또는 
                    <span className="font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">체크리스트</span> 버튼으로 상세 사이드바를 열람하고 원본 표준서를 확인합니다.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: FAQ & Tips */}
          {activeTab === 'faq' && (
            <div className="space-y-4 animate-fadeIn">
              <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                <h4 className="text-xs font-black text-slate-900 mb-1.5 flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  Q. 엑셀 파일의 선행/후행 컬럼은 어떻게 작성하나요?
                </h4>
                <p className="text-xs text-slate-600 font-bold leading-relaxed pl-6">
                  엑셀 공종 시트의 4번째 열(L4 코드: 예 9000-7-1)을 기준으로, 5번째 열(선행)과 6번째 열(후행)에 상대방 L4 코드를 기재합니다. 
                  쉼표(,), 세미콜론(;), 슬래시(/)를 이용해 여러 선/후행 코드를 동시에 입력할 수 있습니다.
                </p>
              </div>

              <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                <h4 className="text-xs font-black text-slate-900 mb-1.5 flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  Q. 카드 제목 위치에 일정이 표시되면 어떻게 되나요?
                </h4>
                <p className="text-xs text-slate-600 font-bold leading-relaxed pl-6">
                  파서 내부의 고도화된 패턴 분석기를 통해 D-90, P-30 등의 기한 문구와 한글 액티비티 명을 자동 식별합니다. 
                  엑셀 컬럼 순서가 뒤바뀌어 있더라도 파서가 자동 교정하여 액티비티 명을 100% 카드 메인 헤더로 표시합니다.
                </p>
              </div>

              <div className="p-5 border-2 border-slate-200 rounded-2xl bg-white hover:border-indigo-300 transition-all shadow-xs">
                <h4 className="text-xs font-black text-slate-900 mb-1.5 flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-indigo-600" />
                  Q. 보고서용 이미지(PNG) 또는 PDF 파일로 저장하려면?
                </h4>
                <p className="text-xs text-slate-600 font-bold leading-relaxed pl-6">
                  상단 툴바 우측의 <span className="font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">PNG</span> 및 
                  <span className="font-extrabold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">PDF</span> 버튼을 누르시면 
                  현재 프로세스 맵 화면을 고해상도 도면 규격 파일로 바로 내보내실 수 있습니다.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* 모달 푸터 (밝은 라이트 푸터) */}
        <div className="flex items-center justify-between px-7 py-4 bg-slate-100/80 border-t border-slate-200">
          <span className="text-xs text-slate-600 font-bold">
            💡 팁: 마우스 휠 스크롤 또는 Ctrl + 휠로 맵 전체를 자유롭게 확대/축소하며 탐색하실 수 있습니다.
          </span>
          <button
            onClick={onClose}
            className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-black shadow-md shadow-indigo-200 transition-all"
          >
            확인 및 닫기
          </button>
        </div>
      </div>
    </div>
  );
}
