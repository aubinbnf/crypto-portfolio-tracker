'use client';

import { useTotals } from './hooks/useTotals';
import { useSnapshot } from './hooks/useSnapshot';
import DashboardHeader from './components/DashboardHeader';
import PortfolioStats from './components/PortfolioStats';
import PortfolioPieChart from './components/PortfolioPieChart';
import AssetTable from './components/AssetTable';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';

export default function Home() {
  const { data: totalsData, loading: totalsLoading, error: totalsError, refetch: refetchTotals } = useTotals();
  const { data: snapshotData, loading: snapshotLoading, createSnapshot } = useSnapshot();

  const handleRefresh = async () => {
    await Promise.all([
      refetchTotals(),
      createSnapshot()
    ]);
  };

  const isLoading = totalsLoading && !totalsData;
  const isRefreshing = totalsLoading || snapshotLoading;

  if (isLoading) {
    return <LoadingState />;
  }

  if (totalsError) {
    return <ErrorState message={totalsError} onRetry={refetchTotals} />;
  }

  if (!totalsData || totalsData.totals.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-8 flex items-center justify-center">
        <div className="max-w-md w-full mx-4">
          <div className="bg-white rounded-lg shadow border p-8 text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">No Assets Found</h2>
            <p className="text-gray-600 mb-6">
              Your portfolio is empty. Add some assets to get started.
            </p>
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              {isRefreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        <DashboardHeader
          totalValue={totalsData.total_usd}
          lastUpdate={snapshotData?.fetched_at || null}
          onRefresh={handleRefresh}
          isRefreshing={isRefreshing}
        />

        <PortfolioStats
          totals={totalsData.totals}
          totalValue={totalsData.total_usd}
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <PortfolioPieChart />

          <div className="bg-white rounded-lg shadow border p-6">
            <h3 className="text-lg font-semibold mb-4">Portfolio Distribution</h3>
            <div className="space-y-3">
              {totalsData.totals.slice(0, 10).map((asset, index) => {
                const percentage = (asset.value_usd / totalsData.total_usd) * 100;
                return (
                  <div key={asset.asset}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium text-gray-700">{asset.asset}</span>
                      <span className="text-gray-600">
                        ${asset.value_usd.toLocaleString()} ({percentage.toFixed(1)}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${Math.min(percentage, 100)}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <AssetTable
          totals={totalsData.totals}
          totalValue={totalsData.total_usd}
        />
      </div>
    </div>
  );
}