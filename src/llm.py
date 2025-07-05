import os
from openai import OpenAI


class LLMManager:

    def __init__(self, api_key, base_url):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def call_llm(self, model_name, messages, temperature):
        self.completion = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            # enable_thinking 参数开启思考过程，QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
            extra_body={"enable_thinking": True},
            stream=True,
            temperature=temperature
            # stream_options={
            #     "include_usage": True
            # },
        )

    def save(self, path, file_name):
        file_path = f'{path}/{file_name.split(".")[0]}.md'
        reasoning_content = ""  # 完整思考过程
        answer_content = ""  # 完整回复
        is_answering = False  # 是否进入回复阶段
        with open(file_path, 'w', encoding='utf-8') as f:
            for chunk in self.completion:
                if not chunk.choices:
                    print("\nUsage:")
                    print(chunk.usage)
                    continue

                delta = chunk.choices[0].delta

                # 只收集思考内容
                if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                    if not is_answering:
                        print(delta.reasoning_content, end="", flush=True)
                    reasoning_content += delta.reasoning_content

                # 收到content，开始进行回复
                if hasattr(delta, "content") and delta.content:
                    if not is_answering:
                        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                        is_answering = True
                    print(delta.content, end="", flush=True)
                    answer_content += delta.content
                    f.write(delta.content)

