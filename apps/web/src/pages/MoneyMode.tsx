import React, { useState, useEffect } from 'react';
import { Download, TrendingUp, Target, Clock, Zap, CheckCircle } from 'lucide-react';

export const MoneyMode: React.FC = () => {
  const [targetAmount, setTargetAmount] = useState(10000);
  const [days, setDays] = useState(7);
  const [skills, setSkills] = useState('graphic_design, content_writing');
  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentIncome, setCurrentIncome] = useState(0);
  const [progress, setProgress] = useState<any>(null);
  const [dailyChecklist, setDailyChecklist] = useState<Record<number, boolean>>({});

  useEffect(() => {
    const saved = localStorage.getItem('moneyMode_progress');
    if (saved) {
      const data = JSON.parse(saved);
      setCurrentIncome(data.currentIncome || 0);
      setDailyChecklist(data.dailyChecklist || {});
    }
  }, []);

  useEffect(() => {
    if (currentIncome > 0 || Object.keys(dailyChecklist).length > 0) {
      localStorage.setItem('moneyMode_progress', JSON.stringify({
        currentIncome,
        dailyChecklist
      }));
    }
  }, [currentIncome, dailyChecklist]);

  const generatePlan = async () => {
    setLoading(true);
    setError('');
    
    const skillsArray = skills.split(',').map(s => s.trim());
    
    try {
      const response = await fetch('/api/money/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_amount: targetAmount,
          days: days,
          skills: skillsArray
        })
      });
      
      const data = await response.json();
      const planData = data.status === 'success' ? data.plan : data;
      setPlan(planData);
      updateProgress(currentIncome, targetAmount);
    } catch (err) {
      setError('Failed to generate plan');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateProgress = async (income: number, target?: number) => {
    try {
      const response = await fetch(`/api/money/progress?current=${income}&target=${target || targetAmount}`);
      const data = await response.json();
      setProgress(data);
    } catch (err) {
      console.error('Progress update error:', err);
    }
  };

  const handleIncomeUpdate = () => {
    updateProgress(currentIncome, targetAmount);
    if (plan && currentIncome >= targetAmount) {
      alert('🎉 GOAL ACHIEVED! 🎉\n\nYou did it! 7 din e 10,000 Taka possible!');
    }
  };

  const toggleDailyTask = (day: number) => {
    setDailyChecklist(prev => ({
      ...prev,
      [day]: !prev[day]
    }));
  };

  const exportToPDF = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Money Mode Survival Plan - JARVIS OS</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
          h1 { color: #10b981; }
          .goal-box { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0; }
          .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 20px 0; }
          .day-plan { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
          .tips { background: #e0e7ff; padding: 15px; border-radius: 8px; margin: 20px 0; }
          @media print { body { margin: 0; padding: 20px; } }
        </style>
      </head>
      <body>
        <h1>💰 Money Mode Survival Plan</h1>
        <p><strong>Generated for:</strong> Mahedi Muktadir | <strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
        
        <div class="goal-box">
          <h2>🎯 Goal: ${targetAmount} BDT in ${days} days</h2>
          <div class="grid">
            <div><strong>Daily Target:</strong> ${plan?.goal?.daily_target || 'N/A'} BDT</div>
            <div><strong>Hourly Rate:</strong> ${plan?.goal?.hourly_rate || 'N/A'} BDT/hr</div>
            <div><strong>Hours/Day:</strong> ${plan?.goal?.hours_needed_per_day || 'N/A'} hrs</div>
            <div><strong>Total Hours:</strong> ${plan?.goal?.total_hours_needed || 'N/A'} hrs</div>
          </div>
          ${progress ? `<div><strong>Progress:</strong> ${progress.percentage}% (${currentIncome}/${targetAmount} BDT)</div>` : ''}
        </div>

        <h2>📋 Daily Action Plan</h2>
        ${plan?.daily_plan?.map((day: any) => `
          <div class="day-plan">
            <h3>${day.title}</h3>
            <ul>
              ${day.tasks?.map((task: string) => `<li>${task}</li>`).join('')}
            </ul>
            <p><strong>Time needed:</strong> ${day.time_needed} hours | <strong>Est. earnings:</strong> ${day.estimated_earnings} BDT</p>
          </div>
        `).join('') || '<p>No plan generated yet</p>'}

        <div class="tips">
          <h3>💡 Pro Survival Tips</h3>
          <ul>
            ${plan?.tips?.map((tip: string) => `<li>${tip}</li>`).join('') || '<li>Generate plan to see tips</li>'}
          </ul>
          <p style="text-align: center; margin-top: 20px;"><em>${plan?.survival_quote || 'Hustle now, shine later! 💪'}</em></p>
        </div>

        <footer style="margin-top: 40px; text-align: center; color: #666;">
          <p>Generated by JARVIS OS v5.3.0 | Sakhipur, Bangladesh</p>
        </footer>
      </body>
      </html>
    `;
    
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.print();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Money Mode 💰</h1>
        <p className="text-gray-400">"7 din e 10,000 Taka" — Smart planning + consistent hustle = Goal achieved!</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-sm text-gray-400 mb-2">Target Amount (BDT)</label>
          <input
            type="number"
            value={targetAmount}
            onChange={(e) => setTargetAmount(Number(e.target.value))}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-2">Days to Achieve</label>
          <input
            type="number"
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-2">Your Skills (comma separated)</label>
          <input
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white"
          />
        </div>
      </div>

      <div className="flex gap-4 mb-6">
        <button
          onClick={generatePlan}
          disabled={loading}
          className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg font-semibold transition-all disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate Survival Plan 🚀'}
        </button>
        
        <button
          onClick={exportToPDF}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2"
        >
          <Download className="w-4 h-4" /> Export as PDF
        </button>
      </div>

      {error && (
        <div className="mt-4 bg-red-500/20 border border-red-500 rounded-lg p-3 text-red-400">
          ❌ {error}
        </div>
      )}

      <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-6 mb-8 border border-blue-500/30">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" /> Progress Tracker
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <p className="text-gray-400 text-sm">Earned</p>
            <p className="text-2xl font-bold text-green-400">৳{currentIncome}</p>
          </div>
          <div>
            <p className="text-gray-400 text-sm">Target</p>
            <p className="text-2xl font-bold">৳{targetAmount}</p>
          </div>
          <div>
            <p className="text-gray-400 text-sm">Progress</p>
            <p className="text-2xl font-bold text-blue-400">{progress?.percentage || 0}%</p>
          </div>
          <div>
            <p className="text-gray-400 text-sm">Remaining</p>
            <p className="text-2xl font-bold text-yellow-400">৳{Math.max(0, targetAmount - currentIncome)}</p>
          </div>
        </div>
        
        <div className="w-full bg-gray-700 rounded-full h-4 mb-3">
          <div 
            className="bg-gradient-to-r from-green-500 to-blue-500 h-4 rounded-full transition-all duration-500"
            style={{ width: `${Math.min(progress?.percentage || 0, 100)}%` }}
          />
        </div>
        
        <p className="text-center text-gray-300 mb-4">{progress?.message || 'Start earning to see progress!'}</p>
        
        <div className="flex gap-3">
          <input
            type="number"
            value={currentIncome}
            onChange={(e) => setCurrentIncome(Number(e.target.value))}
            placeholder="Today's earnings"
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg p-2"
          />
          <button
            onClick={handleIncomeUpdate}
            className="bg-blue-600 px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Update Progress
          </button>
        </div>

        <div className="mt-3">
          <button
            onClick={() => {
              if (confirm('Reset all progress? This cannot be undone.')) {
                setCurrentIncome(0);
                setDailyChecklist({});
                localStorage.removeItem('moneyMode_progress');
                updateProgress(0, targetAmount);
              }
            }}
            className="bg-red-600/20 text-red-400 px-4 py-2 rounded-lg hover:bg-red-600/30 transition-all text-sm"
          >
            Reset Progress 🔄
          </button>
        </div>
      </div>

      {plan && plan.goal && (
        <>
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-green-500" /> Goal Breakdown
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-gray-400 text-sm">Daily Target</p>
                <p className="text-2xl font-bold text-green-400">৳{plan.goal.daily_target}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Hourly Rate</p>
                <p className="text-2xl font-bold text-blue-400">৳{plan.goal.hourly_rate}/hr</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Hours/Day</p>
                <p className="text-2xl font-bold text-yellow-400">{plan.goal.hours_needed_per_day} hrs</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Platforms</p>
                <p className="text-lg font-semibold">{plan.recommended_platforms?.join(', ')}</p>
              </div>
            </div>
          </div>

          <div className="mb-6 bg-gradient-to-r from-green-900/30 to-emerald-900/30 rounded-lg p-4 border border-green-500/30">
            <h3 className="font-bold mb-2 flex items-center gap-2">
              <span className="text-green-400">🎯 Today's Focus</span>
            </h3>
            <p className="text-sm text-gray-300">
              {plan.daily_plan?.[0]?.tasks?.[0] || "Complete platform setup"}
            </p>
            <div className="mt-2 flex justify-between text-xs text-gray-400">
              <span>Goal: ৳{Math.ceil(targetAmount/days)}/day</span>
              <span>Current: ৳{currentIncome}</span>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Clock className="w-5 h-5 text-yellow-500" /> Daily Action Plan
            </h2>
            <div className="space-y-4">
              {plan.daily_plan?.map((day: any) => (
                <div key={day.day} className="border border-gray-700 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1">
                      <button
                        onClick={() => toggleDailyTask(day.day)}
                        className={`mt-1 w-5 h-5 rounded border-2 flex items-center justify-center ${
                          dailyChecklist[day.day] 
                            ? 'bg-green-500 border-green-500' 
                            : 'border-gray-500 hover:border-green-500'
                        }`}
                      >
                        {dailyChecklist[day.day] && <CheckCircle className="w-4 h-4 text-white" />}
                      </button>
                      <div className="flex-1">
                        <h3 className={`font-semibold mb-2 ${dailyChecklist[day.day] ? 'text-green-400 line-through' : 'text-green-400'}`}>
                          {day.title}
                        </h3>
                        <ul className="space-y-1">
                          {day.tasks?.slice(0, 3).map((task: string, idx: number) => (
                            <li key={idx} className="text-sm text-gray-300">• {task}</li>
                          ))}
                          {day.tasks?.length > 3 && (
                            <li className="text-xs text-gray-500">+{day.tasks.length - 3} more tasks</li>
                          )}
                        </ul>
                      </div>
                    </div>
                    <div className="text-right text-sm">
                      <p className="text-gray-400">⏰ {day.time_needed} hrs</p>
                      <p className="text-green-400">💰 ৳{day.estimated_earnings}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-purple-900/30 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-3 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-500" /> Pro Survival Tips
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {plan.tips?.slice(0, 4).map((tip: string, idx: number) => (
                <div key={idx} className="text-sm text-gray-300">• {tip}</div>
              ))}
            </div>
            <p className="mt-4 text-center text-green-400 italic">"{plan.survival_quote}"</p>
          </div>
        </>
      )}
    </div>
  );
};
