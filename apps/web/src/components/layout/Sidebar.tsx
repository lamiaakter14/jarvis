import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Brain,
  Calendar,
  CheckSquare,
  AlertCircle,
  Lightbulb,
  BarChart3,
  Settings,
  MessageSquare,
  BookOpen,
  Target,
  ChevronDown,
  ChevronRight,
  Play,
  Activity,
  Shield,
  Zap,
  FileText,
  FolderOpen,
  Clock,
  Database,
  GitBranch,
  Cpu,
} from 'lucide-react';
import { cn } from '../../utils/cn';

// ============================================================
// Navigation Groups — Flow: Chat → Plan → Execute → Track → Learn
// ============================================================
interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

interface NavGroup {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  items: NavItem[];
}

const navigationGroups: NavGroup[] = [
  {
    label: 'Main',
    icon: LayoutDashboard,
    items: [
      { name: 'Command Center', href: '/', icon: Cpu },
      { name: 'Master Chat', href: '/command-center', icon: MessageSquare, badge: 'CORE' },
    ],
  },
  {
    label: 'Planning',
    icon: Brain,
    items: [
      { name: 'Planner Mode', href: '/command-center', icon: Brain },
      { name: 'Projects', href: '/plans', icon: FolderOpen },
      { name: 'Goals', href: '/goals', icon: Target },
    ],
  },
  {
    label: 'Execution',
    icon: Play,
    items: [
      { name: 'Task Queue', href: '/tasks', icon: CheckSquare },
      { name: 'Active Execution', href: '/cognitive-loop', icon: Activity },
    ],
  },
  {
    label: 'Intelligence',
    icon: Lightbulb,
    items: [
      { name: 'Performance', href: '/performance', icon: BarChart3 },
      { name: 'Innovations', href: '/innovations', icon: Zap },
    ],
  },
  {
    label: 'Memory',
    icon: BookOpen,
    items: [
      { name: 'Digital Diary', href: '/diary', icon: BookOpen },
      { name: 'Knowledge', href: '/gaps', icon: Database },
    ],
  },
  {
    label: 'System',
    icon: Shield,
    items: [
      { name: 'Integrations', href: '/settings', icon: GitBranch },
      { name: 'Settings', href: '/settings', icon: Settings },
    ],
  },
];

// ============================================================
// Sidebar Component
// ============================================================
interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  activeMode?: string;  // 'planner' | 'execution' | 'chat'
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose, activeMode }) => {
  const location = useLocation();
  
  const [collapsedGroups, setCollapsedGroups] = useState<Record<string, boolean>>({});

  const toggleGroup = (label: string) => {
    setCollapsedGroups(prev => ({
      ...prev,
      [label]: !prev[label]
    }));
  };

  const isGroupActive = (group: NavGroup) => {
    return group.items.some(item => location.pathname === item.href);
  };

  const isItemActive = (href: string) => {
    if (href === '/') return location.pathname === '/';
    return location.pathname === href;
  };

  // ✅ FIXED: Dynamic section highlight based on mode
  const getGroupHighlight = (label: string) => {
    if (activeMode === 'planner' && label === 'Planning') return true;
    if (activeMode === 'execution' && label === 'Execution') return true;
    // Find actual group object by label instead of casting string as NavGroup
    const group = navigationGroups.find(g => g.label === label);
    return group ? isGroupActive(group) : false;
  };

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
        <Brain className="w-8 h-8 text-blue-600 mr-2" />
        <div>
          <span className="text-xl font-bold block leading-tight">JARVIS</span>
          <span className="text-[9px] text-gray-400 uppercase tracking-wider">Command OS</span>
        </div>
      </div>

      {/* Navigation Groups */}
      <nav className="flex-1 overflow-y-auto py-2">
        {navigationGroups.map((group) => {
          const GroupIcon = group.icon;
          const isCollapsed = collapsedGroups[group.label] ?? false;
          const active = getGroupHighlight(group.label);

          return (
            <div key={group.label} className="mb-1">
              <button
                onClick={() => toggleGroup(group.label)}
                className={cn(
                  'w-full flex items-center justify-between px-4 py-2 text-xs font-semibold uppercase tracking-wider transition-colors',
                  active
                    ? 'text-blue-600 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/10'
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                )}
              >
                <div className="flex items-center gap-2">
                  <GroupIcon className="w-3.5 h-3.5" />
                  <span>{group.label}</span>
                </div>
                {isCollapsed ? (
                  <ChevronRight className="w-3 h-3" />
                ) : (
                  <ChevronDown className="w-3 h-3" />
                )}
              </button>

              {!isCollapsed && (
                <div className="ml-2">
                  {group.items.map((item) => {
                    const active = isItemActive(item.href);
                    const Icon = item.icon;

                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        onClick={onClose}
                        className={cn(
                          'flex items-center px-4 py-2.5 ml-4 text-sm rounded-l-md transition-colors border-l-2',
                          active
                            ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-blue-600'
                            : 'text-gray-600 dark:text-gray-400 border-transparent hover:bg-gray-50 dark:hover:bg-gray-700/30 hover:text-gray-900 dark:hover:text-gray-200'
                        )}
                      >
                        <Icon className="w-4 h-4 mr-3 flex-shrink-0" />
                        <span className="truncate">{item.name}</span>
                        {active && (
                          <span className="ml-auto w-1.5 h-1.5 bg-blue-600 rounded-full flex-shrink-0" />
                        )}
                        {item.badge && (
                          <span className="ml-2 px-1.5 py-0.5 bg-purple-600 text-white text-[8px] rounded font-bold">
                            {item.badge}
                          </span>
                        )}
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex-shrink-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-gray-500 dark:text-gray-400">System Active</span>
        </div>
        {activeMode && (
          <div className="text-[10px] text-blue-400 mb-1">
            Mode: {activeMode}
          </div>
        )}
        <p className="text-[10px] text-gray-400 dark:text-gray-500 text-center mt-1">
          JARVIS v4.0.0
        </p>
      </div>
    </div>
  );

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          'fixed top-0 left-0 z-50 h-full w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-transform duration-300 ease-in-out',
          'lg:translate-x-0 lg:static lg:z-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {sidebarContent}
      </aside>
    </>
  );
};