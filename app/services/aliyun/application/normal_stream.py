import json
from http import HTTPStatus
from dashscope import Application
from app.schemas.aliyun import AliyunModelMsg

# 普通非流式输出
def normal_stream_generator(
  contract_api_key: str, 
  app_id: str,
  pipeline_ids: list[str],
  messages: list[AliyunModelMsg],
  debug: bool = False
):
  try:
      messages = [msg.model_dump() for msg in messages]

      responses = Application.call(
        api_key=contract_api_key, 
        app_id=app_id,
        messages=messages,
        rag_options={
          "pipeline_ids": pipeline_ids,
        }
      )
      if responses.status_code != HTTPStatus.OK:
          error_info = f'request_id={responses.request_id}' + '\n' + f'code={responses.status_code}' + '\n' + f'message={responses.message}'
          return { "type": "error", "delta": error_info }
      else:
          print("responses: ", responses.output.text)
          return { "type": "message", "delta": responses.output.text }
  except Exception as e:
    error_info = f"[系统异常] {str(e)}\n"
    if debug:
        print(error_info)
    return { "type": "error", "delta": error_info }