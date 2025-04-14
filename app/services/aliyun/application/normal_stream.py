from http import HTTPStatus
from dashscope import Application

def stream_generator(
  contract_api_key: str, 
  app_id: str,
  pipeline_ids: list[str],
  prompt: str
):
  try:
      responses = Application.call(
        api_key=contract_api_key, 
        app_id=app_id,
        prompt=prompt,
        rag_options={
          "pipeline_ids": pipeline_ids,
        },
        stream=True
      )
    
      last_response = "" #用于记录上一次完整输出
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
              current = chunk.output.text
              print('[接口返回] >>>', current)

              # 计算新增部分
              if current.startswith(last_response):
                  delta = current[len(last_response):]
              else:
                  delta = current  # fallback，某些异常情况
              last_response = current  # 更新历史
              yield delta
  except Exception as e:
    error_info = f"[系统异常] {str(e)}\n"
    print(error_info)
    yield error_info