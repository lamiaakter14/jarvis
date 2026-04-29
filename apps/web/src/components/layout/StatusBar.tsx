import React from 'react';

interface MetricBarProps {
  value: number;
  color: string;
}

const MetricBar: React.FC<MetricBarProps> = ({ value, color }) => (
  <div className="flex items-center gap-1.5">
    <div className="w-16 h-1 bg-jarvis-border rounded-full overflow-hidden">
      <div
        className={`h-full rounded-full ${color}`}
        style={{ width: `${value}%` }}
      />
    </div>
  </div>
);

export const StatusBar: React.FC = () => {
  return (
    <div className="h-8 bg-jarvis-surface border-t border-jarvis-border px-4 flex items-center justify-between text-[10px] text-jarvis-muted flex-shrink-0">
      <div className="flex items-center gap-5">
        <div className="flex items-center gap-1.5">
          <span className="tracking-wider">SYSTEM LOAD</span>
          <MetricBar value={23} color="bg-jarvis-cyan" />
          <span className="text-jarvis-text">23%</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="tracking-wider">MEMORY</span>
          <MetricBar value={26} color="bg-jarvis-green" />
          <span className="text-jarvis-text">4.2 GB / 16 GB</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="tracking-wider">CPU</span>
          <MetricBar value={18} color="bg-jarvis-purple" />
          <span className="text-jarvis-text">18%</span>
        </div>
        <div className="hidden sm:flex items-center gap-1.5">
          <span className="tracking-wider">NETWORK</span>
          <MetricBar value={45} color="bg-jarvis-amber" />
          <span className="text-jarvis-text">2.4 MB/s</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <span>J.A.R.V.I.S. v5.3.0</span>
        <span className="w-1.5 h-1.5 rounded-full bg-jarvis-green inline-block" />
        <span className="text-jarvis-green font-semibold">OPERATIONAL</span>
      </div>
    </div>
  );
};
