# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.v1.endpoints import api_router

# app = FastAPI()
# origins = [
#   "http://localhost:5173",
#   "http://127.0.0.1:5173"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # 允许访问的源
#     allow_credentials=True,
#     allow_methods=["*"],    # 允许所有 HTTP 方法
#     allow_headers=["*"],    # 允许所有 headers
# )
# app.include_router(api_router, prefix="/api/v1", tags=["v1"])

from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine) # 自动建表