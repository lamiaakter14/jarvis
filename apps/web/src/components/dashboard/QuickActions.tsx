import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { Brain, Calendar, BarChart3 } from 'lucide-react';

export const QuickActions: React.FC = () => {
  const navigate = useNavigate();

  const actions = [
    {
      label: 'Run Cognitive Loop',
      icon: Brain,
      onClick: () => navigate('/cognitive-loop'),
      variant: 'primary' as const,
    },
    {
      label: 'Generate Plan',
      icon: Calendar,
      onClick: () => navigate('/plans'),
      variant: 'secondary' as const,
    },
    {
      label: 'View Performance',
      icon: BarChart3,
      onClick: () => navigate('/performance'),
      variant: 'secondary' as const,
    },
  ];

  return (
    <Card>
      <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
      <div className="space-y-2">
        {actions.map((action) => {
          const Icon = action.icon;
          return (
            <Button
              key={action.label}
              variant={action.variant}
              className="w-full justify-start"
              onClick={action.onClick}
            >
              <Icon className="w-5 h-5 mr-2" />
              {action.label}
            </Button>
          );
        })}
      </div>
    </Card>
  );
};
