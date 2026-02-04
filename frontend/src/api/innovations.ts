import { apiClient } from './axios';
import { Innovation } from '../types/innovation';

export const innovationsApi = {
  getInnovations: async (): Promise<Innovation[]> => {
    const response = await apiClient.get('/api/innovations');
    return response.data.innovations || [];
  },
};
