# Crypto Portfolio Tracker

An open-source platform to automatically track your crypto portfolio across multiple sources:

- Exchanges (Binance)

- Wallets (Ledger, Metamask, etc. via Etherscan / Blockstream)

- Public blockchains

The goal is to centralize all your crypto holdings, aggregate balances, and calculate their USD value.

## Features

API connections to Binance, Etherscan, and Blockstream

Automatic aggregation of all balances

USD value conversion (via CoinGecko)

Local persistence using SQLite

FastAPI endpoints for interacting with your data

Dockerized for easy deployment

## Project Structure

```
backend/
 ├── config/
 │   ├── chains.yaml         → PUBLIC: Blockchain configurations (committed)
 │   ├── wallets.yaml        → PRIVATE: Your wallet addresses (gitignored)
 │   ├── wallets.yaml.example → Template for wallets.yaml
 │   ├── assets.yaml         → PUBLIC: Token symbol mappings
 │   └── config_manager.py   → Centralized configuration loader
 ├── connectors/             → Crypto API connectors
 ├── models/                 → Pydantic and SQLAlchemy models
 ├── repositories/           → Database access
 ├── services/               → Business logic (aggregation, snapshots)
 └── main.py                 → Entry point
frontend/                    → Next.js frontend application
data/                        → Local SQLite database
tests/                       → Unit tests
docker-compose.yml           → Docker Compose configuration
```

### Configuration Architecture

The app uses a **3-file configuration system** that separates public configs from private secrets:

1. **`chains.yaml`** (PUBLIC) - Blockchain configurations
   - Chain IDs, RPC endpoints, explorer APIs
   - Token contract addresses
   - Can be safely committed to git

2. **`wallets.yaml`** (PRIVATE) - Your wallet addresses
   - User-specific wallet addresses
   - **NEVER commit this file**
   - Already in `.gitignore`

3. **`assets.yaml`** (PUBLIC) - Asset metadata
   - CoinGecko ID mappings
   - Token symbol definitions

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aubinbnf/crypto-portfolio-tracker.git
cd crypto-portfolio-tracker
```

### 2. Configure environment variables

**Create your `.env` file from the example:**

```bash
cp backend/.env.example backend/.env
```

**Edit `backend/.env` and add your API keys:**

```bash
# Binance API credentials
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Etherscan API
ETHERSCAN_API_KEY=your_etherscan_api_key_here

# Wallet addresses to track (comma-separated)
ETH_ADDRESSES=0xYourEthAddress1, 0xYourEthAddress2
BTC_ADDRESSES=bc1YourBtcAddress1, bc1YourBtcAddress2

# Infura API (for Ethereum RPC)
INFURA_API_KEY=your_infura_api_key_here

# Chainstack API (alternative RPC)
CHAINSTACK_API_KEY=your_chainstack_api_key_here

# Database configuration
SQLALCHEMY_DATABASE_URL=sqlite:///./data/portfolio.db

# CORS configuration (comma-separated origins)
CORS_ORIGINS=http://localhost:3000
```

**For production deployment**, add your domain to CORS_ORIGINS:
```bash
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com,https://www.yourdomain.com
```

**Where to get API keys:**

- **Binance API**: https://www.binance.com/en/my/settings/api-management
  - Create a new API key with "Read Only" permissions (no trading needed)

- **Etherscan API**: https://etherscan.io/myapikey
  - Free tier: 5 requests/second

- **Infura**: https://app.infura.io/
  - Free tier: 100,000 requests/day

- **Chainstack**: https://console.chainstack.com/
  - Alternative RPC provider

**Configure wallet addresses:**

```bash
cp backend/config/wallets.yaml.example backend/config/wallets.yaml
```

Edit `backend/config/wallets.yaml` and add your wallet addresses:

```yaml
wallets:
  ethereum_mainnet:
    - "0xYourAddress1"
    - "0xYourAddress2"

  bitcoin:
    - "bc1YourBitcoinAddress"
```

**Security best practices:**

```bash
# Set restrictive permissions on sensitive files
chmod 600 backend/.env
chmod 600 backend/config/wallets.yaml
```

⚠️ **NEVER commit `backend/.env` or `backend/config/wallets.yaml` to git!** They're already in `.gitignore`.

### 3. Choose your installation method

## Running Locally (Development)

**Backend:**

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Access the app at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Running with Docker

**Start all services:**

```bash
docker-compose up --build
```

**Stop services:**

```bash
docker-compose down
```

**View logs:**

```bash
docker-compose logs -f
```
