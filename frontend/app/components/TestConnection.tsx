'use client';

import { useTotals } from '../hooks/useTotals';

export default function TestConnection() {
  const { data, loading, error } = useTotals();

  if (loading) {
    return (
      <div className="p-4 border border-blue-300 bg-blue-50 rounded">
        <p>Connection in progress...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 border border-red-300 bg-red-50 rounded">
        <p className="text-red-700">Error: {error}</p>
        <p className="text-sm mt-2">Verify that your backend is running correctly on localhost:8000</p>
      </div>
    );
  }

  return (
    <div className="p-4 border border-green-300 bg-green-50 rounded">
      <p className="text-green-700">Connection Successfull !</p>
      <p className="mt-2">Total USD: <strong>${data?.total_usd.toFixed(2)}</strong></p>
      <p className="text-sm">Number of assets: {data?.totals.length}</p>
    </div>
  );
}