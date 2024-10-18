import json
from openai import OpenAIError
from openai import OpenAI

class OpenAIService:
    def __init__(self, config):
        self.config = config
        self.api_key = self.config.get('OPENAI_API_KEY')
        self.proxy_url = self.config.get('PROXY_URL')
        self.proxy_port = self.config.get('PROXY_PORT')
        self.client = OpenAI()
        self.client.base_url = self.config.get('OPENAI_API_URL')

        # 设置 OpenAI API 密钥
        self.client.api_key = self.api_key

        # 设置代理（如果需要）
        #openai.proxy = {
        #    'http': f'http://{self.proxy_url}:{self.proxy_port}',
        #    'https': f'http://{self.proxy_url}:{self.proxy_port}'
        #}

    def process_message_finall(self, message: str, images: list, desc: list = None) -> str:
        try:
            # 将每张图片的 base64 字符串构造成带有 image_url 的字典
            base64_images = []
            index = 0
            for base64_image in images:
                base64_images.append({
                    "type": "text",
                    "text": json.dumps(desc[index])
                    })
                base64_images.append({
                    "type": "image_url", 
                    "image_url": {
                        "url":f"data:image/jpeg;base64,{base64_image}"
                    }
                })
                index += 1

            # 构造请求
            messages=[
                    {
                        "role":"system",
                        "content":self.config['GPT_PROMOTE']['FINALL_PROMOTE']
                    },
                    # 用户消息：包含文本信息和多个图像信息
                    {"role": "user", "content": [
                        *base64_images,  # 传入所有的 base64 编码图片
                        {"type": "text", "text": message}
                    ]}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o",  # 使用 GPT-4 模型
                messages=messages,
                max_tokens=400,
                temperature=0.9
            )

            # 返回 GPT 模型的结果
            return response.choices[0].message.content.strip()

        except OpenAIError as e:
            print(f"Error during OpenAI request: {e}")
            return None

    def process_message_get_vdsl(self, message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # 使用 GPT-4 模型
                messages=[
                    {
                        "role": "system",
                        "content": self.config['GPT_PROMOTE']['CLASSIFICATION']
                    },
                    {"role": "user", "content": message}
                ],
                max_tokens=32,
                temperature=0.9  # 控制生成内容的随机性
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            print(f"Error during OpenAI request: {e}")
            return None
