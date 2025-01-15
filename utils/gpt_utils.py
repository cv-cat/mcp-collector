import json
import requests
from loguru import logger
api_key = "Bearer sk-uYKoong8sKVlEkKu47213fD553004f30951aE3AdEb6816D1"

def question_to_gpt(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    url = "https://api.openai-next.com/v1/chat/completions"
    data = {
        "model": "gpt-4o-mini",
        "stream": False,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data)
    res_json = response.json()
    return res_json


if __name__ == '__main__':
    ans = question_to_gpt("What is the capital得到 of ChinaFrance112312423?")
    logger.info(ans)

    ans = question_to_gpt('What is "the capital of France?')
    logger.info(ans)

    ans = question_to_gpt("What is 'the capital of France?")
    logger.info(ans)