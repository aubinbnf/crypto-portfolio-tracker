'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { useHistory } from '../hooks/useHistory';

export default function PortfolioHistoryChart() {
  const { data, loading } = useHistory(30);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow border p-6">
        <h3 className="text-lg font-semibold mb-4">Portfolio History</h3>
        <div className="h-80 flex items-center justify-center">
          <div className="animate-pulse text-gray-400">Loading history...</div>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow border p-6">
        <h3 className="text-lg font-semibold mb-4">Portfolio History</h3>
        <div className="h-80 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p>No historical data available yet</p>
            <p className="text-sm mt-2">Data will appear after creating snapshots</p>
          </div>
        </div>
      </div>
    );
  }

  // Process data: calculate total value for each snapshot
  const chartData = data
    .map((snapshot) => {
      const totalValue = snapshot.items.reduce((sum, item) => {
        return sum + (item.value_usd || 0);
      }, 0);

      return {
        date: new Date(snapshot.fetched_at).toLocaleDateString('fr-FR', {
          day: '2-digit',
          month: 'short',
          hour: '2-digit',
          minute: '2-digit'
        }),
        timestamp: new Date(snapshot.fetched_at).getTime(),
        value: totalValue,
        snapshotId: snapshot.id
      };
    })
    .reverse(); // Reverse to show oldest to newest

  // Calculate percentage change
  const firstValue = chartData[0]?.value || 0;
  const lastValue = chartData[chartData.length - 1]?.value || 0;
  const percentChange = firstValue > 0 ? ((lastValue - firstValue) / firstValue) * 100 : 0;
  const isPositive = percentChange >= 0;

  return (
    <div className="bg-white rounded-lg shadow border p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold">Portfolio History</h3>
          <p className="text-sm text-gray-500">{chartData.length} snapshots</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-gray-900">
            ${lastValue.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </div>
          <div className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? '+' : ''}{percentChange.toFixed(2)}% sur la période
          </div>
        </div>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="date"
              stroke="#6B7280"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#6B7280' }}
            />
            <YAxis
              stroke="#6B7280"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#6B7280' }}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                padding: '12px'
              }}
              formatter={(value: number) => [
                `$${value.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
                })}`,
                'Valeur totale'
              ]}
              labelStyle={{ color: '#374151', fontWeight: 600, marginBottom: '4px' }}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#3B82F6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
