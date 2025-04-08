import os
from http import HTTPStatus
from dashscope import Application
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.schemas.rag_contract_review import RagContractReviewRequest, RagContractReviewResponse

router = APIRouter()

contract_api_key = "sk-2f760d01853c475f9777a5a8c8938b16"
app_id = "e5fe6043e2be4e3b9c99fb3bc11f5ec2"
pipeline_ids = ["xedc4orobz"]

@router.get("/rag_contract_review", response_model=RagContractReviewResponse)
async def rag_contract_review(user_prompt: str = Query(...)):
  def stream_generator():
    try:
      responses = Application.call(
        api_key=contract_api_key, 
        app_id=app_id,
        prompt=user_prompt,
        rag_options={
          "pipeline_ids": pipeline_ids,
        },
        stream=True
      )
      print('responses >>>', responses)
      for chunk in responses:
        if chunk.status_code != HTTPStatus.OK:      
          error_msg = (
            f"Error: code={chunk.status_code}, "
            f"msg={chunk.message}, request_id={chunk.request_id}\n"
          )
          print('[接口错误] >>>', error_msg)
          # print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
          yield error_msg
          break
        if chunk.output and chunk.output.text:
          response = chunk.output.text
          print('[接口返回] >>>', response)
          yield response
    except Exception as e:
      error_info = f"[系统异常] {str(e)}\n"
      print(error_info)
      yield error_info
    
  return StreamingResponse(stream_generator(), media_type="text/plain")