"""Volume reactor with x402 USDC billing on Base.

Scaffold only. Wire paymentMiddleware once the x402 SDK version is pinned.
"""
import os
from fastapi import FastAPI

app = FastAPI(title="volume-reactor", version="0.1.0")

PAY_TO = os.environ["PAY_TO"]
PRICE = os.environ.get("PRICE", "0.01")

# TODO: from x402.middleware.fastapi import paymentMiddleware
# app.add_middleware(
#     paymentMiddleware,
#     pay_to=PAY_TO,
#     price=PRICE,
#     network="base",
#     asset="USDC",
#     facilitator_url=os.environ["FACILITATOR_URL"],
# )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/infer")
def infer():
    """Paid endpoint. Returns 402 until payment middleware is enabled."""
    return {"result": "reactor output goes here"}