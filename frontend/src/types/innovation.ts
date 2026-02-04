export interface Innovation {
  id: string;
  title: string;
  description: string;
  category: string;
  impact_score: number;
  implementation_status: 'proposed' | 'in_progress' | 'implemented';
  notes?: string;
  created_at: string;
  implemented_at?: string;
}
