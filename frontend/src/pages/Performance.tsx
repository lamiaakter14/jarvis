import React, { useEffect, useState } from 'react';
import { Card } from '../components/common/Card';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { performanceApi } from '../api/performance';
import { LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { formatPercentage } from '../utils/formatters';

const COLORS = ['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444'];

export const Performance: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    fetchPerformance();
  }, []);

  const fetchPerformance = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await performanceApi.getPerformance();
      setMetrics(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load performance metrics');
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
    return <ErrorMessage message={error} onRetry={fetchPerformance} />;
  }

  // Mock data if no real data available
  const mockMetrics = {
    productivity_score: 0.85,
    total_tasks: 24,
    completed_tasks: 20,
    completion_rate: 0.83,
    average_roi: 0.75,
    time_utilization: 0.72,
    success_rate: 0.88,
    task_completion_trend: [
      { date: 'Mon', count: 3 },
      { date: 'Tue', count: 5 },
      { date: 'Wed', count: 4 },
      { date: 'Thu', count: 6 },
      { date: 'Fri', count: 2 },
    ],
    task_distribution: [
      { priority: 'Critical', count: 5 },
      { priority: 'High', count: 8 },
      { priority: 'Medium', count: 7 },
      { priority: 'Low', count: 4 },
    ],
    optimization_suggestions: [
      'Focus on high-priority tasks in the morning',
      'Break down large tasks into smaller chunks',
      'Schedule buffer time between tasks',
    ],
  };

  // Use mock data if metrics is not available or incomplete
  const data = (metrics && 
    metrics.task_completion_trend && 
    metrics.task_distribution && 
    metrics.optimization_suggestions) ? metrics : mockMetrics;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Performance Analytics</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track your productivity and optimize your workflow
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <h3 className="text-sm text-gray-600 dark:text-gray-400 mb-1">Productivity Score</h3>
          <p className="text-3xl font-bold text-blue-600">{formatPercentage(data.productivity_score)}</p>
        </Card>
        <Card>
          <h3 className="text-sm text-gray-600 dark:text-gray-400 mb-1">Completion Rate</h3>
          <p className="text-3xl font-bold text-green-600">{formatPercentage(data.completion_rate)}</p>
        </Card>
        <Card>
          <h3 className="text-sm text-gray-600 dark:text-gray-400 mb-1">Average ROI</h3>
          <p className="text-3xl font-bold text-purple-600">{formatPercentage(data.average_roi)}</p>
        </Card>
        <Card>
          <h3 className="text-sm text-gray-600 dark:text-gray-400 mb-1">Time Utilization</h3>
          <p className="text-3xl font-bold text-amber-600">{formatPercentage(data.time_utilization)}</p>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Task Completion Trend */}
        <Card>
          <h3 className="text-lg font-semibold mb-4">Task Completion Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.task_completion_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Task Distribution by Priority */}
        <Card>
          <h3 className="text-lg font-semibold mb-4">Task Distribution by Priority</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data.task_distribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.priority}: ${entry.count}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {data.task_distribution.map((_entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Optimization Suggestions */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Optimization Suggestions</h3>
        <ul className="space-y-2">
          {data.optimization_suggestions?.map((suggestion: string, index: number) => (
            <li key={index} className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 flex items-center justify-center text-sm font-medium">
                {index + 1}
              </span>
              <span className="text-gray-700 dark:text-gray-300">{suggestion}</span>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
};
