from pydantic import BaseModel

class RagContractReviewRequest(BaseModel):
    user_prompt: str

class RagContractReviewResponse(BaseModel):
    text: str
    input_tokens: int
    output_tokens: int