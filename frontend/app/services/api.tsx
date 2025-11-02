const API_BASE_URL = 'http://localhost:8000';

interface CryptoItem {
  id: string;
  symbol: string;
  amount: number;
  purchase_price: number;
  current_value?: number;
}

export const cryptoAPI = {
  async getPortfolio(): Promise<CryptoItem[]> {
    const res = await fetch(`${API_BASE_URL}/portfolio`);
    if (!res.ok) throw new Error('Failed to fetch portfolio');
    return res.json();
  }
};