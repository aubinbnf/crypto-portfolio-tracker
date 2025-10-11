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

app/
 ├── connectors/         → Crypto API connectors
 ├── models/             → Pydantic and SQLAlchemy models
 ├── repositories/       → Database access
 ├── services/           → Business logic (aggregation, snapshots)
 └── main.py             → Entry point
data/                     → Local SQLite database
tests/                    → Unit tests
Dockerfile                → Docker container setup
docker-compose.yml        → Docker Compose configuration
README.md                 → Project documentation

# Local Installation

Clone the repository:

git clone https://github.com/aubinbnf/crypto-portfolio-tracker.git
cd crypto-portfolio-tracker

Install dependencies:

pip install -r requirements.txt

# Running with Docker

docker-compose up --build
