// apps/web/src/components/ChatMessage.tsx

import React from 'react';

interface ChatMessageProps {
  type: 'user' | 'jarvis' | 'system';
  content: string;
  timestamp?: string;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ type, content, timestamp }) => {
  const styles = {
    user: {
      container: 'ml-auto bg-blue-600/20 border border-blue-500/30 rounded-l-lg rounded-tr-lg',
      text: 'text-blue-100',
      label: 'You'
    },
    jarvis: {
      container: 'mr-auto bg-purple-600/20 border border-purple-500/30 rounded-r-lg rounded-tl-lg',
      text: 'text-purple-100',
      label: 'JARVIS'
    },
    system: {
      container: 'mx-auto bg-gray-700/30 border border-gray-600/30 rounded-lg',
      text: 'text-gray-300 text-xs',
      label: 'System'
    }
  }[type];

  return (
    <div className={`flex flex-col ${type === 'user' ? 'items-end' : 'items-start'} mb-3`}>
      <div className={`max-w-[80%] p-4 ${styles.container}`}>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-bold uppercase tracking-wider text-gray-400">
            {styles.label}
          </span>
          {timestamp && (
            <span className="text-[10px] text-gray-500 font-mono">{timestamp}</span>
          )}
        </div>
        <p className={`text-sm leading-relaxed ${styles.text}`}>
          {content}
        </p>
      </div>
    </div>
  );
};