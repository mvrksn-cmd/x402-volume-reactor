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
pip install "x402[fastapi]" python-dotenv
```

## 4. Middleware (real v2 SDK)

In `main.py`:

```python
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServer

facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=os.environ["FACILITATOR_URL"]))
server = x402ResourceServer(facilitator)
server.register("eip155:8453", ExactEvmServerScheme())  # Base mainnet

routes = {
    "POST /v1/infer": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=os.environ["PAY_TO"],
                price=os.environ.get("PRICE", "0.01"),
                network="eip155:8453",
            ),
        ],
        mime_type="application/json",
        description="Volume reactor inference, per-call USDC billing",
    ),
}

app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)
```

Key v2 details:

- Middleware class: `PaymentMiddlewareASGI` (not the old `paymentMiddleware`)
- Network format: CAIP-2 (`eip155:8453` for Base mainnet)
- Price: string like `"$0.01"` (defaults to USDC) or explicit `AssetAmount`
- Register the EVM exact scheme before adding middleware

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