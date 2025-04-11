from pydantic import BaseModel

class AliyunModelMsg(BaseModel):
  role: str
  content: str
