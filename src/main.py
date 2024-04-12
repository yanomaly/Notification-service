from adapters.mongo_adapter import MongoAdapter
from adapters.rabbit_adapter import RabbitAdapter
from adapters.ses_adapter import SESAdapter
from dependencies import RabbitMQClient, mongo_client, ses_client
from use_cases.notification_case import NotificationCase

client = RabbitMQClient()
rabbit = RabbitAdapter(client)

ses = SESAdapter(ses_client)

mongo = MongoAdapter(mongo_client)

notifications = NotificationCase(rabbit, ses, mongo)
notifications.run()
