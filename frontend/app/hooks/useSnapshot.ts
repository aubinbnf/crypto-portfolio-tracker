'use client';

import { useState, useEffect } from 'react';
import { cryptoAPI, Snapshot } from '../services/api';

export function useSnapshot() {
  const [data, setData] = useState<Snapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSnapshot();
  }, []);

  const loadSnapshot = async () => {
    try {
      setLoading(true);
      setError(null);
      const snapshotData = await cryptoAPI.getLatestSnapshot();
      setData(snapshotData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error has occurred');
    } finally {
      setLoading(false);
    }
  };

  const createSnapshot = async () => {
    try {
      setLoading(true);
      setError(null);
      const newSnapshot = await cryptoAPI.createSnapshot();
      setData(newSnapshot);
      return newSnapshot;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create snapshot');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    loading,
    error,
    refetch: loadSnapshot,
    createSnapshot
  };
}
