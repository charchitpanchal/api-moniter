from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI API Monitoring Platform"
    environment: str = "development"
    debug: bool = True
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    default_max_retries: int = 3
    default_retry_delay_seconds: int = 2
    failure_threshold: int = 3
    redis_url: str = "redis://localhost:6379/0"
    ai_provider: str = "openai"
    ai_api_key: str = ""
    ai_model: str = "gpt-4o-mini"
    ai_enabled: bool = True
    notification_provider: str = "console"
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()