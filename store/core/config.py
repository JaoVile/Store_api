# store/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Força o carregamento do arquivo .env. 
# Isso garante que as variáveis de ambiente estarão disponíveis
# antes que o Pydantic tente validar as configurações.
load_dotenv() 

class Settings(BaseSettings):
    """
    Classe de configurações da aplicação, carregada a partir de variáveis de ambiente.
    """
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    # Variável obrigatória, será lida do ambiente (do arquivo .env)
    DATABASE_URL: str

    # Configuração do Pydantic para ler do arquivo .env e ignorar variáveis extras
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Cria uma instância única das configurações para ser usada em toda a aplicação
settings = Settings()