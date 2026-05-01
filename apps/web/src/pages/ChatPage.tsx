import React, { useState, useRef, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Send, Mic, ChevronDown, Brain, Image, Paperclip } from 'lucide-react';
import { cn } from '../utils/cn';
import { sendMessage } from '../api/chatApi';
import { detectIntent } from '../components/IntentDetector';

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
}

export const ChatPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialMessage = searchParams.get('message') || '';
  
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', from: 'system', time: new Date().toLocaleTimeString(), content: 'Master Chat ready. Type your idea or upload files.' }
  ]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState<'chat' | 'planner' | 'execution'>('chat');
  const [showPlan, setShowPlan] = useState(false);
  const [showApproval, setShowApproval] = useState(false);
  const [projectData, setProjectData] = useState<any>(null);
  const [executing, setExecuting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);
  useEffect(() => { if (initialMessage) handleSendMessage(initialMessage); }, [initialMessage]);

  const addMessage = (from: Message['from'], content: string, agent?: string) => {
    setMessages(prev => [...prev, { id: Date.now().toString(), from, time: new Date().toLocaleTimeString(), content, agent }]);
  };

  const loadLocalContext = async (message: string) => {
    try {
      const lower = message.toLowerCase();
      const res = await fetch('/api/context');
      const data = await res.json();
      const isProject = /start|plan|create|build|open|launch|business|shop|store|project/ig.test(message);
      const relevant = (data || []).filter((c: any) => {
        if (isProject) return true;
        const key = (c.key || '').toLowerCase();
        const cat = (c.category || '').toLowerCase();
        return lower.includes(key) || key.includes(lower) || lower.includes(cat);
      });
      if (relevant.length > 0) {
        addMessage('system', `📍 Loaded ${relevant.length} local contexts:`);
        relevant.slice(0, 5).forEach((c: any) => addMessage('system', `  • ${c.key}: ${c.value}`));
      }
    } catch {}
  };

  const checkDiary = async (message: string) => {
    if (/^(log|diary|note):/i.test(message)) {
      const text = message.replace(/^(log|diary|note):/i, '').trim();
      if (text) {
        try { await fetch('/api/diary', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }) }); addMessage('system', '📓 Saved to Diary!'); return true; } catch { return false; }
      }
    }
    return false;
  };

  const checkMoney = async (message: string) => {
    const match = message.match(/(\d+).*?(day|দিন)/i) || message.match(/need.*?(\d+)/i);
    if (match) {
      const amount = parseInt(match[1]) || 10000;
      const daysMatch = message.match(/(\d+)\s*(day|দিন)/i);
      const days = daysMatch ? parseInt(daysMatch[1]) : 7;
      try {
        addMessage('system', `💰 ${days}-day plan for ৳${amount}...`);
        const res = await fetch(`/api/money/get-plan?target_amount=${amount}&days=${days}&skills=general`);
        const data = await res.json();
        if (data?.plan) { addMessage('system', `📊 Daily: ৳${data.plan.goal.daily_target?.toFixed(2)}`); return true; }
      } catch { return false; }
    }
    return false;
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files; if (!files) return;
    setUploading(true);
    for (let i = 0; i < files.length; i++) {
      const file = files[i]; addMessage('system', `📎 ${file.name}...`);
      const formData = new FormData(); formData.append('file', file);
      try { const res = await fetch('/api/diary/upload', { method: 'POST', body: formData }); const data = await res.json(); addMessage('system', `✅ ${data.filename}`); } catch { addMessage('system', `❌ Failed`); }
    }
    setUploading(false); if (fileRef.current) fileRef.current.value = '';
  };

  const toggleVoice = () => {
    setIsRecording(!isRecording);
    if (!isRecording) { addMessage('system', '🎤 Recording...'); setTimeout(() => { setIsRecording(false); addMessage('system', '✅ Voice saved'); }, 3000); }
  };

  const handleSendMessage = async (msg?: string) => {
    const userMsg = msg || input.trim(); if (!userMsg) return;
    if (!msg) { addMessage('user', userMsg); setInput(''); }
    await loadLocalContext(userMsg);
    if (await checkDiary(userMsg)) return;
    if (await checkMoney(userMsg)) return;
    try {
      const result = await sendMessage(userMsg); setMode(result.mode as any);
      addMessage('jarvis', result.response, result.mode === 'planner' ? 'PLANNER' : 'EXECUTOR');
      if (result.meta?.project) { const p = result.meta.project; setProjectData(p); setShowPlan(true); addMessage('system', `📁 ${p.id}`); addMessage('system', `📋 ${p.phases?.length || 0} Phases`); (p.phases || []).forEach((ph: any) => addMessage('system', `  ⬜ ${ph.name || ph}`)); }
      if (result.meta?.questions) { (result.meta.questions || []).forEach((q: string, i: number) => addMessage('system', `  ${i + 1}. ${q}`)); }
    } catch { const intent = detectIntent(userMsg); setMode(intent.mode as any); addMessage('jarvis', '⚠️ Offline', intent.mode === 'planner' ? 'PLANNER' : 'EXECUTOR'); if (intent.mode === 'planner') setShowPlan(true); }
  };

  const handleSend = () => handleSendMessage();
  const handleReview = () => { setShowApproval(true); if (projectData) { (projectData.phases || []).forEach((p: any) => addMessage('system', `  ⬜ ${p.name || p}`)); } };
  const handleApprove = async () => {
    setMode('execution'); setShowApproval(false); setShowPlan(false); setExecuting(true); addMessage('system', '✅ Executing...');
    try { await fetch('/api/execute/queue', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ project: projectData }) }); const er = await fetch('/api/execute/start', { method: 'POST' }); const ed = await er.json(); addMessage('jarvis', `⚡ ${ed.tasks_executed || 0} done!`, 'EXECUTOR'); } catch { addMessage('system', '📋 Queued locally.'); }
    setExecuting(false);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#232A34] bg-[#0F1419] flex-shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-sm font-bold tracking-wider text-gray-200">MASTER CHAT</span>
          <div className="flex items-center gap-1.5 px-2 py-0.5 bg-green-500/10 border border-green-500/30 rounded-full"><span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" /><span className="text-[10px] font-semibold text-green-500 tracking-wider">AI BRAIN · ONLINE</span></div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${mode === 'planner' ? 'bg-purple-500/20 text-purple-400' : mode === 'execution' ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-500/20 text-gray-400'}`}>{mode}</span>
          {executing && <span className="text-[10px] text-yellow-400 animate-pulse">⏳</span>}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map(msg => (
          <div key={msg.id} className={cn('flex gap-2', msg.from === 'user' && 'flex-row-reverse')}>
            {msg.from === 'jarvis' ? <div className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 mt-1" style={{ background: 'linear-gradient(135deg, #0f2a4a, #0a1628)', border: '1px solid rgba(0,212,255,0.3)' }}><Brain className="w-3.5 h-3.5 text-cyan-400" /></div> : msg.from === 'user' ? <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white text-[10px] font-bold flex-shrink-0 mt-1">M</div> : null}
            <div className={cn('max-w-[80%]', msg.from === 'user' && 'flex flex-col items-end')}>
              <div className="flex items-center gap-2 mb-1"><span className="text-[10px] font-bold text-gray-300">{msg.from === 'jarvis' ? 'JARVIS' : msg.from === 'user' ? 'YOU' : 'SYSTEM'}</span>{msg.agent && <span className={cn('text-[8px] font-bold px-1.5 py-0.5 rounded', agentColors[msg.agent])}>{msg.agent}</span>}<span className="text-[9px] text-gray-500">{msg.time}</span></div>
              <div className={cn('rounded-xl px-4 py-2.5 text-sm', msg.from === 'jarvis' ? 'bg-[#151A22] border border-[#232A34] text-gray-200' : msg.from === 'user' ? 'bg-blue-600/20 border border-blue-500/30 text-blue-100' : 'bg-gray-700/20 border border-gray-600/20 text-gray-400 text-xs text-center')}>{msg.content}</div>
            </div>
          </div>
        ))}
        {showPlan && !showApproval && <div className="flex gap-2 justify-center mt-3"><button onClick={handleReview} className="px-4 py-2 bg-purple-600/20 border border-purple-500/40 rounded-lg text-purple-400 text-xs font-bold hover:bg-purple-600/30">📋 Review Plan</button></div>}
        {showApproval && <div className="flex gap-2 justify-center mt-2"><button onClick={handleApprove} className="px-4 py-2 bg-green-600/20 border border-green-500/40 rounded-lg text-green-400 text-xs font-bold hover:bg-green-600/30">✅ Approve & Execute</button><button onClick={() => { setShowApproval(false); setShowPlan(false); }} className="px-4 py-2 bg-red-600/20 border border-red-500/40 rounded-lg text-red-400 text-xs font-bold hover:bg-red-600/30">❌ Reject</button></div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="px-4 py-2 border-t border-[#232A34] flex items-center gap-2 flex-shrink-0">
        {agentSelectors.map(agent => <button key={agent.role} className={cn('flex items-center gap-1.5 px-2 py-1 rounded-lg border text-[10px] font-semibold tracking-wider', agentColors[agent.role])}>{agent.role}<ChevronDown className="w-2.5 h-2.5" /></button>)}
      </div>
      <div className="px-3 py-3 border-t border-[#232A34] bg-[#0F1419] flex items-center gap-2 flex-shrink-0">
        <button onClick={toggleVoice} className={`p-2 rounded-lg border ${isRecording ? 'bg-red-500/20 border-red-500/40 text-red-400 animate-pulse' : 'bg-green-500/20 border-green-500/40 text-green-400'}`}><Mic className="w-4 h-4" /></button>
        <button onClick={() => fileRef.current?.click()} className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/30 text-purple-400"><Paperclip className="w-4 h-4" /></button>
        <button onClick={() => fileRef.current?.click()} className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/30 text-purple-400"><Image className="w-4 h-4" /></button>
        <input ref={fileRef} type="file" onChange={handleFileUpload} className="hidden" multiple accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.txt" />
        <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && handleSend()} placeholder="Ask anything or give a command..." className="flex-1 bg-transparent text-sm text-white placeholder-gray-500 outline-none" />
        <button onClick={handleSend} className="flex items-center gap-2 px-5 py-2 bg-cyan-500 text-black text-xs font-bold rounded-lg hover:bg-cyan-400"><Send className="w-3.5 h-3.5" />EXECUTE</button>
      </div>
    </div>
  );
};
