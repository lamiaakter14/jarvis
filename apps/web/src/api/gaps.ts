import { apiClient } from './axios';
import { Gap } from '../types/gap';

export const gapsApi = {
  getGaps: async (): Promise<Gap[]> => {
    const response = await apiClient.get('/api/gaps');
    return response.data.gaps || [];
  },
};
