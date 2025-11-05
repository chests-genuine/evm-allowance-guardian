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
