import React, { useEffect, useState } from 'react';
import { CheckSquare, ListTodo, AlertCircle, Lightbulb } from 'lucide-react';
import { StatsCard } from '../components/dashboard/StatsCard';
import { ActivityFeed } from '../components/dashboard/ActivityFeed';
import { QuickActions } from '../components/dashboard/QuickActions';
import { SystemStatus } from '../components/dashboard/SystemStatus';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { healthApi } from '../api/health';

export const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [healthData, setHealthData] = useState<any>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const health = await healthApi.checkHealth();
      setHealthData(health);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchDashboardData} />;
  }

  // Mock data for demonstration
  const agents = [
    { name: 'Strategist', status: 'idle' as const },
    { name: 'Mentor', status: 'idle' as const },
    { name: 'Executor', status: 'idle' as const },
    { name: 'Innovator', status: 'idle' as const },
    { name: 'Amplifier', status: 'idle' as const },
  ];

  const activities = [
    { id: '1', type: 'task' as const, title: 'Completed task: Review code', time: '2 hours ago' },
    { id: '2', type: 'plan' as const, title: 'Generated daily plan', time: '5 hours ago' },
    { id: '3', type: 'innovation' as const, title: 'New innovation idea added', time: '1 day ago' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Welcome to JARVIS - Your AI Cognitive Assistant
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Tasks"
          value={24}
          change={12}
          icon={CheckSquare}
          color="blue"
        />
        <StatsCard
          title="Completed Today"
          value={8}
          change={20}
          icon={ListTodo}
          color="green"
        />
        <StatsCard
          title="Knowledge Gaps"
          value={5}
          change={-15}
          icon={AlertCircle}
          color="amber"
        />
        <StatsCard
          title="Innovations"
          value={12}
          change={33}
          icon={Lightbulb}
          color="purple"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ActivityFeed activities={activities} />
        </div>
        
        <div className="space-y-6">
          <SystemStatus agents={agents} isHealthy={healthData?.status === 'healthy'} />
          <QuickActions />
        </div>
      </div>
    </div>
  );
};
