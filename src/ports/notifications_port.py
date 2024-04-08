from abc import ABC, abstractmethod
from typing import Optional

from domain.message_schemas import MessageForm


class NotificationsPort(ABC):
    @abstractmethod
    def send_notification(self, notification: MessageForm) -> Optional[str]: ...
