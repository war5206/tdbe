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

@router.get("/rag_contract_review", response_model=RagContractReviewRequest)
def rag_contract_review(user_prompt: str = Query(...)):
    
  response = Application.call(
    api_key=contract_api_key, 
    app_id=app_id,
    prompt=user_prompt,
    rag_options={
        "pipeline_ids": pipeline_ids,
    },
    stream=True
  )

  if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
  else:
    print('%s\n' % (response.output.text))  # 处理只输出文本text
    print('%s\n' % (response.usage)) # {"models": [{"model_id": "qwen-max-latest", "input_tokens": 6164, "output_tokens": 635}]}
            
  return RagContractReviewResponse(
    text=f"{response.output.text}"
  )