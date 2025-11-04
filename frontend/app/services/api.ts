const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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

export interface SnapshotItem {
  source: string;
  chain: string;
  asset: string;
  balance: number;
  address: string | null;
  price_usd: number | null;
  value_usd: number | null;
}

export interface Snapshot {
  id: number;
  fetched_at: string;
  items: SnapshotItem[];
}

export interface Balance {
  source: string;
  chain: string;
  asset: string;
  balance: number;
  address: string | null;
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

  async getBalances(): Promise<Balance[]> {
    const res = await fetch(`${API_BASE_URL}/balances`, {
      cache: 'no-store'
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    return res.json();
  },

  async createSnapshot(): Promise<Snapshot> {
    const res = await fetch(`${API_BASE_URL}/snapshots`, {
      method: 'POST',
      cache: 'no-store'
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    return res.json();
  },

  async getLatestSnapshot(): Promise<Snapshot> {
    const res = await fetch(`${API_BASE_URL}/snapshots/latest`, {
      cache: 'no-store'
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    return res.json();
  },

  async getAllSnapshots(limit: number = 30): Promise<Snapshot[]> {
    const res = await fetch(`${API_BASE_URL}/snapshots?limit=${limit}`, {
      cache: 'no-store'
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    return res.json();
  }
};