from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.hello_world import HelloWorldRequest, HelloWorldResponse
router = APIRouter()

@router.get("/hello_world", response_model=HelloWorldResponse)
def hello_world(name: str = Query(...)):
    return HelloWorldResponse(message=f"Hello v1, {name}!")