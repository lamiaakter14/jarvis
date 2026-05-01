import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, ArrowUpRight, Paperclip, Image, Zap } from 'lucide-react';

export const MiniChat: React.FC = () => {
  const navigate = useNavigate();
  const [quickInput, setQuickInput] = React.useState('');
  const fileRef = useRef<HTMLInputElement>(null);

  const handleStart = () => {
    if (quickInput.trim()) navigate(`/chat?message=${encodeURIComponent(quickInput.trim())}`);
  };

  return (
    <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4 flex flex-col">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-bold tracking-wider text-gray-300">QUICK CHAT</span>
        <div className="flex gap-2">
          <button onClick={() => navigate('/execute')} className="text-[10px] text-yellow-400 hover:text-yellow-300 flex items-center gap-1">
            <Zap className="w-3 h-3" /> Execute
          </button>
          <button onClick={() => navigate('/chat')} className="text-[10px] text-cyan-400 hover:text-cyan-300 flex items-center gap-1">
            Open Chat <ArrowUpRight className="w-3 h-3" />
          </button>
        </div>
      </div>

      <div className="flex gap-2 mb-3">
        <input type="text" value={quickInput} onChange={e => setQuickInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleStart()}
          placeholder="Type anything..." className="flex-1 bg-[#0A0E14] border border-[#232A34] rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 outline-none focus:border-purple-500" />
        <button onClick={handleStart} className="px-3 py-2 bg-purple-600 text-white rounded-lg text-xs font-bold hover:bg-purple-500">
          <Send className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="flex items-center gap-2 mb-3">
        <button onClick={() => fileRef.current?.click()} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#232A34] text-[10px] text-gray-400 hover:border-purple-500/30 hover:text-purple-400">
          <Paperclip className="w-3.5 h-3.5" /> File
        </button>
        <button onClick={() => fileRef.current?.click()} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#232A34] text-[10px] text-gray-400 hover:border-purple-500/30 hover:text-purple-400">
          <Image className="w-3.5 h-3.5" /> Image
        </button>
        <input ref={fileRef} type="file" className="hidden" multiple accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.txt" />
      </div>

      <div className="flex flex-wrap gap-1.5">
        {['plan project', 'log: today', 'need 5000'].map(cmd => (
          <button key={cmd} onClick={() => navigate(`/chat?message=${encodeURIComponent(cmd)}`)}
            className="text-[9px] text-gray-400 hover:text-white border border-[#232A34] rounded px-2 py-1 hover:border-purple-500/30">{cmd}</button>
        ))}
      </div>
    </div>
  );
};
