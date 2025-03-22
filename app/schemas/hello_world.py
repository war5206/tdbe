from pydantic import BaseModel

class HelloWorldRequest(BaseModel):
    name: str

class HelloWorldResponse(BaseModel):
    message: str