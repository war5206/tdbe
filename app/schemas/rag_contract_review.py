from pydantic import BaseModel

class RagContractReviewRequest(BaseModel):
    user_prompt: str
    file: str

class RagContractReviewResponse(BaseModel):
    text: str