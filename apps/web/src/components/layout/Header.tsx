import React, { useState } from 'react';
import { Menu, Bell, Search, ChevronDown, Hexagon } from 'lucide-react';
import { cn } from '../../utils/cn';

type Mode = 'MANUAL' | 'ASSISTED' | 'AUTONOMOUS';

interface HeaderProps {
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const [mode, setMode] = useState<Mode>('ASSISTED');

  return (
    <header className="h-14 bg-jarvis-surface border-b border-jarvis-border px-4 flex items-center justify-between gap-3 flex-shrink-0">
      {/* Left: Logo + mobile menu */}
      <div className="flex items-center gap-3 flex-shrink-0">
        <button
          onClick={onMenuClick}
          className="lg:hidden p-1.5 rounded text-jarvis-muted hover:text-jarvis-text"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="hidden lg:flex items-center gap-2">
          <div className="relative">
            <Hexagon className="w-8 h-8 text-jarvis-cyan" strokeWidth={1.5} />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-2 h-2 rounded-full bg-jarvis-cyan" />
            </div>
          </div>
          <div className="leading-tight">
            <p className="text-sm font-bold text-jarvis-text tracking-wide">JARVIS</p>
            <p className="text-[9px] text-jarvis-muted tracking-widest uppercase">Personal AI Operating System</p>
          </div>
        </div>
      </div>

      {/* Center: Mode switcher */}
      <div className="flex items-center gap-1 bg-jarvis-bg border border-jarvis-border rounded-lg p-1 flex-shrink-0">
        <span className="text-[10px] text-jarvis-muted px-1 mr-1 tracking-widest">MODE</span>
        {(['MANUAL', 'ASSISTED', 'AUTONOMOUS'] as Mode[]).map((m) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className={cn(
              'px-3 py-1 rounded text-xs font-semibold tracking-wider transition-all',
              mode === m
                ? 'bg-jarvis-cyan/20 text-jarvis-cyan border border-jarvis-cyan/50'
                : 'text-jarvis-muted hover:text-jarvis-text'
            )}
          >
            {m === 'ASSISTED' && mode === m ? (
              <span className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-jarvis-cyan inline-block" />
                {m}
              </span>
            ) : m}
          </button>
        ))}
      </div>

      {/* Right: dropdowns + icons */}
      <div className="flex items-center gap-2 flex-shrink-0">
        {/* Active Project */}
        <div className="hidden md:flex flex-col items-start border border-jarvis-border rounded-lg px-3 py-1 cursor-pointer hover:border-jarvis-cyan/40 transition-colors">
          <span className="text-[9px] text-jarvis-muted tracking-widest uppercase">Active Project</span>
          <div className="flex items-center gap-1">
            <span className="text-xs text-jarvis-text font-medium">Quantum Website Redesign</span>
            <ChevronDown className="w-3 h-3 text-jarvis-muted" />
          </div>
        </div>

        {/* Active Agent */}
        <div className="hidden md:flex flex-col items-start border border-jarvis-border rounded-lg px-3 py-1 cursor-pointer hover:border-jarvis-cyan/40 transition-colors">
          <span className="text-[9px] text-jarvis-muted tracking-widest uppercase">Active Agent</span>
          <div className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-jarvis-green inline-block" />
            <span className="text-xs text-jarvis-text font-medium">Planner</span>
            <ChevronDown className="w-3 h-3 text-jarvis-muted" />
          </div>
        </div>

        {/* Search */}
        <button className="p-2 rounded-lg text-jarvis-muted hover:text-jarvis-text hover:bg-white/5 transition-colors">
          <Search className="w-4 h-4" />
        </button>

        {/* Notifications */}
        <button className="relative p-2 rounded-lg text-jarvis-muted hover:text-jarvis-text hover:bg-white/5 transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-4 h-4 bg-jarvis-cyan text-jarvis-bg text-[9px] font-bold rounded-full flex items-center justify-center">
            3
          </span>
        </button>

        {/* User avatar */}
        <div className="w-8 h-8 rounded-full overflow-hidden border border-jarvis-border">
          <div className="w-full h-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white text-xs font-bold">
            T
          </div>
        </div>
        <ChevronDown className="w-3 h-3 text-jarvis-muted" />
      </div>
    </header>
  );
};
