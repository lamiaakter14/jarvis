import React from 'react';
import { Calendar, Zap, BarChart3, AlertCircle, Lightbulb } from 'lucide-react';

const commands = [
  { label: 'Create weekly plan', icon: Calendar, color: 'text-jarvis-cyan border-jarvis-cyan/30 hover:border-jarvis-cyan/60 hover:bg-jarvis-cyan/5' },
  { label: 'Execute pending tasks', icon: Zap, color: 'text-blue-400 border-blue-400/30 hover:border-blue-400/60 hover:bg-blue-400/5' },
  { label: 'Analyze performance', icon: BarChart3, color: 'text-jarvis-purple border-purple-500/30 hover:border-purple-500/60 hover:bg-purple-500/5' },
  { label: 'Find knowledge gaps', icon: AlertCircle, color: 'text-jarvis-amber border-amber-400/30 hover:border-amber-400/60 hover:bg-amber-400/5' },
  { label: 'Generate ideas', icon: Lightbulb, color: 'text-jarvis-orange border-orange-400/30 hover:border-orange-400/60 hover:bg-orange-400/5' },
];

export const QuickCommands: React.FC = () => {
  return (
    <div className="bg-jarvis-card border border-jarvis-border rounded-xl p-3">
      <p className="text-[10px] font-semibold tracking-widest text-jarvis-muted uppercase mb-2">
        Quick Commands
      </p>
      <div className="flex flex-wrap gap-2">
        {commands.map((cmd) => {
          const Icon = cmd.icon;
          return (
            <button
              key={cmd.label}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all ${cmd.color}`}
            >
              <Icon className="w-3.5 h-3.5" />
              {cmd.label}
            </button>
          );
        })}
      </div>
    </div>
  );
};
