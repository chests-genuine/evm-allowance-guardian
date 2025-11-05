# evm-allowance-guardian

Audit and revoke ERC-20 allowances across EVM chains from your terminal.

- **Audit**: Check allowances for a wallet against a curated list of token and spender addresses.
- **Revoke**: Set approval to `0` for a given token+spender (optional, requires private key).

> Safe by default: read-only. Write actions require explicit flags and a private key.

## Features

- Multi-chain (Ethereum, Base, Arbitrum, Polygon, BNB Smart Chain—configurable).
- Plain JSON config for tokens/spenders per chain.
- Gas-aware revocation (estimates gas; lets node choose a reasonable fee).
- Minimal dependencies, no indexers.

## Install

```bash
git clone https://github.com/yourname/evm-allowance-guardian.git
cd evm-allowance-guardian
python -m venv .venv && source .venv/bin/activate
pip install -e .
```
> SOptionally set RPC endpoints through env vars (see Configuration).

## Quick start

```bash
# 1) Audit allowances for a wallet on all configured chains
python -m src.cli check --address 0xYourWallet

# 2) Audit only on a specific chain
python -m src.cli check --address 0xYourWallet --chain ethereum

# 3) Revoke a specific approval (requires PRIVATE_KEY)
export PRIVATE_KEY=0xabc123...deadbeef
python -m src.cli revoke \
  --chain base \
  --token 0xTokenAddress \
  --spender 0xSpenderAddress
```

Sample output:
```bash
[ethereum] USDC (6) allowance → 0xSpender: 0
[base]     WETH (18) allowance → 0xRouter: 115792089237316195... (UNLIMITED)
```
## Configuration
Networks are defined in src/networks.py. You may override RPCs via env:

RPC_ETHEREUM, RPC_BASE, RPC_ARBITRUM, RPC_POLYGON, RPC_BSC

Tokens and spenders sit in src/data/tokens.json and src/data/spenders.json by chain:
```bash
{
  "ethereum": [
    {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "symbol": "USDC", "decimals": 6}
  ],
  "base": [
    {"address": "0x4200000000000000000000000000000000000006", "symbol": "WETH", "decimals": 18}
  ]
}
```
> Note: Addresses here are examples; update them to your needs.

## Security
- Keep your PRIVATE_KEY safe; prefer .env or ephemeral shells.
- Revocations are on-chain and cost gas.
- Always verify token/spender addresses before revoking.

## Roadmap
1. CSV/Markdown export for audit results.

2. Auto-discover “unlimited” approvals via recent logs (best-effort).

3. Trezor/Ledger signing (via external signer).

## Author
Maintainer: chests-genuine

License: MIT
