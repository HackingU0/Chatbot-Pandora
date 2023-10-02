import requests
import json
import uuid

url = 'https://ai.fakeopen.com/api/conversation'

headers = {
    "Authorization": "Bearer 这段换成自己的accesstoken",
    "Content-Type": "application/json"
}

unique_id = str(uuid.uuid4())

try:
    while True:
        part = input("你：")
        
        if part.lower() in ['exit', 'quit', 'bye']:
            print("再见！")
            break
        
        data = {
            "action": "next",
            "messages": [
                {
                    "id": unique_id,
                    "role": "user",
                    "author": {
                        "role": "user",
                    },
                    "content": {
                        "content_type": "text",
                        "parts": [part],
                    },
                }
            ],
            "model": "gpt-4",
            "parent_message_id": unique_id,
        }
        
        parts = None
        
        with requests.post(url, headers=headers, data=json.dumps(data), stream=True) as response:
            if response.encoding is None:
                response.encoding = 'utf-8'
            
            for line in response.iter_lines(decode_unicode=True):
                if line.strip():
                    prefix, content = line.split(': ', 1)
                    if prefix == 'data':
                        try:
                            message = json.loads(content)
                            if 'message' in message and 'content' in message['message'] and 'parts' in message['message']['content']:
                                parts = message['message']['content']['parts']
                        except json.JSONDecodeError:
                            print(f"无法解析内容为 JSON: {content}")
        
        if parts is not None:
            response_part = " ".join(parts)
            print(f"机器人：{response_part}")
        else:
            print("机器人没有回应")

except KeyboardInterrupt:
    print("\n对话已中断。再见！")
