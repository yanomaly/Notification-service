import logging.config

import boto3
from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials
from pika.exceptions import AMQPError
from pymongo import MongoClient

from config import Settings

logging.config.fileConfig("../logger.ini")
base_logger = logging.getLogger("base")

settings = Settings()

aws_session = boto3.Session()

ses_client = aws_session.client(
    service_name="ses",
    region_name=settings.DEFAULT_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=f"http://{settings.HOSTNAME_EXTERNAL}:{settings.LOCALSTACK_PORT}",
)

mongo_client = MongoClient(settings.ME_CONFIG_MONGODB_URL)


class RabbitMQClient:
    def __init__(self):
        self.connection = self.create_connection()

    @staticmethod
    def create_connection() -> BlockingConnection:
        credentials = PlainCredentials(
            settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS
        )
        parameters = ConnectionParameters(
            host=settings.RABBIT_HOST,
            port=settings.RABBIT_PORT,
            credentials=credentials,
        )
        try:
            connection = BlockingConnection(parameters)
        except AMQPError as e:
            base_logger.error(f"AMQP error during connection to rabbitMQ: {e}")
            raise e
        except Exception as e:
            base_logger.error(f"Unknown error during connection to rabbitMQ: {e}")
            raise e
        return connection

    def get_connection(self) -> BlockingConnection:
        if self.connection is None or self.connection.is_closed:
            self.connection = self.create_connection()
        return self.connection
