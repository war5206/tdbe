from fastapi import FastAPI
from app.api.v1.endpoints import hello_world as hello_world_v1
from app.api.v1.endpoints import rag_contract_review as rag_contract_review_v1
app = FastAPI()

app.include_router(hello_world_v1.router, prefix="/api/v1", tags=["v1"])
app.include_router(rag_contract_review_v1.router, prefix="/api/v1", tags=["v1"])