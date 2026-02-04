import { apiClient } from './axios';

export interface CognitiveLoopResult {
  status: string;
  strategist: {
    plan: any;
  };
  mentor: {
    gaps: any;
    task_feedback: any[];
  };
  executor: {
    status: string;
  };
  innovator: {
    innovations: any;
  };
  amplifier: {
    performance: any;
  };
}

export const cognitiveLoopApi = {
  runLoop: async (): Promise<CognitiveLoopResult> => {
    const response = await apiClient.post<CognitiveLoopResult>('/api/cognitive-loop');
    return response.data;
  },
};
