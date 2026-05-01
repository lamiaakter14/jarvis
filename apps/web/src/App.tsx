import { ChatPage } from './pages/ChatPage';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from './contexts/ThemeContext';
import { AppProvider } from './contexts/AppContext';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { Dashboard } from './pages/Dashboard';
import { CognitiveLoop } from './pages/CognitiveLoop';
import { ContextEngine } from './pages/ContextEngine';
import { LifeSystem } from './pages/LifeSystem';
import { ExecutionHub } from './pages/ExecutionHub';
import { Plans } from './pages/Plans';
import { Tasks } from './pages/Tasks';
import { Gaps } from './pages/Gaps';
import { Innovations } from './pages/Innovations';
import { Performance } from './pages/Performance';
import { Settings } from './pages/Settings';
import { MoneyMode } from './pages/MoneyMode';
import { Diary } from './pages/Diary';
import './styles/globals.css';

function App() {
  return (
    <ThemeProvider>
      <AppProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<DashboardLayout />}>
              <Route index element={<Dashboard />} />
              <Route path="cognitive-loop" element={<CognitiveLoop />} />
              <Route path="plans" element={<Plans />} />
              <Route path="tasks" element={<Tasks />} />
              <Route path="gaps" element={<Gaps />} />
              <Route path="innovations" element={<Innovations />} />
              <Route path="performance" element={<Performance />} />
              <Route path="settings" element={<Settings />} />
              <Route path="chat" element={<ChatPage />} />
              <Route path="money" element={<MoneyMode />} />
              <Route path="context" element={<ContextEngine />} />
              <Route path="life" element={<LifeSystem />} />
              <Route path="execute" element={<ExecutionHub />} />
              <Route path="diary" element={<Diary />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 3000,
              style: {
                background: '#333',
                color: '#fff',
              },
            }}
          />
        </BrowserRouter>
      </AppProvider>
    </ThemeProvider>
  );
}

export default App;
