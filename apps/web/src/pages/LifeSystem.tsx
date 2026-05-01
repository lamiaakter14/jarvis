import React from 'react';
import { Target, TrendingUp, Users, BookOpen, Check } from 'lucide-react';

export const LifeSystem: React.FC = () => {
  return (
    <div className="flex flex-col p-6">
      <div className="flex items-center gap-3 mb-6">
        <Target className="w-6 h-6 text-purple-400" />
        <h1 className="text-xl font-bold text-purple-400">Long-term Life System</h1>
        <span className="text-xs text-gray-500 ml-2">2036 — 10-year roadmap</span>
      </div>

      {/* MP Election 2036 */}
      <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4 mb-4">
        <h2 className="text-sm font-bold text-purple-400 mb-3">🏛️ MP Election 2036</h2>
        <div className="w-full bg-[#232A34] rounded-full h-2 mb-3">
          <div className="bg-purple-500 h-2 rounded-full" style={{ width: '25%' }} />
        </div>
        <p className="text-xs text-gray-400">Overall Progress: 25%</p>
        <div className="mt-3 space-y-1 text-xs text-gray-300">
          <p>✅ 2024: Start business/venture</p>
          <p>✅ 2025: Build local network</p>
          <p>✅ 2026: Community service projects</p>
          <p>🔲 2028: Join local politics</p>
          <p>🔲 2030: Union Parishad level</p>
          <p>🔲 2036: MP Election 🎯</p>
        </div>
      </div>

      {/* Skills */}
      <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4 mb-4">
        <h2 className="text-sm font-bold text-purple-400 mb-3 flex items-center gap-2"><TrendingUp className="w-4 h-4" /> Skills Progress</h2>
        {[
          { name: 'Networking', current: 60, target: 85 },
          { name: 'Leadership', current: 50, target: 90 },
          { name: 'Political Knowledge', current: 30, target: 80 },
          { name: 'Fundraising', current: 25, target: 75 },
          { name: 'Public Speaking', current: 20, target: 85 },
        ].map((skill: any, idx: number) => (
          <div key={idx} className="mb-2">
            <div className="flex justify-between text-xs text-gray-300 mb-1">
              <span>{skill.name}</span>
              <span>{skill.current}% / {skill.target}%</span>
            </div>
            <div className="w-full bg-[#232A34] rounded-full h-1.5">
              <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: `${(skill.current / skill.target) * 100}%` }} />
            </div>
          </div>
        ))}
        <p className="text-xs text-gray-400 mt-3">Skill Gap: 39% to target</p>
      </div>

      {/* Islamic Practice */}
      <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4 mb-4">
        <h2 className="text-sm font-bold text-purple-400 mb-3 flex items-center gap-2"><BookOpen className="w-4 h-4" /> Islamic Practice</h2>
        <div className="grid grid-cols-5 gap-2 mb-3">
          {['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'].map(p => (
            <button key={p} className="px-3 py-2 bg-[#0A0E14] border border-[#232A34] rounded-lg text-xs text-gray-400 hover:border-purple-500/30">
              <Check className="w-3 h-3 inline mr-1 text-green-400" />{p}
            </button>
          ))}
        </div>
        <p className="text-xs text-gray-400">Quran completion: 0.3%</p>
      </div>

      {/* Network */}
      <div className="bg-[#151A22] border border-[#232A34] rounded-xl p-4">
        <h2 className="text-sm font-bold text-purple-400 mb-3 flex items-center gap-2"><Users className="w-4 h-4" /> Network (12/50)</h2>
        {[{ cat: 'Political', count: 3 }, { cat: 'Social', count: 5 }, { cat: 'Business', count: 4 }].map((item: any, idx: number) => (
          <div key={idx} className="flex justify-between text-xs text-gray-300 mb-1">
            <span>{item.cat}</span>
            <span>{item.count}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
