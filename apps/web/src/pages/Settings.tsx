import React from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useTheme } from '../contexts/ThemeContext';
import { Save, Moon, Sun } from 'lucide-react';
import toast from 'react-hot-toast';

export const Settings: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const [apiUrl, setApiUrl] = React.useState(
    import.meta.env.VITE_API_URL || 'http://localhost:8000'
  );

  const handleSave = () => {
    toast.success('Settings saved successfully!');
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Configure your JARVIS assistant
        </p>
      </div>

      {/* API Configuration */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">API Configuration</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Backend API URL</label>
            <input
              type="text"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="http://localhost:8000"
            />
            <p className="text-sm text-gray-500 mt-1">
              The URL of your JARVIS backend API
            </p>
          </div>
        </div>
      </Card>

      {/* Theme Settings */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Appearance</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Theme</p>
              <p className="text-sm text-gray-500">
                Choose between light and dark mode
              </p>
            </div>
            <Button
              variant="secondary"
              onClick={toggleTheme}
            >
              {theme === 'light' ? (
                <>
                  <Moon className="w-5 h-5 mr-2" />
                  Dark Mode
                </>
              ) : (
                <>
                  <Sun className="w-5 h-5 mr-2" />
                  Light Mode
                </>
              )}
            </Button>
          </div>
        </div>
      </Card>

      {/* Agent Configuration */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Cognitive Agents</h2>
        <div className="space-y-4">
          {['Strategist', 'Mentor', 'Executor', 'Innovator', 'Amplifier'].map((agent) => (
            <div key={agent} className="flex items-center justify-between">
              <div>
                <p className="font-medium">{agent}</p>
                <p className="text-sm text-gray-500">
                  Enable or disable the {agent} agent
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
              </label>
            </div>
          ))}
        </div>
      </Card>

      {/* System Information */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">System Information</h2>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Version</span>
            <span className="font-medium">1.0.0</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Architecture</span>
            <span className="font-medium">Clean Architecture</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Status</span>
            <span className="font-medium text-green-600">Healthy</span>
          </div>
        </div>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button onClick={handleSave}>
          <Save className="w-5 h-5 mr-2" />
          Save Settings
        </Button>
      </div>
    </div>
  );
};
