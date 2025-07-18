# tests/usecases/test_product.py

import pytest
from uuid import UUID
from decimal import Decimal
from typing import List

from store.usecases.product import ProductUsecase
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException

# --- INÍCIO DA CORREÇÃO ---
# Remove a instanciação global do usecase daqui
# Em vez disso, criamos uma fixture que será injetada em cada teste
@pytest.fixture
def usecase() -> ProductUsecase:
    return ProductUsecase()
# --- FIM DA CORREÇÃO ---


@pytest.mark.asyncio
async def test_usecases_create_should_return_success(usecase: ProductUsecase):
    product_in = ProductIn(
        name="Teste Usecase",
        quantity=10,
        price=Decimal("1500.00"),
        status=True,
    )
    
    result = await usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Teste Usecase"

@pytest.mark.asyncio
async def test_usecases_get_should_return_success(usecase: ProductUsecase):
    # CORREÇÃO: Adicionado `status=True`
    product_in = ProductIn(name="Produto Teste Get", quantity=1, price=Decimal("10.0"), status=True)
    created_product = await usecase.create(body=product_in)

    result = await usecase.get(id=created_product.id)

    assert isinstance(result, ProductOut)
    assert result.id == created_product.id

@pytest.mark.asyncio
async def test_usecases_get_should_not_found(usecase: ProductUsecase):
    random_id = UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9")
    
    with pytest.raises(NotFoundException) as err:
        await usecase.get(id=random_id)

    assert err.value.message == f"Product not found with filter: {random_id}"

@pytest.mark.asyncio
async def test_usecases_query_should_return_success(usecase: ProductUsecase):
    # CORREÇÃO: Adicionado `status=True`
    await usecase.create(body=ProductIn(name="Query Test 1", quantity=1, price=Decimal("1.0"), status=True))
    await usecase.create(body=ProductIn(name="Query Test 2", quantity=2, price=Decimal("2.0"), status=True))

    result = await usecase.query()

    assert isinstance(result, List)
    assert len(result) >= 2
    assert isinstance(result[0], ProductOut)

@pytest.mark.asyncio
async def test_usecases_update_should_return_success(usecase: ProductUsecase):
    # CORREÇÃO: Adicionado `status=True`
    product_in = ProductIn(name="Produto Para Atualizar", quantity=5, price=Decimal("50.0"), status=True)
    created_product = await usecase.create(body=product_in)

    product_up = ProductUpdate(price=Decimal("75.50"), quantity=4)
    
    result = await usecase.update(id=created_product.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
    assert result.price == Decimal("75.50")

@pytest.mark.asyncio
async def test_usecases_delete_should_return_success(usecase: ProductUsecase):
    # CORREÇÃO: Adicionado `status=True`
    product_in = ProductIn(name="Produto Para Deletar", quantity=1, price=Decimal("1.0"), status=True)
    created_product = await usecase.create(body=product_in)
    
    result = await usecase.delete(id=created_product.id)

    assert result is True
    
    with pytest.raises(NotFoundException):
        await usecase.get(id=created_product.id)

@pytest.mark.asyncio
async def test_usecases_delete_should_not_found(usecase: ProductUsecase):
    random_id = UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9")

    with pytest.raises(NotFoundException) as err:
        await usecase.delete(id=random_id)
    
    assert err.value.message == f"Product not found with filter: {random_id}"