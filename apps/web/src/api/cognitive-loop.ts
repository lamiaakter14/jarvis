import { apiClient } from './axios';

export interface StrategistPlan {
  tasks?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

export interface MentorGaps {
  [key: string]: unknown;
}

export interface MentorTaskFeedbackItem {
  [key: string]: unknown;
}

export interface InnovatorResult {
  [key: string]: unknown;
}

export interface AmplifierPerformance {
  [key: string]: unknown;
}

export interface CognitiveLoopResult {
  status: string;
  strategist: {
    plan: StrategistPlan;
  };
  mentor: {
    gaps: MentorGaps;
    task_feedback: MentorTaskFeedbackItem[];
  };
  executor: {
    status: string;
  };
  innovator: {
    innovations: InnovatorResult;
  };
  amplifier: {
    performance: AmplifierPerformance;
  };
}

export const cognitiveLoopApi = {
  runLoop: async (): Promise<CognitiveLoopResult> => {
    const response = await apiClient.post<CognitiveLoopResult>('/api/cognitive-loop');
    return response.data;
  },
};
