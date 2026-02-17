import React from 'react';
import { Target, TrendingUp } from 'lucide-react';
import { Card } from '../common/Card';

interface SkillData {
  name: string;
  proficiency: number;
  priority: number;
  lastPracticed?: string;
  trend?: number;
}

interface SkillGraphProgressPanelProps {
  skills: SkillData[];
  showTopN?: number;
}

export const SkillGraphProgressPanel: React.FC<SkillGraphProgressPanelProps> = ({
  skills,
  showTopN = 5,
}) => {
  // Sort skills by priority and show top N
  const displaySkills = [...skills]
    .sort((a, b) => b.priority - a.priority)
    .slice(0, showTopN);

  const getProficiencyColor = (proficiency: number) => {
    if (proficiency >= 0.8) return 'bg-green-500';
    if (proficiency >= 0.6) return 'bg-blue-500';
    if (proficiency >= 0.4) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Skill Graph Progress</h3>
          <div className="p-2 rounded-full bg-blue-50 dark:bg-blue-900/20">
            <Target className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
        </div>

        {displaySkills.length === 0 ? (
          <div className="text-center py-4 text-gray-500 dark:text-gray-400">
            No skills tracked yet
          </div>
        ) : (
          <div className="space-y-3">
            {displaySkills.map((skill, index) => (
              <div key={index} className="space-y-1">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">{skill.name}</span>
                    {skill.trend !== undefined && skill.trend > 0 && (
                      <TrendingUp className="w-3 h-3 text-green-600" />
                    )}
                  </div>
                  <span className="text-gray-600 dark:text-gray-400">
                    {Math.round(skill.proficiency * 100)}%
                  </span>
                </div>

                {/* Proficiency bar */}
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                    <div
                      className={`h-2 rounded-full ${getProficiencyColor(skill.proficiency)}`}
                      style={{ width: `${skill.proficiency * 100}%` }}
                    />
                  </div>
                  <div className="w-8 h-2 bg-gray-200 rounded-full dark:bg-gray-700">
                    <div
                      className="h-2 rounded-full bg-purple-500"
                      style={{ width: `${skill.priority * 100}%` }}
                      title={`Priority: ${Math.round(skill.priority * 100)}%`}
                    />
                  </div>
                </div>

                {skill.lastPracticed && (
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Last practiced: {skill.lastPracticed}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="text-sm text-gray-600 dark:text-gray-400">
          Tracks proficiency levels and priority weights for key skills.
        </div>
      </div>
    </Card>
  );
};
