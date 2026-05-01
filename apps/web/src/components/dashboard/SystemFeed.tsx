import React, { useState, useEffect, useRef } from 'react';
import { Activity, AlertTriangle, Zap, Brain } from 'lucide-react';

interface FeedItem {
  id: string;
  type: 'intent' | 'strategy' | 'validation' | 'execution' | 'memory' | 'system';
  message: string;
  timestamp: string;
  status: 'success' | 'warning' | 'error' | 'info';
}

export const SystemFeed: React.FC = () => {
  const [feed, setFeed] = useState<FeedItem[]>([]);
  const feedEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Simulate live feed
    const items: FeedItem[] = [
      { id: '1', type: 'system', message: 'JARVIS OS v11.0.0 initialized', timestamp: new Date().toLocaleTimeString(), status: 'success' },
      { id: '2', type: 'intent', message: 'Intent Engine V2 active', timestamp: new Date().toLocaleTimeString(), status: 'success' },
      { id: '3', type: 'strategy', message: 'Strategist Agent ready', timestamp: new Date().toLocaleTimeString(), status: 'success' },
      { id: '4', type: 'validation', message: 'Validator Agent online', timestamp: new Date().toLocaleTimeString(), status: 'success' },
      { id: '5', type: 'memory', message: 'Memory Engine connected', timestamp: new Date().toLocaleTimeString(), status: 'success' },
    ];
    setFeed(items);
  }, []);

  const typeIcons: Record<string, React.ReactNode> = {
    intent: <Brain className="w-3 h-3 text-purple-400" />,
    strategy: <Brain className="w-3 h-3 text-purple-400" />,
    validation: <AlertTriangle className="w-3 h-3 text-yellow-400" />,
    execution: <Zap className="w-3 h-3 text-blue-400" />,
    memory: <Activity className="w-3 h-3 text-green-400" />,
    system: <Activity className="w-3 h-3 text-cyan-400" />,
  };

  const statusColors: Record<string, string> = {
    success: 'text-green-400 border-green-500/20',
    warning: 'text-yellow-400 border-yellow-500/20',
    error: 'text-red-400 border-red-500/20',
    info: 'text-cyan-400 border-cyan-500/20',
  };

  return (
    <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="w-4 h-4 text-cyan-400" />
        <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">System Feed</h3>
        <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse ml-auto" />
      </div>

      <div className="space-y-1 max-h-64 overflow-y-auto">
        {feed.map(item => (
          <div key={item.id} className={`flex items-start gap-2 p-2 rounded-lg border-l-2 animate-slide-in ${statusColors[item.status]}`}>
            <span className="mt-0.5">{typeIcons[item.type]}</span>
            <div className="flex-1 min-w-0">
              <p className="text-[10px] text-gray-300">{item.message}</p>
              <span className="text-[8px] text-gray-500">{item.timestamp}</span>
            </div>
          </div>
        ))}
        <div ref={feedEndRef} />
      </div>
    </div>
  );
};
