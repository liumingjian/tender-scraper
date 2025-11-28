/**
 * Type definitions for Tender Scraper API
 */

export interface Tender {
  id: number;
  source_name: string;
  source_url: string;
  title: string;
  content: string;
  project_name?: string;
  budget_amount?: number;
  budget_currency?: string;
  deadline?: string;
  contact_person?: string;
  contact_phone?: string;
  contact_email?: string;
  location?: string;
  is_filtered: boolean;
  filter_reason?: string;
  is_manually_corrected: boolean;
  published_at?: string;
  created_at: string;
  updated_at: string;
}

export interface TenderUpdate {
  project_name?: string;
  budget_amount?: number;
  budget_currency?: string;
  deadline?: string;
  contact_person?: string;
  contact_phone?: string;
  contact_email?: string;
  location?: string;
  is_manually_corrected?: boolean;
}

export interface SourceConfig {
  id: number;
  name: string;
  url: string;
  scraper_type: 'http' | 'browser';
  config: Record<string, any>;
  filter_rules?: FilterRules;
  is_active: boolean;
  schedule_cron?: string;
  last_run_at?: string;
  created_at: string;
  updated_at: string;
}

export interface SourceConfigCreate {
  name: string;
  url: string;
  scraper_type: 'http' | 'browser';
  config: Record<string, any>;
  filter_rules?: FilterRules;
  is_active?: boolean;
  schedule_cron?: string;
}

export interface FilterRules {
  include_keywords?: string[];
  exclude_keywords?: string[];
  title_include?: string[];
  title_exclude?: string[];
  min_budget?: number;
  max_budget?: number;
}

export interface TaskRunRequest {
  source_id?: number;
  limit?: number;
}

export interface TaskRunResponse {
  success: boolean;
  message: string;
  results: TaskResult[];
}

export interface TaskResult {
  source_name: string;
  scraped?: number;
  processed?: number;
  filtered?: number;
  errors?: number;
  error?: string;
}

export interface PaginationParams {
  skip?: number;
  limit?: number;
}

export interface TenderFilters extends PaginationParams {
  source_name?: string;
  keyword?: string;
  min_budget?: number;
  max_budget?: number;
  include_filtered?: boolean;
}
