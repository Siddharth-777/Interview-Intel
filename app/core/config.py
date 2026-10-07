from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/interview_intel"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3.2"
    EMBED_MODEL: str = "nomic-embed-text"
    EMBED_DIM: int = 768


settings = Settings()
