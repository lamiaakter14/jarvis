/**
 * Diary API Client for Jarvis OS
 * Handles all diary-related API calls
 */

// Use relative URL for proxy or environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export interface DiaryEntry {
  id: string;
  date: string;
  content: string;
  attachments: Array<{
    filename: string;
    saved_as: string;
    path: string;
    type: string;
    size: number;
  }>;
  tags: string[];
  mood?: string;
  created_at: string;
  updated_at: string;
}

export interface DiaryEntryCreate {
  date: string;
  content: string;
  tags?: string[];
  mood?: string;
}

export interface DiaryStats {
  total_entries: number;
  total_attachments: number;
  total_size_mb: number;
  storage_path: string;
}

class DiaryApi {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `API Error: ${response.statusText}`);
    }

    return response.json();
  }

  private async formRequest<T>(endpoint: string, formData: FormData): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `API Error: ${response.statusText}`);
    }

    return response.json();
  }

  async createOrUpdateEntry(date: string, content: string, tags?: string[], mood?: string): Promise<DiaryEntry> {
    const formData = new FormData();
    formData.append('date', date);
    formData.append('content', content);
    if (tags && tags.length > 0) {
      formData.append('tags', tags.join(','));
    }
    if (mood) {
      formData.append('mood', mood);
    }

    return this.formRequest<DiaryEntry>('/diary/entry', formData);
  }

  async createEntryWithAttachments(
    date: string,
    content: string,
    files: File[],
    tags?: string[],
    mood?: string
  ): Promise<any> {
    const formData = new FormData();
    formData.append('date', date);
    formData.append('content', content);
    if (tags && tags.length > 0) {
      formData.append('tags', tags.join(','));
    }
    if (mood) {
      formData.append('mood', mood);
    }
    
    files.forEach(file => {
      formData.append('files', file);
    });

    return this.formRequest('/diary/entry/with-attachments', formData);
  }

  async getEntryByDate(date: string): Promise<DiaryEntry> {
    return this.request<DiaryEntry>(`/diary/entry/${date}`);
  }

  async getAllEntries(limit: number = 50, offset: number = 0): Promise<DiaryEntry[]> {
    return this.request<DiaryEntry[]>(`/diary/entries?limit=${limit}&offset=${offset}`);
  }

  async searchEntries(query: string): Promise<{ results: DiaryEntry[]; count: number }> {
    return this.request<{ results: DiaryEntry[]; count: number }>(`/diary/search?q=${encodeURIComponent(query)}`);
  }

  async deleteEntry(date: string): Promise<{ message: string; success: boolean }> {
    return this.request(`/diary/entry/${date}`, { method: 'DELETE' });
  }

  async getStats(): Promise<DiaryStats> {
    return this.request<DiaryStats>('/diary/stats');
  }

  async getEntrySummary(date: string): Promise<any> {
    return this.request(`/diary/summary/${date}`);
  }
}

export const diaryApi = new DiaryApi();
