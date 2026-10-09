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
3. Install: `pip install "x402[fastapi]" python-dotenv`
4. Middleware is wired in `main.py` using `PaymentMiddlewareASGI` (x402 v2).
5. Set `PAY_TO`, `FACILITATOR_URL`, and `PRICE` in env.

## Grok Bot integration

Grok Bot is a supported x402 client. Users connect through the remote MCP, sign in with Coinbase, and pay for x402 resources directly from their USDC balance on Base — no API key, no subscription, no checkout.

What a Grok Bot user sees when they hit your endpoint:

1. They ask their bot to use the service (e.g. "run volume inference on this data").
2. The bot sends an HTTP request to your endpoint.
3. Your server returns HTTP 402 with the `PAYMENT-REQUIRED` header (price, asset, pay-to address).
4. The bot shows the user the price and asks for authorization.
5. The user approves; the bot signs the EIP-3009 authorization and retries.
6. Your server returns the result; settlement completes on Base in ~2 seconds.

Requirements on the user side:

- A Coinbase account with USDC on Base
- Grok Bot connected to Coinbase via the remote MCP (sign-in flow)
- A data budget set before the agent spends funds

Docs: https://docs.cdp.coinbase.com/x402/agentic-accounts/coinbase-for-agents

## Security notes

- A 2026 study found 31 vulnerabilities across 15 major x402 facilitators covering 99% of observed transactions (free shopping, asset theft, gas abuse).
- Verify payment signatures locally before trusting facilitator settlement.
- Watch facilitator fix status before production volume.

## Status

Middleware wired with real v2 SDK imports. Ready for wallet + facilitator credentials.

## License

MIT