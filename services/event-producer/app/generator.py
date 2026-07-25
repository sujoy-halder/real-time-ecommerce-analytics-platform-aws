from __future__ import annotations

import random
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Callable


EVENT_TYPES = (
    "order_created",
    "cart_updated",
    "product_viewed",
    "payment_authorized",
    "customer_session_started",
    "shipment_status_changed",
)

PRODUCT_CATEGORIES = ("electronics", "home", "fashion", "beauty", "grocery", "sports")
PAYMENT_METHODS = ("credit_card", "debit_card", "paypal", "apple_pay", "gift_card")
SHIPMENT_STATUSES = ("label_created", "in_transit", "out_for_delivery", "delivered", "delayed")
CHANNELS = ("web", "ios", "android", "partner_api")


def _money(value: float) -> str:
    return str(Decimal(value).quantize(Decimal("0.01")))


def _ids(rng: random.Random) -> dict[str, str]:
    customer_num = rng.randint(1, 250_000)
    product_num = rng.randint(1, 25_000)
    return {
        "customer_id": f"cust_{customer_num:06d}",
        "product_id": f"prod_{product_num:06d}",
        "order_id": f"ord_{rng.randint(1, 9_999_999):07d}",
        "session_id": f"sess_{rng.randint(1, 9_999_999):07d}",
    }


def _order_payload(rng: random.Random, ids: dict[str, str]) -> dict[str, Any]:
    item_count = rng.randint(1, 7)
    subtotal = sum(rng.uniform(8, 500) for _ in range(item_count))
    discount = subtotal * rng.choice((0, 0.05, 0.1, 0.15))
    tax = (subtotal - discount) * 0.0825
    return {
        "order_id": ids["order_id"],
        "items": item_count,
        "order_amount": _money(subtotal - discount + tax),
        "discount_amount": _money(discount),
        "tax_amount": _money(tax),
        "currency": "USD",
        "channel": rng.choice(CHANNELS),
    }


def _cart_payload(rng: random.Random, ids: dict[str, str]) -> dict[str, Any]:
    return {
        "session_id": ids["session_id"],
        "cart_id": f"cart_{rng.randint(1, 9_999_999):07d}",
        "product_id": ids["product_id"],
        "quantity": rng.randint(1, 5),
        "cart_value": _money(rng.uniform(5, 1200)),
        "action": rng.choice(("add", "remove", "update_quantity")),
    }


def _product_view_payload(rng: random.Random, ids: dict[str, str]) -> dict[str, Any]:
    return {
        "session_id": ids["session_id"],
        "product_id": ids["product_id"],
        "category": rng.choice(PRODUCT_CATEGORIES),
        "referrer": rng.choice(("search", "recommendation", "email", "ad", "direct")),
        "page_rank": rng.randint(1, 20),
    }


def _payment_payload(rng: random.Random, ids: dict[str, str]) -> dict[str, Any]:
    return {
        "order_id": ids["order_id"],
        "payment_id": f"pay_{rng.randint(1, 9_999_999):07d}",
        "payment_method": rng.choice(PAYMENT_METHODS),
        "payment_amount": _money(rng.uniform(8, 2500)),
        "authorization_status": rng.choices(
            ("authorized", "declined", "requires_review"),
            weights=(90, 7, 3),
            k=1,
        )[0],
    }


def _session_payload(rng: random.Random, ids: dict[str, str]) -> dict[str, Any]:
    return {
        "session_id": ids["session_id"],
        "device_type": rng.choice(("desktop", "mobile", "tablet")),
        "channel": rng.choice(CHANNELS),
        "geo_country": rng.choice(("US", "CA", "GB", "DE", "IN", "AU")),
        "utm_source": rng.choice(("organic", "paid_search", "affiliate", "newsletter", "social")),
    }


def _shipment_payload(rng: random.Random, ids: dict[str, str]) -> dict[str, Any]:
    return {
        "order_id": ids["order_id"],
        "shipment_id": f"ship_{rng.randint(1, 9_999_999):07d}",
        "carrier": rng.choice(("ups", "fedex", "usps", "dhl")),
        "shipment_status": rng.choice(SHIPMENT_STATUSES),
        "estimated_delivery_days": rng.randint(1, 9),
    }


PAYLOAD_BUILDERS: dict[str, Callable[[random.Random, dict[str, str]], dict[str, Any]]] = {
    "order_created": _order_payload,
    "cart_updated": _cart_payload,
    "product_viewed": _product_view_payload,
    "payment_authorized": _payment_payload,
    "customer_session_started": _session_payload,
    "shipment_status_changed": _shipment_payload,
}


def generate_event(
    event_type: str | None = None,
    *,
    rng: random.Random | None = None,
    clock: Callable[[], datetime] | None = None,
) -> dict[str, Any]:
    rng = rng or random.Random()
    clock = clock or (lambda: datetime.now(UTC))
    selected_type = event_type or rng.choice(EVENT_TYPES)

    if selected_type not in PAYLOAD_BUILDERS:
        raise ValueError(f"Unsupported event_type: {selected_type}")

    ids = _ids(rng)
    payload = PAYLOAD_BUILDERS[selected_type](rng, ids)
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": selected_type,
        "event_time": clock().isoformat().replace("+00:00", "Z"),
        "customer_id": ids["customer_id"],
        "source": "event-producer",
        "schema_version": "1.0.0",
        "payload": payload,
    }


def generate_batch(batch_size: int, rng: random.Random | None = None) -> list[dict[str, Any]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    rng = rng or random.Random()
    return [generate_event(rng=rng) for _ in range(batch_size)]

