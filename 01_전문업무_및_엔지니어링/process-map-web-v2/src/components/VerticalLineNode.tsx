import type { NodeProps } from 'reactflow';
import type { NodeData } from '../store/useStore';
import useStore from '../store/useStore';
import { v4 as uuidv4 } from 'uuid';

export default function VerticalLineNode({ id, data }: NodeProps<NodeData & { height?: number }>) {
  const { addNode, nodes } = useStore();
  const height = data?.height ?? 1700;

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.ctrlKey && e.button === 0) { // Left click + Ctrl
      e.stopPropagation();
      e.preventDefault();
      const currentNode = nodes.find(n => n.id === id);
      if (currentNode) {
        addNode({
          ...currentNode,
          id: uuidv4(),
          position: { x: currentNode.position.x + 100, y: currentNode.position.y },
          selected: true
        });
      }
    }
  };

  return (
    <div
      className="vertical-line-container group flex justify-center"
      style={{ width: 24, height: height, marginTop: 0 }}
      onMouseDown={handleMouseDown}
    >
      <style>{`
        .vertical-line-container {
          cursor: grab;
        }
        .vertical-line-container:active {
          cursor: grabbing;
        }
        .vertical-line-container .vertical-line-inner {
          width: 0px;
          height: 100%;
          border-left: 2px solid transparent;
          transition: border-color 0.15s ease;
        }
        .vertical-line-container:hover .vertical-line-inner {
          border-left: 2px solid #3b82f6;
        }
      `}</style>
      <div className="vertical-line-inner pointer-events-none" />
    </div>
  );
}
