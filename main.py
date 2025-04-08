from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import hello_world as hello_world_v1
from app.api.v1.endpoints import rag_contract_review as rag_contract_review_v1
app = FastAPI()

origins = [
  "http://localhost:5173",
  "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,
    allow_methods=["*"],    # 允许所有 HTTP 方法
    allow_headers=["*"],    # 允许所有 headers
)

app.include_router(hello_world_v1.router, prefix="/api/v1", tags=["v1"])
app.include_router(rag_contract_review_v1.router, prefix="/api/v1", tags=["v1"])

# if __name__ == "__main__":