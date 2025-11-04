'use client';

import { useState, useEffect } from 'react';
import { cryptoAPI, TotalsResponse } from '../services/api';

export function useTotals() {
  const [data, setData] = useState<TotalsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load from cache on initial mount (fast)
    loadTotalsFromCache();
  }, []);

  const loadTotalsFromCache = async () => {
    try {
      setLoading(true);
      setError(null);
      const totalsData = await cryptoAPI.getTotalsCached();
      setData(totalsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error has occurred');
    } finally {
      setLoading(false);
    }
  };

  const loadTotals = async () => {
    try {
      setLoading(true);
      setError(null);
      const totalsData = await cryptoAPI.getTotals();
      setData(totalsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error has occurred');
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    loading,
    error,
    refetch: loadTotalsFromCache // Reload from cache (fast)
  };
}