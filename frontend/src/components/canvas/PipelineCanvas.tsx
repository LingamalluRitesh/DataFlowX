import React, { useCallback, useMemo, useState } from 'react';
import {
  Background,
  BackgroundVariant,
  Connection,
  Controls,
  Edge,
  MiniMap,
  Node,
  ReactFlow,
  addEdge,
  useEdgesState,
  useNodesState,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import {
  CheckCircle2,
  Database,
  FileCode,
  Filter,
  Layers,
  Play,
  Plus,
  Save,
  ShieldCheck,
  Table,
} from 'lucide-react';
import { CustomPipelineNode } from './CustomNode';
import { NodeConfigDrawer } from './NodeConfigDrawer';
import { Button } from '../ui/Button';
import { DAGEdgeData, DAGNodeData } from '@/types';

interface PipelineCanvasProps {
  initialNodes?: DAGNodeData[];
  initialEdges?: DAGEdgeData[];
  onSave?: (nodes: DAGNodeData[], edges: DAGEdgeData[]) => void;
  onRun?: () => void;
  isSaving?: boolean;
  isRunning?: boolean;
}

const nodePalette = [
  { type: 'extract', label: 'Extract Connector', icon: Database },
  { type: 'quality', label: 'Data Quality & Quarantine', icon: ShieldCheck },
  { type: 'transform', label: 'Silver Clean & Transform', icon: Layers },
  { type: 'filter', label: 'Filter Rows', icon: Filter },
  { type: 'aggregate', label: 'Aggregate Mart', icon: Table },
  { type: 'sql', label: 'Custom SQL (DuckDB/SQLite)', icon: FileCode },
  { type: 'warehouse_load', label: 'Warehouse Load', icon: Database },
];

export const PipelineCanvas: React.FC<PipelineCanvasProps> = ({
  initialNodes = [],
  initialEdges = [],
  onSave,
  onRun,
  isSaving = false,
  isRunning = false,
}) => {
  const formattedInitialNodes: Node[] = useMemo(() => {
    return initialNodes.map((n) => ({
      id: n.id,
      type: 'custom',
      position: n.position || { x: 100, y: 100 },
      data: { id: n.id, type: n.type, name: n.name, config: n.config },
    }));
  }, [initialNodes]);

  const formattedInitialEdges: Edge[] = useMemo(() => {
    return initialEdges.map((e, idx) => ({
      id: e.id || `edge-${e.source}-${e.target}-${idx}`,
      source: e.source,
      target: e.target,
      animated: true,
      style: { stroke: '#3b82f6', strokeWidth: 2 },
    }));
  }, [initialEdges]);

  const [nodes, setNodes, onNodesChange] = useNodesState(formattedInitialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(formattedInitialEdges);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const nodeTypes = useMemo(() => ({ custom: CustomPipelineNode }), []);

  const onConnect = useCallback(
    (params: Connection) => {
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            animated: true,
            style: { stroke: '#3b82f6', strokeWidth: 2 },
          },
          eds
        )
      );
    },
    [setEdges]
  );

  const handleAddNode = (paletteItem: (typeof nodePalette)[0]) => {
    const id = `node_${paletteItem.type}_${Date.now()}`;
    const newNode: Node = {
      id,
      type: 'custom',
      position: { x: 200 + nodes.length * 50, y: 150 + nodes.length * 30 },
      data: {
        id,
        type: paletteItem.type,
        name: paletteItem.label,
        config: {},
      },
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const handleNodeClick = (_: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  };

  const handleUpdateNode = (updatedNode: Node) => {
    setNodes((nds) => nds.map((n) => (n.id === updatedNode.id ? updatedNode : n)));
  };

  const handleDeleteNode = (nodeId: string) => {
    setNodes((nds) => nds.filter((n) => n.id !== nodeId));
    setEdges((eds) => eds.filter((e) => e.source !== nodeId && e.target !== nodeId));
  };

  const handleSaveDAG = () => {
    if (onSave) {
      const outputNodes: DAGNodeData[] = nodes.map((n) => ({
        id: n.id,
        type: n.data.type as string,
        name: n.data.name as string,
        config: n.data.config as Record<string, any>,
        position: n.position,
      }));

      const outputEdges: DAGEdgeData[] = edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
      }));

      onSave(outputNodes, outputEdges);
    }
  };

  return (
    <div className="relative w-full h-[750px] bg-slate-900 rounded-2xl border border-slate-800 shadow-2xl overflow-hidden flex">
      {/* Node Palette Toolbar */}
      <div className="w-64 bg-slate-950/80 border-r border-slate-800 p-4 flex flex-col justify-between z-10">
        <div>
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Operator Palette</h4>
          <div className="space-y-2">
            {nodePalette.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.type}
                  onClick={() => handleAddNode(item)}
                  className="w-full flex items-center gap-3 px-3 py-2 text-xs font-medium text-slate-300 bg-slate-900/60 hover:bg-blue-600 hover:text-white border border-slate-800 hover:border-blue-500 rounded-lg transition-all text-left"
                >
                  <Icon className="w-4 h-4" />
                  <span className="truncate">{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Canvas Actions */}
        <div className="space-y-2 pt-4 border-t border-slate-800">
          <Button variant="outline" size="sm" className="w-full" onClick={handleSaveDAG} isLoading={isSaving}>
            <Save className="w-4 h-4 mr-2" />
            Save Pipeline DAG
          </Button>
          {onRun && (
            <Button variant="success" size="sm" className="w-full" onClick={onRun} isLoading={isRunning}>
              <Play className="w-4 h-4 mr-2 fill-current" />
              Trigger Execution
            </Button>
          )}
        </div>
      </div>

      {/* Main Flow Canvas */}
      <div className="flex-1 h-full relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={handleNodeClick}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background color="#334155" gap={20} size={1} variant={BackgroundVariant.Dots} />
          <Controls className="bg-slate-800 text-slate-200 border-slate-700 fill-slate-200" />
          <MiniMap nodeColor="#3b82f6" className="bg-slate-950 border border-slate-800 rounded-lg overflow-hidden" />
        </ReactFlow>
      </div>

      {/* Node Config Drawer */}
      <NodeConfigDrawer
        isOpen={!!selectedNode}
        onClose={() => setSelectedNode(null)}
        node={selectedNode}
        onUpdateNode={handleUpdateNode}
        onDeleteNode={handleDeleteNode}
      />
    </div>
  );
};
