from __future__ import annotations

import os
from datetime import UTC, datetime

from fastapi import FastAPI


app = FastAPI(title="E-Commerce Analytics Operations API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": os.getenv("SERVICE_NAME", "ecommerce-analytics-api"),
        "checked_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }


@app.get("/readiness")
def readiness() -> dict[str, str]:
    return {"status": "ready"}

