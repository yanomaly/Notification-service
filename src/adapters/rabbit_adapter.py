from pika.exceptions import AMQPError

from dependencies import RabbitMQClient, base_logger
from ports.messaging_port import MessagingPort


class RabbitAdapter(MessagingPort):

    def __init__(self, rabbit_client: RabbitMQClient):
        self.rabbit_client = rabbit_client

    def start_consuming(self, on_message_callback) -> None:
        try:
            with self.rabbit_client.get_connection().channel() as channel:
                channel.basic_consume(
                    queue="reset-password-stream",
                    on_message_callback=on_message_callback,
                )
                channel.start_consuming()
        except AMQPError as e:
            base_logger.error(f"AMQP error during consuming: {e}")
            raise e
        except Exception as e:
            base_logger.error(f"Unknown error during consuming: {e}")
            raise e
