import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Brain,
  Zap,
  CheckSquare,
  FolderOpen,
  Target,
  BookOpen,
  TrendingUp,
  RefreshCw,
  Users,
  Settings,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
} from 'lucide-react';
import { cn } from '../../utils/cn';

const sections = [
  {
    label: 'CORE',
    items: [
      { name: 'Dashboard', href: '/', icon: LayoutDashboard },
      { name: 'Planner Mode', href: '/plans', icon: Brain },
      { name: 'Executor Mode', href: '/cognitive-loop', icon: Zap },
    ],
  },
  {
    label: 'SYSTEM',
    items: [
      { name: 'Tasks', href: '/tasks', icon: CheckSquare },
      { name: 'Projects', href: '/projects', icon: FolderOpen },
      { name: 'Goals', href: '/goals', icon: Target },
    ],
  },
  {
    label: 'INTELLIGENCE',
    items: [
      { name: 'Memory (Diary)', href: '/memory', icon: BookOpen },
      { name: 'Insights (Amplifier)', href: '/innovations', icon: TrendingUp },
      { name: 'Reflection (Reflector)', href: '/gaps', icon: RefreshCw },
    ],
  },
  {
    label: 'ADVANCED',
    items: [
      { name: 'Agents', href: '/agents', icon: Users },
      { name: 'Settings', href: '/settings', icon: Settings },
    ],
  },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-50 h-full bg-jarvis-surface border-r border-jarvis-border transition-all duration-300 ease-in-out flex flex-col',
          'lg:static lg:z-0',
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
          collapsed ? 'w-16' : 'w-52'
        )}
      >
        {/* Top controls */}
        <div className="h-14 flex items-center justify-between px-3 border-b border-jarvis-border flex-shrink-0">
          <button
            onClick={onClose}
            className="lg:hidden p-1 rounded text-jarvis-muted hover:text-jarvis-text"
          >
            <X className="w-4 h-4" />
          </button>
          <div className="hidden lg:block">
            <Menu className="w-4 h-4 text-jarvis-muted" />
          </div>
          {!collapsed && (
            <button
              onClick={() => setCollapsed(true)}
              className="p-1 rounded text-jarvis-muted hover:text-jarvis-cyan transition-colors"
              title="Collapse sidebar"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
          )}
          {collapsed && (
            <button
              onClick={() => setCollapsed(false)}
              className="p-1 rounded text-jarvis-muted hover:text-jarvis-cyan transition-colors mx-auto"
              title="Expand sidebar"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-3 space-y-4">
          {sections.map((section) => (
            <div key={section.label}>
              {!collapsed && (
                <p className="px-4 mb-1 text-[10px] font-semibold tracking-widest text-jarvis-muted uppercase">
                  {section.label}
                </p>
              )}
              {section.items.map((item) => {
                const isActive = location.pathname === item.href;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={onClose}
                    title={collapsed ? item.name : undefined}
                    className={cn(
                      'flex items-center py-2 text-sm font-medium transition-all duration-150',
                      collapsed ? 'px-0 justify-center' : 'px-4 gap-3',
                      isActive
                        ? 'text-jarvis-cyan bg-jarvis-cyan/10 border-r-2 border-jarvis-cyan'
                        : 'text-jarvis-muted hover:text-jarvis-text hover:bg-white/5'
                    )}
                  >
                    <Icon className={cn('flex-shrink-0', collapsed ? 'w-5 h-5' : 'w-4 h-4')} />
                    {!collapsed && <span className="truncate">{item.name}</span>}
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>

        {/* J.A.R.V.I.S. status panel */}
        {!collapsed && (
          <div className="border-t border-jarvis-border p-3 flex-shrink-0">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-jarvis-cyan/30 to-blue-600/30 border border-jarvis-cyan/40 flex items-center justify-center">
                <Brain className="w-4 h-4 text-jarvis-cyan" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-bold text-jarvis-text truncate">J.A.R.V.I.S.<span className="text-jarvis-muted font-normal"> CORE</span></p>
              </div>
            </div>
            <div className="space-y-0.5 ml-1">
              <p className="text-[11px] text-jarvis-muted">
                System Status{' '}
                <span className="text-jarvis-green font-semibold">OPERATIONAL</span>
              </p>
              <p className="text-[11px] text-jarvis-muted">Uptime <span className="text-jarvis-text">14h 32m 18s</span></p>
            </div>
          </div>
        )}

        {/* Collapse button (bottom) */}
        {!collapsed && (
          <button
            onClick={() => setCollapsed(true)}
            className="flex items-center gap-2 px-4 py-3 text-xs text-jarvis-muted hover:text-jarvis-cyan border-t border-jarvis-border transition-colors flex-shrink-0"
          >
            <ChevronLeft className="w-3 h-3" />
            Collapse
          </button>
        )}
      </aside>
    </>
  );
};
