/**
 * Local Context Engine API Client
 * Phase 7: Store and retrieve local Bangladesh context
 */

const API_BASE = '/api/context';

export interface Context {
  id: string;
  category: string;
  key: string;
  value: string;
  location: string;
  source: string;
  created_at: string;
}

export async function getContexts(category?: string, keyword?: string): Promise<Context[]> {
  let url = API_BASE;
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (keyword) params.append('keyword', keyword);
  if (params.toString()) url += `?${params.toString()}`;
  
  const response = await fetch(url);
  return response.json();
}

export async function addContext(key: string, value: string, category: string, location: string = 'Sakhipur'): Promise<Context> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key, value, category, location })
  });
  return response.json();
}

export async function updateContext(id: string, updates: Partial<Context>): Promise<Context> {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  return response.json();
}

export async function deleteContext(id: string): Promise<void> {
  await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
}

export async function getCategories(): Promise<string[]> {
  const response = await fetch(`${API_BASE}/categories`);
  const data = await response.json();
  return data.categories;
}

export async function getForPlanner(keywords: string[]): Promise<Context[]> {
  const response = await fetch(`${API_BASE}/planner`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keywords })
  });
  return response.json();
}
