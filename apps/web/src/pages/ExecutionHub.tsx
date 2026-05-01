import React, { useState, useEffect } from 'react';
import { Zap, FileText, GitBranch, Download, Check, X, AlertTriangle } from 'lucide-react';

export const ExecutionHub: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'files' | 'github' | 'pdf'>('files');
  const [gitStatus, setGitStatus] = useState('');
  const [commitMsg, setCommitMsg] = useState('');
  const [filePath, setFilePath] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [pdfData, setPdfData] = useState({ template: 'invoice', client: '', amount: '' });
  const [log, setLog] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/execute/queue').then(r => r.json()).then(d => setLog(d.log || [])).catch(() => {});
    fetch('/api/execute/github/status').then(r => r.json()).then(d => setGitStatus(d.output || '')).catch(() => {});
  }, []);

  const handleGitCommit = async () => {
    const res = await fetch('/api/execute/github/commit', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: commitMsg || 'JARVIS update' })
    });
    const data = await res.json();
    alert(data.status === 'success' ? '✅ Committed!' : '❌ ' + data.message);
    setCommitMsg('');
  };

  const handleCreateFile = async () => {
    const res = await fetch('/api/execute/file/create', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: filePath, content: fileContent })
    });
    const data = await res.json();
    alert(data.status === 'success' ? '✅ File created!' : '❌ ' + data.message);
  };

  const handleGeneratePDF = async () => {
    const res = await fetch('/api/execute/pdf/generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ template: pdfData.template, data: { Client: pdfData.client, Amount: pdfData.amount } })
    });
    const data = await res.json();
    alert(data.status === 'success' ? `✅ PDF: ${data.filename}` : '❌ ' + data.message);
  };

  const tabs = [
    { id: 'files' as const, icon: FileText, label: 'Files' },
    { id: 'github' as const, icon: GitBranch, label: 'GitHub' },
    { id: 'pdf' as const, icon: Download, label: 'PDF Export' },
  ];

  return (
    <div className="flex flex-col h-full p-6">
      <div className="flex items-center gap-3 mb-6">
        <Zap className="w-6 h-6 text-yellow-400" />
        <h1 className="text-xl font-bold text-yellow-400">Execution Hub</h1>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {tabs.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === tab.id ? 'bg-purple-600 text-white' : 'bg-[#151A22] text-gray-400 border border-[#232A34] hover:border-purple-500/30'}`}>
            <tab.icon className="w-4 h-4" /> {tab.label}
          </button>
        ))}
      </div>

      {/* Files Tab */}
      {activeTab === 'files' && (
        <div className="space-y-4">
          <input value={filePath} onChange={e => setFilePath(e.target.value)} placeholder="File path (e.g., blog-post.md)"
            className="w-full bg-[#151A22] border border-[#232A34] rounded-lg px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:border-purple-500" />
          <textarea value={fileContent} onChange={e => setFileContent(e.target.value)} placeholder="File content..."
            className="w-full bg-[#151A22] border border-[#232A34] rounded-lg px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:border-purple-500 h-32" />
          <button onClick={handleCreateFile} className="px-6 py-2 bg-green-600 text-white rounded-lg text-sm font-bold hover:bg-green-500">
            ✅ Create File
          </button>
        </div>
      )}

      {/* GitHub Tab */}
      {activeTab === 'github' && (
        <div className="space-y-4">
          <div className="bg-[#151A22] border border-[#232A34] rounded-lg p-4">
            <p className="text-xs text-gray-400 uppercase mb-2">Git Status</p>
            <pre className="text-sm text-gray-300 font-mono">{gitStatus || 'Loading...'}</pre>
          </div>
          <input value={commitMsg} onChange={e => setCommitMsg(e.target.value)} placeholder="Commit message..."
            className="w-full bg-[#151A22] border border-[#232A34] rounded-lg px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:border-purple-500" />
          <button onClick={handleGitCommit} className="px-6 py-2 bg-purple-600 text-white rounded-lg text-sm font-bold hover:bg-purple-500">
            🔀 Commit All Changes
          </button>
        </div>
      )}

      {/* PDF Tab */}
      {activeTab === 'pdf' && (
        <div className="space-y-4">
          <select value={pdfData.template} onChange={e => setPdfData({ ...pdfData, template: e.target.value })}
            className="w-full bg-[#151A22] border border-[#232A34] rounded-lg px-4 py-3 text-sm text-white outline-none focus:border-purple-500">
            <option value="invoice">Invoice</option>
            <option value="report">Report</option>
            <option value="proposal">Proposal</option>
          </select>
          <input value={pdfData.client} onChange={e => setPdfData({ ...pdfData, client: e.target.value })} placeholder="Client name"
            className="w-full bg-[#151A22] border border-[#232A34] rounded-lg px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:border-purple-500" />
          <input value={pdfData.amount} onChange={e => setPdfData({ ...pdfData, amount: e.target.value })} placeholder="Amount"
            className="w-full bg-[#151A22] border border-[#232A34] rounded-lg px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:border-purple-500" />
          <button onClick={handleGeneratePDF} className="px-6 py-2 bg-yellow-600 text-white rounded-lg text-sm font-bold hover:bg-yellow-500">
            📄 Generate {pdfData.template}
          </button>
        </div>
      )}

      {/* Activity Log */}
      <div className="mt-8">
        <p className="text-xs text-gray-400 uppercase mb-3">Recent Activity</p>
        <div className="space-y-1">
          {log.slice(-5).reverse().map((entry: any, i: number) => (
            <div key={i} className="flex items-center gap-2 text-xs text-gray-400">
              <span className={entry.status === 'success' ? 'text-green-400' : 'text-red-400'}>
                {entry.status === 'success' ? '✅' : '❌'}
              </span>
              <span className="text-gray-500">{entry.timestamp?.slice(11, 19)}</span>
              <span>{entry.action}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
