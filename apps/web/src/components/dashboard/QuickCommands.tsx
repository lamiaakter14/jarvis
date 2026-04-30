import React from 'react';
import { Calendar, Zap, BarChart3, AlertCircle, Lightbulb } from 'lucide-react';

interface QuickCommandsProps {
  onCommand?: (cmd: string) => void;
}

const commands = [
  { label: 'Plan a project', icon: Calendar, color: 'text-purple-400 border-purple-500/30 hover:border-purple-500/60', cmd: 'plan a new project' },
  { label: 'Execute tasks', icon: Zap, color: 'text-blue-400 border-blue-400/30 hover:border-blue-400/60', cmd: 'execute all tasks' },
  { label: 'Analyze performance', icon: BarChart3, color: 'text-cyan-400 border-cyan-400/30 hover:border-cyan-400/60', cmd: 'analyze performance' },
  { label: 'Find gaps', icon: AlertCircle, color: 'text-orange-400 border-orange-400/30 hover:border-orange-400/60', cmd: 'find knowledge gaps' },
  { label: 'Generate ideas', icon: Lightbulb, color: 'text-yellow-400 border-yellow-400/30 hover:border-yellow-400/60', cmd: 'generate innovations' },
];

export const QuickCommands: React.FC<QuickCommandsProps> = ({ onCommand }) => {
  const handleClick = (cmd: string) => {
    // Set input in MasterChat
    const input = document.querySelector('input[placeholder*="Ask anything"]') as HTMLInputElement;
    if (input) {
      input.value = cmd;
      input.focus();
      // Trigger Enter
      const event = new KeyboardEvent('keypress', { key: 'Enter' });
      input.dispatchEvent(event);
    }
    onCommand?.(cmd);
  };

  return (
    <div className="bg-jarvis-card border border-jarvis-border rounded-xl p-3">
      <p className="text-[10px] font-semibold tracking-widest text-jarvis-muted uppercase mb-2">Quick Commands</p>
      <div className="flex flex-wrap gap-2">
        {commands.map(cmd => {
          const Icon = cmd.icon;
          return (
            <button key={cmd.label} onClick={() => handleClick(cmd.cmd)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all hover:scale-105 ${cmd.color}`}>
              <Icon className="w-3.5 h-3.5" />{cmd.label}
            </button>
          );
        })}
      </div>
    </div>
  );
};