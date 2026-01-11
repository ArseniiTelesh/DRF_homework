import stripe
import requests
from decimal import Decimal

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_currency(amount):
    """Конвертирует через открытый API"""
    try:
        response = requests.get(
            'https://api.exchangerate-api.com/v4/latest/RUB',
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        rate = Decimal(str(data['rates']['USD']))
        return int(amount * rate)
    except Exception:
        # Fallback
        return int(amount * Decimal('0.011'))


def create_stripe_price(amount):
    """Создаёт цену в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )

def create_stripe_session(price):
    """Создаёт сессию (сссылку) на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

