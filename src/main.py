from adapters.rabbit_adapter import RabbitAdapter
from dependencies import RabbitMQClient
from use_cases.notification_case import NotificationCase

client = RabbitMQClient()
rabbit = RabbitAdapter(client)

notifications = NotificationCase(rabbit)

notifications.run()
