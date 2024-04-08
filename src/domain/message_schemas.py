import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

email_regexp = r"^[\w.-]+@([\w-]+\.)+[\w-]{2,4}$"


class MessageForm(BaseModel):
    id: UUID
    user_id: UUID
    subject: str
    body: str
    email: str
    published_at: datetime
    sent_at: datetime

    @field_validator("email")
    @classmethod
    def email_val(cls, value: str):
        email_pattern = re.compile(email_regexp)
        if not value or not re.match(email_pattern, value):
            raise ValueError("This email format is not supported")
        return value
