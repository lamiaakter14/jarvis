import { apiClient } from './axios';

export const healthApi = {
  checkHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};
