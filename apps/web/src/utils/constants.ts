export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const POLL_INTERVAL = 5000; // 5 seconds

export const PRIORITY_COLORS = {
  low: 'bg-gray-100 text-gray-800',
  medium: 'bg-blue-100 text-blue-800',
  high: 'bg-amber-100 text-amber-800',
  critical: 'bg-red-100 text-red-800',
};

export const STATUS_COLORS = {
  todo: 'bg-gray-100 text-gray-800',
  in_progress: 'bg-blue-100 text-blue-800',
  done: 'bg-green-100 text-green-800',
};

export const SEVERITY_COLORS = {
  low: 'bg-gray-100 text-gray-800',
  medium: 'bg-blue-100 text-blue-800',
  high: 'bg-amber-100 text-amber-800',
  critical: 'bg-red-100 text-red-800',
};
