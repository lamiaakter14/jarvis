import React from 'react';
import { FileText } from 'lucide-react';

interface Props {
  messages: Array<{ from: string; time: string; content: string }>;
}

export const ExportPDF: React.FC<Props> = ({ messages }) => {
  const exportChat = () => {
    const text = messages.map(m => `[${m.time}] ${m.from}: ${m.content}`).join('\n\n');
    const blob = new Blob([text], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = `chat-${new Date().toISOString().slice(0,10)}.pdf`; a.click();
  };

  return (
    <button onClick={exportChat} className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/30 text-purple-400" title="Export PDF">
      <FileText className="w-4 h-4" />
    </button>
  );
};
