import { apiClient } from './axios';

export const plansApi = {
  getTodayPlan: async (): Promise<any> => {
    const response = await apiClient.get('/api/plan/today');
    return response.data.plan;
  },

  generatePlan: async (): Promise<any> => {
    const response = await apiClient.post('/api/plan/generate');
    return response.data.plan;
  },
};
