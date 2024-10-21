import requests
import json

class OpenRouterService:
    def __init__(self, conf, api_conf):
        self.config = conf
        self.api_conf = api_conf
        self.api_key = api_conf['OPENROUTER_API_KEY']
        self.model = conf['MODEL']
        pass

    def ocr(self, base64_image: str) -> str:
        response = requests.post(
          url="https://openrouter.ai/api/v1/chat/completions",
          headers={
            "Authorization": f"Bearer {self.api_key}",
            "X-Title": f"OCR"
          },
          data=json.dumps({
            "model": self.model, # Optional
            "messages": [
                {
                    "role": "system",
                    "content": self.config['GPT_PROMOTE']['OCR_PROMOTE']
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
          })
        )

        ret = response.json()
        js_ret = json.loads(ret['choices'][0]['message']['content'].strip())

        if js_ret.get("ErrCode", -1) == -1:
            return "0000"
        else :
            return js_ret.get("VerCode", "0000")