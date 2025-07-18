# tests/conftest.py

import asyncio
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from store.db.mongo import db_client
from store.main import app
from store.schemas.product import ProductIn
from tests.factories import products_data

# --- Fixtures de Configuração do Ambiente de Teste ---

@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para toda a sessão de testes, mais eficiente."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Cria um cliente HTTP único para toda a sessão de testes."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def clear_database() -> AsyncGenerator[None, None]:
    """Limpa o banco de dados após cada teste para garantir isolamento."""
    yield
    collections = await db_client.get_database().list_collection_names()
    for collection_name in collections:
        if collection_name.startswith("system"):
            continue
        await db_client.get_database()[collection_name].delete_many({})

# --- Fixtures de Dados de Teste ---

@pytest.fixture
def products_url() -> str:
    """URL base para o endpoint de produtos."""
    return "/products/"

@pytest.fixture
def products_in() -> list[ProductIn]:
    """Lista de produtos para serem criados."""
    return [ProductIn(**product) for product in products_data()]

@pytest.fixture
async def products_inserted(client: AsyncClient, products_url: str, products_in: list[ProductIn]):
    """
    Insere múltiplos produtos na base de dados via API e retorna os dados inseridos.
    É uma fixture mais útil que a 'product_inserted' individual.
    """
    inserted_products = []
    for product_in in products_in:
        response = await client.post(products_url, content=product_in.model_dump_json())
        inserted_products.append(response.json())
    return inserted_products