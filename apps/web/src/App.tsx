import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { Dashboard } from './pages/Dashboard';
import Diary from './pages/Diary';

// Placeholder components for other routes
const MasterChat = () => <div className="p-6">Master Chat Page</div>;
const Knowledge = () => <div className="p-6">Knowledge Base Page</div>;
const Projects = () => <div className="p-6">Projects Page</div>;
const Analytics = () => <div className="p-6">Analytics Page</div>;
const Settings = () => <div className="p-6">Settings Page</div>;
const Help = () => <div className="p-6">Help Page</div>;

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="chat" element={<MasterChat />} />
          <Route path="diary" element={<Diary />} />
          <Route path="knowledge" element={<Knowledge />} />
          <Route path="projects" element={<Projects />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<Settings />} />
          <Route path="help" element={<Help />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
