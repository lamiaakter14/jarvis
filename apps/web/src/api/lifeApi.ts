/**
 * Long-term Life System API Client
 * Phase 8: MP Election 2036, Skills, Islamic Practice
 */

const API_BASE = '/api/life';

export interface Skill {
  current: number;
  required: number;
  priority: string;
}

export interface Milestone {
  year: number;
  title: string;
  completed: boolean;
}

export interface DashboardData {
  mp_election_2036: {
    target_year: number;
    target_role: string;
    constituency: string;
    progress: number;
    milestones: Milestone[];
  };
  mp_progress: number;
  milestones: {
    completed: number;
    total: number;
    percentage: number;
  };
  skills: Record<string, Skill>;
  skill_gap: {
    average_current: number;
    average_required: number;
    gap: number;
  };
  network: {
    political: number;
    social: number;
    business: number;
    total: number;
    target: number;
    contacts?: any[];
  };
  islamic_practice: {
    daily_prayers: Record<string, boolean>;
    quran_pages_today: number;
    quran_completion: number;
    fasting: Record<string, number>;
  };
  daily_accountability: Array<{ date: string; task: string; completed: boolean }>;
}

export async function getDashboard(): Promise<DashboardData> {
  const response = await fetch(`${API_BASE}/dashboard`);
  return response.json();
}

export async function updateSkill(skillName: string, currentLevel: number): Promise<any> {
  const response = await fetch(`${API_BASE}/skill`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ skill_name: skillName, current_level: currentLevel })
  });
  return response.json();
}

export async function updatePrayer(prayerName: string, completed: boolean): Promise<any> {
  const response = await fetch(`${API_BASE}/prayer`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prayer_name: prayerName, completed })
  });
  return response.json();
}

export async function updateQuran(pages: number): Promise<any> {
  const response = await fetch(`${API_BASE}/quran`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pages })
  });
  return response.json();
}

export async function addContact(category: string, name: string, role: string): Promise<any> {
  const response = await fetch(`${API_BASE}/contact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category, name, role })
  });
  return response.json();
}

export async function addAccountability(task: string): Promise<any> {
  const response = await fetch(`${API_BASE}/accountability`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task })
  });
  return response.json();
}

export async function updateMilestone(index: number, completed: boolean): Promise<any> {
  const response = await fetch(`${API_BASE}/milestone`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ milestone_index: index, completed })
  });
  return response.json();
}
