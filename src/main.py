from adapters.rabbit_adapter import RabbitAdapter
from adapters.ses_adapter import SESAdapter
from dependencies import RabbitMQClient, ses_client
from use_cases.notification_case import NotificationCase

client = RabbitMQClient()
rabbit = RabbitAdapter(client)

ses = SESAdapter(ses_client)

notifications = NotificationCase(rabbit, ses)

notifications.run()
