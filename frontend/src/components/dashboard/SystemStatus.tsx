import React from 'react';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import { CheckCircle, Circle } from 'lucide-react';

interface Agent {
  name: string;
  status: 'active' | 'idle';
}

interface SystemStatusProps {
  agents: Agent[];
  isHealthy: boolean;
}

export const SystemStatus: React.FC<SystemStatusProps> = ({ agents, isHealthy }) => {
  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">System Status</h3>
        <Badge variant={isHealthy ? 'success' : 'error'}>
          {isHealthy ? 'Healthy' : 'Unhealthy'}
        </Badge>
      </div>
      
      <div className="space-y-3">
        <div className="text-sm font-medium text-gray-700 dark:text-gray-300">Cognitive Agents</div>
        {agents.map((agent) => (
          <div key={agent.name} className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {agent.status === 'active' ? (
                <CheckCircle className="w-4 h-4 text-green-600" />
              ) : (
                <Circle className="w-4 h-4 text-gray-400" />
              )}
              <span className="text-sm">{agent.name}</span>
            </div>
            <Badge variant={agent.status === 'active' ? 'success' : 'default'}>
              {agent.status}
            </Badge>
          </div>
        ))}
      </div>
    </Card>
  );
};
