from fastapi import APIRouter, Depends, Form, HTTPException
from app.schemas.hello_world import HelloWorldRequest, HelloWorldResponse
router = APIRouter()

@router.post("/hello_world", response_model=HelloWorldResponse)
# def hello_world(request: HelloWorldRequest): # 期待接收JSON格式
def hello_world(name: str = Form(...)): # 期待接收Form表单格式
    # return HelloWorldResponse(message=f"Hello v2, {request.name}!")
    return HelloWorldResponse(message=f"Hello v2, {name}!")