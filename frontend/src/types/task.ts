export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'done';
  priority: 'low' | 'medium' | 'high' | 'critical';
  roi: number;
  cognitive_load: number;
  estimated_hours: number;
  actual_hours?: number;
  created_at: string;
  completed_at?: string;
  tags?: string[];
}
