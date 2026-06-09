from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://arthsaathi:arthsaathi@localhost:5432/arthsaathi"
    app_env: str = "development"

    # LLM providers (set at least one for dynamic Q&A)
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    llm_model_openai: str = "gpt-4o-mini"
    llm_model_anthropic: str = "claude-3-5-sonnet-20241022"
    llm_model_google: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
