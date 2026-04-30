import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import StatusBar from './StatusBar';

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
        <StatusBar />
      </div>
    </div>
  );
};

export default AppLayout;
