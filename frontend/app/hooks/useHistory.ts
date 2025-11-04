'use client';

import { useState, useEffect } from 'react';
import { cryptoAPI, Snapshot } from '../services/api';

export function useHistory(limit: number = 30) {
  const [data, setData] = useState<Snapshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadHistory();
  }, [limit]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const historyData = await cryptoAPI.getAllSnapshots(limit);
      setData(historyData);
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
    refetch: loadHistory
  };
}
