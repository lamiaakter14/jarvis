import React from 'react';
import { LucideIcon, TrendingUp } from 'lucide-react';
import { SparklineChart } from '../common/SparklineChart';

interface StatsCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: LucideIcon;
  color: 'cyan' | 'blue' | 'purple' | 'orange';
  sparklineData: number[];
}

const colorMap = {
  cyan: {
    icon: 'text-jarvis-cyan',
    border: 'border-jarvis-cyan/20',
    glow: 'shadow-[0_0_20px_rgba(0,212,255,0.08)]',
    change: 'text-jarvis-cyan',
    hex: '#00d4ff',
  },
  blue: {
    icon: 'text-blue-400',
    border: 'border-blue-500/20',
    glow: 'shadow-[0_0_20px_rgba(59,130,246,0.08)]',
    change: 'text-blue-400',
    hex: '#60a5fa',
  },
  purple: {
    icon: 'text-jarvis-purple',
    border: 'border-purple-500/20',
    glow: 'shadow-[0_0_20px_rgba(139,92,246,0.08)]',
    change: 'text-jarvis-purple',
    hex: '#8b5cf6',
  },
  orange: {
    icon: 'text-jarvis-orange',
    border: 'border-orange-500/20',
    glow: 'shadow-[0_0_20px_rgba(249,115,22,0.08)]',
    change: 'text-jarvis-orange',
    hex: '#f97316',
  },
};

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  change,
  icon: Icon,
  color,
  sparklineData,
}) => {
  const colors = colorMap[color];

  return (
    <div
      className={`bg-jarvis-card border ${colors.border} ${colors.glow} rounded-xl p-4 flex flex-col gap-2`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-[10px] font-semibold tracking-widest text-jarvis-muted uppercase mb-1">
            {title}
          </p>
          <p className="text-2xl font-bold text-jarvis-text leading-none">{value}</p>
          {change !== undefined && (
            <div className={`flex items-center gap-1 mt-1.5 text-xs font-semibold ${colors.change}`}>
              <TrendingUp className="w-3 h-3" />
              <span>{change >= 0 ? '+' : ''}{change}%</span>
            </div>
          )}
        </div>
        <Icon className={`w-5 h-5 flex-shrink-0 ml-2 ${colors.icon}`} />
      </div>
      <div className="mt-1">
        <SparklineChart data={sparklineData} color={colors.hex} />
      </div>
    </div>
  );
};
