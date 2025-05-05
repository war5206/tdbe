from pydantic import BaseModel

class RagContractReviewRequest(BaseModel):
    user_prompt: str
    file: str

class RagContractReviewResponse(BaseModel):
    type: str
    delta: str | dict[str, str] | list[dict[str, str]] | None = None
