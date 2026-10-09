"""Volume reactor with x402 USDC billing on Base (v2 SDK)."""
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServer

load_dotenv()

PAY_TO = os.environ["PAY_TO"]
FACILITATOR_URL = os.environ["FACILITATOR_URL"]
PRICE = os.environ.get("PRICE", "0.01")

app = FastAPI(title="volume-reactor", version="0.1.0")

# x402 middleware setup
facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=FACILITATOR_URL))
server = x402ResourceServer(facilitator)
server.register("eip155:8453", ExactEvmServerScheme())  # Base mainnet

routes = {
    "POST /v1/infer": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=PAY_TO,
                price=PRICE,
                network="eip155:8453",
            ),
        ],
        mime_type="application/json",
        description="Volume reactor inference, per-call USDC billing",
    ),
}

app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/infer")
async def infer():
    """Paid endpoint. Returns 402 until a valid EIP-3009 payment is attached."""
    return {"result": "reactor output goes here"}