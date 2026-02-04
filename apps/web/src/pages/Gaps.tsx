import React, { useEffect, useState } from 'react';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { EmptyState } from '../components/common/EmptyState';
import { AlertCircle } from 'lucide-react';
import { gapsApi } from '../api/gaps';
import { Gap } from '../types/gap';
import { formatRelativeTime } from '../utils/formatters';
import { SEVERITY_COLORS } from '../utils/constants';

export const Gaps: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [gaps, setGaps] = useState<Gap[]>([]);

  useEffect(() => {
    fetchGaps();
  }, []);

  const fetchGaps = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await gapsApi.getGaps();
      setGaps(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError(err.message || 'Failed to load knowledge gaps');
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
    return <ErrorMessage message={error} onRetry={fetchGaps} />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Knowledge Gaps</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Identified areas for learning and improvement
        </p>
      </div>

      {gaps.length === 0 ? (
        <EmptyState
          title="No knowledge gaps identified"
          description="Run the cognitive loop to identify areas for improvement"
          icon={<AlertCircle className="w-16 h-16 text-gray-400 mb-4" />}
        />
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {gaps.map((gap) => (
            <Card key={gap.id}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">{gap.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400">{gap.description}</p>
                </div>
                <Badge
                  variant={
                    gap.severity === 'critical' ? 'error' :
                    gap.severity === 'high' ? 'warning' :
                    gap.severity === 'medium' ? 'info' : 'default'
                  }
                  className={SEVERITY_COLORS[gap.severity]}
                >
                  {gap.severity}
                </Badge>
              </div>

              {gap.evidence && gap.evidence.length > 0 && (
                <div className="mb-3">
                  <h4 className="text-sm font-medium mb-2">Evidence:</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {gap.evidence.map((item, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400">
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {gap.remediation_suggestions && gap.remediation_suggestions.length > 0 && (
                <div className="mb-3">
                  <h4 className="text-sm font-medium mb-2">Remediation Suggestions:</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {gap.remediation_suggestions.map((suggestion, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400">
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                  <span>Priority: {gap.learning_priority_score?.toFixed(1) || 'N/A'}</span>
                  <span>Status: {gap.status}</span>
                </div>
                <span className="text-sm text-gray-500">
                  {formatRelativeTime(gap.created_at)}
                </span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
