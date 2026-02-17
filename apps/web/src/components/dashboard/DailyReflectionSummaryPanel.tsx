import React from 'react';
import { FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { Card } from '../common/Card';

interface CorrectionAction {
  priority: number;
  title: string;
  description: string;
  expectedImpact: string;
}

interface DailyReflectionSummaryPanelProps {
  reflectionDate: string;
  driftLevel: 'none' | 'minor' | 'moderate' | 'critical';
  completionRate: number;
  strategicAlignment: number;
  correctionActions: CorrectionAction[];
  patternFlags?: string[];
}

export const DailyReflectionSummaryPanel: React.FC<DailyReflectionSummaryPanelProps> = ({
  reflectionDate,
  driftLevel,
  completionRate,
  strategicAlignment,
  correctionActions,
  patternFlags = [],
}) => {
  const getDriftLevelInfo = () => {
    switch (driftLevel) {
      case 'critical':
        return { label: 'Critical Drift', color: 'text-red-600 dark:text-red-400', icon: AlertCircle };
      case 'moderate':
        return { label: 'Moderate Drift', color: 'text-amber-600 dark:text-amber-400', icon: AlertCircle };
      case 'minor':
        return { label: 'Minor Drift', color: 'text-blue-600 dark:text-blue-400', icon: AlertCircle };
      default:
        return { label: 'On Track', color: 'text-green-600 dark:text-green-400', icon: CheckCircle };
    }
  };

  const driftInfo = getDriftLevelInfo();
  const DriftIcon = driftInfo.icon;

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Daily Reflection</h3>
          <div className="p-2 rounded-full bg-purple-50 dark:bg-purple-900/20">
            <FileText className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400">
          {reflectionDate}
        </div>

        {/* Drift Status */}
        <div className="flex items-center space-x-2">
          <DriftIcon className={`w-5 h-5 ${driftInfo.color}`} />
          <span className={`font-medium ${driftInfo.color}`}>
            {driftInfo.label}
          </span>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-4 py-3 border-t border-b dark:border-gray-700">
          <div>
            <div className="text-xs text-gray-500 dark:text-gray-400 uppercase">Completion</div>
            <div className="text-2xl font-bold">{Math.round(completionRate * 100)}%</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 dark:text-gray-400 uppercase">Alignment</div>
            <div className="text-2xl font-bold">{Math.round(strategicAlignment * 100)}%</div>
          </div>
        </div>

        {/* Pattern Flags */}
        {patternFlags.length > 0 && (
          <div className="space-y-2">
            <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
              Patterns Detected
            </div>
            <div className="space-y-1">
              {patternFlags.map((flag, index) => (
                <div key={index} className="text-sm text-amber-600 dark:text-amber-400 flex items-start">
                  <span className="mr-2">•</span>
                  <span>{flag}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Correction Actions */}
        {correctionActions.length > 0 && (
          <div className="space-y-2">
            <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
              Top Corrections
            </div>
            <div className="space-y-2">
              {correctionActions.slice(0, 3).map((action, index) => (
                <div key={index} className="p-2 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="flex items-start space-x-2">
                    <span className="flex-shrink-0 w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 text-xs flex items-center justify-center font-medium">
                      {action.priority}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium">{action.title}</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {action.description.length > 80
                          ? `${action.description.substring(0, 80)}...`
                          : action.description}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};
