import os
import tempfile
from http import HTTPStatus
from dashscope import Application
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from app.schemas.rag_contract_review import RagContractReviewRequest, RagContractReviewResponse
from app.libs.file.index import extract_text_from_docx, extract_text_from_pdf
router = APIRouter()

contract_api_key = "sk-2f760d01853c475f9777a5a8c8938b16"
app_id = "e5fe6043e2be4e3b9c99fb3bc11f5ec2"
pipeline_ids = ["xedc4orobz"]

@router.post("/rag_contract_review_stream", response_model=RagContractReviewResponse)
async def rag_contract_review(
  file: UploadFile = File(..., description="DOCX或PDF文件"),
  user_prompt: str = Form(..., description="用户提示词"),
):
  print("用户提示词: ", user_prompt)
  print("文件: ", file)
  # 检查文件类型
  if file.content_type not in [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword"
  ]:
    raise HTTPException(status_code=400, detail="只支持PDF或Word文件")
  
  # 创建临时文件保存上传内容
  with tempfile.NamedTemporaryFile(delete=False) as tmp:
    tmp.write(await file.read())
    tmp_path = tmp.name

  # 提取文本
  try:
    if file.filename.endswith(".pdf"):
      text = extract_text_from_pdf(tmp_path)
    elif file.filename.endswith(".docx"):
      text = extract_text_from_docx(tmp_path)
    elif file.filename.endswith(".doc"):
      raise HTTPException(status_code=400, detail="暂不支持旧版.doc格式")
    else:
      raise HTTPException(status_code=400, detail="无法识别的文件类型")
  finally:
    os.remove(tmp_path)

  # 拼接 user_prompt 和文本
  combined_prompt = f"{text}\n{user_prompt}"
  print("combined_prompt: ", combined_prompt)


  # def stream_generator():
  #   try:
  #     responses = Application.call(
  #       api_key=contract_api_key, 
  #       app_id=app_id,
  #       prompt=user_prompt,
  #       rag_options={
  #         "pipeline_ids": pipeline_ids,
  #       },
  #       stream=True
  #     )
      
  #     last_response = "" #用于记录上一次完整输出
  #     for chunk in responses:
  #       if chunk.status_code != HTTPStatus.OK:      
  #         error_msg = (
  #           f"Error: code={chunk.status_code}, "
  #           f"msg={chunk.message}, request_id={chunk.request_id}\n"
  #         )
  #         print('[接口错误] >>>', error_msg)
  #         # print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
  #         yield error_msg
  #         break
  #       if chunk.output and chunk.output.text:
  #         current = chunk.output.text
  #         print('[接口返回] >>>', current)

  #         # 计算新增部分
  #         if current.startswith(last_response):
  #           delta = current[len(last_response):]
  #         else:
  #           delta = current  # fallback，某些异常情况
  #         last_response = current  # 更新历史
  #         yield delta
        
  #   except Exception as e:
  #     error_info = f"[系统异常] {str(e)}\n"
  #     print(error_info)
  #     yield error_info
    
  # return StreamingResponse(stream_generator(), media_type="text/plain")
  return '{"text": "测试成功"}'