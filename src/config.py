import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(pathlib.Path(__file__).parent.resolve().parent, ".env")


class Settings(BaseSettings):

    RABBITMQ_DEFAULT_USER: str = ""
    RABBITMQ_DEFAULT_PASS: str = ""
    RABBIT_HOST: str = ""
    RABBIT_PORT: int = 1
    ROUTING_KEY: str = ""
    RABBITMQ_EXCHANGE: str = ""
    DEATH_ROUTING_KEY: str = ""
    MAX_RETRIES: int = 1

    SERVICES: str = ""
    HOSTNAME: str = ""
    LOCALSTACK_PORT: int = 1
    HOSTNAME_EXTERNAL: str = ""
    DEFAULT_REGION: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    SOURCE: str = ""

    DB_NAME: str = ""
    COLLECTION_NAME: str = ""

    ME_CONFIG_MONGODB_URL: str = ""
    ME_CONFIG_MONGODB_SERVER: str = ""
    ME_CONFIG_MONGODB_PORT: int = 1
    ME_CONFIG_MONGODB_ADMINUSERNAME: str = ""
    ME_CONFIG_MONGODB_ADMINPASSWORD: str = ""
    ME_CONFIG_BASICAUTH_USERNAME: str = ""
    ME_CONFIG_BASICAUTH_PASSWORD: str = ""

    MONGODB_ROOT_USER: str = ""
    MONGODB_ROOT_PASSWORD: str = ""
    MONGODB_INITIAL_PRIMARY_ROOT_USER: str = ""
    MONGODB_INITIAL_PRIMARY_ROOT_PASSWORD: str = ""
    MONGODB_REPLICA_SET_KEY: str = ""

    model_config = SettingsConfigDict(env_file=DOTENV)
