import React, { useState, useEffect, useRef } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ZAxis, ReferenceArea, ReferenceLine, LabelList
} from 'recharts';
import { format, parseISO, getTime } from 'date-fns';
import * as XLSX from 'xlsx';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import './index.css';

// ─────────────────────────────────────────────
// ErrorBoundary
// ─────────────────────────────────────────────
class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { hasError: false }; }
  static getDerivedStateFromError() { return { hasError: true }; }
  render() {
    if (this.state.hasError)
      return <div style={{padding:'2rem',color:'#ef4444',textAlign:'center',fontWeight:'bold'}}>차트 렌더링 오류 — 날짜·데이터값을 확인해 주세요.</div>;
    return this.props.children;
  }
}

// ─────────────────────────────────────────────
// STATIONS
// ─────────────────────────────────────────────
const STATIONS = [
  { id:'301',    km:0.0,  name:'301(병점)' },
  { id:'302',    km:0.6,  name:'302' },
  { id:'303',    km:1.2,  name:'303' },
  { id:'304',    km:1.8,  name:'304' },
  { id:'305',    km:2.4,  name:'305' },
  { id:'306',    km:3.0,  name:'306' },
  { id:'307',    km:3.6,  name:'307' },
  { id:'201',    km:4.2,  name:'201(동탄역)' },
  { id:'202',    km:4.8,  name:'202' },
  { id:'203',    km:5.4,  name:'203' },
  { id:'204',    km:6.0,  name:'204' },
  { id:'205',    km:6.6,  name:'205' },
  { id:'206',    km:7.2,  name:'206' },
  { id:'207',    km:7.8,  name:'207' },
  { id:'208',    km:8.4,  name:'208' },
  { id:'209',    km:9.0,  name:'209' },
  { id:'210',    km:9.6,  name:'210' },
  { id:'차량기지', km:10.2, name:'차량기지' },
  { id:'S01',    km:11.5, name:'S01(망포)' },
  { id:'S02',    km:12.1, name:'S02' },
  { id:'101',    km:12.7, name:'101' },
  { id:'102',    km:13.3, name:'102' },
  { id:'103',    km:13.9, name:'103' },
  { id:'104',    km:14.5, name:'104' },
  { id:'105',    km:15.1, name:'105' },
  { id:'106',    km:15.7, name:'106' },
  { id:'107',    km:16.3, name:'107' },
  { id:'108',    km:16.9, name:'108' },
  { id:'109',    km:17.5, name:'109' },
  { id:'110',    km:18.1, name:'110' },
  { id:'111',    km:18.7, name:'111' },
  { id:'112',    km:19.3, name:'112' },
  { id:'113',    km:19.9, name:'113' },
  { id:'114',    km:20.5, name:'114' },
];

const ZONE1_IDS = new Set(['301','302','303','304','305','306','307','201','202','203','204','205','206','207','208','209','210','차량기지']);

// ─────────────────────────────────────────────
// WBS 초기 구조 (독립 계층 트리)
// ─────────────────────────────────────────────
const INITIAL_WBS = [
  { id:'wbs-1',   code:'1',   name:'1공구',   parentId:null,    level:1, color:'#1e3a5f', visible:true },
  { id:'wbs-1-1', code:'1.1', name:'노반공사', parentId:'wbs-1', level:2, color:'#8B4513', visible:true },
  { id:'wbs-1-2', code:'1.2', name:'구조물공', parentId:'wbs-1', level:2, color:'#8884d8', visible:true },
  { id:'wbs-1-3', code:'1.3', name:'궤도공',   parentId:'wbs-1', level:2, color:'#2E8B57', visible:true },
  { id:'wbs-1-4', code:'1.4', name:'전기',     parentId:'wbs-1', level:2, color:'#FFD700', visible:true },
  { id:'wbs-1-5', code:'1.5', name:'신호',     parentId:'wbs-1', level:2, color:'#FF8C00', visible:true },
  { id:'wbs-1-6', code:'1.6', name:'통신',     parentId:'wbs-1', level:2, color:'#1E90FF', visible:true },
  { id:'wbs-2',   code:'2',   name:'2공구',   parentId:null,    level:1, color:'#0f4c75', visible:true },
  { id:'wbs-2-1', code:'2.1', name:'노반공사', parentId:'wbs-2', level:2, color:'#8B4513', visible:true },
  { id:'wbs-2-2', code:'2.2', name:'구조물공', parentId:'wbs-2', level:2, color:'#8884d8', visible:true },
  { id:'wbs-2-3', code:'2.3', name:'궤도공',   parentId:'wbs-2', level:2, color:'#2E8B57', visible:true },
  { id:'wbs-2-4', code:'2.4', name:'전기',     parentId:'wbs-2', level:2, color:'#FFD700', visible:true },
  { id:'wbs-2-5', code:'2.5', name:'신호',     parentId:'wbs-2', level:2, color:'#FF8C00', visible:true },
  { id:'wbs-2-6', code:'2.6', name:'통신',     parentId:'wbs-2', level:2, color:'#1E90FF', visible:true },
];

// ─────────────────────────────────────────────
// 액티비티 초기 데이터 (wbsId 귀속)
// ─────────────────────────────────────────────
const mkInitialActivities = () => {
  const lines = [
    { id:'n-1a', wbsId:'wbs-1-1', actName:'병점~307 노반공사',        type:'line',  startStation:'301', endStation:'307',     startDate:'2027-06-01', endDate:'2029-02-28', isCP:true, visible:true  },
    { id:'n-1b', wbsId:'wbs-1-1', actName:'동탄역~차량기지 노반공사', type:'line',  startStation:'201', endStation:'차량기지', startDate:'2027-09-01', endDate:'2029-08-31', visible:true             },
    { id:'g-1a', wbsId:'wbs-1-3', actName:'병점~307 궤도공',          type:'line',  startStation:'301', endStation:'307',     startDate:'2029-06-01', endDate:'2030-08-31', isCP:true, visible:true  },
    { id:'g-1b', wbsId:'wbs-1-3', actName:'동탄역~차량기지 궤도공',   type:'line',  startStation:'201', endStation:'차량기지', startDate:'2029-09-01', endDate:'2031-02-28', visible:true             },
    { id:'e-1',  wbsId:'wbs-1-4', actName:'1공구 전기공사',           type:'line',  startStation:'301', endStation:'차량기지', startDate:'2030-01-01', endDate:'2031-07-31', visible:true             },
    { id:'s-1',  wbsId:'wbs-1-5', actName:'1공구 신호공사',           type:'line',  startStation:'301', endStation:'차량기지', startDate:'2030-05-01', endDate:'2031-10-31', isCP:true, visible:true  },
    { id:'c-1',  wbsId:'wbs-1-6', actName:'1공구 통신공사',           type:'line',  startStation:'301', endStation:'차량기지', startDate:'2030-03-01', endDate:'2031-08-31', visible:true             },
    { id:'n-2',  wbsId:'wbs-2-1', actName:'2공구 노반공사',           type:'line',  startStation:'S01', endStation:'114',     startDate:'2027-06-01', endDate:'2029-05-31', visible:true             },
    { id:'g-2',  wbsId:'wbs-2-3', actName:'2공구 궤도공',             type:'line',  startStation:'S01', endStation:'114',     startDate:'2029-06-01', endDate:'2030-11-30', visible:true             },
    { id:'e-2',  wbsId:'wbs-2-4', actName:'2공구 전기공사',           type:'line',  startStation:'S01', endStation:'114',     startDate:'2030-01-01', endDate:'2031-06-30', visible:true             },
    { id:'s-2',  wbsId:'wbs-2-5', actName:'2공구 신호공사',           type:'line',  startStation:'S01', endStation:'114',     startDate:'2030-05-01', endDate:'2031-10-31', visible:true             },
    { id:'c-2',  wbsId:'wbs-2-6', actName:'2공구 통신공사',           type:'line',  startStation:'S01', endStation:'114',     startDate:'2030-03-01', endDate:'2031-08-31', visible:true             },
  ];
  const blocks = STATIONS.map((st, index) => {
    const base = new Date(2028, 0, 1);
    const startD = new Date(base); startD.setMonth(startD.getMonth() + index);
    const endD = new Date(startD); endD.setMonth(endD.getMonth() + 3); endD.setDate(endD.getDate() - 1);
    const pad = n => String(n).padStart(2, '0');
    return {
      id: `st-${st.id}`,
      wbsId: ZONE1_IDS.has(st.id) ? 'wbs-1-2' : 'wbs-2-2',
      actName: `${st.name} 구조물공`,
      type: 'block',
      targetStation: st.id,
      startDate: `${startD.getFullYear()}-${pad(startD.getMonth()+1)}-${pad(startD.getDate())}`,
      endDate:   `${endD.getFullYear()}-${pad(endD.getMonth()+1)}-${pad(endD.getDate())}`,
      isCP: false,
      visible: true
    };
  });
  return [...lines, ...blocks];
};

const INITIAL_DATA = mkInitialActivities();

// ─────────────────────────────────────────────
// 공법별 장비 프리셋
// ─────────────────────────────────────────────
const METHOD_PRESETS = {
  '일반개착식 궤도공법': [
    { type:'굴착기 0.6W', count:1 }, { type:'덤프트럭 15T', count:2 }, { type:'콘크리트 믹서트럭', count:1 }
  ],
  '교차로 저진동/무소음 궤도공법': [
    { type:'특수 무소음 다짐기', count:1 }, { type:'휠로더', count:1 }, { type:'크레인 25T', count:1 }
  ],
  '지하차도 인입 특수공법': [
    { type:'천공기 (Jumbo Drill)', count:1 }, { type:'숏크리트 머신', count:1 }, { type:'굴착기 0.8W', count:1 }
  ],
};

// ─────────────────────────────────────────────
// 유틸리티
// ─────────────────────────────────────────────
const getDescendantIds = (wbsId, allItems) => {
  const children = allItems.filter(i => i.parentId === wbsId);
  return [wbsId, ...children.flatMap(c => getDescendantIds(c.id, allItems))];
};

// ─────────────────────────────────────────────
// CustomTooltip
// ─────────────────────────────────────────────
const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload.tooltipInfo;
  if (!d) return null;
  return (
    <div style={{ backgroundColor:'#fff', padding:'10px', border:'1px solid #ccc', borderRadius:'6px', fontSize:'0.8rem', minWidth:'190px', boxShadow:'0 4px 12px rgba(0,0,0,0.1)' }}>
      <p style={{ margin:0, fontWeight:'bold', color: d.color }}>
        <span style={{ fontSize:'0.7rem', background: d.color+'20', border:`1px solid ${d.color}50`, padding:'1px 5px', borderRadius:'3px', marginRight:'6px' }}>{d.wbsCode}</span>
        {d.wbsName}
      </p>
      <p style={{ margin:'4px 0 0', color:'#475569', fontSize:'0.75rem' }}>{d.actName}</p>
      <hr style={{ margin:'6px 0', borderColor:'#f1f5f9' }} />
      {d.type === 'line'
        ? <p style={{ margin:'4px 0 0' }}>구간: {d.startStation} ~ {d.endStation}</p>
        : <p style={{ margin:'4px 0 0' }}>위치: {d.targetStation}</p>}
      <p style={{ margin:'4px 0 0' }}>기간: {d.startDate} ~ {d.endDate}</p>
      {d.workers && <p style={{ margin:'4px 0 0', color:'#475569' }}>🧑‍🔧 {d.workers}</p>}
      {d.equipment && <p style={{ margin:'4px 0 0', color:'#475569' }}>🚜 {d.equipment}</p>}
    </div>
  );
};

// ─────────────────────────────────────────────
// WBS 트리 노드 컴포넌트 (액티비티 포함 통합 렌더)
// ─────────────────────────────────────────────
const WbsTreeNode = ({
  item,
  allItems,
  activities,
  selectedWbsId,
  selectedActivityId,
  onSelectWbs,
  onSelectActivity,
  collapsedIds,
  onToggleCollapse,
  onToggleVisible,
  onToggleActivityVisible,
  onAddChild,
  onDelete,
  onRename,
  // ── 필터링용 프롭 ──
  filteredWbsIds,
  filteredActIds,
  searchActive
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState(item.name);
  const inputRef = useRef(null);

  // WBS 필터 목록에 속해 있지 않으면 렌더링 생략
  if (filteredWbsIds && !filteredWbsIds.has(item.id)) return null;

  const children = allItems.filter(i => i.parentId === item.id);
  // 검색어가 있을 때는 강제로 펼쳐서 보이도록 설정
  const isCollapsed = collapsedIds.has(item.id) && !searchActive;
  const isSelected = selectedWbsId === item.id;

  const descendantIds = getDescendantIds(item.id, allItems);
  const descendantItems = descendantIds.map(id => allItems.find(w => w.id === id)).filter(Boolean);
  const allVisible = descendantItems.every(w => w.visible);
  const someVisible = descendantItems.some(w => w.visible);
  
  // WBS 그룹 및 하위 액티비티 개수 계산
  const localActs = activities.filter(a => a.wbsId === item.id);
  const visibleLocalActs = localActs.filter(act => !filteredActIds || filteredActIds.has(act.id));
  const totalActCount = activities.filter(a => descendantIds.includes(a.wbsId)).length;

  const startEdit = (e) => { e.stopPropagation(); setEditName(item.name); setIsEditing(true); setTimeout(() => inputRef.current?.select(), 0); };
  const commitEdit = () => { setIsEditing(false); if (editName.trim()) onRename(item.id, editName.trim()); };

  // WBS 레벨별 들여쓰기 수치 계산
  const getIndent = (lvl) => {
    return lvl === 1 ? '6px' : (lvl === 2 ? '22px' : '38px');
  };

  const getActIndent = (lvl) => {
    return lvl === 1 ? '24px' : (lvl === 2 ? '40px' : '56px');
  };

  return (
    <div className="wbs-node-container" style={{ borderBottom: '1px solid #f1f5f9' }}>
      {/* WBS 항목 행 */}
      <div
        className={`wbs-node-row ${isSelected ? 'selected' : ''}`}
        style={{
          display:'flex', alignItems:'center', gap:'4px',
          padding:`4px 8px 4px ${getIndent(item.level)}`,
          background: isSelected ? '#eff6ff' : 'transparent',
          borderLeft: isSelected ? '3px solid #3b82f6' : '3px solid transparent',
          cursor:'pointer', userSelect:'none', transition:'background 0.1s',
        }}
        onClick={() => onSelectWbs(item.id)}
      >
        {/* 접기 화살표 */}
        <span
          style={{ width:'14px', fontSize:'0.65rem', color:'#64748b', textAlign:'center', flexShrink:0, cursor: (children.length > 0 || visibleLocalActs.length > 0) ? 'pointer' : 'default' }}
          onClick={e => { e.stopPropagation(); if (children.length > 0 || visibleLocalActs.length > 0) onToggleCollapse(item.id); }}
        >
          {(children.length > 0 || visibleLocalActs.length > 0) ? (isCollapsed ? '▶' : '▼') : '•'}
        </span>

        {/* 가시성 체크박스 */}
        <input
          type="checkbox"
          checked={allVisible}
          ref={el => { if (el) el.indeterminate = !allVisible && someVisible; }}
          onChange={() => onToggleVisible(item.id)}
          onClick={e => e.stopPropagation()}
          style={{ cursor:'pointer', flexShrink:0, width:'13px', height:'13px' }}
        />

        {/* 색상 칩 */}
        <span style={{ display:'inline-block', width:'10px', height:'10px', borderRadius:'3px', background:item.color, flexShrink:0, marginLeft:'1px' }} />

        {/* 이름 (더블클릭 편집) */}
        {isEditing ? (
          <input
            ref={inputRef}
            value={editName}
            onChange={e => setEditName(e.target.value)}
            onBlur={commitEdit}
            onKeyDown={e => { if (e.key === 'Enter') commitEdit(); if (e.key === 'Escape') setIsEditing(false); }}
            onClick={e => e.stopPropagation()}
            style={{ flex:1, fontSize:'0.75rem', border:'1px solid #3b82f6', borderRadius:'3px', padding:'1px 4px', outline:'none' }}
          />
        ) : (
          <span
            className="wbs-name-label"
            style={{ flex:1, fontSize:'0.78rem', fontWeight: item.level === 1 ? '700' : '500', color:'#1e293b', whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}
            title="더블클릭하여 이름 편집"
            onDoubleClick={startEdit}
          >
            {item.code} {item.name}
          </span>
        )}

        {/* 액티비티 개수 뱃지 */}
        {totalActCount > 0 && <span style={{ fontSize:'0.65rem', color:'#64748b', background:'#f1f5f9', padding:'1px 5px', borderRadius:'8px', flexShrink:0 }}>{totalActCount}</span>}

        {/* 자식 WBS 추가 버튼 */}
        {item.level < 3 && (
          <button title="하위 WBS 추가" onClick={e => { e.stopPropagation(); onAddChild(item.id); }}
            className="wbs-node-btn" style={{ color:'#10b981' }}>+</button>
        )}

        {/* 삭제 (루트가 아닐 때) */}
        {item.parentId !== null && (
          <button title="WBS 삭제" onClick={e => { e.stopPropagation(); onDelete(item.id); }}
            className="wbs-node-btn" style={{ color:'#ef4444' }}>✕</button>
        )}
      </div>

      {/* 펼쳐졌을 때: 자식 WBS 및 직속 액티비티 순차적 출력 */}
      {!isCollapsed && (
        <div className="wbs-node-children">
          {/* 1. 하위 WBS 노드들 렌더 */}
          {children.map(child => (
            <WbsTreeNode
              key={child.id}
              item={child}
              allItems={allItems}
              activities={activities}
              selectedWbsId={selectedWbsId}
              selectedActivityId={selectedActivityId}
              onSelectWbs={onSelectWbs}
              onSelectActivity={onSelectActivity}
              collapsedIds={collapsedIds}
              onToggleCollapse={onToggleCollapse}
              onToggleVisible={onToggleVisible}
              onToggleActivityVisible={onToggleActivityVisible}
              onAddChild={onAddChild}
              onDelete={onDelete}
              onRename={onRename}
              filteredWbsIds={filteredWbsIds}
              filteredActIds={filteredActIds}
              searchActive={searchActive}
            />
          ))}

          {/* 2. 현재 WBS 노드에 직접 속해 있는 액티비티 노드들 중 필터를 통과한 것만 렌더 */}
          {visibleLocalActs.map(act => {
            const isActSelected = selectedActivityId === act.id;
            return (
              <div
                key={act.id}
                className={`activity-node-row ${isActSelected ? 'selected' : ''}`}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: `3px 8px 3px ${getActIndent(item.level)}`,
                  background: isActSelected ? '#eff6ff' : 'transparent',
                  borderLeft: isActSelected ? '3px solid #2563eb' : '3px solid transparent',
                  cursor: 'pointer',
                  userSelect: 'none',
                  borderBottom: '1px dashed #f1f5f9'
                }}
                onClick={(e) => { e.stopPropagation(); onSelectActivity(act.id); }}
              >
                {/* 개별 액티비티 표시/숨김 체크박스 */}
                <input
                  type="checkbox"
                  checked={act.visible !== false}
                  onChange={(e) => { e.stopPropagation(); onToggleActivityVisible(act.id); }}
                  onClick={(e) => e.stopPropagation()}
                  style={{ cursor:'pointer', width:'12px', height:'12px', flexShrink:0 }}
                />
                
                {/* 액티비티 아이콘 */}
                <span style={{ fontSize:'0.75rem', flexShrink:0, color:'#64748b' }}>📄</span>
                
                {/* 액티비티 텍스트 */}
                <span
                  style={{
                    fontSize: '0.75rem',
                    color: act.visible !== false ? '#334155' : '#94a3b8',
                    textDecoration: act.visible !== false ? 'none' : 'line-through',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    flex: 1
                  }}
                >
                  {act.actName || '미지정 액티비티'}
                  <span style={{ fontSize:'0.65rem', color:'#94a3b8', marginLeft:'6px' }}>
                    {act.startDate && act.endDate ? `${act.startDate.slice(5)}~${act.endDate.slice(5)}` : ''}
                  </span>
                </span>

                {/* CP 마커 */}
                {act.isCP && (
                  <span style={{ fontSize:'0.6rem', color:'#ef4444', background:'#fee2e2', padding:'1px 3px', borderRadius:'3px', fontWeight:'700', scale:'0.9', flexShrink:0 }}>CP</span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

// ─────────────────────────────────────────────
// App
// ─────────────────────────────────────────────
function App() {
  const [isChartOnly, setIsChartOnly] = useState(false);

  // ── WBS 상태 ──
  const [wbsItems, setWbsItems] = useState(() => {
    const saved = localStorage.getItem('wbsItems_v1');
    if (saved) { try { return JSON.parse(saved); } catch(e) {} }
    return INITIAL_WBS;
  });

  // ── 액티비티 상태 ──
  const [activities, setActivities] = useState(() => {
    const saved = localStorage.getItem('timeChainageData_v18');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        // 하위 호환: visible 필드 누락 마이그레이션
        return parsed.map(a => a.visible === undefined ? { ...a, visible: true } : a);
      } catch(e) {}
    }
    return INITIAL_DATA;
  });

  // ── 대량 액티비티 관리를 위한 트리용 필터 상태 추가 ──
  const [searchQuery, setSearchQuery] = useState('');
  const [filterByZoom, setFilterByZoom] = useState(false);

  // WBS 일괄 접기/펼치기 핸들러
  const handleCollapseAll = () => {
    const allIds = wbsItems.map(w => w.id);
    setCollapsedWbs(new Set(allIds));
  };
  const handleExpandAll = () => {
    setCollapsedWbs(new Set());
  };

  // ── WBS 및 액티비티 UI 선택 상태 ──
  const [selectedWbsId, setSelectedWbsId] = useState(null);
  const [selectedActivityId, setSelectedActivityId] = useState(null);
  const [collapsedWbs, setCollapsedWbs] = useState(new Set());

  // ── 줌 상태 ──
  const [zoomStartStation, setZoomStartStation] = useState('301');
  const [zoomEndStation, setZoomEndStation] = useState('114');
  const [zoomStartDate, setZoomStartDate] = useState('2027-01-01');
  const [zoomEndDate, setZoomEndDate] = useState('2031-12-31');

  // ── 교차로 상태 ──
  const [intersections, setIntersections] = useState(() => {
    const saved = localStorage.getItem('timeChainageIntersections_v1');
    if (saved) { try { return JSON.parse(saved); } catch(e) {} }
    return [{ id:'int-1', fromStation:'301', toStation:'302', name:'벌말 교차로', km:0.3 }];
  });

  // ── 소구간 상세 상태 ──
  const [workZoneDetails, setWorkZoneDetails] = useState(() => {
    const saved = localStorage.getItem('timeChainageZoneDetails_v1');
    if (saved) { try { return JSON.parse(saved); } catch(e) {} }
    return {
      '301_벌말 교차로': {
        selectedMethod:'일반개착식 궤도공법',
        equipmentList:[{ type:'굴착기 0.6W', count:1 }, { type:'덤프트럭 15T', count:2 }],
        obstacles:[{ type:'지상', name:'한전 전주 2주', status:'이설협의중', memo:'교차로 모퉁이 이설 공간 확보 필요' }],
        memo:'출퇴근 시간 병목 우려로 야간 작업 위주 진행'
      }
    };
  });

  // ── 모달 상태 ──
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [detailStartStation, setDetailStartStation] = useState('301');
  const [detailEndStation, setDetailEndStation] = useState('302');
  const [activeSubZoneKey, setActiveSubZoneKey] = useState(null);
  const [newIntName, setNewIntName] = useState('');
  const [newIntKm, setNewIntKm] = useState('');
  const [editingMethod, setEditingMethod] = useState('일반개착식 궤도공법');
  const [editingEquipment, setEditingEquipment] = useState([]);
  const [editingObstacles, setEditingObstacles] = useState([]);
  const [editingMemo, setEditingMemo] = useState('');

  const fileInputRef = useRef(null);
  const chartContainerRef = useRef(null);

  // ── localStorage 영속화 ──
  useEffect(() => { localStorage.setItem('wbsItems_v1', JSON.stringify(wbsItems)); }, [wbsItems]);
  useEffect(() => { localStorage.setItem('timeChainageData_v18', JSON.stringify(activities)); }, [activities]);
  useEffect(() => { localStorage.setItem('timeChainageIntersections_v1', JSON.stringify(intersections)); }, [intersections]);
  useEffect(() => { localStorage.setItem('timeChainageZoneDetails_v1', JSON.stringify(workZoneDetails)); }, [workZoneDetails]);

  // ─────────────────────
  // WBS 핸들러
  // ─────────────────────
  const getWbsItem = (wbsId) => wbsItems.find(w => w.id === wbsId);

  const handleToggleWbsVisible = (wbsId) => {
    const ids = getDescendantIds(wbsId, wbsItems);
    const descendants = ids.map(id => wbsItems.find(w => w.id === id)).filter(Boolean);
    const allVis = descendants.every(w => w.visible);
    setWbsItems(prev => prev.map(w => ids.includes(w.id) ? { ...w, visible: !allVis } : w));
  };

  const handleToggleCollapse = (wbsId) => {
    setCollapsedWbs(prev => { const n = new Set(prev); n.has(wbsId) ? n.delete(wbsId) : n.add(wbsId); return n; });
  };

  const handleSelectWbs = (id) => {
    setSelectedWbsId(prev => prev === id ? null : id);
    setSelectedActivityId(null); // WBS 노드 선택 시 액티비티 선택 해제
  };

  const handleSelectActivity = (id) => {
    setSelectedActivityId(prev => prev === id ? null : id);
    setSelectedWbsId(null); // 액티비티 선택 시 WBS 노드 선택 해제
  };

  const handleAddWbsChild = (parentId) => {
    if (parentId === null) {
      const roots = wbsItems.filter(w => w.parentId === null);
      setWbsItems(prev => [...prev, { id:`wbs-${Date.now()}`, code:String(roots.length+1), name:'새 공구', parentId:null, level:1, color:'#94a3b8', visible:true }]);
    } else {
      const parent = wbsItems.find(w => w.id === parentId);
      if (!parent) return;
      const siblings = wbsItems.filter(w => w.parentId === parentId);
      setWbsItems(prev => [...prev, { id:`wbs-${Date.now()}`, code:`${parent.code}.${siblings.length+1}`, name:'새 항목', parentId, level:parent.level+1, color:'#94a3b8', visible:true }]);
    }
  };

  const handleDeleteWbs = (wbsId) => {
    const hasActs = activities.some(a => a.wbsId === wbsId);
    const hasChildren = wbsItems.some(w => w.parentId === wbsId);
    if (hasActs || hasChildren) { alert('연결된 액티비티 또는 하위 WBS 항목이 있습니다. 먼저 삭제해 주세요.'); return; }
    if (!window.confirm('이 WBS 항목을 삭제하시겠습니까?')) return;
    setWbsItems(prev => prev.filter(w => w.id !== wbsId));
    if (selectedWbsId === wbsId) setSelectedWbsId(null);
  };

  const handleRenameWbs = (wbsId, newName) => {
    setWbsItems(prev => prev.map(w => w.id === wbsId ? { ...w, name: newName } : w));
  };

  // ─────────────────────
  // 액티비티 핸들러
  // ─────────────────────
  const handleActivityChange = (id, field, value) => {
    setActivities(prev => prev.map(a => a.id === id ? { ...a, [field]: value } : a));
  };

  const handleToggleActivityVisible = (actId) => {
    setActivities(prev => prev.map(a => a.id === actId ? { ...a, visible: a.visible === false ? true : false } : a));
  };

  const handleAddActivity = () => {
    // 1. 현재 선택한 WBS 항목이 있으면 자식이 없는 리프인지 확인 후 귀속
    // 2. 선택된 게 없으면 첫 번째 리프 WBS 항목에 귀속
    const targetWbsId = (() => {
      if (selectedWbsId) {
        const isLeaf = !wbsItems.some(w => w.parentId === selectedWbsId);
        if (isLeaf) return selectedWbsId;
      }
      // 리프 WBS 찾기
      const leaf = wbsItems.find(w => !wbsItems.some(c => c.parentId === w.id));
      return leaf?.id || wbsItems[0]?.id || '';
    })();

    const newId = Date.now().toString();
    const newAct = {
      id: newId,
      wbsId: targetWbsId,
      actName: '새 액티비티',
      type: 'line',
      startStation: '301',
      endStation: '307',
      targetStation: '301',
      startDate: '2027-08-01',
      endDate: '2027-08-31',
      isCP: false,
      visible: true,
      workers: '',
      equipment: ''
    };

    setActivities(prev => [...prev, newAct]);
    setSelectedActivityId(newId); // 추가 즉시 상세정보 입력창 활성화
  };

  const handleDeleteActivity = (id) => {
    if (window.confirm('선택한 액티비티를 삭제하시겠습니까?')) {
      setActivities(prev => prev.filter(a => a.id !== id));
      if (selectedActivityId === id) setSelectedActivityId(null);
    }
  };

  // ─────────────────────
  // 줌/유틸
  // ─────────────────────
  const getKm   = (stId) => { const s = STATIONS.find(st => st.id === stId); return s ? s.km : 0; };
  const getName = (stId) => { const s = STATIONS.find(st => st.id === stId); return s ? s.name : ''; };

  const domainX = [getKm(zoomStartStation), getKm(zoomEndStation)].sort((a,b)=>a-b);
  const domainY = [getTime(parseISO(zoomStartDate)), getTime(parseISO(zoomEndDate))].sort((a,b)=>a-b);
  const formatYAxis = (t) => format(new Date(t), 'yy년 MM월');

  // ── 차트용 데이터 필터링 ──
  // 1. 소속 WBS 노드가 표시 상태(`visible: true`)이고, 
  // 2. 액티비티 자체도 표시 상태(`visible: true`)인 것만 차트에 그립니다.
  const chartDataSeries = activities
    .filter(act => {
      const wbs = getWbsItem(act.wbsId);
      return wbs && wbs.visible !== false && act.visible !== false;
    })
    .filter(act => act.startDate && act.endDate)
    .map(act => { const startT = getTime(parseISO(act.startDate)); const endT = getTime(parseISO(act.endDate)); return { ...act, startT, endT }; })
    .filter(act => !isNaN(act.startT) && !isNaN(act.endT))
    .map(act => {
      const { startT, endT } = act;
      const wbs = getWbsItem(act.wbsId);
      const name = wbs?.name || '미분류';
      const color = wbs?.color || '#cccccc';
      const wbsCode = wbs?.code || '';
      const wbsName = wbs?.name || '';
      const tooltipInfo = { ...act, name, color, wbsCode, wbsName };

      if (act.type === 'block') {
        const km = getKm(act.targetStation);
        return { ...act, km, name, color, startT, endT, data: [{ x:km, y:(startT+endT)/2, name, color, tooltipInfo }] };
      }
      const startKm = getKm(act.startStation), endKm = getKm(act.endStation);
      return {
        ...act, startKm, endKm, name, color, startT, endT,
        data: [
          { x:startKm, y:startT, name, color, tooltipInfo },
          { x:endKm,   y:endT,   name, color, tooltipInfo }
        ]
      };
    })
    .filter(s => {
      if (s.type === 'block') {
        const inX = s.km >= domainX[0] && s.km <= domainX[1];
        const inY = (s.startT >= domainY[0] && s.startT <= domainY[1]) || (s.endT >= domainY[0] && s.endT <= domainY[1]) || (s.startT <= domainY[0] && s.endT >= domainY[1]);
        return inX && inY;
      }
      const minX = Math.min(s.startKm, s.endKm), maxX = Math.max(s.startKm, s.endKm);
      const minY = Math.min(s.startT, s.endT), maxY = Math.max(s.startT, s.endT);
      return maxX >= domainX[0] && minX <= domainX[1] && maxY >= domainY[0] && minY <= domainY[1];
    });

  const xTicks = STATIONS.map(s => s.km);
  const formatXAxis = (v) => { const s = STATIONS.find(st => Math.abs(st.km - v) < 0.01); return s ? s.name : `${v}km`; };

  const paddingY = 86400000 * 30;
  const yTicks = [];
  let curD = new Date(domainY[0] - paddingY); curD.setDate(1); curD.setHours(0,0,0,0);
  const endDt = new Date(domainY[1] + paddingY);
  while (curD <= endDt) { yTicks.push(curD.getTime()); curD.setMonth(curD.getMonth()+1); }

  const BOUNDARY_1_2 = 10.85;

  // ── 대량 액티비티 관리를 위한 트리용 필터 연산 ──
  const filteredActIds = new Set();
  const filteredWbsIds = new Set();

  activities.forEach(act => {
    // 1. 줌 영역 필터 검증
    if (filterByZoom) {
      let overlapX = false;
      let overlapY = false;
      
      const startT = act.startDate ? getTime(parseISO(act.startDate)) : NaN;
      const endT = act.endDate ? getTime(parseISO(act.endDate)) : NaN;
      
      if (!isNaN(startT) && !isNaN(endT)) {
        const minY = Math.min(startT, endT);
        const maxY = Math.max(startT, endT);
        overlapY = maxY >= domainY[0] && minY <= domainY[1];
        
        if (act.type === 'block') {
          const km = getKm(act.targetStation);
          overlapX = km >= domainX[0] && km <= domainX[1];
        } else {
          const minX = Math.min(getKm(act.startStation), getKm(act.endStation));
          const maxX = Math.max(getKm(act.startStation), getKm(act.endStation));
          overlapX = maxX >= domainX[0] && minX <= domainX[1];
        }
      }
      
      if (!overlapX || !overlapY) return; // 범위를 벗어나면 필터링 제외
    }

    // 2. 검색어 검증
    const wbs = getWbsItem(act.wbsId);
    const wbsText = wbs ? `${wbs.code} ${wbs.name}` : '';
    const matchText = `${act.actName} ${wbsText}`.toLowerCase();
    
    if (searchQuery && !matchText.includes(searchQuery.toLowerCase())) {
      return; // 검색어 불일치 시 필터링 제외
    }

    // 통과한 액티비티
    filteredActIds.add(act.id);
    
    // 상위 WBS 체인 노출 등록
    let currentWbsId = act.wbsId;
    while (currentWbsId) {
      filteredWbsIds.add(currentWbsId);
      const curr = getWbsItem(currentWbsId);
      currentWbsId = curr ? curr.parentId : null;
    }
  });

  // WBS 명칭 자체가 검색어에 직접 매치되는 경우 예외 노출 처리
  if (searchQuery) {
    wbsItems.forEach(w => {
      if (`${w.code} ${w.name}`.toLowerCase().includes(searchQuery.toLowerCase())) {
        let currentWbsId = w.id;
        while (currentWbsId) {
          filteredWbsIds.add(currentWbsId);
          const curr = getWbsItem(currentWbsId);
          currentWbsId = curr ? curr.parentId : null;
        }
        // 자식들 노출
        const descendants = getDescendantIds(w.id, wbsItems);
        descendants.forEach(dId => filteredWbsIds.add(dId));
      }
    });
  } else if (!filterByZoom) {
    // 필터링 비활성화 상태에서는 전체 허용
    wbsItems.forEach(w => filteredWbsIds.add(w.id));
    activities.forEach(a => filteredActIds.add(a.id));
  } else {
    // 줌 필터만 켜진 상태에서, 자식 중 통과한 액티비티가 있거나 
    // 혹은 트리 아키텍처 상의 공구 노드는 구조 유지를 위해 강제 허용
    wbsItems.forEach(w => {
      const descendants = getDescendantIds(w.id, wbsItems);
      const hasVisibleAct = activities.some(a => descendants.includes(a.wbsId) && filteredActIds.has(a.id));
      if (hasVisibleAct) {
        filteredWbsIds.add(w.id);
      }
    });
    // 최상위 WBS(공구 레벨)는 항상 트리 기본 뼈대로 보여줌
    wbsItems.filter(w => w.parentId === null).forEach(w => filteredWbsIds.add(w.id));
  }

  // 선택된 액티비티 객체 찾기
  const activeActivity = activities.find(a => a.id === selectedActivityId);

  // 리프 WBS 항목 리스트 (액티비티 배정이 가능한 WBS 목록)
  const leafWbsItems = wbsItems.filter(w => !wbsItems.some(c => c.parentId === w.id));

  // ─────────────────────
  // 엑셀 입출력 핸들러
  // ─────────────────────
  const handleExcelUpload = (e) => {
    const file = e.target.files[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const wb = XLSX.read(evt.target.result, { type:'binary', cellDates:true });
        const rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
        const fmt = (v) => v instanceof Date ? v.toISOString().split('T')[0] : (typeof v === 'string' ? v : '2027-01-01');
        
        const newActs = rows.map((row, idx) => {
          const rawType = String(row['타입'] || row['type'] || 'line').trim();
          const type = (rawType === '정거장' || rawType === 'block') ? 'block' : 'line';
          const wbsCode = String(row['WBS코드'] || '');
          const matchedWbs = wbsItems.find(w => w.code === wbsCode);
          
          return {
            id: String(row['ID'] || row['id'] || `excel-${Date.now()}-${idx}`),
            wbsId: matchedWbs?.id || wbsItems.find(w => !wbsItems.some(c => c.parentId === w.id))?.id || '',
            actName: String(row['액티비티명'] || row['공종명'] || row['actName'] || '미분류'),
            type,
            startStation: String(row['시작위치'] || row['startStation'] || '301'),
            endStation:   String(row['종료위치'] || row['endStation'] || '307'),
            targetStation:String(row['위치(정거장)'] || row['targetStation'] || '301'),
            startDate: fmt(row['시작일'] || row['startDate']),
            endDate:   fmt(row['종료일'] || row['endDate']),
            workers:  row['인원'] || '',
            equipment: row['장비'] || '',
            isCP: !!(row['CP'] === 'Y' || row['CP'] === 'y' || row['CP'] === true),
            visible: true
          };
        });
        if (newActs.length > 0) { setActivities(newActs); alert(`${newActs.length}개 액티비티를 업로드했습니다.`); }
      } catch(err) { console.error(err); alert('엑셀 파싱 중 오류가 발생했습니다.'); }
    };
    reader.readAsBinaryString(file);
  };

  const handleExcelDownload = () => {
    const data = activities.map(act => {
      const wbs = getWbsItem(act.wbsId);
      return {
        'WBS코드': wbs?.code || '',
        'WBS명': wbs?.name || '',
        'ID': act.id,
        '액티비티명': act.actName || '',
        '타입': act.type === 'block' ? '정거장' : '본선',
        '시작위치': act.type === 'line' ? act.startStation : '',
        '종료위치': act.type === 'line' ? act.endStation : '',
        '위치(정거장)': act.type === 'block' ? act.targetStation : '',
        '시작일': act.startDate,
        '종료일': act.endDate,
        '인원': act.workers || '',
        '장비': act.equipment || '',
        'CP': act.isCP ? 'Y' : 'N'
      };
    });
    const ws = XLSX.utils.json_to_sheet(data);
    const wbk = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wbk, ws, '공정표데이터');
    XLSX.writeFile(wbk, '동탄트램_통합선형공정표_데이터.xlsx');
  };

  const handleExcelTemplateDownload = () => {
    const tpl = [
      { 'WBS코드':'1.1','WBS명':'노반공사','ID':'task-01','액티비티명':'병점~307 노반공사','타입':'본선','시작위치':'301','종료위치':'307','위치(정거장)':'','시작일':'2027-06-01','종료일':'2029-02-28','인원':'작업원 10명','장비':'백호 2대','CP':'Y' },
      { 'WBS코드':'1.2','WBS명':'구조물공','ID':'task-02','액티비티명':'301역 구조물공','타입':'정거장','시작위치':'','종료위치':'','위치(정거장)':'301','시작일':'2028-01-01','종료일':'2028-03-31','인원':'철근공 5명','장비':'크레인 1대','CP':'N' },
    ];
    const ws = XLSX.utils.json_to_sheet(tpl);
    const wbk = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wbk, ws, '공정표_업로드양식');
    XLSX.writeFile(wbk, '동탄트램_선형공정표_업로드양식.xlsx');
  };

  const exportToPNG = () => {
    if (!chartContainerRef.current) return;
    html2canvas(chartContainerRef.current, { backgroundColor:'#ffffff', scale:2 }).then(canvas => {
      const a = document.createElement('a');
      a.download = `동탄트램_선형공정표_${format(new Date(),'yyyyMMdd')}.png`;
      a.href = canvas.toDataURL('image/png'); a.click();
    });
  };

  const exportToPDF = () => {
    if (!chartContainerRef.current) return;
    html2canvas(chartContainerRef.current, { backgroundColor:'#ffffff', scale:2 }).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('l','mm','a4');
      const w = 297, h = (canvas.height * w) / canvas.width;
      pdf.addImage(imgData,'PNG',0,0,w,h);
      pdf.save(`동탄트램_선형공정표_${format(new Date(),'yyyyMMdd')}.pdf`);
    });
  };

  const handleQuickDateFilter = (s,e) => { setZoomStartDate(s); setZoomEndDate(e); };
  const resetZoom = () => { setZoomStartStation('301'); setZoomEndStation('114'); setZoomStartDate('2027-01-01'); setZoomEndDate('2031-12-31'); };

  // ─────────────────────
  // 소구간 분석
  // ─────────────────────
  const getSubSegments = (startId, endId) => {
    const startK = getKm(startId), endK = getKm(endId);
    const [minK, maxK] = [startK,endK].sort((a,b)=>a-b);
    const pts = [
      { name:getName(startId), km:minK },
      ...intersections.filter(i=>i.km>minK&&i.km<maxK).sort((a,b)=>a.km-b.km).map(i=>({ name:i.name, km:i.km })),
      { name:getName(endId), km:maxK },
    ];
    return pts.slice(0,-1).map((p,i) => ({ key:`${p.name}_${pts[i+1].name}`, fromName:p.name, toName:pts[i+1].name, fromKm:p.km, toKm:pts[i+1].km, lengthM:Math.round((pts[i+1].km-p.km)*1000) }));
  };

  const handleSelectSubZone = (key) => {
    setActiveSubZoneKey(key);
    const d = workZoneDetails[key] || { selectedMethod:'일반개착식 궤도공법', equipmentList:METHOD_PRESETS['일반개착식 궤도공법'], obstacles:[], memo:'' };
    setEditingMethod(d.selectedMethod); setEditingEquipment(d.equipmentList||[]); setEditingObstacles(d.obstacles||[]); setEditingMemo(d.memo||'');
  };

  const handleMethodPresetChange = (m) => { setEditingMethod(m); setEditingEquipment((METHOD_PRESETS[m]||[]).map(p=>({...p}))); };
  const handleEquipCountChange = (i,v) => { const u=[...editingEquipment]; u[i].count=Math.max(0,parseInt(v)||0); setEditingEquipment(u); };
  const handleRemoveEquip = (i) => setEditingEquipment(editingEquipment.filter((_,x)=>x!==i));
  const handleAddEquip = () => setEditingEquipment([...editingEquipment,{type:'신규 장비',count:1}]);
  const handleObstacleChange = (i,f,v) => { const u=[...editingObstacles]; u[i][f]=v; setEditingObstacles(u); };
  const handleAddObstacle = () => setEditingObstacles([...editingObstacles,{type:'지상',name:'신규 지장물',status:'조사중',memo:''}]);
  const handleRemoveObstacle = (i) => setEditingObstacles(editingObstacles.filter((_,x)=>x!==i));
  const handleSaveSubZone = () => {
    if (!activeSubZoneKey) return;
    setWorkZoneDetails({ ...workZoneDetails, [activeSubZoneKey]:{ selectedMethod:editingMethod, equipmentList:editingEquipment, obstacles:editingObstacles, memo:editingMemo } });
    alert('저장되었습니다.');
  };

  const handleAddIntersection = () => {
    if (!newIntName||!newIntKm) { alert('교차로 명칭과 KM을 입력해 주세요.'); return; }
    const km = parseFloat(newIntKm);
    const [minK,maxK] = [getKm(detailStartStation),getKm(detailEndStation)].sort((a,b)=>a-b);
    if (isNaN(km)||km<=minK||km>=maxK) { alert(`KM은 ${minK.toFixed(1)}~${maxK.toFixed(1)} 사이여야 합니다.`); return; }
    setIntersections([...intersections,{id:`int-${Date.now()}`,fromStation:detailStartStation,toStation:detailEndStation,name:newIntName,km}]);
    setNewIntName(''); setNewIntKm('');
  };

  const handleRemoveIntersection = (id) => {
    if (confirm('이 교차로를 삭제하시겠습니까?')) { setIntersections(intersections.filter(i=>i.id!==id)); setActiveSubZoneKey(null); }
  };

  const rootWbsItems = wbsItems.filter(w => w.parentId === null);

  // ─────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────
  return (
    <div className="app-container">

      {/* ═══════════════ SIDEBAR ═══════════════ */}
      {!isChartOnly && (
        <div className="sidebar" style={{ width:'480px', flexShrink:0, display:'flex', flexDirection:'column', borderRight:'1px solid #cbd5e1', background:'#ffffff' }}>

          {/* 헤더 */}
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:'0.5rem', flexShrink:0 }}>
            <div>
              <h1 style={{ margin:0, fontSize:'1.25rem', fontWeight:'bold', color: '#1e3a5f' }}>Time-Chainage MVP</h1>
              <p style={{ fontSize:'0.72rem', color:'#64748b', margin:'2px 0 0' }}>동탄트램 1·2공구 통합 선형공정표</p>
            </div>
            <button style={{ padding:'0.3rem 0.6rem', background:'#475569', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'0.75rem' }} onClick={() => setIsChartOnly(true)}>🔍 크게 보기</button>
          </div>

          {/* WBS & 액티비티 계층 트리 패널 */}
          <div style={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column', background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '8px', overflow: 'hidden', marginBottom: '0.5rem' }}>
            <div style={{ background:'#1e293b', padding:'0.5rem 0.75rem', display:'flex', justifyContent:'space-between', alignItems:'center', flexShrink:0 }}>
              <span style={{ color:'#f1f5f9', fontWeight:'bold', fontSize:'0.8rem' }}>🗂️ WBS & 액티비티 트리</span>
              <div style={{ display:'flex', gap:'4px' }}>
                <button onClick={() => setWbsItems(prev => prev.map(w=>({...w,visible:true})))} style={{ fontSize:'0.65rem', padding:'2px 6px', background:'#3b82f6', color:'white', border:'none', borderRadius:'3px', cursor:'pointer' }}>전체표시</button>
                <button onClick={() => handleAddWbsChild(null)} style={{ fontSize:'0.65rem', padding:'2px 6px', background:'#10b981', color:'white', border:'none', borderRadius:'3px', cursor:'pointer' }}>+ 공구</button>
                <button onClick={handleAddActivity} style={{ fontSize:'0.65rem', padding:'2px 6px', background:'#f97316', color:'white', border:'none', borderRadius:'3px', cursor:'pointer', fontWeight:'bold' }}>+ 액티비티</button>
              </div>
            </div>

            {/* 🔍 트리 전용 조작 컨트롤러 (검색, 접기, 줌연동) */}
            <div style={{ display:'flex', flexDirection:'column', gap:'5px', padding:'6px 8px', background:'#f1f5f9', borderBottom:'1px solid #cbd5e1', flexShrink:0, fontSize:'0.72rem' }}>
              <div style={{ display:'flex', gap:'6px' }}>
                <input
                  type="text"
                  placeholder="WBS 또는 액티비티 검색..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  style={{ flex:1, padding:'3px 6px', border:'1px solid #cbd5e1', borderRadius:'4px', outline:'none', fontSize:'0.72rem' }}
                />
                {searchQuery && (
                  <button onClick={() => setSearchQuery('')} style={{ background:'#94a3b8', border:'none', color:'white', borderRadius:'3px', padding:'0 6px', cursor:'pointer' }}>✕</button>
                )}
              </div>
              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                <label style={{ display:'flex', alignItems:'center', gap:'3px', cursor:'pointer', fontWeight:'bold', color:'#475569' }}>
                  <input
                    type="checkbox"
                    checked={filterByZoom}
                    onChange={e => setFilterByZoom(e.target.checked)}
                    style={{ width:'12px', height:'12px', cursor:'pointer' }}
                  />
                  🔍 현재 줌 영역만 보기
                </label>
                <div style={{ display:'flex', gap:'4px' }}>
                  <button onClick={handleCollapseAll} style={{ padding:'2px 6px', background:'#ffffff', border:'1px solid #cbd5e1', borderRadius:'3px', cursor:'pointer', fontSize:'0.65rem', fontWeight:'500' }}>모두접기</button>
                  <button onClick={handleExpandAll} style={{ padding:'2px 6px', background:'#ffffff', border:'1px solid #cbd5e1', borderRadius:'3px', cursor:'pointer', fontSize:'0.65rem', fontWeight:'500' }}>모두펴기</button>
                </div>
              </div>
            </div>

            {/* 트리 스크롤 바디 */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '4px 0' }}>
              {rootWbsItems.map(item => (
                <WbsTreeNode
                  key={item.id}
                  item={item}
                  allItems={wbsItems}
                  activities={activities}
                  selectedWbsId={selectedWbsId}
                  selectedActivityId={selectedActivityId}
                  onSelectWbs={handleSelectWbs}
                  onSelectActivity={handleSelectActivity}
                  collapsedIds={collapsedWbs}
                  onToggleCollapse={handleToggleCollapse}
                  onToggleVisible={handleToggleWbsVisible}
                  onToggleActivityVisible={handleToggleActivityVisible}
                  onAddChild={handleAddWbsChild}
                  onDelete={handleDeleteWbs}
                  onRename={handleRenameWbs}
                  filteredWbsIds={filteredWbsIds}
                  filteredActIds={filteredActIds}
                  searchActive={!!searchQuery}
                />
              ))}
            </div>
          </div>

          {/* 엑셀 파일 패널 */}
          <div style={{ padding:'0.4rem 0.6rem', background:'#f8fafc', border:'1px solid #cbd5e1', borderRadius:'6px', marginBottom:'0.5rem', flexShrink:0, display:'flex', gap:'5px', alignItems:'center' }}>
            <span style={{ fontSize:'0.75rem', fontWeight:'bold', color:'#475569', flexShrink:0 }}>📊 엑셀:</span>
            <button onClick={() => fileInputRef.current?.click()} style={{ flex:1, padding:'0.28rem', fontSize:'0.7rem', background:'#0284c7', color:'white', border:'none', borderRadius:'4px', cursor:'pointer' }}>📤 가져오기</button>
            <button onClick={handleExcelDownload} style={{ flex:1, padding:'0.28rem', fontSize:'0.7rem', background:'#16a34a', color:'white', border:'none', borderRadius:'4px', cursor:'pointer' }}>📥 내보내기</button>
            <button onClick={handleExcelTemplateDownload} style={{ flex:1, padding:'0.28rem', fontSize:'0.7rem', background:'#64748b', color:'white', border:'none', borderRadius:'4px', cursor:'pointer' }}>📋 양식</button>
            <input type="file" ref={fileInputRef} onChange={handleExcelUpload} accept=".xlsx,.xls" style={{ display:'none' }} />
          </div>

          {/* 선택 액티비티 상세 편집 패널 */}
          <div style={{ height:'260px', border:'1px solid #cbd5e1', borderRadius:'8px', background:'#ffffff', padding:'0.6rem', display:'flex', flexDirection:'column', flexShrink:0, overflowY:'auto' }}>
            {activeActivity ? (
              <div className="activity-editor-form" style={{ display:'flex', flexDirection:'column', gap:'6px', fontSize:'0.7rem' }}>
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', borderBottom:'1px solid #e2e8f0', paddingBottom:'4px', marginBottom:'4px' }}>
                  <span style={{ fontWeight:'bold', color:'#1e3a5f', fontSize:'0.75rem' }}>🛠️ 액티비티 상세 편집</span>
                  <button onClick={() => handleDeleteActivity(activeActivity.id)} style={{ padding:'2px 8px', background:'#ef4444', color:'white', border:'none', borderRadius:'3px', cursor:'pointer', fontSize:'0.65rem' }}>삭제</button>
                </div>

                <div style={{ display:'flex', gap:'5px' }}>
                  <div style={{ flex:1 }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>소속 WBS</label>
                    <select
                      value={activeActivity.wbsId || ''}
                      onChange={e => handleActivityChange(activeActivity.id, 'wbsId', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    >
                      {leafWbsItems.map(w => <option key={w.id} value={w.id}>{w.code} {w.name}</option>)}
                    </select>
                  </div>
                  <div style={{ flex:1.5 }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>액티비티명</label>
                    <input
                      type="text"
                      value={activeActivity.actName || ''}
                      onChange={e => handleActivityChange(activeActivity.id, 'actName', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    />
                  </div>
                </div>

                <div style={{ display:'flex', gap:'5px' }}>
                  <div style={{ width:'30%' }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>작업 타입</label>
                    <select
                      value={activeActivity.type || 'line'}
                      onChange={e => handleActivityChange(activeActivity.id, 'type', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    >
                      <option value="line">본선(구간)</option>
                      <option value="block">정거장(지점)</option>
                    </select>
                  </div>
                  <div style={{ flex:1 }}>
                    {activeActivity.type === 'block' ? (
                      <div>
                        <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>위치 (정거장)</label>
                        <select
                          value={activeActivity.targetStation || '301'}
                          onChange={e => handleActivityChange(activeActivity.id, 'targetStation', e.target.value)}
                          style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                        >
                          {STATIONS.map(st => <option key={st.id} value={st.id}>{st.name}</option>)}
                        </select>
                      </div>
                    ) : (
                      <div>
                        <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>위치 구간 (시작역 ~ 종료역)</label>
                        <div style={{ display:'flex', gap:'3px' }}>
                          <select
                            value={activeActivity.startStation || '301'}
                            onChange={e => handleActivityChange(activeActivity.id, 'startStation', e.target.value)}
                            style={{ flex:1, padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                          >
                            {STATIONS.map(st => <option key={st.id} value={st.id}>{st.id} ({st.name.replace(/[^0-9가-힣]/g,'')})</option>)}
                          </select>
                          <span style={{ alignSelf:'center' }}>~</span>
                          <select
                            value={activeActivity.endStation || '307'}
                            onChange={e => handleActivityChange(activeActivity.id, 'endStation', e.target.value)}
                            style={{ flex:1, padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                          >
                            {STATIONS.map(st => <option key={st.id} value={st.id}>{st.id} ({st.name.replace(/[^0-9가-힣]/g,'')})</option>)}
                          </select>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div style={{ display:'flex', gap:'5px' }}>
                  <div style={{ flex:1 }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>시작일</label>
                    <input
                      type="date"
                      value={activeActivity.startDate || ''}
                      onChange={e => handleActivityChange(activeActivity.id, 'startDate', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    />
                  </div>
                  <div style={{ flex:1 }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>종료일</label>
                    <input
                      type="date"
                      value={activeActivity.endDate || ''}
                      onChange={e => handleActivityChange(activeActivity.id, 'endDate', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    />
                  </div>
                  <div style={{ width:'50px', display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center' }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>CP</label>
                    <input
                      type="checkbox"
                      checked={activeActivity.isCP || false}
                      onChange={e => handleActivityChange(activeActivity.id, 'isCP', e.target.checked)}
                      style={{ width:'14px', height:'14px', cursor:'pointer' }}
                    />
                  </div>
                </div>

                <div style={{ display:'flex', gap:'5px' }}>
                  <div style={{ flex:1 }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>🚜 투입 장비</label>
                    <input
                      type="text"
                      placeholder="예: 굴착기 2대, 덤프 1대"
                      value={activeActivity.equipment || ''}
                      onChange={e => handleActivityChange(activeActivity.id, 'equipment', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    />
                  </div>
                  <div style={{ flex:1 }}>
                    <label style={{ fontWeight:'bold', display:'block', marginBottom:'2px', color:'#475569' }}>🧑‍🔧 투입 인원</label>
                    <input
                      type="text"
                      placeholder="예: 작업자 5명"
                      value={activeActivity.workers || ''}
                      onChange={e => handleActivityChange(activeActivity.id, 'workers', e.target.value)}
                      style={{ width:'100%', padding:'2px', fontSize:'0.7rem', border:'1px solid #cbd5e1', borderRadius:'3px' }}
                    />
                  </div>
                </div>

              </div>
            ) : (
              <div style={{ display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', height:'100%', color:'#94a3b8', fontSize:'0.72rem', textAlign:'center', gap:'5px' }}>
                <span>💡 편집할 액티비티를 선택하세요.</span>
                <span>WBS 트리를 확장하고, 📄 액티비티 항목을 클릭하면 이곳에서 바로 수정할 수 있습니다.</span>
              </div>
            )}
          </div>

        </div>
      )}

      {/* ═══════════════ MAIN CHART ═══════════════ */}
      <div className="main-content" style={{ position:'relative', display:'flex', flexDirection:'column', flex:1 }}>

        {/* 컨트롤 패널 */}
        <div className="control-bar" style={{ background:'#f8fafc', padding:'0.75rem 1rem', border:'1px solid #cbd5e1', borderRadius:'8px', marginBottom:'0.75rem', display:'flex', flexDirection:'column', gap:'0.5rem', fontSize:'0.8rem', boxShadow:'0 2px 4px rgba(0,0,0,0.02)' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap:'10px' }}>
            <span style={{ fontWeight:'bold', fontSize:'0.9rem', color:'#1e293b' }}>⚙️ 차트 인터랙션 & 뷰어 도구</span>
            <div style={{ display:'flex', gap:'6px' }}>
              <button onClick={exportToPNG} style={{ padding:'0.4rem 0.8rem', background:'#4f46e5', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontWeight:'bold', fontSize:'0.75rem' }}>📸 PNG 저장</button>
              <button onClick={exportToPDF} style={{ padding:'0.4rem 0.8rem', background:'#dc2626', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontWeight:'bold', fontSize:'0.75rem' }}>📄 PDF 저장</button>
              <button onClick={() => setShowDetailModal(true)} style={{ padding:'0.4rem 0.8rem', background:'#0284c7', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontWeight:'bold', fontSize:'0.75rem' }}>🔍 현장 여건 & 지장물 분석</button>
              <button onClick={resetZoom} style={{ padding:'0.4rem 0.8rem', background:'#64748b', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontWeight:'bold', fontSize:'0.75rem' }}>🔄 줌 초기화</button>
              {isChartOnly && <button onClick={() => setIsChartOnly(false)} style={{ padding:'0.4rem 0.8rem', background:'#3b82f6', color:'white', border:'none', borderRadius:'4px', cursor:'pointer', fontWeight:'bold', fontSize:'0.75rem' }}>↩️ 돌아가기</button>}
            </div>
          </div>
          <div style={{ display:'flex', gap:'15px', flexWrap:'wrap', fontSize:'0.75rem' }}>
            <div style={{ display:'flex', alignItems:'center', gap:'6px' }}>
              <span style={{ fontWeight:'bold', color:'#475569' }}>📍 구간 확대:</span>
              <select value={zoomStartStation} onChange={e=>setZoomStartStation(e.target.value)} style={{ padding:'0.2rem', borderRadius:'4px', border:'1px solid #cbd5e1' }}>
                {STATIONS.map(st=><option key={`zs-${st.id}`} value={st.id}>{st.name}</option>)}
              </select>
              <span>~</span>
              <select value={zoomEndStation} onChange={e=>setZoomEndStation(e.target.value)} style={{ padding:'0.2rem', borderRadius:'4px', border:'1px solid #cbd5e1' }}>
                {STATIONS.map(st=><option key={`ze-${st.id}`} value={st.id}>{st.name}</option>)}
              </select>
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:'6px' }}>
              <span style={{ fontWeight:'bold', color:'#475569' }}>📅 기간 확대:</span>
              <input type="date" value={zoomStartDate} onChange={e=>setZoomStartDate(e.target.value)} style={{ padding:'0.15rem 0.3rem', borderRadius:'4px', border:'1px solid #cbd5e1' }} />
              <span>~</span>
              <input type="date" value={zoomEndDate} onChange={e=>setZoomEndDate(e.target.value)} style={{ padding:'0.15rem 0.3rem', borderRadius:'4px', border:'1px solid #cbd5e1' }} />
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:'4px' }}>
              <span style={{ fontWeight:'bold', color:'#475569' }}>⚡ 퀵 기간:</span>
              {[['전체','2027-01-01','2031-12-31'],["'27~'28년",'2027-01-01','2028-12-31'],["'29~'30년",'2029-01-01','2030-12-31'],["'31~'32년",'2031-01-01','2032-12-31']].map(([label,s,e])=>(
                <button key={label} onClick={()=>handleQuickDateFilter(s,e)} style={{ padding:'0.2rem 0.4rem', background:'#e2e8f0', border:'none', borderRadius:'4px', cursor:'pointer' }}>{label}</button>
              ))}
            </div>
          </div>
        </div>

        {/* 차트 */}
        <div className="chart-container" ref={chartContainerRef} style={{ flex:1, display:'flex', flexDirection:'column', padding:'1.2rem', background:'#ffffff' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'1rem', flexWrap:'wrap', gap:'10px' }}>
            <div className="chart-title" style={{ fontSize:'1.5rem', fontWeight:'bold', margin:0, color:'#0f172a' }}>동탄트램 1·2공구 전체 노선 통합 선형 공정표</div>
            <div style={{ background:'#f8fafc', padding:'6px 12px', border:'1px solid #cbd5e1', borderRadius:'8px', display:'flex', gap:'8px', flexWrap:'wrap' }}>
              {wbsItems.filter(w => !wbsItems.some(c=>c.parentId===w.id)).map(w=>(
                <div key={w.id} style={{ display:'flex', alignItems:'center', gap:'4px' }}>
                  <div style={{ width:'11px', height:'11px', background:w.color, borderRadius:'3px' }}></div>
                  <span style={{ fontWeight:'700', color:'#475569', fontSize:'0.75rem' }}>{w.code} {w.name}</span>
                </div>
              ))}
            </div>
          </div>

          <div style={{ flex:1, width:'100%', minHeight:0 }}>
            <ResponsiveContainer width="100%" height="100%">
              <ErrorBoundary>
                <ScatterChart margin={{ top:20, right:30, bottom:20, left:10 }}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                  {yTicks.filter(t=>t>=domainY[0]&&t<=domainY[1]).map(t=><ReferenceLine key={`hl-${t}`} y={t} stroke="#cbd5e1" strokeDasharray="3 3" opacity={0.6} />)}
                  <XAxis type="number" dataKey="x" domain={domainX} ticks={xTicks.filter(k=>k>=domainX[0]&&k<=domainX[1])} tickFormatter={formatXAxis} interval={0} angle={-90} textAnchor="end" height={130} tick={{ fontSize:15, fontWeight:'bold', fill:'#0f172a' }} />
                  <YAxis type="number" dataKey="y" domain={domainY} ticks={yTicks.filter(t=>t>=domainY[0]&&t<=domainY[1])} tickFormatter={formatYAxis} reversed={true} tick={{ fontSize:13, fontWeight:'bold', fill:'#475569' }} />
                  <ZAxis range={[40,40]} />
                  <Tooltip content={<CustomTooltip />} />
                  {STATIONS.filter(st=>st.km>=domainX[0]&&st.km<=domainX[1]).map(st=><ReferenceLine key={`vl-${st.id}`} x={st.km} stroke="#e2e8f0" strokeDasharray="2 4" />)}
                  {BOUNDARY_1_2>=domainX[0]&&BOUNDARY_1_2<=domainX[1]&&(
                    <ReferenceLine x={BOUNDARY_1_2} stroke="#ff4500" strokeWidth={3} strokeDasharray="5 5" label={{ value:"1공구 | 2공구 경계", position:'insideTopLeft', fill:'#ff4500', fontSize:18, fontWeight:'bold', dy:10 }} />
                  )}
                  {chartDataSeries.filter(a=>a.type==='block').map(act=>(
                    <ReferenceArea key={`area-${act.id}`} x1={act.km-0.15} x2={act.km+0.15} y1={act.startT} y2={act.endT} fill={act.color} fillOpacity={act.isCP?0.6:0.4} stroke={act.isCP?'red':act.color} strokeWidth={act.isCP?2:1} strokeDasharray={act.isCP?"3 3":"0"} />
                  ))}
                  {chartDataSeries.filter(s=>s.type==='line'&&s.isCP).map(s=>(
                    <Scatter key={`cp-${s.id}`} data={s.data} fill="transparent" line={{ stroke:'red', strokeWidth:12, strokeOpacity:0.3 }} shape={()=>null} />
                  ))}
                  {chartDataSeries.filter(s=>s.type==='line').map(s=>(
                    <Scatter key={s.id} name={s.actName} data={s.data} fill={s.color} line={{ stroke:s.color, strokeWidth:4 }} shape="circle" />
                  ))}
                  {chartDataSeries.filter(s=>s.type==='line'&&s.data.length===2).map(s=>{
                    const midX=(s.data[0].x+s.data[1].x)/2, midY=(s.data[0].y+s.data[1].y)/2;
                    return (
                      <Scatter key={`lbl-${s.id}`} data={[{x:midX,y:midY,name:s.actName}]} fill="transparent" shape="circle">
                        <LabelList dataKey="name" position="top" dy={-10} fill="#000" fontSize={20} fontWeight="900" stroke="rgba(255,255,255,1)" strokeWidth={6} paintOrder="stroke" />
                      </Scatter>
                    );
                  })}
                  {chartDataSeries.filter(s=>s.type==='block').map(s=>(
                    <Scatter key={`hid-${s.id}`} name={s.actName} data={s.data} fill="transparent" shape="circle" />
                  ))}
                </ScatterChart>
              </ErrorBoundary>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* ═══════════════ 소구간 분석 모달 ═══════════════ */}
      {showDetailModal && (
        <div className="modal-overlay">
          <div className="modal-window">
            <div className="modal-header">
              <span className="modal-title">🔍 정거장 간 소구간(교차로 기준) 분석 및 현장 조사 데이터 빌더</span>
              <button className="modal-close-btn" onClick={()=>{setShowDetailModal(false);setActiveSubZoneKey(null);}}>✕ 닫기</button>
            </div>
            <div className="modal-toolbar">
              <div className="toolbar-section">
                <span className="section-label">📍 대상 정거장 구간:</span>
                <select value={detailStartStation} onChange={e=>{setDetailStartStation(e.target.value);setActiveSubZoneKey(null);}} className="toolbar-select">
                  {STATIONS.map(st=><option key={`ds-${st.id}`} value={st.id}>{st.name}</option>)}
                </select>
                <span>~</span>
                <select value={detailEndStation} onChange={e=>{setDetailEndStation(e.target.value);setActiveSubZoneKey(null);}} className="toolbar-select">
                  {STATIONS.map(st=><option key={`de-${st.id}`} value={st.id}>{st.name}</option>)}
                </select>
              </div>
              <div className="toolbar-section divider-left">
                <span className="section-label">➕ 신규 교차로 등록:</span>
                <input type="text" placeholder="교차로 명칭" value={newIntName} onChange={e=>setNewIntName(e.target.value)} className="toolbar-input" />
                <input type="number" step="0.01" placeholder="기점 KM" value={newIntKm} onChange={e=>setNewIntKm(e.target.value)} className="toolbar-input-km" />
                <button onClick={handleAddIntersection} className="btn-add-int">+ 교차로 등록</button>
              </div>
            </div>
            <div className="modal-body">
              <div className="modal-body-left">
                <span className="column-title">1. 정거장 간 노선 및 교차로 분할 모식도</span>
                <div className="track-layout-container">
                  <div className="track-line-base"></div>
                  <div className="track-node-pin station-pin" style={{ left:'5%' }}>
                    <div className="pin-circle"></div>
                    <span className="pin-label">{getName(detailStartStation)}</span>
                    <span className="pin-km">{getKm(detailStartStation).toFixed(2)}km</span>
                  </div>
                  {intersections.filter(i=>{ const [mn,mx]=[getKm(detailStartStation),getKm(detailEndStation)].sort((a,b)=>a-b); return i.km>mn&&i.km<mx; }).map(i=>{
                    const [mn,mx]=[getKm(detailStartStation),getKm(detailEndStation)].sort((a,b)=>a-b);
                    const ratio=((i.km-mn)/(mx-mn))*90+5;
                    return (
                      <div key={`pin-${i.id}`} className="track-node-pin intersection-pin" style={{ left:`${ratio}%` }}>
                        <div className="pin-circle"></div>
                        <span className="pin-label">{i.name}</span>
                        <span className="pin-km">{i.km.toFixed(2)}km</span>
                        <button className="btn-delete-int-pin" onClick={()=>handleRemoveIntersection(i.id)}>✕</button>
                      </div>
                    );
                  })}
                  <div className="track-node-pin station-pin" style={{ left:'95%' }}>
                    <div className="pin-circle"></div>
                    <span className="pin-label">{getName(detailEndStation)}</span>
                    <span className="pin-km">{getKm(detailEndStation).toFixed(2)}km</span>
                  </div>
                </div>
                <div style={{ marginTop:'3.5rem' }}>
                  <span className="column-title">2. 교차로 기준 분류된 세부 작업구간</span>
                  <div className="sub-segment-list">
                    {getSubSegments(detailStartStation, detailEndStation).map(seg=>{
                      const detail = workZoneDetails[seg.key];
                      const hasData = !!detail;
                      return (
                        <div key={seg.key} className={`sub-segment-card ${activeSubZoneKey===seg.key?'active':''}`} onClick={()=>handleSelectSubZone(seg.key)}>
                          <div className="card-header-row">
                            <span className="card-segment-title">{seg.fromName} ~ {seg.toName}</span>
                            <span className={`status-badge ${hasData?'completed':'pending'}`}>{hasData?'✅ 작성 완료':'⚠️ 미입력'}</span>
                          </div>
                          <div className="card-meta-row">
                            <span>📐 {seg.lengthM}m ({seg.fromKm.toFixed(2)}k~{seg.toKm.toFixed(2)}k)</span>
                            <span>🚧 지장물 {detail?.obstacles?.length||0}건</span>
                          </div>
                          {hasData && <div className="card-summary-row"><span>공법: {detail.selectedMethod}</span></div>}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
              <div className="modal-body-right">
                {activeSubZoneKey ? (
                  <div className="detail-editor-form">
                    <span className="column-title">3. 작업구간 조사 자료 ({activeSubZoneKey.replace('_',' ~ ')})</span>
                    <div className="form-group" style={{ marginBottom:'1.25rem' }}>
                      <label className="form-label">⚙️ 적용 시공 공법</label>
                      <select value={editingMethod} onChange={e=>handleMethodPresetChange(e.target.value)} style={{ width:'100%', padding:'0.5rem', fontSize:'0.9rem', borderRadius:'4px', border:'1px solid #cbd5e1', fontWeight:'bold' }}>
                        <option>일반개착식 궤도공법</option>
                        <option>교차로 저진동/무소음 궤도공법</option>
                        <option>지하차도 인입 특수공법</option>
                      </select>
                      <span style={{ fontSize:'0.75rem', color:'#64748b', marginTop:'4px', display:'block' }}>※ 공법 변경 시 표준 장비셋이 자동 적용됩니다.</span>
                    </div>
                    <div className="form-group" style={{ marginBottom:'1.5rem' }}>
                      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'6px' }}>
                        <label className="form-label">🚜 투입 장비</label>
                        <button className="btn-add-table-row" onClick={handleAddEquip}>+ 장비 추가</button>
                      </div>
                      <table className="form-inner-table">
                        <thead><tr><th>장비 모델 / 종류</th><th style={{ width:'80px', textAlign:'center' }}>수량(대)</th><th style={{ width:'40px' }}></th></tr></thead>
                        <tbody>
                          {editingEquipment.length===0 ? <tr><td colSpan="3" style={{ textAlign:'center', color:'#94a3b8', padding:'1rem' }}>등록된 장비 없음</td></tr>
                            : editingEquipment.map((eq,i)=>(
                              <tr key={`eq-${i}`}>
                                <td><input type="text" value={eq.type} onChange={e=>{const u=[...editingEquipment];u[i].type=e.target.value;setEditingEquipment(u);}} style={{ width:'100%', border:'none', background:'transparent' }} /></td>
                                <td><div style={{ display:'flex', alignItems:'center', gap:'4px' }}>
                                  <button className="btn-counter" onClick={()=>handleEquipCountChange(i,eq.count-1)}>-</button>
                                  <input type="number" value={eq.count} onChange={e=>handleEquipCountChange(i,e.target.value)} style={{ width:'40px', textAlign:'center', border:'1px solid #cbd5e1', borderRadius:'3px' }} />
                                  <button className="btn-counter" onClick={()=>handleEquipCountChange(i,eq.count+1)}>+</button>
                                </div></td>
                                <td style={{ textAlign:'center' }}><button onClick={()=>handleRemoveEquip(i)} style={{ color:'red', border:'none', background:'transparent', cursor:'pointer' }}>✕</button></td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                    <div className="form-group" style={{ marginBottom:'1.5rem' }}>
                      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'6px' }}>
                        <label className="form-label">🚧 지장물 조사자료</label>
                        <button className="btn-add-table-row" onClick={handleAddObstacle}>+ 지장물 추가</button>
                      </div>
                      <table className="form-inner-table">
                        <thead><tr><th style={{ width:'80px' }}>구분</th><th>명칭/사양</th><th style={{ width:'110px' }}>조치상태</th><th>특기사항</th><th style={{ width:'30px' }}></th></tr></thead>
                        <tbody>
                          {editingObstacles.length===0 ? <tr><td colSpan="5" style={{ textAlign:'center', color:'#94a3b8', padding:'1rem' }}>지장물 없음</td></tr>
                            : editingObstacles.map((obs,i)=>(
                              <tr key={`obs-${i}`}>
                                <td><select value={obs.type} onChange={e=>handleObstacleChange(i,'type',e.target.value)} style={{ width:'100%', border:'none' }}><option>지상</option><option>지하</option><option>기타</option></select></td>
                                <td><input type="text" value={obs.name} onChange={e=>handleObstacleChange(i,'name',e.target.value)} style={{ width:'100%', border:'none', background:'transparent' }} /></td>
                                <td><select value={obs.status} onChange={e=>handleObstacleChange(i,'status',e.target.value)} style={{ width:'100%', border:'none' }}><option>조사중</option><option>이설협의중</option><option>보호공법적용</option><option>이설완료</option></select></td>
                                <td><input type="text" value={obs.memo||''} onChange={e=>handleObstacleChange(i,'memo',e.target.value)} style={{ width:'100%', border:'none', background:'transparent' }} /></td>
                                <td style={{ textAlign:'center' }}><button onClick={()=>handleRemoveObstacle(i)} style={{ color:'red', border:'none', background:'transparent', cursor:'pointer' }}>✕</button></td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                    <div className="form-group" style={{ marginBottom:'1.5rem' }}>
                      <label className="form-label">📝 현장 여건 종합 의견</label>
                      <textarea value={editingMemo} onChange={e=>setEditingMemo(e.target.value)} style={{ width:'100%', height:'80px', padding:'0.5rem', borderRadius:'4px', border:'1px solid #cbd5e1', resize:'vertical' }} />
                    </div>
                    <button className="btn-save-zone" onClick={handleSaveSubZone}>💾 이 작업구간의 공법/장비/지장물 저장</button>
                  </div>
                ) : (
                  <div className="form-empty-state">
                    <span>👈 왼쪽 목록에서 작업구간(소구간)을 선택해 주세요.</span>
                    <span style={{ fontSize:'0.85rem', color:'#94a3b8', marginTop:'10px' }}>선택된 구간의 공법, 지장물 데이터 빌더가 활성화됩니다.</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
