import React from 'react';
import { Menu } from 'lucide-react';

interface HeaderProps {
  onMenuClick: () => void;
  nodeName?: string;
  status?: 'active' | 'standby' | 'error';
  mode?: 'autonomous' | 'manual';
  uptime?: string;
}

export const Header: React.FC<HeaderProps> = ({ 
  onMenuClick,
  nodeName = 'Sakhipur',
  status = 'active',
  mode = 'autonomous',
  uptime,
}) => {
  const statusColors = {
    active: 'bg-green-500',
    standby: 'bg-orange-500',
    error: 'bg-red-500',
  };

  const statusTextColors = {
    active: 'text-green-400',
    standby: 'text-orange-400',
    error: 'text-red-400',
  };

  return (
    <header className="h-14 bg-[#12171F] border-b border-[#2A3340] px-4 sm:px-6 flex items-center justify-between">
      {/* Left: Logo + Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="lg:hidden p-1.5 rounded hover:bg-[#1A212B] text-[#8899AA]"
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <span className="text-green-400 text-lg">◆</span>
        <div className="hidden sm:block">
          <h1 className="text-[#E0E6ED] text-sm font-bold font-mono tracking-tight">
            JARVIS
          </h1>
          <p className="text-[#556677] text-[10px] font-mono">
            Cognitive Operations System
          </p>
        </div>
      </div>

      {/* Middle: Status (visible on all screens) */}
      <div className="flex items-center gap-4 sm:gap-6 font-mono text-[10px] sm:text-xs">
        <div className="flex items-center gap-1.5">
          <span className="text-[#556677] hidden sm:inline">Node:</span>
          <span className="text-[#E0E6ED]">{nodeName}</span>
        </div>
        
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${statusColors[status]} animate-pulse`} />
          <span className="text-[#556677] hidden sm:inline">Status:</span>
          <span className={`uppercase font-bold ${statusTextColors[status]}`}>
            {status}
          </span>
        </div>

        <div className="hidden sm:flex items-center gap-1.5">
          <span className="text-[#556677]">Mode:</span>
          <span className="text-[#E0E6ED] capitalize">{mode}</span>
        </div>

        {uptime && (
          <div className="hidden md:flex items-center gap-1.5">
            <span className="text-[#556677]">Uptime:</span>
            <span className="text-[#E0E6ED]">{uptime}</span>
          </div>
        )}
      </div>

      {/* Right: Minimal (theme toggle removed — always dark) */}
      <div className="hidden sm:flex items-center">
        <div className="w-7 h-7 rounded bg-[#1A212B] border border-[#2A3340] flex items-center justify-center text-[#8899AA] text-xs font-mono">
          J
        </div>
      </div>
    </header>
  );
};