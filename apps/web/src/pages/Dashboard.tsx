import React from 'react';
import { Activity, Target, Zap, BarChart3 } from 'lucide-react';
import { StatsCard } from '../components/dashboard/StatsCard';
import { ActivityFeed } from '../components/dashboard/ActivityFeed';
import { QuickCommands } from '../components/dashboard/QuickCommands';
import { MiniChat } from '../components/dashboard/MiniChat';
import { AgentPanel } from '../components/dashboard/AgentPanel';
import { SystemFeed } from '../components/dashboard/SystemFeed';
import { MemoryPanel } from '../components/dashboard/MemoryPanel';

const productivitySparkline = [60, 65, 58, 70, 75, 72, 80, 78, 85, 88, 86, 92];
const tasksSparkline = [80, 95, 100, 92, 108, 110, 115, 112, 120, 118, 125, 128];
const focusSparkline = [70, 72, 68, 75, 78, 74, 80, 82, 79, 85, 86, 87];
const efficiencySparkline = [78, 80, 82, 79, 85, 87, 84, 89, 90, 92, 93, 94];

export const Dashboard: React.FC = () => {
  return (
    <div className="flex flex-col gap-4 p-4 overflow-y-auto" style={{ height: 'calc(100vh - 56px)' }}>
      
      {/* ROW 1: Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 flex-shrink-0">
        <StatsCard title="Productivity Score" value="92.4%" change={12.5} icon={Activity} color="cyan" sparklineData={productivitySparkline} />
        <StatsCard title="Tasks Completed" value={128} change={18.2} icon={Target} color="blue" sparklineData={tasksSparkline} />
        <StatsCard title="Focus Level" value="87%" change={8.1} icon={Zap} color="purple" sparklineData={focusSparkline} />
        <StatsCard title="System Efficiency" value="94.7%" change={14.3} icon={BarChart3} color="orange" sparklineData={efficiencySparkline} />
      </div>

      {/* ROW 2: Agent System + Chat + Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-1 min-h-0">
        
        {/* LEFT COLUMN: Agent Panel + System Feed */}
        <div className="flex flex-col gap-4">
          <AgentPanel />
          <SystemFeed />
        </div>

        {/* CENTER: Quick Commands + Mini Chat */}
        <div className="flex flex-col gap-4">
          <QuickCommands />
          <MiniChat />
        </div>

        {/* RIGHT COLUMN: Memory Panel + Activity Feed */}
        <div className="flex flex-col gap-4">
          <MemoryPanel />
          <ActivityFeed />
        </div>
      </div>

    </div>
  );
};
