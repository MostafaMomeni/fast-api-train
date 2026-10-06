from pydantic import BaseModel, field_validator, Field


class BaseAmountSchema(BaseModel):
    amount: float = Field(..., gt=0)
    description: str = Field(default="")

class AmountCreationSchema(BaseAmountSchema):
    pass

class AmountCreationResponseSchema(BaseAmountSchema):
    id: int = Field(...)
    
