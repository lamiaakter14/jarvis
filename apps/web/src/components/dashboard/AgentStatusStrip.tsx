interface AgentStatus {
    name: string;
    state: 'running' | 'idle' | 'analyzing' | 'error';
    description: string;
    color: string;
  }
  
  const defaultAgents: AgentStatus[] = [
    { name: 'STRATEGIST', state: 'idle', description: 'Waiting for plan request', color: '#448AFF' },
    { name: 'MENTOR', state: 'idle', description: 'Waiting for tasks', color: '#FF9100' },
    { name: 'EXECUTOR', state: 'idle', description: 'Waiting for tasks', color: '#00E676' },
    { name: 'INNOVATOR', state: 'idle', description: 'Waiting for context', color: '#B388FF' },
    { name: 'AMPLIFIER', state: 'idle', description: 'No metrics yet', color: '#40C4FF' },
    { name: 'REFLECTOR', state: 'idle', description: 'No baseline yet', color: '#FF80AB' },
  ];
  
  const stateIcons: Record<string, string> = {
    running: '●',
    idle: '◆',
    analyzing: '◈',
    error: '⚠',
  };
  
  export const AgentStatusStrip: React.FC = () => {
    return (
      <div className="bg-[#12171F] border-b border-[#2A3340] px-4 py-2.5">
        <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
          {defaultAgents.map((agent) => (
            <div
              key={agent.name}
              className="bg-[#1A212B] border border-[#2A3340] rounded px-3 py-2"
            >
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className="text-xs" style={{ color: agent.color }}>
                  {stateIcons[agent.state]}
                </span>
                <span className="text-[#E0E6ED] text-[10px] font-bold font-mono">
                  {agent.name}
                </span>
              </div>
              <p className="text-[#556677] text-[9px] font-mono truncate">
                {agent.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  };