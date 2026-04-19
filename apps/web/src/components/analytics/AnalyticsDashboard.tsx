import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { Activity, TrendingUp, Clock, Target } from 'lucide-react';

interface AnalyticsData {
  taskProgress: Array<{ date: string; completed: number; pending: number; failed: number }>;
  memoryUsage: Array<{ type: string; count: number; size: number }>;
  performanceMetrics: Array<{ timestamp: string; latency: number; throughput: number }>;
  agentActivity: Array<{ agent: string; tasks: number; successRate: number }>;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

export const AnalyticsDashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData>({
    taskProgress: [],
    memoryUsage: [],
    performanceMetrics: [],
    agentActivity: [],
  });
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('7d');

  useEffect(() => {
    fetchAnalyticsData();
    const interval = setInterval(fetchAnalyticsData, 30000);
    return () => clearInterval(interval);
  }, [timeRange]);

  const fetchAnalyticsData = async () => {
    try {
      const mockData: AnalyticsData = {
        taskProgress: generateTaskProgressData(),
        memoryUsage: [
          { type: 'Working', count: 45, size: 2.3 },
          { type: 'Knowledge', count: 128, size: 15.7 },
          { type: 'Strategic', count: 23, size: 4.2 },
          { type: 'Execution Logs', count: 342, size: 8.9 },
          { type: 'ADR', count: 15, size: 1.8 },
        ],
        performanceMetrics: generatePerformanceData(),
        agentActivity: [
          { agent: 'Strategist', tasks: 45, successRate: 98 },
          { agent: 'Executor', tasks: 342, successRate: 94 },
          { agent: 'Mentor', tasks: 128, successRate: 96 },
          { agent: 'Innovator', tasks: 67, successRate: 92 },
          { agent: 'Amplifier', tasks: 89, successRate: 99 },
        ],
      };
      setAnalyticsData(mockData);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch analytics data:', error);
      setLoading(false);
    }
  };

  const generateTaskProgressData = () => {
    const days = timeRange === '24h' ? 24 : timeRange === '7d' ? 7 : 30;
    return Array.from({ length: days }, (_, _i) => ({
      date: `Day ${_i + 1}`,
      completed: Math.floor(Math.random() * 50) + 20,
      pending: Math.floor(Math.random() * 20) + 5,
      failed: Math.floor(Math.random() * 5),
    }));
  };

  const generatePerformanceData = () => {
    const points = timeRange === '24h' ? 24 : timeRange === '7d' ? 7 : 30;
    return Array.from({ length: points }, (_, _i) => ({
      timestamp: `T${_i + 1}`,
      latency: Math.floor(Math.random() * 300) + 100,
      throughput: Math.floor(Math.random() * 1000) + 500,
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Analytics Dashboard</h2>
        <div className="flex gap-2">
          {(['24h', '7d', '30d'] as const).map((range) => (
            <button key={range} onClick={() => setTimeRange(range)} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${timeRange === range ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'}`}>{range}</button>
          ))}
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard icon={<Target className="w-6 h-6" />} title="Total Tasks" value="542" change="+12%" positive />
        <StatCard icon={<Activity className="w-6 h-6" />} title="Success Rate" value="95.3%" change="+2.1%" positive />
        <StatCard icon={<Clock className="w-6 h-6" />} title="Avg Latency" value="245ms" change="-15ms" positive />
        <StatCard icon={<TrendingUp className="w-6 h-6" />} title="Throughput" value="1.2k/s" change="+8%" positive />
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Task Progress Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={analyticsData.taskProgress}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="completed" stackId="1" stroke="#10b981" fill="#10b981" name="Completed" />
            <Area type="monotone" dataKey="pending" stackId="1" stroke="#f59e0b" fill="#f59e0b" name="Pending" />
            <Area type="monotone" dataKey="failed" stackId="1" stroke="#ef4444" fill="#ef4444" name="Failed" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Memory Usage by Type</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={analyticsData.memoryUsage} dataKey="count" nameKey="type" cx="50%" cy="50%" outerRadius={100} label>
                {analyticsData.memoryUsage.map((_, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Agent Activity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.agentActivity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="agent" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="tasks" fill="#3b82f6" name="Tasks" />
              <Bar yAxisId="right" dataKey="successRate" fill="#10b981" name="Success Rate %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

interface StatCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  change: string;
  positive: boolean;
}

const StatCard: React.FC<StatCardProps> = ({ icon, title, value, change, positive }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-gray-500 dark:text-gray-400">{icon}</div>
        <span className={`text-sm font-medium ${positive ? 'text-green-600' : 'text-red-600'}`}>{change}</span>
      </div>
      <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
      <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{value}</p>
    </div>
  );
};
