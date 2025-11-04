'use client';

import { TotalItem } from '../services/api';

interface PortfolioStatsProps {
  totals: TotalItem[];
  totalValue: number;
}

export default function PortfolioStats({ totals, totalValue }: PortfolioStatsProps) {
  // Calculate stats
  const numberOfAssets = totals.length;
  const topAsset = totals.reduce((prev, current) =>
    (prev.value_usd > current.value_usd) ? prev : current
  , totals[0]);

  const btcValue = totals.find(t => t.asset === 'BTC')?.value_usd || 0;
  const ethValue = totals.find(t => t.asset === 'ETH')?.value_usd || 0;

  const stats = [
    {
      label: 'Total Assets',
      value: numberOfAssets.toString(),
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      ),
      color: 'bg-blue-500'
    },
    {
      label: 'Top Asset',
      value: topAsset?.asset || 'N/A',
      subValue: topAsset && topAsset.value_usd !== null ? `$${topAsset.value_usd.toLocaleString()}` : '',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      ),
      color: 'bg-green-500'
    },
    {
      label: 'Bitcoin Value',
      value: `$${btcValue.toLocaleString()}`,
      subValue: btcValue > 0 ? `${((btcValue / totalValue) * 100).toFixed(1)}%` : '0%',
      icon: (
        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
          <path d="M23.638 14.904c-1.602 6.43-8.113 10.34-14.542 8.736C2.67 22.05-1.244 15.525.362 9.105 1.962 2.67 8.475-1.243 14.9.358c6.43 1.605 10.342 8.115 8.738 14.548v-.002zm-6.35-4.613c.24-1.59-.974-2.45-2.64-3.03l.54-2.153-1.315-.33-.525 2.107c-.345-.087-.705-.167-1.064-.25l.526-2.127-1.32-.33-.54 2.165c-.285-.067-.565-.132-.84-.2l-1.815-.45-.35 1.407s.975.225.955.236c.535.136.63.486.615.766l-1.477 5.92c-.075.166-.24.406-.614.314.015.02-.96-.24-.96-.24l-.66 1.51 1.71.426.93.242-.54 2.19 1.32.327.54-2.17c.36.1.705.19 1.05.273l-.51 2.154 1.32.330.545-2.19c2.24.427 3.93.257 4.64-1.774.57-1.637-.03-2.58-1.217-3.196.854-.193 1.5-.76 1.68-1.93h.01zm-3.01 4.22c-.404 1.64-3.157.75-4.05.53l.72-2.9c.896.23 3.757.67 3.33 2.37zm.41-4.24c-.37 1.49-2.662.735-3.405.55l.654-2.64c.744.18 3.137.524 2.75 2.084v.006z"/>
        </svg>
      ),
      color: 'bg-orange-500'
    },
    {
      label: 'Ethereum Value',
      value: `$${ethValue.toLocaleString()}`,
      subValue: ethValue > 0 ? `${((ethValue / totalValue) * 100).toFixed(1)}%` : '0%',
      icon: (
        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
          <path d="M11.944 17.97L4.58 13.62 11.943 24l7.37-10.38-7.372 4.35h.003zM12.056 0L4.69 12.223l7.365 4.354 7.365-4.35L12.056 0z"/>
        </svg>
      ),
      color: 'bg-purple-500'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow border p-6">
          <div className="flex items-center justify-between mb-3">
            <div className={`${stat.color} text-white p-3 rounded-lg`}>
              {stat.icon}
            </div>
          </div>
          <h3 className="text-sm text-gray-500 mb-1">{stat.label}</h3>
          <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
          {stat.subValue && (
            <p className="text-sm text-gray-600 mt-1">{stat.subValue}</p>
          )}
        </div>
      ))}
    </div>
  );
}
