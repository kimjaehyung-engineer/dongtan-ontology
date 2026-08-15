import React, { useState } from 'react';
import useStore from '../store/useStore';
import { templateLibrary } from '../data/templateLibrary';
import { FolderOpen, Plus, Trash2, Download, Upload, Check, Sparkles, LayoutGrid, X } from 'lucide-react';
import { parseExcelWbsToDisciplineMaps } from '../utils/excelWbsParser';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onOpenWizard: () => void;
}

export interface SavedProject {
  id: string;
  title: string;
  category: string;
  updatedAt: string;
  nodeCount: number;
  nodes: any[];
  edges: any[];
}

export default function ProjectManagerModal({ isOpen, onClose, onOpenWizard }: Props) {
  const { setNodesAndEdges, setDisciplineMaps, isDarkMode } = useStore();
  const [activeTab, setActiveTab] = useState<'templates' | 'myProjects'>('templates');
  const [savedProjects, setSavedProjects] = useState<SavedProject[]>(() => {
    try {
      const stored = localStorage.getItem('process-map-user-projects');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  if (!isOpen) return null;

  // Load a template into canvas
  const handleLoadTemplate = (templateId: string) => {
    const tmpl = templateLibrary.find(t => t.id === templateId);
    if (tmpl) {
      const { nodes, edges } = tmpl.generator();
      setNodesAndEdges(nodes, edges);
      onClose();
    }
  };

  // Save current canvas as a new project
  const handleSaveCurrentAsProject = () => {
    const name = window.prompt('저장할 프로젝트 맵 이름을 입력하세요:', '나의 프로세스 맵');
    if (!name) return;

    const { nodes, edges } = useStore.getState();
    const newProj: SavedProject = {
      id: `proj-${Date.now()}`,
      title: name,
      category: '사용자 정의',
      updatedAt: new Date().toLocaleDateString('ko-KR'),
      nodeCount: nodes.filter(n => n.type === 'action').length,
      nodes,
      edges,
    };

    const updated = [newProj, ...savedProjects];
    setSavedProjects(updated);
    localStorage.setItem('process-map-user-projects', JSON.stringify(updated));
    alert('프로젝트가 성공적으로 보관함에 저장되었습니다!');
  };

  // Load a saved project
  const handleLoadSavedProject = (proj: SavedProject) => {
    setNodesAndEdges(proj.nodes, proj.edges);
    onClose();
  };

  // Delete a saved project
  const handleDeleteSavedProject = (id: string) => {
    if (!window.confirm('이 프로젝트 맵을 삭제하시겠습니까?')) return;
    const updated = savedProjects.filter(p => p.id !== id);
    setSavedProjects(updated);
    localStorage.setItem('process-map-user-projects', JSON.stringify(updated));
  };

  // Export current map to .pmap (JSON file)
  const handleExportProjectFile = () => {
    const { nodes, edges } = useStore.getState();
    const projectData = {
      version: '2.0',
      exportedAt: new Date().toISOString(),
      nodes,
      edges,
    };

    const blob = new Blob([JSON.stringify(projectData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `process_map_${new Date().toISOString().slice(0, 10)}.pmap`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Import .pmap or .json file
  const handleImportProjectFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const json = JSON.parse(event.target?.result as string);
        if (json.nodes && Array.isArray(json.nodes)) {
          setNodesAndEdges(json.nodes, json.edges || []);
          alert('프로젝트 파일(.pmap)을 성공적으로 불러왔습니다!');
          onClose();
        } else {
          alert('올바른 프로세스 맵 파일 포맷이 아닙니다.');
        }
      } catch (err) {
        alert('파일을 읽는 중 오류가 발생했습니다.');
      }
    };
    reader.readAsText(file);
  };

  // Import Excel WBS File (.xlsx, .xlsm, .csv)
  const handleImportExcelWbs = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const buffer = event.target?.result as ArrayBuffer;
        const result = parseExcelWbsToDisciplineMaps(buffer);
        setDisciplineMaps(result.disciplineMaps);
        alert(`엑셀 공종 파싱 완료!\n총 ${result.disciplineMaps.length}개 공종 시트에 대한 프로세스 맵이 개별 파싱되었습니다.\n\n상단 '공종 선택 메뉴'에서 원하시는 공종 맵을 자유롭게 전환하세요.`);
        onClose();
      } catch (err: any) {
        alert(`엑셀 변환 오류: ${err.message || '파일 형식을 확인해주세요.'}`);
      }
    };
    reader.readAsArrayBuffer(file);
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-md flex items-center justify-center p-4">
      <div
        className={`w-full max-w-4xl max-h-[85vh] rounded-2xl border shadow-2xl flex flex-col overflow-hidden transition-all ${
          isDarkMode ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200 text-slate-900'
        }`}
      >
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center text-white shadow-md">
              <FolderOpen size={20} />
            </div>
            <div>
              <h2 className="text-lg font-black tracking-tight">프로세스 맵 보관함 & 템플릿 라이브러리</h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">사내 공종별 표준 템플릿을 불러오거나 엑셀/파일을 업로드하세요.</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Action Toolbar */}
        <div className="px-6 py-3 border-b border-slate-200 dark:border-slate-800 bg-slate-100/50 dark:bg-slate-950/40 flex items-center justify-between flex-wrap gap-2">
          {/* Tabs */}
          <div className="flex items-center gap-1 bg-slate-200/70 dark:bg-slate-800 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('templates')}
              className={`px-4 py-1.5 rounded-lg text-xs font-extrabold transition-all flex items-center gap-1.5 ${
                activeTab === 'templates'
                  ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <LayoutGrid size={14} />
              <span>공종별 표준 템플릿 ({templateLibrary.length})</span>
            </button>
            <button
              onClick={() => setActiveTab('myProjects')}
              className={`px-4 py-1.5 rounded-lg text-xs font-extrabold transition-all flex items-center gap-1.5 ${
                activeTab === 'myProjects'
                  ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <FolderOpen size={14} />
              <span>내 보관함 ({savedProjects.length})</span>
            </button>
          </div>

          {/* Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                onClose();
                onOpenWizard();
              }}
              className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-md transition-all"
            >
              <Sparkles size={14} />
              <span>✨ 새 맵 만들기 마법사</span>
            </button>

            {/* Excel WBS Upload */}
            <label className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-md transition-all cursor-pointer">
              <Upload size={14} />
              <span>📊 엑셀 WBS 업로드</span>
              <input type="file" accept=".xlsx,.xls,.xlsm,.csv" onChange={handleImportExcelWbs} className="hidden" />
            </label>

            {/* .PMAP File Upload */}
            <label className="px-3 py-1.5 bg-slate-700 hover:bg-slate-800 text-white rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-md transition-all cursor-pointer">
              <Upload size={14} />
              <span>.pmap 파일 열기</span>
              <input type="file" accept=".pmap,.json" onChange={handleImportProjectFile} className="hidden" />
            </label>

            {/* Export Current */}
            <button
              onClick={handleExportProjectFile}
              className="px-3 py-1.5 border border-slate-300 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all"
            >
              <Download size={14} />
              <span>내보내기</span>
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto flex-1 min-h-[380px]">
          {activeTab === 'templates' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {templateLibrary.map(tmpl => (
                <div
                  key={tmpl.id}
                  className={`p-5 rounded-2xl border transition-all flex flex-col justify-between hover:shadow-xl hover:border-indigo-500/50 ${
                    isDarkMode ? 'bg-slate-800/60 border-slate-700/80' : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[11px] font-extrabold px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                        {tmpl.category}
                      </span>
                      <span className="text-xs font-bold text-slate-400">카운트: {tmpl.nodeCount}개 노드</span>
                    </div>
                    <h3 className="text-base font-black text-slate-900 dark:text-slate-100 mb-1">{tmpl.title}</h3>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed mb-4">{tmpl.description}</p>
                  </div>

                  <button
                    onClick={() => handleLoadTemplate(tmpl.id)}
                    className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl flex items-center justify-center gap-2 transition-all shadow-md"
                  >
                    <Check size={14} />
                    이 템플릿으로 맵 생성하기
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-500">현재 보관된 나의 프로젝트 ({savedProjects.length}개)</span>
                <button
                  onClick={handleSaveCurrentAsProject}
                  className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-sm"
                >
                  <Plus size={14} />
                  현재 맵 보관함에 저장하기
                </button>
              </div>

              {savedProjects.length === 0 ? (
                <div className="py-16 text-center text-slate-400 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">
                  <FolderOpen size={40} className="mx-auto mb-3 opacity-40" />
                  <p className="text-sm font-bold">보관함에 저장된 프로젝트가 없습니다.</p>
                  <p className="text-xs text-slate-500 mt-1">상단 템플릿을 선택하거나 '현재 맵 보관함에 저장하기'를 클릭해 저장하세요.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {savedProjects.map(proj => (
                    <div
                      key={proj.id}
                      className={`p-4 rounded-2xl border flex flex-col justify-between ${
                        isDarkMode ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-50 border-slate-200'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-[10px] font-bold text-slate-400">최종 수정: {proj.updatedAt}</span>
                          <span className="text-xs font-bold text-indigo-500">액션 카드 {proj.nodeCount}개</span>
                        </div>
                        <h4 className="text-sm font-black mb-3">{proj.title}</h4>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleLoadSavedProject(proj)}
                          className="flex-1 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 rounded-xl text-xs font-extrabold hover:opacity-90 transition-all"
                        >
                          캔버스에 로딩
                        </button>
                        <button
                          onClick={() => handleDeleteSavedProject(proj.id)}
                          className="p-2 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/50 border border-rose-200 dark:border-rose-800 rounded-xl transition-all"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
