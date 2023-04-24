from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://${POSTGRES_USER}:${pass}@localhost:6552/${POSTGRES_DB}'
    secret_key_jwt: str = 'secret'
    algorithm: str = 'HS256'
    mail_username: str = 'example@meta.ua'
    mail_password: str = 'password'
    mail_from: str = 'example@meta.ua'
    mail_port: int = '439'
    mail_server: str = 'smtp.meta'
    redis_host: str = 'localhost'
    redis_port: int = 4339
    cloudinary_name: str = 'temp'
    cloudinary_api_key: int = 4523469
    cloudinary_api_secret: str = 'secret api'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()