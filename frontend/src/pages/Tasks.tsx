import React from 'react';
import { EmptyState } from '../components/common/EmptyState';
import { CheckSquare } from 'lucide-react';

export const Tasks: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Tasks</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Manage and organize your tasks
        </p>
      </div>

      <EmptyState
        title="Task management coming soon"
        description="This feature is under development. You can view tasks in the Plans page for now."
        icon={<CheckSquare className="w-16 h-16 text-gray-400 mb-4" />}
      />
    </div>
  );
};
