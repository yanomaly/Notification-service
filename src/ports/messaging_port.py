from abc import ABC, abstractmethod


class MessagingPort(ABC):
    @abstractmethod
    def start_consuming(self, on_message_callback) -> None: ...
