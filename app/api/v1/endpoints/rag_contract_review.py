import os, tempfile, json
from datetime import datetime
from dashscope import Application
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.schemas import AliyunModelMsg, RagContractReviewResponse, SessionCreate, ChatMessageCreate, FileCreate
from app.services import session as session_service, message as message_service, file as file_service
from app.utils import extract_text_from_docx, extract_text_from_pdf
from app.services import reasoning_stream_generator

router = APIRouter(prefix="/contract", tags=["合同评审"])

contract_api_key = "sk-a130929633e3400ebe3581645dfc3c88"
app_id = "8468ae9323004e2298343b5f349ed4c1"
pipeline_ids = ["s3p1wlxsf2"]

@router.post("/review", response_model=RagContractReviewResponse)
async def rag_contract_review(
    file: UploadFile = File(..., description="DOCX或PDF文件"),
    user_prompt: str = Form(..., description="用户提示词"),
    user_id: int = Form(..., description="用户-ID"),
    agent_id: int = Form(..., description="AI-Agent-ID"),
    db: Session = Depends(get_db)
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

#   # 提取文本
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
    
    session_payload = SessionCreate(
        user_id=user_id,
        agent_id=agent_id,
        document_ids="[]",
        title="合同评审——" + file.filename
    )
    session = session_service.create_session(db, **session_payload.model_dump())

    session_id = session.id

    user_msg_payload = ChatMessageCreate(
        session_id=session_id,
        message_index=0,
        role="user",
        type="message",
        content=user_prompt,
        reasoning_content=''
    )


    message_service.create_message(db, **user_msg_payload.model_dump())

    messages = [AliyunModelMsg(role="user", content=combined_prompt)]

    index = 1 # 消息索引从1开始

    def stream():
        reasoning_content = ""
        full_response = ""
        for chunk in reasoning_stream_generator(
            contract_api_key=contract_api_key, 
            app_id=app_id,
            pipeline_ids=pipeline_ids,
            messages=messages,
            debug=True
        ):
            if isinstance(chunk, dict):
                if chunk["type"] == "reasoning":
                    reasoning_content += chunk["delta"]
                elif chunk["type"] == "message":
                    full_response += chunk["delta"]
                yield json.dumps({"type": chunk["type"], "content": chunk["delta"]})
            else:
                print("[未知类型]", chunk)
                yield chunk 

        # ✅ 保存 AI 推理过程（type=reasoning）
        if reasoning_content.strip():
            reasoning_msg = ChatMessageCreate(
                session_id=session_id,
                message_index=index,
                role="assistant",
                type="reasoning",
                content=reasoning_content
            )
            message_service.create_message(db, **reasoning_msg.model_dump())
        
        # ✅ 保存 AI 回复（type=message）
        ai_msg_payload = ChatMessageCreate(
            session_id=session_id,
            message_index=index,
            role="assistant",
            type="message",
            content=full_response
        )
        message_service.create_message(db, **ai_msg_payload.model_dump())

    return StreamingResponse(
        stream(),
        media_type="text/plain"
    )


