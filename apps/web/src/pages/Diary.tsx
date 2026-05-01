import React, { useState, useEffect, useRef } from 'react';
import { BookOpen, Send, Mic, Image, Paperclip, Play, FileText } from 'lucide-react';

export const Diary: React.FC = () => {
  const [text, setText] = useState('');
  const [entries, setEntries] = useState<any[]>([]);
  const [dates, setDates] = useState<string[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [files, setFiles] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch('/api/diary').then(r => r.json()).then(data => {
      setEntries(data.entries || []);
      setDates(data.dates || []);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedDate) {
      fetch(`/api/diary/files/${selectedDate}`).then(r => r.json()).then(data => setFiles(data.files || [])).catch(() => {});
    }
  }, [selectedDate]);

  const handleSave = async () => {
    if (!text.trim()) return;
    try {
      const res = await fetch('/api/diary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      setEntries(prev => [data.entry, ...prev]);
      setText('');
    } catch { alert('Backend not reachable'); }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('/api/diary/upload', { method: 'POST', body: formData });
      const data = await res.json();
      if (selectedDate === data.date) setFiles(prev => [...prev, data.filename]);
      else { setSelectedDate(data.date); }
    } catch { alert('Upload failed'); }
    setUploading(false);
    if (fileRef.current) fileRef.current.value = '';
  };

  return (
    <div className="flex h-full bg-[#0A0E14] text-white">
      <div className="flex-1 flex flex-col max-w-2xl mx-auto p-6">
        <div className="flex items-center gap-3 mb-6">
          <BookOpen className="w-6 h-6 text-purple-400" />
          <h1 className="text-xl font-bold text-purple-400">Digital Diary</h1>
        </div>

        {/* Input */}
        <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4 mb-6">
          <textarea value={text} onChange={e => setText(e.target.value)}
            placeholder="What's on your mind today?"
            className="w-full bg-transparent text-sm text-white placeholder-gray-500 outline-none resize-none h-24 mb-3" />
          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              <button onClick={() => fileRef.current?.click()} className="p-2 rounded-lg bg-purple-600/20 border border-purple-500/30 text-purple-400 hover:bg-purple-600/30" title="Upload image">
                <Image className="w-4 h-4" />
              </button>
              <button onClick={() => fileRef.current?.click()} className="p-2 rounded-lg bg-purple-600/20 border border-purple-500/30 text-purple-400 hover:bg-purple-600/30" title="Upload file">
                <Paperclip className="w-4 h-4" />
              </button>
              <button className="p-2 rounded-lg bg-purple-600/20 border border-purple-500/30 text-purple-400 hover:bg-purple-600/30" title="Voice note">
                <Mic className="w-4 h-4" />
              </button>
              <input ref={fileRef} type="file" onChange={handleUpload} className="hidden" accept="image/*,video/*,audio/*,.pdf,.doc,.docx" />
            </div>
            <div className="flex items-center gap-2">
              {uploading && <span className="text-[10px] text-yellow-400 animate-pulse">Uploading...</span>}
              <button onClick={handleSave} className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg text-sm font-bold hover:bg-purple-500">
                <Send className="w-4 h-4" />Save
              </button>
            </div>
          </div>
        </div>

        {/* Date filter */}
        {dates.length > 0 && (
          <div className="flex gap-2 mb-4 overflow-x-auto">
            {dates.map(d => (
              <button key={d} onClick={() => setSelectedDate(d)}
                className={`px-3 py-1 rounded-lg text-xs border transition-all whitespace-nowrap ${selectedDate === d ? 'bg-purple-600/30 border-purple-500/40 text-purple-400' : 'border-[#232A34] text-gray-400 hover:border-purple-500/30'}`}>{d}</button>
            ))}
          </div>
        )}

        {/* Files */}
        {files.length > 0 && (
          <div className="mb-4">
            <p className="text-[10px] text-gray-400 uppercase mb-2">Files ({files.length})</p>
            <div className="flex flex-wrap gap-2">
              {files.map((f: string) => (
                <a key={f} href={`/api/diary/file/${selectedDate}/${f}`} target="_blank" rel="noreferrer"
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-[#151A22] border border-[#232A34] rounded-lg text-xs text-gray-300 hover:border-purple-500/30 transition-all">
                  {f.match(/\.(jpg|png|gif|webp)$/i) ? <Image className="w-3 h-3" /> : f.match(/\.(mp4|mov)$/i) ? <Play className="w-3 h-3" /> : <FileText className="w-3 h-3" />}
                  {f.substring(7, 30)}...
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Entries */}
        <div className="space-y-3">
          {entries.length === 0 && <p className="text-gray-500 text-sm text-center py-8">No entries yet. Start writing!</p>}
          {entries.map((entry, i) => (
            <div key={i} className="bg-[#151A22] border border-[#232A34] rounded-xl p-4 hover:border-purple-500/30 transition-all">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] text-purple-400 font-mono">{entry.date} {entry.time}</span>
              </div>
              <p className="text-sm text-gray-300">{entry.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
