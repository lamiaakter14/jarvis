import React, { useState, useEffect } from 'react';
import { Brain, Shield, Zap, Database, MessageSquare, Check, AlertTriangle, Clock } from 'lucide-react';

interface AgentStatus {
  name: string;
  status: string;
  version: string;
}

export const AgentPanel: React.FC = () => {
  const [agents, setAgents] = useState<AgentStatus[]>([]);
  const [pipeline, setPipeline] = useState('');
  const [systemStatus, setSystemStatus] = useState('loading');

  useEffect(() => {
    fetch('/api/os/agents')
      .then(r => r.json())
      .then(data => {
        setAgents(data.agents || []);
        setPipeline(data.pipeline || '');
        setSystemStatus('operational');
      })
      .catch(() => setSystemStatus('offline'));
  }, []);

  const agentIcons: Record<string, React.ReactNode> = {
    Strategist: <Brain className="w-4 h-4 text-purple-400" />,
    Validator: <Shield className="w-4 h-4 text-yellow-400" />,
    Executor: <Zap className="w-4 h-4 text-blue-400" />,
    'Memory Engine': <Database className="w-4 h-4 text-green-400" />,
    Communicator: <MessageSquare className="w-4 h-4 text-cyan-400" />,
  };

  return (
    <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">🤖 Agent System</h3>
        <span className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold ${
          systemStatus === 'operational' ? 'bg-green-500/10 text-green-400 border border-green-500/30' : 'bg-red-500/10 text-red-400'
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${systemStatus === 'operational' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
          {systemStatus.toUpperCase()}
        </span>
      </div>

      {/* Pipeline */}
      <div className="mb-4 p-3 bg-[#0A0E14] rounded-lg border border-[#232A34]">
        <p className="text-[10px] text-gray-500 mb-2">Active Pipeline</p>
        <div className="flex items-center gap-1 text-[9px] text-gray-400 flex-wrap">
          {['Intent', 'Strategy', 'Validation', 'Approval', 'Execution', 'Memory'].map((step, i) => (
            <React.Fragment key={step}>
              <span className="px-2 py-1 bg-[#151A22] rounded border border-[#232A34]">{step}</span>
              {i < 5 && <span className="text-purple-400">→</span>}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Agent Cards */}
      <div className="space-y-2">
        {agents.map(agent => (
          <div key={agent.name} className="flex items-center justify-between p-3 bg-[#0A0E14] rounded-lg border border-[#232A34] hover:border-purple-500/30 transition-all">
            <div className="flex items-center gap-3">
              {agentIcons[agent.name] || <Zap className="w-4 h-4 text-gray-400" />}
              <div>
                <p className="text-xs font-bold text-gray-300">{agent.name}</p>
                <p className="text-[9px] text-gray-500">v{agent.version}</p>
              </div>
            </div>
            <span className="flex items-center gap-1.5 text-[10px] text-green-400">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
              {agent.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
