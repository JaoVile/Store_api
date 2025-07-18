# store/main.py
from fastapi import FastAPI
from store.core.config import settings
from store.routers import api_router
from decimal import Decimal

class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        # Ensina o FastAPI a converter o tipo Decimal para float ao criar respostas JSON
        super().__init__(
            *args,
            **kwargs,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
            json_encoders={
                Decimal: float
            }
        )

app = App()
app.include_router(api_router)