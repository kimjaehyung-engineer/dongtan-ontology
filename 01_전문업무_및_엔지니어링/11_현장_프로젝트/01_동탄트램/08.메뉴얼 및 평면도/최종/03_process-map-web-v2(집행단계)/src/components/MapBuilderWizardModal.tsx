import { useState } from 'react';
import useStore from '../store/useStore';
import type { Node, Edge } from 'reactflow';
import type { NodeData } from '../store/useStore';
import { Sparkles, Plus, Trash2, Check, ArrowRight, ArrowLeft, X } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function MapBuilderWizardModal({ isOpen, onClose }: Props) {
  const { setNodesAndEdges, isDarkMode } = useStore();
  const [step, setStep] = useState<1 | 2 | 3>(1);

  // Step 1: General Info
  const [projectTitle, setProjectTitle] = useState('동탄도시철도(트램) · 신규 공종 프로세스 맵');

  // Step 2: Department Rows (Swimlanes)
  const [departments, setDepartments] = useState<string[]>([
    '🏢 공무 / 계약관리팀',
    '🏗️ 시공 / 공사수행팀',
    '🛡️ 품질 / 안전관리팀',
  ]);

  // Step 3: Timeline Phases (Columns)
  const [phases, setPhases] = useState<{ name: string; dday: string }[]>([
    { name: 'PHASE 1: 사전 기획', dday: 'D-90' },
    { name: 'PHASE 2: 서류 및 검토', dday: 'D-60' },
    { name: 'PHASE 3: 준비 및 인허가', dday: 'D-30' },
    { name: 'PHASE 4: 현장 착공', dday: 'D-Day' },
    { name: 'PHASE 5: 검수 및 준공', dday: 'D+30' },
  ]);

  if (!isOpen) return null;

  // Add department
  const handleAddDept = () => {
    const name = window.prompt('새 부서(행) 이름을 입력하세요:', '👷 협력사 / 기계설비팀');
    if (name) setDepartments([...departments, name]);
  };

  // Remove department
  const handleRemoveDept = (idx: number) => {
    if (departments.length <= 1) {
      alert('최소 1개 이상의 부서 행이 필요합니다.');
      return;
    }
    setDepartments(departments.filter((_, i) => i !== idx));
  };

  // Add Phase
  const handleAddPhase = () => {
    const name = window.prompt('새 공정 단계(열) 이름을 입력하세요:', 'PHASE 6: 후속 공정');
    if (name) setPhases([...phases, { name, dday: 'D+60' }]);
  };

  // Remove Phase
  const handleRemovePhase = (idx: number) => {
    if (phases.length <= 1) {
      alert('최소 1개 이상의 공정 단계가 필요합니다.');
      return;
    }
    setPhases(phases.filter((_, i) => i !== idx));
  };

  // Generate Nodes & Edges
  const handleGenerateMap = () => {
    const nodes: Node<NodeData>[] = [];
    const edges: Edge[] = [];

    const colWidth = 900;
    const phaseStartOffset = 200;
    const totalCanvasWidth = Math.max(3600, phases.length * colWidth + 400);
    const swimlaneHeight = 580;

    // 1. Frame
    nodes.push({
      id: 'map-frame-master',
      type: 'mapFrame',
      position: { x: -40, y: -150 },
      data: { label: projectTitle },
      style: { width: totalCanvasWidth + 80, height: departments.length * 600 + 200, zIndex: -10 },
      draggable: false,
      selectable: false,
    });

    // 2. Swimlanes (Rows)
    departments.forEach((dept, dIdx) => {
      const yPos = -20 + dIdx * 600;
      nodes.push({
        id: `swimlane-${dIdx}`,
        type: 'swimlane',
        position: { x: 0, y: yPos },
        data: { label: dept },
        style: { width: totalCanvasWidth, height: swimlaneHeight, zIndex: -1 },
        draggable: false,
        selectable: true,
      });

      nodes.push({
        id: `rdiv-${dIdx + 1}`,
        type: 'rowDivider',
        position: { x: 0, y: yPos },
        data: {},
        draggable: true,
        selectable: false,
        style: { zIndex: 10 },
      });
    });

    // Bottom divider
    nodes.push({
      id: `rdiv-${departments.length + 1}`,
      type: 'rowDivider',
      position: { x: 0, y: -20 + departments.length * 600 },
      data: {},
      draggable: true,
      selectable: false,
      style: { zIndex: 10 },
    });

    // 3. Phase Headers (Columns)
    phases.forEach((p, pIdx) => {
      const xPos = phaseStartOffset + pIdx * colWidth;

      nodes.push({
        id: `vline-phase-${pIdx}`,
        type: 'verticalLine',
        position: { x: xPos, y: -70 },
        data: { label: p.name, height: departments.length * 600 + 100 },
        style: { zIndex: 5 },
      });

      nodes.push({
        id: `header-phase-${pIdx}`,
        type: 'milestone',
        position: { x: xPos + 10, y: -56 },
        data: {
          label: `📅 ${p.name}`,
          date: p.dday,
          status: 'normal',
        },
      });

      // Sample Action Card for first phase & first dept
      if (pIdx === 0 && departments.length > 0) {
        nodes.push({
          id: `wizard-card-${pIdx}`,
          type: 'action',
          position: { x: xPos + 30, y: 30 },
          data: {
            label: `[예시 업무] 사전 기획 및 수속`,
            department: departments[0],
            purpose: '기초 공정 계획 작성 및 수속',
            method: '사내 표준 공정 수칙 준수',
            result: '승인 및 착수',
            status: 'normal',
            color: '#6366f1',
          },
          style: { width: 330, height: 230 },
        });
      }
    });

    setNodesAndEdges(nodes, edges);
    alert('새 프로세스 맵이 캔버스에 성공적으로 생성되었습니다!');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-md flex items-center justify-center p-4">
      <div
        className={`w-full max-w-2xl rounded-2xl border shadow-2xl flex flex-col overflow-hidden transition-all ${
          isDarkMode ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200 text-slate-900'
        }`}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md">
              <Sparkles size={20} />
            </div>
            <div>
              <h2 className="text-lg font-black tracking-tight">새 프로세스 맵 생성 마법사</h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">Step {step} / 3: 직관적인 3단계 입력으로 나만의 2D 공정 맵을 생성하세요.</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800">
            <X size={20} />
          </button>
        </div>

        {/* Step Progress Bar */}
        <div className="px-6 py-3 bg-slate-100/50 dark:bg-slate-950/40 border-b border-slate-200 dark:border-slate-800 flex items-center justify-around text-xs font-extrabold">
          <div className={`flex items-center gap-2 ${step >= 1 ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'}`}>
            <span className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs">1</span>
            <span>프로젝트 정보</span>
          </div>
          <div className={`flex items-center gap-2 ${step >= 2 ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'}`}>
            <span className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs">2</span>
            <span>부서 행 (Swimlane)</span>
          </div>
          <div className={`flex items-center gap-2 ${step >= 3 ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'}`}>
            <span className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs">3</span>
            <span>공정 단계 (Timeline)</span>
          </div>
        </div>

        {/* Body Steps */}
        <div className="p-6 flex-1 min-h-[320px]">
          {step === 1 && (
            <div className="space-y-4">
              <label className="block text-xs font-black text-slate-700 dark:text-slate-300">프로젝트 타이틀 명칭</label>
              <input
                type="text"
                value={projectTitle}
                onChange={e => setProjectTitle(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm font-bold focus:ring-2 focus:ring-indigo-500 outline-none"
                placeholder="예: 동탄도시철도 1공구 통신설비 가공 맵"
              />
              <p className="text-xs text-slate-500">생성된 타이틀은 캔버스 최상단 마스터 보드 헤더 프레임에 고정되어 표시됩니다.</p>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-black text-slate-700 dark:text-slate-300">관리 부서 및 스윔레인 행 ({departments.length}개)</label>
                <button
                  onClick={handleAddDept}
                  className="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-extrabold flex items-center gap-1"
                >
                  <Plus size={14} />
                  부서 행 추가
                </button>
              </div>

              <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
                {departments.map((dept, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60">
                    <span className="text-xs font-extrabold">{dept}</span>
                    <button onClick={() => handleRemoveDept(idx)} className="p-1 text-rose-500 hover:bg-rose-50 rounded-lg">
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-black text-slate-700 dark:text-slate-300">공정 단계 및 마일스톤 ({phases.length}개)</label>
                <button
                  onClick={handleAddPhase}
                  className="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-extrabold flex items-center gap-1"
                >
                  <Plus size={14} />
                  공정 단계 추가
                </button>
              </div>

              <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
                {phases.map((p, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60">
                    <div className="flex items-center gap-3">
                      <span className="px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 text-[10px] font-bold">{p.dday}</span>
                      <span className="text-xs font-extrabold">{p.name}</span>
                    </div>
                    <button onClick={() => handleRemovePhase(idx)} className="p-1 text-rose-500 hover:bg-rose-50 rounded-lg">
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer Navigation */}
        <div className="px-6 py-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 flex items-center justify-between">
          <button
            onClick={() => setStep((step - 1) as any)}
            disabled={step === 1}
            className="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold disabled:opacity-30 flex items-center gap-1.5"
          >
            <ArrowLeft size={14} />
            이전 단계
          </button>

          {step < 3 ? (
            <button
              onClick={() => setStep((step + 1) as any)}
              className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-extrabold flex items-center gap-1.5 shadow-md"
            >
              <span>다음 단계</span>
              <ArrowRight size={14} />
            </button>
          ) : (
            <button
              onClick={handleGenerateMap}
              className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-xl text-xs font-black flex items-center gap-2 shadow-lg scale-105 transition-all"
            >
              <Check size={16} />
              <span>나만의 2D 프로세스 맵 완결 생성!</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
