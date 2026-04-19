import React, { useState, useEffect } from 'react';
import { getTasks, deleteTask } from '../../api/taskApi';
import { Task } from '../../types/task';
import { ErrorMessage } from '../common/ErrorMessage';

export const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getTasks();
      setTasks(data);
    } catch {
      setError("Failed to load tasks. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch {
      setError("Failed to delete task. Please try again.");
    }
  };

  if (loading) {
    return <p>Loading tasks...</p>;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Tasks</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {["Pending", "Completed", "Failed"].map((status) => (
          <div key={status} className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
            <p className="text-sm text-gray-600 dark:text-gray-400">{status}</p>
            <p className="text-2xl font-bold">
              {tasks.filter(task => task.status === status.toLowerCase()).length}
            </p>
          </div>
        ))}
      </div>

      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead>
          <tr>
            <th className="text-left px-4 py-2">Task</th>
            <th className="text-left px-4 py-2">Status</th>
            <th className="text-left px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id} className="hover:bg-gray-100 dark:hover:bg-gray-800">
              <td className="px-4 py-2">{task.title}</td>
              <td className="px-4 py-2">
                <span className={`badge badge-${task.status}`}>{task.status}</span>
              </td>
              <td className="px-4 py-2 flex space-x-2">
                <button
                  onClick={() => handleDelete(task.id)}
                  className="btn btn-delete"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
