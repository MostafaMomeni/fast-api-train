from pydantic import BaseModel

class BasePersonSchema(BaseModel):
    name:str

class PersonCreationSchema(BasePersonSchema):
    pass
    
class PersonCreationResponseSchema(BasePersonSchema):
    id:int