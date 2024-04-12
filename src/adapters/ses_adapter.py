from typing import Optional

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from dependencies import base_logger, settings
from domain.message_schemas import MessageForm
from ports.notifications_port import NotificationsPort


class SESAdapter(NotificationsPort):

    def __init__(self, ses_client: BaseClient):
        self.client = ses_client

    def send_notification(self, notification: MessageForm) -> Optional[str]:
        try:
            response = self.client.send_email(
                Source=settings.SOURCE,
                Destination={
                    "ToAddresses": [
                        notification.email,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": "UTF-8",
                            "Data": notification.body,
                        },
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": "Reset password",
                    },
                },
            )
            return response
        except (
            self.client.exceptions.MessageRejected,
            self.client.exceptions.MailFromDomainNotVerifiedException,
            self.client.exceptions.AccountSendingPausedException,
        ) as e:
            base_logger.error(f"SES error during sending message: {e}")
            raise ClientError(e.response, "send_notification")
        except self.client.exceptions as e:
            base_logger.error(f"Unknown SES error during sending message: {e}")
            raise e
        except Exception as e:
            base_logger.error(f"Unknown error during consuming: {e}")
            raise e
