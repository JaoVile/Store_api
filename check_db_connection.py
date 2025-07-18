# check_db_connection.py

import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# A mesma URL de conexão do seu arquivo .env
DATABASE_URL = "mongodb://root:root@localhost:27017/store_db?authSource=admin"

print("--- INICIANDO TESTE DE CONEXÃO DIRETA ---")
print(f"Tentando conectar com a URL: {DATABASE_URL}")

try:
    # 1. Tenta criar um cliente de conexão
    client = MongoClient(DATABASE_URL)

    # 2. Pega o banco de dados
    db = client.get_database()

    # 3. Executa um comando que FORÇA a conexão e a autenticação
    print("Conexão estabelecida. Tentando listar coleções (requer autenticação)...")
    collection_names = db.list_collection_names()
    
    print("\n✅✅✅ SUCESSO! A AUTENTICAÇÃO FUNCIONOU! ✅✅✅")
    print("Coleções encontradas:", collection_names)
    print("O problema está na configuração do Pytest/FastAPI.")

except OperationFailure as e:
    print("\n❌❌❌ FALHA! O ERRO DE AUTENTICAÇÃO ACONTECEU. ❌❌❌")
    print(f"Detalhes do erro: {e.details}")
    print("\nCausa provável: O contêiner Docker não está com o usuário 'root'/'root' configurado corretamente.")
    print("Solução: Execute 'docker-compose down -v' para apagar TUDO e tente de novo.")

except Exception as e:
    print(f"\n❌❌❌ FALHA! Ocorreu um erro inesperado de conexão. ❌❌❌")
    print(f"Tipo de erro: {type(e).__name__}")
    print(f"Detalhes: {e}")
    print("\nCausa provável: O contêiner Docker não está rodando. Verifique com 'docker ps'.")

finally:
    print("\n--- TESTE DE CONEXÃO FINALIZADO ---")