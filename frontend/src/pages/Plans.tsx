import React, { useEffect, useState } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { EmptyState } from '../components/common/EmptyState';
import { Calendar, Plus } from 'lucide-react';
import { plansApi } from '../api/plans';
import { formatHours } from '../utils/formatters';
import { STATUS_COLORS, PRIORITY_COLORS } from '../utils/constants';
import toast from 'react-hot-toast';

export const Plans: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [plan, setPlan] = useState<any>(null);

  useEffect(() => {
    fetchTodayPlan();
  }, []);

  const fetchTodayPlan = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await plansApi.getTodayPlan();
      setPlan(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load plan');
    } finally {
      setLoading(false);
    }
  };

  const generateNewPlan = async () => {
    try {
      toast.loading('Generating plan...', { id: 'gen-plan' });
      const data = await plansApi.generatePlan();
      setPlan(data);
      toast.success('Plan generated successfully!', { id: 'gen-plan' });
    } catch (err: any) {
      toast.error('Failed to generate plan', { id: 'gen-plan' });
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
    return <ErrorMessage message={error} onRetry={fetchTodayPlan} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Daily Plans</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your daily tasks and objectives
          </p>
        </div>
        <Button onClick={generateNewPlan}>
          <Plus className="w-5 h-5 mr-2" />
          Generate Plan
        </Button>
      </div>

      {!plan || !plan.tasks || plan.tasks.length === 0 ? (
        <EmptyState
          title="No plan for today"
          description="Generate a new plan to get started with your daily tasks"
          action={{
            label: 'Generate Plan',
            onClick: generateNewPlan,
          }}
          icon={<Calendar className="w-16 h-16 text-gray-400 mb-4" />}
        />
      ) : (
        <div className="space-y-6">
          {/* Plan Overview */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Today's Plan</h2>
              <Badge variant="info">{plan.date}</Badge>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</p>
                <p className="text-2xl font-bold">{plan.tasks?.length || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Estimated Hours</p>
                <p className="text-2xl font-bold">{formatHours(plan.total_estimated_hours || 0)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Completion Rate</p>
                <p className="text-2xl font-bold">{Math.round((plan.completion_rate || 0) * 100)}%</p>
              </div>
            </div>
          </Card>

          {/* Task List */}
          <Card>
            <h3 className="text-lg font-semibold mb-4">Tasks</h3>
            <div className="space-y-3">
              {plan.tasks?.map((task: any, index: number) => (
                <div
                  key={task.id || index}
                  className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50"
                >
                  <input
                    type="checkbox"
                    checked={task.status === 'done'}
                    className="w-5 h-5 rounded border-gray-300"
                    readOnly
                  />
                  <div className="flex-1">
                    <h4 className="font-medium">{task.title}</h4>
                    {task.description && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {task.description}
                      </p>
                    )}
                    <div className="flex gap-2 mt-2">
                      {task.priority && (
                        <Badge variant="default" className={PRIORITY_COLORS[task.priority as keyof typeof PRIORITY_COLORS]}>
                          {task.priority}
                        </Badge>
                      )}
                      {task.status && (
                        <Badge variant="default" className={STATUS_COLORS[task.status as keyof typeof STATUS_COLORS]}>
                          {task.status}
                        </Badge>
                      )}
                      {task.estimated_hours && (
                        <Badge variant="default">
                          {formatHours(task.estimated_hours)}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
