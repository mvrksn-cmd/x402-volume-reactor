# x402 Volume Reactor

Per-call USDC billing for a FastAPI volume reactor using the x402 payment protocol.

## What it does

- Gates any FastAPI endpoint behind a USDC payment on Base
- No accounts, no API keys, no checkout page
- Gasless for the payer via EIP-3009 (transferWithAuthorization)
- Facilitator settles on-chain; the server never touches a chain

## Pricing

| Price per call | Atomic units (6 decimals) |
|---|---|
| $0.001 | 1,000 |
| $0.01 | 10,000 |
| $0.10 | 100,000 |
| $1.00 | 1,000,000 |

Default: **$0.01 per call**.

## Setup

Full step-by-step instructions: **[INSTRUCTIONS.md](INSTRUCTIONS.md)**

1. Create a fresh Base wallet (pay-to address). Do not reuse your main wallet.
2. Sign up for the Coinbase CDP facilitator (free tier: 1,000 tx/month).
3. Install: `pip install x402`
4. Add one line of middleware to your FastAPI app.
5. Set `PAY_TO`, `FACILITATOR_URL`, and `PRICE` in env.

## Security notes

- A 2026 study found 31 vulnerabilities across 15 major x402 facilitators covering 99% of observed transactions (free shopping, asset theft, gas abuse).
- Verify payment signatures locally before trusting facilitator settlement.
- Watch facilitator fix status before production volume.

## Status

Scaffold. Middleware code to be added.

## License

MIT