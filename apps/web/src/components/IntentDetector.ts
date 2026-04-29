// apps/web/src/components/IntentDetector.ts

export type SystemMode = 'chat' | 'planner' | 'execution' | 'advisor' | 'memory';

export interface IntentResult {
  mode: SystemMode;
  confidence: number;
  trigger: string;
}

const PLANNER_KEYWORDS = ['plan', 'start', 'idea', 'project', 'করতে চাই', 'খুলতে চাই', 'new', 'create', 'build'];
const EXECUTION_KEYWORDS = ['do', 'execute', 'run', 'start task', 'complete', 'finish', 'deploy'];
const QUESTION_KEYWORDS = ['কি', 'কেন', 'কিভাবে', 'কত', 'what', 'why', 'how', 'when', 'who'];
const MEMORY_KEYWORDS = ['remember', 'diary', 'note', 'save', 'মনে রাখো'];

export function detectIntent(message: string): IntentResult {
  const lower = message.toLowerCase();

  if (PLANNER_KEYWORDS.some(kw => lower.includes(kw))) {
    return { mode: 'planner', confidence: 0.85, trigger: 'planning_keyword' };
  }
  
  if (EXECUTION_KEYWORDS.some(kw => lower.includes(kw))) {
    return { mode: 'execution', confidence: 0.75, trigger: 'execution_keyword' };
  }
  
  if (QUESTION_KEYWORDS.some(kw => lower.includes(kw))) {
    return { mode: 'advisor', confidence: 0.7, trigger: 'question_keyword' };
  }
  
  if (MEMORY_KEYWORDS.some(kw => lower.includes(kw))) {
    return { mode: 'memory', confidence: 0.8, trigger: 'memory_keyword' };
  }

  return { mode: 'chat', confidence: 0.5, trigger: 'default' };
}

export const PLANNER_QUESTIONS = [
  'কেন এই idea/project? (Why this?)',
  'Target customer কে?',
  'Competition কে বা কী?',
  'তুমি unique কী দিচ্ছো?',
  'Budget কত?',
  'Timeline কেমন?',
  'Risk factor কী কী?'
];

export const MOCK_PLAN = {
  projectId: 'NirjharonProject-01',
  projectName: 'Demo Project',
  phases: [
    { id: '01', name: 'Market Research', status: 'pending' },
    { id: '02', name: 'Product Design', status: 'pending' },
    { id: '03', name: 'Branding', status: 'pending' },
    { id: '04', name: 'Website', status: 'pending' },
    { id: '05', name: 'Marketing', status: 'pending' }
  ],
  tasks: [
    { id: 'NirjharonWebUI-task01', title: 'Design landing page', assignee: 'Executor', status: 'pending' },
    { id: 'NirjharonContent-task02', title: 'Write product description', assignee: 'Executor', status: 'pending' },
    { id: 'NirjharonBrand-task03', title: 'Create logo concept', assignee: 'Innovator', status: 'pending' }
  ]
};