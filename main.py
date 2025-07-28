import requests

url = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"

data = {
    "model": "ai/llama3.2:latest",
    "messages": [
        {
            "role": "system",
            "content": "you are a helpful assistant"
        },
        {
            "role": "user",
            "content": "write me a song about parrots and ice cream"
        }
    ]
}

response = requests.post(url, json=data)
response.raise_for_status()

print(response.json()['choices'][0]['message']['content'])


