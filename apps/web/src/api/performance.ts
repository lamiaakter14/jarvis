import { apiClient } from './axios';
import { PerformanceMetrics } from '../types/performance';

export const performanceApi = {
  getPerformance: async (): Promise<PerformanceMetrics> => {
    const response = await apiClient.get('/api/performance');
    return response.data.performance;
  },
};
