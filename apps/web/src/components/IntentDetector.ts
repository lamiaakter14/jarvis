export type SystemMode = 'chat' | 'planner' | 'execution' | 'advisor' | 'memory';

export interface IntentResult {
  mode: SystemMode;
  confidence: number;
  trigger: string;
}

export function detectIntent(message: string): IntentResult {
  const lower = message.toLowerCase();
  if (/plan|idea|start|business|create|project|strategy|open|launch|shop|store/.test(lower)) {
    return { mode: 'planner', confidence: 0.85, trigger: 'planning_keyword' };
  }
  if (/do|execute|run|build|deploy|complete|finish/.test(lower)) {
    return { mode: 'execution', confidence: 0.75, trigger: 'execution_keyword' };
  }
  if (/what|why|how|when|who|explain|help|analyze/.test(lower)) {
    return { mode: 'advisor', confidence: 0.7, trigger: 'question_keyword' };
  }
  return { mode: 'chat', confidence: 0.3, trigger: 'default' };
}
