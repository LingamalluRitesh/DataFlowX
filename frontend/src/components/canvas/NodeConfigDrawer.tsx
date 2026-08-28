import React, { useState } from 'react';
import { Drawer } from '../ui/Drawer';
import { Button } from '../ui/Button';
import { Trash2 } from 'lucide-react';

interface NodeConfigDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  node: any;
  onUpdateNode: (updatedNode: any) => void;
  onDeleteNode: (nodeId: string) => void;
}

export const NodeConfigDrawer: React.FC<NodeConfigDrawerProps> = ({
  isOpen,
  onClose,
  node,
  onUpdateNode,
  onDeleteNode,
}) => {
  if (!node) return null;

  const [name, setName] = useState(node.data?.name || '');
  const [configJson, setConfigJson] = useState(JSON.stringify(node.data?.config || {}, null, 2));

  const handleSave = () => {
    try {
      const parsedConfig = JSON.parse(configJson);
      onUpdateNode({
        ...node,
        data: {
          ...node.data,
          name,
          config: parsedConfig,
        },
      });
      onClose();
    } catch (err) {
      alert('Invalid JSON configuration syntax');
    }
  };

  return (
    <Drawer isOpen={isOpen} onClose={onClose} title={`Configure ${node.data?.type || 'Node'}`} width="lg">
      <div className="space-y-6">
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
            Node Label / Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-3.5 py-2 text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
            Configuration (JSON)
          </label>
          <textarea
            rows={12}
            value={configJson}
            onChange={(e) => setConfigJson(e.target.value)}
            className="w-full p-3 font-mono text-xs bg-slate-900 text-slate-100 border border-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-800">
          <Button
            variant="danger"
            size="sm"
            onClick={() => {
              onDeleteNode(node.id);
              onClose();
            }}
          >
            <Trash2 className="w-4 h-4 mr-1.5" />
            Delete Node
          </Button>

          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm" onClick={onClose}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" onClick={handleSave}>
              Save Changes
            </Button>
          </div>
        </div>
      </div>
    </Drawer>
  );
};
