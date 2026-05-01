import React, { useState, useEffect } from 'react';
import { Database, Lightbulb } from 'lucide-react';

export const MemoryPanel: React.FC = () => {
  const [patterns, setPatterns] = useState<any>(null);

  useEffect(() => {
    fetch('/api/memory/patterns').then(r => r.json()).then(setPatterns).catch(() => {});
  }, []);

  if (!patterns) return null;

  return (
    <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4">
      <div className="flex items-center gap-2 mb-4">
        <Database className="w-4 h-4 text-green-400" />
        <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">Memory Engine</h3>
        {patterns.total_interactions > 0 && (
          <span className="text-[10px] text-green-400 ml-auto">{patterns.total_interactions} interactions</span>
        )}
      </div>

      {patterns.insights?.length > 0 && (
        <div className="space-y-2 mb-3">
          {patterns.insights.map((insight: string, i: number) => (
            <div key={i} className="flex items-center gap-2 p-2 bg-[#0A0E14] rounded-lg border border-[#232A34]">
              <Lightbulb className="w-3 h-3 text-yellow-400" />
              <p className="text-[10px] text-gray-300">{insight}</p>
            </div>
          ))}
        </div>
      )}

      {patterns.favorite_intent && (
        <div className="grid grid-cols-2 gap-2 text-[10px]">
          <div className="p-2 bg-[#0A0E14] rounded-lg text-center">
            <p className="text-gray-500">Top Intent</p>
            <p className="text-purple-400 font-bold">{patterns.favorite_intent}</p>
          </div>
          <div className="p-2 bg-[#0A0E14] rounded-lg text-center">
            <p className="text-gray-500">Top Domain</p>
            <p className="text-cyan-400 font-bold">{patterns.top_domain}</p>
          </div>
          <div className="p-2 bg-[#0A0E14] rounded-lg text-center col-span-2">
            <p className="text-gray-500">Success Rate</p>
            <p className="text-green-400 font-bold">{patterns.success_rate}%</p>
          </div>
        </div>
      )}
    </div>
  );
};
