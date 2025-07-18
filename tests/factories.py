# tests/factories.py

from decimal import Decimal

def product_data():
    """
    Gera um dicionário com dados de um único produto,
    garantindo que o preço seja do tipo Decimal.
    """
    return {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": Decimal("8500.0"),  # Corrigido: Usa Decimal e ponto como separador
        "status": True,
    }

def products_data():
    """
    Gera uma lista de dicionários com dados de múltiplos produtos,
    garantindo que os preços sejam do tipo Decimal.
    """
    return [
        {"name": "Iphone 11 Pro Max", "quantity": 20, "price": Decimal("4500.0"), "status": True},
        {"name": "Iphone 12 Pro Max", "quantity": 15, "price": Decimal("5500.0"), "status": True},
        {"name": "Iphone 13 Pro Max", "quantity": 5, "price": Decimal("6500.0"), "status": True},
        {
            "name": "Iphone 15 Pro Max",
            "quantity": 3,
            "price": Decimal("10500.0"),
            "status": False,
        },
    ]