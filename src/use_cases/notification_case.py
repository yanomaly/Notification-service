import json
from datetime import datetime

from botocore.exceptions import ClientError
from pika.exceptions import AMQPError

from dependencies import base_logger, settings
from domain.message_schemas import MessageForm
from ports.db_port import DBPort
from ports.messaging_port import MessagingPort
from ports.notifications_port import NotificationsPort


class NotificationCase:
    def __init__(
        self,
        message_broker: MessagingPort,
        notifications_sender: NotificationsPort,
        db: DBPort,
    ):
        self.message_broker = message_broker
        self.notifications_sender = notifications_sender
        self.db = db

    def run(self) -> None:
        self.message_broker.start_consuming(self.callback)

    def callback(self, ch, method, properties, body) -> None:
        db_session = None
        try:
            db_session = self.db.get_session()
            self.email_proceeding(db_session, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except ClientError:
            base_logger.error(
                "SES error during processing message, trying to process again"
            )
            self.retry_process(ch, method, properties, body, db_session)
        except AMQPError as e:
            base_logger.error(f"AMQP error during processing message: {e}")
        except Exception as e:
            base_logger.error(f"Unknown error during processing message: {e}")

    def retry_process(self, ch, method, properties, body, db_session) -> None:
        try:
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
                base_logger.info("Rollback message saving after 5 retries")
                self.db.rollback_session(db_session)
        except AMQPError as e:
            base_logger.error(f"AMQP error during message retry attempt: {e}")
        except Exception as e:
            base_logger.error(f"Unknown error during message retry attempt: {e}")

    @staticmethod
    def can_retry(properties) -> bool:
        deaths = (properties.headers or {}).get("x-death")
        if not deaths:
            return True
        if deaths[0]["count"] >= settings.MAX_RETRIES:
            return False
        return True

    def email_proceeding(self, db_session, body: str) -> None:
        message = self.parse_message(body)
        self.db.insert(db_session, settings.DB_NAME, settings.COLLECTION_NAME, message)
        self.notifications_sender.send_notification(message)
        self.db.commit_session(db_session)

    @staticmethod
    def parse_message(body: str) -> MessageForm:
        data = json.loads(body)
        if not data:
            raise ValueError("Wrong message body")
        message = MessageForm(
            subject="Password reset",
            body=data["link"],
            email=data["email"],
            published_at=data["publishing_time"],
            sent_at=datetime.utcnow(),
        )
        return message
