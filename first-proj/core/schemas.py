from pydantic import BaseModel , field_validator , Field

class BasePersonSchema(BaseModel):
    name:str = Field(... , description="Enter person name")
    
    @field_validator("name")
    def validate_name(cls , value):
        if len(value) > 32:
            raise ValueError("Name must not exceed 32 character")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic character")
        return value
            

class PersonCreationSchema(BasePersonSchema):
    pass
    
class PersonCreationResponseSchema(BasePersonSchema):
    id:int = Field(... , description="Enter person id")