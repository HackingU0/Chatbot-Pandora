import requests
import json
import uuid

url = 'https://ai.fakeopen.com/api/conversation'

headers = {
    "Authorization": "Bearer <Your token>",
    "Content-Type": "application/json"
}

parent_message_id = str(uuid.uuid4())  # 初始parent_message_id

try:
    while True:
        part = input("User：")
        
        if part.lower() in ['exit', 'quit', 'bye']:
            print("Seeya！")
            break
        
        message_id = str(uuid.uuid4())
        
        data = {
            "action": "next",
            "messages": [
                {
                    "id": message_id,
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
            "parent_message_id": parent_message_id,
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
                            pass  # 忽略JSON解析错误
        
        if parts is not None:
            response_part = " ".join(parts)
            print(f"Bot：{response_part}")
            parent_message_id = message_id
        else:
            print("Bot didn't respond. Please try again.")

except KeyboardInterrupt:
    print("\nByebye")
