import TestConnection from './components/TestConnection';
import RawDataDisplay from './components/RawDataDisplay';
import { useTotals } from './hooks/useTotals';
import PortfolioPieChart from './components/PortfolioPieChart';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-3xl font-bold text-center mb-8">
          Test Connexion API Crypto
        </h1>
        
        <div className="space-y-4">
          <TestConnection />
          <PortfolioPieChart />
        </div>
      </div>
    </div>
  );
}