import * as React from 'react';
import { 
  Home, 
  MessageSquare, 
  BarChart3, 
  FolderKanban, 
  Brain, 
  Settings,
  HelpCircle,
  BookOpen,
  Menu
} from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  const navItems = [
    {
      category: 'MAIN',
      items: [
        { name: 'Dashboard', href: '/', icon: Home },
        { name: 'Master Chat', href: '/chat', icon: MessageSquare },
      ]
    },
    {
      category: 'MEMORY',
      items: [
        { name: 'Diary', href: '/diary', icon: BookOpen },
        { name: 'Knowledge', href: '/knowledge', icon: Brain },
      ]
    },
    {
      category: 'PROJECTS',
      items: [
        { name: 'Projects', href: '/projects', icon: FolderKanban },
        { name: 'Analytics', href: '/analytics', icon: BarChart3 },
      ]
    },
    {
      category: 'SYSTEM',
      items: [
        { name: 'Settings', href: '/settings', icon: Settings },
        { name: 'Help', href: '/help', icon: HelpCircle },
      ]
    }
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => onClose?.()}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 h-full bg-gray-900 text-white z-30
        transition-transform duration-300 ease-in-out
        w-64 lg:translate-x-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-6">
          <div className="mb-8">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              JARVIS OS
            </h1>
            <p className="text-xs text-gray-400 mt-1">v5.3.0 | Personal AI System</p>
          </div>
          
          <nav className="space-y-6">
            {navItems.map((category) => (
              <div key={category.category}>
                <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
                  {category.category}
                </h3>
                <div className="space-y-1">
                  {category.items.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.href;
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        onClick={() => onClose?.()}
                        className={`
                          flex items-center gap-3 px-3 py-2 rounded-lg transition-colors
                          ${isActive 
                            ? 'bg-blue-600 text-white' 
                            : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                          }
                        `}
                      >
                        <Icon className="w-5 h-5" />
                        <span className="text-sm font-medium">{item.name}</span>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </nav>
        </div>
      </aside>
    </>
  );
};
