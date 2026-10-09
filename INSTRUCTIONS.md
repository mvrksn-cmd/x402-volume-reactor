# Instructions: Wire x402 USDC Middleware

Clean, ordered steps. Do not skip.

## 1. Wallet

- Create a fresh Base wallet. This is your `PAY_TO` address.
- Never reuse your main wallet.

## 2. Facilitator

- Sign up at Coinbase CDP: https://docs.cdp.coinbase.com/x402/welcome
- Free tier: 1,000 transactions/month.
- Set `FACILITATOR_URL` in `.env`.

## 3. Install

```bash
pip install x402
```

## 4. Middleware (one line)

In `main.py`, after creating the FastAPI app:

```python
from x402.middleware.fastapi import paymentMiddleware

app.add_middleware(
    paymentMiddleware,
    pay_to=os.environ["PAY_TO"],
    price=os.environ.get("PRICE", "0.01"),
    network="base",
    asset="USDC",
    facilitator_url=os.environ["FACILITATOR_URL"],
)
```

## 5. Env

Copy `.env.example` to `.env` and fill in:

- `PAY_TO` — your Base wallet address
- `FACILITATOR_URL` — CDP facilitator endpoint
- `PRICE` — default `0.01` USDC per call

## 6. Verify

- Unpaid request to `/v1/infer` must return HTTP 402 with `PAYMENT-REQUIRED` header.
- Paid request (signed EIP-3009 auth) must return 200.
- Settlement latency on Base: ~2 seconds. Gasless for payer.

## 7. Security (do not skip)

- A 2026 study found 31 vulnerabilities across 15 major x402 facilitators (99% of observed transactions).
- Verify payment signatures locally before trusting facilitator settlement.
- Watch facilitator fix status before production volume.

## Pricing reference

| Price per call | Atomic units (6 decimals) |
|---|---|
| $0.001 | 1,000 |
| $0.01 | 10,000 |
| $0.10 | 100,000 |
| $1.00 | 1,000,000 |

## License

MIT