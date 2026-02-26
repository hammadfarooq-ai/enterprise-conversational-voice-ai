from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    log_level: str = "INFO"
    media_host: str = "0.0.0.0"
    media_http_port: int = 8010
    media_rtp_host: str = "0.0.0.0"
    media_rtp_port: int = 5004
    media_orch_ws_url: str = "ws://localhost:8000/ws/media"


settings = Settings()
