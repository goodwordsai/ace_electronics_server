from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI(title="Ace Electronics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS = [
    {
        "id": "prod_001",
        "name": "Sony WH-1000XM5 Headphones",
        "price": 349.99,
        "category": "Audio",
        "in_stock": True,
    },
    {
        "id": "prod_002",
        "name": "Samsung 65\" OLED Smart TV",
        "price": 1799.99,
        "category": "TVs",
        "in_stock": True,
    },
    {
        "id": "prod_003",
        "name": "Apple iPad Pro 12.9\"",
        "price": 1099.00,
        "category": "Tablets",
        "in_stock": True,
    },
    {
        "id": "prod_004",
        "name": "Logitech MX Master 3S Mouse",
        "price": 99.99,
        "category": "Accessories",
        "in_stock": True,
    },
    {
        "id": "prod_005",
        "name": "Aukey 737 Power Bank",
        "price": 149.99,
        "category": "Accessories",
        "in_stock": False,
    },
]


class CartItem(BaseModel):
    product_id: str
    quantity: int


class CheckoutRequest(BaseModel):
    items: list[CartItem]
    customer_email: str


@app.get("/ace/api/products")
def get_products():
    return {"products": PRODUCTS}


@app.post("/ace/api/checkout")
def checkout(request: CheckoutRequest):
    total = 0.0
    order_items = []

    for item in request.items:
        product = next((p for p in PRODUCTS if p["id"] == item.product_id), None)
        if product:
            subtotal = product["price"] * item.quantity
            total += subtotal
            order_items.append({
                "product": product["name"],
                "quantity": item.quantity,
                "unit_price": product["price"],
                "subtotal": subtotal,
            })

    return {
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "status": "confirmed",
        "items": order_items,
        "total": round(total, 2),
        "customer_email": request.customer_email,
        "created_at": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
