from pydantic import BaseModel

class RagContractReviewRequest(BaseModel):
    user_prompt: str

class RagContractReviewResponse(BaseModel):
    text: str