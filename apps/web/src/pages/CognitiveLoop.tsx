import React, { useState, useEffect } from 'react';
import { Brain, TrendingUp, Lightbulb, AlertCircle } from 'lucide-react';

export const CognitiveLoop: React.FC = () => {
  const [insights, setInsights] = useState<any>(null);
  const [dailyData, setDailyData] = useState<number[]>([]);
  const [daysLeft, setDaysLeft] = useState(5);

  useEffect(() => {
    // Load progress from localStorage
    const saved = localStorage.getItem('moneyMode_progress');
    if (saved) {
      // For demo, create sample data
      setDailyData([500, 800, 1200, 1500, 2000]);
    }
  }, []);

  const analyzePatterns = async () => {
    try {
      const response = await fetch('/api/cognitive/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          daily_income: dailyData,
          target: target,
          days_remaining: daysLeft,
          skills: ['graphic_design', 'content_writing'],
          platforms: ['Upwork', 'Fiverr']
        })
      });
      const data = await response.json();
      setInsights(data);
    } catch (err) {
      console.error('Cognitive analysis failed:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
          <Brain className="w-8 h-8 text-purple-400" /> Cognitive Loop
        </h1>
        <p className="text-gray-400">AI-powered insights to optimize your earning potential</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Input Card */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">📊 Analyze Progress</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Days Remaining</label>
              <input
                type="number"
                value={daysLeft}
                onChange={(e) => setDaysLeft(Number(e.target.value))}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2"
              />
            </div>
            <button
              onClick={analyzePatterns}
              className="w-full bg-purple-600 hover:bg-purple-700 py-2 rounded-lg font-semibold"
            >
              Run Cognitive Analysis 🧠
            </button>
          </div>
        </div>

        {/* Insights Card */}
        {insights && (
          <div className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-3 flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-yellow-400" /> AI Insights
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span>Pattern:</span>
                <span className="font-semibold text-yellow-400">{insights.pattern}</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Projected:</span>
                <span className="font-semibold text-blue-400">৳{insights.projected_earnings}</span>
              </div>
              {insights.suggestions?.map((suggestion: string, idx: number) => (
                <div key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
                  <span>{suggestion}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Optimization Tips */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-green-400" /> Optimization Engine
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="bg-gray-700/50 rounded-lg p-3">
            <p className="text-sm font-semibold text-green-400">💰 Pricing Strategy</p>
            <p className="text-xs text-gray-300 mt-1">Bundle 3 services → +50% earnings</p>
          </div>
          <div className="bg-gray-700/50 rounded-lg p-3">
            <p className="text-sm font-semibold text-blue-400">⏰ Time Optimization</p>
            <p className="text-xs text-gray-300 mt-1">Morning hours = 2x productivity</p>
          </div>
          <div className="bg-gray-700/50 rounded-lg p-3">
            <p className="text-sm font-semibold text-yellow-400">🎯 Platform Focus</p>
            <p className="text-xs text-gray-300 mt-1">Upwork = highest rates (৳800-8000)</p>
          </div>
          <div className="bg-gray-700/50 rounded-lg p-3">
            <p className="text-sm font-semibold text-purple-400">📈 Growth Hacks</p>
            <p className="text-xs text-gray-300 mt-1">Referral system → 20% commission</p>
          </div>
        </div>
      </div>
    </div>
  );
};
