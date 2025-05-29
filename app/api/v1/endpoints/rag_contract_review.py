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
from app.services import normal_stream_generator

router = APIRouter(prefix="/contract", tags=["合同评审"])

contract_api_key = "sk-99b3c1698e0244738e48489220ecc183"
app_id = "28c2a03ea6a64ab3a5844f0d82a2bb66"
pipeline_ids = ["ey36n0ka3s"]

# 上传文件进行合同评审（第一次）
@router.post("/review")
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
            file_text = extract_text_from_pdf(tmp_path)
        elif file.filename.endswith(".docx"):
            file_text = extract_text_from_docx(tmp_path)
        elif file.filename.endswith(".doc"):
            raise HTTPException(status_code=400, detail="暂不支持旧版.doc格式")
        else:
            raise HTTPException(status_code=400, detail="无法识别的文件类型")
    finally:
        os.remove(tmp_path)
    
    # 拼接 user_prompt 和file文本
    combined_prompt = f"{file_text}\n{user_prompt}" if file else user_prompt

    print("combined_prompt: ", combined_prompt)
    
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
        content=combined_prompt,
        reasoning_content=''
    )


    message_service.create_message(db, **user_msg_payload.model_dump())

    messages = [AliyunModelMsg(role="user", content=combined_prompt)]

    index = 1 # 消息索引从1开始

    def stream():
        full_response = normal_stream_generator(
            contract_api_key=contract_api_key, 
            app_id=app_id,
            pipeline_ids=pipeline_ids,
            messages=messages,
            debug=True
        )

        delta_text = full_response.get("delta", "")

        # 保存 AI 回复（type=message）
        ai_msg_payload = ChatMessageCreate(
            session_id=session_id,
            message_index=index,
            role="assistant",
            type="message",
            content=delta_text
        )

        message_service.create_message(db, **ai_msg_payload.model_dump())

        full_response['session_id'] = session_id

        return full_response

    return stream()

# 进行合同评审（第二次及以上）
@router.post("/multi-review")
async def multi_review(
    user_prompt: str    = Form(...),
    user_id:       int  = Form(...),
    agent_id:      int  = Form(...),
    session_id:    int  = Form(...),
    db:            Session = Depends(get_db)
):
    # 1) 拿历史 ORM
    records = message_service.get_messages_by_session(db, session_id)

    # 2) 转成 AliyunModelMsg，并安全解析 content
    from json import loads, JSONDecodeError
    msgs: list[AliyunModelMsg] = []
    for rec in records:
        raw = rec.content
        try:
            obj = loads(raw)
            delta = obj.get("delta", raw)
        except JSONDecodeError:
            delta = raw

        role_str = rec.role.value if hasattr(rec.role, "value") else rec.role
        msgs.append(AliyunModelMsg(role=role_str, content=delta))

    # 3) 存用户新消息
    next_idx = len(records) + 1
    user_msg = ChatMessageCreate(
        session_id    = session_id,
        message_index = next_idx,
        role          = "user",
        type          = "message",
        content       = user_prompt
    )
    message_service.create_message(db, **user_msg.model_dump())

    # 4) append 到流里
    msgs.append(AliyunModelMsg(role="user", content=user_prompt))

    # 5) 调用流式生成器
    full = normal_stream_generator(
        contract_api_key=contract_api_key,
        app_id          = app_id,
        pipeline_ids    = pipeline_ids,
        messages        = msgs,
        debug           = True
    )

    # 6) 存 AI 回复
    delta_text = full.get("delta", "")
    ai_msg = ChatMessageCreate(
        session_id    = session_id,
        message_index = next_idx + 1,
        role          = "assistant",
        type          = "message",
        content       = delta_text
    )
    message_service.create_message(db, **ai_msg.model_dump())

    # 7) 带 session_id 返回
    full["session_id"] = session_id
    return full
