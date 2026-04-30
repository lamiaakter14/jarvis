import React, { useState } from 'react';
import { 
  Target, 
  Clock, 
  TrendingUp, 
  CheckCircle, 
  AlertCircle,
  DollarSign,
  Briefcase,
  Calendar,
  BarChart3,
  Rocket,
  Star,
  Users,
  Zap
} from 'lucide-react';

interface PlanData {
  goal: {
    amount: number;
    days: number;
    daily_target: number;
    hourly_rate: number;
    hours_needed_per_day: number;
    total_hours_needed: number;
  };
  skills: string[];
  recommended_platforms: string[];
  platform_details: Record<string, any>;
  daily_plan: Array<{
    day: number;
    title: string;
    tasks: string[];
    estimated_earnings: number;
    time_needed: number;
  }>;
  tips: string[];
  survival_quote: string;
}

interface ProgressData {
  current: number;
  target: number;
  percentage: number;
  remaining: number;
  status: string;
  message: string;
}

export const MoneyMode: React.FC = () => {
  const [targetAmount, setTargetAmount] = useState<number>(10000);
  const [days, setDays] = useState<number>(7);
  const [skills, setSkills] = useState<string>('graphic_design, content_writing');
  const [plan, setPlan] = useState<PlanData | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [currentIncome, setCurrentIncome] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const generatePlan = async () => {
    setLoading(true);
    setError('');
    
    try {
      const skillsArray = skills.split(',').map(s => s.trim());
      const response = await fetch('/api/money/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_amount: targetAmount,
          days: days,
          skills: skillsArray
        })
      });
      
      if (!response.ok) throw new Error('Plan generation failed');
      const data = await response.json();
      setPlan(data);
      updateProgress(currentIncome, data.goal.amount);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate plan');
    } finally {
      setLoading(false);
    }
  };

  const updateProgress = async (income: number, target?: number) => {
    try {
      const response = await fetch(`/api/money/progress?current=${income}&target=${target || targetAmount}`);
      if (!response.ok) throw new Error('Progress update failed');
      const data = await response.json();
      setProgress(data);
    } catch (err) {
      console.error('Progress update error:', err);
    }
  };

  const handleIncomeUpdate = () => {
    if (plan) {
      updateProgress(currentIncome, plan.goal.amount);
    }
  };

  const platformIcons: Record<string, any> = {
    'Fiverr': Briefcase,
    'Upwork': TrendingUp,
    'Facebook': Users,
    'Local': Star
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header Section */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <DollarSign className="w-8 h-8 text-green-500" />
          <h1 className="text-3xl font-bold">Money Mode 💰</h1>
          <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
            Survival Income Planner
          </span>
        </div>
        <p className="text-gray-400">
          "7 din e 10,000 Taka" — Smart planning + consistent hustle = Goal achieved! 🚀
        </p>
      </div>

      {/* Input Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <label className="flex items-center gap-2 text-gray-300 mb-2">
            <Target className="w-4 h-4" /> Target Amount (BDT)
          </label>
          <input
            type="number"
            value={targetAmount}
            onChange={(e) => setTargetAmount(Number(e.target.value))}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white"
            placeholder="e.g., 10000"
          />
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <label className="flex items-center gap-2 text-gray-300 mb-2">
            <Calendar className="w-4 h-4" /> Days to Achieve
          </label>
          <input
            type="number"
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white"
            placeholder="e.g., 7"
          />
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <label className="flex items-center gap-2 text-gray-300 mb-2">
            <Briefcase className="w-4 h-4" /> Your Skills (comma separated)
          </label>
          <input
            type="text"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white"
            placeholder="graphic_design, content_writing, video_editing"
          />
          <p className="text-xs text-gray-500 mt-2">
            Available: graphic_design, content_writing, video_editing, web_development, data_entry, virtual_assistant, social_media, coding, teaching, photography
          </p>
        </div>
      </div>

      {/* Generate Button */}
      <div className="mb-8">
        <button
          onClick={generatePlan}
          disabled={loading}
          className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 flex items-center gap-2"
        >
          <Rocket className="w-5 h-5" />
          {loading ? 'Generating Plan...' : 'Generate Survival Plan 🎯'}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 mb-6 flex items-center gap-2 text-red-400">
          <AlertCircle className="w-5 h-5" />
          {error}
        </div>
      )}

      {/* Progress Tracker */}
      {plan && progress && (
        <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-6 mb-8 border border-blue-500/30">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5" /> Progress Tracker
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div>
              <p className="text-gray-400 text-sm">Earned</p>
              <p className="text-2xl font-bold text-green-400">৳{progress.current}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Target</p>
              <p className="text-2xl font-bold">৳{progress.target}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Progress</p>
              <p className="text-2xl font-bold text-blue-400">{progress.percentage}%</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Remaining</p>
              <p className="text-2xl font-bold text-yellow-400">৳{progress.remaining}</p>
            </div>
          </div>
          
          <div className="w-full bg-gray-700 rounded-full h-4 mb-3">
            <div 
              className="bg-gradient-to-r from-green-500 to-blue-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(progress.percentage, 100)}%` }}
            />
          </div>
          
          <p className="text-center text-gray-300">{progress.message}</p>
          
          {/* Update Income */}
          <div className="mt-4 flex gap-3">
            <input
              type="number"
              value={currentIncome}
              onChange={(e) => setCurrentIncome(Number(e.target.value))}
              placeholder="Current income earned"
              className="flex-1 bg-gray-900 border border-gray-700 rounded-lg p-2"
            />
            <button
              onClick={handleIncomeUpdate}
              className="bg-blue-600 px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Update
            </button>
          </div>
        </div>
      )}

      {/* Plan Display */}
      {plan && (
        <div className="space-y-6">
          {/* Goal Summary */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-green-500" /> Goal Breakdown
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-gray-400 text-sm">Daily Target</p>
                <p className="text-lg font-semibold">৳{plan.goal.daily_target}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Hourly Rate</p>
                <p className="text-lg font-semibold">৳{plan.goal.hourly_rate}/hr</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Hours/Day</p>
                <p className="text-lg font-semibold">{plan.goal.hours_needed_per_day} hrs</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Total Hours</p>
                <p className="text-lg font-semibold">{plan.goal.total_hours_needed} hrs</p>
              </div>
            </div>
          </div>

          {/* Recommended Platforms */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-purple-500" /> Best Platforms for You
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {plan.recommended_platforms.map((platform) => {
                const Icon = platformIcons[platform] || Briefcase;
                const details = plan.platform_details[platform];
                return (
                  <div key={platform} className="bg-gray-700/50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Icon className="w-5 h-5 text-green-400" />
                      <h3 className="font-semibold">{platform}</h3>
                    </div>
                    {details && (
                      <>
                        <p className="text-sm text-gray-300">Rate: ৳{details.min_rate}-{details.max_rate}</p>
                        <p className="text-sm text-gray-300">Setup: {details.setup_time} hours</p>
                        <p className="text-sm text-green-400">{details.earning_potential} potential</p>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Daily Action Plan */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Clock className="w-5 h-5 text-yellow-500" /> Daily Action Plan
            </h2>
            <div className="space-y-4">
              {plan.daily_plan.map((day) => (
                <div key={day.day} className="border border-gray-700 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="text-lg font-semibold text-green-400">{day.title}</h3>
                    <div className="text-right">
                      <p className="text-sm text-gray-400">⏰ {day.time_needed} hours</p>
                      <p className="text-sm text-green-400">💰 ৳{day.estimated_earnings}</p>
                    </div>
                  </div>
                  <ul className="space-y-2">
                    {day.tasks.map((task, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                        <CheckCircle className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                        <span>{task}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Pro Tips */}
          <div className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-lg p-6 border border-purple-500/30">
            <h2 className="text-xl font-bold mb-3 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-500" /> Survival Tips 🔥
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {plan.tips.map((tip, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <Star className="w-4 h-4 text-yellow-500 mt-0.5" />
                  <span className="text-sm text-gray-300">{tip}</span>
                </div>
              ))}
            </div>
            <p className="mt-4 text-center text-green-400 font-semibold italic">
              "{plan.survival_quote}"
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
