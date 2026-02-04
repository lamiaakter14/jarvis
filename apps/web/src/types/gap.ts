export interface Gap {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  evidence: string[];
  remediation_suggestions: string[];
  learning_priority_score: number;
  status: 'identified' | 'in_progress' | 'resolved';
  created_at: string;
  resolved_at?: string;
}
