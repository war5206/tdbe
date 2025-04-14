from http import HTTPStatus
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
        responses = Application.call(
          api_key=contract_api_key, 
          app_id=app_id,
          messages=messages,
          rag_options={
            "pipeline_ids": pipeline_ids,
          },
          stream=True
        )
      
        reasoning_content = "" # 定义完整思考过程
        answer_content = "" # 定义完整回复

        last_reasoning_response = "" #用于记录上一次完整思考回复
        last_answer_response = "" #用于记录上一次完整回复

        is_answering = False # 判断是否结束思考过程并开始回复

        for chunk in responses:
            # 检查状态码
            if chunk.status_code != HTTPStatus.OK:      
                error_msg = (
                  f"Error: code={chunk.status_code}, "
                  f"msg={chunk.message}, request_id={chunk.request_id}\n"
                )
                if debug:
                    print('[接口错误]', error_msg)
                    # print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
                yield error_msg
                break

            msg = chunk.output.choices[0].message
            if not msg.content and not msg.reasoning_content:
                continue
            
            # 如果当前为思考过程
            if (msg.reasoning_content and not is_answering):
                reasoning_content += msg.reasoning_content  
                delta = reasoning_content[len(last_reasoning_response):] \
                        if reasoning_content.startswith(last_reasoning_response) \
                        else reasoning_content
                last_reasoning_response = reasoning_content  # 更新历史
                if debug:
                    print("[思考]", delta, flush=True)
                yield delta
              
            # 如果当前为回复
            if msg.content:
                if not is_answering:
                  is_answering = True
                  if debug:
                      print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                answer_content += msg.content
                delta = answer_content[len(last_answer_response):] \
                        if answer_content.startswith(last_answer_response) \
                        else answer_content
                last_answer_response = answer_content
                if debug:
                    print("[回复]", delta, flush=True)
                yield delta
                
    except Exception as e:
      error_info = f"[系统异常] {str(e)}\n"
      if debug:
        print(error_info)
      yield error_info