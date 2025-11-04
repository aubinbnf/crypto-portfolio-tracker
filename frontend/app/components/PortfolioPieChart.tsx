'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { useTotals } from '../hooks/useTotals';

export default function PortfolioPieChart() {
  const { data } = useTotals();

  if (!data) return null;

  const sorted = [...data.totals].sort((a, b) => b.value_usd - a.value_usd);
  const chartData = sorted.slice(0, 15);

  const colors = [
    '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
    '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1',
    '#A855F7', '#14B8A6', '#EAB308', '#64748B', '#DC2626'
  ];

  return (
    <div className="bg-white rounded-lg shadow border p-6">
      <h3 className="text-lg font-semibold mb-4">Portfolio Breakdown</h3>
      
      <div className="flex flex-col lg:flex-row items-center gap-4">
        <div className="w-full lg:w-1/2 h-80 flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <Pie
                data={chartData as any}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value_usd"
                nameKey="asset"
              >
                {chartData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value) => [`$${Number(value).toLocaleString()}`, 'Valeur']}
                contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="w-full lg:w-1/2 max-h-60 overflow-y-auto">
          <div className="space-y-2">
            {chartData.map((asset, index) => {
              const percentage = (asset.value_usd / data.total_usd) * 100;
              
              return (
                <div key={asset.asset} className="flex items-center text-sm">
                  <div 
                    className="w-3 h-3 rounded-full mr-3"
                    style={{ backgroundColor: colors[index] }}
                  ></div>
                  <span className="font-medium w-20">{asset.asset}</span>
                  <div className="flex-1 mx-2">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="h-2 rounded-full"
                        style={{ 
                          backgroundColor: colors[index],
                          width: `${Math.min(percentage, 100)}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-gray-600 min-w-16 text-right">
                    {percentage.toFixed(1)}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}