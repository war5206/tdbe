from fastapi import APIRouter
from .ai_chat.rag_contract_review import router as rag_contract_review_router
from .test.hello_world import router as hello_world_router
from .crud.agent import router as agent_router
from .crud.file import router as file_router
from .crud.user import router as user_router
from .crud.session import router as session_router
from .crud.message import router as message_router
from .asr.single_asr import router as single_asr_router

api_router = APIRouter()
api_router.include_router(rag_contract_review_router)
api_router.include_router(hello_world_router)
api_router.include_router(agent_router)
api_router.include_router(file_router)
api_router.include_router(user_router)
api_router.include_router(session_router)
api_router.include_router(message_router)
api_router.include_router(single_asr_router)