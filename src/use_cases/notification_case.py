from pika.exceptions import AMQPError

from dependencies import base_logger, settings
from ports.messaging_port import MessagingPort


class NotificationCase:
    def __init__(self, message_broker: MessagingPort):
        self.message_broker = message_broker

    def run(self):
        self.message_broker.start_consuming(self.callback)

    def callback(self, ch, method, properties, body):
        try:
            self.email_proceeding()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except AMQPError as e:
            base_logger.error(f"AMQP error during processing message: {e}")
            self.retry_process(ch, method, properties, body)
        except Exception as e:
            base_logger.error(f"Unknown error during processing message: {e}")
            raise e

    def retry_process(self, ch, method, properties, body):
        if self.can_retry(properties):
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        else:
            base_logger.info("Send message to death-letter after 5 retries")
            ch.basic_publish(
                exchange=settings.RABBITMQ_EXCHANGE,
                routing_key=settings.DEATH_ROUTING_KEY,
                properties=properties,
                body=body,
            )

    @staticmethod
    def can_retry(properties):
        deaths = (properties.headers or {}).get("x-death")
        if not deaths:
            return True
        if deaths[0]["count"] >= settings.MAX_RETRIES:
            return False
        return True

    async def email_proceeding(self): ...
