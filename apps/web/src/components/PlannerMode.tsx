// apps/web/src/components/PlannerMode.tsx

import React, { useState } from 'react';
import { PLANNER_QUESTIONS, MOCK_PLAN } from './IntentDetector';

interface PlannerModeProps {
  onGeneratePlan: (plan: typeof MOCK_PLAN) => void;
}

export const PlannerMode: React.FC<PlannerModeProps> = ({ onGeneratePlan }) => {
  const [showQuestions, setShowQuestions] = useState(false);
  const [showPlan, setShowPlan] = useState(false);
  const [answers, setAnswers] = useState<Record<number, string>>({});

  const handleStartPlanning = () => setShowQuestions(true);

  const handleGeneratePlan = () => {
    setShowPlan(true);
    onGeneratePlan(MOCK_PLAN);
  };

  return (
    <div className="bg-[#151A22] border border-[#232A34] rounded p-4 my-3">
      {/* Planner Badge */}
      <div className="flex items-center gap-2 mb-4">
        <span className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" />
        <span className="text-xs font-bold uppercase tracking-wider text-purple-400">
          🧠 Planner Mode Active
        </span>
      </div>

      {!showQuestions && (
        <div className="text-center py-4">
          <p className="text-sm text-gray-300 mb-4">
            Planner detected your intent. Ready to create a structured plan?
          </p>
          <button
            onClick={handleStartPlanning}
            className="px-6 py-2 bg-purple-600 text-white rounded text-sm font-bold 
                       hover:bg-purple-500 transition-colors"
          >
            Start Planning →
          </button>
        </div>
      )}

      {/* Question Layer */}
      {showQuestions && !showPlan && (
        <div className="space-y-3">
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-3">Mandatory Questions</p>
          {PLANNER_QUESTIONS.map((q, i) => (
            <div key={i} className="space-y-1">
              <label className="text-xs text-gray-300">{q}</label>
              <input
                type="text"
                value={answers[i] || ''}
                onChange={(e) => setAnswers({ ...answers, [i]: e.target.value })}
                className="w-full bg-[#0A0E14] border border-[#232A34] rounded px-3 py-2 
                           text-sm text-white font-mono focus:border-purple-500 outline-none"
                placeholder="Your answer..."
              />
            </div>
          ))}
          <button
            onClick={handleGeneratePlan}
            className="w-full py-2 bg-purple-600 text-white rounded text-sm font-bold 
                       hover:bg-purple-500 transition-colors mt-3"
          >
            ⚡ Generate Plan
          </button>
        </div>
      )}

      {/* Plan Output */}
      {showPlan && (
        <div className="space-y-3">
          <div className="bg-[#0A0E14] rounded p-3 border border-[#232A34]">
            <p className="text-sm font-bold text-white mb-1">📁 {MOCK_PLAN.projectName}</p>
            <p className="text-[10px] text-gray-500 font-mono">ID: {MOCK_PLAN.projectId}</p>
          </div>

          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">Phases</p>
            {MOCK_PLAN.phases.map(p => (
              <div key={p.id} className="flex items-center gap-2 py-1">
                <span className="text-gray-500">⬜</span>
                <span className="text-sm text-gray-300">{p.id}. {p.name}</span>
              </div>
            ))}
          </div>

          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">Tasks</p>
            {MOCK_PLAN.tasks.map(t => (
              <div key={t.id} className="flex items-center gap-2 py-1">
                <span className="text-[10px] text-blue-400 font-mono">{t.id}</span>
                <span className="text-sm text-gray-300">{t.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};