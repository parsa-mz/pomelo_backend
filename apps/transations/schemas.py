from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel as BaseSchema


class EventSchema(BaseSchema):
    txnId: str
    eventType: str
    amount: Optional[float] = None  # because of PAYMENT_POSTED
    eventTime: float


class InputData(BaseSchema):
    # creditLimit: float
    events: List[EventSchema]


