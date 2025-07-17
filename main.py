from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import api_router

app = FastAPI()
# origins = [
#   "http://localhost:8081",
#   "http://127.0.0.1:8081"
# ]
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # 允许访问的源
    # allow_credentials=True,
    allow_origins=["*"],  # 或指定你的 Expo dev server 地址
    allow_credentials=True,
    allow_methods=["*"],    # 允许所有 HTTP 方法
    allow_headers=["*"],    # 允许所有 headers
)
app.include_router(api_router, prefix="/api/v1", tags=["v1"])