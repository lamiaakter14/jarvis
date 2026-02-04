import React, { useEffect, useState } from 'react';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { EmptyState } from '../components/common/EmptyState';
import { Lightbulb } from 'lucide-react';
import { innovationsApi } from '../api/innovations';
import { Innovation } from '../types/innovation';
import { formatRelativeTime, formatPercentage } from '../utils/formatters';

export const Innovations: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [innovations, setInnovations] = useState<Innovation[]>([]);

  useEffect(() => {
    fetchInnovations();
  }, []);

  const fetchInnovations = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await innovationsApi.getInnovations();
      setInnovations(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError(err.message || 'Failed to load innovations');
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
    return <ErrorMessage message={error} onRetry={fetchInnovations} />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Innovations</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Creative ideas and innovative approaches
        </p>
      </div>

      {innovations.length === 0 ? (
        <EmptyState
          title="No innovations yet"
          description="Run the cognitive loop to generate innovative ideas"
          icon={<Lightbulb className="w-16 h-16 text-gray-400 mb-4" />}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {innovations.map((innovation) => (
            <Card key={innovation.id}>
              <div className="flex items-start justify-between mb-3">
                <Lightbulb className="w-6 h-6 text-amber-500 flex-shrink-0" />
                <Badge
                  variant={
                    innovation.implementation_status === 'implemented' ? 'success' :
                    innovation.implementation_status === 'in_progress' ? 'info' :
                    'default'
                  }
                >
                  {innovation.implementation_status}
                </Badge>
              </div>

              <h3 className="text-lg font-semibold mb-2">{innovation.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                {innovation.description}
              </p>

              {innovation.category && (
                <div className="mb-3">
                  <Badge variant="default">{innovation.category}</Badge>
                </div>
              )}

              <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">
                    Impact: {formatPercentage(innovation.impact_score || 0)}
                  </span>
                  <span className="text-gray-500">
                    {formatRelativeTime(innovation.created_at)}
                  </span>
                </div>
              </div>

              {innovation.notes && (
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {innovation.notes}
                  </p>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
