from __future__ import annotations
import argparse
import os
from typing import List, Optional

from web3 import Web3
from eth_account import Account

from .allowances import check_allowances, connect
from .erc20 import ERC20

def _print_table(rows: List[tuple]):
    if not rows:
        print("No results.")
        return
    widths = [max(len(str(x[i])) for x in rows) for i in range(4)]
    header = ("chain", "token", "spender", "allowance")
    widths = [max(widths[i], len(header[i])) for i in range(4)]
    print(" | ".join(h.ljust(widths[i]) for i, h in enumerate(header)))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(" | ".join(str(r[i]).ljust(widths[i]) for i in range(4)))

def cmd_check(args: argparse.Namespace) -> None:
    chains = [args.chain] if args.chain else None
    rows = check_allowances(args.address, chains)
    _print_table(rows)

def cmd_revoke(args: argparse.Namespace) -> None:
    chain = args.chain
    token = Web3.to_checksum_address(args.token)
    spender = Web3.to_checksum_address(args.spender)
    pk = os.getenv("PRIVATE_KEY")
    if not pk:
        raise SystemExit("PRIVATE_KEY env var is required for revoke")

    w3 = connect(chain)
    acct = Account.from_key(pk)
    erc = ERC20(w3, token)

    # Build transaction
    tx_fn = erc.contract.functions.approve(spender, 0)
    nonce = w3.eth.get_transaction_count(acct.address)
    tx = tx_fn.build_transaction({
        "from": acct.address,
        "nonce": nonce,
    })
    # Fill gas
    tx["gas"] = tx.get("gas") or w3.eth.estimate_gas(tx)
    tx["maxFeePerGas"] = tx.get("maxFeePerGas") or w3.eth.gas_price
    tx["maxPriorityFeePerGas"] = tx.get("maxPriorityFeePerGas") or w3.eth.gas_price // 10
    tx["chainId"] = tx.get("chainId") or w3.eth.chain_id

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Sent revoke tx: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Status: {receipt.status} | Gas used: {receipt.gasUsed}")

def main(argv: Optional[List[str]] = None) -> None:
    p = argparse.ArgumentParser(prog="evm-allowance-guardian")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Audit allowances")
    p_check.add_argument("--address", required=True, help="Wallet address")
    p_check.add_argument("--chain", help="Single chain (default: all configured)")
    p_check.set_defaults(func=cmd_check)

    p_revoke = sub.add_parser("revoke", help="Revoke an approval (approve spender to 0)")
    p_revoke.add_argument("--chain", required=True, help="Target chain")
    p_revoke.add_argument("--token", required=True, help="Token address")
    p_revoke.add_argument("--spender", required=True, help="Spender address")
    p_revoke.set_defaults(func=cmd_revoke)

    args = p.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
