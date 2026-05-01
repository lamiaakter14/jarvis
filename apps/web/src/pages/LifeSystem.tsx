import React, { useState, useEffect } from 'react';
import { Target, TrendingUp, Users, BookOpen, Calendar, CheckCircle, Circle, Plus, Star, Award, Clock } from 'lucide-react';
import { getDashboard, updateSkill, updatePrayer, updateQuran, addAccountability, DashboardData } from '../api/lifeApi';

export const LifeSystem: React.FC = () => {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [accountabilityTask, setAccountabilityTask] = useState('');
  const [quranPages, setQuranPages] = useState(0);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await getDashboard();
      setDashboard(data);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePrayerToggle = async (prayer: string, currentStatus: boolean) => {
    await updatePrayer(prayer, !currentStatus);
    loadDashboard();
  };

  const handleQuranUpdate = async () => {
    if (quranPages > 0) {
      await updateQuran(quranPages);
      setQuranPages(0);
      loadDashboard();
    }
  };

  const handleAccountability = async () => {
    if (accountabilityTask.trim()) {
      await addAccountability(accountabilityTask);
      setAccountabilityTask('');
      loadDashboard();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
        <div className="text-center">Loading life dashboard... 🧠</div>
      </div>
    );
  }

  if (!dashboard) return null;

  const prayers = [
    { key: 'fajr', name: 'Fajr', time: 'Before sunrise' },
    { key: 'dhuhr', name: 'Dhuhr', time: 'Afternoon' },
    { key: 'asr', name: 'Asr', time: 'Late afternoon' },
    { key: 'maghrib', name: 'Maghrib', time: 'Sunset' },
    { key: 'isha', name: 'Isha', time: 'Night' }
  ];

  const prioritySkills = Object.entries(dashboard.skills)
    .filter(([_, skill]) => skill.priority === 'high')
    .sort((a, b) => (b[1].current - a[1].current));

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
          <Target className="w-8 h-8 text-purple-400" /> Long-term Life System
        </h1>
        <p className="text-gray-400">২০৩৬ জাতীয় সংসদ নির্বাচন — 10-year roadmap 🏛️</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* MP Election 2036 Card */}
        <div className="bg-gray-800 rounded-lg p-6 border border-purple-500/30">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" /> 🏛️ MP Election 2036
          </h2>
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span>Overall Progress</span>
              <span>{dashboard.mp_progress}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${dashboard.mp_progress}%` }} />
            </div>
          </div>
          <div className="space-y-2">
            {dashboard.mp_election_2036.milestones.slice(0, 5).map((m, idx) => (
              <div key={idx} className="flex items-center gap-2 text-sm">
                {m.completed ? <CheckCircle className="w-4 h-4 text-green-400" /> : <Circle className="w-4 h-4 text-gray-500" />}
                <span className={m.completed ? 'line-through text-gray-500' : 'text-gray-300'}>
                  {m.year}: {m.title}
                </span>
              </div>
            ))}
            {dashboard.mp_election_2036.milestones.length > 5 && (
              <p className="text-xs text-gray-500">+{dashboard.mp_election_2036.milestones.length - 5} more milestones</p>
            )}
          </div>
        </div>

        {/* Islamic Practice Card */}
        <div className="bg-gray-800 rounded-lg p-6 border border-green-500/30">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-green-400" /> 🕌 Islamic Practice
          </h2>
          <div className="grid grid-cols-2 gap-2 mb-4">
            {prayers.map((prayer) => (
              <button
                key={prayer.key}
                onClick={() => handlePrayerToggle(prayer.key, dashboard.islamic_practice.daily_prayers[prayer.key])}
                className={`flex items-center justify-between p-2 rounded-lg text-sm ${
                  dashboard.islamic_practice.daily_prayers[prayer.key]
                    ? 'bg-green-600/30 text-green-400'
                    : 'bg-gray-700/50 text-gray-400'
                }`}
              >
                <span>{prayer.name}</span>
                {dashboard.islamic_practice.daily_prayers[prayer.key] ? <CheckCircle className="w-4 h-4" /> : <Circle className="w-4 h-4" />}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="number"
              value={quranPages}
              onChange={(e) => setQuranPages(Number(e.target.value))}
              placeholder="Quran pages read"
              className="flex-1 bg-gray-700 rounded-lg px-3 py-2 text-sm"
            />
            <button onClick={handleQuranUpdate} className="bg-green-600 px-4 py-2 rounded-lg text-sm">Update</button>
          </div>
          <p className="text-xs text-gray-400 mt-2">📖 Quran completion: {dashboard.islamic_practice.quran_completion.toFixed(1)}%</p>
        </div>

        {/* Skill Progress Card */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-400" /> 📊 Skill Progress
          </h2>
          <div className="space-y-3">
            {prioritySkills.map(([name, skill]) => (
              <div key={name}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{name.replace('_', ' ').toUpperCase()}</span>
                  <span>{skill.current}% / {skill.required}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-1.5">
                  <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${skill.current}%` }} />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 p-3 bg-yellow-600/20 rounded-lg">
            <p className="text-sm text-yellow-400">
              ⚠️ Skill Gap: {dashboard.skill_gap.gap.toFixed(0)}% to target
            </p>
          </div>
        </div>

        {/* Network Tracker Card */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-cyan-400" /> 👥 Network ({dashboard.network.total}/50)
          </h2>
          <div className="grid grid-cols-3 gap-3 text-center mb-4">
            <div className="bg-gray-700/50 rounded-lg p-2">
              <p className="text-2xl font-bold text-red-400">{dashboard.network.political}</p>
              <p className="text-xs text-gray-400">Political</p>
            </div>
            <div className="bg-gray-700/50 rounded-lg p-2">
              <p className="text-2xl font-bold text-green-400">{dashboard.network.social}</p>
              <p className="text-xs text-gray-400">Social</p>
            </div>
            <div className="bg-gray-700/50 rounded-lg p-2">
              <p className="text-2xl font-bold text-blue-400">{dashboard.network.business}</p>
              <p className="text-xs text-gray-400">Business</p>
            </div>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div className="bg-cyan-500 h-2 rounded-full" style={{ width: `${(dashboard.network.total / 50) * 100}%` }} />
          </div>
        </div>
      </div>

      {/* Daily Accountability */}
      <div className="mt-6 bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-400" /> ✅ Daily Accountability
        </h2>
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={accountabilityTask}
            onChange={(e) => setAccountabilityTask(e.target.value)}
            placeholder="Goal-এর জন্য আজ কী করলি?"
            className="flex-1 bg-gray-700 rounded-lg px-4 py-2"
          />
          <button onClick={handleAccountability} className="bg-purple-600 px-4 py-2 rounded-lg">Add</button>
        </div>
        <div className="space-y-2 max-h-40 overflow-y-auto">
          {dashboard.daily_accountability.slice(0, 5).map((item, idx) => (
            <div key={idx} className="flex items-center gap-2 text-sm text-gray-300 p-2 bg-gray-700/30 rounded">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>{item.task}</span>
              <span className="text-xs text-gray-500 ml-auto">{item.date}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Quote */}
      <div className="mt-6 text-center">
        <p className="text-gray-400 italic">"২০৩৬ সালের এমপি হওয়ার যাত্রা — প্রতিদিন এক কদম এগিয়ে" 💪🇧🇩</p>
      </div>
    </div>
  );
};
