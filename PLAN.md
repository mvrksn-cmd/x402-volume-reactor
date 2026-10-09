# Build Plan: x402 Volume Reactor

Synchronized order. Each phase gates the next.

## Phase 1 — Payer client (tomorrow morning)

- `payer.py` is in the repo: signs EIP-3009, retries the paid request.
- Run: `PAYER_PRIVATE_KEY=... PAY_TO=... python payer.py --url http://localhost:8000/v1/infer`
- Expect: unpaid -> 402, paid -> 200 + settlement receipt.
- Use a test wallet, never main.

## Phase 2 — Test harness

- Automate phase 1 as a scripted check (unpaid 402, paid 200).
- Add a negative test: expired authorization must be rejected.
- All green before deploy.

## Phase 3 — Deploy

- Docker or small VPS. Load env vars. Health check green.
- Reactor live and earning.

## Phase 4 — Watch numbers

- Track tx count, settlement success rate, facilitator errors.
- Free tier = 1,000 tx/month. Volume spike = signal to move to paid tier.

## Phase 5 — Harden

- Local signature verification before trusting facilitator settlement.
- Only then does production volume make sense.

## Order matters

No payer -> no tests. No tests -> no deploy. No deploy -> nothing to watch. No watching -> no scaling.