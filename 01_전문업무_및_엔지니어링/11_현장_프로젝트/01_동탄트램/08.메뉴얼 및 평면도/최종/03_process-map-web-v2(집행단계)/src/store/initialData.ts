import { generatePreEarthworkNodesAndEdges } from '../utils/preEarthworkLoader';

const { nodes, edges } = generatePreEarthworkNodesAndEdges();

export const initialNodes = nodes;
export const initialEdges = edges;
