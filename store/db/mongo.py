# store/db/mongo.py
from __future__ import annotations
from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings

# --- INÍCIO DA CORREÇÃO ---
# Importa a ferramenta de representação de UUID da biblioteca bson
from bson import UuidRepresentation
# --- FIM DA CORREÇÃO ---

class MongoClient:
    """Uma classe wrapper para o cliente do MongoDB."""
    def __init__(self) -> None:
        # --- INÍCIO DA CORREÇÃO ---
        # Passamos o argumento 'uuidRepresentation="standard"' ao criar o cliente.
        # Isso diz ao pymongo para usar o formato padrão para salvar e ler UUIDs.
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL, uuidRepresentation="standard"
        )
        # --- FIM DA CORREÇÃO ---

    def get(self) -> AsyncIOMotorClient:
        """Retorna a instância do cliente motor para interagir com o banco de dados."""
        return self.client

# Padrão de "lazy loading" para evitar inicialização prematura.
_db_client_instance: MongoClient | None = None

def get_db_client() -> MongoClient:
    """
    Retorna a instância singleton do MongoClient, criando-a apenas na primeira chamada.
    """
    global _db_client_instance
    if _db_client_instance is None:
        _db_client_instance = MongoClient()
    return _db_client_instance