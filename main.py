from fastapi import FastAPI
from app.api.v1.endpoints import hello_world as hello_world_v1
from app.api.v2.endpoints import hello_world as hello_world_v2

app = FastAPI()

app.include_router(hello_world_v1.router, prefix="/v1", tags=["v1"])
app.include_router(hello_world_v2.router, prefix="/v2", tags=["v2"])