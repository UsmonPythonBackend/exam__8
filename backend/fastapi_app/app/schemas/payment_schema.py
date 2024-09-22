from typing import Optional
from pydantic import BaseModel


class PaymentCreateSchema(BaseModel):
    order_id: Optional[str]
    amount: Optional[str]
    payment_status: Optional[str]
    payment_type: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "amount": "str",
            "payment_status": "pn",
            "payment_type": "str",
            "order_id": "str"
        }

