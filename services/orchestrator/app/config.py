from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "development"
    log_level: str = "INFO"

    orch_host: str = "0.0.0.0"
    orch_port: int = 8000

    redis_url: str = "redis://localhost:6379/0"
    supabase_url: str = ""
    supabase_service_role_key: str = ""

    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    deepgram_api_key: str = ""
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""


settings = Settings()
