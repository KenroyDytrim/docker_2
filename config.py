from dotenv import load_dotenv
import os

class Settings:
    app_name: str = "New API"
    admin_email: str ="korney1404@gmail.com"
    DATABASE_URL: str
    POSTGRES_DATABASE_URLS: str
    POSTGRES_DATABASE_URLA: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

dotenv_path = os.path.join(os.path.dirname(__file__), 'py.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

settings = Settings()
settings.POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
settings.POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
settings.POSTGRES_USER = os.environ.get('POSTGRES_USER')
settings.POSTGRES_DB = os.environ.get('POSTGRES_DB')
settings.POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
settings.POSTGRES_DATABASE_URLA = f"postgresql+asyncpg:" \
                                f"//{settings.POSTGRES_USER}:" \
                                f"{settings.POSTGRES_PASSWORD}" \
                                f"@{settings.POSTGRES_HOST}:" \
                                f"{settings.POSTGRES_PORT}" \
                                f"/{settings.POSTGRES_DB}"
settings.POSTGRES_DATABASE_URLS = f"postgresql:" \
                                f"//{settings.POSTGRES_USER}:" \
                                f"{settings.POSTGRES_PASSWORD}" \
                                f"@{settings.POSTGRES_HOST}:" \
                                f"{settings.POSTGRES_PORT}" \
                                f"/{settings.POSTGRES_DB}"