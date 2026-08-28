import React, { useState, useCallback } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  Connection,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Play, Save, Plus, Database, Cpu, CheckCircle, ShieldCheck, RefreshCw } from 'lucide-react';

const initialNodes: Node[] = [
  {
    id: 'node_source',
    type: 'input',
    data: { label: '📥 S3 Bronze Ingest (telemetry_raw)' },
    position: { x: 100, y: 150 },
    style: { background: '#1e293b', color: '#38bdf8', border: '1px solid #38bdf8', borderRadius: '8px', padding: '12px', width: 220 },
  },
  {
    id: 'node_clean',
    data: { label: '⚙️ Clean & Mask PII (CryptoMask)' },
    position: { x: 400, y: 100 },
    style: { background: '#1e293b', color: '#a855f7', border: '1px solid #a855f7', borderRadius: '8px', padding: '12px', width: 220 },
  },
  {
    id: 'node_quality',
    data: { label: '🛡️ Quality Suite (Z-Score & IQR)' },
    position: { x: 400, y: 220 },
    style: { background: '#1e293b', color: '#f59e0b', border: '1px solid #f59e0b', borderRadius: '8px', padding: '12px', width: 220 },
  },
  {
    id: 'node_gold',
    type: 'output',
    data: { label: '🏆 Gold Delta Lake / Snowflake' },
    position: { x: 720, y: 150 },
    style: { background: '#1e293b', color: '#10b981', border: '1px solid #10b981', borderRadius: '8px', padding: '12px', width: 220 },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1', source: 'node_source', target: 'node_clean', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2', source: 'node_source', target: 'node_quality', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3', source: 'node_clean', target: 'node_gold', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4', source: 'node_quality', target: 'node_gold', markerEnd: { type: MarkerType.ArrowClosed } },
];

export function AdvancedDagEditor() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const onConnect = useCallback(
    (params: Edge | Connection) =>
      setEdges((eds) => addEdge({ ...params, animated: true, markerEnd: { type: MarkerType.ArrowClosed } }, eds)),
    [setEdges]
  );

  const addNode = (type: 'source' | 'transform' | 'quality' | 'sink') => {
    const id = `node_${Date.now()}`;
    let label = 'New Node';
    let color = '#38bdf8';

    if (type === 'source') {
      label = '📥 Ingest Source';
      color = '#38bdf8';
    } else if (type === 'transform') {
      label = '⚙️ Transform Step';
      color = '#a855f7';
    } else if (type === 'quality') {
      label = '🛡️ Quality Rule';
      color = '#f59e0b';
    } else if (type === 'sink') {
      label = '🏆 Export Sink';
      color = '#10b981';
    }

    const newNode: Node = {
      id,
      data: { label },
      position: { x: 300 + Math.random() * 100, y: 150 + Math.random() * 100 },
      style: { background: '#1e293b', color, border: `1px solid ${color}`, borderRadius: '8px', padding: '12px', width: 200 },
    };

    setNodes((nds) => [...nds, newNode]);
  };

  return (
    <div className="flex flex-col h-[700px] bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Studio Toolbar */}
      <div className="p-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-white text-sm">DAG Visual Studio</span>
          <span className="text-xs bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded font-mono">
            {nodes.length} nodes | {edges.length} edges
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => addNode('source')}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-medium border border-slate-700 transition"
          >
            <Database className="w-3.5 h-3.5" /> + Source
          </button>
          <button
            onClick={() => addNode('transform')}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-purple-400 text-xs font-medium border border-slate-700 transition"
          >
            <Cpu className="w-3.5 h-3.5" /> + Transform
          </button>
          <button
            onClick={() => addNode('quality')}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-400 text-xs font-medium border border-slate-700 transition"
          >
            <ShieldCheck className="w-3.5 h-3.5" /> + Quality
          </button>
          <button
            onClick={() => addNode('sink')}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-medium border border-slate-700 transition"
          >
            <CheckCircle className="w-3.5 h-3.5" /> + Sink
          </button>

          <div className="h-4 w-px bg-slate-700 mx-1" />

          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium shadow-md shadow-cyan-600/20 transition">
            <Save className="w-3.5 h-3.5" /> Save DAG
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium shadow-md shadow-emerald-600/20 transition">
            <Play className="w-3.5 h-3.5" /> Run Pipeline
          </button>
        </div>
      </div>

      {/* React Flow Canvas */}
      <div className="flex-1 w-full h-full relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={(_, node) => setSelectedNode(node)}
          fitView
        >
          <Background color="#334155" gap={16} size={1} />
          <Controls className="bg-slate-900 border border-slate-800 fill-white" />
          <MiniMap
            nodeColor={(n) => {
              if (n.type === 'input') return '#38bdf8';
              if (n.type === 'output') return '#10b981';
              return '#a855f7';
            }}
            maskColor="rgba(15, 23, 42, 0.8)"
            className="bg-slate-900 border border-slate-800 rounded"
          />
        </ReactFlow>
      </div>
    </div>
  );
}
