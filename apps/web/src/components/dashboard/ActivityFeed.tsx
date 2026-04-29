import React, { useState } from 'react';
import { CheckCircle, AlertTriangle, Lightbulb, Settings, Play, RefreshCw } from 'lucide-react';
import { cn } from '../../utils/cn';

type TabType = 'ALL' | 'TASKS' | 'GAPS' | 'INNOVATIONS' | 'SYSTEM';

interface ActivityItem {
  id: string;
  type: 'task_completed' | 'knowledge_gap' | 'innovation' | 'system_update' | 'task_started' | 'reflection';
  title: string;
  subtitle: string;
  time: string;
}

const activities: ActivityItem[] = [
  {
    id: '1',
    type: 'task_completed',
    title: 'Homepage wireframes approved',
    subtitle: 'Task #TSK-023 completed successfully',
    time: '10:31 AM',
  },
  {
    id: '2',
    type: 'knowledge_gap',
    title: 'API rate limit strategy',
    subtitle: 'Need research on optimal rate limiting',
    time: '10:30 AM',
  },
  {
    id: '3',
    type: 'innovation',
    title: 'AI-powered image optimization',
    subtitle: 'New approach can improve load time by 40%',
    time: '10:28 AM',
  },
  {
    id: '4',
    type: 'system_update',
    title: 'Memory index optimized',
    subtitle: 'System performance improved by 12%',
    time: '10:26 AM',
  },
  {
    id: '5',
    type: 'task_started',
    title: 'Performance optimization',
    subtitle: 'Executor agent started working',
    time: '10:25 AM',
  },
  {
    id: '6',
    type: 'reflection',
    title: 'Weekly reflection ready',
    subtitle: 'Your weekly reflection is ready to review',
    time: '10:20 AM',
  },
];

const typeConfig: Record<ActivityItem['type'], {
  label: string;
  labelColor: string;
  icon: React.ElementType;
  iconBg: string;
  iconColor: string;
  tab: TabType;
}> = {
  task_completed: {
    label: 'TASK COMPLETED',
    labelColor: 'text-jarvis-green',
    icon: CheckCircle,
    iconBg: 'bg-jarvis-green/20 border border-jarvis-green/40',
    iconColor: 'text-jarvis-green',
    tab: 'TASKS',
  },
  knowledge_gap: {
    label: 'KNOWLEDGE GAP',
    labelColor: 'text-jarvis-amber',
    icon: AlertTriangle,
    iconBg: 'bg-amber-500/20 border border-amber-500/40',
    iconColor: 'text-jarvis-amber',
    tab: 'GAPS',
  },
  innovation: {
    label: 'INNOVATION',
    labelColor: 'text-jarvis-purple',
    icon: Lightbulb,
    iconBg: 'bg-purple-500/20 border border-purple-500/40',
    iconColor: 'text-jarvis-purple',
    tab: 'INNOVATIONS',
  },
  system_update: {
    label: 'SYSTEM UPDATE',
    labelColor: 'text-jarvis-cyan',
    icon: Settings,
    iconBg: 'bg-jarvis-cyan/20 border border-jarvis-cyan/40',
    iconColor: 'text-jarvis-cyan',
    tab: 'SYSTEM',
  },
  task_started: {
    label: 'TASK STARTED',
    labelColor: 'text-jarvis-green',
    icon: Play,
    iconBg: 'bg-jarvis-green/20 border border-jarvis-green/40',
    iconColor: 'text-jarvis-green',
    tab: 'TASKS',
  },
  reflection: {
    label: 'REFLECTION',
    labelColor: 'text-jarvis-pink',
    icon: RefreshCw,
    iconBg: 'bg-pink-500/20 border border-pink-500/40',
    iconColor: 'text-jarvis-pink',
    tab: 'SYSTEM',
  },
};

const tabs: TabType[] = ['ALL', 'TASKS', 'GAPS', 'INNOVATIONS', 'SYSTEM'];

export const ActivityFeed: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('ALL');

  const filtered =
    activeTab === 'ALL'
      ? activities
      : activities.filter((a) => typeConfig[a.type].tab === activeTab);

  return (
    <div className="bg-jarvis-card border border-jarvis-border rounded-xl flex flex-col h-full overflow-hidden">
      {/* Tabs */}
      <div className="flex border-b border-jarvis-border px-2 pt-2 gap-1 flex-shrink-0">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              'px-3 py-1.5 text-[10px] font-semibold tracking-wider rounded-t transition-all',
              activeTab === tab
                ? 'text-jarvis-cyan border-b-2 border-jarvis-cyan -mb-px bg-jarvis-cyan/5'
                : 'text-jarvis-muted hover:text-jarvis-text'
            )}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Activity list */}
      <div className="flex-1 overflow-y-auto divide-y divide-jarvis-border">
        {filtered.map((item) => {
          const cfg = typeConfig[item.type];
          const Icon = cfg.icon;
          return (
            <div key={item.id} className="flex items-start gap-3 px-4 py-3 hover:bg-white/3 transition-colors">
              <div className={cn('w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5', cfg.iconBg)}>
                <Icon className={cn('w-4 h-4', cfg.iconColor)} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-1 mb-0.5">
                  <span className={cn('text-[9px] font-bold tracking-widest', cfg.labelColor)}>
                    {cfg.label}
                  </span>
                  <span className="text-[9px] text-jarvis-muted flex-shrink-0">{item.time}</span>
                </div>
                <p className="text-xs font-semibold text-jarvis-text leading-tight">{item.title}</p>
                <p className="text-[10px] text-jarvis-muted mt-0.5 leading-tight">{item.subtitle}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* View all */}
      <div className="p-3 border-t border-jarvis-border flex-shrink-0">
        <button className="w-full py-2 text-xs text-jarvis-muted hover:text-jarvis-text border border-jarvis-border hover:border-jarvis-cyan/40 rounded-lg transition-colors">
          View All Activity
        </button>
      </div>
    </div>
  );
};
