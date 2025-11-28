/**
 * SWR hooks for data fetching
 */
import useSWR from 'swr';
import type { Tender, TenderFilters, SourceConfig } from '@/types/api';
import { tenderApi, sourceApi } from '@/lib/api';

/**
 * Hook to fetch tenders list
 */
export function useTenders(filters?: TenderFilters) {
  const key = filters ? ['/tenders', filters] : '/tenders';

  const { data, error, isLoading, mutate } = useSWR(
    key,
    () => tenderApi.getTenders(filters),
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    }
  );

  return {
    tenders: data,
    isLoading,
    isError: error,
    mutate,
  };
}

/**
 * Hook to fetch single tender
 */
export function useTender(id: number | null) {
  const { data, error, isLoading, mutate } = useSWR(
    id ? `/tenders/${id}` : null,
    () => (id ? tenderApi.getTender(id) : null),
    {
      revalidateOnFocus: false,
    }
  );

  return {
    tender: data,
    isLoading,
    isError: error,
    mutate,
  };
}

/**
 * Hook to fetch sources list
 */
export function useSources(skip = 0, limit = 100) {
  const { data, error, isLoading, mutate } = useSWR(
    ['/sources', skip, limit],
    () => sourceApi.getSources(skip, limit),
    {
      revalidateOnFocus: false,
    }
  );

  return {
    sources: data,
    isLoading,
    isError: error,
    mutate,
  };
}

/**
 * Hook to fetch single source
 */
export function useSource(id: number | null) {
  const { data, error, isLoading, mutate } = useSWR(
    id ? `/sources/${id}` : null,
    () => (id ? sourceApi.getSource(id) : null),
    {
      revalidateOnFocus: false,
    }
  );

  return {
    source: data,
    isLoading,
    isError: error,
    mutate,
  };
}
