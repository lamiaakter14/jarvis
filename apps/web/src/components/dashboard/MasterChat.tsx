import React, { useState } from 'react';
import {
  Settings2,
  Send,
  Paperclip,
  Mic,
  ChevronDown,
  Edit3,
  Check,
  Brain,
} from 'lucide-react';
import { cn } from '../../utils/cn';

const agentColors: Record<string, string> = {
  PLANNER: 'bg-blue-500/20 text-blue-400 border border-blue-500/40',
  EXECUTOR: 'bg-green-500/20 text-green-400 border border-green-500/40',
  AMPLIFIER: 'bg-purple-500/20 text-purple-400 border border-purple-500/40',
  REFLECTOR: 'bg-orange-500/20 text-orange-400 border border-orange-500/40',
};

const agentIcons: Record<string, string> = {
  PLANNER: '#1e3a8a',
  EXECUTOR: '#064e3b',
  AMPLIFIER: '#3b0764',
  REFLECTOR: '#7c2d12',
};

const todaysPlan = [
  { text: 'Finalize homepage design', done: true },
  { text: 'Review API integration', done: true },
  { text: 'Optimize performance', done: false },
  { text: 'Client feedback call', done: false },
];

const agentSelectors = [
  { role: 'PLANNER', subtitle: 'Strategist' },
  { role: 'EXECUTOR', subtitle: 'Doer' },
  { role: 'AMPLIFIER', subtitle: 'Optimizer' },
  { role: 'REFLECTOR', subtitle: 'Analyst' },
];

interface Message {
  id: string;
  from: 'jarvis' | 'user';
  agent?: string;
  time: string;
  content: React.ReactNode;
  typing?: boolean;
}

export const MasterChat: React.FC = () => {
  const [showActions, setShowActions] = useState(false);
  const [input, setInput] = useState('');
  const [activeAgent, setActiveAgent] = useState('PLANNER');

  const messages: Message[] = [
    {
      id: '1',
      from: 'jarvis',
      agent: 'PLANNER',
      time: '10:32 AM',
      content: (
        <div className="space-y-3">
          <p className="text-sm text-jarvis-text leading-relaxed">
            Good morning, Tony. I've analyzed your schedule and priorities.
            Here's what I recommend we focus on today.
          </p>
          {/* Today's Plan card */}
          <div className="bg-jarvis-bg border border-jarvis-border rounded-lg p-3">
            <p className="text-[10px] font-semibold tracking-widest text-jarvis-muted uppercase mb-3">
              Today's Plan
            </p>
            <div className="flex items-start gap-4">
              <div className="flex-1 space-y-2">
                {todaysPlan.map((item, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <div
                      className={cn(
                        'w-4 h-4 rounded-full border-2 flex items-center justify-center flex-shrink-0',
                        item.done
                          ? 'border-jarvis-green bg-jarvis-green/20'
                          : 'border-jarvis-border'
                      )}
                    >
                      {item.done && <Check className="w-2.5 h-2.5 text-jarvis-green" />}
                    </div>
                    <span className={cn('text-xs', item.done ? 'text-jarvis-muted line-through' : 'text-jarvis-text')}>
                      {item.text}
                    </span>
                  </div>
                ))}
              </div>
              {/* Progress circle */}
              <div className="flex-shrink-0 flex flex-col items-center">
                <svg width="64" height="64" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="26" fill="none" stroke="#1a2740" strokeWidth="6" />
                  <circle
                    cx="32"
                    cy="32"
                    r="26"
                    fill="none"
                    stroke="#00d4ff"
                    strokeWidth="6"
                    strokeDasharray={`${2 * Math.PI * 26}`}
                    strokeDashoffset={`${2 * Math.PI * 26 * (1 - 0.66)}`}
                    strokeLinecap="round"
                    transform="rotate(-90 32 32)"
                  />
                  <text x="32" y="33" textAnchor="middle" dominantBaseline="middle" fill="#e2e8f0" fontSize="12" fontWeight="bold">
                    66%
                  </text>
                  <text x="32" y="44" textAnchor="middle" dominantBaseline="middle" fill="#64748b" fontSize="7">
                    COMPLETE
                  </text>
                </svg>
              </div>
            </div>
            {/* Plan action buttons */}
            <div className="flex gap-2 mt-3">
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs border border-jarvis-border rounded-lg text-jarvis-muted hover:text-jarvis-text hover:border-jarvis-cyan/40 transition-colors">
                <Edit3 className="w-3 h-3" />
                Edit Plan
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-jarvis-green/20 border border-jarvis-green/40 rounded-lg text-jarvis-green hover:bg-jarvis-green/30 transition-colors">
                <Check className="w-3 h-3" />
                Approve Plan
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-blue-600/20 border border-blue-500/40 rounded-lg text-blue-400 hover:bg-blue-600/30 transition-colors">
                <Send className="w-3 h-3" />
                Send to Executor
              </button>
            </div>
          </div>
        </div>
      ),
    },
    {
      id: '2',
      from: 'user',
      time: '10:33 AM',
      content: (
        <p className="text-sm text-jarvis-text leading-relaxed">
          Looks good. Prioritize performance optimization and prepare the client call notes.
        </p>
      ),
    },
    {
      id: '3',
      from: 'jarvis',
      agent: 'EXECUTOR',
      time: '10:33 AM',
      content: (
        <div className="space-y-2">
          <p className="text-sm text-jarvis-text leading-relaxed">
            Understood. Updating priorities and executing tasks.
          </p>
          <div className="flex gap-1.5">
            {[0, 1, 2].map((i) => (
              <span
                key={i}
                className="w-2 h-2 rounded-full bg-jarvis-green"
                style={{ animationDelay: `${i * 0.2}s`, animation: 'pulse 1.4s ease-in-out infinite' }}
              />
            ))}
          </div>
        </div>
      ),
    },
  ];

  return (
    <div className="bg-jarvis-card border border-jarvis-border rounded-xl flex flex-col h-full overflow-hidden">
      {/* Chat header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-jarvis-border flex-shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-sm font-bold text-jarvis-text tracking-wider">MASTER CHAT</span>
          <div className="flex items-center gap-1.5 px-2 py-0.5 bg-jarvis-green/10 border border-jarvis-green/30 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-jarvis-green animate-pulse-slow" />
            <span className="text-[10px] font-semibold text-jarvis-green tracking-wider">AI BRAIN · ONLINE</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] text-jarvis-muted">Show Actions</span>
            <button
              onClick={() => setShowActions(!showActions)}
              className={cn(
                'w-8 h-4 rounded-full border transition-all relative',
                showActions
                  ? 'bg-jarvis-cyan/30 border-jarvis-cyan/60'
                  : 'bg-jarvis-border border-jarvis-border'
              )}
            >
              <span
                className={cn(
                  'absolute top-0.5 w-3 h-3 rounded-full transition-all',
                  showActions ? 'right-0.5 bg-jarvis-cyan' : 'left-0.5 bg-jarvis-muted'
                )}
              />
            </button>
          </div>
          <button className="p-1.5 rounded text-jarvis-muted hover:text-jarvis-text hover:bg-white/5 transition-colors">
            <Settings2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={cn('flex gap-3', msg.from === 'user' && 'flex-row-reverse')}>
            {/* Avatar */}
            {msg.from === 'jarvis' ? (
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1 border border-jarvis-cyan/30"
                style={{ background: 'linear-gradient(135deg, #0f2a4a, #0a1628)' }}
              >
                <Brain className="w-4 h-4 text-jarvis-cyan" />
              </div>
            ) : (
              <div className="w-8 h-8 rounded-full overflow-hidden flex-shrink-0 mt-1 border border-jarvis-border">
                <div className="w-full h-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white text-xs font-bold">
                  T
                </div>
              </div>
            )}

            {/* Bubble */}
            <div className={cn('flex-1 max-w-[85%]', msg.from === 'user' && 'flex flex-col items-end')}>
              {/* Name + agent tag */}
              <div className={cn('flex items-center gap-2 mb-1', msg.from === 'user' && 'flex-row-reverse')}>
                {msg.from === 'jarvis' ? (
                  <>
                    <span className="text-xs font-bold text-jarvis-text">JARVIS</span>
                    {msg.agent && (
                      <span className={cn('text-[9px] font-bold px-1.5 py-0.5 rounded tracking-wider', agentColors[msg.agent])}>
                        {msg.agent}
                      </span>
                    )}
                    <span className="text-[10px] text-jarvis-muted">{msg.time}</span>
                  </>
                ) : (
                  <>
                    <span className="text-xs font-bold text-jarvis-text">YOU</span>
                    <span className="text-[10px] text-jarvis-muted">{msg.time}</span>
                    <Check className="w-3 h-3 text-jarvis-cyan" />
                  </>
                )}
              </div>
              <div
                className={cn(
                  'rounded-xl px-4 py-3',
                  msg.from === 'jarvis'
                    ? 'bg-jarvis-surface border border-jarvis-border'
                    : 'bg-blue-600/20 border border-blue-500/30'
                )}
              >
                {msg.content}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Agent selectors */}
      <div className="px-4 py-2 border-t border-jarvis-border flex items-center gap-2 flex-shrink-0 overflow-x-auto">
        {agentSelectors.map((agent) => (
          <button
            key={agent.role}
            onClick={() => setActiveAgent(agent.role)}
            className={cn(
              'flex items-center gap-1.5 px-2 py-1 rounded-lg border text-xs transition-all flex-shrink-0',
              activeAgent === agent.role
                ? agentColors[agent.role]
                : 'border-jarvis-border text-jarvis-muted hover:border-jarvis-cyan/30'
            )}
          >
            <span className="font-semibold text-[10px] tracking-wider">{agent.role}</span>
            <ChevronDown className="w-2.5 h-2.5" />
            <span className="text-[10px] text-jarvis-muted">{agent.subtitle}</span>
          </button>
        ))}
      </div>

      {/* Input bar */}
      <div className="px-3 py-3 border-t border-jarvis-border flex items-center gap-2 flex-shrink-0">
        <button className="p-2 rounded-lg bg-jarvis-green/20 border border-jarvis-green/40 text-jarvis-green hover:bg-jarvis-green/30 transition-colors flex-shrink-0">
          <Mic className="w-4 h-4" />
        </button>
        <button className="p-2 rounded-lg text-jarvis-muted hover:text-jarvis-text hover:bg-white/5 transition-colors flex-shrink-0">
          <Paperclip className="w-4 h-4" />
        </button>
        <button className="p-2 rounded-lg text-jarvis-muted hover:text-jarvis-text hover:bg-white/5 transition-colors flex-shrink-0">
          <Settings2 className="w-4 h-4" />
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything or give a command..."
          className="flex-1 bg-transparent text-sm text-jarvis-text placeholder-jarvis-muted outline-none min-w-0"
        />
        <button className="flex items-center gap-2 px-4 py-2 bg-jarvis-cyan text-jarvis-bg text-xs font-bold rounded-lg hover:bg-jarvis-cyan/80 transition-colors flex-shrink-0">
          <Send className="w-3.5 h-3.5" />
          EXECUTE
          <ChevronDown className="w-3 h-3" />
        </button>
      </div>
    </div>
  );
};
