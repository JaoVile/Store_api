# tests/usecases/test_product.py

import pytest
from uuid import UUID
from decimal import Decimal
from typing import List

# Importa a CLASSE, não a instância
from store.usecases.product import ProductUsecase
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException

# Cria uma instância do usecase APENAS para este módulo de teste
# Isso funciona porque nosso conftest.py limpa a base de dados após cada teste
usecase = ProductUsecase()

@pytest.mark.asyncio
async def test_usecases_create_should_return_success():
    # Dados de entrada para este teste específico
    product_in = ProductIn(
        name="Teste Usecase",
        quantity=10,
        price=Decimal("1500.00"),
        status=True,
    )
    
    result = await usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Teste Usecase"
    assert result.price == Decimal("1500.00")

@pytest.mark.asyncio
async def test_usecases_get_should_return_success():
    # Cria um produto para poder buscá-lo
    product_in = ProductIn(name="Produto Teste Get", quantity=1, price=Decimal("10.0"))
    created_product = await usecase.create(body=product_in)

    result = await usecase.get(id=created_product.id)

    assert isinstance(result, ProductOut)
    assert result.id == created_product.id

@pytest.mark.asyncio
async def test_usecases_get_should_not_found():
    random_id = UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9")
    
    with pytest.raises(NotFoundException) as err:
        await usecase.get(id=random_id)

    assert err.value.message == f"Product not found with filter: {random_id}"

@pytest.mark.asyncio
async def test_usecases_query_should_return_success():
    # Cria alguns produtos para a consulta
    await usecase.create(body=ProductIn(name="Query Test 1", quantity=1, price=Decimal("1.0")))
    await usecase.create(body=ProductIn(name="Query Test 2", quantity=2, price=Decimal("2.0")))

    result = await usecase.query()

    assert isinstance(result, List)
    assert len(result) >= 2
    assert isinstance(result[0], ProductOut)

@pytest.mark.asyncio
async def test_usecases_update_should_return_success():
    # Cria um produto para poder atualizá-lo
    product_in = ProductIn(name="Produto Para Atualizar", quantity=5, price=Decimal("50.0"))
    created_product = await usecase.create(body=product_in)

    # Dados da atualização
    product_up = ProductUpdate(price=Decimal("75.50"), quantity=4)
    
    result = await usecase.update(id=created_product.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
    assert result.price == Decimal("75.50")
    assert result.quantity == 4

@pytest.mark.asyncio
async def test_usecases_delete_should_return_success():
    # Cria um produto para poder deletá-lo
    product_in = ProductIn(name="Produto Para Deletar", quantity=1, price=Decimal("1.0"))
    created_product = await usecase.create(body=product_in)
    
    result = await usecase.delete(id=created_product.id)

    assert result is True
    
    # Verifica se realmente foi deletado
    with pytest.raises(NotFoundException):
        await usecase.get(id=created_product.id)

@pytest.mark.asyncio
async def test_usecases_delete_should_not_found():
    random_id = UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9")

    with pytest.raises(NotFoundException) as err:
        await usecase.delete(id=random_id)
    
    assert err.value.message == f"Product not found with filter: {random_id}"