import os, tempfile
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from dashscope import Application
from app.schemas.rag_contract_review import RagContractReviewResponse
from app.schemas.aliyun import AliyunModelMsg
from app.utils import extract_text_from_docx, extract_text_from_pdf
from app.services import reasoning_stream_generator

router = APIRouter(prefix="/contract", tags=["合同评审"])

contract_api_key = "sk-2f760d01853c475f9777a5a8c8938b16"
app_id = "e5fe6043e2be4e3b9c99fb3bc11f5ec2"
pipeline_ids = ["xedc4orobz"]

@router.post("/review", response_model=RagContractReviewResponse)
async def rag_contract_review(
    file: UploadFile = File(..., description="DOCX或PDF文件"),
    user_prompt: str = Form(..., description="用户提示词"),
):
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
    
    messages: list[AliyunModelMsg] = [
      AliyunModelMsg(role="user", content=combined_prompt)
    ]

    return StreamingResponse(
        reasoning_stream_generator(
          contract_api_key=contract_api_key, 
          app_id=app_id,
          pipeline_ids=pipeline_ids,
          messages=messages
        ), 
        media_type="text/plain"
    )