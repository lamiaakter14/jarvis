import React from 'react';
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
} from 'lucide-react';
import { cn } from '../../utils/cn';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Cognitive Loop', href: '/cognitive-loop', icon: Brain },
  { name: 'Plans', href: '/plans', icon: Calendar },
  { name: 'Tasks', href: '/tasks', icon: CheckSquare },
  { name: 'Knowledge Gaps', href: '/gaps', icon: AlertCircle },
  { name: 'Innovations', href: '/innovations', icon: Lightbulb },
  { name: 'Performance', href: '/performance', icon: BarChart3 },
  { name: 'Settings', href: '/settings', icon: Settings },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-50 h-full w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-transform duration-300 ease-in-out',
          'lg:translate-x-0 lg:static lg:z-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="h-16 flex items-center px-6 border-b border-gray-200 dark:border-gray-700">
            <Brain className="w-8 h-8 text-blue-600 mr-2" />
            <span className="text-xl font-bold">JARVIS</span>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={onClose}
                  className={cn(
                    'flex items-center px-6 py-3 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-r-4 border-blue-600'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'
                  )}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
              JARVIS v1.0.0
            </p>
          </div>
        </div>
      </aside>
    </>
  );
};
