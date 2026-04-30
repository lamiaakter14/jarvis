/**
 * Money Mode API Client
 * Phase 6: Money Mode — Income Planning & Tracking
 * v5.3.0
 */

const API_BASE = '/api/money';

export interface MoneyPlanRequest {
  target_amount: number;
  days: number;
  skills: string[];
}

export interface MoneyPlanResponse {
  goal: {
    amount: number;
    days: number;
    daily_target: number;
    hourly_rate: number;
    hours_needed_per_day: number;
    total_hours_needed: number;
  };
  skills: string[];
  recommended_platforms: string[];
  platform_details: Record<string, any>;
  daily_plan: Array<{
    day: number;
    title: string;
    tasks: string[];
    estimated_earnings: number;
    time_needed: number;
  }>;
  tips: string[];
  survival_quote: string;
}

export interface ProgressResponse {
  current: number;
  target: number;
  percentage: number;
  remaining: number;
  status: string;
  message: string;
}

/**
 * Generate income plan based on target, days, and skills
 */
export async function generateMoneyPlan(request: MoneyPlanRequest): Promise<MoneyPlanResponse> {
  const response = await fetch(`${API_BASE}/plan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Plan generation failed: ${error}`);
  }

  return response.json();
}

/**
 * Track income progress against target
 */
export async function trackProgress(current: number, target: number): Promise<ProgressResponse> {
  const response = await fetch(`${API_BASE}/progress?current=${current}&target=${target}`);

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Progress tracking failed: ${error}`);
  }

  return response.json();
}

/**
 * Quick calculation: daily rate needed
 */
export function calculateDailyRate(target: number, days: number): number {
  return target / days;
}

/**
 * Estimate hours needed based on skill rate
 */
export function estimateHoursNeeded(dailyTarget: number, hourlyRate: number): number {
  return dailyTarget / hourlyRate;
}
