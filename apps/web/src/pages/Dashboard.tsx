import React, { useEffect, useState } from 'react';
import { CheckSquare, ListTodo, AlertCircle, Lightbulb } from 'lucide-react';
import { StatsCard } from '../components/dashboard/StatsCard';
import { ActivityFeed } from '../components/dashboard/ActivityFeed';
import { AgentStatusStrip } from '../components/dashboard/AgentStatusStrip';
import { QuickActions } from '../components/dashboard/QuickActions';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { healthApi } from '../api/health';

export const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    knowledgeGaps: 0,
    innovations: 0,
  });
  const [activities, setActivities] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      await healthApi.checkHealth();
      
      // TODO Phase 5: Replace with real API calls
      
      setStats({
        totalTasks: 0,
        completedTasks: 0,
        knowledgeGaps: 0,
        innovations: 0,
      });
      setActivities([]);
      
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 bg-[#0A0E14]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-[#0A0E14] min-h-screen">
        <ErrorMessage message={error} onRetry={fetchDashboardData} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0A0E14] text-[#E0E6ED]">
      <AgentStatusStrip />

      <div className="p-4 sm:p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold font-mono">Dashboard</h1>
          <p className="text-[#8899AA] text-sm mt-1">
            System overview and agent activity monitor
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Total Tasks"
            value={stats.totalTasks}
            change={0}
            icon={CheckSquare}
            color="blue"
          />
          <StatsCard
            title="Completed"
            value={stats.completedTasks}
            change={0}
            icon={ListTodo}
            color="green"
          />
          <StatsCard
            title="Knowledge Gaps"
            value={stats.knowledgeGaps}
            change={0}
            icon={AlertCircle}
            color="amber"
          />
          <StatsCard
            title="Innovations"
            value={stats.innovations}
            change={0}
            icon={Lightbulb}
            color="purple"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <ActivityFeed activities={activities} />
          </div>
          <div>
            <QuickActions />
          </div>
        </div>
      </div>
    </div>
  );
};