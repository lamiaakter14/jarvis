import React from 'react';
import { Activity } from 'lucide-react';
import { Card } from '../common/Card';

interface MomentumIndexPanelProps {
  momentumIndex: number;
  components?: {
    alignment?: number;
    throughput?: number;
    learning?: number;
  };
}

export const MomentumIndexPanel: React.FC<MomentumIndexPanelProps> = ({
  momentumIndex,
  components = {},
}) => {
  const percentage = Math.round(momentumIndex * 100);

  const getMomentumLevel = () => {
    if (percentage >= 75) return { label: 'Excellent', color: 'text-green-600 dark:text-green-400' };
    if (percentage >= 60) return { label: 'Good', color: 'text-blue-600 dark:text-blue-400' };
    if (percentage >= 40) return { label: 'Moderate', color: 'text-amber-600 dark:text-amber-400' };
    return { label: 'Low', color: 'text-red-600 dark:text-red-400' };
  };

  const level = getMomentumLevel();

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Momentum Index</h3>
          <div className="p-2 rounded-full bg-purple-50 dark:bg-purple-900/20">
            <Activity className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
        </div>

        <div className="flex items-baseline space-x-2">
          <div className={`text-4xl font-bold ${level.color}`}>
            {percentage}
          </div>
          <div className={`text-lg font-medium ${level.color}`}>
            {level.label}
          </div>
        </div>

        {/* Component breakdown */}
        {Object.keys(components).length > 0 && (
          <div className="space-y-2">
            <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
              Components
            </div>
            {components.alignment !== undefined && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Strategic Alignment</span>
                <span className="font-medium">{Math.round(components.alignment * 100)}%</span>
              </div>
            )}
            {components.throughput !== undefined && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Cognitive Throughput</span>
                <span className="font-medium">{components.throughput.toFixed(1)} tasks/hr</span>
              </div>
            )}
            {components.learning !== undefined && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">Learning Velocity</span>
                <span className="font-medium">{components.learning.toFixed(2)}/day</span>
              </div>
            )}
          </div>
        )}

        <div className="text-sm text-gray-600 dark:text-gray-400">
          Combined metric reflecting overall progress and productivity momentum.
        </div>
      </div>
    </Card>
  );
};
