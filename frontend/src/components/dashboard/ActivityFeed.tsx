import React from 'react';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';

interface Activity {
  id: string;
  type: 'task' | 'plan' | 'gap' | 'innovation';
  title: string;
  time: string;
}

interface ActivityFeedProps {
  activities: Activity[];
}

export const ActivityFeed: React.FC<ActivityFeedProps> = ({ activities }) => {
  const getActivityColor = (type: Activity['type']) => {
    switch (type) {
      case 'task': return 'info';
      case 'plan': return 'success';
      case 'gap': return 'warning';
      case 'innovation': return 'default';
      default: return 'default';
    }
  };

  return (
    <Card>
      <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
      <div className="space-y-3">
        {activities.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-4">No recent activity</p>
        ) : (
          activities.map((activity) => (
            <div key={activity.id} className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <Badge variant={getActivityColor(activity.type)}>
                {activity.type}
              </Badge>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{activity.title}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">{activity.time}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </Card>
  );
};
