import React, { useState } from 'react';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { CheckSquare, Clock, AlertCircle, Filter } from 'lucide-react';

// Task interface matching the backend TaskDTO structure
interface Task {
  task_id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'pending' | 'in_progress' | 'completed';
  agent_type?: string;
  created_at?: string;
}

// Mock data for demonstration - TODO: Replace with API integration
const mockTasks: Task[] = [
  {
    task_id: 'task_1',
    title: 'Review Q4 Financial Reports',
    description: 'Analyze financial performance and prepare summary for stakeholders',
    priority: 'high',
    status: 'pending',
    agent_type: 'strategist',
    created_at: '2024-01-15T10:00:00Z'
  },
  {
    task_id: 'task_2',
    title: 'Update User Documentation',
    description: 'Revise user guide with latest features and improvements',
    priority: 'medium',
    status: 'in_progress',
    agent_type: 'executor',
    created_at: '2024-01-14T09:30:00Z'
  },
  {
    task_id: 'task_3',
    title: 'Fix Critical Security Bug',
    description: 'Address vulnerability in authentication system',
    priority: 'critical',
    status: 'pending',
    agent_type: 'executor',
    created_at: '2024-01-16T14:20:00Z'
  },
  {
    task_id: 'task_4',
    title: 'Database Optimization',
    description: 'Optimize database queries for better performance',
    priority: 'high',
    status: 'in_progress',
    agent_type: 'executor',
    created_at: '2024-01-13T11:00:00Z'
  },
  {
    task_id: 'task_5',
    title: 'Deploy Version 1.2.0',
    description: 'Deploy latest version to production environment',
    priority: 'medium',
    status: 'completed',
    agent_type: 'executor',
    created_at: '2024-01-12T16:45:00Z'
  },
  {
    task_id: 'task_6',
    title: 'Research AI Integration Options',
    description: 'Evaluate different AI models for task automation',
    priority: 'low',
    status: 'pending',
    agent_type: 'innovator',
    created_at: '2024-01-10T08:15:00Z'
  },
  {
    task_id: 'task_7',
    title: 'Create Marketing Campaign',
    description: 'Design and launch Q1 marketing campaign',
    priority: 'medium',
    status: 'completed',
    agent_type: 'strategist',
    created_at: '2024-01-08T13:00:00Z'
  },
  {
    task_id: 'task_8',
    title: 'Customer Feedback Analysis',
    description: 'Analyze and categorize customer feedback from last month',
    priority: 'low',
    status: 'completed',
    agent_type: 'mentor',
    created_at: '2024-01-05T10:30:00Z'
  }
];

const getPriorityVariant = (priority: string): 'default' | 'success' | 'warning' | 'error' => {
  switch (priority) {
    case 'critical':
      return 'error';
    case 'high':
      return 'warning';
    case 'medium':
      return 'warning';
    case 'low':
    default:
      return 'default';
  }
};

const TaskCard: React.FC<{ task: Task }> = ({ task }) => {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {task.title}
          </h3>
          <Badge variant={getPriorityVariant(task.priority)}>
            {task.priority.toUpperCase()}
          </Badge>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {task.description}
        </p>
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-500">
          <span>ID: {task.task_id}</span>
          {task.agent_type && (
            <span className="capitalize">Agent: {task.agent_type}</span>
          )}
        </div>
      </div>
    </Card>
  );
};

export const Tasks: React.FC = () => {
  const [selectedPriority, setSelectedPriority] = useState<string>('all');

  // Filter tasks by selected priority
  const filterTasksByPriority = (tasks: Task[]) => {
    if (selectedPriority === 'all') return tasks;
    return tasks.filter(task => task.priority === selectedPriority);
  };

  // Categorize tasks by status
  const pendingTasks = filterTasksByPriority(
    mockTasks.filter(task => task.status === 'pending')
  );
  const inProgressTasks = filterTasksByPriority(
    mockTasks.filter(task => task.status === 'in_progress')
  );
  const completedTasks = filterTasksByPriority(
    mockTasks.filter(task => task.status === 'completed')
  );

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Tasks</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and organize your tasks
          </p>
        </div>

        {/* Priority Filter */}
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-gray-500" />
          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      {/* Task Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-l-4 border-l-red-500">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-8 h-8 text-red-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {pendingTasks.length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Pending Tasks</p>
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-amber-500">
          <div className="flex items-center gap-3">
            <Clock className="w-8 h-8 text-amber-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {inProgressTasks.length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">In Progress</p>
            </div>
          </div>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <div className="flex items-center gap-3">
            <CheckSquare className="w-8 h-8 text-green-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {completedTasks.length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Completed</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Task Lists by Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Pending Tasks - Red Theme */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b-2 border-red-500">
            <AlertCircle className="w-5 h-5 text-red-500" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Pending
            </h2>
            <span className="ml-auto bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {pendingTasks.length}
            </span>
          </div>
          <div className="space-y-3">
            {pendingTasks.map(task => (
              <TaskCard key={task.task_id} task={task} />
            ))}
            {pendingTasks.length === 0 && (
              <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                No pending tasks
              </p>
            )}
          </div>
        </div>

        {/* In Progress Tasks - Yellow/Amber Theme */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b-2 border-amber-500">
            <Clock className="w-5 h-5 text-amber-500" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              In Progress
            </h2>
            <span className="ml-auto bg-amber-100 text-amber-800 dark:bg-amber-900/20 dark:text-amber-400 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {inProgressTasks.length}
            </span>
          </div>
          <div className="space-y-3">
            {inProgressTasks.map(task => (
              <TaskCard key={task.task_id} task={task} />
            ))}
            {inProgressTasks.length === 0 && (
              <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                No tasks in progress
              </p>
            )}
          </div>
        </div>

        {/* Completed Tasks - Green Theme */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b-2 border-green-500">
            <CheckSquare className="w-5 h-5 text-green-500" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Completed
            </h2>
            <span className="ml-auto bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {completedTasks.length}
            </span>
          </div>
          <div className="space-y-3">
            {completedTasks.map(task => (
              <TaskCard key={task.task_id} task={task} />
            ))}
            {completedTasks.length === 0 && (
              <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                No completed tasks
              </p>
            )}
          </div>
        </div>
      </div>

      {/* TODO: API Integration Placeholder */}
      {/* 
        Future API Integration:
        - Replace mockTasks with API call to fetch tasks from backend
        - Use TaskRepository methods to retrieve tasks by status
        - Implement real-time updates using WebSocket or polling
        - Add task CRUD operations (Create, Update, Delete)
        - Connect to execute_tasks.py use case for task execution
        
        Example API integration:
        const fetchTasks = async () => {
          const response = await fetch('/api/v1/tasks');
          const tasks = await response.json();
          setTasks(tasks);
        };
      */}
    </div>
  );
};
