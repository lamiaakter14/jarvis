import React, { useState, useRef, useEffect } from 'react';
import { Settings2, Send, Mic, ChevronDown, Brain } from 'lucide-react';
import { cn } from '../../utils/cn';
import { sendMessage } from '../../api/chatApi';
import { detectIntent } from '../IntentDetector';

// ============================================================
// 2-Agent Architecture: PLANNER + EXECUTOR
// ============================================================
const agentColors: Record<string, string> = {
  PLANNER: 'bg-purple-500/20 text-purple-400 border border-purple-500/40',
  EXECUTOR: 'bg-blue-500/20 text-blue-400 border border-blue-500/40',
};

const agentSelectors = [
  { role: 'PLANNER', subtitle: 'Strategist + Mentor + Innovator' },
  { role: 'EXECUTOR', subtitle: 'Doer + Amplifier + Reflector' },
];

interface Message {
  id: string;
  from: 'jarvis' | 'user' | 'system';
  agent?: string;
  time: string;
  content: string;
  meta?: any;
}

export const MasterChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', from: 'system', time: new Date().toLocaleTimeString(), content: 'JARVIS OS ready. Type your idea or command.' }
  ]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState<'chat' | 'planner' | 'execution'>('chat');
  const [showPlan, setShowPlan] = useState(false);
  const [showApproval, setShowApproval] = useState(false);
  const [projectData, setProjectData] = useState<any>(null);
  const [projectName, setProjectName] = useState<string>();
  const [taskCount, setTaskCount] = useState(0);
  const [executing, setExecuting] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const addMessage = (from: Message['from'], content: string, agent?: string, meta?: any) => {
    setMessages(prev => [...prev, { id: Date.now().toString(), from, time: new Date().toLocaleTimeString(), content, agent, meta }]);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input.trim();
    addMessage('user', userMsg);
    setInput('');

    try {
      const result = await sendMessage(userMsg);
      setMode(result.mode as any);
      addMessage('jarvis', result.response, result.mode === 'planner' ? 'PLANNER' : 'EXECUTOR');

      if (result.meta?.project) {
        const p = result.meta.project;
        setProjectData(p);
        setProjectName(p.title);
        setTaskCount(p.tasks?.length || 0);
        addMessage('system', `📁 Project: ${p.id} — ${p.phases?.length || 0} phases, ${p.tasks?.length || 0} tasks`);
        setShowPlan(true);
      }

      if (result.meta?.questions) {
        addMessage('system', '📋 Planner Questions:');
        result.meta.questions.forEach((q: string, i: number) => addMessage('system', `  ${i + 1}. ${q}`));
      }

      if (result.intent === 'planner') setShowPlan(true);
    } catch {
      const intent = detectIntent(userMsg);
      setMode(intent.mode as any);
      addMessage('jarvis', '⚠️ Offline mode. Backend not reachable.', intent.mode === 'planner' ? 'PLANNER' : 'EXECUTOR');
    }
  };

  const handleApprove = async () => {
    setMode('execution');
    setShowApproval(false);
    setShowPlan(false);
    setExecuting(true);
    addMessage('system', '✅ Plan approved. Queuing tasks...');
    try {
      await fetch('/api/execute/queue', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ project: projectData }) });
      const execRes = await fetch('/api/execute/start', { method: 'POST' });
      const execData = await execRes.json();
      addMessage('system', `⚡ ${execData.tasks_executed} tasks executed successfully!`);
    } catch {
      addMessage('system', '📋 Tasks queued. Backend offline — local mode.');
    }
    setExecuting(false);
  };

  return (
    <div className="bg-jarvis-card border border-jarvis-border rounded-xl flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-jarvis-border flex-shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-sm font-bold text-jarvis-text tracking-wider">MASTER CHAT</span>
          <div className="flex items-center gap-1.5 px-2 py-0.5 bg-jarvis-green/10 border border-jarvis-green/30 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-jarvis-green animate-pulse" />
            <span className="text-[10px] font-semibold text-jarvis-green tracking-wider">AI BRAIN · ONLINE</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
            mode === 'planner' ? 'bg-purple-500/20 text-purple-400' : mode === 'execution' ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-500/20 text-gray-400'
          }`}>
            {mode}
          </span>
          <button className="p-1.5 rounded text-jarvis-muted hover:text-jarvis-text"><Settings2 className="w-4 h-4" /></button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map(msg => (
          <div key={msg.id} className={cn('flex gap-2', msg.from === 'user' && 'flex-row-reverse')}>
            {msg.from === 'jarvis' ? (
              <div className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 mt-1" style={{ background: 'linear-gradient(135deg, #0f2a4a, #0a1628)', border: '1px solid rgba(0,212,255,0.3)' }}>
                <Brain className="w-3.5 h-3.5 text-jarvis-cyan" />
              </div>
            ) : msg.from === 'user' ? (
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white text-[10px] font-bold flex-shrink-0 mt-1">M</div>
            ) : null}
            <div className={cn('max-w-[80%]', msg.from === 'user' && 'flex flex-col items-end')}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-bold text-jarvis-text">{msg.from === 'jarvis' ? 'JARVIS' : msg.from === 'user' ? 'YOU' : 'SYSTEM'}</span>
                {msg.agent && <span className={cn('text-[8px] font-bold px-1.5 py-0.5 rounded', agentColors[msg.agent])}>{msg.agent}</span>}
                <span className="text-[9px] text-jarvis-muted">{msg.time}</span>
              </div>
              <div className={cn('rounded-xl px-4 py-2.5 text-sm', 
                msg.from === 'jarvis' ? 'bg-jarvis-surface border border-jarvis-border text-jarvis-text' :
                msg.from === 'user' ? 'bg-blue-600/20 border border-blue-500/30 text-blue-100' :
                'bg-gray-700/20 border border-gray-600/20 text-gray-400 text-xs text-center'
              )}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}

        {/* Approval Buttons */}
        {showPlan && projectData && (
          <div className="flex gap-2 justify-center mt-3">
            <button onClick={() => { setShowApproval(true); addMessage('system', '📋 Review plan before approving.'); }} className="px-4 py-2 bg-purple-600/20 border border-purple-500/40 rounded-lg text-purple-400 text-xs font-bold hover:bg-purple-600/30">📋 Review Plan</button>
          </div>
        )}
        {showApproval && (
          <div className="flex gap-2 justify-center mt-2">
            <button onClick={handleApprove} className="px-4 py-2 bg-green-600/20 border border-green-500/40 rounded-lg text-green-400 text-xs font-bold hover:bg-green-600/30">✅ Approve & Execute</button>
            <button onClick={() => { setShowApproval(false); setShowPlan(false); addMessage('system', '❌ Plan rejected.'); }} className="px-4 py-2 bg-red-600/20 border border-red-500/40 rounded-lg text-red-400 text-xs font-bold hover:bg-red-600/30">❌ Reject</button>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Agent Selector */}
      <div className="px-4 py-2 border-t border-jarvis-border flex items-center gap-2 flex-shrink-0">
        {agentSelectors.map(agent => (
          <button key={agent.role} className={cn('flex items-center gap-1.5 px-2 py-1 rounded-lg border text-[10px] font-semibold tracking-wider transition-all', agentColors[agent.role])}>
            {agent.role}
            <ChevronDown className="w-2.5 h-2.5" />
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="px-3 py-3 border-t border-jarvis-border flex items-center gap-2 flex-shrink-0">
        <button className="p-2 rounded-lg bg-jarvis-green/20 border border-jarvis-green/40 text-jarvis-green"><Mic className="w-4 h-4" /></button>
        <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && handleSend()}
          placeholder="Ask anything or give a command..." className="flex-1 bg-transparent text-sm text-jarvis-text placeholder-jarvis-muted outline-none" />
        <button onClick={handleSend} className="flex items-center gap-2 px-4 py-2 bg-jarvis-cyan text-jarvis-bg text-xs font-bold rounded-lg hover:bg-jarvis-cyan/80">
          <Send className="w-3.5 h-3.5" />EXECUTE
        </button>
      </div>
    </div>
  );
};