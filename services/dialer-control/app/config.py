from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    log_level: str = "INFO"
    vicidial_api_url: str = ""
    vicidial_user: str = ""
    vicidial_pass: str = ""
    asterisk_ari_url: str = ""
    asterisk_ari_user: str = ""
    asterisk_ari_pass: str = ""

    orchestrator_url: str = "http://orchestrator:8000"
    media_gateway_url: str = "http://media-gateway:8010"


settings = Settings()
