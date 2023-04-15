from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    app_description: str = 'Фонд собирает пожертвования связанные с поддержкой кошачьей популяции'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
