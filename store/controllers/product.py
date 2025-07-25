# store/controllers/product.py

from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase  # MUDANÇA AQUI: Importa a CLASSE
from store.core.exceptions import NotFoundException

router = APIRouter(tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID, usecase: ProductUsecase = Depends()) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID, body: ProductUpdate = Body(...), usecase: ProductUsecase = Depends()
) -> ProductUpdateOut:
    return await usecase.update(id=id, body=body)

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID, usecase: ProductUsecase = Depends()) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)