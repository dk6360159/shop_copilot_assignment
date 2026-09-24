
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    app_name: str = "ShopFloor Copilot"
    database_hostname:str
    database_port: int
    database_username:str
    database_password:str
    database_name:str
    knowledge_dir: str 
    image_dir: str 
    ollama_base_url: str 
    ollama_model: str
    ollama_timeout_seconds: float 
    llm_latency_ceiling_seconds: float 
    epsilon: float 
    gemini_api_key: str = ""


    model_config={
        'env_file':'.env.example',
        'env_file_encoding':'utf-8',
        'extra':'ignore',
        'case_sensitive':False
    }


    @property
    def database_url(self)->str:
        return (
            f"postgresql+asyncpg://"
            f"{quote_plus(self.database_username)}:"
            f"{quote_plus(self.database_password)}@"
            f"{self.database_hostname}:"
            f"{self.database_port}/"
            f"{self.database_name}"
        )

def get_settings()-> Settings:
    return Settings()





