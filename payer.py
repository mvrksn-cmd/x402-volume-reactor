"""
x402 payer client for volume-reactor.

Signs an EIP-3009 transferWithAuthorization and retries the paid request.
Phase 1 of the build plan. Run against a local or deployed reactor.

Usage:
    python payer.py --url http://localhost:8000/v1/infer

Env:
    PAYER_PRIVATE_KEY  - hex private key of the paying wallet (test wallet, not main)
    PAY_TO             - reactor's Base wallet address
"""
import argparse
import json
import os
import time

import requests
from eth_account import Account
from eth_account.messages import encode_typed_data
from web3 import Web3

USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
EIP712_DOMAIN = {
    "name": "USD Coin",
    "version": "2",
    "chainId": 8453,
    "verifyingContract": USDC_BASE,
}
EIP712_TYPES = {
    "TransferWithAuthorization": [
        {"name": "from", "type": "address"},
        {"name": "to", "type": "address"},
        {"name": "value", "type": "uint256"},
        {"name": "validAfter", "type": "uint256"},
        {"name": "validBefore", "type": "uint256"},
        {"name": "nonce", "type": "bytes32"},
    ]
}
PAYMENT_REQUIRED_HEADER = "PAYMENT-REQUIRED"
PAYMENT_SIGNATURE_HEADER = "PAYMENT-SIGNATURE"
PAYMENT_RESPONSE_HEADER = "PAYMENT-RESPONSE"


def build_payment_payload(account: Account, pay_to: str, amount_atomic: str) -> dict:
    now = int(time.time())
    nonce = os.urandom(32)
    message = {
        "from": account.address,
        "to": Web3.to_checksum_address(pay_to),
        "value": int(amount_atomic),
        "validAfter": now - 60,
        "validBefore": now + 300,
        "nonce": nonce,
    }
    signable = encode_typed_data(EIP712_DOMAIN, EIP712_TYPES, message)
    signed = account.sign_message(signable)
    return {
        "x402Version": 2,
        "scheme": "exact",
        "network": "eip155:8453",
        "asset": USDC_BASE,
        "amount": amount_atomic,
        "payTo": pay_to,
        "validAfter": message["validAfter"],
        "validBefore": message["validBefore"],
        "nonce": nonce.hex(),
        "signature": signed.signature.hex(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/v1/infer")
    parser.add_argument("--amount", default="10000", help="atomic units, 10000 = $0.01 USDC")
    args = parser.parse_args()

    pk = os.environ["PAYER_PRIVATE_KEY"]
    pay_to = os.environ["PAY_TO"]
    account = Account.from_key(pk)

    print(f"payer: {account.address}")
    print(f"target: {args.url}")

    # 1. unpaid request -> expect 402
    r = requests.post(args.url)
    print(f"unpaid status: {r.status_code}")
    if r.status_code != 402:
        print("FAIL: expected 402 Payment Required")
        return 1
    pr = json.loads(r.headers[PAYMENT_REQUIRED_HEADER])
    print(f"payment required: {pr['accepts'][0]['amount']} atomic units")

    # 2. sign + retry
    payload = build_payment_payload(account, pay_to, args.amount)
    r2 = requests.post(
        args.url,
        headers={PAYMENT_SIGNATURE_HEADER: json.dumps(payload)},
    )
    print(f"paid status: {r2.status_code}")
    if r2.status_code == 200:
        print("PASS: paid request succeeded")
        if PAYMENT_RESPONSE_HEADER in r2.headers:
            print("settlement:", r2.headers[PAYMENT_RESPONSE_HEADER][:120])
        return 0
    print("FAIL: paid request did not return 200")
    print(r2.text[:500])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())