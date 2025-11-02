'use client';

import { useTotals } from '../hooks/useTotals';

export default function RawDataDisplay() {
  const { data, loading, error } = useTotals();

  if (loading || error) return null;

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4">Raw API data</h2>
      <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}