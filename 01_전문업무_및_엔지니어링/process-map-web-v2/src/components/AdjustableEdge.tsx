import React from 'react';
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
  markerStart,
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

  return (
    <>
      <path
        id={id}
        style={style}
        className="react-flow__edge-path"
        d={path}
        markerStart={markerStart}
        markerEnd={markerEnd}
      />
      {/* Thicker transparent path to make hovering/clicking easier */}
      <path
        d={path}
        fill="none"
        stroke="transparent"
        strokeWidth={15}
        className="react-flow__edge-interaction cursor-pointer"
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
      {/* Edge label rendered at the center handle coordinate */}
      {label && (
        <EdgeLabelRenderer>
          <div
            style={{
              position: 'absolute',
              transform: `translate(-50%, -100%) translate(${handleX}px, ${handleY - 10}px)`,
              background: '#ffffff',
              padding: '2px 6px',
              borderRadius: '4px',
              fontSize: '11px',
              fontWeight: 500,
              color: '#374151',
              border: '1px solid #e5e7eb',
              boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
              pointerEvents: 'all',
            }}
            className="nodrag nopan select-none"
          >
            {label}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}
