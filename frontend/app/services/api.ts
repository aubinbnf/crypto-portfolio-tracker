const API_BASE_URL = 'http://localhost:8000';

export interface TotalItem {
  asset: string;
  balance: number;
  price_usd: number;
  value_usd: number;
}

export interface TotalsResponse {
  totals: TotalItem[];
  total_usd: number;
}

export const cryptoAPI = {
  async getTotals(): Promise<TotalsResponse> {
    const res = await fetch(`${API_BASE_URL}/totals`, {
      cache: 'no-store'
    });
    
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    
    return res.json();
  },
};