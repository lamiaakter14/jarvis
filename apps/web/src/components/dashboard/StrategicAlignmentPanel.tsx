import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Card } from '../common/Card';

interface StrategicAlignmentPanelProps {
  alignmentScore: number;
  trend?: number;
  totalTasks?: number;
  strategicTasks?: number;
}

export const StrategicAlignmentPanel: React.FC<StrategicAlignmentPanelProps> = ({
  alignmentScore,
  trend,
  totalTasks = 0,
  strategicTasks = 0,
}) => {
  const percentage = Math.round(alignmentScore * 100);
  const isPositiveTrend = trend !== undefined && trend >= 0;

  // Color coding based on alignment score
  const getColorClass = () => {
    if (percentage >= 80) return 'text-green-600 dark:text-green-400';
    if (percentage >= 60) return 'text-blue-600 dark:text-blue-400';
    if (percentage >= 40) return 'text-amber-600 dark:text-amber-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getProgressColor = () => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-blue-500';
    if (percentage >= 40) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Strategic Alignment</h3>
          {trend !== undefined && (
            <div className={`flex items-center text-sm ${isPositiveTrend ? 'text-green-600' : 'text-red-600'}`}>
              {isPositiveTrend ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
              {Math.abs(trend)}%
            </div>
          )}
        </div>

        <div>
          <div className="flex items-end justify-between mb-2">
            <div className={`text-4xl font-bold ${getColorClass()}`}>
              {percentage}%
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {strategicTasks} / {totalTasks} tasks aligned
            </div>
          </div>

          {/* Progress bar */}
          <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
            <div
              className={`h-2 rounded-full ${getProgressColor()}`}
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400">
          Measures how well completed tasks align with your primary mission and strategic goals.
        </div>
      </div>
    </Card>
  );
};
