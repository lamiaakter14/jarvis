import { Task } from './task';

export interface Plan {
  id: string;
  date: string;
  tasks: Task[];
  total_estimated_hours: number;
  total_actual_hours?: number;
  completion_rate: number;
  created_at: string;
}
