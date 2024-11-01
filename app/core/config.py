from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    amocrm_client_id: str
    amocrm_client_secret: str
    amocrm_redirect_uri: str
    amocrm_subdomain: str

    database_url: str

    db_name: str
    db_user: str
    db_password: str

    class Config:
        env_file = '.env'

settings = Settings()
