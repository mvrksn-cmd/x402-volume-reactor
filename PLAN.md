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

### Deploy checklist

- [ ] Phase 1 payer test passes (unpaid 402, paid 200)
- [ ] Phase 2 harness green, including expired-auth rejection
- [ ] Fresh Base wallet created; `PAY_TO` set to it
- [ ] Coinbase CDP facilitator account active; `FACILITATOR_URL` set
- [ ] `.env` filled: `PAY_TO`, `FACILITATOR_URL`, `PRICE` (default `0.01`)
- [ ] `Dockerfile` added (python:3.12-slim, `pip install -r requirements.txt`, `uvicorn main:app --host 0.0.0.0 --port 8000`)
- [ ] Container builds and runs locally: `docker build -t reactor . && docker run --env-file .env -p 8000:8000 reactor`
- [ ] `/health` returns 200 from inside the container
- [ ] Unpaid `POST /v1/infer` returns 402 with `PAYMENT-REQUIRED` header
- [ ] Paid request via `payer.py` returns 200 + settlement receipt
- [ ] HTTPS in front (reverse proxy or platform TLS) — x402 payments are worthless over plain HTTP
- [ ] Firewall: only 8000 exposed, SSH key-only
- [ ] Monitoring: log 402/200/5xx counts, facilitator error rate
- [ ] Free tier = 1,000 tx/month; set an alert before hitting the cap
- [ ] Day-one volume kept small until facilitator vulnerability fixes land

## Phase 4 — Watch numbers

- Track tx count, settlement success rate, facilitator errors.
- Free tier = 1,000 tx/month. Volume spike = signal to move to paid tier.

## Phase 5 — Harden

- Local signature verification before trusting facilitator settlement.
- Only then does production volume make sense.

## Order matters

No payer -> no tests. No tests -> no deploy. No deploy -> nothing to watch. No watching -> no scaling.