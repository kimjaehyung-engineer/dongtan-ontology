import { getSmoothStepPath, useViewport, EdgeLabelRenderer } from 'reactflow';
import type { EdgeProps } from 'reactflow';
import useStore from '../store/useStore';

export default function AdjustableEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
  selected,
  data,
  label,
}: EdgeProps) {
  const { zoom } = useViewport();
  const store = useStore();

  const centerX = data?.centerX;
  const centerY = data?.centerY;

  const [path] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
    centerX,
    centerY,
  });

  const handleMouseDown = (event: React.MouseEvent) => {
    event.stopPropagation();
    event.preventDefault();

    const startX = event.clientX;
    const startY = event.clientY;
    const startCenterX = centerX ?? (sourceX + targetX) / 2;
    const startCenterY = centerY ?? (sourceY + targetY) / 2;

    const handleMouseMove = (moveEvent: MouseEvent) => {
      const deltaX = (moveEvent.clientX - startX) / zoom;
      const deltaY = (moveEvent.clientY - startY) / zoom;

      // Update the edge in Zustand store
      store.setNodesAndEdges(
        store.nodes,
        store.edges.map((edge) => {
          if (edge.id === id) {
            return {
              ...edge,
              data: {
                ...edge.data,
                centerX: startCenterX + deltaX,
                centerY: startCenterY + deltaY,
              },
            };
          }
          return edge;
        })
      );
    };

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleX = centerX ?? (sourceX + targetX) / 2;
  const handleY = centerY ?? (sourceY + targetY) / 2;
  const handleEdgeClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    const { edges, nodes, setNodesAndEdges } = useStore.getState();
    const targetEdge = edges.find(edge => edge.id === id);
    if (!targetEdge) return;

    const nextSelected = !targetEdge.selected;

    const updatedEdges = edges.map(edge => {
      if (edge.id === id) {
        return {
          ...edge,
          selected: nextSelected,
          animated: nextSelected ? true : (edge.data?.originalAnimated ?? false),
          style: {
            ...(edge.style || {}),
            zIndex: nextSelected ? 999 : 1,
          },
        };
      }
      return edge;
    });

    setNodesAndEdges(nodes, updatedEdges);
  };

  const markerId = `marker-arrow-${id.replace(/[^a-zA-Z0-9_-]/g, '')}`;
  const isCrimsonRed = style?.stroke === '#b91c1c' || (markerEnd && typeof markerEnd === 'object' && (markerEnd as any).color === '#b91c1c');
  const strokeColor = isCrimsonRed ? '#b91c1c' : ((style?.stroke as string) || (markerEnd && typeof markerEnd === 'object' && (markerEnd as any).color) || '#2563eb');
  const edgeWidth = selected ? 7 : (Number(style?.strokeWidth) || 5.5);

  const activeStyle: React.CSSProperties = {
    ...(style || {}),
    stroke: strokeColor,
    strokeWidth: edgeWidth,
    zIndex: selected ? 999 : 1,
    opacity: 1,
  };

  return (
    <>
      <defs>
        <marker
          id={markerId}
          viewBox="0 0 10 10"
          refX="8"
          refY="5"
          markerWidth="9"
          markerHeight="9"
          orient="auto-start-reverse"
        >
          <path d="M 0 1 L 10 5 L 0 9 z" fill={strokeColor} stroke={strokeColor} strokeWidth="0.8" />
        </marker>
      </defs>
      <path
        id={id}
        style={{
          ...activeStyle,
          stroke: strokeColor,
          strokeWidth: edgeWidth,
          opacity: 1,
          strokeOpacity: 1,
        }}
        stroke={strokeColor}
        strokeWidth={edgeWidth}
        strokeOpacity={1}
        className="react-flow__edge-path cursor-pointer transition-all"
        d={path}
        markerEnd={`url(#${markerId})`}
        onClick={handleEdgeClick}
      />
      {/* Thicker 25px transparent path to make hovering/clicking 100% effortless */}
      <path
        d={path}
        fill="none"
        stroke="transparent"
        strokeWidth={25}
        className="react-flow__edge-interaction cursor-pointer"
        onClick={handleEdgeClick}
      />
      {/* Drag handle, visible only when selected */}
      {selected && (
        <foreignObject
          width={24}
          height={24}
          x={handleX - 12}
          y={handleY - 12}
          requiredExtensions="http://www.w3.org/1999/xhtml"
        >
          <div
            onMouseDown={handleMouseDown}
            className="w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-md flex items-center justify-center hover:bg-blue-600 active:scale-90 transition-transform nodrag cursor-move"
            title="화살표 선 상하좌우 이동"
          >
            <span className="text-xs text-white font-bold select-none leading-none">✛</span>
          </div>
        </foreignObject>
      )}
      {/* Edge label rendered at the center handle coordinate - 마우스 드래그로 자유 이동 가능 */}
      {label && (
        <EdgeLabelRenderer>
          <div
            onMouseDown={handleMouseDown}
            style={{
              position: 'absolute',
              transform: `translate(-50%, -50%) translate(${handleX}px, ${handleY}px)`,
              background: '#ffffff',
              height: '24px',
              padding: '0 10px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: 800,
              color: '#0f172a',
              border: '1.5px solid #cbd5e1',
              boxShadow: '0 2px 4px 0 rgba(0, 0, 0, 0.08)',
              pointerEvents: 'all',
              zIndex: 10,
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              lineHeight: '1',
              whiteSpace: 'nowrap',
              cursor: 'grab',
            }}
            className="nodrag nopan select-none edge-custom-label-badge hover:border-blue-500 hover:text-blue-600 transition-colors"
            title="마우스로 드래그하여 연결선 꺾임 위치 및 라벨 이동"
          >
            <span style={{ display: 'inline-block', transform: 'translateY(-2.5px)' }}>{label}</span>
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}
