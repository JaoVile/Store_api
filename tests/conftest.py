# tests/conftest.py

import asyncio
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from store.db.mongo import get_db_client
from store.main import app
from store.schemas.product import ProductIn
from tests.factories import products_data

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def clear_database() -> None:
    yield
    motor_client = get_db_client().get()
    database = motor_client.get_database()
    collections = await database.list_collection_names()
    for collection_name in collections:
        if collection_name.startswith("system"):
            continue
        await database[collection_name].delete_many({})

@pytest.fixture
def products_url() -> str:
    return "/products/"

@pytest.fixture
def products_in() -> list[ProductIn]:
    return [ProductIn(**product) for product in products_data()]

@pytest.fixture
async def products_inserted(client: AsyncClient, products_url: str, products_in: list[ProductIn]):
    inserted_products = []
    for product_in in products_in:
        # --- INÍCIO DA CORREÇÃO ---
        # Converte o Decimal para float aqui também para resolver o TypeError na fixture
        data_to_send = product_in.model_dump()
        data_to_send["price"] = float(data_to_send["price"])
        
        response = await client.post(products_url, json=data_to_send)
        # --- FIM DA CORREÇÃO ---
        
        response.raise_for_status()
        inserted_products.append(response.json())
    return inserted_products