from decimal import Decimal


def convert_to_brl(price_in_usd):
    """
    Convierte un precio en USD a BRL utilizando una tasa de cambio fija.
    :param price_in_usd: Precio en dólares (float).
    :return: Precio en reales (int, en centavos para Stripe).
    """
    exchange_rate = Decimal("5.00")  # Ejemplo: tasa de cambio actual
    return int(price_in_usd * exchange_rate * 100)  # Stripe requiere centavos
