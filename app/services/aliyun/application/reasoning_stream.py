from http import HTTPStatus
import json
from dashscope import Application
from app.schemas.aliyun import AliyunModelMsg

def reasoning_stream_generator(
  contract_api_key: str, 
  app_id: str,
  pipeline_ids: list[str],
  messages: list[AliyunModelMsg],
  debug: bool = False
):
    try:
        messages = [msg.model_dump() for msg in messages]

        if debug:
            print("[思考]", "messages: ", messages)
            print("messages: ", messages)

        responses = Application.call(
          api_key=contract_api_key, 
          app_id=app_id,
          messages=messages,
          rag_options={
            "pipeline_ids": pipeline_ids,
          },
          stream=True,
          has_thoughts = True,
        )

        for chunk in responses:
            # 检查状态码
            if chunk.status_code != HTTPStatus.OK:      
                error_msg = f"Error: code={chunk.status_code}"
                if debug:
                    print('[接口错误]', error_msg)
                    # print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
                yield json.dumps({ "type": "error", "delta": error_msg }) + "\n"
                break
            
            msg = chunk.output
            if not msg.text and not msg.thoughts[2].thought:
                continue
            
            # 如果当前为思考过程
            if (msg.thoughts and msg.thoughts[2].thought):
                delta = msg.thoughts[2].thought
                if debug:
                    print("[思考]", delta, flush=True)
                # yield { "type": "reasoning", "delta": delta }
                yield json.dumps({ "type": "reasoning", "delta": delta }) + "\n"

            # 如果当前为回复    
            if msg.text:  
                delta = msg.text
                if debug:
                    print("[回复]", delta, flush=True)
                # yield { "type": "message", "delta": delta }
                yield json.dumps({ "type": "message", "delta": delta }) + "\n"

            if msg.finish_reason == "stop":             
                if debug:
                    print("[思考]", "[停止]")
                # yield { "type": "stop", "delta": "回复结束" }
                yield json.dumps({ "type": "stop", "delta": "回复结束" }) + "\n"

            if msg.finish_reason == "length":    
                if debug:
                    print("[思考]", "[长度限制]")
                yield json.dumps({ "type": "length", "delta": "长度限制" }) + "\n"

    except Exception as e:
      error_info = f"[系统异常] {str(e)}\n"
      if debug:
        print(error_info)
      yield json.dumps({ "type": "error", "delta": error_info }) + "\n"
