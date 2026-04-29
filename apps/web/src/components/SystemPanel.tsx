// apps/web/src/components/SystemPanel.tsx

import React from 'react';
import { SystemMode } from './IntentDetector';

interface SystemPanelProps {
  mode: SystemMode;
  projectName?: string;
  taskCount?: number;
}

const modeColors: Record<SystemMode, string> = {
  chat: 'bg-gray-500',
  planner: 'bg-purple-500',
  execution: 'bg-green-500',
  advisor: 'bg-blue-500',
  memory: 'bg-cyan-500'
};

const mockFeed = [
  { time: '10:33:42', text: 'System metrics updated', color: 'text-cyan-400' },
  { time: '10:33:38', text: 'Knowledge gap detected', color: 'text-orange-400' },
  { time: '10:33:34', text: 'Plan generated', color: 'text-purple-400' },
  { time: '10:33:29', text: 'Task completed: TSK-022', color: 'text-green-400' },
  { time: '10:33:25', text: 'Started: TSK-023', color: 'text-green-400' },
];

export const SystemPanel: React.FC<SystemPanelProps> = ({ mode, projectName, taskCount = 0 }) => {
  return (
    <div className="bg-[#151A22] border border-[#232A34] rounded h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-[#232A34]">
        <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">
          ⚡ System State
        </h3>
      </div>

      {/* Active Mode */}
      <div className="p-4 border-b border-[#232A34]">
        <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">Active Mode</p>
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 ${modeColors[mode]} rounded-full animate-pulse`} />
          <span className="text-sm font-bold text-white capitalize">{mode}</span>
        </div>
      </div>

      {/* Current Project */}
      <div className="p-4 border-b border-[#232A34]">
        <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">Current Project</p>
        <p className="text-sm text-white font-mono">
          {projectName || <span className="text-gray-600">—</span>}
        </p>
      </div>

      {/* Active Tasks */}
      <div className="p-4 border-b border-[#232A34]">
        <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">
          Active Tasks
          {taskCount > 0 && (
            <span className="ml-2 px-1.5 py-0.5 bg-blue-600 text-white rounded text-[9px]">
              {taskCount}
            </span>
          )}
        </p>
        {taskCount > 0 ? (
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-gray-500">⬜</span>
              <span className="text-xs text-gray-300">task-01: Design</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-500">⬜</span>
              <span className="text-xs text-gray-300">task-02: Content</span>
            </div>
          </div>
        ) : (
          <p className="text-xs text-gray-600">No active tasks</p>
        )}
      </div>

      {/* System Feed */}
      <div className="p-4 flex-1 overflow-y-auto">
        <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-2">System Feed</p>
        <div className="space-y-2">
          {mockFeed.map((item, i) => (
            <div key={i} className="flex gap-2 text-[10px] border-l-2 border-[#232A34] pl-2">
              <span className="text-gray-600 font-mono">{item.time}</span>
              <span className={item.color}>{item.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};