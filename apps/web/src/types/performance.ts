export interface PerformanceMetrics {
  productivity_score: number;
  total_tasks: number;
  completed_tasks: number;
  completion_rate: number;
  average_roi: number;
  time_utilization: number;
  success_rate: number;
  task_completion_trend: Array<{
    date: string;
    count: number;
  }>;
  task_distribution: Array<{
    priority: string;
    count: number;
  }>;
  optimization_suggestions: string[];
}
