# tests/controllers/test_product.py

from typing import List
from fastapi import status
import pytest
from tests.factories import product_data

@pytest.mark.asyncio
async def test_controller_create_should_return_success(client, products_url):
    data_to_send = product_data()
    data_to_send["price"] = float(data_to_send["price"])
    response = await client.post(products_url, json=data_to_send)
    
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["name"] == data_to_send["name"]
    # --- CORREÇÃO: Compara float com float ---
    assert float(content["price"]) == data_to_send["price"]

@pytest.mark.asyncio
async def test_controller_get_should_return_success(client, products_url):
    data_to_send = product_data()
    data_to_send["price"] = float(data_to_send["price"])
    response_create = await client.post(products_url, json=data_to_send)
    product_id = response_create.json()["id"]

    response = await client.get(f"{products_url}{product_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == product_id

@pytest.mark.asyncio
async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}1e4f214e-85f7-461a-89d0-a751a32e3bb9")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_controller_query_should_return_success(client, products_url, products_inserted):
    response = await client.get(products_url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1

@pytest.mark.asyncio
async def test_controller_patch_should_return_success(client, products_url):
    data_to_send = product_data()
    data_to_send["price"] = float(data_to_send["price"])
    response_create = await client.post(products_url, json=data_to_send)
    product_id = response_create.json()["id"]

    new_price = 7500.50
    response = await client.patch(f"{products_url}{product_id}", json={"price": new_price})
    
    assert response.status_code == status.HTTP_200_OK
    # --- CORREÇÃO: Compara float com float ---
    assert float(response.json()["price"]) == new_price

@pytest.mark.asyncio
async def test_controller_delete_should_return_no_content(client, products_url):
    data_to_send = product_data()
    data_to_send["price"] = float(data_to_send["price"])
    response_create = await client.post(products_url, json=data_to_send)
    product_id = response_create.json()["id"]

    response = await client.delete(f"{products_url}{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio
async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(f"{products_url}1e4f214e-85f7-461a-89d0-a751a32e3bb9")
    assert response.status_code == status.HTTP_404_NOT_FOUND