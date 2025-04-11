from fastapi import APIRouter
from .rag_contract_review import router as rag_contract_review_router
from .hello_world import router as hello_world_router

api_router = APIRouter()
api_router.include_router(rag_contract_review_router)
api_router.include_router(hello_world_router)