import { apiClient } from './axios';
import { Plan } from '../types/plan';

export const plansApi = {
  getTodayPlan: async (): Promise<Plan> => {
    const response = await apiClient.get('/api/plan/today');
    return response.data.plan;
  },

  generatePlan: async (): Promise<Plan> => {
    const response = await apiClient.post('/api/plan/generate');
    return response.data.plan;
  },
};
